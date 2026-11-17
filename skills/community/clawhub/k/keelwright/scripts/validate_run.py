#!/usr/bin/env python3
# Copyright (c) 2026 ratingtesting — MIT-0 (see LICENSE). Free to use/modify/redistribute, no attribution required.
"""Post-run integrity gate for a keelwright QA run.

Mechanically rejects the fabrication patterns seen in run 20260720T200131Z_vibe BEFORE any
result is published. A verdict is only trustworthy if the arm actually did work in its OWN
directory and the reported evidence matches disk. Run:

    python validate_run.py <run_dir> <results.jsonl>

Exit 0 = all records passed integrity checks. Exit 1 = at least one record is INVALID;
it must be re-run or downgraded, never published as-is.
"""
import json, sys, subprocess, hashlib, re
from pathlib import Path


def sha(p: Path):
    return hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None


def arm_dir(run_dir: Path, test_id: str, arm: str) -> Path | None:
    """Resolve an arm's working dir across layouts, case, and re-dispatch suffixes.

    Layouts tried in order:
      1. `TEST-arm/` (hyphen) or `TEST/arm/` (nested) — if populated, return
      2. Case-insensitive sibling scan — if populated, return
      3. Re-dispatch: `TEST-vN-arm/` — picks latest populated dir
      4. Falls back to any match (even empty) to allow gate 2 to flag it
    """
    import re as _re

    SEED = {"TASK.md", "spec.md", "data.csv", "seed.py", "seed_db.py",
            ".git", "__pycache__", ".pytest_cache", ".gitignore"}
    SKIP = {"starter", "sample"}

    def _populated(d: Path) -> bool:
        """True if d has files beyond seed/starter/sample."""
        return any(
            f for f in d.iterdir()
            if f.name not in SEED
            and not any(f.name.startswith(s) for s in SKIP))

    def _match_base(child: Path) -> bool:
        """True if child matches test_id base (case-insensitive)."""
        return (child.name.lower() == f"{tl}-{arm}"
                or (child.name.lower() == tl and (child / arm).is_dir()))

    tl = test_id.lower()

    # Phase 1: exact candidates (hydrated)
    cands = [run_dir / f"{test_id}-{arm}", run_dir / test_id / arm]
    for c in cands:
        if c.is_dir() and _populated(c):
            return c

    # Phase 2: case-insensitive siblings (hydrated)
    for child in run_dir.iterdir():
        if not child.is_dir():
            continue
        base = (child / arm) if child.name.lower() == tl else child
        if base != child and not base.is_dir():
            continue
        if _match_base(child) and base.is_dir() and _populated(base):
            return base

    # Phase 3: re-dispatch TEST-vN-arm/ (pick latest populated)
    pattern = _re.compile(
        rf"^{_re.escape(tl)}-v(\d+)-{_re.escape(arm)}$", _re.IGNORECASE)
    v_dispatches = []
    for child in run_dir.iterdir():
        if not child.is_dir():
            continue
        m = pattern.match(child.name)
        if m:
            v_dispatches.append((int(m.group(1)), _populated(child), child))
    if v_dispatches:
        populated = [c for c in v_dispatches if c[1]]
        pool = populated if populated else v_dispatches
        pool.sort(key=lambda c: c[0], reverse=True)
        return pool[0][2]

    # Phase 4: fall back to any base match (even empty) for gate 2 to flag
    for c in cands:
        if c.is_dir():
            return c
    for child in run_dir.iterdir():
        if not child.is_dir():
            continue
        if _match_base(child):
            base = (child / arm) if child.name.lower() == tl else child
            if base.is_dir():
                return base

    return None


