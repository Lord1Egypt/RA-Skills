#!/usr/bin/env python3
"""Gate: apply mode may not claim success without evidence for each claim.

Composition, not new judgement. Each upstream gate already decided one thing;
this asserts that each of them actually ran, on this workspace, and passed —
because a skipped script produces no output and no output is exactly what a
clean run looks like.

Three rules make "actually ran" mean something, and each closes a way this gate
used to write `pass` over a run that had not been checked:

  * A `--record` receipt is SETUP, not a check. modes/apply.md runs check_claims
    and check_render_freshness with --record at mode entry and before dispatch;
    both store a baseline and verify nothing, and both say "baseline_recorded"
    so this gate can tell them from a verification pass. NOT_VERIFIED — never
    UPSTREAM_FAILED, because nothing failed.
  * Some gates are required only when their input is on disk. The trigger is a
    file, read by conditional_gates(), so "it did not apply" is never guesswork.
  * ANY gate whose latest receipt in this journal says `fail` blocks the package,
    named on either list or not. Enumerating gates does not keep up with the
    gates: check_pages and check_word_limits were both off the list, so either
    could run, print CV_TOO_LONG or OVER_LIMIT, write `verdict: fail`, and have
    this gate write its own `pass` three lines below it in the same file.

Two things it adds. First, the round must have PASSed or the run must record an
honest stop that is classified: **poorly built** (a fixable tailoring miss) or
**honest stretch** (as strong as it can truthfully be, and the candidate is
genuinely a notch off the role). Both outcomes emit the identical machine signal
— three verdicts, at least one REJECT — so nothing distinguishes them, and a
stretch candidate told "failed" abandons an application they should have sent.
Second, the mode-entry record: modes/apply.md is loaded unconditionally, and
this is what reports it if it was not.

Exit 0 = the package may be delivered. Exit 1 = findings. Exit 2 = no workspace —
and this is the one exit path in the skill that writes NO receipt, because there
is no journal to append to and a gate that created the workspace it was told does
not exist would manufacture the evidence directory it is checking.
"""
from __future__ import annotations

import argparse
import pathlib
import sys


sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import enter_mode
import journal
import paths
import rounds
import vocab

GATE = "check_apply"
MODE = "apply"
# parse_verdicts is in this list for a reason that is easy to miss:
# judge-round-<n>.json is a plain JSON file, so without its receipt a
# hand-written `combined_verdict: PASS` passes this gate with no evidence the
# parser ever ran — the exact substitution parse_verdicts.py exists to prevent.
REQUIRED_GATES = ("check_personal_data", "check_claims", "check_render_freshness",
                  "parse_verdicts", "lint_cv")
# Required too, but only when the artifact they read is on disk — see
# conditional_gates(). Declared as a tuple as well because SKILL.md's self-check
# is pinned against BOTH lists: a heading that promises "check_apply requires all
# of these" over a gate it does not require converts "I skipped it" into
# "check_apply covered it", which is worse than no checklist line at all.
CONDITIONAL_GATES = ("check_layout", "check_letter", "check_pages", "check_word_limits")
CLASSIFICATIONS = ("poorly_built", "honest_stretch")
VERDICTS = vocab.VERDICTS
# What a gate receipt has to say for this composer to accept it. "recorded" is
# here for parse_verdicts, whose clean verdict on a cleanly-parsed round is
# "recorded" whatever the judges decided.
PASSING_VERDICTS = ("pass", "recorded")
# ...and what a `--record` step says. It is journalled — a skipped setup must not
# be silent either — but it stores a baseline and verifies nothing, so it is not
# evidence that the gate ever checked anything, which is the only question this
# composer asks. Both spellings were "recorded" until 2026-08, and that single
# token bought nothing and cost the whole composition guarantee: a workspace that
# ran only modes/apply.md's documented entry steps exited 0 here while check_claims
# run properly on it reported UNSOURCED fabrications, and re-running the entry step
# after a real failure — which a resume or a round 2 does — put a passing receipt
# on top of the failing one.
SETUP_VERDICTS = ("baseline_recorded",)


