#!/usr/bin/env python3
"""infoseek_mcp_server.py — Infoseek v1.0.0 MCP 服务器（search server）

版本演进: 内部开发线 1.5.0 → 3.1.0；对外发布版本 v1.0.0 起
  1.5.0: stdio 传输，6 工具
  1.5.1: + SSE 传输 + Bearer Token 认证
  1.5.2: + HTTP /rpc + GET /health
  1.6.0: + cross_subject_analysis 第 7 工具 + multi-server 拆分（archive 独立）
  1.6.1: PATCH 加固: token 来源诊断横幅 + 错误响应含 hint + token 脱敏日志
  1.6.2: PATCH 增强: 健康检查细化（uptime + 工具调用统计）+ 审计日志 + token 健康端点
  1.7.0: MINOR 新增: summarize_content 第 8 工具（summa 主路径 + LLM 兜底）
  3.0.0: GA: research_v3 / research_stream / score_contradiction + 全 async 路径

传输:
  - stdio（本地首选）
  - SSE（HTTP/HTTPS 服务，支持 Bearer Token 认证）
  - HTTP /rpc（短请求-响应模型）

工具（当前 25 个）: search_anchors / fetch_content / save_archive /
       check_dedup / dedup_stats / fuse_analysis / cross_subject_analysis /
       summarize_content / conflict_detection / score_source / research /
       research_v3 / research_stream / score_contradiction + 11 个 *_async
（archive server 仅 2 工具：save_archive + dedup_stats，详见 infoseek_archive_server.py）

启动:
  python scripts/infoseek_mcp_server.py                              # stdio（默认）
  python scripts/infoseek_mcp_server.py --transport sse --port 8080 # SSE
  python scripts/infoseek_mcp_server.py --transport sse --require-token --token <secret>

工具命名: mcp__plugin_infoseek_<server>__<tool>
其中 server = "search"（v1.6.0 前为单一 server），tool = 上述工具名
"""
import argparse
import json
import os
import secrets
import sys
import time
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Dict, List, Optional
from urllib.parse import parse_qs

# ── 路径常量（v1.0.0 状态层中立：运行态数据统一位于 ~/.infoseek 或 env 指定目录，
# ── 公共层（G11 拆分 v1.0.1）：路径常量 / 认证 / 审计状态 / 辅助由 mcp_tools_common 单一提供 ──
from mcp_tools_common import (
    CORE_DIR, INFOSEEK_ROOT, WORKSPACE, INFOSEEK_DIR, DB_PATH, LOG_PATH,
    ARCHIVES_DIR, AUTH_TOKEN, PROTOCOL_VERSION, SERVER_NAME, SERVER_VERSION,
    SERVER_START_TIME, TOOL_CALL_COUNTER, AUDIT_LOG_PATH,
    ensure_dirs, mask_token,
)

# ── V8.4 C 类：OAuth 2.0 /oauth/token 支持（可选依赖 infoseek_auth）──
try:
    from infoseek_auth import AuthManager, SecretCipher  # noqa: F401
    _HAS_AUTH = True
except Exception:
    AuthManager = None
    SecretCipher = None
    _HAS_AUTH = False

_AUTH_MANAGER = AuthManager() if _HAS_AUTH else None

# ── 工具函数（G11 拆分：按职责分布于 mcp_tools_* 模块，门面统一绑定）──
from mcp_tools_search import tool_search_anchors, tool_fetch_content
from mcp_tools_archive import tool_save_archive, tool_check_dedup, tool_dedup_stats
from mcp_tools_analysis import (
    tool_fuse_analysis, tool_score_source, tool_research,
    tool_conflict_detection, tool_cross_subject_analysis, tool_summarize_content,
)
from mcp_tools_keys import tool_manage_keys, tool_key_usage
from mcp_tools_qcm import tool_qcm_query  # V8.4: QCM 反向工具
from mcp_tools_identity import tool_identity_attribution  # v1.5.0: 身份归因工具（T2/G2）
from mcp_tools_forensics import tool_account_forensics  # v1.6.0 融入: 账号取证工具（B1，发现→取证双子）
from mcp_tools_async import (
    _handle_async_wrapper, tool_score_contradiction,
    _handle_async_research_wrapper, _stream_research_wrapper,
    _handle_research_stream_sync,
)

