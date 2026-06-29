# GxpCode Skill — S1 web 源拉取
# 读取 sources.yaml，按 parser 字段路由到对应解析器

import importlib
import json
import os
import time
import yaml
from playwright.sync_api import sync_playwright
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SKILL_DIR)


def _get_parser(name: str):
    """动态加载 parser 模块"""
    mod = importlib.import_module(f"parsers.{name}")
    return mod.parse


def run(sources_path: str, gxpcode: str):
    s1_dir = os.path.join(gxpcode, "s1")
    os.makedirs(s1_dir, exist_ok=True)

    with open(sources_path, "r", encoding="utf-8") as f:
        sources = yaml.safe_load(f).get("sources", [])

    web_sources = [s for s in sources if s.get("type") == "web" and s.get("enabled", True)]
    if not web_sources:
        print("No web sources found")
        return

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-blink-features=AutomationControlled"])
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/125.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080},
            locale="zh-CN",
        )

        for src in web_sources:
            name = src["name"]
            url = src["url"]
            jurisdiction = src.get("jurisdiction", "")
            parser_name = src.get("parser", "")

            if not parser_name:
                print(f"  SKIP {name}: no parser configured")
                continue

            print(f"[{name}] {url[:60]}...")
            page = context.new_page()
            try:
                page.goto(url, timeout=60000, wait_until="domcontentloaded")
                time.sleep(5)

                parse_fn = _get_parser(parser_name)
                # 传递 extract 配置给支持该参数的 parser（如 chp_standard 需要 tab 名）
                try:
                    items = parse_fn(page, name, jurisdiction, extract=src.get("extract"))
                except TypeError:
                    items = parse_fn(page, name, jurisdiction)

                path = os.path.join(s1_dir, f"s1_{name.replace('/', '_')}.json")
                with open(path, "w", encoding="utf-8") as f:
                    json.dump(items, f, ensure_ascii=False, indent=2)
                print(f"  → {len(items)} items → {path}")
            except Exception as e:
                print(f"  FAIL: {e}")
            finally:
                page.close()

        browser.close()


if __name__ == "__main__":
    run(sys.argv[1], sys.argv[2])
