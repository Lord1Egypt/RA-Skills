# 小红书自动化养号 Skill — 需求设计文档

> **版本**: v0.1 Draft (SKILL.md 已升级至 v1.1)  
> **运行环境**: OpenClaw (Claude in Chrome 工具链)  
> **多模型兼容**: Claude / GPT-4o / Gemini / DeepSeek（通过 OpenClaw 统一调度）  
> **核心原则**: 纯浏览器 DOM 操作，不使用 Headless 浏览器、MCP 工具或 API 逆向调用

---

## 一、产品定位

在用户已登录的小红书 Web 会话内，模拟真人浏览与互动行为，自动执行**点赞、收藏、关注、评论**四类动作，通过自然互动吸引目标用户回访、完成引流养号目的。

**与现有 skill 的关系**：
- `xiaohongshu-ops-yj` → 内容创作与发布（生产侧）
- `xhs-creator-copilot` → 本地文案辅助（创作侧）
- **本 skill `xhs-nurture`** → 互动养号与引流（流量侧）

---

## 二、核心功能模块

### 2.1 互动动作引擎

| 动作类型 | 操作方式 | 风控要点 |
|---------|---------|---------|
| **点赞** | 定位心形按钮 → 模拟点击 | 单帖停留 3-15s 后再点赞，不连续秒赞 |
| **收藏** | 定位收藏按钮 → 模拟点击 | 收藏频率低于点赞 (约 1:3~1:5 比例) |
| **关注** | 进入用户主页 → 点击关注 | 每日关注数严格限制（≤30），间隔 ≥ 60s |
| **评论** | 打开评论框 → 输入文本 → 发送 | AI 生成个性化评论，逐字输入模拟打字节奏 |

### 2.2 浏览模拟引擎

| 行为 | 模拟策略 |
|------|---------|
| 页面滚动 | 变速滚动 + 随机停顿（高斯分布），模拟阅读节奏 |
| 停留时长 | 短内容 5-15s，长图文 15-45s，视频按时长 ×0.6~1.0 |
| 滑动方向 | 偶尔回滚（10%概率），模拟反复查看 |
| 页面切换 | Tab 间随机切换，偶尔访问非目标页面（搜索、个人主页） |

### 2.3 内容过滤器

```yaml
filters:
  # 目标笔记筛选
  note:
    min_likes: 100          # 最低点赞数
    max_likes: 50000        # 过滤头部大号（互动无效）
    keywords_include: ["期货", "交易", "投资"]  # 必须包含关键词
    keywords_exclude: ["广告", "代理"]          # 排除关键词
    note_type: ["image_text", "video"]         # 笔记类型
    publish_within_days: 7                     # 仅互动近7天内容

  # 目标用户筛选
  user:
    min_followers: 100
    max_followers: 100000
    min_notes: 5            # 过滤空号
    has_recent_post: true   # 近30天有更新
    is_verified: null       # 不限认证状态
```

### 2.4 速率控制系统

```yaml
rate_control:
  # 每日上限（硬限制，到达即停止）
  daily_limits:
    likes: 120
    collects: 30
    follows: 25
    comments: 15
    total_actions: 150      # 总动作数上限

  # 单次会话控制
  session:
    max_duration_minutes: 45      # 单次运行最长时间
    min_interval_seconds: 8       # 动作最小间隔
    max_interval_seconds: 60      # 动作最大间隔
    cooldown_after_actions: 20    # 每 N 个动作后休息
    cooldown_duration: [120, 300] # 休息时长范围(秒)

  # 抖动（Jitter）配置
  jitter:
    type: "gaussian"              # gaussian | uniform | poisson
    factor: 0.3                   # 抖动系数 (±30%)
    burst_prevention: true        # 防止短时间内连续动作
```

### 2.5 AI 评论生成模块

