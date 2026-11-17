#!/usr/bin/env python3
"""
V1.2 功能测试
覆盖：版本解析、引擎注册表、缓存、SimHash 与排序、统一 HTTP 出口、
      解析诊断、运行日志、隐私优先兜底策略
"""

import ast
import contextlib
import io
import os
import re
import sys
import tempfile
import unittest

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from version_util import (
    get_current_version, parse_version, compare_versions, FALLBACK_VERSION,
)
from engines_registry import (
    ENGINE_REGISTRY, all_engine_names, default_engines, strict_fallback_engines,
    validate_engines, get_authority, is_valid_engine, format_engine_table,
)
from cache import SearchCache, make_cache_key
from ranking import (
    compute_simhash, hamming_distance, deduplicate, rank_results,
    RankWeights, weights_from_config, domain_score, domain_of,
)
from http_client import USER_AGENT_POOL, RetryPolicy, pick_user_agent
from engine_selectors import (
    SELECTORS, get_selectors, is_redirect_url, REDIRECT_PATTERNS,
)
from logging_util import SearchLogger, build_logger_from_config
from privacy import PrivacyManager
from search import SearchResult, SearchOrchestrator


# ============================================================
# 版本解析（P0-1）
# ============================================================

class TestVersionUtil(unittest.TestCase):
    """版本号必须来自 SKILL.md，不得硬编码"""

    def test_version_matches_skill_md(self):
        version = get_current_version()
        skill_md = os.path.join(os.path.dirname(__file__), '..', 'SKILL.md')
        with open(skill_md, encoding='utf-8-sig') as f:
            content = f.read()
        self.assertIn(f"version: {version}", content)

    def test_version_is_not_hardcoded_old(self):
        """确保不再返回 V1.1 时期漂移的 1.0.0"""
        self.assertNotEqual(get_current_version(), "1.0.0")

    def test_parse_version(self):
        self.assertEqual(parse_version("1.2.0"), (1, 2, 0))
        self.assertEqual(parse_version("v1.2.0"), (1, 2, 0))

    def test_compare_versions(self):
        self.assertEqual(compare_versions("1.2.0", "1.1.0"), 1)
        self.assertEqual(compare_versions("1.1.0", "1.2.0"), -1)
        self.assertEqual(compare_versions("1.2.0", "1.2.0"), 0)

    def test_update_checker_uses_same_version(self):
        """更新检查模块必须与 SKILL.md 同源，否则会误报新版本"""
        import update_checker
        self.assertEqual(update_checker.CURRENT_VERSION, get_current_version())

    def test_no_hardcoded_version_in_scripts(self):
        """
        脚本中不得硬编码版本号

        quick_setup.py 曾把标题写死为 v1.1，发版到 1.2.0 后
        用户安装时仍看到旧版本号。版本号只应来自 SKILL.md。
        """
        scripts_dir = os.path.join(os.path.dirname(__file__), "..", "scripts")
        current = get_current_version()
        # 只匹配带 v 前缀的展示型版本号（如 "隐私搜索 v1.1"）。
        # 裸的 "1.0.0" 多为格式示例或解析入参，交由 docstring 过滤即可。
        pattern = re.compile(r"v\d+\.\d+(?:\.\d+)?")
        offenders = []
        for fn in sorted(os.listdir(scripts_dir)):
            if not fn.endswith(".py"):
                continue
            path = os.path.join(scripts_dir, fn)
            with open(path, encoding="utf-8") as f:
                source = f.read()
            tree = ast.parse(source, filename=fn)

            # docstring 与注释属于说明性文字，其中出现历史版本号是正常记述。
            # 逐行扫描无法区分二者，故改用 AST：先登记全部 docstring 节点，
            # 再只检查真正参与运算的字符串字面量。
            docstrings = set()
            for node in ast.walk(tree):
                if isinstance(node, (ast.Module, ast.ClassDef,
                                     ast.FunctionDef, ast.AsyncFunctionDef)):
                    body = getattr(node, "body", None)
                    if not body:
                        continue
                    first = body[0]
                    if (isinstance(first, ast.Expr)
                            and isinstance(first.value, ast.Constant)
                            and isinstance(first.value.value, str)):
                        docstrings.add(id(first.value))

            for node in ast.walk(tree):
                if not isinstance(node, ast.Constant):
                    continue
                if not isinstance(node.value, str) or id(node) in docstrings:
                    continue
                for hit in pattern.findall(node.value):
                    if hit.lstrip("vV") != current:
                        offenders.append(
                            "%s:%s %s" % (fn, node.lineno, hit))
        self.assertFalse(
            offenders,
            "脚本中存在与 SKILL.md 不符的硬编码版本号：%s" % offenders)

    def test_require_dependencies_passes_when_installed(self):
        """依赖齐备时检查函数不得误退出"""
        from version_util import require_dependencies
        try:
            require_dependencies()
        except SystemExit:
            self.fail("依赖已安装却触发了退出")

    def test_require_dependencies_reports_missing(self):
        """
        缺失依赖时应退出并给出安装指引

        直接抛裸 ModuleNotFoundError 会让首次使用的用户
        无从判断该装什么包、用哪个解释器装。
        """
        from version_util import require_dependencies
        buf = io.StringIO()
        with contextlib.redirect_stderr(buf):
            with self.assertRaises(SystemExit) as ctx:
                require_dependencies(("definitely_not_installed_pkg",))
        self.assertEqual(ctx.exception.code, 2)
        message = buf.getvalue()
        self.assertIn("缺少运行所需的依赖", message)
        self.assertIn("pip install", message)


