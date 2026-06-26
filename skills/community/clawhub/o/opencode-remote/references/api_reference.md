# OpenCode API 参考

基于 OpenAPI 3.1.1 规范，版本 0.0.3

## 基础信息

- **基础 URL**: `http://<host>:<port>`
- **健康检查**: `GET /global/health`
- **事件流**: `GET /global/event` (SSE)

---

## Session API

### 列出所有 Sessions
```
GET /session
```
返回所有 session 列表，包含 id、status、title 等基本信息。

### 创建 Session
```
POST /session
Content-Type: application/json

{
  "title": "可选的标题"
}
```

### 获取 Session 详情
```
GET /session/{sessionID}
```
返回 session 的完整信息，包括状态、创建时间、更新时间等。

### 更新 Session
```
PATCH /session/{sessionID}
Content-Type: application/json

{
  "title": "新标题"
}
```

### 删除 Session
```
DELETE /session/{sessionID}
```

---

## Session 消息 API

### 获取消息记录
```
GET /session/{sessionID}/message
```
返回该 session 的所有消息记录。

### 发送消息
```
POST /session/{sessionID}/message
Content-Type: application/json

{
  "parts": [
    {"type": "text", "content": "消息内容"}
  ]
}
```

Part 类型包括：
- `text` - 文本内容
- `file` - 文件引用
- `tool` - 工具调用
- `agent` - Agent 消息
- `subtask` - 子任务

### 异步发送消息
```
POST /session/{sessionID}/prompt_async
Content-Type: application/json

{
  "parts": [...]
}
```

---

## Session 控制 API

### 中止 Session
```
POST /session/{sessionID}/abort
```
中止正在运行中的 session。

### Fork Session
```
POST /session/{sessionID}/fork
```
从当前 session 创建分支。

### 获取子 Sessions
```
GET /session/{sessionID}/children
```
返回该 session 的所有子 session。

### 获取待办事项
```
GET /session/{sessionID}/todo
```
返回 session 中记录的待办事项。

### Summarize Session
```
POST /session/{sessionID}/summarize
Content-Type: application/json

{
  "summary": "用户要求的总结重点（可选）"
}
```
压缩/总结 session 历史记录。

### 获取 Diff
```
GET /session/{sessionID}/diff
```
返回 session 中的文件变更。

### 回退 Session
```
POST /session/{sessionID}/revert
Content-Type: application/json

{
  "messageID": "要回退到的消息ID"
}
```

---

## Session 命令 API

### 执行 Shell 命令
```
POST /session/{sessionID}/shell
Content-Type: application/json

{
  "command": "ls -la"
}
```

### 执行自定义命令
```
POST /session/{sessionID}/command
Content-Type: application/json

{
  "name": "/commit"
}
```

---

## Session 状态

Session 可能的状态值：

| 状态 | 说明 |
|------|------|
| `running` | 正在运行中，AI 正在处理 |
| `stopped` | 已停止，等待用户输入 |
| `completed` | 已完成 |
| `error` | 执行出错 |
| `aborted` | 被中止 |

---

## 其他 API

### 项目 API
```
GET /project              # 列出所有项目
GET /project/current      # 当前项目
PATCH /project/{id}       # 更新项目
```

### 文件 API
```
GET /file?path={path}           # 列出目录
GET /file/content?path={path}   # 读取文件内容
GET /file/status                # 获取 git 状态
```

### 搜索 API
```
GET /find?q={query}             # 文本搜索
GET /find/file?name={name}      # 文件搜索
GET /find/symbol?name={name}    # 符号搜索
```

### 配置 API
```
GET /config               # 获取配置
PATCH /config             # 更新配置
```

### Provider API
```
GET /provider             # 列出 AI 提供商
```

### Agent API
```
GET /agent                # 列出 agents
```

### Skill API
```
GET /skill                # 列出 skills
```

### PTY API
```
GET /pty                  # 列出 PTY 会话
POST /pty                 # 创建 PTY
GET /pty/{id}             # 获取 PTY 详情
DELETE /pty/{id}          # 关闭 PTY
GET /pty/{id}/connect     # WebSocket 连接
```

### MCP API
```
GET /mcp                  # MCP 服务器状态
POST /mcp                 # 添加 MCP 服务器
POST /mcp/{name}/connect  # 连接 MCP
POST /mcp/{name}/disconnect # 断开 MCP
```
