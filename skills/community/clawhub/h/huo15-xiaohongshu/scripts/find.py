#!/usr/bin/env python3
"""火一五小红书"全文搜索" — 跨 drafts / baseline / posts / reviews 找"我写过类似的吗"。

为什么需要
==========
v3.2 加了草稿版本管理后，用户开始持续创作。但写新主题时常有
"之前好像写过类似的"的感觉，没有搜索就只能凭记忆翻文件夹。

搜索范围
========
1. **drafts/<id>/v*.md**       — 所有草稿版本
2. **profile/baseline/*.json** — 代表作样本
3. **posts.jsonl**             — 起草 + 发布历史（标题）
4. **profile/reviews/*.md**    — 历史复盘报告
5. **profile/iter_sessions/**  — 教练改稿轨迹

匹配逻辑
========
- 默认子串匹配（不区分大小写）
- `--regex` 正则匹配
- `--word` 全词匹配（字边界）
- 按"相关度 × 时间"排序

用法
----

    python3 find.py 干皮护肤                       # 找跟"干皮护肤"相关的所有内容
    python3 find.py --regex "(早C晚A|早c晚a)"      # 正则
    python3 find.py 副业 --in drafts               # 只搜草稿
    python3 find.py 节气 --limit 20                # 多展示一些
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

sys.path.insert(0, str(Path(__file__).parent))

from xhs_profile import ProfileStore  # noqa: E402


@dataclass
class Hit:
    source: str               # drafts / baseline / posts / reviews / iter
    location: str             # 文件路径或 ID
    title: str                # 一句话标题
    excerpt: str              # 命中片段
    when: str                 # 创建/更新时间
    score: int                # 命中分（命中次数 + 在标题里加权）

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def _make_matcher(query: str, *, regex: bool, word: bool):
    if regex:
        try:
            pat = re.compile(query, re.IGNORECASE)
        except re.error as e:
            raise SystemExit(f"正则错误：{e}")
    elif word:
        pat = re.compile(rf"(?<![一-鿿\w]){re.escape(query)}(?![一-鿿\w])", re.IGNORECASE)
    else:
        pat = re.compile(re.escape(query), re.IGNORECASE)
    return pat


def _excerpt(text: str, pat: re.Pattern, *, ctx: int = 30) -> str:
    m = pat.search(text)
    if not m:
        return ""
    s = max(0, m.start() - ctx)
    e = min(len(text), m.end() + ctx)
    pre = "…" if s > 0 else ""
    suf = "…" if e < len(text) else ""
    snippet = text[s:e].replace("\n", " ")
    return f"{pre}{snippet}{suf}"


# =====================================================================
# 各数据源搜索
# =====================================================================


def search_drafts(pat: re.Pattern) -> List[Hit]:
    """从 ~/.xiaohongshu/drafts/*/v*.md 搜。"""
    base = os.environ.get("XHS_DRAFTS_DIR")
    drafts_root = Path(os.path.expanduser(base)) if base else Path(
        os.path.expanduser("~/.xiaohongshu/drafts"))
    if not drafts_root.exists():
        return []

    hits: List[Hit] = []
    for d in drafts_root.iterdir():
        if not d.is_dir():
            continue
        meta_p = d / "meta.json"
        meta: Dict[str, Any] = {}
        if meta_p.exists():
            try:
                meta = json.loads(meta_p.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                pass
        for vfile in sorted(d.glob("v*.md"), reverse=True):
            try:
                text = vfile.read_text(encoding="utf-8")
            except OSError:
                continue
            matches = list(pat.finditer(text))
            if not matches:
                continue
            # 标题（取第一行 # 开头）
            title = ""
            for ln in text.splitlines():
                if ln.startswith("# "):
                    title = ln[2:].strip()
                    break
            title_match = pat.search(title or "")
            score = len(matches) + (3 if title_match else 0)
            hits.append(Hit(
                source="drafts",
                location=f"{d.name}/{vfile.name}",
                title=title or meta.get("topic", d.name),
                excerpt=_excerpt(text, pat),
                when=meta.get("updated_at", "") or meta.get("created_at", ""),
                score=score,
            ))
    return hits


def search_baseline(store: ProfileStore, pat: re.Pattern) -> List[Hit]:
    hits: List[Hit] = []
    for p in sorted(store.baseline_dir.glob("*.json")):
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        full = f"{data.get('title','')}\n{data.get('content','')}"
        matches = list(pat.finditer(full))
        if not matches:
            continue
        title_match = pat.search(data.get("title", ""))
        hits.append(Hit(
            source="baseline",
            location=str(p.name),
            title=data.get("title", "(无标题)"),
            excerpt=_excerpt(full, pat),
            when=data.get("published_at", "") or "",
            score=len(matches) + (3 if title_match else 0),
        ))
    return hits


def search_posts(store: ProfileStore, pat: re.Pattern) -> List[Hit]:
    hits: List[Hit] = []
    for p in store.load_posts():
        title = p.get("title", "")
        tags = " ".join(p.get("tags", []) or [])
        full = f"{title}\n{tags}"
        if not pat.search(full):
            continue
        hits.append(Hit(
            source="posts",
            location=p.get("post_uid", ""),
            title=title or "(无标题)",
            excerpt=f"话题：{tags}",
            when=p.get("drafted_at", ""),
            score=2 if pat.search(title) else 1,
        ))
    return hits


def search_reviews(store: ProfileStore, pat: re.Pattern) -> List[Hit]:
    hits: List[Hit] = []
    if not store.reviews_dir.exists():
        return hits
    for p in sorted(store.reviews_dir.glob("review_*.md"), reverse=True):
        try:
            text = p.read_text(encoding="utf-8")
        except OSError:
            continue
        if not pat.search(text):
            continue
        hits.append(Hit(
            source="reviews",
            location=p.name,
            title=p.stem,
            excerpt=_excerpt(text, pat),
            when="",
            score=len(list(pat.finditer(text))),
        ))
    return hits


def search_iter(store: ProfileStore, pat: re.Pattern) -> List[Hit]:
    """iter_sessions 里搜被快照下来的草稿。"""
    iter_root = store.root / "iter_sessions"
    if not iter_root.exists():
        return []
    hits: List[Hit] = []
    for sess in iter_root.iterdir():
        if not sess.is_dir():
            continue
        for snap in sorted(sess.glob("round_*.md"), reverse=True):
            try:
                text = snap.read_text(encoding="utf-8")
            except OSError:
                continue
            if not pat.search(text):
                continue
            title = ""
            for ln in text.splitlines():
                if ln.startswith("# "):
                    title = ln[2:].strip()
                    break
            hits.append(Hit(
                source="iter",
                location=f"{sess.name}/{snap.name}",
                title=title,
                excerpt=_excerpt(text, pat),
                when="",
                score=len(list(pat.finditer(text))),
            ))
            break  # 每个 session 只取一份代表
    return hits


# =====================================================================
# 入口
# =====================================================================


_SOURCE_LABEL = {
    "drafts": "📝 草稿", "baseline": "⭐ 代表作",
    "posts": "📤 发布历史", "reviews": "📊 复盘",
    "iter": "🏋️ 教练快照",
}


def render(hits: List[Hit], query: str, limit: int) -> str:
    if not hits:
        return f"（没找到 {query!r} 相关的内容）"
    parts = [f"🔍 `{query}` — 共 {len(hits)} 处命中（按相关度排序）", ""]
    for h in hits[:limit]:
        parts.append(f"{_SOURCE_LABEL.get(h.source, h.source)}  ·  {h.location}")
        parts.append(f"   📌 {h.title}")
        if h.excerpt:
            parts.append(f"   💬 {h.excerpt}")
        if h.when:
            parts.append(f"   📅 {h.when[:10]}")
        parts.append("")
    if len(hits) > limit:
        parts.append(f"... 省略 {len(hits)-limit} 处（用 --limit 调）")
    return "\n".join(parts)


def main() -> int:
    p = argparse.ArgumentParser(prog="find.py", description="跨数据全文搜索")
    p.add_argument("query", help="搜索词")
    p.add_argument("--in", dest="source", default="all",
                   choices=["all", "drafts", "baseline", "posts", "reviews", "iter"])
    p.add_argument("--regex", action="store_true")
    p.add_argument("--word", action="store_true")
    p.add_argument("--limit", type=int, default=10)
    p.add_argument("--format", choices=["text", "json"], default="text")
    args = p.parse_args()

    pat = _make_matcher(args.query, regex=args.regex, word=args.word)
    store = ProfileStore()

    hits: List[Hit] = []
    if args.source in ("all", "drafts"):
        hits += search_drafts(pat)
    if args.source in ("all", "baseline"):
        hits += search_baseline(store, pat)
    if args.source in ("all", "posts"):
        hits += search_posts(store, pat)
    if args.source in ("all", "reviews"):
        hits += search_reviews(store, pat)
    if args.source in ("all", "iter"):
        hits += search_iter(store, pat)

    # 排序：score 降序，时间降序
    hits.sort(key=lambda h: (-h.score, -len(h.when)))

    if args.format == "json":
        print(json.dumps([h.to_dict() for h in hits[:args.limit]],
                         ensure_ascii=False, indent=2))
    else:
        print(render(hits, args.query, args.limit))
    return 0 if hits else 1


if __name__ == "__main__":
    sys.exit(main())
