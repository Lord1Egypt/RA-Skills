#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微头条发布脚本 - 快速发布短内容
"""

import sys
import os
import time
import json
import argparse

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT_DIR)

from core.article_generator import ArticleGenerator
from core.image_generator import ImageGenerator
from core.feishu_notifier import FeishuNotifier


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
        return None


def main():
    parser = argparse.ArgumentParser(description="微头条发布脚本")
    parser.add_argument("--content", "-c", type=str, help="自定义微头条内容")
    parser.add_argument("--topic", "-t", type=str, help="话题")
    parser.add_argument("--image", "-i", type=str, help="配图文件路径")
    parser.add_argument("--auto-topic", action="store_true", help="自动从话题邀请中选题")
    args = parser.parse_args()

    config = load_config()
    if not config:
        sys.exit(1)

    log("===== 微头条发布开始 =====")

    # 1. 确定内容
    if args.content:
        content = args.content
        topic = args.topic or ""
    elif args.auto_topic:
        # 从话题邀请中获取
        from core.publisher import Publisher
        pub = Publisher(config_file=os.path.join(ROOT_DIR, "config", "account_config.json"))
        hot_topic = pub.get_hot_topic()
        if not hot_topic:
            log("没有获取到话题邀请，退出")
            sys.exit(1)
        topic = hot_topic.get('title', '')
        # 生成200字左右的微头条
        gen = ArticleGenerator()
        article = gen.generate_article(topic)
        # 截取前200字
        content = article['content'][:200] + "..."
        log(f"自动选题: {topic}")
    else:
        log("[错误] 请指定 --content 或 --auto-topic")
        sys.exit(1)

    log(f"内容长度: {len(content)} 字")

    # 2. 获取配图
    image_path = args.image
    if not image_path:
        img_dir = os.path.join(ROOT_DIR, "generated-images")
        if os.path.exists(img_dir):
            img_files = [f for f in os.listdir(img_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
            if img_files:
                image_path = os.path.join(img_dir, img_files[0])

    # 3. 使用 Playwright 发布到微头条
    from playwright.sync_api import sync_playwright

    # 加载Cookie
    cookie_file = config.get("cookie_file")
    if not cookie_file or not os.path.exists(cookie_file):
        log(f"[错误] Cookie文件不存在: {cookie_file}")
        sys.exit(1)

    with open(cookie_file, 'r', encoding='utf-8') as f:
        cookies_data = json.load(f)

    cookies = []
    for c in cookies_data:
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
        cookies.append(cookie)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, args=["--no-sandbox"])
        ctx = browser.new_context(
            viewport={"width": 1440, "height": 900},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        )
        ctx.add_cookies(cookies)
        page = ctx.new_page()

        # 导航到微头条发布页
        log("导航到微头条发布页...")
        page.goto("https://mp.toutiao.com/profile_v4/weitoutiao/publish", wait_until="networkidle", timeout=30000)
        time.sleep(5)

        if "login" in page.url:
            log("Cookie已过期")
            browser.close()
            sys.exit(1)

        # 填写内容
        log("填写微头条内容...")
        try:
            editor = page.wait_for_selector("div[contenteditable='true']", timeout=10000)
            if editor and editor.is_visible():
                editor.click()
                time.sleep(0.5)
                editor.type(content, delay=10)
                log(f"内容已填入 ({len(content)} 字)")
        except Exception as e:
            log(f"填写内容失败: {e}")

        # 上传配图（如果有）
        if image_path and os.path.exists(image_path):
            log("上传配图...")
            try:
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

        # 发布
        log("点击发布...")
        time.sleep(2)
        try:
            publish_btn = page.locator("button").filter(has_text="发布").first
            if publish_btn.count() > 0 and publish_btn.is_visible(timeout=2000):
                publish_btn.click()
                log("已点击发布")
                time.sleep(5)
        except Exception as e:
            log(f"发布失败: {e}")

        # 截图
        log_dir = os.path.join(ROOT_DIR, "logs")
        os.makedirs(log_dir, exist_ok=True)
        try:
            page.screenshot(path=os.path.join(log_dir, f"weitoutiao_{time.strftime('%Y%m%d_%H%M%S')}.png"))
        except:
            pass

        browser.close()

    # 飞书通知
    notifier = FeishuNotifier(config_file=os.path.join(ROOT_DIR, "config", "account_config.json"))
    notifier.send_notification(
        title="微头条发布完成",
        body=f"内容: {content[:50]}...\n话题: {topic}\n账号: {config.get('account_name')}",
        notification_type="success"
    )

    log("===== 微头条发布结束 =====")


if __name__ == "__main__":
    main()
