#!/usr/bin/env python3
"""
PhD Research Companion - Automated Skill Quality Scorer

Scores this skill on 9 weighted dimensions by ACTUALLY running things
(compile check, --help smoke test, mock detection, doc/code cross-check,
test-integrity probe, portability scan, theory-track presence, substance,
hygiene).

Nothing here is self-reported: every score is derived from an executable probe.

Two failure modes are guarded against:
  * mutation   - does a dimension drop when ITS OWN defect is injected?
                 (scripts/score_selftest.py)
  * vacuity    - can a skill with no substance still score 100?
                 dimension caps + the substance dimension below.

Usage:
    python self_score.py                 # score + append to score-history.json
    python self_score.py --no-history    # score only, do not append
    python self_score.py --markdown out.md
    python self_score.py --fast          # skip the mutation-catch probe (slow)
"""

from __future__ import annotations

import argparse
import ast
import json
import os
import py_compile
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent

# Weight must sum to 1.0
WEIGHTS = {
    "compilability": 0.12,
    "runnability": 0.12,
    "authenticity": 0.12,
    "doc_consistency": 0.10,
    "test_integrity": 0.14,
    "portability": 0.08,
    "fitness": 0.10,
    "substance": 0.18,
    "hygiene": 0.04,
}

# A dimension score below `floor` caps the TOTAL at `cap`, because one
# catastrophic failure must not be diluted by the other dimensions' weights.
# (dim, floor, cap, reason)
CAPS = [
    ("test_integrity", 5.0, 60.0, "the test suite cannot fail"),
    ("substance", 3.0, 50.0, "the shipped code has no substance"),
    ("authenticity", 4.0, 70.0, "results are mocked or fabricated"),
]

# Minimum substance for full credit. Deliberately set BELOW this repo's actual
# numbers (LOC ~2400, defs ~68, help >= 227 chars, ~31 documented commands) so
# that passing is not calibrated to this repo alone.
SUBSTANCE_TARGET = {
    "loc": 1200,          # non-blank, non-comment lines across shipped modules
    "defs": 50,           # top-level functions/classes
    "help_chars": 150,    # --help output length for a real CLI
    "cmds": 12,           # runnable command examples documented in SKILL.md
}

THEORY_MODULES = [
    "proof_ledger.py",
    "priority_check.py",
    "rational_certificate.py",
    "self_audit.py",
    "long_horizon_session.py",
]

# Set to False by --fast: skips the expensive mutation-catch probe.
DEEP = True

# Fragments are concatenated so this file does not match its own patterns.
MOCK_PATTERNS = [
    r"\bmock[_\- ]?(results?|data|path|analys|implement)",
    r"TODO:\s*Implement",
    "simulated" + r"\s+for now",
    r"replace with actual",
    r"real implementation would",
]

# Files that HOLD mock patterns as data (the linters themselves) must not be
# scanned by those same patterns, or the scorer reports on itself.
MOCK_SCAN_EXCLUDE = {"self_score.py", "score_selftest.py"}

REAL_API_HOSTS = [
    "export.arxiv.org",
    "api.semanticscholar.org",
    "dblp.org",
    "api.openalex.org",
    "api.crossref.org",
]


def _py_files() -> list[Path]:
    files = sorted(SKILL_ROOT.glob("scripts/*.py"))
    files += sorted(p for p in SKILL_ROOT.glob("*.py") if p.name != "self_score.py")
    return files


def _shipped_files() -> list[Path]:
    """Functional modules only: the linters hold probe patterns as data."""
    return [f for f in _py_files() if f.name not in MOCK_SCAN_EXCLUDE]


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""


# ---------------------------------------------------------------- probes


def probe_compilability() -> tuple[float, list[str]]:
    notes = []
    files = _py_files()
    if not files:
        return 0.0, ["no python files found"]
    ok = 0
    with tempfile.TemporaryDirectory() as td:
        for f in files:
            try:
                py_compile.compile(str(f), cfile=os.path.join(td, "x.pyc"), doraise=True)
                ok += 1
            except Exception as e:
                notes.append(f"FAIL compile {f.name}: {type(e).__name__}: {str(e)[:70]}")
    score = 10.0 * ok / len(files)
    if ok == len(files):
        notes.append(f"all {len(files)} modules compile")
    return round(score, 2), notes


