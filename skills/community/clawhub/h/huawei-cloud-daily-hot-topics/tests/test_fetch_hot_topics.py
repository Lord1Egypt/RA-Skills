"""Unit tests for the daily hot-topics fetcher (offline; HTTP is mocked)."""
import importlib.util
import io
import json
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

SKILL_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = SKILL_DIR / "scripts"
SCRIPT = SCRIPTS_DIR / "fetch_hot_topics.py"

_spec = importlib.util.spec_from_file_location("fetch_hot_topics", SCRIPT)
fht = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(fht)


WEIBO_PAYLOAD = json.dumps(
    {
        "code": 200,
        "message": "获取成功",
        "data": [
            {"title": "话题甲", "hot_value": 1081263, "link": "https://s.weibo.com/weibo?q=甲"},
            {"title": "话题乙", "hot_value": 976412, "link": "https://s.weibo.com/weibo?q=乙"},
            {"title": "话题丙", "hot_value": 842105, "link": ""},
        ],
    },
    ensure_ascii=False,
)

DOUYIN_PAYLOAD = json.dumps(
    {
        "code": 200,
        "data": [
            {"title": "抖音话题一", "hot_value": 12085939, "cover": "https://example.com/a.jpg"},
            {"title": "抖音话题二", "hot_value": 9331021, "cover": "https://example.com/b.jpg"},
        ],
    },
    ensure_ascii=False,
)

ALT_PAYLOAD = json.dumps(
    {"data": [{"name": "备用话题", "hot": "12.3万", "url": "https://example.com/alt"}]},
    ensure_ascii=False,
)


class NormalizeTests(unittest.TestCase):
    def test_weibo_records_normalised_with_rank(self):
        records = fht._extract_records(json.loads(WEIBO_PAYLOAD))
        items = fht.normalize(records, "微博热搜")
        self.assertEqual(len(items), 3)
        self.assertEqual(items[0]["rank"], 1)
        self.assertEqual(items[0]["title"], "话题甲")
        self.assertEqual(items[0]["hot"], 1081263)
        self.assertEqual(items[0]["source"], "微博热搜")
        self.assertEqual(items[0]["url"], "https://s.weibo.com/weibo?q=甲")

    def test_alt_envelope_name_and_string_hot(self):
        records = fht._extract_records(json.loads(ALT_PAYLOAD))
        items = fht.normalize(records, "综合热榜")
        self.assertEqual(items[0]["title"], "备用话题")
        self.assertEqual(items[0]["hot"], "12.3万")

    def test_records_without_title_are_skipped(self):
        items = fht.normalize([{"hot_value": 1}, {"title": "ok", "hot_value": 2}], "s")
        self.assertEqual([i["title"] for i in items], ["ok"])
        self.assertEqual(items[0]["rank"], 1)

    def test_coerce_hot(self):
        self.assertEqual(fht._coerce_hot("1,234"), 1234)
        self.assertEqual(fht._coerce_hot(50), 50)
        self.assertEqual(fht._coerce_hot(None), None)


class FetchSourceTests(unittest.TestCase):
    def test_fetch_source_parses_payload(self):
        with mock.patch.object(fht, "_http_get", return_value=WEIBO_PAYLOAD):
            items = fht.fetch_source("weibo", timeout=1, retries=0)
        self.assertEqual(len(items), 3)
        self.assertEqual(items[1]["title"], "话题乙")

    def test_fetch_source_retries_then_succeeds(self):
        calls = {"n": 0}

        def flaky(url, timeout):
            calls["n"] += 1
            if calls["n"] == 1:
                raise OSError("temporary")
            return WEIBO_PAYLOAD

        with mock.patch.object(fht, "_http_get", side_effect=flaky):
            items = fht.fetch_source("weibo", timeout=1, retries=2)
        self.assertEqual(calls["n"], 2)
        self.assertEqual(len(items), 3)

    def test_fetch_source_rejects_bad_code(self):
        with mock.patch.object(fht, "_http_get", return_value=json.dumps({"code": 500, "data": []})):
            with self.assertRaises(RuntimeError):
                fht.fetch_source("weibo", timeout=1, retries=0)

    def test_fetch_source_unknown_name(self):
        with self.assertRaises(ValueError):
            fht.fetch_source("nope")


