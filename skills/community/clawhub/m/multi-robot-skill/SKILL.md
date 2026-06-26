---
name: multi-robot
description: "多机器人协同控制 Skill。让 AI Agent 具备感知反馈、动态适配、并行调度多种机器人的能力。支持机械臂、四足机器人等任意 HTTP API 机器人。"
metadata: {
  "openclaw": {
    "emoji": "🤖",
    "requires": {
      "python": ">=3.8",
      "pip": ["requests>=2.28.0"]
    }
  }
}
---

# Multi-Robot Coordination Skill

## 你是什么

你是一个多机器人协同控制 Agent。用户会给你机器人的 API 文档，你需要：

1. **读懂文档** → 理解机器人有哪些接口、参数、返回值
2. **生成适配器** → 写一个继承 `RobotAdapter` 的 Python 类
3. **注册机器人** → 用 `skill.register_adapter()` 注入
4. **编排任务** → 用 `create_task` / `create_plan` / `execute_plan` 执行

你不需要预先知道机器人的型号，只需要能读懂 HTTP API 文档。

---

## Skill API 速查

```python
from multi_robot_skill import MultiRobotSkill

skill = MultiRobotSkill()
```

### 注册机器人

```python
# 方式1：内置类型（vansbot / puppypi）
skill.register_robot("arm1", "http://192.168.3.113:5000", robot_type="vansbot")
skill.register_robot("dog1", "http://192.168.3.120:8000", robot_type="puppypi", robot_id=1)

# 方式2：自定义适配器（你生成的代码）
adapter = MyRobotAdapter("robot_name", "http://ip:port")
skill.register_adapter(adapter)  # auto_connect=True 默认自动连接
```

### 创建和执行任务

```python
# 创建计划
plan = skill.create_plan("任务名称", "描述")

# 创建原子任务
task = skill.create_task(
    robot="robot_name",       # 已注册的机器人名称
    action="action_name",     # 动作名称（必须在 get_capabilities() 中定义）
    params={"key": "value"},  # 动作参数（可选）
    name="任务显示名",         # 可选
    depends_on=["task_id"],   # 依赖的任务 ID 列表（可选）
    timeout=60.0              # 超时秒数（可选）
)

# 并行任务（多个任务同时执行）
parallel = skill.create_parallel_tasks([task1, task2], name="并行组")

# 顺序任务（多个任务依次执行）
sequential = skill.create_sequential_tasks([task1, task2], name="顺序组")

# 添加到计划并执行
plan.add_task(task)
results = skill.execute_plan(plan)
```

### 查询状态

```python
skill.list_robots()                          # 已注册机器人列表
skill.get_robot_capabilities("robot_name")   # 某机器人的能力列表
skill.get_status()                           # 系统整体状态
```

### 执行结果

```python
for result in results:
    result.success        # bool
    result.task_name      # str
    result.message        # str
    result.data           # dict | None（动作返回的数据）
    result.execution_time # float（秒）
    result.error          # Exception | None
```

---

## 如何生成适配器

当用户给你一个新机器人的 API 文档时，按以下模板生成适配器代码：

```python
import requests
from multi_robot_skill.adapters.base import (
    RobotAdapter, RobotCapability, RobotState, ActionResult,
    ActionStatus, RobotType
)

class MyRobotAdapter(RobotAdapter):
    """
    [机器人名称] 适配器
    端点: http://ip:port
    """

    def __init__(self, name: str, endpoint: str, **config):
        super().__init__(name, endpoint, **config)
        self.robot_type = RobotType.WHEELED  # 根据实际类型修改
        self.timeout = config.get("timeout", 30)

        # 声明该机器人支持的所有动作
        self._capabilities = [
            RobotCapability("action_name", "动作描述", {"param1": "类型说明"}),
            # ... 更多动作
        ]

    def connect(self) -> bool:
        try:
            # 调用机器人的健康检查或连接接口
            resp = requests.get(f"{self.endpoint}/health", timeout=5)
            self._state.connected = resp.status_code == 200
            return self._state.connected
        except Exception:
            self._state.connected = False
            return False

    def disconnect(self) -> bool:
        self._state.connected = False
        return True

    def get_state(self) -> RobotState:
        try:
            resp = requests.get(f"{self.endpoint}/state", timeout=self.timeout)
            data = resp.json()
            self._state.battery = data.get("battery")
            self._state.position = data.get("position")
        except Exception:
            pass
        return self._state

    def get_capabilities(self):
        return self._capabilities

    def execute_action(self, action: str, params: dict = None) -> ActionResult:
        params = params or {}
        try:
            if action == "action_name":
                resp = requests.post(
                    f"{self.endpoint}/api/action",
                    json=params,
                    timeout=self.timeout
                )
                data = resp.json()
                if data.get("success"):
                    return ActionResult(ActionStatus.SUCCESS, "完成", data=data)
                else:
                    return ActionResult(ActionStatus.FAILED, data.get("message", "失败"))

            # ... 其他动作

            return ActionResult(ActionStatus.FAILED, f"未知动作: {action}")

        except requests.Timeout:
            return ActionResult(ActionStatus.TIMEOUT, f"动作 {action} 超时")
        except Exception as e:
            return ActionResult(ActionStatus.FAILED, str(e), error=e)
```

