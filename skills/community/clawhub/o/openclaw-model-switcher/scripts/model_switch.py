#!/usr/bin/env python3
"""
OpenClaw Default Model Switcher

Safely switch the default model in OpenClaw configuration.
Features: backup, modify-only-primary, restart, health-check, auto-rollback.

Usage:
    python3 model_switch.py <model-name> [--retry N] [--dry-run]
    python3 model_switch.py zai/glm-5.1
    python3 model_switch.py zai/glm-5.1 --retry 5
    python3 model_switch.py zai/glm-5.1 --dry-run

Environment:
    OPENCLAW_CONFIG  - Path to openclaw.json (default: ~/.openclaw/openclaw.json)
"""

import os
import shutil
import subprocess
import time
import argparse
import json
import copy
from datetime import datetime
from typing import Optional


def default_config_path() -> str:
    return os.environ.get("OPENCLAW_CONFIG", os.path.expanduser("~/.openclaw/openclaw.json"))


BACKUP_DIR = os.path.expanduser("~/.openclaw/config_backups")
DEFAULT_RETRY_TIMES = 3
RESTART_WAIT_SECONDS = 8


class OpenClawModelSwitcher:
    def __init__(self, new_model: str, retry_times: int = DEFAULT_RETRY_TIMES,
                 config_path: Optional[str] = None):
        self.new_model = new_model
        self.retry_times = retry_times
        self.config_path = config_path or default_config_path()
        self.backup_file_path: Optional[str] = None
        self.original_config_content: Optional[str] = None
        self.original_config_json: Optional[dict] = None

        os.makedirs(BACKUP_DIR, exist_ok=True)
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"OpenClaw config not found: {self.config_path}")

    def backup_original_config(self) -> bool:
        """Backup config with timestamp."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"config_backup_{timestamp}.json"
        self.backup_file_path = os.path.join(BACKUP_DIR, backup_filename)

        try:
            shutil.copy2(self.config_path, self.backup_file_path)
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.original_config_content = f.read()
                self.original_config_json = json.loads(self.original_config_content)
            print(f"✅ Config backed up to: {self.backup_file_path}")
            return True
        except Exception as e:
            print(f"❌ Backup failed: {e}")
            return False

    def modify_config_default_model(self) -> bool:
        """Modify only agents.defaults.model.primary."""
        try:
            new_config = copy.deepcopy(self.original_config_json)
            old_model = (new_config.get('agents', {})
                         .get('defaults', {})
                         .get('model', {})
                         .get('primary', '(unknown)'))

            new_config.setdefault('agents', {}).setdefault('defaults', {}).setdefault('model', {})
            new_config['agents']['defaults']['model']['primary'] = self.new_model

            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(new_config, f, indent=4, ensure_ascii=False)

            print(f"✅ Config updated: {old_model} → {self.new_model}")
            return True
        except Exception as e:
            print(f"❌ Config modification failed: {e}")
            return False

    def restart_gateway(self) -> bool:
        """Restart OpenClaw Gateway."""
        try:
            print("🔄 Restarting OpenClaw Gateway...")
            result = subprocess.run(
                ["openclaw", "gateway", "restart"],
                capture_output=True, text=True, timeout=60
            )
            if result.returncode != 0:
                print(f"❌ Restart failed: {result.stderr}")
                return False
            print(f"⏳ Waiting {RESTART_WAIT_SECONDS}s for startup...")
            time.sleep(RESTART_WAIT_SECONDS)
            return True
        except Exception as e:
            print(f"❌ Restart exception: {e}")
            return False

    def check_gateway_status(self) -> bool:
        """Check if Gateway is running."""
        try:
            result = subprocess.run(
                ["openclaw", "gateway", "status"],
                capture_output=True, text=True, timeout=10
            )
            return result.returncode == 0 and "running" in result.stdout.lower()
        except Exception as e:
            print(f"❌ Status check failed: {e}")
            return False

    def rollback_config(self) -> bool:
        """Rollback to original config and restart."""
        try:
            print("⚠️  Rolling back to original config...")
            if self.backup_file_path and os.path.exists(self.backup_file_path):
                shutil.copy2(self.backup_file_path, self.config_path)
            elif self.original_config_content:
                with open(self.config_path, 'w', encoding='utf-8') as f:
                    f.write(self.original_config_content)
            else:
                print("❌ No backup available for rollback!")
                return False

            if not self.restart_gateway():
                return False
            if not self.check_gateway_status():
                return False

            print("✅ Rollback successful, service restored")
            return True
        except Exception as e:
            print(f"❌ Rollback failed: {e}")
            print(f"‼️  Manual restore needed, backup at: {self.backup_file_path}")
            return False

    def run_switch(self) -> bool:
        """Execute full switch flow: backup → modify → restart → verify."""
        print(f"🚀 Switching OpenClaw default model to: {self.new_model}")
        print("=" * 50)

        if not self.backup_original_config():
            return False

        if not self.modify_config_default_model():
            return False

        for retry in range(self.retry_times):
            print(f"\n🔍 Attempt {retry + 1}/{self.retry_times}...")
            if not self.restart_gateway():
                continue
            if self.check_gateway_status():
                print(f"\n🎉 Model switch successful! Gateway running normally")
                print(f"📝 Backup at: {self.backup_file_path}")
                return True

        print(f"\n❌ All {self.retry_times} attempts failed, rolling back...")
        return self.rollback_config()


def main():
    parser = argparse.ArgumentParser(
        description="OpenClaw Default Model Switcher — safely switch models with auto-rollback"
    )
    parser.add_argument("new_model", help="Target model name, e.g. zai/glm-5.1")
    parser.add_argument("--retry", type=int, default=DEFAULT_RETRY_TIMES,
                        help=f"Restart retry count (default: {DEFAULT_RETRY_TIMES})")
    parser.add_argument("--dry-run", action="store_true",
                        help="Test only — backup and show diff, no actual changes")
    parser.add_argument("--config", default=None,
                        help="Path to openclaw.json (default: ~/.openclaw/openclaw.json)")

    args = parser.parse_args()

    if args.dry_run:
        print("🧪 Dry run mode — no actual changes")
        switcher = OpenClawModelSwitcher(args.new_model, args.retry, config_path=args.config)
        switcher.backup_original_config()
        test_config = copy.deepcopy(switcher.original_config_json)
        old = test_config.get('agents', {}).get('defaults', {}).get('model', {}).get('primary', '(unset)')
        test_config.setdefault('agents', {}).setdefault('defaults', {}).setdefault('model', {})
        test_config['agents']['defaults']['model']['primary'] = args.new_model
        print(f"✅ Dry run complete: {old} → {args.new_model}")
        print("ℹ️  Only agents.defaults.model.primary would change, provider list untouched")
        return

    try:
        switcher = OpenClawModelSwitcher(args.new_model, args.retry, config_path=args.config)
        success = switcher.run_switch()
        exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        exit(1)


if __name__ == "__main__":
    main()
