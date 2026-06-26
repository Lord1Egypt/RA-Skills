#!/usr/bin/env python3
# Nex GDPR - Data Scanner
# MIT-0 License - Copyright 2026 Nex AI (Kevin Blancaflor)

import os
import re
from pathlib import Path
from typing import List, Dict, Optional
import json

from .config import (
    SESSION_DIRS,
    MEMORY_DIR,
    LOG_DIR,
    UPLOAD_DIR,
    DB_FILES,
    PII_ANONYMIZE_PATTERNS,
)


class DataScanner:
    """Scan system for user data and PII."""

    def __init__(self):
        self.pii_patterns = [
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",  # Email
            r"\+?1?\d{9,15}",  # Phone numbers
            r"\b\d{8}\b",  # Belgian national number (YYYYMMDD)
            r"\bBE\d{10}\b",  # Belgian VAT number
            r"\b\d{3}-\d{2}-\d{4}\b",  # SSN format
            r"\b\d{2}/\d{2}/\d{4}\b",  # Date format
        ]

    def scan_for_user_data(
        self, user_identifier: str, scan_paths: Optional[List[str]] = None
    ) -> List[Dict]:
        """
        Search all configured paths for files/data related to the user.
        Returns list of findings with path, type, size, contains_pii flag.
        """
        findings = []

        if not scan_paths:
            scan_paths = [
                str(p) for p in SESSION_DIRS if p and os.path.exists(p)
            ] + [MEMORY_DIR, LOG_DIR, UPLOAD_DIR]
            scan_paths = [p for p in scan_paths if p and os.path.exists(p)]

        for scan_path in scan_paths:
            if not scan_path or not os.path.exists(scan_path):
                continue

            path_obj = Path(scan_path)
            if path_obj.is_file():
                result = self._search_file(scan_path, user_identifier)
                if result:
                    findings.append(result)
            elif path_obj.is_dir():
                for file_path in path_obj.rglob("*"):
                    if file_path.is_file():
                        result = self._search_file(str(file_path), user_identifier)
                        if result:
                            findings.append(result)

        return findings

    def scan_sessions(self, user_identifier: str) -> List[Dict]:
        """Scan OpenClaw session directories for user-related sessions."""
        findings = []

        for session_dir in SESSION_DIRS:
            if not session_dir or not os.path.exists(session_dir):
                continue

            path_obj = Path(session_dir)
            for session_file in path_obj.rglob("*"):
                if session_file.is_file() and not session_file.name.startswith("."):
                    result = self._search_file(str(session_file), user_identifier)
                    if result:
                        result["data_source"] = "sessions"
                        findings.append(result)

        return findings

    def scan_memory(self, user_identifier: str) -> List[Dict]:
        """Scan agent memory files for user references."""
        findings = []

        if not os.path.exists(MEMORY_DIR):
            return findings

        for mem_file in Path(MEMORY_DIR).rglob("*"):
            if mem_file.is_file():
                result = self._search_file(str(mem_file), user_identifier)
                if result:
                    result["data_source"] = "memory"
                    findings.append(result)

        return findings

    def scan_logs(self, user_identifier: str) -> List[Dict]:
        """Scan log files for user data."""
        findings = []

        if not os.path.exists(LOG_DIR):
            return findings

        for log_file in Path(LOG_DIR).rglob("*.log"):
            if log_file.is_file():
                result = self._search_file(str(log_file), user_identifier)
                if result:
                    result["data_source"] = "logs"
                    findings.append(result)

        return findings

    def scan_databases(self, user_identifier: str) -> List[Dict]:
        """Scan SQLite databases from other nex-* skills for user data."""
        findings = []

        for db_file in DB_FILES:
            db_path = Path(db_file)
            if not db_path.exists():
                continue

            # Try to open and search database
            try:
                import sqlite3

                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()

                # Get all tables
                cursor.execute(
                    "SELECT name FROM sqlite_master WHERE type='table';"
                )
                tables = cursor.fetchall()

                for (table_name,) in tables:
                    # Get columns
                    cursor.execute(f"PRAGMA table_info({table_name})")
                    columns = cursor.fetchall()

                    # Search in string columns
                    for col_info in columns:
                        col_name = col_info[1]
                        col_type = col_info[2]

                        if "text" in col_type.lower() or "char" in col_type.lower():
                            query = f"SELECT COUNT(*) FROM {table_name} WHERE {col_name} LIKE ?"
                            try:
                                cursor.execute(query, (f"%{user_identifier}%",))
                                count = cursor.fetchone()[0]
                                if count > 0:
                                    pii = self._detect_pii_in_db(
                                        conn, table_name, col_name
                                    )
                                    findings.append(
                                        {
                                            "file_path": str(db_path),
                                            "data_source": "database",
                                            "data_type": f"{table_name}.{col_name}",
                                            "description": f"Found {count} matches in database table '{table_name}' column '{col_name}'",
                                            "size_bytes": db_path.stat().st_size,
                                            "contains_pii": pii,
                                        }
                                    )
                            except Exception:
                                pass

                conn.close()
            except Exception:
                pass

        return findings

    def _search_file(self, file_path: str, identifier: str) -> Optional[Dict]:
        """Search a single file for user identifier (grep-like)."""
        try:
            # Check if file is readable and not too large (>100MB)
            file_obj = Path(file_path)
            if file_obj.stat().st_size > 100 * 1024 * 1024:
                return None

            # Try to read as text
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
            except Exception:
                return None

            # Search for identifier
            if identifier.lower() not in content.lower():
                return None

            # Count occurrences
            occurrences = content.lower().count(identifier.lower())

            # Detect PII in file
            pii_detected = self._detect_pii(content)

            return {
                "file_path": file_path,
                "data_source": "file",
                "data_type": "personal_data",
                "description": f"Found '{identifier}' {occurrences} time(s)",
                "size_bytes": file_obj.stat().st_size,
                "contains_pii": len(pii_detected) > 0,
                "pii_types": pii_detected,
            }

        except Exception:
            return None

    def _detect_pii(self, text: str) -> List[str]:
        """Detect PII patterns in text."""
        detected = []

        if re.search(self.pii_patterns[0], text):
            detected.append("email")
        if re.search(self.pii_patterns[1], text):
            detected.append("phone")
        if re.search(self.pii_patterns[2], text):
            detected.append("national_number")
        if re.search(self.pii_patterns[3], text):
            detected.append("vat_number")
        if re.search(self.pii_patterns[4], text):
            detected.append("ssn")
        if re.search(self.pii_patterns[5], text):
            detected.append("date")

        return list(set(detected))

    def _detect_pii_in_db(self, conn, table_name: str, col_name: str) -> bool:
        """Check if database column contains PII."""
        import sqlite3

        try:
            cursor = conn.cursor()
            cursor.execute(f"SELECT {col_name} FROM {table_name} LIMIT 10")
            rows = cursor.fetchall()

            for (value,) in rows:
                if value and isinstance(value, str):
                    pii = self._detect_pii(value)
                    if pii:
                        return True

            return False
        except Exception:
            return False

    def estimate_data_size(self, findings: List[Dict]) -> int:
        """Calculate total data size from findings."""
        total = 0
        for finding in findings:
            total += finding.get("size_bytes", 0)
        return total
