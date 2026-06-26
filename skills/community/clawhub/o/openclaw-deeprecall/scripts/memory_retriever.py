#!/usr/bin/env python3
"""
memory_retriever.py - Token-optimized memory retrieval engine for SQLite-based L1/L2 memory system.
Provides compact-format L1 fact search and exact L2 raw-content retrieval.
"""

import sqlite3
import os
import glob
from pathlib import Path
from typing import List, Optional
from datetime import datetime, timedelta

def get_agent_db_path() -> str:
    """
    Dynamically detect the current agent's database path.
    Priority order:
    1. OPENCLAW_WORKSPACE environment variable
    2. Current directory structure detection (looking for memory/ directory)
    3. Fallback to relative path
    """
    # 1. Check framework environment variable
    workspace = os.environ.get("OPENCLAW_WORKSPACE")
    if workspace:
        potential_path = os.path.join(workspace, "memory", "memory.db")
        if os.path.exists(os.path.dirname(potential_path)):
            return potential_path
    
    # 2. Check current directory structure
    cwd = os.getcwd()
    
    # Check for memory/ subdirectory in current directory
    if os.path.exists(os.path.join(cwd, "memory")):
        return os.path.join(cwd, "memory", "memory.db")
    
    # Check if parent directory is an agents structure
    parent = os.path.dirname(cwd)
    if "agents" in parent or "agents" in cwd:
        # Try to find memory in agents directory structure
        for path in [cwd, parent]:
            memory_dir = os.path.join(path, "memory")
            if os.path.exists(memory_dir):
                return os.path.join(memory_dir, "memory.db")
    
    # 3. Fallback to relative path
    return "./memory/memory.db"

def get_workspace_memory_dir() -> str:
    """
    Get workspace/memory directory path for storing raw .md session files.
    Uses the same priority order as database path detection.
    """
    # 1. Check framework environment variable
    workspace = os.environ.get("OPENCLAW_WORKSPACE")
    if workspace:
        memory_dir = os.path.join(workspace, "memory")
        if os.path.exists(memory_dir) or os.path.exists(os.path.dirname(memory_dir)):
            return memory_dir
    
    # 2. Check current directory structure
    cwd = os.getcwd()
    
    # Check for memory/ subdirectory in current directory
    if os.path.exists(os.path.join(cwd, "memory")):
        return os.path.join(cwd, "memory")
    
    # Check if parent directory is an agents structure
    parent = os.path.dirname(cwd)
    if "agents" in parent or "agents" in cwd:
        # Try to find memory in agents directory structure
        for path in [cwd, parent]:
            memory_dir = os.path.join(path, "memory")
            if os.path.exists(memory_dir):
                return memory_dir
    
    # 3. Fallback to relative path
    return "./memory"

