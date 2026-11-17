#!/usr/bin/env python3
"""
Mutation test for the scorer itself.

A score of 100 means nothing if the scorer cannot go down. This script copies
the skill to a temp directory, injects ONE known defect per dimension, and
checks that the corresponding score actually drops.

A dimension that does not react to its own defect is a BLIND SPOT: it is
reporting a number, not measuring anything.

Phase 2 (vacuity) asks the opposite question: can a skill with NO substance
still score 100? Mutation testing cannot answer that -- it only ever ADDS a
defect to real code. Vacuity attacks REMOVE the substance and check that the
total stays under a ceiling.

Usage:
    python score_selftest.py
    python score_selftest.py --verbose
    python score_selftest.py --phase mutation|vacuity
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
PY = sys.executable

EXCLUDE_DIRS = {"__pycache__", ".git", ".pytest_cache"}
EXCLUDE_FILES = {"score-history.json", "score-report.md", "score-selftest-report.md"}

# dimension -> (relative file, mutation callable, human description)
MUTATIONS = {
    "compilability": ("scripts/verify_math_notation.py",
                      lambda s: s.replace("def main() -> int:", "def main(: -> int:\n    pass\ndef _old() -> int:", 1),
                      "syntax error injected into a shipped script"),
    "runnability": ("scripts/revision_tracker.py",
                    lambda s: s.replace("def main() -> int:", "def main() -> int:\n    sys.exit(3)", 1),
                    "script made to exit non-zero even for --help"),
    "authenticity": ("scripts/check_compliance.py",
                     lambda s: s + "\n\nmock_results = []  # TODO: Implement\n",
                     "mock placeholder injected into shipped code"),
    "doc_consistency": ("SKILL.md",
                        lambda s: s + "\nSee scripts/definitely_missing_module.py for details.\n",
                        "documentation references a file that does not exist"),
    "test_integrity": ("tests/test_skill.py",
                       lambda s: s.replace("self.assertEqual(r.returncode, 2)",
                                           "self.assertEqual(r.returncode, 999)", 1),
                       "an assertion made unsatisfiable"),
    "portability": ("scripts/create_experiment_design.py",
                    lambda s: s.replace('default="."', 'default="/tmp/phd-default"', 1),
                    "unix-only absolute path hardcoded"),
    "fitness": ("scripts/proof_ledger.py", None, "theory module deleted"),
    "substance": (None, None, "every shipped module replaced by a stub"),
    "hygiene": ("README.md",
                lambda s: s.replace("v2.4.0", "v9.9.9", 1),
                "version string made inconsistent"),
}

# A module that compiles, answers --help, and does nothing.
STUB = ("import argparse\n\n\ndef main() -> int:\n"
        "    argparse.ArgumentParser(description='stub').parse_args()\n"
        "    return 0\n\n\nif __name__ == '__main__':\n    raise SystemExit(main())\n")


def stub_all_modules(root: Path) -> None:
    for f in list((root / "scripts").glob("*.py")) + list(root.glob("*.py")):
        if f.name == "self_score.py":
            continue          # the scorer itself must survive
        f.write_text(STUB, encoding="utf-8")


def tautological_suite(root: Path) -> None:
    body = ["import unittest", "", "", "class T(unittest.TestCase):"]
    for i in range(37):
        body += [f"    def test_{i}(self):", "        assert True",
                 "        self.assertEqual(1, 1)", ""]
    (root / "tests").mkdir(exist_ok=True)
    (root / "tests" / "test_skill.py").write_text("\n".join(body), encoding="utf-8")


def empty_shell(root: Path) -> None:
    for name in ("scripts", "tests", "references", ".github"):
        d = root / name
        if d.is_dir():
            shutil.rmtree(d, ignore_errors=True)
    for name in ("run.py", "init_research_project.py", "install_verify.sh",
                 "requirements.txt", "README.md", "BACKGROUND-RUN.md", "_meta.json",
                 "_skillhub_meta.json"):
        p = root / name
        if p.exists():
            p.unlink()
    (root / "scripts").mkdir(exist_ok=True)
    shutil.copy2(SKILL_ROOT / "scripts" / "self_score.py", root / "scripts" / "self_score.py")
    (root / "SKILL.md").write_text("# Empty Skill\n\nIt does nothing. See docs.\n",
                                   encoding="utf-8")


# name -> (attack, ceiling). Observed: 60.0 / 60.0 / 50.0 / 23.2
VACUITY = {
    "no tests at all": (
        lambda root: shutil.rmtree(root / "tests", ignore_errors=True), 70.0),
    "suite of 37 tautological tests": (tautological_suite, 70.0),
    "every module stubbed out": (stub_all_modules, 60.0),
    "empty shell (no code, no tests)": (empty_shell, 40.0),
}


def copy_skill(dest: Path) -> None:
    dest.mkdir(parents=True, exist_ok=True)
    for item in SKILL_ROOT.iterdir():
        if item.name in EXCLUDE_DIRS or item.name in EXCLUDE_FILES:
            continue
        if item.is_dir():
            shutil.copytree(item, dest / item.name,
                            ignore=shutil.ignore_patterns(*EXCLUDE_DIRS, *EXCLUDE_FILES))
        else:
            shutil.copy2(item, dest / item.name)


def score_dim(root: Path, dim: str) -> float | None:
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tf:
        out = tf.name
    r = subprocess.run(
        [PY, str(root / "scripts" / "self_score.py"), "--only", dim,
         "--no-history", "--quiet", "--json", out],
        capture_output=True, text=True, timeout=300, cwd=str(root))
    try:
        data = json.loads(Path(out).read_text(encoding="utf-8"))
        return data["dimensions"][dim]["score"]
    except Exception:
        print(f"    scorer failed on {dim}: rc={r.returncode} {r.stderr[:200]}", file=sys.stderr)
        return None


def score_total(root: Path) -> tuple[float | None, list[str]]:
    """Full score (all dimensions) of a skill tree, plus any caps applied."""
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tf:
        out = tf.name
    subprocess.run(
        [PY, str(root / "scripts" / "self_score.py"),
         "--no-history", "--quiet", "--json", out],
        capture_output=True, text=True, timeout=600, cwd=str(root))
    try:
        data = json.loads(Path(out).read_text(encoding="utf-8"))
        return data["total"], data.get("caps", [])
    except Exception:
        return None, []


def apply_mutation(root: Path, rel: str | None, mutator) -> None:
    if rel is None and mutator is None:
        stub_all_modules(root)          # substance: the vacuity attack
    elif mutator is None:
        (root / rel).unlink()
    else:
        p = root / rel
        p.write_text(mutator(p.read_text(encoding="utf-8")), encoding="utf-8")


def phase_mutation(verbose: bool) -> tuple[int, list]:
    print("Phase 1 - mutation: every dimension must react to its own defect\n")
    with tempfile.TemporaryDirectory() as td:
        clean_root = Path(td) / "clean"
        copy_skill(clean_root)
        baseline = {dim: score_dim(clean_root, dim) for dim in MUTATIONS}
    if any(v is None for v in baseline.values()):
        print("baseline scoring failed; aborting", file=sys.stderr)
        return 2, []

    results = []
    for dim, (rel, mutator, desc) in MUTATIONS.items():
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "mut"
            copy_skill(root)
            apply_mutation(root, rel, mutator)
            after = score_dim(root, dim)
        before = baseline[dim]
        if after is None:
            results.append((dim, before, None, desc, "ERROR"))
            continue
        results.append((dim, before, after, desc,
                        "FALSIFIABLE" if after < before else "BLIND SPOT"))

    print(f"{'dimension':<16}{'clean':>7}{'mutated':>9}   verdict")
    print("-" * 58)
    blind = 0
    for dim, before, after, desc, verdict in results:
        a = f"{after:.2f}" if after is not None else "err"
        print(f"{dim:<16}{before:>7.2f}{a:>9}   {verdict}")
        if verbose:
            print(f"{'':<16}defect: {desc}")
        if verdict != "FALSIFIABLE":
            blind += 1
    print()
    if blind:
        print(f"{blind} dimension(s) do NOT react to their own defect.")
        print("Those numbers are decoration, not measurement.")
    else:
        print(f"All {len(results)} dimensions are falsifiable: "
              "each drops when its own defect is injected.")
    return blind, results


def phase_vacuity(verbose: bool) -> tuple[int, list]:
    print("\nPhase 2 - vacuity: a skill with no substance must NOT score high\n")
    rows = []
    bad = 0
    for name, (attack, ceiling) in VACUITY.items():
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "vac"
            copy_skill(root)
            attack(root)
            total, caps = score_total(root)
        ok = total is not None and total <= ceiling
        if not ok:
            bad += 1
        rows.append((name, total, ceiling, caps, "OK" if ok else "VACUOUS PASS"))
        t = f"{total:.2f}" if total is not None else "err"
        print(f"{name:<34}{t:>8}   ceiling {ceiling:>5.1f}   "
              f"{'OK' if ok else 'VACUOUS PASS'}")
        if verbose:
            for c in caps:
                print(f"{'':<34}cap: {c}")
    print()
    if bad:
        print(f"{bad} vacuity attack(s) still score above their ceiling.")
        print("The scorer rewards the APPEARANCE of quality over its presence.")
    else:
        print(f"All {len(rows)} vacuity attacks are held below their ceiling.")
    return bad, rows


def main() -> int:
    ap = argparse.ArgumentParser(description="Audit the quality scorer itself")
    ap.add_argument("--verbose", "-v", action="store_true")
    ap.add_argument("--phase", choices=("mutation", "vacuity", "all"), default="all")
    args = ap.parse_args()

    blind = vac = 0
    mut_rows: list = []
    vac_rows: list = []
    if args.phase in ("mutation", "all"):
        blind, mut_rows = phase_mutation(args.verbose)
        if blind == 2:
            return 2
    if args.phase in ("vacuity", "all"):
        vac, vac_rows = phase_vacuity(args.verbose)

    lines = ["# Scorer audit", "",
             f"Run: {__import__('datetime').datetime.now().isoformat(timespec='seconds')}", ""]
    if mut_rows:
        lines += ["## Phase 1 - mutation (a dimension must react to its own defect)", "",
                  "| Dimension | Clean | Mutated | Verdict | Defect injected |",
                  "|---|---:|---:|---|---|"]
        for dim, before, after, desc, verdict in mut_rows:
            a = f"{after:.2f}" if after is not None else "error"
            lines.append(f"| {dim} | {before:.2f} | {a} | **{verdict}** | {desc} |")
        lines.append("")
    if vac_rows:
        lines += ["## Phase 2 - vacuity (no substance must not score high)", "",
                  "| Attack | Total | Ceiling | Verdict |",
                  "|---|---:|---:|---|---|"]
        for name, total, ceiling, caps, verdict in vac_rows:
            t = f"{total:.2f}" if total is not None else "error"
            lines.append(f"| {name} | {t} | {ceiling:.1f} | **{verdict}** |")
        lines.append("")
    lines += ["A dimension that does not drop is reporting a number without measuring",
              "anything. An attack that scores above its ceiling means the scorer",
              "rewards the appearance of quality over its presence.", ""]
    report = SKILL_ROOT / "score-selftest-report.md"
    report.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nReport: {report}")

    return 1 if (blind or vac) else 0


if __name__ == "__main__":
    sys.exit(main())