# ── 工具清单 ──
TOOLS = [
    {
        "name": "search_anchors",
        "description": "多渠道并行锚点发现。从行业/主题/人名嗅探信息源，支持 depth（1-3层）和 sources 列表。返回结构化候选源列表，每项含 url/title/score。",
        "inputSchema": {
            "type": "object",
            "properties": {
                "subject": {"type": "string", "description": "调研主题（必填）"},
                "depth": {"type": "integer", "default": 2, "minimum": 1, "maximum": 3,
                          "description": "关键词展开深度"},
                "sources": {"type": "array", "items": {"type": "string"},
                            "description": "限定渠道（web/kb/note），默认全开"}
            },
            "required": ["subject"]
        }
    },
    {
        "name": "fetch_content",
        "description": "内容采集（四级降级提取）。v1.9.0 增强：链式引用追踪 v3（多层递归 + 防环 + 深度折扣 + max_chain_depth 1-3）。v1.8.0 v2：discover/fetch/graph 三模式 + 引用图 dot + 相关性评分。v1.7.3 v1：仅发现链接不抓取。",
        "inputSchema": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "目标 URL（必填）"},
                "format": {"type": "string", "enum": ["md", "json", "txt"], "default": "md"},
                "max_retries": {"type": "integer", "default": 3, "minimum": 1, "maximum": 5},
                "follow_links": {"type": "boolean", "default": False,
                                  "description": "是否启用链式引用追踪（v1.7.3）"},
                "max_depth": {"type": "integer", "default": 1, "minimum": 1, "maximum": 3,
                               "description": "v1.7.3 追踪深度。v1.8.0 起作用于 v2 全链"},
                "chain_strategy": {"type": "string", "enum": ["discover", "fetch", "graph", "recursive"],
                                   "default": "discover",
                                   "description": "v1.8.0+: discover/fetch/graph。v1.9.0 新增 recursive=多层递归"},
                "chain_limit": {"type": "integer", "default": 5, "minimum": 1, "maximum": 20,
                                  "description": "v1.8.0 新增: 链式追踪最大 URL 数"},
                "max_chain_depth": {"type": "integer", "default": 1, "minimum": 1, "maximum": 3,
                                     "description": "v1.9.0 新增: 递归深度上限（仅 recursive 模式有效）"},
                "subject": {"type": "string", "description": "v1.8.0 新增: 用于引用相关性评分的主题"}
            },
            "required": ["url"]
        }
    },
    {
        "name": "save_archive",
        "description": "存档归档（v1.4.0 增强）。将抓取内容保存到 infoseek-archives/<subject>/，自动建元数据表与去重检查。",
        "inputSchema": {
            "type": "object",
            "properties": {
                "subject": {"type": "string", "description": "调研主题（必填）"},
                "url": {"type": "string", "description": "来源 URL（必填）"},
                "title": {"type": "string"},
                "content": {"type": "string", "description": "正文内容"},
                "metadata": {"type": "object", "description": "附加元数据"}
            },
            "required": ["subject", "url", "title", "content"]
        }
    },
    {
        "name": "check_dedup",
        "description": "URL 去重检查。返回是否已在去重 DB 中。",
        "inputSchema": {
            "type": "object",
            "properties": {"url": {"type": "string"}},
            "required": ["url"]
        }
    },
    {
        "name": "dedup_stats",
        "description": "任务报告：URL 总数、主题分布、抓取时间统计。",
        "inputSchema": {
            "type": "object",
            "properties": {"subject": {"type": "string", "description": "可选，限定主题"}}
        }
    },
    {
        "name": "fuse_analysis",
        "description": "融合分析（多源交叉）。输入 subject 与 sources 列表，输出分层根因表。min_score 过滤低质源。v1.8.1 增强：export_formats 参数自动生成 md/json/csv/claude/openai/lobehub 多种格式。",
        "inputSchema": {
            "type": "object",
            "properties": {
                "subject": {"type": "string"},
                "sources": {"type": "array", "items": {"type": "object"},
                            "description": "源列表 [{url, content, score}, ...]"},
                "min_score": {"type": "integer", "default": 40, "minimum": 0, "maximum": 100},
                "export_formats": {
                    "type": "array",
                    "items": {"type": "string", "enum": ["md", "json", "csv", "claude", "openai", "lobehub"]},
                    "default": [],
                    "description": "v1.8.1 新增：自动导出的格式列表（空=不导出）"
                }
            },
            "required": ["subject", "sources"]
        }
    },
    {
        "name": "cross_subject_analysis",
        "description": "跨主题关联分析 (v1.6.0 新增)。输入多个调研主题，输出共享源/共同作者/共有概念等关联信息。min_correlation 过滤低相关主题对。",
        "inputSchema": {
            "type": "object",
            "properties": {
                "subjects": {"type": "array", "items": {"type": "string"},
                             "description": "主题列表（≥2）"},
                "min_correlation": {"type": "integer", "default": 1, "minimum": 1, "maximum": 100,
                                    "description": "最小共享源数阈值"}
            },
            "required": ["subjects"]
        }
    },
    {
        "name": "summarize_content",
        "description": "文本摘要 + 关键词提取 (v1.7.0+)。主路径: summa TextRank（英文友好）+ jieba Textrank（v1.7.1 中文优化）+ LLM API 兜底（需 API Key）。无 API 时自动降级到文本截断。",
        "inputSchema": {
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "待摘要文本（必填）"},
                "max_words": {"type": "integer", "default": 100, "minimum": 10, "maximum": 500,
                              "description": "摘要最大词数"},
                "prefer": {"type": "string", "enum": ["auto", "summa", "jieba", "llm"], "default": "auto",
                           "description": "首选路径（auto=自动检测语言，jieba=中文专用，llm 仅在配置 API Key 时生效）"}
            },
            "required": ["text"]
        }
    },
    {
        "name": "conflict_detection",
        "description": "跨源事实冲突检测 (v1.8.1+ 第 9 工具)。输入多个来源（含 text/title/url/score），自动识别对同一实体的不同表述/数值，按严重度排序输出冲突列表。",
        "inputSchema": {
            "type": "object",
            "properties": {
                "sources": {
                    "type": "array",
                    "items": {"type": "object"},
                    "description": "来源列表，每项含 text/title/url/score"
                },
                "subject": {"type": "string", "description": "调研主题（可选，用于过滤）"},
                "min_sources": {"type": "integer", "default": 2, "minimum": 2, "maximum": 10,
                                  "description": "最少需要多少个来源才检测（默认 2）"},
                "max_conflicts": {"type": "integer", "default": 20, "minimum": 1, "maximum": 50,
                                    "description": "最多返回多少个冲突（默认 20）"}
            },
            "required": ["sources"]
        }
    },
    {
        "name": "score_source",
        "description": "v2 评分 (v2.0.1+ 第 10 工具)。单个源 v2 评分：含 trust_bonus（统一信任源加权）+ Jaccard 语义相似度 + domain_bonus。",
        "inputSchema": {
            "type": "object",
            "properties": {
                "source": {"type": "object", "description": "源 dict（含 url/platform/title/snippet/score）"},
                "subject": {"type": "string", "description": "调研主题"},
                "with_domain": {"type": "boolean", "default": True, "description": "是否自动应用领域加权"}
            },
            "required": ["source", "subject"]
        }
    },
    {
        "name": "score_contradiction",
        "description": "v3.0.0 GA 矛盾评分（v2.7.2 引入）。两句话矛盾评分，含 severity 等级。",
        "inputSchema": {
            "type": "object",
            "properties": {
                "claim_a": {"type": "object"},
                "claim_b": {"type": "object"}
            },
            "required": ["claim_a", "claim_b"]
        }
    },
    {
        "name": "research",
        "description": "v2 端到端调研 (v2.0.1+ 第 11 工具)。一次调用完成：detect_domain → score → conflict → render → report。",
        "inputSchema": {
            "type": "object",
            "properties": {
                "subject": {"type": "string", "description": "调研主题（必填）"},
                "sources": {
                    "type": "array",
                    "items": {"type": "object"},
                    "description": "来源列表（可选；空时仅返回骨架报告）"
                },
                "domain": {"type": "string", "description": "手动指定领域（默认 None=自动）"},
                "with_llm": {"type": "boolean", "default": False, "description": "是否调用 LLM 增强"},
                "output_format": {
                    "type": "string",
                    "enum": ["md", "json", "csv", "traced_md", "traced_csv", "lobehub"],
                    "default": "md"
                }
            },
            "required": ["subject"]
        }
    },
    # ═══════════════════════════════════════════════════════════════
    # v3.0.0 GA 新增工具（11 async + 1 stream = 12 个）
    # v3.0.0-beta Sprint 2 注册了 backend（handle_tools_call），但 TOOLS list 遗漏
    # v3.0.0 GA Sprint 4 补全，对外可见
    # ═══════════════════════════════════════════════════════════════
    {
        "name": "research_v3",
        "description": "异步研究（async_research 包装，一次性完整结果；流式请用 research_stream）。",
        "inputSchema": {
            "type": "object",
            "properties": {
                "subject": {"type": "string", "description": "调研主题（必填）"},
                "sources": {"type": "array", "items": {"type": "object"}, "description": "来源列表"},
                "domain": {"type": "string", "description": "手动指定领域"},
                "output_format": {"type": "string", "enum": ["md", "json", "csv", "lobehub"], "default": "md"},
                "lite": {"type": "boolean", "default": True, "description": "v2.4.0 轻量模式"}
            },
            "required": ["subject"]
        }
    },
    {
        "name": "research_stream",
        "description": "流式研究（7 步 yield 同步收集；同步 JSON-RPC 下收集全部 yield，SSE 客户端可享受首步优势）。",
        "inputSchema": {
            "type": "object",
            "properties": {
                "subject": {"type": "string", "description": "调研主题（必填）"},
                "sources": {"type": "array", "items": {"type": "object"}, "description": "来源列表"},
                "domain": {"type": "string", "description": "手动指定领域"},
                "output_format": {"type": "string", "enum": ["md", "json", "csv", "lobehub"], "default": "md"},
                "lite": {"type": "boolean", "default": True, "description": "v2.4.0 轻量模式"}
            },
            "required": ["subject"]
        }
    },
    # 11 个 v3 async 工具（Sprint 2 注册 backend，本 Sprint 4 补 TOOLS list）
    {
        "name": "manage_keys",
        "description": "Key 生命周期管理（v1.0.1 新增）：list / stat / rotate / revoke。所有输出脱敏（仅指纹）。",
        "inputSchema": {
            "type": "object",
            "properties": {
                "action": {"type": "string", "enum": ["list", "stat", "rotate", "revoke"],
                           "description": "操作类型（list=列出全部脱敏 key；stat=健康/用量；rotate=轮换；revoke=吊销）"},
                "provider": {"type": "string", "description": "provider 名（deepseek/openai/exa 等，list 可省略）"},
                "fingerprint": {"type": "string", "description": "revoke 用：key 指纹子串"}
            },
            "required": ["action"]
        }
    },
    {
        "name": "key_usage",
        "description": "Key 用量/成本报表（v1.0.1 新增）：基于 ~/.infoseek/key_usage.json 输出各 provider 调用数与估算成本。",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "qcm_query",
        "description": "反向调用 QCM：质量危机问题的 4 形态输出（case_application/decision_card/assessment_report/quick_response）。QCM 未安装时优雅降级返回 degraded。",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "质量问题描述（必填）"},
                "form": {"type": "string", "enum": ["case-application", "decision-card", "assessment-report", "quick-response"],
                         "description": "输出形态（可选）"}
            },
            "required": ["query"]
        }
    },
    {
        "name": "identity_attribution",
        "description": "身份归因（v1.5.0 新增）：已知用户名 → 跨平台账号锚点 + 人因验证（Maigret→Sherlock→AccountTrustScorer 链）。合规：需 INFOSEEK_ENABLE_IDENTITY_ATTRIBUTION=1 且 consent=true 显式授权；未满足任一 → blocked 显式报错（不静默返回空）。",
        "inputSchema": {
            "type": "object",
            "properties": {
                "username": {"type": "string", "description": "目标用户名（必填）"},
                "consent": {"type": "boolean", "default": False,
                            "description": "用户授权（涉个人 OSINT 合规闸，须显式 True）"},
                "max_results": {"type": "integer", "default": 10, "minimum": 1, "maximum": 50}
            },
            "required": ["username"]
        }
    },
    {
        "name": "account_forensics",
        "description": "账号深度取证（v1.6.0 融入新增）：显式投喂账号数据集 → 四层取证报告（L1统计红旗 + L2图结构协调集群 + 时序同步组 + L3 ML，含盲区边界声明）。输入 dataset={meta:[{id,followers,following,posts,er}], likes?, growth?, edges?} 或文件路径；与 identity_attribution 构成「发现→取证」双子工具。合规：需 INFOSEEK_ENABLE_FAKE_DETECT=1 且 consent=true；未满足任一 → blocked 显式报错。充分性不足（缺时序/ER/图谱）→ degraded insufficient_signals（缺数据≠水军，建议降级 AccountTrustScorer）。",
        "inputSchema": {
            "type": "object",
            "properties": {
                "dataset": {
                    "type": ["object", "string"],
                    "description": "账号数据集：{meta:[{id,followers,following,posts,er,group_label?}], likes:{id:[每日点赞]}, growth:{id:[每日涨粉]}, edges:[[a,b]]} 或 CSV/JSON 文件路径（经 data_adapter 自动接入）"
                },
                "target_accounts": {
                    "type": "array", "items": {"type": "string"},
                    "description": "可选：只返回这些账号的 verdict（默认全部）"
                },
                "consent": {"type": "boolean", "default": False,
                            "description": "用户授权（涉个人行为画像合规闸，须显式 True）"}
            },
            "required": ["dataset", "consent"]
        }
    },
]

