"""快手 / B 站 / 抖音 视频发布：数据类型与 TXT 配置解析。"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass, field


@dataclass
class VideoPublishConfig:
    """从 TXT 配置文件解析的发布参数。"""

    title: str = ""
    video_path: str = ""
    cover_path: str = ""
    keywords: list[str] = field(default_factory=list)
    raw: dict[str, str] = field(default_factory=dict)

    def validate(self) -> None:
        """校验路径与非空字段。"""
        if not self.title.strip():
            raise ValueError("配置缺少标题（标题）")
        if not self.video_path.strip():
            raise ValueError("配置缺少视频路径（视频 / 视频数据路径）")
        if not os.path.isfile(self.video_path):
            raise FileNotFoundError(f"视频文件不存在: {self.video_path}")
        if self.cover_path and not os.path.isfile(self.cover_path):
            raise FileNotFoundError(f"封面文件不存在: {self.cover_path}")


@dataclass
class PublishResult:
    """单次发布结果（CLI JSON 友好）。"""

    success: bool
    platform: str
    message: str = ""
    detail: str = ""
    upload_phase: str = ""  # e.g. video_uploading | form_filled | published

    def to_dict(self) -> dict:
        return {
            "success": self.success,
            "platform": self.platform,
            "message": self.message,
            "detail": self.detail,
            "upload_phase": self.upload_phase,
        }


def _split_keywords(s: str) -> list[str]:
    s = s.strip()
    if not s:
        return []
    parts = re.split(r"[,，、\s]+", s)
    return [p.strip() for p in parts if p.strip()]


def _normalize_key(key: str) -> str:
    return key.strip().lower().replace(" ", "")


def load_publish_config(path: str) -> VideoPublishConfig:
    """读取 TXT 配置文件。

    支持「键：值」或「键:值」，键名不区分大小写，常见键：

    - 标题
    - 视频 / 视频路径 / 视频数据路径
    - 封面
    - 关键词（逗号、顿号或空格分隔）

    以 # 开头的行为注释。
    """
    raw: dict[str, str] = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            sep = None
            for candidate in ("：", ":"):
                if candidate in line:
                    sep = candidate
                    break
            if sep is None:
                continue
            k, v = line.split(sep, 1)
            raw[k.strip()] = v.strip()

    title = ""
    video = ""
    cover = ""
    keywords_str = ""

    alias_title = ("标题", "title")
    alias_video = ("视频", "视频路径", "视频数据路径", "video", "videopath")
    alias_cover = ("封面", "封面路径", "cover", "coverpath")
    alias_kw = ("关键词", "标签", "话题", "keywords", "tags")

    for k, v in raw.items():
        nk = _normalize_key(k)
        if nk in {_normalize_key(x) for x in alias_title} or nk == "标题":
            title = v
        elif nk in {_normalize_key(x) for x in alias_video}:
            video = v
        elif nk in {_normalize_key(x) for x in alias_cover}:
            cover = v
        elif nk in {_normalize_key(x) for x in alias_kw}:
            keywords_str = v

    # 未按别名匹配时，尝试直接使用英文键
    if not title:
        title = raw.get("标题", raw.get("title", ""))
    if not video:
        for key in ("视频数据路径", "视频路径", "视频", "video"):
            if key in raw:
                video = raw[key]
                break
    if not cover:
        cover = raw.get("封面", raw.get("cover", ""))
    if not keywords_str:
        keywords_str = raw.get("关键词", raw.get("标签", ""))

    return VideoPublishConfig(
        title=title.strip(),
        video_path=video.strip(),
        cover_path=cover.strip(),
        keywords=_split_keywords(keywords_str),
        raw=raw,
    )