def probe_runnability() -> tuple[float, list[str]]:
    """Every script must answer --help with exit code 0."""
    notes = []
    files = [f for f in _py_files() if f.name != "self_score.py"]
    ok = 0
    for f in files:
        try:
            r = subprocess.run(
                [sys.executable, str(f), "--help"],
                capture_output=True, text=True, timeout=30, cwd=str(SKILL_ROOT),
            )
            if r.returncode == 0:
                ok += 1
            else:
                tail = (r.stderr or r.stdout).strip().splitlines()[-1:] or [""]
                notes.append(f"FAIL --help {f.name} (rc={r.returncode}): {tail[0][:70]}")
        except subprocess.TimeoutExpired:
            notes.append(f"FAIL --help {f.name}: timeout")
        except Exception as e:
            notes.append(f"FAIL --help {f.name}: {e}")
    if not files:
        return 0.0, ["no runnable files"]
    score = 10.0 * ok / len(files)
    return round(score, 2), notes


def probe_authenticity() -> tuple[float, list[str]]:
    """Mock placeholders are penalised; real API hosts are credited."""
    notes = []
    files = [f for f in _py_files() if f.name not in MOCK_SCAN_EXCLUDE]
    if not files:
        return 0.0, ["no files"]
    dirty, total = 0, 0
    for f in files:
        src = _read(f)
        total += 1
        hits = [p for p in MOCK_PATTERNS if re.search(p, src, re.I)]
        if hits:
            dirty += 1
            notes.append(f"MOCK in {f.name}: {hits}")
    clean_ratio = 1.0 - dirty / total

    all_src = "\n".join(_read(f) for f in files)
    api_hits = sum(1 for h in REAL_API_HOSTS if h in all_src)
    api_ratio = min(1.0, api_hits / 3.0)  # 3 real sources = full credit

    score = 10.0 * (0.6 * clean_ratio + 0.4 * api_ratio)
    if api_hits:
        notes.append(f"real API hosts wired: {api_hits}")
    else:
        notes.append("no real academic API host found anywhere")
    return round(score, 2), notes


def _run_commands() -> dict[str, Path]:
    """command -> script path, parsed out of run.py's COMMANDS table."""
    src = _read(SKILL_ROOT / "run.py")
    out: dict[str, Path] = {}
    for m in re.finditer(
            r'"([a-z][a-z\-]*)"\s*:\s*\[\s*(ROOT|SCRIPTS)\s*/\s*"([^"]+\.py)"', src):
        cmd, where, name = m.group(1), m.group(2), m.group(3)
        out[cmd] = (SKILL_ROOT / name) if where == "ROOT" else (SKILL_ROOT / "scripts" / name)
    return out


FLAG_RE = re.compile(r"(?<![\w\-])(--?[A-Za-z][A-Za-z0-9_\-]*)")


def _documented_flags(md: str) -> list[tuple[str, str]]:
    """[(command, flag)] from every `run.py <cmd> ...` example in the docs.

    Backslash continuations are joined first, otherwise a wrapped command loses
    half its flags.
    """
    joined, buf = [], ""
    for line in md.splitlines():
        s = line.rstrip()
        if s.endswith("\\"):
            buf += s[:-1] + " "
            continue
        joined.append(buf + s)
        buf = ""
    if buf:
        joined.append(buf)

    out = []
    for line in joined:
        for m in re.finditer(r"run\.py\s+([a-z][a-z\-]*)", line):
            cmd = m.group(1)
            for flag in FLAG_RE.findall(line[m.end():]):
                if flag not in ("-h", "--help"):
                    out.append((cmd, flag))
    return out


def _flag_in_help(flag: str, help_text: str) -> bool:
    """Boundary-aware: `-p` must NOT match inside `--proof`."""
    return re.search(re.escape(flag) + r"(?![A-Za-z0-9_\-])", help_text) is not None


def probe_documented_flags(notes: list[str]) -> float:
    """Every flag the docs show must exist in that command's real CLI.

    Existence checks (does the file exist? is the subcommand wired?) say nothing
    about whether the documented invocation actually runs. This does.
    """
    cmds = _run_commands()
    if not cmds:
        notes.append("could not parse run.py COMMANDS table")
        return 0.0
    md = "\n".join(_read(SKILL_ROOT / n) for n in ("SKILL.md", "README.md"))
    pairs = _documented_flags(md)
    if not pairs:
        notes.append("no documented command examples found")
        return 0.0

    help_cache: dict[str, str] = {}

    def help_of(cmd: str) -> str:
        if cmd in help_cache:
            return help_cache[cmd]
        script = cmds.get(cmd)
        txt = ""
        if script and script.exists():
            try:
                r = subprocess.run([sys.executable, str(script), "--help"],
                                   capture_output=True, text=True, timeout=30,
                                   cwd=str(SKILL_ROOT))
                txt = (r.stdout or "") + (r.stderr or "")
            except Exception:
                txt = ""
        help_cache[cmd] = txt
        return txt

    unknown: list[str] = []
    seen: set[tuple[str, str]] = set()
    for cmd, flag in pairs:
        if (cmd, flag) in seen:
            continue
        seen.add((cmd, flag))
        if cmd not in cmds:
            unknown.append(f"{cmd} {flag} (no such command)")
            continue
        if not _flag_in_help(flag, help_of(cmd)):
            unknown.append(f"run.py {cmd} {flag}")
    for u in unknown:
        notes.append(f"documented flag does not exist: {u}")
    notes.append(f"{len(seen)} documented flag(s) checked against real CLIs")
    return 1.0 - len(unknown) / max(1, len(seen))


