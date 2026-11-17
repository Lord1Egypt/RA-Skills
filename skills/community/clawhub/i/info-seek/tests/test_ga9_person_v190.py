#!/usr/bin/env python3
"""test_ga9_person_v190.py — GA9 人名消歧五步守护测试（v1.9.0）

覆盖（ROADMAP §8.11.3 五步 + §8.13.3 铁律固化）：
  A1  数据真源 schema/规模
  A2  ① 多音字姓氏白名单 preferred 读音（单/查/区 实锤三例，§8.11.2）
  A3  ② 复姓整词长匹配（欧阳/司马/爱新觉罗，禁止逐字拆）
  A4  检测守卫（地名/虚词/常用词/叠字 blocklist）
  A5  subject 模式（2 字名 + 负样本 + token 完整消费）
  A6  ④ 注册 → NER 双路径可见（D2 闭合：中文 name 命中 + 拉丁 alias 命中）
  A7  注册幂等 + teardown 恢复
  A8  pypinyin 缺失优雅降级
  A9  数据文件缺失 → L3 应急最小集
  A10 ③ heteronym 全枚举（生成端不硬判）
  A11 导入纪律 AST 守护（_anchor_mod/_person_mod/_xling_mod 禁 from-import，
      用户指令 2026-09-14：勿把 _anchor_mod 改回 from-import → 固化为测试）
"""

import ast
import os
import sys
import tempfile
from pathlib import Path
from unittest import mock

INFOSEEK = Path(__file__).parent.parent
os.environ['INFOSEEK_DATA_DIR'] = tempfile.mkdtemp()
os.environ.setdefault('INFOSEEK_PLATFORM_WEBSEARCH', 'off')
sys.path.insert(0, str(INFOSEEK / 'scripts'))
sys.path.insert(0, str(INFOSEEK / 'core'))
sys.path.insert(0, str(INFOSEEK))

import person_ner as pn  # noqa: E402

# ── 可选依赖 preflight（沙箱环境重置会卸载 pip 包）─────────────────────
# pypinyin→拼音别名/GA10 桥接；jieba→常用词守卫。二者缺失时本套件核心断言无法执行，
# 显式整体 SKIP（rc=0 + pass==0 → runner 归类 SKIP），避免误报 FAIL 污染绿基线。
_MISSING = []
for _dep in ('pypinyin', 'jieba'):
    try:
        __import__(_dep)
    except Exception:
        _MISSING.append(_dep)
if _MISSING:
    print(f"⚠️ 可选依赖缺失：{', '.join(_MISSING)} —— 本套件核心断言（拼音别名/词频守卫）"
          f"无法执行，整体跳过；装齐后自动启用：pip install {' '.join(_MISSING)}")
    print('0 PASS / 0 FAIL / %d SKIP' % (len(_MISSING),))
    sys.exit(0)