# ═══════════════════════════════════════════════════════════════
# v1.0.0 工具合并：MCP 暴露面 25 → 13
# 规范集 = 11 个 async + research_v3 + research_stream；
# 废弃集 = 11 个 sync + research（并存期保留：tools/call 仍响应，
# 但结果附 deprecated 标记 + 迁移提示；tools/list 不再暴露）。
# ═══════════════════════════════════════════════════════════════
_CANONICAL_TOOL_NAMES = {
    'search_anchors_async', 'fetch_content_async', 'save_archive_async',
    'check_dedup_async', 'dedup_stats_async', 'fuse_analysis_async',
    'cross_subject_analysis_async', 'summarize_content_async',
    'conflict_detection_async', 'score_source_async',
    'score_contradiction_async', 'research_v3', 'research_stream',
    'manage_keys', 'key_usage',  # v1.0.1 PATCH: Key 管理工具
    'qcm_query',  # V8.4: QCM 反向工具（跨 skill 协同）
    'identity_attribution',  # v1.5.0: 身份归因（T2/G2）
    'account_forensics',  # v1.6.0 融入: 账号取证（B1，发现→取证双子）
}

_DEPRECATED_MIGRATION = {
    'search_anchors': 'search_anchors_async',
    'fetch_content': 'fetch_content_async',
    'save_archive': 'save_archive_async',
    'check_dedup': 'check_dedup_async',
    'dedup_stats': 'dedup_stats_async',
    'fuse_analysis': 'fuse_analysis_async',
    'cross_subject_analysis': 'cross_subject_analysis_async',
    'summarize_content': 'summarize_content_async',
    'conflict_detection': 'conflict_detection_async',
    'score_source': 'score_source_async',
    'score_contradiction': 'score_contradiction_async',
    'research': 'research_v3',
}

