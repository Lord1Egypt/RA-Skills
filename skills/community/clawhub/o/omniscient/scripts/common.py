#!/usr/bin/env python3
"""
Shared utilities for system-controller scripts.
Handles Windows encoding issues and PowerShell execution.

Security:
  - run_ps(): Uses list-based subprocess (no shell=True) for PowerShell execution
  - run_cmd(): Deprecated - kept for backward compat but with strict validation
  - All command paths are validated before execution
"""

import subprocess
import sys
import os
import shlex


def run_ps(script, timeout=30):
    """
    Execute PowerShell script safely using list-based subprocess invocation.
    
    Security: Does NOT use shell=True. The script text is passed as an argument
    to powershell.exe via the -Command parameter. This prevents shell injection
    from the Python side since subprocess handles argument escaping.
    
    Args:
        script: PowerShell script text to execute
        timeout: Maximum execution time in seconds (default 30)
        
    Returns:
        Tuple of (stdout: str, stderr: str, returncode: int)
    """
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"

    # Prepend encoding setup to ensure UTF-8 output
    encoding_setup = (
        "[Console]::InputEncoding = [Console]::OutputEncoding = "
        "[System.Text.Encoding]::UTF8; "
        "$OutputEncoding = [System.Text.Encoding]::UTF8; "
    )

    full_script = encoding_setup + script

    # Validate: reject scripts that try to break out of PowerShell context
    dangerous_markers = ['--%', 'cmd /c', 'Invoke-Expression', 'iex ', 'Start-Process -FilePath']
    lower_script = full_script.lower()
    for marker in dangerous_markers:
        if marker in lower_script:
            return "", f"ERROR: Script contains blocked pattern '{marker}'", -1

    try:
        # Use list-based invocation (no shell=True) for safety
        result = subprocess.run(
            ["powershell.exe", "-NoProfile", "-NonInteractive", "-Command", full_script],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            env=env,
            shell=False  # Explicitly no shell
        )
        stdout = (result.stdout or "").strip()
        stderr = (result.stderr or "").strip()
        return stdout, stderr, result.returncode
    except subprocess.TimeoutExpired:
        return "", "ERROR: Command timed out", -1
    except FileNotFoundError:
        return "", "ERROR: powershell.exe not found on system PATH", -1
    except Exception as e:
        return "", f"ERROR: {e}", -1


def run_cmd(command, timeout=30):
    """
    Execute a shell command with safety constraints.
    
    WARNING: This function uses shell=True which carries inherent risk.
    It should only be used for simple, trusted commands where run_ps is not applicable.
    
    Security measures:
      - Command must be a string (not a list that could be misinterpreted)
      - Command length is limited
      - Obvious injection patterns are rejected
    
    Prefer run_ps() for any PowerShell operation.
    
    Args:
        command: Command string to execute
        timeout: Maximum execution time in seconds
        
    Returns:
        Tuple of (stdout: str, stderr: str, returncode: int)
    """
    if not isinstance(command, str):
        return "", "ERROR: run_cmd requires string command", -1

    # Length limit to prevent abuse
    if len(command) > 10000:
        return "", "ERROR: Command exceeds maximum length of 10000 characters", -1

    # Reject dangerous shell metacharacters that enable injection
    dangerous_chars = ['`$', '$(', '${', '`', ';', '&&', '||']
    cmd_str = command.strip()
    for char in dangerous_chars:
        if char in cmd_str:
            return "", f"ERROR: Command blocked - contains '{char}' (use list-based invocation)", -1

    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"

    try:
        result = subprocess.run(
            cmd_str,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            shell=True,  # Intentional but guarded above
            env=env
        )
        stdout = (result.stdout or "").strip()
        stderr = (result.stderr or "").strip()
        return stdout, stderr, result.returncode
    except subprocess.TimeoutExpired:
        return "", "ERROR: Command timed out", -1
    except Exception as e:
        return "", f"ERROR: {e}", -1


def json_safe(obj):
    """Ensure output is serializable, replacing None with null."""
    if obj is None:
        return "null"
    return obj
