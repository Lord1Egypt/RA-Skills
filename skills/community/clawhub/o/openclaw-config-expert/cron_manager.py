#!/usr/bin/env python3
"""
OpenClaw Cron 管理器
配置和管理定期任务（配置验证、健康检查、备份清理等）
"""

import json
import os
import sys
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any


class CronManager:
    """OpenClaw Cron 任务管理器"""
    
    def __init__(self):
        self.config_expert_dir = Path(__file__).parent
        self.config_validator = self.config_expert_dir / "config_validator.py"
        self.emergency_recovery = self.config_expert_dir / "scripts" / "emergency_recovery.py"
    
    def list_jobs(self) -> List[Dict]:
        """列出所有 Cron 任务"""
        try:
            result = subprocess.run(
                ["openclaw", "cron", "list", "--include-disabled"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                print(result.stdout)
                return []
            else:
                print(f"❌ 查询失败：{result.stderr}")
                return []
        except Exception as e:
            print(f"❌ 执行失败：{e}")
            return []
    
    def add_daily_validate(self):
        """添加每日配置验证任务（凌晨 2 点）"""
        job = {
            "name": "daily-config-validate",
            "schedule": {"kind": "cron", "expr": "0 2 * * *", "tz": "Asia/Shanghai"},
            "payload": {
                "kind": "agentTurn",
                "message": "执行每日配置验证：python3 ~/.openclaw/workspace/openclaw-config-expert/config_validator.py validate",
                "timeoutSeconds": 300
            },
            "delivery": {"mode": "announce"},
            "sessionTarget": "isolated",
            "enabled": True,
            "description": "每日凌晨 2 点自动验证 OpenClaw 配置"
        }
        
        return self._add_job(job)
    
    def add_weekly_health(self):
        """添加每周健康检查任务（周日 8 点）"""
        job = {
            "name": "weekly-health-check",
            "schedule": {"kind": "cron", "expr": "0 8 * * 0", "tz": "Asia/Shanghai"},
            "payload": {
                "kind": "agentTurn",
                "message": "执行每周健康检查：python3 ~/.openclaw/workspace/openclaw-config-expert/config_validator.py health",
                "timeoutSeconds": 600
            },
            "delivery": {"mode": "announce"},
            "sessionTarget": "isolated",
            "enabled": True,
            "description": "每周日 8 点自动执行 OpenClaw 健康检查"
        }
        
        return self._add_job(job)
    
    def add_monthly_backup_cleanup(self):
        """添加每月备份清理任务（1 号 3 点）"""
        job = {
            "name": "monthly-backup-cleanup",
            "schedule": {"kind": "cron", "expr": "0 3 1 * *", "tz": "Asia/Shanghai"},
            "payload": {
                "kind": "agentTurn",
                "message": "清理超过 30 天的配置备份：find ~/.openclaw -name 'openclaw.json.bak.*' -mtime +30 -delete",
                "timeoutSeconds": 300
            },
            "delivery": {"mode": "announce"},
            "sessionTarget": "isolated",
            "enabled": True,
            "description": "每月 1 号凌晨 3 点清理超过 30 天的配置备份"
        }
        
        return self._add_job(job)
    
    def _add_job(self, job: Dict) -> bool:
        """添加 Cron 任务"""
        try:
            job_json = json.dumps(job, ensure_ascii=False)
            
            # 使用 openclaw cron add 命令
            cmd = [
                "openclaw", "cron", "add",
                "--job", job_json
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                print(f"✅ Cron 任务已添加：{job['name']}")
                print(result.stdout)
                return True
            else:
                print(f"❌ 添加失败：{result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ 执行失败：{e}")
            return False
    
    def setup_all(self):
        """设置所有推荐 Cron 任务"""
        print("="*60)
        print("OpenClaw Cron 任务设置")
        print("="*60)
        
        tasks = [
            ("每日配置验证", self.add_daily_validate),
            ("每周健康检查", self.add_weekly_health),
            ("每月备份清理", self.add_monthly_backup_cleanup)
        ]
        
        success_count = 0
        
        for name, task_func in tasks:
            print(f"\n正在添加：{name}...")
            if task_func():
                success_count += 1
        
        print("\n" + "="*60)
        print(f"设置完成：{success_count}/{len(tasks)} 个任务成功")
        print("="*60)
        
        # 列出所有任务
        print("\n当前 Cron 任务列表:")
        self.list_jobs()
    
    def test_validate(self):
        """测试配置验证任务"""
        print("="*60)
        print("测试配置验证任务")
        print("="*60)
        
        result = subprocess.run(
            ["python3", str(self.config_validator), "validate"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
        
        return result.returncode == 0
    
    def test_health(self):
        """测试健康检查任务"""
        print("="*60)
        print("测试健康检查任务")
        print("="*60)
        
        result = subprocess.run(
            ["python3", str(self.config_validator), "health"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
        
        return result.returncode == 0


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description="OpenClaw Cron 管理器")
    parser.add_argument("action", choices=["setup", "list", "test-validate", "test-health", "add-daily", "add-weekly", "add-monthly"],
                       help="执行动作：setup(设置全部), list(列表), test-validate(测试验证), test-health(测试健康), add-daily(添加每日), add-weekly(添加每周), add-monthly(添加每月)")
    
    args = parser.parse_args()
    
    manager = CronManager()
    
    if args.action == "setup":
        manager.setup_all()
    
    elif args.action == "list":
        manager.list_jobs()
    
    elif args.action == "test-validate":
        manager.test_validate()
    
    elif args.action == "test-health":
        manager.test_health()
    
    elif args.action == "add-daily":
        manager.add_daily_validate()
    
    elif args.action == "add-weekly":
        manager.add_weekly_health()
    
    elif args.action == "add-monthly":
        manager.add_monthly_backup_cleanup()


if __name__ == "__main__":
    main()
