#!/usr/bin/env python3
"""
ClawHub 同步模块
每小时自动同步 ControlMemory 到 ClawHub
"""

import os
import sys
import json
import hashlib
import requests
from datetime import datetime
from pathlib import Path

# 颜色输出
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'

def print_color(color, text):
    print(f"{color}{text}{Colors.NC}")

class ClawHubSync:
    def __init__(self):
        """初始化 ClawHub 同步器"""
        self.script_dir = Path(__file__).parent
        self.memory_file = self.script_dir / "controlmemory.md"
        self.sync_state_file = self.script_dir / ".sync_state.json"
        
        # ClawHub API 配置
        self.api_base = "https://clawhub.com/api/v1"
        self.skill_id = "macos-desktop-control"
        self.api_key = os.getenv('CLAWHUB_API_KEY', '')
        
        # 同步策略
        self.sync_interval_hours = 6  # 每 6 小时同步
        self.check_interval_hours = 2  # 2 小时内有新记录则同步
        
        # 同步状态
        self.sync_state = self.load_sync_state()
    
    def load_sync_state(self):
        """加载同步状态"""
        if self.sync_state_file.exists():
            with open(self.sync_state_file, 'r') as f:
                return json.load(f)
        return {
            'last_sync': None,
            'last_hash': '',
            'pending_records': []
        }
    
    def save_sync_state(self):
        """保存同步状态"""
        with open(self.sync_state_file, 'w') as f:
            json.dump(self.sync_state, f, indent=2)
    
    def should_sync(self):
        """
        判断是否应该同步
        
        Returns:
            (bool, str): (是否同步，原因)
        """
        last_sync = self.sync_state.get('last_sync')
        
        if not last_sync:
            return True, "首次同步"
        
        last_sync_time = datetime.fromisoformat(last_sync)
        now = datetime.now()
        hours_since_sync = (now - last_sync_time).total_seconds() / 3600
        
        # 检查是否到了 6 小时间隔
        if hours_since_sync >= self.sync_interval_hours:
            return True, f"距离上次同步 {hours_since_sync:.1f} 小时（>{self.sync_interval_hours}小时）"
        
        # 检查 2 小时内是否有新记录
        if hours_since_sync >= self.check_interval_hours:
            if self.has_new_records_since(last_sync_time):
                return True, f"2 小时内有新记录（距离上次同步 {hours_since_sync:.1f} 小时）"
        
        return False, f"距离上次同步仅 {hours_since_sync:.1f} 小时，且无新记录"
    
    def has_new_records_since(self, check_time):
        """
        检查指定时间后是否有新记录
        
        Args:
            check_time: 检查的起始时间
        
        Returns:
            bool: 是否有新记录
        """
        if not self.memory_file.exists():
            return False
        
        content = self.memory_file.read_text()
        
        # 查找所有添加时间
        time_pattern = r'\*\*添加时间\*\*: (\d{4}-\d{2}-\d{2})'
        matches = re.findall(time_pattern, content)
        
        for date_str in matches:
            try:
                record_time = datetime.strptime(date_str, '%Y-%m-%d')
                if record_time > check_time:
                    return True
            except:
                pass
        
        return False
    
    def get_file_hash(self):
        """获取文件哈希"""
        if not self.memory_file.exists():
            return ''
        content = self.memory_file.read_text()
        return hashlib.md5(content.encode()).hexdigest()
    
    def sync(self, force=False):
        """
        执行同步
        
        Args:
            force: 是否强制同步
        """
        print_color(Colors.BLUE, "🔄 开始 ClawHub 同步...")
        print(f"   时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 检查是否到了同步时间
        if not force:
            should_sync, reason = self.should_sync()
            if not should_sync:
                print_color(Colors.YELLOW, f"⚠️  跳过同步：{reason}")
                return
        
        # 检查文件是否变化
        current_hash = self.get_file_hash()
        if current_hash == self.sync_state['last_hash'] and not force:
            print_color(Colors.YELLOW, "⚠️  文件未变化，跳过同步")
            return
        
        print_color(Colors.GREEN, "✅ 检测到文件变化")
        
        # 下载远程记录
        print_color(Colors.BLUE, "📥 下载远程记录...")
        remote_records = self.download_records()
        
        # 合并记录
        print_color(Colors.BLUE, "🔀 合并记录...")
        merged = self.merge_records(remote_records)
        
        # 查重并上传
        print_color(Colors.BLUE, "⏳ 查重并上传新记录...")
        new_records = self.get_new_records()
        uploaded = 0
        
        for record in new_records:
            if not self.is_duplicate_in_remote(record, remote_records):
                if self.upload_record(record):
                    uploaded += 1
        
        # 更新本地文件
        print_color(Colors.BLUE, "📝 更新本地文件...")
        self.update_local_memory(merged)
        
        # 保存状态
        self.sync_state['last_sync'] = datetime.now().isoformat()
        self.sync_state['last_hash'] = current_hash
        self.save_sync_state()
        
        print_color(Colors.GREEN, f"✅ 同步完成！上传 {uploaded} 条新记录")
    
    def download_records(self):
        """下载远程记录"""
        try:
            response = requests.get(
                f"{self.api_base}/skills/{self.skill_id}/records",
                headers={'Authorization': f'Bearer {self.api_key}'} if self.api_key else {},
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json().get('records', [])
            else:
                print_color(Colors.YELLOW, f"⚠️  下载失败：{response.status_code}")
                return []
        except Exception as e:
            print_color(Colors.RED, f"❌ 下载错误：{e}")
            return []
    
    def merge_records(self, remote_records):
        """合并远程和本地记录"""
        # 简单合并，实际应该更复杂
        return remote_records
    
    def get_new_records(self):
        """获取本地新记录"""
        # 解析 controlmemory.md，提取新记录
        # 这里简化处理
        return []
    
    def is_duplicate_in_remote(self, record, remote_records):
        """检查在远程是否重复"""
        for remote in remote_records:
            if (remote.get('app') == record.get('app') and
                remote.get('command') == record.get('command')):
                return True
        return False
    
    def upload_record(self, record):
        """上传记录"""
        try:
            response = requests.post(
                f"{self.api_base}/skills/{self.skill_id}/records",
                json=record,
                headers={
                    'Authorization': f'Bearer {self.api_key}',
                    'Content-Type': 'application/json'
                } if self.api_key else {'Content-Type': 'application/json'},
                timeout=10
            )
            
            if response.status_code in [200, 201]:
                print_color(Colors.GREEN, f"  ✅ 上传成功：{record.get('command')}")
                return True
            else:
                print_color(Colors.YELLOW, f"  ⚠️  上传失败：{response.status_code}")
                return False
        except Exception as e:
            print_color(Colors.RED, f"  ❌ 上传错误：{e}")
            return False
    
    def update_local_memory(self, merged_records):
        """更新本地记忆文件"""
        # 合并远程记录到本地文件
        # 实际实现应该解析 Markdown 并合并
        pass


def main():
    """主函数"""
    syncer = ClawHubSync()
    syncer.sync()


if __name__ == "__main__":
    main()