DEPRECATED_TOOLS = [t for t in TOOLS if t['name'] not in _CANONICAL_TOOL_NAMES]

# v1.0.1 PATCH / G12: async 工具定义由 sync 运行时生成（消除手工重复 + 修复字段描述缺失）
_ASYNC_GENERATED = []
for _sync_name, _async_name in _DEPRECATED_MIGRATION.items():
    # research→research_v3 映射跳过：research_v3 为原生定义，不生成副本
    if _async_name in ('research_v3',):
        continue
    _src = next((t for t in TOOLS if t['name'] == _sync_name), None)
    if _src is not None:
        import copy as _copy_mod
        _copy = _copy_mod.deepcopy(_src)
        _copy['name'] = _async_name
        _copy['description'] = '（v1.0.1 由 sync 定义生成，schema 字段描述完整）' + _src.get('description', '')
        _ASYNC_GENERATED.append(_copy)
TOOLS = TOOLS + _ASYNC_GENERATED

for _t in DEPRECATED_TOOLS:
    _t['deprecated'] = True
    _t['migrate_to'] = _DEPRECATED_MIGRATION.get(_t['name'], '')
TOOLS = [t for t in TOOLS if t['name'] in _CANONICAL_TOOL_NAMES]
# 清理规范工具描述中的「异步版」历史前缀（v1.0.0 起 async 即为规范入口）
for _t in TOOLS:
    _d = _t.get('description', '')
    if _d.startswith('v3.0.0 GA 异步版 '):
        _t['description'] = _d.replace('v3.0.0 GA 异步版 ', '', 1)

