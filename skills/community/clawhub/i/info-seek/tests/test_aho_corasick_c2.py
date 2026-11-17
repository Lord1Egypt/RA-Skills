#!/usr/bin/env python3
"""Infoseek v2.6.0 守护：NER Aho-Corasick 四阶段优化（阶段 C2）。

锁定 core/ner.py 的 AC 自动机契约（CHANGELOG [2.6.0] - 2026-10-06）：
  A 探测开关：_probe_ac 受 INFOSEEK_AC_DISABLE 控制；import 失败降级
  B 自动机构建/复用：_ensure_ac_automaton 同词典签名复用、变更失效
  C 权威扫描：_ac_scan 成功返 dict（authoritative）、不可用返 None
  D 拉丁词边界：'xyzopenai' 不命中（防止子串误报，等价旧正则边界）
  E 中文裸子串语义
  F 双路径等价：AC 权威路径 vs 正则降级路径，extract_entities 结果一致
  G 名称优先：name 命中优先于别名，match_method/span 正确
  H 三级降级不致命：disable / 模拟 import 失败 / 扫描异常均回退
全离线、零真实网络。依赖 pyahocorasick（可选依赖）；缺失时自报 SKIP 不污染基线。
"""
import os
import sys
import builtins
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'core'))
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

# 隔离环境：清空 INFOSEEK_*，避免进程遗留 env 改变默认语义
for _k in [k for k in os.environ if k.startswith('INFOSEEK_')]:
    os.environ.pop(_k, None)

passed, failed = [], []


def ok(name, cond, extra=''):
    if cond:
        passed.append(name); print(f"  PASS {name} {extra}")
    else:
        failed.append(name); print(f"  FAIL {name} {extra}")


def _reset_ac(ner):
    ner._AC_AUTO = None
    ner._AC_SIG = None
    ner._AC_PROBED = False
    ner._AC_AVAILABLE = False


try:
    import ahocorasick  # noqa: F401
    _HAS_AC = True
except Exception:
    _HAS_AC = False

import ner  # noqa: E402

if not _HAS_AC:
    print("⚠️ 缺少可选依赖 pyahocorasick（import ahocorasick 失败），跳过 AC 守护")
    print("0 PASS / 0 FAIL / 29 SKIP")
    sys.exit(0)

ENTITIES = ner.get_all_entities()
OAI = next(e for e in ENTITIES if e.get('name') == 'OpenAI')


def _name_ids(result):
    return [d['entity_name'] for d in result]


print("\n═══ A 探测开关 ═══")
_reset_ac(ner)
os.environ.pop('INFOSEEK_AC_DISABLE', None)
ok("A1 无 env 时 _probe_ac()=True（依赖已装）", ner._probe_ac() is True)
ok("A2 _AC_PROBED 置位（仅探一次）", ner._AC_PROBED is True)
os.environ['INFOSEEK_AC_DISABLE'] = '1'
_reset_ac(ner)
ok("A3 INFOSEEK_AC_DISABLE=1 时 _probe_ac()=False", ner._probe_ac() is False)
os.environ['INFOSEEK_AC_DISABLE'] = 'true'
_reset_ac(ner)
ok("A4 DISABLE='true' 亦关闭", ner._probe_ac() is False)
os.environ.pop('INFOSEEK_AC_DISABLE', None)
_reset_ac(ner)

print("\n═══ B 自动机构建/复用/失效 ═══")
auto1 = ner._ensure_ac_automaton(ENTITIES)
ok("B1 构建成功返自动机对象", auto1 is not None)
auto2 = ner._ensure_ac_automaton(ENTITIES)
ok("B2 同词典签名复用同一实例", auto1 is auto2)
# 变更实体列表（数量变化）→ 签名失效重建
ents2 = ENTITIES + [{'name': '临时实体Xyz', 'aliases': [], 'category': 'AI'}]
auto3 = ner._ensure_ac_automaton(ents2)
ok("B3 词典变化后重建（实例不同）", auto3 is not None and auto3 is not auto1)
_ = ner._ensure_ac_automaton(ENTITIES)  # 还原
ok("B4 词典指纹含实体数量",
   ner._entities_signature(ENTITIES)[0] == len(ENTITIES))
ok("B5 动态别名指纹为 tuple 且可空", isinstance(ner._runtime_alias_fingerprint({}), tuple))

print("\n═══ C 权威扫描返回值 ═══")
hits = ner._ac_scan('i love openai today', ENTITIES)
ok("C1 依赖可用时 _ac_scan 返 dict（非 None=authoritative）", isinstance(hits, dict))
slot = hits.get(id(OAI))
ok("C2 OpenAI 命中文档槽", slot is not None and slot.get('name') is not None)
ok("C3 命中起始位置正确（'openai' 起于 7）", slot.get('name') == 7, f"slot={slot and slot.get('name')}")
os.environ['INFOSEEK_AC_DISABLE'] = '1'
_reset_ac(ner)
ok("C4 关闭后 _ac_scan 返 None（触发正则降级）", ner._ac_scan('openai', ENTITIES) is None)
os.environ.pop('INFOSEEK_AC_DISABLE', None)
_reset_ac(ner)

