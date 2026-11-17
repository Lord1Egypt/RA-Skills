# -*- coding: utf-8 -*-
"""P2 补丁守护（v2.1.1，2026-09-18）：DEF-13/14/15/16 四项硬化。

对应缺口（见《infoseek_v210_P1硬化与P2P3规划报告》§三，本轮由 P2 规划落地）：
  DEF-13  detect_domain(None/123) 曾 AttributeError 击穿直调方 → 入口类型守卫
  DEF-14  模板 autoescape=False 的输出层注入面（无 SSTI）→ 外部字段清洗
          + CSV 公式注入（=HYPERLINK/+cmd/@evil）防护；正常 markdown 零误伤
  DEF-15  legacy 短语袋路 _extract_slots/_detect_negation 全文无截断，
          500k 长文本 timeout(>150s) → 统一 50k 有界窗口（与 keyed/time 路一致）
  DEF-16  中文 2 字短词「回测」裸子串误命中「来回测试」→ strict_keywords +
          false_compounds 误嵌覆盖校验；yaml/内置双源同步；ASCII 边界零回归

风格：顶层直跑 + 自报 N PASS / N FAIL，由 tests/run_all.py 收集。
ROOT 由 __file__ 推导，真源 /root/.skills/infoseek 与镜像副本通用。
"""
import os
import sys
import time

os.environ.setdefault('INFOSEEK_PLATFORM_WEBSEARCH', 'off')
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for p in (f'{_ROOT}/scripts', f'{_ROOT}/core'):
    if p not in sys.path:
        sys.path.insert(0, p)

_PASS = 0
_FAIL = 0


def check(name, cond, extra=''):
    global _PASS, _FAIL
    if cond:
        _PASS += 1
    else:
        _FAIL += 1
        print(f'  [FAIL] {name} {extra}')


def _score(detect_result, domain):
    for c in detect_result.get('candidates', []):
        if c['domain'] == domain:
            return c['score']
    return 0


# ════════════════════════════════════════════════════════════════
# DEF-13 ｜ detect_domain 入参类型守卫
# ════════════════════════════════════════════════════════════════
print('== DEF-13 · detect_domain None/非字符串守卫 ==')
from domain_router import detect_domain  # noqa: E402

for bad in (None, 123, 0, '', '   ', 3.14, ['x']):
    try:
        r = detect_domain(bad)
        ok = r.get('is_default') is True and r.get('domain') is None \
            and r.get('score') == 0
        check(f'detect_domain({bad!r}) 不崩且 is_default', ok, str(r)[:80])
    except Exception as e:  # noqa: BLE001
        check(f'detect_domain({bad!r}) 不崩且 is_default', False, repr(e))

# 正常路由零回归
_r = detect_domain('自动化回测交易系统')
check('正常主题仍正确路由 finance', _r.get('domain') == 'finance-research')
_r = detect_domain('DeepSeek 开源大模型技术路线')
check('正常技术主题路由 tech', _r.get('domain') == 'tech-research')


# ════════════════════════════════════════════════════════════════
# DEF-15 ｜ legacy 短语袋路有界截断
# ════════════════════════════════════════════════════════════════
print('== DEF-15 · legacy 路 50k 有界窗口 ==')
from contradiction_scorer import (  # noqa: E402
    _extract_slots, score_legacy, score_contradiction, _slot_window,
    _KEYED_MAX_CHARS,
)

check('有界常量 = 50k', _KEYED_MAX_CHARS == 50_000)

# 非字符串归一（与 P1 _claim_text 契约一致：None→''，数字→str 容错）
check('_slot_window(None) → ""', _slot_window(None) == '')
check('_slot_window(123) 不崩', isinstance(_slot_window(123), str))

_big = ('公司营收增长百分之二十，业务扩张明显，技术投入持续加大。' * 20000)
check('构造样本 > 50k', len(_big) > _KEYED_MAX_CHARS, f'len={len(_big)}')

_t0 = time.time()
_slots_big = _extract_slots(_big)
_dt_extract = time.time() - _t0
check(f'_extract_slots(500k) 有界 <5s（实测 {_dt_extract:.2f}s）', _dt_extract < 5)

# 截断等价：== 手工前 50k（证明窗口一致，无额外分叉）
check('截断结果 == 手工截前 50k', _slots_big == _extract_slots(_big[:_KEYED_MAX_CHARS]))

_t0 = time.time()
_rl = score_legacy({'text': _big}, {'text': _big}, _big, _big)
_dt_legacy = time.time() - _t0
check(f'score_legacy(500k×2) 有界 <15s（实测 {_dt_legacy:.2f}s）', _dt_legacy < 15)
check('score_legacy 返回结构完整',
      set(('score', 'severity', 'reasons', 'shared_slots',
           'slot_score', 'neg_score')) <= set(_rl.keys()))

