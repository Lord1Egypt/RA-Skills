#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
头条文章发布脚本 - Playwright完整版
整合文章生成、配图生成和浏览器自动化发布
"""

import sys
import os
import time
import json
import argparse
from pathlib import Path

# 添加项目根目录到Python路径
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT_DIR)

from core.article_generator import ArticleGenerator
from core.image_generator import ImageGenerator
from core.feishu_notifier import FeishuNotifier
from core.cookie_manager import CookieManager


def log(message):
    """日志输出"""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")


def load_config():
    """加载配置文件"""
    config_path = os.path.join(ROOT_DIR, "config", "account_config.json")
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        print(f"[错误] 配置文件不存在: {config_path}")
        print("[提示] 请复制 config/account_config.json.example 为 config/account_config.json 并填入你的信息")
        return None


def load_cookies(config):
    """加载Cookie文件"""
    cookie_file = config.get("cookie_file")
    if not cookie_file or not os.path.exists(cookie_file):
        print(f"[错误] Cookie文件不存在: {cookie_file}")
        return None

    import json
    with open(cookie_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    cookies = []
    for c in data:
        cookie = {
            "name": c.get("name"),
            "value": c.get("value"),
            "domain": c.get("domain", ".toutiao.com"),
            "path": c.get("path", "/")
        }
        if c.get("httpOnly"):
            cookie["httpOnly"] = True
        if c.get("secure"):
            cookie["secure"] = True
        if c.get("sameSite"):
            ss = c["sameSite"]
            cookie["sameSite"] = ss if ss in ("Strict", "Lax", "None") else "Lax"
        cookies.append(cookie)

    return cookies


def main():
    parser = argparse.ArgumentParser(description="头条文章发布脚本")
    parser.add_argument("--topic", "-t", type=str, help="文章话题（不传则自动从话题邀请中获取）")
    parser.add_argument("--content", "-c", type=str, help="自定义正文内容")
    parser.add_argument("--title", type=str, help="自定义标题")
    parser.add_argument("--image", "-i", type=str, help="配图文件路径")
    parser.add_argument("--no-publish", action="store_true", help="只生成不发布")
    args = parser.parse_args()

    # 加载配置
    config = load_config()
    if not config:
        sys.exit(1)

    log("===== 头条文章发布开始 =====")
    log(f"账号: {config.get('account_name', '未知')}")

    # 1. 生成文章
    if args.content:
        article = {
            "title": args.title or "自定义文章",
            "content": args.content,
            "topic": args.topic or "自定义"
        }
    else:
        article_gen = ArticleGenerator()
        topic = args.topic or "中年男人的困境"
        article = article_gen.generate_article(topic)
        log(f"话题: {topic}")

    log(f"标题: {article['title']}")
    log(f"字数: {len(article['content'])}")

    if args.no_publish:
        log("===== 仅生成模式（不发布）=====")
        print(f"\n标题: {article['title']}")
        print(f"\n{article['content']}")
        return

    # 2. 获取配图
    image_path = args.image
    if not image_path:
        # 尝试从 generated-images 目录查找
        img_dir = os.path.join(ROOT_DIR, "generated-images")
        if os.path.exists(img_dir):
            img_files = [f for f in os.listdir(img_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
            if img_files:
                image_path = os.path.join(img_dir, img_files[0])
                log(f"使用已有配图: {image_path}")

    # 3. 连接浏览器发布
    from playwright.sync_api import sync_playwright

    cookies = load_cookies(config)
    if not cookies:
        sys.exit(1)

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            slow_mo=80,
            args=["--no-sandbox"]
        )
        ctx = browser.new_context(
            viewport={"width": 1440, "height": 900},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )

        ctx.add_cookies(cookies)
        page = ctx.new_page()

        # 检查登录状态
        page.goto("https://mp.toutiao.com/profile_v4/index", wait_until="networkidle", timeout=30000)
        time.sleep(3)

        if "login" in page.url:
            log("Cookie已过期，需要重新登录")
            browser.close()
            sys.exit(1)

        log(f"登录状态正常")

        # 导航到发布页面
        log("导航到发布页面...")
        page.goto("https://mp.toutiao.com/profile_v4/graphic/publish", wait_until="networkidle", timeout=30000)
        time.sleep(5)

        # 填充标题
        log("填充标题...")
        try:
            title_input = page.wait_for_selector("textarea[placeholder*='标题'], input[placeholder*='标题']", timeout=5000)
            if title_input and title_input.is_visible():
                title_input.click()
                time.sleep(0.5)
                title_input.fill(article['title'])
                log(f"标题已填入: {article['title']}")
        except:
            log("未找到标题输入框")

        # 填充正文
        log("填充正文...")
        try:
            editors = page.query_selector_all("div[contenteditable='true']")
            for editor in editors:
                if editor.is_visible():
                    editor.click()
                    time.sleep(0.5)
                    editor.evaluate("el => el.innerText = ''")
                    time.sleep(0.3)
                    editor.type(article['content'], delay=5)
                    log(f"正文已填入 ({len(article['content'])} 字)")
                    break
        except Exception as e:
            log(f"填充正文失败: {e}")

        # 上传配图（如果有）
        if image_path and os.path.exists(image_path):
            log("上传配图...")
            try:
                img_btn = page.locator(".syl-toolbar-tool.image.static button")
                if img_btn.count() > 0:
                    img_btn.click()
                    time.sleep(2)
                    file_inputs = page.query_selector_all("input[type='file']")
                    for fi in file_inputs:
                        try:
                            fi.set_input_files(image_path)
                            log("配图已上传")
                            time.sleep(3)
                            break
                        except:
                            pass
            except Exception as e:
                log(f"配图上传失败: {e}")

        # 设置封面
        if image_path and os.path.exists(image_path):
            log("设置封面...")
            try:
                single_img = page.locator("label").filter(has_text="单图").first
                if single_img.count() > 0:
                    single_img.click()
                    time.sleep(5)
                    cover_add = page.locator(".article-cover-add")
                    if cover_add.count() > 0 and cover_add.is_visible():
                        cover_add.click()
                        time.sleep(3)
                        try:
                            page.wait_for_selector("#upload-drag-input", state="attached", timeout=10000)
                            file_input = page.locator("#upload-drag-input")
                            file_input.set_input_files(image_path)
                            time.sleep(5)
                            page.keyboard.press("Escape")
                            time.sleep(1)
                            log("封面设置完成")
                        except Exception as e:
                            log(f"封面上传异常: {e}")
            except Exception as e:
                log(f"封面设置失败: {e}")

        # 勾选声明
        log("勾选声明...")
        try:
            view_label = page.locator("label").filter(has_text="个人观点").first
            if view_label.is_visible(timeout=2000):
                view_label.click()
                log("已勾选个人观点")
        except:
            log("勾选个人观点失败")

        # 点击发布
        log("点击发布按钮...")
        try:
            publish_selectors = ["button:has-text('发布文章')", "button:has-text('发布')", ".publish-btn"]
            for sel in publish_selectors:
                btn = page.locator(sel).first
                if btn.is_visible(timeout=2000):
                    btn_text = btn.inner_text().strip()
                    if "预览" not in btn_text:
                        btn.click()
                        log(f"已点击发布: {btn_text}")
                        time.sleep(10)
                        break
        except Exception as e:
            log(f"发布失败: {e}")

        # 保存截图
        log_dir = os.path.join(ROOT_DIR, "logs")
        os.makedirs(log_dir, exist_ok=True)
        screenshot = os.path.join(log_dir, f"publish_{time.strftime('%Y%m%d_%H%M%S')}.png")
        try:
            page.screenshot(path=screenshot)
            log(f"截图已保存: {screenshot}")
        except:
            pass

        browser.close()

    # 发送飞书通知
    notifier = FeishuNotifier(config_file=os.path.join(ROOT_DIR, "config", "account_config.json"))
    notifier.send_notification(
        title="头条文章发布完成",
        body=f"标题: {article['title']}\n字数: {len(article['content'])}\n账号: {config.get('account_name')}",
        notification_type="success"
    )

    log("===== 发布流程结束 =====")


if __name__ == "__main__":
    main()
