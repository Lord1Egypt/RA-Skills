import os
import re
import shutil
import sys

PROTECTED_SKILLS = [
    'local-skill-manager',
    'skill-evolution-tracker',
    'skill-auditor',
    'writing-skills'
]

def validate_skill_name(skill_name: str) -> bool:
    """
    Validate skill name: only allow lowercase letters, numbers, and hyphens.
    Reject any path separators, '..', or absolute paths to prevent
    path traversal attacks (e.g., '../other-dir' or '/etc/passwd').
    """
    return bool(re.match(r'^[a-z0-9-]+$', skill_name))

def resolve_skills_root() -> str:
    """
    Resolve the skills root directory (two levels up from this script).
    Returns the canonicalized absolute path.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.realpath(os.path.abspath(os.path.join(current_dir, '../../')))

def delete_skill(skill_name: str, dry_run: bool = False, force: bool = False) -> None:
    # --- Step 1: Validate skill name format ---
    if not validate_skill_name(skill_name):
        print(
            f"Error: Invalid skill name '{skill_name}'.\n"
            "Skill names must only contain lowercase letters, numbers, and hyphens.\n"
            "Path separators and '..' are not allowed."
        )
        return

    # --- Step 2: Check protected list ---
    if skill_name in PROTECTED_SKILLS:
        print(f"Error: '{skill_name}' is a protected system skill and cannot be deleted.")
        return

    # --- Step 3: Resolve and canonicalize paths ---
    skills_root = resolve_skills_root()
    # Use realpath to resolve any symlinks in the target path
    target_path = os.path.realpath(os.path.join(skills_root, skill_name))

    # --- Step 4: Confirm target is strictly inside skills_root (path traversal guard) ---
    # Add os.sep to prevent prefix collision (e.g., skills_root/foo matching skills_root/foobar)
    if not target_path.startswith(skills_root + os.sep) and target_path != skills_root:
        print(
            f"Error: Resolved path '{target_path}' is outside the skills directory '{skills_root}'.\n"
            "Operation aborted for safety."
        )
        return

    # --- Step 5: Check existence ---
    if not os.path.exists(target_path):
        print(f"Skill '{skill_name}' not found in '{skills_root}'.")
        return

    # --- Step 6: Warn about symlinks ---
    original_path = os.path.join(skills_root, skill_name)
    if os.path.islink(original_path):
        print(
            f"[WARNING] '{skill_name}' is a symbolic link pointing to '{os.readlink(original_path)}'.\n"
            "Deleting it will remove the SYMLINK ONLY, not the target directory."
        )

    # --- Step 7: Dry-run mode ---
    if dry_run:
        print(f"[DRY-RUN] Would delete: {target_path}")
        print("[DRY-RUN] No files were actually removed. Run without --dry-run to proceed.")
        return

    # --- Step 8: Confirmation prompt (unless --force is passed) ---
    if not force:
        print(f"About to permanently delete: {target_path}")
        answer = input("Are you sure? Type 'yes' to confirm: ").strip().lower()
        if answer != 'yes':
            print("Deletion cancelled.")
            return

    # --- Step 9: Execute deletion ---
    try:
        if os.path.islink(original_path):
            os.unlink(original_path)   # Remove symlink only, not target
        else:
            shutil.rmtree(target_path)
        print(f"Successfully deleted '{skill_name}'.")
    except Exception as e:
        print(f"Error deleting skill: {e}")


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print("Usage: python delete_skill.py <skill-name> [--dry-run] [--force]")
        print()
        print("Options:")
        print("  --dry-run   Preview what would be deleted without making any changes.")
        print("  --force     Skip the confirmation prompt (use with caution).")
        sys.exit(1)

    skill_arg = args[0]
    dry_run_flag = '--dry-run' in args
    force_flag = '--force' in args

    delete_skill(skill_arg, dry_run=dry_run_flag, force=force_flag)
