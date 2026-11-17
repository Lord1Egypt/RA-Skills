"""
多智能体应急响应系统 - 核心框架

提供智能体基类、通信协议、协调器等核心组件。
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from pathlib import Path
import json
import uuid
import asyncio
import logging


class AgentState(Enum):
    """智能体状态枚举"""
    IDLE = "idle"
    INITIALIZING = "initializing"
    WORKING = "working"
    WAITING = "waiting"
    BLOCKED = "blocked"
    ERROR = "error"
    COMPLETED = "completed"
    TERMINATED = "terminated"


class MessageType(Enum):
    """消息类型枚举"""
    REQUEST = "request"
    RESPONSE = "response"
    NOTIFICATION = "notification"
    BROADCAST = "broadcast"
    ERROR = "error"


class Priority(Enum):
    """优先级枚举"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class AgentIdentity:
    """智能体身份信息"""
    agent_id: str
    agent_type: str
    role: str
    version: str = "1.0.0"
    capabilities: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "agent_type": self.agent_type,
            "role": self.role,
            "version": self.version,
            "capabilities": self.capabilities
        }


@dataclass
class Message:
    """消息数据结构"""
    message_id: str
    timestamp: str
    sender: AgentIdentity
    receiver: AgentIdentity
    message_type: MessageType
    priority: Priority
    content: Dict[str, Any]
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "message_id": self.message_id,
            "timestamp": self.timestamp,
            "sender": self.sender.to_dict(),
            "receiver": self.receiver.to_dict(),
            "message_type": self.message_type.value,
            "priority": self.priority.value,
            "content": self.content,
            "metadata": self.metadata
        }
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Message':
        return Message(
            message_id=data["message_id"],
            timestamp=data["timestamp"],
            sender=AgentIdentity(**data["sender"]),
            receiver=AgentIdentity(**data["receiver"]),
            message_type=MessageType(data["message_type"]),
            priority=Priority(data["priority"]),
            content=data["content"],
            metadata=data.get("metadata", {})
        )


@dataclass
class Task:
    """任务数据结构"""
    task_id: str
    task_type: str
    priority: Priority
    assigned_agent: Optional[str] = None
    status: str = "pending"
    inputs: Dict[str, Any] = field(default_factory=dict)
    outputs: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "task_type": self.task_type,
            "priority": self.priority.value,
            "assigned_agent": self.assigned_agent,
            "status": self.status,
            "inputs": self.inputs,
            "outputs": self.outputs,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }


class BaseAgent(ABC):
    """智能体基类"""
    
    def __init__(
        self,
        agent_id: str,
        agent_type: str,
        role: str,
        config_path: Optional[str] = None
    ):
        self.identity = AgentIdentity(
            agent_id=agent_id,
            agent_type=agent_type,
            role=role
        )
        self.state = AgentState.IDLE
        self.current_task: Optional[Task] = None
        self.message_queue: asyncio.Queue = asyncio.Queue()
        self.knowledge_base: Dict[str, Any] = {}
        self.logger = logging.getLogger(f"{agent_type}.{agent_id}")
        
        if config_path:
            self.load_config(config_path)
    
    def load_config(self, config_path: str):
        """加载配置文件"""
        config_file = Path(config_path)
        if config_file.exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                self.configure(config)
    
    @abstractmethod
    def configure(self, config: Dict[str, Any]):
        """配置智能体"""
        pass
    
    @abstractmethod
    async def process_message(self, message: Message) -> Optional[Message]:
        """处理消息"""
        pass
    
    @abstractmethod
    async def execute_task(self, task: Task) -> Dict[str, Any]:
        """执行任务"""
        pass
    
    async def send_message(
        self,
        receiver: AgentIdentity,
        message_type: MessageType,
        content: Dict[str, Any],
        priority: Priority = Priority.MEDIUM
    ) -> str:
        """发送消息"""
        message = Message(
            message_id=str(uuid.uuid4()),
            timestamp=datetime.now().isoformat(),
            sender=self.identity,
            receiver=receiver,
            message_type=message_type,
            priority=priority,
            content=content
        )
        
        await self.message_queue.put(message)
        self.logger.info(f"Message sent: {message.message_id}")
        return message.message_id
    
    async def receive_message(self) -> Message:
        """接收消息"""
        message = await self.message_queue.get()
        self.logger.info(f"Message received: {message.message_id}")
        return message
    
    def update_state(self, new_state: AgentState):
        """更新状态"""
        old_state = self.state
        self.state = new_state
        self.logger.info(f"State changed: {old_state.value} -> {new_state.value}")
    
    def add_capability(self, capability: str):
        """添加能力"""
        if capability not in self.identity.capabilities:
            self.identity.capabilities.append(capability)
    
    def has_capability(self, capability: str) -> bool:
        """检查能力"""
        return capability in self.identity.capabilities


