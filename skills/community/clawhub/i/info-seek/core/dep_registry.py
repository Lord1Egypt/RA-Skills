#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""core/dep_registry.py — Infoseek 外部依赖统一注册表（mod-v1.0.0）

S1 · 方向②阶段A「建表零回归」
============================
外部依赖治理现状（审计结论，2026-09-29 实测）：
  - 全仓 `except ImportError` 共 62 处，其中 **45 处为 core 包内部兄弟模块互导垫片**
    （state_dir / domain_router / qveris_client / conflict_* 等），属「脚本独立运行」
    兼容垫片，**不是外部依赖**；真正外部第三方依赖点仅 17 处（14 业务 + 3 测试）。
  - 10+ 套分散探测函数（_probe_camoufox / _probe_obscura / _probe_patchright /
    _probe_chromium / _probe_pypinyin / _probe_free / _probe_timeout …），口径漂移风险。
本模块把「装没装 / 能不能 import / 什么版本」收敛为唯一事实层。

分层（关键架构裁决）
--------------------
  下层 dep_registry（本模块）：事实层 —— 装没装 / 可 import / 版本
  上层 capability_registry（capabilities/registry.yaml）：策略层 —— 开不开 / 授权 / 降级
本模块**绝不** import capability_registry，保证单向依赖。

对外接口（S1 仅建表，**暂不接线**任何消费点）
-------------------------------------------
  dep_status(name)        -> dict 事实快照（声明/可用/版本/来源/降级/血缘）
  is_available(name)      -> bool
  import_optional(name)   -> module | object | None（永不抛错）
  require(name)           -> module | object | True（不可用抛 DependencyMissing）
  get_dep(name) / list_deps(kind)   声明查询
  reset()                 清空进程内缓存（测试用）
  registry_source()       事实来源：'yaml' | 'embedded'

S6/S7 接线（2026-09-30）
------------------------
  has_module(mod)             模块可 import（点分名；永不抛错）
  probe_token(tok)            单个 import:/path:/env:/which: 探测真假
  probe_tokens(toks, mode)    多探测项 any/all 组合
  which_path(cmd)             shutil.which → 路径 | None
l2_renderer / CLI 客户端在这些「事实原语」之上保留 TCP / 路径返回 / 缓存
glob / 隔离 venv 等消费层组合逻辑，保证探测口径收口前后零漂移。

设计约束
--------
- **零第三方硬依赖**：仅 stdlib；PyYAML 缺失或表文件缺失时回退内嵌 `_DEFAULT_DEPS`。
- **委托既有桥**：jieba / pypinyin 经 `delegate` 委托 `core/jieba_bridge.py`，
  不重复探测（避免双轨重造，保持单一真源）。
- **双导入状态分裂防护**：加载尾部做 sys.modules 双向登记
  （`dep_registry` ↔ `core.dep_registry`，同 capability_registry 模式）。
- 版本维度：mod-v1.0.0（模块内部版本），非对外版本
  （对外唯一真源 `scripts/mcp_tools_common.SKILL_VERSION`）。
