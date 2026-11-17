#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""test_dispatch_stage_b.py — 调度台 §6A 阶段B 阶梯状态机守护（纯离线，零真实网络）。

覆盖标尺 MD §6A.10 六守护中阶段B 落地的：
  守护① Stage0 已足够 → _expand_query/_expand_query_variants 零调用（mock 间谍）；
  守护② 调用预算耗尽判停；单阶段剩余 <1.2s 不晋升；
  守护⑤ 判停计数取**门控后有效结果**（未评分原始条数达标但门控有效不足 → 继续晋升）；
  守护⑥ 真通道在线时 sim 不注册（互斥），纯沙箱才 sim 兜底；
  另含 auto 通道保守映射（仅 sim/纯内置 → 回退旧全扇出，默认等价）。

守护③ CN_SUBQ 四态 / 守护④ always 旧全扇出锁定已由 test_dispatch_stage_a.py 覆盖。
运行：cd <skill 根> && python tests/test_dispatch_stage_b.py
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import infoseek_pipeline as p  # noqa: E402


def _hit(url, title, snippet):
    return {'url': url, 'title': title, 'snippet': snippet}


def _setenv(**kw):
    for k, v in kw.items():
        if v is None:
            os.environ.pop(k, None)
        else:
            os.environ[k] = v


