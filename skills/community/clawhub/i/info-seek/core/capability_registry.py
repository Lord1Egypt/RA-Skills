#!/usr/bin/env python3
"""
core/capability_registry.py — Infoseek 统一外部能力注册表（M0.2.5）

声明式能力管理：所有外部能力在 capabilities/registry.yaml 声明，
代码零改动接入。本模块负责加载 / 校验 / 查询 / 启用判定。

核心能力：
  - load_registry()            加载 YAML（PyYAML 缺失时回退内嵌默认）
  - get_capability(name)       取单条声明
  - list_capabilities(kind)    按族列举
  - is_enabled(name)           综合判定（registry.enabled ∩ env 覆盖 ∩ consent 占位）
  - requires_consent(name)     是否需合法用途授权
  - degrade_chain(name)        展开 degrade_to 链（去重、防环）
  - consent_granted(name)      运行期授权态（由调用方经合规闸口写入）

设计约束：
  - 零第三方硬依赖（PyYAML 缺失仅影响外部 YAML 加载，回退内嵌）
  - 与 engine_lifecycle 解耦：本模块只管"声明/启用"，健康/配额由 lifecycle 负责
  - 合规优先：requires_consent 能力在授权前 is_effective_enabled() 恒为 False
"""

from __future__ import annotations

import os
import threading
from pathlib import Path
from typing import Dict, List, Optional

_CORE_DIR = Path(__file__).parent
_REGISTRY_PATH = _CORE_DIR.parent / "capabilities" / "registry.yaml"

# ── G1（边界硬化 openfix）：单例别名，根治双导入路径状态分裂 ──────────
# 本模块既可能以顶层名 `capability_registry`（scripts/ 直接把 core/ 注入 sys.path）
# 导入，也可能以包路径 `core.capability_registry` 导入。两条路径会各建一份模块对象
# ⇒ `_cache` / `_consent_state` 模块级状态分裂（consent 授权跨消费方不可见）。
# 加载时把自身登记到「另一个名字」，保证任一路径都解析到同一模块对象。
import sys as _sys
for _alias in ("capability_registry", "core.capability_registry"):
    if _alias != __name__ and _alias not in _sys.modules:
        _sys.modules[_alias] = _sys.modules[__name__]

