#!/usr/bin/env python3
"""Fixture-driven tests for heatmap.py. Standard library only.

    python3 -m unittest discover -s scripts -p 'test_*.py'
    python3 scripts/test_heatmap.py

These are the invariants that are cheap to state and expensive to notice going wrong: a tile for
every row, a layout that fills its container, an absent reading that is never painted as a zero,
a page small enough for a host that renders it inline, and nothing in the file that reaches out
to the network.
"""

import contextlib
import io
import json
import os
import re
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import heatmap  # noqa: E402

FIXTURE = os.path.join(HERE, "fixtures", "market-heatmap.nasdaq100.sample.json")


def load():
    with open(FIXTURE, "r", encoding="utf-8") as fh:
        return json.load(fh)


def pro(envelope=None, layers=("sentiment", "options")):
    """The same board as a PRO key receives it: overlays present, nothing withheld.

    Built in memory rather than bundled, because the fixture's job is to be the response an
    agent actually gets from a free key. `layers` drops a layer from meta.layers to model a
    layer the writer could not build today.
    """
    envelope = envelope or load()
    envelope["isPreview"] = False
    envelope["previewReason"] = None
    meta = envelope["data"]["meta"]
    meta.pop("previewWithheld", None)
    meta["layers"] = dict((k, v) for k, v in meta["layers"].items()
                          if k in ("prices", "marketMood") or k in layers)
    for i, row in enumerate(envelope["data"]["rows"]):
        if "sentiment" in layers:
            row["sentiment7d"] = round(((i * 37) % 121 - 60) / 100.0, 2)
            row["sentimentChange7d"] = round(((i * 13) % 61 - 30) / 100.0, 2)
            row["sentisenseScore"] = round(((i * 7) % 121) - 60.0, 1)
            row["mentionsZ"] = round(((i * 11) % 71 - 20) / 10.0, 1)
            row["metrics"].append({"label": "SentiSense Score",
                                   "value": row["sentisenseScore"], "unit": "score"})
        if "options" in layers:
            row["optionsInterestScore"] = float((i * 17) % 101)
    return envelope


def render(envelope, metric="changePercent"):
    board = heatmap.build_board(envelope, "nasdaq100", True)
    layout = heatmap.build_layout(board)
    scales = heatmap.build_scales(board)
    html = heatmap.render_page(board, layout, scales, metric, "01 Sep 2026 20:00 UTC")
    return board, layout, scales, html


class SquarifyTest(unittest.TestCase):

    def test_areas_sum_to_the_container(self):
        values = [40.0, 25.0, 15.0, 10.0, 6.0, 3.0, 1.0]
        rects = heatmap.squarify(values, 0.0, 0.0, 160.0, 100.0)
        area = sum(w * h for _, _, w, h in rects)
        self.assertAlmostEqual(area, 160.0 * 100.0, places=6)

    def test_every_value_keeps_its_own_rectangle_and_its_share(self):
        values = [9.0, 1.0, 5.0, 3.0]
        rects = heatmap.squarify(values, 0.0, 0.0, 100.0, 100.0)
        self.assertEqual(len(rects), len(values))
        total = sum(values)
        for value, (_, _, w, h) in zip(values, rects):
            self.assertAlmostEqual(w * h, value / total * 10000.0, places=6)

    def test_rectangles_stay_inside_the_container(self):
        values = [7.0, 7.0, 5.0, 4.0, 2.0, 2.0, 1.0, 1.0, 0.5]
        for x, y, w, h in heatmap.squarify(values, 0.0, 0.0, 160.0, 90.0):
            self.assertGreaterEqual(x, -1e-9)
            self.assertGreaterEqual(y, -1e-9)
            self.assertLessEqual(x + w, 160.0 + 1e-9)
            self.assertLessEqual(y + h, 90.0 + 1e-9)

    def test_layout_is_deterministic_for_a_payload(self):
        board, layout, _, _ = render(load())
        _, again, _, _ = render(load())
        self.assertEqual(layout, again)
        self.assertEqual(len(layout["overview"]), len(board["tiles"]))


