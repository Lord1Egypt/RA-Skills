# -*- coding: utf-8 -*-
"""Offline unit tests for scripts/yaml-check-frontmatter.py.

The script reads ./SKILL.md from the current directory, so each case runs it in
a temporary cwd. No network and no project state is required.
"""

import importlib.util
import io
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS_DIR = os.path.join(SKILL_DIR, "scripts")


def _load_module():
    spec = importlib.util.spec_from_file_location(
        "yaml_check_frontmatter",
        os.path.join(SCRIPTS_DIR, "yaml-check-frontmatter.py"),
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


yaml_check_frontmatter = _load_module()

VALID = "---\nname: x\ndescription: y\ntags: [a, b]\n---\n\nbody\n"


def _run_main(content):
    """Run main() in a temp cwd. content=None means no SKILL.md present."""
    with tempfile.TemporaryDirectory() as tmp:
        if content is not None:
            Path(tmp, "SKILL.md").write_text(content, encoding="utf-8")
        cwd = os.getcwd()
        os.chdir(tmp)
        try:
            buf = io.StringIO()
            with redirect_stdout(buf):
                rc = yaml_check_frontmatter.main()
        finally:
            os.chdir(cwd)
    return rc, buf.getvalue().strip()


class TestValidFrontmatter(unittest.TestCase):
    def test_valid(self):
        rc, out = _run_main(VALID)
        self.assertEqual(rc, 0)
        self.assertEqual(out, "OK")

    def test_real_skill_frontmatter(self):
        cwd = os.getcwd()
        os.chdir(SKILL_DIR)
        try:
            buf = io.StringIO()
            with redirect_stdout(buf):
                rc = yaml_check_frontmatter.main()
        finally:
            os.chdir(cwd)
        self.assertEqual(rc, 0)
        self.assertIn(buf.getvalue().strip(), ("OK", "NO_PYYAML"))


class TestStructuralErrors(unittest.TestCase):
    def test_must_start_with_dashes(self):
        rc, out = _run_main("# Title\n")
        self.assertEqual(rc, 1)
        self.assertTrue(out.startswith("ERR:"), out)

    def test_closing_dashes_missing(self):
        rc, out = _run_main("---\nname: x\n")
        self.assertEqual(rc, 1)
        self.assertIn("closing", out)

    def test_root_not_a_map(self):
        rc, out = _run_main("---\n- a\n- b\n---\n")
        self.assertEqual(rc, 1)
        self.assertIn("root must be a map", out)

    def test_read_error_when_file_absent(self):
        rc, out = _run_main(None)
        self.assertEqual(rc, 1)
        self.assertIn("ERR:read", out)

    def test_invalid_yaml(self):
        rc, out = _run_main("---\nfoo: [unclosed\n---\n")
        self.assertEqual(rc, 1)
        self.assertTrue(out.startswith("ERR:yaml"), out)


class TestFieldValidation(unittest.TestCase):
    def test_name_empty(self):
        rc, out = _run_main("---\ndescription: y\n---\n")
        self.assertEqual(rc, 1)
        self.assertIn("name empty", out)

    def test_description_empty(self):
        rc, out = _run_main("---\nname: x\n---\n")
        self.assertEqual(rc, 1)
        self.assertIn("description empty", out)

    def test_tags_not_list(self):
        rc, out = _run_main("---\nname: x\ndescription: y\ntags: foo\n---\n")
        self.assertEqual(rc, 1)
        self.assertIn("tags must be a list", out)

    def test_tags_more_than_five(self):
        content = "---\nname: x\ndescription: y\ntags: [a, b, c, d, e, f]\n---\n"
        rc, out = _run_main(content)
        self.assertEqual(rc, 1)
        self.assertIn("tags > 5", out)

    def test_version_field_forbidden(self):
        rc, out = _run_main("---\nname: x\ndescription: y\nversion: 1.0\n---\n")
        self.assertEqual(rc, 1)
        self.assertIn("version field must be absent", out)


class TestPyYamlAbsent(unittest.TestCase):
    def test_no_pyyaml_degrades_cleanly(self):
        with mock.patch.dict(sys.modules, {"yaml": None}):
            rc, out = _run_main(VALID)
        self.assertEqual(rc, 0)
        self.assertEqual(out, "NO_PYYAML")


if __name__ == "__main__":
    unittest.main()