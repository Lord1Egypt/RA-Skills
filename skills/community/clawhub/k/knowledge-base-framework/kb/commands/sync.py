#!/usr/bin/env python3
"""
SyncCommand - ChromaDB Sync Tool

Delta Indexing für inkrementelle Updates.

Verbesserungen gegenüber Original:
- Besseres Error Handling
- Batch Processing mit Progress
- Transaction Support
- Dry-Run Verbesserungen
"""

import argparse
import hashlib
import json
import time
from typing import List, Set, Dict, Any, Optional

from kb.base.command import BaseCommand
from kb.base.db import KBConnection, KBConnectionError
from kb.commands import register_command
from kb.framework.chroma_integration import get_chroma, embed_batch
from kb.framework.batching import batched, BatchProgress, batched_chroma_upsert, batched_chroma_delete
from kb.framework.exceptions import DatabaseError, PipelineError


@register_command
class SyncCommand(BaseCommand):
    """ChromaDB Sync Tool – Delta Indexing für inkrementelle Updates."""
    
    name = "sync"
    help = "Sync ChromaDB with SQLite (delta or full)"
    
    BATCH_SIZE = 32
    MODEL_NAME = "all-MiniLM-L6-v2"
    
    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            '--stats', 
            action='store_true', 
            help='Show synchronization statistics'
        )
        parser.add_argument(
            '--dry-run', 
            action='store_true', 
            help='Simulation without making changes'
        )
        parser.add_argument(
            '--delta', 
            action='store_true', 
            help='Delta sync (default: only missing items)'
        )
        parser.add_argument(
            '--full', 
            action='store_true', 
            help='Full re-sync (requires reembed_all script)'
        )
        parser.add_argument(
            '--file-id', 
            type=str, 
            help='Sync specific file by ID'
        )
        parser.add_argument(
            '--delete-orphans', 
            action='store_true', 
            help='Delete orphaned ChromaDB entries'
        )
        parser.add_argument(
            '--batch-size', 
            type=int, 
            default=self.BATCH_SIZE,
            help=f'Batch size for embedding (default: {self.BATCH_SIZE})'
        )
        parser.add_argument(
            '--force', 
            action='store_true', 
            help='Force operation even if errors occur'
        )
    
    def validate(self, args) -> bool:
        """Validate prerequisites."""
        if not super().validate(args):
            return False
        
        # Check ChromaDB path exists
        chroma_path = self.get_config().chroma_path
        if not chroma_path.exists() and not (args.stats or args.dry_run):
            self.get_logger().warning(f"ChromaDB not found: {chroma_path}")
            if not args.force:
                return False
        
        return True
    
    def _execute(self) -> int:
        """Route to appropriate subcommand."""
        if self._args.stats:
            return self._cmd_stats()
        elif self._args.dry_run:
            return self._cmd_dry_run()
        elif self._args.file_id:
            return self._cmd_file(self._args.file_id)
        elif self._args.full:
            return self._cmd_full()
        else:
            return self._cmd_delta()
    
    def _get_sqlite_sections(self, conn: KBConnection) -> Dict[str, Dict[str, str]]:
        """Fetch all section IDs and hashes from SQLite."""
        cursor = conn.execute(
            "SELECT id, file_id, file_hash, content_full FROM file_sections "
            "WHERE content_full IS NOT NULL AND content_full != ''"
        )
        result = {}
        while True:
            rows = cursor.fetchmany(1000)  # Batch von 1000
            if not rows:
                break
            for row in rows:
                section_id = str(row['id'])
                content = row['content_full'] or ""
                content_hash = hashlib.md5(content.encode('utf-8')).hexdigest() if content else ""
                result[section_id] = {
                    'file_id': str(row['file_id']),
                    'file_hash': row['file_hash'] or "",
                    'content_hash': content_hash
                }
        return result
    
    def _get_chroma_sections(self) -> Set[str]:
        """Fetch all section IDs from ChromaDB via singleton."""
        try:
            chroma = get_chroma()
            collection = chroma.client.get_collection(name="kb_sections")
            # Batch-weise abrufen (ChromaDB hat keine direkte count-Methode)
            results = collection.get(include=['metadatas'], limit=1000)
            ids = set(results['ids'])
            # Wenn mehr vorhanden, weiter abrufen
            while len(results['ids']) == 1000:
                offset = len(ids)
                results = collection.get(include=['metadatas'], limit=1000, offset=offset)
                ids.update(results['ids'])
            return ids
        except DatabaseError as e:
            self.get_logger().warning(f"ChromaDB read error: {e}")
            return set()
    
    def _sync_stats(self, conn: KBConnection) -> Dict[str, Any]:
        """Get synchronization statistics."""
        # Use COUNT queries instead of loading all content
        cursor = conn.execute(
            "SELECT COUNT(*) as total, COUNT(DISTINCT file_id) as files FROM file_sections "
            "WHERE content_full IS NOT NULL AND content_full != ''"
        )
        row = cursor.fetchone()
        sqlite_count = row['total']
        file_count = row['files']
        
        chroma_sections = self._get_chroma_sections()
        chroma_count = len(chroma_sections)
        
        # For missing/orphan IDs, we need to compare - use a lighter query
        if sqlite_count > 0:
            cursor = conn.execute(
                "SELECT id FROM file_sections "
                "WHERE content_full IS NOT NULL AND content_full != '' "
                "LIMIT 10000"
            )
            sqlite_ids = set(str(r['id']) for r in cursor.fetchall())
        else:
            sqlite_ids = set()
        
        missing = sqlite_ids - chroma_sections
        orphans = chroma_sections - sqlite_ids
        
        return {
            'sqlite_sections': sqlite_count,
            'total_files': file_count,
            'chroma_sections': chroma_count,
            'missing_from_chroma': len(missing),
            'orphans_in_chroma': len(orphans),
            'coverage_pct': (chroma_count / sqlite_count * 100) if sqlite_count > 0 else 0,
            'missing_ids': list(missing)[:10],
            'orphan_ids': list(orphans)[:10]
        }
    
    def _cmd_stats(self) -> int:
        """Show synchronization statistics."""
        log = self.get_logger()
        
        self.log_section("ChromaDB Sync - Statistiken")
        
        try:
            with self.get_db() as conn:
                stats = self._sync_stats(conn)
            
            log.info(f"SQLite Sections:       {stats['sqlite_sections']}")
            log.info(f"ChromaDB Sections:     {stats['chroma_sections']}")
            log.info(f"Coverage:              {stats['coverage_pct']:.1f}%")
            log.info(f"Missing (in SQLite):  {stats['missing_from_chroma']}")
            log.info(f"Orphans (in ChromaDB): {stats['orphans_in_chroma']}")
            
            return self.EXIT_SUCCESS
            
        except KBConnectionError as e:
            log.error(f"Failed to get stats: {e}")
            return self.EXIT_EXECUTION_ERROR
    
    def _cmd_dry_run(self) -> int:
        """Simulate sync without making changes."""
        log = self.get_logger()
        
        self.log_section("ChromaDB Sync - Dry Run")
        
        try:
            with self.get_db() as conn:
                stats = self._sync_stats(conn)
            
            log.info(f"\nSQLite Sections:       {stats['sqlite_sections']}")
            log.info(f"ChromaDB Sections:     {stats['chroma_sections']}")
            log.info(f"Coverage:              {stats['coverage_pct']:.1f}%")
            log.info(f"Missing (in SQLite):   {stats['missing_from_chroma']}")
            log.info(f"Orphans (in ChromaDB): {stats['orphans_in_chroma']}")
            
            if stats['missing_ids']:
                log.info(f"\n[+] Would add: {stats['missing_from_chroma']} sections")
                for sid in stats['missing_ids'][:5]:
                    log.info(f"    - {sid}")
            
            if stats['orphan_ids']:
                log.info(f"\n[-] Would delete: {stats['orphans_in_chroma']} orphans")
                for sid in stats['orphan_ids'][:5]:
                    log.info(f"    - {sid}")
            
            if stats['missing_from_chroma'] == 0 and stats['orphans_in_chroma'] == 0:
                log.info("\n[OK] Everything in sync!")
            
            return self.EXIT_SUCCESS
            
        except KBConnectionError as e:
            log.error(f"Dry run failed: {e}")
            return self.EXIT_EXECUTION_ERROR
    
    def _cmd_delta(self) -> int:
        """Perform delta synchronization."""
        log = self.get_logger()
        
        self.log_section("ChromaDB Sync - Delta Synchronization")
        
        try:
            with self.get_db() as conn:
                sqlite_data = self._get_sqlite_sections(conn)
                chroma_sections = self._get_chroma_sections()
                
                stats = self._sync_stats(conn)
                missing_ids = list(set(sqlite_data.keys()) - chroma_sections)
                orphans = chroma_sections - set(sqlite_data.keys())
            
            log.info(f"\nPlanned changes:")
            log.info(f"  - Add: {len(missing_ids)}")
            log.info(f"  - Delete orphans: {len(orphans)}")
            
            added = 0
            deleted = 0
            
            if missing_ids:
                log.info(f"\n[1] Adding {len(missing_ids)} missing sections...")
                added = self._embed_missing_sections(missing_ids, self._args.batch_size)
                log.info(f"    -> {added} sections added")
            
            if self._args.delete_orphans and orphans:
                log.info(f"\n[2] Deleting {len(orphans)} orphans...")
                deleted = self._delete_orphans(orphans)
                log.info(f"    -> {deleted} orphans deleted")
            
            log.info("\n[OK] Delta-Sync completed")
            
            return self.EXIT_SUCCESS
            
        except PipelineError as e:
            log.error(f"Delta sync failed: {e}")
            return self.EXIT_EXECUTION_ERROR
    
    def _cmd_file(self, file_id: str) -> int:
        """Sync specific file by ID."""
        log = self.get_logger()
        
        self.log_section(f"ChromaDB Sync - File: {file_id}")
        
        try:
            with self.get_db() as conn:
                cursor = conn.execute("""
                    SELECT id, file_id, file_path, section_header,
                           content_full, content_preview, section_level,
                           importance_score, keywords, file_hash
                    FROM file_sections
                    WHERE file_id = ?
                      AND content_full IS NOT NULL
                      AND content_full != ''
                      AND length(content_full) > 10
                """, (file_id,))
                
                sections = []
                for row in cursor.fetchall():
                    keywords = []
                    try:
                        if row['keywords']:
                            keywords = json.loads(row['keywords'])
                    except json.JSONDecodeError:
                        pass
                    
                    sections.append({
                        'id': str(row['id']),
                        'file_id': str(row['file_id']),
                        'file_path': str(row['file_path']) if row['file_path'] else '',
                        'section_header': row['section_header'] or "",
                        'content_full': row['content_full'] or "",
                        'section_level': row['section_level'] or 0,
                        'importance_score': row['importance_score'] or 0.5,
                        'keywords': keywords,
                        'file_hash': row['file_hash']
                    })
            
            if not sections:
                log.info(f"\n[OK] No sections for file {file_id}")
                return self.EXIT_SUCCESS
            
            log.info(f"\nProcessing {len(sections)} sections...")
            
            # Build texts
            texts = []
            for section in sections:
                header = section['section_header']
                content = section['content_full'][:500]
                keywords = ' '.join(section['keywords'][:10])
                text = f"{header} | {header} | {content} | {keywords}"
                texts.append(text)
            
            # Embed
            embeddings = embed_batch(texts)
            
            # Prepare ChromaDB records
            ids = [s['id'] for s in sections]
            metadatas = []
            documents = []
            
            for idx, section in enumerate(sections):
                content_hash = hashlib.md5(section['content_full'].encode('utf-8')).hexdigest()
                metadatas.append({
                    "file_id": section['file_id'],
                    "file_path": section['file_path'],
                    "section_header": section['section_header'][:200],
                    "section_level": section['section_level'],
                    "importance_score": section['importance_score'],
                    "keywords": json.dumps(section['keywords'][:10]),
                    "file_hash": section['file_hash'],
                    "content_hash": content_hash
                })
                documents.append(texts[idx][:2000])
            
            # Batched upsert to ChromaDB via singleton
            chroma = get_chroma()
            collection = chroma.client.get_or_create_collection(name="kb_sections")
            batched_chroma_upsert(
                collection=collection,
                ids=ids,
                embeddings=embeddings,
                metadatas=metadatas,
                documents=documents,
                batch_size=500,
                desc="ChromaDB file upsert"
            )
            
            log.info(f"\n[OK] {len(sections)} sections embedded")
            
            return self.EXIT_SUCCESS
            
        except PipelineError as e:
            log.error(f"File sync failed: {e}")
            return self.EXIT_EXECUTION_ERROR
    
    def _cmd_full(self) -> int:
        """Full re-sync - delegates to external script."""
        log = self.get_logger()
        
        log.warning("=" * 50)
        log.warning("ChromaDB Sync - Full Re-Sync")
        log.warning("=" * 50)
        log.warning("\n[WARNUNG] Full re-index required!")
        log.info("Use the reembed_all.py script for full re-sync")
        log.info("This command only handles delta operations.")
        
        return self.EXIT_SUCCESS  # Not an error, just informational
    
    def _embed_missing_sections(self, missing_ids: List[str], batch_size: int) -> int:
        """Embed missing sections to ChromaDB via singleton (batched with progress)."""
        if not missing_ids:
            return 0
        
        log = self.get_logger()
        log.info(f"Embedding {len(missing_ids)} missing sections...")
        
        chroma = get_chroma()
        collection = chroma.client.get_or_create_collection(
            name="kb_sections",
            metadata={
                "description": "Knowledge Base Sections Embeddings",
                "embedding_model": self.MODEL_NAME,
                "dimension": 384
            }
        )
        
        processed = 0
        start_time = time.time()
        progress = BatchProgress(
            total=len(missing_ids),
            desc="Embedding missing",
            log_every=max(1, len(missing_ids) // 10)
        )
        
        for batch_ids in batched(missing_ids, batch_size):
            
            placeholders = ','.join('?' * len(batch_ids))
            
            with self.get_db() as conn:
                cursor = conn.execute(
                    """SELECT id, file_id, file_path, section_header,
                           content_full, content_preview, section_level,
                           importance_score, keywords, file_hash
                    FROM file_sections
                    WHERE id IN (""" + placeholders + ")",
                    batch_ids
                )
                
                sections = []
                for row in cursor.fetchall():
                    keywords = []
                    try:
                        if row['keywords']:
                            keywords = json.loads(row['keywords'])
                    except json.JSONDecodeError:
                        pass
                    
                    sections.append({
                        'id': str(row['id']),
                        'file_id': str(row['file_id']),
                        'file_path': str(row['file_path']) if row['file_path'] else '',
                        'section_header': row['section_header'] or "",
                        'content_full': row['content_full'] or "",
                        'section_level': row['section_level'] or 0,
                        'importance_score': row['importance_score'] or 0.5,
                        'keywords': keywords,
                        'file_hash': row['file_hash']
                    })
            
            if not sections:
                continue
            
            # Build texts
            texts = []
            for section in sections:
                header = section['section_header']
                content = section['content_full'][:500]
                keywords = ' '.join(section['keywords'][:10])
                text = f"{header} | {header} | {content} | {keywords}"
                texts.append(text)
            
            # Generate embeddings
            embeddings = embed_batch(texts)
            
            # Prepare ChromaDB records
            ids = [s['id'] for s in sections]
            metadatas = []
            documents = []
            
            for idx, section in enumerate(sections):
                content_hash = hashlib.md5(section['content_full'].encode('utf-8')).hexdigest()
                metadatas.append({
                    "file_id": section['file_id'],
                    "file_path": section['file_path'],
                    "section_header": section['section_header'][:200],
                    "section_level": section['section_level'],
                    "importance_score": section['importance_score'],
                    "keywords": json.dumps(section['keywords'][:10]),
                    "file_hash": section['file_hash'],
                    "content_hash": content_hash
                })
                documents.append(texts[idx][:2000])
            
            # Batched upsert to ChromaDB
            try:
                upsert_result = batched_chroma_upsert(
                    collection=collection,
                    ids=ids,
                    embeddings=embeddings,
                    metadatas=metadatas,
                    documents=documents,
                    batch_size=500,
                    desc="ChromaDB upsert"
                )
                processed += upsert_result.success
                progress.advance(len(batch_ids), failed=upsert_result.failed)
            except PipelineError as exc:
                log.error(f"Upsert batch failed: {exc}")
                progress.advance(len(batch_ids), failed=len(batch_ids))
        
        progress.finish()
        return processed
    
    def _delete_orphans(self, orphan_ids: Set[str]) -> int:
        """Delete orphaned entries from ChromaDB via singleton (batched)."""
        if not orphan_ids:
            return 0
        
        log = self.get_logger()
        log.info(f"Deleting {len(orphan_ids)} orphaned entries...")
        
        try:
            chroma = get_chroma()
            collection = chroma.client.get_collection(name="kb_sections")
            # Batched delete for large orphan sets
            result = batched_chroma_delete(
                collection=collection,
                ids=list(orphan_ids),
                batch_size=1000,
                desc="Deleting orphans"
            )
            log.info(f"Successfully deleted {result.success} orphans")
            if result.failed > 0:
                log.warning(f"Failed to delete {result.failed} orphans")
            return result.success
        except PipelineError as e:
            log.error(f"Failed to delete orphans: {e}")
            return 0
