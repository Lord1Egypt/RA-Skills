"""
Unit tests for git-hooks-manager
"""
import os
import sys
import json
import tempfile
import unittest
import subprocess

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from hooks_manager import HookManager, TEMPLATES, HOOK_NAMES


class TestHookManager(unittest.TestCase):
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        # Initialize git repo
        subprocess.run(["git", "init"], cwd=self.temp_dir, capture_output=True)
        self.manager = HookManager(self.temp_dir)
    
    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_find_git_dir(self):
        git_dir = self.manager._find_git_dir()
        self.assertIsNotNone(git_dir)
    
    def test_install_hook(self):
        self.manager.install("pre-commit", template="lint-and-test")
        hooks = self.manager.list_hooks()
        self.assertIn("pre-commit", hooks)
    
    def test_install_all_templates(self):
        for template_name in TEMPLATES.keys():
            hook_name = "pre-commit" if template_name != "branch-guard" else "pre-push"
            self.manager.install(hook_name, template=template_name)
            hooks = self.manager.list_hooks()
            self.assertIn(hook_name, hooks)
    
    def test_uninstall_hook(self):
        self.manager.install("pre-commit", template="lint-and-test")
        result = self.manager.uninstall("pre-commit")
        self.assertTrue(result)
        hooks = self.manager.list_hooks()
        self.assertNotIn("pre-commit", hooks)
    
    def test_uninstall_missing(self):
        result = self.manager.uninstall("nonexistent")
        self.assertFalse(result)
    
    def test_list_hooks_empty(self):
        hooks = self.manager.list_hooks()
        self.assertEqual(hooks, [])
    
    def test_validate_commit_message_valid(self):
        msg = "feat: add new feature"
        errors = self.manager.validate_commit_message(msg)
        self.assertEqual(errors, [])
    
    def test_validate_commit_message_invalid_type(self):
        msg = "bad: add new feature"
        errors = self.manager.validate_commit_message(msg)
        self.assertTrue(any("type(scope): description" in e for e in errors))
    
    def test_validate_commit_message_too_long(self):
        msg = "feat: " + "x" * 100
        errors = self.manager.validate_commit_message(msg)
        self.assertTrue(any("too long" in e for e in errors))
    
    def test_validate_branch_name_valid(self):
        name = "feature/add-login"
        errors = self.manager.validate_branch_name(name)
        self.assertEqual(errors, [])
    
    def test_validate_branch_name_invalid_prefix(self):
        name = "bugfix/add-login"
        errors = self.manager.validate_branch_name(name)
        self.assertTrue(any("type/description" in e for e in errors))
    
    def test_validate_branch_name_too_long(self):
        name = "feature/" + "x" * 100
        errors = self.manager.validate_branch_name(name)
        self.assertTrue(any("too long" in e for e in errors))
    
    def test_export_import(self):
        self.manager.install("pre-commit", template="lint-and-test")
        
        config_path = os.path.join(self.temp_dir, "hooks.json")
        self.manager.export_config(config_path)
        
        self.assertTrue(os.path.exists(config_path))
        with open(config_path) as f:
            config = json.load(f)
        self.assertIn("hooks", config)
        self.assertIn("pre-commit", config["hooks"])
        
        # Re-import after uninstall
        self.manager.uninstall("pre-commit")
        self.manager.import_config(config_path)
        self.assertIn("pre-commit", self.manager.list_hooks())
    
    def test_run_command(self):
        result = self.manager.run_command("git", ["--version"])
        self.assertEqual(result.returncode, 0)
    
    def test_custom_hook_decorator(self):
        @self.manager.hook("pre-commit")
        def custom_check():
            return True
        self.assertIn("pre-commit", self.manager._hooks)


if __name__ == "__main__":
    unittest.main()
