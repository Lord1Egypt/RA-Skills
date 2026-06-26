"""
Nex Voice - Storage and Database Management
"""

import sys
import sqlite3
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, asdict

from .config import DB_PATH, DATA_DIR


@dataclass
class Recording:
    """Recording data class"""
    id: int
    file_path: str
    original_filename: str
    duration_seconds: float
    language: str
    transcript: str
    summary: str
    processed_at: str
    source: str  # telegram, file, mic
    speaker: Optional[str]
    tags: Optional[str]
    created_at: str


@dataclass
class ActionItem:
    """Action item data class"""
    id: int
    recording_id: int
    type: str  # task, reminder, call, email, meeting, decision, deadline
    description: str
    assigned_to: Optional[str]
    due_date: Optional[str]
    completed: bool
    completed_at: Optional[str]
    priority: str  # low, medium, high
    created_at: str


@dataclass
class Speaker:
    """Speaker data class"""
    id: int
    name: str
    voice_profile_hash: Optional[str]
    notes: Optional[str]
    created_at: str


class Database:
    """Database management for nex-voice"""

    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path
        self.connection: Optional[sqlite3.Connection] = None
        self.ensure_connection()
        self.init_db()

    def ensure_connection(self) -> None:
        """Ensure database connection is open"""
        if self.connection is None:
            self.connection = sqlite3.connect(str(self.db_path))
            self.connection.row_factory = sqlite3.Row

    def close(self) -> None:
        """Close database connection"""
        if self.connection:
            self.connection.close()
            self.connection = None

    def init_db(self) -> None:
        """Initialize database tables"""
        cursor = self.connection.cursor()

        # Recordings table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS recordings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_path TEXT NOT NULL UNIQUE,
                original_filename TEXT NOT NULL,
                duration_seconds REAL NOT NULL,
                language TEXT DEFAULT 'nl',
                transcript TEXT NOT NULL,
                summary TEXT,
                processed_at TIMESTAMP,
                source TEXT DEFAULT 'file',
                speaker TEXT,
                tags TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Action items table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS action_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                recording_id INTEGER NOT NULL,
                type TEXT NOT NULL,
                description TEXT NOT NULL,
                assigned_to TEXT,
                due_date TEXT,
                completed BOOLEAN DEFAULT 0,
                completed_at TIMESTAMP,
                priority TEXT DEFAULT 'medium',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (recording_id) REFERENCES recordings(id) ON DELETE CASCADE
            )
        """)

        # Speakers table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS speakers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                voice_profile_hash TEXT,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Full-text search index for transcripts
        cursor.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS recordings_fts
            USING fts5(transcript, content=recordings, content_rowid=id)
        """)

        self.connection.commit()

    def save_recording(
        self,
        file_path: str,
        original_filename: str,
        duration_seconds: float,
        transcript: str,
        language: str = "nl",
        summary: Optional[str] = None,
        source: str = "file",
        speaker: Optional[str] = None,
        tags: Optional[str] = None,
    ) -> int:
        """Save recording to database"""
        cursor = self.connection.cursor()

        cursor.execute("""
            INSERT INTO recordings
            (file_path, original_filename, duration_seconds, transcript, language,
             summary, processed_at, source, speaker, tags)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            file_path, original_filename, duration_seconds, transcript, language,
            summary, datetime.now().isoformat(), source, speaker, tags
        ))

        recording_id = cursor.lastrowid

        # Insert into FTS index
        cursor.execute("""
            INSERT INTO recordings_fts(rowid, transcript)
            VALUES (?, ?)
        """, (recording_id, transcript))

        self.connection.commit()
        return recording_id

    def get_recording(self, recording_id: int) -> Optional[Recording]:
        """Get recording by ID"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM recordings WHERE id = ?", (recording_id,))
        row = cursor.fetchone()

        if row:
            return Recording(**dict(row))
        return None

    def list_recordings(
        self,
        since: Optional[str] = None,
        speaker: Optional[str] = None,
        tag: Optional[str] = None,
    ) -> List[Recording]:
        """List recordings with optional filters"""
        query = "SELECT * FROM recordings WHERE 1=1"
        params = []

        if since:
            query += " AND created_at >= ?"
            params.append(since)

        if speaker:
            query += " AND speaker = ?"
            params.append(speaker)

        if tag:
            query += " AND tags LIKE ?"
            params.append(f"%{tag}%")

        query += " ORDER BY created_at DESC"

        cursor = self.connection.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()

        return [Recording(**dict(row)) for row in rows]

    def search_recordings(self, query: str) -> List[Dict[str, Any]]:
        """Full-text search recordings"""
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT r.id, r.original_filename, r.transcript, r.created_at
            FROM recordings r
            JOIN recordings_fts f ON r.id = f.rowid
            WHERE f.transcript MATCH ?
            ORDER BY rank
        """, (query,))

        results = []
        for row in cursor.fetchall():
            results.append({
                "id": row[0],
                "filename": row[1],
                "transcript": row[2],
                "created_at": row[3],
            })
        return results

    def save_action_item(
        self,
        recording_id: int,
        type: str,
        description: str,
        assigned_to: Optional[str] = None,
        due_date: Optional[str] = None,
        priority: str = "medium",
    ) -> int:
        """Save action item"""
        cursor = self.connection.cursor()

        cursor.execute("""
            INSERT INTO action_items
            (recording_id, type, description, assigned_to, due_date, priority)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (recording_id, type, description, assigned_to, due_date, priority))

        self.connection.commit()
        return cursor.lastrowid

    def list_action_items(
        self,
        recording_id: Optional[int] = None,
        type: Optional[str] = None,
        completed: bool = False,
        overdue: bool = False,
    ) -> List[ActionItem]:
        """List action items with optional filters"""
        query = "SELECT * FROM action_items WHERE completed = ?"
        params = [1 if completed else 0]

        if recording_id:
            query += " AND recording_id = ?"
            params.append(recording_id)

        if type:
            query += " AND type = ?"
            params.append(type)

        if overdue:
            query += " AND due_date < ? AND completed = 0"
            params.append(datetime.now().date().isoformat())

        query += " ORDER BY created_at DESC"

        cursor = self.connection.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()

        return [ActionItem(**dict(row)) for row in rows]

    def complete_action_item(self, action_id: int) -> None:
        """Mark action item as complete"""
        cursor = self.connection.cursor()

        cursor.execute("""
            UPDATE action_items
            SET completed = 1, completed_at = ?
            WHERE id = ?
        """, (datetime.now().isoformat(), action_id))

        self.connection.commit()

    def get_pending_actions(self) -> List[ActionItem]:
        """Get all pending action items"""
        return self.list_action_items(completed=False)

    def get_recording_stats(self) -> Dict[str, Any]:
        """Get recording statistics"""
        cursor = self.connection.cursor()

        # Total recordings
        cursor.execute("SELECT COUNT(*) FROM recordings")
        total_recordings = cursor.fetchone()[0]

        # Total duration
        cursor.execute("SELECT SUM(duration_seconds) FROM recordings")
        total_duration = cursor.fetchone()[0] or 0

        # Languages
        cursor.execute("""
            SELECT language, COUNT(*) as count
            FROM recordings
            GROUP BY language
        """)
        languages = {row[0]: row[1] for row in cursor.fetchall()}

        # Action items
        cursor.execute("SELECT COUNT(*) FROM action_items WHERE completed = 0")
        pending_actions = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM action_items WHERE completed = 1")
        completed_actions = cursor.fetchone()[0]

        # Overdue
        cursor.execute("""
            SELECT COUNT(*) FROM action_items
            WHERE due_date < ? AND completed = 0
        """, (datetime.now().date().isoformat(),))
        overdue = cursor.fetchone()[0]

        return {
            "total_recordings": total_recordings,
            "total_duration_seconds": total_duration,
            "total_duration_hours": round(total_duration / 3600, 2),
            "languages": languages,
            "pending_actions": pending_actions,
            "completed_actions": completed_actions,
            "overdue_actions": overdue,
        }

    def export_transcript(self, recording_id: int, format: str = "txt") -> str:
        """Export transcript in given format"""
        recording = self.get_recording(recording_id)

        if not recording:
            raise ValueError(f"Recording {recording_id} not found")

        if format == "json":
            # Get action items for this recording
            actions = self.list_action_items(recording_id=recording_id)

            data = {
                "id": recording.id,
                "filename": recording.original_filename,
                "created_at": recording.created_at,
                "duration_seconds": recording.duration_seconds,
                "language": recording.language,
                "speaker": recording.speaker,
                "tags": recording.tags,
                "transcript": recording.transcript,
                "summary": recording.summary,
                "action_items": [
                    {
                        "id": a.id,
                        "type": a.type,
                        "description": a.description,
                        "assigned_to": a.assigned_to,
                        "due_date": a.due_date,
                        "priority": a.priority,
                        "completed": a.completed,
                    }
                    for a in actions
                ],
            }
            return json.dumps(data, indent=2)

        else:  # txt format
            lines = [
                f"Recording: {recording.original_filename}",
                f"Date: {recording.created_at}",
                f"Duration: {recording.duration_seconds:.1f} seconds",
                f"Language: {recording.language}",
                f"Speaker: {recording.speaker or 'Unknown'}",
                f"Tags: {recording.tags or 'None'}",
                "",
                "TRANSCRIPT",
                "---",
                recording.transcript,
            ]

            if recording.summary:
                lines.extend(["", "SUMMARY", "---", recording.summary])

            # Get action items
            actions = self.list_action_items(recording_id=recording_id)
            if actions:
                lines.extend(["", "ACTION ITEMS", "---"])
                for action in actions:
                    status = "✓" if action.completed else "○"
                    lines.append(f"[{status}] {action.type.upper()}: {action.description}")
                    if action.assigned_to:
                        lines.append(f"    Assigned to: {action.assigned_to}")
                    if action.due_date:
                        lines.append(f"    Due: {action.due_date}")

            return "\n".join(lines)


def init_db_cli():
    """CLI entry point for database initialization"""
    db = Database()
    print(f"Database initialized at {DB_PATH}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--init":
        init_db_cli()
    else:
        db = Database()
        stats = db.get_recording_stats()
        print(json.dumps(stats, indent=2))
