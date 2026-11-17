"""Offline synthetic fixtures; no network or publishing in tests."""
import importlib.util
from pathlib import Path
import unittest
from datetime import datetime, date
import pandas as pd

spec = importlib.util.spec_from_file_location("radar", Path(__file__).parents[1] / "scripts/sentiment_analyzer.py")
r = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r)
NOW = datetime(2026, 9, 5, 10, tzinfo=r.TZ)
CAL = ["2026-09-03", "2026-09-04", "2026-09-07"]


class API:
    def tool_trade_date_hist_sina(self):
        return pd.DataFrame({"trade_date": CAL})

    def index_zh_a_hist(self, **kwargs):
        assert kwargs["symbol"] in r.INDICES
        assert kwargs["end_date"] == "20260904"
        return pd.DataFrame({"日期": CAL[:2], "收盘": [100.0, 101.0]})

    def stock_zh_index_daily(self, **kwargs):
        return self.index_zh_a_hist(symbol="000001", end_date="20260904").rename(columns={"日期":"date", "收盘":"close"})


class Tests(unittest.TestCase):
    def test_all_sources_fail(self):
        class Broken(API):
            def index_zh_a_hist(self, **kw): raise RuntimeError()
            def stock_zh_index_daily(self, **kw): raise RuntimeError()
        out = r.collect(Broken(), now=NOW)
        self.assertEqual(out["status"], "unavailable")
        self.assertEqual(out["indices"], [])
        self.assertIsNone(out["score"])
        self.assertEqual(len(out["errors"]), 3)

    def test_calendar_failure(self):
        class Broken(API):
            def tool_trade_date_hist_sina(self): raise RuntimeError()
        self.assertEqual(r.collect(Broken(), now=NOW)["indices"], [])

    def test_success_is_partial_not_full_sentiment(self):
        out = r.collect(API(), now=NOW)
        self.assertEqual(out["trade_date"], "2026-09-04")
        self.assertEqual(out["indices"][0]["change_pct"], 1.0)
        self.assertEqual(out["status"], "partial")
        self.assertIsNone(out["confidence"])
        self.assertIsNone(out["position_suggestion"])

    def test_fallback(self):
        class Fallback(API):
            def index_zh_a_hist(self, **kw): raise RuntimeError()
            def stock_zh_index_daily(self, **kw):
                return pd.DataFrame({"date":CAL[:2], "close":[100, 100]})
        out = r.collect(Fallback(), now=NOW)
        self.assertEqual(out["indices"][0]["change_pct"], 0)
        self.assertIn("新浪", out["indices"][0]["source"])

    def test_eastmoney_fallback(self):
        class Fallback(API):
            def stock_zh_index_daily(self, **kw): raise RuntimeError()
        out = r.collect(Fallback(), now=NOW)
        self.assertEqual(out["indices"][0]["change_pct"], 1.0)
        self.assertIn("东方财富", out["indices"][0]["source"])

    def test_weekend_explicit_is_rejected(self):
        self.assertEqual(r.collect(API(), "2026-09-05", NOW)["indices"], [])

    def test_future_rejected(self):
        self.assertEqual(r.collect(API(), "2026-09-07", NOW)["indices"], [])

    def test_premarket_uses_previous_completed(self):
        now = datetime(2026,9,7,8,30,tzinfo=r.TZ)
        self.assertEqual(r.select_day(CAL, None, now), date(2026,9,4))

    def test_holiday_not_weekday_guess(self):
        self.assertEqual(r.select_day(["2026-09-30","2026-10-09"], None,
                         datetime(2026,10,5,10,tzinfo=r.TZ)), date(2026,9,30))

    def test_stale_calendar(self):
        with self.assertRaises(ValueError): r.select_day(CAL[:2], None, NOW)

    def test_stale_quote_rejected(self):
        with self.assertRaises(ValueError):
            r.observation([{"date":"2026-09-03","close":100}], "000001", date(2026,9,4), "test")

    def test_invalid_numbers(self):
        for bad in [float("nan"), float("inf"), None, -1, 0, True]:
            with self.assertRaises((ValueError, TypeError)):
                r.observation([{"date":CAL[0],"close":100},{"date":CAL[1],"close":bad}],
                              "000001", date(2026,9,4), "test")

    def test_empty_source(self):
        class Empty(API):
            def index_zh_a_hist(self, **kw): return pd.DataFrame()
            def stock_zh_index_daily(self, **kw): return pd.DataFrame()
        self.assertEqual(r.collect(Empty(), now=NOW)["indices"], [])

    def test_missing_previous_day(self):
        class Gap(API):
            def index_zh_a_hist(self, **kw):
                return pd.DataFrame({"日期":["2026-09-02", "2026-09-04"], "收盘":[100,101]})
            def stock_zh_index_daily(self, **kw): raise RuntimeError()
        self.assertEqual(r.collect(Gap(), now=NOW)["indices"], [])

    def test_duplicate_day(self):
        with self.assertRaises(ValueError):
            r.observation([{"date":CAL[0],"close":100}]*2,"000001",date(2026,9,4),"test")


if __name__ == "__main__":
    unittest.main()