class MemoryRetriever:
    def __init__(self, db_path: str = None):
        """
        Initialize the memory retriever.
        
        Parameters
        ----------
        db_path : str, optional
            Database path. If None, auto-detect.
        """
        if db_path is None:
            self.db_path = get_agent_db_path()
        else:
            self.db_path = db_path
        
        # Ensure database directory exists
        db_dir = os.path.dirname(self.db_path)
        if db_dir:  # Only create directory if path contains a directory component
            os.makedirs(db_dir, exist_ok=True)
        
        # Initialize database tables (self-bootstrapping)
        self._init_db()
    
    def _init_db(self):
        """
        Initialize database tables if they don't exist.
        This ensures zero-config deployment - tables are created automatically.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Create L1 structured facts table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS l1_structured (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    source_file TEXT NOT NULL,
                    fact_type TEXT NOT NULL,
                    confidence REAL,
                    tags TEXT,
                    content_hash TEXT UNIQUE,
                    content TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create L2 raw archive table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS l2_archive (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    source_file TEXT UNIQUE NOT NULL,
                    raw_content TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create processed_files table (replaces .processed marker files)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS processed_files (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    file_path TEXT UNIQUE NOT NULL,
                    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create indexes for faster queries
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_l1_date ON l1_structured(date)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_l1_type ON l1_structured(fact_type)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_l1_source ON l1_structured(source_file)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_l2_source ON l2_archive(source_file)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_processed_path ON processed_files(file_path)')
            
            # Create FTS5 virtual table for full-text search (if FTS5 is available)
            try:
                cursor.execute('''
                    CREATE VIRTUAL TABLE IF NOT EXISTS l1_fts 
                    USING fts5(
                        content, 
                        tags,
                        content=l1_structured,
                        content_rowid=id,
                        tokenize='unicode61'
                    )
                ''')
                # FTS5 virtual table created for semantic search
                
                # Create triggers to keep FTS index in sync with l1_structured table
                cursor.execute('''
                    CREATE TRIGGER IF NOT EXISTS l1_ai AFTER INSERT ON l1_structured BEGIN
                        INSERT INTO l1_fts(rowid, content, tags) 
                        VALUES (new.id, new.content, new.tags);
                    END
                ''')
                cursor.execute('''
                    CREATE TRIGGER IF NOT EXISTS l1_ad AFTER DELETE ON l1_structured BEGIN
                        INSERT INTO l1_fts(l1_fts, rowid, content, tags)
                        VALUES ('delete', old.id, old.content, old.tags);
                    END
                ''')
                cursor.execute('''
                    CREATE TRIGGER IF NOT EXISTS l1_au AFTER UPDATE ON l1_structured BEGIN
                        INSERT INTO l1_fts(l1_fts, rowid, content, tags) 
                        VALUES ('delete', old.id, old.content, old.tags);
                        INSERT INTO l1_fts(rowid, content, tags) 
                        VALUES (new.id, new.content, new.tags);
                    END
                ''')
                
                # Check if l1_structured has data but l1_fts is empty, rebuild index
                cursor.execute('SELECT COUNT(*) FROM l1_structured')
                l1_count = cursor.fetchone()[0]
                cursor.execute('SELECT COUNT(*) FROM l1_fts')
                fts_count = cursor.fetchone()[0]
                
                if l1_count > 0 and fts_count < l1_count:
                    print("FTS5 table is missing some records, rebuilding index...")
                    cursor.execute('INSERT INTO l1_fts(l1_fts) VALUES("rebuild")')
                    # FTS5 index rebuilt
                    
            except sqlite3.OperationalError as e:
                print(f"Note: FTS5 not available, using LIKE-based search: {e}")
            
            conn.commit()
    
    def search_l1_structured(self, query: str = None, limit: int = 5) -> List[str]:
        """
        Retrieve L1 structured facts in a compact, token-optimized format.
        
        Parameters
        ----------
        query : str, optional
            Search string. If None or empty, returns the latest facts.
        limit : int, default 5
            Maximum number of results.
            
        Returns
        -------
        List[str]
            Formatted facts: '[YYYY-MM-DD | fact_type | source:source_file] content...'
            No content truncation is applied.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            if query:
                # Try FTS5 full-text search first, fall back to LIKE if needed
                try:
                    # Check if FTS5 table exists
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='l1_fts'")
                    fts_table_exists = cursor.fetchone() is not None
                    
                    if fts_table_exists:
                        # Convert query to FTS5 MATCH syntax
                        # Support "Vue error OR sandbox failure" syntax
                        or_groups = [kw.strip() for kw in query.split(" OR ") if kw.strip()]
                        fts_conditions = []
                        
                        for group in or_groups:
                            # Escape double quotes in query for FTS5
                            escaped_group = group.replace('"', '""')
                            # For multi-word groups, wrap in quotes for phrase search
                            if ' ' in escaped_group:
                                fts_conditions.append(f'"{escaped_group}"')
                            else:
                                fts_conditions.append(escaped_group)
                        
                        if fts_conditions:
                            fts_query = " OR ".join(fts_conditions)
                            
                            sql = '''
                                SELECT s.date, s.fact_type, s.source_file, s.content
                                FROM l1_fts f
                                JOIN l1_structured s ON f.rowid = s.id
                                WHERE l1_fts MATCH ?
                                ORDER BY rank, s.confidence DESC, s.date DESC
                                LIMIT ?
                            '''
                            cursor.execute(sql, (fts_query, limit))
                            results = cursor.fetchall()
                            # FTS5 query succeeded, proceed to formatting regardless of empty results
                        else:
                            raise sqlite3.OperationalError("No valid FTS5 query")
                    else:
                        raise sqlite3.OperationalError("FTS5 table not found")
                        
                except sqlite3.OperationalError:
                    # FTS5 failed, use LIKE-based search
                    # Original LIKE-based search logic
                    keywords = [kw.strip() for kw in query.split(" OR ") if kw.strip()]
                    conditions = []
                    params = []
                    
                    for kw in keywords:
                        # Split each OR group into individual words (AND semantics within group)
                        sub_keywords = kw.split()
                        group_conditions = []
                        for sub_kw in sub_keywords:
                            if sub_kw:  # Skip empty strings
                                group_conditions.append("(content LIKE ? OR tags LIKE ?)")
                                params.extend([f'%{sub_kw}%', f'%{sub_kw}%'])
                        
                        if group_conditions:
                            # Join AND conditions within group
                            conditions.append("(" + " AND ".join(group_conditions) + ")")
                    
                    if not conditions:
                        # Fallback to simple search if no valid keywords
                        conditions.append("(content LIKE ? OR tags LIKE ?)")
                        params.extend([f'%{query}%', f'%{query}%'])
                    
                    where_clause = " OR ".join(conditions)
                    sql = f'''
                        SELECT date, fact_type, source_file, content 
                        FROM l1_structured 
                        WHERE {where_clause}
                        ORDER BY confidence DESC, date DESC
                        LIMIT ?
                    '''
                    params.append(limit)
                    cursor.execute(sql, params)
                    results = cursor.fetchall()
            else:
                # Retrieve latest records
                sql = '''
                    SELECT date, fact_type, source_file, content
                    FROM l1_structured
                    ORDER BY date DESC, confidence DESC
                    LIMIT ?
                '''
                cursor.execute(sql, (limit,))
                results = cursor.fetchall()
        
        # Format output - extreme compression (no content truncation)
        formatted = []
        for date, fact_type, source_file, content in results:
            # Clean fact_type: only strip prefix for project_ types, preserve other types like user_profile
            if fact_type.startswith("project_"):
                clean_type = "project"
            else:
                clean_type = fact_type
            
            # Compact format: [date | type | source:file] content
            # Note: no truncation is applied; content is returned in full
            line = f"[{date} | {clean_type} | source:{source_file}] {content}"
            formatted.append(line)
        
        return formatted
    
    def get_l2_raw(self, source_file: str) -> Optional[str]:
        """
        Retrieve exact raw content from the L2 archive.
        
        Parameters
        ----------
        source_file : str
            Exact filename as stored in the source_file column.
            
        Returns
        -------
        Optional[str]
            Complete raw Markdown content, or None if the file is not found.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT raw_content FROM l2_archive 
                WHERE source_file = ? 
                LIMIT 1
            ''', (source_file,))
            
            result = cursor.fetchone()
        
        return result[0] if result else None
    
    def get_table_stats(self) -> dict:
        """Return basic statistics about the memory database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('SELECT COUNT(*) FROM l1_structured')
            l1_count = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM l2_archive')
            l2_count = cursor.fetchone()[0]
            
            cursor.execute('SELECT DISTINCT fact_type FROM l1_structured')
            fact_types = [row[0] for row in cursor.fetchall()]
        
        return {
            'l1_structured_count': l1_count,
            'l2_archive_count': l2_count,
            'fact_types': fact_types
        }
    
    def mark_file_as_processed(self, file_path: str) -> bool:
        """
        Mark a file as processed in the database.
        
        Parameters
        ----------
        file_path : str
            Path to the file (relative or absolute)
            
        Returns
        -------
        bool
            True if successful, False otherwise
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    '''
                    INSERT OR REPLACE INTO processed_files 
                    (file_path, processed_at) 
                    VALUES (?, CURRENT_TIMESTAMP)
                    ''',
                    (str(file_path),)
                )
                conn.commit()
            return True
        except Exception as e:
            print(f"Error marking file as processed in database: {e}")
            return False
    
    def is_file_processed(self, file_path: str) -> bool:
        """
        Check if a file has been processed.
        
        Parameters
        ----------
        file_path : str
            Path to the file (relative or absolute)
            
        Returns
        -------
        bool
            True if file is marked as processed
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'SELECT id FROM processed_files WHERE file_path = ?',
                    (str(file_path),)
                )
                result = cursor.fetchone()
            return result is not None
        except Exception as e:
            print(f"Error checking if file is processed: {e}")
            return False
    
    def get_unprocessed_files(self, memory_dir: str) -> List[str]:
        """
        Get list of unprocessed .md files in the memory directory.
        Uses batch query to avoid N+1 database queries.
        
        Parameters
        ----------
        memory_dir : str
            Path to memory directory
            
        Returns
        -------
        List[str]
            List of file paths (relative to memory_dir) that are not processed
        """
        try:
            memory_dir_path = Path(memory_dir)
            # Get all .md files in the directory
            all_md_files = [str(f) for f in memory_dir_path.rglob("*.md")]
            
            if not all_md_files:
                return []
            
            # Batch query to get all processed files in one query
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Create placeholders for SQL IN clause
                placeholders = ",".join(["?" for _ in all_md_files])
                
                cursor.execute(
                    f"SELECT file_path FROM processed_files WHERE file_path IN ({placeholders})",
                    all_md_files
                )
                
                processed_set = {row[0] for row in cursor.fetchall()}
            
            # Return files that are not in the processed set
            unprocessed = [f for f in all_md_files if f not in processed_set]
            return unprocessed
            
        except Exception as e:
            print(f"Error getting unprocessed files: {e}")
            # Fallback to individual queries
            unprocessed = []
            try:
                memory_dir_path = Path(memory_dir)
                for file_path in memory_dir_path.rglob("*.md"):
                    if not self.is_file_processed(str(file_path)):
                        unprocessed.append(str(file_path))
            except Exception as e2:
                print(f"Fallback query also failed: {e2}")
            
            return unprocessed

