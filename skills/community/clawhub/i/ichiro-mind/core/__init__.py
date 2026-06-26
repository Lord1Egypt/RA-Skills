#!/usr/bin/env python3
"""
Ichiro-Mind: The Ultimate Unified Memory System
兵步一郎的记忆系统

A 4-layer memory architecture combining:
- HOT: Real-time working memory (SESSION-STATE)
- WARM: Neural graph with spreading activation
- COLD: Semantic vector search (LanceDB)
- ARCHIVE: Persistent long-term storage
"""

import os
import json
import sqlite3
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class MemoryEntry:
    """A single memory entry"""
    content: str
    category: str
    importance: float = 0.5
    timestamp: str = None
    source: str = "user"
    tags: List[str] = None
    relations: List[Dict] = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()
        if self.tags is None:
            self.tags = []
        if self.relations is None:
            self.relations = []


class HotLayer:
    """HOT Layer: Real-time working memory using SESSION-STATE.md"""
    
    def __init__(self, filepath: str = "SESSION-STATE.md"):
        self.filepath = Path(filepath)
        self.state = self._load()
    
    def _load(self) -> Dict:
        """Load current state from file"""
        if not self.filepath.exists():
            return {"current_task": "", "context": {}, "decisions": [], "pending": []}
        
        # Parse markdown structure
        content = self.filepath.read_text()
        return self._parse_md(content)
    
    def _parse_md(self, content: str) -> Dict:
        """Parse SESSION-STATE.md format"""
        state = {"current_task": "", "context": {}, "decisions": [], "pending": []}
        # Simplified parsing - in real impl would be more robust
        return state
    
    def _save(self):
        """Save state to file (WAL protocol)"""
        md_content = self._to_md()
        self.filepath.write_text(md_content)
    
    def _to_md(self) -> str:
        """Convert state to markdown"""
        return f"""# SESSION-STATE.md — Ichiro-Mind HOT Layer

## Current Task
{self.state.get('current_task', 'None')}

## Key Context
{json.dumps(self.state.get('context', {}), indent=2)}

## Recent Decisions
{chr(10).join(f"- {'[x]' if d.get('done') else '[ ]'} {d.get('content', '')}" for d in self.state.get('decisions', []))}

## Pending Actions
{chr(10).join(f"- [ ] {p}" for p in self.state.get('pending', []))}

---
*Last updated: {datetime.now().isoformat()}*
"""
    
    def update(self, key: str, value: Any):
        """Update state with WAL protocol"""
        self.state[key] = value
        self._save()
    
    def get(self, key: str, default=None):
        """Get value from state"""
        return self.state.get(key, default)
    
    def recall(self, query: str) -> List[MemoryEntry]:
        """Fast recall from hot layer"""
        results = []
        # Search in context
        for k, v in self.state.get('context', {}).items():
            if query.lower() in str(v).lower():
                results.append(MemoryEntry(
                    content=f"{k}: {v}",
                    category="context",
                    importance=0.9,
                    source="hot"
                ))
        return results


