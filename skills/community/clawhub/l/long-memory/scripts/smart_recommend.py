#!/usr/bin/env python3
"""智能推荐：基于当前对话推荐相关历史记忆"""

import argparse
import json
import re
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent))
from lib.filelock import safe_read

DEFAULT_MEMORY_DIR = Path.home() / ".openclaw" / "workspace" / "memory"


def extract_keywords(text: str, top_n: int = 10) -> list[str]:
    """从文本中提取关键词"""
    # 中文 2-4 字片段
    cjk = re.findall(r'[\u4e00-\u9fff]{2,4}', text)
    # 英文单词
    en = re.findall(r'[a-zA-Z]{3,}', text.lower())
    all_words = cjk + en
    
    # 过滤停用词
    stopwords = {"这个", "那个", "什么", "怎么", "为什么", "可以", "已经",
                 "应该", "可能", "没有", "不是", "还是", "就是", "但是",
                 "因为", "所以", "如果", "虽然", "不过", "然后", "或者",
                 "the", "and", "for", "but", "not", "this", "that", "with"}
    
    filtered = [w for w in all_words if w not in stopwords and len(w) >= 2]
    return [w for w, _ in Counter(filtered).most_common(top_n)]


def recommend(memory_dir: Path, query: str, top_n: int = 5, days: int | None = None) -> list[dict]:
    """基于输入文本推荐相关历史记忆"""
    conv_dir = memory_dir / "conversations"
    if not conv_dir.exists():
        return []

    cutoff = datetime.now() - timedelta(days=days) if days else None
    keywords = extract_keywords(query)

    scored = []
    for fp in sorted(conv_dir.glob("*.md"), reverse=True):
        if cutoff:
            try:
                file_date = datetime.strptime(fp.stem, "%Y-%m-%d")
                if file_date < cutoff:
                    continue
            except ValueError:
                continue

        content = fp.read_text(encoding="utf-8")

        # 关键词匹配评分
        score = 0
        matched_keywords = []
        for kw in keywords:
            count = content.lower().count(kw.lower())
            if count > 0:
                score += count
                matched_keywords.append(kw)

        # 话题匹配加分
        topics = re.findall(r'###\s*话题[：:]\s*(.+)', content)
        for topic in topics:
            for kw in keywords:
                if kw.lower() in topic.lower():
                    score += 3  # 话题匹配权重更高
                    if kw not in matched_keywords:
                        matched_keywords.append(kw)

        # 标签匹配加分
        tags = re.findall(r'\*\*标签[：:]\*\*\s*(.+)', content)
        for tag_line in tags:
            for tag in tag_line.split("，"):
                tag = tag.strip()
                for kw in keywords:
                    if kw.lower() in tag.lower():
                        score += 2
                        if kw not in matched_keywords:
                            matched_keywords.append(kw)

        # 决策内容加分
        if "**关键决策" in content:
            score += 1

        if score > 0:
            # 提取相关片段
            snippets = extract_relevant_snippets(content, keywords, max_snippets=3)

            scored.append({
                "date": fp.stem,
                "score": score,
                "matched_keywords": list(set(matched_keywords)),
                "topics": [t.strip() for t in topics],
                "tags": list(set(t.strip() for tl in tags for t in tl.split("，") if t.strip())),
                "snippets": snippets,
            })

    # 按分数排序
    scored.sort(key=lambda x: -x["score"])
    return scored[:top_n]


def extract_relevant_snippets(content: str, keywords: list[str], max_snippets: int = 3) -> list[str]:
    """提取包含关键词的上下文片段"""
    lines = content.split("\n")
    snippets = []
    used_lines = set()

    for kw in keywords:
        for i, line in enumerate(lines):
            if i in used_lines:
                continue
            if kw.lower() in line.lower():
                # 收集上下文
                start = max(0, i - 1)
                end = min(len(lines), i + 3)
                snippet = "\n".join(lines[start:end]).strip()
                if snippet and len(snippet) <= 300:
                    snippets.append(snippet)
                    for j in range(start, end):
                        used_lines.add(j)
                    if len(snippets) >= max_snippets:
                        return snippets

    return snippets


def print_recommendations(recommendations: list[dict]):
    if not recommendations:
        print("📭 没有找到相关历史记忆")
        return

    print("=" * 60)
    print(f"💡 智能推荐（{len(recommendations)} 条相关记忆）")
    print("=" * 60)

    for i, rec in enumerate(recommendations, 1):
        print(f"\n📌 [{i}] {rec['date']}（相关度: {'⭐' * min(rec['score'], 5)}）")
        if rec["topics"]:
            print(f"   话题: {', '.join(rec['topics'])}")
        if rec["tags"]:
            print(f"   标签: {', '.join(rec['tags'])}")
        print(f"   匹配: {', '.join(rec['matched_keywords'])}")

        if rec["snippets"]:
            print(f"   💬 相关片段:")
            for snippet in rec["snippets"][:2]:
                # 截断长行
                clean = snippet.replace("**用户：**", "👤").replace("**助手：**", "🤖")
                for line in clean.split("\n")[:4]:
                    if line.strip():
                        print(f"      {line[:80]}")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="智能推荐")
    p.add_argument("query", help="当前对话内容或关键词")
    p.add_argument("--memory-dir", default=None)
    p.add_argument("--top", type=int, default=5)
    p.add_argument("--days", type=int, default=None)
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    md = args.memory_dir if args.memory_dir else DEFAULT_MEMORY_DIR
    md = Path(md)
    recs = recommend(md, args.query, args.top, args.days)

    if args.json:
        print(json.dumps(recs, ensure_ascii=False, indent=2))
    else:
        print_recommendations(recs)
