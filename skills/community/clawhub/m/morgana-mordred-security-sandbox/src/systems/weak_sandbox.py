#!/usr/bin/env python3
"""
WEAK SANDBOX — For Morgana Testing
Intentional vulnerability: Arbitrary code execution via eval()
"""

import subprocess
import os

# Sandbox that doesn't actually sandbox anything!
SANDBOXED_USER = "mordred"

def execute_code(code, user="guest"):
    """
    VULNERABILITY: eval() with no restrictions!
    Real sandbox would use docker, namespace, or seccomp
    """
    print(f"[SANDBOX] Executing as {user}...")
    
    # This is FLAWED - should never use eval with user input
    try:
        # 模拟安全执行 (simulating safe execution - but it's NOT safe)
        result = eval(code)
        return {"safe": True, "result": result}
    except Exception as e:
        return {"safe": False, "error": str(e)}

def run_command(cmd, user="guest"):
    """
    VULNERABILITY: shell=True with no filtering!
    Should use subprocess with shell=False and argument lists
    """
    print(f"[SANDBOX] Running command as {user}...")
    
    # Deliberately FLAWED - shell injection possible
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=5)
        return {"safe": True, "output": result.stdout, "error": result.stderr}
    except Exception as e:
        return {"safe": False, "error": str(e)}

def read_file(filepath, user="guest"):
    """
    VULNERABILITY: No path traversal protection!
    Should validate path doesn't escape intended directory
    """
    print(f"[SANDBOX] Reading {filepath} as {user}...")
    
    # FLAWED - path traversal attack possible
    # /../../etc/passwd would escape sandbox
    try:
        with open(filepath, 'r') as f:
            return {"safe": True, "content": f.read()}
    except Exception as e:
        return {"safe": False, "error": str(e)}

def write_file(filepath, content, user="guest"):
    """
    VULNERABILITY: No path validation!
    Could write anywhere on filesystem
    """
    print(f"[SANDBOX] Writing to {filepath} as {user}...")
    
    try:
        with open(filepath, 'w') as f:
            f.write(content)
        return {"safe": True}
    except Exception as e:
        return {"safe": False, "error": str(e)}

if __name__ == "__main__":
    print("=== Weak Sandbox Test ===")
    print(execute_code("2+2"))
    print(run_command("whoami"))
