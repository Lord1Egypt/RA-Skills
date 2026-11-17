"""Locale-independent UI string mappings for Perplexity."""

UI_STRINGS = {
    "zh": {
        "deep_research": "深度研究",
        "model_council": "模型委员会",
        "step_by_step": "逐步学习",
        "completed": "已完成",
        "show_more": "查看更多",
        "answer_tab": "答案",
        "sources_tab": "链接",
        "images_tab": "图片",
        "search_results": "搜索结果",
        "studied": "已研究",
        "expand": "展开",
        "remove_prefix": "移除 ",
    },
    "en": {
        "deep_research": "Deep Research",
        "model_council": "Model Council",
        "step_by_step": "Step by Step",
        "completed": "Completed",
        "show_more": "Show more",
        "answer_tab": "Answer",
        "sources_tab": "Sources",
        "images_tab": "Images",
        "search_results": "Search results",
        "studied": "Researched",   # NOTE: en labels are NOT live-verified on the English site
        "expand": "Expand",
        "remove_prefix": "Remove ",
    },
}

SKIP_PREFIXES = {
    "zh": ("答案", "链接", "图片", "分享", "已完成", "进行中", "搜索结果", "新闻", "视频"),
    "en": ("Answer", "Sources", "Images", "Share", "Completed", "In progress",
           "Search results", "News", "Videos"),
}

SKIP_ANSWER_KEYWORDS = {
    "zh": ("分享", "搜索", "添加", "展开", "完成", "来源", "会话", "答案", "链接", "图片"),
    "en": ("Share", "Search", "Add", "Expand", "Done", "Sources", "Session",
           "Answer", "Links", "Images"),
}


def get_ui_string(key: str, locale: str = "zh") -> str:
    """Get a UI string for the given key and locale.

    Falls back to zh if the key is missing in the requested locale.
    Returns the key itself as last resort.
    """
    strings = UI_STRINGS.get(locale, UI_STRINGS["zh"])
    return strings.get(key, UI_STRINGS["zh"].get(key, key))


def get_skip_prefixes(locale: str = "zh") -> tuple:
    """Get answer-text skip prefixes for the locale."""
    return SKIP_PREFIXES.get(locale, SKIP_PREFIXES["zh"])


def get_skip_keywords(locale: str = "zh") -> tuple:
    """Get follow-up answer skip keywords for the locale."""
    return SKIP_ANSWER_KEYWORDS.get(locale, SKIP_ANSWER_KEYWORDS["zh"])
