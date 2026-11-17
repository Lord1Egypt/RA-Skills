from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / "scripts"


class WikiToolingTests(unittest.TestCase):
    def run_tool(self, name: str, *args: object) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPTS / name), *(str(arg) for arg in args)],
            text=True,
            capture_output=True,
            check=False,
        )

    def scaffold(self, root: Path) -> None:
        result = self.run_tool("scaffold_wiki.py", root, "--title", "Test Wiki", "--owner", "test-owner", "--strict", "--json")
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)

    @staticmethod
    def source(root: Path, name: str) -> None:
        path = root / "raw/articles" / f"{name}.md"
        path.write_text(f"# {name}\n\nStable source content.\n", encoding="utf-8")

    @staticmethod
    def page(root: Path, name: str, page_id: str, source: str, link: str, updated: str | None = None) -> None:
        path = root / "wiki/concepts" / f"{name}.md"
        path.write_text(
            "\n".join(
                [
                    "---",
                    f"id: {page_id}",
                    "type: concept",
                    f'title: "{name}"',
                    "status: active",
                    f"updated: {updated or date.today().isoformat()}",
                    "owner: test-owner",
                    "sources:",
                    f"  - ../../raw/articles/{source}.md",
                    "---",
                    "",
                    f"# {name}",
                    "",
                    f"Evidence: [source](../../raw/articles/{source}.md).",
                    f"Related: [page]({link}).",
                    "",
                ]
            ),
            encoding="utf-8",
        )

    def test_every_script_exposes_help(self) -> None:
        for script in sorted(SCRIPTS.glob("*.py")):
            with self.subTest(script=script.name):
                result = self.run_tool(script.name, "--help")
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn("usage:", result.stdout.lower())

    def test_scaffold_dry_run_and_non_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "wiki"
            dry = self.run_tool("scaffold_wiki.py", root, "--title", "Dry Wiki", "--dry-run", "--json", "--strict")
            self.assertEqual(dry.returncode, 0, dry.stderr)
            self.assertFalse(root.exists())

            self.scaffold(root)
            original = (root / "WIKI.md").read_text(encoding="utf-8")
            again = self.run_tool("scaffold_wiki.py", root, "--title", "Changed", "--strict", "--json")
            self.assertNotEqual(again.returncode, 0)
            self.assertEqual((root / "WIKI.md").read_text(encoding="utf-8"), original)
            self.assertIn("strict mode refuses", again.stdout)

    def test_good_wiki_builds_manifest_and_passes_strict_audit(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "wiki"
            self.scaffold(root)
            self.source(root, "source-a")
            self.source(root, "source-b")
            self.page(root, "alpha", "concept-alpha", "source-a", "beta.md")
            self.page(root, "beta", "concept-beta", "source-b", "alpha.md")
            (root / "wiki/index.md").write_text(
                "# Test Wiki\n\n- [Alpha](concepts/alpha.md)\n- [Beta](concepts/beta.md)\n",
                encoding="utf-8",
            )

            manifest = self.run_tool("build_manifest.py", root, "--strict", "--json")
            self.assertEqual(manifest.returncode, 0, manifest.stderr + manifest.stdout)
            report = json.loads(manifest.stdout)
            self.assertEqual(report["page_count"], 2)
            data = json.loads((root / ".wiki/manifest.json").read_text(encoding="utf-8"))
            self.assertEqual({page["id"] for page in data["pages"]}, {"concept-alpha", "concept-beta"})

            audit = self.run_tool("audit_wiki.py", root, "--strict", "--json")
            self.assertEqual(audit.returncode, 0, audit.stderr + audit.stdout)
            audit_report = json.loads(audit.stdout)
            self.assertTrue(audit_report["ok"])
            self.assertEqual(audit_report["errors"], 0)
            self.assertEqual(audit_report["warnings"], 0)

    def test_bad_wiki_reports_stable_codes_and_fails_strict(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "wiki"
            self.scaffold(root)
            self.page(root, "alpha", "duplicate-id", "missing-a", "missing-page.md", "2020-01-01")
            self.page(root, "beta", "duplicate-id", "missing-b", "alpha.md", "2020-01-01")
            (root / "wiki/index.md").write_text(
                "# Test Wiki\n\n- [Alpha](concepts/alpha.md)\n- [Beta](concepts/beta.md)\n",
                encoding="utf-8",
            )

            audit = self.run_tool("audit_wiki.py", root, "--strict", "--json")
            self.assertNotEqual(audit.returncode, 0)
            report = json.loads(audit.stdout)
            codes = {issue["code"] for issue in report["issues"]}
            self.assertTrue({"DUPLICATE_ID", "SOURCE_MISSING", "LINK_BROKEN", "PAGE_STALE"}.issubset(codes))

            manifest = self.run_tool("build_manifest.py", root, "--strict", "--json")
            self.assertNotEqual(manifest.returncode, 0)
            manifest_codes = {issue["code"] for issue in json.loads(manifest.stdout)["issues"]}
            self.assertIn("DUPLICATE_ID", manifest_codes)
            self.assertFalse((root / ".wiki/manifest.json").exists())


if __name__ == "__main__":
    unittest.main()
