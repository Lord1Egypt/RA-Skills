#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Multi-AI Search Analysis - 主执行脚本（优化版）
版本：v2.0
功能：并行询问多家 AI，自动汇总生成对比报告
优化：超时重试、进度提示、错误处理、选择器优化
"""

import asyncio
import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Tuple

# Windows 中文环境设置 UTF-8
if sys.platform == 'win32':
    os.system('chcp 65001 > nul')

from colorama import init, Fore, Style

# 导入 tqdm 进度条
try:
    from tqdm import tqdm
    HAS_TQDM = True
except ImportError:
    HAS_TQDM = False
    tqdm = None

# 初始化 colorama
init(autoreset=True)

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from playwright.async_api import async_playwright, Browser, BrowserContext, Page, TimeoutError as PlaywrightTimeout
except ImportError:
    print(f"{Fore.RED}错误：缺少 playwright 模块{Style.RESET_ALL}")
    print(f"请运行：pip install playwright && playwright install msedge")
    sys.exit(1)


class AIPlatform:
    """AI 平台配置"""
    
    def __init__(self, config: dict):
        self.name = config['name']
        self.url = config['url']
        self.login_method = config.get('loginMethod', 'unknown')
        self.avg_response_time = config.get('avgResponseTime', 15)
        self.timeout = config.get('timeout', 120)
        self.selectors = config.get('selectors', {})
        self.features = config.get('features', {})
        
    def __str__(self):
        return f"{self.name} ({self.url})"


class ResponseStatus:
    """响应状态枚举"""
    PENDING = "等待中"
    SENDING = "发送中"
    WAITING = "等待响应"
    COMPLETED = "已完成"
    TIMEOUT = "超时"
    ERROR = "错误"


class MultiAISearch:
    """多 AI 搜索分析器（优化版）"""
    
    def __init__(self, config_path: str = None):
        self.config_path = config_path or self._default_config_path()
        self.config = self._load_config()
        self.platforms = [AIPlatform(p) for p in self.config['platforms']]
        self.browser: Optional[BrowserContext] = None
        self.results: List[Dict] = []
        self.status: Dict[str, str] = {}  # 平台响应状态
        self.retry_count: Dict[str, int] = {}  # 重试次数
        
    def _default_config_path(self) -> str:
        """默认配置文件路径"""
        return str(Path(__file__).parent.parent / 'config' / 'ai-platforms.json')
    
    def _load_config(self) -> dict:
        """加载配置文件"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"{Fore.RED}错误：配置文件不存在 {self.config_path}{Style.RESET_ALL}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"{Fore.RED}错误：配置文件格式错误 {e}{Style.RESET_ALL}")
            sys.exit(1)
    
    def _get_selectors(self, platform: AIPlatform) -> Dict[str, str]:
        """获取平台选择器（带回退机制）"""
        selectors = platform.selectors
        
        # 通用回退选择器
        fallback_selectors = {
            'input': ['textarea', 'input[type="text"]', '[contenteditable="true"]', 'div[role="textbox"]'],
            'send': ['button', '[aria-label*="发送"]', '[aria-label*="Send"]', '[type="submit"]'],
            'response': ['article', 'div[class*="response"]', 'div[class*="answer"]', '.markdown-body', '[class*="message"]'],
        }
        
        return selectors
    
    async def initialize_browser(self, headless: bool = False):
        """初始化浏览器（使用 Edge）"""
        print(f"{Fore.CYAN}正在初始化浏览器...{Style.RESET_ALL}")
        
        playwright = await async_playwright().start()
        
        # 使用用户数据目录保存登录状态
        user_data_dir = str(Path(__file__).parent.parent / 'browser-profile')
        Path(user_data_dir).mkdir(exist_ok=True)
        
        try:
            self.browser = await playwright.chromium.launch_persistent_context(
                user_data_dir=user_data_dir,
                headless=headless,
                channel="msedge",  # 使用 Edge 浏览器
                args=[
                    '--disable-gpu',
                    '--no-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-blink-features=AutomationControlled',
                    '--no-first-run',
                    '--disable-features=TranslateUI'
                ]
            )
            print(f"{Fore.GREEN}[OK] 浏览器初始化完成{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[X] 浏览器初始化失败：{e}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}提示：请确保已安装 Edge 浏览器和 Playwright{Style.RESET_ALL}")
            print(f"       运行：playwright install msedge")
            raise
    
    async def ensure_new_chat(self, page: Page, platform: AIPlatform):
        """
        确保新建会话（上下文干净）- 增强版
        
        策略：
        1. 优先查找并点击"新建会话"按钮
        2. 检查输入框是否存在且为空
        3. 检查是否有欢迎语（表示新会话）
        """
        try:
            # 等待页面加载
            await page.wait_for_load_state('domcontentloaded', timeout=10000)
            await asyncio.sleep(2)
            
            # 策略 1：尝试查找"新建会话"按钮并点击
            new_chat_selectors = [
                'button:has-text("新建会话")',
                'button:has-text("新对话")',
                'button:has-text("开启新对话")',
                'a:has-text("New chat")',
                'a:has-text("新建会话")',
                '[aria-label*="新建"]',
                '[aria-label*="新对话"]',
                '[aria-label*="New"]',
                '[title*="新建"]',
                '[title*="New"]',
            ]
            
            for selector in new_chat_selectors:
                try:
                    new_chat_btn = await page.query_selector(selector)
                    if new_chat_btn:
                        await new_chat_btn.click()
                        await asyncio.sleep(2)
                        print(f"{Fore.GREEN}[OK] [{platform.name}] 已新建会话{Style.RESET_ALL}")
                        return True
                except:
                    continue
            
            # 策略 2：检查输入框是否存在且为空（表示已是新会话）
            input_selectors = platform.selectors.get('input', 'textarea').split(', ')
            for selector in input_selectors:
                try:
                    input_box = await page.query_selector(selector)
                    if input_box:
                        # 检查输入框是否为空
                        input_value = await input_box.input_value()
                        if not input_value or input_value.strip() == '':
                            print(f"{Fore.GREEN}[OK] [{platform.name}] 已是新会话状态{Style.RESET_ALL}")
                            return True
                except:
                    continue
            
            # 策略 3：检查是否有欢迎语（表示新会话）
            welcome_indicators = [
                '有什么可以帮到你', '新对话', '新建会话', '开始新的聊天',
                'What can I help', 'New chat', 'Start a conversation',
                '今天有什么可以帮到你', '我可以随时提供协助'
            ]
            try:
                page_content = await page.content()
                for indicator in welcome_indicators:
                    if indicator.lower() in page_content.lower():
                        print(f"{Fore.GREEN}[OK] [{platform.name}] 已是新会话（欢迎语检测）{Style.RESET_ALL}")
                        return True
            except:
                pass
            
            # 如果以上都失败，默认认为是新会话
            print(f"{Fore.GREEN}[OK] [{platform.name}] 会话就绪{Style.RESET_ALL}")
            return True
                    
        except Exception as e:
            print(f"{Fore.YELLOW}[!] [{platform.name}] 新建会话检测异常：{e}{Style.RESET_ALL}")
            return False
    
    async def check_login_status(self, page: Page, platform: AIPlatform) -> Tuple[bool, str]:
        """
        检查登录状态（增强版 v2.0：多指标 + 登录按钮检测）
        
        返回：(是否登录，状态说明)
        """
        try:
            # 等待页面加载
            await page.wait_for_load_state('domcontentloaded', timeout=10000)
            await asyncio.sleep(2)
            
            # 检测指标 1：输入框（扩展选择器）
            input_selectors = platform.selectors.get('input', 'textarea').split(', ')
            # 添加通用回退选择器
            input_selectors.extend([
                '[role="textbox"]', '[role="combobox"]',
                '[contenteditable="true"]', '[contenteditable=""]',
                'div[placeholder*="发送"]', 'div[placeholder*="Message"]',
                'div[placeholder*="输入"]', 'div[placeholder*="Type"]',
                '[aria-label*="发送"]', '[aria-label*="Send"]',
                '#chat-input', '#input-box',
                '.chat-input', '.input-box',
                'textarea', 'div[contenteditable]',
            ])
            has_input = False
            for selector in input_selectors:
                try:
                    input_box = await page.query_selector(selector, timeout=1000)
                    if input_box:
                        has_input = True
                        print(f"{Fore.GREEN}[OK] [{platform.name}] 找到输入框（选择器：{selector}）{Style.RESET_ALL}")
                        break
                except:
                    continue
            
            # 检测指标 2：发送按钮
            send_selectors = platform.selectors.get('send', 'button').split(', ')
            send_selectors.extend([
                'button[type="submit"]', '[type="submit"]',
                '[aria-label*="Submit"]', '[aria-label*="发送"]',
                'button:has-text("发送")', 'button:has-text("Send")',
                '.send-btn', '#send-button', '#submit-btn',
            ])
            has_send = False
            for selector in send_selectors:
                try:
                    send_btn = await page.query_selector(selector, timeout=1000)
                    if send_btn:
                        has_send = True
                        break
                except:
                    continue
            
            # 检测指标 3：欢迎语/新会话提示
            welcome_indicators = [
                '有什么可以帮到你', '新对话', '新建会话', '开始新的聊天',
                'What can I help', 'New chat', 'Start a conversation',
                '今天有什么可以帮到你', '我可以随时提供协助', 'Hi there',
                'Hello', 'How can I help', '有什么可以帮你'
            ]
            has_welcome = False
            try:
                page_content = await page.content()
                for indicator in welcome_indicators:
                    if indicator.lower() in page_content.lower():
                        has_welcome = True
                        break
            except:
                pass
            
            # 检测指标 4：登录按钮（如果存在登录按钮，说明未登录）
            login_button_selectors = platform.selectors.get('loginButton', '').split(', ')
            login_button_selectors.extend([
                'button:has-text("登录")', 'button:has-text("Login")',
                'button:has-text("扫码")', 'button:has-text("微信")',
                'a[href*="login"]', 'button:has-text("Sign in")',
                '.login-btn', '.login-button',
            ])
            has_login_button = False
            for selector in login_button_selectors:
                if not selector:
                    continue
                try:
                    login_btn = await page.query_selector(selector, timeout=1000)
                    if login_btn:
                        # 检查按钮是否可见（有些页面有隐藏按钮）
                        is_visible = await login_btn.is_visible()
                        if is_visible:
                            has_login_button = True
                            print(f"{Fore.YELLOW}[!] [{platform.name}] 发现登录按钮（选择器：{selector}）{Style.RESET_ALL}")
                            break
                except:
                    continue
            
            # 综合判断
            if has_login_button and not (has_input or has_send or has_welcome):
                # 明确有登录按钮且没有其他登录指标
                print(f"{Fore.RED}[X] [{platform.name}] 未登录（检测到登录按钮）{Style.RESET_ALL}")
                return False, "未登录（检测到登录按钮）"
            elif has_input or has_send:
                print(f"{Fore.GREEN}[OK] [{platform.name}] 已登录{Style.RESET_ALL}")
                return True, "已登录"
            elif has_welcome:
                # 有欢迎语但没找到输入框，可能是选择器问题
                print(f"{Fore.GREEN}[OK] [{platform.name}] 已登录（欢迎语检测）{Style.RESET_ALL}")
                return True, "欢迎语检测"
            else:
                # 无法确定，倾向于认为未登录
                print(f"{Fore.RED}[X] [{platform.name}] 未登录（未检测到输入框、发送按钮或欢迎语）{Style.RESET_ALL}")
                return False, "未检测到登录凭证"
                
        except Exception as e:
            print(f"{Fore.YELLOW}[!] [{platform.name}] 登录状态检测异常：{e}{Style.RESET_ALL}")
            return False, f"检测异常：{e}"
    
    async def send_question(self, page: Page, platform: AIPlatform, question: str) -> bool:
        """
        发送问题（增强选择器版 v2.0）
        
        重试策略：
        1. 第 1 次失败：等待 2 秒，刷新页面后重试
        2. 第 2 次失败：等待 3 秒，尝试 Enter 键发送
        3. 第 3 次失败：返回错误
        
        平台特定优化：
        - Qwen: 优先使用 #chat-input 和 textarea[aria-label*="Prompt"]
        - 豆包：优先使用 textarea 和 .input-box
        - DeepSeek: 优先使用 textarea[placeholder*='输入']
        - Kimi: 优先使用 #input-box 和 textarea#chat-input
        """
        max_retries = 3
        
        for attempt in range(max_retries):
            try:
                # 找到输入框（使用更多选择器）
                input_selectors = platform.selectors.get('input', 'textarea').split(', ')
                
                # 平台特定优化选择器（优先级最高）
                if platform.name == "Qwen":
                    platform_specific = [
                        '#chat-input',
                        'textarea#chat-input',
                        'textarea[aria-label*="Prompt"]',
                        'textarea[aria-label*="消息"]',
                        'textarea[placeholder*="发送"]',
                        '[data-testid*="chat-input"]',
                    ]
                elif platform.name == "豆包":
                    platform_specific = [
                        'textarea',
                        '#input-box',
                        'textarea[placeholder*="消息"]',
                        'textarea[aria-label*="消息"]',
                        '.input-box',
                        '[class*="input"]',
                    ]
                elif platform.name == "DeepSeek":
                    platform_specific = [
                        'textarea[placeholder*="输入"]',
                        'textarea[placeholder*="Message"]',
                        'textarea[aria-label*="发送"]',
                        '[contenteditable="true"]',
                        '[role="textbox"]',
                    ]
                elif platform.name == "Kimi":
                    platform_specific = [
                        '#input-box',
                        'textarea#chat-input',
                        'textarea[placeholder*="输入"]',
                        'textarea[aria-label*="消息"]',
                        '.input-box',
                    ]
                elif platform.name == "Gemini":
                    platform_specific = [
                        'div[contenteditable="true"]',
                        'textarea[aria-label*="Prompt"]',
                        'textarea[aria-label*="消息"]',
                        '[role="textbox"]',
                        'div[placeholder*="Message"]',
                    ]
                else:
                    platform_specific = []
                
                # 合并选择器：平台特定 > 配置 > 通用
                input_selectors = platform_specific + input_selectors
                input_selectors.extend([
                    # ARIA 角色
                    '[role="textbox"]',
                    '[role="combobox"]',
                    # 可编辑元素
                    '[contenteditable="true"]',
                    '[contenteditable=""]',
                    # 占位符
                    'div[placeholder*="发送"]',
                    'div[placeholder*="Message"]',
                    'div[placeholder*="输入"]',
                    'div[placeholder*="Type"]',
                    'div[placeholder*="Prompt"]',
                    # aria-label
                    '[aria-label*="发送"]',
                    '[aria-label*="Send"]',
                    '[aria-label*="Message"]',
                    '[aria-label*="Prompt"]',
                    # 常见 class 和 ID
                    '#chat-input',
                    '#input-box',
                    'textarea#chat-input',
                    'textarea#input-box',
                    '.chat-input',
                    '.input-box',
                    '[class*="chat-input"]',
                    '[class*="input-box"]',
                    '[class*="textarea"]',
                    '[class*="composer"]',
                    # data-testid
                    '[data-testid*="input"]',
                    '[data-testid*="chat-input"]',
                    # 通用选择器
                    'textarea',
                    'div[contenteditable]',
                ])
                
                input_box = None
                used_selector = None
                for selector in input_selectors:
                    try:
                        input_box = await page.wait_for_selector(selector, timeout=2000)
                        if input_box:
                            used_selector = selector
                            print(f"{Fore.GREEN}[OK] [{platform.name}] 找到输入框（选择器：{selector[:60]}...）{Style.RESET_ALL}")
                            break
                    except:
                        continue
                
                if not input_box:
                    if attempt < max_retries - 1:
                        # 刷新页面后重试
                        print(f"{Fore.YELLOW}[!] [{platform.name}] 未找到输入框（已尝试{len(input_selectors)}个选择器），刷新页面重试...{Style.RESET_ALL}")
                        await page.reload(timeout=10000)
                        await asyncio.sleep(2)
                        continue
                    raise Exception("找不到输入框（已尝试" + str(len(input_selectors)) + "个选择器）")
                
                # 清空输入框并填入问题
                await input_box.click()
                await asyncio.sleep(0.5)
                
                # 尝试多种输入方式
                try:
                    await input_box.fill(question)
                except:
                    # 如果 fill 失败，尝试 type（模拟键盘输入）
                    print(f"{Fore.YELLOW}[!] [{platform.name}] fill 失败，尝试 type 输入...{Style.RESET_ALL}")
                    await input_box.type(question, delay=10)
                
                await asyncio.sleep(0.5)
                
                # 找到发送按钮并点击（平台特定优化）
                send_selectors = platform.selectors.get('send', 'button').split(', ')
                
                # 平台特定优化
                if platform.name == "Qwen":
                    platform_send = [
                        '#send-button',
                        'button.send',
                        'button[aria-label*="发送"]',
                        'button[aria-label*="Submit"]',
                        '[data-testid*="send"]',
                    ]
                elif platform.name == "豆包":
                    platform_send = [
                        '.send-btn',
                        'button[class*="send"]',
                        'button[aria-label*="发送"]',
                        '[class*="send"]',
                    ]
                elif platform.name == "DeepSeek":
                    platform_send = [
                        'button[aria-label*="发送"]',
                        'button[aria-label*="Send"]',
                        'button[type="submit"]',
                    ]
                elif platform.name == "Kimi":
                    platform_send = [
                        '#submit-btn',
                        'button.submit',
                        'button[aria-label*="发送"]',
                    ]
                elif platform.name == "Gemini":
                    platform_send = [
                        'button[aria-label*="Send"]',
                        'button[aria-label*="Submit"]',
                        'button[aria-label*="发送"]',
                    ]
                else:
                    platform_send = []
                
                send_selectors = platform_send + send_selectors
                send_selectors.extend([
                    'button[type="submit"]',
                    '[aria-label*="Submit"]',
                    '[type="submit"]',
                    '[aria-label*="发送"]',
                    '[aria-label*="Send"]',
                    'button:has-text("发送")',
                    'button:has-text("Send")',
                    '.send-btn',
                    '#send-button',
                    '#submit-btn',
                    '[class*="send-btn"]',
                    '[class*="submit"]',
                    '[data-testid*="send"]',
                    '[data-testid*="submit"]',
                ])
                
                send_button = None
                for selector in send_selectors:
                    try:
                        send_button = await page.wait_for_selector(selector, timeout=2000)
                        if send_button:
                            print(f"{Fore.GREEN}[OK] [{platform.name}] 找到发送按钮（选择器：{selector[:60]}...）{Style.RESET_ALL}")
                            break
                    except:
                        continue
                
                if not send_button:
                    # 尝试按 Enter 键发送
                    print(f"{Fore.YELLOW}[!] [{platform.name}] 未找到发送按钮，尝试 Enter 键发送...{Style.RESET_ALL}")
                    await input_box.press('Enter')
                else:
                    # Qwen 特殊处理：可能有遮挡元素，优先使用 Enter 键
                    if platform.name == "Qwen":
                        try:
                            # 先尝试关闭可能的遮挡元素（点击页面空白处）
                            await page.click('body', position={'x': 10, 'y': 10})
                            await asyncio.sleep(0.5)
                        except:
                            pass
                        
                        # Qwen 使用 Enter 键发送更可靠
                        print(f"{Fore.YELLOW}[!] [{platform.name}] 使用 Enter 键发送（避免遮挡问题）...{Style.RESET_ALL}")
                        await input_box.press('Enter')
                    else:
                        try:
                            await send_button.click()
                        except Exception as click_error:
                            # 点击失败，回退到 Enter 键
                            print(f"{Fore.YELLOW}[!] [{platform.name}] 点击失败，改用 Enter 键发送：{click_error}{Style.RESET_ALL}")
                            await input_box.press('Enter')
                
                await asyncio.sleep(1)
                print(f"{Fore.GREEN}[OK] [{platform.name}] 问题已发送{Style.RESET_ALL}")
                return True
                
            except Exception as e:
                if attempt < max_retries - 1:
                    wait_time = 2 + attempt  # 第 1 次等 2 秒，第 2 次等 3 秒
                    print(f"{Fore.YELLOW}[!] [{platform.name}] 发送失败，{wait_time}秒后重试 {attempt + 1}/{max_retries}: {e}{Style.RESET_ALL}")
                    await asyncio.sleep(wait_time)
                    
                    # 第 1 次失败后刷新页面
                    if attempt == 0:
                        try:
                            await page.reload(timeout=10000)
                            await asyncio.sleep(2)
                        except:
                            pass
                else:
                    print(f"{Fore.RED}[X] [{platform.name}] 发送失败（已重试{max_retries}次）: {e}{Style.RESET_ALL}")
                    return False
        
        return False
    
    async def wait_for_response(self, page: Page, platform: AIPlatform, timeout: int = None) -> Tuple[bool, str]:
        """
        等待响应（tqdm 进度条版 + 增强选择器）
        
        返回：(是否成功，响应内容)
        """
        timeout = timeout or platform.timeout
        
        # 显示进度提示
        if HAS_TQDM and tqdm:
            # 使用 tqdm 进度条
            with tqdm(total=timeout, desc=f"[{platform.name}]", unit='秒', ncols=80, 
                     bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt}秒 [{percentage:.0f}%]') as pbar:
                elapsed = 0
                interval = 1
                
                while elapsed < timeout:
                    # 等待响应出现（平台特定优化选择器）
                    response_selectors = platform.selectors.get('response', '.markdown-body').split(', ')
                    
                    # 平台特定优化
                    if platform.name == "豆包":
                        platform_response = [
                            '.answer-content',
                            '[class*="answer"]',
                            '.message-content',
                            '[class*="message"]',
                            '.response-content',
                            'div.markdown-body',
                        ]
                    elif platform.name == "Qwen":
                        platform_response = [
                            '.response-content',
                            '.answer',
                            '[class*="response"]',
                            'article',
                            'div.markdown-body',
                        ]
                    elif platform.name == "DeepSeek":
                        platform_response = [
                            'div.markdown-body',
                            '.markdown-body',
                            '[class*="response"]',
                            'article',
                        ]
                    elif platform.name == "Kimi":
                        platform_response = [
                            '.message-ai',
                            '[class*="assistant"]',
                            '.message-content',
                            '[class*="content"]',
                        ]
                    elif platform.name == "Gemini":
                        platform_response = [
                            'article',
                            '[class*="response"]',
                            '[class*="content"]',
                            'div.markdown-body',
                        ]
                    else:
                        platform_response = []
                    
                    # 合并选择器：平台特定 > 配置 > 通用
                    response_selectors = platform_response + response_selectors
                    response_selectors.extend([
                        'article',
                        '[class*="message"]',
                        '[class*="content"]',
                        '[class*="answer"]',
                        '[class*="response"]',
                        'div.markdown-body',
                        '.markdown-body',
                    ])
                    
                    for selector in response_selectors:
                        try:
                            response_element = await page.query_selector(selector)
                            if response_element:
                                # 检查响应是否完整（没有 loading 指示器）
                                loading_selectors = platform.selectors.get('loading', '').split(', ')
                                has_loading = False
                                
                                for loading_selector in loading_selectors:
                                    if loading_selector:
                                        try:
                                            loading_element = await page.query_selector(loading_selector)
                                            if loading_element:
                                                has_loading = True
                                                break
                                        except:
                                            pass
                                
                                if not has_loading:
                                    # 额外等待几秒确保内容完整
                                    await asyncio.sleep(3)
                                    # 提取响应内容
                                    content = await self.extract_response_content(page, platform)
                                    if content:
                                        return True, content
                        except:
                            pass
                    
                    # 等待一段时间后更新进度条
                    await asyncio.sleep(min(interval, timeout - elapsed))
                    elapsed += interval
                    pbar.update(interval)
            
            # 超时
            return False, "等待超时"
        else:
            # 降级使用简单进度显示
            print(f"{Fore.CYAN}[...] [{platform.name}] 等待响应（最多{timeout}秒）...{Style.RESET_ALL}")
            
            elapsed = 0
            interval = 5
            progress_chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
            
            while elapsed < timeout:
                progress_percent = int((elapsed / timeout) * 100)
                progress_char = progress_chars[(elapsed // interval) % len(progress_chars)]
                
                if elapsed > 0:
                    print(f"\r{Fore.CYAN}{progress_char} [{platform.name}] 等待中... [{elapsed}/{timeout}秒] {progress_percent}%", end='', flush=True)
                
                # 等待响应出现
                response_selectors = platform.selectors.get('response', '.markdown-body').split(', ')
                response_selectors.extend([
                    'article',
                    '[class*="message"]',
                    '[class*="content"]',
                    '[class*="answer"]',
                ])
                
                for selector in response_selectors:
                    try:
                        response_element = await page.query_selector(selector)
                        if response_element:
                            loading_selectors = platform.selectors.get('loading', '').split(', ')
                            has_loading = False
                            
                            for loading_selector in loading_selectors:
                                if loading_selector:
                                    try:
                                        loading_element = await page.query_selector(loading_selector)
                                        if loading_element:
                                            has_loading = True
                                            break
                                    except:
                                        pass
                            
                            if not has_loading:
                                await asyncio.sleep(3)
                                content = await self.extract_response_content(page, platform)
                                print(f"\r{Fore.GREEN}[OK] [{platform.name}] 响应已完成{Style.RESET_ALL}          ")
                                return True, content
                    except:
                        pass
                
                await asyncio.sleep(min(interval, timeout - elapsed))
                elapsed += interval
            
            print(f"\r{Fore.YELLOW}[!] [{platform.name}] 等待超时（{timeout}秒）{Style.RESET_ALL}          ")
            return False, "等待超时"
    
    async def extract_response_content(self, page: Page, platform: AIPlatform) -> str:
        """
        提取响应内容（增强选择器版 v2.0 - 平台特定优化）
        
        尝试多个选择器，返回第一个匹配的内容
        
        平台特定优化：
        - 豆包：优先 .answer-content, .message-content
        - Qwen: 优先 .response-content, .answer
        - DeepSeek: 优先 div.markdown-body
        - Kimi: 优先 .message-ai, [class*="assistant"]
        - Gemini: 优先 article, [class*="response"]
        """
        try:
            # 使用配置的选择器
            response_selectors = platform.selectors.get('response', '.markdown-body').split(', ')
            
            # 平台特定优化（优先级最高）
            if platform.name == "豆包":
                platform_response = [
                    '.answer-content',
                    '[class*="answer"]',
                    '.message-content',
                    '[class*="message"]',
                    '.response-content',
                    '[class*="response"]',
                    'div.markdown-body',
                ]
            elif platform.name == "Qwen":
                platform_response = [
                    '.response-content',
                    '.answer',
                    '[class*="response"]',
                    'article',
                    'div.markdown-body',
                ]
            elif platform.name == "DeepSeek":
                platform_response = [
                    'div.markdown-body',
                    '.markdown-body',
                    '[class*="response"]',
                    'article',
                ]
            elif platform.name == "Kimi":
                platform_response = [
                    '.message-ai',
                    '[class*="assistant"]',
                    '.message-content',
                    '[class*="content"]',
                ]
            elif platform.name == "Gemini":
                platform_response = [
                    'article',
                    '[class*="response"]',
                    '[class*="content"]',
                    'div.markdown-body',
                ]
            else:
                platform_response = []
            
            # 合并选择器：平台特定 > 配置 > 通用
            response_selectors = platform_response + response_selectors
            response_selectors.extend([
                # Markdown 内容
                'div.markdown-body',
                '.markdown-body',
                '.markdown-content',
                '[class*="markdown"]',
                # 响应内容
                'div[class*="response"]',
                'div[class*="answer"]',
                'div[class*="message"]',
                'div[class*="content"]',
                'div[class*="assistant"]',
                'div[class*="bot"]',
                'div[class*="reply"]',
                # 文章元素
                'article',
                '[role="article"]',
                # 对话气泡
                '[class*="bubble"]',
                '[class*="chat-bubble"]',
                # 消息容器
                '[class*="message-content"]',
                '[class*="response-content"]',
                '[class*="answer-content"]',
                # data-testid
                '[data-testid*="response"]',
                '[data-testid*="message"]',
                '[data-testid*="answer"]',
                '[data-testid*="content"]',
                # ARIA 角色
                '[role="document"]',
                '[role="region"]',
                # 通用 div
                'div[class*="ai"]',
                'div[class*="bot"]',
                'div[class*="assistant"]',
            ])
            
            # 尝试多个选择器
            for selector in response_selectors:
                try:
                    response_element = await page.query_selector(selector)
                    if response_element:
                        # 尝试多种提取方式
                        content = None
                        
                        # 方式 1：inner_text（最常用）
                        try:
                            content = await response_element.inner_text()
                        except:
                            pass
                        
                        # 方式 2：text_content（备选）
                        if not content or len(content.strip()) < 50:
                            try:
                                content = await response_element.text_content()
                            except:
                                pass
                        
                        # 方式 3：innerHTML（最后手段）
                        if not content or len(content.strip()) < 50:
                            try:
                                content = await response_element.inner_html()
                            except:
                                pass
                        
                        if content and len(content.strip()) > 50:
                            print(f"{Fore.GREEN}[OK] [{platform.name}] 内容已提取（选择器：{selector[:60]}..., {len(content)} 字）{Style.RESET_ALL}")
                            return content
                except:
                    continue
            
            print(f"{Fore.RED}[X] [{platform.name}] 未找到响应内容（已尝试{len(response_selectors)}个选择器）{Style.RESET_ALL}")
            return ""
        except Exception as e:
            print(f"{Fore.RED}[X] [{platform.name}] 提取失败：{e}{Style.RESET_ALL}")
            return ""
    
    async def extract_response(self, page: Page, platform: AIPlatform) -> str:
        """提取响应内容（带多个选择器回退）"""
        try:
            response_selectors = platform.selectors.get('response', '.markdown-body').split(', ')
            
            for selector in response_selectors:
                try:
                    response_element = await page.query_selector(selector)
                    if response_element:
                        content = await response_element.inner_text()
                        if content and len(content.strip()) > 50:  # 确保内容有实际意义
                            print(f"{Fore.GREEN}[OK] [{platform.name}] 内容已提取（{len(content)} 字）{Style.RESET_ALL}")
                            return content
                except:
                    continue
            
            print(f"{Fore.RED}[X] [{platform.name}] 未找到响应内容{Style.RESET_ALL}")
            return ""
        except Exception as e:
            print(f"{Fore.RED}[X] [{platform.name}] 提取失败：{e}{Style.RESET_ALL}")
            return ""
    
    async def query_single_platform(self, platform: AIPlatform, question: str, timeout: int) -> Dict:
        """查询单个平台（带重试机制）"""
        page = await self.browser.new_page()
        max_retries = 2
        
        try:
            print(f"\n{Fore.CYAN}========================================{Style.RESET_ALL}")
            print(f"{Fore.CYAN}  [{platform.name}] 开始查询{Style.RESET_ALL}")
            print(f"{Fore.CYAN}========================================{Style.RESET_ALL}")
            
            # 打开页面
            await page.goto(platform.url, timeout=30000)
            await asyncio.sleep(2)
            
            # 确保新建会话
            await self.ensure_new_chat(page, platform)
            
            # 检查登录状态（增强版）
            is_logged_in, status_msg = await self.check_login_status(page, platform)
            
            if not is_logged_in:
                # 给用户 30 秒时间手动登录，超时自动继续尝试
                print(f"{Fore.YELLOW}[!] [{platform.name}] 请手动完成登录（30 秒后自动继续）...{Style.RESET_ALL}")
                
                # 非阻塞等待，每 5 秒检测一次
                for i in range(6):  # 最多等 30 秒
                    await asyncio.sleep(5)
                    is_logged_in, status_msg = await self.check_login_status(page, platform)
                    if is_logged_in:
                        break
                
                # 如果还是未登录，再给一次手动确认机会
                if not is_logged_in:
                    print(f"{Fore.YELLOW}[!] [{platform.name}] 如已登录，按回车继续；否则输入 q 跳过...{Style.RESET_ALL}")
                    try:
                        user_input = input().strip().lower()
                        if user_input == 'q':
                            return {
                                'platform': platform.name,
                                'content': '',
                                'timestamp': datetime.now().isoformat(),
                                'success': False,
                                'error': '用户跳过登录'
                            }
                        is_logged_in = True  # 用户确认已登录
                    except:
                        is_logged_in = False
            
            if not is_logged_in:
                return {
                    'platform': platform.name,
                    'content': '',
                    'timestamp': datetime.now().isoformat(),
                    'success': False,
                    'error': f'登录检测失败：{status_msg}'
                }
            
            # 发送问题（带重试）
            for attempt in range(max_retries):
                sent = await self.send_question(page, platform, question)
                if sent:
                    break
                elif attempt < max_retries - 1:
                    print(f"{Fore.YELLOW}[!] [{platform.name}] 准备重试发送...{Style.RESET_ALL}")
                    await asyncio.sleep(2)
            else:
                return {
                    'platform': platform.name,
                    'content': '',
                    'timestamp': datetime.now().isoformat(),
                    'success': False,
                    'error': '发送问题失败'
                }
            
            # 等待响应
            responded = await self.wait_for_response(page, platform, timeout)
            if not responded:
                return {
                    'platform': platform.name,
                    'content': '',
                    'timestamp': datetime.now().isoformat(),
                    'success': False,
                    'error': '等待响应超时'
                }
            
            # 提取响应
            content = await self.extract_response(page, platform)
            
            return {
                'platform': platform.name,
                'content': content,
                'timestamp': datetime.now().isoformat(),
                'success': True
            }
            
        except Exception as e:
            print(f"{Fore.RED}[X] [{platform.name}] 查询失败：{e}{Style.RESET_ALL}")
            return {
                'platform': platform.name,
                'content': '',
                'timestamp': datetime.now().isoformat(),
                'success': False,
                'error': str(e)
            }
        finally:
            await page.close()
    
    async def query_parallel(self, platforms: List[AIPlatform], question: str, timeout: int) -> List[Dict]:
        """并行查询多个平台（带进度跟踪）"""
        tasks = [
            self.query_single_platform(platform, question, timeout)
            for platform in platforms
        ]
        
        # 显示进度提示
        print(f"\n{Fore.CYAN}正在并行询问 {len(platforms)} 家 AI...{Style.RESET_ALL}")
        print(f"{Fore.CYAN}预计耗时：{len(platforms) * 15}秒{Style.RESET_ALL}\n")
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 统计结果
        success_count = sum(1 for r in results if isinstance(r, dict) and r.get('success'))
        print(f"\n{Fore.GREEN}[OK] 完成！成功：{success_count}/{len(results)}{Style.RESET_ALL}")
        
        return results
    
    def build_question(self, topic: str, dimensions: List[str], 
                       template: str = None, follow_up: List[str] = None) -> str:
        """构建统一问题（支持自定义模板）"""
        
        # 默认模板（通用型）
        if template is None:
            dimension_str = '、'.join(dimensions) if dimensions else '相关方面'
            question = f"请帮我分析一下 {topic}，包括{dimension_str}等方面的情况。"
            
            # 添加延伸问题（如果有）
            if follow_up:
                question += "\n\n另外，" + " ".join(follow_up)
            
            return question
        
        # 使用自定义模板
        dimension_str = '、'.join(dimensions) if dimensions else '相关方面'
        return template.format(topic=topic, dimensions=dimension_str)
    
    def save_report(self, topic: str, results: List[Dict], output_path: str = None):
        """保存报告（集成数据提取和质量评分）"""
        if output_path is None:
            reports_dir = Path(__file__).parent.parent / 'reports'
            reports_dir.mkdir(exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y-%m-%d-%H%M')
            safe_topic = topic.replace('/', '_').replace('\\', '_')
            output_path = reports_dir / f"{safe_topic}-{timestamp}.md"
        
        # 数据提取和质量评分
        print(f"\n{Fore.CYAN}========================================{Style.RESET_ALL}")
        print(f"{Fore.CYAN}  数据提取与质量评分{Style.RESET_ALL}")
        print(f"{Fore.CYAN}========================================{Style.RESET_ALL}\n")
        
        try:
            from extractor import DataExtractor
            extractor = DataExtractor()
            
            # 为每个结果提取数据并评分
            for result in results:
                if result.get('success') and result.get('content'):
                    platform = result.get('platform', 'Unknown')
                    content = result.get('content', '')
                    
                    # 提取数据
                    print(f"{Fore.YELLOW}[提取] {platform}...{Style.RESET_ALL}")
                    extracted_data = extractor.extract_all(content)
                    result['extracted_data'] = extracted_data
                    
                    # 质量评分
                    quality_score = extractor.calculate_quality_score(content, platform)
                    result['quality_score'] = quality_score
                    
                    print(f"  {Fore.GREEN}✓ 数据点：{len(extracted_data['data_points']) + len(extracted_data['percentages'])} 个{Style.RESET_ALL}")
                    print(f"  {Fore.GREEN}✓ 质量评分：{quality_score['total_score']} ({quality_score['level']}){Style.RESET_ALL}\n")
            
            # 生成对比表
            comparison_table = extractor.generate_comparison_table(results)
            
        except Exception as e:
            print(f"{Fore.YELLOW}[!] 数据提取失败：{e}{Style.RESET_ALL}")
            comparison_table = ""
        
        # 导入报告生成器
        try:
            from reporter import generate_report
            output_path = generate_report(topic, results, str(output_path), 
                                         comparison_table=comparison_table)
        except ImportError:
            print(f"{Fore.YELLOW}[!] 报告生成器未找到，使用简化报告{Style.RESET_ALL}")
            # 简化报告逻辑
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(f"# {topic} - 综合分析报告\n\n")
                f.write(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                # 添加质量评分汇总
                f.write("## 质量评分汇总\n\n")
                f.write("| 平台 | 总分 | 字数 | 数据点 | 结构 | 引用 | 等级 |\n")
                f.write("|------|------|------|--------|------|------|------|\n")
                for result in results:
                    if result.get('success'):
                        qs = result.get('quality_score', {})
                        bd = qs.get('breakdown', {})
                        f.write(f"| {result.get('platform', 'Unknown')} | "
                               f"{qs.get('total_score', 0)} | "
                               f"{bd.get('word_count', {}).get('score', 0)} | "
                               f"{bd.get('data_points', {}).get('score', 0)} | "
                               f"{bd.get('structure', {}).get('score', 0)} | "
                               f"{bd.get('sources', {}).get('score', 0)} | "
                               f"{qs.get('level', '-')} |\n")
                f.write("\n")
                
                # 添加各平台回复
                for result in results:
                    if result.get('success'):
                        f.write(f"\n## {result['platform']}\n\n{result['content']}\n\n")
        
        print(f"\n{Fore.GREEN}[OK] 报告已保存：{output_path}{Style.RESET_ALL}")
        return str(output_path)
    
    async def run(self, topic: str, platforms: List[str] = None, 
                  dimensions: List[str] = None, timeout: int = 120,
                  mode: str = 'parallel', output: str = None, headless: bool = False,
                  question_template: str = None, follow_up_questions: List[str] = None,
                  skip_login: bool = False):
        """执行分析"""
        
        # 过滤平台
        if platforms:
            target_platforms = [p for p in self.platforms if p.name in platforms]
        else:
            target_platforms = self.platforms
        
        # 默认维度（通用型）
        if dimensions is None:
            dimensions = self.config.get('defaultDimensions', [])
        
        # 构建问题（支持自定义模板）
        question = self.build_question(topic, dimensions, question_template, follow_up_questions)
        
        print(f"\n{Fore.GREEN}========================================{Style.RESET_ALL}")
        print(f"{Fore.GREEN}  Multi-AI Search Analysis v2.0.1{Style.RESET_ALL}")
        print(f"{Fore.GREEN}  模式：{'并行' if mode == 'parallel' else '串行'}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}  稳定性增强版（Qwen 优化）{Style.RESET_ALL}")
        print(f"{Fore.GREEN}========================================{Style.RESET_ALL}\n")
        
        print(f"{Fore.YELLOW}分析主题：{topic}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}分析维度：{', '.join(dimensions) if dimensions else 'AI 自由发挥'}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}AI 平台：{', '.join(p.name for p in target_platforms)}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}超时时间：{timeout}秒{Style.RESET_ALL}\n")
        
        # 初始化浏览器
        await self.initialize_browser(headless)
        
        # 预执行检查：验证所有平台的登录状态（除非跳过）
        if not skip_login:
            print(f"\n{Fore.CYAN}========================================{Style.RESET_ALL}")
            print(f"{Fore.CYAN}  预执行检查 - 登录状态验证{Style.RESET_ALL}")
            print(f"{Fore.CYAN}========================================{Style.RESET_ALL}\n")
            
            login_issues = []
            for platform in target_platforms:
                try:
                    page = await self.browser.new_page()
                    await page.goto(platform.url, timeout=30000)
                    await asyncio.sleep(2)
                    
                    is_logged_in, status_msg = await self.check_login_status(page, platform)
                    
                    if is_logged_in:
                        print(f"{Fore.GREEN}[OK] [{platform.name}] 已登录{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.RED}[X] [{platform.name}] 未登录：{status_msg}{Style.RESET_ALL}")
                        login_issues.append(platform.name)
                    
                    await page.close()
                except Exception as e:
                    print(f"{Fore.YELLOW}[!] [{platform.name}] 检查失败：{e}{Style.RESET_ALL}")
                    login_issues.append(platform.name)
            
            if login_issues:
                print(f"\n{Fore.YELLOW}[!] 以下平台需要登录：{', '.join(login_issues)}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}提示：运行 python scripts/login.py 完成登录{Style.RESET_ALL}\n")
                
                # 给用户机会选择继续或取消
                print(f"{Fore.CYAN}按回车继续（脚本会等待手动登录），或输入 q 取消...{Style.RESET_ALL}")
                user_input = input().strip().lower()
                if user_input == 'q':
                    print(f"{Fore.RED}[X] 已取消{Style.RESET_ALL}")
                    return
        else:
            print(f"\n{Fore.YELLOW}[!] 跳过登录检测 - 直接运行{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}提示：如果平台需要登录，请求可能会失败{Style.RESET_ALL}\n")
        
        try:
            if mode == 'parallel':
                # 并行模式
                results = await self.query_parallel(target_platforms, question, timeout)
            else:
                # 串行模式
                results = []
                for platform in target_platforms:
                    result = await self.query_single_platform(platform, question, timeout)
                    results.append(result)
            
            # 保存报告
            self.save_report(topic, results, output)
            
        finally:
            # 关闭浏览器
            if self.browser:
                await self.browser.close()
                print(f"{Fore.CYAN}[OK] 浏览器已关闭{Style.RESET_ALL}")


async def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='Multi-AI Search Analysis - 多 AI 搜索分析工具（优化版）',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 时事分析
  python run.py -t "伊朗局势分析" -d 政治 经济 军事 外交

  # 技术对比
  python run.py -t "Python vs Java 性能对比" -d 性能 易用性 生态 学习曲线

  # 产品评测
  python run.py -t "iPhone 16 Pro 评测" -d 性能 拍照 续航 价格

  # 市场研究
  python run.py -t "2026 年 AI 市场趋势" -d 技术 投资 应用 竞争

  # 自定义问题模板
  python run.py -t "产品对比" --question-template "请详细对比{topic}，从{dimensions}角度分析"

  # 添加延伸问题
  python run.py -t "技术分析" --follow-up "有什么风险？" "未来趋势如何？"

  # 指定平台和超时
  python run.py -t "主题" -p DeepSeek Qwen Kimi --timeout 180
  python run.py -t "主题" -o "C:/reports/output.md"
        """
    )
    
    parser.add_argument('--topic', '-t', type=str, required=True,
                        help='分析主题（必填）')
    parser.add_argument('--platforms', '-p', type=str, nargs='+',
                        choices=['DeepSeek', 'Qwen', '豆包', 'Kimi', 'Gemini'],
                        help='AI 平台列表（默认：全部）')
    parser.add_argument('--dimensions', '-d', type=str, nargs='+',
                        default=None,
                        help='分析维度（默认：无，由 AI 自由发挥）')
    parser.add_argument('--output', '-o', type=str,
                        help='输出文件路径（默认：自动生成）')
    parser.add_argument('--timeout', type=int, default=120,
                        help='每家 AI 等待超时（秒，默认：120）')
    parser.add_argument('--mode', '-m', type=str, choices=['parallel', 'serial'],
                        default='parallel', help='执行模式（默认：parallel）')
    parser.add_argument('--headless', action='store_true',
                        help='无头模式运行（默认：显示浏览器）')
    parser.add_argument('--question-template', type=str,
                        help='自定义问题模板（支持{topic}和{dimensions}占位符）')
    parser.add_argument('--follow-up', type=str, nargs='+',
                        help='延伸问题列表（可选）')
    parser.add_argument('--skip-login', action='store_true',
                        help='跳过登录检测（直接运行）')
    
    args = parser.parse_args()
    
    # 创建分析器并运行
    analyzer = MultiAISearch()
    await analyzer.run(
        topic=args.topic,
        platforms=args.platforms,
        dimensions=args.dimensions,
        timeout=args.timeout,
        mode=args.mode,
        output=args.output,
        headless=args.headless,
        question_template=args.question_template,
        follow_up_questions=args.follow_up,
        skip_login=args.skip_login
    )


if __name__ == '__main__':
    asyncio.run(main())