class TilesTest(unittest.TestCase):

    def test_every_row_gets_a_tile(self):
        envelope = load()
        board, layout, _, html = render(envelope)
        self.assertEqual(len(board["tiles"]), len(envelope["data"]["rows"]))
        self.assertEqual(len(layout["overview"]), len(board["tiles"]))
        placed = sum(len(m) for m in layout["members"])
        self.assertEqual(placed, len(board["tiles"]))
        for ticker in (row["ticker"] for row in envelope["data"]["rows"]):
            self.assertIn(ticker, html)

    def test_a_tile_with_no_market_cap_is_still_drawn(self):
        baseline, _, _, _ = render(load())
        envelope = load()
        for row in envelope["data"]["rows"][:3]:
            row.pop("marketCap", None)
        board, layout, _, _ = render(envelope)
        self.assertEqual(board["capMissing"], baseline["capMissing"] + 3)
        for x, y, w, h in layout["overview"]:
            self.assertGreater(w, 0.0)
            self.assertGreater(h, 0.0)

    def test_sector_rectangles_tile_the_board(self):
        _, layout, _, _ = render(load())
        area = sum(w * h for _, _, w, h in layout["sectorRects"])
        # The rects are rounded to three decimal places in percent before they reach the page,
        # so the summed area carries a rounding envelope that grows with the sector count. The
        # invariant worth holding is that no sector is missing or overlapping, which would move
        # this by whole units, not by hundredths.
        self.assertAlmostEqual(area, 100.0 * 100.0, delta=0.5)


class AbsenceTest(unittest.TestCase):

    def test_a_missing_reading_is_never_coloured_as_a_zero(self):
        envelope = load()
        rows = envelope["data"]["rows"]
        rows[0].pop("sentisenseScore", None)
        rows[1]["sentisenseScore"] = 0.0
        board, _, scales, _ = render(envelope)
        score = [s for s in scales if s["key"] == "sentisenseScore"][0]
        absent = heatmap.band_index(score, board["tiles"][0]["sentisenseScore"])
        measured = heatmap.band_index(score, board["tiles"][1]["sentisenseScore"])
        self.assertEqual(absent, -1, "an absent reading must take the no-reading slot")
        self.assertEqual(measured, -2, "a measured zero must take the flat slot")
        self.assertNotEqual(absent, measured)

    def test_a_missing_reading_reads_as_no_reading_in_the_page(self):
        envelope = load()
        envelope["data"]["rows"][0].pop("mentionsZ", None)
        board, _, _, html = render(envelope, metric="mentionsZ")
        self.assertIsNone(board["tiles"][0]["mentionsZ"])
        self.assertIn("no reading", html)

    def test_a_zero_is_not_dropped(self):
        envelope = load()
        envelope["data"]["rows"][0]["changePercent"] = 0.0
        board, _, _, _ = render(envelope)
        self.assertEqual(board["tiles"][0]["changePercent"], 0.0)
        self.assertEqual(heatmap.fmt_metric("changePercent", 0.0), "0.0%")

    def test_a_move_that_rounds_to_zero_prints_no_sign(self):
        self.assertEqual(heatmap.fmt_metric("changePercent", -0.047), "0.0%")
        self.assertEqual(heatmap.fmt_metric("changePercent", 0.003), "0.0%")
        self.assertEqual(heatmap.fmt_signed(-0.004, 2, "%"), "0.00%")
        self.assertEqual(heatmap.fmt_metric("sentisenseScore", -0.04), "0.0")
        self.assertEqual(heatmap.fmt_metric("changePercent", -0.06), "-0.1%")
        self.assertEqual(heatmap.fmt_metric("changePercent", 2.71), "+2.7%")

    def test_absent_values_display_as_no_reading_not_as_a_number(self):
        self.assertEqual(heatmap.fmt_metric("sentisenseScore", None), "no reading")
        self.assertEqual(heatmap.fmt_usd(None), "no reading")
        self.assertEqual(heatmap.fmt_count(None), "no reading")


