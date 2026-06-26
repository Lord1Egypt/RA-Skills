"""
Embedding Pipeline for Knowledge Base
======================================

Phase 1: Vector Search Foundation
Batch processing for 996 files / 16,626 sections.

Processes file_sections from knowledge.db and generates
embeddings for ChromaDB vector index.

Source: KB_Erweiterungs_Plan.md (Phase 1)
"""

import sqlite3
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional, Generator, List
from dataclasses import dataclass, asdict
from concurrent.futures import ThreadPoolExecutor
import hashlib

from .chroma_integration import ChromaIntegration, get_chroma
from .text import build_embedding_text
from .batching import batched, BatchProgress, BatchResult, batched_chroma_upsert

from .exceptions import ChromaConnectionError, EmbeddingError
from .paths import get_default_chroma_path
from kb.base.config import KBConfig

logger = logging.getLogger(__name__)


@dataclass
class SectionRecord:
    """Structure for a section to be embedded."""
    id: str           # UUID from file_sections
    file_id: str      # Reference to parent file
    file_path: str    # Full file path
    section_header: str
    content_full: str
    content_preview: str
    section_level: int
    importance_score: float
    keywords: list[str]


@dataclass
class EmbeddingJob:
    """An embedding job with input and output."""
    section_id: str
    text: str
    embedding: Optional[list[float]] = None
    status: str = "pending"  # pending, completed, failed
    error: Optional[str] = None
    processed_at: Optional[str] = None


