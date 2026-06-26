#!/usr/bin/env python3
"""
OpenClaw Credential Hardening Tool
Migrate credentials from config files to environment variables
"""

import os
import json
import re
import platform
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional


class CredentialHardening:
    """Credential hardening tool for OpenClaw"""
    
    def __init__(self, openclaw_path: str = None, dry_run: bool = False):
        """Initialize hardening tool
        
        Args:
            openclaw_path: Path to OpenClaw directory (default: ~/.openclaw)
            dry_run: If True, show what would be done without making changes
        """
        self.openclaw_path = Path(openclaw_path or os.path.expanduser("~/.openclaw"))
        self.config_file = self.openclaw_path / "openclaw.json"
        self.backup_dir = self.openclaw_path / "security-backups"
        self.dry_run = dry_run
        
    def backup_config(self) -> Optional[Path]:
        """Create backup of current configuration"""
        if not self.config_file.exists():
            print("[ERROR] openclaw.json not found")
            return None
        
        if self.dry_run:
            print(f"[DRY-RUN] Would create backup in: {self.backup_dir}")
            return None
            
        self.backup_dir.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = self.backup_dir / f"openclaw.json.backup.{timestamp}"
        
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = f.read()
            
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(config)
                
            print(f"[BACKUP] Configuration backed up to: {backup_path}")
            return backup_path
        except Exception as e:
            print(f"[ERROR] Backup failed: {e}")
            return None
        
    def extract_credentials(self) -> Dict[str, str]:
        """Extract credentials from configuration"""
        credentials = {}
        
        if not self.config_file.exists():
            print("[ERROR] openclaw.json not found")
            return credentials
        
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                content = f.read()
                config = json.loads(content)
        except Exception as e:
            print(f"[ERROR] Failed to parse config: {e}")
            return credentials
        
        # Extract Feishu credentials
        feishu_config = config.get('channels', {}).get('feishu', {})
        if feishu_config.get('appSecret'):
            credentials['FEISHU_APP_SECRET'] = feishu_config['appSecret']
        if feishu_config.get('appId'):
            credentials['FEISHU_APP_ID'] = feishu_config['appId']
            
        # Extract Gateway token
        gateway_config = config.get('gateway', {}).get('auth', {})
        if gateway_config.get('token'):
            credentials['OPENCLAW_GATEWAY_TOKEN'] = gateway_config['token']
            
        # Look for other potential credentials
        # This is extensible for future credential types
        
        return credentials
        
    def generate_env_file(self, credentials: Dict[str, str]) -> Optional[Path]:
        """Generate environment variable files"""
        if not credentials:
            print("[INFO] No credentials found to export")
            return None
        
        env_file = self.openclaw_path / ".env"
        env_example = self.openclaw_path / ".env.example"
        
        if self.dry_run:
            print(f"[DRY-RUN] Would create: {env_file}")
            print(f"[DRY-RUN] Would create: {env_example}")
            return None
        
        # Generate .env file (actual credentials)
        lines = [
            "# OpenClaw Environment Variables",
            f"# Generated: {datetime.now().isoformat()}",
            "# WARNING: Keep this file secure! Never commit to version control.",
            "",
        ]
        
        for key, value in credentials.items():
            lines.append(f"{key}={value}")
            
        try:
            with open(env_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(lines))
            print(f"[ENV] Created: {env_file}")
        except Exception as e:
            print(f"[ERROR] Failed to create .env: {e}")
            return None
            
        # Generate .env.example file (template)
        example_lines = [
            "# OpenClaw Environment Variables - Example",
            "# Copy this file to .env and fill in your actual values",
            "",
        ]
        for key in credentials.keys():
            example_lines.append(f"{key}=your_{key.lower()}_here")
            
        try:
            with open(env_example, 'w', encoding='utf-8') as f:
                f.write('\n'.join(example_lines))
            print(f"[ENV] Created: {env_example}")
        except Exception as e:
            print(f"[WARN] Failed to create .env.example: {e}")
            
        return env_file
        
    def sanitize_config(self) -> bool:
        """Remove credentials from config file (replace with placeholders)"""
        if not self.config_file.exists():
            return False
            
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                content = f.read()
                config = json.loads(content)
        except Exception as e:
            print(f"[ERROR] Failed to read config: {e}")
            return False
        
        modified = False
        
        # Sanitize Feishu credentials
        if 'channels' in config and 'feishu' in config['channels']:
            feishu = config['channels']['feishu']
            if 'appSecret' in feishu:
                feishu['appSecret'] = '${FEISHU_APP_SECRET}'
                modified = True
            if 'appId' in feishu:
                feishu['appId'] = '${FEISHU_APP_ID}'
                modified = True
                
        # Sanitize Gateway token
        if 'gateway' in config and 'auth' in config['gateway']:
            auth = config['gateway']['auth']
            if 'token' in auth:
                auth['token'] = '${OPENCLAW_GATEWAY_TOKEN}'
                modified = True
        
        if not modified:
            print("[INFO] No credentials found to sanitize")
            return True
        
        if self.dry_run:
            print("[DRY-RUN] Would sanitize credentials in openclaw.json")
            return True
        
        # Save sanitized config
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            print("[SANITIZE] Credentials removed from openclaw.json")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to save sanitized config: {e}")
            return False
            
    def generate_setup_script(self) -> Optional[Path]:
        """Generate platform-specific environment setup script"""
        system = platform.system()
        
        if system == "Windows":
            return self._generate_windows_script()
        else:
            return self._generate_unix_script()
            
    def _generate_windows_script(self) -> Optional[Path]:
        """Generate Windows PowerShell setup script"""
        script_path = self.openclaw_path / "set_env.ps1"
        env_file = self.openclaw_path / ".env"
        
        if self.dry_run:
            print(f"[DRY-RUN] Would create: {script_path}")
            return None
        
        script_content = f'''# OpenClaw Environment Variables Setup Script
# Run: .\\set_env.ps1

$envFile = "{env_file}"

if (Test-Path $envFile) {{
    Get-Content $envFile | ForEach-Object {{
        if ($_ -match '^([^#][^=]*)=(.*)$') {{
            $name = $matches[1]
            $value = $matches[2]
            [Environment]::SetEnvironmentVariable($name, $value, 'User')
            Write-Host "Set $name = *** (hidden)"
        }}
    }}
    Write-Host "Environment variables set successfully!"
    Write-Host "Note: Restart your terminal for changes to take effect."
}} else {{
    Write-Error ".env file not found at $envFile"
}}
'''
        
        try:
            with open(script_path, 'w', encoding='utf-8') as f:
                f.write(script_content)
            print(f"[SCRIPT] Created: {script_path}")
            return script_path
        except Exception as e:
            print(f"[ERROR] Failed to create script: {e}")
            return None
            
    def _generate_unix_script(self) -> Optional[Path]:
        """Generate Unix (macOS/Linux) shell setup script"""
        script_path = self.openclaw_path / "set_env.sh"
        env_file = self.openclaw_path / ".env"
        
        if self.dry_run:
            print(f"[DRY-RUN] Would create: {script_path}")
            return None
        
        script_content = f'''#!/bin/bash
# OpenClaw Environment Variables Setup Script
# Run: source set_env.sh

ENV_FILE="{env_file}"

if [ -f "$ENV_FILE" ]; then
    while IFS='=' read -r name value; do
        # Skip comments and empty lines
        [[ "$name" =~ ^#.*$ ]] && continue
        [[ -z "$name" ]] && continue
        export "$name=$value"
        echo "Exported $name"
    done < "$ENV_FILE"
    echo "Environment variables set for this session."
    echo "To make permanent, add to ~/.bashrc or ~/.zshrc"
else
    echo "Error: .env file not found at $ENV_FILE"
    exit 1
fi
'''
        
        try:
            with open(script_path, 'w', encoding='utf-8') as f:
                f.write(script_content)
            # Make executable
            os.chmod(script_path, 0o755)
            print(f"[SCRIPT] Created: {script_path}")
            return script_path
        except Exception as e:
            print(f"[ERROR] Failed to create script: {e}")
            return None
            
    def verify_environment(self) -> Tuple[bool, List[str]]:
        """Verify environment variables are set"""
        required_vars = ['FEISHU_APP_ID', 'FEISHU_APP_SECRET', 'OPENCLAW_GATEWAY_TOKEN']
        missing = []
        
        for var in required_vars:
            if not os.environ.get(var):
                missing.append(var)
        
        if missing:
            return False, missing
        return True, []
            
    def run(self) -> bool:
        """Run complete hardening process"""
        print("=" * 60)
        print("OpenClaw Credential Hardening Tool v1.0.0")
        print("=" * 60)
        
        if self.dry_run:
            print("[MODE] Dry run - no changes will be made")
            print()
        
        if not self.config_file.exists():
            print("[ERROR] openclaw.json not found!")
            return False
            
        # Step 1: Backup
        backup_path = self.backup_config()
        if not backup_path and not self.dry_run:
            print("[ERROR] Backup failed, aborting")
            return False
        print()
        
        # Step 2: Extract credentials
        credentials = self.extract_credentials()
        if not credentials:
            print("[INFO] No credentials found to secure.")
            return True
            
        print(f"[INFO] Found {len(credentials)} credential(s):")
        for key in credentials.keys():
            print(f"  - {key}")
        print()
        
        # Step 3: Generate env files
        env_file = self.generate_env_file(credentials)
        if not env_file and not self.dry_run:
            print("[ERROR] Failed to create env file")
            return False
        print()
        
        # Step 4: Sanitize config
        if not self.sanitize_config():
            print("[ERROR] Failed to sanitize config")
            return False
        print()
        
        # Step 5: Generate setup script
        script_path = self.generate_setup_script()
        print()
        
        # Summary
        print("=" * 60)
        if self.dry_run:
            print("[DRY-RUN] No changes were made")
        else:
            print("[DONE] Hardening complete!")
        print("=" * 60)
        print()
        print("NEXT STEPS:")
        print("1. Review the generated .env file")
        print("2. Run the setup script to set environment variables:")
        if platform.system() == "Windows":
            print(f"   .\\set_env.ps1")
        else:
            print(f"   source set_env.sh")
        print("3. Restart OpenClaw Gateway to apply changes")
        print("4. Keep the .env file secure and do not share it")
        print()
        print("WARNING: The .env file contains sensitive credentials!")
        print("         Store it in a secure location.")
        
        return True


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='OpenClaw Credential Hardening Tool')
    parser.add_argument('--path', '-p', help='OpenClaw directory path (default: ~/.openclaw)')
    parser.add_argument('--dry-run', '-n', action='store_true', 
                        help='Show what would be done without making changes')
    parser.add_argument('--verify', '-v', action='store_true',
                        help='Verify environment variables are set')
    
    args = parser.parse_args()
    
    if args.verify:
        hardening = CredentialHardening(openclaw_path=args.path)
        ok, missing = hardening.verify_environment()
        if ok:
            print("[OK] All required environment variables are set")
            exit(0)
        else:
            print(f"[MISSING] Environment variables not set: {', '.join(missing)}")
            exit(1)
    
    hardening = CredentialHardening(
        openclaw_path=args.path,
        dry_run=args.dry_run
    )
    
    success = hardening.run()
    exit(0 if success else 1)


if __name__ == "__main__":
    main()
