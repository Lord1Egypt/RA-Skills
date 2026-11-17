#!/usr/bin/env python3
"""
ecosystem/base.py — 生态平台统一能力接口（v1.0.0）
================================================================

定义平台无关的输入/输出/配置契约，以及每生态适配器的抽象基类。

设计原则：
  - infoseek 核心是「平台无关的分析内核」；
  - 每个生态平台（WorkBuddy / ima / Claude / Codex / Dify / Coze / 通用 MCP）
    通过一个**薄适配器**接入，只处理五件事：
      1. 触发方式（trigger）    — 关键词 / 意图 / 工具声明 / 工作流节点 / 插件
      2. 采集能力（collection） — 宿主有 WebSearch 则注入，否则用内置（已修）搜索
      3. 凭据约定（credential） — 各平台 token/API key 的 env 与注入方式
      4. 状态位置（state）      — 数据目录 / 归档目录（已中立）
      5. 输出形态（output）     — 报告格式与交付方式
  - 配置一律 env-first：平台覆盖通过环境变量注入，代码不写死平台路径。
"""

from __future__ import annotations

import os
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional


# ═══════════════════════════════════════════════════════════════
# 统一数据契约
# ═══════════════════════════════════════════════════════════════

@dataclass
class ResearchInput:
    """平台无关的调研输入。"""
    subject: str
    sources: Optional[List[Dict[str, Any]]] = None   # 宿主注入的源（如 WorkBuddy WebSearch）
    domain: Optional[str] = None                     # 领域提示（可选）
    depth: int = 1                                   # 锚点深度（1-3）
    max_sources: int = 15
    lite: bool = False                               # 轻量模式（跳过 Wikidata 等重步骤）
    output_format: str = 'md'                        # md / json
    # ── P3：多模态附件（由宿主注入，不自研采集）──
    attachments: Optional[List[Dict[str, Any]]] = None  # [{type: image/video/pdf, url|path, caption?}]
    # ── P3：共享知识库上下文（跨会话/跨生态沉淀）──
    kb_topics: Optional[List[str]] = None            # 需要带入上下文的沉淀主题

    @classmethod
    def from_kwargs(cls, **kw) -> "ResearchInput":
        allowed = {f.name for f in cls.__dataclass_fields__.values()}
        return cls(**{k: v for k, v in kw.items() if k in allowed})


@dataclass
class ResearchOutput:
    """平台无关的调研输出。"""
    subject: str
    markdown: str = ''
    sources: List[Dict[str, Any]] = field(default_factory=list)
    conflicts: List[Dict[str, Any]] = field(default_factory=list)
    entities: List[Dict[str, Any]] = field(default_factory=list)
    coverage: Dict[str, Any] = field(default_factory=dict)
    engine: str = 'infoseek-core'                    # 实际引擎（zerodep/jieba/...）
    ecosystem: str = 'generic'                       # 出站生态
    raw: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_core_result(cls, result: Dict[str, Any], subject: str,
                         ecosystem: str, engine: str) -> "ResearchOutput":
        """把 infoseek_core_v2 的结果 dict 映射为平台无关输出。"""
        return cls(
            subject=subject,
            markdown=result.get('markdown', '') or result.get('report', ''),
            sources=result.get('sources', []) or result.get('scored_sources', []),
            conflicts=result.get('conflicts', []),
            entities=result.get('entities', []),
            coverage=result.get('coverage', {}),
            engine=engine,
            ecosystem=ecosystem,
            raw=result,
        )

    def to_dict(self) -> dict:
        return {
            'subject': self.subject,
            'markdown': self.markdown,
            'sources': self.sources,
            'conflicts': self.conflicts,
            'entities': self.entities,
            'coverage': self.coverage,
            'engine': self.engine,
            'ecosystem': self.ecosystem,
        }


