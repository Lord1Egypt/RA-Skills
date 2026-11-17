"""Offline regression: labels, calculations, all exports and old-report migration."""
from copy import deepcopy
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET
import zipfile

import analyze_wx_video as video
from interaction_metrics import (
    normalize_info, interaction_basis, interaction_total, infer_interaction_profile,
    exact_count, SEMANTICS_VERSION,
)


def sample_info():
    # Synthetic exact counts reproducing the customer screenshot's scale.
    return {"code": "OK", "data": {
        "title": "指标口径回归样例（合成数据）", "accountName": "测试账号",
        "metrics": {"likeCount": 2969, "favoriteCount": 18000,
                    "shareCount": 1069, "commentCount": 67},
        "metricDetails": {"favoriteCount": {"display": "1.8万", "value": 18000,
                                             "exact": True, "relation": "exact"}},
    }}


def sample_raw():
    return {"schemaVersion": "1.0", "info": sample_info(), "isLocal": False,
            "inputDesc": "合成回归样例", "billing": [{"name": "历史调用", "path": "test",
                                                      "consumption": .21, "balance": 10}],
            "analysis": {"data": {"observation": {
                "segments": [{"startSeconds": 0, "endSeconds": 5, "visualDescription": "示例镜头"}],
                "summary": "合成视觉观察", "visualFacts": [], "uncertainties": [],
            }}}}


def sample_analysis(raw):
    return {
        "schemaVersion": "1.0", "interactionBasis": interaction_basis(raw.get("info"), raw.get("isLocal", False)),
        "audience": {}, "structure": {"scriptType": "示例", "rationale": "0-5秒示例镜头",
                                      "summary": "合成分析", "segmentNotes": {"1": "示例镜头说明"}},
        "viralAttribution": [{"rank": i, "layer": "内容因素", "factor": "测试因素",
                              "detail": "示例镜头", "contribution": 50, "evidence": "0-5秒"} for i in (1, 2)],
        "viralFormula": "示例结构", "replicability": {"score": 3},
        "sixDimScores": [{"dimension": d, "score": 6, "evidence": "0-5秒", "reason": "合成评分",
                          "suggestion": "补充镜头"} for d in video.SIX_DIMENSIONS],
        "operations": ["补充首帧说明", "简化镜头文案", "增加内容证据"],
        "overall": {"totalScore": 60, "replicabilityStars": 3,
                    "highlights": [{"type": "亮点", "text": "示例亮点"}, {"type": "问题", "text": "示例问题"}],
                    "primaryImprovement": "补充内容证据"},
    }