class EmbeddingPipeline:
    """
    Pipeline for batch embedding of knowledge base sections.

    Responsibility:
    - Reads sections from SQLite (knowledge.db)
    - Generates embeddings (batch processing)
    - Writes to ChromaDB
    - Tracking with cache for incremental updates
    """

    def __init__(
        self,
        db_path: str = None,
        chroma_path: str = None,
        cache_path: str = None,
        batch_size: int = 32,
        max_workers: int = 4
    ):
        """
        Initialize pipeline.

        Args:
            db_path: Path to knowledge.db
            chroma_path: Path for ChromaDB
            cache_path: Path for embedding cache (JSON)
            batch_size: Batch size for embedding
            max_workers: Thread pool workers for parallel processing
        """
        if db_path is None:
            db_path = str(KBConfig.get_instance().db_path)
        self.db_path = Path(db_path).expanduser()
        if chroma_path is None:
            self.chroma_path = get_default_chroma_path()
        else:
            self.chroma_path = Path(chroma_path).expanduser()
        if cache_path is None:
            self.cache_path = KBConfig.get_instance().base_path / "library" / "embeddings" / "cache.json"
        else:
            self.cache_path = Path(cache_path).expanduser()
        self.cache_path.parent.mkdir(parents=True, exist_ok=True)

        self.batch_size = batch_size
        self.max_workers = max_workers

        try:
            self.chroma = get_chroma(chroma_path=str(self.chroma_path))
        except Exception as e:
            self.chroma = None
            self._chroma_error = ChromaConnectionError(f"ChromaDB init failed: {e}")
            self._chroma_error.__cause__ = e
            logger.warning(f"ChromaDB initialization failed, pipeline will run in degraded mode: {e}")
        self._cache: dict = {}  # section_id -> file_hash

        logger.info(f"EmbeddingPipeline init: db={self.db_path}")

    def get_embedding_hash(self, embedding) -> str:
        """Computes SHA256 hash of an embedding vector."""
        import hashlib
        import json
        vec_str = json.dumps(embedding.tolist() if hasattr(embedding, 'tolist') else embedding)
        return hashlib.sha256(vec_str.encode()).hexdigest()

    # -------------------------------------------------------------------------
    # Cache Management
    # -------------------------------------------------------------------------

    def _load_cache(self) -> None:
        """Loads embedding cache from JSON."""
        if self.cache_path.exists():
            try:
                with open(self.cache_path) as f:
                    self._cache = json.load(f)
                logger.info(f"Cache loaded: {len(self._cache)} entries")
            except (json.JSONDecodeError, ValueError) as e:
                logger.warning(f"Could not load cache: {e}")
                self._cache = {}

    def _save_cache(self) -> None:
        """Saves embedding cache as JSON."""
        try:
            self.cache_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.cache_path, 'w') as f:
                json.dump(self._cache, f, indent=2)
            logger.info(f"Cache saved: {len(self._cache)} entries")
        except Exception as e:
            logger.error(f"Could not save cache: {e}")

    def _needs_update(self, section_id: str, file_hash: str) -> bool:
        """Checks if section needs re-embedding."""
        return self._cache.get(section_id) != file_hash

    # -------------------------------------------------------------------------
    # Database Reading
    # -------------------------------------------------------------------------

    def _get_connection(self) -> sqlite3.Connection:
        """Gets SQLite connection with graceful degradation."""
        try:
            return sqlite3.connect(str(self.db_path))
        except sqlite3.OperationalError as e:
            logger.error(f"Cannot open database {self.db_path}: {e}. Pipeline disabled.")
            return None

    def get_sections_for_embedding(
        self,
        limit: Optional[int] = None,
        force_reload: bool = False
    ) -> Generator[SectionRecord, None, None]:
        """
        Yields sections that need embedding.

        Args:
            limit: Optional limit for testing
            force_reload: If True, ignores cache

        Yields:
            SectionRecord for each section to process
        """
        self._load_cache()

        conn = self._get_connection()
        query = """
            SELECT
                id, file_id, file_path, section_header,
                content_full, content_preview, section_level,
                importance_score, keywords, file_hash
            FROM file_sections
            WHERE content_full IS NOT NULL
              AND content_full != ''
              AND length(content_full) > 10
            ORDER BY importance_score DESC, last_indexed ASC
        """

        if limit:
            query += f" LIMIT ?"  # Parameterized query
            cursor = conn.execute(query, (limit,))
        else:
            cursor = conn.execute(query)

        for row in cursor.fetchall():
            (section_id, file_id, file_path, section_header,
             content_full, content_preview, section_level,
             importance_score, keywords_str, file_hash) = row

            # Parse keywords
            try:
                keywords = json.loads(keywords_str) if keywords_str else []
            except (json.JSONDecodeError, ValueError) as e:
                logger.debug(f"Failed to parse keywords JSON for section {section_id}: {e}")
                keywords = []

            # Check cache
            if not force_reload and not self._needs_update(section_id, file_hash):
                continue

            # Build text for embedding
            text = build_embedding_text(
                section_header, content_full, keywords
            )

            yield SectionRecord(
                id=section_id,
                file_id=file_id,
                file_path=file_path,
                section_header=section_header or "",
                content_full=content_full or "",
                content_preview=content_preview or "",
                section_level=section_level or 0,
                importance_score=importance_score or 0.5,
                keywords=keywords
            )

        conn.close()

    def count_pending_sections(self, force_reload: bool = False) -> int:
        """Counts sections that need embedding."""
        count = 0
        for _ in self.get_sections_for_embedding(force_reload=force_reload):
            count += 1
        return count

    # -------------------------------------------------------------------------
    # Embedding Processing
    # -------------------------------------------------------------------------

    def embed(self, sections: list[SectionRecord]) -> list[EmbeddingJob]:
        """
        Processes a batch of sections.

        Args:
            sections: List of SectionRecords

        Returns:
            List of EmbeddingJobs with results
        """
        if self.chroma is None:
            logger.warning("embed() called but ChromaDB is not available, skipping")
            return []

        jobs = []

        # Texte sammeln
        texts = [build_embedding_text(
            s.section_header, s.content_full, s.keywords
        ) for s in sections]

        try:
            # Batch-Embedding
            embeddings = self.chroma.embed_batch(texts, batch_size=self.batch_size)

            for idx, (section, embedding) in enumerate(zip(sections, embeddings)):
                job = EmbeddingJob(
                    section_id=section.id,
                    text=texts[idx],
                    embedding=embedding.tolist() if hasattr(embedding, 'tolist') else embedding,
                    status="completed",
                    processed_at=datetime.now().isoformat()
                )
                jobs.append(job)

        except Exception as e:
            logger.error(f"Batch embedding failed: {e}")
            self._last_embedding_error = EmbeddingError(f"Batch embedding failed: {e}")
            self._last_embedding_error.__cause__ = e
            for section in sections:
                jobs.append(EmbeddingJob(
                    section_id=section.id,
                    text=build_embedding_text(
                        section.section_header, section.content_full, section.keywords
                    ),
                    status="failed",
                    error=str(e)
                ))

        return jobs

    # -------------------------------------------------------------------------
    # ChromaDB Writing
    # -------------------------------------------------------------------------

    def flush(self, jobs, sections, collection_name="kb_sections"):
        """Alias for upsert_to_chroma with graceful degradation."""
        if self.chroma is None:
            logger.warning("flush() called but ChromaDB is not available, skipping")
            return 0
        return self.upsert_to_chroma(jobs, sections, collection_name=collection_name)

    def upsert_to_chroma(
        self,
        jobs: list[EmbeddingJob],
        sections: list[SectionRecord],
        collection_name: str = "kb_sections"
    ) -> int:
        """
        Writes embedding results to ChromaDB.

        Args:
            jobs: EmbeddingJobs with results
            sections: Original SectionRecords
            collection_name: Target collection

        Returns:
            Number of successfully written items
        """
        collection = self.chroma.get_or_create_collection(
            name=collection_name,
            metadata={
                "description": "Knowledge Base Sections Embeddings",
                "source": "embedding_pipeline.py"
            }
        )

        ids = []
        embeddings = []
        metadatas = []
        documents = []

        for job, section in zip(jobs, sections):
            if job.status != "completed" or job.embedding is None:
                continue

            ids.append(job.section_id)
            embeddings.append(job.embedding)
            metadatas.append({
                "file_id": section.file_id,
                "file_path": section.file_path,
                "section_header": section.section_header[:200] if section.section_header else "",
                "section_level": section.section_level,
                "importance_score": section.importance_score,
                "keywords": json.dumps(section.keywords[:10]),
                "processed_at": job.processed_at
            })
            documents.append(job.text[:2000])  # ChromaDB hat 2000 char limit

        successful = len(ids)

        if successful > 0:
            # Batched ChromaDB upsert (splits into chunks of 500)
            upsert_result = batched_chroma_upsert(
                collection=collection,
                ids=ids,
                embeddings=embeddings,
                metadatas=metadatas,
                documents=documents,
                batch_size=500,
                desc="ChromaDB upsert"
            )
            successful = upsert_result.success

            # Track embeddings in SQLite (batch)
            if self.db_path:
                with sqlite3.connect(str(self.db_path)) as track_conn:
                    # Batch-fetch file_ids for all section_ids
                    placeholders = ','.join('?' * len(ids))
                    cur = track_conn.execute(
                        f"SELECT id, file_id FROM file_sections WHERE id IN ({placeholders})",
                        ids
                    )
                    file_id_map = {row[0]: row[1] for row in cur.fetchall()}
                    
                    # Batch-insert tracking rows
                    track_data = [
                        (sid, file_id_map.get(sid), 'all-MiniLM-L6-v2', 384)
                        for sid in ids
                    ]
                    track_conn.executemany("""
                        INSERT OR REPLACE INTO embeddings
                        (section_id, file_id, model, dimension, created_at)
                        VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
                    """, track_data)

            logger.info(f"Upserted {successful} sections to ChromaDB")

        return successful

    # -------------------------------------------------------------------------
    # Main Pipeline Run
    # -------------------------------------------------------------------------

    def run_full(
        self,
        limit: Optional[int] = None,
        force_reload: bool = False,
        collection_name: str = "kb_sections"
    ) -> dict:
        """
        Runs full embedding pipeline (batched with progress tracking).

        Args:
            limit: Optional limit for testing
            force_reload: If True, re-embed despite cache
            collection_name: Collection for output

        Returns:
            Statistics dict with results
        """
        self._load_cache()

        logger.info("=" * 60)
        logger.info("Starting Embedding Pipeline")
        logger.info("=" * 60)

        start_time = datetime.now()

        # Sections sammeln
        logger.info("Collecting sections...")
        sections = list(self.get_sections_for_embedding(
            limit=limit,
            force_reload=force_reload
        ))
        total_sections = len(sections)

        if total_sections == 0:
            logger.info("No sections need embedding (all up to date)")
            return {"status": "up_to_date", "processed": 0}

        logger.info(f"Found {total_sections} sections to embed")

        # Batch-Verarbeitung with progress tracking and error tolerance
        processed = 0
        failed = 0
        progress = BatchProgress(
            total=total_sections,
            desc="Embedding Pipeline",
            log_every=max(1, total_sections // 20)
        )

        for batch_idx, batch in enumerate(batched(sections, self.batch_size)):
            try:
                jobs = self.embed(batch)

                # Update cache
                for job_idx, job in enumerate(jobs):
                    if job.status == "completed":
                        self._cache[job.section_id] = batch[job_idx].content_full[:100]  # pseudo-hash
                    elif job.status == "failed":
                        failed += 1

                # Upsert to ChromaDB (batched internally via upsert_to_chroma)
                success = self.upsert_to_chroma(jobs, batch, collection_name)
                processed += success
                progress.advance(len(batch), failed=len(batch) - success)

            except Exception as exc:
                # Error tolerance: skip failed batch, continue with next
                logger.error(f"Batch {batch_idx + 1} failed: {exc}")
                failed += len(batch)
                progress.advance(len(batch), failed=len(batch))

            # Save cache periodically
            if (batch_idx + 1) % 10 == 0:
                self._save_cache()

        # Final cache save
        self._save_cache()

        progress_stats = progress.finish()
        elapsed = (datetime.now() - start_time).total_seconds()

        num_batches = (total_sections + self.batch_size - 1) // self.batch_size
        stats = {
            "status": "completed",
            "total_sections": total_sections,
            "processed": processed,
            "failed": failed,
            "batches": num_batches,
            "elapsed_seconds": elapsed,
            "sections_per_second": processed / elapsed if elapsed > 0 else 0
        }

        logger.info("=" * 60)
        logger.info("Pipeline Complete!")
        for key, value in stats.items():
            logger.info(f"  {key}: {value}")
        logger.info("=" * 60)

        return stats

    def run_incremental(
        self,
        collection_name: str = "kb_sections"
    ) -> dict:
        """Incremental update (only new/changed sections)."""
        return self.run_full(force_reload=False, collection_name=collection_name)

    def run_full_reload(
        self,
        collection_name: str = "kb_sections"
    ) -> dict:
        """Full reload of all sections."""
        logger.warning("Full reload: clearing cache and re-embedding ALL sections")
        self._cache = {}
        return self.run_full(force_reload=True, collection_name=collection_name)


# =============================================================================
# Main: Pipeline Execution
# =============================================================================

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Embedding Pipeline for KB")
    parser.add_argument("--limit", type=int, default=None, help="Limit for testing")
    parser.add_argument("--reload", action="store_true", help="Full reload")
    parser.add_argument("--stats", action="store_true", help="Statistics only")
    parser.add_argument("--db-path", type=str, default=None)
    parser.add_argument("--chroma-path", type=str, default=None)

    args = parser.parse_args()

    # Resolve default db-path via paths.py if not provided
    if args.db_path is None:
        try:
            from kb.framework.paths import get_default_db_path
            args.db_path = str(get_default_db_path())
        except Exception:
            args.db_path = "library/biblio.db"

    pipeline = EmbeddingPipeline(
        db_path=args.db_path,
        chroma_path=args.chroma_path
    )

    if args.stats:
        print("=" * 60)
        print("Embedding Pipeline Statistics")
        print("=" * 60)

        pending = pipeline.count_pending_sections()
        total = pipeline.count_pending_sections(force_reload=True)

        chroma = get_chroma(chroma_path=args.chroma_path)
        coll_stats = chroma.get_collection_stats("kb_sections")

        print(f"Total Sections in DB: {total}")
        print(f"Sections needing update: {pending}")
        print(f"Already indexed in ChromaDB: {coll_stats['count']}")
        print(f"Cache entries: {len(pipeline._cache)}")

    elif args.reload:
        print("Starting FULL RELOAD...")
        result = pipeline.run_full_reload()
        print(json.dumps(result, indent=2))

    else:
        print("Starting INCREMENTAL update...")
        result = pipeline.run_incremental()
        print(json.dumps(result, indent=2))
