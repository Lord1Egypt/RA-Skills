#!/usr/bin/env python3
"""project_inventory 的标准库回归测试。"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.dont_write_bytecode = True
import project_inventory


class ProjectInventoryTests(unittest.TestCase):
    def inventory(self, root: Path) -> dict:
        arguments = argparse.Namespace(
            repo=root,
            max_files=10_000,
            max_depth=20,
            max_items=40,
            format="json",
            strict=False,
        )
        return project_inventory.build_inventory(arguments)

    def write(self, root: Path, relative: str, content: str = "") -> None:
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def test_maven_multimodule_and_delivery_signals(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write(root, "AGENTS.md", "# fixture")
            self.write(
                root,
                "pom.xml",
                """<project xmlns="http://maven.apache.org/POM/4.0.0">
                <modelVersion>4.0.0</modelVersion>
                <modules><module>app</module><module>lib</module></modules>
                </project>""",
            )
            self.write(root, "app/pom.xml", "<project/>")
            self.write(root, "lib/pom.xml", "<project/>")
            self.write(root, "app/src/main/java/App.java", "class App {}")
            self.write(root, "app/src/test/java/AppTest.java", "class AppTest {}")
            self.write(root, ".github/workflows/ci.yml", "name: ci")
            self.write(root, "Dockerfile", "FROM scratch")
            self.write(root, "app/src/main/resources/db/migration/V1__init.sql", "SELECT 1;")

            inventory = self.inventory(root)
            maven = next(item for item in inventory["ecosystems"] if item["name"] == "maven")
            self.assertEqual(["app", "lib"], maven["members"])
            self.assertIn("multi-module", inventory["repository"]["shape"])
            self.assertEqual("Java", inventory["languages"][0]["name"])
            self.assertEqual(1, inventory["signals"]["tests"]["files"])
            self.assertEqual(1, len(inventory["signals"]["ci"]))
            self.assertEqual(1, len(inventory["signals"]["containers"]))
            self.assertEqual(1, len(inventory["signals"]["migrations"]))

    def test_polyglot_workspaces_are_composed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write(root, "package.json", '{"workspaces":["web"]}')
            self.write(root, "web/package.json", "{}")
            self.write(root, "pyproject.toml", '[tool.uv.workspace]\nmembers = ["python-app"]\n')
            self.write(root, "python-app/pyproject.toml", "[project]\nname='sample'\n")
            self.write(root, "go.work", "go 1.22\nuse ./go-app\n")
            self.write(root, "go-app/go.mod", "module invalid.local/sample\n")
            self.write(root, "Cargo.toml", '[workspace]\nmembers = ["rust-app"]\n')
            self.write(root, "rust-app/Cargo.toml", "[package]\nname='sample'\nversion='0.1.0'\n")

            inventory = self.inventory(root)
            names = {item["name"] for item in inventory["ecosystems"]}
            self.assertTrue({"node", "python", "go", "rust"}.issubset(names))
            self.assertIn("polyglot", inventory["repository"]["shape"])
            self.assertIn("monorepo-candidate", inventory["repository"]["shape"])

    def test_manifest_values_and_untracked_paths_do_not_leak(self) -> None:
        sentinel = "DO-NOT-LEAK-UNIQUE-SENTINEL"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write(root, "package.json", json.dumps({"scripts": {"leak": sentinel}}))
            self.write(root, ".env", f"TOKEN={sentinel}\n")
            self.run_git(root, "init")
            self.run_git(root, "config", "user.email", "fixture@example.invalid")
            self.run_git(root, "config", "user.name", "Fixture")
            self.run_git(root, "add", "package.json", ".env")
            self.run_git(root, "commit", "-m", "fixture")
            self.write(root, "secret-token.txt", sentinel)

            inventory = self.inventory(root)
            serialized = json.dumps(inventory, ensure_ascii=False)
            self.assertNotIn(sentinel, serialized)
            self.assertNotIn("secret-token.txt", serialized)
            self.assertNotIn(".env", serialized)
            self.assertEqual(1, inventory["trackedSensitiveLookingNames"]["total"])
            self.assertEqual(1, inventory["repository"]["git"]["changes"]["untracked"])

    def test_invalid_and_unsafe_manifests_warn_without_echoing_content(self) -> None:
        sentinel = "PRIVATE-XML-SENTINEL"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write(root, "package.json", "{invalid-json")
            self.write(root, "pom.xml", f'<!DOCTYPE project [<!ENTITY x "{sentinel}">]><project/>')

            inventory = self.inventory(root)
            codes = {warning["code"] for warning in inventory["warnings"]}
            self.assertIn("manifest-parse-failed", codes)
            self.assertIn("unsafe-xml", codes)
            self.assertNotIn(sentinel, json.dumps(inventory, ensure_ascii=False))

    def run_git(self, root: Path, *arguments: str) -> None:
        completed = subprocess.run(
            ["git", "-C", str(root), *arguments],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if completed.returncode != 0:
            self.fail(completed.stderr.decode("utf-8", errors="replace"))


if __name__ == "__main__":
    unittest.main()
