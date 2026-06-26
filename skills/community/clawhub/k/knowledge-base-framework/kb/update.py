#!/usr/bin/env python3
"""
KB Framework Update System

Auto-updater that checks GitHub releases and installs the latest version.
Similar to 'openclaw update'.

Usage:
    python3 kb/update.py              # Check and update if needed
    python3 kb/update.py --check      # Only check, don't update
    python3 kb/update.py --force      # Force update even if same version
"""

import argparse
import json
import os
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import urllib.request
from datetime import datetime
from pathlib import Path

# Configuration
GITHUB_REPO = "Minenclown/kb-framework"
VERSION_FILE = Path(__file__).parent / "version.py"
try:
    from kb.framework.paths import get_default_backup_dir
    BACKUP_DIR = get_default_backup_dir()
except ImportError:
    from kb.framework.paths import get_default_base_path
    BACKUP_DIR = get_default_base_path() / "backup"

# Allowed pattern for GitHub repo names (owner/repo format)
import re
_GITHUB_REPO_PATTERN = re.compile(r'^[a-zA-Z0-9_\-]+/[a-zA-Z0-9_\-.]+$')


def get_current_version():
    """Read current installed version."""
    if VERSION_FILE.exists():
        content = VERSION_FILE.read_text()
        # Extract version from VERSION = "x.x.x"
        match = content.split('VERSION = "')[1].split('"')[0] if 'VERSION = "' in content else None
        return match or "0.0.0"
    return "0.0.0"


def get_latest_release(repo=None):
    """Fetch latest release info from GitHub API."""
    repo = repo or GITHUB_REPO
    
    # Validate repo format to prevent injection into URL
    if not _GITHUB_REPO_PATTERN.match(repo):
        print(f"❌ Invalid repository format: {repo}. Expected 'owner/repo' with alphanumeric characters.")
        return None
    
    try:
        url = f"https://api.github.com/repos/{repo}/releases/latest"
        req = urllib.request.Request(url)
        req.add_header("Accept", "application/vnd.github.v3+json")
        req.add_header("User-Agent", "KB-Framework-Updater")
        
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            return {
                "version": data["tag_name"].lstrip("v"),
                "url": data["zipball_url"],
                "published": data["published_at"],
                "notes": data["body"][:200] + "..." if len(data["body"]) > 200 else data["body"]
            }
    except Exception as e:
        print(f"❌ Error checking latest release: {e}")
        return None


