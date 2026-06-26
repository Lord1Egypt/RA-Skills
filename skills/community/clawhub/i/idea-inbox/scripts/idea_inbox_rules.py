#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from urllib.parse import urlparse

CATEGORY_ENUM = ["产品", "技术", "商业", "管理", "内容", "生活", "其他"]

TAG_CANDIDATES = [
    "AI",
    "增长",
    "飞书自动化",
    "爬虫",
    "管理",
    "招聘",
    "内容创作",
    "电商",
    "数据",
    "工程效率",
    "自动化",
]

CATEGORY_RULES: list[tuple[str, str]] = [
    (r"飞书|lark|bitable|多维表格|webhook|机器人", "技术"),
    (r"爬虫|抓取|解析|scrape|crawler|cdp|selenium", "技术"),
    (r"数据库|mysql|redis|kafka|es|elasticsearch|后端|api|接口|服务", "技术"),
    (r"招聘|面试|候选人|jd|绩效|管理|带人", "管理"),
    (r"增长|转化|留存|拉新|gmv|roi|投放|渠道", "商业"),
    (r"产品|需求|PRD|原型|交互|功能|看板", "产品"),
    (r"写作|文章|脚本|标题|视频|播客|内容", "内容"),
    (r"减脂|健身|饮食|跑步|步数|睡眠|健康", "生活"),
]


def _extract_domains(text: str) -> list[str]:
    out: list[str] = []
    # urls
    for m in re.findall(r"https?://[^\s]+", text):
        try:
            d = urlparse(m).netloc
            if d:
                out.append(d)
        except Exception:
            pass
    # bare domains
    for m in re.findall(r"\b[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b", text):
        if m and m not in out:
            out.append(m)
    # keep short
    out2: list[str] = []
    for d in out:
        d = d.strip().lower()
        if len(d) > 40:
            continue
        out2.append(d)
    return out2[:2]


def classify_rules(text: str) -> dict:
    t = text.strip()
    category = "其他"
    for pat, cat in CATEGORY_RULES:
        if re.search(pat, t, flags=re.I):
            category = cat
            break

    tags: list[str] = []

    # domain tags
    tags.extend(_extract_domains(t))

    # keyword tags
    for tag in TAG_CANDIDATES:
        if tag in t and tag not in tags:
            tags.append(tag)

    # heuristic tags
    if re.search(r"注册|登录|账号", t) and "账号注册" not in tags:
        tags.append("账号注册")

    if re.search(r"养号", t) and "养号" not in tags:
        tags.append("养号")

    if not tags:
        tags = ["其他"]

    tags = [x.strip()[:24] for x in tags if x.strip()]
    tags = tags[:5]

    summary = t
    # strip prefix if present
    summary = re.sub(r"^(idea:|灵感：)\s*", "", summary, flags=re.I).strip()
    if len(summary) > 120:
        summary = summary[:120]

    return {"category": category if category in CATEGORY_ENUM else "其他", "tags": tags, "summary": summary}


def main() -> None:
    text = sys.stdin.read().strip()
    if not text:
        print(json.dumps({"error": "empty input"}, ensure_ascii=False))
        sys.exit(2)
    out = classify_rules(text)
    print(json.dumps(out, ensure_ascii=False))


if __name__ == "__main__":
    main()
