# OpenClaw Skill: Lingxi Memory - 灵曦记忆系统

> 基于 OpenClaw + 飞书的 AI 记忆解决方案
> OpenClaw Agent 专用记忆系统

## 简介

Lingxi Memory（灵曦记忆系统）是一套专为 AI Agent 设计的记忆解决方案，结合飞书 IM 和飞书官方插件实现自动记忆功能。

### 核心特性

- 🤖 **自动提炼** - 会话结束自动触发 AI 提炼，无需手动操作
- 📊 **五层存储** - L1 原始会话 → L5 全局规则，结构化沉淀
- 🔄 **跨会话记忆** - 新会话可查看历史提炼报告
- 💾 **永久存储** - 飞书云端永久保存

### 技术栈

- [OpenClaw](https://github.com/openclaw/openclaw) - AI Agent 框架
- 飞书 IM - 消息推送
- 飞书多维表格 - 任务待办（L2）
- 飞书云文档 - 项目记忆（L3）、知识沉淀（L4）
- inotify-tools - 文件监听

---

## ⚠️ 数据安全说明

**在安装和使用本 Skill 前，请务必阅读以下内容：**

### 数据流向

```
本地 OpenClaw 会话文件 (.jsonl)
    ↓ 读取对话内容
AI 提炼（openclaw agent）
    ↓ 提取任务/项目/知识
飞书云端（L2/L3/L4）
    ↓ 推送提炼报告
飞书 IM（用户接收）
```

### 风险提示

1. **数据读取**：本 Skill 会读取本地 OpenClaw 会话文件，提取对话内容
2. **数据外传**：对话内容会被发送到飞书云端存储
3. **AI 处理**：对话内容会经过 OpenClaw AI 处理

### 适用场景

- ✅ 个人使用或内部团队使用
- ✅ 同意对话内容被存储到飞书的场景
- ❌ 对数据安全要求极高的场景
- ❌ 涉及敏感隐私信息的对话

---

## 系统架构

```
用户对话
    ↓
会话结束（.jsonl.reset 文件生成）
    ↓
session_watch.sh 监听检测
    ↓
do_extract.sh AI 提炼
    ↓
process_extract_queue.sh 队列处理
    ↓
┌─────────┬─────────┬─────────┐
│  L2     │  L3     │  L4     │
│ 任务待办│ 项目记忆│ 知识沉淀│
│多维表格 │ 云文档  │ 云文档  │
└─────────┴─────────┴─────────┘
    ↓
飞书 IM 推送提炼报告
```

## 快速开始

### 1. 安装依赖

```bash
# inotify-tools（文件监听）
apt install inotify-tools

# jq（JSON 处理）
apt install jq
```

### 2. 配置飞书

```bash
# 配置飞书 OAuth 授权
openclaw auth feishu
```

### 3. 配置环境变量

创建 `.env` 文件（不要提交到版本控制）：

```bash
# 飞书用户 ID
export FEISHU_USER_OPEN_ID="ou_xxxxxxxx"

# 飞书多维表格（L2-任务待办）
export L2_APP_TOKEN="xxxxxxxxxxxx"
export L2_TABLE_ID="tblxxxxxxxxxxxx"

# 飞书云文档
export L3_DOC_ID="xxxxxxxxxxxx"
export L4_DOC_ID="xxxxxxxxxxxx"

# OpenClaw 目录（可选）
export OPENCLAW_DIR="$HOME/.openclaw"
```

加载环境变量：

```bash
source .env
```

### 4. 启动监听

```bash
# 添加到 crontab
*/5 * * * * cd /path/to/lingxi-memory && source .env && bash scripts/session_watch.sh
```

详细安装说明见 [SKILL.md](./SKILL.md)

## 目录结构

```
lingxi-memory/
├── SKILL.md                    # Skill 定义
├── README.md                   # 项目说明（含数据安全说明）
├── LICENSE                     # MIT 协议
├── .gitignore                  # 忽略 .env 等敏感文件
└── scripts/                    # 核心脚本
    ├── session_watch.sh        # 会话监听
    ├── do_extract.sh           # AI 提炼
    └── process_extract_queue.sh # 队列处理
```

## 五层存储

| 层级 | 名称 | 存储位置 | 说明 |
|:----:|------|---------|------|
| L1 | 原始会话 | OpenClaw 本地 | 完整会话记录 |
| L2 | 任务待办 | 飞书多维表格 | 待办/阻塞事项 |
| L3 | 项目记忆 | 飞书云文档 | 决策/进展/配置 |
| L4 | 知识沉淀 | 飞书云文档 | 经验/SOP/踩坑 |
| L5 | 全局规则 | 本地文件 | 系统规则 |

## 故障排查

```bash
# 检查监听进程
ps aux | grep session_watch

# 查看日志
tail -50 ~/.openclaw/workspace/logs/session_extract.log

# 检查队列
cat /tmp/extract_queue.txt
```

## 开源协议

MIT License - See [LICENSE](./LICENSE)

---

⭐ 如果这个项目对你有帮助，欢迎 star！
