#!/usr/bin/env python3
"""Queue a webpage link, or extract content for supported platforms like Zhihu."""
import sys, json, os, subprocess, pathlib, re

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from queue_utils import append_to_queue

ZHIFU_SCRIPT = pathlib.Path.home() / ".openclaw" / "workspace" / "skills" / "zhihu-article-fetcher" / "scripts" / "fetch_article.py"
MEMORY_DIR = pathlib.Path.home() / ".openclaw" / "workspace" / "memory"


def queue_link(url: str, domain: str = "unknown"):
    entry = f"- [网页收藏]({url}) - webpage - {domain}"
    result = append_to_queue(entry)
    return {
        "action": "queue",
        "url": url,
        "type": "webpage",
        "domain": domain,
        "pendingPath": result["pendingPath"],
    }


def extract_zhihu_article(url: str):
    if not ZHIFU_SCRIPT.exists():
        return None
    try:
        result = subprocess.run(
            [sys.executable, str(ZHIFU_SCRIPT), url],
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )
        if result.returncode != 0:
            return None
        payload = json.loads(result.stdout)
        article = payload.get("data", {})
        if not article or not article.get("content"):
            return None
        return article
    except Exception:
        return None


def save_to_memory(url: str, article: dict):
    MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    safe_title = re.sub(r"[^\w\u4e00-\u9fa5]+", "_", article.get("title", "zhihu_article"))[:40]
    filename = f"{safe_title}.md"
    filepath = MEMORY_DIR / filename
    counter = 1
    while filepath.exists():
        filepath = MEMORY_DIR / f"{safe_title}_{counter}.md"
        counter += 1

    lines = [
        f"# {article.get('title', '知乎文章')}",
        "",
        f"- 来源: {url}",
        f"- 抓取方式: {article.get('fetch_method', 'unknown')}",
        f"- 字数: {article.get('word_count', 0)}",
        "",
        "---",
        "",
        article.get("content", ""),
    ]
    filepath.write_text("\n".join(lines), encoding="utf-8")
    return str(filepath)


def process_webpage(url: str, domain: str = "unknown"):
    # Zhihu zhuanlan special handling
    if "zhuanlan.zhihu.com" in url:
        article = extract_zhihu_article(url)
        if article:
            saved_path = save_to_memory(url, article)
            return {
                "action": "extract",
                "url": url,
                "type": "zhihu-article",
                "title": article.get("title", ""),
                "word_count": article.get("word_count", 0),
                "savedPath": saved_path,
            }
        # fallback to queue if extraction failed
    return queue_link(url, domain)


if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else ""
    domain = sys.argv[2] if len(sys.argv) > 2 else "unknown"

    if not url:
        print(json.dumps({"error": "URL required"}), file=sys.stderr)
        sys.exit(1)

    try:
        result = process_webpage(url, domain)
        print(json.dumps(result, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)
