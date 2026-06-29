# GxpCode Skill — Step 1 rss

import json
import os
import yaml
import feedparser
from lib.logger import get_logger
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

logger = get_logger("step1_rss")

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _load_sources(path: str) -> list:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f).get("sources", [])


def _parse_feed(source: dict) -> list:
    """feedparser 解析单个 RSS 源"""
    items = []
    try:
        feed = feedparser.parse(source["url"])
        for entry in feed.entries:
            published = ""
            if hasattr(entry, "published_parsed") and entry.published_parsed:
                published = f"{entry.published_parsed[0]:04d}-{entry.published_parsed[1]:02d}-{entry.published_parsed[2]:02d}"
            items.append({
                "source": source["name"],
                "jurisdiction": source["jurisdiction"],
                "title": getattr(entry, "title", ""),
                "url": getattr(entry, "link", ""),
                "date": published,
                "summary": getattr(entry, "summary", ""),
                "source_type": "rss",
                "confidence": "high",
            })
    except Exception as e:
        logger.error(f"RSS {source['name']} failed: {e}")
    return items


def run(sources_path: str, gxpcode: str):
    """
    处理 type: rss 的源 → 写入 gxpcode_data/s1/{name}.json
    返回 type: web 的源列表，供 Agent 后续处理
    """
    s1_dir = os.path.join(gxpcode, "s1")
    os.makedirs(s1_dir, exist_ok=True)

    sources = _load_sources(sources_path)
    web_sources = []

    for src in sources:
        if not src.get("enabled", True):
            logger.info(f"RSS {src['name']}: disabled, skip")
            continue
        stype = src.get("type", "")
        if stype == "rss":
            items = _parse_feed(src)
            path = os.path.join(s1_dir, f"s1_{src['name'].replace('/', '_')}.json")
            with open(path, "w", encoding="utf-8") as f:
                json.dump(items, f, ensure_ascii=False, indent=2)
            logger.info(f"RSS {src['name']}: {len(items)} items → {path}")
        elif stype == "web":
            web_sources.append({"name": src["name"], "url": src.get("url", ""), "extract": src.get("extract", {})})

    logger.info(f"Web sources pending: {len(web_sources)}")
    return web_sources


if __name__ == "__main__":
    gxpcode = sys.argv[1] if len(sys.argv) > 1 else "gxpcode_data"
    skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sources_path = os.path.join(skill_dir, "resources", "sources.yaml")
    web = run(sources_path, gxpcode)
    print(f"RSS done. Web sources pending: {len(web)}")
