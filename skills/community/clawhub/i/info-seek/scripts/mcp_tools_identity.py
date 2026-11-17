#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""identity_attribution 工具处理器（v1.5.0 · 身份归因消费侧）

tool_identity_attribution：已知用户名 → 跨平台账号锚点 + 人因验证
  链路：Maigret → Sherlock → AccountTrustScorer → manual_review（pipeline 统一执行）
  合规红线（双闸口，显式报错而非静默返回空，Agent 可感知合规状态）：
    - INFOSEEK_ENABLE_IDENTITY_ATTRIBUTION=1 显式启用
    - consent=true 用户显式授权（涉个人 OSINT）
"""
import os
import sys
from pathlib import Path
from typing import Dict


def _is_enabled() -> bool:
    """综合启用判定：env 闸 ∩ 注册表（Maigret/Sherlock 任一有效启用）"""
    if not os.environ.get("INFOSEEK_ENABLE_IDENTITY_ATTRIBUTION"):
        return False
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
        from core.capability_registry import is_effective_enabled
        return is_effective_enabled("Maigret") or is_effective_enabled("Sherlock")
    except Exception:
        return False


def tool_identity_attribution(args: Dict) -> Dict:
    """identity_attribution 工具实现：username → 归因锚点 + 验证 verdict"""
    username = (args or {}).get("username", "").strip()
    consent = bool((args or {}).get("consent", False))
    max_results = int((args or {}).get("max_results", 10) or 10)
    if not username:
        return {"status": "failed", "reason": "username 不能为空", "degradation": "invalid_input"}

    # 合规闸：显式报错（不静默返回空），Agent 可感知缺失项
    if not os.environ.get("INFOSEEK_ENABLE_IDENTITY_ATTRIBUTION"):
        return {
            "status": "blocked",
            "reason": "身份归因未启用：需设置 INFOSEEK_ENABLE_IDENTITY_ATTRIBUTION=1（合规 opt-in）",
            "degradation": "disabled",
        }
    if not consent:
        return {
            "status": "blocked",
            "reason": "身份归因涉个人 OSINT：需 consent=true 显式授权",
            "degradation": "no_consent",
        }

    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from infoseek_pipeline import search_identity_attribution

    anchors = search_identity_attribution(username, consent=True, max_results=max_results)
    verdicts = sorted({(a.get("verdict_cn") or "未验证") for a in anchors})
    return {
        "status": "ok",
        "username": username,
        "anchors": anchors,
        "anchor_count": len(anchors),
        "verdicts": verdicts,
        "degradation_path": "Maigret→Sherlock→AccountTrustScorer→manual_review",
    }