class DegradationTests(unittest.TestCase):
    def test_chain_degrades_to_second_provider(self):
        def by_url(url, timeout):
            if "weibo" in url:
                raise OSError("weibo down")
            return DOUYIN_PAYLOAD

        with mock.patch.object(fht, "_http_get", side_effect=by_url):
            result = fht.fetch(chain=["weibo", "douyin"], timeout=1, retries=0)
        self.assertFalse(result["is_sample"])
        self.assertEqual(result["source"], "douyin")
        self.assertEqual(result["source_label"], "抖音热点")
        self.assertTrue(result["warnings"])
        self.assertEqual(len(result["items"]), 2)

    def test_all_providers_fail_falls_back_to_sample(self):
        with mock.patch.object(fht, "_http_get", side_effect=OSError("offline")):
            result = fht.fetch(chain=["weibo", "zhihu", "douyin"], timeout=1, retries=0)
        self.assertTrue(result["is_sample"])
        self.assertEqual(result["source"], "sample")
        self.assertEqual(result["source_label"], "示例数据")
        self.assertTrue(result["items"])
        self.assertTrue(any("示例数据" in w for w in result["warnings"]))

    def test_offline_shortcut_uses_sample(self):
        result = fht.fetch(chain=["weibo"], offline=True)
        self.assertTrue(result["is_sample"])
        self.assertGreaterEqual(len(result["items"]), 1)


class ChainTests(unittest.TestCase):
    def test_auto_returns_default_chain(self):
        self.assertEqual(fht.resolve_chain("auto"), list(fht.DEFAULT_SOURCE_CHAIN))

    def test_explicit_source_is_prepended(self):
        chain = fht.resolve_chain("douyin")
        self.assertEqual(chain[0], "douyin")
        self.assertIn("weibo", chain)
        self.assertEqual(len(chain), len(set(chain)))

    def test_unknown_source_raises(self):
        with self.assertRaises(ValueError):
            fht.resolve_chain("not-a-source")


class RenderTests(unittest.TestCase):
    def setUp(self):
        with mock.patch.object(fht, "_http_get", return_value=WEIBO_PAYLOAD):
            self.result = fht.fetch(chain=["weibo"], timeout=1, retries=0)

    def test_render_markdown_has_header_and_rows(self):
        text = fht.render_markdown(self.result, top=3)
        self.assertIn("# 今日热点榜单", text)
        self.assertIn("| 排名 | 标题 | 热度 | 来源 |", text)
        self.assertIn("话题甲", text)
        self.assertIn("微博热搜", text)

    def test_render_markdown_marks_sample(self):
        sample = fht.load_sample()
        sample["is_sample"] = True
        text = fht.render_markdown(sample, top=2)
        self.assertIn("示例数据", text)

    def test_render_text_aligned(self):
        text = fht.render_text(self.result, top=2)
        self.assertIn("今日热点榜单", text)
        self.assertIn("话题甲", text)

    def test_render_json_parseable_and_limited(self):
        text = fht.render_json(self.result, top=2)
        payload = json.loads(text)
        self.assertEqual(len(payload["items"]), 2)
        self.assertEqual(payload["items"][0]["title"], "话题甲")

    def test_top_clamps_to_available(self):
        text = fht.render_json(self.result, top=99)
        self.assertEqual(len(json.loads(text)["items"]), 3)


class MainTests(unittest.TestCase):
    def _run(self, argv, http_return=WEIBO_PAYLOAD):
        buf = io.StringIO()
        with mock.patch.object(fht, "_http_get", return_value=http_return):
            with redirect_stdout(buf):
                rc = fht.main(argv)
        return rc, buf.getvalue()

    def test_main_json_top_constraint(self):
        rc, out = self._run(["--top", "2", "--format", "json"])
        self.assertEqual(rc, 0)
        payload = json.loads(out)
        self.assertEqual(len(payload["items"]), 2)

    def test_main_default_markdown(self):
        rc, out = self._run([])
        self.assertEqual(rc, 0)
        self.assertIn("# 今日热点榜单", out)

    def test_main_offline_returns_sample(self):
        rc, out = self._run(["--offline", "--format", "json"])
        self.assertEqual(rc, 0)
        payload = json.loads(out)
        self.assertTrue(payload["is_sample"])

    def test_main_rejects_zero_top(self):
        rc, _ = self._run(["--top", "0"])
        self.assertEqual(rc, 2)

    def test_main_rejects_unknown_source(self):
        rc, _ = self._run(["--source", "nope"])
        self.assertEqual(rc, 2)

    def test_main_list_sources(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = fht.main(["--list-sources"])
        self.assertEqual(rc, 0)
        self.assertIn("weibo", buf.getvalue())

    def test_main_writes_output_file(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "hot.json"
            with mock.patch.object(fht, "_http_get", return_value=WEIBO_PAYLOAD):
                with redirect_stdout(io.StringIO()):
                    rc = fht.main(["--format", "json", "--output", str(path)])
            self.assertEqual(rc, 0)
            self.assertEqual(len(json.loads(path.read_text(encoding="utf-8"))["items"]), 3)


if __name__ == "__main__":
    unittest.main()