def xlsx_rows(path, sheet=2):
    ns = {"s": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    with zipfile.ZipFile(path) as z:
        strings = ["".join(si.itertext()) for si in ET.fromstring(z.read("xl/sharedStrings.xml"))]
        tree = ET.fromstring(z.read("xl/worksheets/sheet%d.xml" % sheet))
        rows = []
        for row in tree.findall(".//s:row", ns):
            values = []
            for cell in row.findall("s:c", ns):
                value = cell.find("s:v", ns)
                if value is not None:
                    values.append(strings[int(value.text)] if cell.get("t") == "s" else value.text)
                else:
                    values.append("".join(cell.itertext()))
            rows.append(values)
        return rows


class InteractionRegression(unittest.TestCase):
    def test_customer_counts_and_ratio_denominator(self):
        metrics = normalize_info(sample_info())["data"]["metrics"]
        self.assertEqual(metrics, {"likeCount": 18000, "recommendCount": 2969,
                                   "shareCount": 1069, "commentCount": 67})
        profile = infer_interaction_profile(metrics)
        self.assertEqual(profile["dominant"], "点赞")
        self.assertEqual(profile["total"], 22105)
        self.assertEqual(profile["ratios"], {"推荐/点赞": 16.5, "转发/点赞": 5.9, "评论/点赞": .4})
        self.assertNotIn("收藏", profile["counts"])
        self.assertNotIn("存档型", profile["type"])

    def test_normalization_is_nonmutating_and_idempotent(self):
        original = sample_info()
        snapshot = deepcopy(original)
        normalized = normalize_info(original)
        self.assertEqual(original, snapshot)
        self.assertEqual(normalize_info(normalized), normalized)
        self.assertEqual(normalized["data"]["metricDetails"]["likeCount"]["display"], "1.8万")
        self.assertEqual(normalized["data"]["metricSemanticsVersion"], SEMANTICS_VERSION)

    def test_precision_zero_and_missing(self):
        self.assertEqual(exact_count("9007199254740993"), 9007199254740993)
        self.assertEqual(exact_count("0"), 0)
        self.assertEqual(exact_count("123.0"), 123)
        for value in (None, "", True, -1, "NaN", "Infinity", "1.5", "1.8万", "10万+"):
            with self.subTest(value=value):
                self.assertIsNone(exact_count(value))
        empty = normalize_info({"data": {"metrics": {}}})["data"]["metrics"]
        self.assertIsNone(interaction_total(empty))
        self.assertIsNone(infer_interaction_profile(empty))
        zeros = normalize_info({"data": {"metrics": {k: 0 for k in sample_info()["data"]["metrics"]}}})["data"]["metrics"]
        self.assertEqual(interaction_total(zeros), 0)
        self.assertIsNone(infer_interaction_profile(zeros))

    def test_rounded_counts_never_become_exact(self):
        for relation, flag in (("approx", False), ("gte", True), ("unknown", False)):
            info = sample_info()
            info["data"]["metricDetails"]["favoriteCount"].update(exact=flag, relation=relation)
            data = normalize_info(info)["data"]
            self.assertIsNone(data["metrics"]["likeCount"])
            self.assertIsNone(interaction_total(data["metrics"]))
            self.assertIsNone(infer_interaction_profile(data["metrics"]))
        info = sample_info()
        info["data"]["metrics"]["favoriteCount"] = "1.8万"
        info["data"]["metricDetails"] = {}
        self.assertIsNone(normalize_info(info)["data"]["metrics"]["likeCount"])

    def test_unknown_semantics_refused(self):
        info = sample_info()
        info["data"]["metricSemanticsVersion"] = "unknown-v3"
        with self.assertRaises(ValueError):
            normalize_info(info)

    def test_all_exports_agree_on_metrics(self):
        info = sample_info()
        with tempfile.TemporaryDirectory() as tmp:
            md = video.render_report(info, None, [], "offline")
            html_path = video.render_html_dashboard(info, None, [], "offline", out_path=str(Path(tmp) / "report.html"))
            xlsx_path = video.render_xlsx(info, None, [], "offline", out_path=str(Path(tmp) / "report.xlsx"))
            html = Path(html_path).read_text(encoding="utf-8")
            self.assertIn("| 点赞 | 18000 | 1.8万 |", md)
            self.assertIn("| 推荐 | 2969 |", md)
            self.assertIn("点赞<b>18,000</b>", html)
            self.assertIn("推荐<b>2,969</b>", html)
            rows = {row[0]: row[1:] for row in xlsx_rows(xlsx_path)}
            self.assertEqual(rows["点赞"], ["18000", "1.8万"])
            self.assertEqual(rows["推荐"][0], "2969")
            self.assertNotIn("收藏", rows)
            self.assertNotIn("收藏<b>", html)

    def test_missing_and_approximate_export_as_unknown(self):
        info = sample_info()
        info["data"]["metrics"].pop("likeCount")
        info["data"]["metricDetails"]["favoriteCount"].update(exact=False, relation="approx")
        with tempfile.TemporaryDirectory() as tmp:
            md = video.render_report(info, None, [], "offline")
            path = video.render_html_dashboard(info, None, [], "offline", out_path=str(Path(tmp) / "report.html"))
            html = Path(path).read_text(encoding="utf-8")
            self.assertIn("| 点赞 | 未获取精确值 | 1.8万 |", md)
            self.assertIn("点赞<b>1.8万（非精确值）</b>", html)
            self.assertIn("推荐<b>未获取</b>", html)
            self.assertNotIn("推荐<b>0</b>", html)
            self.assertIn("数据不全，未计算", md)

    def test_stale_analysis_rejected_corrected_analysis_accepted(self):
        raw = sample_raw()
        analysis = sample_analysis(raw)
        self.assertEqual(video.validate_analysis(analysis, raw), [])
        stale = deepcopy(analysis)
        stale.pop("interactionBasis")
        self.assertTrue(any("interactionBasis" in e for e in video.validate_analysis(stale, raw)))
        stale = deepcopy(analysis)
        stale["interactionBasis"]["metrics"]["likeCount"] = 2969
        self.assertTrue(any("interactionBasis" in e for e in video.validate_analysis(stale, raw)))
        raw["info"]["data"]["metrics"]["favoriteCount"] += 1
        self.assertTrue(video.validate_analysis(analysis, raw))

    def test_old_raw_rerender_offline_without_recharge_or_mutation(self):
        raw = sample_raw()
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            raw_path = directory / "old_raw.json"
            raw_path.write_text(json.dumps(raw), encoding="utf-8")
            original = raw_path.read_bytes()
            out = directory / "output"
            out.mkdir()
            stdout = io.StringIO()
            with patch.object(video.urllib.request, "urlopen", side_effect=AssertionError("network forbidden")), \
                    patch.object(video, "_make_conn", side_effect=AssertionError("network forbidden")), \
                    patch("sys.stdout", stdout), patch("sys.stderr", io.StringIO()):
                video.run_render(str(raw_path), None, "all", str(out))
            self.assertEqual(raw_path.read_bytes(), original)
            self.assertIn("WM_VIDEO_TOTAL_CONSUMPTION=0.000000", stdout.getvalue())
            self.assertEqual(json.loads((out / "wm_interaction_facts.json").read_text(encoding="utf-8")), interaction_basis(raw["info"]))
            for name in ("wm_video_report.md", "wm_video_report.xlsx", "wm_video_dashboard.html"):
                self.assertTrue((out / name).is_file())
            analysis_path = directory / "analysis.json"
            stale = sample_analysis(raw)
            stale.pop("interactionBasis")
            analysis_path.write_text(json.dumps(stale), encoding="utf-8")
            with patch("sys.stderr", io.StringIO()), self.assertRaises(SystemExit) as caught:
                video.run_render(str(raw_path), str(analysis_path), "all", str(out))
            self.assertEqual(caught.exception.code, 8)

    def test_local_video_has_no_synthetic_engagement(self):
        raw = {"isLocal": True, "info": None}
        self.assertEqual(interaction_basis(None, True)["metrics"], {})
        self.assertEqual(video.validate_analysis(sample_analysis(raw), raw), [])
        with tempfile.TemporaryDirectory() as tmp:
            path = video.render_html_dashboard(None, None, [], "local", is_local=True, out_path=str(Path(tmp) / "local.html"))
            html = Path(path).read_text(encoding="utf-8")
            self.assertNotIn("点赞<b>", html)
            self.assertNotIn("推荐<b>", html)


if __name__ == "__main__":
    unittest.main(verbosity=2)
