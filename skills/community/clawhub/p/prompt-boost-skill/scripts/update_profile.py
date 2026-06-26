#!/usr/bin/env python3
"""
update_profile.py - 更新用户偏好画像（学习型嘴替）
输入: {"user_id": "", "current_domain": "", "confirmed_slots": {}, "feedback": ""}
输出: {"updated_profile": {}}
"""
import json
import sys

DEFAULT_PROFILE = {
    "top_domains": [],
    "preferred_tools": [],
    "preferred_outputs": [],
    "clarification_tolerance": "medium",
    "default_assumptions": {},
}

def update_profile(user_id: str, current_domain: str, confirmed: dict) -> dict:
    # 简化版：每次更新增加计数
    profile = dict(DEFAULT_PROFILE)
    profile["user_id"] = user_id
    profile["top_domains"].append(current_domain)
    if confirmed.get("tool_preference"):
        profile["preferred_tools"].extend(confirmed.get("tool_preference", []))
    if confirmed.get("output_format"):
        profile["preferred_outputs"].append(confirmed.get("output_format"))
    return profile

if __name__ == "__main__":
    try:
        inp = json.loads(sys.stdin.read())
        result = update_profile(inp.get("user_id", "default"), inp.get("current_domain", ""), inp.get("confirmed_slots", {}))
        print(json.dumps({"updated_profile": result}, ensure_ascii=False, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
