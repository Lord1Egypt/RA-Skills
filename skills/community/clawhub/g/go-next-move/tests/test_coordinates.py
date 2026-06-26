import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import next_move  # noqa: E402
from next_move import (  # noqa: E402
    apply_move_overlays,
    board_ascii_to_initial_stones,
    build_result,
    convert_coord,
    convert_move_info,
    format_coord,
    parse_coord,
    parse_move_overlay,
)


class CoordinateTests(unittest.TestCase):
    def test_gtp_format_remains_default_mapping(self):
        self.assertEqual(format_coord(15, 7, 19, "gtp"), "H4")
        self.assertEqual(format_coord(15, 8, 19, "gtp"), "J4")
        self.assertEqual(format_coord(15, 18, 19, "gtp"), "T4")

    def test_sequential_mapping_includes_i(self):
        self.assertEqual(format_coord(15, 7, 19, "sequential"), "H4")
        self.assertEqual(format_coord(15, 8, 19, "sequential"), "I4")
        self.assertEqual(format_coord(15, 18, 19, "sequential"), "S4")
        self.assertEqual(convert_coord("J4", 19, "gtp", "sequential"), "I4")
        self.assertEqual(convert_coord("T4", 19, "gtp", "sequential"), "S4")

    def test_pass_and_resign_are_preserved(self):
        self.assertEqual(convert_coord("pass", 19, "gtp", "sequential"), "PASS")
        self.assertEqual(convert_coord("RESIGN", 19, "gtp", "sequential"), "RESIGN")
        self.assertIsNone(parse_coord("PASS", 19, "sequential"))

    def test_move_info_and_pv_are_converted(self):
        converted = convert_move_info(
            {"move": "J4", "pv": ["J4", "T16", "PASS"], "visits": 100},
            19,
            "sequential",
        )
        self.assertEqual(converted["move"], "I4")
        self.assertEqual(converted["pv"], ["I4", "S16", "PASS"])
        self.assertEqual(converted["visits"], 100)

    def test_initial_stones_always_use_gtp_coordinates(self):
        rows = ["." * 19 for _ in range(19)]
        rows[15] = "........X.........."
        self.assertEqual(board_ascii_to_initial_stones(rows), [["B", "J4"]])

    def test_sequential_overlay_uses_expected_board_point(self):
        rows = ["." * 19 for _ in range(19)]
        overlay = parse_move_overlay("user:B:I4:1", 19, "sequential")
        composed = apply_move_overlays(rows, [overlay], "sequential")
        self.assertEqual(composed[15][8], "X")

    def test_invalid_and_out_of_range_coordinates_are_rejected(self):
        with self.assertRaises(SystemExit):
            parse_coord("T4", 19, "sequential")
        with self.assertRaises(SystemExit):
            parse_coord("I4", 19, "gtp")
        with self.assertRaises(SystemExit):
            parse_coord("A20", 19, "sequential")

    def test_build_result_converts_all_user_facing_coordinates(self):
        rows = ["." * 19 for _ in range(19)]
        args = SimpleNamespace(
            side_to_move="black",
            level="all",
            board_size=19,
            move_overlay=["user:W:I16:1"],
            coordinate_style="sequential",
            komi=7.5,
            visits=10,
            katago="katago",
            model="model",
            analysis_config="config",
            skill_config=Path("katago/analysis_skill.cfg"),
            top_candidates=20,
            result_image=None,
            source_result_image=None,
        )
        analysis = {
            "moveInfos": [
                {
                    "move": "J4",
                    "order": 0,
                    "visits": 10,
                    "winrate": 0.55,
                    "scoreLead": 1.2,
                    "pv": ["J4", "T16", "PASS"],
                }
            ],
            "rootInfo": {},
        }
        with (
            patch.object(next_move, "load_board_source", return_value=(rows, None, None)),
            patch.object(next_move, "run_katago_analysis", return_value=analysis),
        ):
            result = build_result(args)

        self.assertEqual(result["coordinate_style"], "sequential")
        self.assertEqual(result["move_overlays"][0]["move"], "I16")
        self.assertEqual(result["recommendation"]["move"], "I4")
        self.assertEqual(result["recommendation"]["pv"], ["I4", "S16", "PASS"])
        self.assertEqual(result["candidate_moves"][0]["move"], "I4")
        self.assertEqual(result["recommendations_by_level"]["advanced"]["move"], "I4")
        self.assertEqual(result["reason"]["main_variation"], ["I4", "S16", "PASS"])
        self.assertIn("I4", result["reason"]["summary"])
        self.assertEqual(result["display_move_overlays"][-1]["move"], "I4")

    def test_build_result_defaults_can_preserve_gtp_coordinates(self):
        move = {"move": "J4", "pv": ["J4", "T16"]}
        self.assertEqual(convert_move_info(move, 19, "gtp"), move)


if __name__ == "__main__":
    unittest.main()
