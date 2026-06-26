# OpenClaw 集成指南

本文档说明如何将 Multi-Robot Skill 集成到 OpenClaw 框架中。

## 📦 什么是 OpenClaw？

OpenClaw 是基于 Anthropic Claude 的 AI Agent 框架，支持通过即时通讯（微信、WhatsApp 等）控制各种系统。

## 🎯 核心能力

Multi-Robot Skill 为 OpenClaw 提供：

1. **动态适配新机器人** - AI Agent 读取机器人 API 文档，自己生成适配器代码
2. **多机器人协同** - 并行/串行任务编排，依赖关系管理
3. **实时反馈控制** - 基于机器人状态反馈动态调整任务
4. **错误恢复** - 自动重试、回滚、跳过等策略

**关键特性：** OpenClaw 的 Claude 实例不需要预先知道机器人型号，只需要能读懂 HTTP API 文档，就能自己生成适配器并控制机器人。

## 🔗 集成方式

### 方式 1: 作为 OpenClaw Skill 使用（推荐）

将本项目作为 OpenClaw Skill 安装，OpenClaw 会自动加载 `SKILL.md` 到 Claude 的 system prompt。

#### 步骤 1: 确认 Skill 元数据

项目根目录已有 `_meta.json`（OpenClaw 标准格式）：

```json
{
  "name": "multi-robot",
  "version": "1.0.0",
  "description": "多机器人协同控制 Skill，让 AI Agent 具备感知反馈、动态适配、并行调度多种机器人的能力。",
  "author": "LooperRobotics",
  "main": "skill.py",
  "openclaw": {
    "emoji": "🤖",
    "requires": {
      "python": ">=3.8",
      "pip": ["requests>=2.28.0"]
    }
  }
}
```

#### 步骤 2: 安装到 OpenClaw

```bash
# 本地安装（将整个目录复制到 OpenClaw skills 目录）
cp -r multi_robot_skill ~/.openclaw/skills/multi-robot

# 或通过 ClawHub 安装（如果已发布）
npx skills add multi-robot
```

OpenClaw 加载 Skill 后会自动读取 `SKILL.md`，将其注入 Claude 的 system prompt，Claude 就知道如何操作这个 Skill 了。

#### 步骤 3: 给 Claude 提供机器人文档

安装完成后，直接在对话中把机器人的 API 文档发给 OpenClaw：

```
用户：我有一个机械臂，API 文档如下：
  GET /health → {"status": "ok"}
  POST /robot/grab → {"status": "ok"}
  POST /robot/release → {"status": "ok"}
  ...

请帮我控制它抓取物体。
```

Claude 会自动生成适配器、注册机器人、编排任务并执行。

### 方式 2: 直接在 Python 中使用

如果你的 OpenClaw Agent 是用 Python 编写的，可以直接导入使用：

```python
from multi_robot_skill import MultiRobotSkill
from multi_robot_skill.adapters.base import (
    RobotAdapter, RobotCapability, RobotState, ActionResult, ActionStatus, RobotType
)
import requests

# 1. 根据机器人文档生成适配器
class MyRobotAdapter(RobotAdapter):
    def __init__(self, name, endpoint, **config):
        super().__init__(name, endpoint, **config)
        self.robot_type = RobotType.WHEELED
        self._capabilities = [
            RobotCapability("move", "移动", {"x": "float", "y": "float"}),
            RobotCapability("stop", "停止", {}),
        ]

    def connect(self):
        try:
            resp = requests.get(f"{self.endpoint}/health", timeout=5)
            self._state.connected = resp.status_code == 200
            return self._state.connected
        except Exception:
            return False

    def disconnect(self):
        self._state.connected = False
        return True

    def get_state(self):
        return self._state

    def get_capabilities(self):
        return self._capabilities

    def execute_action(self, action, params=None):
        params = params or {}
        try:
            resp = requests.post(f"{self.endpoint}/api/{action}", json=params, timeout=30)
            data = resp.json()
            if data.get("success"):
                return ActionResult(ActionStatus.SUCCESS, "完成", data=data)
            return ActionResult(ActionStatus.FAILED, data.get("message", "失败"))
        except Exception as e:
            return ActionResult(ActionStatus.FAILED, str(e), error=e)

# 2. 注册并使用
skill = MultiRobotSkill()
skill.register_adapter(MyRobotAdapter("my_robot", "http://192.168.1.100:8080"))

# 3. 编排任务
plan = skill.create_plan("测试任务")
plan.add_task(skill.create_task("my_robot", "move", {"x": 1.0, "y": 0.0}))
results = skill.execute_plan(plan)
```

## 🎯 使用示例

### 通过 OpenClaw 即时通讯控制

用户在微信中发送：
```
让机械臂抓取绿色方块放到狗1的篮筐里，然后让狗1运送到卸货区
```

OpenClaw Agent 处理流程：
1. 接收用户消息
2. Claude 读取 SKILL.md，理解任务意图和可用 API
3. 调用 Multi-Robot Skill 创建任务计划（含依赖关系）
4. 执行任务计划，实时获取反馈
5. 返回执行结果给用户

### 接入新机器人的完整流程

```
用户：我有一个新的轮式机器人，API 如下：
  GET  /health
  POST /move  {"x": float, "y": float, "speed": float}
  POST /stop
  GET  /status → {"battery": int, "position": {"x": float, "y": float}}

帮我让它移动到坐标 (2.0, 3.0)
```

Claude 会：
1. 生成 `WheelRobotAdapter` 类（继承 `RobotAdapter`）
2. 调用 `skill.register_adapter()` 注册
3. 创建 `move` 任务并执行
4. 返回执行结果

## 🔧 高级配置

### 事件回调（实时进度推送）

```python
skill.on_event("task_started", lambda e:
    openclaw.send_message(f"🔄 开始执行: {e['task_name']}")
)

skill.on_event("task_completed", lambda e:
    openclaw.send_message(f"✅ 完成: {e['task_name']}")
)

skill.on_event("task_failed", lambda e:
    openclaw.send_message(f"❌ 失败: {e['task_name']} - {e.get('error', '')}")
)
```

### 错误处理策略

```python
skill.configure_error_handling({
    "max_retries": 3,
    "retry_delay": 1.0,
    "timeout": 60.0,
    "default_strategy": "retry"  # retry / skip / abort / rollback / continue
})
```

## 📚 参考资源

- [SKILL.md](SKILL.md) - **OpenClaw Agent 操作手册（最重要）**
- [USAGE_GUIDE.md](USAGE_GUIDE.md) - 详细 API 使用指南
- [ADAPTER_FIXES.md](ADAPTER_FIXES.md) - 内置适配器 API 对照说明
- [examples/](examples/) - 示例代码

## 📄 许可证

MIT License
