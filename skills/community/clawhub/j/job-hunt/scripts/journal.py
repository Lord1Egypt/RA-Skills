#!/usr/bin/env python3
"""The append-only run journal, the receipt every gate leaves in it, and the one
reader that keeps a malformed input file from skipping both.

Risk-register #12: a gate that was skipped produces no output, and no output
looks exactly like a clean run. So each gate writes one receipt here before it
exits — on every exit path, including the "could not run" one — and a mode may
not claim success without quoting its receipts. The receipt carries the hashes
of what the gate actually read, so "the gate passed" is a claim about specific
bytes rather than about a moment in time.

`load_yaml` lives here rather than in paths.py because it exists FOR that
contract, not as a general YAML utility: its whole job is to turn the three ways
a file can be unusable into the could-not-run receipt above. paths.py is pure
path arithmetic and says so; a reader who found a file-parsing function there
would reasonably conclude the two modules were interchangeable.
"""
from __future__ import annotations

import datetime
import hashlib
import json
import pathlib

import yaml

# The closed set a receipt's verdict may take. The last two are NOT synonyms and
# the difference is load-bearing:
#
#   "recorded"          — the gate ran and has no pass/fail to report. The
#                         assess-mode reporters (consistency, count_coverage,
#                         check_evidence_refs, evidence_blocks) and parse_verdicts
#                         on a cleanly-parsed round. A clean CHECK.
#   "baseline_recorded" — the `--record` half of a two-step gate: it stored a
#                         fingerprint for a later comparison and verified nothing.
#                         SETUP, not a check.
#
# They shared the token "recorded" until 2026-08. check_apply.py treated it as
# passing — correctly, for the reporters — so a workspace that ran only the
# documented mode-entry setup satisfied the one gate whose entire job is proving
# the checks ran, and re-running the setup after a real failure erased it.
VERDICTS = ("pass", "fail", "could_not_run", "recorded", "baseline_recorded")


