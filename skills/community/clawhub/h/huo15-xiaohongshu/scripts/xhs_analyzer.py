"""小红书数据分析 — 输入是本地已抓取好的 JSON / JSONL 数据集，离线跑。

分析维度：
- engagement：互动率（liked + collected + comment）/ 预估曝光（粉丝数或中位数）
- 关键词：标题 / 正文 / 话题标签 的高频词
- 时段：发布时间的小时 × 星期分布
- 爆款特征：高互动笔记的长度、图片数、话题数对比中位数
- 同行对比：多账号间的互动中位数、发帖频次

所有函数都接受 `notes: List[Dict]`（对齐 xhs_parser.Note 的结构），返回纯 dict / DataFrame。
"""

from __future__ import annotations

import collections
import datetime as dt
import json
import os
import re
import statistics as stats
from typing import Any, Dict, Iterable, List, Optional, Tuple

# 可选 pandas
try:
    import pandas as pd  # type: ignore
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False


# --------- 加载 ---------


def load_notes(path: str) -> List[Dict[str, Any]]:
    """支持 .json（一个数组）和 .jsonl（逐行）。"""
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    with open(path, encoding="utf-8") as f:
        text = f.read().strip()
    if not text:
        return []
    if text.startswith("["):
        data = json.loads(text)
        return data if isinstance(data, list) else []
    # jsonl
    out = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            pass
    return out


def dump_notes(notes: List[Dict[str, Any]], path: str, jsonl: bool = False) -> None:
    with open(path, "w", encoding="utf-8") as f:
        if jsonl:
            for n in notes:
                f.write(json.dumps(n, ensure_ascii=False) + "\n")
        else:
            json.dump(notes, f, ensure_ascii=False, indent=2)


# --------- 规范化访问 ---------


def _inter(note: Dict[str, Any]) -> Dict[str, int]:
    i = note.get("interactions") or {}
    return {
        "liked": int(i.get("liked_count", 0) or 0),
        "collected": int(i.get("collected_count", 0) or 0),
        "comment": int(i.get("comment_count", 0) or 0),
        "shared": int(i.get("shared_count", 0) or 0),
    }


def _engagement(note: Dict[str, Any]) -> int:
    i = _inter(note)
    return i["liked"] + i["collected"] + i["comment"] + i["shared"]


def _published_dt(note: Dict[str, Any]) -> Optional[dt.datetime]:
    ts = note.get("raw_time")
    if isinstance(ts, (int, float)) and ts > 0:
        try:
            return dt.datetime.fromtimestamp(ts / 1000)
        except (OverflowError, OSError, ValueError):
            return None
    iso = note.get("published_at", "")
    if iso:
        try:
            return dt.datetime.fromisoformat(iso)
        except ValueError:
            return None
    return None


# --------- 互动分析 ---------


