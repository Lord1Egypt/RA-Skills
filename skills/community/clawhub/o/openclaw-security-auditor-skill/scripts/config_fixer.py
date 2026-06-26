#!/usr/bin/env python3
"""
OpenClaw Security Auditor - Configuration Fixer
This script provides safe configuration fixing capabilities for OpenClaw.
"""

import json
import shutil
from datetime import datetime
from pathlib import Path

def backup_config(config_path: str) -> str:
    """Create backup of OpenClaw configuration"""
    config_path = Path(config_path)
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_name = f"openclaw-config-backup-{timestamp}.json"
    backup_path = config_path.parent / backup_name
    
    shutil.copy2(config_path, backup_path)
    return str(backup_path)

def apply_security_profile(config_path: str, mode: str = "balanced") -> bool:
    """
    Apply security profile to OpenClaw configuration
    
    Args:
        config_path: Path to OpenClaw config file
        mode: Security mode ("conservative", "balanced", "aggressive")
    
    Returns:
        True if successful, False otherwise
    """
    try:
        # Load current config
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # Create backup
        backup_path = backup_config(config_path)
        print(f"Backup created: {backup_path}")
        
        # Apply security recommendations based on mode
        if mode == "conservative":
            _apply_conservative_profile(config)
        elif mode == "balanced":
            _apply_balanced_profile(config)
        elif mode == "aggressive":
            _apply_aggressive_profile(config)
        else:
            raise ValueError(f"Unknown mode: {mode}")
        
        # Save updated config
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print(f"Security profile '{mode}' applied successfully!")
        return True
        
    except Exception as e:
        print(f"Error applying security profile: {e}")
        return False

def _apply_conservative_profile(config: dict):
    """Apply conservative security profile"""
    # Gateway settings
    if 'gateway' not in config:
        config['gateway'] = {}
    config['gateway']['bind'] = 'loopback'
    if 'auth' not in config['gateway']:
        config['gateway']['auth'] = {}
    config['gateway']['auth']['mode'] = 'token'
    
    # Tools settings
    if 'tools' not in config:
        config['tools'] = {}
    config['tools']['profile'] = 'messaging'
    if 'fs' not in config['tools']:
        config['tools']['fs'] = {}
    config['tools']['fs']['workspaceOnly'] = True
    
    # Session settings
    if 'session' not in config:
        config['session'] = {}
    config['session']['dmScope'] = 'paired'

def _apply_balanced_profile(config: dict):
    """Apply balanced security profile (recommended)"""
    # Gateway settings
    if 'gateway' not in config:
        config['gateway'] = {}
    config['gateway']['bind'] = 'loopback'
    if 'auth' not in config['gateway']:
        config['gateway']['auth'] = {}
    config['gateway']['auth']['mode'] = 'token'
    
    # Tools settings
    if 'tools' not in config:
        config['tools'] = {}
    config['tools']['profile'] = 'coding'
    if 'fs' not in config['tools']:
        config['tools']['fs'] = {}
    config['tools']['fs']['workspaceOnly'] = True
    
    # Session settings
    if 'session' not in config:
        config['session'] = {}
    config['session']['dmScope'] = 'per-channel-peer'

def _apply_aggressive_profile(config: dict):
    """Apply aggressive security profile (testing only)"""
    # Gateway settings
    if 'gateway' not in config:
        config['gateway'] = {}
    config['gateway']['bind'] = 'lan'
    if 'auth' not in config['gateway']:
        config['gateway']['auth'] = {}
    config['gateway']['auth']['mode'] = 'none'
    
    # Tools settings
    if 'tools' not in config:
        config['tools'] = {}
    config['tools']['profile'] = 'full'
    if 'fs' not in config['tools']:
        config['tools']['fs'] = {}
    config['tools']['fs']['workspaceOnly'] = False
    
    # Session settings
    if 'session' not in config:
        config['session'] = {}
    config['session']['dmScope'] = 'any'

def main():
    """Command line interface for config fixer"""
    import argparse
    
    parser = argparse.ArgumentParser(description="OpenClaw Security Config Fixer")
    parser.add_argument("--config", "-c", required=True, help="Path to OpenClaw config file")
    parser.add_argument("--mode", "-m", default="balanced", 
                       choices=["conservative", "balanced", "aggressive"],
                       help="Security mode to apply")
    parser.add_argument("--dry-run", action="store_true", 
                       help="Show what would be changed without applying")
    
    args = parser.parse_args()
    
    if args.dry_run:
        print(f"Dry run: Would apply {args.mode} profile to {args.config}")
        print("No changes will be made.")
    else:
        success = apply_security_profile(args.config, args.mode)
        if not success:
            exit(1)

if __name__ == "__main__":
    main()