@dataclass
class Config:
    """env-first 运行配置（状态层中立后的统一入口）。"""
    data_dir: Path = field(default_factory=lambda: Path.home() / '.infoseek')
    db_path: Path = field(default_factory=lambda: Path.home() / '.infoseek' / 'infoseek_db.json')
    archives_dir: Path = field(default_factory=lambda: Path.home() / 'infoseek-archives')
    transport: str = 'stdio'             # stdio | sse | http
    host: str = '127.0.0.1'
    port: int = 8765
    auth_token: Optional[str] = None
    search_engine: str = 'auto'          # auto | ddg | bing | wikipedia | jina | ai | builtin
    parallel: bool = True                # 层内并行合并（INFOSEEK_SEARCH_PARALLEL=0 回退顺序）
    min_results: int = 3                 # 质量门控阈值（INFOSEEK_SEARCH_MIN_RESULTS）
    reserve_quota: bool = True           # 配额保护（INFOSEEK_RESERVE_QUOTA=0 关闭）
    reserved: str = ''                   # 固定保留引擎（INFOSEEK_SEARCH_RESERVED=a[,b]）
    prefer_nlp: str = 'auto'             # auto | jieba | summa | zerodep
    min_anchors: int = 3

    @classmethod
    def from_env(cls) -> "Config":
        """env-first：INFOSEEK_* 环境变量优先，兜底 ~/.infoseek（与 state_dir 一致）。"""
        root = Path.home() / '.infoseek'
        data_dir = Path(os.environ.get('INFOSEEK_DATA_DIR', str(root)))
        db_env = os.environ.get('INFOSEEK_DB')
        db_path = Path(db_env) if db_env else (data_dir / 'infoseek_db.json')
        arch_env = os.environ.get('INFOSEEK_ARCHIVE')
        archives_dir = Path(arch_env) if arch_env else (Path.home() / 'infoseek-archives')
        return cls(
            data_dir=data_dir,
            db_path=db_path,
            archives_dir=archives_dir,
            transport=os.environ.get('INFOSEEK_TRANSPORT', 'stdio'),
            host=os.environ.get('INFOSEEK_HOST', '127.0.0.1'),
            port=int(os.environ.get('INFOSEEK_PORT', '8765')),
            auth_token=os.environ.get('INFOSEEK_AUTH_TOKEN'),
            search_engine=os.environ.get('INFOSEEK_SEARCH_ENGINE', 'auto'),
            prefer_nlp=os.environ.get('INFOSEEK_PREFER_NLP', 'auto'),
            min_anchors=int(os.environ.get('INFOSEEK_MIN_ANCHORS', '3')),
            parallel=os.environ.get('INFOSEEK_SEARCH_PARALLEL', '1') != '0',
            min_results=int(os.environ.get('INFOSEEK_SEARCH_MIN_RESULTS', '3')),
            reserve_quota=os.environ.get('INFOSEEK_RESERVE_QUOTA', '1') != '0',
            reserved=os.environ.get('INFOSEEK_SEARCH_RESERVED', ''),
        )


# ═══════════════════════════════════════════════════════════════
# 适配器抽象基类
# ═══════════════════════════════════════════════════════════════

