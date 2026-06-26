#!/usr/bin/env python3
"""
AuditCommand - KB Full Audit Tool

Vollständiger Integritätscheck.

Verbesserungen gegenüber Original:
- Modular Check System
- Detailed Error Reporting
- CSV Report Export
- Summary Statistics
"""

import argparse
import csv
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Any

from kb.base.command import BaseCommand, CommandError
from kb.base.db import KBConnection, KBConnectionError, validate_schema
from kb.commands import register_command
from kb.framework.exceptions import DatabaseError, PipelineError


@register_command
class AuditCommand(BaseCommand):
    """KB Full Audit – Vollständiger Integritätscheck."""
    
    name = "audit"
    help = "Run full KB audit"
    
    OUTPUT_DIR_NAME = "audit"
    REQUIRED_TABLES = ['files', 'file_sections', 'embeddings']
    
    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            '--output-dir', 
            type=Path, 
            help='Custom output directory'
        )
        parser.add_argument(
            '--skip-chroma', 
            action='store_true', 
            help='Skip ChromaDB check'
        )
        parser.add_argument(
            '--skip-files', 
            action='store_true', 
            help='Skip file existence check'
        )
        parser.add_argument(
            '--verbose', '-v', 
            action='store_true', 
            help='Verbose output'
        )
        parser.add_argument(
            '--export-csv', 
            type=Path, 
            help='Export issues to CSV file'
        )
        parser.add_argument(
            '--checks', 
            type=str, 
            help='Comma-separated list of checks to run (default: all)'
        )
    
    def validate(self, args) -> bool:
        if not super().validate(args):
            return False
        
        # Validate output directory
        output_dir = args.output_dir or self._get_default_output_dir()
        try:
            output_dir.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            self.get_logger().error(f"Cannot create output directory: {e}")
            return False
        
        return True
    
    def _execute(self) -> int:
        log = self.get_logger()
        
        output_dir = self._args.output_dir or self._get_default_output_dir()
        output_dir.mkdir(parents=True, exist_ok=True)
        
        self.log_section("KB Audit")
        
        # Initialize issue tracker
        self._issues: List[Dict[str, Any]] = []
        self._stats: Dict[str, int] = {}
        
        # Run checks based on arguments
        checks = self._get_checks_to_run()
        
        for check_name in checks:
            check_method = getattr(self, f"_check_{check_name}", None)
            if check_method and callable(check_method):
                try:
                    check_method()
                except DatabaseError as e:
                    log.error(f"Check '{check_name}' failed: {e}")
                    if self._args.verbose:
                        import traceback
                        traceback.print_exc()
            else:
                log.warning(f"Unknown check: {check_name}")
        
        # Export issues if requested
        if self._args.export_csv:
            self._export_issues_csv(self._args.export_csv)
        
        # Summary
        self._log_summary()
        
        return self.EXIT_SUCCESS if not self._issues else self.EXIT_EXECUTION_ERROR
    
    def _get_checks_to_run(self) -> List[str]:
        """Determine which checks to run."""
        if self._args.checks:
            return [c.strip() for c in self._args.checks.split(',')]
        
        # Default: all checks
        return [
            'db_integrity',
            'schema',
            'library_paths',
            'null_paths',
            'embeddings_table',
            'chroma_sync',
            'orphaned_entries',
        ]
    
    def _get_default_output_dir(self) -> Path:
        return self.get_config().library_path / self.OUTPUT_DIR_NAME
    
    def _add_issue(self, severity: str, check: str, message: str, details: str = None):
        """Add an issue to the tracker."""
        issue = {
            'timestamp': datetime.now().isoformat(),
            'severity': severity,  # ERROR, WARNING, INFO
            'check': check,
            'message': message,
            'details': details,
        }
        self._issues.append(issue)
        
        log = self.get_logger()
        if severity == 'ERROR':
            log.error(f"[{check}] {message}")
        elif severity == 'WARNING':
            log.warning(f"[{check}] {message}")
        else:
            log.info(f"[{check}] {message}")
    
    def _check_db_integrity(self) -> None:
        """Check database integrity."""
        log = self.get_logger()
        log.info("Checking DB integrity...")
        
        self._stats['db_tables'] = 0
        self._stats['db_indexes'] = 0
        
        try:
            with self.get_db() as conn:
                # Check tables
                tables = conn.fetchall(
                    "SELECT name FROM sqlite_master WHERE type='table'"
                )
                self._stats['db_tables'] = len(tables)
                log.info(f"DB Tables: {len(tables)}")
                
                # Check indexes
                indexes = conn.fetchall(
                    "SELECT name FROM sqlite_master WHERE type='index' AND sql IS NOT NULL"
                )
                self._stats['db_indexes'] = len(indexes)
                log.info(f"DB Indexes: {len(indexes)}")
                
                # Check foreign keys
                fk_result = conn.fetchone("PRAGMA foreign_keys")
                fk_on = fk_result[0] if fk_result else 0
                if fk_on:
                    log.info("Foreign Keys: ON")
                    self._stats['foreign_keys'] = 1
                else:
                    log.warning("Foreign Keys: OFF")
                    self._stats['foreign_keys'] = 0
                    self._add_issue('WARNING', 'db_integrity', 'Foreign keys are disabled')
                
        except KBConnectionError as e:
            self._add_issue('ERROR', 'db_integrity', f"Database error: {e}")
    
    def _check_schema(self) -> None:
        """Validate required tables exist."""
        log = self.get_logger()
        log.info("Checking schema...")
        
        try:
            with self.get_db() as conn:
                is_valid, missing = validate_schema(conn, self.REQUIRED_TABLES)
                
                if is_valid:
                    log.info(f"Schema valid (tables: {', '.join(self.REQUIRED_TABLES)})")
                else:
                    self._add_issue(
                        'ERROR', 
                        'schema', 
                        f"Missing tables: {', '.join(missing)}"
                    )
                    
        except KBConnectionError as e:
            self._add_issue('ERROR', 'schema', f"Cannot validate schema: {e}")
    
    def _check_library_paths(self) -> None:
        """Check if library files exist."""
        log = self.get_logger()
        log.info("Checking library paths...")
        
        if self._args.skip_files:
            log.info("Skipping file existence check")
            return
        
        missing_count = 0
        
        try:
            with self.get_db() as conn:
                files = conn.fetchall(
                    "SELECT id, file_path, file_name FROM files WHERE file_path IS NOT NULL"
                )
            
            total = len(files)
            log.info(f"Checking {total} file paths...")
            
            for file_id, file_path, original_name in files:
                if not Path(file_path).exists():
                    missing_count += 1
                    self._add_issue(
                        'WARNING',
                        'library_paths',
                        f"Missing file: {file_path}",
                        f"file_id={file_id}, original_name={original_name}"
                    )
            
            if missing_count > 0:
                log.warning(f"Missing files: {missing_count}")
            else:
                log.info("All library paths valid")
                
        except KBConnectionError as e:
            self._add_issue('ERROR', 'library_paths', f"Cannot check paths: {e}")
    
    def _check_null_paths(self) -> None:
        """Check for NULL/empty file paths."""
        log = self.get_logger()
        log.info("Checking for null paths...")
        
        try:
            with self.get_db() as conn:
                count_row = conn.fetchone(
                    "SELECT COUNT(*) FROM files WHERE file_path IS NULL OR file_path = ''"
                )
                count = count_row[0] if count_row else 0
            
            if count > 0:
                self._add_issue('WARNING', 'null_paths', f"Files with NULL/empty path: {count}")
                
                if self._args.verbose:
                    with self.get_db() as conn:
                        rows = conn.fetchall(
                            "SELECT id, file_name FROM files WHERE file_path IS NULL OR file_path = '' LIMIT 10"
                        )
                    for row in rows:
                        log.warning(f"  - {row['id']}: {row['file_name']}")
            else:
                log.info("All files have valid paths")
                
        except KBConnectionError as e:
            self._add_issue('ERROR', 'null_paths', f"Cannot check null paths: {e}")
    
    def _check_embeddings_table(self) -> None:
        """Check embeddings table status."""
        log = self.get_logger()
        log.info("Checking embeddings table...")
        
        try:
            with self.get_db() as conn:
                # Check table exists
                cursor = conn.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' AND name='embeddings'"
                )
                if not cursor.fetchone():
                    self._add_issue('ERROR', 'embeddings_table', "embeddings table missing")
                    return
                
                # Count entries
                count_row = conn.fetchone("SELECT COUNT(*) FROM embeddings")
                count = count_row[0] if count_row else 0
                
                log.info(f"embeddings table: {count} entries")
                self._stats['embeddings_count'] = count
                
        except KBConnectionError as e:
            self._add_issue('ERROR', 'embeddings_table', f"Cannot check embeddings: {e}")
    
    def _check_chroma_sync(self) -> None:
        """Check ChromaDB/SQLite sync status."""
        log = self.get_logger()
        log.info("Checking ChromaDB sync...")
        
        if self._args.skip_chroma:
            log.info("Skipping ChromaDB check")
            return
        
        config = self.get_config()
        
        try:
            from chromadb import PersistentClient
            from chromadb.config import Settings
            
            # Get ChromaDB count
            client = PersistentClient(
                path=str(config.chroma_path),
                settings=Settings(anonymized_telemetry=False)
            )
            collection = client.get_collection(name="kb_sections")
            chroma_count = collection.count()
            
            # Get SQLite count
            with self.get_db() as conn:
                sqlite_row = conn.fetchone(
                    "SELECT COUNT(*) FROM file_sections WHERE content_full IS NOT NULL"
                )
                sqlite_count = sqlite_row[0] if sqlite_row else 0
            
            log.info(f"ChromaDB: {chroma_count}, SQLite: {sqlite_count}")
            
            if chroma_count != sqlite_count:
                diff = abs(chroma_count - sqlite_count)
                self._add_issue(
                    'WARNING',
                    'chroma_sync',
                    f"Sync mismatch: SQLite={sqlite_count}, ChromaDB={chroma_count}",
                    f"Difference: {diff}"
                )
            else:
                log.info("ChromaDB/SQLite sync OK")
                
            self._stats['chroma_count'] = chroma_count
            self._stats['sqlite_count'] = sqlite_count
            
        except ImportError:
            self._add_issue('WARNING', 'chroma_sync', 'ChromaDB not available')
        except DatabaseError as e:
            self._add_issue('WARNING', 'chroma_sync', f"ChromaDB check failed: {e}")
    
    def _check_orphaned_entries(self) -> None:
        """Check for orphaned entries."""
        log = self.get_logger()
        log.info("Checking for orphaned entries...")
        
        try:
            with self.get_db() as conn:
                # Section entries without file_id reference
                orphan_row = conn.fetchone("""
                    SELECT COUNT(*) FROM file_sections s
                    LEFT JOIN files f ON s.file_id = f.id
                    WHERE f.id IS NULL AND s.file_id IS NOT NULL
                """)
                orphan_count = orphan_row[0] if orphan_row else 0
                
                if orphan_count > 0:
                    self._add_issue('WARNING', 'orphaned_entries', f"Orphaned sections: {orphan_count}")
                else:
                    log.info("No orphaned entries found")
                    
                self._stats['orphaned_count'] = orphan_count
                
        except KBConnectionError as e:
            self._add_issue('ERROR', 'orphaned_entries', f"Cannot check orphans: {e}")
    
    def _export_issues_csv(self, output_path: Path) -> None:
        """Export issues to CSV file."""
        log = self.get_logger()
        
        try:
            with open(output_path, 'w', newline='') as f:
                if self._issues:
                    writer = csv.DictWriter(f, fieldnames=self._issues[0].keys())
                    writer.writeheader()
                    writer.writerows(self._issues)
            
            log.info(f"Issues exported to {output_path}")
        except IOError as e:
            log.error(f"Failed to export issues: {e}")
    
    def _log_summary(self) -> None:
        """Log audit summary."""
        log = self.get_logger()
        
        log.info("=" * 50)
        log.info("Audit Summary")
        log.info("=" * 50)
        
        # Stats
        if self._stats:
            log.info("Statistics:")
            for key, value in sorted(self._stats.items()):
                log.info(f"  {key}: {value}")
        
        # Issues
        error_count = sum(1 for i in self._issues if i['severity'] == 'ERROR')
        warning_count = sum(1 for i in self._issues if i['severity'] == 'WARNING')
        
        log.info(f"\nIssues found: {len(self._issues)}")
        log.info(f"  - Errors: {error_count}")
        log.info(f"  - Warnings: {warning_count}")
        
        if not self._issues:
            log.info("\n[OK] Audit passed - no issues found!")
        elif error_count == 0:
            log.info("\n[WARNING] Audit completed with warnings")
        else:
            log.info("\n[FAIL] Audit failed - errors need attention")