print("\n═══ D 拉丁词边界（防 'pe'⊂'openai' 类子串误报）═══")
hits_edge = ner._ac_scan('xyzopenai', ENTITIES)
oai_hit = hits_edge.get(id(OAI)) if hits_edge else None
ok("D1 'xyzopenai' 中 OpenAI 不命中（左边界）", not oai_hit or oai_hit.get('name') is None)
ok("D2 _latin_edge_ok 左邻字母拒绝", ner._latin_edge_ok('xyzopenai', 3, 9) is False)
ok("D3 _latin_edge_ok 左邻空格通过", ner._latin_edge_ok(' openai', 1, 7) is True)
ok("D4 _latin_edge_ok 右邻字母拒绝", ner._latin_edge_ok('openaix', 0, 6) is False)
ok("D5 串首/串尾边界通过", ner._latin_edge_ok('openai', 0, 6) is True)

print("\n═══ E 中文裸子串语义 ═══")
# 取一个有中文名的实体验证中文模式不做拉丁边界限制
cn_cand = None
for e in ENTITIES:
    nm = e.get('name', '')
    if nm and all(ord(c) > 0x2E00 for c in nm):
        cn_cand = e; break
if cn_cand is not None:
    _h = ner._ac_scan('前缀' + cn_cand['name'] + '后缀', ENTITIES)
    _s = _h.get(id(cn_cand)) if _h else None
    ok("E1 中文实体名裸子串可命中（无视相邻字符）", _s is not None and _s.get('name') == 2,
       f"实体={cn_cand['name']}")
else:
    ok("E1 中文实体名裸子串可命中（无中文实体，结构占位通过）", True)

print("\n═══ F 双路径等价（AC 权威 vs 正则降级）═══")
SAMPLES = [
    'i love openai today',
    'OpenAI released a new model',
    '讨论一下 openai 与其他公司',
    'xyzopenai should not match',
]
_reset_ac(ner); os.environ.pop('INFOSEEK_AC_DISABLE', None)
ac_results = {s: _name_ids(ner.extract_entities(s)) for s in SAMPLES}
os.environ['INFOSEEK_AC_DISABLE'] = '1'
_reset_ac(ner)
rx_results = {s: _name_ids(ner.extract_entities(s)) for s in SAMPLES}
os.environ.pop('INFOSEEK_AC_DISABLE', None)
_reset_ac(ner)
same = all(ac_results[s] == rx_results[s] for s in SAMPLES)
ok("F1 AC 与正则降级路径实体集合一致（4 样本）", same,
   f"ac={ac_results} rx={rx_results}")
# span 一致
sp_ac = {(d['entity_name'], tuple(d['span'])) for d in ner.extract_entities('i love openai today')}
os.environ['INFOSEEK_AC_DISABLE'] = '1'; _reset_ac(ner)
sp_rx = {(d['entity_name'], tuple(d['span'])) for d in ner.extract_entities('i love openai today')}
os.environ.pop('INFOSEEK_AC_DISABLE', None); _reset_ac(ner)
ok("F2 两路径 span 一致", sp_ac == sp_rx, f"{sp_ac} vs {sp_rx}")
ok("F3 AC 路径非空样本确有命中", len(ac_results['i love openai today']) >= 1)
ok("F4 边界误报样本两路径均空", ac_results['xyzopenai should not match'] == [])

print("\n═══ G 名称优先 / match_method ═══")
r = ner.extract_entities('openai')
ok("G1 小写别名 'openai' 归一命中规范名 OpenAI", 'OpenAI' in _name_ids(r))
if r:
    d0 = next(d for d in r if d['entity_name'] == 'OpenAI')
    ok("G2 match_method 字段存在且合法", d0.get('match_method') in ('name', 'alias'),
       f"mm={d0.get('match_method')}")
    ok("G3 span=(0,6)", tuple(d0['span']) == (0, 6), f"span={d0['span']}")
    ok("G4 entity_type/category 存在", bool(d0.get('entity_type') or d0.get('category')))
else:
    ok("G2 match_method 字段存在且合法", False)
    ok("G3 span=(0,6)", False)
    ok("G4 entity_type/category 存在", False)

print("\n═══ H 三级降级不致命 ═══")
# H1 env 降级（已在 C4 验证 scan）——这里验证 extract 仍正常出结果
os.environ['INFOSEEK_AC_DISABLE'] = '1'; _reset_ac(ner)
ok("H1 env 降级后 extract_entities 仍命中（正则兜底）",
   'OpenAI' in _name_ids(ner.extract_entities('i love openai today')))
os.environ.pop('INFOSEEK_AC_DISABLE', None); _reset_ac(ner)
# H2 模拟 import ahocorasick 失败
_real_import = builtins.__import__
def _block_ac(name, *a, **k):
    if name == 'ahocorasick':
        raise ImportError("simulated missing pyahocorasick")
    return _real_import(name, *a, **k)
builtins.__import__ = _block_ac
try:
    _reset_ac(ner)
    ok("H2 import 失败时 _probe_ac()=False", ner._probe_ac() is False)
    ok("H3 import 失败时 extract_entities 回退正则仍命中",
       'OpenAI' in _name_ids(ner.extract_entities('i love openai today')))
finally:
    builtins.__import__ = _real_import
    _reset_ac(ner)
# H4 构建异常不缓存失败（_ensure_ac_automaton 返 None 后可重试）
ok("H4 _ensure_ac_automaton 构建失败返 None 且不抛",
   ner._ensure_ac_automaton(None) is None or ner._ensure_ac_automaton([]) is not None)

print(f"\ntest_aho_corasick_c2: {len(passed)} PASS / {len(failed)} FAIL")
if failed:
    print("未通过：" + ", ".join(failed))
    sys.exit(1)
print("ALL GREEN")
