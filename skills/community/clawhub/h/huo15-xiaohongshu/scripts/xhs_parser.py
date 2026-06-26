"""从小红书网页端 HTML 抽取结构化数据。

核心思路：小红书网页端把数据注入到 `window.__INITIAL_STATE__`（或 SSR 版本）里，
我们只需要把那段 JSON 解出来就行，不涉及 X-s 签名。
"""

from __future__ import annotations

import html as htmlmod
import json
import re
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional


# ----- 数据结构 -----


@dataclass
class Author:
    user_id: str = ""
    nickname: str = ""
    avatar: str = ""
    follower_count: Optional[int] = None
    following_count: Optional[int] = None
    note_count: Optional[int] = None


@dataclass
class Interactions:
    liked_count: int = 0
    collected_count: int = 0
    comment_count: int = 0
    shared_count: int = 0


@dataclass
class Note:
    note_id: str = ""
    title: str = ""
    content: str = ""
    note_type: str = ""  # "normal" | "video"
    images: List[str] = field(default_factory=list)
    video_url: str = ""
    tags: List[str] = field(default_factory=list)
    at_users: List[str] = field(default_factory=list)
    author: Author = field(default_factory=Author)
    interactions: Interactions = field(default_factory=Interactions)
    ip_location: str = ""
    published_at: str = ""  # ISO-like str if available
    last_update_at: str = ""
    url: str = ""
    raw_time: Optional[int] = None  # 毫秒时间戳


@dataclass
class UserProfile:
    user_id: str = ""
    nickname: str = ""
    avatar: str = ""
    description: str = ""
    gender: str = ""
    ip_location: str = ""
    interactions: Dict[str, int] = field(default_factory=dict)  # fans / follows / notes / liked
    recent_notes: List[Dict[str, Any]] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)


# ----- 从 HTML 提取 state -----


_STATE_RE = re.compile(
    r"window\.__INITIAL_STATE__\s*=\s*(\{.*?\})\s*</script>",
    re.DOTALL,
)
_SSR_RE = re.compile(
    r"window\.__INITIAL_SSR_STATE__\s*=\s*(\{.*?\})\s*</script>",
    re.DOTALL,
)


def extract_initial_state(html_text: str) -> Dict[str, Any]:
    """解析 HTML 里的 __INITIAL_STATE__。小红书会把 undefined 写进 JSON，得替换一下。"""
    for regex in (_STATE_RE, _SSR_RE):
        m = regex.search(html_text)
        if not m:
            continue
        blob = m.group(1)
        # XHS 把 JS 的 undefined 直接塞进来了，json.loads 不认，替换成 null
        blob = re.sub(r":\s*undefined([,\}])", r": null\1", blob)
        blob = blob.replace(":undefined,", ":null,").replace(":undefined}", ":null}")
        try:
            return json.loads(blob)
        except json.JSONDecodeError:
            continue
    return {}


# ----- note 解析 -----


def parse_note_page(html_text: str, note_id: str = "") -> Optional[Note]:
    """从 `https://www.xiaohongshu.com/explore/{id}` 页面解析出笔记。"""
    state = extract_initial_state(html_text)
    if not state:
        return None

    note_data = _locate_note_detail(state, note_id)
    if not note_data:
        return None

    return _build_note(note_data, note_id=note_id)


def _locate_note_detail(state: Dict[str, Any], note_id: str) -> Optional[Dict[str, Any]]:
    # 结构：state.note.noteDetailMap[id].note
    note_tree = state.get("note") or {}
    detail_map = note_tree.get("noteDetailMap") or {}
    if note_id and note_id in detail_map:
        entry = detail_map[note_id]
        return entry.get("note") or entry
    # 否则取第一个
    for key, entry in detail_map.items():
        if isinstance(entry, dict):
            return entry.get("note") or entry
    return None


def _build_note(d: Dict[str, Any], note_id: str = "") -> Note:
    note = Note()
    note.note_id = d.get("noteId") or d.get("id") or note_id
    note.title = _clean_text(d.get("title", ""))
    note.content = _clean_text(d.get("desc", ""))
    note.note_type = d.get("type", "normal")
    note.ip_location = d.get("ipLocation", "")
    raw_time = d.get("time") or d.get("publishTime")
    if isinstance(raw_time, (int, float)):
        note.raw_time = int(raw_time)
        note.published_at = _ts_to_iso(int(raw_time))
    last_up = d.get("lastUpdateTime")
    if isinstance(last_up, (int, float)):
        note.last_update_at = _ts_to_iso(int(last_up))
    note.url = f"https://www.xiaohongshu.com/explore/{note.note_id}"

    # 图片
    for img in d.get("imageList", []) or []:
        url = img.get("urlDefault") or img.get("url")
        if url:
            note.images.append(url)

    # 视频
    video = d.get("video") or {}
    media = video.get("media") or {}
    for stream_list in (media.get("stream") or {}).values():
        if isinstance(stream_list, list) and stream_list:
            master = stream_list[0].get("masterUrl") or stream_list[0].get("backupUrls", [""])[0]
            if master:
                note.video_url = master
                break

    # 话题标签 / @
    for tag in d.get("tagList", []) or []:
        name = tag.get("name")
        ttype = tag.get("type")
        if not name:
            continue
        if ttype == "topic":
            note.tags.append(name)
        elif ttype == "mention":
            note.at_users.append(name)

    # 作者
    user = d.get("user") or {}
    note.author = Author(
        user_id=user.get("userId") or user.get("id") or "",
        nickname=_clean_text(user.get("nickname", user.get("nickName", ""))),
        avatar=user.get("avatar", ""),
    )

    # 互动
    inter = d.get("interactInfo") or {}
    note.interactions = Interactions(
        liked_count=_to_int(inter.get("likedCount")),
        collected_count=_to_int(inter.get("collectedCount")),
        comment_count=_to_int(inter.get("commentCount")),
        shared_count=_to_int(inter.get("sharedCount", inter.get("shareCount", 0))),
    )

    return note