# ── MCP 消息处理 ──
def send_message(msg: Dict[str, Any]):
    """发送 MCP 消息（JSON-RPC 2.0 over stdio）"""
    sys.stdout.write(json.dumps(msg, ensure_ascii=False) + '\n')
    sys.stdout.flush()


def receive_message() -> Dict[str, Any]:
    """接收 MCP 消息"""
    line = sys.stdin.readline()
    if not line:
        return None
    try:
        return json.loads(line)
    except json.JSONDecodeError as e:
        return {"error": f"JSON decode failed: {e}"}


def handle_initialize(req_id: int, params: Dict) -> Dict:
    return {
        "jsonrpc": "2.0",
        "id": req_id,
        "result": {
            "protocolVersion": PROTOCOL_VERSION,
            "capabilities": {"tools": {}},
            "serverInfo": {"name": SERVER_NAME, "version": SERVER_VERSION}
        }
    }


def handle_tools_list(req_id: int, params: Dict) -> Dict:
    return {
        "jsonrpc": "2.0",
        "id": req_id,
        "result": {"tools": TOOLS}
    }


def handle_tools_call(req_id: int, params: Dict) -> Dict:
    # v1.0.0 工具合并：废弃名 → 转发到规范名（async），结果附 deprecated 标记
    original_name = params.get('name')
    tool_name = original_name
    args = params.get('arguments', {})
    migrated = _DEPRECATED_MIGRATION.get(original_name)
    if migrated:
        tool_name = migrated

    try:
        if tool_name == "search_anchors":
            result = tool_search_anchors(args)
        elif tool_name == "fetch_content":
            result = tool_fetch_content(args)
        elif tool_name == "save_archive":
            result = tool_save_archive(args)
        elif tool_name == "check_dedup":
            result = tool_check_dedup(args)
        elif tool_name == "dedup_stats":
            result = tool_dedup_stats(args)
        elif tool_name == "fuse_analysis":
            result = tool_fuse_analysis(args)
        elif tool_name == "cross_subject_analysis":
            result = tool_cross_subject_analysis(args)
        elif tool_name == "summarize_content":
            result = tool_summarize_content(args)
        elif tool_name == "conflict_detection":
            result = tool_conflict_detection(args)
        elif tool_name == "score_source":
            result = tool_score_source(args)
        elif tool_name == "score_contradiction":
            result = tool_score_contradiction(args)
        elif tool_name == "research":
            result = tool_research(args)
        # v3.0.0-beta PATCH: 新增 async 工具 + research_stream（向后兼容：旧工具保留）
        elif tool_name == "research_v3":
            result = _handle_async_research_wrapper(args)
        elif tool_name == "research_stream":
            result = _handle_research_stream_sync(args)
        # v3.0.0 GA PATCH: 11 个 async 工具 backend（asyncio.to_thread 包装同步实现）
        elif tool_name == "search_anchors_async":
            result = _handle_async_wrapper("search_anchors", args)
        elif tool_name == "fetch_content_async":
            result = _handle_async_wrapper("fetch_content", args)
        elif tool_name == "save_archive_async":
            result = _handle_async_wrapper("save_archive", args)
        elif tool_name == "check_dedup_async":
            result = _handle_async_wrapper("check_dedup", args)
        elif tool_name == "dedup_stats_async":
            result = _handle_async_wrapper("dedup_stats", args)
        elif tool_name == "fuse_analysis_async":
            result = _handle_async_wrapper("fuse_analysis", args)
        elif tool_name == "cross_subject_analysis_async":
            result = _handle_async_wrapper("cross_subject_analysis", args)
        elif tool_name == "summarize_content_async":
            result = _handle_async_wrapper("summarize_content", args)
        elif tool_name == "conflict_detection_async":
            result = _handle_async_wrapper("conflict_detection", args)
        elif tool_name == "score_source_async":
            result = _handle_async_wrapper("score_source", args)
        elif tool_name == "score_contradiction_async":
            result = _handle_async_wrapper("score_contradiction", args)
        # v1.0.1 PATCH: Key 管理工具（KeyManager）
        elif tool_name == "manage_keys":
            result = tool_manage_keys(args)
        elif tool_name == "key_usage":
            result = tool_key_usage(args)
        elif tool_name == "qcm_query":
            result = tool_qcm_query(args)
        elif tool_name == "identity_attribution":
            result = tool_identity_attribution(args)
        elif tool_name == "account_forensics":
            result = tool_account_forensics(args)
        else:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32601, "message": f"Tool not found: {tool_name}"}
            }

        # 废弃工具：注入迁移标记（并存期行为，不阻断调用）
        if migrated and isinstance(result, dict):
            result = dict(result)
            result['deprecated'] = True
            result['migrate_to'] = tool_name

        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "content": [{"type": "text", "text": json.dumps(result, ensure_ascii=False, indent=2)}]
            }
        }
    except Exception as e:
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {"code": -32603, "message": f"Internal error: {str(e)}"}
        }


