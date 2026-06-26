import importlib.util
import pathlib
import subprocess
import sys
import tempfile
import unittest


SCRIPT_PATH = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "manage_github_skill.py"
SPEC = importlib.util.spec_from_file_location("manage_github_skill", SCRIPT_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


def git(args, cwd):
    subprocess.run(
        ["git", *args],
        cwd=cwd,
        check=True,
        text=True,
        capture_output=True,
    )


def git_output(args, cwd):
    return subprocess.run(
        ["git", *args],
        cwd=cwd,
        check=True,
        text=True,
        capture_output=True,
    ).stdout.strip()


class GitHubSkillUpdaterTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.tempdir.name)
        self.remote = self.root / "remote.git"
        self.seed = self.root / "seed"
        self.skill = self.root / "skills" / "demo-skill"
        self.root.joinpath("skills").mkdir()

        git(["init", "--bare", str(self.remote)], cwd=self.root)
        git(["clone", str(self.remote), str(self.seed)], cwd=self.root)
        git(["config", "user.name", "Test User"], cwd=self.seed)
        git(["config", "user.email", "test@example.com"], cwd=self.seed)
        (self.seed / "SKILL.md").write_text("# Demo\n", encoding="utf-8")
        git(["add", "SKILL.md"], cwd=self.seed)
        git(["commit", "-m", "init"], cwd=self.seed)
        git(["push", "-u", "origin", "main"], cwd=self.seed)
        git(["clone", str(self.remote), str(self.skill)], cwd=self.root)

    def tearDown(self):
        self.tempdir.cleanup()

    def make_remote_commit(self, message="update"):
        (self.seed / "SKILL.md").write_text(f"# {message}\n", encoding="utf-8")
        git(["add", "SKILL.md"], cwd=self.seed)
        git(["commit", "-m", message], cwd=self.seed)
        git(["push"], cwd=self.seed)

    def test_check_reports_branch_update_available(self):
        self.make_remote_commit("branch-update")

        report = MODULE.inspect_skill(self.skill)

        self.assertEqual(report.status, "update-available")
        self.assertEqual(report.tracking, "branch")
        self.assertGreater(report.behind_count, 0)

    def test_update_fast_forwards_branch_repo(self):
        self.make_remote_commit("branch-update")
        before = git_output(["rev-parse", "HEAD"], cwd=self.skill)

        result = MODULE.update_skill(self.skill)
        after = git_output(["rev-parse", "HEAD"], cwd=self.skill)

        self.assertEqual(result.status, "updated")
        self.assertNotEqual(before, after)
        self.assertEqual(after, git_output(["rev-parse", "origin/main"], cwd=self.skill))

    def test_update_refuses_dirty_repo(self):
        self.make_remote_commit("dirty-update")
        (self.skill / "local.txt").write_text("dirty\n", encoding="utf-8")

        result = MODULE.update_skill(self.skill)

        self.assertEqual(result.status, "dirty")
        self.assertIn("未提交改动", result.message)

    def test_check_uses_tag_strategy_for_detached_tag(self):
        git(["tag", "v1.0.0"], cwd=self.seed)
        git(["push", "origin", "v1.0.0"], cwd=self.seed)
        self.make_remote_commit("release-update")
        git(["tag", "v1.1.0"], cwd=self.seed)
        git(["push", "origin", "v1.1.0"], cwd=self.seed)
        git(["fetch", "--tags", "origin"], cwd=self.skill)
        git(["checkout", "v1.0.0"], cwd=self.skill)

        report = MODULE.inspect_skill(self.skill)

        self.assertEqual(report.tracking, "tag")
        self.assertEqual(report.current_ref, "v1.0.0")
        self.assertEqual(report.latest_ref, "v1.1.0")
        self.assertEqual(report.status, "update-available")

    def test_update_switches_to_latest_tag(self):
        git(["tag", "v1.0.0"], cwd=self.seed)
        git(["push", "origin", "v1.0.0"], cwd=self.seed)
        self.make_remote_commit("release-update")
        git(["tag", "v1.1.0"], cwd=self.seed)
        git(["push", "origin", "v1.1.0"], cwd=self.seed)
        git(["fetch", "--tags", "origin"], cwd=self.skill)
        git(["checkout", "v1.0.0"], cwd=self.skill)

        result = MODULE.update_skill(self.skill)

        self.assertEqual(result.status, "updated")
        self.assertEqual(git_output(["describe", "--tags", "--exact-match"], cwd=self.skill), "v1.1.0")

    def test_check_without_origin_is_reported_as_unsupported(self):
        git(["remote", "remove", "origin"], cwd=self.skill)

        report = MODULE.inspect_skill(self.skill)

        self.assertEqual(report.status, "unsupported")
        self.assertIn("origin", report.message)


if __name__ == "__main__":
    unittest.main()
