#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Kwai Life Service - API Key Manager.

Features:
- Parse api_key (format: {app_key}#{merchant_id}#{app_secret})
- Store multiple api_keys to local file
- List all stored api_keys for user selection
- Save current selection to context file
- Get current app_key, merchant_id, app_secret
- Delete api_key by index

Storage files:
  - api_keys file: ./.kuaishou-localife-token/api_keys.txt
  - current context: ./.kuaishou-localife-token/current_context.txt

Usage:
  # Add an api_key
  python3 scripts/api_key_manager.py --add "app_key#merchant_id#app_secret"
  
  # List all api_keys
  python3 scripts/api_key_manager.py --list
  
  # Select an api_key by index
  python3 scripts/api_key_manager.py --select 1
  
  # Delete an api_key by index
  python3 scripts/api_key_manager.py --delete 1
  
  # Show current selection
  python3 scripts/api_key_manager.py --current
  
  # Get current config (for script usage)
  python3 scripts/api_key_manager.py --get-config
"""

import argparse
import json
import os
import sys
from dataclasses import dataclass
from typing import List, Optional, Tuple

DEFAULT_TOKEN_BASE_DIR = "./.kuaishou-localife-token/"
API_KEYS_FILE = os.path.join(DEFAULT_TOKEN_BASE_DIR, "api_keys.txt")
CURRENT_CONTEXT_FILE = os.path.join(DEFAULT_TOKEN_BASE_DIR, "current_context.txt")


@dataclass
class ApiKeyInfo:
    """Represents a parsed API key."""
    app_key: str
    merchant_id: str
    app_secret: str
    
    def to_line(self) -> str:
        """Convert to storage line format: app_key#merchant_id#app_secret"""
        return f"{self.app_key}#{self.merchant_id}#{self.app_secret}"
    
    @staticmethod
    def from_line(line: str) -> Optional['ApiKeyInfo']:
        """Parse from storage line format."""
        line = line.strip()
        if not line:
            return None
        parts = line.split('#')
        if len(parts) != 3:
            return None
        return ApiKeyInfo(app_key=parts[0], merchant_id=parts[1], app_secret=parts[2])
    
    def display_name(self) -> str:
        """Return a human-readable display name."""
        return f"app_key={self.app_key}, merchant_id={self.merchant_id}"


class ApiKeyManager:
    """Manager for API keys storage and selection."""
    
    def __init__(self, token_base_dir: str = DEFAULT_TOKEN_BASE_DIR):
        self.token_base_dir = token_base_dir
        self.api_keys_file = os.path.join(token_base_dir, "api_keys.txt")
        self.current_context_file = os.path.join(token_base_dir, "current_context.txt")
        
    def _ensure_dir(self) -> None:
        """Ensure the token directory exists."""
        if not os.path.exists(self.token_base_dir):
            os.makedirs(self.token_base_dir, exist_ok=True)
    
    def parse_api_key(self, api_key_str: str) -> Optional[ApiKeyInfo]:
        """Parse an API key string.
        
        Format: {app_key}#{merchant_id}#{app_secret}
        """
        parts = api_key_str.strip().split('#')
        if len(parts) != 3:
            return None
        app_key, merchant_id, app_secret = parts
        if not all([app_key, merchant_id, app_secret]):
            return None
        return ApiKeyInfo(app_key=app_key, merchant_id=merchant_id, app_secret=app_secret)
    
    def load_all_api_keys(self) -> List[ApiKeyInfo]:
        """Load all stored API keys."""
        if not os.path.exists(self.api_keys_file):
            return []
        
        keys = []
        try:
            with open(self.api_keys_file, "r", encoding="utf-8") as f:
                for line in f:
                    key_info = ApiKeyInfo.from_line(line)
                    if key_info:
                        keys.append(key_info)
        except Exception:
            pass
        return keys
    
    def save_all_api_keys(self, keys: List[ApiKeyInfo]) -> None:
        """Save all API keys to file."""
        self._ensure_dir()
        with open(self.api_keys_file, "w", encoding="utf-8") as f:
            for key in keys:
                f.write(key.to_line() + "\n")
    
    def add_api_key(self, api_key_str: str) -> Tuple[bool, str]:
        """Add a new API key.
        
        Returns:
            (success, message)
        """
        key_info = self.parse_api_key(api_key_str)
        if not key_info:
            return False, f"Invalid API key format. Expected: {{app_key}}#{{merchant_id}}#{{app_secret}}"
        
        keys = self.load_all_api_keys()
        
        # Check if already exists
        for existing in keys:
            if (existing.app_key == key_info.app_key and 
                existing.merchant_id == key_info.merchant_id):
                return True, f"API key already exists: {key_info.display_name()}"
        
        keys.append(key_info)
        self.save_all_api_keys(keys)
        return True, f"Added API key: {key_info.display_name()}"
    
    def list_api_keys(self) -> List[Tuple[int, ApiKeyInfo]]:
        """List all API keys with their indices (1-based)."""
        keys = self.load_all_api_keys()
        return [(i + 1, key) for i, key in enumerate(keys)]
    
    def select_api_key(self, index: int) -> Tuple[bool, str, Optional[ApiKeyInfo]]:
        """Select an API key by index (1-based).
        
        Returns:
            (success, message, selected_key)
        """
        keys = self.load_all_api_keys()
        
        if index < 1 or index > len(keys):
            return False, f"Invalid index. Valid range: 1-{len(keys)}", None
        
        selected = keys[index - 1]
        
        # Save to current context
        self._ensure_dir()
        with open(self.current_context_file, "w", encoding="utf-8") as f:
            f.write(selected.to_line() + "\n")
        
        return True, f"Selected: {selected.display_name()}", selected
    
    def get_current_context(self) -> Optional[ApiKeyInfo]:
        """Get the currently selected API key context."""
        if not os.path.exists(self.current_context_file):
            return None
        
        try:
            with open(self.current_context_file, "r", encoding="utf-8") as f:
                line = f.readline().strip()
                return ApiKeyInfo.from_line(line)
        except Exception:
            return None
    
    def get_current_context_or_prompt(self) -> Optional[ApiKeyInfo]:
        """Get current context, or return None to prompt user selection."""
        return self.get_current_context()
    
    def clear_current_context(self) -> None:
        """Clear the current selection."""
        if os.path.exists(self.current_context_file):
            os.remove(self.current_context_file)
    
    def delete_api_key(self, index: int) -> Tuple[bool, str]:
        """Delete an API key by index (1-based).
        
        Returns:
            (success, message)
        """
        keys = self.load_all_api_keys()
        
        if index < 1 or index > len(keys):
            return False, f"Invalid index. Valid range: 1-{len(keys)}"
        
        deleted = keys[index - 1]
        del keys[index - 1]
        self.save_all_api_keys(keys)
        
        # Clear current context if it was the deleted key
        current = self.get_current_context()
        if current and current.app_key == deleted.app_key and current.merchant_id == deleted.merchant_id:
            self.clear_current_context()
            return True, f"Deleted: {deleted.display_name()} (was current selection, cleared)"
        
        return True, f"Deleted: {deleted.display_name()}"


def print_selection_prompt(manager: ApiKeyManager) -> None:
    """Print a user-friendly selection prompt."""
    keys_with_index = manager.list_api_keys()
    
    if not keys_with_index:
        print("No API keys stored. Please add one first:")
        print('  python3 scripts/api_key_manager.py --add "app_key#merchant_id#app_secret"')
        return
    
    current = manager.get_current_context()
    
    print("Available API Keys:")
    print("-" * 60)
    for idx, key in keys_with_index:
        marker = " (current)" if current and current.app_key == key.app_key and current.merchant_id == key.merchant_id else ""
        print(f"  [{idx}] {key.display_name()}{marker}")
    print("-" * 60)
    print("\nTo select one:")
    print("  python3 scripts/api_key_manager.py --select <index>")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Kwai Life Service - API Key Manager",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Add an API key
  python3 scripts/api_key_manager.py --add "app_key#merchant_id#app_secret"
  
  # List all API keys
  python3 scripts/api_key_manager.py --list
  
  # Select an API key by index
  python3 scripts/api_key_manager.py --select 1
  
  # Delete an API key by index
  python3 scripts/api_key_manager.py --delete 1
  
  # Show current selection
  python3 scripts/api_key_manager.py --current
  
  # Get config as JSON (for scripting)
  python3 scripts/api_key_manager.py --get-config
"""
    )
    
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--add",
        metavar="API_KEY",
        help="Add a new API key (format: app_key#merchant_id#app_secret)"
    )
    group.add_argument(
        "--list",
        action="store_true",
        help="List all stored API keys"
    )
    group.add_argument(
        "--select",
        type=int,
        metavar="INDEX",
        help="Select an API key by index (1-based)"
    )
    group.add_argument(
        "--delete",
        type=int,
        metavar="INDEX",
        help="Delete an API key by index (1-based)"
    )
    group.add_argument(
        "--current",
        action="store_true",
        help="Show current selection"
    )
    group.add_argument(
        "--get-config",
        action="store_true",
        help="Output current config as JSON (for scripting)"
    )
    group.add_argument(
        "--prompt",
        action="store_true",
        help="Show selection prompt for user to choose"
    )
    
    args = parser.parse_args()
    manager = ApiKeyManager()
    
    if args.add:
        success, message = manager.add_api_key(args.add)
        print(message)
        sys.exit(0 if success else 1)
    
    elif args.list:
        keys_with_index = manager.list_api_keys()
        if not keys_with_index:
            print("No API keys stored.")
            sys.exit(0)
        
        current = manager.get_current_context()
        for idx, key in keys_with_index:
            marker = " (current)" if current and current.app_key == key.app_key and current.merchant_id == key.merchant_id else ""
            print(f"[{idx}] {key.display_name()}{marker}")
        sys.exit(0)
    
    elif args.select:
        success, message, _ = manager.select_api_key(args.select)
        print(message)
        sys.exit(0 if success else 1)
    
    elif args.delete:
        success, message = manager.delete_api_key(args.delete)
        print(message)
        sys.exit(0 if success else 1)
    
    elif args.current:
        current = manager.get_current_context()
        if current:
            print(f"Current: {current.display_name()}")
            print(f"  app_key: {current.app_key}")
            print(f"  merchant_id: {current.merchant_id}")
            print(f"  app_secret: {current.app_secret}")
        else:
            print("No API key selected. Use --select to choose one.")
            print_selection_prompt(manager)
        sys.exit(0)
    
    elif args.get_config:
        current = manager.get_current_context()
        if current:
            config = {
                "app_key": current.app_key,
                "merchant_id": current.merchant_id,
                "app_secret": current.app_secret,
            }
            print(json.dumps(config))
        else:
            print(json.dumps({}))
        sys.exit(0)
    
    elif args.prompt:
        print_selection_prompt(manager)
        sys.exit(0)
    
    else:
        # Default: show current or prompt selection
        current = manager.get_current_context()
        if current:
            print(f"Current: {current.display_name()}")
        else:
            print("No API key selected.")
            print_selection_prompt(manager)
        sys.exit(0)


if __name__ == "__main__":
    main()