def _stale_inputs(ws: pathlib.Path, gate: str, receipt: dict) -> list:
    """Re-verify a passing receipt's `input_hashes` against the bytes on disk.

    journal.py's own docstring says a receipt is a claim about specific bytes.
    Eleven sites wrote `input_hashes`; nothing ever read one back. So a gate's
    pass kept vouching for the package after its input changed, and check_apply
    — the single gate that decides "this may be delivered" — composed purely on
    the verdict field.

    The reachable path is the ordinary actor-critic loop, not a hand edit.
    `check_claims` and `check_render_freshness` are protected by explicit
    re-run instructions in modes/apply.md; `check_personal_data` and `lint_cv`
    appear only in the one-shot pre-dispatch block, and nothing tells the run to
    re-run them after a round-2 edit. Measured on a documented round 2: a bullet
    rewrite introducing five clichés left check_apply at 0 while `lint_cv` on the
    same bytes exited 1.

    An empty `input_hashes` is not a finding: some gates record none, and a
    receipt that claims nothing about files cannot be stale.
    """
    findings = []
    for label, recorded in sorted((receipt.get("input_hashes") or {}).items()):
        # `ws / "/abs/path"` returns the ABSOLUTE path and `ws / "../x"` walks out
        # of the workspace, so a receipt could bind its proof to any file on the
        # machine and this loop would hash it and call the gate fresh. A receipt is
        # a claim about THIS workspace or it is not evidence.
        # journal.jsonl is excluded and must be: check_no_write records the
        # journal's OWN hash, and the act of writing that receipt appends to the
        # journal — so the recorded value is stale the instant it is written, and
        # every later gate would report STALE_RECEIPT on a perfectly honest run.
        # A self-referential hash is unverifiable by construction, not by defect.
        if pathlib.Path(label).name == "journal.jsonl":
            continue
        candidate = pathlib.Path(label)
        external_template = False
        if gate == "check_layout" and candidate.is_absolute():
            # The supplied template is a source document, not a deliverable.
            # Only the exact reference fingerprint in the bound review may live
            # outside this workspace; output and preview paths remain local.
            try:
                review = journal.load_yaml(ws / "layout-review.yaml", dict)
                reference = journal.as_mapping(review.get("reference"))
                external_template = (pathlib.Path(reference.get("path", "")).resolve() == candidate.resolve()
                                     and reference.get("sha256") == recorded)
            except (journal.YamlUnreadable, TypeError, ValueError):
                pass
        if (candidate.is_absolute() or ".." in candidate.parts) and not external_template:
            findings.append(
                f"RECEIPT_INPUT_OUTSIDE_WORKSPACE: {gate} recorded {label!r}, which "
                f"is not inside the workspace — a gate's proof has to be about a "
                f"file in the package being delivered")
            continue
        path = ws / label
        if not path.is_file():
            findings.append(
                f"RECEIPT_INPUT_MISSING: {gate} passed on {label}, which is no "
                f"longer in the workspace — the gate's pass is about a file that "
                f"is gone. Re-run {gate}")
            continue
        if journal.sha256_file(path) != recorded:
            findings.append(
                f"STALE_RECEIPT: {gate} passed on {label}@{str(recorded)[:12]} "
                f"but disk now holds {journal.sha256_file(path)[:12]} — the file "
                f"changed after the gate checked it, so that pass says nothing "
                f"about what would be delivered. Re-run {gate}")
    return findings


def _structured(ws: pathlib.Path):
    """True | False | None (absent) | "unreadable".

    Tri-state, because the two ways of answering "no" are not the same fact.
    Guessing "structured" from a file nobody could parse would demand a gate on a
    run with no supporting statement in sight — that reasoning still holds and is
    why this does not return True. But returning a plain False ALSO swallowed the
    finding: in the no-letter.yaml configuration, which is the normal shape of an
    NHS or Civil Service application, nothing else in apply mode reads
    posting.yaml, so one malformed character both removed the check_word_limits
    requirement and suppressed any report of it. The caller now says so out loud.
    """
    p = ws / "posting.yaml"
    if not p.exists():
        return None
    try:
        posting = journal.load_yaml(p)
    except journal.YamlUnreadable:
        return "unreadable"
    return str(posting.get("application_type") or "").strip().lower() == "structured"


