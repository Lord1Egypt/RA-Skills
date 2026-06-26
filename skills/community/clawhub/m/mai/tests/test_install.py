import os
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class MaiInstallTest(unittest.TestCase):
    def run_install(self, home, *args):
        env = os.environ.copy()
        env["HOME"] = str(home)
        return subprocess.run(
            ["bash", str(ROOT / "scripts" / "install.sh"), *args],
            cwd=str(ROOT),
            env=env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )

    def test_installs_openclaw_and_hermes_symlinks(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            result = self.run_install(home, "--both")

            self.assertEqual(result.returncode, 0, result.stderr)
            openclaw_skill = home / ".openclaw" / "workspace" / "skills" / "mai"
            hermes_skill = home / ".hermes" / "skills" / "commerce" / "mai"
            self.assertTrue(openclaw_skill.is_symlink())
            self.assertTrue(hermes_skill.is_symlink())
            self.assertEqual(openclaw_skill.resolve(), ROOT.resolve())
            self.assertEqual(hermes_skill.resolve(), ROOT.resolve())
            self.assertIn("OpenClaw skill installed", result.stdout)
            self.assertIn("Hermes skill installed", result.stdout)

    def test_dry_run_does_not_write(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            result = self.run_install(home, "--both", "--dry-run")

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse((home / ".openclaw").exists())
            self.assertFalse((home / ".hermes").exists())
            self.assertIn("Would install OpenClaw", result.stdout)
            self.assertIn("Would install Hermes", result.stdout)

    def test_refuses_to_overwrite_existing_target_without_force(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            target = home / ".openclaw" / "workspace" / "skills" / "mai"
            target.parent.mkdir(parents=True)
            target.mkdir()

            result = self.run_install(home, "--openclaw")

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("already exists", result.stderr)


if __name__ == "__main__":
    unittest.main()
