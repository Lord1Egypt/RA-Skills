# 多智能体应急响应系统 - 部署与使用指南

## 一、系统部署

### 1.1 环境要求

```bash
Python 3.8+
asyncio
PyYAML
```

### 1.2 安装依赖

```bash
pip install pyyaml
```

### 1.3 目录结构

```
Corporate-Emergency-Response-Guidance-Skill/
├── multi_agent/
│   ├── ARCHITECTURE.md              # 架构设计文档
│   ├── agents/
│   │   ├── ic_agent.yaml            # 指挥官智能体配置
│   │   ├── analyst_agent.yaml       # 分析师智能体配置
│   │   ├── scribe_agent.yaml        # 记录员智能体配置
│   │   └── advisor_agent.yaml       # 顾问智能体配置
│   ├── workflows/
│   │   └── standard_ir.yaml         # 标准应急响应工作流
│   ├── framework/
│   │   └── agent_framework.py       # 智能体框架实现
│   └── examples/
│       ├── quick_start.py           # 快速开始示例
│       ├── parallel_analysis.py     # 并行分析示例
│       └── hitl_demo.py             # HITL演示示例
├── memory/
│   ├── working/
│   ├── semantic/
│   └── episodic/
├── playbooks/
├── scripts/
└── reports/
```

### 1.4 启动系统

```python
import asyncio
from multi_agent.framework.agent_framework import Orchestrator

async def main():
    # 创建协调器
    orchestrator = Orchestrator()
    await orchestrator.initialize()
    
    # 创建会话
    session_id = await orchestrator.create_session("应急响应事件-2026")
    
    # 创建智能体
    ic_agent_id = await orchestrator.spawn_agent(
        "ic_agent", 
        "multi_agent/agents/ic_agent.yaml"
    )
    analyst_agent_id = await orchestrator.spawn_agent(
        "analyst_agent",
        "multi_agent/agents/analyst_agent.yaml"
    )
    scribe_agent_id = await orchestrator.spawn_agent(
        "scribe_agent",
        "multi_agent/agents/scribe_agent.yaml"
    )
    
    # 启动监控
    asyncio.create_task(orchestrator.monitor_agents())
    asyncio.create_task(orchestrator.handle_emergencies())
    
    # 运行应急响应工作流
    await run_incident_response(orchestrator, session_id)

asyncio.run(main())
```

---

## 二、基本使用

### 2.1 初始化事件

```python
from multi_agent.framework.agent_framework import (
    Orchestrator, Task, Priority
)

async def init_incident(orchestrator: Orchestrator, alert_data: dict):
    """初始化应急事件"""
    
    # 创建事件
    task = Task(
        task_id=str(uuid.uuid4()),
        task_type="create_incident",
        priority=Priority.HIGH,
        inputs={
            "alert_data": alert_data,
            "initial_scope": "srv-01, 10.0.0.0/24"
        }
    )
    
    # 提交任务
    await orchestrator.task_router.submit_task(task)
    
    # 路由到IC Agent
    success = await orchestrator.task_router.route_task(task)
    
    if success:
        print(f"Incident created and assigned")
    else:
        print(f"No available agent")
```

### 2.2 并行分析

```python
async def parallel_analysis(orchestrator: Orchestrator, incident_id: str):
    """并行分析事件"""
    
    # 创建并行任务
    tasks = [
        Task(
            task_id=str(uuid.uuid4()),
            task_type="analyze_logs",
            priority=Priority.HIGH,
            inputs={"incident_id": incident_id, "log_type": "system"}
        ),
        Task(
            task_id=str(uuid.uuid4()),
            task_type="analyze_traffic",
            priority=Priority.HIGH,
            inputs={"incident_id": incident_id, "pcap_file": "/path/to/traffic.pcap"}
        ),
        Task(
            task_id=str(uuid.uuid4()),
            task_type="enrich_iocs",
            priority=Priority.MEDIUM,
            inputs={"ioc_list": ["1.2.3.4", "evil.com"]}
        )
    ]
    
    # 并行提交
    for task in tasks:
        await orchestrator.task_router.submit_task(task)
        await orchestrator.task_router.route_task(task)
    
    # 等待完成
    results = await wait_for_tasks(orchestrator, tasks)
    return results
```

### 2.3 HITL人工确认

```python
async def hitl_approval(orchestrator: Orchestrator, action: str, details: dict):
    """人工确认高风险操作"""
    
    # 发送确认请求
    ic_agent = orchestrator.agents.get("ic_agent-xxx")
    
    message = await ic_agent.send_message(
        receiver=ic_agent.identity,
        message_type=MessageType.REQUEST,
        content={
            "action": "approve_containment",
            "containment_type": action,
            "details": details
        },
        priority=Priority.CRITICAL
    )
    
    # 等待响应
    response = await ic_agent.receive_message()
    
    if response.content.get("approval_status") == "approved":
        print("Approved by human")
        return True
    else:
        print("Rejected or timeout")
        return False
```