# 内嵌默认（与 capabilities/registry.yaml 同步；PyYAML 缺失时回退）
_DEFAULT_REGISTRY = {
    "version": 1,
    "capabilities": [
        {"name": "QVeris", "kind": "structured_data_api", "enabled": True,
         "requires_consent": False, "auth_env": "QVERIS_API_KEY", "weight": 0.9,
         "cost_model": "credits", "health_probe": "engine_lifecycle",
         "degrade_to": ["Exa", "Tavily", "manual_review"]},
        # G3（边界硬化）：Exa/Tavily 搜索替代层占位声明，消除悬空引用
        {"name": "Exa", "kind": "search_api", "enabled": False,
         "requires_consent": False, "auth_env": "EXA_API_KEY", "weight": 0.7,
         "cost_model": "credits", "health_probe": "engine_lifecycle",
         "degrade_to": [], "venv_hint": ""},
        {"name": "Tavily", "kind": "search_api", "enabled": False,
         "requires_consent": False, "auth_env": "TAVILY_API_KEY", "weight": 0.7,
         "cost_model": "credits", "health_probe": "engine_lifecycle",
         "degrade_to": [], "venv_hint": ""},
        {"name": "Maigret", "kind": "identity_attribution", "enabled": False,
         "requires_consent": True, "auth_env": "", "weight": 0.9,
         "cost_model": "none", "cli": "maigret", "health_probe": "engine_lifecycle",
         "degrade_to": ["Sherlock", "manual_review"],
         "venv_hint": "pip install maigret（隔离 venv 推荐）"},
        {"name": "Sherlock", "kind": "identity_attribution", "enabled": False,
         "requires_consent": True, "auth_env": "", "weight": 0.85,
         "cost_model": "none", "cli": "sherlock", "health_probe": "engine_lifecycle",
         "degrade_to": ["manual_review"],
         "venv_hint": "pip install sherlock-project（隔离 venv 推荐）"},
        # P0b 新增：账号人因验证器（L2 真人验证层，纯规则零依赖）
        {"name": "AccountTrustScorer", "kind": "identity_attribution", "enabled": False,
         "requires_consent": True, "auth_env": "", "weight": 0.8,
         "cost_model": "none", "health_probe": "none",
         "degrade_to": ["manual_review"], "venv_hint": ""},
        # P1a 新增：public-apis 免费 API 目录（L0 免费优先层）
        {"name": "PublicApisCatalog", "kind": "free_api", "enabled": False,
         "requires_consent": False, "auth_env": "", "weight": 0.5,
         "cost_model": "none", "health_probe": "none",
         "degrade_to": ["manual_review"], "venv_hint": ""},
        # P1b 新增：AgentKey 统一 MCP 网关（L1 网关付费层）
        {"name": "AgentKey", "kind": "gateway_api", "enabled": False,
         "requires_consent": True, "auth_env": "AGENTKEY_API_KEY", "weight": 0.9,
         "cost_model": "credits", "health_probe": "engine_lifecycle",
         "degrade_to": ["QVeris", "PublicApisCatalog", "manual_review"],
         "venv_hint": "pip install mcp（AgentKey 为 MCP 网关）"},
        # v1.4.2 新增：L2 多引擎渲染器（browser_engine 能力族）
        {"name": "L2Renderer", "kind": "browser_engine", "enabled": False,
         "requires_consent": False, "auth_env": "", "weight": 0.8,
         "cost_model": "none", "health_probe": "engine_lifecycle",
         "degrade_to": ["manual_review"],
         "venv_hint": "pip install camoufox patchright（Obscura 需二进制）"},
        # v1.6.0 融入：FakeDetect 账号深度取证（account_forensics 行为取证新族）
        # 验证层二级（AccountTrustScorer 升级）：L1统计+L2图结构+L3ML+时序同步
        # 命门=数据充分性门控（缺数据≠水军）；consent 双闸，默认 OFF
        {"name": "FakeDetect", "kind": "account_forensics", "enabled": False,
         "requires_consent": True, "auth_env": "", "weight": 0.85,
         "env_var": "INFOSEEK_ENABLE_FAKE_DETECT",
         "cost_model": "none", "health_probe": "engine_lifecycle",
         "degrade_to": ["AccountTrustScorer", "manual_review"],
         "venv_hint": "extensions/fake_detect/requirements.txt"},
        # GA12（v2.0.0）：3 个网络依赖能力化（沙箱受限 host，默认 OFF）
        {"name": "WikiVerify", "kind": "knowledge_verify", "enabled": False,
         "requires_consent": False, "auth_env": "", "weight": 0.6,
         "cost_model": "none", "health_probe": "none",
         "degrade_to": ["manual_review"],
         "network_boundary": "sandbox_restricted",
         "requires_hosts": ["www.wikidata.org", "query.wikidata.org",
                            "en.wikipedia.org", "zh.wikipedia.org"]},
        {"name": "L4Transcribe", "kind": "multimedia_transcribe", "enabled": False,
         "requires_consent": False, "auth_env": "", "weight": 0.5,
         "cost_model": "none", "health_probe": "none",
         "degrade_to": ["manual_review"],
         "network_boundary": "sandbox_restricted",
         "requires_hosts": ["storage.googleapis.com", "r.jina.ai"]},
        {"name": "PatentLookup", "kind": "patent_lookup", "enabled": False,
         "requires_consent": False, "auth_env": "", "weight": 0.5,
         "cost_model": "none", "health_probe": "none",
         "degrade_to": ["manual_review"],
         "network_boundary": "sandbox_restricted",
         "requires_hosts": ["patents.google.com", "github.com"]},
        {"name": "manual_review", "kind": "graceful_fallback", "enabled": True,
         "requires_consent": False, "auth_env": "", "weight": 0.0,
         "cost_model": "none", "health_probe": "none", "degrade_to": [],
         "network_boundary": "local", "requires_hosts": []},
    ],
    # GA12 host 台账（内嵌回退副本，与 registry.yaml network_boundaries 同步）
    "network_boundaries": [
        {"host": "qveris.ai", "boundary": "open",
         "used_by": ["QVeris"]},
        {"host": "qveris.cn", "boundary": "open",
         "used_by": ["QVeris"]},
        {"host": "www.wikidata.org", "boundary": "sandbox_restricted",
         "used_by": ["WikiVerify"]},
        {"host": "query.wikidata.org", "boundary": "sandbox_restricted",
         "used_by": ["WikiVerify"]},
        {"host": "en.wikipedia.org", "boundary": "sandbox_restricted",
         "used_by": ["WikiVerify"]},
        {"host": "zh.wikipedia.org", "boundary": "sandbox_restricted",
         "used_by": ["WikiVerify"]},
        {"host": "commons.wikimedia.org", "boundary": "sandbox_restricted",
         "used_by": []},
        {"host": "upload.wikimedia.org", "boundary": "sandbox_restricted",
         "used_by": []},
        {"host": "api.wikimedia.org", "boundary": "sandbox_restricted",
         "used_by": []},
        {"host": "storage.googleapis.com", "boundary": "sandbox_restricted",
         "used_by": ["L4Transcribe"]},
        {"host": "r.jina.ai", "boundary": "sandbox_restricted",
         "used_by": ["L4Transcribe"]},
        {"host": "patents.google.com", "boundary": "sandbox_restricted",
         "used_by": ["PatentLookup"]},
        {"host": "github.com", "boundary": "sandbox_restricted",
         "used_by": ["PatentLookup"]},
    ],
}

