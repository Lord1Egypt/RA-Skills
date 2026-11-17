#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
writing_notes.py — 写作指导生成器

从 ReferenceEngine 动态加载参考文档，提取写作指导注入生成 prompt。
硬编码规则作为 fallback，当参考文档不可用时使用。
"""

from typing import List, Optional
import re

# ===== 硬编码 fallback 规则（当 ReferenceEngine 不可用时使用） =====

PLATFORM_RULES = {
    "\u756a\u8304": {
        "word_count": "2000-2500\u5b57\uff0c\u4e0d\u8d85\u8fc73000",
        "opening": "\u524d300\u5b57\u5fc5\u987b\u5b8c\u6210\uff1a\u4ecb\u7ecd\u4e3b\u89d2 + \u7ed9\u91d1\u624b\u6307/\u7cfb\u7edf + \u7b2c\u4e00\u4e2a\u51b2\u7a81",
        "pacing": "\u6781\u5feb\u8282\u594f\uff0c\u6bcf\u7ae0\u81f3\u5c111\u6b21\u60c5\u7eea\u6ce2\u52a8",
        "paragraph": "\u6bb5\u843d\u63a7\u5236\u57281-3\u53e5\uff0c\u5bf9\u8bdd\u5360\u6bd430-50%",
        "ending": "\u7ae0\u672b\u5fc5\u987b\u65ad\u5728\'\u63a5\u4e0b\u6765\u4f1a\u600e\u6837\'\u7684\u60ac\u5ff5\u4e0a",
        "description_ratio": "\u63cf\u5199\u5360\u6bd4\u4e0d\u8d85\u8fc720%",
        "ai_level": "L1+L2\u57fa\u7840\u53bbAI",
    },
    "\u8d77\u70b9": {
        "word_count": "3000-5000\u5b57",
        "opening": "\u524d3000\u5b57\u7ed9\u51fa\u6838\u5fc3\u77db\u76fe\uff0c\u4e0d\u4e00\u5b9a\u8981\u91d1\u624b\u6307",
        "pacing": "\u53ef\u6162\u70ed\uff0c\u5141\u8bb8\u5efa\u7acb\u4e16\u754c\u89c2",
        "paragraph": "\u6bb5\u843d3-5\u53e5\uff0c\u5bf9\u8bdd\u5360\u6bd420-35%",
        "ending": "\u7ae0\u672b\u5efa\u8bae\u60ac\u7591\u6536\u5c3e\uff0c\u53ef\u7528\u60c5\u611f\u6536\u675f",
        "description_ratio": "\u63cf\u5199\u5360\u6bd4\u53ef\u8fbe35%",
        "ai_level": "L2\u5168\u8dd1+L3\u57fa\u7840\uff0c\u7981\u7528\u8bcd\u5fc5\u987b\u6e05\u5e72\u51c0",
    },
    "\u4e03\u732b": {
        "word_count": "2000-3000\u5b57",
        "opening": "\u524d1500\u5b57\u7ed9\u723d\u70b9",
        "pacing": "\u5feb\u8282\u594f\uff0c\u60c5\u611f\u7ebf\u53ef\u52a0\u6df1",
        "paragraph": "\u6bb5\u843d2-3\u53e5\uff0c\u5bf9\u8bdd\u5360\u6bd425-40%",
        "ending": "\u7ae0\u672b\u60ac\u7591\u6536\u5c3e",
        "description_ratio": "\u63cf\u5199\u5360\u6bd4\u7ea625%",
        "ai_level": "L1\u5373\u53ef",
    },
    "\u98de\u5362": {
        "word_count": "2000-3000\u5b57",
        "opening": "\u524d500\u5b57\u5185\u5fc5\u987b\u7ed9\u7cfb\u7edf/\u91d1\u624b\u6307",
        "pacing": "\u6781\u5feb\u8282\u594f\uff0c\u723d\u5b57\u7b2c\u4e00",
        "paragraph": "\u6bb5\u843d2-4\u53e5\uff0c\u5bf9\u8bdd\u5360\u6bd430-45%",
        "ending": "\u7ae0\u672b\u5fc5\u987b\u6709\u7ffb\u9875\u94a9\u5b50",
        "description_ratio": "\u63cf\u5199\u5360\u6bd4\u4e0d\u8d85\u8fc720%",
        "ai_level": "L1\u57fa\u7840\u5373\u53ef",
    },
}

DEFAULT_PLATFORM = "\u756a\u8304"

CHAPTER_POSITION_RULES = {
    "first": {"label": "\u7b2c\u4e00\u7ae0", "notes": ["\u8fd9\u662f\u5168\u4e66\u7b2c\u4e00\u7ae0", "\u524d300\u5b57\u5fc5\u987b\u6709\u94a9\u5b50"]},
    "second": {"label": "\u7b2c\u4e8c\u7ae0", "notes": ["\u7b2c\u4e8c\u7ae0\u4efb\u52a1\uff1a\u52a0\u6df1\u94a9\u5b50"]},
    "third": {"label": "\u7b2c\u4e09\u7ae0", "notes": ["\u7b2c\u4e09\u7ae0\u4efb\u52a1\uff1a\u5236\u9020\u671f\u5f85\u4fe1\u53f7"]},
    "early": {"label": "\u5f00\u5c40\u671f\uff084-10\u7ae0\uff09", "notes": ["\u6bcf3\u7ae0\u4e00\u4e2a\u5c0f\u723d\u70b9", "\u6bcf5\u7ae0\u4e00\u4e2a\u4e2d\u578b\u723d\u70b9"]},
    "mid": {"label": "\u6301\u7eed\u671f\uff0811\u7ae0\u8d77\uff09", "notes": ["\u65e5\u5e38\u8fc7\u6e21\u7ae0\u8282\u63a7\u5236\u572815%\u4ee5\u5185", "\u6bcf\u7ae0\u53ea\u56f4\u7ed5\u4e00\u4e2a\u6838\u5fc3\u4e8b\u4ef6"]},
}

GENERAL_WRITING_RULES = [
    "\u60c5\u7eea\u5fc5\u987b\u7528\u52a8\u4f5c/\u73af\u5883\u5c55\u793a\uff0c\u4e0d\u76f4\u63a5\u544a\u77e5",
    "\u5bf9\u8bdd\u7528\u52a8\u4f5c\u66ff\u4ee3\u6807\u7b7e",
    "\u6bcf\u4e2a\u573a\u666f\u4ee5\u5177\u4f53\u611f\u5b98\u5207\u5165",
    "\u957f\u77ed\u53e5\u4ea4\u66ff\uff0c\u53e5\u957f\u65b9\u5dee\u5927\u4e8e8",
    "\u7981\u7528P0\u8bcd\u6c47\uff1a\u5b59\u5b9f\u7f6e\u7591\u3001\u4e0d\u53ef\u5426\u8ba4\u3001\u503c\u5f97\u4e00\u63d0\u7684\u662f",
    "\u7981\u7528\u611f\u609f\u5f0f\u7ed3\u5c3e\uff1a\'\u4ed6\u7ec8\u4e8e\u660e\u767d\u4e86\'",
    "\u4ee5\u8be5\u7ae0\u4e3b\u89d2\u7684\u6709\u9650\u89c6\u89d2\u5199\u4f5c",
    "\u7ae0\u672b\u5fc5\u987b\u7559\u94a9\u5b50",
]
ANTI_AI_RULES = [
    # 原有 5 条
    "身体法则：禁止使用'感到/觉得/认为/知道'引出情绪",
    "痒的法则：每章结尾必须是新问题而非旧答案",
    "拉不说推：禁止直接评价",
    "反平衡：高潮段落字数密度x3，低潮段落/3",
    "记忆痕迹：每个角色至少 2 个过去痕迹",
    # 新增 8 维语言学去AI（参考进阶迭代版第5章）
    "【句式随机化】强制打乱对称句式，段落长短差≥ 5 行，删除机械逻辑连接词（首先/其次/同时）",
    "【矛盾情绪植入】角色增加纠结/犹豫/口是心非等矛盾情绪，杜绝 AI 式单一情绪",
    "【生活化随机细节】每章随机注入 1-2 个无功能性但真实的生活化细节（小动作/环境瑕疵）",
    "【隐性叙事】删除所有 AI 式心理总结，用动作+对话+环境+感官间接体现",
    "【口语化柔化】加入角色专属口头禅、语气停顿、细微语病式自然表达",
    "【留白设计】预留少量情绪留白、细节留白，不把剧情写满，复刻含蓄感",
    "【群像人性化】反派/配角增加个人执念、软肛、无奈，杜绝工具人",
    "【 3-5-10 节奏】每 3 章小爽点、每 5 章冲突升级、每 10 章单元高潮",
]


def _get_ref_engine():
    """懒加载 ReferenceEngine 实例。"""
    try:
        from .reference_engine import ReferenceEngine
        return ReferenceEngine()
    except Exception:
        return None


def _extract_platform_table(text: str, platform_name: str) -> dict:
    """从 platform-strategy.md 的表格中提取指定平台的行数据。"""
    if not text:
        return {}
    # 查找快速选型表
    lines = text.split('\n')
    headers = []
    in_table = False
    results = {}
    for line in lines:
        ls = line.strip()
        if '|' not in ls:
            in_table = False
            continue
        cells = [c.strip() for c in ls.split('|') if c.strip()]
        if not cells:
            continue
        # 检测表头
        if '\u7ef4\u5ea6' in cells[0] and len(cells) >= 4:
            headers = cells[1:]
            in_table = True
            continue
        if in_table and cells[0] == platform_name and len(cells) >= 2:
            for i, header in enumerate(headers):
                if i + 1 < len(cells):
                    results[header] = cells[i + 1]
            break
    return results


def build_writing_notes(
    platform: str = "",
    chapter: int = 1,
    total_chapters: int = 0,
    genre: str = "",
    is_l3: bool = True,
) -> List[str]:
    """\u751f\u6210\u9002\u7528\u4e8e\u5f53\u524d\u7ae0\u8282\u7684\u5199\u4f5c\u6307\u5bfc\u5217\u8868\u3002

    \u4ece ReferenceEngine \u52a8\u6001\u52a0\u8f7d\u53c2\u8003\u6587\u6863\uff0c\u5931\u8d25\u65f6\u56de\u9000\u5230\u786c\u7f16\u7801\u89c4\u5219\u3002
    """
    notes = []

    # \u52a0\u8f7d ReferenceEngine
    ref = _get_ref_engine()

    # 1. \u5e73\u53f0\u89c4\u5219
    p_rules = None
    if ref and platform:
        doc = ref.read_doc("platform-strategy.md")
        if doc:
            table_data = _extract_platform_table(doc, platform)
            if table_data:
                p_rules_raw = {
                    "word_count": table_data.get("\u5355\u7ae0\u5b57\u6570", ""),
                    "opening": f"\u524d300\u5b57\uff1a{table_data.get('\u5f00\u5934\u5f3a\u5ea6', '\u5feb\u901f\u5207\u5165\u51b2\u7a81')}",
                    "pacing": f"\u8282\u594f\uff1a{table_data.get('\u8282\u594f\u8981\u6c42', '')}",
                    "paragraph": f"\u6bb5\u843d\uff1a{table_data.get('\u6bb5\u843d\u957f\u5ea6', '')}\uff0c\u5bf9\u8bdd\uff1a{table_data.get('\u5bf9\u8bdd\u5360\u6bd4', '')}",
                    "ending": f"\u7ed3\u5c3e\uff1a\u7ae0\u672b\u5fc5\u987b\u7559\u94a9\u5b50",
                    "description_ratio": f"\u63cf\u5199\uff1a{table_data.get('\u63cf\u5199\u5360\u6bd4', '')}",
                    "ai_level": f"AI\u68c0\u6d4b\uff1a{table_data.get('AI\u68c0\u6d4b\u4e25\u5ea6', '\u4e2d')}",
                }
                p_rules = p_rules_raw

    if not p_rules:
        # Fallback \uff1a\u786c\u7f16\u7801
        if platform in PLATFORM_RULES:
            p_rules = PLATFORM_RULES[platform]
        else:
            p_rules = PLATFORM_RULES.get("\u756a\u8304", list(PLATFORM_RULES.values())[0])

    notes.append(f"[\u5e73\u53f0] \u76ee\u6807\u5e73\u53f0\uff1a{platform or '\u756a\u8304'}")
    for key, val in p_rules.items():
        if val:
            notes.append(f"[{key}] {val}")

    # 2. \u7ae0\u8282\u4f4d\u7f6e\u89c4\u5219
    if chapter == 1:
        pos_rules = CHAPTER_POSITION_RULES["first"]
    elif chapter == 2:
        pos_rules = CHAPTER_POSITION_RULES["second"]
    elif chapter == 3:
        pos_rules = CHAPTER_POSITION_RULES["third"]
    elif chapter <= 10:
        pos_rules = CHAPTER_POSITION_RULES["early"]
    else:
        pos_rules = CHAPTER_POSITION_RULES["mid"]

    notes.append(f"[\u7ae0\u8282\u5b9a\u4f4d] {pos_rules['label']}")
    for n in pos_rules["notes"]:
        notes.append(f"[\u7ae0\u89c4] {n}")

    # 3. \u901a\u7528\u5199\u4f5c\u89c4\u5219\uff08\u968f\u673a\u90093-5\u6761\uff09
    import hashlib
    seed = f"{platform}-{chapter}-writing-v2"
    rule_hash = int(hashlib.md5(seed.encode()).hexdigest(), 16)
    selected = []
    for i, rule in enumerate(GENERAL_WRITING_RULES):
        if (rule_hash >> i) & 1:
            selected.append(rule)
    if len(selected) < 3:
        selected = GENERAL_WRITING_RULES[:5]
    elif len(selected) > 5:
        selected = selected[:5]
    notes.append("[\u5199\u4f5c\u89c4\u8303]")
    for r in selected:
        notes.append(f"[\u89c4\u8303] {r}")

    # 4. \u53cdAI\u89c4\u5219\uff08\u90092-3\u6761\uff09
    ai_hash = int(hashlib.md5(f"{platform}-{chapter}-ai-v2".encode()).hexdigest(), 16)
    ai_selected = []
    for i, rule in enumerate(ANTI_AI_RULES):
        if (ai_hash >> i) & 1:
            ai_selected.append(rule)
    if len(ai_selected) < 2:
        ai_selected = ANTI_AI_RULES[:3]
    elif len(ai_selected) > 3:
        ai_selected = ai_selected[:3]
    notes.append("[\u53cdAI\u672c\u80fd]")
    for r in ai_selected:
        notes.append(f"[\u53cdAI] {r}")

    # 5. L3 \u63d0\u793a
    if is_l3:
        notes.append("[L3] \u4e09\u6bb5\u53d8\u4f53\u751f\u6210\uff1a\u5f00\u5934\u6bb5\uff08300\u5b57\u5185\u57cb\u94a9\u5b50\uff09\u3001\u4e2d\u6bb5\uff08\u63a8\u8fdb\u60c5\u8282\uff09\u3001\u5c3e\u6bb5\uff08\u60ac\u5ff5\u6536\u5c3e\uff09")
        notes.append("[L3] \u5404\u6bb5\u4f7f\u7528\u4e0d\u540c\u6e29\u5ea6\uff0c\u6ce8\u610f\u6bb5\u95f4\u8fc7\u6e21\u81ea\u7136")

    return notes

# three-sword de-ai refs
THREE_SWORD_REFS = {"word_freq":"","rhythm":"","emotion":""}
CHARACTER_CHECK_REFS = {"extract":"","compare":"","justify":""}
