from __future__ import annotations

import json

import kb_schema as schema

COMMON_MODULE_VERSION = "paperkb-v3.0"


def empty_catalog() -> str:
    return json.dumps({"documents": [], "concepts": [], "resources": [], "people": [], "projects": [], "reviews": [], "imports": []}, ensure_ascii=False, indent=2)


def readme(title: str, kind: str, direction: str = "") -> str:
    return f"# {title}\n\n类型：{kind}\n\n研究方向：{direction or '未填写'}\n\n本仓库由 paper-kb v3 自动维护。\n"


def agents_schema() -> str:
    return """# Wiki Schema\n\n本知识库由 paper-kb v3 自动维护。\n\n- summaries/: 单篇资料摘要，按类型分目录\n- identity/: 团队/个人身份元数据与群聊绑定镜像\n- concepts/: 跨文档概念页\n- resources/: 数据集、工具、硬件、开源项目等资源页\n- people/: 团队人物页\n- projects/: 项目聚合页\n- imports/: 批量导入和增量更新报告\n- reviews/: 综述、研究缺口和阶段总结\n- source_files/: 原始资料归档\n\n所有回答必须基于知识库来源，不允许补通用知识。\n"""


def team_info(team_name: str, direction: str, invite_code: str, repo: str) -> str:
    return f"# 团队信息\n\n团队名称：{team_name}\n团队研究方向：{direction}\n团队邀请码：{invite_code}\n团队知识库：{repo}\n\n团队知识库由 AIFusionBot 自动维护。\n"
