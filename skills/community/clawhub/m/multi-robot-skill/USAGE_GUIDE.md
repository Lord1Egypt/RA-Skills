# Multi-Robot Skill 使用指南

## 🎯 通用设计

这个 Skill 采用通用设计，可以被各种 AI Agent 框架使用：
- **Claude Code** - Anthropic 的 AI 编程助手
- **OpenClaw** - 基于 Claude 的 Agent 框架
- **其他 AI Agent** - 任何支持 Python 的 AI Agent 系统

AI Agent 可以通过简单的 API 调用来协调多个机器人完成复杂任务。

## 🚀 快速开始

### 1. 基础使用

```python
from multi_robot_skill import MultiRobotSkill

# 创建 Skill
skill = MultiRobotSkill()

# 注册机器人
skill.register_robot("vansbot", "http://192.168.3.113:5000")
skill.register_robot("dog1", "http://localhost:8000", robot_type="puppypi", robot_id=1)

# 创建任务计划
plan = skill.create_plan("简单任务")

# 添加任务
task = skill.create_task("vansbot", "detect_objects")
plan.add_task(task)

# 执行
results = skill.execute_plan(plan)
```

### 2. 顺序任务

```python
plan = skill.create_plan("顺序任务")

# 任务1
task1 = skill.create_task("vansbot", "detect_objects", name="检测")

# 任务2（依赖任务1）
task2 = skill.create_task(
    "vansbot",
    "move_to_object",
    {"object_no": 0},
    name="移动",
    depends_on=[task1.id]
)

# 任务3（依赖任务2）
task3 = skill.create_task(
    "vansbot",
    "grab",
    name="抓取",
    depends_on=[task2.id]
)

plan.add_task(task1)
plan.add_task(task2)
plan.add_task(task3)

results = skill.execute_plan(plan)
```

### 3. 并行任务

```python
plan = skill.create_plan("并行任务")

# 创建两个独立的任务
task1 = skill.create_task("dog1", "move_to_zone", {"target_zone": "loading"})
task2 = skill.create_task("dog2", "move_to_zone", {"target_zone": "charging"})

# 包装为并行任务
parallel = skill.create_parallel_tasks([task1, task2], name="同时移动")
plan.add_task(parallel)

results = skill.execute_plan(plan)
```

### 4. 复杂协同

```python
plan = skill.create_plan("协同任务")

# 机械臂任务链
arm_detect = skill.create_task("vansbot", "detect_objects")
arm_grab = skill.create_task("vansbot", "grab", depends_on=[arm_detect.id])

# 机器狗任务链（与机械臂并行）
dog_move = skill.create_task("dog1", "move_to_zone", {"target_zone": "loading"})
dog_ready = skill.create_task("dog1", "load", depends_on=[dog_move.id])

# 协同任务（需要等待双方都准备好）
place = skill.create_task(
    "vansbot",
    "release_to_dog",
    {"point_id": 5},
    depends_on=[arm_grab.id, dog_ready.id]
)

# 后续任务
transport = skill.create_task("dog1", "move_to_zone", {"target_zone": "unloading"}, depends_on=[place.id])
unload = skill.create_task("dog1", "unload", depends_on=[transport.id])

# 添加所有任务
for task in [arm_detect, arm_grab, dog_move, dog_ready, place, transport, unload]:
    plan.add_task(task)

results = skill.execute_plan(plan)
```

## 📚 API 参考

### MultiRobotSkill

#### 初始化

```python
skill = MultiRobotSkill(
    max_workers=4,      # 最大并行线程数
    log_level="INFO"    # 日志级别
)
```

#### 注册机器人

```python
skill.register_robot(
    name="robot_name",              # 机器人名称（唯一）
    endpoint="http://ip:port",      # 端点URL
    robot_type="auto",              # 类型：vansbot, puppypi, auto
    **config                        # 其他配置
)
```

#### 创建任务

