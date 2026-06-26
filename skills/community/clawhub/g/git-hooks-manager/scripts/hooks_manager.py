#!/usr/bin/env python3
"""
Git Hooks Manager - Core Implementation
"""
import os
import sys
import re
import json
import subprocess
import argparse
from pathlib import Path
from typing import List, Optional, Dict, Any, Callable


TEMPLATES = {
    "lint-and-test": """#!/bin/sh
echo "Running lint and test..."
python -m flake8 . || exit 1
python -m pytest tests/ -q || exit 1
""",
    "conventional-commits": """#!/bin/sh
MSG_FILE=$1
python3 -c "
import re, sys
with open('$MSG_FILE') as f:
    msg = f.read().strip()
pattern = r'^(feat|fix|docs|style|refactor|test|chore|ci|build|perf)(\\(.+\\))?: .+$'
if not re.match(pattern, msg):
    print('ERROR: Commit message must follow conventional commits format.')
    print('Example: feat: add new feature')
    sys.exit(1)
"
""",
    "branch-guard": """#!/bin/sh
BRANCH=$(git symbolic-ref --short HEAD)
if [ "$BRANCH" = "main" ] || [ "$BRANCH" = "master" ]; then
    echo "ERROR: Direct commits to $BRANCH are not allowed."
    exit 1
fi
if ! echo "$BRANCH" | grep -Eq '^(feature|fix|hotfix|release|docs)/.+$'; then
    echo "ERROR: Branch name must follow pattern: (feature|fix|hotfix|release|docs)/description"
    exit 1
fi
""",
    "security-scan": """#!/bin/sh
echo "Running security scan..."
python -m bandit -r . -f json -o /dev/null || echo "Security issues found!"
""",
    "ci-simulation": """#!/bin/sh
echo "Simulating CI pipeline..."
python -m flake8 . || exit 1
python -m pytest tests/ -v || exit 1
echo "CI simulation passed!"
"""
}

HOOK_NAMES = [
    "applypatch-msg", "commit-msg", "post-applypatch", "post-checkout",
    "post-commit", "post-merge", "post-rewrite", "pre-applypatch",
    "pre-auto-gc", "pre-commit", "pre-merge-commit", "pre-push",
    "pre-rebase", "pre-receive", "prepare-commit-msg", "push-to-checkout",
    "update"
]


class HookManager:
    """Manage Git hooks in a repository."""
    
    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path).resolve()
        git_dir = self._find_git_dir()
        if not git_dir:
            raise RuntimeError("Not a git repository (or any of the parent directories)")
        self.hooks_dir = git_dir / "hooks"
        self.hooks_dir.mkdir(parents=True, exist_ok=True)
        self._hooks: Dict[str, Callable] = {}
    
    def _find_git_dir(self) -> Optional[Path]:
        """Find the .git directory for this repo."""
        current = self.repo_path
        for _ in range(10):  # Max 10 levels up
            git_dir = current / ".git"
            if git_dir.exists():
                return git_dir
            if current.parent == current:
                break
            current = current.parent
        return None
    
    def install(self, hook_name: str, template: Optional[str] = None, script: Optional[str] = None) -> bool:
        """Install a hook by name."""
        if hook_name not in HOOK_NAMES:
            print(f"Warning: {hook_name} is not a standard Git hook name")
        
        hook_path = self.hooks_dir / hook_name
        
        if script:
            content = script
        elif template and template in TEMPLATES:
            content = TEMPLATES[template]
        else:
            # Default no-op hook
            content = "#!/bin/sh\n# Hook installed by git-hooks-manager\n"
        
        with open(hook_path, "w") as f:
            f.write(content)
        
        # Make executable on Unix
        if os.name != "nt":
            os.chmod(hook_path, 0o755)
        
        print(f"Installed {hook_name} hook at {hook_path}")
        return True
    
    def uninstall(self, hook_name: str) -> bool:
        """Remove a hook."""
        hook_path = self.hooks_dir / hook_name
        if hook_path.exists():
            hook_path.unlink()
            print(f"Removed {hook_name} hook")
            return True
        else:
            print(f"Hook {hook_name} not found")
            return False
    
    def list_hooks(self) -> List[str]:
        """List all installed hooks."""
        installed = []
        for hook_file in self.hooks_dir.iterdir():
            if hook_file.is_file() and not hook_file.name.endswith(".sample"):
                installed.append(hook_file.name)
        return sorted(installed)
    
    def validate_commit_message(self, message: str) -> List[str]:
        """Validate a commit message against conventional commits format."""
        errors = []
        pattern = r"^(feat|fix|docs|style|refactor|test|chore|ci|build|perf)(\(.+\))?: .+$"
        if not re.match(pattern, message):
            errors.append("Commit message must follow: type(scope): description")
            errors.append("Valid types: feat, fix, docs, style, refactor, test, chore, ci, build, perf")
        if len(message) > 72:
            errors.append(f"Subject line too long ({len(message)} chars, max 72)")
        return errors
    
    def validate_branch_name(self, name: str) -> List[str]:
        """Validate a branch name against common conventions."""
        errors = []
        pattern = r"^(feature|fix|hotfix|release|docs|chore)/[a-z0-9._-]+$"
        if not re.match(pattern, name):
            errors.append("Branch name must follow: type/description")
            errors.append("Valid prefixes: feature, fix, hotfix, release, docs, chore")
        if len(name) > 50:
            errors.append(f"Branch name too long ({len(name)} chars, max 50)")
        return errors
    
    def run_command(self, cmd: str, args: Optional[List[str]] = None) -> subprocess.CompletedProcess:
        """Run a shell command and return result."""
        full_cmd = [cmd] + (args or [])
        return subprocess.run(full_cmd, capture_output=True, text=True, cwd=self.repo_path)
    
    def export_config(self, path: str) -> None:
        """Export hook configuration to JSON."""
        config = {"hooks": {}}
        for hook_name in self.list_hooks():
            hook_path = self.hooks_dir / hook_name
            with open(hook_path) as f:
                config["hooks"][hook_name] = f.read()
        with open(path, "w") as f:
            json.dump(config, f, indent=2)
        print(f"Exported hooks config to {path}")
    
    def import_config(self, path: str) -> None:
        """Import hook configuration from JSON."""
        with open(path) as f:
            config = json.load(f)
        for hook_name, script in config.get("hooks", {}).items():
            self.install(hook_name, script=script)
        print(f"Imported hooks config from {path}")
    
    def hook(self, name: str):
        """Decorator for registering custom hooks."""
        def decorator(func: Callable):
            self._hooks[name] = func
            return func
        return decorator