def engagement_summary(notes: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
    values = [_engagement(n) for n in notes]
    if not values:
        return {"count": 0}
    return {
        "count": len(values),
        "mean": round(stats.mean(values), 1),
        "median": stats.median(values),
        "p90": _quantile(values, 0.9),
        "max": max(values),
        "min": min(values),
        "stdev": round(stats.pstdev(values), 1) if len(values) > 1 else 0,
    }


def _quantile(values: List[int], q: float) -> int:
    s = sorted(values)
    idx = int(q * (len(s) - 1))
    return s[idx]


def top_notes(notes: List[Dict[str, Any]], n: int = 10) -> List[Dict[str, Any]]:
    ranked = sorted(notes, key=_engagement, reverse=True)
    out = []
    for note in ranked[:n]:
        inter = _inter(note)
        out.append({
            "note_id": note.get("note_id", ""),
            "title": (note.get("title") or note.get("content", ""))[:60],
            "liked": inter["liked"],
            "collected": inter["collected"],
            "comment": inter["comment"],
            "engagement": _engagement(note),
            "url": note.get("url") or f"https://www.xiaohongshu.com/explore/{note.get('note_id', '')}",
        })
    return out


# --------- 关键词 / 话题 ---------


_PUNCT_RE = re.compile(r"[\s\.,;:!?\"'()\[\]{}<>/\\|\-_=+*&^%$#@~`—…！？，。、：；""''（）【】《》〈〉「」·]+")


def keyword_frequency(notes: Iterable[Dict[str, Any]], *, use_jieba: bool = True,
                      min_len: int = 2, top: int = 30,
                      stopwords: Optional[Iterable[str]] = None) -> List[Tuple[str, int]]:
    """标题 + 正文 + 话题 的词频统计。有 jieba 用 jieba，否则退化为按标点切。"""
    stop = set(stopwords or _DEFAULT_STOPWORDS)
    counter: collections.Counter = collections.Counter()

    text_parts: List[str] = []
    for note in notes:
        text_parts.append(note.get("title", "") or "")
        text_parts.append(note.get("content", "") or "")
        text_parts.extend(note.get("tags", []) or [])

    blob = "\n".join(text_parts)

    tokens: List[str] = []
    if use_jieba:
        try:
            import jieba  # type: ignore
            tokens = list(jieba.cut_for_search(blob))
        except ImportError:
            tokens = []

    if not tokens:
        # 退化方案：按标点/空格切
        tokens = _PUNCT_RE.split(blob)

    for tok in tokens:
        tok = tok.strip().lower()
        if len(tok) < min_len or tok in stop or tok.isdigit():
            continue
        counter[tok] += 1

    return counter.most_common(top)


_DEFAULT_STOPWORDS = {
    "the", "a", "an", "of", "in", "on", "and", "or", "is", "are", "to", "for", "with", "at",
    "我", "你", "他", "她", "它", "我们", "你们", "他们", "的", "了", "吧", "啊", "呀", "哦",
    "这", "那", "都", "也", "就", "还", "再", "说", "说一", "但是", "而且", "所以", "因为",
    "什么", "怎么", "如何", "为什么", "以及", "一个", "一下", "一点", "一些", "真的", "可以", "能够",
    "分享", "今天", "一下", "大家", "朋友", "宝贝", "姐妹", "姐妹们",
    "http", "https", "www", "com", "cn", "xhs",
}


def tag_frequency(notes: Iterable[Dict[str, Any]], top: int = 30) -> List[Tuple[str, int]]:
    counter: collections.Counter = collections.Counter()
    for note in notes:
        for tag in note.get("tags", []) or []:
            if tag:
                counter[tag.strip()] += 1
    return counter.most_common(top)


# --------- 时间分布 ---------


def posting_time_heatmap(notes: Iterable[Dict[str, Any]]) -> Dict[str, Dict[int, int]]:
    """星期 × 小时 发布频次。星期用中文名。"""
    week = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    grid: Dict[str, Dict[int, int]] = {w: {h: 0 for h in range(24)} for w in week}
    for note in notes:
        d = _published_dt(note)
        if not d:
            continue
        grid[week[d.weekday()]][d.hour] += 1
    return grid


def best_posting_windows(notes: Iterable[Dict[str, Any]], top: int = 5) -> List[Dict[str, Any]]:
    """按 (星期 × 小时) 的笔记平均互动排序，给发文时段建议。"""
    buckets: Dict[Tuple[int, int], List[int]] = collections.defaultdict(list)
    for note in notes:
        d = _published_dt(note)
        if not d:
            continue
        buckets[(d.weekday(), d.hour)].append(_engagement(note))
    ranked = []
    for (w, h), vals in buckets.items():
        if len(vals) < 2:
            continue
        ranked.append({
            "weekday": ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][w],
            "hour": h,
            "count": len(vals),
            "median_engagement": stats.median(vals),
            "mean_engagement": round(stats.mean(vals), 1),
        })
    ranked.sort(key=lambda x: x["median_engagement"], reverse=True)
    return ranked[:top]


# --------- 爆款特征 ---------