class CommunicationProtocol:
    """通信协议"""
    
    def __init__(self):
        self.channels: Dict[str, asyncio.Queue] = {}
        self.subscriptions: Dict[str, List[str]] = {}
    
    async def create_channel(self, channel_name: str):
        """创建通道"""
        if channel_name not in self.channels:
            self.channels[channel_name] = asyncio.Queue()
    
    async def subscribe(self, channel_name: str, agent_id: str):
        """订阅通道"""
        if channel_name not in self.subscriptions:
            self.subscriptions[channel_name] = []
        if agent_id not in self.subscriptions[channel_name]:
            self.subscriptions[channel_name].append(agent_id)
    
    async def publish(self, channel_name: str, message: Message):
        """发布消息到通道"""
        if channel_name in self.channels:
            await self.channels[channel_name].put(message)
    
    async def receive(self, channel_name: str) -> Message:
        """从通道接收消息"""
        if channel_name in self.channels:
            return await self.channels[channel_name].get()
        raise ValueError(f"Channel {channel_name} does not exist")


class TaskRouter:
    """任务路由器"""
    
    def __init__(self):
        self.task_queues: Dict[Priority, asyncio.Queue] = {
            Priority.CRITICAL: asyncio.Queue(),
            Priority.HIGH: asyncio.Queue(),
            Priority.MEDIUM: asyncio.Queue(),
            Priority.LOW: asyncio.Queue()
        }
        self.agent_pool: Dict[str, BaseAgent] = {}
        self.task_history: List[Task] = []
    
    def register_agent(self, agent: BaseAgent):
        """注册智能体"""
        self.agent_pool[agent.identity.agent_id] = agent
    
    def unregister_agent(self, agent_id: str):
        """注销智能体"""
        if agent_id in self.agent_pool:
            del self.agent_pool[agent_id]
    
    async def submit_task(self, task: Task):
        """提交任务"""
        await self.task_queues[task.priority].put(task)
        self.task_history.append(task)
    
    async def get_next_task(self, priority: Priority) -> Task:
        """获取下一个任务"""
        return await self.task_queues[priority].get()
    
    def find_capable_agent(self, task: Task) -> Optional[BaseAgent]:
        """查找有能力的智能体"""
        for agent in self.agent_pool.values():
            if agent.state == AgentState.IDLE:
                if task.task_type in agent.identity.capabilities:
                    return agent
        return None
    
    async def route_task(self, task: Task) -> bool:
        """路由任务"""
        agent = self.find_capable_agent(task)
        if agent:
            task.assigned_agent = agent.identity.agent_id
            task.status = "assigned"
            await agent.send_message(
                receiver=agent.identity,
                message_type=MessageType.REQUEST,
                content={"task": task.to_dict()},
                priority=task.priority
            )
            return True
        return False