class EcosystemAdapter(ABC):
    """生态平台薄适配器：只实现五件事的差异 glue。"""

    name: str = 'generic'
    display_name: str = '通用 MCP'

    # ── 五件差异（子类必须实现）──

    @abstractmethod
    def trigger_spec(self) -> dict:
        """触发方式：关键词 / 意图 / 工具声明 / 工作流节点 / 插件。"""

    @abstractmethod
    def collection_spec(self) -> dict:
        """采集能力：inject（宿主注入 WebSearch）| builtin（内置搜索）| both。"""

    @abstractmethod
    def credential_spec(self) -> dict:
        """凭据约定：required（必须的 env）与 optional（可选 env）。"""

    @abstractmethod
    def state_spec(self) -> dict:
        """状态位置：数据目录 / 归档目录 / 是否支持本地持久化。"""

    @abstractmethod
    def output_spec(self) -> dict:
        """输出形态：格式 / 交付方式 / 是否归档。"""

    # ── P3：默认能力（可覆盖）──

    def multimodal_spec(self) -> dict:
        """多模态能力：host_inject（宿主注入附件）| none（不支持）。

        infoseek 不自研多模态采集——附件一律由宿主平台注入
        （ResearchInput.attachments），核心只做分析层透传。
        """
        return {'mode': 'none', 'supported_types': []}

    def kb_context(self, topic: str, limit: int = 5) -> list:
        """共享知识库上下文（P3）：从可信知识库取沉淀源。

        依托中立状态层 + trusted_kb；跨生态/跨会话沉淀可复用。
        返回 [{url, title, credibility, ...}]；无沉淀时返回 []。
        """
        try:
            import sys as _sys
            _sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))
            from trusted_kb import kb_lookup
            return kb_lookup(topic, limit=limit) or []
        except Exception:
            return []

    # ── 默认实现（可覆盖）──

    def config(self, cfg: Optional[Config] = None) -> Config:
        return cfg or Config.from_env()

    def resolve_collector(self, inp: ResearchInput, cfg: Config) -> List[Dict[str, Any]]:
        """按采集能力决议来源：宿主注入 > 内置（已修）搜索 > 空。

        返回 sources 列表（可直接交给 core.async_research）。
        P3：若请求 kb_topics，优先并入共享知识库沉淀源（去重）。
        """
        sources: List[Dict[str, Any]] = []
        # 1) 共享知识库沉淀（P3，跨会话可复用）
        if inp.kb_topics:
            seen = set()
            for t in inp.kb_topics:
                for kb in self.kb_context(t, limit=5):
                    url = kb.get('url', '') or kb.get('entry', '')
                    if url and url not in seen:
                        seen.add(url)
                        sources.append({
                            'url': url,
                            'title': kb.get('title') or kb.get('name', t),
                            'snippet': '',
                            'platform': kb.get('platform', 'kb'),
                        })
        # 2) 宿主注入来源
        if inp.sources:
            seen = {s.get('url') for s in sources}
            sources += [s for s in inp.sources if s.get('url') not in seen]
        # 3) 无宿主/无沉淀 → 内置搜索（builtin/both 生态）
        if not sources:
            spec = self.collection_spec()
            if spec.get('mode') in ('builtin', 'both'):
                sources = self._builtin_collect(inp, cfg)
        return sources

    def _builtin_collect(self, inp: ResearchInput, cfg: Config) -> List[Dict[str, Any]]:
        """内置搜索（v1.0.0 已修复降级链 + 覆盖率门控）。断网返回空。"""
        try:
            import sys as _sys
            _sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))
            import infoseek_pipeline as pipe
            anchors = pipe.industry_to_anchors(
                inp.subject, min_anchors=min(cfg.min_anchors, 1))
            return [
                {'url': a.get('entry', ''), 'title': a.get('name', ''),
                 'snippet': '', 'platform': a.get('platform', 'web')}
                for a in anchors
            ]
        except Exception:
            return []

    async def run(self, inp: ResearchInput,
                  cfg: Optional[Config] = None) -> ResearchOutput:
        """端到端执行：决议来源 → 调核心 → 映射为 ResearchOutput。

        子类可覆盖以注入生态特定行为（如 ima 无搜索 → builtin）。
        """
        cfg = self.config(cfg)
        sources = self.resolve_collector(inp, cfg)
        import sys as _sys
        _sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))
        import infoseek_core_v2 as core
        result = await core.async_research(
            inp.subject,
            sources=sources or None,
            domain=inp.domain,
            output_format=inp.output_format,
            lite=inp.lite,
        )
        engine = self._detect_engine()
        return ResearchOutput.from_core_result(
            result, inp.subject, ecosystem=self.name, engine=engine)

    def _detect_engine(self) -> str:
        """报告实际 NLP 引擎（用于审计）。"""
        try:
            import sys as _sys
            _sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))
            from infoseek_zerodep_nlp import _optional_jieba, _optional_summa
            txt = '检测'  # 探测包是否可用
            if _optional_jieba(txt, 5):
                return 'jieba'
            if _optional_summa(txt, 5):
                return 'summa'
            return 'zerodep'
        except Exception:
            return 'zerodep'

    def describe(self) -> dict:
        """适配器自述（审计/注册用）。"""
        return {
            'name': self.name,
            'display_name': self.display_name,
            'trigger': self.trigger_spec(),
            'collection': self.collection_spec(),
            'credential': self.credential_spec(),
            'state': self.state_spec(),
            'output': self.output_spec(),
        }
