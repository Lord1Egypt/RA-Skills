"""
PostgreSQL Memory System v2.7.0 — Multi-Instance Support
Features: observations, summaries, chains, templates, conflict detection, reminders, 
bulk import, multi-instance tracking, auto-generated instance IDs
"""
import os
import re
import sys
import json
import time
import uuid
import hashlib
import threading
import platform
from pathlib import Path
from decimal import Decimal
from functools import wraps
from contextlib import contextmanager
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any, Union
from dataclasses import dataclass
from collections import deque

import psycopg2
from psycopg2 import pool
from psycopg2.extras import RealDictCursor, Json

# ============================================================================
# MULTI-INSTANCE CONFIGURATION
# ============================================================================

def get_config_directory() -> Path:
    """Get platform-appropriate config directory."""
    system = platform.system()
    if system == "Darwin":  # macOS
        return Path.home() / "Library" / "Application Support" / "pg-memory"
    elif system == "Windows":
        return Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming")) / "pg-memory"
    else:  # Linux and others
        xdg_config = os.environ.get("XDG_CONFIG_HOME")
        if xdg_config:
            return Path(xdg_config) / "pg-memory"
        return Path.home() / ".config" / "pg-memory"

def load_config_from_file() -> Dict[str, str]:
    """Load configuration from file if it exists."""
    config = {}
    config_dir = get_config_directory()
    config_file = config_dir / "config.env"
    
    if config_file.exists():
        with open(config_file) as f:
            for line in f:
                line = line.strip()
                if line and '=' in line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    config[key] = value
    
    return config