class TestDisplayWidth(unittest.TestCase):
    """终端输出对齐必须按显示列数计算，不能按字符数"""

    def test_cjk_counts_as_two_columns(self):
        from version_util import display_width
        self.assertEqual(display_width("abc"), 3)
        self.assertEqual(display_width("中文"), 4)
        self.assertEqual(display_width("中a文"), 5)
        self.assertEqual(display_width("🔔"), 2)

    def test_pad_display_fills_to_target(self):
        from version_util import display_width, pad_display
        for text in ("abc", "中文标题", "🔔 提示", ""):
            self.assertEqual(display_width(pad_display(text, 20)), 20)

    def test_pad_display_clips_overlong(self):
        """超长内容按列裁剪，不得把边框顶开"""
        from version_util import display_width, pad_display
        self.assertEqual(display_width(pad_display("中文" * 30, 10)), 10)

    def test_update_box_lines_are_aligned(self):
        """
        更新提示框每行宽度必须一致

        早期实现用 f-string 的 {:<52} 按字符数填充，
        中文标签实占两列，边框永远错位。
        """
        from datetime import datetime
        from update_checker import (
            display_update_notification, UpdateInfo, _BOX_WIDTH,
        )
        from version_util import display_width

        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            display_update_notification(UpdateInfo(
                current_version="1.1.0",
                latest_version="1.2.0",
                changelog="增加缓存层、优化排序权重、修复跳转链重复问题、补充解析健壮性处理",
                download_url=(
                    "https://skillhub.example.com/skills/"
                    "privacy-search/releases/v1.2.0"),
                checked_at=datetime.now(),
                has_update=True,
            ))
        rendered = [ln for ln in buf.getvalue().splitlines() if ln.strip()]
        self.assertTrue(rendered)
        for line in rendered:
            self.assertEqual(
                display_width(line), _BOX_WIDTH + 2,
                "提示框行宽不一致：%r" % line)

    def test_update_box_wraps_instead_of_truncating(self):
        """长链接必须折行完整显示，截断会导致无法复制"""
        from datetime import datetime
        from update_checker import display_update_notification, UpdateInfo

        url = ("https://skillhub.example.com/skills/"
               "privacy-search/releases/v1.2.0")
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            display_update_notification(UpdateInfo(
                current_version="1.1.0", latest_version="1.2.0",
                changelog="更新说明", download_url=url,
                checked_at=datetime.now(), has_update=True,
            ))
        # 去掉边框与填充空格后，完整链接应能重新拼出
        joined = "".join(
            ln.strip("║").strip()
            for ln in buf.getvalue().splitlines())
        self.assertIn(url, joined.replace(" ", ""))


# ============================================================
# 引擎注册表（P0-2 / P0-7）
# ============================================================

class TestEnginesRegistry(unittest.TestCase):
    """引擎清单单一真相源"""

    def test_ten_engines(self):
        self.assertEqual(len(all_engine_names()), 10)

    def test_no_phantom_engine(self):
        """Ecosia / Kagi 从未实现，不得出现在注册表"""
        names = all_engine_names()
        self.assertNotIn("ecosia", names)
        self.assertNotIn("kagi", names)

    def test_strict_engines_exclude_low_privacy(self):
        strict = strict_fallback_engines()
        for name in ("baidu", "bing", "sogou", "360"):
            self.assertNotIn(name, strict)

    def test_validate_engines(self):
        valid, invalid = validate_engines(["baidu", "notexist", "bing"])
        self.assertEqual(valid, ["baidu", "bing"])
        self.assertEqual(invalid, ["notexist"])

    def test_privacy_blocked_count(self):
        """strict 模式应屏蔽 4 个国内引擎，V1.1 时因硬编码只统计到部分"""
        pm = PrivacyManager({"privacy": {"default_mode": "strict"}})
        pm.set_mode_silent("strict")
        blocked = pm.get_blocked_engines()
        self.assertEqual(sorted(blocked), sorted(["baidu", "bing", "sogou", "360"]))

    def test_engine_table_alignment(self):
        """中文列宽按显示宽度计算，表格不应错位"""
        table = format_engine_table()
        lines = [ln for ln in table.splitlines() if ln.strip()]
        self.assertGreaterEqual(len(lines), 11)


