"""KingDoc 品类元数据模块

v3.8.0 变更：8 品类扩展为 9 品类
- 新增：smart_canvas（智能画布元素级编辑，对标腾讯文档）
- 新增：content_search（文档内容全文搜索，超越腾讯）
- v3.7.0：新增 history_mgmt（历史管理，合并回收站+版本历史）
- v3.6.0：已合并 mindmap+flowchart → visualization
- v3.5.0：已合并 doc+smart_note → doc
"""
from __future__ import annotations

from typing import Dict, List, Optional, Tuple


# 9 品类元数据
CATEGORIES: Dict[str, Dict] = {
    "doc": {
        "name": "文档",
        "name_en": "document",
        "doc_type": "doc",
        "sub_types": ["doc", "smart_note", "smart_canvas"],
        "description": "文字文档/智能文档/智能画布，本地生成→上传覆盖；智能画布支持元素级CRUD + Markdown追加",
        "icon": "📄",
        "edit_method": "local_generate_upload",
        "available": True,
    },
    "content_search": {
        "name": "全文搜索",
        "name_en": "content_search",
        "doc_type": "search",
        "sub_types": ["content", "name"],
        "description": "文档内容全文搜索（超越腾讯：搜内容+结果定位高亮）",
        "icon": "🔍",
        "edit_method": "search_api",
        "available": True,
    },
    "sheet": {
        "name": "电子表格",
        "name_en": "sheet",
        "doc_type": "sheet",
        "sub_types": [],
        "description": "电子表格，API 精细编辑（单元格/公式）",
        "icon": "📊",
        "edit_method": "api_cell",
        "available": True,
    },
    "ppt": {
        "name": "演示文稿",
        "name_en": "slide",
        "doc_type": "ppt",
        "sub_types": [],
        "description": "演示文稿，本地生成→上传覆盖",
        "icon": "🎬",
        "edit_method": "local_generate_upload",
        "available": True,
    },
    "smartsheet": {
        "name": "多维表格",
        "name_en": "smartsheet",
        "doc_type": "smartsheet",
        "sub_types": [],
        "description": "多维表格，API 精细编辑（记录/字段/视图）",
        "icon": "🗂️",
        "edit_method": "api_record",
        "available": True,
    },
    "form": {
        "name": "收集表",
        "name_en": "form",
        "doc_type": "form",
        "sub_types": [],
        "description": "收集表/问卷，API 配置",
        "icon": "📝",
        "edit_method": "api_config",
        "available": True,
    },
    "visualization": {
        "name": "可视化",
        "name_en": "visualization",
        "doc_type": "mindmap",
        "sub_types": ["mindmap", "flowchart"],
        "sub_commands": ["mindmap", "flowchart"],
        "description": "思维导图/流程图，本地渲染 SVG→上传（共享 mermaid 渲染管线）",
        "icon": "🧠",
        "edit_method": "local_render_upload",
        "available": True,
    },
    "attachment": {
        "name": "附件",
        "name_en": "attachment",
        "doc_type": "attachment",
        "sub_types": [],
        "description": "本地文件直接上传",
        "icon": "📎",
        "edit_method": "upload_only",
        "available": True,
    },
    "history_mgmt": {
        "name": "历史管理",
        "name_en": "history_mgmt",
        "doc_type": "history",
        "sub_types": ["trash", "version"],
        "description": "回收站+版本历史统一管理（列出/恢复/彻底删除/回滚）",
        "icon": "🕐",
        "edit_method": "api_unified",
        "available": True,
    },
}

# 用户意图关键词 → 品类路由
INTENT_ROUTING: Dict[str, List[str]] = {
    "doc": ["文档", "文字", "word", "doc", "智能文档", "报告", "纪要", "周报", "合同", "笔记", "文章"],
    "sheet": ["表格", "excel", "sheet", "电子表格", "数据表", "统计表"],
    "ppt": ["ppt", "演示", "幻灯片", "汇报", "展示", "演示文稿"],
    "smartsheet": ["多维表格", "smartsheet", "数据库", "记录表", "数据收集"],
    "form": ["收集表", "form", "问卷", "表单", "投票", "报名"],
    "visualization": ["思维导图", "mindmap", "脑图", "导图", "知识图谱", "流程图", "flowchart", "流程", "步骤图", "架构图", "可视化"],
    "attachment": ["附件", "attachment", "文件", "上传", "图片", "pdf"],
    "history_mgmt": ["历史管理", "回收站", "trash", "版本历史", "version", "恢复", "restore", "回滚", "历史版本", "误删", "撤销删除"],
    "smart_canvas": ["智能画布", "smart_canvas", "元素编辑", "element", "元素级", "元素查询", "元素新增", "元素更新", "元素删除", "markdown追加", "增量追加", "追加内容"],
    "content_search": ["全文搜索", "content_search", "搜内容", "搜索文档内容", "找内容", "内容搜索", "查找", "定位高亮", "搜索文档"],
}

