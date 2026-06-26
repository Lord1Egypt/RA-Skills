# OpenClaw 能力矩阵

判断工作流子流程是否可用 OpenClaw 实现时，参考此文档。

## 目录

- [一、开箱即用能力](#一开箱即用能力)
- [二、需要配置 + 写 Skill 的能力](#二需要配置--写-skill-的能力)
- [三、需要开发 Plugin 的能力](#三需要开发-plugin-的能力)
- [四、不适合 / 无法实现的场景](#四openclaw-不适合--无法实现的场景)
- [五、实际案例参考](#五实际案例参考来自社区-showcase)

## 一、开箱即用能力（⭐~⭐⭐）

这些能力 OpenClaw 原生支持，无需额外开发：

### 消息与通知
- 跨平台消息收发（Telegram、Discord、Slack、WhatsApp、Signal、iMessage、飞书、Matrix 等 20+ 平台）
- 消息转发（A 平台 → B 平台）
- 定时消息推送（Cron 调度：at/every/cron 表达式）
- 群聊/私聊管理

### 文件操作
- 本地文件读写（read/write/list）
- 文件搜索、内容提取
- 目录管理

### Shell 命令执行
- 执行本地 Shell 命令（需审批流）
- 调用本地已安装的 CLI 工具（git、curl、ffmpeg 等）

### 网络与搜索
- 网页搜索
- URL 内容抓取
- 浏览器自动化（Chrome）

### 记忆与上下文
- 长期记忆（MEMORY.md 策展层）
- 每日日志（memory/YYYY-MM-DD.md 自动追加）
- 语义搜索（向量 + BM25 混合检索）

### 多 Agent
- 创建独立 Agent（各自独立工作区/人格/工具/记忆）
- Agent 路由（按消息来源自动分配）

### 定时任务（Cron）
- 一次性定时（at）
- 循环执行（every/cron）
- 投递到指定通道
- 错误自动退避和禁用

### 原生客户端能力
- iOS：Share Extension、摄像头、录屏、语音唤醒、位置
- Android：通话记录、SMS
- macOS：AppleScript、Shell、系统通知

## 二、需要配置 + 写 Skill 的能力（⭐⭐~⭐⭐⭐）

需要编写 SKILL.md（声明式，无需编程），可能需要配置 API Key：

### 第三方 API 集成（通过 Skill 声明 + 工具调用）
- REST API 调用（需要目标服务提供 API）
- 日历集成（CalDAV）
- 智能家居控制（Home Assistant API）
- 任务管理（Todoist、Linear 等有 API 的服务）
- 代码仓库操作（GitHub/GitLab API）
- 邮件收发（通过 IMAP/SMTP 或 API）

### 内容处理
- 文本总结/翻译/改写（利用 LLM 能力）
- PDF/文档解析（通过 Shell 调用工具链）
- 图片生成（调用 DALL-E/Midjourney 等 API）
- 音频转录（调用 Whisper 等服务）

### 数据聚合
- 从多个源拉取数据并汇总
- RSS 订阅聚合
- 健康数据整合（Oura、Apple Health 等有 API 的设备）

### 浏览器自动化流程
- 网页登录 + 操作（无 API 时的替代方案）
- 截图 + 分析
- 表单填写、预订系统操作

## 三、需要开发 Plugin 的能力（⭐⭐⭐⭐~⭐⭐⭐⭐⭐）

需要 TypeScript 编程，使用 Plugin SDK 开发：

### 新通道接入
- 接入 OpenClaw 未内置的消息平台
- 自定义协议对接（WebSocket、MQTT 等）

### 自定义工具
- 需要复杂逻辑的工具（超出 Shell+API 调用范围）
- 需要持久化状态的工具
- 需要与 Gateway 深度交互的工具

### 高级扩展
- 自定义上下文引擎（Context Engine）
- 生命周期钩子（Hook）
- Webhook 入口
- 后台服务（Service）

## 四、OpenClaw 不适合 / 无法实现的场景

### 架构限制
- ❌ 多租户/企业级部署（单一可信运营者假设）
- ❌ 高并发场景（单进程架构）
- ❌ 需要外部数据库的场景（仅文件系统存储）

### 实时性要求
- ❌ 毫秒级实时响应（LLM 推理有延迟）
- ❌ 高频交易/实时监控告警（Cron 最短间隔有限）

### 安全与合规
- ❌ 处理高度敏感数据（无端到端加密保证）
- ❌ 需要审计合规的企业场景
- ❌ 需要细粒度权限控制的多用户场景

### 计算密集型
- ❌ 大规模数据处理（本地硬件限制）
- ❌ 模型训练/微调
- ❌ 视频/音频实时流处理

### 数据依赖
- ⚠️ 需要第三方数据但该服务无 API 且无法浏览器自动化的
- ⚠️ 需要付费 API 但用户无预算/账号的
- ⚠️ 数据在企业内网且无法从运行 OpenClaw 的机器访问的

## 五、实际案例参考（来自社区 Showcase）

| 场景 | 实现层 | 难度 | 说明 |
|------|--------|------|------|
| PR 评审 → Telegram 通知 | Skill | ⭐⭐ | GitHub API + Telegram 通道 |
| Tesco 超市购物自动化 | Skill（浏览器） | ⭐⭐⭐ | 无 API，纯浏览器操控 |
| 每日天气+任务可视化简报 | Skill + Cron | ⭐⭐ | 定时触发 + API 聚合 |
| 会计收据自动整理 | Skill | ⭐⭐ | 邮件 API + PDF 处理 |
| 职位搜索 + CV 匹配 | Skill | ⭐⭐⭐ | 招聘网站 API + LLM 分析 |
| TradingView 技术分析 | Skill（浏览器） | ⭐⭐⭐ | 登录 + 截图 + 分析 |
| Slack 自动客服 | Skill + Cron | ⭐⭐ | Slack 通道 + 自动回复 |
| Jira 集成 | Skill | ⭐⭐ | Jira REST API |
| 智能家居控制 | Plugin | ⭐⭐⭐⭐ | Home Assistant API |
| 3D 打印机控制 | Plugin | ⭐⭐⭐⭐ | 硬件协议对接 |
| 14+ Agent 编排系统 | Plugin | ⭐⭐⭐⭐⭐ | 多 Agent 协调 |
| WhatsApp 记忆库 | Skill | ⭐⭐⭐ | 导入 + 转录 + 向量索引 |
