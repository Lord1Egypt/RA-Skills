#!/usr/bin/env python3
"""
scripts/mirror_map.py — 镜像域映射（P2-2 G4 修复，v2.5.0）

策略①A 配置级落地：把不可达域名重写到可达镜像（受限网络环境）。

- 配置：references/mirror-domains.yaml（mappings: host → mirror_host）
- 默认空表 → resolve_url 恒返回原样（零行为变化）
- env:
  - INFOSEEK_MIRROR_MAP    配置文件路径覆盖
  - INFOSEEK_MIRROR_ENABLED 0 关闭（默认 1）
- 用法：
  from mirror_map import resolve_url
  url2 = resolve_url(url)   # 命中映射 → 重写 host；未命中/关闭 → 原样

零依赖：PyYAML 缺失时尝试 JSON 解析，再失败回退空表。
"""

import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, Optional

ROOT = Path(__file__).parent.parent
_DEFAULT_CONFIG = ROOT / 'references' / 'mirror-domains.yaml'

# ── S7：dep_registry 事实层惰性 accessor（外部依赖可用性统一求值，零漂移）──
_dr = None


def _dep_reg():
    global _dr
    if _dr is None:
        _cand = Path(__file__).resolve().parent.parent / "core"
        if str(_cand) not in sys.path:
            sys.path.insert(0, str(_cand))
        import dep_registry as _mod
        _dr = _mod
    return _dr

_CACHE: Optional[Dict[str, str]] = None
_CACHE_FAILED = False


def enabled() -> bool:
    v = os.environ.get('INFOSEEK_MIRROR_ENABLED', '1')
    return v not in ('0', 'false', 'False', 'no', 'off')


def _config_path() -> Path:
    env = os.environ.get('INFOSEEK_MIRROR_MAP')
    return Path(env) if env else _DEFAULT_CONFIG


def load_mirror_map(force: bool = False) -> Dict[str, str]:
    """加载 host→mirror_host 映射（模块缓存）

    缺失/解析失败 → 空表（resolve_url 恒原样，不阻断抓取）。
    """
    global _CACHE, _CACHE_FAILED
    if _CACHE is not None and not force:
        return _CACHE
    if _CACHE_FAILED and not force:
        return {}
    mapping: Dict[str, str] = {}
    p = _config_path()
    try:
        if p.exists():
            text = p.read_text(encoding='utf-8')
            data = None
            if _dep_reg().is_available("PyYAML"):
                try:
                    import yaml  # noqa: WPS433
                    data = yaml.safe_load(text)
                except ImportError:
                    data = None
            if data is None:
                try:
                    data = json.loads(text)
                except Exception:  # noqa: BLE001
                    data = None
            if isinstance(data, dict):
                m = data.get('mappings') or {}
                if isinstance(m, dict):
                    for k, v in m.items():
                        if k and v:
                            mapping[str(k).strip().lower()] = str(v).strip()
    except Exception:  # noqa: BLE001 配置缺失不阻断抓取
        _CACHE_FAILED = True
        mapping = {}
    _CACHE = mapping
    return mapping


def _host_of(url: str) -> str:
    m = re.search(r'(?:https?://)?(?:www\.)?([^/:?#]+)', url)
    return m.group(1).lower() if m else ''


def resolve_host(host: str) -> Optional[str]:
    """host → 镜像 host（未配置/关闭 → None）"""
    if not enabled():
        return None
    return load_mirror_map().get(host.lower())


def resolve_url(url: str) -> str:
    """URL 重写：host 命中映射 → 替换镜像 host；否则原样返回"""
    if not enabled() or not url:
        return url
    host = _host_of(url)
    if not host:
        return url
    mirror = load_mirror_map().get(host)
    if not mirror:
        return url
    # 替换 URL 中的 host（保留协议/路径/查询；host 大小写不敏感）
    new_url = re.sub(
        r'(https?://)(?:www\.)?' + re.escape(host) + r'(?=[/:?#]|$)',
        r'\1' + mirror, url, count=1, flags=re.IGNORECASE,
    )
    return new_url


def main():
    import sys
    if len(sys.argv) < 3 or sys.argv[1] != 'resolve':
        print("Usage: python -m scripts.mirror_map resolve <url>")
        print("       python -m scripts.mirror_map list")
        sys.exit(1)
    if sys.argv[1] == 'list':
        for k, v in load_mirror_map(force=True).items():
            print(f"  {k} → {v}")
        return
    url = sys.argv[2]
    orig = url
    new = resolve_url(url)
    print(f"原 URL: {orig}")
    print(f"重写后: {new}")
    print('（未变更 = 未命中映射 / 关闭）' if orig == new else '')


if __name__ == '__main__':
    main()