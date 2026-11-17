#!/usr/bin/env python3
"""WorkBuddy 生态适配器（v1.0.0）。"""

from ..base import EcosystemAdapter


class WorkBuddyAdapter(EcosystemAdapter):
    name = 'workbuddy'
    display_name = 'WorkBuddy'

    def trigger_spec(self) -> dict:
        return {
            'mode': 'keyword_intent',
            'detail': 'SKILL 关键词触发（调研/采集/报告类意图），经 SKILL.md 剧本驱动',
            'entry': 'SKILL.md 定义，宿主技能系统加载',
        }

    def collection_spec(self) -> dict:
        return {
            'mode': 'both',
            'inject_sources': True,   # 宿主可注入 WebSearch/WebFetch 结果
            'builtin_fallback': True, # 无注入时用内置（已修）搜索链
            'detail': '优先使用宿主 WebSearch/WebFetch（更强、受维护）；无则内置',
        }

    def credential_spec(self) -> dict:
        return {
            'required_env': [],
            'optional_env': ['INFOSEEK_AUTH_TOKEN', 'INFOSEEK_DB', 'INFOSEEK_ARCHIVE'],
            'detail': '本地执行，无需平台凭据；远程模式可选 token',
        }

    def state_spec(self) -> dict:
        return {
            'data_dir': '~/.infoseek（env INFOSEEK_DATA_DIR 可覆盖）',
            'archives_dir': '~/infoseek-archives',
            'local_persistence': True,
            'readonly_install_ok': True,  # 状态中立后成立
        }

    def output_spec(self) -> dict:
        return {
            'format': 'markdown',
            'delivery': 'inline + 可选归档',
            'archive': True,
            'extra': '支持流式输出（research_stream）',
        }

    def multimodal_spec(self) -> dict:
        """P3：WorkBuddy 宿主可注入图片/文档附件（不自研采集）。"""
        return {
            'mode': 'host_inject',
            'supported_types': ['image', 'pdf', 'docx'],
            'detail': '附件经 ResearchInput.attachments 注入，核心做分析层透传',
        }
