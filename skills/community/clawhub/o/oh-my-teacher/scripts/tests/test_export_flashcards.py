"""Tests for scripts/export_flashcards.py."""
from __future__ import annotations

import csv
import io
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPT_DIR))

from export_flashcards import (  # noqa: E402
    _ParseState,
    _dedup_cards,
    _expand_clozes,
    parse_cards,
)


def _run_cli(args: list[str]) -> subprocess.CompletedProcess:
    """Helper to run the export_flashcards.py script with the given arguments."""
    script = SCRIPT_DIR / "export_flashcards.py"
    return subprocess.run(
        [sys.executable, str(script)] + args,
        capture_output=True,
        text=True,
        cwd=str(SCRIPT_DIR),
    )


class ParseCardsTests(unittest.TestCase):
    def test_simple_qa(self):
        cards = parse_cards("Q: What is 2+2?\nA: 4\nTags: math")
        self.assertEqual(len(cards), 1)
        front, back, tags, deck = cards[0]
        self.assertEqual(front, "What is 2+2?")
        self.assertEqual(back, "4")
        self.assertEqual(tags, "math")
        self.assertEqual(deck, "")

    def test_front_pipe_back_shorthand(self):
        cards = parse_cards("Capital of France | Paris")
        self.assertEqual(len(cards), 1)
        self.assertEqual(cards[0][0], "Capital of France")
        self.assertEqual(cards[0][1], "Paris")

    def test_front_back_aliases(self):
        cards = parse_cards("Front: f\nBack: b")
        self.assertEqual(cards[0], ("f", "b", "", ""))

    def test_cloze_single_default_keeps_syntax(self):
        text = "Cloze: The limit {{c1::exists}} when ...\nTags: analysis"
        cards = parse_cards(text, expand_cloze=False)
        self.assertEqual(len(cards), 1)
        self.assertEqual(cards[0][0], "The limit {{c1::exists}} when ...")
        self.assertEqual(cards[0][1], "")
        self.assertEqual(cards[0][2], "analysis")

    def test_cloze_single_with_expand_still_one_card(self):
        cards = parse_cards(
            "Cloze: The limit {{c1::exists}} when ...",
            expand_cloze=True,
        )
        self.assertEqual(len(cards), 1)
        self.assertEqual(cards[0][0], "The limit {{c1::exists}} when ...")

    def test_cloze_multi_default_keeps_syntax(self):
        text = "Cloze: d/dx {{c1::sin(x)}} = {{c2::cos(x)}}."
        cards = parse_cards(text, expand_cloze=False)
        self.assertEqual(len(cards), 1)
        self.assertEqual(cards[0][0], "d/dx {{c1::sin(x)}} = {{c2::cos(x)}}.")

    def test_cloze_multi_expand(self):
        text = "Cloze: d/dx {{c1::sin(x)}} = {{c2::cos(x)}}.\nTags: calculus"
        cards = parse_cards(text, expand_cloze=True)
        self.assertEqual(len(cards), 2)
        self.assertEqual(cards[0][0], "d/dx ____ = [cos(x)].")
        self.assertEqual(cards[0][1], "d/dx [sin(x)] = [cos(x)].")
        self.assertEqual(cards[1][0], "d/dx [sin(x)] = ____.")
        self.assertEqual(cards[1][1], "d/dx [sin(x)] = [cos(x)].")
        self.assertEqual(cards[0][2], "calculus")
        self.assertEqual(cards[1][2], "calculus")

    def test_cloze_multi_expand_three_clozes(self):
        text = "Cloze: {{c1::A}} + {{c2::B}} = {{c3::C}}"
        cards = parse_cards(text, expand_cloze=True)
        self.assertEqual(len(cards), 3)
        self.assertEqual(cards[0][0], "____ + [B] = [C]")
        self.assertEqual(cards[1][0], "[A] + ____ = [C]")
        self.assertEqual(cards[2][0], "[A] + [B] = ____")
        for card in cards:
            self.assertEqual(card[1], "[A] + [B] = [C]")

    def test_cloze_with_note_in_a_dropped_in_expansion(self):
        text = "Cloze: d/dx {{c1::sin(x)}} = {{c2::cos(x)}}.\nA: basic trig identity"
        cards = parse_cards(text, expand_cloze=True)
        # In expanded mode the fully-revealed cloze is more useful than the
        # A: meta-note, so the meta-note is dropped on expanded rows.
        self.assertEqual(cards[0][1], "d/dx [sin(x)] = [cos(x)].")
        self.assertEqual(cards[1][1], "d/dx [sin(x)] = [cos(x)].")
        # In default mode the A: note is preserved as the back.
        default_cards = parse_cards(text, expand_cloze=False)
        self.assertEqual(default_cards[0][1], "basic trig identity")

    def test_default_deck_applied(self):
        cards = parse_cards("Q: q\nA: a", default_deck="Math Final")
        self.assertEqual(cards[0][3], "Math Final")

    def test_explicit_deck_overrides_default(self):
        cards = parse_cards("Q: q\nA: a\nDeck: Specific", default_deck="Math Final")
        self.assertEqual(cards[0][3], "Specific")

    def test_bom_in_front_is_stripped(self):
        cards = parse_cards("\ufeffQ: q\nA: a")
        self.assertEqual(len(cards), 1)
        self.assertEqual(cards[0][0], "q")

    def test_multiple_cards_separated_by_blank_line(self):
        text = "Q: a\nA: 1\n\nQ: b\nA: 2"
        cards = parse_cards(text)
        self.assertEqual(len(cards), 2)
        self.assertEqual(cards[0][0], "a")
        self.assertEqual(cards[1][0], "b")

    def test_normalizes_crlf_and_cr(self):
        cards = parse_cards("Q: a\r\nA: 1\r\rQ: b\rA: 2")
        self.assertEqual(len(cards), 2)

    def test_empty_input(self):
        self.assertEqual(parse_cards(""), [])
        self.assertEqual(parse_cards("\n\n\n"), [])
        self.assertEqual(parse_cards("   \n  \n"), [])

    def test_block_without_front_is_skipped(self):
        # Block has only Tags: — should not produce a card
        self.assertEqual(parse_cards("Tags: only"), [])

    def test_mixed_block_formats(self):
        text = (
            "Q: a\nA: 1\n\n"
            "Cloze: {{c1::b}}\n\n"
            "c | d\n\n"
            "Front: e\nBack: f"
        )
        cards = parse_cards(text)
        self.assertEqual(len(cards), 4)
        self.assertEqual(cards[0][0], "a")
        self.assertEqual(cards[1][0], "{{c1::b}}")
        self.assertEqual(cards[2], ("c", "d", "", ""))
        self.assertEqual(cards[3], ("e", "f", "", ""))

    def test_bidirectional_emits_two_cards(self):
        text = "Q: [Bi-directional] What is the derivative of x^2?\nA: 2x\nTags: calculus"
        cards = parse_cards(text)
        self.assertEqual(len(cards), 2)
        self.assertEqual(cards[0][0], "What is the derivative of x^2?")
        self.assertEqual(cards[0][1], "2x")
        self.assertEqual(cards[0][2], "calculus")
        self.assertEqual(cards[1][0], "2x")
        self.assertEqual(cards[1][1], "What is the derivative of x^2?")
        self.assertEqual(cards[1][2], "calculus")

    def test_bidirectional_with_front_label(self):
        text = "Front: [Bi-directional] definition\nBack: meaning"
        cards = parse_cards(text)
        self.assertEqual(len(cards), 2)
        self.assertEqual(cards[0][0], "definition")
        self.assertEqual(cards[0][1], "meaning")
        self.assertEqual(cards[1][0], "meaning")
        self.assertEqual(cards[1][1], "definition")

    def test_bidirectional_without_back_does_not_reverse(self):
        text = "Q: [Bi-directional] just front\nA:"
        cards = parse_cards(text)
        # The A: value is empty string = falsy, so no reversed card is emitted
        self.assertEqual(len(cards), 1)
        self.assertEqual(cards[0][0], "just front")
        self.assertEqual(cards[0][1], "")

    def test_bidirectional_with_expand_cloze(self):
        text = "Cloze: [Bi-directional] {{c1::A}} = {{c2::B}}\nA: note"
        cards = parse_cards(text, expand_cloze=True)
        # 2 expanded clozes + 2 reversed (the A: note is overridden by the
        # expanded back in bidirectional mode since exp_back is truthy)
        self.assertEqual(len(cards), 4)
        self.assertEqual(cards[0][0], "____ = [B]")
        self.assertEqual(cards[0][1], "[A] = [B]")
        self.assertEqual(cards[1][0], "[A] = [B]")
        self.assertEqual(cards[1][1], "____ = [B]")
        self.assertEqual(cards[2][0], "[A] = ____")
        self.assertEqual(cards[2][1], "[A] = [B]")
        self.assertEqual(cards[3][0], "[A] = [B]")
        self.assertEqual(cards[3][1], "[A] = ____")

    def test_bidirectional_cli(self):
        with tempfile.TemporaryDirectory() as tmp:
            inp = Path(tmp) / "cards.md"
            out = Path(tmp) / "cards.csv"
            inp.write_text("Q: [Bi-directional] hello\nA: world\nTags: greet", encoding="utf-8")
            result = _run_cli([str(inp), str(out)])
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Exported 2 cards", result.stdout)
            rows = list(csv.reader(out.read_text(encoding="utf-8-sig").splitlines()))
            self.assertEqual(rows[0], ["Front", "Back", "Tags", "Deck"])
            self.assertEqual(rows[1], ["hello", "world", "greet", ""])
            self.assertEqual(rows[2], ["world", "hello", "greet", ""])


