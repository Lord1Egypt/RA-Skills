"""KingDoc 更新检查模块 — 增强版

能力：
- 每日首次使用自动检查（本地缓存，避免频繁请求）
- 离线 / 网络异常时静默降级，绝不阻塞主流程
- 返回「用户可读」的升级提醒文案，供 AI 主动提示用户
- 内置反馈邮箱入口（有更好建议：njskills@agent.qq.com）
"""
from __future__ import annotations

import json
import sys
import argparse
import time
from pathlib import Path
from datetime import datetime, date

try:
    import requests
except ImportError:
    requests = None

# SkillHub API endpoint for checking updates
SKILLHUB_UPDATE_URL = "https://api.skillhub.cn/api/v1/skills/check_update"
SKILLHUB_SKILL_SLUG = "kingdoc"

# 本地缓存：记录最近一次检查结果，做到「每天只查一次」
_CACHE_NAME = ".kingdoc_update_cache.json"

# 反馈邮箱（SKILL.md 同步展示）
FEEDBACK_EMAIL = "njskills@agent.qq.com"


def _cache_path() -> Path:
    return Path(__file__).resolve().parent.parent.parent / _CACHE_NAME


def _load_cache() -> dict:
    try:
        return json.loads(_cache_path().read_text(encoding="utf-8"))
    except Exception:
        return {}


def _save_cache(data: dict) -> None:
    try:
        _cache_path().write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    except Exception:
        pass


def check_update(current_version: str, force: bool = False) -> dict:
    """检查是否有新版本。

    Returns:
        dict: {has_update, latest, release_note, instruction, error, checked_at, cached}
    """
    # 1) 命中当日缓存则直接返回（除非 force）
    cache = _load_cache()
    today = date.today().isoformat()
    if not force and cache.get("checked_date") == today and "has_update" in cache:
        return {
            "has_update": cache.get("has_update", False),
            "latest": cache.get("latest", current_version),
            "release_note": cache.get("release_note", ""),
            "instruction": cache.get("instruction", ""),
            "error": None,
            "checked_at": cache.get("checked_at", ""),
            "cached": True,
        }

    # 2) 无网络库直接降级
    if requests is None:
        result = {"error": "requests 未安装，跳过在线检查", "has_update": False}
    else:
        try:
            resp = requests.get(
                SKILLHUB_UPDATE_URL,
                params={"slug": SKILLHUB_SKILL_SLUG, "version": current_version},
                timeout=8,
            )
            if resp.status_code == 200:
                data = resp.json()
                latest = data.get("latest", current_version)
                has_update = _version_compare(latest, current_version) > 0
                result = {
                    "has_update": has_update,
                    "latest": latest,
                    "release_note": data.get("release_note", ""),
                    "instruction": data.get("instruction", ""),
                    "error": None,
                }
            else:
                result = {"error": f"HTTP {resp.status_code}", "has_update": False}
        except Exception as e:
            result = {"error": str(e), "has_update": False}

    # 3) 写缓存（每天一次）
    result["checked_at"] = datetime.now().isoformat(timespec="seconds")
    result["checked_date"] = today
    result["cached"] = False
    _save_cache(result)
    return result


def build_reminder(current_version: str, force: bool = False) -> str:
    """生成「用户可读」的升级提醒文案。

    返回值直接交给 AI，由 AI 在对话中主动提示用户（不自动安装）。
    """
    info = check_update(current_version, force=force)
    if info.get("error") and not info.get("has_update"):
        # 离线 / 异常：安静退出，不打扰用户
        return ""
    if not info.get("has_update"):
        return ""
    lines = [
        "🔔 KingDoc 有新版本可用，建议升级（不会自动安装）：",
        f"   当前版本：v{current_version}  →  最新版本：v{info.get('latest')}",
    ]
    if info.get("release_note"):
        lines.append("   更新内容：")
        for ln in info["release_note"].splitlines():
            if ln.strip():
                lines.append(f"     · {ln.strip()}")
    if info.get("instruction"):
        lines.append(f"   升级方式：{info['instruction']}")
    lines.append(f"   有更好建议？欢迎反馈：{FEEDBACK_EMAIL}")
    return "\n".join(lines)


def _version_compare(v1: str, v2: str) -> int:
    """v1 > v2 返回 >0，否则 <0，相等返回 0。"""
    def norm(v):
        return [int(x) for x in v.split(".") if x.isdigit()]
    p1, p2 = norm(v1), norm(v2)
    for a, b in zip(p1, p2):
        if a != b:
            return a - b
    return len(p1) - len(p2)


def main():
    parser = argparse.ArgumentParser(description="KingDoc Update Checker")
    parser.add_argument("--version", required=True, help="当前版本（如 3.0.0）")
    parser.add_argument("--reminder", action="store_true", help="仅输出用户提醒文案")
    parser.add_argument("--force", action="store_true", help="忽略缓存强制检查")
    args = parser.parse_args()

    if args.reminder:
        msg = build_reminder(args.version, force=args.force)
        if msg:
            print(msg)
        sys.exit(0)

    print("KingDoc Update Checker")
    print(f"Current version: {args.version}")
    result = check_update(args.version, force=args.force)
    if result.get("error"):
        print(f"[WARN] 未检查到更新（{result['error']}）")
        sys.exit(0)
    if result.get("has_update"):
        print(f"\n🆕 发现新版本：v{result['latest']}")
        if result.get("release_note"):
            print(f"\n更新内容:\n{result['release_note']}")
        if result.get("instruction"):
            print(f"\n升级方式:\n{result['instruction']}")
        print(f"\n反馈邮箱：{FEEDBACK_EMAIL}")
    else:
        print(f"[OK] 已是最新版本（v{args.version}）")
    sys.exit(0)


if __name__ == "__main__":
    main()
