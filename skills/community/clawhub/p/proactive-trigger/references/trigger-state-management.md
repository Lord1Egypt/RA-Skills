# 触发状态管理 - 详细数据结构与规则

## 整体状态结构

```json
{
  "date": "2026-04-01",
  "version": "1.0",
  
  // 每日限制
  "daily_limits": {
    "max_triggers": 6,
    "used_today": 2,
    "remaining": 4,
    "reset_time": "2026-04-02T00:00:00+08:00"
  },
  
  // 时间窗口管理
  "time_windows": {
    "morning": {"start": "07:00", "end": "09:00", "enabled": true},
    "work_morning": {"start": "09:00", "end": "12:00", "enabled": true},
    "lunch": {"start": "12:00", "end": "14:00", "enabled": true, "intensity": "low"},
    "work_afternoon": {"start": "14:00", "end": "18:00", "enabled": true},
    "evening": {"start": "18:00", "end": "22:00", "enabled": true},
    "night": {"start": "22:00", "end": "07:00", "enabled": false}
  },
  
  // 话题注册表
  "topic_registry": {
    "供应链优化": {
      "state": "活跃",
      "category": "工作",
      "mentions": 5,
      "recent_mentions": [
        {"time": "2026-04-01T09:30:00", "context": "讨论供应链优化方案"},
        {"time": "2026-04-01T08:15:00", "context": "询问供应链工具"}
      ],
      "last_at": "2026-04-01T09:30:00",
      "first_at": "2026-03-20T00:00:00",
      "heat_score": 0.85,
      "pings_today": 0,
      "last_ping": null,
      "ping_cooldown": null,
      "user_interest": 0.9,
      "priority": 8
    }
  },
  
  // 触发历史
  "trigger_history": [
    {
      "id": "trigger_001",
      "timestamp": "2026-04-01T10:00:00+08:00",
      "type": "topic_pulse",
      "topic": "供应链优化",
      "message": "看你最近在研究供应链优化，这是昨天讨论的延续。有新进展吗？",
      "silence_index": 0.6,
      "topic_heat": 0.85,
      "trigger_score": 0.9,
      "user_response": "accepted",
      "response_time": 300  // 秒
    }
  ],
  
  // 冷却期管理
  "cooldowns": {
    "global": "2026-04-01T12:00:00+08:00",
    "by_type": {
      "topic_pulse": "2026-04-01T11:30:00+08:00",
      "health_guardian": "2026-04-01T14:00:00+08:00"
    },
    "by_topic": {
      "供应链优化": "2026-04-01T13:00:00+08:00"
    }
  },
  
  // 用户反馈学习
  "learning": {
    "acceptance_rates": {
      "topic_pulse": 0.75,
      "health_guardian": 0.9,
      "daily_summary": 0.85,
      "quiet_care": 0.6
    },
    "rejection_streaks": {
      "topic_pulse": 0,
      "health_guardian": 0
    },
    "preferred_times": ["09:00-11:00", "20:00-22:00"],
    "avoided_topics": ["熬夜工作", "过度加班"]
  },
  
  // 系统状态
  "system_state": {
    "focus_mode": false,
    "last_active": "2026-04-01T10:00:00+08:00",
    "silence_index": 0.6,
    "daily_summary_done": false,
    "last_daily_summary": null,
    "health_reminder_done": false
  }
}
```

## 状态字段详细说明

### 每日限制 (daily_limits)

| 字段 | 类型 | 说明 | 默认值 |
|------|------|------|-------|
| max_triggers | integer | 每日最大触发次数 | 6 |
| used_today | integer | 今日已使用次数 | 0 |
| remaining | integer | 剩余次数 | max_triggers |
| reset_time | string | 重置时间（ISO格式） | 次日00:00 |

### 时间窗口 (time_windows)

每个时间窗口包含：

| 字段 | 类型 | 说明 |
|------|------|------|
| start | string | 开始时间（HH:MM） |
| end | string | 结束时间（HH:MM） |
| enabled | boolean | 是否启用 |
| intensity | string | 强度级别（high/medium/low/minimal） |
| allowed_types | array | 允许的触发类型 |

**强度级别定义：**
- high: 可触发所有类型
- medium: 仅触发重要类型
- low: 仅触发关怀类型  
- minimal: 仅紧急触发

### 话题注册表条目 (topic_registry entry)

