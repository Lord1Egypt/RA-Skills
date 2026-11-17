#!/usr/bin/env python3
"""
test_ga5_tokenizer_v184.py — GA5 分词单源化守护测试（v1.8.4）

守护对象：
  1. 单源性：`_tokenize_subject` / `_tokenize_query` 必须委托 `text_tokenizer.tokenize_text`
     （禁止任何一侧重新长出独立分词算法体 → 防 GA5 回归）
  2. 门控语义：require_chinese 有意分叉 A 保留（纯英文/数字 query → 空集）
  3. 口径等价：两侧对含中文输入结果完全一致（无意分叉 B 永久归零）
  4. 性能护栏：`_filter_relevant` 函数体 AST 级零 import / 零 sys.path.insert，
     300 次调用后 sys.path 恒定（防 O(n²) 膨胀复发，同 GA8 根因）
  5. 回退算法：中文 ≤4 整段 / >4 2-gram；英数 ≥2 整词；≥2 字符过滤；小写归一

独立运行：python3 tests/test_ga5_tokenizer_v184.py
"""
import ast
import logging
import os
import sys
import unittest
from pathlib import Path
from unittest import mock

os.environ.setdefault('INFOSEEK_PLATFORM_WEBSEARCH', 'off')
# 测试卫生：G14 的 300 次 _filter_relevant 循环会逐次打 INFO，且真源会发一次性
# jieba 缺失 WARNING —— 全部静默，避免污染 run_all.py 汇总输出。
logging.disable(logging.WARNING)
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(_ROOT, 'scripts'))

from text_tokenizer import tokenize_text, has_chinese, MOD_VERSION  # noqa: E402
import anchor_adapter  # noqa: E402
import infoseek_pipeline as pipeline  # noqa: E402

PASS = FAIL = 0


def check(name, cond, detail=''):
    global PASS, FAIL
    if cond:
        PASS += 1
        print(f"  PASS | {name}")
    else:
        FAIL += 1
        print(f"  FAIL | {name}" + (f" | {detail}" if detail else ''))


CN_SAMPLES = ['无限工坊 机器人', '钢卷分切工艺参数', 'AI芯片2026', 'iPhone17 发布会',
              '新能源汽车', '量化交易 策略 回测', '质量 管理 体系 ISO9001',
              '深圳无限工坊', '让刀 微裂纹 冷柜', '中文Mixed英文Test混排', '钢铁-水泥_价差']
EN_SAMPLES = ['OpenAI Agent', '2026', 'Zhang San person disambiguation', 'arxiv preprints']


