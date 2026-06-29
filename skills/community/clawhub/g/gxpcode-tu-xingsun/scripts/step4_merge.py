# GxpCode Skill — ④ 合并 LLM 分析结果到 S4
# 用法: python step4_merge.py gxpcode_data analysis.json
# 从 S3 读取原始数据，与 analysis.json 合并写入 S4，保留 url/date/attachment 等字段

import json
import os
from collections import defaultdict

REQUIRED_FIELDS = ["summary", "tags", "applicability", "reason", "needs_manual_review"]


def _validate(entry: dict, index: int) -> list:
    """校验单条分析结果，返回缺失字段列表"""
    missing = [f for f in REQUIRED_FIELDS if f not in entry]
    if "applicability" in entry and entry["applicability"] not in ("high", "medium", "low", "none"):
        missing.append(f"applicability={entry['applicability']} (invalid)")
    if missing:
        print(f"  [WARN] entry {index}: missing/invalid {missing}")
    return missing


def _normalize(text: str) -> str:
    """标准化文本：替换 \\xa0 为普通空格，移除全角标点前后的空格，合并多余空格并 strip"""
    import re
    text = text.replace("\xa0", " ")
    # 移除中文全角标点前后的空格
    text = re.sub(r"\s+([））\]］」』》〉、，。；：？！…—])", r"\1", text)
    text = re.sub(r"([（(\[［「『《〈])\s+", r"\1", text)
    return " ".join(text.split())


def _load_s3(gxpcode: str) -> dict:
    """读取所有 S3 数据，返回 {(source, normalized_title): item}"""
    s3_dir = os.path.join(gxpcode, "s3")
    s3_items = {}
    if not os.path.exists(s3_dir):
        return s3_items
    for fname in sorted(os.listdir(s3_dir)):
        if not fname.endswith(".json"):
            continue
        with open(os.path.join(s3_dir, fname), "r", encoding="utf-8") as f:
            for item in json.load(f):
                key = (item.get("source", ""), _normalize(item.get("title", "")))
                s3_items[key] = item
    return s3_items


def run(gxpcode: str, analysis_path: str):
    with open(analysis_path, "r", encoding="utf-8") as f:
        analyses = json.load(f)

    if not isinstance(analyses, list):
        print("ERROR: analysis.json must be a JSON array")
        return

    # 校验
    errors = sum(1 for i, a in enumerate(analyses) if _validate(a, i))
    if errors:
        print(f"  {errors} entries have validation issues, continuing anyway")

    # 加载 S3 原始数据
    s3_items = _load_s3(gxpcode)
    if not s3_items:
        print("WARNING: S3 directory is empty or missing, S4 will lack url/date fields")

    # 合并：S3 原始字段 + LLM 分析字段
    merged = []
    s3_matched = set()
    for entry in analyses:
        key = (entry.get("source", ""), _normalize(entry.get("title", "")))
        s3_item = s3_items.get(key, {})
        if s3_item:
            s3_matched.add(key)
        # 以 S3 字段为基础，LLM 分析字段覆盖
        merged_item = dict(s3_item)
        merged_item.update(entry)
        merged.append(merged_item)

    # 检查是否有 S3 条目没有被 analysis.json 覆盖
    unmatched = set(s3_items.keys()) - s3_matched
    if unmatched:
        print(f"  [WARN] {len(unmatched)} S3 items not matched by analysis.json")
        for src, title in list(unmatched)[:3]:
            try:
                print(f"    - [{src}] {title[:50]}...")
            except UnicodeEncodeError:
                print(f"    - [{src}] {title[:30].encode('ascii', 'replace').decode()}...")

    # 按 source 分组写入 S4
    s4_dir = os.path.join(gxpcode, "s4")
    os.makedirs(s4_dir, exist_ok=True)
    for fname in os.listdir(s4_dir):
        if fname.endswith(".json"):
            os.remove(os.path.join(s4_dir, fname))

    src_groups = defaultdict(list)
    for item in merged:
        src_groups[item.get("source", "unknown")].append(item)

    for src, grp in src_groups.items():
        fname = f"s4_{src.replace('/', '_')}.json"
        path = os.path.join(s4_dir, fname)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(grp, f, ensure_ascii=False, indent=2)
        print(f"  {fname}: {len(grp)} items")

    # 写 .done
    with open(os.path.join(s4_dir, ".done"), "w") as f:
        f.write("")

    high = sum(1 for d in merged if d.get("applicability") == "high")
    with_url = sum(1 for d in merged if d.get("url"))
    with_date = sum(1 for d in merged if d.get("date"))
    total = len(merged)
    print(f"s4/: {total} items (high={high}, with_url={with_url}, with_date={with_date})")


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Usage: python step4_merge.py gxpcode_data analysis.json")
        sys.exit(1)
    run(sys.argv[1], sys.argv[2])
