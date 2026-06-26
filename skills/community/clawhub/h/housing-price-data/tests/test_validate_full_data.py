import sys
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import validate_full_data  # noqa: E402
from config import INDICATORS  # noqa: E402


SAMPLE_HTML = """
<html>
  <body>
    <div class="trs_editor_view">
      <p>2025年1月70个大中城市新建商品住宅销售价格指数</p>
      <table>
        <tr>
          <th>城市</th><th>环比</th><th>同比</th><th>定基</th>
          <th>城市</th><th>环比</th><th>同比</th><th>定基</th>
        </tr>
        <tr>
          <td>北京</td><td>100.1</td><td>101.0</td><td>99.9</td>
          <td>武 汉</td><td>99.8</td><td>95.2</td><td>97.1</td>
        </tr>
      </table>
      <p>2025年1月70个大中城市二手住宅销售价格指数</p>
      <table>
        <tr><th>城市</th><th>环比</th><th>同比</th></tr>
        <tr><td>北京</td><td>99.9</td><td>96.2</td></tr>
        <tr><td>武汉</td><td>99.3</td><td>93.1</td></tr>
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


class ValidateFullDataTests(unittest.TestCase):
    def test_split_row_segments_handles_multi_city_header(self):
        header = ["城市", "环比", "同比", "城市", "环比", "同比"]
        row = ["北京", "100.1", "101.0", "武汉", "99.8", "95.2"]

        segments = validate_full_data.split_row_segments(header, row)

        self.assertEqual(len(segments), 2)
        self.assertEqual(segments[0][1][0], "北京")
        self.assertEqual(segments[1][1][0], "武汉")

    def test_parse_full_page_extracts_all_city_records(self):
        records = validate_full_data.parse_full_page(
            SAMPLE_HTML,
            "2025-01",
            "https://example.com/page",
        )

        self.assertEqual(len(records), 4)
        cities = {(record["city"], record["indicator"]) for record in records}
        self.assertIn(("北京", INDICATORS["new"]), cities)
        self.assertIn(("武汉", INDICATORS["new"]), cities)
        self.assertIn(("北京", INDICATORS["used"]), cities)
        self.assertIn(("武汉", INDICATORS["used"]), cities)

    def test_validate_record_schema_accepts_valid_record(self):
        issues = validate_full_data.validate_record_schema({
            "period": "2025-01",
            "city": "武汉",
            "indicator": INDICATORS["new"],
            "metrics": {"环比": 99.8, "同比": 95.2},
            "source_url": "https://example.com/page",
        })

        self.assertEqual(issues, [])

    def test_compare_records_detects_metric_mismatch(self):
        expected = [{
            "period": "2025-01",
            "city": "武汉",
            "indicator": INDICATORS["new"],
            "metrics": {"环比": 99.8},
            "source_url": "https://example.com/page",
        }]
        actual = [{
            "period": "2025-01",
            "city": "武汉",
            "indicator": INDICATORS["new"],
            "metrics": {"环比": 100.0},
            "source_url": "https://example.com/page",
        }]

        issues = validate_full_data.compare_records(expected, actual)

        self.assertEqual(len(issues), 1)
        self.assertIn("value mismatch", issues[0])

    def test_compare_records_treats_missing_and_null_metric_as_equal(self):
        expected = [{
            "period": "2025-10",
            "city": "北京",
            "indicator": INDICATORS["new"],
            "metrics": {"环比": 99.9, "同比": 98.0},
            "source_url": "https://example.com/page",
        }]
        actual = [{
            "period": "2025-10",
            "city": "北京",
            "indicator": INDICATORS["new"],
            "metrics": {"环比": 99.9, "同比": 98.0, "定基": None},
            "source_url": "https://example.com/page",
        }]

        issues = validate_full_data.compare_records(expected, actual)

        self.assertEqual(issues, [])


if __name__ == "__main__":
    unittest.main()