```python
task = skill.create_task(
    robot="robot_name",             # 机器人名称
    action="action_name",           # 动作名称
    params={"key": "value"},        # 动作参数
    name="task_name",               # 任务名称（可选）
    description="description",      # 任务描述（可选）
    depends_on=["task_id"],         # 依赖的任务ID列表（可选）
    timeout=60.0                    # 超时时间（可选）
)
```

#### 创建并行任务

```python
parallel_task = skill.create_parallel_tasks(
    tasks=[task1, task2, task3],    # 子任务列表
    name="parallel_name",           # 任务名称（可选）
    description="description",      # 任务描述（可选）
    depends_on=["task_id"]          # 依赖的任务ID列表（可选）
)
```

#### 创建顺序任务

```python
sequential_task = skill.create_sequential_tasks(
    tasks=[task1, task2, task3],    # 子任务列表（按顺序执行）
    name="sequential_name",         # 任务名称（可选）
    description="description",      # 任务描述（可选）
    depends_on=["task_id"]          # 依赖的任务ID列表（可选）
)
```

#### 执行计划

```python
results = skill.execute_plan(plan)

# 结果是 ExecutionResult 列表
for result in results:
    print(f"任务: {result.task_name}")
    print(f"成功: {result.success}")
    print(f"消息: {result.message}")
    print(f"耗时: {result.execution_time}秒")
    if result.data:
        print(f"数据: {result.data}")
```

#### 事件回调

```python
def on_task_started(event):
    print(f"任务开始: {event['task_name']}")

def on_task_completed(event):
    print(f"任务完成: {event['task_id']}")

skill.on_event("task_started", on_task_started)
skill.on_event("task_completed", on_task_completed)
```

支持的事件：
- `plan_started` - 计划开始
- `plan_completed` - 计划完成
- `plan_failed` - 计划失败
- `task_started` - 任务开始
- `task_completed` - 任务完成
- `task_failed` - 任务失败
- `task_error` - 任务异常

#### 获取状态

```python
status = skill.get_status()

# 返回格式：
{
    "system": {
        "status": "idle",           # idle, running, paused, error
        "active_tasks": 0,
        "completed_tasks": 5,
        "failed_tasks": 0
    },
    "robots": {
        "vansbot": {
            "connected": True,
            "busy": False,
            "battery": "85%",
            ...
        },
        "dog1": {
            "connected": True,
            "busy": False,
            ...
        }
    }
}
```

#### 错误处理配置

```python
skill.configure_error_handling({
    "max_retries": 3,               # 最大重试次数
    "retry_delay": 1.0,             # 重试延迟（秒）
    "timeout": 60.0,                # 超时时间（秒）
    "default_strategy": "retry"     # 默认策略
})
```

策略选项：
- `retry` - 重试
- `skip` - 跳过
- `abort` - 中止
- `rollback` - 回滚
- `continue` - 继续

## 🤖 机器人能力

### Vansbot (机械臂)

| 动作 | 参数 | 说明 |
|------|------|------|
| `detect_objects` | `move_to_capture`, `include_image` | 检测桌面物体 |
| `move_to_object` | `object_no` | 移动到物体上方 |
| `grab` | - | 抓取物体 |
| `release` | - | 释放物体 |
| `move_to_place` | `place_name` | 移动到预设位置 |
| `capture_for_dog` | `move_to_capture`, `include_image` | 拍摄定位篮筐 |
| `release_to_dog` | `point_id` | 放入篮筐 |

### PuppyPi (机器狗)

| 动作 | 参数 | 说明 |
|------|------|------|
| `move_to_zone` | `target_zone` | 移动到区域 |
| `adjust_posture` | `posture` | 调整姿态 |
| `load` | `target_zone` | 进入装货姿态 |
| `unload` | - | 执行卸货 |

## 💡 最佳实践

### 1. 使用上下文管理器

```python
with MultiRobotSkill() as skill:
    # 使用 skill
    pass
# 自动清理资源
```

