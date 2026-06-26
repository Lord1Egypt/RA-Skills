#!/usr/bin/env python3
"""
GitHub Assistant Configuration Module

This module provides centralized configuration for data storage paths.
All user data (tokens, auth sessions, browser data) is stored in the user's
home directory (~/.github-assistant/) instead of the skill folder to:
1. Keep sensitive data separate from code
2. Avoid accidental commits of credentials
3. Persist data across skill updates
"""

import os

# Base data directory in user's home folder
DATA_DIR = os.path.expanduser("~/.github-assistant")

# Token file for API authentication
TOKEN_FILE = os.path.join(DATA_DIR, "github_token.txt")

# Browser session state file (cookies, localStorage)
AUTH_STATE_FILE = os.path.join(DATA_DIR, "github_auth.json")

# Browser persistent context data directory
BROWSER_DATA_DIR = os.path.join(DATA_DIR, "browser_data")


def ensure_data_dir():
    """Ensure the data directory exists"""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    return DATA_DIR


def ensure_browser_data_dir():
    """Ensure the browser data directory exists"""
    if not os.path.exists(BROWSER_DATA_DIR):
        os.makedirs(BROWSER_DATA_DIR)
    return BROWSER_DATA_DIR


def get_token_file():
    """Get the token file path, ensuring directory exists"""
    ensure_data_dir()
    return TOKEN_FILE


def get_auth_state_file():
    """Get the auth state file path, ensuring directory exists"""
    ensure_data_dir()
    return AUTH_STATE_FILE


def get_browser_data_dir():
    """Get the browser data directory path, ensuring it exists"""
    ensure_data_dir()
    return ensure_browser_data_dir()


def get_stored_token():
    """Get the stored token if it exists"""
    token_file = get_token_file()
    if os.path.exists(token_file):
        with open(token_file) as f:
            return f.read().strip()
    return ""


def save_token(token):
    """Save token to file"""
    token_file = get_token_file()
    with open(token_file, "w") as f:
        f.write(token.strip())
    return token_file


def has_token():
    """Check if a token file exists"""
    return os.path.exists(TOKEN_FILE)


def has_browser_session():
    """Check if a browser session exists"""
    return os.path.exists(AUTH_STATE_FILE)


def clear_credentials():
    """Remove all stored credentials"""
    removed = []
    
    if os.path.exists(TOKEN_FILE):
        os.remove(TOKEN_FILE)
        removed.append("token")
    
    if os.path.exists(AUTH_STATE_FILE):
        os.remove(AUTH_STATE_FILE)
        removed.append("browser_session")
    
    # Clear browser data directory
    if os.path.exists(BROWSER_DATA_DIR):
        import shutil
        shutil.rmtree(BROWSER_DATA_DIR)
        removed.append("browser_data")
    
    return removed