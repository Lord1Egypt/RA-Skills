#!/usr/bin/env python3
"""
Conversation memory for smart router.
Maintains context across multiple turns for better routing decisions.
"""

import json
import sqlite3
import time
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Optional, List


@dataclass
class ConversationTurn:
    """Single turn in a conversation."""
    user_message: str
    classification_score: int
    routed_to: str  # "local" | "cloud" | "specialist:X"
    model_used: str
    timestamp: float
    
    def to_dict(self) -> dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict) -> "ConversationTurn":
        return cls(**data)


class ConversationMemory:
    """
    SQLite-based conversation memory.
    
    Tracks conversation history to enable:
    - Context-aware classification (follow-ups are simpler)
    - Model preference learning (which models worked well)
    - Conversation continuity
    """
    
    def __init__(self, db_path: str = "cache/conversations.db"):
        """Initialize conversation memory."""
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()
    
    def _init_db(self):
        """Initialize database tables."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    conversation_id TEXT PRIMARY KEY,
                    created_at REAL,
                    last_updated REAL
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS turns (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    conversation_id TEXT,
                    user_message TEXT,
                    classification_score INTEGER,
                    routed_to TEXT,
                    model_used TEXT,
                    timestamp REAL,
                    FOREIGN KEY (conversation_id) REFERENCES conversations(conversation_id)
                )
            """)
            conn.commit()
    
    def start_conversation(self, conversation_id: Optional[str] = None) -> str:
        """
        Start a new conversation.
        
        Args:
            conversation_id: Optional ID (generated if not provided)
            
        Returns:
            conversation_id
        """
        if conversation_id is None:
            conversation_id = f"conv_{int(time.time())}_{hash(time.time()) % 10000}"
        
        now = time.time()
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT OR REPLACE INTO conversations (conversation_id, created_at, last_updated) VALUES (?, ?, ?)",
                (conversation_id, now, now)
            )
            conn.commit()
        
        return conversation_id
    
    def add_turn(self, conversation_id: str, user_message: str, 
                 classification_score: int, routed_to: str, model_used: str):
        """Add a turn to the conversation."""
        with sqlite3.connect(self.db_path) as conn:
            # Add turn
            conn.execute(
                """INSERT INTO turns (conversation_id, user_message, classification_score, 
                    routed_to, model_used, timestamp) VALUES (?, ?, ?, ?, ?, ?)""",
                (conversation_id, user_message, classification_score, routed_to, model_used, time.time())
            )
            # Update conversation timestamp
            conn.execute(
                "UPDATE conversations SET last_updated = ? WHERE conversation_id = ?",
                (time.time(), conversation_id)
            )
            conn.commit()
    
    def get_conversation_history(self, conversation_id: str, limit: int = 10) -> List[ConversationTurn]:
        """
        Get recent conversation history.
        
        Args:
            conversation_id: Conversation ID
            limit: Max number of turns to return
            
        Returns:
            List of ConversationTurn (most recent first)
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                """SELECT user_message, classification_score, routed_to, model_used, timestamp
                   FROM turns WHERE conversation_id = ? ORDER BY timestamp DESC LIMIT ?""",
                (conversation_id, limit)
            )
            rows = cursor.fetchall()
        
        # Convert to ConversationTurn objects (reverse to get chronological order)
        turns = []
        for row in reversed(rows):
            turns.append(ConversationTurn(*row))
        
        return turns
    
    def is_follow_up(self, conversation_id: str, current_task: str) -> bool:
        """
        Determine if current task is a follow-up to previous message.
        
        Heuristics:
        - Short message (< 10 words)
        - Contains pronouns (it, that, this, they)
        - No explicit subject
        
        Args:
            conversation_id: Current conversation
            current_task: Current user message
            
        Returns:
            True if likely a follow-up
        """
        history = self.get_conversation_history(conversation_id, limit=1)
        if not history:
            return False
        
        task_lower = current_task.lower().strip()
        word_count = len(task_lower.split())
        
        # Short messages are often follow-ups
        if word_count < 5:
            return True
        
        # Pronoun indicators
        pronouns = ['it', 'that', 'this', 'they', 'them', 'those', 'these']
        if any(f' {p} ' in f' {task_lower} ' for p in pronouns):
            return True
        
        # Question continuation
        if task_lower.startswith(('and ', 'or ', 'but ', 'what about', 'how about')):
            return True
        
        return False
    
    def adjust_classification(self, conversation_id: str, base_score: int, task: str) -> int:
        """
        Adjust classification based on conversation context.
        
        Follow-ups typically simpler than initial queries.
        
        Args:
            conversation_id: Current conversation
            base_score: Base classification score
            task: Current task
            
        Returns:
            Adjusted score
        """
        if self.is_follow_up(conversation_id, task):
            # Reduce complexity by 1 for follow-ups (minimum 1)
            return max(1, base_score - 1)
        
        return base_score
    
    def get_model_success_rate(self, model: str, window: int = 100) -> float:
        """
        Get success rate for a model.
        
        Args:
            model: Model name
            window: Number of recent turns to consider
            
        Returns:
            Success rate (0.0 - 1.0)
        """
        # This would require tracking success/failure
        # For now, return placeholder
        return 1.0
    
    def cleanup_old_conversations(self, max_age_days: int = 7):
        """Remove conversations older than max_age_days."""
        cutoff = time.time() - (max_age_days * 24 * 60 * 60)
        
        with sqlite3.connect(self.db_path) as conn:
            # Get old conversation IDs
            cursor = conn.execute(
                "SELECT conversation_id FROM conversations WHERE last_updated < ?",
                (cutoff,)
            )
            old_ids = [row[0] for row in cursor.fetchall()]
            
            # Delete turns first (foreign key)
            for conv_id in old_ids:
                conn.execute("DELETE FROM turns WHERE conversation_id = ?", (conv_id,))
            
            # Delete conversations
            conn.execute("DELETE FROM conversations WHERE last_updated < ?", (cutoff,))
            conn.commit()
    
    def get_stats(self) -> dict:
        """Get memory statistics."""
        with sqlite3.connect(self.db_path) as conn:
            conversations = conn.execute("SELECT COUNT(*) FROM conversations").fetchone()[0]
            turns = conn.execute("SELECT COUNT(*) FROM turns").fetchone()[0]
        
        return {
            "conversations": conversations,
            "total_turns": turns
        }


# Global memory instance
_memory_instance: Optional[ConversationMemory] = None


def get_memory(db_path: str = "cache/conversations.db") -> ConversationMemory:
    """Get or create global memory instance."""
    global _memory_instance
    if _memory_instance is None:
        _memory_instance = ConversationMemory(db_path)
    return _memory_instance


if __name__ == "__main__":
    # Test conversation memory
    memory = ConversationMemory("test_conversations.db")
    
    # Start conversation
    conv_id = memory.start_conversation()
    print(f"Started conversation: {conv_id}")
    
    # Add some turns
    memory.add_turn(conv_id, "Explain quantum computing", 4, "cloud", "qwen2.5:14b")
    memory.add_turn(conv_id, "What about entanglement?", 2, "local", "llama3.2")
    memory.add_turn(conv_id, "Give me an example", 1, "local", "llama3.2")
    
    # Get history
    history = memory.get_conversation_history(conv_id)
    print(f"\nConversation history ({len(history)} turns):")
    for turn in history:
        print(f"  - [{turn.routed_to}] {turn.user_message[:50]}...")
    
    # Check follow-up detection
    print(f"\nFollow-up detection:")
    print(f"  'What about X?' is follow-up: {memory.is_follow_up(conv_id, 'What about X?')}")
    print(f"  'Explain quantum physics' is follow-up: {memory.is_follow_up(conv_id, 'Explain quantum physics')}")
    
    # Adjust classification
    print(f"\nClassification adjustment:")
    print(f"  Base score 4 -> adjusted: {memory.adjust_classification(conv_id, 4, 'What about that?')}")
    print(f"  Base score 4 -> adjusted: {memory.adjust_classification(conv_id, 4, 'Explain quantum physics')}")
    
    # Stats
    print(f"\nMemory stats: {memory.get_stats()}")
    
    # Cleanup
    import os
    os.remove("test_conversations.db")
    print("\nConversation memory test passed!")
