"""
ChromaDB Plugin for BiblioIndexer
==================================

Plugin system for automatic ChromaDB integration after indexing.

Uses background queue for non-blocking embedding.

Usage:
    from kb.indexer import BiblioIndexer
    
    
    with BiblioIndexer("knowledge.db", plugins=[ChromaDBPlugin()]) as indexer:
        indexer.index_file(Path("test.md"))
        # -> SQLite + ChromaDB (automatic via plugin)
"""

import json
import logging
import sqlite3
import threading
from pathlib import Path
from typing import List, Optional, Set

# Import shared utility for embedding text building
from .batching import BatchProgress
from dataclasses import dataclass, field

from .embedding_pipeline import SectionRecord
from .exceptions import ChromaConnectionError, PipelineError
from .paths import get_default_chroma_path
from kb.base.config import KBConfig

logger = logging.getLogger(__name__)


@dataclass
class EmbeddingTask:
    """An embedding task to be processed."""
    section_id: str
    file_id: str
    file_path: str
    section_header: str
    content_full: str
    content_preview: str
    section_level: int
    keywords: List[str] = field(default_factory=list)


class ChromaDBPlugin:
    """
    ChromaDB embedding plugin for BiblioIndexer.
    
    Responsibility:
    - Queue manages freshly indexed sections for embedding
    - Background thread for non-blocking processing
    - Batch processing for efficiency
    
    Features:
    - Non-blocking: Indexing not blocked by embedding
    - Batch processing: Sections processed in batches
    - Toggle: can be enabled/disabled
    - Graceful: works even when ChromaDB is unavailable
    """
    
    def __init__(
        self,
        db_path: str = None,
        chroma_path: str = None,
        batch_size: int = 32,
        enabled: bool = True,
        auto_flush: bool = True,
        collection_name: str = "kb_sections"
    ):
        """
        Initialize ChromaDB plugin.
        
        Args:
            db_path: Path to SQLite database
            chroma_path: Path for ChromaDB
            batch_size: Batch size for embedding
            enabled: Whether plugin is active
            auto_flush: Auto flush after index_directory
            collection_name: ChromaDB collection name
        """
        if db_path is None:
            db_path = str(KBConfig.get_instance().db_path)
        self.db_path = Path(db_path).expanduser()
        if chroma_path is None:
            self.chroma_path = get_default_chroma_path()
        else:
            self.chroma_path = Path(chroma_path).expanduser()
        self.batch_size = batch_size
        self.enabled = enabled
        self.auto_flush = auto_flush
        self.collection_name = collection_name
        
        # Queue for background embedding
        self._queue: List[EmbeddingTask] = []
        self._processed_files: Set[str] = set()  # file_ids already queued
        
        # Thread-safety
        self._lock = threading.RLock()
        
        # Background thread
        self._bg_thread: Optional[threading.Thread] = None
        self._bg_running = False
        
        # Lazy-loaded components
        self._chroma = None
        self._pipeline = None
        
        logger.info(f"ChromaDBPlugin init: enabled={enabled}, batch_size={batch_size}")
    
    @property
    def chroma(self):
        """Lazy-load ChromaDB integration (singleton)."""
        if self._chroma is None:
            try:
                from kb.framework.chroma_integration import get_chroma
                self._chroma = get_chroma(chroma_path=str(self.chroma_path))
                logger.info("ChromaDB connection established (singleton)")
            except Exception as e:
                logger.warning(f"ChromaDB not available: {e}")
                self._chroma = None
                self._chroma_error = ChromaConnectionError(f"ChromaDB init failed: {e}")
                self._chroma_error.__cause__ = e
        return self._chroma
    
    @property
    def pipeline(self):
        """Lazy-load EmbeddingPipeline."""
        if self._pipeline is None:
            try:
                from kb.framework.embedding_pipeline import EmbeddingPipeline
                self._pipeline = EmbeddingPipeline(
                    db_path=str(self.db_path),
                    chroma_path=str(self.chroma_path),
                    batch_size=self.batch_size
                )
                logger.info("EmbeddingPipeline initialized")
            except Exception as e:
                logger.warning(f"EmbeddingPipeline not available: {e}")
                self._pipeline = None
                self._pipeline_error = PipelineError(f"Pipeline init failed: {e}")
                self._pipeline_error.__cause__ = e
        return self._pipeline
    
    def on_file_indexed(self, file_path: Path, sections: int, file_id: str) -> None:
        """
        Callback after successful indexing of a file.
        
        Queues all sections of the file for later embedding.
        
        Args:
            file_path: Path to indexed file
            sections: Number of indexed sections
            file_id: UUID of the file in database
        """
        if not self.enabled:
            return
        
        if file_id in self._processed_files:
            logger.debug(f"File {file_id} already queued, skipping")
            return
        
        try:
            # Hole alle section_ids für diese file_id
            with sqlite3.connect(str(self.db_path)) as conn:
                conn.row_factory = sqlite3.Row
                
                rows = conn.execute("""
                    SELECT 
                        id, file_id, file_path, section_header,
                        content_full, content_preview, section_level,
                        keywords
                    FROM file_sections
                    WHERE file_id = ?
                """, (file_id,)).fetchall()
            
            if not rows:
                logger.debug(f"No sections found for file_id {file_id}")
                return
            
            with self._lock:
                for row in rows:
                    # Parse keywords
                    keywords = []
                    if row['keywords']:
                        try:
                            keywords = json.loads(row['keywords'])
                        except (json.JSONDecodeError, ValueError) as e:
                            logger.debug(f"Failed to parse keywords JSON for section {row['id']}: {e}")
                            keywords = []
                    
                    task = EmbeddingTask(
                        section_id=row['id'],
                        file_id=row['file_id'],
                        file_path=row['file_path'],
                        section_header=row['section_header'] or "",
                        content_full=row['content_full'] or "",
                        content_preview=row['content_preview'] or "",
                        section_level=row['section_level'] or 0,
                        keywords=keywords
                    )
                    self._queue.append(task)
                
                self._processed_files.add(file_id)
            
            logger.info(f"Queued {len(rows)} sections for embedding: {file_path.name}")
            
        except (sqlite3.OperationalError, OSError) as e:
            logger.error(f"Error queuing sections for {file_path}: {e}")
    
    def on_file_removed(self, file_path: Path) -> None:
        """
        Callback after removing a file from index.
        
        Removes corresponding entries from ChromaDB.
        
        Args:
            file_path: Path of removed file
        """
        if not self.enabled:
            return
        
        try:
            # Hole alle file_ids für diesen Pfad
            with sqlite3.connect(str(self.db_path)) as conn:
                conn.row_factory = sqlite3.Row
                rows = conn.execute(
                    "SELECT id FROM files WHERE file_path = ?", (str(file_path),)
                ).fetchall()
            
            if not rows:
                logger.debug(f"No file entries found for: {file_path}")
                return
            
            file_ids = [row['id'] for row in rows]
            
            # Lösche aus ChromaDB
            if self.chroma:
                for file_id in file_ids:
                    self.chroma.delete_by_file_id(file_id)
                logger.info(f"ChromaDB entries removed for: {file_path}")
            else:
                logger.warning("ChromaDB not available, orphan entries may remain")
                
        except Exception as e:
            logger.error(f"Error removing ChromaDB entries for {file_path}: {e}")
    
    def on_indexing_complete(self, stats: dict) -> None:
        """
        Optional callback after complete indexing.
        
        Args:
            stats: Statistics dict with 'files' and 'sections' counters
        """
        if not self.enabled:
            return
        
        if self.auto_flush and stats.get('sections', 0) > 0:
            logger.info(f"Indexing complete: {stats['sections']} sections queued")
            # Non-blocking background flush
            self.flush_async()
    
    def flush(self) -> int:
        """
        Processes the queue and writes to ChromaDB.
        
        Delegates embedding and upsert logic to EmbeddingPipeline
        to avoid duplicated implementation.
        
        Blocking method - should not be called in main thread with many items.
        
        Returns:
            Number of processed sections
        """
        if not self.enabled:
            return 0
        
        pipeline = self.pipeline
        if not pipeline:
            logger.warning("EmbeddingPipeline not available, skipping flush")
            return 0
        
        with self._lock:
            if not self._queue:
                logger.debug("Queue empty, nothing to flush")
                return 0
            
            # Copy queue and clear
            tasks = self._queue.copy()
            self._queue.clear()
        
        if not tasks:
            return 0
        
        logger.info(f"Flushing {len(tasks)} sections via EmbeddingPipeline...")
        
        # Convert EmbeddingTask → SectionRecord for pipeline
        sections = []
        for task in tasks:
            sections.append(SectionRecord(
                id=task.section_id,
                file_id=task.file_id,
                file_path=task.file_path,
                section_header=task.section_header,
                content_full=task.content_full,
                content_preview=task.content_preview,
                section_level=task.section_level,
                importance_score=0.5,
                keywords=task.keywords
            ))
        
        processed = 0
        failed = 0
        progress = BatchProgress(
            total=len(sections),
            desc="Plugin flush",
            log_every=max(1, len(sections) // 10)
        )

        # Process in batches via EmbeddingPipeline methods
        for i in range(0, len(sections), self.batch_size):
            batch = sections[i:i + self.batch_size]
            
            try:
                jobs = pipeline.process_batch(batch)
                success = pipeline.upsert_to_chroma(
                    jobs, batch, collection_name=self.collection_name
                )
                processed += success
                failed += len(batch) - success
                progress.advance(len(batch), failed=len(batch) - success)
                logger.info(f"Batch {i // self.batch_size + 1}: {success} sections embedded")
                
            except Exception as e:
                logger.error(f"Batch embedding failed: {e}")
                failed += len(batch)
                progress.advance(len(batch), failed=len(batch))
        
        progress.finish()
        logger.info(f"Flush complete: {processed} processed, {failed} failed")
        return processed
    
    def flush_async(self) -> None:
        """
        Starts background thread for non-blocking flush.
        
        Non-blocking important so indexing is not blocked.
        """
        if self._bg_thread and self._bg_thread.is_alive():
            logger.debug("Background flush already running")
            return
        
        self._bg_running = True
        self._bg_thread = threading.Thread(
            target=self._bg_flush_worker,
            name="ChromaDB-Flush",
            daemon=True
        )
        self._bg_thread.start()
        logger.info("Background flush started")
    
    def _bg_flush_worker(self) -> None:
        """Background worker for flush."""
        try:
            self.flush()
        except Exception as e:
            logger.error(f"Background flush error: {e}")
        finally:
            self._bg_running = False
    
    # _build_embedding_text removed - using shared build_embedding_text from text.py
    
    def get_queue_size(self) -> int:
        """Returns current queue size."""
        with self._lock:
            return len(self._queue)
    
    def clear_queue(self) -> int:
        """
        Clears the queue without processing.
        
        Returns:
            Number of discarded tasks
        """
        with self._lock:
            count = len(self._queue)
            self._queue.clear()
            self._processed_files.clear()
        logger.info(f"Queue cleared: {count} tasks discarded")
        return count
    
    def stop(self) -> None:
        """Stops background thread."""
        self._bg_running = False
        if self._bg_thread:
            self._bg_thread.join(timeout=2.0)
        logger.info("ChromaDBPlugin stopped")