passed, failed = [], []
def check(name, cond, detail=''):
    (passed if cond else failed).append(name)
    print(f"[{'PASS' if cond else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))


# ── A1 数据真源 ──
d = pn.load_surname_data(force=True)
need_keys = {'compound_surnames', 'single_surnames', 'polyphonic_surnames',
             'blocklist_words', 'blocklist_geo', 'geo_suffix_chars', 'stop_given_chars'}
check('A1 schema 七键齐全', need_keys <= set(d.keys()), str(sorted(d.keys())))
check('A1 数据规模下限', len(d['single_surnames']) >= 150
      and len(d['compound_surnames']) >= 50 and len(d['polyphonic_surnames']) >= 20
      and len(d['blocklist_words']) >= 300,
      f"singles={len(d['single_surnames'])} compounds={len(d['compound_surnames'])}")
check('A1 多音字姓均在单姓表', all(s in d['single_surnames']
                                 for s in d['polyphonic_surnames']))
check('A1 历史人名未入 blocklist（防阻断人物调研）',
      not any(x in d['blocklist_words'] for x in ('陆游', '孙权', '聂耳', '晁错')))

# ── A2 ① 多音字白名单 preferred（§8.11.2 实锤三例）──
for name, want in (('单雄信', 'shan'), ('查良镛', 'zha'), ('区楚良', 'ou')):
    a = pn.person_pinyin_aliases(name)
    check(f'A2 {name} preferred={want}', bool(a) and a[0].startswith(want), str(a[:2]))
    het = {'单雄信': 'dan', '查良镛': 'cha', '区楚良': 'qu'}[name]
    check(f'A2 {name} heteronym 候选保留({het})', any(x.startswith(het) for x in a), str(a))

# ── A3 ② 复姓整词长匹配 ──
r = {p['name']: p['surname'] for p in pn.detect_person_names(
    '欧阳娜娜和司马光都研究爱新觉罗溥仪', mode='text')}
check('A3 欧阳娜娜→复姓欧阳', r.get('欧阳娜娜') == '欧阳', str(r))
check('A3 司马光→复姓司马', r.get('司马光') == '司马', str(r))
check('A3 爱新觉罗溥仪→4字复姓', r.get('爱新觉罗溥仪') == '爱新觉罗', str(r))
check('A3 复姓未逐字拆（无 欧/司 单姓误报）',
      not any(s in ('欧', '司') for s in r.values()), str(r))

# ── A4 检测守卫（text 模式）──
NEG = '随后考察王府井、石家庄、张家口、张家港、马鞍山，讨论关系人责任与发展方向感，张管理都研究过此题。'
neg_hits = [p['name'] for p in pn.detect_person_names(NEG, mode='text')]
check('A4 地名/虚词/常用词零误报', neg_hits == [], str(neg_hits))
POS = '项林坚与谢博文均出席，单雄信后代与王建国、李志明、刘泽天同场。'
pos_hits = {p['name'] for p in pn.detect_person_names(POS, mode='text')}
check('A4 真名全检出', {'项林坚', '谢博文', '单雄信', '王建国', '李志明', '刘泽天'} <= pos_hits,
      str(pos_hits))
check('A4 text 模式不检 2 字名（精度优先）',
      all(len(n) >= 3 for n in pos_hits), str(pos_hits))

# ── A5 subject 模式 ──
s1 = [p['name'] for p in pn.detect_person_names('马云 创业史', mode='subject')]
check('A5 subject 2字名可检', s1 == ['马云'], str(s1))
s2 = [p['name'] for p in pn.detect_person_names('马上就到 方向感 关系人 数据库管理', mode='subject')]
check('A5 subject 负样本零误报', s2 == [], str(s2))
s3 = [p['name'] for p in pn.detect_person_names('项林坚 RoboMaster 创始人履历', mode='subject')]
check('A5 subject 人名+混排', s3 == ['项林坚'], str(s3))
check('A5 token 须完整消费（石家庄旅游不检）',
      pn.detect_person_names('石家庄旅游', mode='subject') == [])

# ── A6/A7 ④ 注册 → NER 双路径可见（D2 闭合）+ 幂等 ──
import entities as ent_top            # noqa: E402
import core.entities as ent_pkg      # noqa: E402
from core.ner import extract_entities as ex_pkg   # noqa: E402
from ner import extract_entities as ex_top        # noqa: E402

_snapshot = (len(ent_top.PERSON_ENTITIES), len(ent_pkg.PERSON_ENTITIES))
try:
    reg = pn.bootstrap_subject('项林坚 RoboMaster 创始人履历')
    check('A6 bootstrap 返回注册体', len(reg) == 1 and reg[0]['name'] == '项林坚'
          and 'xiang linjian' in reg[0]['aliases'], str(reg))
    zh_pkg = [e['entity_name'] for e in ex_pkg('项林坚创办了RoboMaster赛事')]
    zh_top = [e['entity_name'] for e in ex_top('项林坚创办了RoboMaster赛事')]
    en_pkg = [e['entity_name'] for e in ex_pkg('Linjian Xiang founded RoboMaster at UAlberta')]
    check('A6 中文源 NER 命中（包路径）', '项林坚' in zh_pkg, str(zh_pkg))
    check('A6 中文源 NER 命中（顶层路径，双模块一致）', '项林坚' in zh_top, str(zh_top))
    check('A6 英文源经拉丁别名命中（D2 闭合实锤）', '项林坚' in en_pkg, str(en_pkg))
    hit = [e for e in ex_pkg('Linjian Xiang founded RoboMaster')]
    check('A6 英文命中 match_method=alias',
          hit and hit[0].get('match_method') == 'alias', str(hit[:1]))
    n_before = len(ent_top.PERSON_ENTITIES)
    pn.bootstrap_subject('项林坚 RoboMaster 创始人履历')
    check('A7 重复 bootstrap 幂等', len(ent_top.PERSON_ENTITIES) == n_before)
finally:
    for m in (ent_top, ent_pkg):
        m.PERSON_ENTITIES[:] = [e for e in m.PERSON_ENTITIES
                                if e.get('source') != 'person_ner']
        m._ALL_ENTITIES_CACHE = None
    check('A7 teardown 恢复 PERSON 列表',
          (len(ent_top.PERSON_ENTITIES), len(ent_pkg.PERSON_ENTITIES)) == _snapshot,
          f'{_snapshot} → ({len(ent_top.PERSON_ENTITIES)},{len(ent_pkg.PERSON_ENTITIES)})')

# ── A8 pypinyin 缺失降级 ──
# 2026-09-29：探测收口到 jieba_bridge，原 pn._PYPINYIN/_PYPINYIN_PROBED
# 私有状态删除 → mock bridge.get_pypinyin 返回 None 模拟缺失。
try:
    with mock.patch.object(pn._jb, 'get_pypinyin', return_value=None):
        check('A8 无 pypinyin 别名降级为空（不抛错）', pn.person_pinyin_aliases('项林坚') == [])
        check('A8 无 pypinyin 白名单姓读音仍可用', pn.surname_readings('单')[0] == ['shan'])
        check('A8 无 pypinyin 检测仍工作',
              [p['name'] for p in pn.detect_person_names('项林坚出席', mode='text')] == ['项林坚'])
finally:
    pass

# ── A9 数据文件缺失 → L3 应急最小集 ──
_ref, _warned = pn._REF_PATH, pn._DATA_WARNED
try:
    pn._REF_PATH = Path('/nonexistent/person-surnames.json')
    pn._DATA_WARNED = False
    fb = pn.load_surname_data(force=True)
    check('A9 缺失→L3 fallback', fb.get('version') == '0-fallback')
    check('A9 fallback 下检测仍工作（谢在最小集）',
          [p['name'] for p in pn.detect_person_names('谢博文出席', mode='text')] == ['谢博文'])
finally:
    pn._REF_PATH, pn._DATA_WARNED = _ref, _warned
    pn.load_surname_data(force=True)

# ── A10 ③ heteronym 全枚举（生成端不硬判，交门控收敛）──
a = pn.person_pinyin_aliases('单雄信')
check('A10 preferred+heteronym 并存（shan 与 dan 均在）',
      any(x.startswith('shan') for x in a) and any(x.startswith('dan') for x in a), str(a))
check('A10 别名上限 6', len(a) <= 6, str(len(a)))
check('A10 名部分连写符合英文惯例（linjian 整词）',
      'xiang linjian' in pn.person_pinyin_aliases('项林坚'))

# ── A11 导入纪律 AST 守护（用户指令固化：勿改回 from-import）──
def _from_imports(path, modules):
    tree = ast.parse(Path(path).read_text(encoding='utf-8'))
    return [n for n in ast.walk(tree)
            if isinstance(n, ast.ImportFrom) and n.module in modules]

pipe_src = (INFOSEEK / 'scripts' / 'infoseek_pipeline.py').read_text(encoding='utf-8')
core_src = (INFOSEEK / 'scripts' / 'infoseek_core_v2.py').read_text(encoding='utf-8')
check('A11 pipeline 保持 import anchor_adapter as _anchor_mod',
      'import anchor_adapter as _anchor_mod' in pipe_src)
# 契约符号禁 from-import（§8.13.3：mock/monkey-patch 晚绑定契约的两个函数）。
# 注：`from anchor_adapter import infos_to_seek` 为 v1.2.0 既有合法导入（无 mock 契约），不在守卫范围。
_CONTRACT_SYMS = {'compute_semantic_similarity', '_string_containment_similarity'}
_aa_fi = [al.name for n in _from_imports(
    INFOSEEK / 'scripts' / 'infoseek_pipeline.py', {'anchor_adapter'}) for al in n.names]
check('A11 pipeline 契约符号无 from-import（§8.13.3 铁律）',
      not (_CONTRACT_SYMS & set(_aa_fi)), str(_aa_fi))
check('A11 双脚本无 from xling_bridge/person_ner import（模块对象纪律）',
      not _from_imports(INFOSEEK / 'scripts' / 'infoseek_pipeline.py',
                        {'xling_bridge', 'person_ner'})
      and not _from_imports(INFOSEEK / 'scripts' / 'infoseek_core_v2.py',
                            {'xling_bridge', 'person_ner'}))
check('A11 core_v2 保持模块对象导入',
      'import person_ner as _person_mod' in core_src
      and 'import xling_bridge as _xling_mod' in core_src)

print(f"\n=== GA9 人名消歧守护: {len(passed)} PASS / {len(failed)} FAIL ===")
sys.exit(1 if failed else 0)