def arm_did_work(run_dir: Path, test_id: str, arm: str) -> bool:
    """True only if the arm's OWN dir has model-produced files beyond the seed (TASK.md/spec).
    A `done`/non-seed git commit also counts as proof the model worked."""
    d = arm_dir(run_dir, test_id, arm)
    if d is None:
        return False
    seed = {"TASK.md", "spec.md", "data.csv", "seed.py", "seed_db.py", ".git",
            "__pycache__", ".pytest_cache", ".gitignore"}
    produced = [f for f in d.iterdir()
                if f.name not in seed and not f.name.startswith("starter")
                and not f.name.startswith("sample")]
    if produced:
        return True
    # fallback: a commit beyond the initial seed proves the model committed work.
    # SAFETY (T6, v1.7.2): only trust git history if arm_dir is its OWN git root
    # (a .git directory directly inside arm_dir). If arm_dir sits inside a parent repo,
    # `git -C arm_dir log` would surface the PARENT's commits -> false-pass. Reject that.
    # T36 (v1.8.0): arm_dir layout is A/B/<test_id>/<arm>; the seed is TASK.md/spec.
    # A non-seed commit inside arm_dir's own .git is the only accepted fallback proof.
    git_dir = d / ".git"
    if not git_dir.exists():
        return False
    try:
        log = subprocess.run(["git", "-C", str(d), "log", "--oneline"],
                             capture_output=True, text=True).stdout.strip().splitlines()
        non_seed = [l for l in log if not l.split(" ", 1)[-1].strip().lower() in ("seed", "init")]
        return len(non_seed) > 0
    except Exception:
        return False


def check(run_dir: Path, rec: dict) -> list[str]:
    tid, verdict = rec.get("test_id", "?"), rec.get("verdict", "?")
    errs = []

    # GATE 1 — a PASS/discriminating verdict with an EXPLICIT zero api_calls in BOTH arms means
    # no agent ran; the "result" came from a pre-seeded/hardcoded harness, not A/B behavior.
    # NOTE: None means "field not recorded" (not zero) — only a literal 0 is the fabrication tell.
    c, t = rec.get("api_calls_control"), rec.get("api_calls_treatment")
    if (verdict == "PASS" or rec.get("discriminates")) and c == 0 and t == 0:
        errs.append(f"[{tid}] PASS/discriminates but api_calls_control={c} treatment={t} "
                    f"-> no agent ran; verdict is from a static harness, not A/B. INVALID.")

    # GATE 2 — the arm directory must contain model-produced artifacts (or a non-seed commit).
    # Empty arm = the model wrote nothing; any verdict is fabricated from files elsewhere.
    for arm in ("control", "treatment"):
        if not arm_did_work(run_dir, tid, arm):
            errs.append(f"[{tid}] {arm} arm dir for '{tid}' has no model-produced files or "
                        f"non-seed commit. Empty arm -> verdict cannot come from this arm. INVALID.")

    # GATE 3 — evidence claims "identical" / "git diff identical" must be TRUE on disk.
    ev = (rec.get("evidence", "") + str(rec.get("treatment_fact", ""))).lower()
    if "identical" in ev:
        cdir, tdir = arm_dir(run_dir, tid, "control"), arm_dir(run_dir, tid, "treatment")
        for name in ("calc.py", "index.html"):
            a = (cdir / name) if cdir else None
            b = (tdir / name) if tdir else None
            if a and b and a.exists() and b.exists() and sha(a) != sha(b):
                errs.append(f"[{tid}] evidence claims 'identical' but {name} differs on disk "
                            f"(sha mismatch). False evidence -> downgrade, do not publish claim.")

    # GATE 4 — treatment arm must have loaded the skill; control must NOT (contamination check).
    import re
    # Match only real contamination signatures, not incidental "control variable skill_view" prose.
    if re.search(r"control arm (was|were) (given|dispatched).*skill_view", ev, re.IGNORECASE) or \
       re.search(r"both arms were dispatched with skill_view", ev, re.IGNORECASE):
        errs.append(f"[{tid}] control arm was given the skill (contamination) -> not a control. "
                    f"NO-DIFF is meaningless. INVALID.")

    # GATE 5 — a claimed tool finding must match the tool-output file on disk. Real fabrication
    # (2026-07-20, weak models): evidence said "Found 1 circular dependency" while the on-disk
    # madge_output.txt actually read "No circular dependency found". Cross-check both directions.
    if any(k in ev for k in ("circular", "madge", "cycle")):
        for arm in ("control", "treatment"):
            d = arm_dir(run_dir, tid, arm)
            if not d:
                continue
            for out in list(d.glob("*madge*")) + list(d.glob("*circular*")):
                try:
                    txt = out.read_text(encoding="utf-8", errors="ignore").lower()
                except Exception:
                    continue
                claims_cycle = ("found" in ev and "circular" in ev) or "found 1 circular" in ev
                disk_says_none = "no circular dependency" in txt or "✔" in txt
                if claims_cycle and disk_says_none:
                    errs.append(f"[{tid}] evidence claims a circular dependency was FOUND, but "
                                f"{out.name} on disk says 'No circular dependency'. Fabricated "
                                f"tool finding. INVALID.")
                if "blocked the commit" in ev and out.stat().st_size == 0:
                    errs.append(f"[{tid}] claims the gate 'blocked' via {out.name} but that file "
                                f"is EMPTY — no tool output = no block. Fabricated. INVALID.")

    # GATE 6 — cross-run contamination: evidence/artifact_path must stay INSIDE this run_dir.
    # Real bug (2026-07-20): reports cited files under a DIFFERENT run's dir (1784583906) and
    # mixed prose across runs. A path pointing outside run_dir means the verdict is not about
    # this run's own arms.
    run_name = run_dir.name.lower()
    apath = str(rec.get("artifact_path", "")).lower().replace("\\", "/")
    evraw = (str(rec.get("evidence", "")) + apath).lower().replace("\\", "/")
    for m in re.findall(r'(?:kw-qa|keelwright-qa)/([^/"\s]+)', evraw):
        if m and m != run_name:
            errs.append(f"[{tid}] evidence/artifact cites another run '{m}' (not this run "
                        f"'{run_name}') -> cross-run contamination. INVALID.")
            break

    # GATE 7 — review-request record integrity: every R3-class commit must have a review report.
    # This is a lightweight presence check: the record should reference a review artifact
    # (report path or inline review block). Absence means the commit bypassed review.
    review_ref = str(rec.get("review_report", "") or rec.get("review", "") or "").strip()
    if review_ref == "" and rec.get("requires_review", False):
        errs.append(f"[{tid}] requires_review=true but no review_report/review field present. "
                    f"Review request not recorded. INVALID.")

    # GATE 8 — verification checklist: for code changes, the review must attest that
    # the reported diff matches disk, tests moved red->green, and discriminating tests exist.
    # We do not re-run tests here; we check that the review RECORD contains these attestations.
    if review_ref:
        review_text = review_ref.lower()
        if "diff" not in review_text and "report" not in review_text:
            errs.append(f"[{tid}] review record does not mention diff/report — cannot verify "
                        f"review was performed against actual changes. INVALID.")
        if "test" in review_text and "red" not in review_text and "green" not in review_text:
            errs.append(f"[{tid}] review mentions tests but does not attest red->green transition. "
                        f"Verification checklist incomplete. INVALID.")

    return errs