"""

from __future__ import annotations

import importlib
import importlib.util
import os
import shutil
import sys as _sys
import threading
from pathlib import Path
from typing import Any, Dict, List, Optional

__all__ = [
    'MOD_VERSION', 'DependencyMissing',
    'dep_status', 'is_available', 'import_optional', 'require',
    'get_dep', 'list_deps', 'reset', 'registry_source',
    # S6/S7：公共事实原语（供 l2_renderer / CLI 客户端 / 各探测点收口复用）
    'has_module', 'probe_token', 'probe_tokens', 'which_path',
]

MOD_VERSION = '1.1.0'

_CORE_DIR = Path(__file__).resolve().parent
_REGISTRY_PATH = _CORE_DIR.parent / 'deps' / 'registry.yaml'

# ── 双导入状态分裂防护（同 capability_registry G1）────────────────────
# 本模块既可能以顶层名 `dep_registry`（scripts/ 把 core/ 注入 sys.path）导入，
# 也可能以包路径 `core.dep_registry` 导入；两条路径各建一份模块对象会致
# `_cache` / `_status_cache` 分裂。加载时把自身登记到「另一个名字」。
for _alias in ('dep_registry', 'core.dep_registry'):
    if _alias != __name__ and _alias not in _sys.modules:
        _sys.modules[_alias] = _sys.modules[__name__]


class DependencyMissing(Exception):
    """外部依赖不可用。`code=0` 对齐 engine_lifecycle.classify 的「未安装/未知」语义。"""

    def __init__(self, name: str, detail: str = '', install_hint: str = ''):
        msg = f"外部依赖 '{name}' 不可用"
        if detail:
            msg += f"：{detail}"
        if install_hint:
            msg += f"（安装：{install_hint}）"
        super().__init__(msg)
        self.code = 0
        self.dep_name = name
        self.install_hint = install_hint
        self.detail = detail


# 内嵌默认（registry.yaml 缺失 / PyYAML 缺失时回退；与 deps/registry.yaml 保持同步）
_DEFAULT_DEPS: List[Dict[str, Any]] = [
    {'name': 'PyYAML', 'kind': 'python_pkg', 'pip': 'PyYAML', 'import': 'yaml',
     'version_floor': '6.0', 'required': True,
     'install_hint': 'pip install PyYAML>=6.0'},
    {'name': 'Jinja2', 'kind': 'python_pkg', 'pip': 'Jinja2', 'import': 'jinja2',
     'version_floor': '3.1', 'required': True,
     'install_hint': 'pip install jinja2>=3.1'},
    {'name': 'httpx', 'kind': 'python_pkg', 'import': 'httpx',
     'version_floor': '0.27', 'required': True,
     'install_hint': 'pip install httpx>=0.27'},
    {'name': 'jieba', 'kind': 'python_pkg', 'import': 'jieba',
     'version_floor': '0.42.1', 'required': False,
     'delegate': 'jieba_bridge:get_jieba', 'install_hint': 'pip install jieba'},
    {'name': 'pypinyin', 'kind': 'python_pkg', 'import': 'pypinyin',
     'version_floor': '0.55', 'required': False,
     'delegate': 'jieba_bridge:get_pypinyin', 'install_hint': 'pip install pypinyin'},
    {'name': 'summa', 'kind': 'python_pkg', 'import': 'summa',
     'version_floor': '1.2.0', 'required': False, 'install_hint': 'pip install summa'},
    {'name': 'opentelemetry', 'kind': 'python_pkg', 'import': 'opentelemetry',
     'required': False,
     'install_hint': 'pip install opentelemetry-api opentelemetry-sdk'},
    {'name': 'cryptography', 'kind': 'python_pkg', 'import': 'cryptography',
     'required': False, 'install_hint': 'pip install cryptography'},
    {'name': 'keyring', 'kind': 'python_pkg', 'import': 'keyring',
     'required': False, 'install_hint': 'pip install keyring'},
    {'name': 'schedule', 'kind': 'python_pkg', 'import': 'schedule',
     'required': False, 'install_hint': 'pip install schedule'},
    {'name': 'openai-whisper', 'kind': 'python_pkg', 'pip': 'openai-whisper',
     'import': 'whisper', 'required': False, 'install_hint': 'pip install openai-whisper'},
    {'name': 'playwright', 'kind': 'python_pkg', 'import': 'playwright',
     'version_floor': '1.44', 'required': False,
     'install_hint': 'pip install playwright（requirements-extra.txt）'},
    {'name': 'playwright-stealth', 'kind': 'python_pkg', 'pip': 'playwright-stealth',
     'import': 'playwright_stealth', 'required': False,
     'install_hint': 'pip install playwright-stealth'},
    {'name': 'patchright', 'kind': 'python_pkg', 'import': 'patchright',
     'required': False, 'install_hint': 'pip install patchright'},
    {'name': 'camoufox', 'kind': 'browser_binary',
     'probe': ['import:camoufox', 'path:~/.cache/camoufox/browsers/official'],
     'probe_mode': 'all', 'required': False,
     'install_hint': 'pip install camoufox && python -m camoufox fetch'},
    {'name': 'obscura', 'kind': 'browser_binary',
     'probe': ['which:obscura', 'env:INFOSEEK_OBSCURA_PATH', 'path:~/.infoseek/bin/obscura'],
     'probe_mode': 'any', 'required': False,
     'install_hint': '安装 obscura 二进制并置于 PATH（或设 INFOSEEK_OBSCURA_PATH）'},
    {'name': 'chromium', 'kind': 'browser_binary',
     'probe': ['env:CHROMIUM_PATH', 'which:chromium',
               'path:/usr/bin/chromium', 'path:/usr/lib/chromium/chromium'],
     'probe_mode': 'any', 'required': False,
     'install_hint': 'apt-get install chromium（或设置 CHROMIUM_PATH）'},
    {'name': 'maigret', 'kind': 'cli_binary', 'cli': 'maigret', 'pip': 'maigret',
     'required': False, 'install_hint': 'pip install maigret（隔离 venv 推荐）'},
    {'name': 'sherlock', 'kind': 'cli_binary', 'cli': 'sherlock', 'pip': 'sherlock-project',
     'required': False, 'install_hint': 'pip install sherlock-project（隔离 venv 推荐）'},
]

_VALID_KINDS = {'python_pkg', 'cli_binary', 'browser_binary'}

_lock = threading.Lock()
_cache: Optional[Dict[str, Dict[str, Any]]] = None
_status_cache: Dict[str, Dict[str, Any]] = {}
_source = 'unloaded'


# ── 加载 ────────────────────────────────────────────────────────────────

def _load_deps() -> Dict[str, Dict[str, Any]]:
    """加载 deps/registry.yaml → {name: decl}；PyYAML/文件缺失回退内嵌。"""
    global _cache, _source
    if _cache is not None:
        return _cache
    with _lock:
        if _cache is not None:
            return _cache
        items: Optional[List[Any]] = None
        src = 'embedded'
        try:
            if _REGISTRY_PATH.exists():
                try:
                    import yaml  # PyYAML（可选；缺失则回退内嵌）
                    data = yaml.safe_load(_REGISTRY_PATH.read_text(encoding='utf-8'))
                    if isinstance(data, dict):
                        items = data.get('deps')
                        src = 'yaml'
                except Exception:
                    items = None
        except Exception:
            items = None
        if not isinstance(items, list) or not items:
            items = _DEFAULT_DEPS
            src = 'embedded'
        _cache = {str(d.get('name')): d for d in items
                  if isinstance(d, dict) and d.get('name')}
        _source = src
        return _cache


# ── 探测原语 ───────────────────────────────────────────────────────────

def _has_module(mod: str) -> bool:
    """模块是否可 import（进程内已加载或 find_spec 可解析）。永不抛错。"""
    if not mod:
        return False
    try:
        if mod in _sys.modules:
            return True
        return importlib.util.find_spec(mod) is not None
    except Exception:
        return False


def _pkg_version(pip: str, imp: str) -> Optional[str]:
    """取已安装版本（importlib.metadata）；取不到返回 None。"""
    try:
        import importlib.metadata as _md
    except Exception:
        return None
    for dist in (pip, imp):
        if not dist:
            continue
        try:
            return _md.version(dist)
        except Exception:
            continue
    return None


def _probe_token(tok: str) -> bool:
    """声明式探测项：import:<mod> | path:<展开路径> | env:<VAR> | which:<cmd>。"""
    kind, _, val = str(tok).strip().partition(':')
    if kind == 'import':
        return _has_module(val)
    if kind == 'path':
        try:
            return Path(os.path.expanduser(val)).exists()
        except Exception:
            return False
    if kind == 'env':
        return bool(os.environ.get(val))
    if kind == 'which':
        return bool(shutil.which(val))
    return False


def has_module(mod: str) -> bool:
    """公共：模块是否可 import（已加载或 find_spec 可解析，支持点分名）。永不抛错。"""
    return _has_module(mod)


def probe_token(tok: str) -> bool:
    """公共：单个声明式探测项 import:/path:/env:/which: 的真假。永不抛错。"""
    return _probe_token(tok)


def probe_tokens(tokens, mode: str = 'any') -> bool:
    """公共：组合多个探测项（mode='any'|'all'）。空 tokens→False。永不抛错。"""
    toks = list(tokens or [])
    if not toks:
        return False
    results = [_probe_token(t) for t in toks]
    return all(results) if mode == 'all' else any(results)


def which_path(cmd: str) -> Optional[str]:
    """公共：shutil.which 封装，命中返回可执行路径，否则 None。永不抛错。"""
    if not cmd:
        return None
    try:
        return shutil.which(cmd)
    except Exception:
        return None


def _call_delegate(spec: str):
    """调用委托桥 `module:attr`（如 jieba_bridge:get_jieba）；不可用返回 None。

    候选模块名覆盖「顶层名」与「core. 包路径」两种导入方式，保证任一路径命中。
    """
    mod_name, _, attr = str(spec).partition(':')
    if not mod_name or not attr:
        return None
    cands = [mod_name]
    if not mod_name.startswith('core.'):
        cands.append('core.' + mod_name)
    cands.append(mod_name.split('.')[-1])
    for cand in cands:
        try:
            m = importlib.import_module(cand)
            fn = getattr(m, attr, None)
            if callable(fn):
                return fn()
        except Exception:
            continue
    return None


# ── 求值 ────────────────────────────────────────────────────────────────

def _evaluate(name: str, decl: Dict[str, Any]) -> Dict[str, Any]:
    kind = decl.get('kind', 'python_pkg')
    imp = decl.get('import') or ''
    pip = decl.get('pip') or imp
    version: Optional[str] = None
    detail = ''
    delegate = decl.get('delegate')
    if delegate:
        obj = _call_delegate(str(delegate))
        available = obj is not None
        detail = f"委托 {delegate} → {'可用' if available else '不可用'}"
    elif kind == 'python_pkg':
        available = _has_module(imp) if imp else False
        if available:
            version = _pkg_version(pip, imp)
        detail = f"import {imp}" if imp else ''
    else:
        toks = decl.get('probe') or []
        mode = decl.get('probe_mode', 'any')
        results = [(str(t), _probe_token(t)) for t in toks]
        if mode == 'all':
            available = bool(results) and all(r for _, r in results)
        else:
            available = any(r for _, r in results)
        detail = '; '.join(f"{t}={'Y' if r else 'N'}" for t, r in results)
    pip_hint = decl.get('install_hint') or (f"pip install {pip}" if pip else '')
    return {
        'name': name,
        'declared': True,
        'kind': kind,
        'available': bool(available),
        'installed': bool(available),
        'version': version,
        'required': bool(decl.get('required')),
        'source': _source,
        'pip_hint': pip_hint,
        'degrade': decl.get('degrade', ''),
        'detail': detail,
        'consumers': list(decl.get('consumers') or []),
    }


# ── 对外接口 ────────────────────────────────────────────────────────────

def dep_status(name: str, *, refresh: bool = False) -> Dict[str, Any]:
    """单个依赖的事实快照。未声明的依赖返回 declared=False（不抛错）。"""
    decl = _load_deps().get(name)
    if decl is None:
        return {'name': name, 'declared': False, 'kind': 'unknown',
                'available': False, 'installed': False, 'version': None,
                'required': False, 'source': _source, 'pip_hint': '',
                'degrade': '', 'detail': '未在 deps/registry.yaml 声明',
                'consumers': []}
    if not refresh:
        cached = _status_cache.get(name)
        if cached is not None:
            return cached
    st = _evaluate(name, decl)
    _status_cache[name] = st
    return st


def is_available(name: str) -> bool:
    return bool(dep_status(name).get('available'))


def import_optional(name: str):
    """尝试返回依赖模块 / 委托对象；不可用一律返回 None（永不抛错）。"""
    decl = _load_deps().get(name)
    if decl is None:
        return None
    delegate = decl.get('delegate')
    if delegate:
        return _call_delegate(str(delegate))
    imp = decl.get('import') or ''
    if not imp:
        return None
    try:
        return importlib.import_module(imp)
    except Exception:
        return None


def require(name: str):
    """返回可用依赖（可 import 者返回模块，CLI/浏览器返回 True）；不可用抛 DependencyMissing。"""
    decl = _load_deps().get(name)
    if decl is None:
        raise DependencyMissing(name, detail='未在 deps/registry.yaml 声明')
    st = dep_status(name)
    if not st.get('available'):
        raise DependencyMissing(name, detail=st.get('detail', ''),
                                install_hint=decl.get('install_hint', ''))
    if decl.get('delegate') or decl.get('import'):
        obj = import_optional(name)
        if obj is not None:
            return obj
    return True


def get_dep(name: str) -> Optional[Dict[str, Any]]:
    decl = _load_deps().get(name)
    return dict(decl) if decl is not None else None


def list_deps(kind: Optional[str] = None) -> List[Dict[str, Any]]:
    decls = [dict(d) for d in _load_deps().values()]
    if kind:
        decls = [d for d in decls if d.get('kind') == kind]
    return decls


def registry_source() -> str:
    """事实来源：'yaml'（表文件已加载）| 'embedded'（回退内嵌）。"""
    _load_deps()
    return _source


def reset() -> None:
    """清空进程内缓存（加载表 + 状态快照）；测试用。"""
    global _cache
    with _lock:
        _cache = None
        _status_cache.clear()
