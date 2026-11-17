# -*- coding: utf-8 -*-
"""网页功能开关（单一真源，2026-09-17）。

背景 —— 用户裁定（2026-09-17）：
    「网页只提供 A2 检索 + A3 PDF 下载；A4 数据提取暂时隐藏不提供。」

设计原则：
- **集中开关**：后端（block_a / fullflow / form_schema / server）与前端（GET /api/features）
  读同一份定义，不散落魔法布尔值。
- **隐藏 ≠ 删除**：所有被隐藏的能力代码原样保留，恢复只需把对应值改回 True
  （或临时用环境变量覆盖，便于线上排查）。
- 语义：True = 提供该功能；False = 隐藏。

环境变量覆盖（临时调试 / CI，无需改代码）：
    CT_FEATURE_A4_EXTRACTION=1     → 恢复 A4 数据提取
    CT_FEATURE_FASTPATH_PDF=1      → 恢复「自备 PDF 跳 A4」通道
    CT_FEATURE_FASTPATH_RAW_CSV=1  → 开关「自备原始数据进 B」通道（默认已开）
    CT_FEATURE_FASTPATH_DRAFT=1    → 开关「自备 B 信封进 C」通道（默认已开）
"""

import os

#: 功能开关表（True = 提供；False = 隐藏）
FEATURES = {
    # A4 数据提取：逐篇 2×2 抽取 / 原文对照 / 剔除 / 手工补行 / 补传 PDF / 红线核验。
    # False → A4 节点降级为「PDF 全文下载」：只按 A2 裁决清单下载 OA 全文，
    #         不做任何抽取；下载完成后流程即终点（不进 Block B）。
    #         B/C 节点定义保留，日后开启本开关即可续跑。
    #         2026-09-27 旁路收口：三处直连 pdf_extractor.extract()、原本绕过本开关的
    #         后端端点（/api/upload_pdf、/api/upload_pdf_auto、fastpath data_mode="pdf"）
    #         已统一加 a4_extraction_enabled() 闸门（关闭时返回 409）。解冻只需把本值改回 True。
    "a4_extraction": False,
    # 开始页「我已备好全文 PDF → 跳到 A4 数据提取步骤」（依赖 a4_extraction；A4 隐藏期间不开放）
    "fastpath_pdf": False,
    # 开始页「我已备好原始数据 → 直接进 B 部分合并计算」（2026-09-17 重新开放）
    "fastpath_raw_csv": True,
    # 开始页「我已备好 B 信封 → 直接进 C 部分撰稿」（2026-09-17 新增：
    # 后端 run_fastpath("draft") 早已支持，此前缺前端入口）
    "fastpath_draft": True,
}

_ENV_KEYS = {
    "a4_extraction": "CT_FEATURE_A4_EXTRACTION",
    "fastpath_pdf": "CT_FEATURE_FASTPATH_PDF",
    "fastpath_raw_csv": "CT_FEATURE_FASTPATH_RAW_CSV",
    "fastpath_draft": "CT_FEATURE_FASTPATH_DRAFT",
}

_TRUE_WORDS = ("1", "true", "yes", "on", "y", "t")


def enabled(name):
    """读取开关。环境变量优先；未知名字返回 True（未知项不误伤既有能力）。"""
    env_key = _ENV_KEYS.get(name)
    if env_key:
        raw = os.environ.get(env_key)
        if raw is not None and str(raw).strip() != "":
            return str(raw).strip().lower() in _TRUE_WORDS
    return bool(FEATURES.get(name, True))


def a4_extraction_enabled():
    """A4 数据提取是否启用（block_a 抽取路径 / fullflow 推进逻辑共用）。"""
    return enabled("a4_extraction")


def as_dict():
    """开关快照（供 build_state 与 GET /api/features 下发前端）。"""
    return {k: enabled(k) for k in FEATURES}
