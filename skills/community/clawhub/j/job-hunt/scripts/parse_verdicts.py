#!/usr/bin/env python3
"""Parse the three judges' VERDICT blocks into judge-round-<n>.json.

Every agent file ends with "The orchestrator parses this block programmatically
— formatting must be exact", and until now no such program existed: the
orchestrator was a model reading prose. Three things move into code here, and
each of them is a place where a charitable read produces a package that looks
fully reviewed and is not:

  * anything other than exactly PASS or REJECT is AMBIGUOUS, and AMBIGUOUS means
    re-dispatch that judge — fail-closed, never "close enough to a pass";
  * combined PASS requires all three, because each agent file states only its own
    bar and none of them knows it is being ANDed;
  * LEVELING and STANDOUT_SIGNAL are extracted but do not touch the verdict —
    treating them as gates stalls a package that should pass, ignoring them drops
    the highest-value tailoring instruction the loop produces.

Exit 0 = all three returned exactly PASS. Exit 1 = REJECT or AMBIGUOUS (i.e. the
round needs another pass; findings on stdout). Exit 2 = a transcript is missing.
"""
from __future__ import annotations

import argparse
import datetime
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import journal
import rounds

GATE = "parse_verdicts"
JUDGES = ("ats", "recruiter", "hiring_manager")

SINGLE_LINE_FIELDS = ("VERDICT", "COVERAGE", "SCREEN_NOTE", "LEVELING", "STANDOUT_SIGNAL")
LIST_FIELDS = ("NON_KEYWORD_REQUIREMENTS", "MISSING_OR_WEAK", "FORMAT_ISSUES", "TOP_FEEDBACK",
               "SUPPLEMENTARY_QUESTIONS_FOR_CANDIDATE")
BLOCK_FIELDS = ("SCORES",)

_KEY_RE = re.compile(r"^\s{0,3}(?P<key>[A-Za-z][A-Za-z_]{2,})\s*:\s*(?P<rest>.*)$")
_BULLET_RE = re.compile(r"^\s*[-*]\s+(?P<text>.*?)\s*$")
_SCORE_RE = re.compile(r"^\s+(?P<name>[A-Za-z_]+)\s*:\s*(?P<value>.*?)\s*$")
_ALL_KEYS = set(SINGLE_LINE_FIELDS) | set(LIST_FIELDS) | set(BLOCK_FIELDS)


def _key_at(line):
    m = _KEY_RE.match(line)
    if not m:
        return None, None
    key = m.group("key").upper()
    return (key, m.group("rest").strip()) if key in _ALL_KEYS else (None, None)


def _key_positions(lines):
    """{KEY: index of its LAST occurrence}.

    Last, not first: a judge that has read its own agent file (opened by path,
    or pasted in by the fallback dispatch) can echo the template block and two
    worked examples, each containing a literal VERDICT line. The output contract
    says the real block is the last thing in the reply.
    """
    pos = {}
    for i, line in enumerate(lines):
        key, _ = _key_at(line)
        if key:
            pos[key] = i
    return pos


def _stop(line):
    """True at the end of a field's body."""
    if _key_at(line)[0]:
        return True
    stripped = line.strip()
    return bool(stripped) and not stripped.startswith("```") \
        and not _BULLET_RE.match(line)


def _collect_bullets(lines, start):
    out = []
    for line in lines[start + 1:]:
        if _stop(line):
            break
        m = _BULLET_RE.match(line)
        if m and m.group("text").strip():
            out.append(m.group("text").strip())
    if len(out) == 1 and out[0].lower() == "none":
        return []
    return out


def _collect_scores(lines, start):
    out = {}
    for line in lines[start + 1:]:
        if _key_at(line)[0]:
            break
        m = _SCORE_RE.match(line)
        if m:
            out[m.group("name")] = m.group("value")
        elif line.strip() and not line.strip().startswith("```"):
            break
    return out


