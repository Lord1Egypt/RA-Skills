#!/usr/bin/env python3
"""
心跳引擎 - 主动提醒系统
定期检查市场/用户状态，触发宠物主动提醒
集成合规检查器（Compliance Checker）
"""

import json
import time
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
import requests
import sys

# 导入合规检查器
sys.path.insert(0, str(Path(__file__).parent))
from compliance_checker import ComplianceChecker

class HeartbeatEngine:
    """心跳引擎（带合规检查）"""
    
    def __init__(self, user_id, pet_type=None, db_path=None):
        self.user_id = user_id
        self.db_path = db_path or Path(__file__).parent.parent / "data" / "pet_data.db"
        self.config = self.load_config()
        self.init_db()  # 先初始化数据库
        self.compliance = ComplianceChecker()  # 初始化合规检查器
        self.pet = self.load_pet(pet_type)  # 再加载宠物（支持传入 pet_type）
    
    def load_config(self):
        """加载配置"""
        return {
            "heartbeat_interval": 300,  # 5 分钟检查一次
            "market_check_url": "http://qt.gtimg.cn/q=s_sh000001,s_sz399001",
            "notification_channels": ["local", "email"],  # 本地通知/邮件
            "quiet_hours": {"start": 22, "end": 8}  # 安静时间（22:00-8:00）
        }
    
    def load_pet(self, pet_type=None):
        """加载宠物信息
        
        Args:
            pet_type: 宠物类型（如 'songguo'）。如未提供，则从数据库读取
        """
        # 优先使用传入的 pet_type
        if pet_type:
            pet_path = Path(__file__).parent.parent / "pets" / f"{pet_type}.json"
            if pet_path.exists():
                with open(pet_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        
        # 从数据库读取用户宠物
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT pet_type FROM pets WHERE user_id = ?",
            (self.user_id,)
        )
        result = cursor.fetchone()
        conn.close()
        
        if not result:
            return None
        
        pet_type = result[0]
        pet_path = Path(__file__).parent.parent / "pets" / f"{pet_type}.json"
        
        if pet_path.exists():
            with open(pet_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        return None
    
    def init_db(self):
        """初始化数据库"""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        # 创建用户表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                pet_type TEXT,
                sip_day INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # 创建宠物表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                pet_type TEXT,
                activated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                level INTEGER DEFAULT 1,
                xp INTEGER DEFAULT 0
            )
        """)
        
        # 创建提醒记录表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS notifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                trigger_type TEXT,
                message TEXT,
                priority TEXT,
                sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                acknowledged BOOLEAN DEFAULT FALSE
            )
        """)
        
        # 创建互动记录表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS interactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                action TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
    
    def check_market(self):
        """检查市场状态"""
        try:
            response = requests.get(self.config["market_check_url"], timeout=5)
            data = response.text
            
            # 解析腾讯 API 返回（非 JSON 格式）
            # 格式：v_s_sh000001="51~上证指数~3052.14~..."
            parts = data.split('~')
            if len(parts) > 3:
                current_price = float(parts[3])
                # 计算涨跌幅（需要昨日收盘价，简化处理）
                change_percent = float(parts[32]) if len(parts) > 32 else 0
                
                return {
                    "index": "上证指数",
                    "price": current_price,
                    "change_percent": change_percent,
                    "timestamp": datetime.now()
                }
        except Exception as e:
            print(f"市场数据获取失败：{e}")
        
        return None
    
    def check_user_status(self):
        """检查用户状态"""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        # 检查定投日
        cursor.execute(
            "SELECT sip_day FROM users WHERE id = ?",
            (self.user_id,)
        )
        result = cursor.fetchone()
        sip_day = result[0] if result else None
        
        today = datetime.now().day
        is_sip_day = (sip_day == today) if sip_day else False
        
        # 检查最近互动时间
        cursor.execute(
            "SELECT MAX(created_at) FROM interactions WHERE user_id = ?",
            (self.user_id,)
        )
        last_interaction = cursor.fetchone()[0]
        
        days_since_interaction = None
        if last_interaction:
            last_dt = datetime.fromisoformat(last_interaction)
            days_since_interaction = (datetime.now() - last_dt).days
        
        conn.close()
        
        return {
            "is_sip_day": is_sip_day,
            "last_interaction_days": days_since_interaction
        }
    
    def is_quiet_hours(self):
        """检查是否在安静时间"""
        current_hour = datetime.now().hour
        quiet_start = self.config["quiet_hours"]["start"]
        quiet_end = self.config["quiet_hours"]["end"]
        
        if quiet_start > quiet_end:  # 跨天情况（如 22:00-8:00）
            return current_hour >= quiet_start or current_hour < quiet_end
        else:
            return quiet_start <= current_hour < quiet_end
    
    def generate_trigger(self, market_data, user_status):
        """生成触发（带合规检查）"""
        triggers = []
        
        if not self.pet:
            return triggers
        
        # 1. 市场波动触发
        if market_data:
            change = market_data["change_percent"]
            
            if change < -5 and self.pet["personality_traits"]["intervention_level"] > 50:
                message = self.generate_compliant_message(
                    "market_drop",
                    {"percent": change},
                    needs_disclaimer=True
                )
                triggers.append({
                    "type": "market_drop",
                    "priority": "high",
                    "message": message,
                    "pet_id": self.pet["pet_id"],
                    "compliance_checked": True
                })
            elif change > 5 and self.pet["personality_traits"]["proactivity_level"] > 60:
                message = self.generate_compliant_message(
                    "market_rise",
                    {"percent": change},
                    needs_disclaimer=True
                )
                triggers.append({
                    "type": "market_rise",
                    "priority": "medium",
                    "message": message,
                    "pet_id": self.pet["pet_id"],
                    "compliance_checked": True
                })
        
        # 2. 定投日触发
        if user_status["is_sip_day"] and self.pet["personality_traits"]["proactivity_level"] > 60:
            message = self.generate_compliant_message(
                "sip_reminder",
                None,
                needs_disclaimer=False
            )
            triggers.append({
                "type": "sip_reminder",
                "priority": "medium",
                "message": message,
                "pet_id": self.pet["pet_id"],
                "compliance_checked": True
            })
        
        # 3. 长时间未互动触发
        if user_status["last_interaction_days"] and user_status["last_interaction_days"] > 7:
            message = self.generate_compliant_message(
                "inactive_reminder",
                None,
                needs_disclaimer=False
            )
            triggers.append({
                "type": "inactive_reminder",
                "priority": "low",
                "message": message,
                "pet_id": self.pet["pet_id"],
                "compliance_checked": True
            })
        
        return triggers
    
    def generate_compliant_message(self, trigger_type, data=None, needs_disclaimer=False):
        """生成合规消息"""
        # 1. 从宠物配置获取话术模板
        templates = self.pet.get("talk_templates", {})
        template = templates.get(trigger_type, "...")
        
        # 2. 填充数据
        if data:
            try:
                message = template.format(**data)
            except KeyError:
                message = template
        else:
            message = template
        
        # 3. 应用人格化风格
        message = self.apply_personality_style(message)
        
        # 4. 合规检查
        context = {"needs_disclaimer": needs_disclaimer}
        check_result = self.compliance.check_message(message, context)
        
        # 5. 如果不合规，修复
        if not check_result["is_compliant"]:
            message = self.fix_compliance_violation(message, check_result["violations"])
        
        # 6. 添加风险提示（如果需要）
        if needs_disclaimer:
            message = self.add_personality_disclaimer(message)
        
        return message
    
    def apply_personality_style(self, message):
        """应用人格化风格"""
        style = self.pet.get("communication_style", "friendly")
        
        style_handlers = {
            "warm": lambda m: m + "哦~" if not m.endswith(("哦", "~", "呢")) else m,
            "calm": lambda m: m.replace("!", "。").replace("~", "。"),
            "rational": lambda m: m + " 数据仅供参考。",
            "decisive": lambda m: m + "！" if not m.endswith("！") else m,
            "witty": lambda m: m + " 机智如我~",
            "friendly": lambda m: m + "呀~",
            "visionary": lambda m: m + " 未来已来！",
            "energetic": lambda m: m + " 加油！"
        }
        
        handler = style_handlers.get(style, lambda m: m)
        return handler(message)
    
    def add_personality_disclaimer(self, message):
        """添加人格化风险提示"""
        style = self.pet.get("communication_style", "friendly")
        
        disclaimer_templates = {
            "warm": "💡 投资有风险，要谨慎决策哦~",
            "calm": "市场有风险。请独立判断。",
            "rational": "风险提示：历史数据不代表未来表现。",
            "decisive": "风险自负！不要盲目跟风！",
            "witty": "投资有风险，别全听我的~ 机智如我",
            "friendly": "记得哦，投资有风险，要自己判断呀~",
            "visionary": "未来不确定，投资需谨慎。",
            "energetic": "冲之前先想好风险！"
        }
        
        disclaimer = disclaimer_templates.get(style, "市场有风险，投资需谨慎")
        return f"{message}\n\n{disclaimer}"
    
    def fix_compliance_violation(self, message, violations):
        """修复合规违规"""
        for v in violations:
            if v["type"] == "specific_recommendation":
                message = message.replace(
                    "买这个基金",
                    "我可以教你筛选方法，但不会推荐具体产品"
                )
            elif v["type"] == "return_promise":
                message = message.replace(
                    "肯定赚钱",
                    "历史业绩不代表未来表现"
                )
            elif v["type"] == "fear_tactics":
                message = message.replace(
                    "赶紧买",
                    "理性决策"
                )
        
        return message
    
    def send_notification(self, trigger):
        """发送通知"""
        # 检查安静时间
        if self.is_quiet_hours() and trigger["priority"] == "low":
            print(f"安静时间，跳过低优先级通知：{trigger['type']}")
            return False
        
        # 保存到数据库
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        cursor.execute(
            """INSERT INTO notifications 
               (user_id, trigger_type, message, priority) 
               VALUES (?, ?, ?, ?)""",
            (self.user_id, trigger["type"], trigger["message"], trigger["priority"])
        )
        
        conn.commit()
        conn.close()
        
        # 打印通知（实际应推送到用户设备）
        print(f"\n🔔 [{trigger['priority'].upper()}] {trigger['pet_id']}: {trigger['message']}")
        
        return True
    
    def tick(self):
        """执行一次心跳检查"""
        print(f"\n[{datetime.now().isoformat()}] 心跳检查...")
        
        # 1. 检查市场
        market_data = self.check_market()
        if market_data:
            print(f"市场：{market_data['index']} {market_data['price']} ({market_data['change_percent']}%)")
        
        # 2. 检查用户状态
        user_status = self.check_user_status()
        print(f"用户状态：定投日={user_status['is_sip_day']}, 最近互动={user_status['last_interaction_days']}天前")
        
        # 3. 生成触发
        triggers = self.generate_trigger(market_data, user_status)
        
        # 4. 发送通知
        for trigger in triggers:
            self.send_notification(trigger)
        
        return triggers
    
    def start(self):
        """启动心跳引擎"""
        print(f"🚀 心跳引擎启动（用户：{self.user_id}）")
        print(f"宠物：{self.pet['name'] if self.pet else '未加载'}")
        print(f"检查间隔：{self.config['heartbeat_interval']}秒")
        print(f"安静时间：{self.config['quiet_hours']['start']}:00 - {self.config['quiet_hours']['end']}:00")
        
        try:
            while True:
                self.tick()
                time.sleep(self.config["heartbeat_interval"])
        except KeyboardInterrupt:
            print("\n⏹️ 心跳引擎停止")


def main():
    """测试心跳引擎"""
    import argparse
    
    parser = argparse.ArgumentParser(description="心跳引擎 - 主动提醒系统")
    parser.add_argument("--user-id", required=True, help="用户 ID")
    parser.add_argument("--pet-type", type=str, default=None, help="宠物类型（如 songguo, wugui）")
    parser.add_argument("--once", action="store_true", help="只执行一次（测试用）")
    
    args = parser.parse_args()
    
    engine = HeartbeatEngine(user_id=args.user_id, pet_type=args.pet_type)
    
    if args.once:
        # 只执行一次
        engine.tick()
    else:
        # 持续运行
        engine.start()


if __name__ == "__main__":
    main()
