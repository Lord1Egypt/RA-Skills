#!/usr/bin/env python3
import sys
import subprocess
import os

def check_python_version():
    print("Checking Python version...")
    major, minor = sys.version_info[:2]
    if major < 3 or minor < 10:
        print(f"Error: Python 3.10+ required. Found {major}.{minor}")
        return False
    print(f"OK: Python {major}.{minor} found.")
    return True

def install_dependencies():
    print("Installing dependencies from requirements.txt...")
    req_file = os.path.join(os.path.dirname(__file__), "..", "requirements.txt")
    if not os.path.exists(req_file):
        print(f"Error: {req_file} not found.")
        return False
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", req_file])
        print("OK: Dependencies installed.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        return False

def setup_permissions():
    print("Setting script permissions...")
    scripts_dir = os.path.dirname(__file__)
    for filename in os.listdir(scripts_dir):
        if filename.endswith(".sh"):
            filepath = os.path.join(scripts_dir, filename)
            os.chmod(filepath, 0o755)
            print(f"OK: chmod +x {filename}")
    return True

if __name__ == "__main__":
    success = True
    if not check_python_version(): success = False
    if not install_dependencies(): success = False
    if not setup_permissions(): success = False
    
    if success:
        print("\nSetup complete! You can now use the Modern Portfolio Theory skill.")
    else:
        print("\nSetup failed. Please check the errors above.")
        sys.exit(1)