class TestSingleSource(unittest.TestCase):
    def test_all(self):
        aa_src = Path(anchor_adapter.__file__).read_text(encoding='utf-8')
        pl_src = Path(pipeline.__file__).read_text(encoding='utf-8')
        pl_tree = ast.parse(pl_src)
        aa_tree = ast.parse(aa_src)

        print('\n[1] 单源性（GA5 核心）')
        fn_aa = next(n for n in aa_tree.body
                     if isinstance(n, ast.FunctionDef) and n.name == '_tokenize_subject')
        fn_pl = next(n for n in pl_tree.body
                     if isinstance(n, ast.FunctionDef) and n.name == '_tokenize_query')
        body_aa = [ast.unparse(s) for s in fn_aa.body if not isinstance(s, ast.Expr)]
        body_pl = [ast.unparse(s) for s in fn_pl.body if not isinstance(s, ast.Expr)]
        check('G1 _tokenize_subject 函数体仅一句委托',
              body_aa == ['return tokenize_text(subject)'], f'{body_aa}')
        check('G2 _tokenize_query 函数体仅一句委托（带门控+告警）',
              body_pl == ['return tokenize_text(query, require_chinese=True, '
                          'warn_on_fallback=True)'], f'{body_pl}')
        # 注：anchor_adapter 仍有 jieba.analyse.textrank（三跑关键词**抽取**流水线，
        # 属另一能力，不在 GA5「分词」单源化范围）；此处只禁「分词调用」复活。
        check('G3 两侧均无独立分词算法体（jieba.lcut 仅存于真源）',
              'jieba.lcut' not in aa_src and 'jieba.lcut' not in pl_src
              and '_SEG_RE' not in aa_src and '_SEG_RE' not in pl_src)
        check('G4 两侧顶层均导入 tokenize_text',
              'from text_tokenizer import tokenize_text' in aa_src
              and 'from text_tokenizer import tokenize_text' in pl_src)
        check('G5 text_tokenizer 零 infoseek 内部依赖（无循环依赖风险）',
              not [n for n in ast.walk(ast.parse(Path(
                  _ROOT, 'scripts', 'text_tokenizer.py').read_text(encoding='utf-8')))
                  if isinstance(n, ast.ImportFrom) and n.module
                  and n.module.split('.')[0] in ('anchor_adapter', 'infoseek_pipeline',
                                                 'infoseek_core_v2', 'domain_router')])

        print('\n[2] 门控语义（有意分叉 A）')
        check('G6 纯英文/数字 query → 空集（中文硬门槛不触发）',
              all(pipeline._tokenize_query(s) == set() for s in EN_SAMPLES))
        check('G7 同样本 subject 侧无门控 → 非空',
              all(anchor_adapter._tokenize_subject(s) for s in EN_SAMPLES))
        check('G8 含中文 query 门控放行',
              all(pipeline._tokenize_query(s) for s in CN_SAMPLES))

        print('\n[3] 口径等价（无意分叉 B 归零）')
        forks = [s for s in CN_SAMPLES
                 if anchor_adapter._tokenize_subject(s) != pipeline._tokenize_query(s)]
        check('G9 含中文样本两侧结果完全一致（分叉=0）', not forks, f'分叉={forks}')
        check('G10 全样本分叉集合 == 无中文样本集合（分叉唯一来源=门控）',
              {s for s in CN_SAMPLES + EN_SAMPLES
               if anchor_adapter._tokenize_subject(s) != pipeline._tokenize_query(s)}
              == {s for s in EN_SAMPLES if s.strip()})

        print('\n[4] 性能护栏（996-999 局部 import 收口）')
        fn_f = next(n for n in pl_tree.body
                    if isinstance(n, ast.FunctionDef) and n.name == '_filter_relevant')
        imps = [ast.unparse(n) for n in ast.walk(fn_f)
                if isinstance(n, (ast.Import, ast.ImportFrom))]
        pins = [ast.unparse(n) for n in ast.walk(fn_f)
                if isinstance(n, ast.Call) and 'path.insert' in ast.unparse(n.func)]
        check('G11 _filter_relevant 体内零 import', not imps, f'{imps}')
        check('G12 _filter_relevant 体内零 sys.path.insert', not pins, f'{pins}')
        check('G13 pipeline 以模块对象引用 anchor_adapter（晚绑定，非 from-import）',
              'import anchor_adapter as _anchor_mod' in pl_src
              and '_anchor_mod.compute_semantic_similarity' in pl_src
              and '_anchor_mod._string_containment_similarity' in pl_src
              and 'from anchor_adapter import (infos_to_seek, compute' not in pl_src)
        results = [{'title': f'新能源汽车 报告 {i}',
                    'snippet': '钢卷分切工艺参数 无限工坊 机器人',
                    'url': f'http://x/{i}'} for i in range(25)]
        n0 = len(sys.path)
        for _ in range(300):
            pipeline._filter_relevant([dict(r) for r in results], '新能源汽车 无限工坊')
        d = len(sys.path) - n0
        check('G14 300 次调用后 sys.path 恒定（Δ=0）', d == 0, f'Δ={d}')

        print('\n[5] 回退算法口径')
        # 显式锁定纯 Python 回退路径：jieba 装了会走 jieba.lcut（切词粒度不同），
        # 本组断言测的是**回退算法**本身。2026-09-29：探测收口到 jieba_bridge，
        # 原 _tt._JIEBA/_JIEBA_PROBED 私有状态删除 → mock bridge.lcut 返回 None
        # （语义=jieba 缺失/异常）锁定回退路径。
        import jieba_bridge as _jb
        with mock.patch.object(_jb, 'lcut', return_value=None):
            tk = tokenize_text('钢卷分切工艺参数')
            check('G15 中文 >4 字切 2-gram', '钢卷' in tk and '分切' in tk, f'{sorted(tk)}')
            check('G16 中文 ≤4 字整段成词（5 字起才切 2-gram）',
                  tokenize_text('质量管理') == {'质量管理'}
                  and tokenize_text('无限工坊') == {'无限工坊'}
                  and len(tokenize_text('新能源汽车')) == 4,
                  f"{sorted(tokenize_text('无限工坊'))}")
            check('G17 英数 ≥2 整词 + 小写归一',
                  tokenize_text('OpenAI Agent 2026') == {'openai', 'agent', '2026'})
            check('G18 单字符过滤（≥2）', tokenize_text('A 新 钢') == set())
            check('G19 中英混排不跨边界切分（无跨边界 2-gram 噪声）',
                  'i1' not in tokenize_text('AI芯片2026')
                  and set(tokenize_text('AI芯片2026')) >= {'ai', '芯片', '2026'},
                  f"{sorted(tokenize_text('AI芯片2026'))}")
        check('G20 空输入安全', tokenize_text('') == set() and tokenize_text(None or '') == set())
        check('G21 has_chinese 判据正确',
              has_chinese('中文') and not has_chinese('OpenAI 2026'))
        check('G22 mod-v 声明存在', bool(MOD_VERSION), MOD_VERSION)

        print('\n[6] mock 可patch性（既有测试隐性契约，防 from-import 早绑定复发）')
        with mock.patch('anchor_adapter.compute_semantic_similarity',
                        side_effect=lambda t, q: 15), \
             mock.patch('anchor_adapter._string_containment_similarity', return_value=0):
            out = pipeline._filter_relevant(
                [{'url': 'https://e', 'title': 'edge', 'snippet': ''}], 'q')
        check('G23 mock.patch(anchor_adapter.*) 对 _filter_relevant 生效',
              any(r.get('relevance') == 15 for r in out), f'{out}')
        _fake = lambda t, s, method='jaccard': 42
        _save = anchor_adapter._string_containment_similarity
        try:
            anchor_adapter._string_containment_similarity = _fake
            check('G24 直接赋值 monkey-patch 同样生效（test_p1p3p2_fixes 契约）',
                  anchor_adapter._string_containment_similarity('x', 'y') == 42
                  and pipeline._anchor_mod._string_containment_similarity('x', 'y') == 42)
        finally:
            anchor_adapter._string_containment_similarity = _save

        print(f'\n结果: {PASS} PASS / {FAIL} FAIL')
        self.assertEqual(FAIL, 0, f'{FAIL} 项守护断言失败')


if __name__ == '__main__':
    unittest.main(verbosity=0, exit=True)