| 字段 | 类型 | 说明 |
|------|------|------|
| state | string | 状态（活跃/浮现/休眠） |
| category | string | 分类（工作/健康/家庭/兴趣） |
| mentions | integer | 累计提及次数 |
| recent_mentions | array | 最近提及记录 |
| last_at | string | 最后提及时间 |
| first_at | string | 首次提及时间 |
| heat_score | float | 热度评分（0-1） |
| pings_today | integer | 今日触发次数 |
| last_ping | string/null | 上次触发时间 |
| ping_cooldown | string/null | 触发冷却到期时间 |
| user_interest | float | 用户兴趣度（0-1） |
| priority | integer | 优先级（1-10） |

### 触发历史条目 (trigger_history entry)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | string | 唯一标识符 |
| timestamp | string | 触发时间 |
| type | string | 触发类型 |
| topic | string | 相关话题 |
| message | string | 触发消息（前50字符） |
| silence_index | float | 沉默指数 |
| topic_heat | float | 话题热度 |
| trigger_score | float | 综合触发评分 |
| user_response | string | 用户响应（accepted/ignored/rejected） |
| response_time | integer | 响应时间（秒，null表示无响应） |

## 状态转换规则

### 每日重置

```
每日00:00自动执行：
1. used_today = 0
2. remaining = max_triggers
3. 所有话题的pings_today = 0
4. daily_summary_done = false
5. health_reminder_done = false
```

### 话题状态转换

#### 活跃 → 浮现
条件：最后提及时间 > 3天
动作：state = "浮现", heat_score ×= 0.7

#### 浮现 → 休眠
条件：最后提及时间 > 7天  
动作：state = "休眠", heat_score = 0.1

#### 休眠 → 浮现
条件：用户主动提及
动作：state = "浮现", heat_score = 0.3

#### 浮现 → 活跃
条件：累计提及次数 ≥ 3 且 heat_score ≥ 0.7
动作：state = "活跃"

### 冷却期管理

#### 全局冷却
- 每次触发后：全局冷却2小时
- 冷却期间：只允许urgency ≥ 1.5的触发

#### 类型冷却
- topic_pulse: 冷却1小时
- health_guardian: 冷却4小时  
- daily_summary: 冷却24小时（每天一次）
- quiet_care: 冷却3小时

#### 话题冷却
- 同一话题：冷却1小时
- 相似话题（同category）：冷却30分钟

## 安全检查规则

### Pre-Trigger检查清单

每次触发前必须通过所有检查：

1. **时间窗口检查**
   - 当前时间在enabled的时间窗口内
   - 当前窗口的intensity允许该触发类型

2. **次数限制检查**
   - used_today < max_triggers
   - 该话题的pings_today < 1（同一话题每天最多1次）

3. **冷却期检查**
   - 全局冷却已过期
   - 该触发类型的冷却已过期
   - 该话题的冷却已过期

4. **系统状态检查**
   - focus_mode = false
   - 用户非明确忙碌状态
   - 用户非深度休息状态（从mood-simulator获取）

5. **价值检查**
   - 触发不与用户核心价值冲突（从value-aware-guard验证）
   - 话题不在avoided_topics列表中

### 检查失败处理

| 检查项 | 失败动作 | 重试时间 |
|--------|---------|---------|
| 时间窗口 | 等待到下一个窗口 | 窗口开始时间 |
| 次数限制 | 等待次日重置 | 次日00:00 |
| 冷却期 | 等待冷却到期 | 冷却到期时间 |
| 系统状态 | 等待状态改变 | 定期检查（15分钟） |
| 价值冲突 | 放弃触发 | 不重试 |

## 数据持久化与恢复

### 存储位置
```
~/.openclaw/workspace/.soul/trigger-state.json
```

### 自动保存
- 每次状态变更后保存
- 至少每15分钟保存一次

### 恢复机制
- 启动时加载最新状态
- 如果文件损坏：从trigger_history重建基础状态
- 如果无历史：使用默认状态

## 监控与调试

### 状态健康检查

每日执行健康检查：
1. 检查各字段数据类型
2. 验证时间窗口逻辑
3. 分析触发成功率
4. 识别异常模式

### 调试信息

触发时可选的调试输出：

```json
{
  "debug_info": {
    "checks_passed": ["time_window", "daily_limit", "cooldown"],
    "checks_failed": [],
    "calculated_values": {
      "silence_index": 0.6,
      "topic_heat": 0.85,
      "urgency": 1.0,
      "context_relevance": 0.9,
      "final_score": 0.9
    },
    "decision_reason": "score_above_threshold",
    "alternative_options": [
      {"type": "quiet_care", "score": 0.7, "reason": "lower_urgency"}
    ]
  }
}
```