# ----- user 解析 -----


def parse_user_page(html_text: str) -> Optional[UserProfile]:
    state = extract_initial_state(html_text)
    if not state:
        return None
    user_tree = state.get("user") or {}
    page = user_tree.get("userPageData") or user_tree.get("pageData") or user_tree
    basic = page.get("basicInfo") or user_tree.get("basicInfo") or {}
    inter = page.get("interactions") or []
    tags = page.get("tags") or []
    notes = page.get("notes") or []

    if not basic:
        # 有的主页结构 userPageData 直接就是基础信息
        basic = page

    profile = UserProfile(
        user_id=basic.get("userId") or basic.get("redId") or "",
        nickname=_clean_text(basic.get("nickname", "")),
        avatar=basic.get("imageb", basic.get("images", "")),
        description=_clean_text(basic.get("desc", "")),
        gender=str(basic.get("gender", "")),
        ip_location=basic.get("ipLocation", ""),
    )

    if isinstance(inter, list):
        for item in inter:
            k = item.get("type") or item.get("name")
            v = item.get("count")
            if k and v is not None:
                profile.interactions[str(k)] = _to_int(v)
    elif isinstance(inter, dict):
        for k, v in inter.items():
            profile.interactions[str(k)] = _to_int(v)

    profile.tags = [t.get("name") for t in tags if isinstance(t, dict) and t.get("name")]

    # 主页笔记列表（preview，信息有限但有 note_id、likes、封面）
    if isinstance(notes, list):
        for group in notes:
            if isinstance(group, list):
                for item in group:
                    preview = _note_preview(item)
                    if preview:
                        profile.recent_notes.append(preview)
            elif isinstance(group, dict):
                preview = _note_preview(group)
                if preview:
                    profile.recent_notes.append(preview)

    return profile


def _note_preview(raw: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    card = raw.get("noteCard") or raw
    note_id = card.get("noteId") or raw.get("id") or card.get("id")
    if not note_id:
        return None
    inter = card.get("interactInfo") or {}
    return {
        "note_id": note_id,
        "title": _clean_text(card.get("displayTitle") or card.get("title") or ""),
        "type": card.get("type", ""),
        "cover": ((card.get("cover") or {}).get("urlDefault", "")),
        "liked_count": _to_int(inter.get("likedCount")),
        "url": f"https://www.xiaohongshu.com/explore/{note_id}",
    }


# ----- search 解析 -----


def parse_search_page(html_text: str) -> List[Dict[str, Any]]:
    state = extract_initial_state(html_text)
    if not state:
        return []
    search = state.get("search") or {}
    feeds = search.get("feeds") or search.get("feedList") or []
    results = []
    if isinstance(feeds, list):
        for f in feeds:
            if isinstance(f, dict):
                preview = _note_preview(f)
                if preview:
                    results.append(preview)
    return results


# ----- 小工具 -----


def _clean_text(text: Any) -> str:
    if not text:
        return ""
    if not isinstance(text, str):
        text = str(text)
    return htmlmod.unescape(text).strip()


def _to_int(val: Any) -> int:
    if val is None:
        return 0
    if isinstance(val, (int, float)):
        return int(val)
    s = str(val).strip()
    if not s:
        return 0
    # 处理 "1.2万" / "3000+" 这种
    s = s.replace(",", "").replace("+", "")
    mult = 1
    if s.endswith("万"):
        mult = 10000
        s = s[:-1]
    elif s.endswith("k") or s.endswith("K"):
        mult = 1000
        s = s[:-1]
    try:
        return int(float(s) * mult)
    except ValueError:
        return 0


def _ts_to_iso(ts_ms: int) -> str:
    import datetime
    try:
        return datetime.datetime.fromtimestamp(ts_ms / 1000).isoformat(timespec="seconds")
    except (OverflowError, OSError, ValueError):
        return ""


# ----- dataclass → dict helper -----


def note_to_dict(note: Note) -> Dict[str, Any]:
    return asdict(note)


def profile_to_dict(p: UserProfile) -> Dict[str, Any]:
    return asdict(p)
