#!/usr/bin/env python3
"""Dify 生态适配器（v1.0.0）。"""

from ..base import EcosystemAdapter


class DifyAdapter(EcosystemAdapter):
    name = 'dify'
    display_name = 'Dify'

    def trigger_spec(self) -> dict:
        return {
            'mode': 'workflow_node',
            'detail': '工作流节点调用；dist/dify/plugin.yaml + tools.json 模板',
            'entry': 'Dify 插件导入',
        }

    def collection_spec(self) -> dict:
        return {
            'mode': 'builtin',
            'inject_sources': False,
            'builtin_fallback': True,
            'detail': '节点内执行，无宿主 WebSearch → 内置搜索',
        }

    def credential_spec(self) -> dict:
        return {
            'required_env': [],
            'optional_env': ['INFOSEEK_AUTH_TOKEN', 'INFOSEEK_DB'],
            'detail': '远程 SSE/HTTP 形态建议配置 token',
        }

    def state_spec(self) -> dict:
        return {
            'data_dir': '~/.infoseek（节点宿主机）',
            'archives_dir': '~/infoseek-archives',
            'local_persistence': True,
            'remote_capable': True,
        }

    def output_spec(self) -> dict:
        return {
            'format': 'markdown / json',
            'delivery': '节点输出变量',
            'archive': True,
        }
