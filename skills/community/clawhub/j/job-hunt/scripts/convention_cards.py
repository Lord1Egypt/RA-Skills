#!/usr/bin/env python3
"""Print the run-time half of one market-conventions table, verbatim.

An assess run needs four things from each entry: its `id`, the `applies_when`
condition that decides whether the card renders at all, its `review_by` date
(and whether that date has passed), and the reader text it must copy character
for character. The rest of each entry -- `source` with its quotes and `also`
citations, `why`, `added`, `protected_trait_note`, and the table's `unverified`
notes -- is what a maintainer reviews the entry against. It is most of the bytes
(about four fifths of every shipped table, measured 2026-10-24) and none of it may
appear on the card, so reading the whole YAML spent every assessment's context on
text the run is forbidden to use.

Read-only by design. It takes no --workspace, writes nothing and journals no
receipt: it is a lookup, like `check_conventions.py --ci`, and the gate that
judges the card is still `check_assessment.py`, reading the YAML itself. This
script cannot loosen that gate, only feed it:

* the text is printed exactly as `check_conventions.load_market_file` parses it,
  so what the run copies is what `check_assessment.py` compares against (it
  compares with whitespace removed, so the table's hard wraps do not matter);
* "stale" is decided by `check_conventions.check_file`, the same call and the same
  EXPIRED_REVIEW_BY finding `check_assessment.py` turns into its banner
  requirement, and the banner is printed from `report_locales`, the module the
  gate reads its accepted spellings from. Two date comparisons would be two
  answers to "is this card stale?".

Exit 0 = printed (including `--market other`, which has no table by design).
Exit 2 = the table is absent or cannot be parsed; the reason goes to stderr and
nothing to stdout, because a partial card list reads as the complete one.
"""
from __future__ import annotations

import argparse
import datetime
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import check_conventions as conventions  # noqa: E402
import journal  # noqa: E402
import report_locales as locales  # noqa: E402
import vocab  # noqa: E402

TEXT_FIELDS = {"zh": ("text_zh",), "en": ("text_en",), "both": ("text_en", "text_zh")}


def expired_ids(table: pathlib.Path, today: datetime.date) -> set[str]:
    """The ids check_assessment.py will require a stale banner for, derived the way
    it derives them -- from check_file's EXPIRED_REVIEW_BY findings."""
    found = set()
    for finding in conventions.check_file(table, today):
        if finding.startswith("EXPIRED_REVIEW_BY:"):
            found.add(finding.split(":", 1)[1].strip().split()[0])
    return found


def render(table: pathlib.Path, market: str, lang: str, text: str,
           today: datetime.date) -> str:
    entries = conventions.load_market_file(table).get("conventions") or []
    stale = expired_ids(table, today)
    banner = locales.GATE_TEXT[lang]["stale"]
    out = [f"# market: {market} ({len(entries)} entries; runtime fields only, "
           f"verbatim from {table.name})"]
    for entry in entries:
        entry = entry or {}
        entry_id = str(entry.get("id") or "")
        review_by = str(entry.get("review_by") or "")
        out.append("")
        out.append(f"[{entry_id}]")
        out.append(f"applies_when: {str(entry.get('applies_when') or '').strip()}")
        if entry_id in stale:
            out.append(f"review_by: {review_by} -- passed; render with the banner: {banner}")
        else:
            out.append(f"review_by: {review_by}")
        for field in TEXT_FIELDS[text]:
            out.append(f"{field}:")
            out.append(str(entry.get(field) or ""))
    return "\n".join(out) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Print one market table's runtime fields (id, applies_when, "
                    "review_by, reader text) verbatim, for an assess run.")
    parser.add_argument("--market", required=True,
                        choices=tuple(vocab.MARKET_KEYS) + (vocab.NO_MARKET,))
    parser.add_argument("--lang", default="zh", choices=locales.LANGUAGES,
                        help="the user's report language; picks the stale banner and, "
                             "unless --text says otherwise, the reader text "
                             "(zh -> text_zh, en -> text_en, ja/ko/es -> both)")
    parser.add_argument("--text", choices=tuple(TEXT_FIELDS), default=None,
                        help="which sourced text to print: zh, en or both")
    source = parser.add_mutually_exclusive_group()
    source.add_argument("--market-dir", type=pathlib.Path, default=None,
                        help="a directory of <market>.yaml tables (default: the shipped ones)")
    source.add_argument("--table", type=pathlib.Path, default=None,
                        help="one table file, when the session names a table other than "
                             "the shipped one (an eval fixture, for example)")
    parser.add_argument("--today", default=None, help="YYYY-MM-DD, for deterministic tests")
    args = parser.parse_args(argv)

    if args.market == vocab.NO_MARKET:
        print(f"# market: {vocab.NO_MARKET} -- no convention table; render no convention card")
        return 0
    text = args.text or {"zh": "zh", "en": "en"}.get(args.lang, "both")
    today = (datetime.date.fromisoformat(args.today) if args.today
             else datetime.date.today())
    table = args.table or (args.market_dir or conventions.CONVENTIONS_DIR) / f"{args.market}.yaml"
    if not table.is_file():
        print(f"NO_INPUT: {table} not found", file=sys.stderr)
        return 2
    try:
        body = render(table, args.market, args.lang, text, today)
    except journal.YamlUnreadable as exc:
        print(f"{journal.UNREADABLE_INPUT}: {exc}", file=sys.stderr)
        return 2
    sys.stdout.write(body)
    return 0


if __name__ == "__main__":
    from cli_io import configure_output

    configure_output()
    raise SystemExit(main())
