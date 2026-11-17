#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
趋势源路由（M7a）

**为什么不做成平台全覆盖的抓取路由器**：那种定位是「给 Agent 免 Key 接入全网」，
上百个平台、故障转移、安装器。但 love-companion 要的不是全网接入能力，
而是**一句能跟恋人开口的话**。堆一张大平台注册表只会得到一个没人看的配置表。

所以这里只关心两件事：
1. **这个话题值不值得跟恋人聊**（可聊度）——财经/时政/社会新闻天然不适合亲密对话，
   美食/旅行/影视/宠物天然适合；用户人设里的「内容边界」一票否决
2. **能怎么开口**（聊天切口）——抓回来什么不重要，重要的是拿到之后说什么

抓取仍然交给上层网络能力（本模块不发请求），故障转移保留但只服务于"哪个源还能用"。
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# 允许 `python scripts/trends/sources.py` 直接跑（此时 sys.path[0] 是脚本所在目录）
_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from scripts.core import settings as core_settings  # noqa: E402
from scripts.core.storage import read_json, write_json  # noqa: E402

# 恋人陪伴真的用得上的源（不做全网覆盖）
PLATFORMS: Dict[str, Dict[str, Any]] = {
    "小红书": {
        "url": "https://www.xiaohongshu.com/search_result?keyword={q}",
        "hint": "生活方式类最鲜活，适合找「一起去」「给你带」这类切口",
    },
    "B站": {
        "url": "https://search.bilibili.com/all?keyword={q}",
        "hint": "兴趣类话题与流行梗，弹幕热词是很好的共鸣素材",
    },
    "微博": {
        "url": "https://s.weibo.com/weibo?q={q}",
        "hint": "热搜最直接，但广告和营销号多，提炼时去噪要狠",
    },
}

# 可聊度：这个话题适不适合亲密对话（0–1）
# 依据：恋人之间聊得起来的是「生活质感 + 共同想象」，
# 不是「信息量」。财经/时政/社会新闻信息量大但聊不起来。
TOPIC_TALKABILITY: Dict[str, float] = {
    "美食": 0.95, "旅行": 0.95, "影视": 0.9, "音乐": 0.9, "宠物": 0.95,
    "穿搭": 0.85, "游戏": 0.8, "摄影": 0.85, "家居": 0.8, "运动": 0.75,
    "情感": 0.7, "工作": 0.55, "学习": 0.5, "科技": 0.5,
    "财经": 0.15, "时政": 0.05, "社会新闻": 0.1, "军事": 0.05,
}
DEFAULT_TALKABILITY = 0.5

# 话题 → 聊天切口（拿到素材后怎么开口，这才是 love-companion 要的产物）
TOPIC_OPENERS: Dict[str, List[str]] = {
    "美食": ["看着好好吃，改天带你去", "这个我会做，下次做给你吃"],
    "旅行": ["这个地方想去，跟我去吗", "看到这个突然想出去走走了"],
    "影视": ["这个我看了，想跟你一起再看一遍", "听说这个不错，一起看？"],
    "音乐": ["这首歌给你听", "听到这个想到你"],
    "宠物": ["你看这个像不像我们说的那只", "好想养一只啊"],
    "穿搭": ["这件适合你", "下次穿这个给我看"],
    "游戏": ["这个看起来好玩，一起？", "我有点心动了"],
    "摄影": ["这个构图好看，我给你拍一张", "想去这里拍照"],
}
DEFAULT_OPENERS = ["看到这个想到你", "这个挺有意思的"]

# 话题 → 推荐源顺序（primary 在前）
TOPIC_PLATFORMS: Dict[str, List[str]] = {
    "美食": ["小红书", "B站"], "旅行": ["小红书", "B站"],
    "穿搭": ["小红书", "B站"], "摄影": ["小红书", "B站"],
    "游戏": ["B站", "微博"], "音乐": ["B站", "微博"],
    "影视": ["微博", "B站"], "宠物": ["小红书", "B站"],
}
DEFAULT_CHAIN = ["小红书", "B站", "微博"]

# 用户人设里常见的内容边界关键词 → 命中即拒绝抓取
BLOCKED_HINTS = ("政治", "时政", "宗教", "色情", "暴力", "赌博", "违禁")


