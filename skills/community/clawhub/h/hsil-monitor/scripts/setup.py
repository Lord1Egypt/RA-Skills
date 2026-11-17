import os
import subprocess
import sys

def check_command(cmd):
    try:
        subprocess.run(["command", "-v", cmd], check=True, capture_output=True, shell=True)
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    print("Checking hsil-monitor requirements...")
    
    requirements = ["curl", "jq", "sort", "awk", "sed", "date", "mv"]
    missing = []
    
    for req in requirements:
        if check_command(req):
            print(f"  [OK] {req}")
        else:
            print(f"  [MISSING] {req}")
            missing.append(req)
            
    home_dir = os.environ.get("HSIL_MONITOR_HOME", os.path.expanduser("~/.config/hsil-monitor"))
    print(f"Checking storage path: {home_dir}")
    
    try:
        os.makedirs(home_dir, exist_ok=True)
        test_file = os.path.join(home_dir, ".write_test")
        with open(test_file, "w") as f:
            f.write("test")
        os.remove(test_file)
        print("  [OK] Storage path is writable")
    except Exception as e:
        print(f"  [ERROR] Storage path is not writable: {e}")
        sys.exit(1)
        
    if missing:
        print(f"\nError: Missing required commands: {', '.join(missing)}")
        sys.exit(1)
        
    print("\nSetup validation complete. hsil-monitor is ready for agent use.")

if __name__ == "__main__":
    main()