def cleanup_raw_files(retention_days: int = 1, max_size_kb: int = 250, memory_dir: str = None, dry_run: bool = False) -> dict:
    """
    Clean up raw .md session files, keeping recent data and controlling total size.
    
    Important: This function only cleans raw .md files in workspace/memory/ directory,
    and does NOT affect the permanent L1/L2 data in memory.db database.
    
    Parameters
    ----------
    retention_days : int, default 1
        Keep files newer than N days (based on modification time)
    max_size_kb : int, default 250
        Maximum total file size (KB), delete oldest files if exceeds
    memory_dir : str, optional
        Memory directory path, if None auto-detected
    dry_run : bool, default False
        If True, only calculate files to delete without actually deleting
        
    Returns
    -------
    dict
        Cleanup statistics
    """
    if memory_dir is None:
        memory_dir = get_workspace_memory_dir()
    
    # Ensure directory exists
    if not os.path.exists(memory_dir):
        return {"status": "skipped", "reason": f"Directory not found: {memory_dir}"}
    
    # Get all .md files (excluding memory.db)
    md_files = glob.glob(os.path.join(memory_dir, "*.md"))
    
    if not md_files:
        return {"status": "skipped", "reason": "No .md files found"}
    
    # Sort by modification time (oldest to newest)
    files_with_info = []
    for file_path in md_files:
        try:
            stat = os.stat(file_path)
            files_with_info.append({
                "path": file_path,
                "size_kb": stat.st_size / 1024,
                "mtime": stat.st_mtime,
                "date": datetime.fromtimestamp(stat.st_mtime),
                "filename": os.path.basename(file_path)
            })
        except Exception as e:
            continue
    
    # Sort by modification time (oldest to newest)
    files_with_info.sort(key=lambda x: x["mtime"])
    
    total_size_kb = sum(f["size_kb"] for f in files_with_info)
    total_files = len(files_with_info)
    
    # Calculate cutoff time (keep files from last retention_days)
    cutoff_time = datetime.now() - timedelta(days=retention_days)
    cutoff_timestamp = cutoff_time.timestamp()
    
    # First pass cleanup: time-based
    to_delete_time = []
    kept_files = []
    
    for file_info in files_with_info:
        if file_info["mtime"] < cutoff_timestamp:
            to_delete_time.append(file_info)
        else:
            kept_files.append(file_info)
    
    # Second pass cleanup: size-based (if needed)
    remaining_size_kb = sum(f["size_kb"] for f in kept_files)
    to_delete_size = []
    
    if remaining_size_kb > max_size_kb:
        # Delete oldest files until size limit is met
        kept_files.sort(key=lambda x: x["mtime"])  # Ensure chronological order
        
        while kept_files and remaining_size_kb > max_size_kb:
            oldest_file = kept_files.pop(0)
            to_delete_size.append(oldest_file)
            remaining_size_kb -= oldest_file["size_kb"]
    
    # Combine files to delete
    files_to_delete = to_delete_time + to_delete_size
    
    # Execute deletion (unless dry-run)
    deleted_files = []
    deleted_size_kb = 0
    
    if not dry_run:
        for file_info in files_to_delete:
            try:
                os.remove(file_info["path"])
                deleted_files.append(file_info["path"])
                deleted_size_kb += file_info["size_kb"]
            except Exception as e:
                continue
    else:
        # Dry-run mode: only record files that would be deleted
        deleted_files = [f["path"] for f in files_to_delete]
        deleted_size_kb = sum(f["size_kb"] for f in files_to_delete)
    
    # Clean up orphaned .processed marker files (if any exist from previous version)
    orphaned_markers_deleted = 0
    for marker_path in Path(memory_dir).glob("*.md.processed"):
        # Check if corresponding .md file exists
        source_md = marker_path.with_suffix("")  # Remove .processed suffix
        if not source_md.exists():
            if not dry_run:
                try:
                    marker_path.unlink()
                    orphaned_markers_deleted += 1
                except Exception as e:
                    continue
            else:
                orphaned_markers_deleted += 1
    
    # Return cleanup statistics
    result = {
        "status": "completed" if not dry_run else "dry_run",
        "memory_dir": memory_dir,
        "total_files_before": total_files,
        "total_size_before_kb": round(total_size_kb, 2),
        "deleted_files_count": len(files_to_delete),
        "deleted_size_kb": round(deleted_size_kb, 2),
        "remaining_files_count": len(kept_files),
        "remaining_size_kb": round(remaining_size_kb, 2),
        "deleted_files": [f["filename"] for f in files_to_delete][:10],  # Limit output length
        "orphaned_markers_deleted": orphaned_markers_deleted,
        "config": {
            "retention_days": retention_days,
            "max_size_kb": max_size_kb,
            "dry_run": dry_run
        }
    }
    
    if orphaned_markers_deleted > 0:
        result["reason"] = f"Cleaned {orphaned_markers_deleted} orphaned .processed marker files"
    
    return result

