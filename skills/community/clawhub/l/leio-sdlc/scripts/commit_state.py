import argparse
import os
import sys
import subprocess

def main():
    parser = argparse.ArgumentParser(description="Safely commit administrative files like STATE.md and PRDs")
    parser.add_argument("--files", nargs="+", required=True, help="Absolute paths to administrative files to commit")
    args = parser.parse_args()

    # Find git root
    try:
        git_root = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()
    except subprocess.CalledProcessError:
        print("[FATAL] Not in a git repository")
        sys.exit(1)

    valid_files = []
    for f in args.files:
        abs_f = os.path.abspath(f)
        
        # Check if it exists
        if not os.path.exists(abs_f):
            print(f"Error: file not found: {abs_f}")
            sys.exit(1)

        rel_path = os.path.relpath(abs_f, git_root)
        
        # Validate administrative files
        is_valid = False
        if rel_path == "STATE.md":
            is_valid = True
        elif rel_path.startswith("docs/PRDs/") and rel_path.endswith(".md"):
            is_valid = True
            
        if not is_valid:
            print("[FATAL] commit_state.py can only be used for state and PRD files. Source code changes must go through the SDLC pipeline.")
            sys.exit(1)
            
        valid_files.append(abs_f)

    # Check for git index lock
    lock_file = os.path.join(git_root, ".git", "index.lock")
    if os.path.exists(lock_file):
        print("[FATAL] Git index is locked. Please wait or remove .git/index.lock if a previous process crashed.")
        sys.exit(1)

    # Add and commit
    try:
        subprocess.run(["git", "add"] + valid_files, check=True)
        subprocess.run(["git", "-c", "sdlc.runtime=1", "commit", "-m", "chore(state): update manager state"], check=True)
        print("Successfully baselined PRD/state files.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to commit files: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
