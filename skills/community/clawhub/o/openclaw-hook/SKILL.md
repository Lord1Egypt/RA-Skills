---
name: openclaw-hook
description: Create, debug, and maintain OpenClaw Gateway internal hooks. Use when: (1) creating new hooks for agent events like bootstrap, (2) debugging hook execution issues, (3) understanding hook configuration and event structure, (4) injecting virtual bootstrap files, (5) fixing issues like Telegram notifications not sending, Content-Length errors, or context access problems. Triggers on phrases like "create a hook", "fix hook", "debug hook", "hook not working", "internal hook".
---

# OpenClaw Internal Hook 开发指南

## 什么是 Internal Hook？

Internal Hook 是 OpenClaw Gateway 内部的事件处理器，在 agent 生命周期事件（如 `agent:bootstrap`）触发时执行 JavaScript/TypeScript 代码。

**用途**：
- 在会话启动时注入上下文文件
- 检查和提醒用户待处理的事项
- 发送通知（Telegram、Webhook 等）
- 记录日志和审计

## 快速开始

### 1. 创建 Hook 目录

```
~/.openclaw/hooks/
└── my-hook/
    ├── HOOK.md      # Hook 元数据（可选但推荐）
    └── handler.js   # 主要处理逻辑（必须）
```

### 2. 编写 Handler

```javascript
// ~/.openclaw/hooks/my-hook/handler.js
const handler = async (event) => {
  // 检查事件类型
  if (event.type !== 'agent' || event.action !== 'bootstrap') return;
  
  // 检查上下文
  if (!event.context?.workspaceDir) return;
  
  // 跳过 sub-agent
  if (event.sessionKey?.includes(':subagent:')) return;
  
  // 注入虚拟文件
  if (Array.isArray(event.context.bootstrapFiles)) {
    event.context.bootstrapFiles.push({
      path: 'MY_CONTEXT.md',
      content: '# Hello from hook!',
      virtual: true,
    });
  }
};

module.exports = handler;
module.exports.default = handler;
```

### 3. 注册 Hook

在 `~/.openclaw/openclaw.json` 中添加：

```json
{
  "hooks": {
    "internal": {
      "enabled": true,
      "entries": {
        "my-hook": {
          "enabled": true
        }
      },
      "load": {
        "extraDirs": ["~/.openclaw/hooks"]
      }
    }
  }
}
```

### 4. 重启 Gateway

```bash
openclaw gateway restart
```

## 事件结构

### agent:bootstrap 事件

```javascript
{
  type: 'agent',
  action: 'bootstrap',
  sessionKey: 'agent:main:telegram:direct:YOUR_USER_ID',
  context: {
    workspaceDir: '~/.openclaw/workspace',
    bootstrapFiles: [
      { path: 'MEMORY.md', content: '...' },
      // 可以 push 新文件到这里
    ],
    cfg: { /* 配置对象 */ },
    sessionId: 'uuid',
    agentId: 'main'
  }
}
```

### 上下文字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `workspaceDir` | string | 工作区目录路径 |
| `bootstrapFiles` | array | 要注入的文件列表 |
| `cfg` | object | Gateway 配置（可能不完整） |
| `sessionId` | string | 会话 UUID |
| `agentId` | string | Agent ID（如 'main', 'baixiaosheng'） |

## HOOK.md 元数据

```yaml
---
name: my-hook
description: "What this hook does"
metadata:
  openclaw:
    emoji: "📚"
    events: ["agent:bootstrap"]
    requires:
      config: ["workspace.dir"]
---
# Hook 说明
...
```

## 核心模式

### 1. 安全检查（必须！）

```javascript
const handler = async (event) => {
  // 检查事件对象
  if (!event || typeof event !== 'object') return;
  
  // 只处理 bootstrap 事件
  if (event.type !== 'agent' || event.action !== 'bootstrap') return;
  
  // 检查上下文
  if (!event.context || typeof event.context !== 'object') return;
  
  // 跳过 sub-agent
  if (event.sessionKey?.includes(':subagent:')) return;
  
  // 检查工作区
  const workspaceDir = event.context?.workspaceDir;
  if (!workspaceDir) return;
  
  // 继续处理...
};
```