def parse_judge(text: str) -> dict:
    lines = text.replace("\r\n", "\n").split("\n")
    pos = _key_positions(lines)
    fields = {}
    for key in SINGLE_LINE_FIELDS:
        if key in pos:
            fields[key.lower()] = _key_at(lines[pos[key]])[1]
    for key in LIST_FIELDS:
        if key in pos:
            fields[key.lower()] = _collect_bullets(lines, pos[key])
    for key in BLOCK_FIELDS:
        if key in pos:
            fields[key.lower()] = _collect_scores(lines, pos[key])
    raw = fields.pop("verdict", None)
    token = (raw or "").strip().upper()
    fields["verdict_line"] = raw
    fields["verdict"] = token if token in ("PASS", "REJECT") else "AMBIGUOUS"
    return fields


def combine(judges: dict) -> str:
    verdicts = [judges[j]["verdict"] for j in JUDGES]
    if all(v == "PASS" for v in verdicts):
        return "PASS"
    if any(v == "AMBIGUOUS" for v in verdicts):
        return "AMBIGUOUS"
    return "REJECT"


def _relative(path, ws) -> str:
    """A receipt key check_apply can resolve back to a file.

    Falls back to the absolute path when the file lives outside the workspace —
    which is loud rather than silent: check_apply will report it missing instead
    of skipping it, and a judge transcript stored outside the workspace is worth
    reporting.
    """
    path, ws = pathlib.Path(path), pathlib.Path(ws)
    try:
        return path.resolve().relative_to(ws.resolve()).as_posix()
    except ValueError:
        return str(path)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workspace", required=True)
    ap.add_argument("--round", type=int, required=True)
    ap.add_argument("--ats", required=True)
    ap.add_argument("--recruiter", required=True)
    ap.add_argument("--hiring-manager", dest="hiring_manager", required=True)
    args = ap.parse_args(argv)

    ws = pathlib.Path(args.workspace)
    if not ws.is_dir():
        # journal.receipt() would mkdir it, and a gate that creates the
        # workspace it is auditing has manufactured its own evidence.
        print(f"cannot run {GATE}: workspace {ws} does not exist", file=sys.stderr)
        return 2
    paths = {"ats": pathlib.Path(args.ats),
             "recruiter": pathlib.Path(args.recruiter),
             "hiring_manager": pathlib.Path(args.hiring_manager)}
    for name, p in paths.items():
        if not p.exists():
            journal.receipt(ws, GATE, {}, "could_not_run", [f"MISSING_INPUT: {p}"])
            print(f"cannot run {GATE}: {name} transcript {p} does not exist",
                  file=sys.stderr)
            return 2

    distinct = {p.resolve() for p in paths.values()}
    if len(distinct) < len(paths):
        journal.receipt(ws, GATE, {}, "could_not_run",
                        ["SAME_TRANSCRIPT: the three judges are not three files"])
        print(f"cannot run {GATE}: --ats, --recruiter and --hiring-manager resolve "
              f"to {len(distinct)} distinct file(s), not 3. The review loop's whole "
              f"claim is that three INDEPENDENT judges agreed; one file read three "
              f"times is one judge, and the receipt's input_hashes would collapse "
              f"to a single entry and hide it.", file=sys.stderr)
        return 2

    judges = {n: parse_judge(p.read_text(encoding="utf-8")) for n, p in paths.items()}
    combined = combine(judges)
    redispatch = [n for n in JUDGES if judges[n]["verdict"] == "AMBIGUOUS"]

    findings = []
    for name in JUDGES:
        j = judges[name]
        if j["verdict"] == "AMBIGUOUS":
            if j["verdict_line"] is None:
                findings.append(f"NO_VERDICT: {name} emitted no VERDICT: line — "
                                f"re-dispatch this judge")
            else:
                findings.append(f"AMBIGUOUS: {name} returned {j['verdict_line']!r}, "
                                f"which is not exactly PASS or REJECT — re-dispatch "
                                f"this judge")
        elif j["verdict"] == "REJECT":
            findings.append(f"REJECT: {name} returned REJECT")

    rounds.merge_round(ws, args.round, {
        "round": args.round,
        "parsed_at": datetime.datetime.now(datetime.timezone.utc)
                             .strftime("%Y-%m-%dT%H:%M:%SZ"),
        "judges": judges,
        "combined_verdict": combined,
        "redispatch": redispatch,
    })
    hashes = {_relative(p, ws): journal.sha256_file(p) for p in paths.values()}
    previous = [r for r in journal.read_receipts(ws, GATE)
                if r.get("round") is not None and int(r["round"]) != int(args.round)]
    stale_round = bool(
        previous
        and set((previous[-1].get("input_hashes") or {}).values()) == set(hashes.values()))
    if stale_round:
        # Stamping the round forced the parser to RUN for round n; it did not force
        # it to run on round n's JUDGEMENTS. Re-parsing the previous round's
        # transcripts produced a correctly-stamped receipt for a round nobody judged.
        findings.append(
            f"SAME_JUDGEMENTS_AS_ROUND_{previous[-1]['round']}: the three transcripts "
            f"are byte-identical to the ones parsed for round "
            f"{previous[-1]['round']}. Re-parsing an earlier round's replies is not a "
            f"new round — dispatch the judges again against the current package")
    for f in findings:
        print(f)
    # The receipt reports on the PARSE, not on the round. A round that parsed
    # cleanly is a successful parse whatever the three judges said, so it is
    # "recorded"; the REJECT itself is carried by judge-round-<n>.json, which
    # check_apply.py reads separately and acts on.
    #
    # Writing "fail" here made the honest-stretch branch unreachable. This gate is
    # in check_apply.REQUIRED_GATES, so every REJECT round failed the composer —
    # and the entire honest-stop.yaml path, validated four findings deep and the
    # reason that code exists, could never reach exit 0. A stretch candidate whose
    # application was as strong as it could truthfully be was told the run failed.
    #
    # "fail" is kept for the parse that produced no usable verdict (AMBIGUOUS /
    # NO_VERDICT). Exempting this gate from the composer outright would have been
    # the wrong fix: combine() also returns AMBIGUOUS when a judge emitted nothing,
    # and a round nobody judged would then exit 0 behind an honest-stop.yaml —
    # one silent failure traded for another.
    # `round` is recorded because check_apply reads the LATEST parse_verdicts
    # receipt and, without it, could not tell which round that receipt was for.
    # From round 2 onward that gap was a bypass: skip `parse_verdicts --round 2`,
    # hand-write `combined_verdict: "PASS"` into judge-round-2.json, and the
    # package went out over a round the judges had rejected — round 1's receipt
    # vouching for it. Round 1 alone was protected, by MISSING_RECEIPT.
    # Keyed by WORKSPACE-RELATIVE PATH, not by judge name. `input_hashes` is now
    # re-verified against disk by check_apply, and a key like "ats" names no
    # file, so the three judge transcripts — the evidence the whole review loop
    # rests on — would have been the one required gate whose receipt could not be
    # checked. Nothing reads these keys by name (the path-keyed map
    # check_render_freshness uses is a different field, `dispatch.input_hashes`).
    # `stale_round` joins AMBIGUOUS for the same reason: neither produced a
    # usable verdict FOR THIS ROUND. It printed the finding and exited 0 with a
    # "recorded" receipt, so check_apply — which reads that receipt and its round
    # stamp — passed a round nobody judged. That is the bypass the round stamp was
    # added to close, reopened one level up.
    journal.receipt(ws, GATE, hashes,
                    "fail" if combined == "AMBIGUOUS" or stale_round else "recorded",
                    findings, extra={"round": int(args.round)})
    if stale_round:
        return 1
    return 0 if combined == "PASS" else 1


if __name__ == "__main__":
    from cli_io import configure_output

    configure_output()
    sys.exit(main())
