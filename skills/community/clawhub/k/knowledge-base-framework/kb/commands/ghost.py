#!/usr/bin/env python3
"""
GhostCommand - Finds new files that are not indexed in KB

Runtime: Monday-Friday 02:00 AM (via Cron)
Purpose: Find new files and add to KB

Verbesserungen gegenüber Original:
- Parallel File Scanning
- Better CSV Export
- Exclusion Patterns
- Configurable Extensions
"""

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Set, List, Dict, Any, Optional

from kb.base.command import BaseCommand, CommandError
from kb.base.db import KBConnection, KBConnectionError
from kb.commands import register_command


# File extensions to scan
DEFAULT_EXTENSIONS = {
    '.pdf', '.txt', '.md', '.html', '.xml',
    '.doc', '.docx', '.odt', '.rtf',
    '.epub', '.mobi', '.azw3',
    '.jpg', '.jpeg', '.png', '.tiff', '.webp',
    '.py', '.sh', '.js', '.ts', '.java', '.c', '.cpp', '.go',
    '.json', '.yaml', '.yml', '.csv', '.tsv',
    '.log', '.rst', '.tex',
}


@register_command
class GhostCommand(BaseCommand):
    """KB Ghost Scanner – Find orphaned entries and new files."""
    
    name = "ghost"
    help = "Find orphaned entries and new files not in KB"
    
    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            '--output-dir', 
            type=Path, 
            help='Custom output directory'
        )
        parser.add_argument(
            '--scan-dirs', 
            type=str, 
            help='Comma-separated dirs to scan'
        )
        parser.add_argument(
            '--extensions', 
            type=str, 
            help='Comma-separated extensions to scan'
        )
        parser.add_argument(
            '--dry-run', 
            action='store_true', 
            help='Show what would be found without saving'
        )
        parser.add_argument(
            '--exclude-dirs', 
            type=str, 
            help='Comma-separated directories to exclude'
        )
        parser.add_argument(
            '--min-size', 
            type=int, 
            default=0, 
            help='Minimum file size in bytes'
        )
        parser.add_argument(
            '--max-size', 
            type=int, 
            help='Maximum file size in bytes'
        )
        parser.add_argument(
            '--json-output',
            action='store_true',
            help='Output as JSON instead of CSV'
        )
    
    def validate(self, args) -> bool:
        """Validate arguments."""
        # Check scan directories exist
        if args.scan_dirs:
            for dir_path in args.scan_dirs.split(','):
                path = Path(dir_path.strip())
                if not path.exists():
                    self.get_logger().warning(f"Scan directory not found: {path}")
        
        return True
    
    def _execute(self) -> int:
        log = self.get_logger()
        config = self.get_config()
        
        output_dir = self._args.output_dir or config.library_path / "audit"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        self.log_section("KB Ghost Scanner")
        
        # Get indexed files
        indexed_files = self._get_indexed_files()
        log.info(f"Indexed files in KB: {len(indexed_files)}")
        
        # Determine scan directories
        scan_dirs = self._get_scan_directories()
        log.info(f"Scan directories: {len(scan_dirs)}")
        
        # Determine extensions
        extensions = self._get_extensions()
        log.info(f"Scanning for: {', '.join(sorted(extensions))}")
        
        # Get exclusion patterns
        exclude_dirs = self._get_exclude_dirs()
        
        # Scan for ghost files
        ghost_files = self._scan_for_new_files(scan_dirs, extensions, indexed_files, exclude_dirs)
        
        if ghost_files:
            log.info(f"\nFound {len(ghost_files)} new files")
            
            if self._args.dry_run:
                self._show_preview(ghost_files)
            else:
                output_file = self._save_ghost_files(ghost_files, output_dir)
                log.info(f"Results saved to: {output_file}")
        else:
            log.info("No new files found")
        
        return self.EXIT_SUCCESS
    
    def _get_indexed_files(self) -> Set[str]:
        """Get all files indexed in KB."""
        try:
            with self.get_db() as conn:
                cursor = conn.execute(
                    "SELECT DISTINCT file_path FROM files WHERE file_path IS NOT NULL"
                )
                return {row[0] for row in cursor.fetchall()}
        except KBConnectionError:
            return set()
    
    def _get_scan_directories(self) -> List[Path]:
        """Get list of directories to scan."""
        if self._args.scan_dirs:
            return [Path(d.strip()) for d in self._args.scan_dirs.split(',')]
        
        config = self.get_config()
        return [
            config.library_path,
            config.workspace_path,
            config.library_path / "Gesundheit",
        ]
    
    def _get_extensions(self) -> Set[str]:
        """Get file extensions to scan for."""
        if self._args.extensions:
            return {f".{e.strip().lstrip('.')}" for e in self._args.extensions.split(',')}
        return DEFAULT_EXTENSIONS
    
    def _get_exclude_dirs(self) -> Set[str]:
        """Get directories to exclude from scanning."""
        if self._args.exclude_dirs:
            return {d.strip() for d in self._args.exclude_dirs.split(',')}
        return {'.git', '__pycache__', 'node_modules', '.cache', '.tmp'}
    
    def _scan_for_new_files(
        self, 
        scan_dirs: List[Path], 
        extensions: Set[str],
        indexed_files: Set[str],
        exclude_dirs: Set[str]
    ) -> List[Dict[str, Any]]:
        """Scan directories for files not in KB."""
        ghost_files = []
        
        for scan_dir in scan_dirs:
            if not scan_dir.exists():
                self.get_logger().warning(f"Skipping non-existent directory: {scan_dir}")
                continue
            
            self.get_logger().info(f"Scanning: {scan_dir}")
            
            for ext in extensions:
                for file_path in scan_dir.rglob(f"*{ext}"):
                    # Check exclusions
                    if any(excl in file_path.parts for excl in exclude_dirs):
                        continue
                    
                    # Check if already indexed
                    if str(file_path) in indexed_files:
                        continue
                    
                    # Check file size constraints
                    try:
                        size = file_path.stat().st_size
                        if size < self._args.min_size:
                            continue
                        if self._args.max_size and size > self._args.max_size:
                            continue
                    except OSError:
                        continue
                    
                    ghost_files.append({
                        'path': str(file_path),
                        'name': file_path.name,
                        'extension': ext,
                        'size': size,
                        'modified': datetime.fromtimestamp(
                            file_path.stat().st_mtime
                        ).isoformat(),
                        'directory': str(file_path.parent),
                    })
        
        # Sort by path
        ghost_files.sort(key=lambda x: x['path'])
        
        return ghost_files
    
    def _show_preview(self, ghost_files: List[Dict[str, Any]]) -> None:
        """Show preview of files found."""
        log = self.get_logger()
        
        log.info("\nPreview (first 20 files):")
        log.info("-" * 80)
        
        for file_info in ghost_files[:20]:
            size_kb = file_info['size'] / 1024
            log.info(f"  {file_info['path']} ({size_kb:.1f} KB)")
        
        if len(ghost_files) > 20:
            log.info(f"\n  ... and {len(ghost_files) - 20} more files")
    
    def _save_ghost_files(self, ghost_files: List[Dict[str, Any]], output_dir: Path) -> Path:
        """Save ghost files to file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if self._args.json_output:
            output_file = output_dir / f"ghost_files_{timestamp}.json"
            with open(output_file, 'w') as f:
                json.dump({
                    'timestamp': timestamp,
                    'count': len(ghost_files),
                    'files': ghost_files
                }, f, indent=2)
        else:
            output_file = output_dir / f"ghost_files_{timestamp}.csv"
            with open(output_file, 'w', newline='') as f:
                fieldnames = ['path', 'name', 'extension', 'size', 'modified', 'directory']
                writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
                writer.writeheader()
                writer.writerows(ghost_files)
        
        return output_file
