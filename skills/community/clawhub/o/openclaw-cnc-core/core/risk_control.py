#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CNC 智能报价系统 - P0 风险控制模块
版本：v1.0 (P0)
功能：人工审核标记、管理员通知、异常处理
"""

import json
import os
import logging
import sqlite3
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ReviewStatus(Enum):
    """审核状态"""
    PENDING = "PENDING"  # 待审核
    IN_PROGRESS = "IN_PROGRESS"  # 审核中
    APPROVED = "APPROVED"  # 已批准
    REJECTED = "REJECTED"  # 已拒绝 (需重新报价)
    ESCALATED = "ESCALATED"  # 已升级 (转交上级)


@dataclass
class ReviewTask:
    """审核任务数据结构"""
    task_id: str
    order_id: str
    customer: str
    reason: str  # 审核原因
    quote_data: dict  # 报价数据
    raw_text: str  # 原始邮件文本 (脱敏后)
    status: ReviewStatus
    created_at: str
    assigned_to: Optional[str] = None  # 分配给谁审核
    reviewed_at: Optional[str] = None
    reviewed_by: Optional[str] = None
    review_notes: Optional[str] = None
    corrected_surface_type: Optional[str] = None  # 人工修正后的表面处理类型
    
    def to_dict(self) -> dict:
        result = asdict(self)
        result['status'] = self.status.value
        return result


class RiskControl:
    """
    风险控制模块
    
    核心功能:
    1. 检测需要人工审核的报价
    2. 创建审核任务
    3. 发送管理员通知
    4. 记录审核历史
    """
    
    def __init__(self, db_path: str, notifier=None):
        """
        初始化风险控制模块
        
        Args:
            db_path: SQLite 数据库路径
            notifier: 通知器实例 (可选)
        """
        self.db_path = db_path
        self.notifier = notifier
        
        # 确保数据库目录存在
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        # 初始化数据库
        self._init_database()
        
        logger.info(f"风险控制模块初始化完成，数据库：{db_path}")
    
    def _init_database(self):
        """初始化数据库表结构"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 审核任务表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS review_tasks (
                task_id TEXT PRIMARY KEY,
                order_id TEXT NOT NULL,
                customer TEXT,
                reason TEXT NOT NULL,
                quote_data TEXT,  -- JSON
                raw_text TEXT,
                status TEXT DEFAULT 'PENDING',
                assigned_to TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                reviewed_at TIMESTAMP,
                reviewed_by TEXT,
                review_notes TEXT,
                corrected_surface_type TEXT
            )
        ''')
        
        # 审核历史表 (用于 P1 训练)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS review_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id TEXT NOT NULL,
                order_id TEXT NOT NULL,
                original_surface_type TEXT,
                corrected_surface_type TEXT,
                reason TEXT,
                reviewed_by TEXT,
                reviewed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (task_id) REFERENCES review_tasks(task_id)
            )
        ''')
        
        # 创建索引
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_review_status ON review_tasks(status)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_review_order ON review_tasks(order_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_review_assigned ON review_tasks(assigned_to)')
        
        conn.commit()
        conn.close()
        
        logger.info("数据库表结构初始化完成")
    
    def handle_unknown_surface(self, order_data: dict, quote_result: dict) -> ReviewTask:
        """
        处理 UNKNOWN 表面处理情况 - 🔴 关键风险控制点
        
        流程:
        1. 创建审核任务
        2. 保存到数据库
        3. 发送管理员通知
        4. ❌ 不发送报价单给客户
        
        Args:
            order_data: 原始订单数据
            quote_result: 报价引擎返回的结果
        
        Returns:
            ReviewTask 创建的审核任务
        """
        # ========== 步骤 1: 创建审核任务 ==========
        task_id = f"REVIEW-{datetime.now().strftime('%Y%m%d%H%M%S')}-{order_data.get('order_id', 'UNKNOWN')}"
        
        task = ReviewTask(
            task_id=task_id,
            order_id=order_data.get("order_id", "UNKNOWN"),
            customer=order_data.get("customer", "未知客户"),
            reason="表面处理类型未识别 (UNKNOWN)",
            quote_data=quote_result,
            raw_text=order_data.get("raw_text", "")[:500],  # 截取前 500 字
            status=ReviewStatus.PENDING,
            created_at=datetime.now().isoformat(),
            assigned_to=None
        )
        
        # ========== 步骤 2: 保存到数据库 ==========
        self._save_review_task(task)
        
        # ========== 步骤 3: 发送管理员通知 ==========
        if self.notifier:
            self.notifier.send_alert({
                "type": "MANUAL_REVIEW_REQUIRED",
                "task_id": task_id,
                "order_id": task.order_id,
                "customer": task.customer,
                "reason": task.reason,
                "material": order_data.get("material", "未知"),
                "volume": order_data.get("volume_cm3", 0),
                "area": order_data.get("area_dm2", 0),
                "raw_text_snippet": task.raw_text[:200],
                "created_at": task.created_at,
                "action_url": f"/admin/review/{task_id}"  # 审核界面链接
            })
        
        # ========== 步骤 4: 🔴 禁止发送报价单 ==========
        # (不调用 email_sender.send_quote())
        # 这个逻辑由调用方控制
        
        logger.warning(f"创建审核任务：{task_id}, 订单：{task.order_id}, 原因：{task.reason}")
        
        return task
    
    def handle_low_confidence(self, order_data: dict, quote_result: dict, 
                               confidence: float, threshold: float = 0.5) -> ReviewTask:
        """
        处理低置信度识别情况
        
        Args:
            order_data: 原始订单数据
            quote_result: 报价引擎返回的结果
            confidence: 识别置信度
            threshold: 置信度阈值
        
        Returns:
            ReviewTask 创建的审核任务
        """
        task_id = f"REVIEW-{datetime.now().strftime('%Y%m%d%H%M%S')}-{order_data.get('order_id', 'UNKNOWN')}"
        
        task = ReviewTask(
            task_id=task_id,
            order_id=order_data.get("order_id", "UNKNOWN"),
            customer=order_data.get("customer", "未知客户"),
            reason=f"表面处理识别置信度低 ({confidence:.2f} < {threshold})",
            quote_data=quote_result,
            raw_text=order_data.get("raw_text", "")[:500],
            status=ReviewStatus.PENDING,
            created_at=datetime.now().isoformat(),
            assigned_to=None
        )
        
        self._save_review_task(task)
        
        if self.notifier:
            self.notifier.send_alert({
                "type": "LOW_CONFIDENCE_REVIEW",
                "task_id": task_id,
                "order_id": task.order_id,
                "customer": task.customer,
                "reason": task.reason,
                "surface_type": quote_result.get("surface_type", "未知"),
                "confidence": confidence,
                "threshold": threshold,
                "raw_text_snippet": task.raw_text[:200],
                "created_at": task.created_at,
                "action_url": f"/admin/review/{task_id}"
            })
        
        logger.warning(f"创建低置信度审核任务：{task_id}, 置信度：{confidence:.2f}")
        
        return task
    
    def _save_review_task(self, task: ReviewTask):
        """保存审核任务到数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO review_tasks 
            (task_id, order_id, customer, reason, quote_data, raw_text, status, assigned_to, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            task.task_id,
            task.order_id,
            task.customer,
            task.reason,
            json.dumps(task.quote_data, ensure_ascii=False),
            task.raw_text,
            task.status.value,
            task.assigned_to,
            task.created_at
        ))
        
        conn.commit()
        conn.close()
    
    def approve_review(self, task_id: str, reviewer: str, 
                        corrected_surface_type: str, notes: str = None) -> bool:
        """
        批准审核任务
        
        Args:
            task_id: 审核任务 ID
            reviewer: 审核人
            corrected_surface_type: 人工修正后的表面处理类型
            notes: 审核备注
        
        Returns:
            bool 是否成功
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        reviewed_at = datetime.now().isoformat()
        
        # 更新审核任务
        cursor.execute('''
            UPDATE review_tasks 
            SET status = ?, reviewed_at = ?, reviewed_by = ?, 
                review_notes = ?, corrected_surface_type = ?
            WHERE task_id = ?
        ''', (
            ReviewStatus.APPROVED.value,
            reviewed_at,
            reviewer,
            notes,
            corrected_surface_type,
            task_id
        ))
        
        # 获取任务信息 (用于记录历史)
        cursor.execute('SELECT order_id, corrected_surface_type FROM review_tasks WHERE task_id = ?', (task_id,))
        row = cursor.fetchone()
        
        if row:
            order_id, original_surface_type = row
            
            # 记录审核历史
            cursor.execute('''
                INSERT INTO review_history 
                (task_id, order_id, original_surface_type, corrected_surface_type, reason, reviewed_by, reviewed_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                task_id,
                order_id,
                original_surface_type,
                corrected_surface_type,
                "人工审核修正",
                reviewer,
                reviewed_at
            ))
        
        conn.commit()
        conn.close()
        
        logger.info(f"审核任务批准：{task_id}, 审核人：{reviewer}, 修正类型：{corrected_surface_type}")
        
        return True
    
    def reject_review(self, task_id: str, reviewer: str, notes: str = None) -> bool:
        """
        拒绝审核任务 (需要重新报价)
        
        Args:
            task_id: 审核任务 ID
            reviewer: 审核人
            notes: 审核备注
        
        Returns:
            bool 是否成功
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE review_tasks 
            SET status = ?, reviewed_at = ?, reviewed_by = ?, review_notes = ?
            WHERE task_id = ?
        ''', (
            ReviewStatus.REJECTED.value,
            datetime.now().isoformat(),
            reviewer,
            notes,
            task_id
        ))
        
        conn.commit()
        conn.close()
        
        logger.info(f"审核任务拒绝：{task_id}, 审核人：{reviewer}, 备注：{notes}")
        
        return True
    
    def get_pending_tasks(self, limit: int = 20) -> List[ReviewTask]:
        """
        获取待审核任务列表
        
        Args:
            limit: 返回数量限制
        
        Returns:
            List[ReviewTask] 待审核任务列表
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT task_id, order_id, customer, reason, quote_data, raw_text, 
                   status, assigned_to, created_at
            FROM review_tasks 
            WHERE status = ? 
            ORDER BY created_at ASC 
            LIMIT ?
        ''', (ReviewStatus.PENDING.value, limit))
        
        rows = cursor.fetchall()
        conn.close()
        
        tasks = []
        for row in rows:
            task = ReviewTask(
                task_id=row[0],
                order_id=row[1],
                customer=row[2],
                reason=row[3],
                quote_data=json.loads(row[4]) if row[4] else {},
                raw_text=row[5],
                status=ReviewStatus(row[6]),
                assigned_to=row[7],
                created_at=row[8]
            )
            tasks.append(task)
        
        return tasks
    
    def get_review_statistics(self) -> dict:
        """
        获取审核统计数据
        
        Returns:
            dict 统计信息
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 各状态任务数
        cursor.execute('''
            SELECT status, COUNT(*) 
            FROM review_tasks 
            GROUP BY status
        ''')
        status_counts = dict(cursor.fetchall())
        
        # 今日审核数
        today = datetime.now().strftime('%Y-%m-%d')
        cursor.execute('''
            SELECT COUNT(*) 
            FROM review_tasks 
            WHERE reviewed_at LIKE ?
        ''', (f"{today}%",))
        today_count = cursor.fetchone()[0]
        
        # 平均审核时长 (分钟)
        cursor.execute('''
            SELECT AVG(
                (julianday(reviewed_at) - julianday(created_at)) * 24 * 60
            )
            FROM review_tasks 
            WHERE reviewed_at IS NOT NULL
        ''')
        avg_review_time = cursor.fetchone()[0] or 0
        
        conn.close()
        
        return {
            "pending": status_counts.get(ReviewStatus.PENDING.value, 0),
            "in_progress": status_counts.get(ReviewStatus.IN_PROGRESS.value, 0),
            "approved": status_counts.get(ReviewStatus.APPROVED.value, 0),
            "rejected": status_counts.get(ReviewStatus.REJECTED.value, 0),
            "today_count": today_count,
            "avg_review_time_minutes": round(avg_review_time, 1)
        }


# ========== 管理员通知器 ==========

class AdminNotifier:
    """
    管理员通知器
    
    支持多种通知方式:
    - 飞书机器人
    - 邮件
    - 短信 (可选)
    """
    
    def __init__(self, feishu_webhook: str = None):
        """
        初始化通知器
        
        Args:
            feishu_webhook: 飞书机器人 Webhook URL
        """
        self.feishu_webhook = feishu_webhook
    
    def send_alert(self, alert_data: dict):
        """
        发送告警通知
        
        Args:
            alert_data: 告警数据
        """
        # 飞书通知
        if self.feishu_webhook:
            self._send_feishu_alert(alert_data)
        
        # 日志记录
        logger.info(f"发送管理员通知：{alert_data.get('type')} - {alert_data.get('order_id')}")
    
    def _send_feishu_alert(self, alert_data: dict):
        """发送飞书卡片通知"""
        import requests
        
        alert_type = alert_data.get("type", "UNKNOWN")
        
        # 构建飞书卡片
        if alert_type == "MANUAL_REVIEW_REQUIRED":
            card = self._build_unknown_surface_card(alert_data)
        elif alert_type == "LOW_CONFIDENCE_REVIEW":
            card = self._build_low_confidence_card(alert_data)
        else:
            card = self._build_generic_card(alert_data)
        
        try:
            response = requests.post(self.feishu_webhook, json=card, timeout=10)
            if response.status_code == 200:
                logger.info(f"飞书通知发送成功：{alert_data.get('task_id')}")
            else:
                logger.error(f"飞书通知发送失败：{response.status_code}")
        except Exception as e:
            logger.error(f"飞书通知发送异常：{e}")
    
    def _build_unknown_surface_card(self, data: dict) -> dict:
        """构建 UNKNOWN 表面处理通知卡片"""
        return {
            "msg_type": "interactive",
            "card": {
                "config": {
                    "wide_screen_mode": True
                },
                "header": {
                    "template": "red",
                    "title": {
                        "content": "🔴 CNC 报价 - 人工审核提醒",
                        "tag": "plain_text"
                    }
                },
                "elements": [
                    {
                        "tag": "div",
                        "text": {
                            "tag": "lark_md",
                            "content": f"**订单号**: {data.get('order_id')}\n**客户**: {data.get('customer')}\n**材料**: {data.get('material')}\n**体积**: {data.get('volume')} cm³\n**面积**: {data.get('area')} dm²"
                        }
                    },
                    {
                        "tag": "divider"
                    },
                    {
                        "tag": "div",
                        "text": {
                            "tag": "lark_md",
                            "content": f"**⚠️ 问题**: {data.get('reason')}"
                        }
                    },
                    {
                        "tag": "div",
                        "text": {
                            "tag": "lark_md",
                            "content": f"**原始文本片段**:\n{data.get('raw_text_snippet', '无')}"
                        }
                    },
                    {
                        "tag": "action",
                        "actions": [
                            {
                                "tag": "button",
                                "text": {
                                    "tag": "plain_text",
                                    "content": "立即审核"
                                },
                                "type": "primary",
                                "url": data.get("action_url", "#")
                            },
                            {
                                "tag": "button",
                                "text": {
                                    "tag": "plain_text",
                                    "content": "稍后处理"
                                },
                                "type": "default"
                            }
                        ]
                    }
                ]
            }
        }
    
    def _build_low_confidence_card(self, data: dict) -> dict:
        """构建低置信度通知卡片"""
        return {
            "msg_type": "interactive",
            "card": {
                "config": {
                    "wide_screen_mode": True
                },
                "header": {
                    "template": "yellow",
                    "title": {
                        "content": "⚠️ CNC 报价 - 低置信度审核",
                        "tag": "plain_text"
                    }
                },
                "elements": [
                    {
                        "tag": "div",
                        "text": {
                            "tag": "lark_md",
                            "content": f"**订单号**: {data.get('order_id')}\n**客户**: {data.get('customer')}\n**识别结果**: {data.get('surface_type')}\n**置信度**: {data.get('confidence'):.2f} (阈值：{data.get('threshold')})"
                        }
                    },
                    {
                        "tag": "divider"
                    },
                    {
                        "tag": "div",
                        "text": {
                            "tag": "lark_md",
                            "content": f"**⚠️ 问题**: {data.get('reason')}"
                        }
                    },
                    {
                        "tag": "action",
                        "actions": [
                            {
                                "tag": "button",
                                "text": {
                                    "tag": "plain_text",
                                    "content": "立即审核"
                                },
                                "type": "primary",
                                "url": data.get("action_url", "#")
                            }
                        ]
                    }
                ]
            }
        }
    
    def _build_generic_card(self, data: dict) -> dict:
        """构建通用通知卡片"""
        return {
            "msg_type": "text",
            "content": {
                "text": f"CNC 报价系统通知\n类型：{data.get('type')}\n订单：{data.get('order_id')}\n详情：{data.get('reason', '无')}"
            }
        }


# ========== 测试代码 ==========

if __name__ == "__main__":
    # 测试风险控制模块
    db_path = os.path.join(os.path.dirname(__file__), "database", "risk_control.db")
    notifier = AdminNotifier()  # 实际使用时传入飞书 webhook
    
    risk_control = RiskControl(db_path, notifier)
    
    # 测试 UNKNOWN 情况
    order_data = {
        "order_id": "TEST-RISK-001",
        "customer": "测试客户",
        "material": "不锈钢 304",
        "volume_cm3": 50,
        "area_dm2": 10,
        "raw_text": "需要表面防护处理，具体要求待定"
    }
    
    quote_result = {
        "surface_type": "UNKNOWN",
        "total_price": 0,
        "flag": "MANUAL_REVIEW_REQUIRED"
    }
    
    task = risk_control.handle_unknown_surface(order_data, quote_result)
    print("\n=== 创建审核任务 ===")
    print(json.dumps(task.to_dict(), indent=2, ensure_ascii=False))
    
    # 测试获取待审核任务
    pending_tasks = risk_control.get_pending_tasks()
    print(f"\n=== 待审核任务数：{len(pending_tasks)} ===")
    
    # 测试审核统计
    stats = risk_control.get_review_statistics()
    print("\n=== 审核统计 ===")
    print(json.dumps(stats, indent=2, ensure_ascii=False))
