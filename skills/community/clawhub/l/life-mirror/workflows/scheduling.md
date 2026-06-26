# Claw 定时任务与主动触达

## 初始化配置（必须执行）
- 每次执行前先读取 `core/config.yaml` 配置文件
- 根据配置设置所有可变参数（定时任务、推送配置等）

## 关键说明

### 技能启动时自动添加任务
- **执行时机**：技能启动时自动检查并添加必要的定时任务
- **检查逻辑**：若任务已存在则不再重复添加，若不存在则自动添加
- **必须添加的任务**：
  1. 每小时同步任务（从配置 `scheduling.hourly_task` 读取）
  2. 每周一报告任务（从配置 `scheduling.weekly_report_task` 读取）
  3. 月度报告任务（从配置 `scheduling.monthly_report_task` 读取）
  4. 每天更新用户画像任务（从配置 `scheduling.daily_profile_update` 读取）

### 自动推送到 Claw 绑定的通讯渠道
- **推送方式**：消息自动推送到 Claw 绑定的默认消息通讯渠道（如 QClaw 绑定了微信，就自动发送到微信）
- **自动目标**：消息自动发送给当前对话的用户

## 核心任务

### 1. 每小时同步任务
- **调度**：从配置 `scheduling.hourly_task` 读取，时区从配置 `scheduling.timezone` 读取
- **内容引用**：
  - **消息推送**：执行时引用 `content/push.md` 中的推送类型和推送原则
  - **待办提醒**：执行时引用 `content/todo.md` 中的待办提醒部分
- **推送上限**：从配置 `push.daily_limit` 读取
- **下限保障**：从配置 `push.daily_minimum` 读取
- **详细执行步骤**：详见下方「定时任务执行步骤」中的「每小时同步任务执行步骤」

### 2. 每周一报告任务
- **调度**：从配置 `scheduling.weekly_report_task` 读取，时区从配置 `scheduling.timezone` 读取
- **内容引用**：执行时引用 `content/reports.md` 中的周进展报告部分
- **详细执行步骤**：详见下方「定时任务执行步骤」中的「每周一报告任务执行步骤」

### 3. 月度报告任务
- **调度**：从配置 `scheduling.monthly_report_task` 读取，时区从配置 `scheduling.timezone` 读取
- **内容引用**：执行时引用 `content/reports.md` 中的月度报告部分
- **详细执行步骤**：详见下方「定时任务执行步骤」中的「月度报告任务执行步骤」

### 4. 每天更新用户画像任务
- **调度**：从配置 `scheduling.daily_profile_update` 读取，时区从配置 `scheduling.timezone` 读取
- **详细执行步骤**：详见下方「定时任务执行步骤」中的「每天更新用户画像任务执行步骤」

## 任务模板

### 每小时同步任务
```json
{
  "action": "add",
  "job": {
    "name": "life-mirror-hourly",
    "schedule": { "kind": "cron", "expr": "${scheduling.hourly_task}", "tz": "${scheduling.timezone}" },
    "sessionTarget": "isolated",
    "wakeMode": "now",
    "payload": {
      "kind": "agentTurn",
      "message": "执行 life-mirror：读已授权平台进行增量同步 → 基于新数据分析 → 值得则推送/入队；若当日主动触达仍偏少，可发一条短关心。",
      "deliver": true
    }
  }
}
```

### 每周一报告任务
```json
{
  "action": "add",
  "job": {
    "name": "life-mirror-weekly-report",
    "schedule": { "kind": "cron", "expr": "${scheduling.weekly_report_task}", "tz": "${scheduling.timezone}" },
    "sessionTarget": "isolated",
    "wakeMode": "now",
    "payload": {
      "kind": "agentTurn",
      "message": "生成并发送本周陪伴报告：上周目标完成度、情绪趋势、下周1-3个关键动作",
      "deliver": true
    }
  }
}
```

### 月度报告任务
```json
{
  "action": "add",
  "job": {
    "name": "life-mirror-monthly-report",
    "schedule": { "kind": "cron", "expr": "${scheduling.monthly_report_task}", "tz": "${scheduling.timezone}" },
    "sessionTarget": "isolated",
    "wakeMode": "now",
    "payload": {
      "kind": "agentTurn",
      "message": "生成并发送月度报告：消费分析、行车记录、月度目标完成度、下月重点关注。",
      "deliver": true
    }
  }
}
```

### 每天更新用户画像任务
```json
{
  "action": "add",
  "job": {
    "name": "life-mirror-daily-profile-update",
    "schedule": { "kind": "cron", "expr": "${scheduling.daily_profile_update}", "tz": "${scheduling.timezone}" },
    "sessionTarget": "isolated",
    "wakeMode": "now",
    "payload": {
      "kind": "agentTurn",
      "message": "执行 life-mirror：读取所有存储文件，归纳总结用户信息，更新 profile.json 文件，确保内容简洁便于后续使用。",
      "deliver": false
    }
  }
}
```