class SkippedBlockWarningTests(unittest.TestCase):
    """Tests for the warning mechanism when blocks are skipped."""

    def test_skipped_blocks_are_tracked(self):
        text = "Tags: only\n\nQ: valid\nA: answer"
        state = _ParseState()
        cards = parse_cards(text, state=state)
        self.assertEqual(len(cards), 1)
        self.assertEqual(len(state.skipped_blocks), 1)
        block_num, preview = state.skipped_blocks[0]
        self.assertEqual(block_num, 1)
        self.assertIn("Tags: only", preview)

    def test_no_skipped_blocks_when_all_valid(self):
        state = _ParseState()
        parse_cards("Q: x\nA: y", state=state)
        self.assertEqual(len(state.skipped_blocks), 0)

    def test_multiple_skipped_blocks(self):
        state = _ParseState()
        text = "Tags: only1\n\nTags: only2\n\nQ: valid\nA: answer"
        parse_cards(text, state=state)
        self.assertEqual(len(state.skipped_blocks), 2)


class ExpandClozesHelperTests(unittest.TestCase):
    def test_no_cloze_returns_none(self):
        self.assertIsNone(_expand_clozes("plain text"))

    def test_single_cloze_returns_none(self):
        self.assertIsNone(_expand_clozes("Limit {{c1::exists}}."))

    def test_multi_cloze_expands(self):
        result = _expand_clozes("{{c1::A}} and {{c2::B}}")
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0][0], "____ and [B]")
        self.assertEqual(result[0][1], "[A] and [B]")
        self.assertEqual(result[1][0], "[A] and ____")
        self.assertEqual(result[1][1], "[A] and [B]")

    def test_cloze_hints_dropped_in_expansion(self):
        result = _expand_clozes("{{c1::A::first}} {{c2::B::second}}")
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0][1], "[A] [B]")

    def test_non_sequential_cloze_numbers(self):
        # c1 and c3, no c2 — should still produce 2 cards
        result = _expand_clozes("{{c1::A}} ... {{c3::C}}")
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0][0], "____ ... [C]")
        self.assertEqual(result[1][0], "[A] ... ____")


