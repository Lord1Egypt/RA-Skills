#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""test_jieba_bridge_zerodep_v230.py — 六处裸 import 收敛 + zerodep 增强守护（v2.3.0）

守护对象：
  ① 单源：jieba/pypinyin 的探测/初始化/告警仅存在于 `core/jieba_bridge.py`，
     全仓其他位置再无裸 import（防 6 处裸 import 复活）
  ② bridge 能力契约：lcut / posseg / word_freq / textrank / lazy_pinyin
     探测进程内一次 + reset 钩子 + 降级永不抛错
  ③ 双模块合一：顶层 jieba_bridge 与 core.jieba_bridge 为同一对象
  ④ mock 晚绑定契约：对 bridge 函数 patch 在消费点（text_tokenizer/person_ner）生效
  ⑤ zerodep 增强：词典锚点召回单频专业词、掩码去跨词噪声、分层合成、加权投票

独立运行：python3 tests/test_jieba_bridge_zerodep_v230.py
"""
import ast
import glob
import os
import sys
from pathlib import Path
from unittest import mock

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
for p in (os.path.join(ROOT, 'scripts'), os.path.join(ROOT, 'core'), ROOT):
    if p not in sys.path:
        sys.path.insert(0, p)
os.environ.setdefault('INFOSEEK_PLATFORM_WEBSEARCH', 'off')

PASS = FAIL = 0


def check(name, cond, detail=''):
    global PASS, FAIL
    if cond:
        PASS += 1
        print(f'  PASS {name}')
    else:
        FAIL += 1
        print(f'  FAIL {name} {detail}')


import jieba_bridge as jb                      # noqa: E402
import core.jieba_bridge as jb_pkg             # noqa: E402
import text_tokenizer as tt                    # noqa: E402
import person_ner as pn                        # noqa: E402
import infoseek_zerodep_nlp as zd              # noqa: E402


print('[A] bridge 单源与双模块合一')
# A1 全仓除 bridge 外无 jieba/pypinyin 裸 import
_BARE = re = __import__('re')
_pat = _BARE.compile(r'^\s*(?:import|from)\s+(?:jieba|pypinyin)(?:\.|\s|$)', _BARE.M)
_offenders = []
for f in glob.glob(os.path.join(ROOT, 'core', '*.py')) + \
          glob.glob(os.path.join(ROOT, 'scripts', '*.py')):
    if os.path.basename(f) == 'jieba_bridge.py':
        continue
    with open(f, encoding='utf-8', errors='replace') as fh:
        for ln in fh:
            if _pat.match(ln):
                _offenders.append(os.path.relpath(f, ROOT))
check('A1 裸 import 仅存于 bridge（六处收敛不复活）', not _offenders, str(_offenders))
check('A2 顶层 ↔ core. 双模块合一（状态不分裂）', jb is jb_pkg)
check('A3 bridge mod-v 声明', bool(jb.MOD_VERSION))

print('\n[B] bridge 能力契约（降级永不抛错）')
jb.reset()
try:
    j_lcut = jb.lcut('人工智能大模型')
    check('B1 lcut 返回 list', isinstance(j_lcut, list), str(type(j_lcut)))
    check('B2 word_freq 返回 int', isinstance(jb.word_freq('研究'), int))
    check('B3 textrank 返回 set', isinstance(jb.textrank('人工智能技术发展', 3), set))
    check('B4 lazy_pinyin 返回 list', isinstance(jb.lazy_pinyin('单雄信'), list))
    _ps = jb.posseg_cut('腾讯发布模型')
    check('B5 posseg_cut 可迭代', _ps is not None and hasattr(_ps, '__iter__'))
except Exception as e:
    check('B* bridge 能力不抛错', False, repr(e)[:80])

# B6 降级语义：模拟依赖全缺
with mock.patch.object(jb, 'get_jieba', return_value=None), \
     mock.patch.object(jb, 'get_pypinyin', return_value=None):
    check('B6 jieba缺→lcut None / word_freq 0 / textrank 空',
          jb.lcut('x') is None and jb.word_freq('x') == 0 and jb.textrank('x', 3) == set())
    check('B7 pypinyin缺→lazy_pinyin None', jb.lazy_pinyin('x') is None)

# B8 reset 后可重新探测
jb.reset()
check('B8 reset 钩子恢复探测', jb.get_jieba() is not None and jb.get_pypinyin() is not None)

print('\n[C] 收敛后消费点契约保持（委托 bridge）')
check('C1 text_tokenizer tokenize 正常',
      isinstance(tt.tokenize_text('人工智能大模型'), set))
check('C2 person_ner 词频守卫工作',
      pn._freq_common('研究') in (True, False))
# mock 晚绑定：patch bridge.word_freq 在 person_ner 消费点生效
with mock.patch.object(jb, 'word_freq', return_value=99999):
    check('C3 patch bridge.word_freq 对 person_ner 生效', pn._freq_common('任意词') is True)
# patch bridge.lcut 在 text_tokenizer 消费点生效
with mock.patch.object(jb, 'lcut', return_value=['甲词', '乙词']):
    check('C4 patch bridge.lcut 对 tokenizer 生效',
          tt.tokenize_text('随便') == {'甲词', '乙词'}, str(tt.tokenize_text('随便')))
# 消费方无 from-import bridge 函数（晚绑定 AST 契约）
def _from_bridge(paths):
    bad = []
    for f in paths:
        tree = ast.parse(Path(f).read_text(encoding='utf-8'))
        for n in ast.walk(tree):
            if isinstance(n, ast.ImportFrom) and n.module in ('jieba_bridge', 'core.jieba_bridge'):
                bad.append(os.path.basename(f))
    return bad
_no_from = _from_bridge([
    os.path.join(ROOT, 'scripts', 'text_tokenizer.py'),
    os.path.join(ROOT, 'core', 'person_ner.py'),
])
check('C5 消费方无 from-import bridge（模块对象晚绑定）', not _no_from, str(_no_from))

print('\n[D] zerodep 增强（锚点 + 掩码 + 分层合成）')
with mock.patch.object(zd, '_optional_jieba', return_value=set()), \
     mock.patch.object(zd, '_optional_summa', return_value=set()):
    # D1 词表输入：单频专业词锚点召回
    k1, e1 = zd.extract_keywords_detailed(
        '人工智能 大模型 自然语言处理 量化交易', max_kw=6)
    _s1 = {w for w, _ in k1}
    check('D1 单频专业词锚点召回', e1 == 'zerodep'
          and {'人工智能', '大模型', '自然语言处理', '量化交易'} <= _s1, str(k1))
    # D2 连续文本：无跨词噪声（"智能大模"类）
    t2 = ('人工智能大模型技术正在快速迭代。大模型在自然语言处理任务上表现突出。'
          '多家科技公司发布自研大模型产品。')
    k2, _ = zd.extract_keywords_detailed(t2, max_kw=8)
    _noise = [w for w, _ in k2 if ('大模' in w and w != '大模型')
              or ('任务上表' in w) or ('正在快速' in w)]
    check('D2 掩码消除跨词噪声', not _noise, str(k2))
    check('D3 连续文本锚点词仍保留',
          {'人工智能', '大模型'} <= {w for w, _ in k2}, str(k2))
    # D4 置信分在合理量纲 (0,3]
    check('D4 置信分 ∈ (0,3]', all(0 < s <= 3 for _, s in k2), str(k2))

# D5 词典估计器直接验
check('D5 中文词典匹配',
      {'量化交易', '风险管理'} <= zd._est_zh_dictionary('量化交易与风险管理', 10))
check('D6 掩码切碎锚点（命中词替换为全角空格）',
      '人工智能' not in zd._mask_zh_anchors('人工智能大模型')
      and '大模型' not in zd._mask_zh_anchors('人工智能大模型')
      and zd._mask_zh_anchors('人工智能') == '　　　　'
      and '技术' in zd._mask_zh_anchors('人工智能技术'))

print('\n[E] 加权共识投票')
sets3 = [{'人工智能', '大模型'}, {'人工智能', '量化'}, {'人工智能', '大模型'}]
cons, sc = zd.weighted_consensus(sets3, weights=[1.0, 1.0, 1.0])
check('E1 加权投票 3 估计器 ≥2 通过', '人工智能' in cons and '大模型' in cons
      and '量化' not in cons, str((sorted(cons), dict(sc))))
cons2, _ = zd.weighted_consensus([{'a', 'b'}, {'a', 'c'}])
check('E2 2 估计器阈值自适应（须两侧互证）', cons2 == {'a'}, str(sorted(cons2)))
check('E3 空输入安全', zd.weighted_consensus([]) == (set(), __import__('collections').Counter()))
# 旧等票接口仍可用（向后兼容）
check('E4 redundant_consensus 兼容',
      'a' in zd.redundant_consensus([{'a', 'b'}, {'a', 'c'}], min_votes=2))

print(f'\n=== test_jieba_bridge_zerodep_v230: {PASS} PASS / {FAIL} FAIL ===')
sys.exit(1 if FAIL else 0)
