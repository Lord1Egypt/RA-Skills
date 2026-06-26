#!/usr/bin/env python3
"""
LLMContentManager - Content Management for LLM-Generated Files

Manages essences, reports, and knowledge graph files with:
- Async operations
- YAML frontmatter for metadata
- Integration with KBConnection for metadata tracking
- Markdown output for KB indexing
"""

import asyncio
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, List, Dict, Any

import yaml

from kb.base.config import KBConfig, get_config
from kb.base.db import KBConnection
from kb.biblio.config import LLMConfig, get_llm_config
from kb.base.logger import KBLogger, get_logger

logger = get_logger("kb.llm.content_manager")


class ContentManagerError(Exception):
    """Error in content management operations."""
    pass


class LLMContentManager:
    """
    Manages LLM-generated content: essences, reports, and graph files.
    
    Content is stored as Markdown with YAML frontmatter for easy KB indexing.
    Metadata is also tracked in the database via KBConnection.
    
    Usage:
        manager = LLMContentManager()
        
        # Save essence
        await manager.save_essence(
            title="Machine Learning Basics",
            summary="Key concepts of ML...",
            key_points=["Supervised learning", "..."],
            source_file="/path/to/source.pdf",
            model_used="gemma4:e2b"
        )
        
        # List essences
        essences = await manager.list_essences()
        
        # Get by topic
        essence = await manager.get_essence_by_topic("machine learning")
    """
    
    def __init__(
        self,
        llm_config: Optional[LLMConfig] = None,
        kb_config: Optional[KBConfig] = None
    ):
        self._llm_config = llm_config or get_llm_config()
        self._kb_config = kb_config or get_config()
        self._ensure_directories()
        
        # Ensure LLM dirs exist
        self._llm_config.ensure_dirs()
    
    def _ensure_directories(self) -> None:
        """Ensure all required directories exist."""
        dirs = [
            self._llm_config.essences_path,
            self._llm_config.reports_path,
            self._llm_config.reports_path / "daily",
            self._llm_config.reports_path / "weekly",
            self._llm_config.reports_path / "monthly",
            self._llm_config.graph_path,
            self._llm_config.incoming_path,
        ]
        for d in dirs:
            d.mkdir(parents=True, exist_ok=True)
    
    # --- File Hashing ---
    
    def _compute_file_hash(self, file_path: Path) -> str:
        """Compute SHA256 hash of a file."""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                sha256_hash.update(chunk)
        return f"sha256:{sha256_hash.hexdigest()[:16]}"
    
    # --- Markdown with Frontmatter ---
    
    def _format_frontmatter(self, metadata: Dict[str, Any]) -> str:
        """Format metadata as YAML frontmatter."""
        # Ensure required fields
        if "created_at" not in metadata:
            metadata["created_at"] = datetime.now(timezone.utc).isoformat()
        
        yaml_content = yaml.dump(
            metadata,
            default_flow_style=False,
            sort_keys=False,
            allow_unicode=True
        )
        return f"---\n{yaml_content}---"
    
    def _parse_frontmatter(self, content: str) -> tuple[Dict[str, Any], str]:
        """Parse YAML frontmatter from markdown content.
        
        Returns:
            (metadata dict, markdown body)
        """
        pattern = r"^---\n(.*?)\n---\n?(.*)$"
        match = re.match(pattern, content, re.DOTALL)
        
        if match:
            yaml_str = match.group(1)
            body = match.group(2)
            metadata = yaml.safe_load(yaml_str) or {}
            return metadata, body
        
        return {}, content
    
    # --- Essence Operations ---
    
    async def save_essence(
        self,
        title: str,
        summary: str,
        key_points: List[str],
        content: str,
        *,
        source_file: Optional[Path] = None,
        source_hash: Optional[str] = None,
        entities: Optional[List[str]] = None,
        relationships: Optional[List[Dict[str, str]]] = None,
        keywords: Optional[List[str]] = None,
        model_used: Optional[str] = None,
        tags: Optional[List[str]] = None,
        confidence: float = 0.8,
    ) -> Path:
        """
        Save an essence as Markdown with YAML frontmatter.
        
        Args:
            title: Essence title
            summary: Brief summary
            key_points: List of key points
            content: Full content/analysis
            source_file: Source file path
            source_hash: Pre-computed source hash
            entities: Extracted entities
            relationships: Entity relationships
            keywords: Keywords for search
            model_used: LLM model used
            tags: Custom tags
            confidence: Extraction confidence (0-1)
            
        Returns:
            Path to saved essence file
        """
        # Compute source hash if not provided
        if source_hash is None and source_file:
            source_hash = self._compute_file_hash(source_file)
        
        # Compute essence hash for directory name
        essence_hash = hashlib.sha256(
            f"{title}{summary}{datetime.now().isoformat()}".encode()
        ).hexdigest()[:16]
        
        # Build metadata
        metadata = {
            "version": "1.0",
            "title": title,
            "source_hash": source_hash,
            "source_path": str(source_file) if source_file else None,
            "extracted_at": datetime.now(timezone.utc).isoformat(),
            "model": model_used or self._llm_config.model,
            "type": "essence",
            "tags": tags or [],
            "confidence": confidence,
        }
        
        # Build markdown content
        markdown_body = f"# {title}\n\n## Zusammenfassung\n\n{summary}\n\n## Kernpunkte\n\n"
        for point in key_points:
            markdown_body += f"- {point}\n"
        
        markdown_body += "\n## Detailanalyse\n\n" + content + "\n"
        
        if entities:
            markdown_body += "\n## Entitäten\n\n"
            for entity in entities:
                markdown_body += f"- {entity}\n"
        
        if relationships:
            markdown_body += "\n## Beziehungen\n\n"
            for rel in relationships:
                markdown_body += f"- **{rel.get('from', '?')}** → {rel.get('type', 'related')} → **{rel.get('to', '?')}**\n"
        
        if keywords:
            markdown_body += f"\n## Keywords\n\n{', '.join(keywords)}\n"
        
        markdown_body += f"\n---\n\n*Extracted: {metadata['extracted_at']} | Model: {metadata['model']}*\n"
        
        # Combine frontmatter and body
        full_content = self._format_frontmatter(metadata) + "\n" + markdown_body
        
        # Save to essences/[hash]/essence.md
        essence_dir = self._llm_config.essences_path / essence_hash
        essence_dir.mkdir(parents=True, exist_ok=True)
        
        essence_file = essence_dir / "essence.md"
        essence_file.write_text(full_content, encoding="utf-8")
        
        # Save structured JSON alongside
        json_data = {
            "version": "1.0",
            "source_hash": source_hash,
            "source_path": str(source_file) if source_file else None,
            "extracted_at": metadata["extracted_at"],
            "model": metadata["model"],
            "essence": {
                "title": title,
                "summary": summary,
                "key_points": key_points,
                "entities": entities or [],
                "relationships": relationships or [],
                "keywords": keywords or [],
                "confidence": confidence,
            }
        }
        
        json_file = essence_dir / "essence.json"
        json_file.write_text(json.dumps(json_data, indent=2), encoding="utf-8")
        
        # Track in database
        await self._track_essence(essence_hash, metadata)
        
        logger.info(
            f"Saved essence",
            extra={
                "essence_hash": essence_hash,
                "title": title,
                "path": str(essence_file)
            }
        )
        
        return essence_file
    
    async def list_essences(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        List all stored essences.
        
        Args:
            limit: Maximum number of essences to return
            
        Returns:
            List of essence metadata dicts
        """
        essences = []
        
        for essence_dir in self._llm_config.essences_path.iterdir():
            if not essence_dir.is_dir():
                continue
            
            json_file = essence_dir / "essence.json"
            if json_file.exists():
                try:
                    data = json.loads(json_file.read_text(encoding="utf-8"))
                    essences.append({
                        "hash": essence_dir.name,
                        "path": str(essence_dir / "essence.md"),
                        "title": data.get("essence", {}).get("title", "Untitled"),
                        "extracted_at": data.get("extracted_at"),
                        "model": data.get("model"),
                        "source_hash": data.get("source_hash"),
                    })
                except (json.JSONDecodeError, IOError) as e:
                    logger.warning(f"Failed to read essence {essence_dir.name}: {e}")
                    continue
        
        # Sort by extracted_at descending
        essences.sort(key=lambda x: x.get("extracted_at") or "", reverse=True)
        
        return essences[:limit]
    
    async def get_essence_by_topic(self, topic: str) -> Optional[Dict[str, Any]]:
        """
        Find essence matching or related to topic.
        
        Searches title, keywords, and entities.
        
        Args:
            topic: Topic to search for
            
        Returns:
            Essence data dict or None
        """
        topic_lower = topic.lower()
        
        for essence_dir in self._llm_config.essences_path.iterdir():
            if not essence_dir.is_dir():
                continue
            
            json_file = essence_dir / "essence.json"
            if not json_file.exists():
                continue
            
            try:
                data = json.loads(json_file.read_text(encoding="utf-8"))
                essence = data.get("essence", {})
                
                # Check title
                if topic_lower in essence.get("title", "").lower():
                    return {
                        "hash": essence_dir.name,
                        "path": str(essence_dir / "essence.md"),
                        "title": essence.get("title"),
                        "summary": essence.get("summary"),
                        "key_points": essence.get("key_points", []),
                        "extracted_at": data.get("extracted_at"),
                        "model": data.get("model"),
                        "match_type": "title"
                    }
                
                # Check keywords
                keywords = [k.lower() for k in essence.get("keywords", [])]
                if topic_lower in keywords:
                    return {
                        "hash": essence_dir.name,
                        "path": str(essence_dir / "essence.md"),
                        "title": essence.get("title"),
                        "summary": essence.get("summary"),
                        "key_points": essence.get("key_points", []),
                        "extracted_at": data.get("extracted_at"),
                        "model": data.get("model"),
                        "match_type": "keyword"
                    }
                
                # Check entities
                entities = [e.lower() for e in essence.get("entities", [])]
                if topic_lower in entities:
                    return {
                        "hash": essence_dir.name,
                        "path": str(essence_dir / "essence.md"),
                        "title": essence.get("title"),
                        "summary": essence.get("summary"),
                        "key_points": essence.get("key_points", []),
                        "extracted_at": data.get("extracted_at"),
                        "model": data.get("model"),
                        "match_type": "entity"
                    }
                    
            except (json.JSONDecodeError, IOError) as e:
                logger.warning(f"Failed to read essence {essence_dir.name}: {e}")
                continue
        
        return None
    
    # --- Report Operations ---
    
    async def save_report(
        self,
        title: str,
        content: str,
        query: str,
        *,
        report_type: str = "daily",
        source_hashes: Optional[List[str]] = None,
        model_used: Optional[str] = None,
        related_topics: Optional[List[str]] = None,
        tags: Optional[List[str]] = None,
    ) -> Path:
        """
        Save a report as Markdown with YAML frontmatter.
        
        Args:
            title: Report title
            content: Report content
            query: Original query that generated the report
            report_type: Type of report (daily, weekly, monthly)
            source_hashes: List of essence hashes used as sources
            model_used: LLM model used
            related_topics: Related topic tags
            tags: Custom tags
            
        Returns:
            Path to saved report file
        """
        timestamp = datetime.now(timezone.utc)
        timestamp_str = timestamp.strftime("%Y%m%d_%H%M%S")
        
        # Determine report subdirectory
        report_subdir = self._llm_config.reports_path / report_type
        report_subdir.mkdir(parents=True, exist_ok=True)
        
        # Build metadata
        metadata = {
            "version": "1.0",
            "title": title,
            "report_type": report_type,
            "generated_at": timestamp.isoformat(),
            "query": query,
            "model": model_used or self._llm_config.model,
            "type": "report",
            "sources": source_hashes or [],
            "related_topics": related_topics or [],
            "tags": tags or [],
        }
        
        # Build markdown content
        markdown_body = f"# {title}\n\n> **Abfrage:** {query}\n\n"
        markdown_body += content + "\n\n---\n\n## Quellen\n\n"
        
        if source_hashes:
            for src_hash in source_hashes:
                src_path = self._llm_config.essences_path / src_hash / "essence.md"
                if src_path.exists():
                    markdown_body += f"- [{src_hash}]({src_path})\n"
                else:
                    markdown_body += f"- {src_hash}\n"
        else:
            markdown_body += "- Keine Quellen\n"
        
        markdown_body += f"\n---\n\n*Automatisch generiert: {metadata['generated_at']}*\n"
        
        # Combine frontmatter and body
        full_content = self._format_frontmatter(metadata) + "\n" + markdown_body
        
        # Save to reports/[type]/[timestamp]_report.md
        report_file = report_subdir / f"{timestamp_str}_report.md"
        report_file.write_text(full_content, encoding="utf-8")
        
        # Save metadata JSON alongside
        json_data = {
            "version": "1.0",
            "title": title,
            "report_type": report_type,
            "generated_at": metadata["generated_at"],
            "query": query,
            "model": metadata["model"],
            "sources": source_hashes or [],
        }
        
        json_file = report_subdir / f"{timestamp_str}_metadata.json"
        json_file.write_text(json.dumps(json_data, indent=2), encoding="utf-8")
        
        logger.info(
            f"Saved report",
            extra={
                "report_type": report_type,
                "title": title,
                "path": str(report_file)
            }
        )
        
        return report_file
    
    async def list_reports(
        self,
        report_type: Optional[str] = None,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        List stored reports.
        
        Args:
            report_type: Filter by type (daily, weekly, monthly) or None for all
            limit: Maximum number to return
            
        Returns:
            List of report metadata dicts
        """
        reports = []
        
        # Determine which subdirs to scan
        if report_type:
            search_dirs = [self._llm_config.reports_path / report_type]
        else:
            search_dirs = [
                self._llm_config.reports_path / "daily",
                self._llm_config.reports_path / "weekly",
                self._llm_config.reports_path / "monthly",
            ]
        
        for subdir in search_dirs:
            if not subdir.is_dir():
                continue
            
            for report_file in subdir.glob("*_report.md"):
                try:
                    content = report_file.read_text(encoding="utf-8")
                    metadata, _ = self._parse_frontmatter(content)
                    
                    reports.append({
                        "path": str(report_file),
                        "title": metadata.get("title", "Untitled"),
                        "report_type": metadata.get("report_type", "unknown"),
                        "generated_at": metadata.get("generated_at"),
                        "query": metadata.get("query", ""),
                        "sources_count": len(metadata.get("sources", [])),
                    })
                except (yaml.YAMLError, IOError) as e:
                    logger.warning(f"Failed to read report {report_file.name}: {e}")
                    continue
        
        # Sort by generated_at descending
        reports.sort(key=lambda x: x.get("generated_at") or "", reverse=True)
        
        return reports[:limit]
    
    # --- Database Tracking ---
    
    async def _track_essence(
        self,
        essence_hash: str,
        metadata: Dict[str, Any]
    ) -> None:
        """Track essence in database for searchability."""
        try:
            db_path = self._kb_config.db_path
            
            with KBConnection(db_path) as conn:
                # Check if tracking table exists
                table_exists = conn.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' AND name='llm_essences'"
                ).fetchone()
                
                if not table_exists:
                    conn.execute("""
                        CREATE TABLE IF NOT EXISTS llm_essences (
                            essence_hash TEXT PRIMARY KEY,
                            title TEXT,
                            source_hash TEXT,
                            source_path TEXT,
                            extracted_at TEXT,
                            model TEXT,
                            keywords TEXT,
                            created_at TEXT DEFAULT CURRENT_TIMESTAMP
                        )
                    """)
                    conn.commit()
                
                # Insert or update essence record
                keywords = metadata.get("tags", [])
                keywords_str = ",".join(keywords) if keywords else ""
                
                conn.execute("""
                    INSERT OR REPLACE INTO llm_essences
                    (essence_hash, title, source_hash, source_path, extracted_at, model, keywords)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    essence_hash,
                    metadata.get("title"),
                    metadata.get("source_hash"),
                    metadata.get("source_path"),
                    metadata.get("extracted_at"),
                    metadata.get("model"),
                    keywords_str
                ))
                conn.commit()
                
        except Exception as e:
            logger.warning(f"Failed to track essence in database: {e}")
            # Don't raise - DB tracking is non-critical
    
    # --- Incoming Queue ---
    
    async def add_incoming(self, file_path: Path) -> Path:
        """
        Add a file to the incoming queue for processing.
        
        Args:
            file_path: Path to file to queue
            
        Returns:
            Path to queued file
        """
        incoming_dir = self._llm_config.incoming_path
        incoming_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        filename = file_path.name
        queued_path = incoming_dir / f"{timestamp}_{filename}"
        
        # Copy file to incoming queue
        import shutil
        shutil.copy2(file_path, queued_path)
        
        logger.info(
            f"Added file to incoming queue",
            extra={"original": str(file_path), "queued": str(queued_path)}
        )
        
        return queued_path
    
    async def list_incoming(self) -> List[Dict[str, Any]]:
        """
        List files in incoming queue.
        
        Returns:
            List of queued file info dicts
        """
        incoming_dir = self._llm_config.incoming_path
        
        if not incoming_dir.exists():
            return []
        
        files = []
        for f in incoming_dir.iterdir():
            if f.is_file():
                stat = f.stat()
                files.append({
                    "path": str(f),
                    "name": f.name,
                    "size": stat.st_size,
                    "queued_at": datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat()
                })
        
        return sorted(files, key=lambda x: x["queued_at"])
    
    async def clear_incoming(self, name_filter: Optional[str] = None) -> int:
        """
        Clear files from incoming queue.
        
        Args:
            name_filter: Only clear files matching this string (None = all)
            
        Returns:
            Number of files cleared
        """
        incoming_dir = self._llm_config.incoming_path
        
        if not incoming_dir.exists():
            return 0
        
        count = 0
        for f in incoming_dir.iterdir():
            if f.is_file():
                if name_filter is None or name_filter in f.name:
                    f.unlink()
                    count += 1
        
        logger.info(f"Cleared {count} files from incoming queue")
        return count


# --- Convenience Functions ---

async def save_essence_async(**kwargs) -> Path:
    """Async convenience wrapper for save_essence."""
    manager = LLMContentManager()
    return await manager.save_essence(**kwargs)


async def save_report_async(**kwargs) -> Path:
    """Async convenience wrapper for save_report."""
    manager = LLMContentManager()
    return await manager.save_report(**kwargs)


async def list_essences_async(limit: int = 100) -> List[Dict[str, Any]]:
    """Async convenience wrapper for list_essences."""
    manager = LLMContentManager()
    return await manager.list_essences(limit=limit)


async def get_essence_by_topic_async(topic: str) -> Optional[Dict[str, Any]]:
    """Async convenience wrapper for get_essence_by_topic."""
    manager = LLMContentManager()
    return await manager.get_essence_by_topic(topic)