class Orchestrator:
    """总协调器"""
    
    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {}
        self.communication = CommunicationProtocol()
        self.task_router = TaskRouter()
        self.sessions: Dict[str, Dict[str, Any]] = {}
        self.logger = logging.getLogger("Orchestrator")
    
    async def initialize(self):
        """初始化协调器"""
        await self.communication.create_channel("control")
        await self.communication.create_channel("task")
        await self.communication.create_channel("event")
        self.logger.info("Orchestrator initialized")
    
    async def create_session(self, incident_name: str) -> str:
        """创建会话"""
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = {
            "session_id": session_id,
            "incident_name": incident_name,
            "start_time": datetime.now().isoformat(),
            "phase": "detect",
            "agents": [],
            "tasks": []
        }
        self.logger.info(f"Session created: {session_id}")
        return session_id
    
    async def spawn_agent(self, agent_type: str, config_path: str) -> str:
        """创建智能体"""
        agent_id = f"{agent_type}-{uuid.uuid4().hex[:8]}"
        
        agent_classes = {
            "ic_agent": ICAgent,
            "analyst_agent": AnalystAgent,
            "scribe_agent": ScribeAgent,
            "advisor_agent": AdvisorAgent,
        }
        
        agent_class = agent_classes.get(agent_type)
        if not agent_class:
            raise ValueError(f"Unknown agent type: {agent_type}")
        
        agent = agent_class(
            agent_id=agent_id,
            agent_type=agent_type,
            role=agent_type.replace("_agent", ""),
            config_path=config_path
        )
        
        self.agents[agent_id] = agent
        self.task_router.register_agent(agent)
        
        self.logger.info(f"Agent spawned: {agent_id}")
        return agent_id
    
    async def terminate_agent(self, agent_id: str):
        """终止智能体"""
        if agent_id in self.agents:
            agent = self.agents[agent_id]
            agent.update_state(AgentState.TERMINATED)
            self.task_router.unregister_agent(agent_id)
            del self.agents[agent_id]
            self.logger.info(f"Agent terminated: {agent_id}")
    
    async def broadcast_event(self, event_type: str, data: Dict[str, Any]):
        """广播事件"""
        message = Message(
            message_id=str(uuid.uuid4()),
            timestamp=datetime.now().isoformat(),
            sender=AgentIdentity(
                agent_id="orchestrator",
                agent_type="orchestrator",
                role="coordinator"
            ),
            receiver=AgentIdentity(
                agent_id="all",
                agent_type="all",
                role="all"
            ),
            message_type=MessageType.BROADCAST,
            priority=Priority.HIGH,
            content={
                "event_type": event_type,
                "data": data
            }
        )
        
        await self.communication.publish("event", message)
        self.logger.info(f"Event broadcasted: {event_type}")
    
    async def monitor_agents(self):
        """监控智能体状态"""
        while True:
            for agent_id, agent in self.agents.items():
                self.logger.debug(
                    f"Agent {agent_id}: state={agent.state.value}, "
                    f"capabilities={agent.identity.capabilities}"
                )
            await asyncio.sleep(30)
    
    async def handle_emergencies(self):
        """处理紧急情况"""
        while True:
            # 检查智能体超时
            for agent_id, agent in self.agents.items():
                if agent.state == AgentState.ERROR:
                    self.logger.warning(f"Agent {agent_id} in error state")
                    # 尝试重启
                    await self.restart_agent(agent_id)
            
            await asyncio.sleep(10)
    
    async def restart_agent(self, agent_id: str):
        """重启智能体"""
        if agent_id in self.agents:
            agent = self.agents[agent_id]
            self.logger.info(f"Restarting agent: {agent_id}")
            agent.update_state(AgentState.IDLE)
            agent.current_task = None


