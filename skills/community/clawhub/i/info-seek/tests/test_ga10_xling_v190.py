#!/usr/bin/env python3
"""test_ga10_xling_v190.py — GA10 跨语言别名桥接守护测试（v1.9.0）

覆盖（ROADMAP §8.11.1 D1 / §8.12.2 GA10）：
  B1  D1 复现：英文一手权威源 × 中文人名主题 → ≥55 🟡潜力（原 9 分 ❌噪声）
  B2  无关英文源桥接不触发（不误抬）
  B3  中文×中文零回归（env on/off 分数恒等 + xling_bridge=0）
  B4  词典实体桥接（比亚迪→BYD / 商汤科技→SenseTime）+ 常见英文词防误桥
  B5  多组命中递增（55+5=60）与封顶
  B6  env 闸 INFOSEEK_XLING_BRIDGE=off → 恒 0
  B7  _filter_relevant 英文源过双门槛 + 垃圾源仍滤除（召回侧闸门）
  B8  _expand_query ⑤ 拼音别名扩展 + 既有 RE 契约零回归 + 预算 cap
  B9  build_alias_groups 缓存防污染（外层 copy）
  B10 mock 契约守护：patch xling_bridge.bridge_score 在两消费点生效（晚绑定）
  B11 别名区分度守卫（单 token <4 字符 / 常见词拒绝 / 全大写缩写放行）
"""

import os
import sys
import tempfile
import unittest.mock as mock
from pathlib import Path

INFOSEEK = Path(__file__).parent.parent
os.environ['INFOSEEK_DATA_DIR'] = tempfile.mkdtemp()
os.environ.setdefault('INFOSEEK_PLATFORM_WEBSEARCH', 'off')
sys.path.insert(0, str(INFOSEEK / 'scripts'))
sys.path.insert(0, str(INFOSEEK / 'core'))
sys.path.insert(0, str(INFOSEEK))

import xling_bridge as xb            # noqa: E402
import person_ner as pn              # noqa: E402
import infoseek_core_v2 as c2        # noqa: E402
import infoseek_pipeline as pipe     # noqa: E402
import entities as ent_top           # noqa: E402
import core.entities as ent_pkg      # noqa: E402

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

USRC = {'url': 'https://www.ualberta.ca/engineering/alumni/linjian-xiang',
        'title': 'Linjian Xiang - RoboMaster founder | University of Alberta',
        'snippet': 'Linjian Xiang founded the RoboMaster competition while at UAlberta.'}
SUBJ = '项林坚 RoboMaster 创始人履历'

def _cleanup_persons():
    for m in (ent_top, ent_pkg):
        m.PERSON_ENTITIES[:] = [e for e in m.PERSON_ENTITIES
                                if e.get('source') != 'person_ner']
        m._ALL_ENTITIES_CACHE = None
    xb._groups_cached.cache_clear()