def backup_current_installation(kb_path):
    """Create backup of current installation."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = BACKUP_DIR / f"kb_backup_{timestamp}"
    
    print(f"📦 Creating backup at {backup_path}...")
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    
    # Backup kb/ directory
    if kb_path.exists():
        shutil.copytree(kb_path, backup_path / "kb", ignore_dangling_symlinks=True)
    
    # Backup config if exists
    config_path = kb_path / "config.py"
    if config_path.exists():
        shutil.copy2(config_path, backup_path / "config.py.bak")
    
    # Backup database
    try:
        from kb.framework.paths import get_default_db_path
        db_path = get_default_db_path()
    except ImportError:
        from kb.framework.paths import get_default_base_path
        db_path = get_default_base_path() / "library" / "biblio.db"
    if db_path.exists():
        shutil.copy2(db_path, backup_path / "biblio.db.bak")
    
    return backup_path


def preserve_config(kb_path):
    """Save config.py for restoration."""
    config_path = kb_path / "config.py"
    if config_path.exists():
        temp_dir = Path(tempfile.gettempdir())
        preserved = temp_dir / "kb_config_backup.py"
        shutil.copy2(config_path, preserved)
        return preserved
    return None


def restore_config(kb_path, preserved_config):
    """Restore preserved config.py."""
    if preserved_config and preserved_config.exists():
        config_path = kb_path / "config.py"
        shutil.copy2(preserved_config, config_path)
        print("✅ Restored config.py")


def download_and_install(release_info, kb_path, scripts_path):
    """Download and install latest version."""
    import zipfile
    
    temp_dir = Path(tempfile.gettempdir()) / "kb_update"
    temp_dir.mkdir(exist_ok=True)
    
    zip_path = temp_dir / "kb_latest.zip"
    
    print(f"⬇️  Downloading v{release_info['version']}...")
    try:
        urllib.request.urlretrieve(release_info["url"], zip_path)
    except Exception as e:
        print(f"❌ Download failed: {e}")
        return False
    
    print("📂 Extracting...")
    extract_path = temp_dir / "extracted"
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)
    
    # Find the actual kb-framework folder inside extracted
    extracted_dirs = [d for d in extract_path.iterdir() if d.is_dir()]
    if not extracted_dirs:
        print("❌ Invalid archive structure")
        return False
    
    source_path = extracted_dirs[0]
    
    # Preserve current config
    preserved_config = preserve_config(kb_path)
    
    # Replace kb/ directory
    print("🔄 Updating files...")
    if kb_path.exists():
        # Validate before deletion
        kb_path = Path(kb_path).resolve()
        try:
            from kb.framework.paths import get_default_base_path
            expected_base = get_default_base_path()
        except ImportError:
            expected_base = Path.home() / ".openclaw" / "kb"
        if not str(kb_path).startswith(str(expected_base)):
            raise ValueError(f"Refusing to delete {kb_path}: outside expected directory")
        shutil.rmtree(kb_path)
    
    new_kb = source_path / "kb"
    if new_kb.exists():
        shutil.copytree(new_kb, kb_path)
    
    # Update scripts
    new_scripts = source_path / "scripts"
    if new_scripts.exists() and scripts_path.exists():
        # Validate before deletion
        scripts_path = Path(scripts_path).resolve()
        try:
            from kb.framework.paths import get_default_base_path
            expected_base = get_default_base_path()
        except ImportError:
            expected_base = Path.home() / ".openclaw" / "kb"
        if not str(scripts_path).startswith(str(expected_base)):
            raise ValueError(f"Refusing to delete {scripts_path}: outside expected directory")
        shutil.rmtree(scripts_path)
        shutil.copytree(new_scripts, scripts_path)
    
    # Restore config
    restore_config(kb_path, preserved_config)
    
    # Update version file
    VERSION_FILE.write_text(f'VERSION = "{release_info["version"]}"\n')
    
    # Cleanup
    temp_dir = Path(temp_dir).resolve()
    try:
        from kb.framework.paths import get_default_base_path
        expected_base = get_default_base_path()
    except ImportError:
        expected_base = Path.home() / ".openclaw" / "kb"
    if not str(temp_dir).startswith(str(expected_base)):
        raise ValueError(f"Refusing to delete {temp_dir}: outside expected directory")
    shutil.rmtree(temp_dir)
    
    return True


def _validate_script_path(script_path: Path, allowed_parent: Path) -> Path:
    """
    Validate a script path is safe to execute.
    
    Ensures:
    - Path is resolved and within the allowed parent directory
    - Path points to an existing .py file
    - No path traversal (../) attacks
    
    Args:
        script_path: Path to validate
        allowed_parent: Parent directory the script must reside in
    
    Returns:
        Resolved, validated path
    
    Raises:
        ValueError: If path is invalid or outside allowed directory
    """
    resolved = script_path.resolve()
    allowed_resolved = allowed_parent.resolve()
    
    # Check path is within allowed directory
    try:
        resolved.relative_to(allowed_resolved)
    except ValueError:
        raise ValueError(
            f"Script path {resolved} is outside allowed directory {allowed_resolved}"
        )
    
    # Check it's a .py file
    if resolved.suffix != '.py':
        raise ValueError(f"Script must be a .py file, got: {resolved}")
    
    # Check it exists
    if not resolved.is_file():
        raise ValueError(f"Script does not exist: {resolved}")
    
    return resolved


def update_database_schema(kb_path):
    """Run any necessary database migrations."""
    try:
        from kb.framework.paths import get_default_db_path
        db_path = get_default_db_path()
    except ImportError:
        from kb.framework.paths import get_default_base_path
        db_path = get_default_base_path() / "library" / "biblio.db"
    if not db_path.exists():
        return
    
    # Check if migration script exists
    migrate_script = kb_path / "scripts" / "migrate.py"
    if migrate_script.exists():
        print("🔄 Running database migrations...")
        try:
            # Validate script path to prevent command injection
            safe_path = _validate_script_path(migrate_script, kb_path)
            subprocess.run([sys.executable, str(safe_path)], check=True)
        except ValueError as e:
            print(f"⚠️  Migration script validation failed: {e}")
        except subprocess.CalledProcessError:
            print("⚠️  Migration had issues, but continuing...")


def main(args=None):
    """Main entry point - can be called with args or parse sys.argv."""
    parser = argparse.ArgumentParser(description="KB Framework Updater")
    parser.add_argument("--check", action="store_true", help="Only check, don't update")
    parser.add_argument("--force", action="store_true", help="Force update")
    parser.add_argument("--repo", default=GITHUB_REPO, help="GitHub repo (owner/name)")
    args = parser.parse_args()
    
    # Determine paths
    kb_path = Path(__file__).parent
    scripts_path = kb_path.parent / "scripts"
    
    print("🔧 KB Framework Update Checker")
    print("=" * 40)
    
    current = get_current_version()
    print(f"📍 Current version: {current}")
    
    print("🌐 Checking GitHub for latest release...")
    latest = get_latest_release(args.repo)
    
    if not latest:
        print("❌ Could not fetch release info")
        sys.exit(1)
    
    print(f"📦 Latest version: {latest['version']}")
    print(f"📅 Published: {latest['published'][:10]}")
    
    if args.check:
        if latest["version"] != current:
            print(f"\n⬆️  Update available: {current} → {latest['version']}")
        else:
            print("\n✅ Already up to date")
        return
    
    if latest["version"] == current and not args.force:
        print("\n✅ Already up to date! Use --force to reinstall anyway.")
        return
    
    # Confirm update
    if not args.force:
        print(f"\n⬆️  Update: {current} → {latest['version']}")
        confirm = input("Proceed with update? [Y/n]: ").strip().lower()
        if confirm and confirm not in ('y', 'yes'):
            print("Cancelled.")
            return
    
    # Perform update
    print("\n" + "=" * 40)
    backup_path = backup_current_installation(kb_path)
    
    if download_and_install(latest, kb_path, scripts_path):
        print("✅ Files updated successfully")
        
        # Run migrations if needed
        update_database_schema(kb_path)
        
        print("\n" + "=" * 40)
        print(f"🎉 Updated to v{latest['version']}!")
        print(f"📦 Backup saved at: {backup_path}")
        print("\nNext steps:")
        print("  - Test: python3 kb/indexer.py --stats")
        print("  - If issues: restore from backup and report")
    else:
        print("\n❌ Update failed!")
        print(f"📦 Backup available at: {backup_path}")
        sys.exit(1)


if __name__ == "__main__":
    main()