class PreviewTest(unittest.TestCase):

    def test_a_free_key_gets_every_tile_and_the_footer_says_what_is_missing(self):
        envelope = load()
        self.assertTrue(envelope["isPreview"])
        self.assertEqual(envelope["totalCount"], len(envelope["data"]["rows"]))
        board, _, _, html = render(envelope)
        self.assertEqual(len(board["tiles"]), envelope["totalCount"])
        self.assertIn("Whole board", html)
        self.assertIn("are part of PRO", html)
        self.assertIn("nothing is estimated in their place", html)
        self.assertNotIn("largest names of", html)
        self.assertNotIn("PRO renders the full board", html)

    def test_a_pro_board_claims_no_withholding_at_all(self):
        _, _, _, html = render(pro())
        self.assertIn("Whole board", html)
        self.assertNotIn("part of PRO", html)
        self.assertNotIn("PRO overlay, not on this key", html)

    def test_a_legacy_truncated_response_still_reads_truthfully(self):
        # An older deployment could still hand back fewer rows than the board holds.
        envelope = load()
        envelope["data"]["rows"] = envelope["data"]["rows"][:60]
        board, _, _, html = render(envelope)
        self.assertTrue(heatmap.is_partial_board(board))
        self.assertIn("largest names of", html)
        self.assertIn("Sector Market Mood readings cover the whole index", html)

    def test_breadth_says_whose_breadth_it_is(self):
        board = heatmap.build_board(load(), "nasdaq100", True)
        self.assertIn("tiles drawn", heatmap.breadth_coverage(board))


class WithheldLayerTest(unittest.TestCase):

    def test_a_withheld_overlay_is_disabled_rather_than_coloured(self):
        board, _, scales, html = render(load())
        self.assertEqual(board["withheld"], ["sentiment", "options"])
        for key in ("sentiment7d", "sentisenseScore", "mentionsZ", "optionsInterestScore"):
            self.assertEqual(board["metricStates"][key], "pro")
        self.assertEqual(board["metricStates"]["changePercent"], "ok")
        self.assertIn("PRO overlay, not on this key", html)
        for key in ("sentiment7d", "sentisenseScore", "mentionsZ", "optionsInterestScore"):
            self.assertRegex(html, r'data-m="%s"[^>]*disabled' % key)
        self.assertNotRegex(html, r'data-m="changePercent"[^>]*disabled')
        for scale in scales:
            if scale["key"] == "changePercent":
                continue
            self.assertEqual(scale["count"], 0, "a withheld layer carries no readings at all")

    def test_a_layer_the_writer_could_not_build_reads_differently_from_a_tier(self):
        board, _, _, html = render(pro(layers=("sentiment",)))
        self.assertEqual(board["withheld"], [])
        self.assertEqual(board["metricStates"]["optionsInterestScore"], "unavailable")
        self.assertEqual(board["metricStates"]["sentisenseScore"], "ok")
        self.assertIn("was not built for this board today", html)
        self.assertNotIn("PRO overlay, not on this key", html)
        self.assertIn("did not run for this board", html)

    def test_an_absent_marker_never_invents_a_withheld_layer(self):
        envelope = pro()
        envelope["data"]["meta"].pop("previewWithheld", None)
        board, _, _, _ = render(envelope)
        self.assertEqual(board["withheld"], [])
        self.assertEqual(set(board["metricStates"].values()), {"ok"})

    def test_the_summary_names_the_withheld_layers_for_the_reply(self):
        board, _, scales, _ = render(load())
        summary = heatmap.build_summary(board, scales, "changePercent", "/tmp/x.html", 10,
                                        "01 Sep 2026 20:00 UTC")
        self.assertEqual(summary["preview"]["withheldLayers"], ["sentiment", "options"])
        self.assertIn("options interest", summary["preview"]["withheldDisplay"])
        self.assertIn("part of PRO", summary["preview"]["noteDisplay"])
        self.assertEqual(summary["preview"]["totalCount"], len(board["tiles"]))
        self.assertFalse(summary["preview"]["isPartialBoard"])

    def test_asking_for_a_withheld_metric_falls_back_instead_of_failing(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "board.html")
            summary_path = os.path.join(tmp, "board.json")
            stderr = io.StringIO()
            with contextlib.redirect_stderr(stderr):
                code = heatmap.main(["--fixture", FIXTURE, "--out", out, "--metric", "score",
                                     "--summary-json", summary_path])
            self.assertEqual(code, 0, "a withheld overlay is not a failure")
            self.assertIn("PRO overlay", stderr.getvalue())
            with open(summary_path, "r", encoding="utf-8") as fh:
                summary = json.load(fh)
            self.assertEqual(summary["colourMetric"]["key"], "changePercent")
            self.assertEqual(summary["colourMetric"]["requestedKey"], "sentisenseScore")
            self.assertTrue(summary["colourMetric"]["fellBack"])