---

## 三、工作流执行

### 3.1 标准应急响应工作流

```python
async def run_incident_response(orchestrator: Orchestrator, session_id: str):
    """运行标准应急响应工作流"""
    
    # Phase 1: Detect
    await detect_phase(orchestrator, session_id)
    
    # Phase 2: Triage
    await triage_phase(orchestrator, session_id)
    
    # Phase 3: Contain
    await contain_phase(orchestrator, session_id)
    
    # Phase 4: Eradicate
    await eradicate_phase(orchestrator, session_id)
    
    # Phase 5: Recover
    await recover_phase(orchestrator, session_id)
    
    # Phase 6: Postmortem
    await postmortem_phase(orchestrator, session_id)
    
    # Phase 7: Report
    await report_phase(orchestrator, session_id)


async def detect_phase(orchestrator: Orchestrator, session_id: str):
    """检测阶段"""
    print("=== Detect Phase ===")
    
    # 创建事件
    task = Task(
        task_id=str(uuid.uuid4()),
        task_type="create_incident",
        priority=Priority.HIGH,
        inputs={"session_id": session_id}
    )
    await orchestrator.task_router.submit_task(task)
    await orchestrator.task_router.route_task(task)
    
    # 分类事件
    task = Task(
        task_id=str(uuid.uuid4()),
        task_type="classify_incident",
        priority=Priority.HIGH,
        inputs={"alert_data": {"type": "可疑进程"}}
    )
    await orchestrator.task_router.submit_task(task)
    await orchestrator.task_router.route_task(task)


async def triage_phase(orchestrator: Orchestrator, session_id: str):
    """研判阶段"""
    print("=== Triage Phase ===")
    
    # 并行收集证据和分析
    tasks = [
        Task(
            task_id=str(uuid.uuid4()),
            task_type="collect_evidence",
            priority=Priority.HIGH,
            inputs={"session_id": session_id, "target": "srv-01"}
        ),
        Task(
            task_id=str(uuid.uuid4()),
            task_type="analyze_incident",
            priority=Priority.HIGH,
            inputs={"session_id": session_id}
        )
    ]
    
    for task in tasks:
        await orchestrator.task_router.submit_task(task)
        await orchestrator.task_router.route_task(task)


async def contain_phase(orchestrator: Orchestrator, session_id: str):
    """遏制阶段"""
    print("=== Contain Phase ===")
    
    # 提出遏制方案
    task = Task(
        task_id=str(uuid.uuid4()),
        task_type="propose_containment",
        priority=Priority.CRITICAL,
        inputs={"session_id": session_id}
    )
    await orchestrator.task_router.submit_task(task)
    await orchestrator.task_router.route_task(task)
    
    # 评估遏制方案
    task = Task(
        task_id=str(uuid.uuid4()),
        task_type="evaluate_containment",
        priority=Priority.CRITICAL,
        inputs={"session_id": session_id}
    )
    await orchestrator.task_router.submit_task(task)
    await orchestrator.task_router.route_task(task)
    
    # 审批遏制方案（可能需要HITL）
    # ...
```

---

## 四、高级特性

### 4.1 动态扩容

```python
async def auto_scaling(orchestrator: Orchestrator):
    """自动扩容智能体池"""
    
    while True:
        # 检查任务队列长度
        queue_length = orchestrator.task_router.task_queues[Priority.HIGH].qsize()
        
        # 如果队列过长，创建新的智能体
        if queue_length > 5:
            new_agent_id = await orchestrator.spawn_agent(
                "analyst_agent",
                "multi_agent/agents/analyst_agent.yaml"
            )
            print(f"Spawned new analyst agent: {new_agent_id}")
        
        await asyncio.sleep(30)
```

### 4.2 智能体协作示例

```python
async def agent_collaboration_example(orchestrator: Orchestrator):
    """智能体协作示例"""
    
    # Analyst Agent请求Forensics Agent收集证据
    analyst_agent = orchestrator.agents["analyst_agent-xxx"]
    
    # 发送请求到Forensics Agent
    forensics_agent_id = await orchestrator.spawn_agent(
        "forensics_agent",
        "multi_agent/agents/forensics_agent.yaml"
    )
    forensics_agent = orchestrator.agents[forensics_agent_id]
    
    # Analyst发送请求
    message_id = await analyst_agent.send_message(
        receiver=forensics_agent.identity,
        message_type=MessageType.REQUEST,
        content={
            "action": "collect_memory_dump",
            "target": "srv-01"
        }
    )
    
    # Forensics处理请求
    response = await forensics_agent.receive_message()
    result = await forensics_agent.process_message(response)
    
    # Forensics返回结果
    await forensics_agent.send_message(
        receiver=analyst_agent.identity,
        message_type=MessageType.RESPONSE,
        content=result.content
    )
```

