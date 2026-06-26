#!/usr/bin/env python3
"""
Backup and restore database.
"""

import argparse
import json
import os
import shutil
import sys
from datetime import datetime
from typing import Dict, Any


def get_db_path(username: str) -> str:
    """Get database file path for a user."""
    skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(skill_dir, 'data')
    return os.path.join(data_dir, f"{username}.db")


def get_backup_dir() -> str:
    """Get backup directory."""
    skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    backup_dir = os.path.join(skill_dir, 'backups')
    os.makedirs(backup_dir, exist_ok=True)
    return backup_dir


def backup(username: str) -> Dict[str, Any]:
    """Create database backup."""
    db_path = get_db_path(username)
    
    if not os.path.exists(db_path):
        return {"status": "error", "error": "database_not_found", "message": f"Database not found: {db_path}"}
    
    backup_dir = get_backup_dir()
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = os.path.join(backup_dir, f"{username}_{timestamp}.db")
    
    try:
        shutil.copy2(db_path, backup_file)
        
        # Clean old backups (keep last 10)
        backups = sorted([
            f for f in os.listdir(backup_dir) 
            if f.startswith(f"{username}_") and f.endswith('.db')
        ])
        
        for old_backup in backups[:-10]:
            os.remove(os.path.join(backup_dir, old_backup))
        
        return {
            "status": "success",
            "backup_file": backup_file,
            "original_size": os.path.getsize(db_path),
            "backups_kept": min(len(backups), 10)
        }
        
    except Exception as e:
        return {"status": "error", "error": "backup_failed", "message": str(e)}


def list_backups(username: str) -> Dict[str, Any]:
    """List available backups."""
    backup_dir = get_backup_dir()
    
    backups = []
    for f in os.listdir(backup_dir):
        if f.startswith(f"{username}_") and f.endswith('.db'):
            path = os.path.join(backup_dir, f)
            backups.append({
                "file": f,
                "path": path,
                "size": os.path.getsize(path),
                "created": datetime.fromtimestamp(os.path.getctime(path)).isoformat()
            })
    
    backups.sort(key=lambda x: x["created"], reverse=True)
    
    return {
        "status": "success",
        "backups": backups,
        "count": len(backups)
    }


def restore(username: str, backup_file: str, force: bool = False) -> Dict[str, Any]:
    """Restore database from backup."""
    db_path = get_db_path(username)
    
    # Check if backup exists
    if not os.path.exists(backup_file):
        # Try relative to backup dir
        backup_dir = get_backup_dir()
        backup_file = os.path.join(backup_dir, backup_file)
        
        if not os.path.exists(backup_file):
            return {"status": "error", "error": "backup_not_found", "message": f"Backup not found: {backup_file}"}
    
    # Check if current db exists
    if os.path.exists(db_path) and not force:
        return {
            "status": "error", 
            "error": "database_exists",
            "message": f"Database exists. Use --force to overwrite."
        }
    
    try:
        # Backup current before restore
        if os.path.exists(db_path):
            backup(username)
        
        shutil.copy2(backup_file, db_path)
        
        return {
            "status": "success",
            "restored_from": backup_file,
            "database_path": db_path
        }
        
    except Exception as e:
        return {"status": "error", "error": "restore_failed", "message": str(e)}


def main():
    parser = argparse.ArgumentParser(description='Database backup and restore')
    parser.add_argument('--user', required=True, help='Username')
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Backup
    subparsers.add_parser('backup', help='Create backup')
    
    # List
    subparsers.add_parser('list', help='List backups')
    
    # Restore
    restore_parser = subparsers.add_parser('restore', help='Restore from backup')
    restore_parser.add_argument('--file', required=True, help='Backup file name or path')
    restore_parser.add_argument('--force', action='store_true', help='Overwrite existing database')
    
    args = parser.parse_args()
    
    if args.command == 'backup':
        result = backup(args.user)
    elif args.command == 'list':
        result = list_backups(args.user)
    elif args.command == 'restore':
        result = restore(args.user, args.file, args.force)
    else:
        parser.print_help()
        sys.exit(1)
    
    print(json.dumps(result, indent=2))
    sys.exit(0 if result['status'] == 'success' else 1)


if __name__ == '__main__':
    main()