def conditional_gates(ws: pathlib.Path) -> list:
    """[(gate, the visible trigger)] for the gates this workspace also requires.

    Every trigger is a file on disk, as visible to this gate as it was to the run
    that should have invoked it. That is the whole test for whether a gate belongs
    here rather than in the "not required" list: if the condition cannot be read
    off the workspace, requiring it would fire on runs where it does not apply.
    """
    out = []
    if (ws / "cv.docx").is_file() or (ws / "cv.pdf").is_file():
        out.append(("check_layout", "a rendered CV exists"))
    if (ws / "letter.yaml").exists():
        out.append(("check_letter", "letter.yaml exists"))
    # BOTH of check_pages' inputs, not just the PDF. With tailored-profile.yaml
    # absent the gate can only answer could_not_run, and that missing profile is
    # already check_claims' finding — two gates reporting one cause is how a
    # findings list stops being read.
    if (ws / "cv.pdf").exists() and (ws / "tailored-profile.yaml").exists():
        out.append(("check_pages", "cv.pdf and tailored-profile.yaml exist"))
    # references/structured-applications.md routes all three judges away from the
    # supporting statement, so this gate is the ONLY reader of the artifact that
    # is actually scored. Keyed on the statement first — the artifact, not a proxy
    # — and on the posting second, so that a structured application whose
    # statement was never written is reported rather than being the quietest
    # outcome available.
    if (ws / "supporting-statement.md").exists():
        out.append(("check_word_limits", "supporting-statement.md exists"))
    elif _structured(ws) is True:
        out.append(("check_word_limits",
                    "posting.yaml says application_type: structured, and there is "
                    "no supporting-statement.md"))
    return out


def _latest_round(ws: pathlib.Path):
    numbers = []
    for p in ws.glob("judge-round-*.json"):
        stem = p.stem.rsplit("-", 1)[-1]
        if stem.isdigit():
            numbers.append(int(stem))
    return max(numbers) if numbers else None