class ICAgent(BaseAgent):
    """指挥官智能体"""
    
    def configure(self, config: Dict[str, Any]):
        """配置"""
        self.decision_authority = config.get("decision_authority", {})
        self.hitl_policy = config.get("hitl_policy", {})
        self.add_capability("risk_assessment")
        self.add_capability("decision_making")
        self.add_capability("coordination")
    
    async def process_message(self, message: Message) -> Optional[Message]:
        """处理消息"""
        if message.message_type == MessageType.REQUEST:
            action = message.content.get("action")
            
            if action == "approve_containment":
                return await self.handle_approval_request(message, "containment")
            elif action == "approve_eradication":
                return await self.handle_approval_request(message, "eradication")
            elif action == "escalate":
                return await self.handle_escalation(message)
        
        return None
    
    async def handle_approval_request(
        self,
        message: Message,
        approval_type: str
    ) -> Message:
        """处理审批请求"""
        # 检查是否需要HITL
        if self.needs_hitl(approval_type):
            # 请求人工确认
            hitl_response = await self.request_hitl(message, approval_type)
            approval_status = hitl_response
        else:
            # 自动审批
            approval_status = "approved"
        
        return Message(
            message_id=str(uuid.uuid4()),
            timestamp=datetime.now().isoformat(),
            sender=self.identity,
            receiver=message.sender,
            message_type=MessageType.RESPONSE,
            priority=Priority.HIGH,
            content={
                "approval_status": approval_status,
                "approval_type": approval_type
            }
        )
    
    def needs_hitl(self, action_type: str) -> bool:
        """检查是否需要HITL"""
        triggers = self.hitl_policy.get("triggers", [])
        return any(trigger["action_type"] == action_type for trigger in triggers)
    
    async def request_hitl(self, message: Message, action_type: str) -> str:
        """请求人工确认"""
        self.logger.warning(f"HITL required for {action_type}")
        # 这里应该调用人类决策接口
        # 简化实现：返回超时（拒绝）
        return "timeout"
    
    async def handle_escalation(self, message: Message) -> Message:
        """处理升级"""
        self.logger.critical(f"Escalation received: {message.content}")
        # 通知人类指挥官
        return Message(
            message_id=str(uuid.uuid4()),
            timestamp=datetime.now().isoformat(),
            sender=self.identity,
            receiver=message.sender,
            message_type=MessageType.RESPONSE,
            priority=Priority.CRITICAL,
            content={"status": "escalated_to_human"}
        )
    
    async def execute_task(self, task: Task) -> Dict[str, Any]:
        """执行任务"""
        self.update_state(AgentState.WORKING)
        self.current_task = task
        
        try:
            task_type = task.task_type
            
            if task_type == "create_incident":
                result = await self.create_incident(task.inputs)
            elif task_type == "classify_incident":
                result = await self.classify_incident(task.inputs)
            else:
                result = {"error": f"Unknown task type: {task_type}"}
            
            self.update_state(AgentState.COMPLETED)
            return result
            
        except Exception as e:
            self.logger.error(f"Task execution failed: {e}")
            self.update_state(AgentState.ERROR)
            return {"error": str(e)}
    
    async def create_incident(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """创建事件"""
        incident_id = str(uuid.uuid4())
        self.logger.info(f"Incident created: {incident_id}")
        return {"incident_id": incident_id}
    
    async def classify_incident(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """分类事件"""
        # 简化实现：基于规则分类
        alert_data = inputs.get("alert_data", {})
        incident_type = "unknown"
        severity = "medium"
        
        if "xmrig" in str(alert_data).lower():
            incident_type = "挖矿"
            severity = "high"
        elif "ransomware" in str(alert_data).lower():
            incident_type = "勒索"
            severity = "critical"
        
        return {
            "incident_type": incident_type,
            "severity": severity
        }


class AnalystAgent(BaseAgent):
    """分析师智能体"""
    
    def configure(self, config: Dict[str, Any]):
        """配置"""
        self.specializations = config.get("specializations", {})
        self.add_capability("log_analysis")
        self.add_capability("traffic_analysis")
        self.add_capability("malware_analysis")
        self.add_capability("ioc_extraction")
    
    async def process_message(self, message: Message) -> Optional[Message]:
        """处理消息"""
        if message.message_type == MessageType.REQUEST:
            action = message.content.get("action")
            
            if action == "analyze_incident":
                return await self.analyze_incident(message)
            elif action == "extract_iocs":
                return await self.extract_iocs(message)
        
        return None
    
    async def analyze_incident(self, message: Message) -> Message:
        """分析事件"""
        self.update_state(AgentState.WORKING)
        
        incident_data = message.content.get("incident_data", {})
        evidence_list = message.content.get("evidence_list", [])
        
        # 模拟分析过程
        findings = {
            "iocs": await self.extract_iocs_from_evidence(evidence_list),
            "timeline": await self.build_timeline(evidence_list),
            "root_cause_hypothesis": "需要进一步分析"
        }
        
        self.update_state(AgentState.COMPLETED)
        
        return Message(
            message_id=str(uuid.uuid4()),
            timestamp=datetime.now().isoformat(),
            sender=self.identity,
            receiver=message.sender,
            message_type=MessageType.RESPONSE,
            priority=Priority.HIGH,
            content=findings
        )
    
    async def extract_iocs_from_evidence(self, evidence_list: List[str]) -> List[Dict]:
        """从证据提取IOC"""
        # 简化实现：返回模拟IOC
        return [
            {"type": "ip", "value": "1.2.3.4", "confidence": "high"},
            {"type": "domain", "value": "evil.com", "confidence": "medium"}
        ]
    
    async def build_timeline(self, evidence_list: List[str]) -> List[Dict]:
        """构建时间线"""
        return [
            {
                "timestamp": "2026-04-29T10:00:00Z",
                "event": "告警触发",
                "source": "EDR"
            },
            {
                "timestamp": "2026-04-29T10:05:00Z",
                "event": "异常进程启动",
                "source": "主机日志"
            }
        ]
    
    async def execute_task(self, task: Task) -> Dict[str, Any]:
        """执行任务"""
        self.update_state(AgentState.WORKING)
        self.current_task = task
        
        try:
            # 执行分析任务
            result = await self.perform_analysis(task.inputs)
            
            self.update_state(AgentState.COMPLETED)
            return result
            
        except Exception as e:
            self.logger.error(f"Analysis failed: {e}")
            self.update_state(AgentState.ERROR)
            return {"error": str(e)}
    
    async def perform_analysis(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """执行分析"""
        # 模拟分析过程
        await asyncio.sleep(2)  # 模拟耗时
        return {"analysis_result": "completed"}


class ScribeAgent(BaseAgent):
    """记录员智能体"""
    
    def configure(self, config: Dict[str, Any]):
        """配置"""
        self.wal_path = Path(config.get("wal_path", "memory/working/current_session.json"))
        self.evidence_path = Path(config.get("evidence_path", "evidence/"))
        self.add_capability("recording")
        self.add_capability("report_generation")
    
    async def process_message(self, message: Message) -> Optional[Message]:
        """处理消息"""
        if message.message_type == MessageType.REQUEST:
            action = message.content.get("action")
            
            if action == "record_event":
                return await self.record_event(message)
            elif action == "generate_report":
                return await self.generate_report(message)
        
        return None
    
    async def record_event(self, message: Message) -> Message:
        """记录事件"""
        event_data = message.content.get("event_data", {})
        
        # 写入WAL
        await self.write_to_wal(event_data)
        
        return Message(
            message_id=str(uuid.uuid4()),
            timestamp=datetime.now().isoformat(),
            sender=self.identity,
            receiver=message.sender,
            message_type=MessageType.RESPONSE,
            priority=Priority.MEDIUM,
            content={"status": "recorded", "event_id": str(uuid.uuid4())}
        )
    
    async def write_to_wal(self, data: Dict[str, Any]):
        """写入WAL"""
        self.wal_path.parent.mkdir(parents=True, exist_ok=True)
        
        if self.wal_path.exists():
            with open(self.wal_path, 'r', encoding='utf-8') as f:
                wal_data = json.load(f)
        else:
            wal_data = {"events": []}
        
        wal_data["events"].append({
            "timestamp": datetime.now().isoformat(),
            "data": data
        })
        
        with open(self.wal_path, 'w', encoding='utf-8') as f:
            json.dump(wal_data, f, indent=2, ensure_ascii=False)
    
    async def generate_report(self, message: Message) -> Message:
        """生成报告"""
        report_type = message.content.get("report_type", "markdown")
        
        # 生成报告（简化实现）
        report_content = "# 应急响应报告\n\n## 概述\n待补充..."
        
        return Message(
            message_id=str(uuid.uuid4()),
            timestamp=datetime.now().isoformat(),
            sender=self.identity,
            receiver=message.sender,
            message_type=MessageType.RESPONSE,
            priority=Priority.MEDIUM,
            content={"report": report_content, "format": report_type}
        )
    
    async def execute_task(self, task: Task) -> Dict[str, Any]:
        """执行任务"""
        self.update_state(AgentState.WORKING)
        self.current_task = task
        
        try:
            task_type = task.task_type
            
            if task_type == "initialize_wal":
                result = await self.initialize_wal(task.inputs)
            elif task_type == "record_findings":
                result = await self.record_findings(task.inputs)
            else:
                result = {"error": f"Unknown task type: {task_type}"}
            
            self.update_state(AgentState.COMPLETED)
            return result
            
        except Exception as e:
            self.logger.error(f"Recording failed: {e}")
            self.update_state(AgentState.ERROR)
            return {"error": str(e)}
    
    async def initialize_wal(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """初始化WAL"""
        session_data = {
            "session_id": inputs.get("session_id", str(uuid.uuid4())),
            "incident_name": inputs.get("incident_name", "未知事件"),
            "start_time": datetime.now().isoformat(),
            "phase": "detect"
        }
        
        await self.write_to_wal(session_data)
        return {"status": "initialized", "session_id": session_data["session_id"]}
    
    async def record_findings(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """记录发现"""
        await self.write_to_wal(inputs)
        return {"status": "recorded"}


class AdvisorAgent(BaseAgent):
    """顾问智能体"""
    
    def configure(self, config: Dict[str, Any]):
        """配置"""
        self.loop_detection_thresholds = config.get("loop_detection", {}).get("thresholds", {})
        self.add_capability("loop_detection")
        self.add_capability("recommendation")
        self.add_capability("knowledge_retrieval")
    
    async def process_message(self, message: Message) -> Optional[Message]:
        """处理消息"""
        if message.message_type == MessageType.REQUEST:
            action = message.content.get("action")
            
            if action == "detect_loop":
                return await self.detect_loop(message)
            elif action == "get_recommendation":
                return await self.get_recommendation(message)
        
        return None
    
    async def detect_loop(self, message: Message) -> Message:
        """检测循环"""
        event_history = message.content.get("event_history", [])
        
        # 检测重复动作
        loop_detected = await self.check_for_loops(event_history)
        
        return Message(
            message_id=str(uuid.uuid4()),
            timestamp=datetime.now().isoformat(),
            sender=self.identity,
            receiver=message.sender,
            message_type=MessageType.RESPONSE,
            priority=Priority.HIGH,
            content={"loop_detected": loop_detected}
        )
    
    async def check_for_loops(self, event_history: List[Dict]) -> Dict:
        """检查循环"""
        # 简化实现：检查最近5个事件是否有重复
        if len(event_history) < 3:
            return {"detected": False}
        
        recent_events = event_history[-5:]
        action_counts = {}
        
        for event in recent_events:
            action = event.get("action")
            if action:
                action_counts[action] = action_counts.get(action, 0) + 1
        
        for action, count in action_counts.items():
            if count >= self.loop_detection_thresholds.get("warning", 2):
                return {
                    "detected": True,
                    "action": action,
                    "count": count,
                    "recommendation": f"动作 '{action}' 已重复 {count} 次，建议尝试替代方案"
                }
        
        return {"detected": False}
    
    async def get_recommendation(self, message: Message) -> Message:
        """获取建议"""
        problem = message.content.get("problem", "")
        context = message.content.get("context", {})
        
        # 简化实现：返回模板建议
        recommendation = self.generate_advisor_template(problem, context)
        
        return Message(
            message_id=str(uuid.uuid4()),
            timestamp=datetime.now().isoformat(),
            sender=self.identity,
            receiver=message.sender,
            message_type=MessageType.RESPONSE,
            priority=Priority.HIGH,
            content=recommendation
        )
    
    def generate_advisor_template(self, problem: str, context: Dict) -> Dict:
        """生成顾问模板"""
        return {
            "problem_statement": problem,
            "root_cause_analysis": "需要进一步信息来确定根因",
            "information_gaps": [
                "缺少关键日志",
                "缺少完整攻击链"
            ],
            "alternative_approaches": [
                "方案A：通过内存取证补充信息",
                "方案B：通过流量分析重建攻击链"
            ],
            "recommended_actions": [
                "步骤1：收集缺失的日志（VBR：日志文件路径）",
                "步骤2：执行内存取证（VBR：内存镜像文件）",
                "步骤3：分析网络流量（VBR：PCAP文件）"
            ],
            "vbr_checkpoints": [
                "验证日志完整性",
                "验证内存镜像可用性",
                "验证流量包时间范围"
            ]
        }
    
    async def execute_task(self, task: Task) -> Dict[str, Any]:
        """执行任务"""
        self.update_state(AgentState.WORKING)
        self.current_task = task
        
        try:
            task_type = task.task_type
            
            if task_type == "evaluate_containment":
                result = await self.evaluate_containment(task.inputs)
            else:
                result = {"error": f"Unknown task type: {task_type}"}
            
            self.update_state(AgentState.COMPLETED)
            return result
            
        except Exception as e:
            self.logger.error(f"Advisory failed: {e}")
            self.update_state(AgentState.ERROR)
            return {"error": str(e)}
    
    async def evaluate_containment(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """评估遏制措施"""
        containment_options = inputs.get("containment_options", [])
        business_context = inputs.get("business_context", {})
        
        # 简化评估：推荐低影响方案
        recommended = None
        for option in containment_options:
            if option.get("impact") == "low":
                recommended = option
                break
        
        if not recommended and containment_options:
            recommended = containment_options[0]
        
        return {
            "recommended_containment": recommended,
            "risk_assessment": {
                "business_impact": "low",
                "reversibility": "high"
            }
        }


# 导入yaml（用于配置加载）
import yaml

if __name__ == "__main__":
    # 测试代码
    async def test_orchestrator():
        orchestrator = Orchestrator()
        await orchestrator.initialize()
        
        # 创建会话
        session_id = await orchestrator.create_session("测试事件")
        print(f"Session created: {session_id}")
        
        # 创建智能体
        ic_agent_id = await orchestrator.spawn_agent("ic_agent", "multi_agent/agents/ic_agent.yaml")
        print(f"IC Agent created: {ic_agent_id}")
        
        analyst_agent_id = await orchestrator.spawn_agent("analyst_agent", "multi_agent/agents/analyst_agent.yaml")
        print(f"Analyst Agent created: {analyst_agent_id}")
        
        scribe_agent_id = await orchestrator.spawn_agent("scribe_agent", "multi_agent/agents/scribe_agent.yaml")
        print(f"Scribe Agent created: {scribe_agent_id}")
        
        # 清理
        await orchestrator.terminate_agent(ic_agent_id)
        await orchestrator.terminate_agent(analyst_agent_id)
        await orchestrator.terminate_agent(scribe_agent_id)
    
    asyncio.run(test_orchestrator())
