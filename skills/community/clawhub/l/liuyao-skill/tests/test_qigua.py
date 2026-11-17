import importlib.util
import json
import random
import re
import unittest
from datetime import datetime
from io import StringIO
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("qigua", ROOT / "scripts" / "qigua.py")
qigua = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(qigua)


def result_for(inputs):
    return qigua.build_result(qigua.load_gua_data(), qigua.divine_manual(inputs))


# -- Trigram mapping --


class TrigramMappingTests(unittest.TestCase):
    """Verify trigram recognition for all 8 trigrams in both positions."""

    def test_lower_trigram_mapping_uses_bottom_to_top_lines(self):
        upper_qian = [1, 1, 1]
        cases = [
            ([1, 1, 1], "乾为天", "乾"),
            ([1, 1, 2], "天泽履", "兑"),
            ([1, 2, 1], "天火同人", "离"),
            ([1, 2, 2], "天雷无妄", "震"),
            ([2, 1, 1], "天风姤", "巽"),
            ([2, 1, 2], "天水讼", "坎"),
            ([2, 2, 1], "天山遁", "艮"),
            ([2, 2, 2], "天地否", "坤"),
        ]
        for lower, expected_name, expected_lower in cases:
            with self.subTest(lower=lower):
                result = result_for(lower + upper_qian)
                self.assertEqual(result["ben_gua"]["name"], expected_name)
                self.assertEqual(result["ben_gua"]["lower"], expected_lower)

    def test_upper_trigram_mapping_uses_bottom_to_top_lines(self):
        lower_qian = [1, 1, 1]
        cases = [
            ([1, 1, 1], "乾为天", "乾"),
            ([1, 1, 2], "泽天夬", "兑"),
            ([1, 2, 1], "火天大有", "离"),
            ([1, 2, 2], "雷天大壮", "震"),
            ([2, 1, 1], "风天小畜", "巽"),
            ([2, 1, 2], "水天需", "坎"),
            ([2, 2, 1], "山天大畜", "艮"),
            ([2, 2, 2], "地天泰", "坤"),
        ]
        for upper, expected_name, expected_upper in cases:
            with self.subTest(upper=upper):
                result = result_for(lower_qian + upper)
                self.assertEqual(result["ben_gua"]["name"], expected_name)
                self.assertEqual(result["ben_gua"]["upper"], expected_upper)


# -- All 64 hexagrams lookup --


class AllHexagramsTests(unittest.TestCase):
    """Verify all 64 hexagrams can be resolved from gua-data.json."""

    @classmethod
    def setUpClass(cls):
        cls.gua_data = qigua.load_gua_data()
        cls.all_hexagrams = cls.gua_data["hexagrams"]

    def test_all_64_hexagrams_exist(self):
        self.assertEqual(len(self.all_hexagrams), 64)

    def test_all_hexagrams_have_required_fields(self):
        for key, entry in self.all_hexagrams.items():
            with self.subTest(key=key):
                self.assertIn("name", entry)
                self.assertIn("upper", entry)
                self.assertIn("lower", entry)
                self.assertIn("number", entry)

    def test_all_hexagram_numbers_unique(self):
        numbers = [e["number"] for e in self.all_hexagrams.values()]
        self.assertEqual(len(numbers), len(set(numbers)))
        self.assertEqual(sorted(numbers), list(range(1, 65)))

    def test_lookup_table_derived_correctly(self):
        data = qigua.load_gua_data()
        expected = {k: v["name"] for k, v in self.all_hexagrams.items()}
        self.assertEqual(data["lookup"], expected)

    def test_each_hexagram_resolves_via_build_result(self):
        """Build a manual input for each trigram combo and verify the name matches."""
        trigram_inputs = {
            "qian": [1, 1, 1],
            "kun": [2, 2, 2],
            "zhen": [1, 2, 2],
            "xun": [2, 1, 1],
            "kan": [2, 1, 2],
            "li": [1, 2, 1],
            "gen": [2, 2, 1],
            "dui": [1, 1, 2],
        }
        for key, entry in self.all_hexagrams.items():
            with self.subTest(key=key):
                lower_input = trigram_inputs[entry["lower"]]
                upper_input = trigram_inputs[entry["upper"]]
                result = result_for(lower_input + upper_input)
                self.assertEqual(result["ben_gua"]["name"], entry["name"])


# -- Moving yao scenarios --