```yaml
comment_generation:
  # 多模型支持（通过 OpenClaw 路由）
  model_priority: ["deepseek-chat", "gpt-4o-mini", "claude-haiku"]
  
  # 评论风格配置
  style:
    tone: "casual"                # casual | professional | humorous
    max_length: 50                # 字符上限
    use_emoji: true               # 是否使用 emoji
    emoji_frequency: 0.3          # emoji 出现概率
    
  # 评论模板（当 AI 不可用时的降级方案）
  fallback_templates:
    - "写得好棒！学到了{emoji}"
    - "感谢分享，收藏了{emoji}"
    - "这个角度很独特，期待更多内容"
    
  # 安全策略
  safety:
    no_sensitive_words: true      # 过滤敏感词
    no_marketing_links: true      # 禁止留链接
    no_contact_info: true         # 禁止留联系方式
    diversity_check: true         # 避免重复评论
```

---

## 三、反检测策略（核心风控层）

### 3.1 行为指纹伪装

| 维度 | 策略 |
|------|------|
| **鼠标轨迹** | 贝塞尔曲线移动 + 微颤抖，非直线路径到达目标 |
| **点击坐标** | 按钮区域内随机偏移 ±3px，不总是点击中心 |
| **打字节奏** | 字符间隔 80-200ms（高斯分布），偶尔停顿/删除重打 |
| **滚动行为** | 非匀速，模拟惯性滚动 + 手指抬起减速 |
| **操作时段** | 仅在自然活跃时间段运行（9:00-23:00），避免凌晨 |
| **设备一致性** | 复用登录会话的 UA/分辨率，不修改浏览器指纹 |

### 3.2 频率控制规则

```
规则 1: 相邻两次点赞间隔 ≥ 8s (+ jitter)
规则 2: 连续点赞不超过 5 次，之后必须有浏览行为
规则 3: 每 20 个动作后强制休息 2-5 分钟
规则 4: 评论后必须等待 ≥ 90s 再执行下一动作
规则 5: 关注后必须浏览该用户 1-3 条笔记
规则 6: 单日首次启动前随机延迟 1-10 分钟
规则 7: 异常检测（验证码/登录弹窗）→ 立即暂停 + 通知用户
```

### 3.3 会话健康度监控

```yaml
health_monitor:
  checks:
    - type: "login_state"         # 登录态检测
      interval: 60s
      action_on_fail: "pause_and_notify"
      
    - type: "captcha_detection"   # 验证码检测
      trigger: "before_each_action"
      action_on_fail: "stop_immediately"
      
    - type: "rate_limit_signal"   # 频率限制信号(操作失败/按钮灰色)
      action_on_fail: "exponential_backoff"
      
    - type: "page_anomaly"        # 页面异常(空白/错误页)
      action_on_fail: "retry_3_then_stop"
```

---

## 四、工作流程设计

### 4.1 主流程（状态机）

```
[初始化] → [登录态验证] → [加载配置] → [选择任务路径]
                                              ↓
                    ┌─────────────────────────────────────┐
                    ↓                    ↓                ↓
            [发现页互动]         [搜索页互动]       [用户主页互动]
                    ↓                    ↓                ↓
            [内容过滤]           [内容过滤]         [用户过滤]
                    ↓                    ↓                ↓
            [执行互动动作]       [执行互动动作]     [执行互动动作]
                    ↓                    ↓                ↓
                    └─────────────────────────────────────┘
                                        ↓
                    [日志记录] → [限额检查] → [继续/暂停/结束]
```

### 4.2 任务路径

| 路径 | 入口 | 适用场景 |
|------|------|---------|
| **发现页模式** | 首页推荐流 | 广泛互动，提升账号活跃度 |
| **搜索页模式** | 按关键词搜索结果 | 精准定位目标赛道内容 |
| **用户主页模式** | 指定用户/竞品列表 | 互动竞品粉丝，精准引流 |
| **评论区模式** | 热门帖子评论区 | 在高曝光位置留下评论吸引关注 |

### 4.3 会话生命周期

```
启动 → 预热(随机浏览 2-5 分钟，不执行动作)
     → 正式互动(按配置执行动作)
     → 中场休息(每 15-20 分钟休息 3-8 分钟)
     → 收尾(减速 + 纯浏览 1-3 分钟)
     → 结束(输出统计报告)
```