# ============================================================
# 缓存（F1-1）
# ============================================================

class TestCache(unittest.TestCase):
    """结果缓存与搜索历史"""

    def setUp(self):
        self.db = os.path.join(tempfile.mkdtemp(), "cache_test.db")
        self.cache = SearchCache(db_path=self.db, ttl=3600, max_size_mb=1)

    def tearDown(self):
        try:
            self.cache.close()
        except Exception:
            pass

    def test_key_is_engine_order_independent(self):
        """引擎顺序不同不应产生不同缓存键"""
        k1 = make_cache_key("python", ["baidu", "bing"], "normal", 10)
        k2 = make_cache_key("python", ["bing", "baidu"], "normal", 10)
        self.assertEqual(k1, k2)

    def test_key_differs_by_privacy_mode(self):
        """不同隐私模式结果不同，不得复用缓存"""
        k1 = make_cache_key("python", ["bing"], "normal", 10)
        k2 = make_cache_key("python", ["bing"], "strict", 10)
        self.assertNotEqual(k1, k2)

    def test_set_and_get(self):
        key = make_cache_key("test", ["bing"], "normal", 5)
        data = [{"title": "T", "url": "https://a.com", "snippet": "s", "engine": "bing"}]
        self.cache.set(key, "test", ["bing"], "normal", data)
        got = self.cache.get(key)
        self.assertIsNotNone(got)
        self.assertEqual(got[0]["title"], "T")

    def test_expired_entry_not_returned(self):
        """TTL 到期后不得返回旧结果"""
        import time as _t
        short = SearchCache(db_path=self.db, ttl=1, max_size_mb=1)
        key = make_cache_key("x", ["bing"], "normal", 5)
        short.set(key, "x", ["bing"], "normal", [{"title": "T"}])
        self.assertIsNotNone(short.get(key))
        _t.sleep(1.2)
        self.assertIsNone(short.get(key))
        short.close()

    def test_zero_ttl_disables_cache(self):
        """ttl=0 表示不缓存，而非永不过期（避免隐私数据长期滞留）"""
        zero = SearchCache(db_path=self.db, ttl=0, max_size_mb=1)
        self.assertFalse(zero.available)
        key = make_cache_key("x", ["bing"], "normal", 5)
        zero.set(key, "x", ["bing"], "normal", [{"title": "T"}])
        self.assertIsNone(zero.get(key))

    def test_history_recorded(self):
        self.cache.add_history("查询词", ["bing"], "normal", 3, 1.2)
        rows = self.cache.get_history(10)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["query"], "查询词")

    def test_clear_cache_keeps_history(self):
        """
        清缓存与清历史相互独立

        回归用例：VACUUM 曾被写在事务内，导致 clear() 整体回滚，
        返回 False 且缓存实际未被清除。
        """
        key = make_cache_key("a", ["bing"], "normal", 5)
        self.cache.set(key, "a", ["bing"], "normal", [{"title": "T"}])
        self.cache.add_history("a", ["bing"], "normal", 1, 0.5)
        self.assertTrue(self.cache.clear(), "clear() 应返回 True")
        self.assertIsNone(self.cache.get(key))
        self.assertEqual(len(self.cache.get_history(10)), 1)

    def test_lru_eviction_enforces_size_limit(self):
        """
        容量超限时按最近最少访问淘汰

        回归用例：淘汰语句中的 VACUUM 同样处于事务内，
        曾导致整个淘汰被回滚、缓存无限增长。
        """
        db = os.path.join(tempfile.mkdtemp(), "lru.db")
        cache = SearchCache(db_path=db, ttl=3600, max_size_mb=1)
        blob = "x" * 3000
        for i in range(400):
            key = make_cache_key(f"q{i}", ["bing"], "normal", 10)
            cache.set(key, f"q{i}", ["bing"], "normal",
                      [{"title": blob, "url": f"https://a.com/{i}",
                        "snippet": blob, "engine": "bing"}])
        self.assertLess(cache.stats().entries, 400, "应触发淘汰")
        self.assertLess(os.path.getsize(db) / (1024 * 1024), 3,
                        "占用不应远超上限")
        cache.close()

    def test_disabled_cache_degrades_silently(self):
        c = SearchCache(db_path=self.db, enabled=False)
        self.assertFalse(c.available)
        self.assertIsNone(c.get("anykey"))

    def test_unwritable_path_degrades_silently(self):
        """路径不可用时不得抛异常影响搜索"""
        bad = os.path.join(tempfile.gettempdir(), "bad\0dir", "c.db")
        c = SearchCache(db_path=bad)
        self.assertIsNone(c.get("k"))


# ============================================================
# SimHash 与排序（F1-5 / F1-6）
# ============================================================