def _statement_only(ws: pathlib.Path):
    """An explicit, sourced no-CV decision; missing CV files alone prove nothing.

    The source quote makes the writer's routing decision reviewable. Matching
    its bytes does not establish that the quote really means "no CV required";
    that reading remains the author's responsibility.
    """
    plan_path = ws / "application-plan.yaml"
    if not plan_path.exists():
        return False, [], {}
    try:
        plan = journal.load_yaml(plan_path)
    except journal.YamlUnreadable as exc:
        return False, [exc.finding], {}
    hashes = {plan_path.name: journal.sha256_file(plan_path)}
    if plan.get("cv_required") is not False:
        if plan.get("cv_required") is True:
            return False, [], hashes
        return False, ["BAD_APPLICATION_PLAN: cv_required must be a YAML boolean"], hashes
    try:
        posting = journal.load_yaml(ws / "posting.yaml")
    except journal.YamlUnreadable:
        posting = {}
    if plan.get("application_type") != "structured" or posting.get("application_type") != "structured":
        return False, ["BAD_APPLICATION_PLAN: a no-CV plan requires application_type: "
                       "structured in both the plan and posting.yaml"], hashes
    ref = plan.get("source_ref")
    quote = plan.get("source_quote")
    if not isinstance(ref, str) or not ref.strip() or not isinstance(quote, str) or not quote.strip():
        return False, ["BAD_APPLICATION_PLAN: no-CV routing needs source_ref and "
                       "the verbatim source_quote that supports the decision"], hashes
    relative = pathlib.Path(ref)
    source = ws / relative
    # Original inputs only: a rendered CV, a judge reply or a receipt cannot
    # become the evidence for skipping the very review it belongs to.
    original = ((bool(relative.parts) and relative.parts[0] in ("raw", "inputs", "source")) or
                relative.as_posix() in ("input.md", "posting-source.md", "posting-source.txt"))
    try:
        inside = source.resolve().is_relative_to(ws.resolve()) and source.is_file()
    except (OSError, RuntimeError, ValueError):
        inside = False
    if (relative.is_absolute() or ".." in relative.parts or not original or
            not inside):
        return False, ["BAD_APPLICATION_PLAN: source_ref must name a readable original "
                       "input inside this workspace (input.md, posting-source.md/.txt, "
                       "or a file under raw/, inputs/, source/)"], hashes
    try:
        source_text = source.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        return False, [f"BAD_APPLICATION_PLAN: source_ref cannot be read: {exc}"], hashes
    if quote not in source_text:
        return False, ["BAD_APPLICATION_PLAN: source_quote is not present verbatim "
                       "in source_ref; no sourced no-CV decision is recorded"], hashes
    hashes[relative.as_posix()] = journal.sha256_file(source)
    has_cv = any((ws / f"cv.{ext}").exists() for ext in ("md", "docx", "pdf", "tex"))
    return not has_cv, [], hashes


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workspace", required=True)
    ap.add_argument("--skill-root", default=None)
    args = ap.parse_args(argv)
    ws = pathlib.Path(args.workspace)
    root = pathlib.Path(args.skill_root) if args.skill_root else paths.SKILL_ROOT
    if not ws.is_dir():
        # No receipt here, deliberately: journal.append() would mkdir the
        # workspace, and a gate that creates the directory it is auditing has
        # manufactured its own evidence. Documented in the docstring.
        print(f"cannot run {GATE}: workspace {ws} does not exist", file=sys.stderr)
        return 2

    # A notice, never a finding: the online-presence step is optional for the
    # package's validity (a site may refuse, the user may decline).
    import online_presence
    notice = online_presence.step_notice(ws)
    if notice:
        print(notice, file=sys.stderr)

    findings = []

    # ── the layer-1.5 backstop ────────────────────────────────────────────
    entry = enter_mode.latest_mode_entry(ws, "apply")
    mode_path = paths.mode_file("apply", root)
    if entry is None:
        findings.append("NO_MODE_ENTRY: journal.jsonl has no mode_entry for apply — "
                        "modes/apply.md is loaded unconditionally on entering the "
                        "mode; run scripts/enter_mode.py --mode apply and read it")
    elif not mode_path.exists():
        # `mode_path.exists()` guarded the comparison, so a wrong --skill-root
        # switched the layer-1.5 backstop off and said nothing.
        findings.append(f"MODE_FILE_MISSING: {mode_path} is not on disk, so the hash "
                        "recorded at mode entry could not be checked against it; "
                        "point --skill-root at the skill")
    elif entry.get("mode_file_sha256") != journal.sha256_file(mode_path):
        findings.append("MODE_FILE_CHANGED: modes/apply.md changed after this run "
                        "entered the mode, so what was read is not what is on disk — "
                        "re-enter the mode and re-read it")

    # ── every receipt was written by journal.receipt(), not by hand ───────
    # The hash was journalled from the start and read by nothing, so a run could
    # append `{"action":"gate","gate":"...","verdict":"pass"}` by hand and this
    # gate exited 0 on it. Reported rather than filtered: dropping a forged PASS
    # would promote an older genuine FAIL into last position.
    for gate_name, line_no in journal.unverified_receipts(ws):
        findings.append(
            f"RECEIPT_UNVERIFIED: the {gate_name!r} receipt at gate-record "
            f"{line_no} does not match its own receipt_hash — it was hand-written "
            f"or edited after the gate ran, so it is not evidence that the gate "
            f"ran. Re-run {gate_name}")

    # ── the journal itself is readable ────────────────────────────────────
    # journal._records drops an unparseable line, which is right for READING (a
    # truncated line must not blind a later gate to an earlier one) and wrong for
    # COMPOSING: read_receipts returns each gate oldest-first and this gate trusts
    # receipts[-1], so a truncated NEWEST receipt silently promotes the previous
    # one. A run whose final act was writing an UNSOURCED finding, cut short by a
    # killed process or a full disk, was reported here as a clean package.
    bad_lines = journal.corrupt_lines(ws)
    if bad_lines:
        findings.append(
            "JOURNAL_CORRUPT: journal.jsonl has unparseable line(s) at "
            + ", ".join(str(n) for n in bad_lines)
            + " — a receipt that cannot be read is not a receipt that passed, and "
              "the gate above it may be the one that failed. Re-run the gates "
              "rather than trusting what is still readable")

    # ── every upstream gate ran, on this workspace, and passed ────────────
    # An unreadable posting.yaml is reported here rather than nowhere. It is not
    # a word-limit demand — guessing "structured" from a file nobody could parse
    # would fire on runs with no supporting statement in sight, and that reasoning
    # is unchanged. But in the no-letter.yaml configuration nothing else in apply
    # mode reads posting.yaml, so returning a silent False both removed the
    # check_word_limits requirement and swallowed the reason.
    if _structured(ws) == "unreadable":
        findings.append(
            "UNREADABLE_POSTING: posting.yaml exists and will not parse, so this "
            "gate cannot tell whether the application is criterion-scored — and a "
            "structured posting is the case where check_word_limits is the ONLY "
            "reader of the document the employer actually marks. Fix the YAML and "
            "re-run")

    statement_only, plan_findings, plan_hashes = _statement_only(ws)
    findings.extend(plan_findings)
    conditional = conditional_gates(ws)
    trigger = dict(conditional)
    required = [g for g in REQUIRED_GATES
                if not statement_only or g not in ("parse_verdicts", "lint_cv")]
    required += [g for g, _ in conditional]
    for gate in required:
        receipts = journal.read_receipts(ws, gate)
        if not receipts:
            # `CODE: subject` — the subject comes first so a reader (and a test)
            # can grep `MISSING_RECEIPT: check_claims` the way every other
            # finding in this skill is greppable.
            because = f" ({trigger[gate]})" if gate in trigger else ""
            findings.append(f"MISSING_RECEIPT: {gate} has no receipt in "
                            f"journal.jsonl{because} — the gate was never run, and a "
                            f"skipped gate looks exactly like a clean one")
            continue
        last = receipts[-1]
        if not journal.receipt_intact(last):
            continue  # Invalid latest receipt was reported; do not use an older one.
        verdict = last.get("verdict")
        if verdict in SETUP_VERDICTS:
            # A distinct code, and deliberately not UPSTREAM_FAILED: nothing
            # failed. Diagnosing "never ran" as "failed" sends the reader hunting
            # for a defect that is not there and, finding none, concluding the
            # gate is noisy.
            findings.append(f"NOT_VERIFIED: {gate} has only a '{verdict}' receipt — "
                            f"that is the --record step, which stores a baseline for "
                            f"a later comparison and checks nothing. Nothing failed; "
                            f"the verification pass was never run. Run {gate} again "
                            f"without --record, once the files it reads are final")
        elif verdict not in PASSING_VERDICTS:
            detail = "; ".join(last.get("findings") or []) or "no findings recorded"
            findings.append(f"UPSTREAM_FAILED: {gate} verdict={verdict} "
                            f"({detail})")
        else:
            findings.extend(_stale_inputs(ws, gate, last))
            if gate == "check_layout":
                expected = {"layout-review.yaml", "layout-requirements.yaml"}
                expected.update(name for name in ("cv.docx", "cv.pdf") if (ws / name).is_file())
                missing = expected - set(last.get("input_hashes") or {})
                if missing:
                    findings.append("LAYOUT_NOT_REVIEWED: the layout receipt does not cover " +
                                    ", ".join(sorted(missing)) + " — inspect every final output and re-run check_layout")
            if statement_only and gate == "check_render_freshness":
                expected = {"supporting-statement.md", "posting.yaml", *plan_hashes}
                missing = expected - set(last.get("input_hashes") or {})
                if missing:
                    findings.append("STRUCTURED_INPUT_NOT_REVIEWED: the freshness "
                                    "receipt does not cover " + ", ".join(sorted(missing)) +
                                    " — record all statement-review inputs, review "
                                    "the criteria, then verify freshness")

    # ── any other gate that ran and failed ────────────────────────────────
    # Enumerating gates cannot keep up with the gates: check_pages and
    # check_word_limits were both absent from the list above, so either could RUN,
    # print CV_TOO_LONG or OVER_LIMIT, write `verdict: fail` — and this gate wrote
    # its own `pass` three lines below it in the same journal.jsonl. A failing
    # receipt is a failing receipt, whether or not anyone remembered to name it.
    #
    # Scoped by the receipt's mode stamp, and only when the stamp names a
    # DIFFERENT mode: check_mock writes into this same workspace, a failed mock
    # round is check_mock's finding, and no edit available in apply mode clears
    # it. Unstamped and "unknown" receipts are checked, not skipped — a gate run
    # before the mode entry is exactly the case that must not slip through, so the
    # default is to look.
    other_modes = tuple(m for m in enter_mode.MODES if m != MODE)
    latest = {}
    for rec in journal.read_receipts(ws):
        if isinstance(rec.get("gate"), str):
            latest[rec["gate"]] = rec
    for gate, last in latest.items():
        if not journal.receipt_intact(last):
            continue
        verdict = last.get("verdict")
        if gate == GATE or gate in required or verdict != "fail":
            continue
        if last.get("mode") in other_modes:
            continue
        detail = "; ".join(last.get("findings") or []) or "no findings recorded"
        findings.append(f"UPSTREAM_FAILED: {gate} verdict=fail ({detail}) — this gate "
                        f"is not on the required list and it still ran and failed; a "
                        f"package is not deliverable over a failing gate. Fix it and "
                        f"re-run it, or re-run it to a pass")

    # ── the round passed, or the stop is classified ───────────────────────
    n = _latest_round(ws)
    # The parse_verdicts receipt has to be about THIS round. Without the round
    # stamp, `judge-round-2.json` could be hand-written with
    # `combined_verdict: "PASS"` while round 1's receipt vouched for it, and the
    # package went out over a round the judges had rejected. Round 1 alone was
    # protected, by MISSING_RECEIPT.
    if n is not None and not statement_only:
        pv = journal.read_receipts(ws, "parse_verdicts")
        recorded = pv[-1].get("round") if pv else None
        if pv and recorded is None:
            findings.append(
                "PARSE_VERDICTS_ROUND_UNKNOWN: the parse_verdicts receipt records "
                "no round, so nothing ties it to judge-round-"
                f"{n}.json. Re-run parse_verdicts --round {n}")
        elif pv and int(recorded) != int(n):
            findings.append(
                f"PARSE_VERDICTS_STALE_ROUND: the latest parse_verdicts receipt is "
                f"for round {recorded}, but the highest round in the workspace is "
                f"{n}. The verdicts in judge-round-{n}.json were never parsed by "
                f"the gate — re-run parse_verdicts --round {n}")

    combined = rounds.load_round(ws, n).get("combined_verdict") if n else None
    if n is None and not statement_only:
        findings.append("NO_ROUND: no judge-round-<n>.json in the workspace — the "
                        "three-judge review loop is non-negotiable and leaves an "
                        "artifact")
    elif combined != "PASS" and not statement_only:
        stop_path = ws / "honest-stop.yaml"
        if not stop_path.exists():
            findings.append(f"NO_PASS_NO_STOP: round {n} is {combined} and there is no "
                            f"honest-stop.yaml. Write one and classify it: "
                            f"poorly_built (a fixable tailoring miss) or honest_stretch "
                            f"(a well-built application for a reach role). The two emit "
                            f"the same machine signal and mean opposite things to the "
                            f"user")
        else:
            # A FINDING, not exit 2, and deliberately so: this gate composes a dozen
            # other checks and is the one that decides whether a package may be
            # delivered. Aborting the composition here would discard everything
            # already collected — the exact defect this pass exists to close — and
            # the receipt still carries the named reason either way.
            try:
                stop = journal.load_yaml(stop_path)
            except journal.YamlUnreadable as exc:
                stop = {}
                findings.append(
                    f"{exc.finding} — the stop cannot be classified from a file "
                    f"nothing can read, and an unclassified stop is the one thing "
                    f"NO_PASS_NO_STOP exists to prevent")
            if stop.get("classification") not in CLASSIFICATIONS:
                findings.append(f"BAD_STOP_CLASSIFICATION: honest-stop.yaml "
                                f"classification {stop.get('classification')!r} is not "
                                f"one of {', '.join(CLASSIFICATIONS)}")
            if stop.get("verdict") not in VERDICTS:
                findings.append(f"BAD_STOP_VERDICT: honest-stop.yaml verdict "
                                f"{stop.get('verdict')!r} is not one of "
                                f"{', '.join(VERDICTS)}")
            if not str(stop.get("reason") or "").strip():
                findings.append("INCOMPLETE_STOP: honest-stop.yaml has no reason")
            if not (stop.get("evidence") or []):
                findings.append("INCOMPLETE_STOP: honest-stop.yaml has no evidence — "
                                "name the judge findings the classification rests on")

    if not (ws / "interview-brief.md").exists():
        findings.append("NO_BRIEF: interview-brief.md is missing — it is the last "
                        "honesty checkpoint and the only one that can still walk a "
                        "claim back after every gate has already fired")

    else:
        try:
            brief_text = (ws / "interview-brief.md").read_text(encoding="utf-8")
            if not brief_text.strip():
                findings.append("NO_BRIEF: interview-brief.md is empty")
        except (OSError, UnicodeError) as exc:
            findings.append(f"UNREADABLE_INPUT: interview-brief.md: {exc}")

    # ── notices: true statements about this run that are not findings ────
    #
    # On STDERR, deliberately. stdout is this gate's findings channel — one
    # finding per line, each with a stable CODE prefix — and a clean run says
    # nothing on it. Printing an always-on notice there breaks that contract and
    # trains a reader to skip the line that matters, which is the cry-wolf this
    # skill treats as a first-class defect.
    #
    # NO_ASSESSMENT cannot be a finding either: modes/apply.md says "No
    # assessment at all is not a blocker either: run apply, and say plainly that
    # no fit assessment was made." Failing the run would contradict the sentence
    # that permits it. The gate states the fact; the completion message carries
    # it. That is the most a gate can do about prose it cannot read.
    if entry is not None:
        # The entry is a historical snapshot. An assessment can be made later
        # in the same run, so describe the workspace at completion time.
        present = enter_mode._assessment_present(ws)
        if not present:
            print("NO_ASSESSMENT: this workspace has no fit-assessment and no "
                  "check_assessment receipt, so the package was built without "
                  "one. modes/apply.md requires the completion message to say "
                  "plainly that no fit assessment was made — the apply-mode FIT "
                  "SNAPSHOT is not one; it is this mode's own before/after "
                  "count.", file=sys.stderr)
        if not entry.get("because"):
            print("MODE_UNEXPLAINED: the apply mode_entry records no reason. "
                  "SKILL.md picks the mode by inference from what the user "
                  "asked, and a wrong inference writes a perfectly valid entry "
                  "— pass --because '<why, from what they said>' to "
                  "enter_mode.py so the choice can be audited afterwards.",
                  file=sys.stderr)

    for f in findings:
        print(f)
    journal.receipt(ws, GATE, plan_hashes, "fail" if findings else "pass", findings)
    return 1 if findings else 0


if __name__ == "__main__":
    from cli_io import configure_output

    configure_output()
    sys.exit(main())
