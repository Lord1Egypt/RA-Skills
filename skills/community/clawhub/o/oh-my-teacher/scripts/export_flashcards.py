#!/usr/bin/env python3
"""Convert Markdown flashcards to Anki/Quizlet-friendly CSV or TSV.

Input formats supported per card block (blank lines separate cards):

  Q: question
  A: answer
  Tags: tag1, tag2
  Deck: deck name

  Cloze: The limit {{c1::exists}} when ...
  A: optional notes
  Tags: limits

  Front | Back

  Q: [Bi-directional] question
  A: answer

CSV columns: Front, Back, Tags, Deck (use --format tsv for tab-separated output)

When a Q: or Front: field starts with `[Bi-directional]`, the script emits
two CSV rows: the original card (front → back) plus a reversed card
(back → front). This saves the user from duplicating cards manually in
Anki's Basic (and reversed card) note type.

By default, Cloze blocks are emitted as a single CSV row containing the
original {{c1::...}} syntax, which is what Anki's Cloze note type expects
on import. With --expand-cloze, blocks that contain more than one cloze
number are expanded into one CSV row per cloze number, with the target
cloze blanked and the other clozes' answers revealed. This second format
works for Quizlet and any tool that does not understand Anki cloze syntax.
Cloze hints (the {{c1::answer::hint}} form) are preserved on the
{{c1::...}} row but dropped on the expanded rows; use the default mode
when hints matter.
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

Card = tuple[str, str, str, str]

CLOZE_PATTERN = re.compile(r"\{\{c(\d+)::(.+?)(?:::([^}]*))?\}\}")

# More precise field matcher: avoids matching "quote:" as "q:" etc.
_FIELD_RE = re.compile(
    r"^(?P<key>Q|Front|A|Back|Cloze|Tags|Deck)\s*:\s*(?P<value>.*)$",
    re.IGNORECASE,
)

_BI_RE = re.compile(r"^\[Bi-directional]\s*(.*)$", re.IGNORECASE)


class _ParseState:
    """Encapsulates mutable state during a parse run, avoiding module-level globals."""

    def __init__(self, verbose: bool = False) -> None:
        self.verbose = verbose
        self.skipped_blocks: list[tuple[int, str]] = []

    def log_verbose(self, msg: str) -> None:
        if self.verbose:
            print(msg, file=sys.stderr)


def _expand_clozes(text: str) -> list[tuple[str, str]] | None:
    """Return one (front, back) pair per unique cloze number.

    Returns None when the text has no clozes or only one cloze number; in
    that case the caller should keep the original cloze syntax so the card
    stays compatible with Anki's Cloze note type.
    """
    matches = list(CLOZE_PATTERN.finditer(text))
    if not matches:
        return None
    numbers = sorted({int(m.group(1)) for m in matches})
    if len(numbers) <= 1:
        return None

    cards: list[tuple[str, str]] = []
    for n in numbers:
        def _blank_target(m: re.Match[str], target: int = n) -> str:
            return "____" if int(m.group(1)) == target else f"[{m.group(2)}]"

        def _reveal_all(m: re.Match[str]) -> str:
            return f"[{m.group(2)}]"

        front = CLOZE_PATTERN.sub(_blank_target, text)
        back = CLOZE_PATTERN.sub(_reveal_all, text)
        cards.append((front, back))
    return cards


def parse_cards(
    text: str,
    default_deck: str = "",
    expand_cloze: bool = False,
    state: _ParseState | None = None,
) -> list[Card]:
    if state is None:
        state = _ParseState()
    state.skipped_blocks = []

    cards: list[Card] = []
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    blocks = [block.strip() for block in re.split(r"\n\s*\n", normalized) if block.strip()]

    for block_idx, block in enumerate(blocks):
        lines = [line.strip().lstrip("\ufeff") for line in block.splitlines() if line.strip()]
        if not lines:
            continue

        front = ""
        back = ""
        tags = ""
        deck = default_deck

        _current_field: str | None = None
        for line in lines:
            m = _FIELD_RE.match(line)
            if m:
                key = m.group("key").lower()
                value = m.group("value")
                _current_field = key
                if key in ("q", "front"):
                    front = value
                elif key in ("a", "back"):
                    back = value
                elif key == "cloze":
                    front = value
                elif key == "tags":
                    tags = value
                elif key == "deck":
                    deck = value
            elif _current_field is not None:
                # Append continuation lines to the current multi-line field.
                if _current_field in ("q", "front"):
                    front += "\n" + line
                elif _current_field in ("a", "back"):
                    back += "\n" + line
                elif _current_field == "cloze":
                    front += "\n" + line
                elif _current_field == "tags":
                    tags += "\n" + line
                elif _current_field == "deck":
                    deck += "\n" + line

        if (
            not front
            and not back
            and len(lines) == 1
            and "|" in block
            and not any(_FIELD_RE.match(line) for line in lines)
        ):
            parts = block.split("|", 1)
            front, back = parts[0].strip(), parts[1].strip()

        if not front:
            preview = block[:80].replace("\n", "\\n")
            state.skipped_blocks.append((block_idx + 1, preview))
            continue

        # Check for [Bi-directional] marker
        bi_match = _BI_RE.match(front) if front else None
        if bi_match:
            front = bi_match.group(1)
            bidirectional = True
        else:
            bidirectional = False

        expansions = _expand_clozes(front) if expand_cloze else None
        if expansions:
            for exp_front, exp_back in expansions:
                cards.append((exp_front, exp_back or back, tags, deck))
                if bidirectional and exp_back:
                    cards.append((exp_back, exp_front, tags, deck))
        else:
            cards.append((front, back, tags, deck))
            if bidirectional and back:
                cards.append((back, front, tags, deck))

        state.log_verbose(f"  Parsed card {len(cards)}: front={front[:60]!r} deck={deck!r} tags={tags!r}")

    return cards


def _dedup_cards(cards: list[Card]) -> tuple[list[Card], int]:
    """Remove cards with a duplicate (Front, Back) pair, keeping the first.

    Tags and Deck are ignored for the duplicate key so that the same Q/A pair
    tagged differently across files still collapses to one card. Returns the
    deduplicated list and the count of removed cards.
    """
    seen: set[tuple[str, str]] = set()
    result: list[Card] = []
    removed = 0
    for card in cards:
        key = (card[0], card[1])
        if key in seen:
            removed += 1
            continue
        seen.add(key)
        result.append(card)
    return result, removed


def main() -> int:
    parser = argparse.ArgumentParser(description="Export Markdown flashcards to CSV or TSV.")
    parser.add_argument("input", nargs="+", help="Markdown flashcard file(s) or glob pattern(s)")
    parser.add_argument("output", help="Output path (CSV or TSV)")
    parser.add_argument(
        "--format",
        choices=("csv", "tsv"),
        default="csv",
        help="Output format: csv (default) or tsv (tab-separated, better for Anki import when fields contain commas).",
    )
    parser.add_argument(
        "--deck",
        default="",
        help="Default deck name when a card omits Deck:",
    )
    parser.add_argument(
        "--expand-cloze",
        action="store_true",
        help="Expand multi-cloze blocks into one CSV row per cloze number, "
        "with the target cloze blanked and others revealed.",
    )
    parser.add_argument(
        "--dedup",
        action="store_true",
        help="Drop duplicate cards (same Front and Back) when merging multiple files. "
        "Keeps the first occurrence and reports how many were removed.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print each parsed card and skipped block details to stderr.",
    )
    args = parser.parse_args()

    state = _ParseState(verbose=args.verbose)

    # Collect all files from input arguments (support glob patterns)
    input_files: list[Path] = []
    for input_arg in args.input:
        arg_path = Path(input_arg)
        if arg_path.is_file():
            input_files.append(arg_path)
        elif "*" in input_arg or "?" in input_arg:
            # Glob expansion — use the parent directory from the pattern
            glob_base = arg_path.parent if str(arg_path.parent) != "." else Path(".")
            pattern = arg_path.name
            matches = list(glob_base.glob(pattern))
            if matches:
                input_files.extend(m for m in matches if m.is_file())
            else:
                print(f"Warning: glob pattern matched no files: {input_arg}", file=sys.stderr)
        else:
            print(f"Error: input file not found: {input_arg}", file=sys.stderr)
            return 1

    if not input_files:
        print(f"Error: no input files found from arguments: {args.input}", file=sys.stderr)
        return 1

    # Report which files were actually read so glob expansion is never silent.
    if len(input_files) > 1:
        names = ", ".join(str(f) for f in input_files)
        print(f"Read {len(input_files)} files: {names}", file=sys.stderr)

    # Read and concatenate all files
    combined_text = ""
    for source in input_files:
        combined_text += source.read_text(encoding="utf-8") + "\n\n"

    cards = parse_cards(
        combined_text,
        default_deck=args.deck,
        expand_cloze=args.expand_cloze,
        state=state,
    )

    # Optionally drop duplicate cards (same Front and Back), keeping first occurrence.
    if args.dedup:
        cards, removed = _dedup_cards(cards)
        if removed:
            print(f"Deduplicated: removed {removed} duplicate card(s).", file=sys.stderr)

    # Report skipped blocks as warnings.
    if state.skipped_blocks:
        for block_num, preview in state.skipped_blocks:
            print(
                f"Warning: block {block_num} skipped (no front/Q/Cloze field): {preview}",
                file=sys.stderr,
            )

    if not cards:
        print(
            "Error: no cards parsed. Use Q:/A:, Cloze:, or 'Front | Back' blocks separated by blank lines.",
            file=sys.stderr,
        )
        if state.skipped_blocks:
            print(
                f"  ({len(state.skipped_blocks)} block(s) were skipped — see warnings above for details)",
                file=sys.stderr,
            )
        return 1

    delimiter = "\t" if args.format == "tsv" else ","

    # Support "-" as stdout
    if args.output == "-":
        import io
        handle = io.StringIO(newline="")
        writer = csv.writer(handle, delimiter=delimiter)
        writer.writerow(["Front", "Back", "Tags", "Deck"])
        writer.writerows(cards)
        sys.stdout.buffer.write(handle.getvalue().encode("utf-8-sig"))
        print(f"\nExported {len(cards)} cards to stdout", file=sys.stderr)
        return 0

    target = Path(args.output)
    with target.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.writer(handle, delimiter=delimiter)
        writer.writerow(["Front", "Back", "Tags", "Deck"])
        writer.writerows(cards)

    print(f"Exported {len(cards)} cards to {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
