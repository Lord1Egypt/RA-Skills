# -*- coding: utf-8 -*-
"""invest_skill_copilot · 仓库驱动的全场景投研分析

占位骨架：本 Skill 的真实执行逻辑写在 SKILL.md（提示词）与 scripts/repo_sync.py（功能目录同步）中，
尚未包装为 BaseSkill 的 run()。此处仅声明元数据以满足 invest-skill 框架 registry 的自动扫描注册。

对齐项目现状：14/14 Skill 均为直连数据源（calls_gateway: false）；统一 ctx.gateway 在 Roadmap 中，
待网关实现后再适配 run() 走 ctx.gateway.query(...)。
"""
from skills.base.skill_base import BaseSkill, SkillContext, SkillResult


class InvestSkillCopilotSkill(BaseSkill):
    skill_id = "invest_skill_copilot"
    skill_name = "仓库驱动的全场景投研分析"
    category = "subject_analysis"
    description = (
        "运行时读取 invest-skill 项目（Gitee 主源，GitHub 镜像可降级）的方法论与数据纪律并内化，"
        "由一个统一入口完成全场景股票投研分析，功能目录随仓库更新自动同步。"
    )
    input_schema = {
        "query": {"type": "string", "required": True},
        "scene": {"type": "string", "required": False},
        "sync_catalog": {"type": "string", "required": False},
    }
    output_schema = {
        "report_md": {"type": "file"},
        "report_html": {"type": "file"},
        "data": {"type": "object"},
    }

    def run(self, ctx: SkillContext, **kwargs) -> SkillResult:
        # 真实逻辑在 SKILL.md：Agent 读 SKILL.md → Step 0 同步功能目录 → 内化方法论 → 取数 → 分析 → 产出 MD/HTML。
        # 尚未适配 BaseSkill 执行链（与仓库内其余 Skill 现状一致），返回空结果骨架。
        return SkillResult(
            skill_id=self.skill_id,
            success=True,
            data={},
            data_source=None,
            meta={"note": "逻辑见 SKILL.md；待适配 BaseSkill + 统一网关后实现 run()"},
        )