def probe_doc_consistency() -> tuple[float, list[str]]:
    """Every .py / ./run subcommand that SKILL.md advertises must exist."""
    notes = []
    skill_md = _read(SKILL_ROOT / "SKILL.md")
    if not skill_md:
        return 0.0, ["SKILL.md missing"]

    refs = set(re.findall(r"scripts/([A-Za-z0-9_\-]+\.py)", skill_md))
    refs |= set(re.findall(r"(?<![/\w])([A-Za-z0-9_\-]+\.py)(?![/\w])", skill_md))
    refs = {r for r in refs if not r.startswith("test")}
    missing = [r for r in sorted(refs) if not (SKILL_ROOT / "scripts" / r).exists()
               and not (SKILL_ROOT / r).exists()]
    for m in missing:
        notes.append(f"SKILL.md references missing file: {m}")

    subcmds = set(re.findall(r"(?:\./run|run\.py)\s+([a-z][a-z\-]*)", skill_md))
    run_py = SKILL_ROOT / "run.py"
    wired = 0
    if run_py.exists():
        rsrc = _read(run_py)
        wired = sum(1 for c in subcmds if f'"{c}"' in rsrc or f"'{c}'" in rsrc)
    else:
        notes.append("run.py entrypoint missing (SKILL.md uses ./run)")
    for c in sorted(subcmds):
        if run_py.exists() and c not in _read(run_py):
            notes.append(f"./run {c} documented but not wired in run.py")

    ref_score = 1.0 - (len(missing) / max(1, len(refs)))
    cmd_score = wired / max(1, len(subcmds)) if subcmds else 0.0
    flag_score = probe_documented_flags(notes)
    score = 10.0 * (0.35 * ref_score + 0.30 * cmd_score + 0.35 * flag_score)
    return round(score, 2), notes


def _taut_call(call: ast.Call) -> bool:
    """assertTrue(True) / assertEqual(x, x) / assertIsNone(None) ..."""
    f = call.func
    if not isinstance(f, ast.Attribute) or not f.attr.startswith("assert"):
        return False
    name, a = f.attr, call.args
    lit = lambda i: a[i] if len(a) > i else None            # noqa: E731
    c0 = lit(0)
    if name == "assertTrue" and isinstance(c0, ast.Constant) and c0.value is True:
        return True
    if name == "assertFalse" and isinstance(c0, ast.Constant) and c0.value is False:
        return True
    if name == "assertIsNone" and isinstance(c0, ast.Constant) and c0.value is None:
        return True
    if name in ("assertEqual", "assertIs", "assertIn", "assertNotEqual",
                "assertNotIn", "assertIsNot") and len(a) == 2:
        try:
            if ast.dump(a[0]) == ast.dump(a[1]):
                return True
        except Exception:
            pass
    return False


def _taut_expr(t: ast.expr) -> bool:
    """Bare `assert <expr>` that cannot fail."""
    if isinstance(t, ast.Constant):
        return t.value is True
    if isinstance(t, ast.Call):
        return _taut_call(t)
    if isinstance(t, ast.Compare) and len(t.comparators) == 1:
        try:
            return ast.dump(t.left) == ast.dump(t.comparators[0])
        except Exception:
            return False
    return False


def _is_tautological(node: ast.AST) -> bool:
    """True if this assertion node is structurally incapable of failing."""
    if isinstance(node, ast.Assert):
        return _taut_expr(node.test)
    if isinstance(node, ast.Call):
        return _taut_call(node)
    return False


