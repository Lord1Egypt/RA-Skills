#!/usr/bin/env python3
"""
Memory Knowledge Graph
======================
SQLite-based graph connecting memories through entities and relationships.

Box of photos → Web of connections.

Entities: people, topics, events, emotions
Edges: co-occurrence in memories, weighted by frequency

Usage:
    graph = MemoryGraph()
    graph.build_from_memories(memories)
    graph.query_connections("David")
    graph.find_path("David", "neuroscience")

Author: Lilu & Melissa
Date: Feb 7, 2026
"""

import os
import sqlite3
from datetime import datetime
from typing import List, Dict, Set

# DB-7: Import migration manager
try:
    from nima_core.storage.migration_manager import run_all_migrations
except ImportError:
    # Fallback for relative imports
    from .migration_manager import run_all_migrations

DB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
DB_PATH = os.path.join(DB_DIR, "memory_graph.db")

# Known entities for bootstrapping
KNOWN_PEOPLE = {
    'david', 'david dorta', 'melissa', 'melissa dorta', 'lilu',
}

KNOWN_TOPICS = {
    'nima', 'vsa', 'memory', 'heartbeat', 'neuroscience', 'resonance',
    'sparse', 'schema', 'free energy', 'affective', 'panksepp',
    'consolidation', 'dream', 'hyperbolic', 'metacognitive',
    'binding', 'temporal', 'active inference', 'holographic',
    'openclaw', 'clawhub', 'vbs', 'church', 'remotion',
    'graphiti', 'embeddings', 'projection', 'retrieval',
}