### 4.3 冲突解决

```python
async def resolve_conflict(orchestrator: Orchestrator, conflicting_recommendations: list):
    """解决智能体间的冲突"""
    
    # 方法1：投票
    votes = {}
    for recommendation in conflicting_recommendations:
        option = recommendation["option"]
        votes[option] = votes.get(option, 0) + 1
    
    # 选择得票最多的
    winner = max(votes, key=votes.get)
    
    # 方法2：权重（基于历史准确率）
    weighted_votes = {}
    for recommendation in conflicting_recommendations:
        option = recommendation["option"]
        confidence = recommendation["confidence"]  # 基于历史表现
        weighted_votes[option] = weighted_votes.get(option, 0) + confidence
    
    # 方法3：IC Agent最终决策
    ic_agent = orchestrator.agents["ic_agent-xxx"]
    decision = await ic_agent.make_decision(conflicting_recommendations)
    
    return decision
```

---

## 五、监控与调试

### 5.1 日志配置

```python
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/multi_agent_system.log'),
        logging.StreamHandler()
    ]
)
```

### 5.2 性能监控

```python
async def monitor_performance(orchestrator: Orchestrator):
    """监控性能指标"""
    
    metrics = {
        "active_agents": len([a for a in orchestrator.agents.values() if a.state == AgentState.WORKING]),
        "idle_agents": len([a for a in orchestrator.agents.values() if a.state == AgentState.IDLE]),
        "pending_tasks": sum(q.qsize() for q in orchestrator.task_router.task_queues.values()),
        "completed_tasks": len(orchestrator.task_router.task_history)
    }
    
    print(f"Performance Metrics: {metrics}")
    return metrics
```

### 5.3 调试工具

```python
async def debug_agent_state(orchestrator: Orchestrator, agent_id: str):
    """调试智能体状态"""
    
    agent = orchestrator.agents.get(agent_id)
    if not agent:
        print(f"Agent {agent_id} not found")
        return
    
    print(f"=== Agent {agent_id} ===")
    print(f"State: {agent.state.value}")
    print(f"Capabilities: {agent.identity.capabilities}")
    print(f"Current Task: {agent.current_task}")
    print(f"Message Queue Size: {agent.message_queue.qsize()}")
```

---

## 六、最佳实践

### 6.1 智能体设计原则

1. **单一职责**：每个智能体专注于一个领域
2. **最小权限**：只授予必要的权限
3. **异步优先**：使用异步API避免阻塞
4. **错误恢复**：实现健壮的错误处理
5. **可观测性**：记录关键事件和指标

### 6.2 通信优化

1. **批量处理**：合并小消息
2. **消息压缩**：大消息使用压缩
3. **优先级队列**：重要消息优先处理
4. **超时控制**：设置合理的超时
5. **幂等性**：确保重复消息不会造成问题

### 6.3 资源管理

1. **连接池**：复用连接资源
2. **内存限制**：限制每个智能体的内存使用
3. **并发控制**：限制并发任务数量
4. **定期清理**：清理过期数据和缓存
5. **优雅关闭**：实现平滑的关闭流程

---

## 七、故障排查

### 7.1 常见问题

**问题1：智能体无响应**
```python
# 检查智能体状态
agent = orchestrator.agents[agent_id]
if agent.state == AgentState.ERROR:
    # 重启智能体
    await orchestrator.restart_agent(agent_id)
```

**问题2：消息丢失**
```python
# 检查消息队列
queue_size = agent.message_queue.qsize()
if queue_size > 100:
    print(f"Message queue overflow for agent {agent_id}")
    # 增加处理速度或扩容
```

**问题3：死锁**
```python
# 检测死锁
if await detect_deadlock(orchestrator):
    # 强制终止部分智能体
    await orchestrator.terminate_agent(blocked_agent_id)
```

### 7.2 调试技巧

1. **启用详细日志**
```python
logging.getLogger("Orchestrator").setLevel(logging.DEBUG)
logging.getLogger("ICAgent").setLevel(logging.DEBUG)
```

2. **使用调试模式**
```python
# 在配置文件中启用
debug:
  enabled: true
  log_all_messages: true
  trace_state_changes: true
```

