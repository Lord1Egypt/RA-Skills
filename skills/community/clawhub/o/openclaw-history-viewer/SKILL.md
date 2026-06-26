---
name: openclaw-history-viewer
description: 启动一个 web 服务来浏览和查看 OpenClaw 的历史聊天记录。支持会话列表、消息详情查看、JSON API 导出、自动会话备份、刷新功能。使用场景：当用户想要查看、浏览、搜索或导出 OpenClaw 的聊天历史记录时触发此技能。触发词包括："启动历史记录"、"打开聊天记录"、"查看历史"、"启动 history viewer"、"打开聊天历史"等。
---

# OpenClaw History Viewer

浏览和查看 OpenClaw 的历史聊天记录，**支持自动会话备份**，即使开启新会话也不会丢失旧记录。

## 快速启动

### 🗣️ 自然语言启动

直接告诉我以下任何一句话即可启动：

- "启动历史记录查看器"
- "打开聊天记录"
- "查看 OpenClaw 历史"
- "启动历史查看服务"
- "帮我打开历史聊天"

我会自动为你启动服务！

### 🆕 最新版本 v1.1.1

- 🔄 **刷新按钮**：重新加载最新数据，保持当前阅读位置
- 💬 **Favicon 图标**：浏览器标签页显示对话气泡
- ✨ **界面优化**：移除冗余标题，布局更紧凑

### 💻 命令行启动

启动 web 服务器（默认端口 8765）：

```bash
python3 ~/.openclaw/skills/openclaw-history-viewer/scripts/history_server.py
```

自定义端口：

```bash
python3 ~/.openclaw/skills/openclaw-history-viewer/scripts/history_server.py 9000
```

### 🔙 后台启动

```bash
nohup python3 ~/.openclaw/skills/openclaw-history-viewer/scripts/history_server.py > /tmp/history.log 2>&1 &
```

## 功能特性

### 🔄 自动会话备份（新增！）

**问题**：OpenClaw 在开启新会话时会覆盖 `sessions.json`，导致旧会话记录"消失"。

**解决**：本技能支持读取 OpenClaw 自动创建的 `.reset.` 备份文件，**无需后台监控进程**！

#### OpenClaw 自动备份机制

当你使用 `/new` 或 `/reset` 命令时，OpenClaw 会自动：
1. 将当前会话文件重命名为 `<session-id>.jsonl.reset.<timestamp>`
2. 创建新的会话文件

这些 `.reset.` 文件会**自动显示在历史记录列表中**！

#### 备份文件位置

```
~/.openclaw/agents/main/sessions/
├── sessions.json                    # 当前活跃会话索引
├── <session-id>.jsonl               # 当前会话文件
└── <session-id>.jsonl.reset.*       # 自动备份的旧会话
```

#### 查看备份的会话

启动 Web 服务后，所有 `.reset.` 备份的会话会**自动显示在列表中**，带有 "📦 reset-backup" 标识：
- 备份会话按时间排序
- 点击可查看完整的聊天历史
- 支持聊天视图和 Raw 视图切换

### 手动备份（可选）

如果你需要额外备份到独立目录：

```bash
# 备份当前会话
python3 ~/.openclaw/skills/openclaw-history-viewer/scripts/backup_session.py

# 备份指定会话
python3 ~/.openclaw/skills/openclaw-history-viewer/scripts/backup_session.py <session_id>
```

备份文件位置：`~/.openclaw/workspace/history/`

### Web 界面

#### 📋 列表视图 (`/`)
传统的列表展示方式，显示所有会话：
- Session ID
- 消息数量
- 频道类型 (webchat, discord, telegram 等)
- 最后更新时间
- 点击可查看会话详情（Raw 模式）

#### 💬 聊天视图 (`/chat`)
**新增！** 现代化的聊天界面展示方式：
- 类似微信/Telegram 的对话式布局
- 用户消息显示在右侧（紫色气泡）
- 助手消息显示在左侧（灰色气泡）
- 系统消息居中显示
- 支持展示思考过程（带折叠/展开）
- 支持展示工具调用和结果
- 渐变紫色背景，毛玻璃效果
- 响应式设计，支持移动端

