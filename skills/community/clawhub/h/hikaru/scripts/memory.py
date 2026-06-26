"""
Memory System for Hikaru
Manages conversation history, important moments, and relationship memories
"""

import sqlite3
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional


class MemorySystem:
    """Manages Hikaru's memory and conversation history"""

    def __init__(self, data_dir: Path):
        self.data_dir = Path(data_dir)
        self.db_path = self.data_dir / "relationship.db"

        # Initialize database
        self._init_database()

    def _init_database(self):
        """Initialize SQLite database schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Interactions table - stores all conversations
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS interactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                user_message TEXT NOT NULL,
                hikaru_response TEXT NOT NULL,
                emotional_state TEXT,
                importance_score REAL DEFAULT 0.5,
                tags TEXT
            )
        ''')

        # Important moments - manually or automatically flagged
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS important_moments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                interaction_id INTEGER,
                timestamp TEXT NOT NULL,
                moment_type TEXT,
                description TEXT,
                emotional_impact REAL,
                FOREIGN KEY (interaction_id) REFERENCES interactions(id)
            )
        ''')

        # Shared experiences - things you've done/talked about together
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS shared_experiences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                experience_type TEXT,
                description TEXT,
                related_interactions TEXT
            )
        ''')

        # Feedback log
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                feedback_text TEXT NOT NULL,
                context TEXT
            )
        ''')

        # User profile - things Hikaru learns about you
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_profile (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                confidence REAL DEFAULT 0.5,
                last_updated TEXT
            )
        ''')

        conn.commit()
        conn.close()

    def store_interaction(self, user_message: str, hikaru_response: str,
                         emotional_state: Dict[str, Any], timestamp: datetime):
        """Store a conversation interaction"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO interactions
            (timestamp, user_message, hikaru_response, emotional_state)
            VALUES (?, ?, ?, ?)
        ''', (
            timestamp.isoformat(),
            user_message,
            hikaru_response,
            json.dumps(emotional_state)
        ))

        interaction_id = cursor.lastrowid

        # Check if this should be marked as important
        importance = self._calculate_importance(user_message, emotional_state)
        if importance > 0.7:
            cursor.execute('''
                UPDATE interactions SET importance_score = ? WHERE id = ?
            ''', (importance, interaction_id))

        conn.commit()
        conn.close()

        return interaction_id

    def retrieve_relevant(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieve relevant memories for current context

        This is simplified - real implementation would use embeddings
        and semantic search
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # For now, just get recent important interactions
        cursor.execute('''
            SELECT id, timestamp, user_message, hikaru_response,
                   emotional_state, importance_score
            FROM interactions
            WHERE importance_score > 0.6
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (limit,))

        memories = []
        for row in cursor.fetchall():
            memories.append({
                "id": row[0],
                "timestamp": row[1],
                "user_message": row[2],
                "hikaru_response": row[3],
                "emotional_state": json.loads(row[4]) if row[4] else {},
                "importance": row[5],
                "summary": f"{row[2][:50]}..." if len(row[2]) > 50 else row[2]
            })

        conn.close()
        return memories

    def store_feedback(self, feedback_text: str, timestamp: datetime):
        """Store user feedback"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO feedback (timestamp, feedback_text)
            VALUES (?, ?)
        ''', (timestamp.isoformat(), feedback_text))

        conn.commit()
        conn.close()

    def mark_as_important(self, interaction_id: int, moment_type: str,
                         description: str, emotional_impact: float):
        """Mark an interaction as an important moment"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO important_moments
            (interaction_id, timestamp, moment_type, description, emotional_impact)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            interaction_id,
            datetime.now().isoformat(),
            moment_type,
            description,
            emotional_impact
        ))

        conn.commit()
        conn.close()

    def add_shared_experience(self, experience_type: str, description: str,
                             related_interaction_ids: List[int] = None):
        """Add a shared experience"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO shared_experiences
            (timestamp, experience_type, description, related_interactions)
            VALUES (?, ?, ?, ?)
        ''', (
            datetime.now().isoformat(),
            experience_type,
            description,
            json.dumps(related_interaction_ids or [])
        ))

        conn.commit()
        conn.close()

    def update_user_profile(self, key: str, value: str, confidence: float = 0.8):
        """Update something learned about the user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT OR REPLACE INTO user_profile
            (key, value, confidence, last_updated)
            VALUES (?, ?, ?, ?)
        ''', (key, value, confidence, datetime.now().isoformat()))

        conn.commit()
        conn.close()

    def extract_and_store_location(self, message: str):
        """
        Extract location mentions from user message and store them

        Examples:
        - "我到办公室了" → location: office
        - "在家休息" → location: home
        - "去咖啡馆" → location: cafe
        """
        location_patterns = {
            'office': ['办公室', 'office', '公司', 'work'],
            'home': ['家', 'home', '家里'],
            'cafe': ['咖啡馆', 'cafe', 'coffee shop', '咖啡店'],
            'gym': ['健身房', 'gym'],
            'restaurant': ['餐厅', 'restaurant', '饭店'],
            'park': ['公园', 'park'],
            'beach': ['海边', 'beach', '海滩'],
            'airport': ['机场', 'airport'],
            'station': ['车站', 'station', '地铁站']
        }

        message_lower = message.lower()

        for location_type, keywords in location_patterns.items():
            if any(keyword in message_lower for keyword in keywords):
                # Store as user profile
                self.update_user_profile(
                    f'last_location',
                    location_type,
                    confidence=0.7
                )

                # Also store with timestamp for history
                self.update_user_profile(
                    f'location_history_{datetime.now().strftime("%Y%m%d_%H%M")}',
                    location_type,
                    confidence=0.7
                )

                return location_type

        return None

    def get_last_known_location(self) -> Optional[str]:
        """Get user's last known location"""
        profile = self.get_user_profile()
        location_data = profile.get('last_location')

        if location_data:
            return location_data.get('value')

        return None

    def get_user_profile(self) -> Dict[str, Any]:
        """Get current user profile"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('SELECT key, value, confidence FROM user_profile')

        profile = {}
        for row in cursor.fetchall():
            profile[row[0]] = {
                "value": row[1],
                "confidence": row[2]
            }

        conn.close()
        return profile

    def get_conversation_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent conversation history"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT timestamp, user_message, hikaru_response
            FROM interactions
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (limit,))

        history = []
        for row in cursor.fetchall():
            history.append({
                "timestamp": row[0],
                "user": row[1],
                "hikaru": row[2]
            })

        conn.close()
        return list(reversed(history))  # Return in chronological order

    def _calculate_importance(self, message: str, emotional_state: Dict[str, Any]) -> float:
        """
        Calculate importance score for an interaction

        This is simplified - real implementation would be more sophisticated
        """
        importance = 0.5  # Base importance

        # Emotional intensity increases importance
        if emotional_state:
            intensity = emotional_state.get('intensity', 0.5)
            importance += intensity * 0.3

        # Length suggests depth
        if len(message) > 100:
            importance += 0.1

        # Certain keywords suggest importance
        important_keywords = ['love', 'hate', 'dream', 'fear', 'hope', 'remember']
        if any(keyword in message.lower() for keyword in important_keywords):
            importance += 0.2

        return min(importance, 1.0)