def append(workspace, record: dict) -> None:
    """Append one JSON record as a line to <workspace>/journal.jsonl."""
    workspace = pathlib.Path(workspace)
    workspace.mkdir(parents=True, exist_ok=True)
    line = json.dumps(record, ensure_ascii=False, sort_keys=True)
    # A killed process writes the newline LAST, so the realistic shape of a
    # crash is a final line with no terminator. Appending straight onto it
    # merged the next receipt into the corrupt line and destroyed BOTH: measured
    # on all four composers, and check_shortlist then exited 0 with empty stdout
    # and no receipt of its own — a silent pass on the first read after a crash,
    # which is exactly when the receipt matters. The corrupt line stays corrupt
    # and JOURNAL_CORRUPT still reports it; the new record is simply not fed
    # into it.
    path = workspace / "journal.jsonl"
    if path.exists() and path.stat().st_size:
        with open(path, "rb") as fh:
            fh.seek(-1, 2)
            if fh.read(1) != b"\n":
                with open(path, "a", encoding="utf-8") as fix:
                    fix.write("\n")
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def sha256_file(path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _decode(path) -> str:
    """Journal text, with an unreadable byte sequence surviving as U+FFFD.

    A killed process cuts the newest line at an arbitrary BYTE, and this file is
    full of `—` and `…` and non-ASCII company names — so the cut lands
    mid-character often. `read_text(encoding="utf-8")` then raises
    UnicodeDecodeError, which took down `corrupt_lines`, `read_receipts`,
    `_records` and `latest_mode_entry` together: the exact scenario
    JOURNAL_CORRUPT exists to report, turned into an unhandled crash, leaving the
    previous `pass` as the newest readable receipt. Replacement characters make
    the line fail to parse, which is what corruption should look like.
    """
    return pathlib.Path(path).read_bytes().decode("utf-8", errors="replace")


def _records(workspace):
    """Every parseable JSON record in the journal, oldest first."""
    path = pathlib.Path(workspace) / "journal.jsonl"
    if not path.exists():
        return []
    out = []
    for line in _decode(path).splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue          # a half-written line must not blind the reader
        if isinstance(rec, dict):
            out.append(rec)
    return out


def corrupt_lines(workspace) -> list:
    """1-based line numbers of journal lines that are not parseable records.

    Separate from `_records` on purpose. Dropping a bad line is right for
    READING — a truncated line must not blind a later gate to an earlier one,
    which test_journal.py pins — but silently dropping it is wrong for
    COMPOSING. `read_receipts` returns each gate's receipts oldest-first and
    check_apply trusts `receipts[-1]`, so a truncated NEWEST receipt promotes
    the previous one: a run whose final act was writing
    `UNSOURCED: 'Kubernetes' appears in the CV and in no evidence block`, cut
    short by a killed process or a full disk, was reported as a clean package.

    check_opencli_result already keeps its corruption rather than dropping it.
    One file, two opposite policies, and the failing-open reader was the one
    that authorises hand-off.
    """
    path = pathlib.Path(workspace) / "journal.jsonl"
    if not path.exists():
        return []
    bad = []
    for number, line in enumerate(_decode(path).splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            bad.append(number)
            continue
        if not isinstance(rec, dict):
            bad.append(number)
    return bad


def current_mode(workspace) -> str:
    """The mode of the most recent mode_entry record, or "unknown".

    Read from the journal, never guessed. The obvious alternative — an
    environment variable with a default — is worse than useless here: nothing
    in any mode sets it, so every receipt written by discover, assess and
    interview would be stamped with the default and a journal read months later
    would be confidently wrong about which mode produced which evidence.
    "unknown" is the honest answer when nothing recorded an entry, and it is
    also the shape check_apply's NO_MODE_ENTRY finding exists to catch.
    """
    mode = "unknown"
    for rec in _records(workspace):
        if rec.get("action") == "mode_entry" and rec.get("mode"):
            mode = str(rec["mode"])
    return mode


def receipt(workspace, gate: str, input_hashes: dict, verdict: str,
            findings=None, extra: dict = None) -> dict:
    """Build, journal and return one gate receipt.

    `verdict` is one of `VERDICTS` above: "pass" | "fail" | "could_not_run" |
    "recorded" | "baseline_recorded" — read that comment before picking one, the
    last two mean different things. `mode`
    is read from the latest mode_entry record in this workspace's journal
    (see current_mode) rather than passed in, because the gate signature is
    fixed by the shared contract and does not carry it.
    """
    record = {
        "ts": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "mode": current_mode(workspace),
        "action": "gate",
        "gate": gate,
        "input_hashes": dict(input_hashes or {}),
        "verdict": verdict,
        "findings": list(findings or []),
    }
    # `extra` carries facts ABOUT the run that are not file hashes — `round` is
    # the one that matters. It cannot go in `input_hashes`: that map is now
    # re-verified against disk by check_apply, so a non-path key there would be
    # looked up as a filename and reported missing.
    for key, value in (extra or {}).items():
        if key not in record:
            record[key] = value
    record["receipt_hash"] = _receipt_hash(record)
    append(workspace, record)
    # Every gate writes its receipt through here, so this is the one place that
    # can tell a reader a green light is not the finish line — and the one place
    # a gate added later inherits it from, rather than 25 copies to keep in step.
    if verdict == "pass":
        import cli_io
        cli_io.pass_notice(gate, record.get("mode"))
    return record


def _receipt_hash(record: dict) -> str:
    """The hash over a receipt's own fields, `receipt_hash` itself excluded.

    Excluding it is what makes the value reproducible from the record as read
    back, so `receipt_intact` can recompute rather than trust.
    """
    payload = json.dumps({k: v for k, v in record.items() if k != "receipt_hash"},
                         ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def sign_receipt(record: dict) -> dict:
    """A copy of `record` carrying the hash `receipt()` would have given it.

    For callers that must build a well-formed receipt without going through
    `receipt()` — test fixtures that seed an upstream gate's result without
    running it. Exposed rather than hidden: `receipt_intact` is tamper EVIDENCE,
    not a security boundary, so a private signer would only have meant fixtures
    reaching into `_receipt_hash` anyway. A fixture that hand-writes an UNSIGNED
    receipt is simulating a forgery, which is a different test.
    """
    signed = {k: v for k, v in record.items() if k != "receipt_hash"}
    signed["receipt_hash"] = _receipt_hash(signed)
    return signed


def receipt_intact(record: dict) -> bool:
    """Was this receipt written by `receipt()` and unedited since?

    The hash was computed and journalled from the day receipts existed and read
    back by nothing, which made every receipt trust-on-write: a run could append
    `{"action":"gate","gate":"check_claims","verdict":"pass","input_hashes":{}}`
    by hand and check_apply exited 0 on it. Measured 2026-09-05 on a workspace
    whose only real receipt was a FAILING one.

    This is tamper EVIDENCE, not a security boundary — anything that can write
    the journal can also run this function. What it buys is that a hand-written
    "the gate passed" line no longer looks like a gate that passed, which is the
    failure mode this skill actually has: not an attacker, a model taking a
    shortcut and a reader who cannot tell.
    """
    if not isinstance(record, dict):
        return False
    hashes = record.get("input_hashes", {})
    findings = record.get("findings", [])
    if (not isinstance(hashes, dict)
            or any(not isinstance(k, str) or not isinstance(v, str) for k, v in hashes.items())
            or not isinstance(findings, list)
            or any(not isinstance(f, str) for f in findings)):
        return False
    if record.get("action") == "gate" and not isinstance(record.get("gate"), str):
        return False
    recorded = record.get("receipt_hash")
    return isinstance(recorded, str) and recorded == _receipt_hash(record)


def read_receipts(workspace, gate: str | None = None) -> list:
    """Every gate receipt in the journal, oldest first, optionally one gate.

    Returns them ALL, intact or not. Filtering the unverifiable out here would
    turn a forged receipt into a MISSING_RECEIPT, which reads as "the gate was
    never run" and sends the reader looking for the wrong thing; worse, dropping
    a forged PASS could promote an older genuine FAIL into last position and be
    read as the current state. Composers call `unverified_receipts` and report.
    """
    return [rec for rec in _records(workspace)
            if rec.get("action") == "gate"
            and (gate is None or rec.get("gate") == gate)]


def unverified_receipts(workspace) -> list:
    """[(gate, index)] for every gate receipt whose hash does not check out."""
    out = []
    for index, rec in enumerate(read_receipts(workspace), 1):
        if not receipt_intact(rec):
            out.append((str(rec.get("gate")), index))
    return out


# --------------------------------------------------------------- reading YAML input

# The code every gate prints and journals when an input file is present and
# unusable. Deliberately NOT "NO_INPUT", which the same gates use for a file that
# is absent: a reader told NO_INPUT goes looking for a file that is right there,
# and "the file could not be parsed" is a different instruction from "the file
# says something wrong".
UNREADABLE_INPUT = "UNREADABLE_INPUT"


def as_mapping(item):
    """A row as a dict, or an empty dict if it is anything else.

    The idiom this replaces was `(row or {})`, which guards None and every falsy
    value and NOT a non-empty string — so a requirement written `- R1` instead of
    `- {id: R1, ...}`, one missing `id:` in hand-written YAML, raised
    AttributeError deep inside a generator. Measured 2026-09-05: count_coverage
    and consistency both exited 1 with no finding and NO RECEIPT, which is
    indistinguishable from a gate nobody ran.

    Reporting the bad row is count_coverage's job (INVALID_ROW). This just stops
    every OTHER reader of the same list from crashing before it gets there.
    """
    return item if isinstance(item, dict) else {}


class YamlUnreadable(Exception):
    """An input file could not be turned into the document shape a gate expects.

    Carries `.path`, `.reason` and `.finding` — the last already prefixed with
    UNREADABLE_INPUT, so a gate routing this into its cannot_run path does not
    have to re-spell the code and cannot spell it differently from its neighbour.
    """

    def __init__(self, path, reason: str):
        self.path = pathlib.Path(path)
        self.reason = reason
        super().__init__(f"{self.path}: {reason}")

    @property
    def finding(self) -> str:
        return f"{UNREADABLE_INPUT}: {self.path}: {self.reason}"


_EMPTY = {dict: "mapping", list: "list"}


def load_yaml(path, expect: type = dict):
    """Parse a YAML file into `expect` (dict or list), or raise YamlUnreadable.

    WHY THIS EXISTS — reproduced 2026-08-16, and worth reading before anyone
    "simplifies" it back to `yaml.safe_load(path.read_text(...)) or {}`. On a
    workspace whose fit-assessment.yaml had one unclosed quote:

        consistency          exit=1   (a yaml parse traceback)
        count_coverage       exit=1   (a yaml parse traceback)
        journal.jsonl        2 lines  — only from the gates that exited 2 cleanly

    In this repo's contract exit 1 means "the gate ran and found problems". So a
    caller reading exit codes was told there were findings, a caller reading the
    journal saw nothing, and check_apply — whose whole composition rule is reading
    those receipts — saw a gate that never ran. The one state the journal exists to
    make visible was the one state that produced no journal line. There were 25
    `yaml.safe_load` call sites and 8 of them caught YAMLError.

    Three failures land in that same place and all three are handled here:

      * the document does not parse (yaml.YAMLError);
      * the file cannot be read at all — absent, unreadable, not UTF-8 (OSError,
        UnicodeDecodeError);
      * the document parses to a string or a list where a mapping is expected, so
        the caller's very next `.get()` raises AttributeError.

    An empty or comment-only file is NOT one of those: it yields the empty mapping
    (or list), which is what every call site's `or {}` meant and what the callers
    downstream are written against.

    The caller catches YamlUnreadable and routes it to its own cannot_run / exit-2
    path, so the workspace-does-not-exist exception stays where each gate documents
    it: nothing to append to, stderr only, no receipt.
    """
    if expect not in _EMPTY:
        raise ValueError(f"expect must be dict or list, not {expect!r}")
    path = pathlib.Path(path)
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise YamlUnreadable(path, f"is not valid UTF-8 ({exc.reason})") from exc
    except OSError as exc:
        raise YamlUnreadable(
            path, f"could not be read ({exc.strerror or exc})") from exc
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        detail = " ".join(str(exc).split())
        raise YamlUnreadable(path, f"did not parse as YAML ({detail})") from exc
    if data is None:
        return expect()
    if not isinstance(data, expect):
        raise YamlUnreadable(
            path,
            f"parses to a {type(data).__name__}, not a {_EMPTY[expect]} — "
            f"the gate reads named fields off it and cannot read them off this")
    return data


def require_lists(data: dict, path, **fields) -> None:
    """Validate collection shape before iterating model-authored input.

    Missing/null fields remain the domain gate's decision. A supplied scalar or
    mapping is never an empty list, and iterating a string character by character
    is never a valid interpretation. Values in fields specify an optional item
    type (dict/str), or None when the caller diagnoses individual bad rows.
    """
    for name, item_type in fields.items():
        value = data.get(name)
        if value is None:
            continue
        if not isinstance(value, list):
            raise YamlUnreadable(path, f"{name} must be a list, not {type(value).__name__}")
        if item_type is not None:
            for index, item in enumerate(value):
                if not isinstance(item, item_type):
                    raise YamlUnreadable(path, f"{name}[{index}] must be {item_type.__name__}")