---

## 五、配置体系

### 5.1 用户配置文件 (`nurture-config.yaml`)

```yaml
# 账号信息
account:
  nickname: "不期而遇"
  category: "期货/财经"
  stage: "nurturing"         # nurturing(养号期) | growth(增长期) | mature(成熟期)

# 目标定义
targets:
  keywords: ["期货入门", "交易心得", "投资理财"]
  competitor_accounts: ["@用户A", "@用户B"]
  hashtags: ["#期货", "#投资"]

# 互动策略（按阶段调整）
strategy:
  nurturing:                 # 养号期：保守策略
    daily_likes: 60
    daily_collects: 15
    daily_follows: 10
    daily_comments: 5
    session_duration: 30
    
  growth:                    # 增长期：积极策略
    daily_likes: 120
    daily_collects: 30
    daily_follows: 25
    daily_comments: 15
    session_duration: 45

# 运行计划
schedule:
  active_hours: ["09:00-11:30", "14:00-16:00", "20:00-22:30"]
  days_of_week: ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
  sessions_per_day: 2
```

### 5.2 运行时状态文件 (`nurture-state.json`)

```json
{
  "date": "2026-05-16",
  "session_id": "sess_20260516_1",
  "counters": {
    "likes": 42,
    "collects": 12,
    "follows": 8,
    "comments": 3,
    "total": 65
  },
  "last_action_time": "2026-05-16T14:32:15",
  "status": "running",
  "errors": [],
  "interacted_notes": ["note_id_1", "note_id_2"],
  "interacted_users": ["user_id_1"]
}
```

---

## 六、多模型兼容架构

### 6.1 OpenClaw 统一调度

```
┌─────────────────────────────────────────┐
│           OpenClaw Runtime               │
├─────────────────────────────────────────┤
│  Model Router (按任务分发)               │
│  ┌──────────┐ ┌──────────┐ ┌─────────┐ │
│  │ Claude   │ │ GPT-4o   │ │DeepSeek │ │
│  │(决策/规划)│ │(评论生成) │ │(评论生成)│ │
│  └──────────┘ └──────────┘ └─────────┘ │
├─────────────────────────────────────────┤
│  Browser Tool Layer (统一接口)           │
│  navigate | find | read_page | computer │
│  javascript_tool | form_input           │
├─────────────────────────────────────────┤
│  Chrome Browser (用户已登录会话)          │
└─────────────────────────────────────────┘
```

### 6.2 模型任务分工

| 任务 | 首选模型 | 降级模型 | 说明 |
|------|---------|---------|------|
| 流程控制/决策 | Claude | GPT-4o | 解析页面状态、决定下一步动作 |
| 评论生成 | DeepSeek | GPT-4o-mini | 低成本、高质量中文生成 |
| 内容理解/过滤 | Claude | GPT-4o | 判断笔记是否符合目标 |
| 异常处理 | Claude | — | 识别验证码/弹窗/异常状态 |

### 6.3 工具调用标准化

所有浏览器操作统一通过以下工具完成（OpenClaw 环境）：

```
- navigate(url)              → 页面导航
- find(query)                → 自然语言元素定位
- read_page(filter)          → 读取页面结构
- computer(action, ...)      → 鼠标/键盘操作
- javascript_tool(code)      → DOM 状态读取
- form_input(ref, value)     → 表单填写
```

---

## 七、日志与数据

### 7.1 操作日志

```
data/nurture-log/
├── 2026-05-16.jsonl         # 每日操作明细
├── stats-weekly.json        # 周统计
└── stats-monthly.json       # 月统计
```

每条日志格式：
```json
{
  "ts": "2026-05-16T14:32:15.123Z",
  "action": "like",
  "target_note_id": "xxx",
  "target_user": "xxx",
  "success": true,
  "duration_ms": 1200,
  "context": "discover_feed"
}
```

### 7.2 效果追踪指标

| 指标 | 说明 |
|------|------|
| 互动回访率 | 被互动用户回访我方主页的比例 |
| 新增粉丝/日 | 每日净增粉丝数 |
| 笔记曝光提升 | 互动后自身笔记的曝光变化 |
| 账号权重信号 | 搜索排名、推荐流出现频率 |