class DedupCardsHelperTests(unittest.TestCase):
    def test_no_duplicates_unchanged(self):
        cards = [("Q1", "A1", "", ""), ("Q2", "A2", "", "")]
        result, removed = _dedup_cards(cards)
        self.assertEqual(removed, 0)
        self.assertEqual(result, cards)

    def test_exact_duplicate_removed(self):
        cards = [("Q1", "A1", "t1", ""), ("Q1", "A1", "t1", "")]
        result, removed = _dedup_cards(cards)
        self.assertEqual(removed, 1)
        self.assertEqual(len(result), 1)

    def test_same_qa_different_tags_collapses(self):
        # Front+Back is the key; differing Tags/Deck still counts as duplicate.
        cards = [("Q1", "A1", "tagA", "deckA"), ("Q1", "A1", "tagB", "deckB")]
        result, removed = _dedup_cards(cards)
        self.assertEqual(removed, 1)
        # First occurrence is kept.
        self.assertEqual(result[0], ("Q1", "A1", "tagA", "deckA"))

    def test_different_back_not_duplicate(self):
        cards = [("Q1", "A1", "", ""), ("Q1", "A2", "", "")]
        result, removed = _dedup_cards(cards)
        self.assertEqual(removed, 0)
        self.assertEqual(len(result), 2)

    def test_order_preserved(self):
        cards = [("Q1", "A1", "", ""), ("Q2", "A2", "", ""), ("Q1", "A1", "", "")]
        result, removed = _dedup_cards(cards)
        self.assertEqual(removed, 1)
        self.assertEqual([c[0] for c in result], ["Q1", "Q2"])