def _classify_tests(src: str) -> tuple[int, int] | None:
    """(total_assertion_slots, tautological_slots) for one test module.

    Counts BARE `assert` statements AND unittest `self.assertX(...)` calls --
    a suite written with unittest methods has no bare asserts at all.
    """
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return None
    slots = []
    for n in ast.walk(tree):
        if isinstance(n, ast.Assert):
            slots.append(n)
        elif (isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
              and n.func.attr.startswith("assert")):
            slots.append(n)
    taut = sum(1 for n in slots if _is_tautological(n))
    empty = 0
    for n in ast.walk(tree):
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name.startswith("test"):
            body = [s for s in n.body
                    if not (isinstance(s, ast.Expr) and isinstance(s.value, ast.Constant))]
            if not body or all(isinstance(s, ast.Pass) for s in body):
                empty += 1
    return len(slots) + empty, taut + empty


_RUNNER: list[str] = []


def _detect_runner() -> list[str]:
    """Resolve the test runner ONCE. Probing pytest on every call cost 0.6s and,
    when pytest is absent, hid the real 2-minute unittest run behind a
    misleading `ModuleNotFoundError` fallback."""
    if _RUNNER:
        return _RUNNER
    try:
        r = subprocess.run([sys.executable, "-m", "pytest", "--version"],
                           capture_output=True, text=True, timeout=120)
        _RUNNER.extend((["pytest"], ) if r.returncode == 0 else (["unittest"], ))
    except Exception:
        _RUNNER.append("unittest")
    return _RUNNER


def _run_suite(root: Path, extra: list[str] | None = None) -> tuple[int, str]:
    """Run the test suite under `root`; returns (returncode, combined output).

    `extra` is passed to BOTH runners. unittest's `-k` is a substring filter and
    may be repeated; pytest's `-k` ANDs the expressions and also accepts repeats,
    so the same selector list is meaningful either way.
    """
    runner = _detect_runner()[0]
    if runner == "pytest":
        cmd = [sys.executable, "-m", "pytest", "-q", "--no-header", str(root / "tests")]
    else:
        cmd = [sys.executable, "-m", "unittest", "discover", "-s", "tests"]
    try:
        r = subprocess.run(cmd + (extra or []), capture_output=True, text=True,
                           timeout=900, cwd=str(root))
        return r.returncode, (r.stdout or "") + (r.stderr or "")
    except Exception:
        if runner == "pytest":                       # last-resort fallback
            r = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests"]
                               + (extra or []), capture_output=True, text=True,
                               timeout=900, cwd=str(root))
            return r.returncode, (r.stdout or "") + (r.stderr or "")
        raise


def _ran_no_tests(out: str) -> bool:
    """True when a filtered run selected zero tests.

    pytest says `no tests ran`; unittest says `Ran 0 tests`. Both spellings
    are checked because a silent zero-test run is indistinguishable from a
    pass unless you look.
    """
    low = out.lower()
    return "ran 0 tests" in low or "no tests ran" in low or "0 selected" in low


def _break_module(src: str) -> str:
    """Make a module fail at import time, so BOTH import and CLI paths break.

    The naive version (append `raise ...` at end of file) is inert: a script
    that ends with `if __name__ == '__main__': sys.exit(main())` raises
    SystemExit before reaching the appended line. Inject after the last
    top-level import instead.
    """
    marker = "\nraise RuntimeError('MUTATION')\n"
    try:
        tree = ast.parse(src)
        last = 0
        for n in tree.body:
            if isinstance(n, (ast.Import, ast.ImportFrom)):
                last = max(last, getattr(n, "end_lineno", 0) or 0)
        if last:
            lines = src.splitlines(keepends=True)
            return "".join(lines[:last]) + marker + "".join(lines[last:])
    except SyntaxError:
        pass
    return marker + src


