#!/usr/bin/env python3
"""
Mermaid-CLI Installation Checker

Checks if mermaid-cli and required dependencies are installed.
Provides helpful guidance for installation and troubleshooting.
"""

import sys
import os
import subprocess
import argparse
from pathlib import Path

def run_command(cmd):
    """Run a command and return (success, output)."""
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=10
        )
        return result.returncode == 0, result.stdout.strip()
    except Exception as e:
        return False, str(e)

def check_nodejs():
    """Check if Node.js is installed and get version."""
    success, output = run_command("node --version")
    if success:
        return True, f"✅ Node.js {output}"
    else:
        return False, "❌ Node.js not installed"

def check_npm():
    """Check if npm is installed and get version."""
    success, output = run_command("npm --version")
    if success:
        return True, f"✅ npm {output}"
    else:
        return False, "❌ npm not installed"

def check_mermaid_cli():
    """Check if mermaid-cli is installed."""
    # Try mmdc command (global installation)
    success, _ = run_command("mmdc --version 2>/dev/null")
    if success:
        return True, "✅ mermaid-cli (global)"
    
    # Try npx mmdc (local or npx)
    success, _ = run_command("npx mmdc --version 2>/dev/null")
    if success:
        return True, "✅ mermaid-cli (via npx)"
    
    # Check package.json for local installation
    if Path("package.json").exists():
        success, output = run_command("grep mermaid-cli package.json")
        if success:
            return True, "✅ mermaid-cli (local package.json)"
    
    return False, "❌ mermaid-cli not found"

def check_chrome():
    """Check if Chrome/Chromium is available."""
    # Try common Chrome/Chromium executables
    chrome_paths = [
        "/usr/bin/google-chrome",
        "/usr/bin/chromium",
        "/usr/bin/chromium-browser",
        "/usr/local/bin/chrome",
        "google-chrome-stable",
    ]
    
    for chrome in chrome_paths:
        success, _ = run_command(f"which {chrome} 2>/dev/null")
        if success:
            return True, f"✅ Chrome/Chromium found"
    
    return False, "⚠️  Chrome/Chromium not found (Puppeteer may fail)"

def print_status():
    """Print installation status."""
    print("Mermaid-CLI Installation Status")
    print("=" * 50)
    
    checks = [
        ("Node.js", check_nodejs()),
        ("npm", check_npm()),
        ("mermaid-cli", check_mermaid_cli()),
        ("Chrome/Chromium", check_chrome()),
    ]
    
    all_ok = True
    for name, (success, message) in checks:
        print(f"{name:20} {message}")
        if not success and name != "Chrome/Chromium":
            all_ok = False
    
    print("\n" + "=" * 50)
    
    if all_ok:
        print("✅ All dependencies are installed and ready!")
        return 0
    else:
        print("❌ Some dependencies are missing")
        return 1

def print_installation_guide():
    """Print installation instructions."""
    print("\nInstallation Guide")
    print("=" * 50)
    
    print("""
1. Install Node.js (if not installed):
   - macOS: brew install node
   - Ubuntu/Debian: apt install nodejs npm
   - Windows: Download from nodejs.org
   - Verify: node --version (should be >= 14)

2. Install mermaid-cli:
   # Global installation (recommended)
   npm install -g @mermaid-js/mermaid-cli
   
   # Local installation (for specific project)
   npm install @mermaid-js/mermaid-cli
   
   # Verify: mmdc --version

3. Ensure Chrome/Chromium is installed:
   - mermaid-cli uses Puppeteer which requires Chrome/Chromium
   - Install via package manager or download from google.com/chrome

4. Test installation:
   mmdc -i test.mmd -o test.png
   
   With a simple test.mmd:
     graph TD
        A[Start] --> B[End]
""")

def install_mermaid_cli():
    """Interactive installation of mermaid-cli."""
    print("Installing mermaid-cli...")
    print("-" * 40)
    
    # Check Node.js first
    node_ok, node_msg = check_nodejs()
    if not node_ok:
        print("Node.js is required but not installed.")
        print("Please install Node.js first (see installation guide).")
        return False
    
    # Ask for installation type
    print("Installation options:")
    print("1. Global installation (recommended)")
    print("2. Local installation (current directory)")
    print("3. Cancel")
    
    try:
        choice = input("\nSelect option [1]: ").strip() or "1"
        
        if choice == "1":
            print("\nInstalling globally...")
            success, output = run_command("npm install -g @mermaid-js/mermaid-cli")
            if success:
                print("✅ mermaid-cli installed globally")
                print("You can now use: mmdc -i input.mmd -o output.png")
                return True
            else:
                print(f"❌ Installation failed: {output}")
                return False
                
        elif choice == "2":
            print("\nInstalling locally...")
            success, output = run_command("npm install @mermaid-js/mermaid-cli")
            if success:
                print("✅ mermaid-cli installed locally")
                print("Use with: npx mmdc -i input.mmd -o output.png")
                return True
            else:
                print(f"❌ Installation failed: {output}")
                return False
                
        else:
            print("Installation cancelled.")
            return False
            
    except KeyboardInterrupt:
        print("\nInstallation cancelled.")
        return False

def main():
    parser = argparse.ArgumentParser(
        description="Check and install mermaid-cli dependencies"
    )
    parser.add_argument(
        "--check", action="store_true",
        help="Check installation status (default)"
    )
    parser.add_argument(
        "--install", action="store_true",
        help="Interactive installation"
    )
    parser.add_argument(
        "--guide", action="store_true",
        help="Show installation guide"
    )
    
    args = parser.parse_args()
    
    if args.install:
        return 0 if install_mermaid_cli() else 1
    elif args.guide:
        print_installation_guide()
        return 0
    else:  # default is --check
        return print_status()

if __name__ == "__main__":
    sys.exit(main())