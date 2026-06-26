import sys
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import fetch_data  # noqa: E402
from config import INDICATORS  # noqa: E402


SAMPLE_HTML = """
<html>
  <body>
    <div class="trs_editor_view">
      <p>2025年1月70个大中城市新建商品住宅销售价格指数</p>
      <table>
        <tr><th>城市</th><th>环比</th><th>同比</th><th>定基</th></tr>
        <tr><td>北京</td><td>100.1</td><td>101.0</td><td>99.9</td></tr>
        <tr><td>武汉</td><td>99.8</td><td>95.2</td><td>97.1</td></tr>
      </table>
      <p>2025年1月70个大中城市二手住宅销售价格指数</p>
      <table>
        <tr><th>城市</th><th>环比</th><th>同比</th><th>定基</th></tr>
        <tr><td>北京</td><td>99.9</td><td>96.2</td><td>94.0</td></tr>
        <tr><td>武汉</td><td>99.3</td><td>93.1</td><td>92.6</td></tr>
      </table>
      <p>2025年1月70个大中城市新建商品住宅销售价格分类指数</p>
      <table>
        <tr><th>城市</th><th>分类</th><th>环比</th></tr>
        <tr><td>武汉</td><td>90平方米及以下</td><td>100.0</td></tr>
      </table>
    </div>
  </body>
</html>
""".encode("utf-8")


class FetchDataTests(unittest.TestCase):
    def test_normalize_metric_name(self):
        self.assertEqual(fetch_data.normalize_metric_name("MoM"), "环比")
        self.assertEqual(fetch_data.normalize_metric_name("同比指数"), "同比")
        self.assertEqual(fetch_data.normalize_metric_name("fixed-base"), "定基")
        self.assertIsNone(fetch_data.normalize_metric_name("unknown"))

    def test_normalize_city_name(self):
        self.assertEqual(fetch_data.normalize_city_name(" 北京市 "), "北京")
        self.assertEqual(fetch_data.normalize_city_name("呼和浩特市"), "呼和浩特")
        self.assertEqual(fetch_data.normalize_city_name("武 汉"), "武汉")
        self.assertEqual(fetch_data.normalize_city_name("不存在的城市"), "不存在的城市")

    def test_parse_page_extracts_target_city_records(self):
        records = fetch_data.parse_page(
            SAMPLE_HTML,
            "2025-01",
            "武汉",
            ["环比", "同比", "定基"],
            source_url="https://example.com/page",
        )

        self.assertEqual(len(records), 2)
        indicators = {record["indicator"] for record in records}
        self.assertEqual(indicators, {INDICATORS["new"], INDICATORS["used"]})
        self.assertTrue(all(record["city"] == "武汉" for record in records))

        new_record = next(record for record in records if record["indicator"] == INDICATORS["new"])
        used_record = next(record for record in records if record["indicator"] == INDICATORS["used"])
        self.assertEqual(new_record["metrics"]["环比"], 99.8)
        self.assertEqual(used_record["metrics"]["同比"], 93.1)

    def test_build_chart_series_aligns_missing_values(self):
        records = [
            {
                "period": "2025-01",
                "city": "北京",
                "indicator": INDICATORS["new"],
                "metrics": {"环比": 100.1, "同比": 101.0},
                "source_url": "https://example.com/1",
            },
            {
                "period": "2025-02",
                "city": "北京",
                "indicator": INDICATORS["new"],
                "metrics": {"环比": 100.2, "同比": 100.5},
                "source_url": "https://example.com/2",
            },
            {
                "period": "2025-02",
                "city": "北京",
                "indicator": INDICATORS["used"],
                "metrics": {"环比": 99.8, "同比": 98.8},
                "source_url": "https://example.com/2",
            },
        ]

        chart_data = fetch_data.build_chart_series(records)
        self.assertEqual(chart_data["periods"], ["2025-01", "2025-02"])
        self.assertEqual(chart_data["series"][INDICATORS["new"]]["同比"], [101.0, 100.5])
        self.assertEqual(chart_data["series"][INDICATORS["used"]]["同比"], [None, 98.8])
        self.assertAlmostEqual(chart_data["gap"][1], 1.7)
        self.assertIsNone(chart_data["gap"][0])


if __name__ == "__main__":
    unittest.main()
