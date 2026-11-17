#!/usr/bin/env python3
"""test_version_single_source.py — 版本单源一致性守护（v1.8.1 治理）

防止全仓版本编号再次脱节（v1.7.8 审计 P0：6 套版本体系并存）。
纯静态 + 轻量 import，无网络、无副作用。
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(ROOT, 'scripts')
sys.path.insert(0, SCRIPTS)

PASS, FAIL = 0, 0


def check(name, cond, detail=''):
    global PASS, FAIL
    if cond:
        PASS += 1
        print(f'  [PASS] {name}')
    else:
        FAIL += 1
        print(f'  [FAIL] {name} {detail}')


def read(rel):
    with open(os.path.join(ROOT, rel), encoding='utf-8', newline='') as f:
        return f.read()


# ── V1 真源存在且格式合法 ──
import mcp_tools_common as mtc  # noqa: E402

V = getattr(mtc, 'SKILL_VERSION', None)
check('V1 SKILL_VERSION 真源存在', V is not None)
check('V2 SKILL_VERSION 格式 x.y.z', bool(re.fullmatch(r'\d+\.\d+\.\d+', V or '')), f'got {V!r}')

# ── V3 SERVER_VERSION 引用真源（同值） ──
check('V3 SERVER_VERSION == SKILL_VERSION', mtc.SERVER_VERSION == V,
      f'{mtc.SERVER_VERSION!r} != {V!r}')

# ── V4 真源在 mcp_tools_common 中以字面量定义（非从别处 import） ──
common_src = read('scripts/mcp_tools_common.py')
check('V4 真源为字面量定义', f'SKILL_VERSION = "{V}"' in common_src)
check('V5 SERVER_VERSION 为引用而非硬编码',
      'SERVER_VERSION = SKILL_VERSION' in common_src)

# ── V6 SKILL.md frontmatter ──
skill_md = read('SKILL.md')
m = re.search(r'^version:\s*(\S+)\s*$', skill_md, re.M)
check('V6 SKILL.md version 一致', bool(m) and m.group(1) == V,
      f'got {m.group(1) if m else None!r}')

# ── V7 manifest.yaml ──
mani = read('manifest.yaml')
m2 = re.search(r'^version:\s*(\S+)\s*$', mani, re.M)
check('V7 manifest.yaml version 一致', bool(m2) and m2.group(1) == V,
      f'got {m2.group(1) if m2 else None!r}')

# ── V8 CHANGELOG 顶部条目 ──
cl = read('CHANGELOG.md')
m3 = re.search(r'^## \[(\d+\.\d+\.\d+)\]', cl, re.M)
check('V8 CHANGELOG 顶部条目 == SKILL_VERSION', bool(m3) and m3.group(1) == V,
      f'got {m3.group(1) if m3 else None!r}')

# ── V9 core/__init__.__version__ ──
core_init = read('core/__init__.py')
m4 = re.search(r'^__version__\s*=\s*"(\d+\.\d+\.\d+)"', core_init, re.M)
check('V9 core.__version__ 一致', bool(m4) and m4.group(1) == V,
      f'got {m4.group(1) if m4 else None!r}')

# ── V10 archive_server 无本地版本覆盖 ──
arch = read('scripts/infoseek_archive_server.py')
check('V10 archive_server 无 SERVER_VERSION 本地覆盖',
      not re.search(r'^SERVER_VERSION\s*=\s*["\']', arch, re.M))
check('V11 archive_server 无 v1.6.0 硬编码描述', 'v1.6.0 (写操作)' not in arch)
check('V12 archive_server description 动态引用', 'v{SERVER_VERSION}' in arch)

# ── V13 mcp_server 应答用变量而非字面量 ──
mcp_srv = read('scripts/infoseek_mcp_server.py')
check('V13 mcp_server serverInfo 用 SERVER_VERSION 变量',
      '"version": SERVER_VERSION' in mcp_srv)
check('V14 mcp_server 无版本字面量硬编码',
      not re.search(r'^SERVER_VERSION\s*=\s*["\']', mcp_srv, re.M))

# ── V15 RELEASE_NOTES 首个版本标题 ──
rn = read('RELEASE_NOTES.md')
m5 = re.search(r'^# Infoseek v(\d+\.\d+\.\d+) 发布说明', rn, re.M)
check('V15 RELEASE_NOTES 首标题 == SKILL_VERSION', bool(m5) and m5.group(1) == V,
      f'got {m5.group(1) if m5 else None!r}')

# ── V16 四维度语义声明存在（防再次混读为"倒挂"） ──
check('V16 真源处四维度声明', 'mod-v' in common_src and 'algo-v' in common_src
      and 'proto-v' in common_src)
check('V17 domain_router mod-v 声明', 'mod-v1.8.1' in read('scripts/domain_router.py'))
check('V18 anchor_adapter mod-v 声明', 'mod-v2.0.2' in read('scripts/anchor_adapter.py'))
check('V19 anchor_score_v2 mod-v 声明', 'mod-v2.0.2' in read('core/anchor_score_v2.py'))
check('V20 core_v2 algo-v 声明', 'algo-v' in read('scripts/infoseek_core_v2.py'))

# ── V21 algo-v 契约稳定性：core_v2 返回体版本未被误改为 skill 版本 ──
cv2 = read('scripts/infoseek_core_v2.py')
check('V21 algo-v 结果体版本保持 1.2.0（未被误改）', "'version': '1.2.0'" in cv2)
check('V22 algo-v 与 skill 版本不同值（维度确已分离）',
      "'version': '1.2.0'" in cv2 and V != '1.2.0')

print(f'\n结果: {PASS} PASS / {FAIL} FAIL')
sys.exit(1 if FAIL else 0)