**关键规则：**
- `connect()` 失败时 `register_adapter()` 会返回 False，注册不成功
- `execute_action()` 必须返回 `ActionResult`，不能抛出异常
- `_capabilities` 里的 `name` 必须和 `execute_action` 里的 `action` 字符串完全一致
- `ActionStatus` 枚举值：`SUCCESS` / `FAILED` / `TIMEOUT` / `CANCELLED` / `IN_PROGRESS`

---

## 内置机器人能力参考

### Vansbot（机械臂）

| 动作 | 参数 | 说明 |
|------|------|------|
| `detect_objects` | `move_to_capture=True`, `include_image=False` | 检测桌面物体，返回物体列表 |
| `move_to_object` | `object_no: int` | 移动到指定编号物体上方 |
| `grab` | — | 抓取当前位置物体 |
| `release` | — | 释放物体 |
| `move_to_place` | `place_name: str` | 移动到预设位置 |
| `capture_for_dog` | `move_to_capture=True`, `include_image=False` | 拍摄定位篮筐 |
| `release_to_dog` | `point_id: int` | 放入篮筐指定点位 |

### PuppyPi（四足机器狗）

| 动作 | 参数 | 说明 |
|------|------|------|
| `move_to_zone` | `target_zone: str` | 移动到区域（loading/unloading/charging/parking） |
| `adjust_posture` | `posture: str` | 调整姿态 |
| `load` | `target_zone: str` | 进入装货姿态 |
| `unload` | — | 执行卸货动作 |

---

## 任务编排模式

### 模式1：顺序依赖

```python
t1 = skill.create_task("arm", "detect_objects", name="检测")
t2 = skill.create_task("arm", "grab", name="抓取", depends_on=[t1.id])
t3 = skill.create_task("arm", "release", name="释放", depends_on=[t2.id])

plan = skill.create_plan("顺序任务")
for t in [t1, t2, t3]:
    plan.add_task(t)
results = skill.execute_plan(plan)
```

### 模式2：并行执行

```python
t1 = skill.create_task("dog1", "move_to_zone", {"target_zone": "loading"})
t2 = skill.create_task("dog2", "move_to_zone", {"target_zone": "charging"})

plan = skill.create_plan("并行移动")
plan.add_task(skill.create_parallel_tasks([t1, t2]))
results = skill.execute_plan(plan)
```

### 模式3：多机器人协同（最常用）

```python
# 机械臂和机器狗同时准备，都准备好后再协同动作
arm_detect = skill.create_task("arm", "detect_objects")
arm_grab   = skill.create_task("arm", "grab", depends_on=[arm_detect.id])

dog_move   = skill.create_task("dog1", "move_to_zone", {"target_zone": "loading"})
dog_ready  = skill.create_task("dog1", "load", depends_on=[dog_move.id])

# 等待双方都完成后执行放置
place = skill.create_task(
    "arm", "release_to_dog", {"point_id": 5},
    depends_on=[arm_grab.id, dog_ready.id]  # 等待两个前置任务
)

transport = skill.create_task("dog1", "move_to_zone", {"target_zone": "unloading"}, depends_on=[place.id])
unload    = skill.create_task("dog1", "unload", depends_on=[transport.id])

plan = skill.create_plan("协同搬运")
for t in [arm_detect, arm_grab, dog_move, dog_ready, place, transport, unload]:
    plan.add_task(t)

results = skill.execute_plan(plan)
```

---

## 处理用户请求的标准流程

1. **用户描述任务** → 理解意图，确认需要哪些机器人
2. **用户提供机器人文档** → 生成适配器代码，注册机器人
3. **规划任务** → 分析哪些步骤可以并行，哪些必须顺序
4. **执行并反馈** → 执行计划，把结果用自然语言告诉用户

如果用户没有提供机器人文档，先问清楚：
- 机器人的 IP 和端口
- 有哪些 HTTP 接口（或者让用户粘贴 API 文档）

---

## 错误处理

```python
# 配置重试策略（在执行前设置）
skill.configure_error_handling({
    "max_retries": 3,
    "retry_delay": 1.0,
    "timeout": 60.0,
    "default_strategy": "retry"  # retry / skip / abort / rollback / continue
})

# 检查执行结果
results = skill.execute_plan(plan)
failed = [r for r in results if not r.success]
if failed:
    for r in failed:
        print(f"失败: {r.task_name} - {r.message}")
```

---

## 注意事项

- `depends_on` 接受 task ID 列表（`task.id` 是自动生成的 UUID 字符串）
- 同一个机器人的任务会自动串行（不会并发调用同一机器人）
- `execute_plan()` 是阻塞调用，等所有任务完成后返回
- 用 `with MultiRobotSkill() as skill:` 可以自动清理连接