class MovingYaoTests(unittest.TestCase):
    """Test moving yao logic for 0, 1, 2, 3, 4, 5, 6 moving lines."""

    def test_no_moving_yao_static_hexagram(self):
        result = result_for([1, 1, 1, 1, 1, 1])
        self.assertEqual(result["moving_yao"], [])
        self.assertEqual(result["ben_gua"]["name"], result["bian_gua"]["name"])

    def test_single_moving_yao(self):
        result = result_for([3, 1, 1, 1, 1, 1])
        self.assertEqual(len(result["moving_yao"]), 1)
        self.assertEqual(result["moving_yao"][0], "初九")

    def test_two_moving_yao(self):
        result = result_for([3, 1, 3, 1, 1, 1])
        self.assertEqual(len(result["moving_yao"]), 2)

    def test_three_moving_yao(self):
        result = result_for([3, 3, 3, 1, 1, 1])
        self.assertEqual(len(result["moving_yao"]), 3)

    def test_four_moving_yao(self):
        result = result_for([3, 3, 3, 3, 1, 1])
        self.assertEqual(len(result["moving_yao"]), 4)

    def test_five_moving_yao(self):
        result = result_for([3, 3, 3, 3, 3, 1])
        self.assertEqual(len(result["moving_yao"]), 5)

    def test_six_moving_yao_all_moving(self):
        result = result_for([3, 3, 3, 3, 3, 3])
        self.assertEqual(len(result["moving_yao"]), 6)

    def test_moving_yin_yao_flips_to_yang(self):
        result = result_for([0, 1, 1, 1, 1, 1])
        self.assertEqual(result["moving_yao"], ["初六"])
        self.assertNotEqual(result["ben_gua"]["name"], result["bian_gua"]["name"])

    def test_bian_gua_differs_when_moving_yao_present(self):
        result = result_for([3, 1, 1, 1, 1, 1])
        self.assertNotEqual(result["ben_gua"]["name"], result["bian_gua"]["name"])

    def test_bian_gua_same_when_no_moving_yao(self):
        result = result_for([1, 1, 1, 1, 1, 1])
        self.assertEqual(result["ben_gua"]["name"], result["bian_gua"]["name"])


# -- Yao label --


class YaoLabelTests(unittest.TestCase):
    """Test yao_label for all 6 positions with yin and yang."""

    def test_yang_positions(self):
        expected = {1: "初九", 2: "九二", 3: "九三", 4: "九四", 5: "九五", 6: "上九"}
        for pos, label in expected.items():
            with self.subTest(pos=pos):
                self.assertEqual(qigua.yao_label(pos, True), label)

    def test_yin_positions(self):
        expected = {1: "初六", 2: "六二", 3: "六三", 4: "六四", 5: "六五", 6: "上六"}
        for pos, label in expected.items():
            with self.subTest(pos=pos):
                self.assertEqual(qigua.yao_label(pos, False), label)


# -- Coin method --


class CoinMethodTests(unittest.TestCase):
    def test_coin_returns_six_lines(self):
        yaos = qigua.divine_coin()
        self.assertEqual(len(yaos), 6)

    def test_coin_deterministic_with_seed(self):
        random.seed(42)
        yaos1 = qigua.divine_coin()
        random.seed(42)
        yaos2 = qigua.divine_coin()
        self.assertEqual(yaos1, yaos2)

    def test_coin_all_types_possible(self):
        """With enough random seeds, all 4 types should appear."""
        types_seen = set()
        for seed in range(100):
            random.seed(seed)
            yaos = qigua.divine_coin()
            for y in yaos:
                types_seen.add(y["type"])
        self.assertEqual(types_seen, {"老阴", "少阳", "少阴", "老阳"})

    def test_coin_back_count_range(self):
        for _ in range(100):
            count = qigua.coin_back_count()
            self.assertIn(count, {0, 1, 2, 3})


# -- Shicao method --


class ShicaoMethodTests(unittest.TestCase):
    def test_shicao_generates_six_valid_lines(self):
        random.seed(20260522)
        yaos = qigua.divine_shicao()
        self.assertEqual(len(yaos), 6)
        for yao in yaos:
            self.assertIn(yao["shicao_value"], {6, 7, 8, 9})
            self.assertIn(yao["type"], {"老阴", "少阳", "少阴", "老阳"})

    def test_shicao_line_value_uses_classic_change_odds(self):
        with patch.object(qigua.random, "random", side_effect=[0.1, 0.1, 0.1]):
            self.assertEqual(qigua.shicao_line_value(), 9)
        with patch.object(qigua.random, "random", side_effect=[0.9, 0.9, 0.9]):
            self.assertEqual(qigua.shicao_line_value(), 6)

    def test_shicao_probability_distribution(self):
        """Verify approximate probability distribution over many trials."""
        counts = {6: 0, 7: 0, 8: 0, 9: 0}
        n = 10000
        random.seed(0)
        for _ in range(n):
            v = qigua.shicao_line_value()
            counts[v] += 1
        self.assertAlmostEqual(counts[6] / n, 1 / 16, delta=0.02)
        self.assertAlmostEqual(counts[7] / n, 5 / 16, delta=0.02)
        self.assertAlmostEqual(counts[8] / n, 7 / 16, delta=0.02)
        self.assertAlmostEqual(counts[9] / n, 3 / 16, delta=0.02)

    def test_shicao_stalks_decrease(self):
        """shicao_change always reduces stalks."""
        random.seed(1)
        stalks = 49
        for i in range(3):
            new_stalks = qigua.shicao_change(stalks, i)
            self.assertLess(new_stalks, stalks)
            stalks = new_stalks


