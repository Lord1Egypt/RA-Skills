"""Phase verifier — mechanical verification (never trust self-assessment)."""

from __future__ import annotations
import subprocess
import os
import shlex
import glob
import re
import hashlib
import json
from pathlib import Path
from typing import Tuple


def is_safe_content(content: str) -> Tuple[bool, str]:
    """
    Verify content doesn't contain dangerous operations.

    Returns:
        (is_safe, reason) tuple
    """
    dangerous_patterns = {
        "eval(": "Code evaluation",
        "exec(": "Code execution",
        "__import__": "Dynamic imports",
        "compile(": "Code compilation",
        "rm -rf /": "Destructive file deletion",
        "rm -rf ~": "Home directory deletion",
        "dd if=": "Disk destruction",
        ":(){ :|:& };:": "Fork bomb",
        "chmod 777 /": "Root permission escalation",
        "mkfs.": "Filesystem formatting",
        "/dev/sda": "Direct disk access",
        "> /dev/sda": "Direct disk write",
        "dd if=/dev/zero": "Disk wiping",
        ":(){:|:&};:": "Fork bomb (alternate)",
    }

    for pattern, danger in dangerous_patterns.items():
        if pattern in content:
            return False, f"Dangerous pattern detected: {danger} ({pattern})"

    return True, ""


def verify_content_safety(file_path: Path) -> Tuple[bool, str]:
    """
    Verify a file's content is safe.

    Returns:
        (is_safe, reason) tuple
    """
    try:
        content = file_path.read_text(encoding="utf-8", errors="ignore")
        return is_safe_content(content)
    except Exception as e:
        return False, f"Failed to read file: {e}"