class TestSimHash(unittest.TestCase):
    """标准 SimHash 实现"""

    def test_identical_text_distance_zero(self):
        text = "Python 异步编程入门教程"
        self.assertEqual(
            hamming_distance(compute_simhash(text), compute_simhash(text)), 0
        )

    def test_similar_text_small_distance(self):
        a = compute_simhash("Python 异步编程入门教程 asyncio 详解")
        b = compute_simhash("Python 异步编程入门教程 asyncio 讲解")
        self.assertLess(hamming_distance(a, b), 20)

    def test_unrelated_text_large_distance(self):
        a = compute_simhash("Python 异步编程入门教程")
        b = compute_simhash("红烧肉的家常做法与调味技巧")
        self.assertGreater(hamming_distance(a, b), 10)

    def test_empty_text(self):
        self.assertIsInstance(compute_simhash(""), int)


class TestRanking(unittest.TestCase):
    """多因子加权排序"""

    def _mk(self, title, url, engine, rank=1):
        return SearchResult(title=title, url=url, snippet="", engine=engine, rank=rank)

    def test_dedup_same_url(self):
        results = [
            self._mk("A", "https://a.com/p", "baidu"),
            self._mk("A", "https://a.com/p", "bing"),
        ]
        self.assertEqual(len(deduplicate(results)), 1)

    def test_consensus_ranks_higher(self):
        """被多引擎收录的结果应排在前面"""
        results = [
            self._mk("Only", "https://only.com", "baidu", rank=1),
            self._mk("Both", "https://both.com", "baidu", rank=3),
            self._mk("Both", "https://both.com", "bing", rank=3),
        ]
        ranked = rank_results(deduplicate(results), query="")
        self.assertEqual(ranked[0].url, "https://both.com")

    def test_dedup_preserves_engine_sources(self):
        """
        去重必须把被丢弃条目的引擎来源合并进保留条目

        若不合并，排序阶段每个 URL 只剩一条记录，
        共识度恒为最小值，多引擎交叉验证会完全失效。
        """
        results = [
            self._mk("A", "https://a.com/p", "baidu", rank=5),
            self._mk("A", "https://a.com/p", "bing", rank=2),
        ]
        uniq = deduplicate(results)
        self.assertEqual(len(uniq), 1)
        self.assertEqual(set(uniq[0].engine_set), {"baidu", "bing"})

    def test_dedup_keeps_best_rank(self):
        """同一页面在不同引擎排名不同时，应保留最优位次"""
        results = [
            self._mk("A", "https://a.com/p", "baidu", rank=7),
            self._mk("A", "https://a.com/p", "bing", rank=2),
        ]
        self.assertEqual(deduplicate(results)[0].rank, 2)

    def test_total_engines_affects_consensus(self):
        """
        共识度分母应取实际发起搜索的引擎数

        某引擎全军覆没时，若分母由结果反推会偏小，
        使剩余结果的共识度虚高。
        """
        results = deduplicate([
            self._mk("A", "https://a.com", "baidu", rank=1),
            self._mk("A2", "https://a2.com", "bing", rank=1),
        ])
        # rank_results 会把得分写回条目对象，两次调用作用于同一批实例，
        # 必须立即取值，否则后一次结果会覆盖前一次
        high = rank_results(results, query="", total_engines=2)[0].score
        low = rank_results(results, query="", total_engines=4)[0].score
        self.assertGreater(high, low)

    def test_redirect_merges_with_direct_link(self):
        """
        跳转中转地址应与同标题直链合并

        百度等引擎返回 link?url= 形式的中转地址，
        与其他引擎的直链 URL 不同却指向同一页面，
        不合并会导致同一结果重复占据两个位次。
        """
        items = [
            self._mk("同一篇文档", "https://docs.python.org/3/library/asyncio.html", "bing", rank=4),
            self._mk("同一篇文档", "http://www.baidu.com/link?url=abcdef", "baidu", rank=1),
        ]
        out = deduplicate(items)
        self.assertEqual(len(out), 1)
        # 代表条目应为直链而非跳转地址
        self.assertTrue(out[0].url.startswith("https://docs.python.org"))
        self.assertEqual(set(out[0].engine_set), {"bing", "baidu"})

    def test_redirect_merge_is_order_independent(self):
        """跳转链先出现时也应正确合并，结果不受引擎返回顺序影响"""
        items = [
            self._mk("同一篇文档", "http://www.baidu.com/link?url=abcdef", "baidu", rank=1),
            self._mk("同一篇文档", "https://docs.python.org/3/library/asyncio.html", "bing", rank=4),
        ]
        out = deduplicate(items)
        self.assertEqual(len(out), 1)
        self.assertTrue(out[0].url.startswith("https://docs.python.org"))

    def test_redirect_merge_tolerates_title_variants(self):
        """
        标题存在标点差异或截断时仍应合并

        实测中百度返回半角冒号并追加截断尾巴，
        必应返回全角冒号的完整标题，两者指向同一篇文章。
        """
        items = [
            self._mk("从搜索引擎到推荐算法:SimHash的原理、优化与实践_simhash算法...",
                     "http://www.baidu.com/link?url=m9hx", "baidu", rank=1),
            self._mk("从搜索引擎到推荐算法：SimHash的原理、优化与实践",
                     "https://blog.csdn.net/x/article/details/149391540", "bing", rank=4),
        ]
        out = deduplicate(items)
        self.assertEqual(len(out), 1)
        self.assertEqual(set(out[0].engine_set), {"baidu", "bing"})

    def test_short_titles_not_prefix_merged(self):
        """短通用标题不得因前缀相同被误合并"""
        items = [
            self._mk("Python 教程", "http://www.baidu.com/link?url=aa", "baidu", rank=1),
            self._mk("Python 教程进阶", "https://x.com/y", "bing", rank=1),
        ]
        self.assertEqual(len(deduplicate(items)), 2)

    def test_different_titles_not_merged(self):
        """
        内容不同的跳转链接不得被误合并

        标题需具备真实结果的长度，极短标题（如三字）在 SimHash 下
        特征过少、汉明距离趋近于 0，属于短文本固有局限而非缺陷。
        """
        items = [
            self._mk("Python 异步编程完全指南",
                     "http://www.baidu.com/link?url=aaa", "baidu", rank=1),
            self._mk("Java 并发编程实战教程",
                     "http://www.baidu.com/link?url=bbb", "baidu", rank=2),
        ]
        self.assertEqual(len(deduplicate(items)), 2)

    def test_result_dict_roundtrip_keeps_engines(self):
        """缓存往返不得丢失引擎来源，否则命中缓存后排序依据会退化"""
        r = self._mk("A", "https://a.com", "baidu", rank=1)
        r.engines = ["baidu", "bing"]
        restored = SearchResult.from_dict(r.to_dict())
        self.assertEqual(set(restored.engine_set), {"baidu", "bing"})

    def test_weights_from_config(self):
        w = weights_from_config({"ranking": {"consensus": 9.0}})
        self.assertEqual(w.consensus, 9.0)
        self.assertEqual(w.relevance, RankWeights().relevance)

    def test_weights_reject_invalid(self):
        w = weights_from_config({"ranking": {"consensus": "abc", "position": -5}})
        self.assertEqual(w.consensus, RankWeights().consensus)
        self.assertEqual(w.position, RankWeights().position)

    def test_redirect_url_downweighted(self):
        """跳转链接会破坏去重与域名评分，应降权"""
        self.assertLess(domain_score("http://www.baidu.com/link?url=abc"), 0)

    def test_high_quality_domain_scored_up(self):
        self.assertGreater(domain_score("https://github.com/python/cpython"), 0)

    def test_domain_of(self):
        self.assertEqual(domain_of("https://www.example.com/a/b"), "example.com")


