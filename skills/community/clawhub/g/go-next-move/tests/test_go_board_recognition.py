import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import go_board_recognition  # noqa: E402


class GoBoardRecognitionTests(unittest.TestCase):
    def test_right_top_adjacent_white_stone_is_detected(self):
        fixture = Path(__file__).resolve().parent / "fixtures" / "right-top-white-regression.jpg"

        result, _, _, _, _ = go_board_recognition.recognize_board(fixture)
        rows = result["board_ascii"]

        self.assertEqual(result["white_stones"], 6)
        self.assertEqual(rows[2][15], "O")
        self.assertEqual(rows[4][15], "O")
        self.assertEqual(rows[5][15], "O")
        self.assertEqual(rows[4][16], "X")
        self.assertEqual(rows[5][16], "X")
        self.assertEqual(rows[6][16], "X")

    def test_right_side_middle_white_stone_is_detected(self):
        fixture = Path(__file__).resolve().parent / "fixtures" / "right-side-white-label-regression.jpg"

        result, _, _, _, _ = go_board_recognition.recognize_board(fixture)
        rows = result["board_ascii"]

        self.assertEqual(result["white_stones"], 10)
        self.assertEqual(rows[5][15], "O")
        self.assertEqual(rows[5][16], "X")
        self.assertEqual(rows[6][14], "O")
        self.assertEqual(rows[6][15], "X")
        self.assertEqual(rows[6][16], "X")

    def test_right_side_two_adjacent_white_stones_are_detected(self):
        fixture = Path(__file__).resolve().parent / "fixtures" / "recommendation-occupied-white-regression.jpg"

        result, _, _, _, _ = go_board_recognition.recognize_board(fixture)
        rows = result["board_ascii"]

        self.assertEqual(result["white_stones"], 13)
        self.assertEqual(rows[3][16], "O")
        self.assertEqual(rows[6][14], "O")
        self.assertEqual(rows[4][15], "O")
        self.assertEqual(rows[4][16], "X")
        self.assertEqual(rows[5][15], "O")
        self.assertEqual(rows[5][16], "X")

    def test_uniform_white_stones_with_dark_centers_are_detected(self):
        fixture = Path(__file__).resolve().parent / "fixtures" / "two-white-stones-edge-contrast-regression.jpg"

        result, _, _, _, _ = go_board_recognition.recognize_board(fixture)
        rows = result["board_ascii"]

        self.assertEqual(result["white_stones"], 13)
        self.assertEqual(rows[3][16], "O")
        self.assertEqual(rows[6][14], "O")
        self.assertEqual(rows[4][15], "O")
        self.assertEqual(rows[5][15], "O")


if __name__ == "__main__":
    unittest.main()
