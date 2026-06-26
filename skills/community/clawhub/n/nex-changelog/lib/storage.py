"""Database storage and retrieval for changelog entries."""

import sqlite3
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
from .config import DB_PATH, CHANGE_TYPES, AUDIENCE_TYPES


class ChangelogDB:
    """SQLite-based changelog database."""

    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.init_db()

    def _get_connection(self):
        """Get database connection."""
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self):
        """Initialize database schema."""
        conn = self._get_connection()
        cursor = conn.cursor()

        # Projects table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                repo_path TEXT,
                current_version TEXT,
                client_name TEXT,
                client_email TEXT,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Changelog entries table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS changelog_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER NOT NULL,
                version TEXT,
                change_type TEXT NOT NULL,
                description TEXT NOT NULL,
                audience TEXT,
                details TEXT,
                author TEXT,
                commit_hash TEXT,
                breaking BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (project_id) REFERENCES projects(id)
            )
        """)

        # Releases table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS releases (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER NOT NULL,
                version TEXT NOT NULL,
                release_date TIMESTAMP,
                summary TEXT,
                client_notes TEXT,
                internal_notes TEXT,
                telegram_sent BOOLEAN DEFAULT 0,
                email_sent BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (project_id) REFERENCES projects(id),
                UNIQUE(project_id, version)
            )
        """)

        # Create indexes for performance
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_entries_project ON changelog_entries(project_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_entries_version ON changelog_entries(version)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_entries_type ON changelog_entries(change_type)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_entries_audience ON changelog_entries(audience)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_releases_project ON releases(project_id)")

        conn.commit()
        conn.close()

    def save_project(self, name: str, repo_path: Optional[str] = None,
                    client_name: Optional[str] = None, client_email: Optional[str] = None,
                    description: Optional[str] = None) -> int:
        """Save or update a project. Returns project_id."""
        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO projects (name, repo_path, client_name, client_email, description)
                VALUES (?, ?, ?, ?, ?)
            """, (name, repo_path, client_name, client_email, description))
            conn.commit()
            project_id = cursor.lastrowid
        except sqlite3.IntegrityError:
            # Update existing project
            cursor.execute("""
                UPDATE projects
                SET repo_path = COALESCE(?, repo_path),
                    client_name = COALESCE(?, client_name),
                    client_email = COALESCE(?, client_email),
                    description = COALESCE(?, description)
                WHERE name = ?
            """, (repo_path, client_name, client_email, description, name))
            conn.commit()
            cursor.execute("SELECT id FROM projects WHERE name = ?", (name,))
            project_id = cursor.fetchone()[0]

        conn.close()
        return project_id

    def get_project(self, name: str) -> Optional[Dict]:
        """Get a project by name."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM projects WHERE name = ?", (name,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return dict(row)
        return None

    def get_project_by_id(self, project_id: int) -> Optional[Dict]:
        """Get a project by ID."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM projects WHERE id = ?", (project_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return dict(row)
        return None

    def list_projects(self) -> List[Dict]:
        """List all projects."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM projects ORDER BY created_at DESC")
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    def save_entry(self, project_id: int, version: Optional[str],
                  change_type: str, description: str,
                  audience: Optional[str] = None, details: Optional[str] = None,
                  author: Optional[str] = None, commit_hash: Optional[str] = None,
                  breaking: bool = False) -> int:
        """Save a changelog entry. Returns entry_id."""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO changelog_entries
            (project_id, version, change_type, description, audience, details, author, commit_hash, breaking)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (project_id, version, change_type, description, audience, details, author, commit_hash, breaking))

        conn.commit()
        entry_id = cursor.lastrowid
        conn.close()
        return entry_id

    def list_entries(self, project_id: Optional[int] = None, version: Optional[str] = None,
                    change_type: Optional[str] = None, audience: Optional[str] = None) -> List[Dict]:
        """List changelog entries with optional filters."""
        conn = self._get_connection()
        cursor = conn.cursor()

        query = "SELECT * FROM changelog_entries WHERE 1=1"
        params = []

        if project_id is not None:
            query += " AND project_id = ?"
            params.append(project_id)
        if version is not None:
            query += " AND version = ?"
            params.append(version)
        if change_type is not None:
            query += " AND change_type = ?"
            params.append(change_type)
        if audience is not None:
            query += " AND audience = ?"
            params.append(audience)

        query += " ORDER BY created_at DESC"
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    def create_release(self, project_id: int, version: str, summary: Optional[str] = None,
                      client_notes: Optional[str] = None, internal_notes: Optional[str] = None) -> int:
        """Create a release. Returns release_id."""
        conn = self._get_connection()
        cursor = conn.cursor()

        # Update project current_version
        cursor.execute("UPDATE projects SET current_version = ? WHERE id = ?", (version, project_id))

        try:
            cursor.execute("""
                INSERT INTO releases (project_id, version, release_date, summary, client_notes, internal_notes)
                VALUES (?, ?, CURRENT_TIMESTAMP, ?, ?, ?)
            """, (project_id, version, summary, client_notes, internal_notes))
            conn.commit()
            release_id = cursor.lastrowid
        except sqlite3.IntegrityError:
            cursor.execute("""
                UPDATE releases
                SET release_date = CURRENT_TIMESTAMP,
                    summary = COALESCE(?, summary),
                    client_notes = COALESCE(?, client_notes),
                    internal_notes = COALESCE(?, internal_notes)
                WHERE project_id = ? AND version = ?
            """, (summary, client_notes, internal_notes, project_id, version))
            conn.commit()
            cursor.execute("SELECT id FROM releases WHERE project_id = ? AND version = ?", (project_id, version))
            release_id = cursor.fetchone()[0]

        conn.close()
        return release_id

    def get_release(self, project_id: int, version: str) -> Optional[Dict]:
        """Get a specific release."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM releases WHERE project_id = ? AND version = ?", (project_id, version))
        row = cursor.fetchone()
        conn.close()

        if row:
            return dict(row)
        return None

    def list_releases(self, project_id: Optional[int] = None) -> List[Dict]:
        """List releases."""
        conn = self._get_connection()
        cursor = conn.cursor()

        if project_id is not None:
            cursor.execute("""
                SELECT * FROM releases WHERE project_id = ?
                ORDER BY release_date DESC
            """, (project_id,))
        else:
            cursor.execute("SELECT * FROM releases ORDER BY release_date DESC")

        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    def get_unreleased_entries(self, project_id: int) -> List[Dict]:
        """Get entries that haven't been released yet."""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM changelog_entries
            WHERE project_id = ? AND version IS NULL
            ORDER BY created_at DESC
        """, (project_id,))

        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    def search_entries(self, query: str, project_id: Optional[int] = None) -> List[Dict]:
        """Search entries by description or details (simple text search)."""
        conn = self._get_connection()
        cursor = conn.cursor()

        sql = """
            SELECT * FROM changelog_entries
            WHERE (description LIKE ? OR details LIKE ?)
        """
        params = [f"%{query}%", f"%{query}%"]

        if project_id is not None:
            sql += " AND project_id = ?"
            params.append(project_id)

        sql += " ORDER BY created_at DESC"
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    def export_changelog(self, project_id: int, version: Optional[str] = None) -> str:
        """Export changelog as markdown. Returns markdown string."""
        conn = self._get_connection()
        cursor = conn.cursor()

        # Get project info
        cursor.execute("SELECT * FROM projects WHERE id = ?", (project_id,))
        project = dict(cursor.fetchone())

        # Get entries
        if version:
            cursor.execute("""
                SELECT * FROM changelog_entries
                WHERE project_id = ? AND version = ?
                ORDER BY change_type, created_at DESC
            """, (project_id, version))
        else:
            cursor.execute("""
                SELECT * FROM changelog_entries
                WHERE project_id = ?
                ORDER BY version DESC, change_type, created_at DESC
            """, (project_id,))

        entries = [dict(row) for row in cursor.fetchall()]
        conn.close()

        # Build markdown
        markdown = f"# {project['name']}\n\n"
        if project['description']:
            markdown += f"{project['description']}\n\n"

        if not entries:
            markdown += "No changelog entries.\n"
            return markdown

        # Group by version
        by_version = {}
        for entry in entries:
            v = entry['version'] or 'Unreleased'
            if v not in by_version:
                by_version[v] = []
            by_version[v].append(entry)

        # Output by version
        for version_key in sorted(by_version.keys(), reverse=True):
            markdown += f"## {version_key}\n\n"
            version_entries = by_version[version_key]

            # Group by type
            by_type = {}
            for entry in version_entries:
                t = entry['change_type']
                if t not in by_type:
                    by_type[t] = []
                by_type[t].append(entry)

            for type_key in sorted(by_type.keys()):
                type_name = CHANGE_TYPES.get(type_key, type_key)
                markdown += f"### {type_name}\n\n"
                for entry in by_type[type_key]:
                    markdown += f"- {entry['description']}\n"
                markdown += "\n"

        return markdown