class PageTest(unittest.TestCase):

    def test_the_page_fits_the_inline_limit(self):
        _, _, _, html = render(load())
        self.assertLess(len(html), heatmap.INLINE_LIMIT)

    def test_a_full_five_hundred_row_board_still_fits_the_inline_limit(self):
        # The bundled fixture is the Nasdaq-100 board, so the S&P-sized case is grown here
        # rather than shipped: the big board is what has to fit, not what has to install.
        envelope = load()
        rows = envelope["data"]["rows"]
        grown = []
        for i in range(6):
            for row in rows:
                clone = dict(row)
                if i:
                    clone["ticker"] = (row["ticker"] + chr(ord("A") + i))[:6]
                    clone["rowId"] = clone["ticker"]
                grown.append(clone)
        envelope["data"]["rows"] = grown[:501]
        envelope["isPreview"] = False
        board, _, _, html = render(envelope)
        self.assertEqual(len(board["tiles"]), 501)
        self.assertLess(len(html), heatmap.INLINE_LIMIT)

    def test_the_page_reaches_nothing_but_our_own_domain(self):
        _, _, _, html = render(load())
        urls = re.findall(r"https?://[^\s\"'<>)]+", html)
        self.assertTrue(urls, "the page should still carry the site link")
        for url in urls:
            host = url.split("//", 1)[1].split("/", 1)[0]
            self.assertTrue(host == "sentisense.ai" or host.endswith(".sentisense.ai"),
                            "unexpected external URL: " + url)
        for pattern in ("<img", "<iframe", "@import", "url(", "srcset", "fetch(",
                        "XMLHttpRequest", "<link"):
            self.assertNotIn(pattern, html, "the page must load nothing from anywhere")

    def test_the_page_carries_the_disclaimer_and_the_sample_warning(self):
        _, _, _, html = render(load())
        self.assertIn("Not investment advice", html)
        self.assertIn("Sample data", html)
        self.assertIn("sentisense.ai", html)

    def test_no_long_dash_anywhere_in_the_page(self):
        # Written as code points so this gate never itself becomes the thing it looks for.
        _, _, _, html = render(load())
        for code in (0x2014, 0x2013):
            self.assertNotIn(chr(code), html)


class ScaleTest(unittest.TestCase):

    def test_a_quiet_board_is_not_amplified_into_drama(self):
        envelope = load()
        for row in envelope["data"]["rows"]:
            row["changePercent"] = 0.05
        _, _, scales, _ = render(envelope)
        change = [s for s in scales if s["key"] == "changePercent"][0]
        self.assertGreaterEqual(change["cap"], 1.0)

    def test_an_attention_metric_never_borrows_the_bull_and_bear_pair(self):
        _, _, scales, _ = render(load())
        for scale in scales:
            if scale["kind"] != "sequential":
                continue
            for fill in scale["palette"]:
                red, green, blue = heatmap.hex_to_rgb(fill)
                self.assertGreaterEqual(blue, red, "an attention ramp must stay on the data hue")


class SummaryTest(unittest.TestCase):

    def test_every_number_comes_with_a_display_string(self):
        board, _, scales, _ = render(load())
        summary = heatmap.build_summary(board, scales, "changePercent", "/tmp/x.html", 1234,
                                        "01 Sep 2026 20:00 UTC")
        self.assertEqual(summary["marketMood"]["scoreDisplay"], "56")
        self.assertTrue(summary["breadth"]["capWeightedChangeDisplay"].endswith("%"))
        self.assertIn("Whole board", summary["preview"]["noteDisplay"])
        self.assertEqual(summary["apiCalls"], 0, "a fixture render costs no call")
        self.assertTrue(summary["withinInlineLimit"])
        for mover in summary["biggestMovesUp"] + summary["biggestMovesDown"]:
            self.assertRegex(mover["changeDisplay"], r"^[-+]?\d+\.\d%$")
        for sector in summary["sectorsByChange"]:
            self.assertIsInstance(sector["moodScoreDisplay"], str)

    def test_the_summary_never_prints_a_hole_as_a_zero(self):
        envelope = load()
        for row in envelope["data"]["rows"]:
            row.pop("sentisenseScore", None)
        board, _, scales, _ = render(envelope)
        summary = heatmap.build_summary(board, scales, "sentisenseScore", "/tmp/x.html", 10,
                                        "01 Sep 2026 20:00 UTC")
        self.assertEqual(summary["noReadingCounts"]["sentisenseScore"], len(board["tiles"]))


