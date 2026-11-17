#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
趋势知识库与调味料注入（M7a）

职责：
1. 接收上层抓回来的原始文本（HTML/纯文本），离线**提炼**成若干条短要点
2. 按兴趣主题归档，去重、限量、可清除
3. 在线只注入一句「趋势调味料」，默认 ≤50 Token

纪律：
- 原始内容**绝不进上下文**，只留提炼后的要点（红线：能不注入就不注入）
- 每条要点记来源，可追溯
- 主题来自用户画像「互动偏好.喜欢的话题」，不主观臆测用户兴趣
"""

import json
import re
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

# 允许 `python scripts/trends/store.py` 直接跑（此时 sys.path[0] 是脚本所在目录）
_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from scripts.core import settings as core_settings  # noqa: E402
from scripts.core.storage import read_json, write_json  # noqa: E402
from scripts.pipeline.injector import estimate_tokens, truncate_to_tokens  # noqa: E402

# 热度信号词：命中说明这句话在说「什么东西火了」
HEAT_WORDS = ("火了", "爆火", "爆", "热搜", "刷屏", "出圈", "同款", "流行",
              "梗", "绝绝子", "yyds", "破防", "上头", "都在", "爆了", "疯传")

# 广告与导航噪声：命中即降权，避免把招商信息当成热点
NOISE_WORDS = ("广告", "招商", "联系电话", "扫码", "关注我们", "版权", "备案",
               "登录", "注册", "下载app", "立即购买", "优惠券")

# 引号内的短语通常是流行语本体
_QUOTED = re.compile(r"[“\"'「『【]([^”\"'」』】]{2,12})[”\"'」』】]")

_TAG_RE = re.compile(r"<[^>]{1,200}>")
_CJK_RUN = re.compile(r"[\u4e00-\u9fff]{2,}")

STOPWORDS = set("""
的 了 是 我 你 他 她 它 我们 你们 他们 在 有 就 不 也 都 很 到 说 要 去 会 着 没 看 好 自己 这 那
什么 怎么 为什么 一个 这个 那个 可以 因为 所以 但是 然后 还有 就是 一下 一点 现在 时候 知道 觉得
""".split())


def _now() -> str:
    return datetime.now().isoformat(timespec="seconds")


def strip_html(raw: str) -> str:
    """去掉 HTML 标签与脚本块，只留文字

    块级标签（p/div/br/li…）先换成换行再剥标签——否则整页会糊成一长句，
    正文被页头广告挤到后面，提炼出来的第一条反而是广告。
    """
    text = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", raw or "")
    text = re.sub(r"(?i)<\s*/?\s*(?:p|div|br|li|tr|td|h[1-6]|section|article)\b[^>]*>",
                  "\n", text)
    text = _TAG_RE.sub(" ", text)
    text = re.sub(r"&nbsp;?|&amp;|&lt;|&gt;|&quot;", " ", text)
    return re.sub(r"[ \t]{2,}", " ", text).strip()


def _jaccard(a: str, b: str) -> float:
    sa, sb = set(a), set(b)
    if not sa or not sb:
        return 0.0
    return len(sa & sb) / len(sa | sb)


def buzzwords(raw: str, top_k: int = 3) -> List[str]:
    """提取流行语候选：引号内短语优先，其次高频实词"""
    text = strip_html(raw)
    counter: Counter = Counter()
    for m in _QUOTED.finditer(text):
        w = m.group(1).strip()
        if 2 <= len(w) <= 12 and not w.isdigit():
            counter[w] += 3          # 引号里的加权
    for run in _CJK_RUN.findall(text):
        for n in (2, 3, 4):
            for i in range(len(run) - n + 1):
                g = run[i:i + n]
                if g not in STOPWORDS:
                    counter[g] += 1
    picked: List[str] = []
    for w, c in counter.most_common(200):
        if c < 3:
            break
        if any(w in p or p in w for p in picked):
            continue
        picked.append(w)
        if len(picked) >= top_k:
            break
    return picked


def digest(raw: str, topic: str = "", max_points: int = 4, point_len: int = 22) -> List[str]:
    """把抓取回来的原始文本提炼成数条短要点

    打分：含主题词 +2；含热度词 +1；长度适中 +1；与已选要点重复的直接丢弃。
    """
    text = strip_html(raw)
    if not text:
        return []

    candidates = [s.strip() for s in re.split(r"[。！？!?\n；;]", text) if 8 <= len(s.strip()) <= 80]
    scored: List[tuple] = []
    for s in candidates:
        score = 0.0
        if topic and topic in s:
            score += 2
        score += sum(1 for w in HEAT_WORDS if w in s)
        if 12 <= len(s) <= 45:
            score += 1
        # 纯链接/纯数字/广告导航直接判负
        if re.match(r"^https?://", s) or s.count("/") > 3:
            score -= 2
        if any(w in s for w in NOISE_WORDS):
            score -= 3
        scored.append((score, s))
    scored.sort(key=lambda kv: -kv[0])

    points: List[str] = []
    for _score, s in scored:
        if s and len(s) > point_len:
            s = s[:point_len].rstrip("，,、 ")
        if not s:
            continue
        if any(_jaccard(s, p) > 0.6 for p in points):
            continue
        points.append(s)
        if len(points) >= max_points:
            break
    return points


class TrendStore:
    """趋势知识库"""

    def __init__(self, data_dir: Optional[str] = None):
        self.data_dir = core_settings.resolve_data_dir(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.file = self.data_dir / "trends.json"
        self.max_items = 200

    def _load(self) -> Dict[str, Any]:
        data = read_json(self.file, {"items": [], "updated_at": None})
        return data if isinstance(data, dict) else {"items": [], "updated_at": None}

    def _save(self, data: Dict[str, Any]) -> None:
        data["updated_at"] = _now()
        write_json(self.file, data)

    # ---------- 入库 ----------

    def ingest(self, raw: str, topic: str = "", source: str = "") -> Dict[str, Any]:
        """提炼并入库（去重：同主题同要点只刷新时间戳）"""
        points = digest(raw, topic=topic)
        if not points:
            return {"added": 0, "reason": "无可提炼内容"}

        data = self._load()
        items = data.get("items", [])
        added = 0
        for p in points:
            hit = next((it for it in items if it["topic"] == topic and it["point"] == p), None)
            if hit:
                hit["ts"] = _now()
                hit["hits"] = int(hit.get("hits", 1)) + 1
            else:
                items.append({"topic": topic, "point": p, "source": source,
                              "ts": _now(), "hits": 1})
                added += 1
        data["items"] = items[-self.max_items:]
        self._save(data)
        return {"added": added, "points": points}

    # ---------- 查询 ----------

    def topics(self) -> List[str]:
        data = self._load()
        seen: List[str] = []
        for it in data.get("items", []):
            if it.get("topic") and it["topic"] not in seen:
                seen.append(it["topic"])
        return seen

    def by_topic(self, topic: str, limit: int = 3) -> List[Dict[str, Any]]:
        items = [it for it in self._load().get("items", []) if it.get("topic") == topic]
        items.sort(key=lambda it: (-int(it.get("hits", 1)), it.get("ts", "")))
        return items[:limit]

    # ---------- 在线注入 ----------

    def seasoning(self, topics: Optional[Sequence[str]] = None,
                  budget: Optional[int] = None, per_topic: int = 1) -> str:
        """一句趋势调味料（默认 50 Token 硬预算）

        topics 为空时，自动取用户画像里「喜欢的话题」。
        预算不够就少带几个主题，绝不挤占其它模块。
        """
        limit = int(budget if budget is not None
                    else core_settings.budget(str(self.data_dir), "趋势调味料"))
        if not topics:
            try:
                from scripts.user.profile import UserProfileStore
                topics = (UserProfileStore(str(self.data_dir)).get()
                          .get("互动偏好", {}).get("喜欢的话题") or [])
            except Exception:  # noqa: BLE001 - 画像不可用就退化成不注入
                topics = []

        chunks: List[str] = []
        for t in topics or []:
            items = self.by_topic(t, limit=per_topic)
            if not items:
                continue
            chunk = f"{t}：" + "、".join(it["point"] for it in items)
            trial = "；".join(chunks + [chunk])
            if estimate_tokens(trial) > limit:
                break
            chunks.append(chunk)
        if not chunks:
            return ""
        return truncate_to_tokens("；".join(chunks), limit)

    # ---------- 数据主权 ----------

    def purge(self, topic: Optional[str] = None) -> int:
        data = self._load()
        items = data.get("items", [])
        if topic is None:
            removed = len(items)
            data["items"] = []
        else:
            left = [it for it in items if it.get("topic") != topic]
            removed = len(items) - len(left)
            data["items"] = left
        self._save(data)
        return removed

    def export(self) -> str:
        return json.dumps(self._load(), ensure_ascii=False, indent=2)


if __name__ == "__main__":
    import sys
    store = TrendStore()
    if len(sys.argv) > 2 and sys.argv[1] == "ingest":
        raw = Path(sys.argv[2]).read_text(encoding="utf-8", errors="ignore")
        print(json.dumps(store.ingest(raw, topic=sys.argv[3] if len(sys.argv) > 3 else ""),
                         ensure_ascii=False, indent=2))
    else:
        print(json.dumps({"topics": store.topics(), "seasoning": store.seasoning()},
                         ensure_ascii=False, indent=2))