def consent_log_path() -> str:
    """合规授权日志路径（~/.infoseek/consent.log；M1.1/T8 审计 UX）。"""
    try:
        from core.state_dir import get_data_dir
    except Exception:
        try:
            from state_dir import get_data_dir
        except Exception:
            return ""
    return str(get_data_dir() / "consent.log")


def _append_consent_log(event: str, name: str) -> None:
    """授权/撤销落盘（非阻塞；审计失败不影响运行）。"""
    try:
        p = consent_log_path()
        if not p:
            return
        from datetime import datetime
        import os
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "a", encoding="utf-8") as f:
            f.write(f"{datetime.now().isoformat()} {event} {name}\n")
    except Exception:
        pass


_lock = threading.Lock()
_cache: Optional[Dict] = None
# 运行期授权态：cap_name -> bool（由合规闸口写入，非持久）
_consent_state: Dict[str, bool] = {}


def _load_raw() -> Dict:
    global _cache
    if _cache is not None:
        return _cache
    with _lock:
        if _cache is not None:
            return _cache
        data = None
        try:
            if _REGISTRY_PATH.exists():
                # S7：PyYAML 可用性经 dep_registry 事实层统一求值
                try:
                    import dep_registry as _dr
                except ImportError:
                    from core import dep_registry as _dr  # type: ignore
                if _dr.is_available("PyYAML"):
                    try:
                        import yaml
                        data = yaml.safe_load(_REGISTRY_PATH.read_text(encoding="utf-8"))
                    except ImportError:
                        data = None  # 回退内嵌
                # 无 PyYAML 时 data 保持 None → 回退 _DEFAULT_REGISTRY
        except Exception:
            data = None
        _cache = data if (isinstance(data, dict) and data.get("capabilities")) else _DEFAULT_REGISTRY
        return _cache


def _index() -> Dict[str, Dict]:
    raw = _load_raw()
    return {c["name"]: c for c in raw.get("capabilities", [])}


def get_capability(name: str) -> Optional[Dict]:
    return _index().get(name)


def list_capabilities(kind: Optional[str] = None) -> List[Dict]:
    caps = list(_index().values())
    if kind:
        caps = [c for c in caps if c.get("kind") == kind]
    return caps