def run_stdio_server():
    """stdio 传输 MCP 服务器"""
    print(f"[infoseek-mcp] starting stdio server v{SERVER_VERSION}", file=sys.stderr)

    while True:
        msg = receive_message()
        if not msg:
            break

        method = msg.get('method', '')
        req_id = msg.get('id')
        params = msg.get('params', {})

        if method == 'initialize':
            response = handle_initialize(req_id, params)
        elif method == 'notifications/initialized':
            continue  # 无响应
        elif method == 'tools/list':
            response = handle_tools_list(req_id, params)
        elif method == 'tools/call':
            response = handle_tools_call(req_id, params)
        else:
            response = {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32601, "message": f"Method not found: {method}"}
            }

        send_message(response)


def mask_token(token: str) -> str:
    """Token 脱敏（v1.6.1 加固：日志中不显示完整 token）"""
    if not token:
        return "(empty)"
    if len(token) <= 8:
        return "***"
    return f"{token[:4]}***{token[-4:]}"


def check_auth(headers: Dict[str, str], require_token: bool, expected_token: Optional[str]) -> bool:
    """检查 Bearer Token 认证（v1.6.1 加固：错误信息更友好 + 详细化）

    返回: bool（True=通过，False=拒绝）
    """
    if not require_token:
        return True
    auth = headers.get('Authorization', '')
    if not auth:
        return False
    if not auth.startswith('Bearer '):
        return False
    token = auth[7:]
    if not token:
        return False
    # V8.4 C 类：OAuth JWT（infoseek. 前缀）→ 校验签名 + 有效期（admin 全放行）
    if token.startswith("infoseek.") and _AUTH_MANAGER is not None:
        return _AUTH_MANAGER.verify(token) is not None
    # 优先级: --token 参数 > 环境变量 > 拒绝
    if expected_token:
        return secrets.compare_digest(token, expected_token)
    elif AUTH_TOKEN:
        return secrets.compare_digest(token, AUTH_TOKEN)
    else:
        # 启用 --require-token 但未配置 token → 全部拒绝
        return False


def get_token_source(fixed_token: Optional[str]) -> str:
    """Token 来源诊断（v1.6.1 加固：明确显示 token 来源）"""
    if fixed_token:
        return f"--token ({mask_token(fixed_token)})"
    elif AUTH_TOKEN:
        return f"env INFOSEEK_AUTH_TOKEN ({mask_token(AUTH_TOKEN)})"
    else:
        return "未配置（认证将拒绝所有请求）"


# ── v1.6.2 新增：审计日志 ──
def write_audit_log(method: str, tool_name: str = None, client_ip: str = "unknown", status: int = 200):
    """写入审计日志（JSON 行格式，不泄露 token/敏感数据）"""
    import json as _json
    record = {
        "time": datetime.now().isoformat(),
        "method": method,
        "tool": tool_name,
        "client_ip": client_ip,
        "status": status
    }
    try:
        AUDIT_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with AUDIT_LOG_PATH.open('a', encoding='utf-8') as f:
            f.write(_json.dumps(record, ensure_ascii=False) + '\n')
    except Exception as e:
        sys.stderr.write(f"[audit] write failed: {e}\n")


def increment_tool_counter(tool_name: str):
    """增加工具调用计数"""
    TOOL_CALL_COUNTER[tool_name] = TOOL_CALL_COUNTER.get(tool_name, 0) + 1

