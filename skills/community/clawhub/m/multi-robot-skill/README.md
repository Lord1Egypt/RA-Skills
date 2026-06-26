# Multi-Robot Coordination Skill

一个可用于任意机器人的多机器人协同控制技能包，适用于各种 AI Agent 框架（OpenClaw、Claude Code 等）。

## 🎯 设计目标

让 AI Agent 能够：
1. **理解自然语言任务** - 用户用自然语言描述任务，AI 自动理解
2. **自动任务分解** - 将复杂任务分解为可执行的子任务
3. **智能协调调度** - 协调多个机器人并行/串行执行
4. **处理现实问题** - 网络超时、错误恢复、状态同步等

## 🏗️ 架构设计

```
┌─────────────────────────────────────────────────────┐
│              AI Agent (Claude Code/OpenClaw)        │
│         (自然语言理解 + 任务规划)                     │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│           Multi-Robot Skill (本项目)                │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────┐ │
│  │ Task Planner │  │ Coordinator  │  │   State   │ │
│  │  任务规划器   │  │   协调器      │  │  Manager  │ │
│  └──────────────┘  └──────────────┘  └───────────┘ │
└──────────────────┬──────────────────────────────────┘
                   │
        ┌──────────┼──────────┐
        ▼          ▼          ▼
   ┌────────┐ ┌────────┐ ┌────────────┐
   │Vansbot │ │PuppyPi │ │  任意机器人 │
   │Adapter │ │Adapter │ │  (AI生成)  │
   └────┬───┘ └────┬───┘ └─────┬──────┘
        │          │           │
        ▼          ▼           ▼
   ┌────────┐ ┌────────┐ ┌────────────┐
   │机械臂   │ │机器狗  │ │  任意设备   │
   │HTTP API│ │HTTP API│ │  任意协议   │
   └────────┘ └────────┘ └────────────┘
```

## ✨ 核心特性

### 1. 统一的机器人抽象
- 标准化的机器人接口
- 支持多种通信协议（HTTP、ROS、SDK）
- 能力描述系统

### 2. 智能任务规划
- 任务依赖分析
- 并行/串行执行决策
- 资源冲突检测

### 3. 可靠的协调执行
- 并发控制
- 超时和重试机制
- 错误恢复策略

### 4. 实时状态管理
- 机器人状态跟踪
- 任务进度监控
- 事件通知

## 🚀 快速开始

> **最简单的方式：** 直接告诉你的 AI Agent（如 OpenClaw）：
>
> *"帮我安装这个 skill：https://github.com/Alan1112223331/multi-robot-skill.git，然后我给你机器人的技术文档，你来接入它。"*
>
> Agent 会自动 clone、安装依赖、读取 `SKILL.md`，并根据你提供的机器人 API 文档生成适配器。

### 手动安装

```bash
git clone https://github.com/Alan1112223331/multi-robot-skill.git
cd multi_robot_skill
pip install -r requirements.txt
```

### 基础使用

```python
from multi_robot_skill import MultiRobotSkill

# 初始化 Skill
skill = MultiRobotSkill()

# 注册机器人
skill.register_robot("vansbot", "http://192.168.3.113:5000")
skill.register_robot("dog1", "http://localhost:8000", robot_id=1)
skill.register_robot("dog2", "http://localhost:8000", robot_id=2)

# 执行任务（自然语言）
result = skill.execute_task("""
让机械臂抓取绿色方块放到狗1的篮筐里，
然后让狗1运送到卸货区
""")

print(result)
```

### 高级用法

```python
# 定义复杂的协同任务
task_plan = {
    "name": "物流协同任务",
    "steps": [
        {
            "id": "detect",
            "robot": "vansbot",
            "action": "detect_objects",
            "description": "识别桌面物体"
        },
        {
            "id": "parallel_move",
            "type": "parallel",
            "subtasks": [
                {
                    "robot": "dog1",
                    "action": "move_to_zone",
                    "params": {"zone": "loading"}
                },
                {
                    "robot": "dog2",
                    "action": "move_to_zone",
                    "params": {"zone": "charging"}
                }
            ]
        },
        {
            "id": "grab_and_place",
            "robot": "vansbot",
            "action": "grab_and_place",
            "params": {"object_id": 0, "target": "dog1_basket"},
            "depends_on": ["detect", "parallel_move"]
        }
    ]
}

result = skill.execute_plan(task_plan)
```

## 📚 API 文档

### MultiRobotSkill

主要的 Skill 接口类。

#### 方法

