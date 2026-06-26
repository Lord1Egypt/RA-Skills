# 全功能版 Control Center 部署指南

> 真实 Control Center 项目（React + TypeScript + WebSocket），适合需要团队协作、多人查看、实时推送的高级用户。

## 项目信息

| 项目 | 信息 |
|------|------|
| GitHub | github.com/TianyiDataScience/openclaw-control-center |
| 技术栈 | TypeScript + React + WebSocket |
| 端口 | 4310 |
| 语言 | 双语（中/英） |

## 环境要求

- Node.js 22+
- npm 或 yarn
- git（用于 clone）
- OpenClaw Gateway 可连接

## 部署步骤（5分钟）

### 方式一：手动部署

```bash
# 1. 克隆项目
git clone https://github.com/TianyiDataScience/openclaw-control-center.git
cd openclaw-control-center

# 2. 安装依赖
npm install

# 3. 配置环境
cp .env.example .env

# 4. 构建
npm run build
npm run test
npm run smoke:ui

# 5. 启动
npm run dev:ui
```

Windows 推荐：
```bash
npm run dev:ui
```

### 方式二：让 AI 自动部署（推荐）

将以下指令粘贴给 OpenClaw：

```
帮我 clone 并启动 OpenClaw Control Center
仓库：https://github.com/TianyiDataScience/openclaw-control-center
端口：4310 / 中文界面
```

AI 会自动完成：环境探测 → 依赖安装 → 构建 → 启动

## 访问地址

| 语言 | 地址 |
|------|------|
| 中文 | `http://127.0.0.1:4310/?section=overview&lang=zh` |
| 英文 | `http://127.0.0.1:4310/?section=overview&lang=en` |

## 主要功能模块

### 1. 总览 Overview
一句话回答"OpenClaw 现在正常吗"，包含：
- 系统状态 / 活跃会话 / 异常任务 / 预算风险

### 2. 用量 Usage
- 今日/7天/30天平铺
- Token 消耗归因
- 上下文压力预警

### 3. 员工 Staff
- 真正在工作 vs 只是在排队中
- 区分：忙 / 闲 / 卡住

### 4. 协作 Collaboration
- 父子会话接力可视化
- Main ⇄ 子智能体通信追踪

### 5. 任务 Tasks
- 计划 vs 真实执行证据
- 审批链 / 卡点提示

### 6. 记忆 Memory
- 源文件驱动的记忆工作台
- 健康状态监测

### 7. 文档 Documents
- 源文件驱动的文档工作台
- 直接读写生效

### 8. 设置 Settings
- 接线状态
- 安全风险摘要
- 更新状态

## 安全默认值

| 安全项 | 默认值 | 说明 |
|--------|--------|------|
| READONLY_MODE | true | 只读模式 |
| APPROVAL_ACTIONS_ENABLED | false | 审批默认关闭 |
| APPROVAL_ACTIONS_DRY_RUN | true | 模拟运行 |
| IMPORT_MUTATION_ENABLED | false | 导入修改关闭 |

## 上下文压力监测

展示哪些会话接近上下文上限：

| 压力 | 颜色 | 建议 |
|------|------|------|
| > 70% | 🟡 黄色 | 预警 |
| > 90% | 🔴 红色 | 必须处理 |

## 团队使用建议

1. **个人使用**：用本技能（静态 HTML 版）即可，无需额外安装
2. **团队使用**：部署全功能版，多人共享同一控制台
3. **安全要求高**：保持 READONLY_MODE=true，仅允许查看

## 故障排查

| 问题 | 解决方案 |
|------|---------|
| 页面空白 | 检查 Gateway 是否运行在 28789 端口 |
| 数据不更新 | 刷新页面，WebSocket 会重连 |
| 401 Unauthorized | 检查 .env 中的 token 配置 |
| 端口被占用 | 改用其他端口：`PORT=4311 npm run dev:ui` |
