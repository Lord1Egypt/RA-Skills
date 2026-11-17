#!/usr/bin/env python3
"""
tests/test_mirror_map.py — 镜像域映射回归（P2-2 G4 修复，v2.5.0）

覆盖：
- M1 默认空表 → resolve_url 恒原样（零行为变化）
- M2 未命中 host → 原样返回
- M3 命中 host → 重写镜像（协议/路径/查询保留）
- M4 INFOSEEK_MIRROR_ENABLED=0 关闭 → 原样
- M5 env 路径覆盖（临时 yaml 生效）
- M6 www. 前缀剥离
- M7 mcp_tools_search._mirror_resolve 集成接线
"""

import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

os.environ.pop('INFOSEEK_MIRROR_MAP', None)
os.environ.pop('INFOSEEK_MIRROR_ENABLED', None)

from mirror_map import (  # noqa: E402
    enabled, load_mirror_map, resolve_url, resolve_host,
)

_fails = []


def _check(name, cond, detail=''):
    if cond:
        print(f"  [PASS] {name}")
    else:
        _fails.append(name)
        print(f"  [FAIL] {name} {detail}")


_TMP_CONFIG = None


def _temp_config(mappings: dict) -> str:
    global _TMP_CONFIG
    fd, path = tempfile.mkstemp(suffix='.yaml', prefix='mirror_')
    os.close(fd)
    body = "version: 1\nmappings:\n"
    for k, v in mappings.items():
        body += f'  {k}: "{v}"\n'
    Path(path).write_text(body, encoding='utf-8')
    _TMP_CONFIG = path
    return path


def main():
    # M1 默认空表
    print('--- M1 默认空表 ---')
    mm = load_mirror_map(force=True)
    _check('默认映射为空', len(mm) == 0, f'len={len(mm)}')
    _check('enabled 默认开', enabled() is True)

    # M2 未命中 → 原样
    print('--- M2 未命中原样 ---')
    u = 'https://example.com/path?q=1'
    _check('resolve_url 原样', resolve_url(u) == u)

    # M3 命中重写
    print('--- M3 命中重写 ---')
    os.environ['INFOSEEK_MIRROR_MAP'] = _temp_config({
        'github.com': 'gh-mirror.example.org',
        'raw.githubusercontent.com': 'raw-mirror.example.org',
    })
    load_mirror_map(force=True)
    new = resolve_url('https://github.com/GYINT/infoseek/blob/main/README.md?tab=readme')
    _check('host 已重写', 'gh-mirror.example.org/GYINT/infoseek' in new, new)
    _check('路径保留', new.endswith('/blob/main/README.md?tab=readme'), new)
    _check('协议保留', new.startswith('https://'), new)
    _check('resolve_host', resolve_host('github.com') == 'gh-mirror.example.org')
    _check('大小写不敏感', resolve_url('https://GITHUB.com/x') == 'https://gh-mirror.example.org/x')

    # M4 关闭
    print('--- M4 开关关闭 ---')
    os.environ['INFOSEEK_MIRROR_ENABLED'] = '0'
    _check('关闭后原样', resolve_url('https://github.com/x') == 'https://github.com/x')
    os.environ.pop('INFOSEEK_MIRROR_ENABLED', None)

    # M5 恢复后生效
    print('--- M5 env 覆盖（恢复） ---')
    _check('恢复后重写', resolve_url('https://github.com/x').startswith('https://gh-mirror'))

    # M6 www 剥离
    print('--- M6 www 前缀 ---')
    _check('www.github.com 命中', resolve_url('https://www.github.com/x') == 'https://gh-mirror.example.org/x')

    # M7 集成接线
    print('--- M7 mcp_tools_search._mirror_resolve ---')
    import mcp_tools_search  # noqa: F401
    from mcp_tools_search import _mirror_resolve
    _check('集成重写', _mirror_resolve('https://github.com/a/b') == 'https://gh-mirror.example.org/a/b')
    _check('集成未命中原样', _mirror_resolve('https://other.com/x') == 'https://other.com/x')

    # 清理
    os.environ.pop('INFOSEEK_MIRROR_MAP', None)
    load_mirror_map(force=True)
    print()
    if _fails:
        print(f"FAIL: {len(_fails)} 项失败 → {_fails}")
        sys.exit(1)
    print("ALL PASS (test_mirror_map) ✅")
    sys.exit(0)


if __name__ == '__main__':
    main()