"""
跨工作区任务分发通信协议
Cross-Workspace Task Distribution Protocol

消息类型定义：
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List
import time
import uuid


class TaskStatus(Enum):
    """任务状态"""
    PENDING = "pending"        # 待执行
    ASSIGNED = "assigned"      # 已分配
    RUNNING = "running"       # 执行中
    COMPLETED = "completed"  # 完成
    FAILED = "failed"       # 失败
    CANCELLED = "cancelled"  # 取消


class MessageType(Enum):
    """消息类型"""
    TASK_REQUEST = "task_request"       # 任务请求
    TASK_RESPONSE = "task_response"       # 任务响应
    TASK_HEARTBEAT = "task_heartbeat"   # 心跳保活
    TASK_CANCEL = "task_cancel"        # 取消任务
    TASK_RESULT = "task_result"         # 任务结果
    REGISTRATION = "registration"     # 注册
    HEARTBEAT = "heartbeat"         # 连接心跳


@dataclass
class TaskMessage:
    """任务消息结构"""
    # 消息头
    msg_id: str = field(default_factory=lambda: uuid.uuid4().hex[:8])
    msg_type: str = MessageType.TASK_REQUEST.value
    protocol_version: str = "1.0"
    timestamp: float = field(default_factory=time.time)
    
    # 发送者信息
    sender_ws: str = ""           # 发送工作区ID
    sender_name: str = ""           # 发送者名称
    
    # 接收者信息
    recipient_ws: str = ""          # 接收工作区ID
    recipient_name: str = ""       # 接收者名称
    
    # 任务信息
    task_id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    task_type: str = ""              # 任务类型
    task_action: str = ""           # 任务动作
    task_params: Dict[str, Any] = field(default_factory=dict)
    priority: int = 5            # 优先级 1-10
    
    # 执行信息
    status: str = TaskStatus.PENDING.value
    assigned_at: float = 0
    started_at: float = 0
    completed_at: float = 0
    
    # 结果
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    
    # 回调
    callback_url: str = ""           # 结果回调地址
    correlation_id: str = ""       # 关联ID（用于追踪）


@dataclass
class WorkerInfo:
    """工作区 Worker 信息"""
    ws_id: str
    ws_name: str
    host: str
    port: int
    status: str = "offline"
    capabilities: List[str] = field(default_factory=list)  # 支持的任务类型
    # 设备能力信息（用于层级调度）
    cpu_cores: int = 0
    memory_gb: int = 0
    storage_gb: int = 0
    registered_at: float = 0
    last_heartbeat: float = 0

    def get_tier(self) -> str:
        """计算设备层级 T1/T2/T3"""
        # 综合评分 = CPU*100 + 内存*50 + 存储*10
        score = self.cpu_cores * 100 + self.memory_gb * 50 + self.storage_gb * 10
        if score >= 1500:
            return "T1"
        elif score >= 500:
            return "T2"
        else:
            return "T3"

    def get_total_score(self) -> int:
        """获取设备综合评分"""
        return self.cpu_cores * 100 + self.memory_gb * 50 + self.storage_gb * 10


# ==================== 通信协议示例 ====================
#
# 1. 任务分发消息:
# {
#     "msg_type": "task_request",
#     "sender_ws": "ws_main",
#     "sender_name": "主工作区",
#     "recipient_ws": "ws_finance",
#     "task_id": "task_abc123",
#     "task_type": "data_query",
#     "task_action": "查股价",
#     "task_params": {"stock": "600519"},
#     "priority": 5,
#     "callback_url": "ws://localhost:8765/callback"
# }
#
# 2. 任务结果消息:
# {
#     "msg_type": "task_result",
#     "sender_ws": "ws_finance",
#     "task_id": "task_abc123",
#     "status": "completed",
#     "result": {"price": 1850.5},
#     "completed_at": 1234567890.123
# }
#
# 3. 注册消息:
# {
#     "msg_type": "registration",
#     "sender_ws": "ws_finance",
#     "sender_name": "金融数据分析区",
#     "capabilities": ["data_query", "stock_analysis", "fund_query"],
#     "host": "192.168.1.100",
#     "port": 8765
# }
#
# 4. 心跳消息:
# {
#     "msg_type": "heartbeat",
#     "sender_ws": "ws_finance",
#     "status": "online"
# }
#

# ==================== 任务分发流程 ====================
#
# [步骤1: 注册]
#   工作区B ──▶ 注册消息 ──▶ 主工作区
#   工作区C ──▶ 注册消息 ──▶ 主工作区
#
# [步骤2: 分发任务]
#   你 ──▶ 发布任务 ──▶ 我判断交给谁 ──▶ 分发任务到目标工作区
#
# [步骤3: 执行]
#   目标工作区 ──▶ 接收任务 ──▶ 执行 ──▶ 返回结果
#
# [步骤4: 回调]
#   目标工作区 ──▶ 回调 ──▶ 主工作区聚合
#
# [步骤5: 通知]
#   主工作区 ──▶ 聚合结果 ──▶ 通知你
#

# ==================== 错误处理 ====================
#
# - 超时: 任务默认 5 分钟超时，可配置
# - 重试: 失败任务最多重试 2 次
# - 降级: 目标工作区不可用时自动选择下一个
# - 日志: 所有消息记录可追溯