#!/usr/bin/env python3
"""Coze 生态适配器（v1.0.0）。"""

from ..base import EcosystemAdapter


class CozeAdapter(EcosystemAdapter):
    name = 'coze'
    display_name = 'Coze'

    def trigger_spec(self) -> dict:
        return {
            'mode': 'plugin',
            'detail': '插件调用；dist/coze/plugin.json + tools.json 模板',
            'entry': 'Coze 插件发布',
        }

    def collection_spec(self) -> dict:
        return {
            'mode': 'builtin',
            'inject_sources': False,
            'builtin_fallback': True,
            'detail': '插件内执行，无宿主 WebSearch → 内置搜索',
        }

    def credential_spec(self) -> dict:
        return {
            'required_env': [],
            'optional_env': ['INFOSEEK_AUTH_TOKEN'],
            'detail': '远程 SSE 形态需 token（token_env: INFOSEEK_AUTH_TOKEN）',
        }

    def state_spec(self) -> dict:
        return {
            'data_dir': '~/.infoseek（插件运行时）',
            'archives_dir': '~/infoseek-archives',
            'local_persistence': True,
            'remote_capable': True,
        }

    def output_spec(self) -> dict:
        return {
            'format': 'markdown',
            'delivery': '插件返回值',
            'archive': True,
        }