### 2. 合理设置依赖关系

```python
# ✅ 好的做法：明确依赖
task2 = skill.create_task(..., depends_on=[task1.id])

# ❌ 不好的做法：循环依赖
task1 = skill.create_task(..., depends_on=[task2.id])
task2 = skill.create_task(..., depends_on=[task1.id])
```

### 3. 使用并行任务提高效率

```python
# 如果两个任务可以同时执行，使用并行任务
parallel = skill.create_parallel_tasks([task1, task2])
```

### 4. 设置合理的超时时间

```python
# 根据实际情况设置超时
task = skill.create_task(..., timeout=30.0)
```

### 5. 使用事件回调监控进度

```python
skill.on_event("task_completed", lambda e: print(f"✓ {e['task_name']}"))
```

## 🐛 调试技巧

### 1. 启用详细日志

```python
skill = MultiRobotSkill(log_level="DEBUG")
```

### 2. 检查任务计划

```python
plan = skill.create_plan("test")
# ... 添加任务 ...

# 验证计划
valid, error = skill.planner.validate_plan(plan)
if not valid:
    print(f"计划无效: {error}")

# 查看执行顺序
execution_order = plan.get_execution_order()
for i, batch in enumerate(execution_order):
    print(f"批次 {i+1}: {[t.name for t in batch]}")
```

### 3. 查看执行结果

```python
results = skill.execute_plan(plan)

for result in results:
    if not result.success:
        print(f"失败: {result.task_name}")
        print(f"原因: {result.message}")
        if result.error:
            print(f"异常: {result.error}")
```

## 🔧 扩展新机器人

如果需要添加新的机器人类型：

```python
from multi_robot_skill.adapters.base import RobotAdapter, RobotCapability, ActionResult, ActionStatus

class MyRobotAdapter(RobotAdapter):
    def __init__(self, name, endpoint, **config):
        super().__init__(name, endpoint, **config)
        self.robot_type = RobotType.WHEELED  # 设置类型

        # 定义能力
        self._capabilities = [
            RobotCapability("move", "移动", {"x": "float", "y": "float"}),
            RobotCapability("stop", "停止", {}),
        ]

    def connect(self):
        # 实现连接逻辑
        self._state.connected = True
        return True

    def disconnect(self):
        # 实现断开逻辑
        self._state.connected = False
        return True

    def execute_action(self, action, params):
        # 实现动作执行逻辑
        if action == "move":
            # 执行移动
            return ActionResult(ActionStatus.SUCCESS, "移动完成")
        # ...

    def get_state(self):
        # 返回当前状态
        return self._state

    def get_capabilities(self):
        # 返回能力列表
        return self._capabilities
```

然后在 `skill.py` 中注册：

```python
from .adapters.my_robot_adapter import MyRobotAdapter

# 在 register_robot 方法中添加：
elif robot_type == "myrobot":
    adapter = MyRobotAdapter(name, endpoint, **config)
```

## 📝 常见问题

### Q: 如何处理任务失败？

A: 配置错误处理策略：

```python
skill.configure_error_handling({
    "max_retries": 3,
    "default_strategy": "retry"
})
```

### Q: 如何取消正在执行的任务？

A: 目前不支持取消，但可以设置超时：

```python
task = skill.create_task(..., timeout=30.0)
```

### Q: 如何知道任务执行进度？

A: 使用事件回调：

```python
skill.on_event("task_started", lambda e: print(f"开始: {e['task_name']}"))
skill.on_event("task_completed", lambda e: print(f"完成: {e['task_name']}"))
```

### Q: 如何处理网络超时？

A: 在注册机器人时设置超时：

```python
skill.register_robot("vansbot", "http://...", timeout=60)
```

## 🎓 学习资源

- 查看 `examples/simple_examples.py` 了解基础用法
- 查看 `examples/demo_coordination.py` 了解完整的协同任务
- 阅读源代码中的文档字符串
