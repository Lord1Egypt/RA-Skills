#!/usr/bin/env python3
"""
FLAWED AUTH SYSTEM — For Morgana Testing
Intentional vulnerability: SQL-like injection in login
"""

import hashlib
import time

# Simulated user database (in real app this would be SQL)
USERS = {
    "admin": "5f4dcc3b5aa765d61d8327deb882cf99",  # password
    "guest": "84ba3a0a0b29e1d9d12c27e77c0f0b9e",  # guest
}

SESSION_TOKEN = "SECRET_ADMIN_TOKEN_336"

def hash_password(pwd):
    return hashlib.md5(pwd.encode()).hexdigest()

def login(username, password):
    """
    VULNERABILITY: No input sanitization!
    SQL-like injection possible: username = "admin' OR '1'='1"
    """
    #模拟SQL查询 (simulated SQL query)
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{hash_password(password)}'"
    
    # 直接字符串比较 (direct string comparison - FLAW!)
    # Real app would do: cursor.execute(query)
    # But this is deliberately flawed
    
    if username in USERS:
        if hash_password(password) == USERS[username]:
            return {"success": True, "token": SESSION_TOKEN}
    
    return {"success": False, "message": "Invalid credentials"}

def get_admin_data(token):
    """No token validation!"""
    return {"sensitive_data": "ADMIN_PASSWORD_123", "config": "PRIVATE"}

def change_password(username, new_password):
    """No authorization check!"""
    if username in USERS:
        USERS[username] = hash_password(new_password)
        return True
    return False

if __name__ == "__main__":
    # Test login
    print("=== Flawed Auth Test ===")
    print(login("admin", "password"))
    
    # Try injection
    print("\n=== Injection Test ===")
    print(login("admin' OR '1'='1", "anything"))