# 正常长度真实矛盾零回归（time 路 2024Q1↔2025Q3 不相交）
_a = {'text': '该公司 2024年Q1 营收同比增长 30%，实现盈利，业务开源。'}
_b = {'text': '该公司 2025年Q3 营收同比下滑，出现亏损，项目闭源。'}
_rc = score_contradiction(_a, _b)
check('真实矛盾仍判冲突', _rc.get('verdict') == 'conflict', str(_rc.get('verdict')))
check('真实矛盾分 >=60（high 边界）', _rc.get('score', 0) >= 60, str(_rc.get('score')))

# 短文本一致语义不被截断影响
check('短文本 _extract_slots 非空（模板/2gram）',
      len(_extract_slots('公司宣布开源全新推理框架')) >= 0)


# ════════════════════════════════════════════════════════════════
# DEF-14 ｜ Markdown 输出清洗 + CSV 公式注入
# ════════════════════════════════════════════════════════════════
print('== DEF-14 · 报告输出层注入清洗 ==')
from domain_orchestrator import (  # noqa: E402
    sanitize_markdown_input, DomainOrchestrator,
)
from exporter import to_csv, to_traced_csv, _csv_safe  # noqa: E402

# 攻击载荷失效
check('script 标签移除',
      '<script' not in sanitize_markdown_input('x<script>alert(1)</script>y'))
check('iframe/object/embed/svg 移除',
      '<iframe' not in sanitize_markdown_input('<iframe src="http://x"></iframe>')
      and '<svg' not in sanitize_markdown_input('<svg/onload=alert(1)>'))
check('双引号 on*= 事件属性摘除',
      'onerror=' not in sanitize_markdown_input('<img src=x onerror="alert(1)">'))
check("单引号 on*= 事件属性摘除",
      'onload=' not in sanitize_markdown_input("<b onload='a()'>hi</b>"))
check('裸 on*= 事件属性摘除',
      'onclick=' not in sanitize_markdown_input('<b onclick=alert(1)>hi</b>'))
check('markdown 链接 javascript: 协议中和',
      'javascript:' not in sanitize_markdown_input('[x](javascript:alert(1))'))
check('vbscript/data 协议中和',
      'vbscript:' not in sanitize_markdown_input('[x](vbscript:msgbox)')
      and 'data:' not in sanitize_markdown_input('[x](data:text/html,x)'))

# 正常 markdown / 中文 / details / https 零误伤
_normal = ('<details><summary>折叠</summary>内容</details> 见 '
           '[文档](https://example.com/a?b=c) 与中文、表格 | 列、公式 a=b+c')
check('正常 markdown 原样零误伤', sanitize_markdown_input(_normal) == _normal)
check('None → 空串', sanitize_markdown_input(None) == '')
check('数字归一为字符串', sanitize_markdown_input(123) == '123')

# 端到端：恶意 subject + 恶意源字段进报告
_orc = DomainOrchestrator()
_rr = _orc.render_report('量化<script>x</script>回测主题', [
    {'title': '<img src=x onerror=alert(1)>标题', 'url': 'https://ok.com/p',
     'platform': '知乎', 'score': 80,
     'snippet': '正常内容 [坏](javascript:alert(1)) 与中文'},
], min_score=40)
_md = _rr['markdown']
check('e2e 报告无 script', '<script' not in _md)
check('e2e 报告无 onerror', 'onerror=' not in _md)
check('e2e 报告无 javascript:', 'javascript:' not in _md)
check('e2e 正常内容保留', '知乎' in _md and 'https://ok.com/p' in _md and '中文' in _md)

# fallback 渲染路径（无模板域）也清洗
_rf = _orc.render_report('<script>bad</script>无模板域主题', [
    {'title': '正常标题', 'url': 'https://n.com', 'platform': 'p', 'score': 90,
     'snippet': 'x'},
], min_score=40, domain_override='__no_such_domain__')
check('fallback 路径也无 script', '<script' not in _rf['markdown'])

# CSV 公式注入
check('csv = 公式加前缀', _csv_safe('=HYPERLINK("http://e","x")').startswith("'="))
check('csv + 命令加前缀', _csv_safe('+cmd|calc').startswith("'+"))
check('csv - 公式加前缀', _csv_safe('-1+1').startswith("'-"))
check('csv @ 公式加前缀', _csv_safe('@SUM(A1)').startswith("'@"))
check('csv Tab 首字符加前缀', _csv_safe('\t1+1').startswith("'"))
check('csv 正常文本不加前缀', _csv_safe('普通标题 http://x') == '普通标题 http://x')
check('csv 负号开头的普通中文不影响（保守前置引号）',
      _csv_safe('-0.5') == "'-0.5")  # 首字符 - 一律按公式风险处理
check('csv 数值型不处理', _csv_safe(72) == 72 and _csv_safe(0) == 0)
check('csv None → 空串', _csv_safe(None) == '')

_rep = {'domain': '金融', 'anchors': [{
    'title': '=HYPERLINK("http://e","x")', 'url': '+cmd|calc',
    'platform': '@evil', 'score': 72, 'credibility': 80}]}