# Singleton retriever instance for OpenClaw tool calls
_retriever_instance = None

def _get_retriever():
    """Get or create singleton MemoryRetriever instance."""
    global _retriever_instance
    if _retriever_instance is None:
        _retriever_instance = MemoryRetriever()
    return _retriever_instance

# Tool functions - for OpenClaw Tool calls
def retrieve_l1_facts(query: str = "", limit: int = 5) -> str:
    """
    Primary entry point for L1 fact retrieval.
    
    Parameters
    ----------
    query : str, default ""
        Search string. Empty string returns the latest facts.
    limit : int, default 5
        Maximum number of results.
        
    Returns
    -------
    str
        Compact formatted facts separated by newlines.
        Format: '[YYYY-MM-DD | fact_type | source:source_file] content...'
        
    Example
    -------
    >>> retrieve_l1_facts("example-project", 2)
    '[2024-01-01 | project | source:example-project.md] example-project backend upgrade...'
    '[2024-01-01 | technical | source:example-project.md] Database model upgrade: Task model adds project_id field...'
    """
    retriever = _get_retriever()
    facts = retriever.search_l1_structured(query, limit)
    
    if not facts:
        return "No matching facts found."
    
    # Convert list to compact text block
    return "\n".join(facts)

def retrieve_l2_raw(source_file: str) -> str:
    """
    Primary entry point for L2 raw-content retrieval.
    
    Parameters
    ----------
    source_file : str
        Exact filename as obtained from an L1 search result.
        
    Returns
    -------
    str
        Complete raw Markdown content of the specified file.
        If the file is not found, returns an error message.
    """
    retriever = _get_retriever()
    content = retriever.get_l2_raw(source_file)
    
    if content is None:
        return f"Source file not found: {source_file}"
    
    return content

