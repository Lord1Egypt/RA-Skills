# 适配器修正说明

> **注意：** 本文档记录了内置适配器（Vansbot、PuppyPi）的历史修正。如果你是 OpenClaw Agent，需要接入新机器人，请参考 [SKILL.md](SKILL.md) 中的适配器生成模板。

## 修正日期
2026-03-05

## 修正内容

根据实际 API 文档进行了以下修正：

### 1. Vansbot 适配器 (vansbot_adapter.py)

#### 修正1：健康检查端点
- **问题**：使用了不存在的 `/status` 端点
- **修正**：改为 `/health` 端点
- **影响方法**：
  - `connect()` - 连接检查
  - `get_state()` - 状态获取

**修正前：**
```python
response = self.session.get(f"{self.endpoint}/status", timeout=5)
```

**修正后：**
```python
response = self.session.get(f"{self.endpoint}/health", timeout=5)
```

**API 文档参考：**
```
GET /health
响应：
{
  "status": "ok",
  "captured_at": "2026-01-26T10:30:00.000Z",
  "detections_available": true
}
```

### 2. PuppyPi 适配器 (puppypi_adapter.py)

#### 修正1：位置字段名称
- **问题**：API 返回的是 `pose` 字段，而不是 `position`
- **修正**：正确解析 `pose` 字段并转换为 `position` 格式
- **影响方法**：
  - `get_state()` - 状态获取

**修正前：**
```python
self._state.position = data.get("position")
```

**修正后：**
```python
pose = data.get("pose")
if pose:
    self._state.position = {
        "x": pose.get("x"),
        "y": pose.get("y"),
        "yaw": pose.get("yaw")
    }
```

**API 文档参考：**
```
GET /api/dogs/<dog_id>/status
响应：
{
  "id": 1,
  "name": "Dog1",
  "connected": true,
  "state": "MOVING",
  "pose": { "x": -1000, "y": 0, "yaw": 90 },
  "current_task": { ... }
}
```

## 验证清单

### Vansbot 适配器 ✅
- [x] `/health` 端点用于健康检查
- [x] `/capture` 端点用于检测物体
- [x] `/robot/move_to_object` 端点用于移动到物体
- [x] `/robot/grab` 端点用于抓取
- [x] `/robot/release` 端点用于释放
- [x] `/robot/move_to_place` 端点用于移动到预设位置
- [x] `/capture_for_finding_dog` 端点用于拍摄网格图
- [x] `/robot/release_to_dog` 端点用于放入篮筐

### PuppyPi 适配器 ✅
- [x] `/api/status` 端点用于系统状态
- [x] `/api/dogs/<dog_id>/status` 端点用于机器狗状态
- [x] `/api/task` 端点用于创建任务
- [x] `action: "move"` 用于移动
- [x] `action: "load"` 用于装货姿态
- [x] `action: "unload"` 用于卸货
- [x] `action: "posture"` 用于调整姿态
- [x] `pose` 字段正确解析

## 其他发现

### Vansbot API 特点
1. 所有机器人控制端点都在 `/robot/` 路径下
2. 健康检查使用 `/health` 而不是 `/status`
3. 响应格式统一为 `{"status": "ok"}` 或包含数据的 JSON

### PuppyPi API 特点
1. 所有端点都在 `/api/` 路径下
2. 任务创建统一使用 `/api/task` 端点，通过 `action` 字段区分动作类型
3. 机器狗状态返回 `pose` 对象，包含 `x`, `y`, `yaw` 字段
4. 需要在请求中指定 `dog_id` 来区分不同的机器狗

## 测试建议

### 测试 Vansbot 连接
```python
from multi_robot_skill import MultiRobotSkill

skill = MultiRobotSkill()
success = skill.register_robot("vansbot", "http://192.168.3.113:5000")
print(f"连接成功: {success}")

# 获取状态
status = skill.get_status()
print(status['robots']['vansbot'])
```

### 测试 PuppyPi 连接
```python
from multi_robot_skill import MultiRobotSkill

skill = MultiRobotSkill()
success = skill.register_robot("dog1", "http://localhost:8000", robot_type="puppypi", robot_id=1)
print(f"连接成功: {success}")

# 获取状态
status = skill.get_status()
print(status['robots']['dog1'])
```

## 影响评估

### 影响范围
- ✅ 修正后的适配器与实际 API 完全兼容
- ✅ 不影响 Skill 的其他部分
- ✅ 不影响任务规划和协调逻辑
- ✅ 示例代码无需修改

### 向后兼容性
- ✅ 接口签名未改变
- ✅ 返回值格式未改变
- ✅ 用户代码无需修改

## 总结

所有发现的问题已修正，适配器现在与实际 API 文档完全一致。修正主要集中在：
1. Vansbot 的健康检查端点
2. PuppyPi 的位置字段解析

这些修正确保了 Skill 能够正确地与实际的机器人系统通信。