try:
    # ── B1 D1 复现（评分侧）──
    pn.bootstrap_subject(SUBJ)          # research 入口同款引导
    xb._groups_cached.cache_clear()
    r1 = c2.score_source(dict(USRC), SUBJ)
    check('B1 英文一手源 ≥55 脱离❌噪声', r1['base_score'] >= 55
          and r1['classification'] != '❌噪声', f"{r1['base_score']} {r1['classification']}")
    check('B1 base_origin 仍为 semantic_fallback', r1['base_origin'] == 'semantic_fallback')
    check('B1 xling_bridge 字段可观测', r1.get('xling_bridge', 0) >= 55, str(r1.get('xling_bridge')))
    check('B1 algo-v 契约不变（version=1.2.0）', r1['version'] == '1.2.0')

    # ── B2 无关英文源不误抬 ──
    r2 = c2.score_source({'url': 'https://x.com', 'title': 'Tesla quarterly delivery report',
                          'snippet': 'Tesla Q2 deliveries beat estimates'}, SUBJ)
    check('B2 无关英文源 bridge=0', r2.get('xling_bridge') == 0, str(r2.get('xling_bridge')))
    check('B2 无关英文源仍❌噪声', r2['classification'] == '❌噪声', str(r2['final_score']))

    # ── B3 中文×中文零回归（on/off 恒等）──
    zsrc = {'url': 'https://zh.com', 'title': '项林坚创办RoboMaster的历程',
            'snippet': '项林坚是RoboMaster创始人，赛事起源于校园'}
    os.environ['INFOSEEK_XLING_BRIDGE'] = 'off'
    r_off = c2.score_source(dict(zsrc), SUBJ)
    os.environ.pop('INFOSEEK_XLING_BRIDGE')
    r_on = c2.score_source(dict(zsrc), SUBJ)
    check('B3 中文源 on/off final 恒等', r_off['final_score'] == r_on['final_score'],
          f"{r_off['final_score']} vs {r_on['final_score']}")
    check('B3 中文源 bridge=0（原路径不变）', r_on.get('xling_bridge') == 0)

    # ── B4 词典实体桥接 + 常见词防误桥 ──
    check('B4 比亚迪×BYD 桥接 55', xb.bridge_score(
        'BYD sales report 2026 shows record EV delivery', '比亚迪 2026 财报') == 55)
    check('B4 apple 常见词防误桥', xb.bridge_score(
        'Apple Inc announces new iPhone', '苹果公司 新品') == 0)
    check('B4 商汤×SenseTime 词典桥接', xb.bridge_score(
        'SenseTime released a new vision model', '商汤科技 新模型') >= 55,
        str(xb.build_alias_groups('商汤科技 新模型')))

    # ── B5 多组递增 + 封顶 ──
    s5 = xb.bridge_score('Linjian Xiang met BYD executives in Shenzhen', '项林坚 比亚迪 2026')
    check('B5 双组命中 60（55+5）', s5 == 60, str(s5))
    check('B5 封顶 ≤70', xb.BRIDGE_CAP == 70 and s5 <= 70)

    # ── B6 env 闸 ──
    os.environ['INFOSEEK_XLING_BRIDGE'] = 'off'
    try:
        check('B6 off → bridge 恒 0', xb.bridge_score(
            'Linjian Xiang founded RoboMaster', '项林坚 履历') == 0)
        check('B6 off → expansion 恒空', xb.expansion_aliases('项林坚 履历') == [])
    finally:
        os.environ.pop('INFOSEEK_XLING_BRIDGE')

    # ── B7 _filter_relevant 召回侧闸门 ──
    res = [{'url': 'https://ualberta.ca/x',
            'title': 'Linjian Xiang RoboMaster founder',
            'snippet': 'University of Alberta alumni page'},
           {'url': 'https://spam.com', 'title': 'Casino bonus offers',
            'snippet': 'best poker site 2026'}]
    with mock.patch.object(pipe, '_min_expected', return_value=0):
        out = pipe._filter_relevant([dict(x) for x in res], '项林坚 履历')
    urls = [x['url'] for x in out]
    check('B7 英文一手源过双门槛', 'https://ualberta.ca/x' in urls, str(urls))
    check('B7 过闸条目带 xling_bridge 标记',
          all(x.get('xling_bridge', 0) >= 12 for x in out if 'ualberta' in x['url']))
    check('B7 垃圾源仍被滤除', 'https://spam.com' not in urls, str(urls))

    # ── B8 _expand_query ⑤ + RE 契约零回归 ──
    q1 = pipe._expand_query('项林坚 履历')
    check('B8 拼音别名进入扩展', 'xiang linjian' in q1 and q1.startswith('项林坚 履历'), q1)
    check('B8 扩展预算 cap=6 生效', len(xb.expansion_aliases('项林坚 履历', cap=6)) <= 6)
    with mock.patch('core.entities.get_all_entities',
                    return_value=[{'name': '比亚迪', 'aliases': ['BYD', 'byd'], 'category': 'ORG'}]):
        q2 = pipe._expand_query('比亚迪 2026 财报')
    # RE1 原契约（v1.2.x）：'BYD' in q 且原样前缀；实体通道自带大小写双别名（既有行为）
    # → xling 通道不得再追加第三个 byd 变体（exclude 去重守护）
    check('B8 RE1 契约（BYD 扩展 + xling 不重复追加）',
          'BYD' in q2 and q2.startswith('比亚迪 2026 财报')
          and q2.lower().count('byd') <= 2, q2)
    q3 = pipe._expand_query('量子计算 2026 趋势')
    check('B8 RE2 契约（无命中原样）', q3 == '量子计算 2026 趋势', q3)

    # ── B9 缓存防污染（外层 copy）──
    g1 = xb.build_alias_groups('项林坚 履历')
    if g1:
        g1[0]['latin'].append('POISON')
    g2 = xb.build_alias_groups('项林坚 履历')
    check('B9 mutate 返回值不污染缓存',
          all('POISON' not in g['latin'] for g in g2), str(g2))

    # ── B10 mock 契约守护（晚绑定，§8.13.3 铁律固化）──
    with mock.patch('xling_bridge.bridge_score', return_value=99):
        r10 = c2.score_source({'url': 'https://e.com', 'title': 'zzz qqq unrelated',
                               'snippet': 'nothing related at all'}, '某中文主题词')
        check('B10 score_source 侧 patch 生效', r10.get('xling_bridge') == 99
              and r10['base_score'] == 99, str(r10.get('xling_bridge')))
        with mock.patch.object(pipe, '_min_expected', return_value=0):
            out10 = pipe._filter_relevant(
                [{'url': 'https://e10', 'title': 'zzz qqq', 'snippet': ''}], '某中文主题词')
        check('B10 _filter_relevant 侧 patch 生效',
              len(out10) == 1 and out10[0].get('xling_bridge') == 99, str(out10))

    # ── B11 区分度守卫 ──
    check('B11 单token<4 拒绝', not xb._alias_distinctive('abc'))
    check('B11 全大写缩写≥2 放行', xb._alias_distinctive('byd', original='BYD'))
    check('B11 多token 放行', xb._alias_distinctive('linjian xiang'))
    check('B11 常见词拒绝', not xb._alias_distinctive('apple'))
finally:
    _cleanup_persons()

print(f"\n=== GA10 跨语言桥接守护: {len(passed)} PASS / {len(failed)} FAIL ===")
sys.exit(1 if failed else 0)
