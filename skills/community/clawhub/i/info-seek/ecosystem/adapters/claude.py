#!/usr/bin/env python3
"""Claude Desktop 生态适配器（v1.0.0）。"""

from ..base import EcosystemAdapter


class ClaudeAdapter(EcosystemAdapter):
    name = 'claude'
    display_name = 'Claude Desktop'

    def trigger_spec(self) -> dict:
        return {
            'mode': 'tool_declaration',
            'detail': 'mcp.json 声明 mcpServers，宿主按工具名调用（research_v3 等 25 工具）',
            'entry': 'dist/claude/mcp.json（stdio 本地 + SSE 远程双形态）',
        }

    def collection_spec(self) -> dict:
        return {
            'mode': 'builtin',          # Claude Desktop 无内置 WebSearch 工具
            'inject_sources': False,
            'builtin_fallback': True,
            'detail': '内置搜索链（DDG HTML → Bing RSS → Wikipedia）',
        }

    def credential_spec(self) -> dict:
        return {
            'required_env': [],
            'optional_env': ['INFOSEEK_AUTH_TOKEN', 'INFOSEEK_DB', 'INFOSEEK_ARCHIVE'],
            'detail': 'stdio 本地无需凭据；SSE 远程需 Bearer token',
        }

    def state_spec(self) -> dict:
        return {
            'data_dir': '~/.infoseek',
            'archives_dir': '~/infoseek-archives',
            'local_persistence': True,
            'remote_capable': True,     # SSE 远程模式状态落在托管机
        }

    def output_spec(self) -> dict:
        return {
            'format': 'markdown',
            'delivery': '工具返回值',
            'archive': True,
            'extra': '支持 research_stream 流式',
        }