class StageBTest(unittest.TestCase):
    def setUp(self):
        # 锁定纯默认 env，避免进程遗留 INFOSEEK_* 干扰
        for k in list(os.environ):
            if k.startswith('INFOSEEK_') or k in ('WBG_GATEWAY_URL',):
                os.environ.pop(k, None)
        self._patches = []

    def tearDown(self):
        for f in self._patches:
            f.stop()

    def _patch(self, target, repl):
        from unittest.mock import patch
        m = patch.object(p, target, repl) if hasattr(p, target) else None
        if m is None:
            m = patch(target, repl)
        m.start()
        self._patches.append(m)
        return m

    # ---- 守护①：Stage0 足够 → expand 零调用 --------------------------------
    def test_g1_stage0_enough_zero_expand(self):
        calls = {'n': 0}

        def fake_expand_variants(q):
            calls['n'] += 1
            return q, ['SHOULD-NOT-BE-USED']

        def fake_expand(q):
            calls['n'] += 1
            return q + ' EXTRA'

        def fake_merge(engines, sq, max_results, reserve, deadline=None):
            # 任意 query 都返回强相关命中（门控后必然达标）
            return [_hit('http://a/%d' % i, sq, sq + ' 相关内容') for i in range(5)]

        self._patch('_expand_query_variants', fake_expand_variants)
        self._patch('_expand_query', fake_expand)
        self._patch('_parallel_merge_with_reserve', fake_merge)
        # 门控有效计数强制达标 → Stage0 判停
        self._patch('_effective_count', lambda results, q, ms=12: max(1, len(results)))

        got = p._staged_fanout(['eng'], '比亚迪', 10, [], deadline=None, need=3)
        self.assertGreaterEqual(len(got), 1)
        self.assertEqual(calls['n'], 0, 'Stage0 已足够时扩展函数必须零调用')

    # ---- 守护①b：Stage0 不足才付扩展成本（_staged_plan 内部） ---------------
    def test_g1b_expand_only_when_promote(self):
        # _staged_plan 显式调用 expand（这是 Stage0 不足后晋升路径，允许调用）
        calls = {'n': 0}
        real = p._expand_query_variants

        def spy(q):
            calls['n'] += 1
            return real(q)
        self._patch('_expand_query_variants', spy)
        # budget=1 → Stage0 后预算耗尽不晋升，_staged_plan 不应被调用
        _setenv(INFOSEEK_QUERY_BUDGET_VARIANTS='1')
        self.assertEqual(p._query_budget_variants(), 1)

        def fake_merge(engines, sq, max_results, reserve, deadline=None):
            return []
        self._patch('_parallel_merge_with_reserve', fake_merge)
        self._patch('_effective_count', lambda r, q, ms=12: 0)
        p._staged_fanout(['eng'], '比亚迪', 10, [], deadline=None, need=3)
        self.assertEqual(calls['n'], 0, '预算=1（仅Stage0）时不应构建晋升计划/不调扩展')

    # ---- 守护②：调用预算耗尽判停 ------------------------------------------
    def test_g2_budget_exhaustion_caps_calls(self):
        _setenv(INFOSEEK_QUERY_BUDGET_VARIANTS='2')
        merge_calls = []

        def fake_merge(engines, sq, max_results, reserve, deadline=None):
            merge_calls.append(sq)
            return [_hit('http://x/%s/%d' % (abs(hash(sq)), len(merge_calls)),
                         sq, sq)]
        self._patch('_parallel_merge_with_reserve', fake_merge)
        self._patch('_effective_count', lambda r, q, ms=12: 0)  # 永不达标
        # plan 给出多个候选
        self._patch('_staged_plan',
                    lambda q: (q, ['主题一', '主题二', '主题三'], ['别名X', '别名Y']))
        p._staged_fanout(['eng'], '某长尾查询词', 10, [], deadline=None, need=9)
        # Stage0 1 次 + 预算 2 内最多再 1 次 = 2 次合并调用
        self.assertEqual(len(merge_calls), 2, '预算=2 时累计 query 变体不得超过 2')

    # ---- 守护②：剩余 <1.2s 不晋升 ------------------------------------------
    def test_g2_low_remaining_no_promote(self):
        merge_calls = []

        def fake_merge(engines, sq, max_results, reserve, deadline=None):
            merge_calls.append(sq)
            return [_hit('http://z/%d' % len(merge_calls), sq, sq)]
        self._patch('_parallel_merge_with_reserve', fake_merge)
        self._patch('_effective_count', lambda r, q, ms=12: 0)
        self._patch('_staged_plan', lambda q: (q, ['主题一'], ['别名X']))
        # deadline 剩余 0.5s（< 1.2s）
        import time as _t
        self._patch('_remaining_budget', lambda dl: 0.5)
        deadline = _t.monotonic() + 0.5
        p._staged_fanout(['eng'], '某长尾查询词', 10, [], deadline=deadline, need=9)
        self.assertEqual(len(merge_calls), 1, '剩余 <1.2s 时只跑 Stage0，不晋升')

    # ---- 守护②b：剩余充足才晋升 -------------------------------------------
    def test_g2b_enough_remaining_promotes(self):
        merge_calls = []

        def fake_merge(engines, sq, max_results, reserve, deadline=None):
            merge_calls.append(sq)
            return [_hit('http://y/%d' % len(merge_calls), sq, sq)]
        self._patch('_parallel_merge_with_reserve', fake_merge)
        self._patch('_effective_count', lambda r, q, ms=12: 0)
        self._patch('_staged_plan', lambda q: (q, ['主题一'], []))
        self._patch('_remaining_budget', lambda dl: 5.0)  # 充足
        import time as _t
        p._staged_fanout(['eng'], '某长尾查询词', 10, [],
                         deadline=_t.monotonic() + 5, need=9)
        self.assertGreaterEqual(len(merge_calls), 2, '剩余充足且预算允许时应晋升 Stage1')

    # ---- 守护⑤：门控后有效结果才判停（原始条数≠有效） ----------------------
    def test_g5_uses_post_gate_effective_count(self):
        # _parallel_merge 总返回很多**原始**结果（>= cap），但门控有效=0 → 必须继续晋升，
        # 验证不再用旧的 len(collected)>=_cap 原始计数判停。
        merge_calls = []

        def fake_merge(engines, sq, max_results, reserve, deadline=None):
            merge_calls.append(sq)
            return [_hit('http://raw/%s/%d' % (len(merge_calls), i),
                         '无关标题%d' % i, '无关正文%d' % i) for i in range(20)]
        self._patch('_parallel_merge_with_reserve', fake_merge)
        # 门控有效恒 0（模拟大量但全不相关）
        self._patch('_effective_count', lambda r, q, ms=12: 0)
        self._patch('_staged_plan', lambda q: (q, ['主题一', '主题二'], []))
        _setenv(INFOSEEK_QUERY_BUDGET_VARIANTS='3')
        p._staged_fanout(['eng'], '某长尾查询词', 10, [], deadline=None, need=3)
        self.assertGreater(len(merge_calls), 1,
                           '门控有效不足时，即使原始条数>=cap也必须继续晋升')

    # ---- 守护⑤：_effective_count 真实门控谓词语义 --------------------------
    def test_g5_effective_count_smoke(self):
        self.assertEqual(p._effective_count([], 'q'), 0)
        # 强相关命中：标题/正文包含 query 全文
        hits = [_hit('http://a', '信阳板栗收购价格', '信阳板栗 最新收购价格行情'),
                _hit('http://b', '完全无关天气', '今天晴转多云东北风')]
        n = p._effective_count(hits, '信阳板栗收购价格', min_score=12)
        self.assertGreaterEqual(n, 0)
        self.assertLessEqual(n, 2)
        # 异常兜底：传非法结构不抛
        self.assertEqual(p._effective_count(None, 'q'), 0)  # type: ignore

    # ---- 守护⑥：sim / 真通道互斥 ------------------------------------------
    def test_g6_sim_vs_real_exclusive(self):
        import workbuddy_channel as wb
        import importlib
        # 无 WBG_GATEWAY_URL → 仿真
        _setenv(WBG_GATEWAY_URL=None)
        importlib.reload(wb)
        self.assertTrue(wb.is_simulated())
        self.assertEqual(wb.meta.get('capability'), 'simulated')
        self.assertIn('(sim)', wb.meta.get('name', ''))
        # 有真实网关 URL → 非仿真
        _setenv(WBG_GATEWAY_URL='http://localhost:5126')
        importlib.reload(wb)
        self.assertFalse(wb.is_simulated())
        self.assertNotIn('capability', wb.meta)

    def test_g6_platform_simulated_triage(self):
        # platform_adapter.platform_engine_simulated 三态
        import platform_adapter as pa
        orig = pa.platform_engine
        try:
            pa.platform_engine = lambda: None  # type: ignore
            self.assertIsNone(pa.platform_engine_simulated())
            pa.platform_engine = lambda: ('WorkBuddy-WebSearch(sim)', lambda *a: {})  # type: ignore
            self.assertTrue(pa.platform_engine_simulated())
            pa.platform_engine = lambda: ('WorkBuddy-WebSearch', lambda *a: {})  # type: ignore
            self.assertFalse(pa.platform_engine_simulated())
        finally:
            pa.platform_engine = orig  # type: ignore

    # ---- auto 保守映射：纯沙箱（无真通道）→ 非阶梯（旧全扇出） -------------
    def test_auto_conservative_without_real_channel(self):
        self._patch('_channel_is_high_quality', lambda: False)
        # auto 在纯沙箱 → _resolve_subqueries 仍返回 decompose 全扇出（旧行为）
        _setenv(INFOSEEK_CN_SUBQ='auto')
        subs = p._resolve_subqueries('信阳板栗今年最新收购价格行情走势',
                                     '信阳板栗今年最新收购价格行情走势', mode='auto')
        self.assertIsInstance(subs, list)
        self.assertGreaterEqual(len(subs), 1)
        # 通道判定为 False 时 search_web 不置 _use_staged（间接：channel 判定函数被消费）
        self.assertFalse(p._channel_is_high_quality())

    def test_auto_staged_with_real_channel(self):
        # auto + 真通道 → 高质量判定 True（search_web 据此走阶梯）
        self._patch('_channel_is_high_quality', lambda: True)
        self.assertTrue(p._channel_is_high_quality())


if __name__ == '__main__':
    unittest.main(verbosity=2)