# ============================================================
# 统一 HTTP 出口（P0-8 / F1-3 / F1-4）
# ============================================================

class TestHttpClient(unittest.TestCase):
    """UA 池与重试策略"""

    def test_ua_pool_size(self):
        self.assertGreaterEqual(len(USER_AGENT_POOL), 5)

    def test_ua_pool_all_realistic(self):
        for ua in USER_AGENT_POOL:
            self.assertTrue(ua.startswith("Mozilla/5.0"))

    def test_pick_ua_returns_from_pool(self):
        self.assertIn(pick_user_agent(), USER_AGENT_POOL)

    def test_retry_policy_defaults(self):
        p = RetryPolicy()
        self.assertGreaterEqual(p.max_retries, 1)
        self.assertGreater(p.max_delay, p.base_delay)

    def test_privacy_context_includes_ua(self):
        pm = PrivacyManager({"privacy": {"default_mode": "strict"}})
        pm.set_mode_silent("strict")
        ctx = pm.build_request_context()
        self.assertIn("User-Agent", ctx.headers)

    def test_custom_ua_overrides_pool(self):
        pm = PrivacyManager({
            "privacy": {"default_mode": "strict",
                        "strict": {"user_agent": "MyCustomUA/1.0"}}
        })
        pm.set_mode_silent("strict")
        ctx = pm.build_request_context()
        self.assertEqual(ctx.headers.get("User-Agent"), "MyCustomUA/1.0")

    def test_proxy_passed_to_context(self):
        pm = PrivacyManager({
            "privacy": {"default_mode": "strict",
                        "strict": {"proxy": "http://127.0.0.1:7890"}}
        })
        pm.set_mode_silent("strict")
        ctx = pm.build_request_context()
        self.assertEqual(ctx.proxy, "http://127.0.0.1:7890")

    def test_mode_key_alias_accepted(self):
        """
        误写 privacy.mode 也应识别为严格模式

        只认 default_mode 时，用户写 mode: strict 会静默落回 normal，
        自以为已开启严格模式，查询词却照常发往国内引擎。
        """
        pm = PrivacyManager({"privacy": {"mode": "strict"}})
        self.assertEqual(pm.get_mode(), "strict")
        self.assertNotIn("baidu", pm.get_allowed_engines())

    def test_mode_value_normalized(self):
        """模式值应容忍大小写与首尾空格"""
        for raw in ("STRICT", " strict ", "Strict"):
            pm = PrivacyManager({"privacy": {"default_mode": raw}})
            self.assertEqual(pm.get_mode(), "strict", f"未能识别 {raw!r}")

    def test_invalid_mode_warns_not_silent(self):
        """无法识别的模式值必须给出告警，不得静默处理"""
        pm = PrivacyManager({"privacy": {"default_mode": "ultra"}})
        self.assertEqual(pm.get_mode(), "normal")
        self.assertTrue(pm.config_warnings, "非法模式值应产生配置告警")

    def test_strict_whitelist_excludes_domestic_engines(self):
        """strict 白名单不得包含隐私保护不足的国内引擎"""
        pm = PrivacyManager({"privacy": {"default_mode": "strict"}})
        allowed = set(pm.get_allowed_engines())
        for engine in ("baidu", "bing", "sogou", "360"):
            self.assertNotIn(engine, allowed)