def _mutation_catch(notes: list[str], clean_ok: bool) -> float | None:
    """Break the most-tested module in a temp copy; the suite MUST fail.

    Returns None when the probe does not apply so the caller can renormalise
    instead of scoring a non-applicable check as zero. In particular, a suite
    that is ALREADY red cannot demonstrate that it catches a regression.
    """
    if not clean_ok:
        notes.append("suite is already failing; mutation catch not applicable "
                     "(a red suite cannot demonstrate it catches regressions)")
        return None
    tests = sorted(list(SKILL_ROOT.glob("tests/test_*.py")) + list(SKILL_ROOT.glob("test*.py")))
    tsrc = "\n".join(_read(t) for t in tests)
    ranked = []
    for f in _shipped_files():
        stem = f.stem
        variants = {v for v in (stem, stem.replace("_", ""),
                               "".join(w.title() for w in stem.split("_")))
                    if len(v) > 3}
        n = sum(tsrc.count(v) for v in variants)
        ranked.append((-n, f.name, f, variants))
    ranked.sort(key=lambda r: (r[0], r[1]))
    if not ranked:
        return None
    if ranked[0][0] == 0:
        # No test names any module. That is not "not applicable" -- a suite that
        # never names the code it covers cannot be trusted to cover it. Break
        # the largest module instead: the suite must at least react to that.
        target = max(_shipped_files(), key=lambda f: _module_shape(f)[1])
        notes.append("no test names any shipped module; "
                     f"falling back to the largest one ({target.name})")
    else:
        target = ranked[0][2]
    # Recompute the selector for the CHOSEN target. Deriving it from the loop
    # variable instead silently selected whatever module happened to be last,
    # which produced an empty `-k` list and a full-suite run -- the mutation
    # probe then cost as much as the score it was supposed to be cheap.
    variants = {v for v in (target.stem, target.stem.replace("_", ""),
                           "".join(w.title() for w in target.stem.split("_")))
                if len(v) > 3}

    with tempfile.TemporaryDirectory() as td:
        dst = Path(td) / "skill"
        shutil.copytree(SKILL_ROOT, dst, ignore=shutil.ignore_patterns(
            "__pycache__", ".pytest_cache", ".git", "score-*", "dist"))
        p = dst / target.relative_to(SKILL_ROOT)
        p.write_text(_break_module(_read(p)), encoding="utf-8")
        # Only the tests whose id names this module: the question is whether
        # THIS module's tests notice. Running the whole suite a second time
        # doubles the cost of every score for no extra signal.
        sel: list[str] = []
        for v in sorted(variants):
            sel += ["-k", v]
        rc, out = _run_suite(dst, sel)
        if _ran_no_tests(out):
            # No test *id* names this module (it may be referenced by path only).
            # Correctness beats speed here: fall back to the full suite rather
            # than reporting a false failure. This branch is rare.
            notes.append(f"no test id matched {target.name}; running the full suite")
            rc, out = _run_suite(dst)

    caught = rc != 0
    if caught:
        tail = [l for l in out.splitlines() if "FAILED" in l or "FAIL:" in l or "Error" in l]
        notes.append(f"mutation in {target.name} caught by suite"
                     + (f": {tail[0].strip()[:80]}" if tail else ""))
    else:
        notes.append(f"MUTATION SURVIVED: breaking {target.name} does not fail "
                     "the suite -> the suite does not test it")
    return 1.0 if caught else 0.0


def probe_test_integrity() -> tuple[float, list[str]]:
    """A test suite that cannot fail is worse than no test suite."""
    notes = []
    tests = sorted(list(SKILL_ROOT.glob("tests/test_*.py")) + list(SKILL_ROOT.glob("test*.py")))
    if not tests:
        return 0.0, ["no test files found"]

    total_slots = 0
    taut_slots = 0
    for t in tests:
        got = _classify_tests(_read(t))
        if got is None:
            notes.append(f"{t.name} does not parse")
            continue
        a, taut = got
        total_slots += a
        taut_slots += taut
        if a == 0:
            notes.append(f"{t.name}: zero assertions -> cannot fail")
        elif taut == a:
            notes.append(f"{t.name}: every assertion is tautological -> cannot fail")
    assert_ratio = (total_slots - taut_slots) / max(1, total_slots)
    if taut_slots:
        notes.append(f"{taut_slots}/{total_slots} assertion slot(s) are tautological")

    # legacy self-confirming suite still present?
    legacy = SKILL_ROOT / "test_suit.py"

    rc, out = _run_suite(SKILL_ROOT)
    executed, passed = True, rc == 0
    runner = "pytest" if "pytest" in out[:200] or "passed" in out else "unittest"
    notes.append(f"{runner} rc={rc}")
    if not passed:
        tail = [l for l in out.splitlines() if "FAILED" in l or "FAIL:" in l or "Error" in l]
        notes += [t.strip()[:110] for t in tail[:5]]
    if legacy.exists():
        notes.append("legacy self-confirming test_suit.py still shipped")

    # (weight, value) components; None = not applicable / skipped -> renormalise
    components = [
        (0.25, assert_ratio),
        (0.25, 1.0 if (executed and passed) else 0.0),
        (0.40, _mutation_catch(notes, passed) if DEEP else None),
        (0.10, 1.0 if not legacy.exists() else 0.0),
    ]
    live = [(w, v) for w, v in components if v is not None]
    if not DEEP:
        notes.append("fast mode: mutation-catch probe skipped")
    score = 10.0 * sum(w * v for w, v in live) / sum(w for w, _ in live)
    return round(score, 2), notes