def run_sse_server(port: int, require_token: bool, fixed_token: Optional[str]):
    """SSE 传输（HTTP + Bearer Token 认证）"""

    class SSEHandler(BaseHTTPRequestHandler):
        """SSE 请求处理器"""
        # SSE 客户端连接池
        clients = []

        def log_message(self, format, *args):
            """自定义日志（避免默认 stderr 噪声）"""
            sys.stderr.write(f"[sse] {self.address_string()} - {format % args}\n")

        def _send_json(self, status: int, payload: Dict[str, Any]):
            """发送 JSON 响应"""
            self.send_response(status)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(payload, ensure_ascii=False).encode('utf-8'))

        def _send_sse_event(self, event: str, data: str):
            """发送 SSE 事件"""
            self.wfile.write(f"event: {event}\n".encode())
            self.wfile.write(f"data: {data}\n\n".encode())
            self.wfile.flush()

        def do_OPTIONS(self):
            """CORS 预检"""
            self.send_response(204)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
            self.end_headers()

        def _handle_oauth_token(self):
            """OAuth 2.0 client_credentials token 端点（POST /oauth/token，无需认证）"""
            content_length = int(self.headers.get('Content-Length', 0) or 0)
            body = self.rfile.read(content_length).decode('utf-8') if content_length else ''
            params = {}
            if body:
                try:
                    parsed = parse_qs(body)
                    params = {k: v[0] for k, v in parsed.items()}
                except Exception:
                    params = {}
            if _AUTH_MANAGER is None:
                self._send_json(501, {
                    "error": "not_implemented",
                    "hint": "Infoseek 未启用 OAuth（infoseek_auth 缺失）",
                })
                return
            cid = params.get("client_id", "")
            csec = params.get("client_secret", "")
            scope_raw = params.get("scope", "")
            scope = scope_raw.split() if scope_raw else None
            try:
                result = _AUTH_MANAGER.client_credentials(cid, csec, scope)
                write_audit_log("POST", "/oauth/token", self.address_string(), 200)
                self._send_json(200, result)
            except ValueError:
                write_audit_log("POST", "/oauth/token", self.address_string(), 401)
                self._send_json(401, {
                    "error": "invalid_client",
                    "error_description": "client_id 或 client_secret 无效",
                })

        def do_POST(self):
            """POST /messages /rpc — JSON-RPC；POST /tools/<name> — REST 桥（v1.0.0）"""
            # V8.4 C 类：OAuth 2.0 token 端点（无需认证）
            if self.path == '/oauth/token':
                self._handle_oauth_token()
                return
            if not check_auth(dict(self.headers), require_token, fixed_token):
                write_audit_log("POST", self.path, self.address_string(), 401)
                self._send_json(401, {
                    "error": "Unauthorized",
                    "hint": "需要 Bearer Token。请设置 Authorization: Bearer <token> 头",
                    "expected_token_source": get_token_source(fixed_token) if require_token else None
                })
                return

            # v1.0.0 REST 桥：POST /tools/<tool_name> — 每个生态工具映射为独立端点
            # （供 Coze/Dify 等按 OpenAPI 导入的平台使用；内部仍走 JSON-RPC 分发）
            if self.path.startswith('/tools/'):
                tool_name = self.path[len('/tools/'):].strip('/')
                if not tool_name:
                    self._send_json(400, {"error": "Missing tool name",
                                          "hint": "POST /tools/<tool_name>"})
                    return
                content_length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_length).decode('utf-8') if content_length else '{}'
                try:
                    raw = json.loads(body) if body.strip() else {}
                except json.JSONDecodeError as e:
                    self._send_json(400, {"error": f"Invalid JSON: {e}"})
                    return
                # 兼容 {arguments: {...}} 与裸参数对象两种请求体
                arguments = raw.get('arguments', raw) if isinstance(raw, dict) else {}
                resp = handle_tools_call(1, {"name": tool_name, "arguments": arguments})
                if 'error' in resp:
                    self._send_json(400, {"error": resp['error']})
                    return
                increment_tool_counter(tool_name)
                write_audit_log("POST", self.path, self.address_string(), 200)
                self._send_json(200, resp['result'])
                return

            if self.path not in ('/messages', '/rpc'):
                write_audit_log("POST", self.path, self.address_string(), 404)
                self._send_json(404, {"error": "Not Found", "hint": "POST /messages or /rpc for JSON-RPC"})
                return

            # 读取请求体
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length == 0:
                self._send_json(400, {"error": "Empty body"})
                return

            body = self.rfile.read(content_length).decode('utf-8')
            try:
                msg = json.loads(body)
            except json.JSONDecodeError as e:
                self._send_json(400, {"error": f"Invalid JSON: {e}"})
                return

            # 路由到 handler
            method = msg.get('method', '')
            req_id = msg.get('id')
            params = msg.get('params', {})

            # v1.6.2：工具调用计数 + 审计
            tool_name = None
            if method == 'tools/call':
                tool_name = params.get('name')
                if tool_name:
                    increment_tool_counter(tool_name)

            if method == 'initialize':
                response = handle_initialize(req_id, params)
            elif method == 'notifications/initialized':
                self._send_json(204, {})
                write_audit_log(method, tool_name, self.address_string(), 204)
                return
            elif method == 'tools/list':
                response = handle_tools_list(req_id, params)
            elif method == 'tools/call':
                response = handle_tools_call(req_id, params)
            else:
                response = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32601, "message": f"Method not found: {method}"}
                }

            self._send_json(200, response)
            write_audit_log(method, tool_name, self.address_string(), 200)

        def do_GET(self):
            """GET /sse（流式）/ GET /health（健康检查）/ GET /auth-check（token 配置诊断）"""
            # /health 不需要认证（K8s 探针场景）— v1.6.2 增强：含 uptime + 工具调用统计
            if self.path == '/health':
                uptime = int(time.time() - SERVER_START_TIME)
                self._send_json(200, {
                    "status": "ok",
                    "version": SERVER_VERSION,
                    "tools": len(TOOLS),
                    "transport": "sse",
                    "uptime_seconds": uptime,
                    "tool_call_stats": dict(TOOL_CALL_COUNTER)
                })
                return

            # /auth-check v1.6.2 新增：诊断 token 配置（无需 token，但返回 token 状态）
            if self.path == '/auth-check':
                self._send_json(200, {
                    "auth_required": require_token,
                    "token_source": get_token_source(fixed_token),
                    "version": SERVER_VERSION,
                    "note": "此端点不暴露 token 本身，仅显示来源诊断"
                })
                return

            # 其他 GET 端点需要认证
            if not check_auth(dict(self.headers), require_token, fixed_token):
                write_audit_log("GET", self.path, self.address_string(), 401)
                self._send_json(401, {
                    "error": "Unauthorized",
                    "hint": "需要 Bearer Token。请设置 Authorization: Bearer <token> 头",
                    "expected_token_source": get_token_source(fixed_token) if require_token else None
                })
                return

            if self.path != '/sse':
                write_audit_log("GET", self.path, self.address_string(), 404)
                self._send_json(404, {"error": "Not Found", "hint": "GET /sse, /health, or /auth-check"})
                return

            # SSE 响应头
            self.send_response(200)
            self.send_header('Content-Type', 'text/event-stream')
            self.send_header('Cache-Control', 'no-cache')
            self.send_header('Connection', 'keep-alive')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

            # 发送 endpoint 事件（客户端拿到 POST 端点）
            self._send_sse_event('endpoint', json.dumps({"uri": "/messages"}))

            # 保持连接（每 30s 发心跳，time 已在模块顶部导入）
            try:
                last_ping = time.time()
                while True:
                    time.sleep(1)
                    if time.time() - last_ping >= 30:
                        self._send_sse_event('ping', json.dumps({"ts": time.time()}))
                        last_ping = time.time()
            except (BrokenPipeError, ConnectionResetError):
                pass

    # 启动 HTTP 服务
    server = ThreadingHTTPServer(('127.0.0.1', port), SSEHandler)
    token_source = get_token_source(fixed_token) if require_token else "无认证"
    auth_status = f"（已启用 Bearer Token 认证 / 来源: {token_source}）" if require_token else "（无认证）"
    print(f"[infoseek-mcp] SSE/HTTP 服务器 v{SERVER_VERSION} 启动 http://127.0.0.1:{port} {auth_status}", file=sys.stderr)
    print(f"[infoseek-mcp] GET  /sse      → SSE 流式响应", file=sys.stderr)
    print(f"[infoseek-mcp] GET  /health   → 健康检查（无需认证）", file=sys.stderr)
    print(f"[infoseek-mcp] POST /messages → JSON-RPC 调用（双端点兼容）", file=sys.stderr)
    print(f"[infoseek-mcp] POST /rpc      → JSON-RPC 调用（短请求-响应）", file=sys.stderr)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print(f"\n[infoseek-mcp] 关闭 SSE/HTTP 服务器", file=sys.stderr)
        server.shutdown()


def main():
    parser = argparse.ArgumentParser(description='Infoseek MCP Server v1.5.2')
    parser.add_argument('--transport', default='stdio', choices=['stdio', 'sse'],
                        help='传输方式：stdio（默认）或 sse')
    parser.add_argument('--port', type=int, default=8080, help='SSE/HTTP 端口（默认 8080）')
    parser.add_argument('--require-token', action='store_true',
                        help='启用 Bearer Token 认证（SSE/HTTP 模式）')
    parser.add_argument('--token', default=None,
                        help='固定 Token（优先于环境变量 INFOSEEK_AUTH_TOKEN）')
    parser.add_argument('--list-tools', action='store_true', help='打印工具清单后退出')
    args = parser.parse_args()

    if args.list_tools:
        print(json.dumps(TOOLS, ensure_ascii=False, indent=2))
        return

    if args.transport == 'stdio':
        run_stdio_server()
    elif args.transport == 'sse':
        run_sse_server(
            port=args.port,
            require_token=args.require_token,
            fixed_token=args.token
        )
    else:
        print(f"[infoseek-mcp] 未知 transport: {args.transport}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()

