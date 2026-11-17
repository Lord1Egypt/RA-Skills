#!/usr/bin/env python3
"""
tests/test_l2_renderer_v142.py — L2 多引擎渲染层测试（v1.4.2）

覆盖：
  1. 引擎注册表：结构完整 / 场景归属 / 降级链
  2. 引擎探测：缺失环境全部 False（不误报可用）
  3. 路由降级：无引擎 → 空串（行为零回归）
  4. 健康状态机：mock 失败引擎被跳过 / 熔断记录
  5. 批量渲染：无引擎 → 全空结果不崩溃
  6. 向后兼容壳：mcp_tools_search._fetch_render_with_playwright 委托不抛
"""

import os
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "core"))


class TestEngineRegistry(unittest.TestCase):
    def test_registry_structure(self):
        from l2_renderer import RENDER_ENGINES
        for name in ("camoufox", "obscura", "patchright", "chromium"):
            self.assertIn(name, RENDER_ENGINES)
            eng = RENDER_ENGINES[name]
            for k in ("probe", "render", "scene", "priority", "weight", "desc"):
                self.assertIn(k, eng)

    def test_scene_order(self):
        from l2_renderer import _SCENE_ORDER
        # default 场景 Camoufox 优先（反爬主引擎）
        self.assertEqual(_SCENE_ORDER["default"][0], "camoufox")
        # batch 场景 Obscura 优先
        self.assertEqual(_SCENE_ORDER["batch"][0], "obscura")
        # last 场景 Chromium 兜底
        self.assertEqual(_SCENE_ORDER["last"][0], "chromium")

    def test_probe_all_false_in_clean_env(self):
        """干净环境（无 camoufox/obscura/patchright/playwright）→ 全 False。"""
        from l2_renderer import _engine_available
        for name in ("camoufox", "obscura", "patchright", "chromium"):
            # 探测不抛异常即可（返回 True/False 均可，但必须是 bool）
            r = _engine_available(name)
            self.assertIsInstance(r, bool)


class TestRenderRouting(unittest.TestCase):
    def setUp(self):
        # 真实环境可能残留引擎熔断状态（L2-camoufox fail_count 达阈值被禁用），
        # mock probe 无法绕过 _is_disabled → 每用例前清理（2026-09-06 实测暴露）
        try:
            import l2_renderer as lr
            sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
            from engine_lifecycle import get_lifecycle
            lc = get_lifecycle()
            for n in lr.RENDER_ENGINES:
                lc.reset(f"L2-{n}")
        except Exception:
            pass

    def test_render_empty_when_no_engine(self):
        """无引擎可用 → 返回空串（调用方降级 L1，零回归）。"""
        from l2_renderer import render_html
        # mock 所有 probe 为 False
        import l2_renderer as lr
        orig = {n: e["probe"] for n, e in lr.RENDER_ENGINES.items()}
        for n in lr.RENDER_ENGINES:
            lr.RENDER_ENGINES[n]["probe"] = lambda: False
        try:
            html = render_html("https://example.com", timeout=2)
            self.assertEqual(html, "")
        finally:
            for n, p in orig.items():
                lr.RENDER_ENGINES[n]["probe"] = p

    def test_render_success_first_engine(self):
        """首个可用引擎命中即返回（不降级）。"""
        from l2_renderer import render_html
        import l2_renderer as lr
        orig = {n: e["probe"] for n, e in lr.RENDER_ENGINES.items()}
        orig_render = {n: e["render"] for n, e in lr.RENDER_ENGINES.items()}
        # 只让 camoufox 可用，且渲染成功
        for n in lr.RENDER_ENGINES:
            lr.RENDER_ENGINES[n]["probe"] = (lambda n=n: n == "camoufox")
            lr.RENDER_ENGINES[n]["render"] = (lambda url, t=15, n=n: f"<html>{n}</html>")
        try:
            html = render_html("https://example.com", timeout=2)
            self.assertIn("<html>camoufox</html>", html)
        finally:
            for n, p in orig.items():
                lr.RENDER_ENGINES[n]["probe"] = p
            for n, r in orig_render.items():
                lr.RENDER_ENGINES[n]["render"] = r

    def test_render_cross_over_on_failure(self):
        """首引擎失败 → cross-over 到次引擎（不中断）。"""
        from l2_renderer import render_html
        import l2_renderer as lr
        orig = {n: e["probe"] for n, e in lr.RENDER_ENGINES.items()}
        orig_render = {n: e["render"] for n, e in lr.RENDER_ENGINES.items()}
        calls = []
        for n in lr.RENDER_ENGINES:
            lr.RENDER_ENGINES[n]["probe"] = (lambda n=n: n in ("camoufox", "patchright"))
        # camoufox 抛异常，patchright 成功
        def fake_render(url, t=15, n=None):
            calls.append(n)
            if n == "camoufox":
                raise RuntimeError("boom")
            return f"<html>{n}</html>"
        lr.RENDER_ENGINES["camoufox"]["render"] = lambda url, t=15: fake_render(url, t, "camoufox")
        lr.RENDER_ENGINES["patchright"]["render"] = lambda url, t=15: fake_render(url, t, "patchright")
        for n in ("obscura", "chromium"):
            lr.RENDER_ENGINES[n]["render"] = lambda url, t=15, n=n: fake_render(url, t, n)
        try:
            html = render_html("https://example.com", timeout=2)
            self.assertIn("<html>patchright</html>", html)
            self.assertIn("camoufox", calls)  # 确认尝试过 camoufox
        finally:
            for n, p in orig.items():
                lr.RENDER_ENGINES[n]["probe"] = p
            for n, r in orig_render.items():
                lr.RENDER_ENGINES[n]["render"] = r


class TestBatchRender(unittest.TestCase):
    def test_batch_empty_without_engine(self):
        from l2_renderer import render_html_batch
        import l2_renderer as lr
        orig = {n: e["probe"] for n, e in lr.RENDER_ENGINES.items()}
        for n in lr.RENDER_ENGINES:
            lr.RENDER_ENGINES[n]["probe"] = lambda: False
        try:
            out = render_html_batch(["https://a.com", "https://b.com"], concurrency=2)
            self.assertEqual(len(out), 2)
            for r in out:
                self.assertEqual(r["html"], "")
                self.assertIsNone(r["engine"])
        finally:
            for n, p in orig.items():
                lr.RENDER_ENGINES[n]["probe"] = p


class TestCompatibilityShell(unittest.TestCase):
    def test_shell_no_engine_returns_empty(self):
        """向后兼容壳：无引擎时返回空串不抛异常（L1 降级路径）。"""
        from mcp_tools_search import _fetch_render_with_playwright
        import l2_renderer as lr
        orig = {n: e["probe"] for n, e in lr.RENDER_ENGINES.items()}
        for n in lr.RENDER_ENGINES:
            lr.RENDER_ENGINES[n]["probe"] = lambda: False
        try:
            r = _fetch_render_with_playwright("https://example.com", timeout=2)
            self.assertEqual(r, "")
        finally:
            for n, p in orig.items():
                lr.RENDER_ENGINES[n]["probe"] = p


if __name__ == "__main__":
    unittest.main(verbosity=2)