class PhaseVerifier:
    """Mechanical verification after each phase execution."""

    def verify(
        self, worktree_path: str, verification: str, config: dict
    ) -> tuple[bool, str]:
        """Run verification. Returns (passed, message)."""
        if not os.path.exists(worktree_path):
            return False, f"Worktree not found: {worktree_path}"

        method = getattr(self, f"_verify_{verification}", None)
        if method is None:
            return True, f"No verification method for '{verification}' (skipping)"

        try:
            return method(worktree_path, config)
        except Exception as e:
            return False, f"Verification error: {e}"

    def _verify_none(self, worktree: str, config: dict) -> tuple[bool, str]:
        return True, "Read-only phase, no verification needed"

    def _verify_check_files_exist(
        self, worktree: str, config: dict
    ) -> tuple[bool, str]:
        paths = config.get("paths", [])
        if not paths:
            return False, "No paths specified in verification config"

        for path in paths:
            full_path = os.path.join(worktree, path)
            if not os.path.exists(full_path):
                return False, f"File missing: {path}"

            # Enhanced: check minimum size (catches empty files)
            size = os.path.getsize(full_path)
            if size < 1:
                return False, f"File is empty: {path}"

            # Enhanced: check for placeholder content
            try:
                with open(full_path) as f:
                    content = f.read(500)
                if (
                    "TODO" in content
                    and len(content.strip().strip("#").strip("-").strip()) < 50
                ):
                    return False, f"File appears to be placeholder: {path}"
            except UnicodeDecodeError:
                pass  # Binary file, skip content check

            # Enhanced: content safety check (safety check)
            is_safe, reason = verify_content_safety(Path(full_path))
            if not is_safe:
                return False, f"Content safety check failed for {path}: {reason}"

        return (
            True,
            f"All {len(paths)} files exist with meaningful content and are safe",
        )

    def _verify_run_tests(self, worktree: str, config: dict) -> tuple[bool, str]:
        command = config.get("command", "")
        if not command:
            return False, "No test command specified"

        return self._run_command(worktree, command, timeout=120)

    def _verify_run_build(self, worktree: str, config: dict) -> tuple[bool, str]:
        command = config.get("command", "")
        if not command:
            return False, "No build command specified"
        return self._run_command(worktree, command, timeout=180)

    def _verify_lint_check(self, worktree: str, config: dict) -> tuple[bool, str]:
        command = config.get("command")
        if command:
            return self._run_command(worktree, command, timeout=60)

        py_files = [
            path
            for path in glob.glob("**/*.py", root_dir=worktree, recursive=True)
            if not path.startswith((".git/", "node_modules/", ".venv/", "venv/"))
        ]
        if not py_files:
            return True, "No Python files to compile"
        return self._run_args(worktree, ["python3", "-m", "py_compile", *py_files], timeout=60)

    def _verify_check_git_diff(self, worktree: str, config: dict) -> tuple[bool, str]:
        result = subprocess.run(
            ["git", "diff", "--stat", "HEAD"],
            cwd=worktree,
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode != 0:
            return False, "No git changes detected"

        stats = result.stdout.strip()
        if not stats or "insertion" not in stats.lower():
            return False, "Diff shows no meaningful changes"

        # Count insertions
        lines = stats.split("\n")
        for line in lines:
            if "insertion" in line.lower():
                match = re.search(r"(\d+)\s+insertion", line)
                if match and int(match.group(1)) == 0:
                    return False, "Only deletions, no insertions"

        return (
            True,
            f"Meaningful changes detected: {stats.split(chr(10))[-1] if stats else 'unknown'}",
        )

    def _verify_integration_check(
        self, worktree: str, config: dict
    ) -> tuple[bool, str]:
        """Verify functions are CALLED, not just defined (Fischman bug #2)."""
        functions = config.get("functions", [])
        caller_files = config.get("caller_files", [])

        if not functions or not caller_files:
            return True, "No functions/callers specified (skipping integration check)"

        found_calls = 0
        for func in functions:
            for caller_rel in caller_files:
                caller_path = os.path.join(worktree, caller_rel)
                if not os.path.exists(caller_path):
                    continue
                with open(caller_path, errors="replace") as f:
                    content = f.read()
                # Look for func_name( but NOT def func_name(
                pattern = rf"(?<!def )\b{re.escape(func)}\s*\("
                # Then filter out comment lines separately
                matches = []
                for line_no, line in enumerate(content.split('\n'), 1):
                    stripped = line.lstrip()
                    if stripped.startswith('#'):
                        continue
                    if re.search(pattern, line):
                        matches.append((line_no, line.strip()))
                calls = matches
                if calls:
                    found_calls += 1

        if found_calls == 0:
            return (
                False,
                f"None of {len(functions)} functions are called in caller files",
            )
        return True, f"{found_calls} function call(s) found"

    def _verify_smoke_test(self, worktree: str, config: dict) -> tuple[bool, str]:
        command = config.get("command", "")
        if not command:
            return True, "No smoke test command (skipping)"
        return self._run_command(worktree, command, timeout=60)

    def _verify_import_check(self, worktree: str, config: dict) -> tuple[bool, str]:
        module = config.get("module", "")
        if not module:
            return True, "No module specified (skipping)"

        result = subprocess.run(
            [
                "python3",
                "-c",
                f"import sys; sys.path.insert(0, '{worktree}'); import {module}; print('OK')",
            ],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=worktree,
        )
        if result.returncode != 0:
            return False, f"Module {module} import failed: {result.stderr[:200]}"
        return True, f"Module {module} imports successfully"

    def _verify_snapshot_diff(self, worktree: str, config: dict) -> tuple[bool, str]:
        snapshot_path = config.get("snapshot_path", ".night-shift-snapshot.json")
        full_snapshot = os.path.join(worktree, snapshot_path)

        before = {}
        if os.path.exists(full_snapshot):
            try:
                before = json.loads(open(full_snapshot).read())
            except (json.JSONDecodeError, IOError):
                pass

        after = self._create_snapshot(worktree)

        changed = 0
        for path, after_hash in after.items():
            if before.get(path) != after_hash:
                changed += 1

        if changed == 0:
            return False, "No files changed (snapshot comparison)"

        # Save after snapshot for next comparison
        try:
            with open(full_snapshot, "w") as f:
                json.dump(after, f, indent=2)
        except IOError:
            pass

        return True, f"{changed} file(s) changed"

    # --- Helpers ---

    def _run_command(
        self, worktree: str, command: str, timeout: int = 60
    ) -> tuple[bool, str]:
        """Run an allowlisted verification command without invoking a shell."""
        command = command.replace("{worktree}", worktree)
        try:
            args = shlex.split(command)
        except ValueError as exc:
            return False, f"Invalid verification command: {exc}"
        if not args:
            return False, "Empty verification command"

        # Support the common old pattern: cd {worktree} && <command>
        if len(args) >= 4 and args[0] == "cd" and args[2] == "&&":
            args = args[3:]

        return self._run_args(worktree, args, timeout=timeout)

    def _run_args(
        self, worktree: str, args: list[str], timeout: int = 60
    ) -> tuple[bool, str]:
        """Run an allowlisted argv command in the worktree."""
        safe_commands = {
            "python", "python3", "pytest", "ruff", "mypy",
            "npm", "pnpm", "bun", "node", "go", "cargo", "make",
        }
        executable = Path(args[0]).name
        if executable not in safe_commands:
            return (
                False,
                f"Verification command not allowlisted: {executable}. "
                "Use a standard test/lint/build command or review manually.",
            )

        try:
            result = subprocess.run(
                args,
                cwd=worktree,
                capture_output=True,
                text=True,
                timeout=timeout,
            )
            if result.returncode != 0:
                return (
                    False,
                    f"Command failed (exit {result.returncode}): {(result.stderr or result.stdout)[:500]}",
                )
            return True, f"Command succeeded: {result.stdout[:200]}"
        except subprocess.TimeoutExpired:
            return False, f"Command timed out after {timeout}s"
        except Exception as e:
            return False, f"Command error: {e}"

    def _create_snapshot(self, worktree: str) -> dict[str, str]:
        """Create a hash map of all files in worktree."""
        snapshot = {}
        for root, dirs, files in os.walk(worktree):
            # Skip .git and __pycache__
            dirs[:] = [
                d
                for d in dirs
                if d not in (".git", "__pycache__", "node_modules", ".venv")
            ]
            for fname in files:
                fpath = os.path.join(root, fname)
                rel = os.path.relpath(fpath, worktree)
                try:
                    with open(fpath, "rb") as f:
                        snapshot[rel] = hashlib.md5(f.read()).hexdigest()
                except (IOError, OSError):
                    pass
        return snapshot
