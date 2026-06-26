"""
Basic usage examples for git-hooks-manager
"""
import os
import sys
import tempfile
import shutil

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from hooks_manager import HookManager


def example_install_hook():
    """Install a pre-commit hook with lint-and-test template."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Init a git repo
        os.system(f"cd {tmpdir} && git init -q")
        
        manager = HookManager(tmpdir)
        manager.install("pre-commit", template="lint-and-test")
        
        hooks = manager.list_hooks()
        print("Installed hooks:", hooks)
        assert "pre-commit" in hooks


def example_validate_message():
    """Validate commit messages."""
    manager = HookManager(".")
    
    valid = "feat: add user authentication"
    errors = manager.validate_commit_message(valid)
    print(f"'{valid}' -> {'VALID' if not errors else 'INVALID'}")
    
    invalid = "bad message format"
    errors = manager.validate_commit_message(invalid)
    print(f"'{invalid}' -> INVALID ({len(errors)} errors)")
    for e in errors:
        print(f"  - {e}")


def example_validate_branch():
    """Validate branch names."""
    manager = HookManager(".")
    
    valid = "feature/add-login"
    errors = manager.validate_branch_name(valid)
    print(f"'{valid}' -> {'VALID' if not errors else 'INVALID'}")
    
    invalid = "main"
    errors = manager.validate_branch_name(invalid)
    print(f"'{invalid}' -> INVALID ({len(errors)} errors)")
    for e in errors:
        print(f"  - {e}")


def example_export_import():
    """Export and import hook configurations."""
    with tempfile.TemporaryDirectory() as tmpdir:
        os.system(f"cd {tmpdir} && git init -q")
        
        manager = HookManager(tmpdir)
        manager.install("pre-commit", template="conventional-commits")
        
        config_path = os.path.join(tmpdir, "hooks-config.json")
        manager.export_config(config_path)
        
        with open(config_path) as f:
            print("Exported config preview:")
            print(f.read()[:500])
        
        # Uninstall and re-import
        manager.uninstall("pre-commit")
        manager.import_config(config_path)
        assert "pre-commit" in manager.list_hooks()
        print("Import successful!")


def example_custom_hook():
    """Register a custom hook using decorator."""
    manager = HookManager(".")
    
    @manager.hook("pre-commit")
    def my_custom_check():
        print("Running custom pre-commit check...")
        return True
    
    print("Custom hook registered:", "pre-commit" in manager._hooks)


if __name__ == "__main__":
    print("=" * 50)
    print("Example 1: Install Hook")
    print("=" * 50)
    example_install_hook()
    
    print("\n" + "=" * 50)
    print("Example 2: Validate Message")
    print("=" * 50)
    example_validate_message()
    
    print("\n" + "=" * 50)
    print("Example 3: Validate Branch")
    print("=" * 50)
    example_validate_branch()
    
    print("\n" + "=" * 50)
    print("Example 4: Export/Import")
    print("=" * 50)
    example_export_import()
    
    print("\n" + "=" * 50)
    print("Example 5: Custom Hook")
    print("=" * 50)
    example_custom_hook()