class SectorRankTest(unittest.TestCase):

    @staticmethod
    def _unclassify(envelope, count, change=-9.5):
        rows = envelope["data"]["rows"][:count] if count else envelope["data"]["rows"]
        for row in rows:
            row["sector"] = heatmap.UNCLASSIFIED
            row["category"] = heatmap.UNCLASSIFIED
            row["changePercent"] = change
        envelope["data"]["meta"]["sectors"].append({
            "sector": heatmap.UNCLASSIFIED, "count": len(rows), "capWeightedChangePct": change,
            "equalWeightedChangePct": change, "capUsd": 1.0e12, "up": 0, "down": len(rows)})
        return envelope

    def summary_of(self, envelope):
        board, _, scales, _ = render(envelope)
        return board, heatmap.build_summary(board, scales, "changePercent", "/tmp/x.html", 10,
                                            "01 Sep 2026 20:00 UTC")

    def test_unclassified_never_wins_the_weakest_sector_line(self):
        # A data-quality bucket is not a sector, and "weakest sector Unclassified" tells a
        # reader nothing. It still gets drawn; it just cannot be ranked as a sector.
        board, summary = self.summary_of(self._unclassify(load(), 6))
        self.assertIn(heatmap.UNCLASSIFIED, [s["name"] for s in board["sectors"]])
        self.assertNotEqual(summary["weakestSector"]["name"], heatmap.UNCLASSIFIED)
        self.assertNotEqual(summary["strongestSector"]["name"], heatmap.UNCLASSIFIED)
        self.assertNotIn(heatmap.UNCLASSIFIED,
                         [s["name"] for s in summary["sectorsByChange"]])

    def test_a_board_that_is_all_unclassified_has_no_ranked_sector_at_all(self):
        _, summary = self.summary_of(self._unclassify(load(), 0))
        self.assertEqual(summary["sectorsByChange"], [])
        self.assertIsNone(summary["strongestSector"])
        self.assertIsNone(summary["weakestSector"])


class CliTest(unittest.TestCase):

    def test_stdout_summary_mode_writes_only_the_named_html_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "board.html")
            stdout = io.StringIO()
            with contextlib.redirect_stdout(stdout):
                code = heatmap.main(["--fixture", FIXTURE, "--out", out,
                                     "--summary-json", "-"])
            self.assertEqual(code, 0)
            self.assertEqual(os.listdir(tmp), ["board.html"])
            summary = json.loads(stdout.getvalue())
            self.assertEqual(summary["outputPath"], out)
            self.assertTrue(summary["withinInlineLimit"])

    def test_a_fixture_render_writes_a_file_and_prints_its_absolute_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            # A PRO-shaped fixture, so the alias resolves AND the metric survives.
            path = os.path.join(tmp, "pro.json")
            with open(path, "w", encoding="utf-8") as fh:
                json.dump(pro(), fh)
            out = os.path.join(tmp, "board.html")
            summary = os.path.join(tmp, "board.json")
            code = heatmap.main(["--fixture", path, "--out", out,
                                 "--summary-json", summary, "--metric", "score"])
            self.assertEqual(code, 0)
            self.assertTrue(os.path.isfile(out))
            with open(summary, "r", encoding="utf-8") as fh:
                self.assertEqual(json.load(fh)["colourMetric"]["key"], "sentisenseScore")

    def test_an_unknown_scope_is_a_usage_error(self):
        self.assertEqual(heatmap.main(["--scope", "ftse100"]), heatmap.EXIT_USAGE)

    def test_an_unknown_metric_is_a_usage_error(self):
        self.assertEqual(heatmap.main(["--metric", "vibes", "--fixture", FIXTURE]),
                         heatmap.EXIT_USAGE)

    def test_an_unreadable_fixture_is_a_usage_error(self):
        self.assertEqual(heatmap.main(["--fixture", "/nope/missing.json"]), heatmap.EXIT_USAGE)

    def test_an_empty_board_is_a_not_found_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "empty.json")
            with open(path, "w", encoding="utf-8") as fh:
                json.dump({"isPreview": False, "data": {"rows": [], "meta": {}}}, fh)
            self.assertEqual(heatmap.main(["--fixture", path]), heatmap.EXIT_NOT_FOUND)


if __name__ == "__main__":
    unittest.main(verbosity=2)
