#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comprehensive Test Suite for ms-todo-oauth.py
Tests all commands and features to ensure they work properly
"""

import subprocess
import time
import json
import sys
import os
import argparse
import importlib.util
from datetime import datetime, timedelta
from pathlib import Path

# ANSI colors for better output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"

TEST_CLIENT_ID = "00000000-0000-0000-0000-000000000001"
TEST_ENV_CLIENT_ID = "00000000-0000-0000-0000-000000000002"
TEST_CLIENT_SECRET = "test-secret"

class TestRunner:
    def __init__(self, script_path=None):
        self.script_path = str(Path(script_path) if script_path else Path(__file__).with_name("ms-todo-oauth.py"))
        self.test_list_name = f"🧪 Test List {datetime.now().strftime('%H:%M:%S')}"
        self.passed = 0
        self.failed = 0
        self.test_results = []
        self._cli_module = None

    def load_cli_module(self):
        """Load the CLI module without requiring a package import name."""
        if self._cli_module is None:
            spec = importlib.util.spec_from_file_location("ms_todo_oauth_cli", self.script_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            self._cli_module = module
        return self._cli_module
        
    def run_command(self, *args, env=None):
        """Run a ms-todo-oauth.py command and return output"""
        cmd = [sys.executable, self.script_path] + list(args)
        command_env = os.environ.copy()
        if env:
            command_env.update(env)
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                encoding='utf-8',
                env=command_env
            )
            return result.returncode, result.stdout, result.stderr
        except Exception as e:
            return -1, "", str(e)
    
    def test(self, name, *args, expect_success=True, check_output=None, env=None):
        """Run a test case"""
        print(f"\n{BLUE}Testing:{RESET} {name}")
        print(f"  Command: ms-todo-oauth.py {' '.join(args)}")
        
        returncode, stdout, stderr = self.run_command(*args, env=env)
        
        # Check return code
        success = (returncode == 0) if expect_success else (returncode != 0)
        
        # Check output if specified
        if success and check_output:
            if isinstance(check_output, str):
                success = check_output in stdout
            elif callable(check_output):
                success = check_output(stdout)
        
        # Record result
        if success:
            print(f"  {GREEN}✓ PASSED{RESET}")
            self.passed += 1
            self.test_results.append(("PASS", name))
        else:
            print(f"  {RED}✗ FAILED{RESET}")
            print(f"  Return code: {returncode}")
            if stdout:
                print(f"  Output: {stdout[:200]}")
            if stderr:
                print(f"  Error: {stderr[:200]}")
            self.failed += 1
            self.test_results.append(("FAIL", name))
        
        time.sleep(0.5)  # Small delay between tests
        return success

    def record_result(self, name, success, details=None):
        """Record a test result for checks that do not run subprocess commands."""
        print(f"\n{BLUE}Testing:{RESET} {name}")
        if success:
            print(f"  {GREEN}✓ PASSED{RESET}")
            self.passed += 1
            self.test_results.append(("PASS", name))
        else:
            print(f"  {RED}✗ FAILED{RESET}")
            if details:
                print(f"  Error: {details}")
            self.failed += 1
            self.test_results.append(("FAIL", name))
        time.sleep(0.5)
        return success

    def test_client_credential_resolution(self):
        """Verify credential fallback and explicit constructor overrides."""
        try:
            module = self.load_cli_module()
            default_client = module.MicrosoftTodoClient()
            explicit_client = module.MicrosoftTodoClient(
                client_id=TEST_CLIENT_ID,
                client_secret=TEST_CLIENT_SECRET,
                tenant_id="organizations",
            )
            explicit_args = module.create_parser().parse_args([
                "--client-id", TEST_CLIENT_ID,
                "--client-secret", TEST_CLIENT_SECRET,
                "--tenant-id", "organizations",
                "lists",
            ])
            success = (
                default_client.client_id == module.MicrosoftTodoClient.DEFAULT_CLIENT_ID
                and default_client.client_secret == module.MicrosoftTodoClient.DEFAULT_CLIENT_SECRET
                and explicit_client.client_id == TEST_CLIENT_ID
                and explicit_client.client_secret == TEST_CLIENT_SECRET
                and explicit_client.tenant_id == "organizations"
                and explicit_args.client_id == TEST_CLIENT_ID
                and explicit_args.client_secret == TEST_CLIENT_SECRET
                and explicit_args.tenant_id == "organizations"
            )
            return self.record_result("Credential fallback and explicit override resolution", success)
        except Exception as e:
            return self.record_result("Credential fallback and explicit override resolution", False, str(e))

    def test_environment_credential_resolution(self):
        """Verify environment variable credential overrides without network calls."""
        saved = {
            "MS_TODO_CLIENT_ID": os.environ.get("MS_TODO_CLIENT_ID"),
            "MS_TODO_CLIENT_SECRET": os.environ.get("MS_TODO_CLIENT_SECRET"),
            "MS_TODO_TENANT_ID": os.environ.get("MS_TODO_TENANT_ID"),
        }
        try:
            os.environ["MS_TODO_CLIENT_ID"] = TEST_ENV_CLIENT_ID
            os.environ["MS_TODO_CLIENT_SECRET"] = TEST_CLIENT_SECRET
            os.environ["MS_TODO_TENANT_ID"] = "organizations"

            module = self.load_cli_module()
            client = module.MicrosoftTodoClient(
                tenant_id=os.getenv("MS_TODO_TENANT_ID", "consumers")
            )
            env_args = module.create_parser().parse_args(["lists"])
            success = (
                client.client_id == TEST_ENV_CLIENT_ID
                and client.client_secret == TEST_CLIENT_SECRET
                and client.tenant_id == "organizations"
                and env_args.tenant_id == "organizations"
            )
            return self.record_result("Environment credential override resolution", success)
        except Exception as e:
            return self.record_result("Environment credential override resolution", False, str(e))
        finally:
            for key, value in saved.items():
                if value is None:
                    os.environ.pop(key, None)
                else:
                    os.environ[key] = value

    def test_authorization_code_normalization(self):
        """Verify copied callback values are normalized before token exchange."""
        try:
            module = self.load_cli_module()
            encoded_code = "M.C526_BL2.example%24"
            callback_url = f"http://localhost:8000/callback?code={encoded_code}&state=abc"
            success = (
                module._normalize_authorization_code(encoded_code) == "M.C526_BL2.example$"
                and module._normalize_authorization_code(callback_url) == "M.C526_BL2.example$"
                and module._normalize_authorization_code(f'"{encoded_code}"') == "M.C526_BL2.example$"
            )
            return self.record_result("Authorization code URL decoding and callback extraction", success)
        except Exception as e:
            return self.record_result("Authorization code URL decoding and callback extraction", False, str(e))

    def run_preflight_tests(self):
        """Run non-destructive CLI and credential configuration tests."""
        print("\n" + "="*70)
        print(f"{YELLOW}ms-todo-oauth preflight tests{RESET}")
        print("="*70)

        self.test(
            "Help includes credential override options",
            "--help",
            check_output=lambda x: "--client-id" in x and "--client-secret" in x and "--tenant-id" in x
        )

        self.test_client_credential_resolution()
        self.test_environment_credential_resolution()
        self.test_authorization_code_normalization()
    
    def run_all_tests(self):
        """Run comprehensive test suite"""
        print("\n" + "="*70)
        print(f"{YELLOW}ms-todo-oauth comprehensive test suite{RESET}")
        print("="*70)
        
        # Test 1: List all task lists
        self.test(
            "List all task lists",
            "lists",
            check_output=lambda x: "Task Lists" in x or "No task lists" in x
        )
        
        # Test 2: Create a test list
        self.test(
            "Create a new task list",
            "create-list",
            self.test_list_name,
            check_output=f"✓ List created: {self.test_list_name}"
        )
        
        # Test 3: Add simple task
        self.test(
            "Add simple task",
            "add",
            "-l", self.test_list_name,
            "Simple test task",
            check_output="✓ Task added"
        )
        
        # Test 4: Add task with high priority
        self.test(
            "Add high priority task",
            "add",
            "-l", self.test_list_name,
            "High priority task",
            "-p", "high",
            check_output="✓ Task added"
        )
        
        # Test 5: Add task with due date (tomorrow)
        self.test(
            "Add task with due date (1 day)",
            "add",
            "-l", self.test_list_name,
            "Task due tomorrow",
            "-d", "1",
            check_output="✓ Task added"
        )
        
        # Test 6: Add task with specific date
        future_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
        self.test(
            "Add task with specific due date",
            "add",
            "-l", self.test_list_name,
            "Task due next week",
            "-d", future_date,
            check_output="✓ Task added"
        )
        
        # Test 7: Add task with reminder (3 hours)
        self.test(
            "Add task with reminder",
            "add",
            "-l", self.test_list_name,
            "Task with reminder",
            "-r", "3h",
            check_output="✓ Task added"
        )
        
        # Test 8: Add task with description
        self.test(
            "Add task with description",
            "add",
            "-l", self.test_list_name,
            "Task with notes",
            "-D", "This is a detailed description of the task",
            check_output="✓ Task added"
        )
        
        # Test 9: Add task with tags/categories
        self.test(
            "Add task with tags",
            "add",
            "-l", self.test_list_name,
            "Task with tags",
            "-t", "work,important,urgent",
            check_output="✓ Task added"
        )
        
        # Test 10: Add daily recurring task
        self.test(
            "Add daily recurring task",
            "add",
            "-l", self.test_list_name,
            "Daily recurring task",
            "-R", "daily",
            check_output="✓ Task added"
        )
        
        # Test 11: Add weekly recurring task
        self.test(
            "Add weekly recurring task",
            "add",
            "-l", self.test_list_name,
            "Weekly recurring task",
            "-R", "weekly",
            check_output="✓ Task added"
        )
        
        # Test 12: Add weekdays recurring task
        self.test(
            "Add weekdays recurring task",
            "add",
            "-l", self.test_list_name,
            "Weekday recurring task",
            "-R", "weekdays",
            check_output="✓ Task added"
        )
        
        # Test 13: Add task with all options combined
        self.test(
            "Add task with all options",
            "add",
            "-l", self.test_list_name,
            "Complete featured task",
            "-p", "high",
            "-d", "3",
            "-D", "Task with all features enabled",
            "-t", "test,comprehensive",
            check_output="✓ Task added"
        )
        
        # Test 14: List tasks in the test list
        self.test(
            "List tasks in test list",
            "tasks",
            self.test_list_name,
            check_output=lambda x: "Tasks in list" in x and self.test_list_name in x
        )
        
        # Test 15: List tasks including completed
        self.test(
            "List all tasks including completed",
            "tasks",
            self.test_list_name,
            "-a",
            check_output="Tasks in list"
        )
        
        # Test 16: View task details
        self.test(
            "View task details",
            "detail",
            "-l", self.test_list_name,
            "Simple test task",
            check_output="Task Details"
        )
        
        # Test 17: Search for tasks
        self.test(
            "Search for tasks",
            "search",
            "test task",
            check_output=lambda x: "Search results" in x or "Tasks found" in x or "Simple test task" in x
        )
        
        # Test 18: Complete a task
        self.test(
            "Complete a task",
            "complete",
            "-l", self.test_list_name,
            "Simple test task",
            check_output="✓ Task completed"
        )
        
        # Test 19: View statistics
        self.test(
            "View statistics",
            "stats",
            check_output="Task Statistics"
        )
        
        # Test 20: View pending tasks
        self.test(
            "View pending tasks",
            "pending",
            check_output=lambda x: "incomplete task" in x.lower() or "pending" in x.lower()
        )
        
        # Test 21: View pending tasks grouped
        self.test(
            "View pending tasks grouped by list",
            "pending",
            "-g",
            check_output=self.test_list_name
        )
        
        # Test 22: View today's tasks
        self.test(
            "View today's tasks",
            "today",
            check_output=lambda x: "due today" in x.lower() or "no tasks" in x.lower()
        )
        
        # Test 23: View overdue tasks
        self.test(
            "View overdue tasks",
            "overdue",
            check_output=lambda x: "overdue" in x.lower() or "no overdue" in x.lower()
        )
        
        # Test 24: Export tasks to JSON
        export_file = f"test_export_{int(time.time())}.json"
        if self.test(
            "Export tasks to JSON",
            "export",
            "-o", export_file,
            check_output=f"✓ Tasks exported to: {export_file}"
        ):
            # Verify the export file exists and is valid JSON
            try:
                import os
                if os.path.exists(export_file):
                    with open(export_file, 'r', encoding='utf-8') as f:
                        json.load(f)
                    print(f"  {GREEN}✓ Export file is valid JSON{RESET}")
                    os.remove(export_file)  # Clean up
            except Exception as e:
                print(f"  {RED}✗ Export file validation failed: {e}{RESET}")
        
        # Test 25: Delete a task
        self.test(
            "Delete a task",
            "delete",
            "-l", self.test_list_name,
            "Task with tags",
            "-y",  # Skip confirmation
            check_output="✓ Task deleted"
        )
        
        # Test 26: Try to delete non-existent task
        self.test(
            "Attempt to delete non-existent task",
            "delete",
            "-l", self.test_list_name,
            "This task does not exist",
            "-y",
            expect_success=False,
            check_output="Task not found"
        )
        
        # Test 27: Delete the test list
        self.test(
            "Delete test list",
            "delete-list",
            self.test_list_name,
            "-y",  # Skip confirmation
            check_output="✓ List deleted"
        )
        
        # Test 28: Verify list was deleted
        returncode, stdout, stderr = self.run_command("lists")
        if self.test_list_name not in stdout:
            print(f"\n{BLUE}Testing:{RESET} Verify list deletion")
            print(f"  {GREEN}✓ PASSED{RESET} - Test list no longer exists")
            self.passed += 1
            self.test_results.append(("PASS", "Verify list deletion"))
        else:
            print(f"\n{BLUE}Testing:{RESET} Verify list deletion")
            print(f"  {RED}✗ FAILED{RESET} - Test list still exists")
            self.failed += 1
            self.test_results.append(("FAIL", "Verify list deletion"))
        
        # Test 29: Verbose mode
        self.test(
            "Verbose mode with lists",
            "-v",
            "lists",
            check_output="ID:"
        )
        
        # Print summary
        self.print_summary()
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "="*70)
        print(f"{YELLOW}TEST SUMMARY{RESET}")
        print("="*70)
        
        total = self.passed + self.failed
        pass_rate = (self.passed / total * 100) if total > 0 else 0
        
        print(f"\nTotal tests: {total}")
        print(f"{GREEN}Passed: {self.passed}{RESET}")
        print(f"{RED}Failed: {self.failed}{RESET}")
        print(f"Pass rate: {pass_rate:.1f}%")
        
        if self.failed > 0:
            print(f"\n{RED}Failed tests:{RESET}")
            for status, name in self.test_results:
                if status == "FAIL":
                    print(f"  ✗ {name}")
        
        print("\n" + "="*70)
        
        if self.failed == 0:
            print(f"{GREEN}🎉 ALL TESTS PASSED! 🎉{RESET}")
        else:
            print(f"{YELLOW}⚠️  Some tests failed. Please review the output above.{RESET}")
        
        print("="*70 + "\n")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Run ms-todo-oauth tests")
    parser.add_argument(
        "--preflight-only",
        action="store_true",
        help="Run only non-destructive CLI/configuration tests and skip live Microsoft Graph tests",
    )
    args = parser.parse_args()

    print(f"\n{BLUE}Starting comprehensive test suite...{RESET}\n")
    
    runner = TestRunner()
    runner.run_preflight_tests()

    if args.preflight_only:
        runner.print_summary()
        sys.exit(0 if runner.failed == 0 else 1)

    if runner.failed > 0:
        runner.print_summary()
        sys.exit(1)

    # Check if authenticated before running live Microsoft Graph tests.
    returncode, stdout, stderr = runner.run_command("lists")
    
    if returncode != 0:
        output = stdout + stderr
        if "Not logged in" in output:
            print(f"{RED}ERROR: Not authenticated!{RESET}")
            print("\nPlease authenticate first:")
            print("  1. python scripts/ms-todo-oauth.py login get")
            print('  2. python scripts/ms-todo-oauth.py login verify "<code-or-callback-url>"')
        else:
            print(f"{RED}ERROR: CLI preflight failed!{RESET}")
            if stdout:
                print(stdout)
            if stderr:
                print(stderr)
        runner.print_summary()
        sys.exit(1)
    
    # Run all tests
    runner.run_all_tests()
    
    sys.exit(0 if runner.failed == 0 else 1)

if __name__ == "__main__":
    main()