class CLIIntegrationTests(unittest.TestCase):
    """End-to-end tests for the CLI interface."""

    def _run_cli(self, args: list[str]) -> subprocess.CompletedProcess:
        return _run_cli(args)

    def test_cli_basic_export(self):
        with tempfile.TemporaryDirectory() as tmp:
            inp = Path(tmp) / "cards.md"
            out = Path(tmp) / "cards.csv"
            inp.write_text("Q: hello\nA: world\nTags: greet", encoding="utf-8")
            result = _run_cli([str(inp), str(out)])
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Exported 1 cards", result.stdout)

            rows = list(csv.reader(out.read_text(encoding="utf-8-sig").splitlines()))
            self.assertEqual(rows[0], ["Front", "Back", "Tags", "Deck"])
            self.assertEqual(rows[1], ["hello", "world", "greet", ""])

    def test_cli_csv_encoding_utf8_bom(self):
        with tempfile.TemporaryDirectory() as tmp:
            inp = Path(tmp) / "cards.md"
            out = Path(tmp) / "cards.csv"
            inp.write_text("Q: 极限\nA: limit\nTags: 数学", encoding="utf-8")
            result = _run_cli([str(inp), str(out)])
            self.assertEqual(result.returncode, 0, result.stderr)

            content = out.read_bytes()
            # utf-8-sig starts with BOM
            self.assertTrue(content.startswith(b"\xef\xbb\xbf"))

    def test_cli_csv_quote_escaping(self):
        with tempfile.TemporaryDirectory() as tmp:
            inp = Path(tmp) / "cards.md"
            out = Path(tmp) / "cards.csv"
            inp.write_text('Q: What is "hello"?\nA: a greeting', encoding="utf-8")
            result = _run_cli([str(inp), str(out)])
            self.assertEqual(result.returncode, 0, result.stderr)

            content = out.read_text(encoding="utf-8-sig")
            rows = list(csv.reader(io.StringIO(content)))
            # Row 1 should have the quoted value properly escaped
            self.assertIn("hello", rows[1][0])

    def test_cli_file_not_found(self):
        result = self._run_cli(["nonexistent.md", "out.csv"])
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("not found", result.stderr)

    def test_cli_no_cards_parsed(self):
        with tempfile.TemporaryDirectory() as tmp:
            inp = Path(tmp) / "empty.md"
            out = Path(tmp) / "out.csv"
            inp.write_text("Tags: only\n", encoding="utf-8")
            result = _run_cli([str(inp), str(out)])
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("no cards parsed", result.stderr)

    def test_cli_warning_on_skipped_blocks(self):
        with tempfile.TemporaryDirectory() as tmp:
            inp = Path(tmp) / "cards.md"
            out = Path(tmp) / "out.csv"
            inp.write_text("Tags: orphan\n\nQ: valid\nA: ok", encoding="utf-8")
            result = _run_cli([str(inp), str(out)])
            self.assertEqual(result.returncode, 0)
            self.assertIn("Warning: block 1 skipped", result.stderr)

    def test_cli_verbose_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            inp = Path(tmp) / "cards.md"
            out = Path(tmp) / "out.csv"
            inp.write_text("Q: q\nA: a\nTags: t\nDeck: d", encoding="utf-8")
            result = _run_cli([str(inp), str(out), "--verbose"])
            self.assertEqual(result.returncode, 0)
            self.assertIn("Parsed card", result.stderr)

    def test_cli_with_deck_flag(self):
        with tempfile.TemporaryDirectory() as tmp:
            inp = Path(tmp) / "cards.md"
            out = Path(tmp) / "out.csv"
            inp.write_text("Q: q\nA: a", encoding="utf-8")
            result = _run_cli([str(inp), str(out), "--deck", "My Deck"])
            self.assertEqual(result.returncode, 0)

            rows = list(csv.reader(out.read_text(encoding="utf-8-sig").splitlines()))
            self.assertEqual(rows[1][3], "My Deck")

    def test_cli_expand_cloze(self):
        with tempfile.TemporaryDirectory() as tmp:
            inp = Path(tmp) / "cards.md"
            out = Path(tmp) / "out.csv"
            inp.write_text("Cloze: {{c1::A}} + {{c2::B}} = C", encoding="utf-8")
            result = _run_cli([str(inp), str(out), "--expand-cloze"])
            self.assertEqual(result.returncode, 0)
            self.assertIn("Exported 2 cards", result.stdout)

    def test_cli_tsv_format(self):
        with tempfile.TemporaryDirectory() as tmp:
            inp = Path(tmp) / "cards.md"
            out = Path(tmp) / "out.tsv"
            inp.write_text("Q: What is 2+2?\nA: 4\nTags: math", encoding="utf-8")
            result = _run_cli([str(inp), str(out), "--format", "tsv"])
            self.assertEqual(result.returncode, 0)
            content = out.read_text(encoding="utf-8-sig")
            self.assertIn("\t", content)
            rows = list(csv.reader(content.splitlines(), delimiter="\t"))
            self.assertEqual(rows[0], ["Front", "Back", "Tags", "Deck"])
            self.assertEqual(rows[1][0], "What is 2+2?")
            self.assertEqual(rows[1][1], "4")

    def test_cli_multiple_input_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            inp1 = Path(tmp) / "cards1.md"
            inp2 = Path(tmp) / "cards2.md"
            out = Path(tmp) / "combined.csv"
            inp1.write_text("Q: First question\nA: First answer\nTags: set1", encoding="utf-8")
            inp2.write_text("Q: Second question\nA: Second answer\nTags: set2", encoding="utf-8")
            result = _run_cli([str(inp1), str(inp2), str(out)])
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Exported 2 cards", result.stdout)
            # Multi-file runs should report which files were read.
            self.assertIn("Read 2 files", result.stderr)
            rows = list(csv.reader(out.read_text(encoding="utf-8-sig").splitlines()))
            self.assertEqual(len(rows), 3)  # header + 2 cards
            self.assertEqual(rows[1][0], "First question")
            self.assertEqual(rows[2][0], "Second question")

    def test_cli_dedup_across_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            inp1 = Path(tmp) / "cards1.md"
            inp2 = Path(tmp) / "cards2.md"
            out = Path(tmp) / "combined.csv"
            inp1.write_text("Q: Shared\nA: Same\nTags: a", encoding="utf-8")
            inp2.write_text("Q: Shared\nA: Same\nTags: b\n\nQ: Unique\nA: Other", encoding="utf-8")
            result = _run_cli([str(inp1), str(inp2), str(out), "--dedup"])
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Exported 2 cards", result.stdout)
            self.assertIn("removed 1 duplicate", result.stderr)
            rows = list(csv.reader(out.read_text(encoding="utf-8-sig").splitlines()))
            self.assertEqual(len(rows), 3)  # header + 2 unique cards

    def test_cli_no_dedup_keeps_duplicates(self):
        with tempfile.TemporaryDirectory() as tmp:
            inp1 = Path(tmp) / "cards1.md"
            inp2 = Path(tmp) / "cards2.md"
            out = Path(tmp) / "combined.csv"
            inp1.write_text("Q: Shared\nA: Same", encoding="utf-8")
            inp2.write_text("Q: Shared\nA: Same", encoding="utf-8")
            result = _run_cli([str(inp1), str(inp2), str(out)])
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Exported 2 cards", result.stdout)


