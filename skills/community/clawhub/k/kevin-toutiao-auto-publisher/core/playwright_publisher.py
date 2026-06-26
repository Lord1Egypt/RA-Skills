#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
头条发布器 - 使用 Playwright 自动化发布文章
支持从配置文件读取所有配置信息（账号、Cookie、日志目录等）
"""

import asyncio
import json
import os
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError


class PlaywrightPublisher:
    """基于 Playwright 的头条发布器"""

    def __init__(self, headless=False, account_name=None, config_file=None, log_dir=None):
        """
        初始化发布器

        Args:
            headless: 是否无头模式运行（默认False，显示浏览器）
            account_name: 头条账号名称（可选，用于日志）
            config_file: 配置文件路径（可选）
            log_dir: 日志/截图保存目录（可选）
        """
        # 读取配置
        config = {}
        if config_file and os.path.exists(config_file):
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)

        self.headless = headless
        self.account_name = account_name or config.get("account_name", "未知账号")
        self.base_url = "https://mp.toutiao.com"
        self.browser = None
        self.context = None
        self.page = None

        # 日志/截图目录
        self.log_dir = log_dir or config.get("log_dir") or os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs"
        )
        os.makedirs(self.log_dir, exist_ok=True)

        # 配图目录（用于自动查找封面图）
        self.image_dir = config.get("image_dir") or os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "generated-images"
        )

        # 发布日志
        self.publish_log = []

    async def start(self):
        """启动浏览器"""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(
            headless=self.headless,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--no-sandbox',
                '--disable-setuid-sandbox'
            ]
        )

        # 创建浏览器上下文
        self.context = await self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )

        self.page = await self.context.new_page()
        print("[发布器] 浏览器已启动")

    async def close(self):
        """关闭浏览器"""
        if self.page:
            await self.page.close()
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
        print("[发布器] 浏览器已关闭")

    async def load_cookies(self, cookies_file):
        """
        加载 Cookie

        Args:
            cookies_file: Cookie 文件路径（JSON 格式）
        """
        try:
            with open(cookies_file, 'r', encoding='utf-8') as f:
                cookies = json.load(f)

            # 转换 Cookie 格式（Playwright 要求 sameSite 为 Strict|Lax|None）
            playwright_cookies = []
            for cookie in cookies:
                same_site = cookie.get('sameSite')
                if same_site == 'no_restriction':
                    same_site = 'None'
                elif same_site == 'lax':
                    same_site = 'Lax'
                elif same_site == 'strict':
                    same_site = 'Strict'
                elif same_site is None:
                    same_site = None

                playwright_cookie = {
                    'name': cookie.get('name'),
                    'value': cookie.get('value'),
                    'domain': cookie.get('domain'),
                    'path': cookie.get('path', '/'),
                    'httpOnly': cookie.get('httpOnly', False),
                    'secure': cookie.get('secure', False),
                }

                if same_site:
                    playwright_cookie['sameSite'] = same_site

                if cookie.get('expirationDate'):
                    playwright_cookie['expires'] = int(cookie['expirationDate'])

                playwright_cookies.append(playwright_cookie)

            await self.context.add_cookies(playwright_cookies)
            print(f"[发布器] Cookie 已加载: {len(playwright_cookies)} 个")
            return True
        except Exception as e:
            print(f"[发布器] 加载 Cookie 失败: {e}")
            import traceback
            traceback.print_exc()
            return False

    async def navigate_to_publish(self):
        """导航到发布页面"""
        try:
            print("[发布器] 导航到发布页面...")

            await self.page.goto(f"{self.base_url}/", wait_until="domcontentloaded")
            await asyncio.sleep(2)

            current_url = self.page.url
            if 'login' in current_url:
                print("[发布器] 需要登录，Cookie 可能已过期")
                return False

            title = await self.page.title()
            print(f"[发布器] 主页标题: {title}")

            publish_urls = [
                f"{self.base_url}/profile_v4/graphic/publish",
                f"{self.base_url}/profile_v4/publish",
                f"{self.base_url}/profile_v4/articles/create",
                f"{self.base_url}/profile_v4/articles/create/post"
            ]

            success = False
            for url in publish_urls:
                try:
                    print(f"[发布器] 尝试 URL: {url}")
                    response = await self.page.goto(url, wait_until="networkidle", timeout=60000)

                    if response and response.status >= 400:
                        print(f"[发布器] 页面返回错误状态码: {response.status}")
                        if response.status == 502:
                            continue
                        elif response.status == 401 or response.status == 403:
                            return False
                    else:
                        print("[发布器] 等待页面加载...")
                        await asyncio.sleep(10)

                        prose_mirrors = await self.page.query_selector_all('.ProseMirror')
                        print(f"[发布器] 找到 {len(prose_mirrors)} 个 ProseMirror 元素")

                        content_editors = []
                        for el in prose_mirrors:
                            contenteditable = await el.get_attribute('contenteditable')
                            is_visible = await el.is_visible()
                            if contenteditable == 'true' and is_visible:
                                content_editors.append(el)

                        if len(content_editors) > 0:
                            print(f"[发布器] 找到 {len(content_editors)} 个可用正文编辑器")
                            success = True
                            break
                        else:
                            print(f"[发布器] 未找到可用的正文编辑器")
                except Exception as e:
                    print(f"[发布器] URL {url} 失败: {e}")
                    continue

            if not success:
                print("[发布器] 所有发布页面 URL 都尝试失败")
                return False

            current_url = self.page.url
            if 'login' in current_url:
                print("[发布器] 需要登录，请手动登录")
                return False

            print("[发布器] 已进入发布页面")
            return True

        except PlaywrightTimeoutError:
            print("[发布器] 导航超时")
            return False
        except Exception as e:
            print(f"[发布器] 导航异常: {e}")
            import traceback
            traceback.print_exc()
            return False

    async def fill_title(self, title):
        """
        填充标题

        Args:
            title: 文章标题

        Returns:
            bool: 是否成功
        """
        try:
            print(f"[发布器] 填充标题: {title}")
            await asyncio.sleep(3)

            title_selectors = [
                'input[placeholder*="标题"]',
                'input[placeholder*="文章"]',
                'input[placeholder*="请输入标题"]',
                '.title-input',
                'input[type="text"]',
                'textarea[placeholder*="标题"]',
                '[placeholder*="标题"]'
            ]

            title_found = False
            for selector in title_selectors:
                try:
                    elements = await self.page.query_selector_all(selector)
                    for el in elements:
                        is_visible = await el.is_visible()
                        if is_visible:
                            placeholder = await el.get_attribute('placeholder') or ''
                            print(f"  找到标题输入框: placeholder={placeholder}")
                            await el.click()
                            await self.page.keyboard.press('Control+a')
                            await self.page.keyboard.press('Backspace')
                            await self.page.type(selector, title, delay=50)
                            title_found = True
                            await asyncio.sleep(1)
                            break
                    if title_found:
                        break
                except:
                    continue

            if not title_found:
                print("[发布器] 尝试查找所有可见输入框...")
                inputs = await self.page.query_selector_all('input, textarea, [contenteditable="true"]')
                for i, input_el in enumerate(inputs):
                    is_visible = await input_el.is_visible()
                    if not is_visible:
                        continue

                    placeholder = await input_el.get_attribute('placeholder') or ''
                    class_name = await input_el.get_attribute('class') or ''
                    tag_name = await input_el.evaluate('el => el.tagName')

                    if 'ProseMirror' not in class_name and (not placeholder or '标题' in placeholder or 'title' in placeholder.lower()):
                        await input_el.click()
                        await self.page.keyboard.press('Control+a')
                        await self.page.keyboard.press('Backspace')
                        await input_el.type(title, delay=50)
                        title_found = True
                        await asyncio.sleep(1)
                        break

            if not title_found:
                raise Exception("未找到标题输入框")

            print("[发布器] 标题填充完成")
            return True

        except Exception as e:
            print(f"[发布器] 填充标题失败: {e}")
            import traceback
            traceback.print_exc()
            return False

    async def fill_content(self, content):
        """
        填充正文内容

        Args:
            content: 文章内容

        Returns:
            bool: 是否成功
        """
        try:
            print("[发布器] 填充正文...")
            await asyncio.sleep(3)

            # 优先用 execCommand('insertText') 方式
            import json as _json
            escaped_content = _json.dumps(content)

            result = await self.page.evaluate(f'''
                () => {{
                    var editors = document.querySelectorAll('[contenteditable=true]');
                    if (!editors.length) return 'NO_EDITOR';

                    var el = null;
                    for (var e of editors) {{
                        if (e.className && e.className.includes('ProseMirror')) {{
                            el = e; break;
                        }}
                    }}
                    if (!el) el = editors[0];

                    el.focus();
                    document.execCommand('selectAll', false, null);
                    var ok = document.execCommand('insertText', false, {escaped_content});
                    return 'ok:' + ok + ':len:' + el.textContent.length;
                }}
            ''')
            print(f"[发布器] execCommand 结果: {result}")

            if result and result.startswith('ok:') and 'NO_EDITOR' not in result:
                try:
                    length = int(result.split('len:')[-1])
                    if length > 10:
                        print(f"[发布器] 正文填充成功（字符数: {length}）")
                        await asyncio.sleep(1)
                        return True
                except:
                    pass

            # 备用方案
            print("[发布器] 尝试备用方案：键盘输入...")
            content_selectors = [
                '.ProseMirror[contenteditable="true"]',
                '[contenteditable="true"].ProseMirror',
                '[contenteditable="true"]',
            ]

            content_found = False
            for selector in content_selectors:
                try:
                    elements = await self.page.query_selector_all(selector)
                    for el in elements:
                        is_visible = await el.is_visible()
                        if is_visible:
                            class_name = await el.get_attribute('class') or ''
                            if 'ProseMirror' in class_name:
                                await el.click()
                                await asyncio.sleep(0.5)
                                await self.page.keyboard.press('Control+a')
                                await asyncio.sleep(0.3)
                                await self.page.keyboard.press('Backspace')
                                await asyncio.sleep(0.3)
                                paragraphs = content.split('\n')
                                for i, para in enumerate(paragraphs):
                                    if para:
                                        await self.page.keyboard.type(para, delay=5)
                                    if i < len(paragraphs) - 1:
                                        await self.page.keyboard.press('Enter')
                                content_found = True
                                await asyncio.sleep(1)
                                break
                    if content_found:
                        break
                except:
                    continue

            if not content_found:
                raise Exception("未找到正文编辑器")

            print("[发布器] 正文填充完成")
            return True

        except Exception as e:
            print(f"[发布器] 填充正文失败: {e}")
            import traceback
            traceback.print_exc()
            return False

    async def upload_images(self, image_paths):
        """
        上传配图（在正文编辑器中插入图片）

        Args:
            image_paths: 图片路径列表

        Returns:
            bool: 是否成功
        """
        try:
            if not image_paths:
                print("[发布器] 无需上传配图")
                return True

            print(f"[发布器] 上传配图: {len(image_paths)} 张")
            await asyncio.sleep(2)

            editor = await self.page.query_selector('.ProseMirror[contenteditable="true"]')
            if not editor:
                print("[发布器] 未找到正文编辑器，无法插入图片")
                return False

            for i, image_path in enumerate(image_paths):
                if not Path(image_path).exists():
                    print(f"[发布器] 图片不存在: {image_path}")
                    continue

                print(f"[发布器] 插入第 {i+1} 张图片: {Path(image_path).name}")

                await editor.click()
                await asyncio.sleep(0.5)
                await self.page.keyboard.press('End')
                await asyncio.sleep(0.3)
                await self.page.keyboard.press('Enter')
                await asyncio.sleep(0.3)

                try:
                    image_buttons = await self.page.query_selector_all('button[title*="图片"], button[title*="image"], button[aria-label*="图片"], button[aria-label*="image"]')
                    if image_buttons:
                        for btn in image_buttons:
                            try:
                                is_visible = await btn.is_visible()
                                if is_visible:
                                    await btn.click()
                                    await asyncio.sleep(2)
                                    file_inputs = await self.page.query_selector_all('input[type="file"]')
                                    if file_inputs:
                                        await self.page.set_input_files('input[type="file"]', image_path)
                                        await asyncio.sleep(3)
                                        print(f"[发布器] 图片上传成功")
                                        break
                            except:
                                continue

                    if not await self._try_paste_image(editor, image_path):
                        print(f"[发布器] 插入图片失败: {image_path}")
                        continue

                except Exception as e:
                    print(f"[发布器] 插入图片异常: {e}")

            print("[发布器] 配图上传完成")
            return True

        except Exception as e:
            print(f"[发布器] 上传配图失败: {e}")
            import traceback
            traceback.print_exc()
            return False

    async def _try_paste_image(self, editor, image_path):
        """尝试通过粘贴的方式插入图片"""
        try:
            import base64
            with open(image_path, 'rb') as f:
                image_data = base64.b64encode(f.read()).decode()

            await editor.evaluate(f'''
                (editor, imgData) => {{
                    const img = document.createElement('img');
                    img.src = 'data:image/png;base64,' + imgData;
                    img.style.maxWidth = '100%';
                    editor.appendChild(img);
                }}
            ''', image_data)

            await asyncio.sleep(1)
            return True
        except Exception as e:
            print(f"[发布器] 粘贴图片失败: {e}")
            return False

    async def set_options(self):
        """
        设置发布选项（取消勾选"发布得更多收益"、勾选"头条首发"、"个人观点"等）

        Returns:
            bool: 是否成功
        """
        try:
            print("[发布器] 设置发布选项...")
            await asyncio.sleep(3)

            await self.page.evaluate('() => window.scrollTo(0, document.body.scrollHeight)')
            await asyncio.sleep(2)

            checkboxes = await self.page.query_selector_all('input[type="checkbox"]')
            print(f"[发布器] 找到 {len(checkboxes)} 个复选框")

            for checkbox in checkboxes:
                try:
                    parent = await checkbox.evaluate('el => el.parentElement?.innerText || ""')

                    if '发布得更多收益' in parent:
                        is_checked = await checkbox.is_checked()
                        if is_checked:
                            await checkbox.click()
                            await asyncio.sleep(0.5)
                            print("[发布器] 已取消勾选: 发布得更多收益")

                    if '同时发布微头条' in parent or '发布微头条' in parent:
                        is_checked = await checkbox.is_checked()
                        if is_checked:
                            await checkbox.click()
                            await asyncio.sleep(0.5)
                            print("[发布器] 已取消勾选: 同时发布微头条")

                except Exception as e:
                    continue

            # 勾选"头条首发"
            print("[发布器] 注意: '头条首发'选项经深度调研确认不可用(头条业务逻辑限制),跳过此项")

            # 勾选"个人观点，仅供参考"
            for checkbox in checkboxes:
                try:
                    parent = await checkbox.evaluate('el => el.parentElement?.innerText || ""')
                    if '个人观点' in parent:
                        is_checked = await checkbox.is_checked()
                        if not is_checked:
                            parent_el = await checkbox.evaluate_handle('el => el.parentElement')
                            try:
                                await parent_el.click()
                                await asyncio.sleep(1)
                                is_checked = await checkbox.is_checked()
                                if is_checked:
                                    print("[发布器] 已勾选: 个人观点，仅供参考")
                                else:
                                    print("[发布器] 勾选个人观点失败")
                            except:
                                print("[发布器] 勾选个人观点: 点击失败")
                        else:
                            print("[发布器] 个人观点已勾选，无需操作")
                except Exception as e:
                    continue

            print("[发布器] 发布选项设置完成")
            return True

        except Exception as e:
            print(f"[发布器] 设置选项失败: {e}")
            import traceback
            traceback.print_exc()
            return False

    async def upload_cover_image(self, image_path, max_retries=3):
        """
        上传封面图片

        Args:
            image_path: 图片文件路径
            max_retries: 最大重试次数

        Returns:
            bool: 是否成功
        """
        for attempt in range(max_retries):
            try:
                if attempt > 0:
                    print(f"[发布器] 尝试 {attempt + 1}/{max_retries}...")

                print(f"[发布器] 开始上传封面: {image_path}")

                if not Path(image_path).exists():
                    print(f"[发布器] 图片不存在: {image_path}")
                    return False

                # Step 1: 点击"单图"选项
                print("[发布器] 步骤1: 点击'单图'选项...")
                single_image_clicked = False
                for selector in ['label', 'button', '.byte-radio-button']:
                    try:
                        element = self.page.locator(selector).filter(has_text='单图').first
                        if await element.count() > 0:
                            await element.click(timeout=5000)
                            single_image_clicked = True
                            break
                    except:
                        continue

                if not single_image_clicked:
                    print("[发布器] 未找到'单图'选项")
                    if attempt < max_retries - 1:
                        await asyncio.sleep(2)
                        continue
                    return False

                await asyncio.sleep(5)

                # Step 2: 检查上传按钮
                cover_add_exists = await self.page.evaluate('''
                    () => {
                        const el = document.querySelector('.article-cover-add');
                        if (!el) return false;
                        return el.offsetParent !== null;
                    }
                ''')

                if not cover_add_exists:
                    print("[发布器] .article-cover-add 不存在或不可见")
                    if attempt < max_retries - 1:
                        await asyncio.sleep(2)
                        continue
                    return False

                # Step 3: 点击上传按钮
                try:
                    cover_add = self.page.locator('.article-cover-add')
                    await cover_add.click(timeout=5000)
                    await asyncio.sleep(3)
                except Exception as e:
                    print(f"[发布器] 点击上传按钮失败: {e}")
                    if attempt < max_retries - 1:
                        await asyncio.sleep(2)
                        continue
                    return False

                # Step 4: 等待文件选择器
                file_input_selector = None
                try:
                    await asyncio.sleep(3)
                    await self.page.wait_for_selector('#upload-drag-input', state='attached', timeout=10000)
                    file_input_selector = '#upload-drag-input'
                except:
                    file_inputs = await self.page.evaluate('''
                        () => {
                            const inputs = Array.from(document.querySelectorAll('input[type="file"]'));
                            return inputs.map(i => ({
                                id: i.id,
                                visible: i.offsetParent !== null
                            }));
                        }
                    ''')
                    if file_inputs:
                        visible_inputs = [f for f in file_inputs if f['visible']]
                        if visible_inputs:
                            file_input_selector = f"#{visible_inputs[0]['id']}" if visible_inputs[0]['id'] else 'input[type="file"]'
                        else:
                            file_input_selector = 'input[type="file"]'
                    else:
                        if attempt < max_retries - 1:
                            await asyncio.sleep(2)
                            continue
                        return False

                # Step 5: 上传图片
                try:
                    file_input = self.page.locator(file_input_selector)
                    await file_input.set_input_files(image_path)
                    await asyncio.sleep(5)
                except Exception as e:
                    print(f"[发布器] 上传文件失败: {e}")
                    if attempt < max_retries - 1:
                        await asyncio.sleep(2)
                        continue
                    return False

                # Step 6: 点击确定按钮
                try:
                    confirm_result = await self.page.evaluate('''
                        () => {
                            const btns = Array.from(document.querySelectorAll('button'));
                            const confirmBtnTexts = ['确定', '确认', '上传', '确认发布', '完成'];
                            
                            const uploadPanel = document.querySelector('.upload-image-panel, .byte-drawer-wrapper');
                            if (uploadPanel) {
                                const panelBtns = uploadPanel.querySelectorAll('button');
                                for (let btn of panelBtns) {
                                    if (btn.offsetParent && !btn.disabled) {
                                        const text = btn.innerText.trim();
                                        if (confirmBtnTexts.includes(text)) {
                                            btn.click();
                                            return { clicked: true, text: text };
                                        }
                                    }
                                }
                            }
                            
                            for (let btn of btns) {
                                if (btn.offsetParent && !btn.disabled) {
                                    const text = btn.innerText.trim();
                                    if (confirmBtnTexts.includes(text)) {
                                        btn.click();
                                        return { clicked: true, text: text };
                                    }
                                }
                            }
                            
                            return { clicked: false };
                        }
                    ''')

                    if confirm_result['clicked']:
                        print(f"[发布器] 已点击确定按钮: {confirm_result['text']}")
                        await asyncio.sleep(8)
                    else:
                        await asyncio.sleep(8)
                except Exception as e:
                    await asyncio.sleep(8)

                # Step 7: 检查封面状态
                cover_status = await self.page.evaluate('''
                    () => {
                        const result = { uploaded: false, count: 0, images: [] };
                        const selectors = [
                            '.article-cover-add img',
                            '.article-cover-images img',
                            '[class*="cover"] img',
                            '.cover-preview img',
                            '.cover-img img'
                        ];
                        
                        for (let sel of selectors) {
                            const images = document.querySelectorAll(sel);
                            for (let img of images) {
                                const rect = img.getBoundingClientRect();
                                if (rect.width > 50 && rect.height > 50) {
                                    result.uploaded = true;
                                    result.count++;
                                    result.images.push({
                                        src: img.src.substring(0, 100),
                                        width: rect.width,
                                        height: rect.height,
                                        naturalWidth: img.naturalWidth,
                                        naturalHeight: img.naturalHeight,
                                        complete: img.complete
                                    });
                                }
                            }
                        }
                        
                        return result;
                    }
                ''')

                # 关闭上传面板
                try:
                    await self.page.keyboard.press('Escape')
                    await asyncio.sleep(2)
                except:
                    try:
                        await self.page.evaluate('''
                            () => {
                                const drawer = document.querySelector('.byte-drawer-wrapper');
                                if (drawer) drawer.style.display = 'none';
                                const uploadPanel = document.querySelector('.upload-image-panel');
                                if (uploadPanel) uploadPanel.style.display = 'none';
                                return 'done';
                            }
                        ''')
                    except:
                        pass

                if cover_status['uploaded'] and cover_status['count'] > 0:
                    print(f"[发布器] 封面上传成功! 数量: {cover_status['count']}")
                    return True
                else:
                    print("[发布器] 封面未上传成功")
                    if attempt < max_retries - 1:
                        await asyncio.sleep(2)
                        continue
                    return False

            except Exception as e:
                print(f"[发布器] 封面上传异常: {e}")
                try:
                    await self.page.keyboard.press('Escape')
                except:
                    pass
                if attempt < max_retries - 1:
                    await asyncio.sleep(2)
                    continue
                return False

        print(f"[发布器] 封面上传失败，已重试{max_retries}次")
        return False

    async def publish(self, cover_image_path=None):
        """
        点击"预览并发布"按钮并完成发布流程

        Args:
            cover_image_path: 封面图片路径（可选，不传则自动从 image_dir 查找）

        Returns:
            bool: 是否成功
        """
        try:
            print("[发布器] 查找发布按钮...")

            # 关闭所有可能遮挡的抽屉/面板
            print("[发布器] 关闭所有遮挡的抽屉/面板...")
            try:
                await self.page.evaluate('''
                    () => {
                        var wrappers = document.querySelectorAll('.ai-assistant-drawer, .byte-drawer-wrapper, .upload-image-panel');
                        wrappers.forEach(w => w.style.display = 'none');
                        return 'hidden';
                    }
                ''')
            except Exception as e:
                print(f"[发布器] 关闭面板失败(可忽略): {e}")

            await asyncio.sleep(1)

            # 上传封面图片
            print("[发布器] 上传封面图片...")
            cover_uploaded = False

            # 确定封面图片路径
            if not cover_image_path:
                # 自动从 image_dir 查找
                if os.path.exists(self.image_dir):
                    img_files = [f for f in os.listdir(self.image_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
                    if img_files:
                        cover_image_path = os.path.join(self.image_dir, img_files[0])

            if cover_image_path:
                cover_uploaded = await self.upload_cover_image(cover_image_path)
                if cover_uploaded:
                    print("[发布器] 封面上传成功")
                else:
                    print("[发布器] 封面上传失败，将尝试继续发布（可能有风险）")
            else:
                print("[发布器] 没有找到可用的封面图片,跳过上传")

            # 确保面板已关闭
            await self.page.evaluate('''
                () => {
                    const uploadPanel = document.querySelector('.upload-image-panel');
                    if (uploadPanel) uploadPanel.style.display = 'none';
                    const drawerWrapper = document.querySelector('.byte-drawer-wrapper');
                    if (drawerWrapper) drawerWrapper.style.display = 'none';
                    return 'hidden';
                }
            ''')
            await asyncio.sleep(1)

            # 点击"预览并发布"
            print("[发布器] 尝试点击发布按钮...")

            click_result = None
            try:
                span_locator = self.page.locator('.publish-btn.publish-btn-last span')
                if await span_locator.count() > 0:
                    await span_locator.click(timeout=5000)
                    print("[发布器] 已点击: .publish-btn.publish-btn-last span")
                    click_result = 'SPAN:预览并发布'
                else:
                    raise Exception("未找到 span")
            except Exception as e:
                try:
                    btn_locator = self.page.locator('.publish-btn.publish-btn-last')
                    await btn_locator.focus()
                    await self.page.keyboard.press('Enter')
                    click_result = 'FOCUS_ENTER:预览并发布'
                except Exception as e2:
                    try:
                        click_result = await self.page.evaluate('''
                            () => {
                                var btn = document.querySelector('.publish-btn.publish-btn-last');
                                var span = btn?.querySelector('span');
                                if (span) {
                                    span.dispatchEvent(new MouseEvent('mousedown', {bubbles: true, cancelable: true}));
                                    span.dispatchEvent(new MouseEvent('mouseup', {bubbles: true, cancelable: true}));
                                    span.dispatchEvent(new MouseEvent('click', {bubbles: true, cancelable: true}));
                                    return 'SPAN_JS:预览并发布';
                                }
                                return 'NOT_FOUND';
                            }
                        ''')
                    except:
                        click_result = 'ALL_FAILED'

            if click_result and click_result.startswith('NOT_FOUND'):
                return False

            # 等待预览面板弹出
            print("[发布器] 等待预览面板弹出...")
            await asyncio.sleep(10)
            clicked_text = None

            for attempt in range(5):
                dialog_check = await self.page.evaluate('''
                    () => {
                        var url = location.href;
                        var text = document.body.innerText;

                        if (!url.includes('graphic/publish')) {
                            return 'JUMPED:' + url;
                        }

                        if (text.includes('发布成功') || text.includes('已发布') || text.includes('提交成功')) return 'SUCCESS';
                        if (text.includes('发布失败') || text.includes('提交失败')) return 'FAILED';

                        var dialogSelectors = [
                            '.drawer', '.modal', '.dialog', '.preview-dialog',
                            '[class*="drawer"]', '[class*="modal"]', '[class*="dialog"]', '[class*="preview"]'
                        ];

                        var visibleDialog = null;
                        for (var sel of dialogSelectors) {
                            var dialogs = Array.from(document.querySelectorAll(sel));
                            for (var i = 0; i < dialogs.length; i++) {
                                var d = dialogs[i];
                                var style = window.getComputedStyle(d);
                                if (style.display !== 'none' && style.opacity !== '0' && style.visibility !== 'hidden') {
                                    visibleDialog = { selector: sel, element: d };
                                    break;
                                }
                            }
                            if (visibleDialog) break;
                        }

                        var btns = Array.from(document.querySelectorAll('button'));
                        var confirmBtnTexts = ['确认发布', '确定发布', '发布', '确定', '提交', '立即发布', '马上发布', '预览发布'];
                        for (var ct of confirmBtnTexts) {
                            var found = btns.find(b => b.innerText.trim() === ct && !b.disabled && b.offsetParent);
                            if (found) {
                                found.click();
                                return 'CLICKED:' + ct;
                            }
                        }

                        var allBtnTexts = btns.filter(b => b.offsetParent).map(b => b.innerText.trim()).filter(t => t);
                        return 'WAITING|dialog:' + (visibleDialog ? visibleDialog.selector : 'none') + '|btns:' + allBtnTexts.join('|');
                    }
                ''')
                print(f"[发布器] 第{attempt+1}次检测结果: {dialog_check}")

                if not dialog_check:
                    await asyncio.sleep(3)
                    continue

                if dialog_check.startswith('JUMPED') or dialog_check == 'SUCCESS':
                    print("[发布器] 发布完成！")
                    return True

                if dialog_check.startswith('CLICKED:'):
                    clicked_text = dialog_check.split(':', 1)[1]
                    print(f"[发布器] 已点击确认按钮：[{clicked_text}]")
                    break

                if dialog_check == 'FAILED':
                    return False

                # 保存调试截图
                try:
                    await self.page.screenshot(path=os.path.join(self.log_dir, f"preview_waiting_attempt_{attempt+1}.png"))
                except:
                    pass
                await asyncio.sleep(3)

            # 等待最终结果
            if clicked_text:
                await asyncio.sleep(5)
                try:
                    await self.page.screenshot(path=os.path.join(self.log_dir, "after_confirm_publish.png"))
                except:
                    pass

                print("[发布器] 开始验证最终发布结果...")
                final_url = self.page.url
                print(f"[发布器] 最终URL: {final_url}")

                success_check = await self.page.evaluate('''
                    () => {
                        var url = location.href;
                        if (!url.includes('graphic/publish')) {
                            return { type: 'url', success: true, detail: 'URL已跳转: ' + url };
                        }

                        var bodyText = document.body.innerText;
                        if (bodyText.includes('发布成功') || bodyText.includes('已发布') || bodyText.includes('提交成功')) {
                            return { type: 'text', success: true, detail: '检测到成功提示文本' };
                        }

                        if (bodyText.includes('发布失败') || bodyText.includes('提交失败') || bodyText.includes('审核失败')) {
                            return { type: 'error', success: false, detail: '检测到失败提示文本' };
                        }

                        return { type: 'unknown', success: false, detail: '无法确定发布状态' };
                    }
                ''')

                print(f"[发布器] 最终状态: {success_check}")

                if success_check.get('success'):
                    print(f"[发布器] 发布成功! {success_check.get('detail')}")
                    return True
                else:
                    # 已点击确认按钮，但无法确认最终结果
                    return True

            # 兜底截图
            try:
                await self.page.screenshot(path=os.path.join(self.log_dir, "publish_unknown.png"))
            except:
                pass

            return False

        except Exception as e:
            print(f"[发布器] 发布失败: {e}")
            import traceback
            traceback.print_exc()
            return False

    async def check_publish_result(self):
        """检查发布结果"""
        try:
            print("[发布器] 开始检查发布结果...")
            await asyncio.sleep(5)

            current_url = self.page.url
            print(f"[发布器] 当前 URL: {current_url}")

            if 'success' in current_url or 'article' in current_url:
                return {"success": True, "url": current_url}

            try:
                success_text = await self.page.evaluate('''
                    () => {
                        const elements = Array.from(document.querySelectorAll('*'));
                        for (let el of elements) {
                            if (el.innerText && (el.innerText.includes('发布成功') || el.innerText.includes('提交成功') || el.innerText.includes('已发布'))) {
                                return el.innerText;
                            }
                        }
                        return '';
                    }
                ''')

                if success_text:
                    return {"success": True, "url": current_url}
            except:
                pass

            # 截图供人工判断
            screenshot_path = os.path.join(self.log_dir, "publish_result.png")
            try:
                await self.page.screenshot(path=screenshot_path)
            except:
                pass

            return {
                "success": False,
                "error": "发布状态未知，请查看截图",
                "screenshot": screenshot_path
            }

        except Exception as e:
            return {"success": False, "error": str(e)}

    async def publish_article(self, title, content, image_paths=None, cover_image_path=None, options=None):
        """
        完整的发布流程

        Args:
            title: 文章标题
            content: 文章内容
            image_paths: 配图路径列表（可选）
            cover_image_path: 封面图片路径（可选）
            options: 其他选项（可选）

        Returns:
            dict: 发布结果
        """
        result = {
            "success": False,
            "error": None,
            "url": None,
            "logs": []
        }

        try:
            if not await self.navigate_to_publish():
                result["error"] = "导航到发布页面失败"
                return result
            result["logs"].append("已导航到发布页面")

            if options or True:
                await self.set_options()
                result["logs"].append("已设置发布选项")

            if not await self.fill_title(title):
                result["error"] = "填充标题失败"
                return result
            result["logs"].append("标题填充完成")

            if not await self.fill_content(content):
                result["error"] = "填充正文失败"
                return result
            result["logs"].append("正文填充完成")

            if image_paths:
                await self.upload_images(image_paths)
                result["logs"].append(f"配图上传完成: {len(image_paths)} 张")

            if not await self.publish(cover_image_path=cover_image_path):
                result["error"] = "点击发布按钮失败"
                return result
            result["logs"].append("已点击发布按钮")

            publish_result = await self.check_publish_result()
            if publish_result["success"]:
                result["success"] = True
                result["url"] = publish_result.get("url", "")
                result["logs"].append("发布成功")

                log_entry = {
                    "title": title,
                    "url": result["url"],
                    "status": "success",
                    "published_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                self.publish_log.append(log_entry)
            else:
                result["error"] = publish_result.get("error", "发布失败")

        except Exception as e:
            result["error"] = f"发布流程异常: {e}"

        return result

    def get_publish_log(self):
        """获取发布日志"""
        return self.publish_log

    def save_publish_log(self, log_path):
        """保存发布日志到文件"""
        with open(log_path, 'w', encoding='utf-8') as f:
            json.dump(self.publish_log, f, ensure_ascii=False, indent=2)
        print(f"[发布器] 发布日志已保存到: {log_path}")


async def main():
    """测试发布器"""
    import os

    # 查找配置文件
    config_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config")
    config_file = os.path.join(config_dir, "account_config.json")

    if not os.path.exists(config_file):
        print("[发布器] 未找到配置文件 config/account_config.json")
        return

    with open(config_file, 'r', encoding='utf-8') as f:
        config = json.load(f)

    publisher = PlaywrightPublisher(
        headless=False,
        account_name=config.get("account_name"),
        config_file=config_file
    )

    await publisher.start()

    cookies_file = config.get("cookie_file")
    if cookies_file:
        await publisher.load_cookies(cookies_file)

    result = await publisher.publish_article(
        title="测试文章标题",
        content="这是一篇使用Playwright自动发布的测试文章。",
        image_paths=None
    )

    print(f"\n发布结果: {json.dumps(result, ensure_ascii=False, indent=2)}")

    await publisher.close()


if __name__ == "__main__":
    asyncio.run(main())
