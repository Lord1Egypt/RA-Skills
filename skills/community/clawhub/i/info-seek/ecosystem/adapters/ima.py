#!/usr/bin/env python3
"""ima.copilot 生态适配器（v1.0.0）。"""

from ..base import EcosystemAdapter


class ImaAdapter(EcosystemAdapter):
    name = 'ima'
    display_name = 'ima.copilot'

    def trigger_spec(self) -> dict:
        return {
            'mode': 'natural_language_intent',
            'detail': '平台助手意图识别；v1.0.0 最终版已通过 MCP stdio 注册（历史旧版 v3.1.0 id 7486824209471306 已由 v1.0.0 取代）',
            'entry': 'MCP stdio 注册',
        }

    def collection_spec(self) -> dict:
        return {
            'mode': 'builtin',         # ima 无宿主 WebSearch → 内置（已修）搜索
            'inject_sources': False,
            'builtin_fallback': True,
            'detail': '全部走内置搜索降级链（DDG HTML → Bing RSS → Wikipedia）',
        }

    def credential_spec(self) -> dict:
        return {
            'required_env': [],
            'optional_env': ['INFOSEEK_DB', 'INFOSEEK_ARCHIVE'],
            'detail': 'ima 平台注入运行环境；本地 Python 执行',
        }

    def state_spec(self) -> dict:
        return {
            'data_dir': '~/.infoseek',
            'archives_dir': '~/infoseek-archives',
            'local_persistence': True,
            'readonly_install_ok': True,
        }

    def output_spec(self) -> dict:
        return {
            'format': 'markdown',
            'delivery': 'inline 回复',
            'archive': True,
            'extra': '实体自沉淀跨会话可用（状态已中立）',
        }
