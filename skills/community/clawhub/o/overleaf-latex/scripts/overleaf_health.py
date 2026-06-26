#!/usr/bin/env python3
"""Overleaf health check script.

Verifies:
1. Overleaf credentials are stored
2. Git can reach overleaf.com
3. pdflatex is available
4. A test LaTeX compile succeeds
"""

import os
import shutil
import subprocess
import sys
import tempfile

CREDENTIALS_PATH = os.path.expanduser("~/.openclaw/.overleaf_credentials")


def check_credentials():
    """Check that Overleaf credentials file exists and is readable."""
    print("1. Checking Overleaf credentials...")
    if not os.path.exists(CREDENTIALS_PATH):
        print(f"   FAIL: {CREDENTIALS_PATH} not found")
        print("   Run: echo 'OVERLEAF_EMAIL=your@email.com' > ~/.openclaw/.overleaf_credentials")
        return False
    
    perms = oct(os.stat(CREDENTIALS_PATH).st_mode)[-3:]
    if perms != "600":
        print(f"   WARN: {CREDENTIALS_PATH} has permissions {perms}, expected 600")
        print(f"   Run: chmod 600 {CREDENTIALS_PATH}")
    
    with open(CREDENTIALS_PATH) as f:
        lines = f.read().strip().splitlines()
    
    has_email = any(l.startswith("OVERLEAF_EMAIL=") for l in lines)
    has_auth = any(l.startswith("OVERLEAF_PASSWORD=") for l in lines) or \
               any(l.startswith("OVERLEAF_TOKEN=") for l in lines)
    
    if not has_email or not has_auth:
        print("   FAIL: Missing OVERLEAF_EMAIL or OVERLEAF_PASSWORD/OVERLEAF_TOKEN")
        return False
    
    print("   OK: Credentials found")
    return True


def check_git_overleaf():
    """Check that git can reach overleaf.com."""
    print("2. Checking git.overleaf.com connectivity...")
    result = subprocess.run(
        ["git", "ls-remote", "https://git.overleaf.com/", "HEAD"],
        capture_output=True, text=True, timeout=10
    )
    if result.returncode == 0 or "Authentication" in result.stderr:
        # Authentication error means connectivity works, just no creds in URL
        print("   OK: Can reach git.overleaf.com")
        return True
    else:
        print(f"   FAIL: Cannot reach git.overleaf.com: {result.stderr[:200]}")
        return False


def check_pdflatex():
    """Check that pdflatex is installed and available."""
    print("3. Checking pdflatex...")
    pdflatex_path = shutil.which("pdflatex")
    if pdflatex_path:
        result = subprocess.run(["pdflatex", "--version"], capture_output=True, text=True)
        version_line = result.stdout.splitlines()[0] if result.stdout else "unknown"
        print(f"   OK: {version_line}")
        return True
    else:
        print("   FAIL: pdflatex not found in PATH")
        print("   Install: sudo apt-get install -y texlive-latex-base texlive-latex-extra texlive-fonts-recommended")
        return False


def check_test_compile():
    """Check that a minimal LaTeX document compiles."""
    print("4. Checking test LaTeX compilation...")
    latex_content = r"""\documentclass{article}
\begin{document}
Hello, Overleaf!
\end{document}
"""
    with tempfile.TemporaryDirectory() as tmpdir:
        tex_path = os.path.join(tmpdir, "test.tex")
        with open(tex_path, "w") as f:
            f.write(latex_content)
        
        result = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "-output-directory", tmpdir, tex_path],
            capture_output=True, text=True, timeout=30
        )
        
        pdf_path = os.path.join(tmpdir, "test.pdf")
        if os.path.exists(pdf_path):
            print("   OK: Test compilation succeeded")
            return True
        else:
            print(f"   FAIL: Test compilation failed")
            print(f"   stdout: {result.stdout[:200]}")
            print(f"   stderr: {result.stderr[:200]}")
            return False


def main():
    print("=== Overleaf Health Check ===\n")
    
    results = []
    results.append(("Credentials", check_credentials()))
    results.append(("Git Connectivity", check_git_overleaf()))
    results.append(("pdflatex", check_pdflatex()))
    results.append(("Test Compile", check_test_compile()))
    
    print("\n=== Summary ===")
    all_pass = True
    for name, passed in results:
        status = "PASS" if passed else "FAIL"
        print(f"  {name}: {status}")
        if not passed:
            all_pass = False
    
    if all_pass:
        print("\nAll checks passed. Overleaf integration is ready.")
        return 0
    else:
        print("\nSome checks failed. Fix the issues above before using Overleaf integration.")
        return 1


if __name__ == "__main__":
    sys.exit(main())