# -- Manual input --


class ManualInputTests(unittest.TestCase):
    def test_manual_input_errors_are_catchable(self):
        with self.assertRaises(ValueError):
            qigua.divine_manual([1, 2, 3])
        with self.assertRaises(ValueError):
            qigua.divine_manual([1, 2, 3, 0, 1, 4])

    def test_manual_input_accepts_valid_values(self):
        for v in [0, 1, 2, 3]:
            yaos = qigua.divine_manual([v] * 6)
            self.assertEqual(len(yaos), 6)
            self.assertEqual(yaos[0]["type"], qigua.YAO_TYPE_MAP[v]["type"])

    def test_manual_input_too_many_values(self):
        with self.assertRaises(ValueError):
            qigua.divine_manual([1, 2, 3, 0, 1, 2, 1])

    def test_manual_input_boundary_values(self):
        yaos = qigua.divine_manual([0, 0, 0, 0, 0, 0])
        for y in yaos:
            self.assertEqual(y["type"], "老阴")
            self.assertTrue(y["moving"])

        yaos = qigua.divine_manual([3, 3, 3, 3, 3, 3])
        for y in yaos:
            self.assertEqual(y["type"], "老阳")
            self.assertTrue(y["moving"])


# -- Build result structure --


class BuildResultTests(unittest.TestCase):
    def test_result_has_all_required_keys(self):
        result = result_for([1, 2, 1, 2, 1, 2])
        required = {"ben_gua", "bian_gua", "yao_details", "moving_yao", "timestamp"}
        self.assertEqual(set(result.keys()), required)

    def test_ben_gua_has_upper_lower_name(self):
        result = result_for([1, 1, 1, 1, 1, 1])
        for key in ("name", "upper", "lower"):
            self.assertIn(key, result["ben_gua"])

    def test_yao_details_has_six_entries(self):
        result = result_for([1, 2, 3, 0, 1, 2])
        self.assertEqual(len(result["yao_details"]), 6)

    def test_yao_details_positions_1_to_6(self):
        result = result_for([1, 2, 3, 0, 1, 2])
        positions = [y["position"] for y in result["yao_details"]]
        self.assertEqual(positions, [1, 2, 3, 4, 5, 6])

    def test_yao_details_required_fields(self):
        result = result_for([3, 0, 1, 2, 1, 2])
        for yao in result["yao_details"]:
            for field in ("position", "type", "symbol", "moving", "label"):
                self.assertIn(field, yao)

    def test_timestamp_is_iso_format(self):
        result = result_for([1, 1, 1, 1, 1, 1])
        datetime.fromisoformat(result["timestamp"])

    def test_timestamp_includes_timezone(self):
        result = result_for([1, 1, 1, 1, 1, 1])
        self.assertIsNotNone(datetime.fromisoformat(result["timestamp"]).tzinfo)

    def test_invalid_shape_is_rejected(self):
        with self.assertRaises(ValueError):
            qigua.build_result(qigua.load_gua_data(), qigua.divine_manual([1] * 5))

    def test_invalid_trigram_shape_is_rejected(self):
        with self.assertRaises(ValueError):
            qigua.get_trigram_key([])


# -- Print visual --


class PrintVisualTests(unittest.TestCase):
    def test_print_visual_outputs_hexagram_name(self):
        result = result_for([1, 1, 1, 1, 1, 1])
        with patch("sys.stdout", new_callable=StringIO) as mock_out:
            qigua.print_visual(result)
            output = mock_out.getvalue()
        self.assertIn("乾为天", output)

    def test_print_visual_shows_moving_yao(self):
        result = result_for([3, 1, 1, 1, 1, 1])
        with patch("sys.stdout", new_callable=StringIO) as mock_out:
            qigua.print_visual(result)
            output = mock_out.getvalue()
        self.assertIn("动爻", output)

    def test_print_visual_shows_static_message(self):
        result = result_for([1, 1, 1, 1, 1, 1])
        with patch("sys.stdout", new_callable=StringIO) as mock_out:
            qigua.print_visual(result)
            output = mock_out.getvalue()
        self.assertIn("静卦", output)


