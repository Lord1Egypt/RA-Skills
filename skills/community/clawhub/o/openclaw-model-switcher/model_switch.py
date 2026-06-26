#!/usr/bin/env python3
import os
import shutil
import subprocess
import time
import argparse
import json
from datetime import datetime
from typing import Optional

# 配置常量 - 修正为实际JSON配置路径
OPENCLAW_CONFIG_PATH = os.path.expanduser("~/.openclaw/openclaw.json")
BACKUP_DIR = os.path.expanduser("~/.openclaw/config_backups")
DEFAULT_RETRY_TIMES = 3
RESTART_WAIT_SECONDS = 8
STATUS_CHECK_KEYWORD = "running"

class OpenClawModelSwitcher:
    def __init__(self, new_model: str, retry_times: int = DEFAULT_RETRY_TIMES):
        self.new_model = new_model
        self.retry_times = retry_times
        self.backup_file_path: Optional[str] = None
        self.original_config_content: Optional[str] = None
        self.original_config_json: Optional[dict] = None
        
        # 初始化备份目录
        os.makedirs(BACKUP_DIR, exist_ok=True)
        # 预检查配置文件存在
        if not os.path.exists(OPENCLAW_CONFIG_PATH):
            raise FileNotFoundError(f"OpenClaw配置文件不存在: {OPENCLAW_CONFIG_PATH}")
        
    def backup_original_config(self) -> bool:
        """备份原始配置文件，带时间戳"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"config_backup_{timestamp}.json"
        self.backup_file_path = os.path.join(BACKUP_DIR, backup_filename)
        
        try:
            shutil.copy2(OPENCLAW_CONFIG_PATH, self.backup_file_path)
            # 同时缓存原始配置内容和json结构，防止备份文件读取失败
            with open(OPENCLAW_CONFIG_PATH, 'r', encoding='utf-8') as f:
                self.original_config_content = f.read()
                self.original_config_json = json.loads(self.original_config_content)
            print(f"✅ 原始配置已备份到: {self.backup_file_path}")
            return True
        except Exception as e:
            print(f"❌ 备份配置失败: {str(e)}")
            return False
        
    def modify_config_default_model(self) -> bool:
        """修改配置文件中的默认模型，只修改agents.defaults.model.primary，模型列表不动"""
        try:
            import copy
            new_config = copy.deepcopy(self.original_config_json)
            
            # 定位 agents.defaults.model.primary
            old_model = new_config.get('agents',{}).get('defaults',{}).get('model',{}).get('primary','(未知)')
            if 'agents' not in new_config:
                new_config['agents'] = {}
            if 'defaults' not in new_config['agents']:
                new_config['agents']['defaults'] = {}
            if 'model' not in new_config['agents']['defaults']:
                new_config['agents']['defaults']['model'] = {}
            
            new_config['agents']['defaults']['model']['primary'] = self.new_model
            
            with open(OPENCLAW_CONFIG_PATH, 'w', encoding='utf-8') as f:
                json.dump(new_config, f, indent=4, ensure_ascii=False)
            
            print(f"✅ 配置已修改: {old_model} → {self.new_model}")
            print(f"ℹ️  仅修改了 agents.defaults.model.primary，模型列表等其他配置完全不动")
            return True
        except Exception as e:
            print(f"❌ 修改配置失败: {str(e)}")
            return False
        
    def restart_gateway(self) -> bool:
        """执行Gateway重启命令"""
        try:
            print("🔄 正在重启OpenClaw Gateway...")
            result = subprocess.run(
                ["openclaw", "gateway", "restart"],
                capture_output=True,
                text=True,
                timeout=60
            )
            if result.returncode != 0:
                print(f"❌ 重启命令执行失败: {result.stderr}")
                return False
            
            # 等待服务启动
            print(f"⏳ 等待服务启动 {RESTART_WAIT_SECONDS} 秒...")
            time.sleep(RESTART_WAIT_SECONDS)
            return True
        except Exception as e:
            print(f"❌ 重启命令执行异常: {str(e)}")
            return False
        
    def check_gateway_status(self) -> bool:
        """检测Gateway运行状态"""
        try:
            result = subprocess.run(
                ["openclaw", "gateway", "status"],
                capture_output=True,
                text=True,
                timeout=10
            )
            return (result.returncode == 0) and (STATUS_CHECK_KEYWORD in result.stdout.lower())
        except Exception as e:
            print(f"❌ 状态检测失败: {str(e)}")
            return False
        
    def rollback_config(self) -> bool:
        """回滚到原始配置"""
        try:
            print("⚠️  正在回滚到原始配置...")
            if self.backup_file_path and os.path.exists(self.backup_file_path):
                shutil.copy2(self.backup_file_path, OPENCLAW_CONFIG_PATH)
            else:
                # 备份文件丢失时用缓存内容恢复
                with open(OPENCLAW_CONFIG_PATH, 'w', encoding='utf-8') as f:
                    f.write(self.original_config_content)
            
            # 回滚后重启
            if not self.restart_gateway():
                return False
            if not self.check_gateway_status():
                return False
            
            print("✅ 回滚成功，服务已恢复到原始状态")
            return True
        except Exception as e:
            print(f"❌ 回滚失败: {str(e)}")
            print("‼️  请手动恢复配置文件，备份路径: ", self.backup_file_path)
            return False
        
    def run_switch(self) -> bool:
        """执行完整切换流程"""
        print(f"🚀 开始切换OpenClaw默认模型到: {self.new_model}")
        print("="*50)
        
        # 1. 备份原始配置
        if not self.backup_original_config():
            return False
        
        # 2. 修改配置（仅修改default_model字段）
        if not self.modify_config_default_model():
            return False
        
        # 3. 重启+检测，支持多次重试
        for retry in range(self.retry_times):
            print(f"\n🔍 第 {retry+1}/{self.retry_times} 次尝试...")
            if not self.restart_gateway():
                continue
            
            if self.check_gateway_status():
                print("\n🎉 模型切换成功！Gateway运行正常")
                print(f"📝 原始配置备份保留在: {self.backup_file_path}")
                return True
        
        # 所有重试都失败，回滚
        print(f"\n❌ {self.retry_times} 次重启都失败，开始回滚...")
        return self.rollback_config()
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="OpenClaw默认模型切换工具（外部运行，无需在OpenClaw会话内执行）")
    parser.add_argument("new_model", help="新的默认模型名称，比如 zai/glm-5.1")
    parser.add_argument("--retry", type=int, default=DEFAULT_RETRY_TIMES, help="重启失败重试次数，默认3次")
    parser.add_argument("--dry-run", action="store_true", help="仅测试流程，不实际修改配置和重启")
    
    args = parser.parse_args()
    
    if args.dry_run:
        print("🧪  dry run模式，仅做配置备份测试，不实际修改和重启")
        switcher = OpenClawModelSwitcher(args.new_model, args.retry)
        switcher.backup_original_config()
        # 模拟修改逻辑，展示效果
        test_config = switcher.original_config_json.copy()
        old_primary = test_config.get('agents',{}).get('defaults',{}).get('model',{}).get('primary','(未设置)')
        test_config.setdefault('agents',{}).setdefault('defaults',{}).setdefault('model',{})['primary'] = args.new_model
        print(f"✅ dry run测试完成: {old_primary} → {args.new_model}")
        print(f"ℹ️  仅修改 agents.defaults.model.primary，模型列表完全不变")
        exit(0)
    
    try:
        switcher = OpenClawModelSwitcher(args.new_model, args.retry)
        success = switcher.run_switch()
        exit(0 if success else 1)
    except Exception as e:
        print(f"❌ 执行失败: {str(e)}")
        exit(1)