# ============================================================
# 解析健壮性（F1-2）
# ============================================================

class TestSelectors(unittest.TestCase):
    """多套备选选择器与跳转链接识别"""

    def test_every_engine_has_selectors(self):
        for name in all_engine_names():
            if name == "searxng":
                continue  # SearXNG 走 JSON，无需选择器
            self.assertIn(name, SELECTORS, f"{name} 缺少选择器配置")

    def test_html_engines_have_multiple_variants(self):
        """至少两套选择器，用于应对引擎改版"""
        for name, cfg in SELECTORS.items():
            self.assertGreaterEqual(
                len(cfg.variants), 2, f"{name} 应配置多套备选选择器"
            )

    def test_redirect_detection(self):
        self.assertTrue(is_redirect_url("http://www.baidu.com/link?url=abc"))
        self.assertFalse(is_redirect_url("https://github.com/python"))

    def test_redirect_patterns_not_empty(self):
        self.assertGreater(len(REDIRECT_PATTERNS), 0)

    def test_get_selectors_unknown_engine(self):
        self.assertIsNone(get_selectors("nonexistent_engine"))


class TestPartialDiagnosis(unittest.TestCase):
    """
    有结果不等于正常

    引擎限流时可能只吐出一两条并夹带验证页特征，
    若一律判为 OK，用户要 10 条只拿到 1 条却得不到解释。
    """

    def test_blocked_page_detected_with_results(self):
        """带拦截特征的页面即便有结果也须判为 BLOCKED"""
        from engine_selectors import diagnose_partial, ParseDiagnosis
        html = "<html>百度安全验证 请输入验证码</html>"
        self.assertEqual(
            diagnose_partial("baidu", html, got=2, expected=10),
            ParseDiagnosis.BLOCKED)

    def test_too_few_results_flagged_partial(self):
        from engine_selectors import diagnose_partial, ParseDiagnosis
        html = "<html>" + "正常内容" * 800 + "</html>"
        self.assertEqual(
            diagnose_partial("baidu", html, got=1, expected=10),
            ParseDiagnosis.PARTIAL)

    def test_reasonable_count_is_ok(self):
        """未达满额但在合理范围内不应误报"""
        from engine_selectors import diagnose_partial, ParseDiagnosis
        html = "<html>" + "正常内容" * 800 + "</html>"
        for got in (4, 7, 10):
            self.assertEqual(
                diagnose_partial("baidu", html, got=got, expected=10),
                ParseDiagnosis.OK, "got=%d 不应判为异常" % got)

    def test_single_result_request_not_flagged(self):
        """只要 1 条时拿到 1 条是正常的，不得误报"""
        from engine_selectors import diagnose_partial, ParseDiagnosis
        html = "<html>" + "正常内容" * 800 + "</html>"
        self.assertEqual(
            diagnose_partial("baidu", html, got=1, expected=1),
            ParseDiagnosis.OK)

    def test_partial_hint_is_actionable(self):
        """提示须说明可采取的动作，而非仅陈述现象"""
        from engine_selectors import diagnosis_hint, ParseDiagnosis
        hint = diagnosis_hint(ParseDiagnosis.PARTIAL)
        self.assertTrue(hint)
        self.assertTrue(
            any(k in hint for k in ("重试", "其他引擎")),
            "偏少提示应给出可执行建议：%r" % hint)

    def test_is_blocked_page_tolerates_unknown_engine(self):
        from engine_selectors import is_blocked_page
        self.assertFalse(is_blocked_page("nonexistent", "任意内容"))
        self.assertFalse(is_blocked_page("baidu", ""))


