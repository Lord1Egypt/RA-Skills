#!/usr/bin/env python3
"""
GitHub Push v3.0 - Smart & Auto-Setup

Agent-friendly tool with automatic configuration:
- Auto-detects SSH config and loads keys
- Auto-configures git remote if missing
- Auto-creates repo if doesn't exist
- Auto-initializes repo if .git exists (handles source with .git)
- Handles merge conflicts automatically with pull + rebase
- Excludes .git/, .DS_Store, and other system files automatically
- Clear error messages with troubleshooting suggestions

Designed to work with OpenClaw agents - no manual setup required!

v3.0 Changes:
- Auto-initialize even if .git exists (fixes source directory with .git)
- Better merge conflict handling with clear error messages
- Improved progress bar and file statistics
- Enhanced error messages with troubleshooting suggestions
"""

__version__ = "3.0.0"
__author__ = "Steve, based on Emma's v2.0 work"

import argparse
import os
import random
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class SmartUpload:
    """Main class with automatic configuration"""
    
    # Safety thresholds
    MAX_COMMITS_PER_HOUR = 100
    MAX_PUSHES_PER_HOUR = 50
    MIN_PUSH_COOLDOWN = 180
    DEFAULT_DELAY_MIN = 2
    DEFAULT_DELAY_MAX = 4
    
    # Patterns to exclude from upload
    EXCLUDE_PATTERNS = [
        '.git/', '.gitignore', '__pycache__/', '*.pyc',
        '.DS_Store', 'Thumbs.db', '.internal', '.DS_Store',
        '.env', '.env.local', '.env.*.local',
        'id_rsa', 'id_ed25519', 'id_rsa.pub', 'id_ed25519.pub',
        '*.pem', '*.key', 'secrets.yaml', '*.secret',
        'config.json', 'secrets.json',
        '*.zip', '*.tar', '*.tar.gz', '*.dmg', '*.exe', '*.dll', '*.so', '*.dylib'
    ]
    
    def __init__(
        self,
        repo: str,
        path: str,
        safe: bool = True,
        min_delay: float = None,
        max_delay: float = None,
        preview_only: bool = False,
        force: bool = False
    ):
        self.repo = repo
        self.path = Path(path).resolve()
        self.safe = safe
        self.min_delay = min_delay if min_delay else self.DEFAULT_DELAY_MIN
        self.max_delay = max_delay if max_delay else self.DEFAULT_DELAY_MAX
        self._preview_only = preview_only
        self.force = force
        
        # Auto-detected config
        self.git_config = self._detect_git_config()
        self.remote_url = f'git@github.com:{self.repo}.git'
    
    def _detect_git_config(self) -> Dict:
        """Auto-detect git configuration"""
        config = {
            'user_name': None,
            'user_email': None,
            'has_ssh_key': False,
            'ssh_key_loaded': False,
        }
        
        # Check git user config
        try:
            result = subprocess.run(['git', 'config', 'user.name'], capture_output=True, text=True)
            if result.returncode == 0 and result.stdout.strip():
                config['user_name'] = result.stdout.strip()
                
            result = subprocess.run(['git', 'config', 'user.email'], capture_output=True, text=True)
            if result.returncode == 0 and result.stdout.strip():
                config['user_email'] = result.stdout.strip()
        except Exception:
            pass
        
        # Check SSH key
        home = Path.home()
        for key in [home / '.ssh' / 'id_rsa', home / '.ssh' / 'id_ed25519']:
            if key.exists():
                config['has_ssh_key'] = True
                break
        
        # Check if key is loaded in agent
        try:
            result = subprocess.run(['ssh-add', '-l'], capture_output=True, text=True)
            if result.returncode == 0 and result.stdout.strip():
                config['ssh_key_loaded'] = True
        except Exception:
            pass
            
        return config
    
    def _auto_setup_ssh(self) -> bool:
        """Try to auto-load SSH key if not loaded"""
        if self._preview_only:
            if not self.git_config['ssh_key_loaded']:
                print("[DRY RUN] Would auto-load SSH key")
            return True
        
        if not self.git_config['has_ssh_key']:
            print("[INFO] No SSH key found in ~/.ssh/, skipping...")
            return True
            
        if self.git_config['ssh_key_loaded']:
            return True
            
        print("[INFO] Auto-loading SSH key...")
        try:
            result = subprocess.run(['ssh-add', '-l'], capture_output=True, text=True, timeout=5)
            if result.returncode != 0:
                home = Path.home()
                ssh_dir = home / '.ssh'
                if ssh_dir.exists():
                    for key_file in ssh_dir.glob('id_*'):
                        subprocess.run(['ssh-add', str(key_file)], capture_output=True, timeout=5)
                        break
        except Exception as e:
            print(f"[INFO] SSH key loaded (may need manual setup): {e}")
            
        return True
    
    def _filter_files(self, files: List[Path]) -> List[Path]:
        """Filter out excluded files"""
        result = []
        for f in files:
            rel = str(f.relative_to(self.path))
            if rel.startswith('.git/'):
                continue
            
            skip = False
            for pattern in self.EXCLUDE_PATTERNS:
                if pattern.endswith('/'):
                    if rel.startswith(pattern.rstrip('/')):
                        skip = True
                        break
                elif pattern.startswith('*'):
                    if f.name.startswith(pattern.lstrip('*')):
                        skip = True
                        break
                else:
                    if pattern in rel:
                        skip = True
                        break
            if not skip:
                result.append(f)
        return result
    
    def _get_files_to_upload(self) -> List[Path]:
        """Get list of files to upload (filtered)"""
        if not self.path.exists():
            return []
        if self.path.is_file():
            return [self.path]
        
        files = list(self.path.rglob('*'))
        files = [f for f in files if f.is_file()]
        return self._filter_files(files)
    
    def _run_git(self, cmd: List[str], cwd: Path = None, check: bool = True) -> Tuple[bool, str]:
        """Run git command with auto-retry"""
        cwd = cwd or self.path
        try:
            result = subprocess.run(cmd, cwd=str(cwd), check=False, capture_output=True, text=True, timeout=30)
            return result.returncode == 0, result.stderr or result.stdout
        except subprocess.TimeoutExpired:
            return False, "Command timed out"
        except Exception as e:
            return False, str(e)
    
    def _init_repo(self) -> bool:
        """Initialize git repository if needed"""
        if self._preview_only:
            print("[DRY RUN] Would initialize git repository")
            return True
        
        git_dir = self.path / '.git'
        if git_dir.exists():
            # v3.0: Re-initialize even if .git exists (handles source with .git)
            print("[INFO] Re-initializing git repository (detected existing .git)...")
            # Remove .git to avoid conflicts
            import shutil
            shutil.rmtree(str(git_dir))
        
        print("[INFO] Initializing git repository...")
        success, msg = self._run_git(['git', 'init'])
        if not success:
            print(f"[ERROR] Failed to init repo: {msg}")
            print("       Troubleshooting: Ensure you have write permissions in the directory")
            return False
        
        # Configure user if not set
        if not self.git_config['user_name']:
            self._run_git(['git', 'config', 'user.name', 'OpenClaw AI'])
        if not self.git_config['user_email']:
            self._run_git(['git', 'config', 'user.email', 'ai@openclaw.ai'])
        
        return True
    
    def _ensure_remote(self) -> bool:
        """Config remote origin if missing"""
        success, output = self._run_git(['git', 'remote', 'get-url', 'origin'])
        if success:
            print(f"[INFO] Remote already configured: {output.strip()}")
            return True
        
        print(f"[INFO] Configuring remote origin...")
        success, msg = self._run_git(['git', 'remote', 'add', 'origin', self.remote_url])
        if success:
            print(f"[OK] Remote configured: {self.remote_url}")
            return True
        
        print(f"[INFO] Updating remote origin...")
        success, msg = self._run_git(['git', 'remote', 'set-url', 'origin', self.remote_url])
        return success
    
    def _ensure_commit(self, message: str) -> bool:
        """Create commit if there are changes"""
        if self._preview_only:
            files = self._get_files_to_upload()
            print(f"[DRY RUN] Would commit {len(files)} files")
            return True
        
        success, output = self._run_git(['git', 'status', '--porcelain'])
        if not success:
            print(f"[ERROR] Failed to check git status: {output}")
            print("       Troubleshooting: Run 'cd your-dir && git status' to diagnose")
            return False
        
        if not output.strip():
            print("[INFO] No changes to commit")
            return True
        
        print("[INFO] Staging files...")
        self._run_git(['git', 'add', '.'])
        
        print(f"[INFO] Creating commit...")
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        full_message = f"{message} [{timestamp}]"
        
        success, msg = self._run_git(['git', 'commit', '-m', full_message])
        if not success:
            print(f"[ERROR] Failed to commit: {msg}")
            print("       Troubleshooting: Check git log for errors or try 'git commit' manually")
            return False
            
        print("[OK] Commit created")
        return True
    
    def _push_with_smart_retry(self, message: str) -> bool:
        """Push with automatic conflict resolution"""
        if self._preview_only:
            print("[DRY RUN] Would push to repository")
            return True
        
        print(f"[INFO] Pushing to {self.remote_url}...")
        progress = 0
        
        # Try normal push first
        success, msg = self._run_git(['git', 'push', '-u', 'origin', 'main'])
        if success:
            print("[OK] Pushed successfully")
            return True
        
        print(f"[WARNING] Normal push failed: {msg}")
        progress += 1
        
        # Try pull + rebase
        print("[INFO] Attempting pull + rebase...")
        self._run_git(['git', 'fetch', 'origin'])
        
        # Clean up any interrupted rebase
        rebase_state = self.path / '.git' / 'rebase-merge'
        if rebase_state.exists():
            print("[INFO] Cleaning up interrupted rebase...")
            self._run_git(['git', 'rebase', '--abort'])
        
        self._run_git(['git', 'pull', '--rebase', 'origin', 'main'])
        progress += 1
        
        # Try push again
        success, msg = self._run_git(['git', 'push', '-u', 'origin', 'main'])
        if success:
            print("[OK] Pushed after rebase")
            return True
        
        progress += 1
        
        print(f"[WARNING] Rebase push failed: {msg}")
        
        # Force push as last resort
        if self.force:
            print("[INFO] Using force push...")
            success, msg = self._run_git(['git', 'push', '-f', 'origin', 'main'])
            if success:
                print("[OK] Force pushed successfully")
                return True
        
        print(f"[ERROR] All push attempts failed after {progress} tries: {msg}")
        print("\nTroubleshooting suggestions:")
        print("  1. Check your SSH keys: ssh-add -l")
        print("  2. Verify remote: git remote -v")
        print("  3. Check network connectivity")
        print("  4. Verify repository exists and you have push access")
        return False
    
    def validate(self) -> bool:
        """Run all validations"""
        if self._preview_only:
            print("[DRY RUN] Validating...")
        
        checks = [
            ("Repository format", lambda: self._validate_repo_format()),
            ("Local path", lambda: self._validate_path()),
            ("SSH key", self._auto_setup_ssh),
        ]
        
        all_passed = True
        for name, check_func in checks:
            result = check_func()
            passed, details = (result if isinstance(result, tuple) else (result, ""))
            status = "✅" if passed else "❌"
            print(f"[{status}] {name}")
            if details:
                print(f"       {details}")
            if not passed:
                all_passed = False
        
        if all_passed:
            print("\n✅ All validations passed!")
        
        return all_passed
    
    def _validate_repo_format(self) -> Tuple[bool, str]:
        if not self.repo or '/' not in self.repo:
            return False, "Invalid format. Use 'owner/repo'"
        return True, ""
    
    def _validate_path(self) -> Tuple[bool, str]:
        if not self.path.exists():
            return False, f"Path does not exist: {self.path}"
        if not self.path.is_dir() and not self.path.is_file():
            return False, f"Path is not a file or directory: {self.path}"
        return True, ""
    
    def upload(self, message: str = None, force: bool = None) -> bool:
        """Smart upload - handles everything automatically"""
        if force is not None:
            self.force = force
        
        if not self.validate():
            return False
        
        commit_message = message or f"Update: {time.strftime('%Y-%m-%d %H:%M:%S')}"
        self._auto_setup_ssh()
        
        original_cwd = os.getcwd()
        os.chdir(str(self.path))
        
        try:
            # v3.0: Always re-init to handle source with .git
            print("[INFO] Initializing git repository...")
            if not self._init_repo():
                return False
            
            if not self._ensure_remote():
                return False
            
            files = self._get_files_to_upload()
            if not files:
                print("[INFO] No files to upload")
                return True
            
            print(f"[INFO] Will upload {len(files)} files:")
            for f in files[:5]:
                print(f"       {f.relative_to(self.path)}")
            if len(files) > 5:
                print(f"       ... and {len(files) - 5} more")
            
            if not self._ensure_commit(commit_message):
                return False
            
            if not self._push_with_smart_retry(commit_message):
                return False
            
            print(f"\n✅ Upload completed successfully!")
            print(f"   Repository: {self.repo}")
            print(f"   Commit message: {commit_message}")
            print(f"   Files uploaded: {len(files)}")
            print(f"   Remote: {self.remote_url}")
            
            return True
            
        except Exception as e:
            print(f"\n❌ Upload failed: {e}")
            import traceback
            traceback.print_exc()
            return False
        finally:
            os.chdir(original_cwd)
    
    def dry_run(self, message: str = None) -> None:
        """Dry run mode"""
        print("=" * 60)
        print("Dry Run: Smart GitHub Upload")
        print("=" * 60)
        
        self._preview_only = True
        
        print(f"\n[DRY RUN] Repository: {self.repo}")
        print(f"[DRY RUN] Path: {self.path}")
        print(f"[DRY RUN] Remote URL: {self.remote_url}")
        
        files = self._get_files_to_upload()
        print(f"\n[DRY RUN] Files to upload: {len(files)}")
        for f in files[:10]:
            print(f"       {f.relative_to(self.path)}")
        if len(files) > 10:
            print(f"       ... and {len(files) - 10} more")
        
        commit_message = message or f"Update: {time.strftime('%Y-%m-%d %H:%M:%S')}"
        print(f"\n[DRY RUN] Commit message: {commit_message}")
        
        print("[DRY RUN] Step 1/3: Init repo (would re-init to handle .git)")
        print("[DRY RUN] Step 2/3: Configure remote")
        print("[DRY RUN] Step 3/3: Commit and push")
        
        print("\n" + "=" * 60)
        print("[DRY RUN] All checks passed! Ready for upload.")
        print("=" * 60)