#### 🔍 视图切换
- 在聊天详情页可以通过按钮切换 "聊天视图" 和 "Raw 视图"
- 聊天视图 URL: `/chat?id=<session_id>`
- Raw 视图 URL: `/session?id=<session_id>`

#### 🔄 刷新功能（v1.1.1 新增）
- **重新加载按钮**：位于页面顶部，紧邻视图切换器
- **保持阅读位置**：刷新后保持当前屏幕内容不变
- **自动调整滚动条**：有新消息时可继续下拉查看
- **状态提示**：加载中 → 已加载（1.5 秒）

#### 💬 Favicon 图标
- 浏览器标签页显示 💬 对话气泡图标
- 所有页面统一使用相同图标
- 使用内嵌 SVG，无需额外文件

### URL 路由

| URL | 说明 |
|-----|------|
| `/` | **默认** - 聊天视图列表（现代化界面） |
| `/list` | 列表视图（传统表格界面） |
| `/chat?id=<session_id>` | 聊天详情视图 |
| `/session?id=<session_id>` | Raw 详情视图 |
| `/api/sessions` | 获取会话列表 API |
| `/api/session?id=<session_id>` | 获取会话详情 API |

### JSON API

- **获取会话列表**: `GET /api/sessions`
  
  ```json
  {
    "sessions": [
      {
        "sessionId": "xxx-xxx-xxx",
        "updatedAt": 1234567890,
        "updatedAtStr": "2026-03-15 13:00:00",
        "channel": "webchat",
        "chatType": "direct",
        "messageCount": 150
      }
    ],
    "total": 10
  }
  ```

- **获取会话详情**: `GET /api/session?id=<session_id>`
  
  ```json
  {
    "sessionId": "xxx-xxx-xxx",
    "sessionInfo": {...},
    "messages": [
      {
        "line": 1,
        "type": "session",
        "timestamp": "2026-03-15T05:18:57.108Z",
        "id": "...",
        "data": {...}
      }
    ],
    "total": 150
  }
  ```

## 数据存储位置

OpenClaw 会话数据存储在：
```
~/.openclaw/agents/main/sessions/
├── sessions.json          # 会话索引
├── <session-id>.jsonl     # 会话消息记录 (JSONL 格式)
```

## 消息类型

会话中可能包含的消息类型：

- `session` - 会话元数据
- `message` - 用户或助手消息
- `toolCall` - 工具调用
- `toolResult` - 工具执行结果
- `model_change` - 模型切换
- `thinking_level_change` - 思考级别变更
- `custom` - 自定义事件

## 使用示例

### 场景 1：启动服务（最简单！）

```bash
# 启动 Web 服务
python3 ~/.openclaw/skills/openclaw-history-viewer/scripts/history_server.py

# 访问 http://localhost:8765
```

**无需后台监控！** OpenClaw 已自动创建 `.reset.` 备份文件，服务会自动读取并显示。

### 场景 2：查看最近的聊天历史

```bash
# 启动服务
python3 ~/.openclaw/skills/openclaw-history-viewer/scripts/history_server.py

# 在浏览器打开 http://localhost:8765
```

### 场景 3：通过 API 获取会话列表（包含 .reset. 备份）

```bash
curl http://localhost:8765/api/sessions | jq
```

### 场景 4：导出特定会话

```bash
# 导出活跃会话
curl "http://localhost:8765/api/session?id=<session_id>" > session_export.json

# 导出 .reset. 备份会话
curl "http://localhost:8765/api/session?id=<reset_session_id>" > reset_session_export.json
```

### 场景 5：手动备份到独立目录（可选）

```bash
# 备份当前会话到 ~/.openclaw/workspace/history/
python3 ~/.openclaw/skills/openclaw-history-viewer/scripts/backup_session.py

# 备份指定会话
python3 ~/.openclaw/skills/openclaw-history-viewer/scripts/backup_session.py <session_id>
```

## 注意事项

- 服务默认监听 `localhost:8765`，仅本地访问
- 会话文件为 JSONL 格式，每行一个 JSON 对象
- 长消息在 Web 界面中会被截断预览，可点击展开