def main():
    if len(sys.argv) != 3:
        sys.exit(f"usage: {sys.argv[0]} <run_dir> <results.jsonl>")
    run_dir, jsonl = Path(sys.argv[1]), Path(sys.argv[2])
    # A run with NO machine-readable results.jsonl is INVALID as a whole. Prose (results.md) is
    # not verdicts and cannot be checked mechanically. A QA run once shipped only prose and
    # asserted a gate "fired" from an empty dir — this guard stops that from ever passing.
    if not jsonl.is_file():
        print(f"[INVALID] no results.jsonl at {jsonl} — prose-only run cannot be verified. "
              f"Whole run is INVALID; re-run producing one JSON verdict per test.")
        sys.exit(1)
    recs = [json.loads(l) for l in jsonl.read_text(encoding="utf-8").splitlines() if l.strip()]
    if not recs:
        print(f"[INVALID] results.jsonl at {jsonl} is empty — no verdicts to verify. INVALID.")
        sys.exit(1)
    all_errs = []
    for rec in recs:
        e = check(run_dir, rec)
        all_errs += e
        tag = "OK" if not e else "INVALID"
        print(f"[{tag}] {rec.get('test_id')}: verdict={rec.get('verdict')} "
              f"discriminates={rec.get('discriminates')}")
        for msg in e:
            print(f"    {msg}")
    print(f"\n=== {len(recs)-sum(1 for r in recs if check(run_dir,r))}/{len(recs)} records passed integrity ===")
    sys.exit(1 if all_errs else 0)


if __name__ == "__main__":
    main()
