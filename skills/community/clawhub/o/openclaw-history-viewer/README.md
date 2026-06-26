# OpenClaw 会话历史查看器

浏览和查看 OpenClaw 的历史聊天记录，**自动支持 OpenClaw 的 .reset. 备份文件**，无需额外的监控进程！

## 最新版本 v1.1.1

- ✅ 新增刷新按钮：重新加载最新数据，保持当前阅读位置
- ✅ 添加 favicon 图标：浏览器标签页显示 💬 对话气泡
- ✅ 优化界面：移除冗余标题，布局更紧凑
- ✅ 自动滚动：页面加载时自动定位到最新消息

## 工作原理

### OpenClaw 自动备份机制

当你使用 `/new` 或 `/reset` 命令时，OpenClaw 会：
1. 将当前会话文件重命名为 `<session-id>.jsonl.reset.<timestamp>`
2. 创建新的会话文件

### History Viewer 增强

本技能增强了 `history_server.py`，可以：
- 读取当前活跃会话（`sessions.json`）
- **自动扫描并读取 `.reset.` 备份文件**
- 读取手动备份（`~/.openclaw/workspace/history/`）
- 合并显示所有会话，按时间排序

```
┌─────────────────────────────────────────────────────────────┐
│              ~/.openclaw/agents/main/sessions/              │
│  ├── sessions.json                    (活跃会话索引)         │
│  ├── <session-id>.jsonl               (活跃会话)            │
│  └── <session-id>.jsonl.reset.*       (自动备份) ← 新增！   │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
         ┌────────────────────────┐
         │   history_server.py    │
         │   (读取所有会话)        │
         └────────────┬───────────┘
                      │
                      ▼
         http://localhost:8765/
         (显示所有会话)
```

## 快速开始

```bash
# 启动服务
python3 ~/.openclaw/skills/openclaw-history-viewer/scripts/history_server.py

# 访问 http://localhost:8765
```

**就这么简单！** 无需配置后台监控，所有 `.reset.` 备份会自动显示。

## 功能特性

### 1. 自动读取 .reset. 备份

- 扫描 `~/.openclaw/agents/main/sessions/*.jsonl.reset.*`
- 解析时间戳和会话 ID
- 显示在会话列表中（标识为 "reset-backup"）

### 2. 合并显示所有会话

| 来源 | 标识 | 说明 |
|------|------|------|
| `sessions.json` | 🟢 webchat | 当前活跃会话 |
| `.jsonl.reset.*` | 📦 reset-backup | OpenClaw 自动备份 |
| `history/*.jsonl` | 📦 backup | 手动备份（可选） |

### 3. 两种查看模式

- **聊天视图** (`/chat?id=xxx`)：类似微信/Telegram 的气泡界面
- **Raw 视图** (`/session?id=xxx`)：原始 JSON 格式，适合调试

### 4. 刷新功能（v1.1.1 新增）

- **🔄 重新加载按钮**：位于页面顶部，紧邻视图切换器
- **保持阅读位置**：刷新后保持当前屏幕内容不变
- **自动调整滚动条**：有新消息时可继续下拉查看
- **状态提示**：加载中 → 已加载（1.5 秒）

### 5. 界面优化

- **💬 Favicon 图标**：浏览器标签页显示对话气泡图标
- **简洁布局**：移除冗余的"会话详情"标题
- **紧凑设计**：按钮和元数据排列更紧凑

## 文件说明

| 文件 | 用途 | 是否需要 |
|------|------|----------|
| `history_server.py` | Web 服务器 | ✅ 必需 |
| `backup_session.py` | 手动备份工具 | ⭕ 可选 |
| `session_watcher.py` | 监控脚本 | ❌ 已废弃 |
| `backup_and_start.sh` | 启动脚本 | ⭕ 可选 |

## 高级用法

### 刷新聊天数据（v1.1.1 新增）

在聊天详情页或 Raw 详情页：
1. 点击顶部的 **🔄 重新加载** 按钮
2. 数据会从会话文件重新加载
3. 当前阅读位置保持不变
4. 如有新消息，可继续下拉查看

### 手动备份到独立目录

```bash
# 备份当前会话
python3 ~/.openclaw/skills/openclaw-history-viewer/scripts/backup_session.py

# 备份文件位置
ls -lh ~/.openclaw/workspace/history/
```

### API 使用

```bash
# 获取所有会话（包含 .reset. 备份）
curl http://localhost:8765/api/sessions | jq

# 获取特定会话详情
curl "http://localhost:8765/api/session?id=<session_id>" | jq

# 导出会话
curl "http://localhost:8765/api/session?id=<session_id>" > export.jsonl
```