_csv = to_csv(_rep)
check('to_csv 三字段全部中和',
      "'=HYPERLINK" in _csv and "'+cmd" in _csv and "'@evil" in _csv)
import csv as _csvmod  # noqa: E402
import io as _io  # noqa: E402
_rows = list(_csvmod.DictReader(_io.StringIO(_csv)))
check('to_csv 数值分数仍为 \"72\"（未加防护前缀）', _rows[0]['score'] == '72')

_csv2 = to_traced_csv({'domain': 'd', 'anchors': [{
    'title': '=evil', 'url': 'http://x', 'platform': 'p', 'score': 1,
    'credibility': 1, 'via_refs': [], 'ref_id': 1}]})
check('to_traced_csv 同样中和', "'=evil" in _csv2)


# ════════════════════════════════════════════════════════════════
# DEF-16 ｜ 中文歧义短词边界（回测 vs 来回测试）
# ════════════════════════════════════════════════════════════════
print('== DEF-16 · 中文短词误嵌守卫 ==')
import domain_router as _dr  # noqa: E402
from domain_router import _keyword_hit, _all_occurrences_embedded  # noqa: E402

# 双源配置存在（yaml 真源或内置兜底都应带这两字段）
_cfg = _dr.DOMAIN_TRIGGERS['finance-research']
check('finance 配置含 strict_keywords=[回测]',
      _cfg.get('strict_keywords') == ['回测'], str(_cfg.get('strict_keywords')))
check('finance 配置含 false_compounds',
      set(_cfg.get('false_compounds', ())) >= {'来回测试', '回测设备'},
      str(_cfg.get('false_compounds')))

# 纯函数：误嵌覆盖判定
check('「回测」in「工业来回测试」被「来回测试」全覆盖',
      _all_occurrences_embedded('回测', '工业来回测试平台', ['来回测试']) is True)
check('「回测」in「回测框架」无 false_compound 覆盖 → False',
      _all_occurrences_embedded('回测', '量化回测框架', ['来回测试']) is False)
check('混合「来回测试后做回测」存在干净出现 → False',
      _all_occurrences_embedded('回测', '来回测试后再做回测', ['来回测试']) is False)

# _keyword_hit strict 模式
check('strict 命中: 量化回测',
      _keyword_hit('回测', '量化回测平台', True, ['来回测试', '回测设备']) is True)
check('strict 拒绝: 来回测试',
      _keyword_hit('回测', '工业来回测试平台', True, ['来回测试', '回测设备']) is False)
check('strict 拒绝: 回测设备',
      _keyword_hit('回测', '回测设备维修', True, ['来回测试', '回测设备']) is False)
check('非 strict 长词仍走子串（市盈率）',
      _keyword_hit('市盈率', '讨论市盈率水平', False, []) is True)

# 端到端正反样本（报告验收 2 正 2 反 + 混合）
_POS = [('自动化回测交易系统', '真「回测」'),
        ('量化策略回测平台', '量化回测'),
        ('来回测试后再做回测分析', '混合含干净回测'),
        ('回测设备与回测框架研发', '混合含干净回测')]
_NEG = [('工业来回测试平台', '来回测试零金融语义'),
        ('回测设备的研发与制造', '回测设备误嵌'),
        ('来回测试自动化设备', '来回测试+设备')]
for text, desc in _POS:
    s = _score(detect_domain(text), 'finance-research')
    check(f'[正] {desc} → finance 命中 (>0)', s > 0, f'score={s}')
for text, desc in _NEG:
    s = _score(detect_domain(text), 'finance-research')
    check(f'[反] {desc} → finance 不命中 (=0)', s == 0, f'score={s}')

# 「来回测试设备」铁证：finance=0，tech 设备词可命中但不被回测污染
_iron = detect_domain('工业来回测试平台')
check('铁证「工业来回测试平台」finance=0',
      _score(_iron, 'finance-research') == 0)

# ASCII 词边界零回归（PE 不应命中 openai；GPT 产品词正常）
_ra = detect_domain('OpenAI Agent 大模型')
check('ASCII 零回归：openai 不因 PE 误命中 finance',
      _score(_ra, 'finance-research') == 0)
check('ASCII 零回归：openai/agent 正常命中 tech',
      _score(_ra, 'tech-research') > 0)

# 其余领域路由不受影响
for q, dom in [('股票基金估值', 'finance-research'),
               ('政策法规监管', 'policy-research'),
               ('竞品差异化对比', 'competitor-intel'),
               ('市场规模增速', 'market-research')]:
    check(f'其他域路由正常: {q}', detect_domain(q).get('domain') == dom)


# ════════════════════════════════════════════════════════════════
# 汇总
# ════════════════════════════════════════════════════════════════
print(f'\n{"="*60}')
print(f'P2 v2.1.1 守护结果：{_PASS} PASS / {_FAIL} FAIL')
print(f'{"="*60}')
sys.exit(1 if _FAIL else 0)