def viral_pattern(notes: List[Dict[str, Any]], percentile: float = 0.8) -> Dict[str, Any]:
    """对比 top 20% 笔记与其他笔记的特征差异。"""
    if len(notes) < 5:
        return {"note": "样本太少，至少 5 条"}
    scored = sorted(notes, key=_engagement, reverse=True)
    cut = max(1, int(len(scored) * (1 - percentile)))
    top = scored[:cut]
    rest = scored[cut:]

    def _stats(group: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not group:
            return {}
        titles = [len(n.get("title", "") or "") for n in group]
        contents = [len(n.get("content", "") or "") for n in group]
        imgs = [len(n.get("images", []) or []) for n in group]
        tags = [len(n.get("tags", []) or []) for n in group]
        return {
            "count": len(group),
            "title_len_med": int(stats.median(titles)) if titles else 0,
            "content_len_med": int(stats.median(contents)) if contents else 0,
            "images_med": int(stats.median(imgs)) if imgs else 0,
            "tags_med": int(stats.median(tags)) if tags else 0,
            "engagement_med": int(stats.median([_engagement(n) for n in group])),
        }

    return {
        "top": _stats(top),
        "rest": _stats(rest),
    }


# --------- 综合报告 ---------


def full_report(notes: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {
        "sample_size": len(notes),
        "engagement_summary": engagement_summary(notes),
        "top_notes": top_notes(notes, 10),
        "keyword_top30": keyword_frequency(notes, top=30),
        "tag_top30": tag_frequency(notes, top=30),
        "posting_time_heatmap": posting_time_heatmap(notes),
        "best_windows": best_posting_windows(notes, 5),
        "viral_pattern": viral_pattern(notes),
    }


def report_to_markdown(report: Dict[str, Any]) -> str:
    """把分析报告渲染成 Markdown，方便直接写到笔记里。"""
    parts: List[str] = []
    parts.append(f"# 小红书数据分析报告\n\n样本量：**{report['sample_size']}** 条笔记\n")

    es = report["engagement_summary"]
    if es.get("count"):
        parts.append("## 互动概览\n")
        parts.append(f"- 平均互动：**{es['mean']}**")
        parts.append(f"- 中位数：{es['median']}")
        parts.append(f"- P90：{es['p90']}")
        parts.append(f"- 最高：{es['max']} / 最低：{es['min']}\n")

    parts.append("## Top 10 笔记\n")
    parts.append("| 排名 | 标题 | 点赞 | 收藏 | 评论 | 互动合计 |")
    parts.append("|---|---|---|---|---|---|")
    for idx, t in enumerate(report["top_notes"], 1):
        title = (t["title"] or "(无标题)").replace("|", "/")
        parts.append(f"| {idx} | {title} | {t['liked']} | {t['collected']} | {t['comment']} | **{t['engagement']}** |")

    parts.append("\n## Top 30 关键词\n")
    parts.append(", ".join(f"`{k}`({v})" for k, v in report["keyword_top30"][:30]))

    parts.append("\n\n## Top 30 话题标签\n")
    parts.append(", ".join(f"#{k}({v})" for k, v in report["tag_top30"][:30]))

    parts.append("\n\n## 最佳发文时段（按中位互动）\n")
    for w in report["best_windows"]:
        parts.append(f"- {w['weekday']} {w['hour']:02d}:00 — 中位互动 {w['median_engagement']}（{w['count']} 条样本）")

    vp = report["viral_pattern"]
    if isinstance(vp, dict) and "top" in vp and "rest" in vp:
        parts.append("\n## 爆款 vs 普通")
        parts.append(f"- 爆款 ({vp['top']['count']} 条): 标题 {vp['top']['title_len_med']} 字 / 正文 "
                     f"{vp['top']['content_len_med']} 字 / {vp['top']['images_med']} 图 / "
                     f"{vp['top']['tags_med']} 话题 / 互动中位 {vp['top']['engagement_med']}")
        parts.append(f"- 普通 ({vp['rest']['count']} 条): 标题 {vp['rest']['title_len_med']} 字 / 正文 "
                     f"{vp['rest']['content_len_med']} 字 / {vp['rest']['images_med']} 图 / "
                     f"{vp['rest']['tags_med']} 话题 / 互动中位 {vp['rest']['engagement_med']}")

    return "\n".join(parts) + "\n"