- `register_robot(name, endpoint, **config)` - 注册机器人
- `execute_task(description)` - 执行自然语言任务
- `execute_plan(plan)` - 执行结构化任务计划
- `get_status()` - 获取系统状态
- `cancel_task(task_id)` - 取消任务

### RobotAdapter

机器人适配器基类。

#### 必须实现的方法

- `connect()` - 连接机器人
- `disconnect()` - 断开连接
- `execute_action(action, params)` - 执行动作
- `get_state()` - 获取状态
- `get_capabilities()` - 获取能力描述

## 🔧 扩展新机器人

创建新的适配器非常简单：

```python
from multi_robot_skill.adapters.base import RobotAdapter, RobotCapability

class MyRobotAdapter(RobotAdapter):
    def __init__(self, endpoint, **config):
        super().__init__(endpoint, **config)
        self.api_client = MyRobotAPI(endpoint)

    def connect(self):
        return self.api_client.connect()

    def execute_action(self, action, params):
        if action == "move":
            return self.api_client.move(**params)
        elif action == "grab":
            return self.api_client.grab(**params)
        # ... 其他动作

    def get_capabilities(self):
        return [
            RobotCapability("move", "移动到指定位置"),
            RobotCapability("grab", "抓取物体"),
        ]
```

## 🎯 使用场景

### 场景1：简单的单机器人任务

```python
skill.execute_task("让机械臂抓取0号物体")
```

### 场景2：多机器人并行任务

```python
skill.execute_task("让狗1去装货区，同时让狗2去充电区")
```

### 场景3：复杂的协同任务

```python
skill.execute_task("""
1. 机械臂识别桌面物体
2. 机械臂抓取绿色方块
3. 狗1移动到装货区并调整姿势
4. 机械臂将方块放入狗1篮筐
5. 狗1运送到卸货区并卸货
6. 狗1返回停靠区
""")
```

## 🛡️ 错误处理

系统内置多层错误处理：

1. **网络层** - 自动重试、超时控制
2. **执行层** - 动作失败恢复、状态回滚
3. **协调层** - 任务失败重新规划

```python
# 配置错误处理策略
skill.configure_error_handling({
    "max_retries": 3,
    "retry_delay": 1.0,
    "timeout": 30.0,
    "on_failure": "rollback"  # 或 "continue", "abort"
})
```

## 📊 监控和调试

```python
# 启用详细日志
skill.set_log_level("DEBUG")

# 获取执行历史
history = skill.get_execution_history()

# 实时监控
skill.on_event("task_started", lambda e: print(f"任务开始: {e}"))
skill.on_event("task_completed", lambda e: print(f"任务完成: {e}"))
skill.on_event("error", lambda e: print(f"错误: {e}"))
```

## 🧪 测试

```bash
# 运行所有测试
pytest tests/

# 运行特定测试
pytest tests/test_coordinator.py

# 模拟模式测试（不需要真实机器人）
pytest tests/ --mock
```

## 📝 配置文件

`config.yaml`:

```yaml
robots:
  vansbot:
    type: manipulator
    endpoint: http://192.168.3.113:5000
    timeout: 30
    capabilities:
      - detect_objects
      - grab
      - release
      - move_to_object

  dog1:
    type: quadruped
    endpoint: http://localhost:8000
    robot_id: 1
    capabilities:
      - move_to_zone
      - adjust_posture
      - load
      - unload

coordination:
  max_parallel_tasks: 4
  task_timeout: 60
  enable_collision_detection: true

error_handling:
  max_retries: 3
  retry_delay: 1.0
  on_failure: rollback
```

## 🔗 集成到其他框架

### OpenClaw 集成

本 Skill 可以轻松集成到 OpenClaw 框架中，实现通过即时通讯（微信、WhatsApp 等）控制机器人。

OpenClaw 加载后会自动读取 `SKILL.md`，Claude 就知道如何操作这个 Skill，包括：
- 读取用户提供的机器人 API 文档，自动生成适配器
- 编排多机器人协同任务
- 实时反馈执行进度

详细集成指南请参考：[OPENCLAW_INTEGRATION.md](OPENCLAW_INTEGRATION.md)
**OpenClaw Agent 操作手册：[SKILL.md](SKILL.md)**

### 其他 AI Agent 框架

本 Skill 采用标准 Python API，可以集成到任何支持 Python 的 AI Agent 框架中。

## 🤝 贡献

欢迎贡献新的机器人适配器或改进！

## 📄 许可证

MIT License