class TestLowRelevanceWarning(unittest.TestCase):
    """
    整体跑题的兜底响应须提示用户

    搜索引擎对无 cookie 的裸请求可能返回泛化的缓存页：
    查「python 装饰器 原理」却回一堆 Python 官网下载页。
    状态码正常、条数充足，仅凭 HTTP 层无从察觉。
    """

    def _make(self, engine, titles):
        return [SearchResult(title=t, url="https://e.com/%d" % i,
                             snippet="", engine=engine, rank=i)
                for i, t in enumerate(titles, 1)]

    def _orch(self):
        o = SearchOrchestrator({})
        o._notices = []
        return o

    def test_generic_fallback_page_warns(self):
        o = self._orch()
        o._warn_low_relevance("python 装饰器 原理", self._make("bing", [
            "Welcome to Python.org",
            "Download Python | Python.org",
            "欢迎来到Python.org - Python编程语言",
            "Python基础教程 | 菜鸟教程",
        ]))
        self.assertTrue(o.notices, "整体跑题未产生提示")
        self.assertIn("bing", o.notices[0])

    def test_relevant_results_stay_silent(self):
        """结果正常时不得打扰用户"""
        o = self._orch()
        o._warn_low_relevance("docker 容器 网络配置", self._make("bing", [
            "Docker 容器网络配置全攻略：桥接、Host",
            "docker网络配置：bridge模式、host模式",
            "Docker容器网络配置一网打尽",
        ]))
        self.assertFalse(o.notices, "正常结果不应告警：%s" % o.notices)

    def test_one_relevant_hit_prevents_warning(self):
        """
        只要有一条命中就不算整体跑题

        判据取最大值而非平均值：搜索结果本就良莠不齐，
        用平均值会在正常场景下频繁误报。
        """
        o = self._orch()
        o._warn_low_relevance("机器学习 入门教程", self._make("baidu", [
            "机器（由各种金属和非金属部件组装成的装置）_百度百科",
            "机器学习简介 - 菜鸟教程",
            "machine是什么意思_machine的翻译",
        ]))
        self.assertFalse(o.notices, "存在相关结果时不应告警：%s" % o.notices)

    def test_too_few_samples_skipped(self):
        """样本过少时波动大，不做判定"""
        o = self._orch()
        o._warn_low_relevance("python 装饰器 原理",
                              self._make("bing", ["Welcome to Python.org"]))
        self.assertFalse(o.notices)

    def test_warning_is_per_engine(self):
        """只提示出问题的引擎，不牵连正常引擎"""
        o = self._orch()
        results = self._make("bing", [
            "Welcome to Python.org", "Download Python", "Python.org 首页",
        ]) + self._make("baidu", [
            "Python装饰器原理和用法", "深入理解Python装饰器原理",
            "Python装饰器实现原理详解",
        ])
        o._warn_low_relevance("python 装饰器 原理", results)
        self.assertEqual(len(o.notices), 1)
        self.assertIn("bing", o.notices[0])
        self.assertNotIn("baidu", o.notices[0])

    def test_empty_results_no_crash(self):
        o = self._orch()
        o._warn_low_relevance("任意查询", [])
        self.assertFalse(o.notices)


class TestNoBytecodePollution(unittest.TestCase):
    """
    运行测试不得在仓库留下字节码（死规则 13）

    仅靠各文件顶部的 sys.dont_write_bytecode 不足以覆盖：
    unittest discover 用 importlib 加载模块，字节码在模块代码执行前
    就已写盘，按字母序最先加载的模块必然留下一个 .pyc。
    """

    def test_all_python_files_disable_bytecode(self):
        root = os.path.join(os.path.dirname(__file__), "..")
        missing = []
        for sub in ("scripts", "tests"):
            d = os.path.join(root, sub)
            for fn in sorted(os.listdir(d)):
                if not fn.endswith(".py"):
                    continue
                with open(os.path.join(d, fn), encoding="utf-8") as f:
                    if "dont_write_bytecode" not in f.read():
                        missing.append("%s/%s" % (sub, fn))
        self.assertFalse(
            missing, "以下文件缺少 dont_write_bytecode 设置：%s" % missing)

    def test_tests_package_purges_bytecode(self):
        """测试包须具备清理能力，而非仅设置开关"""
        init_py = os.path.join(os.path.dirname(__file__), "__init__.py")
        with open(init_py, encoding="utf-8") as f:
            content = f.read()
        self.assertIn("__pycache__", content,
                      "测试包应主动清理字节码目录")
        self.assertIn("atexit", content,
                      "应在退出时再清一次，覆盖设置生效前写入的字节码")


# ============================================================
# 运行日志
# ============================================================

