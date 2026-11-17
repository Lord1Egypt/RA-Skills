#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""开发期发布冻结守卫（meta-analysis 架构重构开发期）。

读取本目录 DEV_POLICY.json：若 publish_freeze=true，则任何 meta-analysis
技能新版本发布（GitHub / SkillHub / ClawHub）必须被拦截。

这是「禁止发布新版本」的权威检查点：每次发布动作前都应先跑本脚本 / 调
assert_publish_allowed()，冻结时直接抛错或非零退出，绝不静默放行。

用法：
    python adapters/publish_guard.py            # 退出码 0=允许发布 / 2=冻结中
    # 或在 Python 中：
    from publish_guard import is_publish_frozen, assert_publish_allowed
    assert_publish_allowed("GitHub")            # 冻结则抛 RuntimeError

依赖：仅标准库。无策略文件 / publish_freeze 缺失 → 视为未冻结（正常生产态）。
"""
import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_POLICY_PATH = os.path.join(_HERE, "DEV_POLICY.json")


def _load_policy() -> dict:
    try:
        with open(_POLICY_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def is_publish_frozen() -> bool:
    """发布是否被冻结。无策略文件 / publish_freeze 缺失 → 未冻结。"""
    return bool(_load_policy().get("publish_freeze", False))


def frozen_reason() -> str:
    p = _load_policy()
    return p.get("reason") or p.get("unset_when") or "开发期冻结"


def assert_publish_allowed(platform: str = "any") -> None:
    """发布前调用；冻结则抛 RuntimeError（带明确文案，提示如何解除）。"""
    if is_publish_frozen():
        raise RuntimeError(
            f"⛔ 发布冻结中（meta-analysis 开发期）：禁止发布新版本到 {platform}。\n"
            f"   原因：{frozen_reason()}\n"
            f"   解除：用户明确告知开发期结束后，删除 adapters/DEV_POLICY.json 即可。"
        )


def main() -> int:
    if is_publish_frozen():
        print("⛔ 发布冻结中（meta-analysis 开发期）：当前禁止发布新版本。")
        print(f"   原因：{frozen_reason()}")
        print("   解除：用户明确告知开发期结束后，删除 adapters/DEV_POLICY.json 即可。")
        return 2
    print("✓ 发布未冻结，可正常发布。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
