#!/usr/bin/env python3
"""通用 MCP 生态适配器（v1.0.0）：任何 MCP 客户端的默认形态。"""

from ..base import EcosystemAdapter


class GenericMcpAdapter(EcosystemAdapter):
    name = 'generic_mcp'
    display_name = '通用 MCP'

    def trigger_spec(self) -> dict:
        return {
            'mode': 'tool_declaration',
            'detail': '任意 MCP 客户端按工具清单调用（dist/generic-mcp/mcp.json）',
            'entry': 'mcp.json（stdio / SSE / HTTP 三传输皆可）',
        }

    def collection_spec(self) -> dict:
        return {
            'mode': 'both',
            'inject_sources': True,
            'builtin_fallback': True,
            'detail': '宿主可注入；无则内置搜索链',
        }

    def credential_spec(self) -> dict:
        return {
            'required_env': [],
            'optional_env': ['INFOSEEK_AUTH_TOKEN', 'INFOSEEK_DB',
                             'INFOSEEK_ARCHIVE', 'INFOSEEK_DATA_DIR'],
            'detail': 'env-first，零必填凭据',
        }

    def state_spec(self) -> dict:
        return {
            'data_dir': '~/.infoseek（env 可覆盖）',
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