class CJKAndEdgeCaseTests(unittest.TestCase):
    """Tests for CJK characters, cloze hints, and multi-line pipe blocks."""

    def test_chinese_content_in_cards(self):
        text = "Q: 极限的定义是什么?\nA: 对于任意 epsilon>0...\nTags: 分析, 极限\nDeck: 数学期末"
        cards = parse_cards(text)
        self.assertEqual(len(cards), 1)
        self.assertEqual(cards[0][0], "极限的定义是什么?")
        self.assertIn("分析", cards[0][2])
        self.assertEqual(cards[0][3], "数学期末")

    def test_cloze_hint_preserved_in_default_mode(self):
        text = "Cloze: The limit {{c1::exists::check both sides}} when x approaches a."
        cards = parse_cards(text, expand_cloze=False)
        self.assertEqual(len(cards), 1)
        self.assertIn("{{c1::exists::check both sides}}", cards[0][0])

    def test_multiline_block_with_pipe_not_parsed_as_shorthand(self):
        # A multi-line block containing | should NOT be treated as Front|Back shorthand
        text = "This is a sentence with | in it\nbut it has multiple lines"
        cards = parse_cards(text)
        # Should be skipped because it has no Q:/Front:/Cloze: field and is multi-line
        self.assertEqual(len(cards), 0)

    def test_single_line_pipe_shorthand_still_works(self):
        # Ensure single-line Front|Back still works after the multi-line fix
        cards = parse_cards("Capital of France | Paris")
        self.assertEqual(len(cards), 1)
        self.assertEqual(cards[0][0], "Capital of France")
        self.assertEqual(cards[0][1], "Paris")

    def test_qa_block_with_pipe_in_answer(self):
        # Q:/A: block where the answer contains | should parse correctly
        text = "Q: What is the truth table for AND?\nA: T|T=T, T|F=F, F|T=F, F|F=F"
        cards = parse_cards(text)
        self.assertEqual(len(cards), 1)
        self.assertEqual(cards[0][0], "What is the truth table for AND?")
        self.assertIn("|", cards[0][1])


class PreciseFieldMatchingTests(unittest.TestCase):
    """Tests that field labels are matched precisely (regex-based), not by simple prefix."""

    def test_quote_not_matched_as_q(self):
        # "quote:" should NOT be treated as a Q: field
        text = "quote: hello\nA: world"
        cards = parse_cards(text)
        self.assertEqual(len(cards), 0)

    def test_frontier_not_matched_as_front(self):
        text = "frontier: edge\nA: boundary"
        cards = parse_cards(text)
        self.assertEqual(len(cards), 0)

    def test_cloze_exact_match(self):
        text = "Cloze: {{c1::test}}"
        cards = parse_cards(text)
        self.assertEqual(len(cards), 1)
        self.assertEqual(cards[0][0], "{{c1::test}}")

    def test_case_insensitive_match(self):
        text = "q: lower\nA: a\n\nQ: upper\nA: b\n\nFront: f\nBack: g"
        cards = parse_cards(text)
        self.assertEqual(len(cards), 3)

    def test_spaces_around_colon_allowed(self):
        text = "Q : spaced\nA : also spaced"
        cards = parse_cards(text)
        self.assertEqual(len(cards), 1)
        self.assertEqual(cards[0][0], "spaced")
        self.assertEqual(cards[0][1], "also spaced")


