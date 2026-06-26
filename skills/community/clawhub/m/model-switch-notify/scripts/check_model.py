#!/usr/bin/env python3
"""
模型切换检查脚本 v3.0
只使用 SQLite 存储，支持心跳检测机制
"""

import json
import argparse
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

# 数据目录
DATA_DIR = Path("/home/wljmmx/.openclaw/data")
DB_PATH = DATA_DIR / "model-switch.db"


class ModelStateManager:
    """模型状态管理器，使用 SQLite 存储"""
    
    def __init__(self):
        self._init_db()
    
    def _init_db(self):
        """初始化 SQLite 数据库"""
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS model_states (
                agent_id TEXT PRIMARY KEY,
                last_model TEXT NOT NULL,
                last_notify TIMESTAMP,
                last_heartbeat TIMESTAMP,
                channel TEXT,
                session TEXT,
                pending_notify INTEGER DEFAULT 0,
                pending_message TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()
    
    def load_state(self, agent_id: str) -> Dict[str, Any]:
        """从 SQLite 加载状态"""
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()
        cursor.execute(
            """SELECT last_model, last_notify, last_heartbeat, channel, session, 
                      pending_notify, pending_message 
               FROM model_states WHERE agent_id = ?""",
            (agent_id,)
        )
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                "lastModel": row[0],
                "lastNotify": row[1],
                "lastHeartbeat": row[2],
                "channel": row[3],
                "session": row[4],
                "pendingNotify": bool(row[5]) if row[5] else False,
                "pendingMessage": row[6]
            }
        return {
            "lastModel": None,
            "lastNotify": None,
            "lastHeartbeat": None,
            "channel": None,
            "session": None,
            "pendingNotify": False,
            "pendingMessage": None
        }
    
    def save_state(self, agent_id: str, model: str, channel: str, session: str) -> None:
        """保存状态到 SQLite"""
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()
        
        now = datetime.now().isoformat()
        cursor.execute('''
            INSERT INTO model_states (agent_id, last_model, last_notify, last_heartbeat, channel, session, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(agent_id) DO UPDATE SET
                last_model = excluded.last_model,
                last_notify = excluded.last_notify,
                channel = excluded.channel,
                session = excluded.session,
                updated_at = excluded.updated_at,
                pending_notify = 0,
                pending_message = NULL
        ''', (agent_id, model, now, now, channel, session, now))
        
        conn.commit()
        conn.close()
    
    def update_heartbeat(self, agent_id: str, model: str) -> None:
        """更新心跳时间戳"""
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()
        
        now = datetime.now().isoformat()
        cursor.execute('''
            INSERT INTO model_states (agent_id, last_model, last_heartbeat, updated_at)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(agent_id) DO UPDATE SET
                last_heartbeat = excluded.last_heartbeat,
                updated_at = excluded.updated_at
        ''', (agent_id, model, now, now))
        
        conn.commit()
        conn.close()
    
    def set_pending_notify(self, agent_id: str, model: str, message: str) -> None:
        """设置待发送通知（消息中断时使用）"""
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()
        
        now = datetime.now().isoformat()
        cursor.execute('''
            INSERT INTO model_states (agent_id, last_model, pending_notify, pending_message, updated_at)
            VALUES (?, ?, 1, ?, ?)
            ON CONFLICT(agent_id) DO UPDATE SET
                last_model = excluded.last_model,
                pending_notify = 1,
                pending_message = excluded.pending_message,
                updated_at = excluded.updated_at
        ''', (agent_id, model, message, now))
        
        conn.commit()
        conn.close()
    
    def clear_pending_notify(self, agent_id: str) -> None:
        """清除待发送通知"""
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE model_states SET pending_notify = 0, pending_message = NULL 
            WHERE agent_id = ?
        ''', (agent_id,))
        conn.commit()
        conn.close()
    
    def get_pending_notify(self, agent_id: str) -> Dict[str, Any]:
        """获取待发送通知"""
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()
        cursor.execute(
            "SELECT pending_notify, pending_message FROM model_states WHERE agent_id = ?",
            (agent_id,)
        )
        row = cursor.fetchone()
        conn.close()
        
        if row and row[0]:
            return {
                "hasPending": True,
                "message": row[1]
            }
        return {"hasPending": False, "message": None}
    
    def list_all(self) -> list:
        """列出所有 agent 状态"""
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()
        cursor.execute("""
            SELECT agent_id, last_model, last_notify, last_heartbeat, channel, pending_notify 
            FROM model_states ORDER BY updated_at DESC
        """)
        rows = cursor.fetchall()
        conn.close()
        
        return [
            {
                "agentId": row[0],
                "lastModel": row[1],
                "lastNotify": row[2],
                "lastHeartbeat": row[3],
                "channel": row[4],
                "pendingNotify": bool(row[5]) if row[5] else False
            }
            for row in rows
        ]
    
    def reset_state(self, agent_id: str) -> bool:
        """重置状态"""
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()
        cursor.execute("DELETE FROM model_states WHERE agent_id = ?", (agent_id,))
        deleted = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return deleted


def check_model_change(manager: ModelStateManager, agent_id: str, current_model: str, 
                       channel: str, session: str) -> Dict[str, Any]:
    """
    检查模型是否变化（心跳检测）
    
    每次会话回复时调用此函数：
    1. 检查是否有待发送通知（上次中断时）
    2. 检查模型是否变化
    3. 更新心跳时间戳
    
    Returns:
        dict: {
            "changed": bool,
            "previousModel": str or None,
            "currentModel": str,
            "shouldNotify": bool,
            "notifyMessage": str,
            "firstTime": bool,
            "pendingNotify": bool,
            "pendingMessage": str or None
        }
    """
    previous_state = manager.load_state(agent_id)
    previous_model = previous_state.get("lastModel")
    pending_notify = previous_state.get("pendingNotify", False)
    pending_message = previous_state.get("pendingMessage")
    
    # 检查是否有待发送通知
    has_pending = pending_notify and pending_message
    
    # 判断是否首次使用
    first_time = previous_model is None
    
    # 判断模型是否变化
    changed = previous_model != current_model
    
    # 判断是否需要通知
    should_notify = first_time or changed or has_pending
    
    # 生成通知消息
    if has_pending:
        notify_message = pending_message
    elif first_time:
        notify_message = f"当前使用模型：{current_model}"
    elif changed:
        notify_message = f"老板，模型已切换，当前使用：{current_model}"
    else:
        notify_message = ""
    
    # 保存当前状态并清除待发送通知
    if should_notify:
        manager.save_state(agent_id, current_model, channel, session)
    else:
        # 只更新心跳
        manager.update_heartbeat(agent_id, current_model)
    
    return {
        "changed": changed,
        "previousModel": previous_model,
        "currentModel": current_model,
        "shouldNotify": should_notify,
        "notifyMessage": notify_message,
        "firstTime": first_time,
        "pendingNotify": has_pending,
        "pendingMessage": pending_message if has_pending else None
    }


def set_interrupt_notify(manager: ModelStateManager, agent_id: str, model: str, message: str) -> Dict[str, Any]:
    """
    设置中断通知（消息中断时调用）
    
    当消息发送中断时，调用此函数保存待通知状态，
    下次会话时会在第一条消息中通知用户。
    """
    manager.set_pending_notify(agent_id, model, message)
    return {
        "success": True,
        "message": "待发送通知已保存，下次会话时将通知用户"
    }


def main():
    parser = argparse.ArgumentParser(description="模型切换检查工具 v3.0 (SQLite 存储 + 心跳检测)")
    
    subparsers = parser.add_subparsers(dest="command", help="命令")
    
    # check 命令 - 心跳检测
    check_parser = subparsers.add_parser("check", help="检查模型变化（心跳检测）")
    check_parser.add_argument("--agent", required=True, help="agent 标识")
    check_parser.add_argument("--current-model", required=True, help="当前模型名称")
    check_parser.add_argument("--channel", required=True, help="当前渠道")
    check_parser.add_argument("--session", required=True, help="当前会话 ID")
    
    # heartbeat 命令 - 更新心跳
    hb_parser = subparsers.add_parser("heartbeat", help="更新心跳时间戳")
    hb_parser.add_argument("--agent", required=True, help="agent 标识")
    hb_parser.add_argument("--current-model", required=True, help="当前模型名称")
    
    # interrupt 命令 - 设置中断通知
    int_parser = subparsers.add_parser("interrupt", help="设置中断通知（消息中断时）")
    int_parser.add_argument("--agent", required=True, help="agent 标识")
    int_parser.add_argument("--model", required=True, help="当前模型")
    int_parser.add_argument("--message", required=True, help="待发送的通知消息")
    
    # get 命令
    get_parser = subparsers.add_parser("get", help="获取当前模型信息")
    get_parser.add_argument("--agent", required=True, help="agent 标识")
    
    # reset 命令
    reset_parser = subparsers.add_parser("reset", help="重置模型状态")
    reset_parser.add_argument("--agent", required=True, help="agent 标识")
    
    # list 命令
    subparsers.add_parser("list", help="列出所有 agent 状态")
    
    args = parser.parse_args()
    
    manager = ModelStateManager()
    
    if args.command == "check":
        result = check_model_change(
            manager=manager,
            agent_id=args.agent,
            current_model=args.current_model,
            channel=args.channel,
            session=args.session
        )
    elif args.command == "heartbeat":
        manager.update_heartbeat(args.agent, args.current_model)
        result = {"success": True, "message": "Heartbeat updated"}
    elif args.command == "interrupt":
        result = set_interrupt_notify(manager, args.agent, args.model, args.message)
    elif args.command == "get":
        state = manager.load_state(args.agent)
        result = {
            "agentId": args.agent,
            "currentModel": state.get("lastModel"),
            "lastNotify": state.get("lastNotify"),
            "lastHeartbeat": state.get("lastHeartbeat"),
            "channel": state.get("channel"),
            "session": state.get("session"),
            "pendingNotify": state.get("pendingNotify", False),
            "pendingMessage": state.get("pendingMessage")
        }
    elif args.command == "reset":
        success = manager.reset_state(args.agent)
        result = {"success": success, "message": f"Model state reset for {args.agent}"}
    elif args.command == "list":
        result = {"agents": manager.list_all()}
    else:
        parser.print_help()
        return
    
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()