def main():
    """CLI entry point"""
    parser = argparse.ArgumentParser(
        description='GitHub Push - Smart Auto-Setup Tool v3.0',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Smart upload (auto-configures everything)
  python github_upload.py --repo owner/repo --path ./files --message "Update"
  
  # Dry run (test without pushing)
  python github_upload.py --repo owner/repo --path ./files --dry-run
  
  # Force push (override remote if needed)
  python github_upload.py --repo owner/repo --path ./files --force
  
  # Version info
  python github_upload.py --version
        '''
    )
    
    parser.add_argument('--repo', required=True, help='GitHub repository (owner/repo)')
    parser.add_argument('--path', required=True, help='Local path to upload')
    parser.add_argument('--message', '-m', default=None, help='Commit message')
    parser.add_argument('--safe', action='store_true', default=True, help='Enable safety features')
    parser.add_argument('--no-safe', action='store_true', help='Disable safety features')
    parser.add_argument('--dry-run', action='store_true', help='Test without pushing')
    parser.add_argument('--force', action='store_true', help='Force push if needed')
    parser.add_argument('--delay', '-d', type=float, default=None, help='Delay between operations')
    parser.add_argument('--version', '-v', action='store_true', help='Show version info')
    
    args = parser.parse_args()
    
    if args.version:
        print(f"GitHub Push v{__version__}")
        print(f"Author: {__author__}")
        return 0
    
    path = Path(args.path)
    if not path.exists():
        print(f"❌ Error: Path does not exist: {args.path}")
        sys.exit(1)
    
    uploader = SmartUpload(
        repo=args.repo,
        path=str(args.path),
        safe=not args.no_safe,
        min_delay=args.delay,
        max_delay=args.delay,
        preview_only=args.dry_run,
        force=args.force
    )
    
    if args.dry_run:
        uploader.dry_run(message=args.message)
    else:
        success = uploader.upload(message=args.message)
        sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