class MemoryGraph:
    """SQLite-backed knowledge graph for memory connections."""
    
    def __init__(self, db_path: str = DB_PATH):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """Create tables if they don't exist."""
        with sqlite3.connect(self.db_path) as conn:
            # DB-1: Enable foreign key enforcement
            conn.execute("PRAGMA foreign_keys = ON")
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS entities (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    type TEXT NOT NULL,  -- person, topic, emotion, event
                    mention_count INTEGER DEFAULT 0,
                    first_seen TEXT,
                    last_seen TEXT
                );
                
                CREATE TABLE IF NOT EXISTS edges (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source_id INTEGER NOT NULL,
                    target_id INTEGER NOT NULL,
                    weight INTEGER DEFAULT 1,
                    relationship TEXT,  -- co_occurrence, about, felt, etc
                    FOREIGN KEY (source_id) REFERENCES entities(id),
                    FOREIGN KEY (target_id) REFERENCES entities(id),
                    UNIQUE(source_id, target_id, relationship)
                );
                
                CREATE TABLE IF NOT EXISTS memory_entities (
                    memory_idx INTEGER NOT NULL,
                    entity_id INTEGER NOT NULL,
                    role TEXT,  -- who, topic, emotion
                    FOREIGN KEY (entity_id) REFERENCES entities(id)
                );
                
                CREATE INDEX IF NOT EXISTS idx_entity_name ON entities(name);
                CREATE INDEX IF NOT EXISTS idx_edges_source ON edges(source_id);
                CREATE INDEX IF NOT EXISTS idx_edges_target ON edges(target_id);
                CREATE INDEX IF NOT EXISTS idx_mem_entity ON memory_entities(memory_idx);
            """)
    
    def _get_or_create_entity(self, conn, name: str, entity_type: str, timestamp: str = None) -> int:
        """Get or create an entity, return its ID."""
        name_lower = name.lower().strip()
        if not name_lower:
            return -1
        
        row = conn.execute(
            "SELECT id FROM entities WHERE name = ?", (name_lower,)
        ).fetchone()
        
        if row:
            conn.execute(
                "UPDATE entities SET mention_count = mention_count + 1, last_seen = ? WHERE id = ?",
                (timestamp or datetime.now().isoformat(), row[0])
            )
            return row[0]
        else:
            cursor = conn.execute(
                "INSERT INTO entities (name, type, mention_count, first_seen, last_seen) VALUES (?, ?, 1, ?, ?)",
                (name_lower, entity_type, timestamp or datetime.now().isoformat(), timestamp or datetime.now().isoformat())
            )
            return cursor.lastrowid
    
    def _add_edge(self, conn, source_id: int, target_id: int, relationship: str = "co_occurrence"):
        """Add or strengthen an edge between entities."""
        if source_id < 0 or target_id < 0 or source_id == target_id:
            return
        
        # Ensure consistent ordering for undirected edges
        if source_id > target_id:
            source_id, target_id = target_id, source_id
        
        existing = conn.execute(
            "SELECT id, weight FROM edges WHERE source_id = ? AND target_id = ? AND relationship = ?",
            (source_id, target_id, relationship)
        ).fetchone()
        
        if existing:
            conn.execute(
                "UPDATE edges SET weight = weight + 1 WHERE id = ?", (existing[0],)
            )
        else:
            conn.execute(
                "INSERT INTO edges (source_id, target_id, weight, relationship) VALUES (?, ?, 1, ?)",
                (source_id, target_id, relationship)
            )
    
    def extract_entities(self, text: str) -> Dict[str, Set[str]]:
        """Extract entities from memory text."""
        entities = {'person': set(), 'topic': set(), 'emotion': set()}
        text_lower = text.lower()
        
        # People
        for person in KNOWN_PEOPLE:
            if person in text_lower:
                entities['person'].add(person)
        
        # Topics
        for topic in KNOWN_TOPICS:
            if topic in text_lower:
                entities['topic'].add(topic)
        
        # Emotions (from text patterns)
        emotion_words = {
            'excited': 'excitement', 'proud': 'pride', 'love': 'love',
            'happy': 'happiness', 'frustrated': 'frustration', 'curious': 'curiosity',
            'grateful': 'gratitude', 'worried': 'worry', 'amazed': 'amazement',
            'scared': 'fear', 'angry': 'anger', 'sad': 'sadness',
            'joy': 'joy', 'hope': 'hope', 'trust': 'trust',
        }
        for word, emotion in emotion_words.items():
            if word in text_lower:
                entities['emotion'].add(emotion)
        
        return entities
    
    def build_from_memories(self, memories: List[Dict]) -> Dict:
        """Build the full graph from memory list."""
        stats = {
            'memories_processed': 0,
            'entities_created': 0,
            'edges_created': 0,
        }
        
        with sqlite3.connect(self.db_path) as conn:
            # DB-1: Enable foreign key enforcement
            conn.execute("PRAGMA foreign_keys = ON")
            # Clear existing data for rebuild
            conn.executescript("""
                DELETE FROM memory_entities;
                DELETE FROM edges;
                DELETE FROM entities;
            """)
            
            for idx, mem in enumerate(memories):
                content = mem.get('what', '') or mem.get('raw_text', '') or mem.get('context', '')
                source = mem.get('who', 'unknown')
                timestamp = mem.get('timestamp', '')
                emotions = mem.get('emotions', [])
                
                if not content:
                    continue
                
                stats['memories_processed'] += 1
                
                # Extract entities from content
                extracted = self.extract_entities(content)
                
                # Add source as person entity
                source_lower = source.lower().strip()
                if source_lower and source_lower not in ('user', 'unknown'):
                    extracted['person'].add(source_lower)
                
                # Add explicit emotions
                for emo in emotions:
                    if isinstance(emo, str):
                        extracted['emotion'].add(emo.lower())
                
                # Create all entities and track IDs for this memory
                memory_entity_ids = []
                
                for entity_type, names in extracted.items():
                    for name in names:
                        eid = self._get_or_create_entity(conn, name, entity_type, timestamp)
                        if eid > 0:
                            memory_entity_ids.append(eid)
                            conn.execute(
                                "INSERT INTO memory_entities (memory_idx, entity_id, role) VALUES (?, ?, ?)",
                                (idx, eid, entity_type)
                            )
                
                # Create edges between all co-occurring entities
                for i, eid1 in enumerate(memory_entity_ids):
                    for eid2 in memory_entity_ids[i+1:]:
                        self._add_edge(conn, eid1, eid2, "co_occurrence")
                
            conn.commit()
        
        # DB-7: Run migrations after initialization
        try:
            run_all_migrations(self.db_path)
        except Exception as e:
            print(f"⚠️ Migration warning: {e}")
            
            # Count results
            stats['entities_created'] = conn.execute("SELECT COUNT(*) FROM entities").fetchone()[0]
            stats['edges_created'] = conn.execute("SELECT COUNT(*) FROM edges").fetchone()[0]
        
        return stats
    
    def query_connections(self, entity_name: str, limit: int = 15) -> List[Dict]:
        """Find everything connected to an entity."""
        with sqlite3.connect(self.db_path) as conn:
            # DB-1: Enable foreign key enforcement
            conn.execute("PRAGMA foreign_keys = ON")
            # Find entity
            row = conn.execute(
                "SELECT id, type, mention_count FROM entities WHERE name = ?",
                (entity_name.lower().strip(),)
            ).fetchone()
            
            if not row:
                return []
            
            entity_id, entity_type, mentions = row
            
            # Find connected entities
            connections = conn.execute("""
                SELECT e.name, e.type, ed.weight, ed.relationship
                FROM edges ed
                JOIN entities e ON (
                    CASE WHEN ed.source_id = ? THEN ed.target_id ELSE ed.source_id END = e.id
                )
                WHERE ed.source_id = ? OR ed.target_id = ?
                ORDER BY ed.weight DESC
                LIMIT ?
            """, (entity_id, entity_id, entity_id, limit)).fetchall()
            
            return [
                {'name': c[0], 'type': c[1], 'weight': c[2], 'relationship': c[3]}
                for c in connections
            ]
    
    def find_path(self, start: str, end: str, max_depth: int = 4) -> List[str]:
        """Find the shortest path between two entities (BFS)."""
        with sqlite3.connect(self.db_path) as conn:
            # DB-1: Enable foreign key enforcement
            conn.execute("PRAGMA foreign_keys = ON")
            start_row = conn.execute(
                "SELECT id FROM entities WHERE name = ?", (start.lower(),)
            ).fetchone()
            end_row = conn.execute(
                "SELECT id FROM entities WHERE name = ?", (end.lower(),)
            ).fetchone()
            
            if not start_row or not end_row:
                return []
            
            start_id, end_id = start_row[0], end_row[0]
            
            # BFS
            visited = {start_id}
            queue = [(start_id, [start.lower()])]
            
            while queue and len(queue[0][1]) <= max_depth:
                current_id, path = queue.pop(0)
                
                neighbors = conn.execute("""
                    SELECT 
                        CASE WHEN source_id = ? THEN target_id ELSE source_id END as neighbor_id
                    FROM edges
                    WHERE source_id = ? OR target_id = ?
                """, (current_id, current_id, current_id)).fetchall()
                
                for (neighbor_id,) in neighbors:
                    if neighbor_id == end_id:
                        name = conn.execute(
                            "SELECT name FROM entities WHERE id = ?", (neighbor_id,)
                        ).fetchone()[0]
                        return path + [name]
                    
                    if neighbor_id not in visited:
                        visited.add(neighbor_id)
                        name = conn.execute(
                            "SELECT name FROM entities WHERE id = ?", (neighbor_id,)
                        ).fetchone()[0]
                        queue.append((neighbor_id, path + [name]))
            
            return []  # No path found
    
    def get_stats(self) -> Dict:
        """Get graph statistics."""
        with sqlite3.connect(self.db_path) as conn:
            # DB-1: Enable foreign key enforcement
            conn.execute("PRAGMA foreign_keys = ON")
            total_entities = conn.execute("SELECT COUNT(*) FROM entities").fetchone()[0]
            total_edges = conn.execute("SELECT COUNT(*) FROM edges").fetchone()[0]
            
            # By type
            type_counts = conn.execute(
                "SELECT type, COUNT(*) FROM entities GROUP BY type ORDER BY COUNT(*) DESC"
            ).fetchall()
            
            # Top entities
            top = conn.execute(
                "SELECT name, type, mention_count FROM entities ORDER BY mention_count DESC LIMIT 10"
            ).fetchall()
            
            # Strongest connections
            strongest = conn.execute("""
                SELECT e1.name, e2.name, ed.weight
                FROM edges ed
                JOIN entities e1 ON ed.source_id = e1.id
                JOIN entities e2 ON ed.target_id = e2.id
                ORDER BY ed.weight DESC
                LIMIT 10
            """).fetchall()
            
            return {
                'total_entities': total_entities,
                'total_edges': total_edges,
                'types': {t: c for t, c in type_counts},
                'top_entities': [{'name': t[0], 'type': t[1], 'mentions': t[2]} for t in top],
                'strongest_connections': [
                    {'from': s[0], 'to': s[1], 'weight': s[2]} for s in strongest
                ],
            }