def probe_portability() -> tuple[float, list[str]]:
    notes = []
    checks = {}

    run_py = SKILL_ROOT / "run.py"
    checks["cross-platform run.py"] = run_py.exists()
    if not run_py.exists():
        notes.append("no run.py (bash-only ./run is unusable on Windows)")

    # shebang lines are portable; only flag python3 used as an invocation
    all_src = "\n".join(
        re.sub(r"^#!.*$", "", _read(f), flags=re.M) for f in _shipped_files())
    checks["no hardcoded python3"] = not re.search(r"python3\s", all_src)
    if not checks["no hardcoded python3"]:
        notes.append("hardcoded 'python3' invocation found")

    unix_tmp = len(re.findall(r"/tmp/|/home/[a-z]+/", all_src))
    checks["no unix-only paths"] = unix_tmp == 0
    if unix_tmp:
        notes.append(f"{unix_tmp} unix-only absolute path(s) hardcoded")

    checks["requirements declared"] = (SKILL_ROOT / "requirements.txt").exists()
    if not checks["requirements declared"]:
        notes.append("requirements.txt missing")

    checks["references/ present"] = (SKILL_ROOT / "references").is_dir()
    if not checks["references/ present"]:
        notes.append("references/ directory missing (declared in SKILL.md)")

    score = 10.0 * sum(1 for v in checks.values() if v) / len(checks)
    return round(score, 2), notes


def _module_shape(path: Path) -> tuple[int, int]:
    """(top-level defs/classes, non-blank non-comment lines)."""
    src = _read(path)
    loc = len([l for l in src.splitlines() if l.strip() and not l.strip().startswith("#")])
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return 0, loc
    defs = sum(1 for n in tree.body
               if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)))
    return defs, loc


def _module_is_real(path: Path) -> bool:
    """A file that merely exists is not a module; it must have a shape."""
    defs, loc = _module_shape(path)
    return defs >= 3 and loc >= 40


def probe_fitness() -> tuple[float, list[str]]:
    """Theory-track coverage: this user is a theory ML PhD, not a CV empiricist.

    Presence alone is NOT credited: a stub named proof_ledger.py does not make
    this a theory skill.
    """
    notes = []
    present = []
    for m in THEORY_MODULES:
        p = SKILL_ROOT / "scripts" / m
        if not p.exists():
            notes.append(f"theory module missing: {m}")
        elif not _module_is_real(p):
            defs, loc = _module_shape(p)
            notes.append(f"theory module is a stub: {m} (defs={defs}, loc={loc})")
        else:
            present.append(m)
    skill_md = _read(SKILL_ROOT / "SKILL.md")
    routed = bool(re.search(r"--track\s*=\s*(theory|empirical)", skill_md))
    if not routed:
        notes.append("SKILL.md has no --track=theory|empirical routing")
    score = 10.0 * (0.75 * len(present) / len(THEORY_MODULES) + 0.25 * (1.0 if routed else 0.0))
    return round(score, 2), notes


def probe_substance() -> tuple[float, list[str]]:
    """Does the skill contain real code, or only files with the right names?

    Guards the vacuity failure mode: stubs compile, answer --help, carry no
    mock markers, and satisfy every existence check.
    """
    notes = []
    files = _shipped_files()
    if not files:
        return 0.0, ["no shipped modules"]

    loc = 0
    defs = 0
    for f in files:
        d, l = _module_shape(f)
        defs += d
        loc += l

    help_ok, help_total, help_bad = 0, 0, []
    for f in files:
        try:
            r = subprocess.run([sys.executable, str(f), "--help"],
                               capture_output=True, text=True, timeout=30,
                               cwd=str(SKILL_ROOT))
        except Exception:
            continue
        help_total += 1
        if r.returncode == 0 and len(r.stdout or "") >= SUBSTANCE_TARGET["help_chars"]:
            help_ok += 1
        else:
            help_bad.append(f.name)
    if help_bad:
        notes.append(f"thin --help (<{SUBSTANCE_TARGET['help_chars']} chars): "
                     f"{', '.join(help_bad[:6])}")

    skill_md = _read(SKILL_ROOT / "SKILL.md")
    cmds = len(re.findall(r"(?:run\.py|python[^\s]*\s+\S*\.py)\s+[a-z]", skill_md))

    t = SUBSTANCE_TARGET
    loc_r = min(1.0, loc / t["loc"])
    def_r = min(1.0, defs / t["defs"])
    help_r = help_ok / max(1, help_total)
    cmd_r = min(1.0, cmds / t["cmds"])
    notes.append(f"loc={loc}/{t['loc']}  defs={defs}/{t['defs']}  "
                 f"help={help_ok}/{help_total}  documented_cmds={cmds}/{t['cmds']}")
    score = 10.0 * (0.35 * loc_r + 0.25 * def_r + 0.30 * help_r + 0.10 * cmd_r)
    return round(score, 2), notes


