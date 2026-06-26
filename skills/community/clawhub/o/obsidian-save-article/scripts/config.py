#!/usr/bin/env python3
"""
Configuration management for obsidian-save-article skill.
Handles path configuration storage and retrieval.
"""

import os
import sys
import json
from datetime import datetime

CONFIG_PATH = os.path.expanduser("~/.obsidian-save-article-config.json")

def load_config():
    """Load configuration from file. Returns None if not configured."""
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return None
    return None

def save_config(config):
    """Save configuration to file."""
    config["configured"] = True
    config["configured_at"] = datetime.now().isoformat()
    
    # Compute full path
    vault_path = config.get("vault_path", "")
    subfolder = config.get("subfolder", "")
    
    if subfolder:
        full_path = os.path.join(vault_path, subfolder)
    else:
        full_path = vault_path
    
    config["full_path"] = full_path
    
    # Ensure directory exists
    os.makedirs(full_path, exist_ok=True)
    
    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    return config

def get_save_path():
    """Get the configured save path. Returns None if not configured."""
    config = load_config()
    if config and config.get("configured"):
        return config.get("full_path")
    return None

def get_vault_path():
    """Get the vault path without subfolder."""
    config = load_config()
    if config and config.get("configured"):
        return config.get("vault_path")
    return None

def is_configured():
    """Check if the skill has been configured."""
    config = load_config()
    return config and config.get("configured", False)

def clear_config():
    """Clear the configuration."""
    if os.path.exists(CONFIG_PATH):
        os.remove(CONFIG_PATH)
    return True

def verify_path_exists(path):
    """Verify that a path exists and is accessible."""
    expanded_path = os.path.expanduser(path)
    return os.path.exists(expanded_path) and os.path.isdir(expanded_path)

if __name__ == '__main__':
    # CLI interface for testing
    if len(sys.argv) < 2:
        print("Usage: python config.py <action> [args]")
        print("Actions:")
        print("  status          - Show current configuration status")
        print("  get-path        - Get the configured save path")
        print("  set <vault> [subfolder] - Set the save path")
        print("  clear           - Clear configuration")
        sys.exit(1)
    
    action = sys.argv[1]
    
    if action == "status":
        config = load_config()
        if config and config.get("configured"):
            print(f"✅ 已配置")
            print(f"   类型: {config.get('type', 'local')}")
            print(f"   Vault: {config.get('vault_path')}")
            print(f"   子文件夹: {config.get('subfolder', '(无)')}")
            print(f"   完整路径: {config.get('full_path')}")
            print(f"   配置时间: {config.get('configured_at')}")
        else:
            print("❌ 未配置 - 请运行配置流程")
    
    elif action == "get-path":
        path = get_save_path()
        if path:
            print(path)
        else:
            print("")
    
    elif action == "set":
        if len(sys.argv) < 3:
            print("Usage: python config.py set <vault_path> [subfolder]")
            sys.exit(1)
        
        vault_path = sys.argv[2]
        subfolder = sys.argv[3] if len(sys.argv) > 3 else ""
        
        # Determine type based on path
        config_type = "icloud" if "iCloud" in vault_path or "Mobile Documents" in vault_path else "local"
        
        config = {
            "type": config_type,
            "vault_path": vault_path,
            "subfolder": subfolder
        }
        
        saved = save_config(config)
        print(f"✅ 配置已保存")
        print(f"   完整路径: {saved.get('full_path')}")
    
    elif action == "clear":
        clear_config()
        print("✅ 配置已清除")
    
    else:
        print(f"Unknown action: {action}")
        sys.exit(1)