# Example usage and testing
if __name__ == "__main__":
    retriever = MemoryRetriever()
    
    print("=== Database Statistics ===")
    stats = retriever.get_table_stats()
    print(f"L1 facts count: {stats['l1_structured_count']}")
    print(f"L2 files count: {stats['l2_archive_count']}")
    print(f"Fact types: {', '.join(stats['fact_types'][:5])}...")
    
    print("\n=== Auto-Detected Paths ===")
    print(f"Database path: {retriever.db_path}")
    print(f"Memory directory: {get_workspace_memory_dir()}")
    
    print("\n=== L1 Retrieval Test (query 'example-project') ===")
    results = retrieve_l1_facts("example-project", 3)
    print(results)
    
    print("\n=== L1 Retrieval Test (latest records) ===")
    results = retrieve_l1_facts(limit=2)
    print(results)
    
    print("\n=== L2 Retrieval Test ===")
    raw = retrieve_l2_raw("example-project-update.md")
    if raw:
        print(f"Raw file size: {len(raw)} characters")
        print("First 200 characters preview:", raw[:200] + "...")
    else:
        print("File not found")
    
    print("\n=== File Cleanup Test (Dry Run) ===")
    cleanup_result = cleanup_raw_files(retention_days=1, max_size_kb=250, dry_run=True)
    print(f"Cleanup status: {cleanup_result.get('status', 'unknown')}")
    print(f"Files to delete: {cleanup_result.get('deleted_files_count', 0)}")
    print(f"Files to keep: {cleanup_result.get('remaining_files_count', 0)}")