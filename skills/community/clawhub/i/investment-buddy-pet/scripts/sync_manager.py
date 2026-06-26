#!/usr/bin/env python3
"""
信息同步管理器
本地存储 + 可选云同步（iCloud/坚果云）
"""

import json
import sqlite3
import shutil
from datetime import datetime
from pathlib import Path

class SyncManager:
    """信息同步管理器"""
    
    def __init__(self, user_id, db_path=None):
        self.user_id = user_id
        self.db_path = db_path or Path(__file__).parent.parent / "data" / "pet_data.db"
        self.cloud_config = self.load_cloud_config()
        self.init_db()
    
    def load_cloud_config(self):
        """加载云同步配置"""
        config_file = Path(__file__).parent.parent / "config" / "sync.yaml"
        
        if config_file.exists():
            # 简化处理，实际应解析 YAML
            return {
                "enabled": False,
                "provider": "icloud",  # icloud/nutstore
                "remote_path": "/investment-buddy-pet/",
                "sync_interval": 3600  # 1 小时同步一次
            }
        
        return {
            "enabled": False,
            "provider": None,
            "remote_path": None,
            "sync_interval": 3600
        }
    
    def init_db(self):
        """初始化数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 创建用户表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                risk_tolerance INTEGER,
                investment_goal TEXT,
                sip_day INTEGER,
                sip_amount REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # 创建宠物表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pets (
                id TEXT PRIMARY KEY,
                user_id TEXT,
                pet_type TEXT,
                pet_level INTEGER DEFAULT 1,
                experience INTEGER DEFAULT 0,
                skills JSON,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        
        # 创建互动日志表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS interactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                event_type TEXT,
                xp_reward INTEGER,
                metadata JSON,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        
        # 创建持仓记录表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS holdings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                snapshot JSON,
                analysis_result JSON,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        
        # 创建同步记录表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sync_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                sync_type TEXT,  # upload/download
                status TEXT,     # success/failed
                synced_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                message TEXT
            )
        """)
        
        conn.commit()
        conn.close()
    
    def create_user(self, user_data):
        """创建用户"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            """INSERT OR REPLACE INTO users 
               (id, risk_tolerance, investment_goal, sip_day, sip_amount, updated_at)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (
                self.user_id,
                user_data.get("risk_tolerance", 3),
                user_data.get("investment_goal", "养老"),
                user_data.get("sip_day", 5),
                user_data.get("sip_amount", 2000),
                datetime.now().isoformat()
            )
        )
        
        conn.commit()
        conn.close()
        
        print(f"✅ 用户创建成功：{self.user_id}")
    
    def create_pet(self, pet_data):
        """创建宠物"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            """INSERT OR REPLACE INTO pets 
               (id, user_id, pet_type, pet_level, experience, skills, updated_at)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                f"{self.user_id}_pet",
                self.user_id,
                pet_data["pet_type"],
                1,
                0,
                json.dumps(["每日问候"]),
                datetime.now().isoformat()
            )
        )
        
        conn.commit()
        conn.close()
        
        print(f"✅ 宠物创建成功：{pet_data['pet_type']}")
    
    def log_interaction(self, event_type, xp_reward, metadata=None):
        """记录互动"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            """INSERT INTO interactions 
               (user_id, event_type, xp_reward, metadata)
               VALUES (?, ?, ?, ?)""",
            (self.user_id, event_type, xp_reward, json.dumps(metadata or {}))
        )
        
        # 更新宠物经验值
        cursor.execute(
            """UPDATE pets 
               SET experience = experience + ?, 
                   updated_at = ?
               WHERE user_id = ?""",
            (xp_reward, datetime.now().isoformat(), self.user_id)
        )
        
        conn.commit()
        conn.close()
        
        print(f"📝 互动记录：{event_type} (+{xp_reward}经验)")
    
    def save_holdings(self, snapshot, analysis_result):
        """保存持仓记录"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            """INSERT INTO holdings 
               (user_id, snapshot, analysis_result)
               VALUES (?, ?, ?)""",
            (self.user_id, json.dumps(snapshot), json.dumps(analysis_result))
        )
        
        conn.commit()
        conn.close()
        
        print(f"💼 持仓记录保存成功")
    
    def get_user_data(self):
        """获取用户数据"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 获取用户信息
        cursor.execute("SELECT * FROM users WHERE id = ?", (self.user_id,))
        user_row = cursor.fetchone()
        
        # 获取宠物信息
        cursor.execute("SELECT * FROM pets WHERE user_id = ?", (self.user_id,))
        pet_row = cursor.fetchone()
        
        # 获取互动统计
        cursor.execute(
            """SELECT event_type, COUNT(*), SUM(xp_reward) 
               FROM interactions 
               WHERE user_id = ? 
               GROUP BY event_type""",
            (self.user_id,)
        )
        interaction_stats = cursor.fetchall()
        
        # 获取最近持仓
        cursor.execute(
            """SELECT * FROM holdings 
               WHERE user_id = ? 
               ORDER BY created_at DESC 
               LIMIT 1""",
            (self.user_id,)
        )
        latest_holding = cursor.fetchone()
        
        conn.close()
        
        return {
            "user": user_row,
            "pet": pet_row,
            "interaction_stats": interaction_stats,
            "latest_holding": latest_holding
        }
    
    def export_data(self, output_path=None):
        """导出数据"""
        output_path = output_path or Path(__file__).parent.parent / "data" / f"{self.user_id}_export.json"
        
        data = self.get_user_data()
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"📤 数据导出成功：{output_path}")
        return output_path
    
    def sync_to_cloud(self):
        """同步到云端"""
        if not self.cloud_config["enabled"]:
            print("⚠️  云同步未启用")
            return False
        
        provider = self.cloud_config["provider"]
        
        if provider == "icloud":
            return self.sync_to_icloud()
        elif provider == "nutstore":
            return self.sync_to_nutstore()
        else:
            print(f"⚠️  不支持的云服务商：{provider}")
            return False
    
    def sync_to_icloud(self):
        """同步到 iCloud"""
        # 简化实现，实际应使用 iCloud API
        icloud_path = Path.home() / "Library" / "Mobile Documents" / "com~apple~CloudDocs" / self.cloud_config["remote_path"]
        
        if not icloud_path.exists():
            icloud_path.mkdir(parents=True, exist_ok=True)
        
        # 复制数据库文件
        shutil.copy(
            self.db_path,
            icloud_path / "pet_data.db"
        )
        
        print(f"☁️  已同步到 iCloud: {icloud_path}")
        return True
    
    def sync_from_cloud(self):
        """从云端同步"""
        if not self.cloud_config["enabled"]:
            print("⚠️  云同步未启用")
            return False
        
        provider = self.cloud_config["provider"]
        
        if provider == "icloud":
            icloud_path = Path.home() / "Library" / "Mobile Documents" / "com~apple~CloudDocs" / self.cloud_config["remote_path"] / "pet_data.db"
            
            if icloud_path.exists():
                shutil.copy(icloud_path, self.db_path)
                print(f"⬇️  已从 iCloud 同步：{icloud_path}")
                return True
        
        return False
    
    def log_sync(self, sync_type, status, message=""):
        """记录同步日志"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            """INSERT INTO sync_log 
               (user_id, sync_type, status, message)
               VALUES (?, ?, ?, ?)""",
            (self.user_id, sync_type, status, message)
        )
        
        conn.commit()
        conn.close()


def main():
    """测试同步管理器"""
    import argparse
    
    parser = argparse.ArgumentParser(description="信息同步管理器")
    parser.add_argument("--user-id", required=True, help="用户 ID")
    parser.add_argument("--action", choices=["create_user", "create_pet", "export", "sync_to", "sync_from"], help="操作类型")
    parser.add_argument("--pet-type", help="宠物类型（songguo/wugui/maotouying/lang/daxiang）")
    
    args = parser.parse_args()
    
    manager = SyncManager(user_id=args.user_id)
    
    if args.action == "create_user":
        user_data = {
            "risk_tolerance": 3,
            "investment_goal": "养老",
            "sip_day": 5,
            "sip_amount": 2000
        }
        manager.create_user(user_data)
    
    elif args.action == "create_pet" and args.pet_type:
        pet_data = {"pet_type": args.pet_type}
        manager.create_pet(pet_data)
    
    elif args.action == "export":
        manager.export_data()
    
    elif args.action == "sync_to":
        manager.sync_to_cloud()
    
    elif args.action == "sync_from":
        manager.sync_from_cloud()
    
    else:
        # 显示用户数据
        data = manager.get_user_data()
        print(f"\n用户数据：{data['user']}")
        print(f"宠物数据：{data['pet']}")
        print(f"互动统计：{data['interaction_stats']}")


if __name__ == "__main__":
    main()
