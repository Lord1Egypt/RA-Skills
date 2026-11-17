#!/usr/bin/env python3
"""
Real test suite for phd-research-companion.

Written with unittest so it runs under `python -m unittest discover` (stdlib,
no dependency) and under `pytest` alike. Every test asserts something that can
fail. There is no "print success at the end" path.

Run:
    python -m unittest discover -s tests -v
    python -m pytest tests -q
"""

import importlib.util
import json
import py_compile
import re
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
PY = sys.executable


def load(name: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run_cli(script: Path, *args, cwd=None):
    return subprocess.run([PY, str(script), *args], capture_output=True,
                          text=True, timeout=120, cwd=str(cwd or ROOT))


class TestCompilation(unittest.TestCase):
    def test_every_script_compiles(self):
        files = sorted(SCRIPTS.glob("*.py")) + [ROOT / "run.py", ROOT / "init_research_project.py"]
        self.assertGreaterEqual(len(files), 10, "expected at least 10 modules")
        with tempfile.TemporaryDirectory() as td:
            for f in files:
                with self.subTest(f=f.name):
                    py_compile.compile(str(f), cfile=str(Path(td) / f"{f.stem}.pyc"),
                                       doraise=True)


class TestCLI(unittest.TestCase):
    def test_every_script_answers_help(self):
        files = sorted(SCRIPTS.glob("*.py")) + [ROOT / "init_research_project.py"]
        for f in files:
            with self.subTest(f=f.name):
                r = run_cli(f, "--help")
                self.assertEqual(r.returncode, 0,
                                 f"{f.name} --help failed: {r.stderr[-300:]}")

    def test_run_unknown_command_exits_2(self):
        r = subprocess.run([PY, str(ROOT / "run.py"), "definitely-not-a-command"],
                           capture_output=True, text=True, cwd=str(ROOT))
        self.assertEqual(r.returncode, 2)

    def test_run_help_exits_0(self):
        r = subprocess.run([PY, str(ROOT / "run.py"), "help"],
                           capture_output=True, text=True, cwd=str(ROOT))
        self.assertEqual(r.returncode, 0)
        self.assertIn("search", r.stdout)


class TestInit(unittest.TestCase):
    def test_init_places_dashboard_inside_00_dashboard(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "proj"
            r = run_cli(ROOT / "init_research_project.py", "-d", "test domain",
                        "-j", "JMLR", "-o", str(out))
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertTrue((out / "00-dashboard" / "index.html").is_file(),
                            "dashboard must be created in 00-dashboard/, not project root")
            self.assertFalse((out / "index.html").exists(),
                             "dashboard must not be dumped at project root")
            for d in ("01-literature-survey", "02-methodology-dev", "03-paper-drafting",
                      "04-experiments", "05-revision-rounds", "06-collaboration",
                      "07-audit-trail"):
                self.assertTrue((out / d).is_dir(), f"missing {d}")
            self.assertTrue((out / "project.json").is_file())

    def test_init_readme_uses_given_domain(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "proj"
            run_cli(ROOT / "init_research_project.py", "-d", "zebra grazing theory",
                    "-o", str(out))
            readme = (out / "README.md").read_text(encoding="utf-8")
            self.assertIn("zebra grazing theory", readme)
            self.assertNotIn("network traffic", readme.lower())


class TestLatexTemplate(unittest.TestCase):
    def test_generated_tex_is_balanced_and_has_docclass(self):
        with tempfile.TemporaryDirectory() as td:
            r = run_cli(SCRIPTS / "generate_latex_template.py", "-j", "JMLR",
                        "-t", "A Title", "-a", "Author One",
                        "--track", "theory", "-o", td)
            self.assertEqual(r.returncode, 0, r.stderr)
            tex = (Path(td) / "main.tex").read_text(encoding="utf-8")
            self.assertIn("\\documentclass", tex)
            self.assertIn("\\begin{document}", tex)
            self.assertIn("\\end{document}", tex)
            self.assertNotIn("%%TITLE%%", tex, "unsubstituted placeholder left behind")
            self.assertEqual(tex.count("{"), tex.count("}"), "unbalanced braces")
            self.assertTrue((Path(td) / "references.bib").exists())

    def test_theory_track_emits_theorem_env(self):
        with tempfile.TemporaryDirectory() as td:
            run_cli(SCRIPTS / "generate_latex_template.py", "-j", "JMLR",
                    "--track", "theory", "-o", td)
            tex = (Path(td) / "main.tex").read_text(encoding="utf-8")
            self.assertIn("\\begin{theorem}", tex)
            self.assertIn("\\begin{proof}", tex)


class TestRevisionTracker(unittest.TestCase):
    def test_round_roundtrip_and_evidence_hash(self):
        with tempfile.TemporaryDirectory() as td:
            ev = Path(td) / "evidence.txt"
            ev.write_text("diff content", encoding="utf-8")
            tracker_dir = Path(td) / "05-revision-rounds"
            r = run_cli(SCRIPTS / "revision_tracker.py", "--action", "add_round",
                        "-r", "2", "-i", "weak baseline", "lemma 4 gap",
                        "-x", "fixed both", "-e", str(ev), "-d", str(tracker_dir))
            self.assertEqual(r.returncode, 0, r.stderr)
            hist = (tracker_dir / "revision-history.json").read_text(encoding="utf-8")
            self.assertIn('"round": 2', hist)
            self.assertIn("sha256", hist)
            r2 = run_cli(SCRIPTS / "revision_tracker.py", "--action", "summary",
                         "-d", str(tracker_dir))
            self.assertIn("2/5", r2.stdout)

    def test_missing_evidence_is_recorded_not_ignored(self):
        with tempfile.TemporaryDirectory() as td:
            tracker_dir = Path(td) / "rev"
            r = run_cli(SCRIPTS / "revision_tracker.py", "--action", "add_round",
                        "-r", "1", "-i", "x", "-x", "y",
                        "-e", str(Path(td) / "nope.diff"), "-d", str(tracker_dir))
            self.assertEqual(r.returncode, 0)
            report = run_cli(SCRIPTS / "revision_tracker.py", "--action", "report",
                             "-d", str(tracker_dir))
            self.assertIn("MISSING", (tracker_dir / "revision-tracking-report.md")
                          .read_text(encoding="utf-8"))


class TestMathVerifier(unittest.TestCase):
    def _write(self, td, body):
        p = Path(td) / "main.tex"
        p.write_text(body, encoding="utf-8")
        return p

    def test_flags_undefined_command(self):
        with tempfile.TemporaryDirectory() as td:
            tex = self._write(td, r"""
\documentclass{article}
\begin{document}
\begin{theorem}
\[
  \zzzfoo + \alpha \leq \zzzbar
\]
\end{theorem}
\end{document}
""")
            r = run_cli(SCRIPTS / "verify_math_notation.py", "-i", str(tex),
                        "-o", str(Path(td) / "out.md"))
            self.assertEqual(r.returncode, 0, r.stderr)
            report = (Path(td) / "out.md").read_text(encoding="utf-8")
            self.assertIn("zzzfoo", report)
            self.assertNotIn("\\alpha", report.split("| Command")[1].split("|---|")[1]
                             if "| Command" in report else "", "standard cmd must not be flagged")

    def test_strict_exits_1_when_undefined(self):
        with tempfile.TemporaryDirectory() as td:
            tex = self._write(td, r"\documentclass{article}\begin{document}$\qqqzz$\end{document}")
            r = run_cli(SCRIPTS / "verify_math_notation.py", "-i", str(tex),
                        "-o", str(Path(td) / "o.md"), "--strict")
            self.assertEqual(r.returncode, 1)

    def test_defined_command_is_not_flagged(self):
        with tempfile.TemporaryDirectory() as td:
            tex = self._write(td, r"""
\documentclass{article}
\newcommand{\regret}{R_T}
\begin{document}
\[
\regret \leq \alpha
\]
\end{document}
""")
            r = run_cli(SCRIPTS / "verify_math_notation.py", "-i", str(tex),
                        "-o", str(Path(td) / "o.md"), "--strict")
            self.assertEqual(r.returncode, 0, "newcommand-defined symbol must not be flagged")


class TestCompliance(unittest.TestCase):
    def test_empty_project_does_not_crash_and_marks_unverified(self):
        with tempfile.TemporaryDirectory() as td:
            r = run_cli(SCRIPTS / "check_compliance.py", "-p", td)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertIn("UNVERIFIED", r.stdout)

    def test_ready_project_scores_high(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td)
            (p / "01-literature-survey").mkdir()
            (p / "01-literature-survey" / "lib.bib").write_text(
                "\n".join(f"@article{{k{i},\n  title={{T{i}}},\n}}\n" for i in range(60)),
                encoding="utf-8")
            (p / "04-experiments").mkdir()
            for f in ("experiment-comparison-design.yaml", "experiment-ablation-design.yaml",
                      "experiment-robustness-design.yaml"):
                (p / "04-experiments" / f).write_text("kind: x\n", encoding="utf-8")
            (p / "03-paper-drafting").mkdir()
            (p / "03-paper-drafting" / "main.tex").write_text(
                r"\documentclass{article}\begin{document}\begin{abstract}A\end{abstract}"
                r"\bibliography{references}\end{document}", encoding="utf-8")
            (p / "03-paper-drafting" / "math-notation-check.md").write_text(
                "Notation Discrepancies Identified: 0", encoding="utf-8")
            (p / "05-revision-rounds").mkdir()
            (p / "05-revision-rounds" / "revision-history.json").write_text(
                '{"rounds_completed": 5, "total_issues": 3, "rounds": []}', encoding="utf-8")
            r = run_cli(SCRIPTS / "check_compliance.py", "-p", str(p))
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertEqual(r.stdout.count("[PASS"), 7,
                             f"expected 7 passes (figures stay unverified), got:\n{r.stdout}")


class TestExperimentDesign(unittest.TestCase):
    def test_results_are_null_not_fabricated(self):
        with tempfile.TemporaryDirectory() as td:
            r = run_cli(SCRIPTS / "create_experiment_design.py", "--type", "comparison",
                        "--datasets", "A,B", "--baselines", "X,Y", "-o", td)
            self.assertEqual(r.returncode, 0, r.stderr)
            y = (Path(td) / "experiment-comparison-design.yaml").read_text(encoding="utf-8")
            self.assertIn("results: null", y)
            self.assertIn("seeds", y)

    def test_comparison_requires_datasets(self):
        with tempfile.TemporaryDirectory() as td:
            r = run_cli(SCRIPTS / "create_experiment_design.py", "--type", "comparison",
                        "-o", td)
            self.assertEqual(r.returncode, 2)


def make_png_with_dpi(path: Path, dpi: int) -> Path:
    """Minimal PNG carrying a pHYs chunk at the given DPI (for header parsing)."""
    import struct, zlib
    ppu = int(round(dpi / 0.0254))

    def chunk(tag: bytes, data: bytes) -> bytes:
        return (len(data).to_bytes(4, "big") + tag + data
                + zlib.crc32(tag + data).to_bytes(4, "big"))

    ihdr = struct.pack(">IIBBBBB", 1, 1, 8, 0, 0, 0, 0)
    phys = struct.pack(">IIB", ppu, ppu, 1)
    body = (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
            + chunk(b"pHYs", phys) + chunk(b"IDAT", zlib.compress(b"\x00\x00\x00\x00"))
            + chunk(b"IEND", b""))
    path.write_bytes(body)
    return path


class TestFigureDpi(unittest.TestCase):
    def test_reads_dpi_from_png_header(self):
        mod = load("check_compliance")
        with tempfile.TemporaryDirectory() as td:
            p = make_png_with_dpi(Path(td) / "a.png", 300)
            self.assertEqual(mod.ComplianceChecker.dpi_of(p), 300)
            q = make_png_with_dpi(Path(td) / "b.png", 96)
            self.assertEqual(mod.ComplianceChecker.dpi_of(q), 96)

    def test_high_dpi_figures_pass(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "proj"
            (p / "03-paper-drafting").mkdir(parents=True)
            make_png_with_dpi(p / "03-paper-drafting" / "fig1.png", 600)
            r = run_cli(SCRIPTS / "check_compliance.py", "-p", str(p))
            self.assertIn("[PASS", r.stdout)
            self.assertNotIn("Figure assets", r.stdout.split("UNVERIFIED")[0]
                             if "UNVERIFIED" in r.stdout else "")

    def test_low_dpi_figures_fail(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "proj"
            (p / "03-paper-drafting").mkdir(parents=True)
            make_png_with_dpi(p / "03-paper-drafting" / "fig1.png", 72)
            r = run_cli(SCRIPTS / "check_compliance.py", "-p", str(p))
            self.assertIn("below 300 DPI", r.stdout)


class TestPriorityIds(unittest.TestCase):
    def test_similar_claims_get_distinct_ids(self):
        mod = load("priority_check")
        a = mod.record_id("C(d,n) = A_leq d(n) for regression")
        b = mod.record_id("C(d,n) = A_leq d(n) for classification")
        self.assertNotEqual(a, b, "prefix collision would silently overwrite a record")
        self.assertEqual(mod.record_id("C(d,n) = A_leq d(n) for regression"), a)


class TestSearchBibtex(unittest.TestCase):
    def test_bibtex_entry_is_balanced(self):
        mod = load("multi_source_search")
        entry = mod.to_bibtex({"title": "A Title", "authors": ["A One", "B Two"],
                               "year": 2025, "venue": "COLT", "doi": "10.1/xyz",
                               "source": "arxiv", "url": "http://x"}, 1)
        self.assertIsNotNone(entry)
        self.assertEqual(entry.count("{"), entry.count("}"))

    def test_incomplete_record_is_refused(self):
        mod = load("multi_source_search")
        self.assertIsNone(mod.to_bibtex({"title": ""}, 1))

    def test_dedupe_removes_duplicates(self):
        mod = load("multi_source_search")
        recs = [{"title": "Same Title"}, {"title": "same title"}, {"title": "Other"}]
        self.assertEqual(len(mod.dedupe(recs)), 2)


class TestNoMockData(unittest.TestCase):
    def test_no_mock_markers_in_shipped_scripts(self):
        import re
        bad = re.compile(r"mock[_\- ]?(results?|data|path|analys)|simulated for now|"
                         r"TODO:\s*Implement", re.I)
        # self_score.py / score_selftest.py HOLD these patterns as data; skip them.
        skip = {"self_score.py", "score_selftest.py"}
        for f in sorted(p for p in SCRIPTS.glob("*.py") if p.name not in skip):
            with self.subTest(f=f.name):
                self.assertIsNone(bad.search(f.read_text(encoding="utf-8")),
                                  f"mock marker found in {f.name}")


class TestProofLedger(unittest.TestCase):
    @staticmethod
    def _add(td, cid, kind, statement, depends="", status="open"):
        args = [str(SCRIPTS / "proof_ledger.py"), "-d", td, "--add", cid,
                "--kind", kind, "--statement", statement, "--status", status]
        if depends:
            args += ["--depends", depends]
        return subprocess.run([PY] + args, capture_output=True, text=True, timeout=60)

    def test_refuses_proven_over_unproven_dependency(self):
        with tempfile.TemporaryDirectory() as td:
            self._add(td, "L1", "lemma", "base step")
            self._add(td, "T1", "theorem", "main", depends="L1")
            r = run_cli(SCRIPTS / "proof_ledger.py", "-d", td, "--set", "T1", "--to", "proven")
            self.assertEqual(r.returncode, 1, "must refuse while L1 is open")
            self.assertIn("refusing", r.stderr)

    def test_allows_proven_when_deps_proven(self):
        with tempfile.TemporaryDirectory() as td:
            self._add(td, "L1", "lemma", "base", status="proven")
            self._add(td, "T1", "theorem", "main", depends="L1")
            r = run_cli(SCRIPTS / "proof_ledger.py", "-d", td, "--set", "T1", "--to", "proven")
            self.assertEqual(r.returncode, 0, r.stderr)

    def test_report_flags_cycle(self):
        with tempfile.TemporaryDirectory() as td:
            self._add(td, "A", "lemma", "a", depends="B")
            self._add(td, "B", "lemma", "b", depends="A")
            run_cli(SCRIPTS / "proof_ledger.py", "-d", td, "--report")
            md = (Path(td) / "proof-ledger.md").read_text(encoding="utf-8")
            self.assertIn("CIRCULAR", md)


class TestPriorityCheck(unittest.TestCase):
    def _seed(self, td):
        (Path(td) / "priority-records.json").write_text(
            json.dumps({"records": {"P1": {"claim": "x", "verdict": "unchecked",
                                           "evidence": None}}}), encoding="utf-8")

    def test_resolve_without_url_is_refused(self):
        with tempfile.TemporaryDirectory() as td:
            self._seed(td)
            r = run_cli(SCRIPTS / "priority_check.py", "-d", td, "--resolve", "P1",
                        "--verdict", "novel")
            self.assertEqual(r.returncode, 2, "a verdict needs a source URL")

    def test_resolve_with_url_succeeds(self):
        with tempfile.TemporaryDirectory() as td:
            self._seed(td)
            r = run_cli(SCRIPTS / "priority_check.py", "-d", td, "--resolve", "P1",
                        "--verdict", "covered", "--evidence", "https://arxiv.org/abs/1")
            self.assertEqual(r.returncode, 0, r.stderr)

    def test_strict_exits_1_while_unchecked(self):
        with tempfile.TemporaryDirectory() as td:
            self._seed(td)
            r = run_cli(SCRIPTS / "priority_check.py", "-d", td, "--strict")
            self.assertEqual(r.returncode, 1)


class TestRationalCertificate(unittest.TestCase):
    def test_demo_is_certified(self):
        r = run_cli(SCRIPTS / "rational_certificate.py", "--demo")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("CERTIFIED", r.stdout)

    def test_float_script_is_flagged(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "floaty.py"
            p.write_text("x = 1.0\nprint('CERTIFIED')\n", encoding="utf-8")
            r = run_cli(SCRIPTS / "rational_certificate.py", "--script", str(p),
                        "--out", td)
            self.assertEqual(r.returncode, 0)
            self.assertIn("float_literal", r.stdout)
            cert = json.loads((Path(td) / "certificate-floaty.json").read_text())
            self.assertIn("float_literal", cert["float_contamination"])


class TestSelfAudit(unittest.TestCase):
    def test_empty_project_is_not_publishable(self):
        with tempfile.TemporaryDirectory() as td:
            r = run_cli(SCRIPTS / "self_audit.py", "-p", td)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertIn("NOT PUBLISHABLE", r.stdout)

    def test_strict_exits_1_with_blockers(self):
        with tempfile.TemporaryDirectory() as td:
            r = run_cli(SCRIPTS / "self_audit.py", "-p", td, "--strict")
            self.assertEqual(r.returncode, 1)


class TestLongHorizonSession(unittest.TestCase):
    def test_failure_without_reason_is_refused(self):
        with tempfile.TemporaryDirectory() as td:
            run_cli(SCRIPTS / "long_horizon_session.py", "--start", "prove X", "-d", td)
            r = run_cli(SCRIPTS / "long_horizon_session.py", "-d", td,
                        "--attempt", "LP duality", "--outcome", "failure")
            self.assertEqual(r.returncode, 2, "dead end must record why")

    def test_resume_prints_dead_ends(self):
        with tempfile.TemporaryDirectory() as td:
            run_cli(SCRIPTS / "long_horizon_session.py", "--start", "prove X", "-d", td)
            run_cli(SCRIPTS / "long_horizon_session.py", "-d", td, "--attempt",
                    "LP duality", "--outcome", "failure", "--why", "unbounded")
            r = run_cli(SCRIPTS / "long_horizon_session.py", "-d", td, "--resume")
            self.assertIn("LP duality", r.stdout)
            self.assertIn("unbounded", r.stdout)


def make_stub_skill(root: Path) -> None:
    """A skill that has the right file names and nothing inside them."""
    (root / "scripts").mkdir(parents=True, exist_ok=True)
    for i in range(3):
        (root / "scripts" / f"mod{i}.py").write_text(
            "import argparse\n\n\ndef main() -> int:\n"
            "    argparse.ArgumentParser(description='stub').parse_args()\n"
            "    return 0\n\n\nif __name__ == '__main__':\n"
            "    raise SystemExit(main())\n", encoding="utf-8")
    (root / "SKILL.md").write_text("# Stub skill\n\nDoes nothing.\n", encoding="utf-8")


class TestSubstanceProbe(unittest.TestCase):
    """A file that merely exists must not earn credit."""

    def setUp(self):
        self.sc = load("self_score")
        self.real_root = self.sc.SKILL_ROOT

    def tearDown(self):
        self.sc.SKILL_ROOT = self.real_root

    def test_stub_skill_has_no_substance(self):
        with tempfile.TemporaryDirectory() as td:
            make_stub_skill(Path(td))
            self.sc.SKILL_ROOT = Path(td)
            score, notes = self.sc.probe_substance()
        self.assertLess(score, 3.0, f"stubs scored {score}: {notes}")

    def test_real_skill_has_substance(self):
        score, notes = self.sc.probe_substance()
        self.assertGreaterEqual(score, 8.0, f"real skill scored {score}: {notes}")

    def test_theory_module_stub_is_not_credited(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            for m in self.sc.THEORY_MODULES:
                (root / "scripts").mkdir(parents=True, exist_ok=True)
                (root / "scripts" / m).write_text("def main() -> int:\n    return 0\n",
                                                  encoding="utf-8")
            (root / "SKILL.md").write_text("# x\n\n--track=theory\n", encoding="utf-8")
            self.sc.SKILL_ROOT = root
            score, notes = self.sc.probe_fitness()
        self.assertLess(score, 5.0, f"stub theory modules scored {score}: {notes}")


class TestTautologyDetection(unittest.TestCase):
    def setUp(self):
        self.sc = load("self_score")

    def test_assert_true_is_detected(self):
        src = ("import unittest\n\n\nclass T(unittest.TestCase):\n"
               "    def test_a(self):\n        assert True\n"
               "    def test_b(self):\n        self.assertEqual(1, 1)\n")
        slots, taut = self.sc._classify_tests(src)
        self.assertEqual(slots, taut, "every slot is tautological")
        self.assertGreater(slots, 0)

    def test_unittest_methods_count_as_assertions(self):
        """Regression: a suite using self.assertX must not read as 'no asserts'."""
        src = ("import unittest\n\n\nclass T(unittest.TestCase):\n"
               "    def test_a(self):\n        self.assertEqual(1, 2)\n")
        slots, taut = self.sc._classify_tests(src)
        self.assertEqual(slots, 1)
        self.assertEqual(taut, 0)

    def test_empty_test_body_is_detected(self):
        src = ("import unittest\n\n\nclass T(unittest.TestCase):\n"
               "    def test_a(self):\n        pass\n")
        slots, taut = self.sc._classify_tests(src)
        self.assertEqual(slots, taut)

    def test_real_suite_is_not_mostly_tautological(self):
        src = (ROOT / "tests" / "test_skill.py").read_text(encoding="utf-8")
        slots, taut = self.sc._classify_tests(src)
        self.assertGreater(slots, 50)
        self.assertEqual(taut, 0, "real suite contains tautological assertions")


class TestMutationInjection(unittest.TestCase):
    def setUp(self):
        self.sc = load("self_score")

    def test_break_module_actually_breaks_a_cli_script(self):
        """Regression: appending the raise at EOF is hidden behind sys.exit()."""
        src = ("import sys\n\n\ndef main() -> int:\n    return 0\n\n\n"
               "if __name__ == '__main__':\n    sys.exit(main())\n")
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "m.py"
            p.write_text(self.sc._break_module(src), encoding="utf-8")
            r = subprocess.run([PY, str(p)], capture_output=True, text=True, timeout=60)
        self.assertNotEqual(r.returncode, 0, "mutation did not take effect")

    def test_break_module_also_breaks_import(self):
        src = "import sys\n\n\ndef main() -> int:\n    return 0\n"
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "m.py"
            p.write_text(self.sc._break_module(src), encoding="utf-8")
            r = subprocess.run([PY, "-c", f"import sys; sys.path.insert(0, {str(td)!r}); import m"],
                               capture_output=True, text=True, timeout=60)
        self.assertNotEqual(r.returncode, 0)


class TestScoreCaps(unittest.TestCase):
    """One collapsed dimension must cap the total, not just lose its weight."""

    def setUp(self):
        self.sc = load("self_score")

    def _res(self, **dims):
        return {"total": 100.0,
                "dimensions": {k: {"score": v} for k, v in dims.items()}}

    def test_broken_suite_caps_total(self):
        out = self.sc.apply_caps(self._res(test_integrity=3.5, substance=10.0,
                                           authenticity=10.0))
        self.assertEqual(out["total"], 60.0)
        self.assertTrue(out["caps"])

    def test_no_substance_caps_total(self):
        out = self.sc.apply_caps(self._res(test_integrity=10.0, substance=1.95,
                                           authenticity=10.0))
        self.assertEqual(out["total"], 50.0)

    def test_healthy_scores_are_not_capped(self):
        out = self.sc.apply_caps(self._res(test_integrity=10.0, substance=10.0,
                                           authenticity=10.0))
        self.assertEqual(out["total"], 100.0)
        self.assertEqual(out["caps"], [])

    def test_unmeasured_dimension_is_not_capped(self):
        """--only runs must not cap on dimensions they never measured."""
        out = self.sc.apply_caps(self._res(test_integrity=10.0))
        self.assertEqual(out["total"], 100.0)
        self.assertEqual(out["caps"], [])


def run_entry(*args, cwd=None):
    """Invoke `python run.py ...` with an explicit cwd."""
    return subprocess.run([PY, str(ROOT / "run.py"), *args], capture_output=True,
                          text=True, timeout=180, cwd=str(cwd or ROOT))


class TestRunPyCwd(unittest.TestCase):
    """Regression: run.py used to pin cwd to the install directory, so every
    command with a relative default output wrote INTO the skill folder."""

    def test_output_lands_in_caller_cwd_not_skill_dir(self):
        leaked = ROOT / "math-notation-check.md"
        self.assertFalse(leaked.exists(), "pre-existing leak in skill dir")
        with tempfile.TemporaryDirectory() as td:
            self.assertEqual(run_entry("template", "-j", "article", "-o", td).returncode, 0)
            self.assertEqual(run_entry("math", "-i", "main.tex", cwd=td).returncode, 0,
                             "math must run against the generated main.tex")
            self.assertTrue((Path(td) / "math-notation-check.md").is_file(),
                            "report must land in the caller's directory")
        self.assertFalse(leaked.exists(), "run.py wrote its output into the skill dir")


class TestTrackAwareCompliance(unittest.TestCase):
    """A theory paper is not graded on experiments it will never run."""

    def _audit(self, track):
        with tempfile.TemporaryDirectory() as td:
            proj = Path(td) / "proj"
            r = run_cli(ROOT / "init_research_project.py", "-d", "x", "-j", "JMLR",
                        "--track", track, "-o", str(proj))
            self.assertEqual(r.returncode, 0)
            out = Path(td) / "c.json"
            run_cli(SCRIPTS / "check_compliance.py", "-p", str(proj), "--json", str(out))
            return json.loads(out.read_text(encoding="utf-8"))

    def test_theory_track_skips_experiment_checks(self):
        checks = self._audit("theory")
        for key in ("baselines", "ablations", "robustness"):
            self.assertEqual(checks[key]["status"], "n/a",
                             f"{key} must be not-applicable for a theory project")
        self.assertIn("theory_artifacts", checks)

    def test_empirical_track_still_runs_experiment_checks(self):
        checks = self._audit("empirical")
        for key in ("baselines", "ablations", "robustness"):
            self.assertEqual(checks[key]["status"], "evaluated",
                             f"{key} must still be graded for an empirical project")
        self.assertEqual(checks["theory_artifacts"]["status"], "n/a")

    def test_experiment_rows_never_count_as_failures_for_theory(self):
        with tempfile.TemporaryDirectory() as td:
            proj = Path(td) / "proj"
            run_cli(ROOT / "init_research_project.py", "-d", "x", "--track", "theory",
                    "-o", str(proj))
            # An empty project is genuinely not ready; what matters is WHICH
            # rows fail. The experiment rows must not be among them.
            r = run_cli(SCRIPTS / "check_compliance.py", "-p", str(proj), "--strict")
            self.assertEqual(r.returncode, 1)
            failed = [l for l in r.stdout.splitlines() if l.strip().startswith("[FAIL")]
            for key in ("Baseline comparison", "Ablation study", "Robustness"):
                self.assertFalse(any(key in l for l in failed),
                                 f"{key} must not fail a theory project: {failed}")
            self.assertTrue(any("N/A" in l and "Baseline" in l for l in r.stdout.splitlines()))


class TestCliAliases(unittest.TestCase):
    """Same concept, same flag. -p for project dir, -o for output."""

    def test_ledger_accepts_p(self):
        with tempfile.TemporaryDirectory() as td:
            self.assertEqual(run_cli(SCRIPTS / "proof_ledger.py", "-p", td,
                                     "--init").returncode, 0)

    def test_ledger_accepts_deps_alias(self):
        with tempfile.TemporaryDirectory() as td:
            run_cli(SCRIPTS / "proof_ledger.py", "-d", td, "--init")
            self.assertEqual(run_cli(SCRIPTS / "proof_ledger.py", "-d", td, "--add", "L1",
                                     "--kind", "lemma", "--statement", "s").returncode, 0)
            self.assertEqual(run_cli(SCRIPTS / "proof_ledger.py", "-d", td, "--add", "T1",
                                     "--kind", "theorem", "--statement", "s",
                                     "--deps", "L1").returncode, 0)

    def test_session_accepts_p(self):
        with tempfile.TemporaryDirectory() as td:
            self.assertEqual(run_cli(SCRIPTS / "long_horizon_session.py", "-p", td,
                                     "--start", "prove X").returncode, 0)

    def test_certify_accepts_o(self):
        with tempfile.TemporaryDirectory() as td:
            self.assertEqual(run_cli(SCRIPTS / "rational_certificate.py", "--demo",
                                     "-o", td).returncode, 0)


class TestDocumentedFlags(unittest.TestCase):
    """Documented invocations must actually be runnable."""

    def setUp(self):
        self.sc = load("self_score")

    def test_short_flag_is_not_matched_inside_a_long_flag(self):
        self.assertTrue(self.sc._flag_in_help("-p", "-p DIR, --dir DIR"))
        self.assertFalse(self.sc._flag_in_help("-p", "--proof PROOF"),
                         "'-p' must not match inside '--proof'")
        self.assertFalse(self.sc._flag_in_help("--out", "--output OUTPUT"))

    def test_backslash_continuations_are_joined(self):
        md = 'python run.py ledger -d ./p \\\n    --statement "s" --kind lemma\n'
        pairs = self.sc._documented_flags(md)
        self.assertIn(("ledger", "--kind"), pairs)
        self.assertIn(("ledger", "-d"), pairs)

    def test_every_documented_flag_exists(self):
        notes: list[str] = []
        ratio = self.sc.probe_documented_flags(notes)
        self.assertEqual(ratio, 1.0, f"docs show flags that do not exist: {notes}")


class TestNoStrayArtifacts(unittest.TestCase):
    def setUp(self):
        self.sc = load("self_score")
        self.real_root = self.sc.SKILL_ROOT

    def tearDown(self):
        self.sc.SKILL_ROOT = self.real_root

    def test_skill_dir_is_clean(self):
        self.assertEqual(self.sc._stray_artifacts(), [])

    def test_leaked_report_is_detected(self):
        with tempfile.TemporaryDirectory() as td:
            (Path(td) / "math-notation-check.md").write_text("x", encoding="utf-8")
            self.sc.SKILL_ROOT = Path(td)
            self.assertEqual(self.sc._stray_artifacts(), ["math-notation-check.md"])

    def test_leak_in_a_subdirectory_is_detected(self):
        """Regression: the guard used to scan only the skill root, so
        `07-audit-trail/certificate-*.json` leaked silently. A leak is a leak
        wherever it lands inside the installation."""
        with tempfile.TemporaryDirectory() as td:
            sub = Path(td) / "07-audit-trail"
            sub.mkdir()
            (sub / "certificate-check_bound.json").write_text("{}", encoding="utf-8")
            self.sc.SKILL_ROOT = Path(td)
            self.assertEqual(self.sc._stray_artifacts(),
                             ["07-audit-trail/certificate-check_bound.json"])

    def test_source_dirs_are_not_flagged(self):
        """scripts/ and tests/ legitimately contain same-prefix names."""
        with tempfile.TemporaryDirectory() as td:
            for d in ("scripts", "tests"):
                (Path(td) / d).mkdir()
                (Path(td) / d / "claims.json").write_text("{}", encoding="utf-8")
                (Path(td) / d / "__pycache__").mkdir()
                (Path(td) / d / "__pycache__" / "x.pyc").write_bytes(b"\0")
            self.sc.SKILL_ROOT = Path(td)
            self.assertEqual(self.sc._stray_artifacts(), [])

    def test_scorer_reports_are_sanctioned(self):
        with tempfile.TemporaryDirectory() as td:
            for n in self.sc.SANCTIONED_IN_ROOT:
                (Path(td) / n).write_text("x", encoding="utf-8")
            self.sc.SKILL_ROOT = Path(td)
            self.assertEqual(self.sc._stray_artifacts(), [])


class TestForgivingFlags(unittest.TestCase):
    """The spelling people actually type must work."""

    def test_baseline_is_an_alias_for_comparison(self):
        with tempfile.TemporaryDirectory() as td:
            r = run_cli(SCRIPTS / "create_experiment_design.py", "--type", "baseline",
                        "--dataset", "spindly", "--baseline", "gd", "-o", td)
            self.assertEqual(r.returncode, 0, r.stderr)
            made = [p.name for p in Path(td).glob("*comparison*")]
            self.assertTrue(made, "a baseline design must still be a comparison config "
                                  "or check_compliance cannot find it")

    def test_singular_dataset_and_ablations(self):
        with tempfile.TemporaryDirectory() as td:
            self.assertEqual(run_cli(SCRIPTS / "create_experiment_design.py", "--type",
                                     "comparison", "--dataset", "a", "--baselines", "x",
                                     "-o", td).returncode, 0)
            self.assertEqual(run_cli(SCRIPTS / "create_experiment_design.py", "--type",
                                     "ablation", "--ablations", "c1,c2",
                                     "-o", td).returncode, 0)

    def test_revision_add_alias(self):
        with tempfile.TemporaryDirectory() as td:
            r = run_cli(SCRIPTS / "revision_tracker.py", "--action", "add", "-r", "1",
                        "-d", td, "-i", "issue one", "-x", "fixed")
            self.assertEqual(r.returncode, 0, r.stderr)
            hist = json.loads((Path(td) / "revision-history.json").read_text(encoding="utf-8"))
            self.assertEqual(len(hist["rounds"]), 1)


class TestPackageReadiness(unittest.TestCase):
    """What a publishing platform will actually validate."""

    def test_frontmatter_is_valid(self):
        src = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(src.startswith("---\n"), "SKILL.md must open with frontmatter")
        fm = src.split("---", 2)[1]
        keys = dict(re.findall(r"^(\w[\w-]*):\s*(.+)$", fm, re.M))
        for required in ("name", "description"):
            self.assertIn(required, keys, f"frontmatter missing {required}")
        self.assertRegex(keys["name"], r"^[a-z0-9]+(-[a-z0-9]+)*$")
        self.assertLessEqual(len(keys["name"]), 64)
        self.assertLessEqual(len(keys["description"]), 1024,
                             "platform description limit is 1024 chars")

    def test_licence_is_declared(self):
        self.assertTrue((ROOT / "LICENSE").is_file(), "a publishable skill needs a licence")
        self.assertIn("MIT", (ROOT / "LICENSE").read_text(encoding="utf-8"))

    def test_package_script_produces_a_valid_zip(self):
        pack = load("package_skill")
        with tempfile.TemporaryDirectory() as td:
            zip_path = Path(td) / "out.zip"
            report = pack.build_zip(Path(zip_path), include_reports=False)
            self.assertTrue(zip_path.is_file(), "package_skill wrote nothing")
            self.assertEqual(report["problems"], [],
                             f"package not clean: {report['problems']}")
            names = report["names"]
            self.assertIn("phd-research-companion/SKILL.md", names)
            self.assertIn("phd-research-companion/run.py", names)
            self.assertIn("phd-research-companion/LICENSE", names)
            self.assertIn("phd-research-companion/MANIFEST.txt", names)
            self.assertFalse([n for n in names if "__pycache__" in n])
            self.assertFalse([n for n in names if n.endswith("_skillhub_meta.json")],
                             "local install state must not be published")
            self.assertFalse([n for n in names if "score-history" in n])
            self.assertEqual(len(names), len(set(names)), "duplicate zip entries")
            with zipfile.ZipFile(zip_path) as z:
                self.assertIsNone(z.testzip(), "corrupt archive")


class TestOptionalCommandsDegradeGracefully(unittest.TestCase):
    """A trimmed build (Coze export) drops score/selftest. run.py must degrade
    them with a clear message and rc=2, not a bare 'missing script' traceback.

    Regression: run.py used to reference those modules unconditionally, so the
    Coze artifact would have failed on the first call. The export validator
    caught it; this test keeps it caught.
    """

    def test_required_table_excludes_optional_scripts(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location("_run_mod", ROOT / "run.py")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        required = {Path(p[0]).name for p in mod.COMMANDS.values()}
        optional = {Path(p[0]).name for p in mod.OPTIONAL_COMMANDS.values()}
        self.assertFalse(required & optional, "a command cannot be both required and optional")
        for name in optional:
            self.assertNotIn(name, required)
        # every optional module is allowed to be absent at runtime
        present, absent = mod._available()
        self.assertEqual(set(present) | set(absent), set(mod.COMMANDS) | set(mod.OPTIONAL_COMMANDS))
        self.assertFalse(set(present) & set(absent))

    def test_help_reports_shipped_and_unshipped(self):
        r = run_entry("help")
        self.assertEqual(r.returncode, 0)
        self.assertIn("self-check:", r.stdout)

    def test_unknown_command_still_rc2(self):
        self.assertEqual(run_entry("definitely-not-a-command").returncode, 2)


class TestCozeExport(unittest.TestCase):
    """The Coze artifact is generated, not hand-copied; these guard the export."""

    EXPORTER = ROOT / "scripts" / "export_coze.py"

    def test_check_only_passes(self):
        r = run_cli(self.EXPORTER, "--check-only")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_store_metadata_respects_coze_limits(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location("_exp", self.EXPORTER)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        self.assertLessEqual(len(mod.COZE_STORE_NAME), 20, "Coze caps the name at 20 chars")
        self.assertLessEqual(len(mod.COZE_STORE_DESC), 200, "Coze caps the description at 200")
        self.assertRegex(mod.COZE_SKILL_ID, r"\A[a-z0-9_]+\Z", "skill_id must be slug-shaped")

    def test_dropped_modules_are_not_required_commands(self):
        for rel in ("scripts/self_score.py", "scripts/score_selftest.py",
                    "scripts/package_skill.py"):
            self.assertIn(rel, _coze_drop(), f"{rel} should be excluded from the Coze build")


def _coze_drop():
    import importlib.util
    spec = importlib.util.spec_from_file_location("_exp2", ROOT / "scripts" / "export_coze.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.COZE_DROP


if __name__ == "__main__":
    unittest.main(verbosity=2)
