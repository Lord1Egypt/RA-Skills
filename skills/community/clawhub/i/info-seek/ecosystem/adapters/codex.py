#!/usr/bin/env python3
"""Codex 生态适配器（v1.0.0）。"""

from ..base import EcosystemAdapter


class CodexAdapter(EcosystemAdapter):
    name = 'codex'
    display_name = 'Codex'

    def trigger_spec(self) -> dict:
        return {
            'mode': 'tool_declaration',
            'detail': 'MCP/HTTP 工具声明（--transport http 为 Codex 形态）',
            'entry': 'dist/generic-mcp/mcp.json 或 HTTP /rpc 直连',
        }

    def collection_spec(self) -> dict:
        return {
            'mode': 'both',
            'inject_sources': True,    # Codex 环境可注入网络抓取结果
            'builtin_fallback': True,
            'detail': '宿主可注入；无则内置搜索',
        }

    def credential_spec(self) -> dict:
        return {
            'required_env': [],
            'optional_env': ['INFOSEEK_AUTH_TOKEN'],
            'detail': 'HTTP 传输推荐启用 Bearer token',
        }

    def state_spec(self) -> dict:
        return {
            'data_dir': '~/.infoseek',
            'archives_dir': '~/infoseek-archives',
            'local_persistence': True,
            'remote_capable': True,
        }

    def output_spec(self) -> dict:
        return {
            'format': 'markdown',
            'delivery': '工具返回值',
            'archive': True,
        }
