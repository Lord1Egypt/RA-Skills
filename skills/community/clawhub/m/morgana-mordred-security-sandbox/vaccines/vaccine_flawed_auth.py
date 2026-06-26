#!/usr/bin/env python3
"""
VACCINE: flawed_auth.py
Patch for SQL Injection + Auth Bypass vulnerability

APPLIQUER CE PATCH POUR CORRIGER:
- SQL Injection via input non-sanitized
- Auth bypass via ' OR '1'='1' payload
"""

import sqlite3
from typing import Optional, Tuple

class SecureAuth:
    """Version sécurisée de l'authentification."""
    
    def __init__(self, db_path: str = ":memory:"):
        self.conn = sqlite3.connect(db_path)
        self._init_db()
    
    def _init_db(self):
        """Initialise la DB avec des données de test."""
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE,
                password TEXT,
                role TEXT DEFAULT 'user'
            )
        """)
        # Ajouter un admin
        cursor.execute(
            "INSERT OR IGNORE INTO users (username, password, role) VALUES (?, ?, ?)",
            ("admin", "SecureP@ssw0rd!", "admin")
        )
        self.conn.commit()
    
    def authenticate(self, username: str, password: str) -> Tuple[bool, Optional[str]]:
        """
        Authentification SÉCURISÉE avec requêtes paramétrées.
        
        VULNÉRABILITÉ CORRIGÉE:
        - AVANT: f"SELECT * FROM users WHERE username = '{username}'..."
        - APRÈS: "SELECT * FROM users WHERE username = ? AND password = ?", (username, password)
        """
        cursor = self.conn.cursor()
        
        # ✅ UTILISER DES PARAMÈTRES (PRÉVIENT SQL INJECTION)
        cursor.execute(
            "SELECT role FROM users WHERE username = ? AND password = ?",
            (username, password)
        )
        result = cursor.fetchone()
        
        if result:
            return True, result[0]  # (success, role)
        return False, None
    
    def authenticate_unsafe(self, username: str, password: str) -> bool:
        """
        Version VULNÉRABLE - POUR TEST SEULEMENT
        NE PAS UTILISER EN PRODUCTION
        """
        cursor = self.conn.cursor()
        
        # ❌ VULNÉRABLE: String formatting (SQL Injection possible)
        query = f"SELECT role FROM users WHERE username = '{username}' AND password = '{password}'"
        cursor.execute(query)
        result = cursor.fetchone()
        
        return result is not None


def test_vaccine():
    """Test le vaccine."""
    auth = SecureAuth()
    
    # Test payloads known to exploit the vulnerable version
    test_cases = [
        # (username, password, should_succeed, description)
        ("admin", "SecureP@ssw0rd!", True, "Legitimate login"),
        ("admin", "wrong_password", False, "Wrong password"),
        ("admin' OR '1'='1' --", "anything", False, "SQL Injection attempt - BLOCKED"),
        ("' OR 1=1 --", "anything", False, "SQL Injection attempt - BLOCKED"),
        ("admin", "' OR '1'='1", False, "SQL Injection in password - BLOCKED"),
    ]
    
    print("🧪 TESTING SECURE AUTHENTICATION")
    print("=" * 60)
    
    all_passed = True
    for username, password, should_succeed, description in test_cases:
        success, role = auth.authenticate(username, password)
        status = "✅ PASS" if (success == should_succeed) else "❌ FAIL"
        
        if success != should_succeed:
            all_passed = False
        
        print(f"{status}: {description}")
        print(f"       Input: username='{username}', password='{password}'")
        print(f"       Expected: {should_succeed}, Got: {success}")
        print()
    
    print("=" * 60)
    if all_passed:
        print("✅ ALL TESTS PASSED - VACCINE EFFECTIVE!")
    else:
        print("❌ SOME TESTS FAILED - VACCINE NEEDS REVIEW")
    
    return all_passed


if __name__ == "__main__":
    test_vaccine()