class MultilineValueTests(unittest.TestCase):
    """Tests for multi-line field values (continuation lines)."""

    def test_multiline_answer(self):
        text = "Q: What is the proof?\nA: Step 1: assume x > 0.\nStep 2: derive contradiction.\nTags: math"
        cards = parse_cards(text)
        self.assertEqual(len(cards), 1)
        self.assertEqual(cards[0][0], "What is the proof?")
        self.assertIn("\n", cards[0][1])
        self.assertIn("Step 1: assume x > 0.", cards[0][1])
        self.assertIn("Step 2: derive contradiction.", cards[0][1])
        self.assertEqual(cards[0][2], "math")

    def test_multiline_question(self):
        text = "Q: Consider the function\nf(x) = x^2\nWhat is the derivative?\nA: 2x"
        cards = parse_cards(text)
        self.assertEqual(len(cards), 1)
        self.assertIn("\n", cards[0][0])
        self.assertIn("f(x) = x^2", cards[0][0])

    def test_multiline_cloze(self):
        text = "Cloze: The derivative of\nsin(x) is {{c1::cos(x)}}.\nA: basic trig"
        cards = parse_cards(text)
        self.assertEqual(len(cards), 1)
        self.assertIn("\n", cards[0][0])
        self.assertIn("sin(x)", cards[0][0])


class SpecialCharacterTests(unittest.TestCase):
    """Tests for special characters that need proper CSV escaping."""

    def test_comma_in_content(self):
        text = 'Q: What are a, b, c?\nA: They are variables, constants, and coefficients.'
        cards = parse_cards(text)
        self.assertEqual(len(cards), 1)
        self.assertIn(",", cards[0][0])
        self.assertIn(",", cards[0][1])

    def test_quotes_in_content(self):
        text = 'Q: What does "idempotent" mean?\nA: "f(f(x)) = f(x)"'
        cards = parse_cards(text)
        self.assertEqual(len(cards), 1)
        self.assertIn('"idempotent"', cards[0][0])
        self.assertIn('"f(f(x)) = f(x)"', cards[0][1])

    def test_newline_in_content_preserved(self):
        text = "Q: Line one\nLine two\nA: Answer line one\nAnswer line two"
        cards = parse_cards(text)
        self.assertEqual(len(cards), 1)
        self.assertIn("\n", cards[0][0])
        self.assertIn("\n", cards[0][1])


class StdoutOutputTests(unittest.TestCase):
    """Tests for writing to stdout when output path is '-'."""

    def test_stdout_export(self):
        with tempfile.TemporaryDirectory() as tmp:
            inp = Path(tmp) / "cards.md"
            inp.write_text("Q: hello\nA: world\nTags: greet", encoding="utf-8")
            result = _run_cli([str(inp), "-"])
            self.assertEqual(result.returncode, 0, result.stderr)
            # stdout should contain the CSV data
            self.assertIn("Front,Back,Tags,Deck", result.stdout)
            self.assertIn("hello,world,greet,", result.stdout)
            # stderr should have the summary
            self.assertIn("stdout", result.stderr)


class EmptyFieldTests(unittest.TestCase):
    """Tests for edge cases with empty or minimal fields."""

    def test_empty_q_value_is_skipped(self):
        text = "Q:\nA: nothing"
        cards = parse_cards(text)
        self.assertEqual(len(cards), 0)

    def test_empty_a_value_allowed(self):
        text = "Q: question\nA:"
        cards = parse_cards(text)
        self.assertEqual(len(cards), 1)
        self.assertEqual(cards[0][0], "question")
        self.assertEqual(cards[0][1], "")

    def test_only_front_no_back(self):
        text = "Front: just front"
        cards = parse_cards(text)
        self.assertEqual(len(cards), 1)
        self.assertEqual(cards[0][0], "just front")
        self.assertEqual(cards[0][1], "")