---

## 八、安全与合规

### 8.1 红线规则（不可突破）

1. **不使用 Headless 浏览器** — 仅在用户可见的 Chrome 窗口中操作
2. **不调用小红书私有 API** — 仅通过 DOM 交互
3. **不修改浏览器指纹** — 不注入 Canvas/WebGL/UA 伪装代码
4. **不突破平台限额** — 各动作日限额低于平台已知阈值的 60%
5. **不发送营销内容** — 评论中不包含链接、二维码、联系方式
6. **不存储他人隐私** — 不保存其他用户的个人信息

### 8.2 风险分级与响应

| 风险信号 | 级别 | 响应 |
|---------|------|------|
| 操作按钮无响应 | Low | 等待 30s 重试 |
| 操作后出现 Toast 警告 | Medium | 暂停 5 分钟 |
| 出现滑块验证码 | High | 立即停止，通知用户 |
| 账号被登出 | Critical | 终止所有操作，保存状态 |
| 页面出现违规提示 | Critical | 终止 + 通知 + 建议 24h 不操作 |

---

## 九、Skill 文件结构

```
xhs-nurture/
├── SKILL.md                    # Skill 主入口（OpenClaw 加载）
├── DESIGN.md                   # 本设计文档
├── CHANGELOG.md
├── references/
│   ├── interaction-engine.md   # 互动引擎详细逻辑
│   ├── anti-detection.md       # 反检测策略细则
│   ├── comment-generation.md   # AI评论生成规范
│   ├── rate-control.md         # 速率控制算法
│   ├── filters.md              # 过滤器配置规范
│   ├── multi-account.md        # 多账号切换逻辑
│   ├── scheduler.md            # 定时调度规范
│   └── dashboard.md            # 数据看板规范
├── config/
│   ├── nurture-config.yaml     # 默认配置模板
│   ├── schedule.yaml           # 定时任务配置
│   └── profiles/               # 多账号配置
│       ├── default.yaml
│       └── ...
├── data/
│   ├── nurture-log/            # 运行日志 (*.jsonl)
│   └── reports/                # 可视化报告 (*.html)
└── templates/
    ├── comments/               # 评论模板库
    │   ├── casual.yaml
    │   ├── professional.yaml
    │   └── humorous.yaml
    └── dashboard/              # 报告 HTML 模板
        └── base.html
```

---

## 十、实现优先级（里程碑）

| 阶段 | 功能 | 预计工作量 |
|------|------|-----------|
| **M1** | 登录态检测 + 发现页浏览模拟 + 点赞 | 2天 |
| **M2** | 收藏 + 关注 + 速率控制 + 日志 | 2天 |
| **M3** | AI评论生成 + 多模型路由 | 2天 |
| **M4** | 搜索页/用户主页模式 + 过滤器 | 2天 |
| **M5** | 反检测加固 + 异常处理 + 健康监控 | 2天 |
| **M6** | 多账号切换 + 账号 Profile 管理 | 2天 |
| **M7** | 定时调度（OpenClaw cron 集成） | 1天 |
| **M8** | 数据看板（HTML 可视化报告） | 2天 |

---

## 十一、与 yanghao.app 的差异化

| 维度 | yanghao.app | 本 Skill |
|------|-------------|---------|
| 形态 | Chrome 扩展（固定逻辑） | AI Skill（智能决策） |
| 评论能力 | 模板或简单 AI | 多模型路由，上下文感知评论 |
| 过滤精度 | 基础阈值 | 语义理解 + 多维过滤 |
| 策略适应 | 手动调参 | 按账号阶段自动调整 |
| 扩展性 | 封闭 | 开放配置，可组合其他 Skill |
| 异常处理 | 简单暂停 | 分级响应 + 用户通知 |

---

## 十二、已确认决策

