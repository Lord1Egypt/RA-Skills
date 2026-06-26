# -*- coding: utf-8 -*-
"""
Late Brake - Track Storage Management

管理内置赛道和用户自定义赛道：
- 内置赛道：从包内 data/tracks 读取
- 用户自定义赛道：从 ~/.late-brake/tracks 读取
- 支持添加/更新自定义赛道
- 自动验证 JSON 格式符合规范
"""

import os
import json
import re
from typing import List, Dict, Optional, Tuple
from jsonschema import validate, ValidationError

from late_brake.models import Track


# Track ID validation: only allow alphanumeric, underscore, hyphen
TRACK_ID_PATTERN = re.compile(r'^[a-zA-Z0-9_-]+$')


# JSON Schema for track validation (based on track-format.md)
TRACK_JSON_SCHEMA = {
    "type": "object",
    "required": ["id", "name", "length_m", "turn_count", "anchor", "gate", "centerline"],
    "properties": {
        "id": {"type": "string"},
        "name": {"type": "string"},
        "full_name": {"type": "string"},
        "location": {"type": "string"},
        "length_m": {"type": "number"},
        "turn_count": {"type": "integer"},
        "anchor": {
            "type": "object",
            "required": ["lat", "lon", "radius_m"],
            "properties": {
                "lat": {"type": "number"},
                "lon": {"type": "number"},
                "radius_m": {"type": "number"}
            }
        },
        "gate": {
            "type": "array",
            "minItems": 2,
            "maxItems": 2,
            "items": {
                "type": "array",
                "minItems": 2,
                "maxItems": 2,
                "items": {"type": "number"}
            }
        },
        "centerline": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "array",
                "minItems": 2,
                "maxItems": 2,
                "items": {"type": "number"}
            }
        },
        "geofence": {
            "type": ["array", "null"],
            "items": {
                "type": "array",
                "minItems": 2,
                "maxItems": 2,
                "items": {"type": "number"}
            }
        },
        "sectors": {
            "type": ["array", "null"],
            "items": {
                "type": "object",
                "required": ["id", "name", "start_distance_m", "end_distance_m"],
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string"},
                    "start_distance_m": {"type": "number"},
                    "end_distance_m": {"type": "number"},
                    "turns": {"type": "array", "items": {"type": "integer"}}
                }
            }
        },
        "turns": {
            "type": ["array", "null"],
            "items": {
                "type": "object",
                "required": ["name", "type", "start_distance_m", "apex_distance_m", "apex_coordinates", "end_distance_m", "min_speed_target"],
                "properties": {
                    "name": {"type": "string"},
                    "type": {"type": "string"},
                    "start_distance_m": {"type": "number"},
                    "apex_distance_m": {"type": "number"},
                    "apex_coordinates": {
                        "type": "array",
                        "minItems": 2,
                        "maxItems": 2,
                        "items": {"type": "number"}
                    },
                    "end_distance_m": {"type": "number"},
                    "radius_m": {"type": ["number", "null"]},
                    "min_speed_target": {"type": "number"}
                }
            }
        }
    },
    "additionalProperties": False
}


def get_user_track_dir() -> str:
    """获取用户自定义赛道目录"""
    home = os.path.expanduser("~")
    return os.path.join(home, ".late-brake", "tracks")


def get_builtin_track_dir() -> str:
    """获取内置赛道目录"""
    import late_brake
    pkg_dir = os.path.dirname(os.path.abspath(late_brake.__file__))
    return os.path.join(pkg_dir, "data", "tracks")


def list_all_tracks() -> List[Track]:
    """列出所有已配置赛道（内置 + 用户自定义）

    任意赛道校验失败则立即抛出异常，不静默跳过（US-034）
    """
    tracks: List[Track] = []

    # 先读内置赛道
    builtin_dir = get_builtin_track_dir()
    if os.path.exists(builtin_dir):
        for filename in os.listdir(builtin_dir):
            if filename.endswith(".json"):
                path = os.path.join(builtin_dir, filename)
                valid, err_msg, track = validate_track_file(path)
                if not valid or track is None:
                    raise ValueError(f"赛道文件 '{path}' 校验失败: {err_msg}")
                tracks.append(track)

    # 再读用户自定义赛道，覆盖同名ID
    user_dir = get_user_track_dir()
    if os.path.exists(user_dir):
        for filename in os.listdir(user_dir):
            if filename.endswith(".json"):
                path = os.path.join(user_dir, filename)
                valid, err_msg, track = validate_track_file(path)
                if not valid or track is None:
                    raise ValueError(f"赛道文件 '{path}' 校验失败: {err_msg}")
                # 移除同名内置赛道，用户覆盖内置
                tracks = [t for t in tracks if t.id != track.id]
                tracks.append(track)

    return tracks


def load_track_from_file(path: str) -> Optional[Track]:
    """从JSON文件加载赛道，返回 Track 对象，加载失败返回 None"""
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # 先验证 JSON Schema
        validate(instance=data, schema=TRACK_JSON_SCHEMA)

        # 用 Pydantic 验证模型
        track = Track(**data)
        return track

    except (json.JSONDecodeError, ValidationError, Exception) as e:
        return None


def validate_track_file(path: str) -> Tuple[bool, Optional[str], Optional[Track]]:
    """验证赛道JSON文件，返回 (是否有效, 错误信息, Track 对象)"""
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        validate(instance=data, schema=TRACK_JSON_SCHEMA)
        track = Track(**data)
        return True, None, track

    except json.JSONDecodeError as e:
        return False, f"JSON 格式错误: {str(e)}", None
    except ValidationError as e:
        # 只输出错误路径和信息，不打印完整JSON实例（US-036）
        # jsonschema validate() 只抛出第一个错误，无需遍历多个
        path = "/".join(str(p) for p in e.path) if e.path else "(root)"
        msg = f"字段 '{path}': {e.message}"
        return False, f"格式验证失败: {msg}", None
    except Exception as e:
        return False, f"加载失败: {str(e)}", None


def add_track_from_file(source_path: str) -> Tuple[bool, str, Optional[Track]]:
    """添加或更新用户自定义赛道
    返回 (是否成功, 消息, Track 对象)
    """
    valid, err_msg, track = validate_track_file(source_path)
    if not valid or track is None:
        return False, err_msg, None  # type: ignore

    # Validate track.id against allowed pattern
    if not TRACK_ID_PATTERN.fullmatch(track.id):
        return False, f"赛道ID '{track.id}' 包含非法字符，只允许字母、数字、下划线(_)和横杠(-)", None

    user_dir = get_user_track_dir()
    os.makedirs(user_dir, exist_ok=True)

    dest_path = os.path.join(user_dir, f"{track.id}.json")
    # Normalize and verify path is still within user track directory (prevent path traversal)
    dest_path = os.path.normpath(dest_path)
    if not dest_path.startswith(os.path.normpath(user_dir) + os.sep):
        return False, f"赛道ID '{track.id}' 生成路径非法，可能包含路径遍历字符", None

    with open(dest_path, "w", encoding="utf-8") as f:
        json.dump(track.model_dump(), f, indent=2, ensure_ascii=False)

    action = "更新" if os.path.exists(dest_path) else "添加"
    return True, f"{action}成功: {track.id} - {track.name}", track


def get_track_by_id(track_id: str) -> Optional[Track]:
    """根据ID获取赛道

    加载过程中任意赛道校验失败则抛出异常（US-034）
    """
    all_tracks = list_all_tracks()
    for track in all_tracks:
        if track.id == track_id:
            return track
    return None