class WarmLayer:
    """WARM Layer: Neural graph with spreading activation"""
    
    def __init__(self, db_path: str = "~/.ichiro-mind/neural.db"):
        self.db_path = Path(db_path).expanduser()
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(self.db_path))
        self._init_db()
    
    def _init_db(self):
        """Initialize neural graph database"""
        cursor = self.conn.cursor()
        
        # Neurons (memories)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS neurons (
                id INTEGER PRIMARY KEY,
                content TEXT NOT NULL,
                type TEXT,
                importance REAL DEFAULT 0.5,
                access_count INTEGER DEFAULT 0,
                last_access TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Synapses (connections)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS synapses (
                id INTEGER PRIMARY KEY,
                from_neuron INTEGER,
                to_neuron INTEGER,
                type TEXT,
                strength REAL DEFAULT 1.0,
                FOREIGN KEY (from_neuron) REFERENCES neurons(id),
                FOREIGN KEY (to_neuron) REFERENCES neurons(id)
            )
        """)
        
        self.conn.commit()
    
    def remember(self, entry: MemoryEntry) -> int:
        """Store memory in neural graph"""
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO neurons (content, type, importance) VALUES (?, ?, ?)",
            (entry.content, entry.category, entry.importance)
        )
        neuron_id = cursor.lastrowid
        
        # Create synapses for relations
        for rel in entry.relations:
            # Find or create target neuron
            cursor.execute("SELECT id FROM neurons WHERE content = ?", (rel.get('target'),))
            result = cursor.fetchone()
            if result:
                target_id = result[0]
                cursor.execute(
                    "INSERT INTO synapses (from_neuron, to_neuron, type, strength) VALUES (?, ?, ?, ?)",
                    (neuron_id, target_id, rel.get('type', 'RELATED_TO'), rel.get('strength', 1.0))
                )
        
        self.conn.commit()
        return neuron_id
    
    def recall(self, query: str, depth: int = 1) -> List[MemoryEntry]:
        """Recall with spreading activation"""
        cursor = self.conn.cursor()
        
        # Find seed neurons matching query
        cursor.execute(
            "SELECT id, content, type, importance FROM neurons WHERE content LIKE ?",
            (f"%{query}%",)
        )
        seeds = cursor.fetchall()
        
        results = []
        activated = set()
        
        for seed in seeds:
            neuron_id, content, type_, importance = seed
            if neuron_id not in activated:
                activated.add(neuron_id)
                results.append(MemoryEntry(
                    content=content,
                    category=type_ or "unknown",
                    importance=importance,
                    source="warm"
                ))
                
                # Spreading activation
                if depth > 0:
                    cursor.execute(
                        """SELECT n.id, n.content, n.type, n.importance, s.strength 
                           FROM synapses s JOIN neurons n ON s.to_neuron = n.id 
                           WHERE s.from_neuron = ?""",
                        (neuron_id,)
                    )
                    for related in cursor.fetchall():
                        if related[0] not in activated:
                            activated.add(related[0])
                            results.append(MemoryEntry(
                                content=related[1],
                                category=related[2] or "related",
                                importance=related[3] * related[4],  # importance * strength
                                source="warm-spread"
                            ))
        
        return results
    
    def strengthen(self, neuron_id: int):
        """Strengthen memory (Hebbian learning)"""
        cursor = self.conn.cursor()
        cursor.execute(
            "UPDATE neurons SET access_count = access_count + 1, last_access = ? WHERE id = ?",
            (datetime.now().isoformat(), neuron_id)
        )
        self.conn.commit()


class ColdLayer:
    """COLD Layer: Semantic vector search"""
    
    def __init__(self, db_path: str = "~/.ichiro-mind/vectors.lance"):
        self.db_path = Path(db_path).expanduser()
        self.memories: List[MemoryEntry] = []
        self._load()
    
    def _load(self):
        """Load vector memories"""
        # Simplified - real impl would use LanceDB
        pass
    
    def remember(self, entry: MemoryEntry):
        """Store with embedding"""
        self.memories.append(entry)
        # In real impl: create embedding, store in LanceDB
    
    def search(self, query: str, top_k: int = 5) -> List[MemoryEntry]:
        """Semantic search"""
        # Simplified - real impl would use vector similarity
        results = []
        for mem in self.memories:
            if query.lower() in mem.content.lower():
                results.append(mem)
        return results[:top_k]


class ArchiveLayer:
    """ARCHIVE Layer: Persistent long-term storage"""
    
    def __init__(self, memory_file: str = "MEMORY.md", daily_dir: str = "memory/"):
        self.memory_file = Path(memory_file)
        self.daily_dir = Path(daily_dir)
        self.daily_dir.mkdir(parents=True, exist_ok=True)
    
    def write_daily(self, content: str):
        """Write to daily log"""
        today = datetime.now().strftime("%Y-%m-%d")
        daily_file = self.daily_dir / f"{today}.md"
        
        with open(daily_file, 'a') as f:
            f.write(f"\n## {datetime.now().strftime('%H:%M')}\n{content}\n")
    
    def read_memory_md(self) -> str:
        """Read MEMORY.md"""
        if self.memory_file.exists():
            return self.memory_file.read_text()
        return ""
    
    def append_memory(self, section: str, content: str):
        """Append to MEMORY.md section"""
        # Simplified - real impl would parse and update sections
        pass


class ExperienceTracker:
    """Track decisions and learn from outcomes"""
    
    def __init__(self, db_path: str = "~/.ichiro-mind/experience.db"):
        self.db_path = Path(db_path).expanduser()
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(self.db_path))
        self._init_db()
    
    def _init_db(self):
        """Initialize experience database"""
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS experiences (
                id INTEGER PRIMARY KEY,
                decision TEXT NOT NULL,
                context TEXT,
                outcome TEXT,
                lesson TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.commit()
    
    def learn(self, decision: str, outcome: str, lesson: str, context: str = ""):
        """Learn from experience"""
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO experiences (decision, context, outcome, lesson) VALUES (?, ?, ?, ?)",
            (decision, context, outcome, lesson)
        )
        self.conn.commit()
    
    def get_lessons(self, context: str = "", limit: int = 5) -> List[Dict]:
        """Get relevant lessons"""
        cursor = self.conn.cursor()
        if context:
            cursor.execute(
                "SELECT * FROM experiences WHERE context LIKE ? ORDER BY timestamp DESC LIMIT ?",
                (f"%{context}%", limit)
            )
        else:
            cursor.execute("SELECT * FROM experiences ORDER BY timestamp DESC LIMIT ?", (limit,))
        
        columns = [desc[0] for desc in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]


class IchiroMind:
    """
    The main Ichiro-Mind interface.
    Unified memory system combining all 4 layers.
    """
    
    def __init__(self, config_path: str = None):
        self.config = self._load_config(config_path)
        
        # Initialize layers
        self.hot = HotLayer()
        self.warm = WarmLayer()
        self.cold = ColdLayer()
        self.archive = ArchiveLayer()
        self.experience = ExperienceTracker()
    
    def _load_config(self, config_path: str = None) -> Dict:
        """Load configuration"""
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config" / "default.json"
        
        with open(config_path) as f:
            return json.load(f)
    
    def remember(self, content: str, category: str = "general", 
                 importance: float = 0.5, tags: List[str] = None,
                 relations: List[Dict] = None) -> Dict:
        """
        Store memory (auto-routes to appropriate layer based on importance/type)
        
        Args:
            content: The memory content
            category: Type of memory (preference, decision, fact, etc.)
            importance: 0.0-1.0 importance score
            tags: Optional tags
            relations: Optional semantic relations
        """
        entry = MemoryEntry(
            content=content,
            category=category,
            importance=importance,
            tags=tags or [],
            relations=relations or []
        )
        
        results = {}
        
        # Route to layers based on importance and type
        if importance >= 0.9:
            # Critical: Store in all layers
            results['warm'] = self.warm.remember(entry)
            results['cold'] = self.cold.remember(entry)
            self.archive.write_daily(f"[{category}] {content}")
        elif importance >= 0.7:
            # Important: Warm + Cold
            results['warm'] = self.warm.remember(entry)
            results['cold'] = self.cold.remember(entry)
        elif importance >= 0.5:
            # Normal: Cold only
            results['cold'] = self.cold.remember(entry)
        else:
            # Low priority: Daily log only
            self.archive.write_daily(f"[{category}] {content}")
        
        # If has relations, definitely store in warm layer
        if relations:
            results['warm'] = self.warm.remember(entry)
        
        return results
    
    def recall(self, query: str, strategy: str = "smart") -> List[MemoryEntry]:
        """
        Recall memories with smart routing
        
        Args:
            query: Search query
            strategy: "smart" (auto), "hot", "warm", "cold", "archive", "all"
        """
        results = []
        
        if strategy == "smart":
            # Try layers in order of speed/relevance
            # 1. HOT: Recent context
            hot_results = self.hot.recall(query)
            if hot_results:
                results.extend(hot_results)
            
            # 2. WARM: Neural graph (if query suggests relationships)
            if any(word in query.lower() for word in ["why", "because", "caused", "decision"]):
                warm_results = self.warm.recall(query, depth=1)
                results.extend(warm_results)
            
            # 3. COLD: Vector search
            cold_results = self.cold.search(query)
            results.extend(cold_results)
        
        elif strategy == "hot":
            results = self.hot.recall(query)
        elif strategy == "warm":
            results = self.warm.recall(query, depth=2)
        elif strategy == "cold":
            results = self.cold.search(query)
        
        # Sort by importance
        results.sort(key=lambda x: x.importance, reverse=True)
        return results
    
    def recall_deep(self, query: str, depth: int = 2) -> List[MemoryEntry]:
        """Deep recall with spreading activation"""
        return self.warm.recall(query, depth=depth)
    
    def learn(self, decision: str, outcome: str, lesson: str, context: str = ""):
        """Learn from experience"""
        self.experience.learn(decision, outcome, lesson, context)
        
        # Also store as important memory
        self.remember(
            content=f"Lesson: {lesson} (from: {decision} → {outcome})",
            category="lesson",
            importance=0.85,
            tags=["experience", "learned"]
        )
    
    def get_lessons(self, context: str = "", limit: int = 5) -> List[Dict]:
        """Get learned lessons"""
        return self.experience.get_lessons(context, limit)
    
    def auto_capture(self, text: str):
        """Auto-extract memories from text"""
        # Simplified extraction - real impl would use LLM
        # Look for patterns like "I prefer", "We decided", etc.
        import re
        
        # Preference extraction
        pref_match = re.search(r'(?:prefer|like|want)\s+(.+)', text, re.IGNORECASE)
        if pref_match:
            self.remember(
                content=f"Preference: {pref_match.group(1)}",
                category="preference",
                importance=0.8
            )
        
        # Decision extraction
        decision_match = re.search(r'(?:decided|choose|going with)\s+(.+)', text, re.IGNORECASE)
        if decision_match:
            self.remember(
                content=f"Decision: {decision_match.group(1)}",
                category="decision",
                importance=0.85
            )
    
    def stats(self) -> Dict:
        """Get memory statistics"""
        return {
            "hot": "active",
            "warm": "active", 
            "cold": len(self.cold.memories),
            "archive": "active",
            "experience": "active"
        }


# CLI Interface
if __name__ == "__main__":
    import sys
    
    mind = IchiroMind()
    
    if len(sys.argv) < 2:
        print("Ichiro-Mind v1.0.0 - The Ultimate Memory System")
        print("Usage: python -m ichiro_mind [init|remember|recall|learn|stats]")
        sys.exit(0)
    
    command = sys.argv[1]
    
    if command == "init":
        print("✅ Ichiro-Mind initialized")
        print(f"   Config: ~/.ichiro-mind/")
        print(f"   Database: {mind.warm.db_path}")
    
    elif command == "remember" and len(sys.argv) >= 3:
        content = sys.argv[2]
        category = sys.argv[3] if len(sys.argv) > 3 else "general"
        mind.remember(content, category)
        print(f"✅ Remembered: {content}")
    
    elif command == "recall" and len(sys.argv) >= 3:
        query = sys.argv[2]
        results = mind.recall(query)
        print(f"🔍 Recall results for '{query}':")
        for r in results[:5]:
            print(f"   [{r.category}] {r.content[:80]}...")
    
    elif command == "stats":
        stats = mind.stats()
        print("📊 Ichiro-Mind Statistics:")
        for layer, status in stats.items():
            print(f"   {layer.upper()}: {status}")
    
    else:
        print(f"Unknown command: {command}")