# Outputs of the skill's own commands. If any of these sit in the skill
# directory, a command wrote its result into the installation instead of the
# user's project. The scorer's own reports are sanctioned.
GENERATED_PREFIXES = (
    "math-notation-check", "compliance-audit-", "search-results-", "search-summary-",
    "self-audit-", "certificate-", "compliance-status.json", "session.json",
    "claims.json", "priority-records.json", "revision-history.json",
    "experiment-design", "analysis", "index.html", "main.tex",
)
SANCTIONED_IN_ROOT = {"score-report.md", "score-selftest-report.md", "score-history.json"}
# Directories that legitimately live inside the skill (source, not output).
SOURCE_DIRS = {"scripts", "tests", "references", "assets", "dist",
                "__pycache__", ".pytest_cache", ".github", ".idea"}


def _stray_artifacts() -> list[str]:
    """Generated output that leaked into the installation instead of the
    user's project.

    Scans SUBDIRECTORIES too: a root-only scan missed
    `07-audit-trail/certificate-*.json`, which is exactly as much a leak as a
    root-level `math-notation-check.md` and just as invisible to the user.
    """
    try:
        entries = sorted(SKILL_ROOT.rglob("*"))
    except Exception:
        return []
    out = []
    for p in entries:
        if not p.is_file():
            continue
        if p.name in SANCTIONED_IN_ROOT:
            continue
        if any(part in SOURCE_DIRS or part.endswith(".egg-info") for part in p.parts):
            continue
        if p.suffix in {".pyc", ".pyo"}:
            continue
        if any(p.name.startswith(pre) for pre in GENERATED_PREFIXES):
            out.append(p.relative_to(SKILL_ROOT).as_posix())
    return sorted(out)


def probe_hygiene() -> tuple[float, list[str]]:
    notes = []
    checks = {}
    versions = set()
    for name in ("SKILL.md", "README.md", "_meta.json", "run.py"):
        p = SKILL_ROOT / name
        if not p.exists():
            continue
        src = _read(p)
        versions |= set(re.findall(r'"version"\s*:\s*"([0-9]+\.[0-9]+\.[0-9]+)"', src))
        versions |= set(re.findall(r"[Vv]ersion:?\s*\**\s*([0-9]+\.[0-9]+\.[0-9]+)", src))
        # README/CHANGELOG style: "v2.3.0" without the word "version"
        versions |= set(re.findall(r"\bv([0-9]+\.[0-9]+\.[0-9]+)\b", src))
    checks["single version"] = len(versions) == 1
    if len(versions) > 1:
        notes.append(f"version strings disagree: {sorted(versions)}")

    checks["no typo filenames"] = not (SKILL_ROOT / "test_suit.py").exists()
    if not checks["no typo filenames"]:
        notes.append("misspelled test_suit.py present")

    # Regression guard: run.py used to pin its cwd to the install directory, so
    # every command with a relative default output wrote INTO the skill folder.
    checks["no generated artifacts"] = not (stray := _stray_artifacts())
    if stray:
        notes.append(f"generated output leaked into the skill directory: {', '.join(stray)}")

    all_src = "\n".join(_read(f) for f in _shipped_files())
    checks["no foreign attribution"] = "openclaw" not in all_src.lower()
    if not checks["no foreign attribution"]:
        notes.append("foreign attribution (openclaw) still in shipped code")

    # "\\n" (double-escaped) is the v1.x corruption that printed a literal \n;
    # a single "\n" inside a normal string literal is fine.
    checks["no double-escaped newline"] = re.search(r"\\\\n(?![A-Za-z])", all_src) is None
    if not checks["no double-escaped newline"]:
        hit = [f.name for f in _shipped_files() if re.search(r"\\\\n(?![A-Za-z])", _read(f))]
        notes.append(f"double-escaped '\\n' in: {hit}")
    score = 10.0 * sum(1 for v in checks.values() if v) / len(checks)
    return round(score, 2), notes


