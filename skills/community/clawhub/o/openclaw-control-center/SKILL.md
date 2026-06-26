---
name: openclaw-control-center
description: OpenClaw 可视化控制中心。当用户需要查看系统状态、打开控制台、监控 AI 运行指标、管理定时任务/会话/技能，或需要可视化运营面板时触发。触发词：打开控制中心 / 控制中心 / dashboard / 系统总览 / 系统状态。
---

# openclaw-control-center

双模式可视化仪表盘 — 让 AI 的运行状态一目了然。

## 双模式说明

| 模式 | 触发 | 输出 |
|------|------|------|
| 🌿 简洁模式（默认） | 打开控制中心 | 大数字 + 说人话 + 说明提示 |
| 📊 专业模式 | 控制中心 --pro | 完整表格 + 架构图 + API 端点 |

两种模式均为**实时数据**，每次生成都从系统采集最新状态。

## 简洁模式 — 面向普通人

**核心三问，每问配通俗说明：**

- 🌟 **系统是否正常？** → ✓/⚠️/✕ + 状态列表
- 🧠 **AI 用了多少？** → Token 消耗 + 上下文进度条
- 👥 **谁在干活？** → 工作中/待命/空闲 三态

次要信息：定时任务 / 记忆系统 / 插件 / 安全设置（均附带通俗说明栏）

> 📌 Token 通俗解释：AI 的"阅读量"，越高 = 响应越慢 + 费用越高
> 📌 工作中=正在处理任务；待命=有任务但还没开始；空闲=没有活动

## 专业模式 — 面向技术人员

完整数据面板，详见 `references/pro-mode.md`：
- Token 7天趋势柱状图
- 会话管理完整表格（含 Session Key / Token / 通道）
- Cron Jobs 详细参数（含 Job ID / Payload / Timeout / Delivery）
- 插件表格（含类型 / 状态 / 说明 / 路径）
- 消息渠道（WebSocket 地址）
- 安全配置完整表格（5项默认安全策略）
- Gateway API 端点一览

## 执行流程

### Step 0 — 读取风格记忆

```
read("references/style-memory.md")   → 用户偏好 + 展示规范 + 禁忌
read("references/dashboard-rules.md") → 预警阈值 + 模式规则 + 数据采集规则
```

**必须遵守的风格规则：**
- 简洁 > 详细，说人话 > 术语（详见 `references/style-memory.md`）
- 上下文 >70% 黄色预警，>90% 红色闪烁（详见 `references/dashboard-rules.md`）
- 每个技术术语必须配通俗解释

### Step 1 — 采集实时数据（并行）

```
session_status()              → 系统 / 模型 / Token / 上下文
sessions_list()               → 全部会话
cron(action="list")           → 定时任务详情
gateway(action="config.get")   → Gateway / 插件 / 渠道
```

### Step 2 — 生成 HTML 仪表盘

生成 `~/.qclaw/workspace/control-center.html`，包含：
- 实时时间戳（采集时间）
- 简洁 + 专业两个模式（内置切换按钮）
- 所有数据以卡片/表格形式展示
- **风格记忆应用**：
  - 上下文压力根据阈值自动变色（绿/黄/红）
  - >90% 时进度条脉冲动画 + 红色警告块
  - 深色主题、圆角卡片、微光效果
  - 通俗解释提示框（hint）
  - 模式偏好 localStorage 持久化
  - 深夜时段（23:00-07:00）降低动画频率

### Step 3 — 浏览器打开

```
Start-Process control-center.html
```
默认显示简洁模式，用户可随时点击按钮切换。

## 参考文件

| 文件 | 用途 |
|------|------|
| `references/style-memory.md` | 用户偏好 + 写作风格 + 视觉规范 + 禁忌 |
| `references/dashboard-rules.md` | 展示规则 + 预警阈值 + 模式切换逻辑 |
| `references/pro-mode.md` | 专业模式完整数据定义 |
| `references/deployment.md` | 全功能版部署指南 |

## 全功能版（进阶用户）

如需 React + WebSocket 实时推送版，参看 `references/deployment.md`。

## 依赖

- OpenClaw 2026.3+（内置 session_status / sessions_list / cron / gateway / browser / exec）
- 浏览器（Chrome / Edge / Firefox）
- 无需 npm / Node.js / git（纯静态）

## 错误处理

- 工具调用失败：记录错误，继续生成其余部分
- 缺失数据：显示 "—" 而非报错
- 超时（>5s）：标记 "⚠️ 获取超时"
- 无浏览器权限：提示用户手动打开 HTML 文件