**说明**：模板中的 `${scheduling.hourly_task}` 等占位符需要从 `core/config.yaml` 配置文件中读取实际值。

## 通用规则
- 必须调用 `cron` 工具注册任务，不能只口头承诺
- 周期任务必须带时区，从配置 `scheduling.timezone` 读取
- `sessionTarget` 必须为 `"isolated"`
- 一次性任务用 `schedule.kind = "at"`；周期任务用 `schedule.kind = "cron"`

## 任务管理
1. 查询：`{ "action": "list" }`
2. 删除：先 `list` 拿 `jobId`，再 `{"action":"remove","jobId":"..."}`
3. 修改：删除后重建（remove -> add）

## 主动沟通策略
- **频率**：每天至少主动沟通从配置 `push.daily_minimum` 读取的次数，每日上限从配置 `push.daily_limit` 读取
- **时间窗口**：深夜（从配置 `push.quiet_hours` 读取）不主动打扰
- **触发逻辑**：每小时增量同步后检查高价值更新（目标变化、情绪波动、求职/兴趣行为显著变化）
- **内容规则**：必须引用历史上下文，每条消息包含一个"最小下一步"
- **去重规则**：同一主题 24 小时内不重复推送
- **优先级**：紧急提醒 > 周期性报告 > 高价值内容 > 一般性洞察

## 推送时机策略
- **作息识别**：平台活跃时间、消息阅读时间、任务完成时间
- **典型时段**：
  - 早晨通勤（07:30-09:00）：轻量内容
  - 午休（12:00-13:30）：中等深度内容
  - 睡前浏览（21:00-23:00）：深度内容
- **策略**：冷启动后 3-7 天收集数据，动态调整，支持用户设置偏好时段

## 定时任务执行步骤

### 通用执行步骤
1. **读取配置和存储**：
   - 加载 `core/config.yaml` 配置文件
   - 读取存储目录下的所有文件

2. **执行特定任务**：
   - 根据任务类型执行相应的操作

3. **记录状态**：
   - 记录任务执行状态和时间戳

### 每小时同步任务执行步骤
1. **执行平台同步**：
   - 对已授权平台做增量同步，优先使用edge浏览器
   - 若拉起平台失败，可跳过该平台，继续处理其他平台
   - 记录同步状态到 `platform_sync_state.json`

2. **分析数据**：
   - 基于新数据判断是否值得联系用户
   - 即使没有变化也要满足一天最小发送次数（从配置 `push.daily_minimum` 读取）
   - 检查是否在深夜时段（从配置 `push.quiet_hours` 读取）

3. **生成内容**：
   - 若需要推送，根据场景生成相应内容：
     - 消息推送：遵照 `content/push.md`，**优先寻找用户感兴趣的内容**
     - 待办提醒：遵照 `content/todo.md`
     - **注意**：只发送最后生成的内容（如用户感兴趣的资讯、待办提醒等），不要发送同步了多少信息等分析过程内容
     - 如果已授权平台的信息获取不到，可以作为非关键信息适当告知用户

4. **发送或入队**：
   - 若在深夜时段，将消息入队，不直接发送
   - 若不在深夜时段，直接发送消息
   - 记录发送状态

### 每周一报告任务执行步骤
1. **生成周报告**：
   - 基于本周数据生成周进展报告
   - 参考 `content/reports.md` 中的周进展报告部分内容进行生成

2. **发送报告**：
   - 直接发送周进展报告给用户
   - 记录发送状态

### 月度报告任务执行步骤
1. **生成月度报告**：
   - 基于本月数据生成月度报告
   - 参照 `content/reports.md` 中的月度报告部分内容进行生成

2. **发送报告**：
   - 直接发送月度报告给用户
   - 记录发送状态

### 每天更新用户画像任务执行步骤
1. **读取所有存储文件**：
   - 读取 `memory_facts.jsonl`、`memory_inferences.jsonl`、`todos.jsonl` 等文件
   - 分析用户的行为模式、偏好和状态

2. **归纳总结**：
   - 基于所有存储的信息，归纳总结用户的基本信息、偏好、行为模式等
   - 确保内容简洁，只保留关键信息，避免文件过大
   - 提取用户的核心特征和最近的行为趋势

3. **更新 profile.json**：
   - 将归纳总结的信息写入 `profile.json` 文件
   - 确保文件大小适中，便于每次回答时快速读取
   - 保持 profile.json 的结构清晰，便于解析

4. **记录更新时间**：
   - 在 `profile.json` 中记录本次更新的时间戳
   - 确保时间戳格式统一，便于后续查询

5. **不发送通知**：
   - 此任务仅更新文件，不向用户发送通知
   - 确保任务执行过程中不会打扰用户