# -- Data integrity --


class DataIntegrityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.gua_data = qigua.load_gua_data()

    def test_trigrams_count_is_8(self):
        self.assertEqual(len(self.gua_data["trigrams"]), 8)

    def test_trigram_binary_fields_match_names(self):
        """Verify TRIGRAM_NAMES mapping is consistent with gua-data.json trigrams."""
        for name, info in self.gua_data["trigrams"].items():
            binary = info["binary"]
            with self.subTest(name=name):
                reversed_binary = binary[::-1]
                self.assertIn(reversed_binary, qigua.TRIGRAM_NAMES)

    def test_reference_headings_cover_all_hexagrams(self):
        expected_names = {e["name"] for e in self.gua_data["hexagrams"].values()}
        for rel_path in ["references/guaci-full.md", "references/yaoci-full.md"]:
            text = (ROOT / rel_path).read_text(encoding="utf-8")
            headings = set(re.findall(r"^## (.+)$", text, flags=re.M))
            self.assertEqual(headings, expected_names, msg=f"Mismatch in {rel_path}")

    def test_gua_data_json_is_valid(self):
        raw = (ROOT / "assets" / "gua-data.json").read_text(encoding="utf-8")
        data = json.loads(raw)
        self.assertIn("trigrams", data)
        self.assertIn("hexagrams", data)

    def test_generated_guaci_matches_committed_reference(self):
        import scripts.regenerate_guaci as regenerate_guaci

        expected = regenerate_guaci.generate_guaci()
        actual = (ROOT / "references/guaci-full.md").read_text(encoding="utf-8")
        self.assertEqual(actual, expected)

    def test_trigram_display_covers_all_names(self):
        for name in self.gua_data["trigrams"]:
            self.assertIn(name, qigua.TRIGRAM_DISPLAY)


# -- CLI main() --


class CLITests(unittest.TestCase):
    """Test the main() CLI entry point."""

    def test_coin_method_json_output(self):
        argv = ["qigua.py", "--method", "coin", "--seed", "42", "--json"]
        with (
            patch("sys.argv", argv),
            patch("sys.stdout", new_callable=StringIO) as mock_out,
        ):
            qigua.main()
            output = mock_out.getvalue()
        data = json.loads(output)
        self.assertIn("ben_gua", data)
        self.assertIn("bian_gua", data)

    def test_shicao_method_json_output(self):
        argv = ["qigua.py", "--method", "shicao", "--seed", "42", "--json"]
        with (
            patch("sys.argv", argv),
            patch("sys.stdout", new_callable=StringIO) as mock_out,
        ):
            qigua.main()
            output = mock_out.getvalue()
        data = json.loads(output)
        self.assertIn("ben_gua", data)

    def test_manual_method_json_output(self):
        argv = ["qigua.py", "--method", "manual", "--input", "1,2,3,0,1,2", "--json"]
        with (
            patch("sys.argv", argv),
            patch("sys.stdout", new_callable=StringIO) as mock_out,
        ):
            qigua.main()
            output = mock_out.getvalue()
        data = json.loads(output)
        self.assertIn("ben_gua", data)

    def test_manual_without_input_exits_with_error(self):
        with patch("sys.argv", ["qigua.py", "--method", "manual"]):
            with self.assertRaises(SystemExit) as ctx:
                qigua.main()
            self.assertEqual(ctx.exception.code, 1)

    def test_manual_bad_format_exits_with_error(self):
        with patch("sys.argv", ["qigua.py", "--method", "manual", "--input", "abc"]):
            with self.assertRaises(SystemExit) as ctx:
                qigua.main()
            self.assertEqual(ctx.exception.code, 1)

    def test_manual_wrong_count_exits_with_error(self):
        with patch("sys.argv", ["qigua.py", "--method", "manual", "--input", "1,2"]):
            with self.assertRaises(SystemExit) as ctx:
                qigua.main()
            self.assertEqual(ctx.exception.code, 1)

    def test_visual_output_includes_hexagram(self):
        argv = ["qigua.py", "--method", "coin", "--seed", "42"]
        with (
            patch("sys.argv", argv),
            patch("sys.stdout", new_callable=StringIO) as mock_out,
        ):
            qigua.main()
            output = mock_out.getvalue()
        self.assertIn("本卦", output)
        self.assertIn("卦象", output)


if __name__ == "__main__":
    unittest.main()