def requires_consent(name: str) -> bool:
    cap = get_capability(name)
    return bool(cap and cap.get("requires_consent"))


def grant_consent(name: str) -> None:
    """合规闸口：记录运行期授权（非持久，进程级）+ 授权审计落盘（T8 consent.log）。"""
    with _lock:
        _consent_state[name] = True
    _append_consent_log("grant", name)


def revoke_consent(name: str) -> None:
    with _lock:
        _consent_state.pop(name, None)
    _append_consent_log("revoke", name)


def consent_granted(name: str) -> bool:
    with _lock:
        return bool(_consent_state.get(name))


def _env_override(name: str) -> Optional[bool]:
    """INFOSEEK_ENABLE_<NAME> 显式覆盖（1/true/on 启用，0/false/off 禁用）。
    支持条目显式 env_var 字段（兼容驼峰能力名的语义化 env 命名，
    如 FakeDetect -> INFOSEEK_ENABLE_FAKE_DETECT，缺省回退自动推导）。"""
    cap = get_capability(name)
    env_name = (cap or {}).get("env_var") or f"INFOSEEK_ENABLE_{name.upper()}"
    env = os.environ.get(env_name)
    if env is None:
        return None
    return env.lower() not in ("0", "false", "no", "off")


def is_enabled(name: str) -> bool:
    """声明层启用判定（不含 consent / 运行期健康）。"""
    cap = get_capability(name)
    if not cap:
        return False
    ov = _env_override(name)
    if ov is not None:
        return ov
    return bool(cap.get("enabled", False))


def is_effective_enabled(name: str) -> bool:
    """综合启用判定：声明启用 ∩ env 覆盖 ∩ （无需 consent 或 已授权）。"""
    if not is_enabled(name):
        return False
    if requires_consent(name) and not consent_granted(name):
        return False
    return True


def degrade_chain(name: str, _seen: Optional[set] = None) -> List[str]:
    """展开 degrade_to 链（去重、防自环），含起点。"""
    seen = _seen if _seen is not None else set()
    if name in seen:
        return []
    seen.add(name)
    chain = [name]
    cap = get_capability(name)
    if cap:
        for nxt in cap.get("degrade_to", []):
            if nxt in seen:
                continue
            chain.extend(degrade_chain(nxt, seen))
    return chain


# ── GA12（v2.0.0）网络边界访问器 ───────────────────────────
VALID_BOUNDARIES = ("open", "sandbox_restricted", "local")


def get_requires_hosts(name: str) -> List[str]:
    """能力声明的依赖 host 列表（未声明 → []）。"""
    cap = get_capability(name)
    if not cap:
        return []
    hosts = cap.get("requires_hosts") or []
    return [str(h) for h in hosts]


def get_network_boundary(name: str) -> Optional[str]:
    """能力的网络边界声明（open/sandbox_restricted/local）；未声明 → None。"""
    cap = get_capability(name)
    if not cap:
        return None
    b = cap.get("network_boundary")
    return b if b in VALID_BOUNDARIES else None


def get_network_boundaries() -> Dict[str, Dict]:
    """host 台账：{host: {boundary, used_by, evidence}}（含 yaml 与内嵌回退）。"""
    raw = _load_raw()
    out: Dict[str, Dict] = {}
    for item in raw.get("network_boundaries", []) or []:
        host = item.get("host")
        if host:
            out[host] = {
                "boundary": item.get("boundary"),
                "used_by": list(item.get("used_by") or []),
                "evidence": item.get("evidence", ""),
            }
    return out


def reload() -> None:
    """清空缓存（测试/热更新用）。"""
    global _cache
    with _lock:
        _cache = None


if __name__ == "__main__":
    import json
    print(json.dumps({
        "caps": [c["name"] for c in list_capabilities()],
        "maigret_enabled": is_enabled("Maigret"),
        "maigret_effective": is_effective_enabled("Maigret"),
        "maigret_degrade": degrade_chain("Maigret"),
    }, ensure_ascii=False, indent=2))
