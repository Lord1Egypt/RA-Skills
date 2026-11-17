"""Unit tests for ocas-skilllab scripts (run: python3 -m unittest discover -s tests)."""
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(HERE)
SCRIPTS = os.path.join(SKILL_DIR, "scripts")
sys.path.insert(0, SCRIPTS)

import critique_code_ratio  # noqa: E402
import skilllab  # noqa: E402


class TestSanitizeSkill(unittest.TestCase):
    def test_sanitize_secrets(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = os.path.join(tmpdir, "config.py")
            with open(test_file, "w") as f:
                f.write('OPENAI_KEY = "REDACTED-SECRET"\n')
                f.write('STRIPE_KEY = "sk_live_1234567890abcdef"\n')
                f.write('AWS_KEY = "REDACTED-SECRET"\n')

            summary = skilllab.sanitize_skill("test-skill", tmpdir)
            self.assertIn("config.py", summary)

            with open(test_file) as f:
                content = f.read()
            self.assertIn("${OPENAI_API_KEY}", content)
            self.assertIn("${STRIPE_LIVE_SECRET_KEY}", content)
            self.assertIn("${AWS_ACCESS_KEY_ID}", content)
            self.assertNotIn("sk-1234567890", content)

    def test_sanitize_non_secret_bypass(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = os.path.join(tmpdir, "helper.py")
            normal_code = "def add(a, b):\n    return a + b\n"
            with open(test_file, "w") as f:
                f.write(normal_code)

            summary = skilllab.sanitize_skill("test-skill", tmpdir)
            self.assertEqual(summary, {})

            with open(test_file) as f:
                content = f.read()
            self.assertEqual(content, normal_code)

    def test_sanitize_multi_files_and_empty_dirs(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            # Test empty subfolder does not cause UnboundLocalError
            subdir = os.path.join(tmpdir, "empty_subdir")
            os.makedirs(subdir)

            # Test multiple files: non-last file has secret, last file is clean
            f1 = os.path.join(tmpdir, "a_config.py")
            f2 = os.path.join(tmpdir, "b_normal.py")
            with open(f1, "w") as f:
                f.write('OPENAI_KEY = "REDACTED-SECRET"\n')
            with open(f2, "w") as f:
                f.write('x = 100\n')

            summary = skilllab.sanitize_skill("test-skill", tmpdir)
            self.assertIn("a_config.py", summary)

            with open(f1) as f:
                content = f.read()
            self.assertIn("${OPENAI_API_KEY}", content)

    def test_sanitize_taglines_and_tool_refs(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            readme = os.path.join(tmpdir, "README.md")
            skill_md = os.path.join(tmpdir, "SKILL.md")
            with open(readme, "w") as f:
                f.write("# Skill\nTell it what you need. It does the work.\nPowered by Elephas.")
            with open(skill_md, "w") as f:
                f.write("# Skill MD\nOne clear job, done well.\n")

            summary = skilllab.sanitize_skill("test-skill", tmpdir)
            self.assertIn("README.md", summary)
            self.assertIn("SKILL.md", summary)

            with open(readme) as f:
                readme_content = f.read()
            self.assertNotIn("Tell it what you need.", readme_content)
            self.assertIn("Operational skill for the OCAS family.", readme_content)
            self.assertIn("See references/integration-notes.md", readme_content)

            with open(skill_md) as f:
                skill_content = f.read()
            self.assertNotIn("One clear job, done well.", skill_content)

    def test_sanitize_session_log_quarantine(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            session_file = os.path.join(tmpdir, "session-2026-01-01.md")
            with open(session_file, "w") as f:
                f.write("# Session Log\nDetails here.\n")

            summary = skilllab.sanitize_skill("test-skill", tmpdir)
            self.assertIn("session-2026-01-01.md", summary)
            self.assertFalse(os.path.exists(session_file))
            quarantined = os.path.join(tmpdir, ".archive", "session-logs-export", "session-2026-01-01.md")
            self.assertTrue(os.path.exists(quarantined))


class TestCodeRatio(unittest.TestCase):
    def test_empty_file_passes(self):
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
            f.write("# nothing\n")
            path = f.name
        try:
            r = critique_code_ratio.measure_code_ratio(path)
            self.assertLess(r["ratio"], 20)
        finally:
            os.unlink(path)

    def test_all_code_fails(self):
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
            for _ in range(30):
                f.write("```\nx = 1\n```\n")
            path = f.name
        try:
            r = critique_code_ratio.measure_code_ratio(path)
            self.assertGreaterEqual(r["ratio"], 30)
        finally:
            os.unlink(path)


class TestRunnerHeuristics(unittest.TestCase):
    def test_score_skill_missing_file(self):
        import critique_10khr_runner as runner
        res = runner.score_skill("nope", "/nonexistent/SKILL.md")
        self.assertEqual(res["total"], 0)

    def test_state_roundtrip_no_mutation(self):
        # load_state must not create or write the canonical state file
        import critique_10khr_runner as runner
        if os.path.exists(runner.STATE_FILE):
            before = open(runner.STATE_FILE).read()
            runner.load_state()
            self.assertEqual(open(runner.STATE_FILE).read(), before)


class TestScriptHelp(unittest.TestCase):
    """D9: every bundled script answers --help with exit 0."""

    def test_python_scripts_help(self):
        broken = []
        for name in sorted(os.listdir(SCRIPTS)):
            if not name.endswith(".py"):
                continue
            p = subprocess.run([sys.executable, os.path.join(SCRIPTS, name), "--help"],
                               capture_output=True, timeout=60)
            if p.returncode != 0:
                broken.append(name)
        self.assertEqual(broken, [])

    def test_bash_scripts_help(self):
        broken = []
        for name in sorted(os.listdir(SCRIPTS)):
            if not name.endswith(".sh"):
                continue
            p = subprocess.run(["bash", os.path.join(SCRIPTS, name), "--help"],
                               capture_output=True, timeout=60)
            if p.returncode != 0:
                broken.append(name)
        self.assertEqual(broken, [])


if __name__ == "__main__":
    unittest.main()
