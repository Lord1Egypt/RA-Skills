#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run.py
News Brief Skill 一键运行入口

用法：
  python run.py              # 使用 config.yaml + 环境变量
  python run.py --preview    # 只打印，不保存文件
"""

import argparse
import logging
import os
import sys
import yaml
from datetime import datetime
from pathlib import Path


def load_dotenv():
    """自动加载 .env 文件中的环境变量"""
    env_path = Path(__file__).parent / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        os.environ.setdefault(key.strip(), val.strip())

# ============================================================
# 路径
# ============================================================
BASE_DIR   = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "output"
LOG_DIR    = BASE_DIR / "logs"


def setup_logging():
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_file = LOG_DIR / f"{datetime.now().strftime('%Y-%m-%d')}.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(str(log_file), encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )


def load_config() -> dict:
    cfg_path = BASE_DIR / "config.yaml"
    if not cfg_path.exists():
        print("❌ 找不到 config.yaml，请参考 SKILL.md 创建配置文件")
        sys.exit(1)
    with open(cfg_path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def get_api_keys() -> tuple[str, str]:
    serper_key   = os.environ.get("SERPER_API_KEY", "")
    deepseek_key = os.environ.get("DEEPSEEK_API_KEY", "")

    missing = []
    if not serper_key:
        missing.append("SERPER_API_KEY")
    if not deepseek_key:
        missing.append("DEEPSEEK_API_KEY")

    if missing:
        print(f"❌ 缺少环境变量：{', '.join(missing)}")
        print("   请参考 SKILL.md 设置 API Keys")
        sys.exit(1)

    return serper_key, deepseek_key


def main():
    parser = argparse.ArgumentParser(description="News Brief Skill")
    parser.add_argument("--preview", action="store_true", help="只打印，不保存文件")
    args = parser.parse_args()

    load_dotenv()   # 自动读取 .env，无需手动 source
    setup_logging()

    # ── 加载配置 ─────────────────────────────────────────────
    config       = load_config()
    categories   = config.get("categories", ["科技"])[:3]
    news_per_cat = config.get("news_per_category", 6)
    time_range   = config.get("time_range", "24h")

    serper_key, deepseek_key = get_api_keys()

    logging.info(f"{'='*50}")
    logging.info(f"📰 News Brief  分类：{' / '.join(categories)}  每类{news_per_cat}条  时间：{time_range}")
    logging.info(f"{'='*50}")

    # ── 抓取新闻 ─────────────────────────────────────────────
    from fetch import fetch_all
    all_news = fetch_all(categories, news_per_cat, serper_key, deepseek_key, time_range)

    total = sum(len(v) for v in all_news.values())
    if total == 0:
        logging.error("❌ 未抓取到任何新闻，请检查 API Key 或网络")
        sys.exit(1)

    logging.info(f"\n✅ 共抓取 {total} 条新闻")

    # ── 生成简报 ─────────────────────────────────────────────
    from brief import generate_brief
    logging.info("📝 生成简报...")
    brief_text = generate_brief(all_news, config, deepseek_key)

    # ── 输出 ─────────────────────────────────────────────────
    print("\n" + "="*50)
    print(brief_text)
    print("="*50 + "\n")

    # 始终确保 output 目录存在（相对于 SKILL 目录，不受工作目录影响）
    out_dir_cfg = config.get("output_dir", "./output")
    out_dir = (BASE_DIR / out_dir_cfg).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    if not args.preview:
        today    = datetime.now().strftime("%Y-%m-%d")
        out_path = out_dir / f"{today}_brief.txt"
        out_path.write_text(brief_text, encoding="utf-8")
        logging.info(f"💾 简报已保存：{out_path}")
    else:
        logging.info(f"📁 output 目录：{out_dir}（预览模式不保存文件）")

    logging.info(f"{'='*50}")
    logging.info(f"✅ 完成！")
    logging.info(f"{'='*50}")


if __name__ == "__main__":
    main()