class TestLogging(unittest.TestCase):
    """日志配置必须真正生效，且不泄露查询词"""

    def setUp(self):
        self.path = os.path.join(tempfile.mkdtemp(), "test.log")

    def test_info_does_not_leak_query(self):
        logger = SearchLogger(path=self.path, level="INFO")
        logger.log_search("我的敏感搜索词", ["bing"], "normal", 3, 1.0, cache_hit=False)
        with open(self.path, encoding="utf-8") as f:
            content = f.read()
        self.assertNotIn("我的敏感搜索词", content)
        self.assertIn("query_len=", content)

    def test_debug_records_query(self):
        logger = SearchLogger(path=self.path, level="DEBUG")
        logger.log_search("调试查询", ["bing"], "normal", 1, 0.5, cache_hit=False)
        with open(self.path, encoding="utf-8") as f:
            self.assertIn("调试查询", f.read())

    def test_off_level_writes_nothing(self):
        logger = SearchLogger(path=self.path, level="OFF")
        logger.info("should not appear")
        self.assertFalse(os.path.exists(self.path))

    def test_cache_hit_marked(self):
        logger = SearchLogger(path=self.path, level="INFO")
        logger.log_search("q", ["bing"], "normal", 2, 0.1, cache_hit=True)
        with open(self.path, encoding="utf-8") as f:
            self.assertIn("source=cache", f.read())

    def test_unwritable_path_degrades_silently(self):
        """
        路径不可用时静默降级，绝不影响搜索

        用非法字符构造跨平台都无法创建的路径。
        注意不能用 /nonexistent/... ：Windows 下会被解析为当前盘符的
        相对根路径并创建成功，反而在磁盘上留下垃圾目录。
        """
        bad = os.path.join(tempfile.gettempdir(), "bad\0dir", "x.log")
        logger = SearchLogger(path=bad)
        logger.info("no crash")   # 不应抛异常
        self.assertFalse(logger.enabled)

    def test_build_from_config(self):
        logger = build_logger_from_config({"logging": {"level": "WARNING", "file": self.path}})
        self.assertEqual(logger.level_name, "WARNING")

    def test_invalid_level_falls_back(self):
        logger = build_logger_from_config({"logging": {"level": "NOPE", "file": self.path}})
        self.assertEqual(logger.level_name, "INFO")


# ============================================================
# 配置消费（P0-4 / P0-5）
# ============================================================

class TestConfigConsumption(unittest.TestCase):
    """配置项必须真正生效，不能只写在文档里"""

    def test_num_results_from_config(self):
        import inspect
        src = inspect.getsource(SearchOrchestrator.search)
        self.assertIn('num_results', src)

    def test_searxng_disabled_removes_engine(self):
        orch = SearchOrchestrator({
            "search": {"default_engines": ["baidu", "searxng"]},
            "searxng": {"enabled": False},
        })
        self.assertNotIn("searxng", orch.resolve_engines(None, "normal"))

    def test_searxng_enabled_keeps_engine(self):
        orch = SearchOrchestrator({
            "search": {"default_engines": ["baidu", "searxng"]},
            "searxng": {"enabled": True},
        })
        self.assertIn("searxng", orch.resolve_engines(None, "normal"))

    def test_ranking_weights_injected(self):
        orch = SearchOrchestrator({"ranking": {"consensus": 8.8}})
        self.assertEqual(orch.rank_weights.consensus, 8.8)

    def test_logger_built_from_config(self):
        orch = SearchOrchestrator({"logging": {"level": "ERROR"}})
        self.assertEqual(orch.logger.level_name, "ERROR")


# ============================================================
# 隐私优先策略
# ============================================================

class TestPrivacyFirstPolicy(unittest.TestCase):
    """strict 模式的隐私承诺不得被绕过"""

    def _orch(self):
        return SearchOrchestrator({
            "search": {"default_engines": ["baidu", "bing"]},
            "searxng": {"enabled": False},
            "privacy": {"default_mode": "strict"},
        })

    def test_strict_rejects_low_privacy_engine(self):
        """显式指定百度也应被拒绝，否则隐私报告与实际行为矛盾"""
        orch = self._orch()
        orch.privacy_manager.set_mode_silent("strict")
        selected = orch.resolve_engines(["baidu"], "strict")
        self.assertNotIn("baidu", selected)
        self.assertTrue(any("拒绝" in n for n in orch.notices))

    def test_strict_falls_back_to_privacy_engines(self):
        orch = self._orch()
        orch.privacy_manager.set_mode_silent("strict")
        selected = orch.resolve_engines(["baidu"], "strict")
        for name in selected:
            self.assertIn(name, strict_fallback_engines() + ["searxng"])

    def test_normal_mode_allows_any_engine(self):
        orch = self._orch()
        self.assertIn("baidu", orch.resolve_engines(["baidu"], "normal"))

    def test_fallback_disabled_by_default(self):
        """默认不降级，避免查询词意外外泄"""
        self.assertFalse(self._orch().allow_fallback)


if __name__ == "__main__":
    unittest.main(verbosity=2)