def get_or_create_instance_id() -> str:
    """Get or generate unique instance ID for this machine."""
    config_dir = get_config_directory()
    config_dir.mkdir(parents=True, exist_ok=True)
    
    instance_file = config_dir / "instance.json"
    
    if instance_file.exists():
        try:
            with open(instance_file) as f:
                data = json.load(f)
                return data['instance_id']
        except (json.JSONDecodeError, KeyError):
            pass  # Regenerate if corrupted
    
    # Generate new UUID
    instance_id = str(uuid.uuid4())
    data = {
        "instance_id": instance_id,
        "created_at": datetime.now().isoformat(),
        "platform": platform.system(),
        "hostname": platform.node()
    }
    
    with open(instance_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    return instance_id

# Load config from file (overrides will happen in MemoryConfig)
_config_file = load_config_from_file()
for key, value in _config_file.items():
    os.environ.setdefault(key, value)

# ============================================================================
# CONFIGURATION
# ============================================================================

@dataclass
class MemoryConfig:
    """Configuration with environment override support and file-based config."""
    db_name: str = os.getenv("PG_MEMORY_DB", _config_file.get("PG_MEMORY_DB", "openclaw_memory"))
    db_user: str = os.getenv("PG_MEMORY_USER", _config_file.get("PG_MEMORY_USER", os.getenv("USER", "postgres")))
    db_host: str = os.getenv("PG_MEMORY_HOST", _config_file.get("PG_MEMORY_HOST", "localhost"))
    db_port: int = int(os.getenv("PG_MEMORY_PORT", _config_file.get("PG_MEMORY_PORT", "5432")))
    db_password: str = os.getenv("PG_MEMORY_PASSWORD", _config_file.get("PG_MEMORY_PASSWORD", ""))
    
    # Instance identification (v2.7.0)
    instance_id: str = get_or_create_instance_id()
    agent_label: str = os.getenv("OPENCLAW_NAME", _config_file.get("OPENCLAW_NAME", "unknown"))
    
    # Security limits
    max_content_length: int = int(os.getenv("PG_MEMORY_MAX_CONTENT", "100000"))  # 100KB
    max_tags: int = int(os.getenv("PG_MEMORY_MAX_TAGS", "20"))
    max_tag_length: int = int(os.getenv("PG_MEMORY_MAX_TAG_LENGTH", "50"))
    rate_limit_window: int = int(os.getenv("PG_MEMORY_RATE_WINDOW", "60"))  # seconds
    rate_limit_max: int = int(os.getenv("PG_MEMORY_RATE_LIMIT", "100"))  # per window
    
    # Performance
    pool_min: int = int(os.getenv("PG_MEMORY_POOL_MIN", "2"))
    pool_max: int = int(os.getenv("PG_MEMORY_POOL_MAX", "10"))
    query_timeout: int = int(os.getenv("PG_MEMORY_TIMEOUT", "30"))  # seconds
    
    # Caching
    cache_size: int = int(os.getenv("PG_MEMORY_CACHE_SIZE", "100"))
    cache_ttl: int = int(os.getenv("PG_MEMORY_CACHE_TTL", "300"))  # 5 minutes


# ============================================================================
# INPUT VALIDATION
# ============================================================================

class ValidationError(Exception):
    """Raised when input validation fails."""
    pass


class RateLimitError(Exception):
    """Raised when rate limit exceeded."""
    pass


class DuplicateObservationError(Exception):
    """Raised when duplicate observation detected with check_duplicates=True."""
    def __init__(self, message, duplicates=None):
        super().__init__(message)
        self.duplicates = duplicates or []


def validate_content(content: str, max_length: int = 100000) -> str:
    """Validate and sanitize content."""
    if not isinstance(content, str):
        raise ValidationError("Content must be a string")
    
    if not content.strip():
        raise ValidationError("Content cannot be empty")
    
    if len(content) > max_length:
        raise ValidationError(f"Content exceeds max length of {max_length} characters")
    
    # Sanitize: remove null bytes and control chars
    content = content.replace('\x00', '')
    content = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', content)
    
    return content.strip()


def validate_tags(tags: Optional[List[str]], max_tags: int = 20, max_length: int = 50) -> Optional[List[str]]:
    """Validate tags."""
    if tags is None:
        return None
    
    if not isinstance(tags, list):
        raise ValidationError("Tags must be a list")
    
    if len(tags) > max_tags:
        raise ValidationError(f"Too many tags: max {max_tags}")
    
    validated = []
    for tag in tags:
        if not isinstance(tag, str):
            raise ValidationError(f"Tag must be a string: {tag}")
        if len(tag) > max_length:
            raise ValidationError(f"Tag too long: max {max_length} chars")
        # Santize: alphanumeric + underscore + hyphen only
        tag = re.sub(r'[^\w\-]', '_', tag.lower().strip())
        if tag and tag not in validated:
            validated.append(tag)
    
    return validated if validated else None


def validate_importance(score: float) -> float:
    """Validate importance score."""
    if not isinstance(score, (int, float)):
        raise ValidationError("Importance must be numeric")
    return max(0.0, min(1.0, float(score)))


def validate_filepath(filepath: str, allowed_base: Optional[str] = None) -> str:
    """Validate filepath to prevent directory traversal attacks.
    
    Args:
        filepath: The requested file path
        allowed_base: Optional base directory that must contain the file
    
    Returns:
        Absolute, validated path
    
    Raises:
        ValidationError: If path is invalid or outside allowed_base
    """
    if not isinstance(filepath, str):
        raise ValidationError("Filepath must be a string")
    
    # Normalize the path
    filepath = filepath.strip()
    if not filepath:
        raise ValidationError("Filepath cannot be empty")
    
    # Reject paths with traversal patterns
    dangerous_patterns = ['..', '~', '$', '\x00', '|', ';', '&', '`']
    for pattern in dangerous_patterns:
        if pattern in filepath:
            raise ValidationError(f"Invalid characters in filepath: {repr(pattern)}")
    
    # Get absolute path
    abs_path = os.path.abspath(filepath)
    
    # Check allowed base directory
    if allowed_base is not None:
        allowed_abs = os.path.abspath(allowed_base)
        if not abs_path.startswith(allowed_abs + os.sep) and abs_path != allowed_abs:
            raise ValidationError(
                f"Path must be within {allowed_base}, got: {filepath}"
            )
    
    # Ensure parent directory exists
    parent_dir = os.path.dirname(abs_path)
    if not os.path.exists(parent_dir):
        try:
            os.makedirs(parent_dir, exist_ok=True)
        except OSError as e:
            raise ValidationError(f"Cannot create directory: {e}")
    
    # Check if file already exists and is not a regular file
    if os.path.exists(abs_path) and not os.path.isfile(abs_path):
        raise ValidationError(f"Path exists and is not a regular file: {filepath}")
    
    return abs_path


# ============================================================================
# RATE LIMITING
# ============================================================================

class RateLimiter:
    """Simple in-memory rate limiter per user/process."""
    
    def __init__(self, max_calls: int = 100, window: int = 60):
        self.max_calls = max_calls
        self.window = window
        self._calls: deque = deque()
        self._lock = threading.Lock()
    
    def check(self) -> bool:
        """Check if allowed to proceed."""
        with self._lock:
            now = time.time()
            # Remove old calls outside window
            while self._calls and self._calls[0] < now - self.window:
                self._calls.popleft()
            
            if len(self._calls) >= self.max_calls:
                return False
            
            self._calls.append(now)
            return True
    
    def get_remaining(self) -> int:
        """Get remaining calls in current window."""
        with self._lock:
            now = time.time()
            while self._calls and self._calls[0] < now - self.window:
                self._calls.popleft()
            return max(0, self.max_calls - len(self._calls))


# ============================================================================
# SIMPLE CACHE
# ============================================================================

class MemoryCache:
    """LRU cache with TTL."""
    
    def __init__(self, max_size: int = 100, ttl: int = 300):
        self.max_size = max_size
        self.ttl = ttl
        self._cache: Dict[str, Dict] = {}
        self._access_times: deque = deque(maxlen=max_size)
        self._lock = threading.Lock()
    
    def _make_key(self, *args) -> str:
        """Create cache key from args."""
        return hashlib.md5(json.dumps(args, sort_keys=True).encode()).hexdigest()
    
    def get(self, *args) -> Optional[Any]:
        """Get from cache if exists and not expired."""
        key = self._make_key(*args)
        with self._lock:
            if key in self._cache:
                entry = self._cache[key]
                if time.time() - entry['time'] < self.ttl:
                    return entry['value']
                else:
                    del self._cache[key]
            return None
    
    def set(self, value: Any, *args) -> None:
        """Set cache value."""
        key = self._make_key(*args)
        with self._lock:
            # Evict oldest if at capacity
            if len(self._cache) >= self.max_size and key not in self._cache:
                oldest = next(iter(self._cache))
                del self._cache[oldest]
            
            self._cache[key] = {
                'value': value,
                'time': time.time()
            }
    
    def clear(self) -> None:
        """Clear cache."""
        with self._lock:
            self._cache.clear()


# ============================================================================
# MAIN CLASS
# ============================================================================

class PostgresMemory:
    """Optimized PostgreSQL-based memory system."""
    
    _instance: Optional['PostgresMemory'] = None
    _instance_lock = threading.Lock()
    
    def __new__(cls, config: Optional[MemoryConfig] = None):
        """Singleton pattern for connection pool sharing."""
        if cls._instance is None:
            with cls._instance_lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self, config: Optional[MemoryConfig] = None):
        if self._initialized:
            return
        
        self.config = config or MemoryConfig()
        self._pool: Optional[pool.ThreadedConnectionPool] = None
        self._pgvector_available = False
        self._rate_limiter = RateLimiter(
            self.config.rate_limit_max,
            self.config.rate_limit_window
        )
        self._cache = MemoryCache(
            self.config.cache_size,
            self.config.cache_ttl
        )
        
        # Expose instance tracking (v2.7.0)
        self.instance_id = self.config.instance_id
        self.agent_label = self.config.agent_label
        
        self._init_pool()
        self._check_pgvector()
        self._initialized = True
        
        print(f"✓ PostgresMemory initialized ({self.agent_label}:{self.instance_id[:8]}")
    
    def _init_pool(self) -> None:
        """Initialize connection pool."""
        try:
            conn_params = {
                'dbname': self.config.db_name,
                'user': self.config.db_user,
                'host': self.config.db_host,
                'port': self.config.db_port,
                'connect_timeout': self.config.query_timeout,
            }
            
            if self.config.db_password:
                conn_params['password'] = self.config.db_password
            
            self._pool = pool.ThreadedConnectionPool(
                self.config.pool_min,
                self.config.pool_max,
                **conn_params
            )
        except Exception as e:
            raise RuntimeError(f"Failed to initialize connection pool: {e}")
    
    def _check_pgvector(self) -> None:
        """Check if pgvector extension is available (cached)."""
        try:
            with self._get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT EXISTS(SELECT 1 FROM pg_extension 
                        WHERE extname = 'vector')
                    """)
                    self._pgvector_available = cur.fetchone()[0]
        except Exception:
            self._pgvector_available = False
    
    @contextmanager
    def _get_connection(self):
        """Get connection from pool."""
        if not self._pool:
            raise RuntimeError("Connection pool not initialized")
        
        conn = None
        try:
            conn = self._pool.getconn()
            yield conn
        finally:
            if conn:
                self._pool.putconn(conn)
    
    # ========================================================================
    # PUBLIC API — WITH RATE LIMITING & VALIDATION
    # ========================================================================
    
    def capture_observation(
        self,
        content: str,
        session_id: Optional[str] = None,
        source: str = "manual",
        content_type: str = "text",
        embedding: Optional[List[float]] = None,
        metadata: Optional[Dict] = None,
        tags: Optional[List[str]] = None,
        importance_score: float = 0.5,
        derived_from_exchange_ids: Optional[List[str]] = None,
        related_files: Optional[List[str]] = None,
        related_urls: Optional[List[str]] = None,
        check_duplicates: bool = False,
        duplicate_threshold: float = 0.85
    ) -> int:
        """Capture an observation with validation and rate limiting.

        Args:
            content: The observation text
            session_id: Link to conversation session
            source: Who/what created this (e.g., 'arty', 'user', 'system')
            content_type: Type of content ('text', 'decision', 'error', etc.)
            embedding: Optional vector embedding for semantic search
            metadata: Additional structured data
            tags: Category labels
            importance_score: 0.0-1.0 priority score
            derived_from_exchange_ids: UUIDs of chat messages that led to this
            related_files: File paths related to this observation
            related_urls: URLs referenced

        Returns:
            Observation ID

        Raises:
            DuplicateObservationError: If check_duplicates=True and similar content found
        """
        # Rate limiting
        if not self._rate_limiter.check():
            raise RateLimitError(
                f"Rate limit exceeded. Try again in {self.config.rate_limit_window}s"
            )

        # Input validation
        content = validate_content(content, self.config.max_content_length)
        tags = validate_tags(tags, self.config.max_tags, self.config.max_tag_length)
        importance_score = validate_importance(importance_score)

        # Duplicate detection
        if check_duplicates:
            duplicates = self.find_similar(
                content=content,
                min_similarity=duplicate_threshold,
                limit=5
            )
            if duplicates:
                raise DuplicateObservationError(
                    f"Found {len(duplicates)} similar observations. Use force=True to capture anyway.",
                    duplicates=duplicates
                )

        # Sanitize metadata
        if metadata is not None:
            metadata = {k: v for k, v in metadata.items()
                       if isinstance(k, str) and len(k) < 100}

        # Validate UUIDs in exchange_ids
        if derived_from_exchange_ids:
            derived_from_exchange_ids = [
                eid[:64] for eid in derived_from_exchange_ids
                if isinstance(eid, str) and len(eid) > 0
            ][:50]  # Max 50 exchange IDs

        # Validate related files
        if related_files:
            related_files = [
                f[:500] for f in related_files
                if isinstance(f, str) and len(f) < 500
            ][:20]  # Max 20 files

        # Validate related URLs
        if related_urls:
            related_urls = [
                u[:1000] for u in related_urls
                if isinstance(u, str) and len(u) < 1000
            ][:10]  # Max 10 URLs

        # Insert with retries
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute("""
                        INSERT INTO observations
                        (session_id, source, content, content_type,
                         embedding, metadata, tags, importance_score,
                         derived_from_exchange_ids, related_files, related_urls,
                         derived_from_raw, instance_id, agent_label)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        RETURNING id, timestamp
                    """, (
                        session_id[:64] if session_id else None,
                        source[:50],
                        content,
                        content_type[:50],
                        Json(embedding) if embedding else None,
                        Json(metadata) if metadata else None,
                        tags,
                        importance_score,
                        derived_from_exchange_ids,
                        related_files,
                        related_urls,
                        bool(derived_from_exchange_ids),  # True if linked to exchanges
                        self.instance_id[:36] if self.instance_id else None,  # v2.7.0
                        self.agent_label[:100] if self.agent_label else None   # v2.7.0
                    ))
                    result = cur.fetchone()
                    conn.commit()

                    # Invalidate cache
                    self._cache.clear()

                    return result[0]

                except Exception as e:
                    conn.rollback()
                    raise RuntimeError(f"Failed to capture observation: {e}")
    
    def find_similar(
        self,
        content: str,
        min_similarity: float = 0.85,
        limit: int = 5
    ) -> List[Dict]:
        """Find observations with similar content using full-text search.

        Args:
            content: Content to check for similarity
            min_similarity: Minimum similarity threshold (0.0-1.0)
            limit: Maximum number of results to return

        Returns:
            List of similar observations with similarity scores
        """
        # Use PostgreSQL full-text search for fast similarity check
        from psycopg2.extras import RealDictCursor
        
        with self._get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                # Get ts_rank for similarity scoring
                cur.execute("""
                    SELECT 
                        id,
                        content,
                        source,
                        updated_at,
                        ts_rank(
                            to_tsvector('english', content), 
                            plainto_tsquery('english', %s)
                        ) as similarity
                    FROM observations
                    WHERE to_tsvector('english', content) @@ plainto_tsquery('english', %s)
                    ORDER BY similarity DESC
                    LIMIT %s
                """, (content, content, limit))
                
                results = []
                for row in cur.fetchall():
                    if row['similarity'] >= min_similarity:
                        results.append(dict(row))
                
                return results
    
    def suggest_tags(self, content: str, limit: int = 5) -> List[str]:
        """Suggest tags based on content using existing tag frequency.
        
        Analyzes content and existing observations to suggest relevant tags.
        
        Args:
            content: Content to analyze for tag suggestions
            limit: Maximum number of suggestions to return
            
        Returns:
            List of suggested tags sorted by relevance
        """
        # Extract keywords from content (simple approach)
        import re
        content_lower = content.lower()
        
        # Common tech/entertainment keywords to check for
        keyword_mapping = {
            'streaming': ['netflix', 'hbo', 'disney', 'paramount', 'warner', 'hulu', 'amazon'],
            'ai': ['ai', 'artificial intelligence', 'machine learning', 'gpt', 'llm', 'chatgpt', 'openai'],
            'merger': ['merger', 'acquisition', 'billion', 'deal', 'warner', 'paramount', 'discovery'],
            'movies': ['movie', 'film', 'cinema', 'theater', 'box office', 'scream', 'matrix'],
            'gaming': ['game', 'gaming', 'esports', 'steam', 'playstation', 'xbox', 'nintendo'],
            'tech': ['tech', 'technology', 'software', 'app', 'samsung', 'apple', 'microsoft'],
            'newsletter': ['newsletter', 'subscriber', 'email', 'issue'],
            'trends': ['trend', 'viral', 'trending', 'popular', 'buzz'],
            'content': ['content', 'creator', 'create', 'produce', 'media'],
            'business': ['business', 'corporate', 'strategy', 'revenue', 'profit', 'market']
        }
        
        suggested = []
        for tag, keywords in keyword_mapping.items():
            if any(kw in content_lower for kw in keywords):
                suggested.append(tag)
                if len(suggested) >= limit:
                    break
        
        # Also check existing popular tags in database
        from psycopg2.extras import RealDictCursor
        with self._get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                # Get most common tags that might match
                cur.execute("""
                    SELECT DISTINCT unnest(tags) as tag, COUNT(*) as freq
                    FROM observations
                    GROUP BY tag
                    ORDER BY freq DESC
                    LIMIT 20
                """)
                
                for row in cur.fetchall():
                    tag = row['tag']
                    if tag not in suggested and len(suggested) < limit:
                        # Check if tag words appear in content
                        tag_words = tag.lower().split('_') if '_' in tag else [tag.lower()]
                        if any(word in content_lower for word in tag_words):
                            suggested.append(tag)
        
        return suggested[:limit]
    
    def suggest_tags_from_existing(self, partial_tag: str = "", limit: int = 10) -> List[str]:
        """Autocomplete tags from existing observations.
        
        Provides tag suggestions for autocomplete UI.
        
        Args:
            partial_tag: Partial tag text to match (e.g., 'tech' matches 'technology', 'tech-stack')
            limit: Maximum suggestions to return
            
        Returns:
            List of existing tags matching the partial string
        """
        from psycopg2.extras import RealDictCursor
        
        with self._get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                if partial_tag:
                    # Search for tags containing partial_tag
                    cur.execute("""
                        SELECT DISTINCT unnest(tags) as tag, COUNT(*) as freq
                        FROM observations
                        WHERE EXISTS (
                            SELECT 1 FROM unnest(tags) t 
                            WHERE t ILIKE %s
                        )
                        GROUP BY tag
                        ORDER BY freq DESC
                        LIMIT %s
                    """, (f'%{partial_tag}%', limit))
                else:
                    # Get most popular tags
                    cur.execute("""
                        SELECT DISTINCT unnest(tags) as tag, COUNT(*) as freq
                        FROM observations
                        GROUP BY tag
                        ORDER BY freq DESC
                        LIMIT %s
                    """, (limit,))
                
                return [row['tag'] for row in cur.fetchall()]
    
    # ============================================================================
    # OBSERVATION PROTOCOL — Auto-creation for Projects/Tasks
    # ============================================================================
    
    def check_observation_exists(
        self,
        project_name: str,
        session_id: Optional[str] = None
    ) -> bool:
        """Check if observation exists for project/task.
        
        Observation Protocol: "All new projects or tasks assigned should have 
        an observation created if one does not exist."
        """
        tags = [f"project:{project_name}"]
        
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT EXISTS(
                        SELECT 1 FROM observations 
                        WHERE tags && %s
                        AND content_type = 'observation'
                        AND timestamp > NOW() - INTERVAL '30 days'
                    )
                """, (tags,))
                return cur.fetchone()[0]
    
    def ensure_observation_exists(
        self,
        project_name: str,
        project_location: str,
        assigned_by: Optional[str] = None,
        key_details: Optional[str] = None,
        next_steps: Optional[str] = None,
        session_id: Optional[str] = None
    ) -> Dict:
        """Ensure observation exists for project/task. Creates if missing.
        
        Observation Protocol — CRITICAL
        Priority: ⛔ REMEMBER FOREVER
        Directive: "All new projects or tasks assigned should have an 
        observation created if one does not exist."
        
        This overrides passive behavior. When in doubt, WRITE IT DOWN.
        """
        # Check if observation already exists
        if self.check_observation_exists(project_name, session_id):
            # Find and return existing observation
            with self._get_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    cur.execute("""
                        SELECT id, session_id, timestamp, source, content,
                               content_type, metadata, tags, importance_score
                        FROM observations 
                        WHERE tags @> ARRAY[%s]
                        AND content_type = 'observation'
                        ORDER BY timestamp DESC
                        LIMIT 1
                    """, (f"project:{project_name}",))
                    result = cur.fetchone()
                    if result:
                        return {**dict(result), "was_created": False}
            return {"was_created": False, "message": "Observation already exists"}
        
        # Create observation using template
        content = f"""## {project_name}
**Assigned**: {datetime.now().strftime('%Y-%m-%d %H:%M')} EST
**Status**: Active
**Location**: {project_location}
**Key Details**: {key_details or 'To be determined'}
**Next Steps**: {next_steps or 'To be determined'}

*Observation created per protocol*"""
        
        tags = [
            f"project:{project_name}",
            "observation",
            "assigned",
            "active"
        ]
        
        if assigned_by:
            tags.append(f"assigned_by:{assigned_by}")
        
        # Capture with high importance
        observation_id = self.capture_observation(
            content=content,
            session_id=session_id,
            source="observation_protocol",
            content_type="observation",
            metadata={
                "project_name": project_name,
                "project_location": project_location,
                "assigned_by": assigned_by,
                "protocol_version": "2.0",
                "protocol_date": "2026-02-27"
            },
            tags=tags,
            importance_score=0.9  # High importance for new assignments
        )
        
        return {
            "id": observation_id,
            "project_name": project_name,
            "was_created": True,
            "timestamp": datetime.now().isoformat(),
            "message": f"Observation created per protocol for '{project_name}'"
        }
    
    def auto_capture_project(
        self,
        task_description: str,
        **kwargs
    ) -> Dict:
        """Auto-capture new project/task with observation protocol.
        
        Convenience wrapper that extracts project name and ensures
        observation exists before proceeding.
        """
        # Extract project name from task description
        lines = task_description.strip().split('\n')
        project_name = lines[0][:100]  # First line, max 100 chars
        key_details = '\n'.join(lines[1:]) if len(lines) > 1 else None
        
        # Ensure observation exists
        return self.ensure_observation_exists(
            project_name=project_name,
            project_location=kwargs.get('project_location', 'unknown'),
            assigned_by=kwargs.get('assigned_by'),
            key_details=key_details,
            next_steps=kwargs.get('next_steps'),
            session_id=kwargs.get('session_id')
        )
    
    def capture_batch(
        self,
        observations: List[Dict]
    ) -> List[int]:
        """Capture multiple observations in a single transaction (much faster)."""
        if not observations:
            return []
        
        if not self._rate_limiter.check():
            raise RateLimitError("Rate limit exceeded")
        
        if len(observations) > 100:
            raise ValidationError("Batch size limited to 100 observations")
        
        ids = []
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                try:
                    for obs in observations:
                        content = validate_content(
                            obs['content'], 
                            self.config.max_content_length
                        )
                        tags = validate_tags(
                            obs.get('tags'),
                            self.config.max_tags,
                            self.config.max_tag_length
                        )
                        
                        cur.execute("""
                            INSERT INTO observations 
                            (session_id, source, content, content_type,
                             embedding, metadata, tags, importance_score)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                            RETURNING id
                        """, (
                            obs.get('session_id', '')[:64],
                            obs.get('source', 'batch')[:50],
                            content,
                            obs.get('content_type', 'text')[:50],
                            Json(obs.get('embedding')),
                            Json(obs.get('metadata')),
                            tags,
                            validate_importance(obs.get('importance_score', 0.5))
                        ))
                        ids.append(cur.fetchone()[0])
                    
                    conn.commit()
                    self._cache.clear()
                    return ids
                    
                except Exception as e:
                    conn.rollback()
                    raise RuntimeError(f"Failed batch capture: {e}")
    
    def search_observations(
        self,
        query: str,
        limit: int = 10,
        session_id: Optional[str] = None,
        tags: Optional[List[str]] = None,
        days: Optional[int] = None,
        min_importance: Optional[float] = None,
        use_cache: bool = True
    ) -> List[Dict]:
        """Search with caching and prepared query."""
        # Check cache
        if use_cache:
            cached = self._cache.get('search', query, limit, session_id, tags, days, min_importance)
            if cached is not None:
                return cached
        
        # Use prepared statement for common queries
        with self._get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                # Build optimized query
                if self._pgvector_available and query.startswith('embedding:'):
                    # Semantic search
                    embedding = json.loads(query[10:])
                    cur.execute("""
                        SELECT 
                            id, session_id, timestamp, source, content,
                            content_type, metadata, tags, importance_score,
                            1 - (embedding <=> %s::vector) as similarity
                        FROM observations
                        WHERE embedding IS NOT NULL
                        ORDER BY embedding <=> %s::vector
                        LIMIT %s
                    """, (Json(embedding), Json(embedding), limit))
                else:
                    # Full-text search with optional filters
                    conditions = ["to_tsvector('english', content) @@ plainto_tsquery('english', %s)"]
                    # Query appears twice: once for WHERE, once for SELECT rank calculation
                    params = [query, query]
                    
                    if session_id:
                        conditions.append("session_id = %s")
                        params.append(session_id)
                    
                    if tags:
                        conditions.append("tags && %s")
                        params.append(tags)
                    
                    if days:
                        conditions.append("timestamp > NOW() - INTERVAL '%s days'")
                        params.append(days)
                    
                    if min_importance is not None:
                        conditions.append("importance_score >= %s")
                        params.append(min_importance)
                    
                    sql = f"""
                        SELECT 
                            id, session_id, timestamp, source, content,
                            content_type, metadata, tags, importance_score,
                            ts_rank(to_tsvector('english', content), 
                                   plainto_tsquery('english', %s)) as rank
                        FROM observations
                        WHERE {' AND '.join(conditions)}
                        ORDER BY importance_score DESC, rank DESC, timestamp DESC
                        LIMIT %s
                    """
                    params.append(limit)
                    cur.execute(sql, params)
                
                results = [dict(row) for row in cur.fetchall()]
                
                # Cache results
                if use_cache and results:
                    self._cache.set(results, 'search', query, limit, session_id, tags, days, min_importance)
                
                return results
    
    def get_recent_observations(
        self,
        limit: int = 20,
        hours: int = 24
    ) -> List[Dict]:
        """Get recent observations from the last N hours."""
        with self._get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT 
                        id, session_id, created_at as timestamp, source, content,
                        content_type, metadata, tags, importance_score, status
                    FROM observations
                    WHERE created_at > NOW() - INTERVAL '%s hours'
                    ORDER BY created_at DESC
                    LIMIT %s
                """, (hours, limit))
                
                return [dict(row) for row in cur.fetchall()]
    
    def get_stats(self) -> Dict:
        """Get database statistics (cached for 60s)."""
        cached = self._cache.get('stats')
        if cached is not None:
            return cached
        
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT 
                        COUNT(*) as total,
                        COUNT(DISTINCT session_id) as sessions,
                        MAX(timestamp) as latest,
                        AVG(importance_score) as avg_importance
                    FROM observations
                """)
                obs_row = cur.fetchone()
                
                cur.execute("SELECT COUNT(*) FROM summaries")
                summary_count = cur.fetchone()[0]
                
                stats = {
                    'observations': obs_row[0] if obs_row else 0,
                    'summaries': summary_count,
                    'distinct_sessions': obs_row[1] if obs_row else 0,
                    'latest_capture': obs_row[2] if obs_row else None,
                    'average_importance': round(float(obs_row[3] or 0), 2) if obs_row else 0,
                    'pgvector_available': self._pgvector_available,
                    'cache_size': len(self._cache._cache),
                    'rate_limit_remaining': self._rate_limiter.get_remaining()
                }
                
                self._cache.set(stats, 'stats')
                return stats
    
    def get_instance_stats(self) -> List[Dict]:
        """Get statistics by instance/agent (v2.7.0).
        
        Returns list of dictionaries with stats per instance:
        - agent_label: Human-readable name
        - instance_id: UUID of machine
        - observation_count: Total captures
        - last_capture: Most recent timestamp
        - first_capture: First capture timestamp
        """
        with self._get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT 
                        agent_label,
                        COALESCE(instance_id::text, 'unknown') as instance_id,
                        COUNT(*) as observation_count,
                        MAX(timestamp) as last_capture,
                        MIN(timestamp) as first_capture,
                        COUNT(DISTINCT DATE(timestamp)) as active_days,
                        AVG(importance_score) as avg_importance
                    FROM observations
                    WHERE instance_id IS NOT NULL
                    GROUP BY agent_label, instance_id
                    ORDER BY last_capture DESC
                """)
                return cur.fetchall()
    
    def prune_old_observations(
        self,
        days: int,
        min_importance: float = 0.0
    ) -> int:
        """Delete old observations, preserving high-importance ones."""
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    DELETE FROM observations
                    WHERE timestamp < NOW() - INTERVAL '%s days'
                    AND importance_score < %s
                    RETURNING id
                """, (days, min_importance))
                
                deleted = cur.fetchall()
                conn.commit()
                
                self._cache.clear()
                return len(deleted)
    
    def export_to_markdown(
        self,
        filepath: str,
        days: Optional[int] = None,
        min_importance: float = 0.0,
        allowed_base: Optional[str] = None
    ) -> int:
        """Export observations to markdown file with path validation."""
        # Validate filepath for security
        safe_path = validate_filepath(filepath, allowed_base)
        
        with self._get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                sql = """
                    SELECT * FROM observations
                    WHERE importance_score >= %s
                """
                params = [min_importance]
                
                if days:
                    sql += " AND timestamp > NOW() - INTERVAL '%s days'"
                    params.append(days)
                
                sql += " ORDER BY timestamp DESC"
                
                cur.execute(sql, params)
                observations = cur.fetchall()
        
        # Write to file
        with open(safe_path, 'w', encoding='utf-8') as f:
            f.write(f"# Memory Export — {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
            f.write(f"Total observations: {len(observations)}\n\n")
            
            for obs in observations:
                f.write(f"## {obs['source']} — {obs['timestamp'].strftime('%Y-%m-%d %H:%M')}\n\n")
                f.write(f"**Importance:** {obs['importance_score']}\n\n")
                if obs['tags']:
                    tags_str = ', '.join(f'`{t}`' for t in obs['tags'])
                    f.write(f"**Tags:** {tags_str}\n\n")
                f.write(f"{obs['content']}\n\n")
                f.write("---\n\n")
        
        return len(observations)

    def update_observation_status(
        self,
        observation_id: str,
        new_status: str,
        resolution_notes: Optional[str] = None
    ) -> Dict:
        """Update observation status and set resolved_at if status is 'resolved'.

        Args:
            observation_id: UUID of the observation to update
            new_status: One of 'active', 'ongoing', 'resolved', 'superseded'
            resolution_notes: Optional notes about the resolution

        Returns:
            Dict with updated observation info

        Raises:
            ValidationError: If status is invalid
            ValueError: If observation not found
        """
        # Validate status
        valid_statuses = {'active', 'ongoing', 'resolved', 'superseded'}
        if new_status not in valid_statuses:
            raise ValidationError(f"Invalid status '{new_status}'. Must be one of: {', '.join(valid_statuses)}")

        with self._get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                # Build update query
                if new_status == 'resolved':
                    cur.execute("""
                        UPDATE observations
                        SET status = %s,
                            resolved_at = NOW(),
                            content = content || %s
                        WHERE id = %s
                        RETURNING *
                    """, (new_status, f"\n\n**[RESOLVED]**\n{resolution_notes or 'Completed'}", observation_id))
                else:
                    cur.execute("""
                        UPDATE observations
                        SET status = %s,
                            resolved_at = NULL
                        WHERE id = %s
                        RETURNING *
                    """, (new_status, observation_id))

                result = cur.fetchone()
                if not result:
                    raise ValueError(f"Observation {observation_id} not found")

                conn.commit()
                return {
                    'id': result['id'],
                    'status': result['status'],
                    'started_at': result['started_at'],
                    'resolved_at': result['resolved_at'],
                    'content': result['content'][:100] + '...' if len(result['content']) > 100 else result['content']
                }

    def mark_project_complete(
        self,
        project_name: str,
        resolution_notes: Optional[str] = None
    ) -> List[Dict]:
        """Mark all observations for a project as resolved.

        Args:
            project_name: Project tag to search for
            resolution_notes: Notes about completion

        Returns:
            List of updated observations
        """
        with self._get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    UPDATE observations
                    SET status = 'resolved',
                        resolved_at = NOW(),
                        content = content || %s
                    WHERE tags @> ARRAY[%s]
                    AND status NOT IN ('resolved', 'superseded')
                    RETURNING id, title, status, created_at
                """, (f"\n\n**[PROJECT COMPLETED]**\n{resolution_notes or 'All tasks finished'}", f"project:{project_name}"))

                updated = cur.fetchall()
                conn.commit()

                return [dict(row) for row in updated]

    # ============================================================================
    # FEATURE 1: RELATED OBSERVATIONS
    # ============================================================================

    def link_observations(
        self,
        observation_id: str,
        related_ids: List[str],
        bidirectional: bool = True
    ) -> bool:
        """Link an observation to other observations."""
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT related_observation_ids FROM observations WHERE id = %s",
                    (observation_id,)
                )
                result = cur.fetchone()
                current = result[0] if result and result[0] else []

                all_related = list(set(current + related_ids))[:50]

                cur.execute(
                    "UPDATE observations SET related_observation_ids = %s WHERE id = %s",
                    (all_related, observation_id)
                )

                if bidirectional:
                    for rel_id in related_ids:
                        if rel_id == observation_id:
                            continue
                        cur.execute(
                            "SELECT related_observation_ids FROM observations WHERE id = %s",
                            (rel_id,)
                        )
                        res = cur.fetchone()
                        rel_current = res[0] if res and res[0] else []
                        rel_all = list(set(rel_current + [observation_id]))[:50]
                        cur.execute(
                            "UPDATE observations SET related_observation_ids = %s WHERE id = %s",
                            (rel_all, rel_id)
                        )

                conn.commit()
                self._cache.clear()
                return True

    def find_related(
        self,
        observation_id: str,
        match_tags: bool = True,
        match_session: bool = False
    ) -> List[Dict]:
        """Find related observations."""
        with self._get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    "SELECT * FROM find_related_observations(%s, %s, %s)",
                    (observation_id, match_tags, match_session)
                )
                return [dict(row) for row in cur.fetchall()]

    # ============================================================================
    # FEATURE 2: TEMPLATES
    # ============================================================================

    def get_templates(
        self,
        template_type: Optional[str] = None,
        active_only: bool = True
    ) -> List[Dict]:
        """Get observation templates."""
        with self._get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                sql = "SELECT * FROM observation_templates WHERE 1=1"
                params = []

                if active_only:
                    sql += " AND is_active = TRUE"
                if template_type:
                    sql += " AND template_type = %s"
                    params.append(template_type)

                sql += " ORDER BY usage_count DESC"
                cur.execute(sql, params)
                return [dict(row) for row in cur.fetchall()]

    def apply_template(
        self,
        template_name: str,
        values: Dict[str, str],
        **capture_kwargs
    ) -> int:
        """Apply a template and capture observation."""
        with self._get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    "SELECT * FROM observation_templates WHERE template_name = %s",
                    (template_name,)
                )
                template = cur.fetchone()
                if not template:
                    raise ValueError(f"Template '{template_name}' not found")

                title = template['title_template']
                content = template['content_template']

                for key, value in values.items():
                    placeholder = "{" + key + "}"
                    title = title.replace(placeholder, value)
                    content = content.replace(placeholder, value)

                cur.execute(
                    "UPDATE observation_templates SET usage_count = usage_count + 1, updated_at = NOW() WHERE id = %s",
                    (template['id'],)
                )
                conn.commit()

        return self.capture_observation(
            content=content,
            title=title,
            tags=list(set((template['default_tags'] or []) + (capture_kwargs.get('tags') or []))),
            importance_score=capture_kwargs.get('importance_score', template['default_importance']),
            **{k: v for k, v in capture_kwargs.items() if k not in ['tags', 'importance_score']}
        )

    # ============================================================================
    # FEATURE 3: SUMMARIES (Auto-generated, separate from observations)
    # ============================================================================

    def create_summary(
        self,
        source_observation_ids: List[str],
        content: str,
        summary_type: str = 'manual',
        title: Optional[str] = None,
        generated_by: str = 'system',
        covers_from: Optional[datetime] = None,
        covers_until: Optional[datetime] = None,
        source_tags: Optional[List[str]] = None
    ) -> int:
        """Create a summary of observations. ADDITIONAL data only."""
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO summaries
                    (source_observation_ids, source_tags, summary_type, title, content,
                     generated_by, covers_from, covers_until, status)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'active')
                    RETURNING id
                    """,
                    (
                        source_observation_ids,
                        source_tags,
                        summary_type,
                        title,
                        content,
                        generated_by,
                        covers_from,
                        covers_until
                    )
                )
                result = cur.fetchone()
                conn.commit()
                return result[0]

    def generate_summary(
        self,
        tags: Optional[List[str]] = None,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
        min_importance: float = 0.5
    ) -> int:
        """Auto-generate a summary. Originals are NOT modified."""
        from_date = from_date or (datetime.now() - timedelta(days=7))
        to_date = to_date or datetime.now()

        with self._get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                sql = """
                    SELECT id, title, content, importance_score, tags, created_at
                    FROM observations
                    WHERE created_at BETWEEN %s AND %s
                    AND importance_score >= %s
                """
                params = [from_date, to_date, min_importance]

                if tags:
                    sql += " AND tags && %s"
                    params.append(tags)

                sql += " ORDER BY importance_score DESC, created_at DESC LIMIT 50"
                cur.execute(sql, params)
                observations = cur.fetchall()

                if not observations:
                    raise ValueError("No observations found to summarize")

                obs_ids = [o['id'] for o in observations]

                summary_lines = [
                    f"## Summary ({from_date.strftime('%Y-%m-%d')} to {to_date.strftime('%Y-%m-%d')})",
                    f"\n**Observations:** {len(observations)}",
                    "\n### Key Items\n"
                ]

                for obs in observations[:10]:
                    summary_lines.append(f"- [{obs['importance_score']:.1f}] {obs['title'] or obs['content'][:80]}...")

                content = "\n".join(summary_lines)

                cur.execute(
                    """
                    INSERT INTO summaries
                    (source_observation_ids, source_tags, summary_type, title, content,
                     generated_by, covers_from, covers_until, importance_score)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id
                    """,
                    (
                        obs_ids,
                        tags,
                        'auto',
                        f"Summary: {from_date.strftime('%Y-%m-%d')} to {to_date.strftime('%Y-%m-%d')}",
                        content,
                        'pg-memory',
                        from_date,
                        to_date,
                        0.7
                    )
                )
                result = cur.fetchone()
                conn.commit()
                self._cache.clear()
                return result[0]

    def search_summaries(
        self,
        query: str,
        summary_type: Optional[str] = None,
        days: Optional[int] = None,
        limit: int = 10
    ) -> List[Dict]:
        """Search summaries."""
        with self._get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                sql = """
                    SELECT *,
                        ts_rank(to_tsvector('english', content), plainto_tsquery('english', %s)) as rank
                    FROM summaries
                    WHERE (
                        to_tsvector('english', content) @@ plainto_tsquery('english', %s)
                        OR title ILIKE %s
                    )
                """
                params = [query, query, f"%{query}%"]

                if summary_type:
                    sql += " AND summary_type = %s"
                    params.append(summary_type)

                if days:
                    sql += " AND created_at > NOW() - INTERVAL '%s days'"
                    params.append(days)

                sql += " ORDER BY rank DESC, created_at DESC LIMIT %s"
                params.append(limit)

                cur.execute(sql, params)
                return [dict(row) for row in cur.fetchall()]

    # ============================================================================
    # FEATURE 4: CONFLICT DETECTION
    # ============================================================================

    def detect_conflicts(
        self,
        observation_id: str,
        check_days: int = 30
    ) -> List[Dict]:
        """Detect potential conflicts with recent observations."""
        with self._get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    "SELECT content, tags FROM observations WHERE id = %s",
                    (observation_id,)
                )
                source = cur.fetchone()
                if not source:
                    raise ValueError(f"Observation {observation_id} not found")

                cur.execute(
                    """
                    SELECT 
                        o.id,
                        o.title,
                        substring(o.content from 1 for 200) as preview,
                        o.importance_score,
                        ts_rank(to_tsvector('english', o.content), plainto_tsquery('english', %s)) + 
                            CASE WHEN o.tags && %s THEN 0.3 ELSE 0 END as conflict_score
                    FROM observations o
                    WHERE o.id != %s
                    AND o.created_at > NOW() - INTERVAL '%s days'
                    AND ts_rank(to_tsvector('english', o.content), plainto_tsquery('english', %s)) > 0.3
                    ORDER BY conflict_score DESC
                    LIMIT 10
                    """,
                    (source['content'], source['tags'] or [], observation_id, check_days, source['content'])
                )

                return [{**dict(row), 'conflict_score': round(row['conflict_score'], 2)} 
                        for row in cur.fetchall() if row['conflict_score'] > 0.5]

    def record_conflict(
        self,
        obs_1_id: str,
        obs_2_id: str,
        conflict_type: str = 'contradiction',
        conflict_score: float = 0.5,
        description: str = ""
    ) -> int:
        """Record a detected conflict."""
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO observation_conflicts
                    (observation_1_id, observation_2_id, conflict_type, conflict_score, conflict_description)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id
                    """,
                    (obs_1_id, obs_2_id, conflict_type, conflict_score, description)
                )
                result = cur.fetchone()
                conn.commit()
                return result[0]

    def get_open_conflicts(self) -> List[Dict]:
        """Get all open conflicts."""
        with self._get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    """
                    SELECT c.*, 
                        o1.title as obs_1_title,
                        o2.title as obs_2_title
                    FROM observation_conflicts c
                    LEFT JOIN observations o1 ON c.observation_1_id = o1.id
                    LEFT JOIN observations o2 ON c.observation_2_id = o2.id
                    WHERE c.status = 'open'
                    ORDER BY c.conflict_score DESC
                    """
                )
                return [dict(row) for row in cur.fetchall()]

    # ============================================================================
    # FEATURE 5: FOLLOW-UP REMINDERS
    # ============================================================================

    def create_reminder(
        self,
        observation_id: Optional[str] = None,
        chain_id: Optional[str] = None,
        reminder_type: str = 'follow_up',
        message: str = "",
        remind_at: Optional[datetime] = None
    ) -> int:
        """Create a follow-up reminder."""
        remind_at = remind_at or (datetime.now() + timedelta(days=1))

        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO follow_up_reminders
                    (observation_id, chain_id, reminder_type, reminder_message, remind_at)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id
                    """,
                    (observation_id, chain_id, reminder_type, message, remind_at)
                )
                result = cur.fetchone()
                conn.commit()
                return result[0]

    def check_stale_observations(self, min_days: int = 3) -> int:
        """Check for stale ongoing observations."""
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT create_stale_reminders(%s)", (min_days,))
                result = cur.fetchone()
                conn.commit()
                return result[0]

    def get_pending_reminders(self) -> List[Dict]:
        """Get all pending reminders that are due."""
        with self._get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    """
                    SELECT r.*,
                        o.title as observation_title,
                        c.chain_name
                    FROM follow_up_reminders r
                    LEFT JOIN observations o ON r.observation_id = o.id
                    LEFT JOIN observation_chains c ON r.chain_id = c.id
                    WHERE r.status = 'pending'
                    AND r.remind_at <= NOW()
                    ORDER BY r.remind_at ASC
                    """
                )
                return [dict(row) for row in cur.fetchall()]

    # ============================================================================
    # FEATURE 6: BULK MARKDOWN IMPORT
    # ============================================================================

    def import_markdown_file(
        self,
        filepath: str,
        source: str = 'markdown_import',
        default_importance: float = 0.5
    ) -> int:
        """Import a single markdown file."""
        from pathlib import Path

        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {filepath}")

        content = path.read_text(encoding='utf-8')

        import re
        headers = list(re.finditer(r'^##\s+(.+)$', content, re.MULTILINE))

        observations_created = 0

        if not headers:
            self.capture_observation(
                content=content[:self.config.max_content_length],
                source=source,
                title=path.stem,
                tags=['imported', 'markdown'],
                importance_score=default_importance,
                related_files=[str(path)]
            )
            observations_created = 1
        else:
            for i, header_match in enumerate(headers):
                title = header_match.group(1).strip()
                start = header_match.start()
                end = headers[i + 1].start() if i + 1 < len(headers) else len(content)
                section_content = content[start:end].strip()

                self.capture_observation(
                    content=section_content[:self.config.max_content_length],
                    source=source,
                    title=title,
                    tags=['imported', 'markdown', path.stem],
                    importance_score=default_importance,
                    related_files=[str(path)]
                )
                observations_created += 1

        return observations_created

    def import_markdown_directory(
        self,
        dirpath: str,
        pattern: str = '*.md',
        recursive: bool = False
    ) -> Dict:
        """Bulk import all markdown files in a directory."""
        from pathlib import Path

        base_path = Path(dirpath)
        if not base_path.is_dir():
            raise NotADirectoryError(f"Not a directory: {dirpath}")

        results = {'files_processed': 0, 'observations_created': 0, 'errors': []}
        glob_pattern = f'**/{pattern}' if recursive else pattern

        for md_file in base_path.glob(glob_pattern):
            try:
                count = self.import_markdown_file(str(md_file))
                results['files_processed'] += 1
                results['observations_created'] += count
            except Exception as e:
                results['errors'].append({'file': str(md_file), 'error': str(e)})

        return results

    # ============================================================================
    # FEATURE 7: OBSERVATION CHAINS
    # ============================================================================

    def create_chain(
        self,
        chain_name: str,
        chain_type: str = 'project',
        chain_description: str = "",
        root_observation_id: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> int:
        """Create a new observation chain."""
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO observation_chains
                    (chain_name, chain_type, chain_description, root_observation_id, tags)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id
                    """,
                    (chain_name, chain_type, chain_description, root_observation_id, tags)
                )
                result = cur.fetchone()
                conn.commit()

                if root_observation_id:
                    self.add_chain_step(result[0], root_observation_id, 1, 'milestone')

                return result[0]

    def add_chain_step(
        self,
        chain_id: str,
        observation_id: Optional[str],
        step_number: Optional[int] = None,
        step_type: str = 'milestone'
    ) -> int:
        """Add a step to a chain."""
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                if step_number is None:
                    cur.execute(
                        "SELECT COALESCE(MAX(step_number), 0) + 1 FROM chain_steps WHERE chain_id = %s",
                        (chain_id,)
                    )
                    step_number = cur.fetchone()[0]

                cur.execute(
                    """
                    INSERT INTO chain_steps (chain_id, observation_id, step_number, step_type)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id
                    """,
                    (chain_id, observation_id, step_number, step_type)
                )
                result = cur.fetchone()

                cur.execute(
                    """
                    UPDATE observation_chains
                    SET total_steps = (SELECT COUNT(*) FROM chain_steps WHERE chain_id = %s),
                        updated_at = NOW()
                    WHERE id = %s
                    """,
                    (chain_id, chain_id)
                )

                conn.commit()
                return result[0]

    def get_chain(self, chain_id: str) -> Dict:
        """Get full chain details with all steps."""
        with self._get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    """
                    SELECT c.*,
                        ROUND(100.0 * c.current_step / NULLIF(c.total_steps, 0), 1) as percent_complete
                    FROM observation_chains c
                    WHERE c.id = %s
                    """,
                    (chain_id,)
                )
                chain = cur.fetchone()

                if not chain:
                    raise ValueError(f"Chain {chain_id} not found")

                cur.execute(
                    """
                    SELECT cs.*, o.title as observation_title
                    FROM chain_steps cs
                    LEFT JOIN observations o ON cs.observation_id = o.id
                    WHERE cs.chain_id = %s
                    ORDER BY cs.step_number
                    """,
                    (chain_id,)
                )
                steps = cur.fetchall()

                return {**dict(chain), 'steps': [dict(s) for s in steps]}

    def list_chains(
        self,
        status: Optional[str] = None,
        chain_type: Optional[str] = None,
        limit: int = 20
    ) -> List[Dict]:
        """List chains with progress."""
        with self._get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                sql = """
                    SELECT c.*, 
                        ROUND(100.0 * c.current_step / NULLIF(c.total_steps, 0), 1) as percent_complete
                    FROM observation_chains c
                    WHERE 1=1
                """
                params = []

                if status:
                    sql += " AND c.status = %s"
                    params.append(status)
                if chain_type:
                    sql += " AND c.chain_type = %s"
                    params.append(chain_type)

                sql += " ORDER BY c.updated_at DESC LIMIT %s"
                params.append(limit)

                cur.execute(sql, params)
                return [dict(row) for row in cur.fetchall()]

    def complete_chain(self, chain_id: str) -> bool:
        """Mark a chain as complete."""
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE observation_chains
                    SET status = 'complete',
                        current_step = total_steps,
                        completed_at = NOW()
                    WHERE id = %s
                    """,
                    (chain_id,)
                )
                conn.commit()
                return cur.rowcount > 0

    # ============================================================================
    # NATURAL LANGUAGE QUERY METHODS
    # ============================================================================

    def natural_query(self, query: str, explain: bool = False) -> Union[NLQueryResult, str]:
        """
        Execute a natural language query against the memory database.

        Args:
            query: Natural language query string
            explain: If True, return explanation instead of executing

        Returns:
            NLQueryResult with SQL, params, results, and interpretation
            Or explanation string if explain=True

        Examples:
            "show me high-importance unresolved projects from last week"
            "what did I work on yesterday"
            "find all observations tagged with docker and error"
            "list active projects from this month"
            "top 10 recent decisions"
            "errors with high importance"
        """
        nlq = NaturalLanguageQuery(self)
        if explain:
            return nlq.explain_query(query)
        return nlq.parse(query)

    def close(self) -> None:
        """Clean up connection pool."""
        if self._pool:
            self._pool.closeall()
            self._pool = None
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    # ============================================================================
    # SETTINGS MANAGEMENT (for nl_query and other config)
    # ============================================================================

    def get_setting(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """Get a setting value from pg_memory_settings table."""
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT setting_value FROM pg_memory_settings WHERE setting_key = %s",
                    (key,)
                )
                result = cur.fetchone()
                return result[0] if result else default

    def set_setting(self, key: str, value: str, group: str = 'general', description: str = '') -> bool:
        """Set a setting value in pg_memory_settings table."""
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO pg_memory_settings (setting_key, setting_value, setting_group, description)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (setting_key) DO UPDATE SET
                        setting_value = EXCLUDED.setting_value,
                        setting_group = EXCLUDED.setting_group,
                        description = EXCLUDED.description
                    """,
                    (key, value, group, description)
                )
                conn.commit()
                return cur.rowcount > 0

    def get_nl_model(self) -> str:
        """Get the current nl_query model (from settings or env)."""
        # Check env first
        env_model = os.getenv('PG_MEMORY_NL_MODEL')
        if env_model:
            return env_model
        # Then check settings
        setting = self.get_setting('nl_query_model')
        if setting:
            return setting
        # Fall back to OpenClaw's model or default
        return os.getenv('OPENCLAW_MODEL', 'ollama/mistral:latest')

    def set_nl_model(self, model: str) -> bool:
        """Change the nl_query model."""
        # Test the model works
        try:
            self._test_ollama_model(model)
        except Exception as e:
            raise ValueError(f"Model '{model}' not available: {e}")

        # Save to settings
        return self.set_setting(
            'nl_query_model',
            model,
            group='nl_query',
            description='Model used for natural language to SQL queries'
        )

    def _test_ollama_model(self, model: str) -> None:
        """Test if Ollama model is available."""
        import subprocess
        model_name = model.replace('ollama/', '') if model.startswith('ollama/') else model
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
        if model_name not in result.stdout:
            raise RuntimeError(f"Model '{model_name}' not found. Run: ollama pull {model_name}")

    # ============================================================================
    # ADVANCED NL QUERY (using external LLM for complex queries)
    # ============================================================================

    def ask(self, question: str, model: Optional[str] = None) -> List[Dict]:
        """
        Natural language query using LLM SQL generation.

        Args:
            question: Natural language question
            model: Override model (uses settings if not specified)

        Returns:
            List of result dictionaries

        Examples:
            "Show me high importance observations from last week"
            "What projects are still ongoing?"
            "Find conflicts related to video production"
        """
        try:
            from nl_query import NLQueryEngine
        except ImportError:
            # Try relative import
            import sys
            sys.path.insert(0, os.path.dirname(__file__))
            from nl_query import NLQueryEngine

        # Use provided model or get from settings
        nl_model = model or self.get_nl_model()

        engine = NLQueryEngine()
        if nl_model:
            engine.config.model = nl_model

        return engine.ask(self._get_connection(), question)

    def preview_sql(self, question: str, model: Optional[str] = None) -> str:
        """Generate SQL from natural language without executing."""
        try:
            from nl_query import NLQueryEngine
        except ImportError:
            import sys
            sys.path.insert(0, os.path.dirname(__file__))
            from nl_query import NLQueryEngine

        nl_model = model or self.get_nl_model()
        engine = NLQueryEngine()
        if nl_model:
            engine.config.model = nl_model

        return engine.generate_sql(question)


# ============================================================================
# NATURAL LANGUAGE QUERY BUILDER (Simple pattern-based for common queries)
# ============================================================================

@dataclass
class NLQueryResult:
    """Result from natural language query."""
    sql_query: str
    params: List[Any]
    result_count: int
    results: List[Dict]
    execution_time_ms: float
    interpretation: str


class NaturalLanguageQuery:
    """
    Converts natural language queries to SQL for the pg-memory system.

    Examples:
        "show me high-importance unresolved projects from last week"
        "what did I work on yesterday"
        "find all observations tagged with docker and error"
        "list active projects from this month"
    """

    # Time patterns
    TIME_PATTERNS = {
        'today': lambda: (datetime.now().replace(hour=0, minute=0, second=0), datetime.now()),
        'yesterday': lambda: (datetime.now().replace(hour=0, minute=0, second=0) - timedelta(days=1),
                              datetime.now().replace(hour=0, minute=0, second=0)),
        'this week': lambda: (datetime.now().replace(hour=0, minute=0, second=0) - timedelta(days=datetime.now().weekday()),
                              datetime.now()),
        'last week': lambda: (datetime.now().replace(hour=0, minute=0, second=0) - timedelta(days=datetime.now().weekday() + 7),
                              datetime.now().replace(hour=0, minute=0, second=0) - timedelta(days=datetime.now().weekday())),
        'this month': lambda: (datetime.now().replace(day=1, hour=0, minute=0, second=0),
                               datetime.now()),
        'last month': lambda: ((datetime.now().replace(day=1) - timedelta(days=1)).replace(day=1, hour=0, minute=0, second=0),
                               datetime.now().replace(day=1, hour=0, minute=0, second=0)),
        'last 7 days': lambda: (datetime.now() - timedelta(days=7), datetime.now()),
        'last 30 days': lambda: (datetime.now() - timedelta(days=30), datetime.now()),
        'last 24 hours': lambda: (datetime.now() - timedelta(hours=24), datetime.now()),
    }

    # Status mappings
    STATUS_PATTERNS = {
        'active': ['active'],
        'ongoing': ['ongoing'],
        'resolved': ['resolved'],
        'complete': ['resolved'],
        'unresolved': ['active', 'ongoing'],
        'in progress': ['ongoing', 'active'],
        'pending': ['active'],
        'superseded': ['superseded'],
        'all': ['active', 'ongoing', 'resolved', 'superseded'],
    }

    # Importance patterns
    IMPORTANCE_PATTERNS = {
        'high-importance': (0.7, 1.0),
        'high importance': (0.7, 1.0),
        'very important': (0.8, 1.0),
        'critical': (0.9, 1.0),
        'medium-importance': (0.4, 0.7),
        'medium importance': (0.4, 0.7),
        'important': (0.5, 1.0),
        'low-importance': (0.0, 0.4),
        'low importance': (0.0, 0.4),
    }

    def __init__(self, memory: PostgresMemory):
        self.memory = memory

    def parse(self, query: str) -> NLQueryResult:
        """Parse natural language query and execute it."""
        start_time = time.time()

        # Normalize query
        query_lower = query.lower().strip()

        # Build SQL components
        where_clauses = []
        params = []
        order_by = "o.created_at DESC"
        limit = 50

        interpretation_parts = []

        # Parse time filters
        for pattern, date_func in self.TIME_PATTERNS.items():
            if pattern in query_lower:
                start_date, end_date = date_func()
                where_clauses.append("o.created_at >= %s AND o.created_at <= %s")
                params.extend([start_date, end_date])
                interpretation_parts.append(f"from {pattern}")
                break

        # Parse status filters
        for pattern, statuses in self.STATUS_PATTERNS.items():
            if pattern in query_lower:
                placeholders = ', '.join(['%s'] * len(statuses))
                where_clauses.append(f"o.status IN ({placeholders})")
                params.extend(statuses)
                interpretation_parts.append(f"with status: {', '.join(statuses)}")
                break

        # Parse importance filters
        for pattern, (min_imp, max_imp) in self.IMPORTANCE_PATTERNS.items():
            if pattern in query_lower:
                where_clauses.append("o.importance_score >= %s AND o.importance_score <= %s")
                params.extend([min_imp, max_imp])
                interpretation_parts.append(f"importance: {int(min_imp*100)}-{int(max_imp*100)}%")
                break

        # Parse tag filters
        tag_match = re.search(r'tagged (?:with )?(?:#?)([\w\-]+(?:,\s*#?[\w\-]+)*)', query_lower)
        if tag_match:
            tags = [t.strip().lstrip('#') for t in tag_match.group(1).split(',')]
            for tag in tags:
                where_clauses.append("o.tags @> ARRAY[%s]")
                params.append(tag)
            interpretation_parts.append(f"tags: {', '.join(tags)}")

        # Parse content search
        content_keywords = ['about', 'containing', 'with', 'search for', 'find', 'mentioning']
        for keyword in content_keywords:
            if keyword in query_lower:
                # Extract content after keyword (simple approach)
                idx = query_lower.find(keyword) + len(keyword)
                content_term = query[idx:].strip().split()[0:3]  # First 3 words
                if content_term:
                    search_term = ' '.join(content_term).rstrip('?.,;')
                    where_clauses.append("(o.content ILIKE %s OR o.title ILIKE %s)")
                    params.extend([f'%{search_term}%', f'%{search_term}%'])
                    interpretation_parts.append(f"containing '{search_term}'")
                break

        # Parse limit
        limit_match = re.search(r'top\s*(\d+)|limit\s*(\d+)|first\s*(\d+)', query_lower)
        if limit_match:
            limit = int(limit_match.group(1) or limit_match.group(2) or limit_match.group(3))
            interpretation_parts.append(f"limit: {limit}")

        # Parse order
        if 'oldest' in query_lower or 'first' in query_lower:
            order_by = "o.created_at ASC"
            interpretation_parts.append("sorted: oldest first")
        elif 'recent' in query_lower or 'latest' in query_lower:
            order_by = "o.created_at DESC"
            interpretation_parts.append("sorted: newest first")

        # Parse specific observation types
        if 'project' in query_lower or 'projects' in query_lower:
            where_clauses.append("(o.tags @> ARRAY['project'] OR o.obs_type = 'project')")
            interpretation_parts.append("type: project")
        elif 'task' in query_lower or 'tasks' in query_lower:
            where_clauses.append("(o.tags @> ARRAY['task'] OR o.obs_type = 'task')")
            interpretation_parts.append("type: task")
        elif 'decision' in query_lower:
            where_clauses.append("o.obs_type = 'decision'")
            interpretation_parts.append("type: decision")
        elif 'error' in query_lower:
            where_clauses.append("(o.obs_type = 'error' OR o.tags @> ARRAY['error'])")
            interpretation_parts.append("type: error")

        # Build final SQL
        base_sql = """
            SELECT o.id, o.content, o.title, o.obs_type, o.status,
                   o.importance_score, o.tags, o.created_at, o.updated_at,
                   o.started_at, o.resolved_at, o.related_files, o.related_urls
            FROM observations o
        """

        if where_clauses:
            base_sql += " WHERE " + " AND ".join(where_clauses)

        base_sql += f" ORDER BY {order_by} LIMIT %s"
        params.append(limit)

        # Execute query
        with self.memory._get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(base_sql, params)
                results = [dict(row) for row in cur.fetchall()]

        execution_time = (time.time() - start_time) * 1000

        interpretation = "Search: " + ("; ".join(interpretation_parts) if interpretation_parts else "all observations")

        return NLQueryResult(
            sql_query=base_sql,
            params=params,
            result_count=len(results),
            results=results,
            execution_time_ms=execution_time,
            interpretation=interpretation
        )

    def explain_query(self, query: str) -> str:
        """Explain what the query will do without executing it."""
        result = self.parse(query)
        return f"""