def main():
    parser = argparse.ArgumentParser(description="Git Hooks Manager")
    subparsers = parser.add_subparsers(dest="command")
    
    # install
    install_parser = subparsers.add_parser("install", help="Install a hook")
    install_parser.add_argument("hook", nargs="?", help="Hook name")
    install_parser.add_argument("--all", action="store_true", help="Install all recommended hooks")
    install_parser.add_argument("--template", choices=list(TEMPLATES.keys()), help="Template to use")
    
    # uninstall
    uninstall_parser = subparsers.add_parser("uninstall", help="Uninstall a hook")
    uninstall_parser.add_argument("hook", help="Hook name")
    
    # list
    subparsers.add_parser("list", help="List installed hooks")
    
    # validate-message
    msg_parser = subparsers.add_parser("validate-message", help="Validate commit message")
    msg_parser.add_argument("message", help="Commit message to validate")
    
    # validate-branch
    branch_parser = subparsers.add_parser("validate-branch", help="Validate branch name")
    branch_parser.add_argument("name", help="Branch name to validate")
    
    # export
    export_parser = subparsers.add_parser("export", help="Export hooks config")
    export_parser.add_argument("file", help="Output JSON file")
    
    # import
    import_parser = subparsers.add_parser("import", help="Import hooks config")
    import_parser.add_argument("file", help="Input JSON file")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    manager = HookManager()
    
    if args.command == "install":
        if args.all:
            manager.install("pre-commit", template="lint-and-test")
            manager.install("commit-msg", template="conventional-commits")
            manager.install("pre-push", template="ci-simulation")
        elif args.hook:
            manager.install(args.hook, template=args.template)
        else:
            install_parser.print_help()
    
    elif args.command == "uninstall":
        manager.uninstall(args.hook)
    
    elif args.command == "list":
        hooks = manager.list_hooks()
        if hooks:
            print("Installed hooks:")
            for h in hooks:
                print(f"  - {h}")
        else:
            print("No custom hooks installed")
    
    elif args.command == "validate-message":
        errors = manager.validate_commit_message(args.message)
        if errors:
            print("Validation FAILED:")
            for e in errors:
                print(f"  - {e}")
            sys.exit(1)
        else:
            print("Commit message is valid!")
    
    elif args.command == "validate-branch":
        errors = manager.validate_branch_name(args.name)
        if errors:
            print("Validation FAILED:")
            for e in errors:
                print(f"  - {e}")
            sys.exit(1)
        else:
            print("Branch name is valid!")
    
    elif args.command == "export":
        manager.export_config(args.file)
    
    elif args.command == "import":
        manager.import_config(args.file)


if __name__ == "__main__":
    main()