class TSVEdgeCaseTests(unittest.TestCase):
    """Tests for TSV-specific edge cases including tab characters in content."""

    def test_tsv_with_tab_in_content_is_quoted(self):
        # Content containing literal tabs should still produce valid TSV.
        # The csv module handles this by quoting fields that contain the delimiter.
        with tempfile.TemporaryDirectory() as tmp:
            inp = Path(tmp) / "cards.md"
            out = Path(tmp) / "out.tsv"
            inp.write_text("Q: hello\tworld\nA: foo\tbar\nTags: greet", encoding="utf-8")
            result = _run_cli([str(inp), str(out), "--format", "tsv"])
            self.assertEqual(result.returncode, 0, result.stderr)
            content = out.read_text(encoding="utf-8-sig")
            # The TSV should contain the header and one data row
            lines = content.strip().split("\n")
            self.assertEqual(len(lines), 2)
            self.assertIn("Front", lines[0])
            # Tab characters in content are preserved (csv module quotes the field)
            self.assertIn("hello\tworld", lines[1])

    def test_tsv_with_comma_in_content_no_problem(self):
        # Commas in content should not break TSV since delimiter is tab.
        with tempfile.TemporaryDirectory() as tmp:
            inp = Path(tmp) / "cards.md"
            out = Path(tmp) / "out.tsv"
            inp.write_text("Q: a, b, c\nA: x, y, z\nTags: math, logic", encoding="utf-8")
            result = _run_cli([str(inp), str(out), "--format", "tsv"])
            self.assertEqual(result.returncode, 0, result.stderr)
            content = out.read_text(encoding="utf-8-sig")
            lines = content.strip().split("\n")
            self.assertEqual(len(lines), 2)
            # Verify the TSV is parseable: read back with csv.reader
            rows = list(csv.reader(content.splitlines(), delimiter="\t"))
            self.assertEqual(len(rows), 2)
            self.assertEqual(rows[0], ["Front", "Back", "Tags", "Deck"])
            self.assertEqual(rows[1][0], "a, b, c")
            self.assertEqual(rows[1][1], "x, y, z")
            self.assertEqual(rows[1][2], "math, logic")

    def test_tsv_output_is_utf8_bom(self):
        with tempfile.TemporaryDirectory() as tmp:
            inp = Path(tmp) / "cards.md"
            out = Path(tmp) / "out.tsv"
            inp.write_text("Q: 你好\nA: world", encoding="utf-8")
            result = _run_cli([str(inp), str(out), "--format", "tsv"])
            self.assertEqual(result.returncode, 0, result.stderr)
            content = out.read_bytes()
            self.assertTrue(content.startswith(b"\xef\xbb\xbf"))


class ParseStateTests(unittest.TestCase):
    """Tests for the _ParseState class."""

    def test_default_state_has_no_skipped_blocks(self):
        state = _ParseState()
        self.assertEqual(state.skipped_blocks, [])
        self.assertFalse(state.verbose)

    def test_verbose_state(self):
        state = _ParseState(verbose=True)
        self.assertTrue(state.verbose)

    def test_log_verbose_prints_when_verbose(self):
        import io
        state = _ParseState(verbose=True)
        buf = io.StringIO()
        # Redirect stderr temporarily
        import sys as _sys
        old_stderr = _sys.stderr
        try:
            _sys.stderr = buf
            state.log_verbose("test message")
            self.assertIn("test message", buf.getvalue())
        finally:
            _sys.stderr = old_stderr

    def test_log_verbose_silent_when_not_verbose(self):
        import io
        state = _ParseState(verbose=False)
        buf = io.StringIO()
        import sys as _sys
        old_stderr = _sys.stderr
        try:
            _sys.stderr = buf
            state.log_verbose("should not appear")
            self.assertEqual(buf.getvalue(), "")
        finally:
            _sys.stderr = old_stderr

    def test_skipped_blocks_reset_on_parse(self):
        state = _ParseState()
        state.skipped_blocks.append((1, "old"))
        parse_cards("Q: valid\nA: ok", state=state)
        # parse_cards resets skipped_blocks at the start
        self.assertEqual(len(state.skipped_blocks), 0)

    def test_state_passed_to_parse_cards_collects_skipped(self):
        state = _ParseState()
        cards = parse_cards("Tags: only\n\nQ: valid\nA: ok", state=state)
        self.assertEqual(len(cards), 1)
        self.assertEqual(len(state.skipped_blocks), 1)
        self.assertEqual(state.skipped_blocks[0][0], 1)

    def test_parse_cards_without_state_creates_default(self):
        # Backward compatibility: calling without state should work
        cards = parse_cards("Q: x\nA: y")
        self.assertEqual(len(cards), 1)
        self.assertEqual(cards[0][0], "x")