PROBES = {
    "compilability": probe_compilability,
    "runnability": probe_runnability,
    "authenticity": probe_authenticity,
    "doc_consistency": probe_doc_consistency,
    "test_integrity": probe_test_integrity,
    "portability": probe_portability,
    "fitness": probe_fitness,
    "substance": probe_substance,
    "hygiene": probe_hygiene,
}


def apply_caps(result: dict) -> dict:
    """One collapsed dimension caps the total; weights must not dilute it."""
    total = result["total"]
    applied = []
    for dim, floor, cap, why in CAPS:
        d = result["dimensions"].get(dim)
        if d is None:          # not measured in this run (--only)
            continue
        if d["score"] < floor:
            applied.append(f"{dim}={d['score']} < {floor} -> total capped at {cap} ({why})")
            total = min(total, cap)
    result["total"] = round(total, 2)
    result["caps"] = applied
    return result


def run_score() -> dict:
    dims = {}
    for name, fn in PROBES.items():
        s, notes = fn()
        dims[name] = {"score": s, "weight": WEIGHTS[name], "notes": notes}
    total = round(10.0 * sum(d["score"] * d["weight"] for d in dims.values()), 2)
    result = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "total": total,
        "dimensions": dims,
    }
    return apply_caps(result)


def render_markdown(result: dict, history: list[dict]) -> str:
    lines = [
        "# Skill Quality Score",
        "",
        f"**Generated:** {result['timestamp']}  ",
        f"**Total: {result['total']} / 100**",
        "",
        "| Dimension | Weight | Score | Status |",
        "|---|---:|---:|---|",
    ]
    for name, d in result["dimensions"].items():
        s = d["score"]
        mark = "OK" if s >= 8 else ("PARTIAL" if s >= 5 else "FAIL")
        lines.append(f"| {name} | {d['weight']} | {s} / 10 | {mark} |")
    if result.get("caps"):
        lines += ["", "## Caps applied", ""]
        for c in result["caps"]:
            lines.append(f"- {c}")
    lines += ["", "## Findings", ""]
    for name, d in result["dimensions"].items():
        if d["notes"]:
            lines.append(f"### {name}")
            for n in d["notes"]:
                lines.append(f"- {n}")
            lines.append("")
    if len(history) > 1:
        lines += ["## Score history", "", "| # | Time | Total |", "|---:|---|---:|"]
        for i, h in enumerate(history, 1):
            lines.append(f"| {i} | {h['timestamp']} | {h['total']} |")
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description="Automated quality score for this skill")
    ap.add_argument("--no-history", action="store_true", help="do not append to score-history.json")
    ap.add_argument("--markdown", type=str, default=None, help="also write a markdown report")
    ap.add_argument("--quiet", action="store_true")
    ap.add_argument("--only", type=str, default=None,
                    help="run only these dimensions, comma-separated (fast, for mutation tests)")
    ap.add_argument("--fast", action="store_true",
                    help="skip the mutation-catch probe (spawns a second suite run)")
    ap.add_argument("--json", type=str, default=None, help="write raw scores to this JSON path")
    args = ap.parse_args()

    global PROBES, DEEP
    DEEP = not args.fast
    if args.only:
        wanted = {w.strip() for w in args.only.split(",") if w.strip()}
        unknown = wanted - set(PROBES)
        if unknown:
            print(f"unknown dimension(s): {sorted(unknown)}", file=sys.stderr)
            return 2
        PROBES = {k: v for k, v in PROBES.items() if k in wanted}

    result = run_score()
    if args.json:
        Path(args.json).write_text(json.dumps(result, indent=2), encoding="utf-8")
    history_path = SKILL_ROOT / "score-history.json"
    history = []
    if history_path.exists():
        try:
            history = json.loads(_read(history_path))
        except Exception:
            history = []

    if not args.no_history:
        history.append({"timestamp": result["timestamp"], "total": result["total"],
                        "dims": {k: v["score"] for k, v in result["dimensions"].items()}})
        history_path.write_text(json.dumps(history, indent=2), encoding="utf-8")

    if args.markdown:
        Path(args.markdown).write_text(
            render_markdown(result, history), encoding="utf-8")

    if not args.quiet:
        print(f"\n=== PhD Research Companion quality score ===")
        for name, d in result["dimensions"].items():
            bar = "#" * int(round(d["score"]))
            print(f"  {name:<16} {d['score']:>5.2f}/10  w={d['weight']:<5} {bar}")
        print(f"  {'TOTAL':<16} {result['total']:>5.2f}/100")
        for c in result.get("caps", []):
            print(f"  CAP: {c}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