def _now() -> str:
    return datetime.now().isoformat(timespec="seconds")


def talkability(topic: str) -> float:
    """这个话题适不适合跟恋人聊"""
    return float(TOPIC_TALKABILITY.get(topic, DEFAULT_TALKABILITY))


def opener(topic: str, seed: int = 0) -> str:
    """拿到素材后怎么开口——love-companion 真正要的产物"""
    pool = TOPIC_OPENERS.get(topic) or DEFAULT_OPENERS
    return pool[seed % len(pool)]


def worth_it(topic: str, min_talkability: float = 0.4) -> bool:
    """值不值得为这个话题跑一次抓取"""
    return talkability(topic) >= min_talkability


class SourceRouter:
    """按话题产出抓取计划；源挂了自动换下一个"""

    def __init__(self, data_dir: Optional[str] = None):
        self.data_dir = core_settings.resolve_data_dir(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.file = self.data_dir / "trend_sources.json"

    def _load(self) -> Dict[str, Any]:
        data = read_json(self.file, {})
        return data if isinstance(data, dict) else {}

    def _save(self, data: Dict[str, Any]) -> None:
        write_json(self.file, data)

    def health(self) -> Dict[str, Dict[str, int]]:
        return self._load().get("health", {})

    def mark(self, platform: str, ok: bool) -> Dict[str, int]:
        data = self._load()
        h = data.setdefault("health", {}).setdefault(platform, {"ok": 0, "fail": 0})
        h["ok" if ok else "fail"] = int(h.get("ok" if ok else "fail", 0)) + 1
        h["ts"] = _now()
        self._save(data)
        return h

    def _score(self, platform: str) -> float:
        h = self.health().get(platform, {})
        ok, fail = int(h.get("ok", 0)), int(h.get("fail", 0))
        if not ok and not fail:
            return 1.0
        return round(ok / max(1, ok + fail), 3)

    def blocked(self, topic: str, content_bounds: Optional[List[str]] = None) -> Optional[str]:
        """命中内容边界就别抓了，返回拒绝原因

        用户写的是「不谈前任」，话题是「前任相关」——直接比对整句永远命中不了，
        靠 scripts/core/boundary.py 把祈使句还原成关键词。
        """
        from scripts.core import boundary
        for hint in BLOCKED_HINTS:
            if hint in (topic or ""):
                return f"话题命中内容边界：{hint}"
        for hit in boundary.hit(topic or "", content_bounds or []):
            return f"话题命中用户设置的边界：{hit}"
        return None

    def plan(self, topic: str, keyword: Optional[str] = None,
             content_bounds: Optional[List[str]] = None,
             seed: Optional[int] = None) -> Dict[str, Any]:
        """产出抓取计划

        Returns:
            {"topic", "keyword", "primary", "fallbacks", "specs",
             "可聊度", "值得抓", "开口", "拒绝原因"}
        """
        q = keyword or topic
        seed = datetime.now().day if seed is None else seed
        deny = self.blocked(topic, content_bounds)
        if deny:
            return {"topic": topic, "值得抓": False, "拒绝原因": deny, "specs": []}

        chain = TOPIC_PLATFORMS.get(topic, DEFAULT_CHAIN)
        ordered = sorted([p for p in chain if p in PLATFORMS],
                         key=lambda p: -self._score(p))
        specs = [{
            "platform": p,
            "url": PLATFORMS[p]["url"].format(q=q),
            "hint": PLATFORMS[p]["hint"],
            "health": self._score(p),
        } for p in ordered]

        return {
            "topic": topic,
            "keyword": q,
            "primary": specs[0]["platform"] if specs else None,
            "fallbacks": [s["platform"] for s in specs[1:]],
            "specs": specs,
            "可聊度": talkability(topic),
            "值得抓": worth_it(topic),
            "开口": opener(topic, seed),
        }

    def next_source(self, topic: str, tried: List[str]) -> Optional[Dict[str, Any]]:
        for s in self.plan(topic)["specs"]:
            if s["platform"] not in tried:
                return s
        return None

    def reset(self) -> None:
        self._save({})


if __name__ == "__main__":
    import sys
    r = SourceRouter()
    topic = sys.argv[1] if len(sys.argv) > 1 else "美食"
    print(json.dumps(r.plan(topic), ensure_ascii=False, indent=2))