class StdoutEncodingTests(unittest.TestCase):
    """Tests for stdout output path ('-') encoding behavior."""

    def _run_cli_bytes(self, args: list[str]) -> subprocess.CompletedProcess:
        """Run CLI with capture_output=True to get bytes."""
        script = SCRIPT_DIR / "export_flashcards.py"
        return subprocess.run(
            [sys.executable, str(script)] + args,
            capture_output=True,
            cwd=str(SCRIPT_DIR),
        )

    def test_stdout_contains_bom(self):
        with tempfile.TemporaryDirectory() as tmp:
            inp = Path(tmp) / "cards.md"
            inp.write_text("Q: 中文问题\nA: 中文答案\nTags: 标签", encoding="utf-8")
            result = self._run_cli_bytes([str(inp), "-"])
            self.assertEqual(result.returncode, 0, result.stderr.decode())
            # stdout should start with UTF-8 BOM
            self.assertTrue(result.stdout.startswith(b"\xef\xbb\xbf"))

    def test_stdout_csv_structure(self):
        with tempfile.TemporaryDirectory() as tmp:
            inp = Path(tmp) / "cards.md"
            inp.write_text("Q: hello\nA: world\nTags: greet\nDeck: Test", encoding="utf-8")
            result = self._run_cli_bytes([str(inp), "-"])
            self.assertEqual(result.returncode, 0, result.stderr.decode())
            # Skip BOM and decode
            output = result.stdout.decode("utf-8-sig")
            lines = output.strip().split("\r\n")
            self.assertIn("Front,Back,Tags,Deck", lines[0])
            self.assertIn("hello,world,greet,Test", lines[1])

    def test_stdout_stderr_has_summary(self):
        with tempfile.TemporaryDirectory() as tmp:
            inp = Path(tmp) / "cards.md"
            inp.write_text("Q: x\nA: y", encoding="utf-8")
            result = self._run_cli_bytes([str(inp), "-"])
            self.assertEqual(result.returncode, 0, result.stderr.decode())
            stderr_text = result.stderr.decode()
            self.assertIn("stdout", stderr_text)
            self.assertIn("Exported 1 cards", stderr_text)


class DedupTests(unittest.TestCase):
    """Tests for the _dedup_cards helper and the --dedup CLI flag."""

    def _run_cli(self, args: list[str]) -> subprocess.CompletedProcess:
        script = SCRIPT_DIR / "export_flashcards.py"
        return subprocess.run(
            [sys.executable, str(script)] + args,
            capture_output=True,
            text=True,
            cwd=str(SCRIPT_DIR),
        )

    def test_dedup_removes_exact_duplicate(self):
        cards = [
            ("Q1", "A1", "tags", "deck"),
            ("Q2", "A2", "other", "deck2"),
            ("Q1", "A1", "different-tags", "different-deck"),
        ]
        result, removed = _dedup_cards(cards)
        self.assertEqual(removed, 1)
        self.assertEqual(len(result), 2)
        # First occurrence kept
        self.assertEqual(result[0], ("Q1", "A1", "tags", "deck"))
        self.assertEqual(result[1], ("Q2", "A2", "other", "deck2"))

    def test_dedup_no_duplicates(self):
        cards = [
            ("Q1", "A1", "", ""),
            ("Q2", "A2", "", ""),
        ]
        result, removed = _dedup_cards(cards)
        self.assertEqual(removed, 0)
        self.assertEqual(len(result), 2)

    def test_dedup_empty_list(self):
        result, removed = _dedup_cards([])
        self.assertEqual(removed, 0)
        self.assertEqual(result, [])

    def test_dedup_all_duplicates(self):
        cards = [
            ("Q", "A", "t1", "d1"),
            ("Q", "A", "t2", "d2"),
            ("Q", "A", "t3", "d3"),
        ]
        result, removed = _dedup_cards(cards)
        self.assertEqual(removed, 2)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], ("Q", "A", "t1", "d1"))

    def test_dedup_cli_flag(self):
        with tempfile.TemporaryDirectory() as tmp:
            inp = Path(tmp) / "cards.md"
            out = Path(tmp) / "out.csv"
            # Two identical cards + one distinct
            inp.write_text(
                "Q: hello\nA: world\nTags: greet\n\n"
                "Q: hello\nA: world\nTags: other\n\n"
                "Q: unique\nA: answer\n",
                encoding="utf-8",
            )
            result = self._run_cli([str(inp), str(out), "--dedup"])
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Deduplicated: removed 1", result.stderr)
            content = out.read_text(encoding="utf-8-sig")
            rows = list(csv.reader(io.StringIO(content)))
            self.assertEqual(len(rows), 3)  # header + 2 data rows

    def test_dedup_cli_no_duplicates(self):
        with tempfile.TemporaryDirectory() as tmp:
            inp = Path(tmp) / "cards.md"
            out = Path(tmp) / "out.csv"
            inp.write_text(
                "Q: a\nA: 1\n\nQ: b\nA: 2\n",
                encoding="utf-8",
            )
            result = self._run_cli([str(inp), str(out), "--dedup"])
            self.assertEqual(result.returncode, 0, result.stderr)
            # No dedup message should appear
            self.assertNotIn("Deduplicated", result.stderr)

    def test_dedup_cli_with_multiple_input_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            f1 = Path(tmp) / "a.md"
            f2 = Path(tmp) / "b.md"
            out = Path(tmp) / "out.csv"
            f1.write_text("Q: same\nA: answer\n", encoding="utf-8")
            f2.write_text("Q: same\nA: answer\n\nQ: unique\nA: u\n", encoding="utf-8")
            result = self._run_cli([str(f1), str(f2), str(out), "--dedup"])
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Deduplicated: removed 1", result.stderr)
            self.assertIn("Read 2 files", result.stderr)


if __name__ == "__main__":
    unittest.main()
