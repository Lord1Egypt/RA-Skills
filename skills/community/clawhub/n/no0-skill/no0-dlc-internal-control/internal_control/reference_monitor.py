"""
Reference Monitor - 强制访问控制决策点

核心原则：
1. 不可绕过性 - 所有 Agent 文件访问必须经过 Monitor
2. 防篡改性 - Monitor 自身代码和配置受保护
3. 可验证性 - 所有决策可审计、可验证
4. 最小权限 - 基于分级的最小权限访问
5. Fail-Closed - 故障时默认拒绝访问
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Union
import hashlib
import json
import secrets
import time
from pathlib import Path
from contextvars import ContextVar

# 从 rules.models 统一导入 DataLevel 和相关函数
from .rules.models import DataLevel, get_level_strictness

# ========== 枚举定义 ==========

class AccessOperation(Enum):
    """访问操作类型"""
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    EXECUTE = "execute"


class AccessDecision(Enum):
    """访问决策结果"""
    ALLOW = "allow"
    DENY = "deny"
    PENDING = "pending"  # 等待授权
    ESCALATE = "escalate"  # 上报 CEO


class AgentPermissionLevel(Enum):
    """Agent 权限级别"""
    LEVEL_0_UNTRUSTED = 0   # 不受信任，无文件访问权限
    LEVEL_1_BASIC = 1       # 基础：读取 L1, L2
    LEVEL_2_STANDARD = 2    # 标准：读取 L1-L3（L3需授权）
    LEVEL_3_TRUSTED = 3     # 受信任：读取 L1-L4（L4需授权）
    LEVEL_4_SYSTEM = 4      # 系统：读取 L1-L5（特殊情况），写入 L1-L2
    LEVEL_5_ADMIN = 5       # 管理：完整访问（需审计）


class AuditEventType(Enum):
    """审计事件类型"""
    ACCESS_REQUESTED = "access_requested"
    ACCESS_GRANTED = "access_granted"
    ACCESS_DENIED = "access_denied"
    AUTHORIZATION_REQUESTED = "authorization_requested"
    AUTHORIZATION_APPROVED = "authorization_approved"
    AUTHORIZATION_DENIED = "authorization_denied"
    SYSTEM_DEGRADED = "system_degraded"
    SYSTEM_RECOVERED = "system_recovered"
    INTEGRITY_VIOLATION = "integrity_violation"
    AUTHENTICATION_FAILURE = "authentication_failure"
    POLICY_VIOLATION = "policy_violation"


# ========== 数据模型 ==========

@dataclass
class Agent:
    """Agent 定义"""
    agent_id: str
    name: str
    permission_level: AgentPermissionLevel
    public_key: Optional[str]  # 用于数字签名验证
    registered_at: datetime
    last_authenticated: Optional[datetime] = None
    
    def can_access(self, level: DataLevel, operation: AccessOperation) -> bool:
        """检查是否有权限访问指定级别的文件"""
        required_level = self._get_required_permission_level(level, operation)
        return self.permission_level.value >= required_level.value
    
    def _get_required_permission_level(
        self,
        level: DataLevel,
        operation: AccessOperation
    ) -> AgentPermissionLevel:
        """获取访问指定级别所需的最小权限"""
        level_requirements = {
            DataLevel.L1_PUBLIC: {
                AccessOperation.READ: AgentPermissionLevel.LEVEL_1_BASIC,
                AccessOperation.WRITE: AgentPermissionLevel.LEVEL_1_BASIC,
            },
            DataLevel.L2_INTERNAL: {
                AccessOperation.READ: AgentPermissionLevel.LEVEL_1_BASIC,
                AccessOperation.WRITE: AgentPermissionLevel.LEVEL_4_SYSTEM,
            },
            DataLevel.L3_RESTRICTED: {
                AccessOperation.READ: AgentPermissionLevel.LEVEL_2_STANDARD,
                AccessOperation.WRITE: AgentPermissionLevel.LEVEL_5_ADMIN,
            },
            DataLevel.L4_CONFIDENTIAL: {
                AccessOperation.READ: AgentPermissionLevel.LEVEL_3_TRUSTED,
                AccessOperation.WRITE: AgentPermissionLevel.LEVEL_5_ADMIN,
            },
            DataLevel.L5_SECRET: {
                AccessOperation.READ: AgentPermissionLevel.LEVEL_4_SYSTEM,
                AccessOperation.WRITE: AgentPermissionLevel.LEVEL_5_ADMIN,
            },
            DataLevel.L6_CRITICAL: {
                AccessOperation.READ: AgentPermissionLevel.LEVEL_5_ADMIN,
                AccessOperation.WRITE: AgentPermissionLevel.LEVEL_5_ADMIN,
            },
        }
        
        return level_requirements.get(level, {}).get(
            operation,
            AgentPermissionLevel.LEVEL_5_ADMIN
        )


@dataclass
class Classification:
    """文件分级结果"""
    path: str
    level: DataLevel
    source: str  # 分级来源
    confidence: float = 1.0
    reason: str = ""


@dataclass
class AccessRequest:
    """访问请求"""
    agent_id: str
    file_path: str
    operation: AccessOperation
    context: Dict[str, Any]
    timestamp: datetime


@dataclass
class AccessResult:
    """访问决策结果"""
    decision: AccessDecision
    token: Optional[str]  # 授权令牌
    expires_at: Optional[datetime]
    level: DataLevel
    policy: str
    reason: str
    audit_record_id: str


@dataclass
class AuditRecord:
    """审计记录"""
    record_id: str
    correlation_id: str
    event_type: AuditEventType
    timestamp: datetime
    recorded_at: datetime
    actor_type: str
    actor_id: str
    resource_path: str
    resource_level: DataLevel
    operation: AccessOperation
    decision: AccessDecision
    decision_reason: str
    context: Dict[str, Any]
    record_hash: str
    prev_hash: str


@dataclass
class PolicyDecision:
    """策略决策"""
    decision: AccessDecision
    reason: str
    requires_auth: bool = False
    auth_method: Optional[str] = None


@dataclass
class AgentContext:
    """Agent 运行时上下文"""
    agent_id: str
    agent_name: str
    permission_level: AgentPermissionLevel
    session_key: str
    current_task: Optional[str] = None
    start_time: Optional[datetime] = None
    access_token: Optional[str] = None


# ========== 核心异常 ==========

class AccessDeniedError(Exception):
    """访问拒绝异常"""
    def __init__(
        self,
        message: str,
        decision: AccessDecision = AccessDecision.DENY,
        level: Optional[DataLevel] = None,
        policy: str = "deny_by_default",
        audit_record_id: str = ""
    ):
        super().__init__(message)
        self.decision = decision
        self.level = level
        self.policy = policy
        self.audit_record_id = audit_record_id


class ReferenceMonitorError(Exception):
    """Reference Monitor 内部错误"""
    pass


# ========== Agent 认证 ==========

class AgentAuthenticator:
    """Agent 认证器"""
    
    def __init__(self, registry_path: Optional[Path] = None):
        self.registry_path = registry_path or Path.home() / ".openclaw" / "agents" / "registry.yaml"
        self._agents: Dict[str, Agent] = {}
        self._load_registry()
    
    def _load_registry(self):
        """加载 Agent 注册表"""
        if not self.registry_path.exists():
            return
        
        try:
            import yaml
            with open(self.registry_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            
            if not data or 'agents' not in data:
                return
            
            for agent_id, agent_data in data['agents'].items():
                self._agents[agent_id] = Agent(
                    agent_id=agent_id,
                    name=agent_data.get('name', 'Unknown'),
                    permission_level=AgentPermissionLevel[agent_data.get('permission_level', 'LEVEL_1_BASIC')],
                    public_key=agent_data.get('public_key'),
                    registered_at=datetime.fromisoformat(agent_data.get('registered_at', datetime.now().isoformat())),
                    last_authenticated=None
                )
        except Exception as e:
            print(f"加载 Agent 注册表失败: {e}")
    
    async def authenticate(self, agent_id: str) -> Optional[Agent]:
        """认证 Agent"""
        agent = self._agents.get(agent_id)
        if agent:
            agent.last_authenticated = datetime.now()
        return agent
    
    def get_agent(self, agent_id: str) -> Optional[Agent]:
        """获取 Agent（不认证）"""
        return self._agents.get(agent_id)
    
    def register_agent(self, agent: Agent):
        """注册新 Agent"""
        self._agents[agent.agent_id] = agent
        self._save_registry()
    
    def _save_registry(self):
        """保存注册表"""
        try:
            import yaml
            self.registry_path.parent.mkdir(parents=True, exist_ok=True)
            
            data = {'agents': {}}
            for agent_id, agent in self._agents.items():
                data['agents'][agent_id] = {
                    'name': agent.name,
                    'permission_level': agent.permission_level.name,
                    'public_key': agent.public_key,
                    'registered_at': agent.registered_at.isoformat()
                }
            
            with open(self.registry_path, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, default_flow_style=False)
        except Exception as e:
            print(f"保存 Agent 注册表失败: {e}")


# ========== 策略引擎 ==========

class PolicyEngine:
    """访问策略引擎"""
    
    # 分级到访问策略的映射
    LEVEL_POLICIES = {
        DataLevel.L1_PUBLIC: {
            'agent_read': 'allow',
            'agent_write': 'allow_with_log',
            'audit_level': 'minimal'
        },
        DataLevel.L2_INTERNAL: {
            'agent_read': 'allow_with_log',
            'agent_write': 'deny',
            'audit_level': 'standard'
        },
        DataLevel.L3_RESTRICTED: {
            'agent_read': 'require_approval',
            'agent_write': 'deny',
            'audit_level': 'detailed'
        },
        DataLevel.L4_CONFIDENTIAL: {
            'agent_read': 'require_approval',
            'agent_write': 'deny',
            'audit_level': 'full'
        },
        DataLevel.L5_SECRET: {
            'agent_read': 'deny',
            'agent_write': 'deny',
            'audit_level': 'full'
        },
        DataLevel.L6_CRITICAL: {
            'agent_read': 'deny',
            'agent_write': 'deny',
            'audit_level': 'full'
        },
    }
    
    async def evaluate(
        self,
        agent: Agent,
        classification: Classification,
        operation: AccessOperation,
        context: Dict[str, Any]
    ) -> PolicyDecision:
        """评估访问策略"""
        
        # 获取分级对应的策略
        policy = self.LEVEL_POLICIES.get(classification.level)
        if not policy:
            return PolicyDecision(
                decision=AccessDecision.DENY,
                reason="Unknown data level"
            )
        
        # 确定操作类型对应的策略
        if operation == AccessOperation.READ:
            access_policy = policy['agent_read']
        elif operation == AccessOperation.WRITE:
            access_policy = policy['agent_write']
        else:
            access_policy = 'deny'
        
        # 评估策略
        if access_policy == 'allow':
            return PolicyDecision(
                decision=AccessDecision.ALLOW,
                reason="Direct access granted"
            )
        
        elif access_policy == 'allow_with_log':
            return PolicyDecision(
                decision=AccessDecision.ALLOW,
                reason="Access granted with audit logging"
            )
        
        elif access_policy == 'require_approval':
            # 检查 Agent 是否有权限发起授权请求
            if not agent.can_access(classification.level, operation):
                return PolicyDecision(
                    decision=AccessDecision.DENY,
                    reason="Agent lacks required permission level"
                )
            
            return PolicyDecision(
                decision=AccessDecision.PENDING,
                reason="Authorization required",
                requires_auth=True,
                auth_method='interactive'
            )
        
        elif access_policy == 'deny':
            return PolicyDecision(
                decision=AccessDecision.DENY,
                reason="Access denied by policy"
            )
        
        else:
            return PolicyDecision(
                decision=AccessDecision.DENY,
                reason="Unknown access policy"
            )


# ========== 审计日志 ==========

class AuditLogger:
    """审计日志记录器（链式哈希保护）"""
    
    def __init__(self, log_dir: Optional[Path] = None):
        self.log_dir = log_dir or Path.home() / ".openclaw" / "internal_control" / "audit"
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        self._secret_key: Optional[bytes] = None
        self._prev_hash: str = "0" * 64
        self._load_last_hash()
    
    def _load_last_hash(self):
        """加载最后一条记录的哈希"""
        hash_file = self.log_dir / ".last_hash"
        if hash_file.exists():
            self._prev_hash = hash_file.read_text().strip()
    
    def _save_last_hash(self, hash_value: str):
        """保存最后一条记录的哈希"""
        hash_file = self.log_dir / ".last_hash"
        hash_file.write_text(hash_value)
    
    def _compute_hash(self, record: AuditRecord) -> str:
        """计算记录哈希（包含前一条哈希，形成链）"""
        data = {
            "record_id": record.record_id,
            "timestamp": record.timestamp.isoformat(),
            "actor_id": record.actor_id,
            "resource_path": record.resource_path,
            "operation": record.operation.value,
            "decision": record.decision.value,
            "prev_hash": self._prev_hash
        }
        
        data_str = json.dumps(data, sort_keys=True)
        return hashlib.sha256(data_str.encode()).hexdigest()
    
    async def log_access_request(
        self,
        request: AccessRequest,
        classification: Classification,
        policy_decision: PolicyDecision
    ) -> str:
        """记录访问请求"""
        
        record_id = secrets.token_hex(16)
        correlation_id = request.context.get('correlation_id', record_id)
        
        # 确定事件类型
        if policy_decision.decision == AccessDecision.ALLOW:
            event_type = AuditEventType.ACCESS_GRANTED
        elif policy_decision.decision == AccessDecision.PENDING:
            event_type = AuditEventType.AUTHORIZATION_REQUESTED
        else:
            event_type = AuditEventType.ACCESS_DENIED
        
        record = AuditRecord(
            record_id=record_id,
            correlation_id=correlation_id,
            event_type=event_type,
            timestamp=request.timestamp,
            recorded_at=datetime.now(),
            actor_type="agent",
            actor_id=request.agent_id,
            resource_path=request.file_path,
            resource_level=classification.level,
            operation=request.operation,
            decision=policy_decision.decision,
            decision_reason=policy_decision.reason,
            context=request.context,
            record_hash="",  # 稍后计算
            prev_hash=self._prev_hash
        )
        
        # 计算哈希
        record.record_hash = self._compute_hash(record)
        
        # 写入日志
        await self._write_to_log(record)
        
        # 更新 prev_hash
        self._prev_hash = record.record_hash
        self._save_last_hash(self._prev_hash)
        
        return record_id
    
    async def _write_to_log(self, record: AuditRecord):
        """写入日志文件"""
        log_file = self.log_dir / f"audit_{datetime.now().strftime('%Y%m')}.csv"
        
        # 创建文件头（如果不存在）
        if not log_file.exists():
            header = "record_id,correlation_id,event_type,timestamp,recorded_at,actor_type,actor_id,resource_path,resource_level,operation,decision,decision_reason,record_hash,prev_hash\n"
            log_file.write_text(header)
        
        # 追加记录
        line = f"{record.record_id},{record.correlation_id},{record.event_type.value},{record.timestamp.isoformat()},{record.recorded_at.isoformat()},{record.actor_type},{record.actor_id},{record.resource_path},{record.resource_level.value},{record.operation.value},{record.decision.value},{record.decision_reason},{record.record_hash},{record.prev_hash}\n"
        
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(line)
    
    async def log_error(self, request: AccessRequest, error: Exception):
        """记录错误"""
        # 简化实现，实际应该写入专门的错误日志
        print(f"Audit Error: {request.agent_id} - {error}")


# ========== Reference Monitor 主类 ==========

class ReferenceMonitor:
    """
    强制访问控制决策点
    
    使用示例:
        monitor = ReferenceMonitor()
        result = await monitor.check_access(
            agent_id="shrimp-agent-001",
            file_path="~/.ssh/id_rsa",
            operation=AccessOperation.READ,
            context={"task": "备份 SSH 密钥"}
        )
    """
    
    def __init__(self):
        self.agent_auth = AgentAuthenticator()
        self.policy_engine = PolicyEngine()
        self.audit_logger = AuditLogger()
        self._classification_engine = None
        self._initialized = False
    
    async def initialize(self):
        """初始化 Monitor"""
        if self._initialized:
            return
        
        # 初始化分类引擎
        import sys
        from pathlib import Path
        sys.path.insert(0, str(Path(__file__).parent.parent))
        from core.classification_engine import ClassificationEngine
        self._classification_engine = ClassificationEngine()
        
        self._initialized = True
    
    async def check_access(
        self,
        agent_id: str,
        file_path: str,
        operation: AccessOperation,
        context: Dict[str, Any]
    ) -> AccessResult:
        """
        访问控制检查主入口
        
        流程:
        1. 验证 Agent 身份
        2. 查询文件分级
        3. 评估访问策略
        4. 记录审计日志
        5. 返回决策结果
        """
        request = AccessRequest(
            agent_id=agent_id,
            file_path=file_path,
            operation=operation,
            context=context,
            timestamp=datetime.now()
        )
        
        try:
            # 1. Agent 身份验证
            agent = await self._authenticate_agent(agent_id)
            if not agent:
                return await self._deny_access(request, "Agent authentication failed")
            
            # 2. 查询文件分级
            classification = await self._get_classification(file_path)
            
            # 3. 评估访问策略
            policy_decision = await self._evaluate_policy(
                agent, classification, operation, context
            )
            
            # 4. 记录审计日志
            audit_record_id = await self.audit_logger.log_access_request(
                request, classification, policy_decision
            )
            
            # 5. 返回结果
            return await self._build_result(
                request, classification, policy_decision, audit_record_id
            )
            
        except Exception as e:
            # 任何异常都执行 Fail-Closed
            return await self._handle_error(request, e)
    
    async def _authenticate_agent(self, agent_id: str) -> Optional[Agent]:
        """验证 Agent 身份"""
        return await self.agent_auth.authenticate(agent_id)
    
    async def _get_classification(self, file_path: str) -> Classification:
        """查询文件分级（带 Fail-Closed 保护）"""
        try:
            if self._classification_engine is None:
                await self.initialize()
            
            result = self._classification_engine.classify(file_path)
            
            if result.level:
                # 将字符串级别转换为枚举
                level_map = {
                    'PUBLIC': DataLevel.L1_PUBLIC,
                    'INTERNAL': DataLevel.L2_INTERNAL,
                    'PRIVATE-R': DataLevel.L3_RESTRICTED,
                    'PRIVATE-W': DataLevel.L4_CONFIDENTIAL,
                    'PRIVATE-B': DataLevel.L5_SECRET,
                    'PRIVATE-C': DataLevel.L6_CRITICAL,
                }
                level = level_map.get(result.level, DataLevel.L6_CRITICAL)
            else:
                # 未匹配到规则，默认 L2
                level = DataLevel.L2_INTERNAL
            
            return Classification(
                path=file_path,
                level=level,
                source=result.source,
                confidence=result.confidence,
                reason=result.reason
            )
            
        except Exception as e:
            # 服务故障，返回最高安全级别
            return Classification(
                path=file_path,
                level=DataLevel.L6_CRITICAL,
                source="fail_closed",
                confidence=1.0,
                reason=f"Classification service unavailable: {e}"
            )
    
    async def _evaluate_policy(
        self,
        agent: Agent,
        classification: Classification,
        operation: AccessOperation,
        context: Dict[str, Any]
    ) -> PolicyDecision:
        """评估访问策略"""
        return await self.policy_engine.evaluate(
            agent, classification, operation, context
        )
    
    async def _deny_access(
        self,
        request: AccessRequest,
        reason: str
    ) -> AccessResult:
        """拒绝访问"""
        audit_record_id = secrets.token_hex(16)
        
        return AccessResult(
            decision=AccessDecision.DENY,
            token=None,
            expires_at=None,
            level=DataLevel.L6_CRITICAL,
            policy="deny_by_default",
            reason=reason,
            audit_record_id=audit_record_id
        )
    
    async def _handle_error(
        self,
        request: AccessRequest,
        error: Exception
    ) -> AccessResult:
        """错误处理 - Fail-Closed"""
        await self.audit_logger.log_error(request, error)
        
        # 通知用户（简化实现）
        print(f"⚠️ Reference Monitor 降级: {error}")
        
        return AccessResult(
            decision=AccessDecision.DENY,
            token=None,
            expires_at=None,
            level=DataLevel.L6_CRITICAL,
            policy="fail_closed",
            reason=f"System error, access denied for security: {str(error)}",
            audit_record_id="error"
        )
    
    async def _build_result(
        self,
        request: AccessRequest,
        classification: Classification,
        policy_decision: PolicyDecision,
        audit_record_id: str
    ) -> AccessResult:
        """构建访问结果"""
        
        if policy_decision.decision == AccessDecision.ALLOW:
            # 生成访问令牌
            token = self._generate_access_token(
                request.agent_id,
                request.file_path,
                request.operation
            )
            
            return AccessResult(
                decision=AccessDecision.ALLOW,
                token=token,
                expires_at=datetime.now() + timedelta(minutes=5),  # 5分钟有效期
                level=classification.level,
                policy=policy_decision.reason,
                reason=policy_decision.reason,
                audit_record_id=audit_record_id
            )
        
        elif policy_decision.decision == AccessDecision.PENDING:
            return AccessResult(
                decision=AccessDecision.PENDING,
                token=None,
                expires_at=None,
                level=classification.level,
                policy="require_authorization",
                reason=policy_decision.reason,
                audit_record_id=audit_record_id
            )
        
        else:  # DENY
            return AccessResult(
                decision=AccessDecision.DENY,
                token=None,
                expires_at=None,
                level=classification.level,
                policy="deny_by_policy",
                reason=policy_decision.reason,
                audit_record_id=audit_record_id
            )
    
    def _generate_access_token(
        self,
        agent_id: str,
        file_path: str,
        operation: AccessOperation
    ) -> str:
        """生成访问令牌"""
        data = f"{agent_id}:{file_path}:{operation.value}:{time.time()}"
        return hashlib.sha256(data.encode()).hexdigest()[:32]


# 线程安全的 Agent 上下文
_current_agent: ContextVar[Optional[AgentContext]] = ContextVar('current_agent', default=None)


class AgentContextManager:
    """Agent 上下文管理器"""
    
    @staticmethod
    def set_context(context: AgentContext):
        """设置当前 Agent 上下文"""
        _current_agent.set(context)
    
    @staticmethod
    def get_context() -> Optional[AgentContext]:
        """获取当前 Agent 上下文"""
        return _current_agent.get()
    
    @staticmethod
    def clear_context():
        """清除当前 Agent 上下文"""
        _current_agent.set(None)
    
    @staticmethod
    def update_task(task_description: str):
        """更新当前任务描述"""
        context = _current_agent.get()
        if context:
            context.current_task = task_description