# 子类型识别关键词（用于 doc 品类进一步识别 smart_note vs doc）
SUBTYPE_KEYWORDS: Dict[str, List[str]] = {
    "smart_note": ["智能文档", "smart_note", "smart note", "markdown", "md"],
    "doc": ["文字", "word", "doc", "文档", "报告", "纪要", "周报", "合同"],
}

# 子命令识别关键词（用于 visualization 品类进一步识别 mindmap vs flowchart）
SUB_COMMAND_KEYWORDS: Dict[str, List[str]] = {
    "mindmap": ["思维导图", "mindmap", "脑图", "导图", "知识图谱"],
    "flowchart": ["流程图", "flowchart", "流程", "步骤图", "架构图"],
}


def get_category(category_id: str) -> Optional[Dict]:
    """获取品类元数据。"""
    return CATEGORIES.get(category_id)


def get_category_list() -> List[Dict]:
    """获取所有品类列表。"""
    return [
        {"id": k, **v}
        for k, v in CATEGORIES.items()
        if v.get("available", True)
    ]


def detect_category(user_input: str) -> Optional[str]:
    """根据用户输入自动识别品类。

    返回品类 ID（如 "doc", "sheet"），无法识别返回 None。
    """
    if not user_input:
        return None

    user_input_lower = user_input.lower()

    # 统计每个品类的匹配次数
    scores: Dict[str, int] = {}
    for cat_id, keywords in INTENT_ROUTING.items():
        score = 0
        for kw in keywords:
            if kw.lower() in user_input_lower:
                score += 1
        if score > 0:
            scores[cat_id] = score

    if not scores:
        return None

    # 返回得分最高的品类
    return max(scores, key=scores.get)


def detect_sub_type(category_id: str, user_input: str) -> Optional[str]:
    """在 doc 品类中进一步识别子类型（doc / smart_note）。"""
    if category_id != "doc":
        return None

    if not user_input:
        return "doc"  # 默认子类型

    user_input_lower = user_input.lower()

    for sub_type, keywords in SUBTYPE_KEYWORDS.items():
        for kw in keywords:
            if kw.lower() in user_input_lower:
                return sub_type

    return "doc"  # 默认普通文档


def detect_sub_command(category_id: str, user_input: str) -> Optional[str]:
    """在 visualization 品类中进一步识别子命令（mindmap / flowchart）。"""
    if category_id != "visualization":
        return None

    if not user_input:
        return "mindmap"  # 默认子命令

    user_input_lower = user_input.lower()

    for sub_cmd, keywords in SUB_COMMAND_KEYWORDS.items():
        for kw in keywords:
            if kw.lower() in user_input_lower:
                return sub_cmd

    return "mindmap"  # 默认思维导图


def route(user_input: str) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """智能路由：返回 (category_id, sub_type, sub_command)。"""
    category_id = detect_category(user_input)
    if not category_id:
        return (None, None, None)
    sub_type = detect_sub_type(category_id, user_input)
    sub_command = detect_sub_command(category_id, user_input)
    return (category_id, sub_type, sub_command)


def get_edit_method(category_id: str) -> str:
    """获取品类的编辑方式。"""
    cat = CATEGORIES.get(category_id)
    if not cat:
        return "unknown"
    return cat.get("edit_method", "unknown")


def get_doc_type(category_id: str, sub_type: str = "", sub_command: str = "") -> str:
    """获取金山文档 API 对应的 doc_type。"""
    cat = CATEGORIES.get(category_id)
    if not cat:
        return "unknown"
    if sub_command and sub_command in cat.get("sub_commands", []):
        return sub_command
    if sub_type and sub_type in cat.get("sub_types", []):
        return sub_type
    return cat.get("doc_type", category_id)


# 便捷函数
def list_categories() -> List[Dict]:
    """列出所有可用品类（供 MCP 工具返回）。"""
    return get_category_list()


def resolve_category(user_input: str) -> Dict:
    """解析用户输入，返回完整品类信息。"""
    category_id, sub_type, sub_command = route(user_input)
    if not category_id:
        return {"error": "无法识别品类", "input": user_input}

    cat = CATEGORIES[category_id]
    return {
        "category_id": category_id,
        "category_name": cat["name"],
        "sub_type": sub_type,
        "sub_command": sub_command,
        "edit_method": cat["edit_method"],
        "doc_type": get_doc_type(category_id, sub_type, sub_command),
        "description": cat["description"],
    }