3. **单元测试**
```python
# tests/test_multi_agent.py
import pytest

@pytest.mark.asyncio
async def test_ic_agent_decision():
    ic_agent = ICAgent("test-ic", "ic_agent", "ic")
    # 测试决策逻辑
    result = await ic_agent.execute_task(test_task)
    assert result["status"] == "approved"
```

---

## 八、扩展开发

### 8.1 添加新智能体

```python
# multi_agent/agents/custom_agent.yaml
name: custom_agent
version: 1.0.0
type: worker_agent
role: Custom Specialist

capabilities:
  - custom_capability_1
  - custom_capability_2

responsibilities:
  - 自定义职责1
  - 自定义职责2

# multi_agent/framework/custom_agent.py
class CustomAgent(BaseAgent):
    def configure(self, config: Dict[str, Any]):
        # 自定义配置
        pass
    
    async def process_message(self, message: Message) -> Optional[Message]:
        # 自定义消息处理
        pass
    
    async def execute_task(self, task: Task) -> Dict[str, Any]:
        # 自定义任务执行
        pass
```

### 8.2 添加新工作流

```yaml
# multi_agent/workflows/custom_workflow.yaml
name: custom_incident_response
version: 1.0.0
type: workflow

phases:
  - id: custom_phase_1
    name: 自定义阶段1
    activities:
      - agent: custom_agent
        action: custom_action
```

### 8.3 集成外部系统

```python
# integrations/external_system.py
class ExternalSystemIntegration:
    def __init__(self, api_endpoint: str, api_key: str):
        self.endpoint = api_endpoint
        self.api_key = api_key
    
    async def send_alert(self, alert_data: dict):
        """发送告警到外部系统"""
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.endpoint}/alerts",
                json=alert_data,
                headers={"Authorization": f"Bearer {self.api_key}"}
            ) as response:
                return await response.json()
```

---

## 九、生产部署

### 9.1 Docker部署

```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY multi_agent/ ./multi_agent/
COPY playbooks/ ./playbooks/
COPY scripts/ ./scripts/
COPY memory/ ./memory/

ENV PYTHONUNBUFFERED=1

CMD ["python", "-m", "multi_agent.framework.agent_framework"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  orchestrator:
    build: .
    command: python -m multi_agent.framework.agent_framework
    volumes:
      - ./logs:/app/logs
      - ./memory:/app/memory
      - ./evidence:/app/evidence
    environment:
      - LOG_LEVEL=INFO
    ports:
      - "8000:8000"
```

### 9.2 Kubernetes部署

```yaml
# kubernetes/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: multi-agent-system
spec:
  replicas: 3
  selector:
    matchLabels:
      app: multi-agent
  template:
    metadata:
      labels:
        app: multi-agent
    spec:
      containers:
      - name: orchestrator
        image: multi-agent-system:latest
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
```

### 9.3 监控与告警

```python
# monitoring/prometheus_exporter.py
from prometheus_client import Counter, Gauge, start_http_server

# 定义指标
TASKS_TOTAL = Counter('tasks_total', 'Total tasks processed')
ACTIVE_AGENTS = Gauge('active_agents', 'Number of active agents')
QUEUE_LENGTH = Gauge('queue_length', 'Task queue length')

def export_metrics(orchestrator: Orchestrator):
    """导出指标到Prometheus"""
    ACTIVE_AGENTS.set(len(orchestrator.agents))
    QUEUE_LENGTH.set(sum(q.qsize() for q in orchestrator.task_router.task_queues.values()))
    
if __name__ == "__main__":
    start_http_server(8000)
```

---

## 十、总结

这个多智能体应急响应系统提供了：

1. ✅ **角色分工明确**：IC/Analyst/Scribe/Advisor各司其职
2. ✅ **并行处理能力**：多智能体同时工作，提高效率
3. ✅ **智能协调机制**：自动路由、负载均衡、冲突解决
4. ✅ **人工确认闸门**：HITL确保高风险操作安全
5. ✅ **可扩展架构**：易于添加新智能体和工作流
6. ✅ **生产就绪**：提供Docker/Kubernetes部署方案

立即开始使用：

```bash
# 1. 克隆项目
cd Corporate-Emergency-Response-Guidance-Skill

# 2. 安装依赖
pip install pyyaml

# 3. 运行示例
python multi_agent/examples/quick_start.py
```

更多示例和文档：
- `multi_agent/examples/parallel_analysis.py` - 并行分析示例
- `multi_agent/examples/hitl_demo.py` - HITL演示
- `multi_agent/ARCHITECTURE.md` - 详细架构设计