### 2. 注入虚拟文件

```javascript
if (Array.isArray(event.context.bootstrapFiles)) {
  event.context.bootstrapFiles.push({
    path: 'REMINDER.md',
    content: '# Reminder\nDo something!',
    virtual: true,
  });
}
```

### 3. 读取工作区文件

```javascript
const fs = require('fs');
const path = require('path');

const memoryDir = path.join(workspaceDir, 'memory');
if (fs.existsSync(memoryDir)) {
  const files = fs.readdirSync(memoryDir).filter(f => f.endsWith('.md'));
  // 处理文件...
}
```

### 4. 发送 HTTP 请求（如 Telegram）

```javascript
const https = require('https');

async function sendNotification(botToken, chatId, message) {
  const data = JSON.stringify({
    chat_id: chatId,
    text: message,
  });
  
  return new Promise((resolve) => {
    const options = {
      hostname: 'api.telegram.org',
      port: 443,
      path: `/bot${botToken}/sendMessage`,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        // ⚠️ 关键：使用 Buffer.byteLength
        'Content-Length': Buffer.byteLength(data),
      },
    };
    
    const req = https.request(options, (res) => {
      let body = '';
      res.on('data', (chunk) => body += chunk);
      res.on('end', () => resolve(res.statusCode === 200));
    });
    
    req.on('error', (e) => {
      console.error('[hook] Error:', e.message);
      resolve(false);
    });
    
    req.write(data);
    req.end();
  });
}
```

### 5. 获取配置（从文件读取更可靠）

```javascript
const fs = require('fs');

function getBotToken(accountName) {
  try {
    const configPath = path.join(os.homedir(), '.openclaw/openclaw.json');
    const content = fs.readFileSync(configPath, 'utf-8');
    const match = content.match(
      new RegExp(`"${accountName}"[\\s\\S]*?"botToken"\\s*:\\s*"([^"]+)"`)
    );
    return match?.[1] || null;
  } catch (e) {
    console.error('[hook] Config read error:', e.message);
    return null;
  }
}
```

## 调试方法

### 1. 添加日志

```javascript
console.error('[my-hook] Debug:', JSON.stringify({
  sessionKey: event.sessionKey,
  workspaceDir: event.context?.workspaceDir,
}));
```

### 2. 查看日志

```bash
# 实时查看
tail -f ~/.openclaw/logs/gateway.err.log

# 搜索特定 hook
grep -i "my-hook" ~/.openclaw/logs/gateway.err.log | tail -20
```

### 3. 独立测试发送逻辑

```bash
node -e "
const https = require('https');
const data = JSON.stringify({
  chat_id: 'YOUR_CHAT_ID',
  text: 'Test message'
});
console.log('Byte length:', Buffer.byteLength(data));
// ... 发送逻辑
"
```

### 4. 测试 Hook 执行

发送 `/new` 命令触发 bootstrap 事件，然后检查日志。

## 常见陷阱

### 1. Content-Length 字节计算

**问题**：发送中文时 Telegram 返回 `message text is empty`

**原因**：`data.length` 是字符数，不是字节数。中文字符在 UTF-8 中占 3 字节。

```javascript
// ❌ 错误
'Content-Length': data.length

// ✅ 正确
'Content-Length': Buffer.byteLength(data)
```

### 2. Markdown 解析问题

Telegram Markdown 解析很严格，特殊字符会导致失败。

**解决方案**：不使用 `parse_mode`，发送纯文本。

### 3. cfg 对象不完整

`event.context.cfg` 可能不包含完整配置。

**解决方案**：直接从配置文件读取。

### 4. 忘记导出 handler

```javascript
// 必须导出
module.exports = handler;
module.exports.default = handler;
```

### 5. 忘记重启 Gateway

修改 hook 后必须重启：
```bash
openclaw gateway restart
```

## 完整示例

参见 `references/complete-example.js` 获取包含所有功能的完整 hook 示例。
