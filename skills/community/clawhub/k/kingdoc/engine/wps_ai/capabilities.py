"""WPS AI 能力定义与用户意图映射"""
from typing import Dict, List, Optional

# 能力清单
CAPABILITIES = {
    "write": {
        "name": "AI 写作辅助",
        "description": "续写、改写、润色、翻译、扩写、缩写",
        "actions": ["polish", "expand", "shorten", "continue_write", "rewrite"],
        "keywords": ["写", "润色", "改写", "续写", "扩写", "缩写", "翻译", "重写", "优化文字", "改稿"],
    },
    "analyze": {
        "name": "AI 数据分析",
        "description": "自然语言提问，生成公式、图表、数据洞察",
        "keywords": ["分析", "数据", "趋势", "公式", "图表", "统计", "平均", "总和", "占比", "增长"],
    },
    "ppt": {
        "name": "AI PPT 生成",
        "description": "输入主题/大纲，自动生成 PPT 初稿",
        "keywords": ["ppt", "幻灯片", "演示", "汇报", "展示", "大纲", "讲稿"],
    },
    "read": {
        "name": "AI 阅读助手",
        "description": "长文档总结、问答、思维导图",
        "actions": ["summarize", "qa", "mindmap"],
        "keywords": ["总结", "摘要", "问答", "问题", "思维导图", "关键信息", "提取", "概括"],
    },
}

# 用户意图 → 能力映射
INTENT_MAP = {
    "polish": ("write", "polish"),
    "expand": ("write", "expand"),
    "shorten": ("write", "shorten"),
    "continue_write": ("write", "continue_write"),
    "rewrite": ("write", "rewrite"),
    "analyze": ("analyze", None),
    "ppt": ("ppt", None),
    "summarize": ("read", "summarize"),
    "qa": ("read", "qa"),
    "mindmap": ("read", "mindmap"),
}


def detect_intent(user_input: str) -> Optional[tuple]:
    """从用户输入检测意图，返回 (capability, action) 或 None"""
    text = user_input.lower()
    for cap_name, cap_info in CAPABILITIES.items():
        for kw in cap_info.get("keywords", []):
            if kw in text:
                action = cap_info.get("actions", [None])[0]
                return (cap_name, action)
    return None


def get_capability_list() -> List[Dict]:
    """获取能力清单（供 AI 理解）"""
    return [
        {"name": v["name"], "description": v["description"], "keywords": v.get("keywords", [])}
        for v in CAPABILITIES.values()
    ]