| # | 问题 | 决策 | 备注 |
|---|------|------|------|
| 1 | 多账号切换 | **纳入** (M6) | 同一浏览器内切换已登录账号，通过 profiles/ 管理 |
| 2 | 定时调度 | **纳入** (M7) | 集成 OpenClaw cron，支持无人值守定时运行 |
| 3 | 数据看板 | **纳入** (M8) | HTML 可视化报告，展示互动效果趋势 |
| 4 | 与发布 Skill 联动 | **不做** | 互动与发布解耦，各自独立运行 |
| 5 | 私信功能 | **不做** | 风险过高，不纳入范围 |

---

## 十三、多账号切换设计（M6）

### 账号 Profile 体系

```
config/profiles/
├── default.yaml           # 默认账号（不期而遇）
├── account-2.yaml         # 第二个账号
└── account-3.yaml         # 第三个账号
```

每个 Profile 包含：
```yaml
profile:
  name: "不期而遇"
  category: "期货/财经"
  stage: "growth"
  
  # 账号专属互动策略（覆盖全局配置）
  strategy_override:
    daily_likes: 80
    keywords: ["期货", "原油"]
    
  # 切换方式
  switch_method: "cookie_session"   # cookie_session | logout_login
  session_indicator: "nickname_text" # 用于确认当前登录账号的页面元素
```

### 切换流程

```
[读取目标 Profile] → [检查当前登录账号]
    ↓ (不一致)
[导航到个人页/设置页] → [确认当前用户身份]
    ↓
[切换账号（点击头像→切换账号）] → [验证切换成功]
    ↓
[加载该账号的配置] → [开始执行互动任务]
```

### 安全约束
- 切换前保存当前账号状态
- 切换失败不强制重试，通知用户手动介入
- 每个账号独立的日限额计数器
- 多账号间互动目标去重（避免同一笔记被多账号互动）

---

## 十四、定时调度设计（M7）

### OpenClaw Cron 集成

```yaml
schedule:
  # 每日运行计划
  plans:
    - name: "morning_session"
      cron: "30 9 * * *"           # 每天 9:30
      account: "default"
      mode: "discover_feed"
      duration: 30
      
    - name: "afternoon_session"
      cron: "0 14 * * 1-5"        # 工作日 14:00
      account: "default"
      mode: "search"
      duration: 25
      
    - name: "evening_session"
      cron: "30 20 * * *"         # 每天 20:30
      account: "default"
      mode: "user_profile"
      duration: 40

  # 调度抖动（避免固定时间启动）
  start_jitter_minutes: 10         # 实际启动时间 ±10 分钟随机

  # 健康检查
  pre_check:
    - browser_open: true
    - login_valid: true
    - daily_limit_not_reached: true
```

### 调度生命周期

```
[Cron 触发] → [启动前检查(浏览器/登录态/限额)]
    ↓ (通过)                    ↓ (失败)
[随机延迟 0-10min]           [记录失败 + 通知用户]
    ↓
[启动互动会话]
    ↓
[正常执行/异常中断]
    ↓
[写入日志 + 更新状态]
```

---

## 十五、数据看板设计（M8）

### 报告内容

```
data/reports/
├── daily-2026-05-16.html    # 每日报告
├── weekly-2026-W20.html     # 周报
└── dashboard.html           # 总览面板（实时更新）
```

### 可视化指标

| 板块 | 图表类型 | 指标 |
|------|---------|------|
| **今日概览** | 数字卡片 | 点赞/收藏/关注/评论计数 + 完成率 |
| **趋势图** | 折线图 | 近 7/30 天每日互动量变化 |
| **效果追踪** | 柱状图 | 互动回访率、新增粉丝/日 |
| **时段分布** | 热力图 | 各时段互动密度（检查是否自然） |
| **账号健康** | 仪表盘 | 风控信号次数、成功率、异常率 |
| **目标达成** | 进度条 | 按阶段目标的完成进度 |

### 技术方案
- 纯静态 HTML + 内嵌 Chart.js（无服务端依赖）
- 数据源：读取 `data/nurture-log/*.jsonl` 聚合生成
- 每次会话结束后自动更新报告
- 支持用户通过浏览器直接打开查看