Interpretation: {result.interpretation}

SQL Query:
{result.sql_query}

Parameters: {result.params}

Expected to return up to {result.params[-1] if result.params else 50} results.
"""


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

_global_memory: Optional[PostgresMemory] = None

def get_memory(config: Optional[MemoryConfig] = None) -> PostgresMemory:
    """Get or create global memory instance."""
    global _global_memory
    if _global_memory is None:
        _global_memory = PostgresMemory(config)
    return _global_memory

def capture(content: str, **kwargs) -> int:
    """Quick capture."""
    return get_memory().capture_observation(content, **kwargs)

def capture_batch(observations: List[Dict]) -> List[int]:
    """Quick batch capture."""
    return get_memory().capture_batch(observations)

def search(query: str, **kwargs) -> List[Dict]:
    """Quick search."""
    return get_memory().search_observations(query, **kwargs)

def stats() -> Dict:
    """Quick stats."""
    return get_memory().get_stats()

def prune(days: int, min_importance: float = 0.0) -> int:
    """Quick prune."""
    return get_memory().prune_old_observations(days, min_importance)

def export(path: str, **kwargs) -> int:
    """Quick export."""
    return get_memory().export_to_markdown(path, **kwargs)

def ensure_observation(project_name: str, project_location: str, **kwargs) -> Dict:
    """Quick observation protocol check. Ensures observation exists."""
    return get_memory().ensure_observation_exists(project_name, project_location, **kwargs)

def check_observation(project_name: str, session_id: Optional[str] = None) -> bool:
    """Quick check if observation exists for project."""
    return get_memory().check_observation_exists(project_name, session_id)

def update_status(observation_id: str, new_status: str, notes: Optional[str] = None) -> Dict:
    """Quick update observation status (active, ongoing, resolved, superseded)."""
    return get_memory().update_observation_status(observation_id, new_status, notes)

def complete_project(project_name: str, notes: Optional[str] = None) -> List[Dict]:
    """Quick mark all observations for a project as resolved."""
    return get_memory().mark_project_complete(project_name, notes)

def auto_capture(task_description: str, **kwargs) -> Dict:
    """Quick auto-capture with observation protocol enforcement."""
    return get_memory().auto_capture_project(task_description, **kwargs)


# ============================================================================
# NEW CONVENIENCE FUNCTIONS (v2.3)
# ============================================================================

# --- Feature 1: Related Observations ---
def link_obs(observation_id: str, related_ids: List[str]) -> bool:
    """Quick link observations together."""
    return get_memory().link_observations(observation_id, related_ids)

def find_related_obs(observation_id: str) -> List[Dict]:
    """Quick find related observations."""
    return get_memory().find_related(observation_id)

# --- Feature 2: Templates ---
def get_templates(template_type: Optional[str] = None) -> List[Dict]:
    """Quick get templates."""
    return get_memory().get_templates(template_type)

def use_template(template_name: str, values: Dict[str, str], **kwargs) -> int:
    """Quick apply template and capture."""
    return get_memory().apply_template(template_name, values, **kwargs)

# --- Feature 3: Summaries ---
def summarize(tags: Optional[List[str]] = None, days: int = 7) -> int:
    """Quick generate summary of recent observations."""
    from_date = datetime.now() - timedelta(days=days)
    return get_memory().generate_summary(tags=tags, from_date=from_date)

def search_summaries(query: str, limit: int = 10) -> List[Dict]:
    """Quick search summaries."""
    return get_memory().search_summaries(query, limit=limit)

# --- Feature 4: Conflict Detection ---
def check_conflicts(observation_id: str) -> List[Dict]:
    """Quick check for conflicting observations."""
    return get_memory().detect_conflicts(observation_id)

def list_conflicts() -> List[Dict]:
    """Quick list open conflicts."""
    return get_memory().get_open_conflicts()

# --- Feature 5: Reminders ---
def remind(observation_id: str, message: str, days: int = 1) -> int:
    """Quick create reminder."""
    remind_at = datetime.now() + timedelta(days=days)
    return get_memory().create_reminder(observation_id=observation_id, message=message, remind_at=remind_at)

def check_stale(min_days: int = 3) -> int:
    """Quick check for stale ongoing observations."""
    return get_memory().check_stale_observations(min_days)

def pending_reminders() -> List[Dict]:
    """Quick get pending reminders."""
    return get_memory().get_pending_reminders()

# --- Feature 6: Bulk Import ---
def import_md(filepath: str, importance: float = 0.5) -> int:
    """Quick import markdown file."""
    return get_memory().import_markdown_file(filepath, default_importance=importance)

def import_dir(dirpath: str, recursive: bool = False) -> Dict:
    """Quick bulk import markdown directory."""
    return get_memory().import_markdown_directory(dirpath, recursive=recursive)

# --- Feature 7: Chains ---
def create_chain(name: str, chain_type: str = 'project', **kwargs) -> int:
    """Quick create chain."""
    return get_memory().create_chain(chain_name=name, chain_type=chain_type, **kwargs)

def add_step(chain_id: str, observation_id: Optional[str] = None, step_type: str = 'milestone') -> int:
    """Quick add step to chain."""
    return get_memory().add_chain_step(chain_id, observation_id, step_type=step_type)

def get_chain(chain_id: str) -> Dict:
    """Quick get chain details."""
    return get_memory().get_chain(chain_id)

def list_chains(status: Optional[str] = None, limit: int = 20) -> List[Dict]:
    """Quick list chains."""
    return get_memory().list_chains(status=status, limit=limit)

def finish_chain(chain_id: str) -> bool:
    """Quick complete chain."""
    return get_memory().complete_chain(chain_id)


# --- Natural Language Query ---
def ask(query: str, explain: bool = False) -> Union[NLQueryResult, str]:
    """
    Quick natural language query.

    Examples:
        ask("show me high-importance unresolved projects from last week")
        ask("what did I work on yesterday")
        ask("find all errors tagged with docker")
        ask("list top 10 recent decisions")
    """
    nlq = NaturalLanguageQuery(get_memory())
    if explain:
        return nlq.explain_query(query)
    return nlq.parse(query)

def query_nl(query: str, explain: bool = False) -> Union[NLQueryResult, str]:
    """Alias for ask()."""
    return ask(query, explain)


def recent(limit: int = 20, hours: int = 24) -> List[Dict]:
    """Quick get recent observations."""
    return get_memory().get_recent_observations(limit=limit, hours=hours)


# ============================================================================
# BACKUP/RESTORE FUNCTIONS (v2.6.0)
# ============================================================================

def backup(output_dir: Optional[str] = None, compress: bool = True) -> str:
    """Create full database backup using pg_dump.
    
    Args:
        output_dir: Directory for backup file (default: ~/.pg-memory/backups/)
        compress: Whether to gzip the backup
        
    Returns:
        Path to backup file
    """
    import subprocess
    from pathlib import Path
    
    config = get_memory().config
    db_name = config.db_name
    db_user = config.db_user
    db_host = config.db_host
    db_port = config.db_port
    
    # Determine backup directory
    if output_dir is None:
        backup_dir = Path.home() / ".pg-memory" / "backups"
    else:
        backup_dir = Path(output_dir)
    
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate backup filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"pgmemory_backup_{timestamp}.sql"
    if compress:
        filename += ".gz"
    backup_path = backup_dir / filename
    
    # Build pg_dump command
    cmd = [
        "pg_dump",
        "-h", db_host,
        "-p", str(db_port),
        "-U", db_user,
        "-d", db_name,
        "-F", "p",  # Plain text format
        "-v"  # Verbose
    ]
    
    # Add compression if requested
    if compress:
        cmd_str = " ".join(cmd) + f" | gzip > {backup_path}"
        result = subprocess.run(cmd_str, shell=True, capture_output=True, text=True)
    else:
        # Run pg_dump and redirect to file
        with open(backup_path, 'w') as f:
            result = subprocess.run(cmd, stdout=f, stderr=subprocess.PIPE, text=True)
    
    if result.returncode != 0:
        raise RuntimeError(f"Backup failed: {result.stderr}")
    
    # Create manifest
    manifest_path = backup_dir / "manifest.json"
    manifest = []
    if manifest_path.exists():
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)
    
    manifest.append({
        "file": str(backup_path),
        "timestamp": timestamp,
        "database": db_name,
        "compressed": compress,
        "size_bytes": backup_path.stat().st_size if backup_path.exists() else 0
    })
    
    # Keep only last 100 entries in manifest
    manifest = manifest[-100:]
    
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2)
    
    return str(backup_path)


def restore(backup_file: str, drop_existing: bool = False) -> None:
    """Restore database from backup file.
    
    Args:
        backup_file: Path to backup file (.sql or .sql.gz)
        drop_existing: Whether to drop existing database before restore
        
    Raises:
        RuntimeError: If restore fails
    """
    import subprocess
    from pathlib import Path
    
    config = get_memory().config
    db_name = config.db_name
    db_user = config.db_user
    db_host = config.db_host
    db_port = config.db_port
    
    backup_path = Path(backup_file)
    if not backup_path.exists():
        raise FileNotFoundError(f"Backup file not found: {backup_file}")
    
    # Drop existing database if requested
    if drop_existing:
        cmd = [
            "psql",
            "-h", db_host,
            "-p", str(db_port),
            "-U", db_user,
            "-d", "postgres",
            "-c", f"DROP DATABASE IF EXISTS {db_name};"
        ]
        subprocess.run(cmd, capture_output=True)
        
        cmd = [
            "psql",
            "-h", db_host,
            "-p", str(db_port),
            "-U", db_user,
            "-d", "postgres",
            "-c", f"CREATE DATABASE {db_name};"
        ]
        subprocess.run(cmd, capture_output=True)
    
    # Restore from backup
    is_compressed = str(backup_path).endswith('.gz')
    
    if is_compressed:
        cmd_str = f"gunzip -c {backup_path} | psql -h {db_host} -p {db_port} -U {db_user} -d {db_name}"
        result = subprocess.run(cmd_str, shell=True, capture_output=True, text=True)
    else:
        cmd = [
            "psql",
            "-h", db_host,
            "-p", str(db_port),
            "-U", db_user,
            "-d", db_name,
            "-f", str(backup_path)
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        raise RuntimeError(f"Restore failed: {result.stderr}")


def list_backups(backup_dir: Optional[str] = None) -> List[Dict]:
    """List available backups.
    
    Args:
        backup_dir: Directory to search (default: ~/.pg-memory/backups/)
        
    Returns:
        List of backup metadata dictionaries
    """
    from pathlib import Path
    
    if backup_dir is None:
        backup_dir = Path.home() / ".pg-memory" / "backups"
    else:
        backup_dir = Path(backup_dir)
    
    manifest_path = backup_dir / "manifest.json"
    if manifest_path.exists():
        with open(manifest_path, 'r') as f:
            return json.load(f)
    
    # Fallback: scan directory
    backups = []
    for f in sorted(backup_dir.glob("pgmemory_backup_*.sql*"), reverse=True):
        stat = f.stat()
        backups.append({
            "file": str(f),
            "timestamp": f.stem.replace("pgmemory_backup_", ""),
            "size_bytes": stat.st_size,
            "created": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "compressed": str(f).endswith('.gz')
        })
    
    return backups


def export_json(output_file: str, since: Optional[datetime] = None) -> int:
    """Export observations to JSON format.
    
    Args:
        output_file: Path to output JSON file
        since: Only export observations since this date (optional)
        
    Returns:
        Number of observations exported
    """
    mem = get_memory()
    
    with mem._get_connection() as conn:
        with conn.cursor() as cur:
            sql = "SELECT * FROM observations"
            params = []
            
            if since:
                sql += " WHERE timestamp > %s"
                params.append(since)
            
            sql += " ORDER BY timestamp"
            
            cur.execute(sql, params)
            rows = cur.fetchall()
            
            observations = []
            for row in rows:
                # Convert to dict (RealDictCursor would be better but this works)
                columns = [desc[0] for desc in cur.description]
                obs = dict(zip(columns, row))
                observations.append(obs)
    
    export_data = {
        "version": "2.6.0",
        "exported_at": datetime.now().isoformat(),
        "observations": observations,
        "count": len(observations)
    }
    
    # Custom encoder to handle Decimal and datetime
    class DateTimeEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, Decimal):
                return float(obj)
            if isinstance(obj, datetime):
                return obj.isoformat()
            if isinstance(obj, list):
                return [self.default(i) for i in obj]
            return super().default(obj)
    
    with open(output_file, 'w') as f:
        json.dump(export_data, f, indent=2, cls=DateTimeEncoder)
    
    return len(observations)


def import_json(input_file: str, skip_duplicates: bool = True) -> int:
    """Import observations from JSON file.
    
    Args:
        input_file: Path to JSON file
        skip_duplicates: Skip observations with similar content (default: True)
        
    Returns:
        Number of observations imported
    """
    mem = get_memory()
    
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    observations = data.get("observations", [])
    imported = 0
    
    for obs in observations:
        try:
            # Check for duplicates if enabled
            if skip_duplicates:
                duplicates = mem.find_similar(obs.get("content", ""), min_similarity=0.95, limit=1)
                if duplicates:
                    continue
            
            mem.capture_observation(
                content=obs.get("content", ""),
                session_id=obs.get("session_id"),
                source=obs.get("source", "import"),
                content_type=obs.get("content_type", "text"),
                metadata=obs.get("metadata"),
                tags=obs.get("tags", []),
                importance_score=obs.get("importance_score", 0.5),
                check_duplicates=False  # Already checked above
            )
            imported += 1
        except Exception as e:
            # Log error and continue
            print(f"Warning: Failed to import observation: {e}", file=sys.stderr)
            continue
    
    return imported


# ============================================================================
# MAIN — TEST
# ============================================================================

if __name__ == "__main__":
    print("🧠 PostgreSQL Memory System v2.0")
    print("=" * 50)
    
    try:
        config = MemoryConfig()
        mem = PostgresMemory(config)
        
        print("\n📊 Stats:")
        for k, v in mem.get_stats().items():
            print(f"  {k}: {v}")
        
        print("\n📝 Testing capture with validation...")
        obs_id = mem.capture_observation(
            content="Testing the optimized memory system",
            tags=["test", "optimized"],
            importance_score=0.5
        )
        print(f"  Captured ID: {obs_id}")
        
        print("\n🔍 Testing search...")
        results = mem.search_observations("memory", limit=5)
        print(f"  Found {len(results)} results")
        
        print("\n✅ All tests passed!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
    finally:
        if 'mem' in locals():
            mem.close()
