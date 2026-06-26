#!/usr/bin/env python3
"""
Version Manager - Backup and rollback leader skill versions.
Part of create-leader skill.
"""

import argparse
import json
import os
import shutil
import sys
from datetime import datetime


def parse_args():
    parser = argparse.ArgumentParser(description='Leader Skill Version Manager')
    parser.add_argument('--action', choices=['backup', 'rollback', 'list'], required=True,
                        help='Action to perform')
    parser.add_argument('--slug', required=True,
                        help='Leader slug')
    parser.add_argument('--version', help='Version to rollback to (for rollback action)')
    parser.add_argument('--base-dir', default='./leaders',
                        help='Base directory for leader skills')
    return parser.parse_args()


def backup_version(base_dir, slug):
    """Backup current version of a leader skill."""
    leader_dir = os.path.join(base_dir, slug)
    if not os.path.exists(leader_dir):
        print(f"Error: Leader skill not found: {slug}", file=sys.stderr)
        sys.exit(1)

    versions_dir = os.path.join(leader_dir, 'versions')
    os.makedirs(versions_dir, exist_ok=True)

    # Generate version number based on timestamp
    now = datetime.utcnow()
    version = now.strftime('%Y%m%d_%H%M%S')
    backup_dir = os.path.join(versions_dir, f'v_{version}')

    # Copy current files to backup
    files_to_backup = ['leadership.md', 'upward.md', 'replacement.md', 'meta.json', 'SKILL.md']
    for filename in files_to_backup:
        src = os.path.join(leader_dir, filename)
        if os.path.exists(src):
            shutil.copy2(src, backup_dir)

    # Also copy knowledge directory if exists
    knowledge_dir = os.path.join(leader_dir, 'knowledge')
    if os.path.exists(knowledge_dir):
        shutil.copytree(knowledge_dir, os.path.join(backup_dir, 'knowledge'))

    print(f"✅ Version backed up: v_{version}")
    return version


def rollback_version(base_dir, slug, version):
    """Rollback to a previous version."""
    leader_dir = os.path.join(base_dir, slug)
    if not os.path.exists(leader_dir):
        print(f"Error: Leader skill not found: {slug}", file=sys.stderr)
        sys.exit(1)

    versions_dir = os.path.join(leader_dir, 'versions')
    if not os.path.exists(versions_dir):
        print(f"Error: No versions found for: {slug}", file=sys.stderr)
        sys.exit(1)

    # Find version directory
    backup_dir = None
    if version.startswith('v_'):
        backup_dir = os.path.join(versions_dir, version)
    else:
        # Try with v_ prefix
        backup_dir = os.path.join(versions_dir, f'v_{version}')

    if not os.path.exists(backup_dir):
        print(f"Error: Version not found: {version}", file=sys.stderr)
        print("Available versions:")
        list_versions(base_dir, slug)
        sys.exit(1)

    # Backup current version first
    backup_version(base_dir, slug)

    # Restore from backup
    files_to_restore = ['leadership.md', 'upward.md', 'replacement.md', 'meta.json', 'SKILL.md']
    for filename in files_to_restore:
        src = os.path.join(backup_dir, filename)
        dst = os.path.join(leader_dir, filename)
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"  Restored: {filename}")

    # Restore knowledge directory
    knowledge_backup = os.path.join(backup_dir, 'knowledge')
    knowledge_dst = os.path.join(leader_dir, 'knowledge')
    if os.path.exists(knowledge_backup):
        if os.path.exists(knowledge_dst):
            shutil.rmtree(knowledge_dst)
        shutil.copytree(knowledge_backup, knowledge_dst)
        print(f"  Restored: knowledge/")

    print(f"✅ Rolled back to version: {version}")


def list_versions(base_dir, slug):
    """List all available versions."""
    leader_dir = os.path.join(base_dir, slug)
    if not os.path.exists(leader_dir):
        print(f"Error: Leader skill not found: {slug}", file=sys.stderr)
        sys.exit(1)

    versions_dir = os.path.join(leader_dir, 'versions')
    if not os.path.exists(versions_dir):
        print(f"No versions found for: {slug}")
        return

    versions = []
    for item in sorted(os.listdir(versions_dir), reverse=True):
        item_path = os.path.join(versions_dir, item)
        if os.path.isdir(item_path):
            # Parse version timestamp
            version_name = item
            if version_name.startswith('v_'):
                try:
                    ts_str = version_name[2:]  # Remove v_ prefix
                    dt = datetime.strptime(ts_str, '%Y%m%d_%H%M%S')
                    versions.append({
                        'name': version_name,
                        'datetime': dt,
                        'path': item_path
                    })
                except ValueError:
                    pass

    if not versions:
        print(f"No versions found for: {slug}")
        return

    print(f"Found {len(versions)} version(s) for {slug}:\n")
    for v in versions:
        print(f"  {v['name']} - {v['datetime'].strftime('%Y-%m-%d %H:%M:%S UTC')}")


def main():
    args = parse_args()

    if args.action == 'backup':
        backup_version(args.base_dir, args.slug)
    elif args.action == 'rollback':
        if not args.version:
            print("Error: --version is required for rollback action", file=sys.stderr)
            sys.exit(1)
        rollback_version(args.base_dir, args.slug, args.version)
    elif args.action == 'list':
        list_versions(args.base_dir, args.slug)


if __name__ == '__main__':
    main()
