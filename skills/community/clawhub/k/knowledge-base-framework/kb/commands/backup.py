#!/usr/bin/env python3
"""
BackupCommand - Backup KB data and configuration

Provides two backup modes:
- --library-only: Backup only ~/kb/library/ (essences, reports, graph, biblio.db)
- --full: Backup library/ + DB + ChromaDB + config

Usage:
    python3 -m kb backup --library-only
    python3 -m kb backup --full
    python3 -m kb backup              # defaults to --library-only
"""

import argparse
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from kb.base.command import BaseCommand
from kb.base.config import KBConfig
from kb.commands import register_command
from kb.framework.exceptions import PipelineError


@register_command
class BackupCommand(BaseCommand):
    """Backup KB data and configuration."""
    
    name = "backup"
    help = "Backup KB data (library-only or full)"
    
    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        group = parser.add_mutually_exclusive_group()
        group.add_argument(
            "--library-only",
            action="store_true",
            default=True,
            help="Backup only the library/ directory (essences, reports, graph, biblio.db) [default]"
        )
        group.add_argument(
            "--full",
            action="store_true",
            default=False,
            help="Full backup: library/ + DB + ChromaDB + config"
        )
        parser.add_argument(
            "--output", "-o",
            type=str,
            default=None,
            help="Output directory (default: ~/.knowledge/backup/kb_backup_<timestamp>)"
        )
    
    def validate(self, args: argparse.Namespace) -> bool:
        config = self.get_config()
        
        if args.full:
            # For full backup, verify critical paths exist
            if not config.db_path.exists():
                self.get_logger().warning(f"Database not found: {config.db_path}")
        return True
    
    def _execute(self) -> int:
        log = self.get_logger()
        config = self.get_config()
        args = self._args
        
        # Determine backup mode
        full_backup = getattr(args, 'full', False)
        
        # Determine output directory
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        if args.output:
            backup_root = Path(args.output).resolve()
        else:
            backup_root = config.backup_dir / f"kb_backup_{timestamp}"
        
        # Create backup root
        backup_root.mkdir(parents=True, exist_ok=True)
        
        log.info(f"📦 Creating {'full' if full_backup else 'library-only'} backup at {backup_root}")
        
        try:
            if full_backup:
                self._backup_full(config, backup_root, log)
            else:
                self._backup_library_only(config, backup_root, log)
            
            # Write backup manifest
            self._write_manifest(config, backup_root, full_backup, log)
            
            log.info(f"✅ Backup complete: {backup_root}")
            print(f"📦 Backup saved to: {backup_root}")
            return self.EXIT_SUCCESS
            
        except PipelineError as e:
            log.error(f"Backup failed: {e}")
            print(f"❌ Backup failed: {e}", file=sys.stderr)
            return self.EXIT_EXECUTION_ERROR
    
    def _backup_library_only(self, config: KBConfig, backup_root: Path, log) -> None:
        """Backup only the library/ directory."""
        library_path = config.library_path
        
        if not library_path.exists():
            log.warning(f"Library path does not exist: {library_path}")
            print(f"⚠️  Library path not found: {library_path}")
            return
        
        # Copy library/ directory (includes biblio/, content/, agent/, biblio.db, etc.)
        dest = backup_root / "library"
        log.info(f"  📁 Copying library/ → {dest}")
        shutil.copytree(
            library_path,
            dest,
            ignore_dangling_symlinks=True,
            dirs_exist_ok=False
        )
        log.info(f"  ✅ library/ backed up ({self._dir_size(dest)})")
    
    def _backup_full(self, config: KBConfig, backup_root: Path, log) -> None:
        """Backup library/ + DB + ChromaDB + config."""
        
        # 1. Library
        self._backup_library_only(config, backup_root, log)
        
        # 2. SQLite Database
        db_path = config.db_path
        if db_path.exists():
            dest = backup_root / "knowledge.db.bak"
            log.info(f"  🗄️  Copying database → {dest}")
            shutil.copy2(db_path, dest)
            log.info(f"  ✅ Database backed up ({self._file_size(dest)})")
        else:
            log.warning(f"  ⚠️  Database not found: {db_path}")
        
        # 3. ChromaDB
        chroma_path = config.chroma_path
        if chroma_path.exists():
            dest = backup_root / "chroma_db"
            log.info(f"  🔍 Copying ChromaDB → {dest}")
            shutil.copytree(
                chroma_path,
                dest,
                ignore_dangling_symlinks=True,
                dirs_exist_ok=False
            )
            log.info(f"  ✅ ChromaDB backed up ({self._dir_size(dest)})")
        else:
            log.warning(f"  ⚠️  ChromaDB not found: {chroma_path}")
        
        # 4. Config (if accessible)
        config_path = config.base_path / "config.py"
        if config_path.exists():
            dest = backup_root / "config.py.bak"
            log.info(f"  ⚙️  Copying config → {dest}")
            shutil.copy2(config_path, dest)
            log.info(f"  ✅ Config backed up")
        else:
            log.info(f"  ℹ️  No config.py found at {config_path}")
    
    def _write_manifest(self, config: KBConfig, backup_root: Path, full_backup: bool, log) -> None:
        """Write a manifest file describing what was backed up."""
        timestamp = datetime.now(timezone.utc).isoformat()
        manifest = (
            f"KB Backup Manifest\n"
            f"==================\n"
            f"Timestamp: {timestamp}\n"
            f"Mode: {'full' if full_backup else 'library-only'}\n"
            f"KB base_path: {config.base_path}\n"
            f"Library path: {config.library_path}\n"
            f"DB path: {config.db_path}\n"
            f"ChromaDB path: {config.chroma_path}\n"
            f"\n"
            f"Contents:\n"
            f"  - library/     ✅\n"
        )
        if full_backup:
            manifest += (
                f"  - knowledge.db ✅\n"
                f"  - chroma_db/   ✅\n"
                f"  - config.py    ✅\n"
            )
        
        manifest_path = backup_root / "MANIFEST.txt"
        manifest_path.write_text(manifest, encoding="utf-8")
        log.debug(f"  Manifest written to {manifest_path}")
    
    @staticmethod
    def _file_size(path: Path) -> str:
        """Human-readable file size."""
        size = path.stat().st_size
        for unit in ("B", "KB", "MB", "GB"):
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"
    
    @staticmethod
    def _dir_size(path: Path) -> str:
        """Human-readable directory size."""
        total = sum(f.stat().st_size for f in path.rglob("*") if f.is_file())
        for unit in ("B", "KB", "MB", "GB"):
            if total < 1024:
                return f"{total:.1f} {unit}"
            total /= 1024
        return f"{total:.1f} TB"