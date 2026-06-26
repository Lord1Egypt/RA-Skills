#!/usr/bin/env python3
"""
Git commit helper script with changelog-style templates.
Supports: Added, Changed, Deprecated, Removed, Fixed
"""

import subprocess
import sys
from typing import Optional


COMMIT_TYPES = {
    "Added": "for new features",
    "Changed": "for changes in existing functionality",
    "Deprecated": "for soon-to-be removed features",
    "Removed": "for now removed features",
    "Fixed": "for any bug fixes"
}


def run_git_command(args: list[str]) -> tuple[int, str, str]:
    """Run a git command and return (returncode, stdout, stderr)."""
    result = subprocess.run(
        ["git"] + args,
        capture_output=True,
        text=True
    )
    return result.returncode, result.stdout, result.stderr


def get_staged_files() -> list[str]:
    """Get list of staged files."""
    returncode, stdout, _ = run_git_command(["diff", "--cached", "--name-only"])
    if returncode != 0:
        return []
    return [f for f in stdout.strip().split('\n') if f]


def create_commit(commit_type: str, title: str, body: Optional[str] = None, 
                  no_verify: bool = False) -> bool:
    """
    Create a git commit with the specified template.
    
    Args:
        commit_type: One of Added, Changed, Deprecated, Removed, Fixed
        title: Short description for commit title
        body: Optional detailed description for commit body
        no_verify: Skip git hooks if True
        
    Returns:
        True if commit successful, False otherwise
    """
    if commit_type not in COMMIT_TYPES:
        print(f"Error: Invalid commit type '{commit_type}'")
        print(f"Valid types: {', '.join(COMMIT_TYPES.keys())}")
        return False
    
    # Check if there are staged changes
    staged_files = get_staged_files()
    if not staged_files:
        print("Error: No staged changes to commit")
        print("Use 'git add' to stage files first")
        return False
    
    # Build commit message
    commit_message = f"[{commit_type}] {title}"
    if body:
        commit_message += f"\n\n{body}"
    
    # Create the commit
    commit_args = ["commit", "-m", commit_message]
    if no_verify:
        commit_args.append("--no-verify")
    
    returncode, stdout, stderr = run_git_command(commit_args)
    
    if returncode == 0:
        print(f"✓ Commit created successfully:")
        print(f"  [{commit_type}] {title}")
        if body:
            print(f"\n  {body[:100]}{'...' if len(body) > 100 else ''}")
        print(f"\n  Files: {', '.join(staged_files)}")
        return True
    else:
        print(f"✗ Commit failed:")
        print(stderr)
        return False


def interactive_commit() -> bool:
    """Interactive mode to create a commit."""
    print("Git Commit Template Helper")
    print("=" * 50)
    
    # Check for staged files
    staged_files = get_staged_files()
    if not staged_files:
        print("Error: No staged changes found")
        print("Use 'git add <files>' to stage changes first")
        return False
    
    print(f"\nStaged files ({len(staged_files)}):")
    for f in staged_files:
        print(f"  - {f}")
    
    # Select commit type
    print("\nSelect commit type:")
    types_list = list(COMMIT_TYPES.keys())
    for i, (ctype, desc) in enumerate(COMMIT_TYPES.items(), 1):
        print(f"  {i}. {ctype:12} - {desc}")
    
    while True:
        try:
            choice = input("\nEnter number (1-5): ").strip()
            idx = int(choice) - 1
            if 0 <= idx < len(types_list):
                commit_type = types_list[idx]
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 5.")
        except (ValueError, KeyboardInterrupt):
            print("\nCancelled")
            return False
    
    # Get title
    print(f"\n[{commit_type}] ", end="")
    title = input().strip()
    if not title:
        print("Error: Title cannot be empty")
        return False
    
    # Get body (optional)
    print("\nCommit body (optional, press Enter twice to finish):")
    body_lines = []
    empty_count = 0
    while empty_count < 2:
        try:
            line = input()
            if line.strip():
                body_lines.append(line)
                empty_count = 0
            else:
                empty_count += 1
        except KeyboardInterrupt:
            print("\nCancelled")
            return False
    
    body = '\n'.join(body_lines).strip() if body_lines else None
    
    # Confirm
    print("\n" + "=" * 50)
    print("Preview:")
    print(f"[{commit_type}] {title}")
    if body:
        print(f"\n{body}")
    print("=" * 50)
    
    confirm = input("\nCreate this commit? [Y/n]: ").strip().lower()
    if confirm and confirm not in ('y', 'yes'):
        print("Cancelled")
        return False
    
    return create_commit(commit_type, title, body)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Command-line mode
        if sys.argv[1] == "--help" or sys.argv[1] == "-h":
            print("Usage:")
            print("  Interactive mode:")
            print("    python commit.py")
            print("\n  Direct mode:")
            print("    python commit.py <type> <title> [body]")
            print(f"\n  Types: {', '.join(COMMIT_TYPES.keys())}")
            print("\nExamples:")
            print("  python commit.py")
            print("  python commit.py Added 'user authentication'")
            print("  python commit.py Fixed 'memory leak in parser' 'Fixed buffer overflow'")
        else:
            # Direct commit
            commit_type = sys.argv[1]
            title = sys.argv[2] if len(sys.argv) > 2 else ""
            body = sys.argv[3] if len(sys.argv) > 3 else None
            
            if not title:
                print("Error: Title is required")
                sys.exit(1)
            
            success = create_commit(commit_type, title, body)
            sys.exit(0 if success else 1)
    else:
        # Interactive mode
        success = interactive_commit()
        sys.exit(0 if success else 1)
