# HTTP API 参考

## 端点概览
Gateway同端口多路复用WebSocket + HTTP:
- `ws://<host>:<port>/` — WebSocket (主协议)
- `POST /v1/responses` — OpenResponses API (默认禁用)
- Canvas: `http://<host>:<port+4>/__openclaw__/canvas/`

## OpenResponses API

### 启用
```json5
gateway: { http: { endpoints: { responses: { enabled: true } } } }
```

### 认证
`Authorization: Bearer <gateway.auth.token>`

### 选择智能体
- `model: "openclaw:<agentId>"` (如 `"openclaw:main"`)
- 或 `x-openclaw-agent-id: <agentId>` 头
- 可选: `x-openclaw-session-key: <key>` 控制会话路由

### 请求
```json
{
  "model": "openclaw:main",
  "input": "hello",           // 字符串或item数组
  "instructions": "...",       // 合并到系统提示
  "tools": [{ "type": "function", "function": { "name": "...", "parameters": {} } }],
  "stream": true,             // SSE流式
  "user": "stable-id"         // 稳定会话路由
}
```

### Item类型
| 类型 | 说明 |
|------|------|
| `message` | 角色: system/developer/user/assistant |
| `function_call_output` | 工具结果返回 |
| `input_image` | 图片(base64/URL) |
| `input_file` | 文件(base64/URL) |

### SSE事件 (stream=true)
response.created → response.in_progress → response.output_text.delta → response.completed

### 示例
```bash
curl -sS http://127.0.0.1:18789/v1/responses \
  -H 'Authorization: Bearer TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{"model":"openclaw:main","input":"hi"}'
```

### 限制配置
```json5
gateway: { http: { endpoints: { responses: {
  enabled: true,
  maxBodyBytes: 20000000,
  files: { maxBytes: 5242880, allowedMimes: ["text/plain","application/json","application/pdf"] },
  images: { maxBytes: 10485760, allowedMimes: ["image/jpeg","image/png","image/gif","image/webp"] }
}}}}
```

## Gateway RPC
```bash
openclaw gateway call <method> --params '{}'
```

### 常用方法
| 方法 | 说明 |
|------|------|
| `config.get` | 获取配置 |
| `config.apply` | 应用完整配置(需baseHash) |
| `config.patch` | 补丁配置(需baseHash) |
| `sessions.list` | 列出会话 |
| `cron.list` | 列出定时任务 |
| `cron.add` | 添加定时任务 |
| `cron.update` | 更新定时任务 |
| `cron.remove` | 删除定时任务 |
| `cron.run` | 运行定时任务 |

# 安全参考

## 访问控制层级
1. **渠道白名单**: allowFrom/groupAllowFrom 控制谁能发消息
2. **配对模式**: 首次联系需配对码批准
3. **网关认证**: gateway.auth.token 保护API访问
4. **工具策略**: tools.policy 控制工具可用性
5. **Exec审批**: tools.exec.approvals 控制命令执行
6. **沙箱隔离**: sandbox.mode 隔离执行环境

## 安全审计
```bash
openclaw security audit [--deep] [--fix]
```

## 最佳实践
- API Key用环境变量 `${VAR}` 引用，不硬编码
- 非loopback绑定必须设置 `gateway.auth.token`
- 生产环境启用沙箱隔离
- 定期运行 `openclaw security audit`
- 使用Tailscale进行远程访问(而非公网暴露)

## 沙箱配置
```json5
sandbox: {
  mode: "non-main",           // off|non-main|all
  scope: "agent",             // session|agent|shared
  workspaceAccess: "ro",      // none|ro|rw
  docker: {
    image: "openclaw-sandbox:bookworm-slim",
    network: "none",          // none|bridge
    memory: "1g", cpus: 1, pidsLimit: 256
  }
}
```

## Exec审批
```json5
tools: { exec: {
  approvals: { mode: "allowlist" },  // off|allowlist|full
  security: "allowlist"              // deny|allowlist|full
}}
```
审批存储: `~/.openclaw/exec-approvals.json`

## OpenAI Chat Completions API

### 启用
```json5
gateway: { http: { endpoints: { chat: { enabled: true } } } }
```

### 端点
`POST /v1/chat/completions` (与Gateway同端口)

### 认证
`Authorization: Bearer <gateway.auth.token>`

### 选择智能体
- `model: "openclaw:<agentId>"` (如 `"openclaw:main"`)
- 或 `x-openclaw-agent-id: <agentId>`

### 请求 (OpenAI兼容)
```json
{
  "model": "openclaw:main",
  "messages": [{"role": "user", "content": "hello"}],
  "stream": true
}
```

### 示例
```bash
curl http://127.0.0.1:18789/v1/chat/completions \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"model":"openclaw:main","messages":[{"role":"user","content":"hi"}]}'
```

## Tools Invoke API

### 端点
`POST /tools/invoke` (与Gateway同端口)

### 请求
```json
{
  "tool": "exec",
  "params": { "command": "ls -la" },
  "agentId": "main"
}
```

## 沙箱隔离详解

### 什么被沙箱隔离
exec, read, write, edit, apply_patch, process 等工具执行

### 模式
| 模式 | 说明 |
|------|------|
| `off` | 禁用(默认) |
| `non-main` | 非主会话沙箱化(群组/子智能体) |
| `all` | 所有会话沙箱化 |

### 作用域
| 作用域 | 说明 |
|--------|------|
| `session` | 每会话独立容器 |
| `agent` | 每智能体共享容器 |
| `shared` | 所有智能体共享 |

### 工作区访问
| 级别 | 说明 |
|------|------|
| `none` | 无访问 |
| `ro` | 只读挂载 |
| `rw` | 读写挂载 |

### 完整配置
```json5
sandbox: {
  mode: "non-main",
  scope: "agent",
  workspaceAccess: "ro",
  workspaceRoot: "~/.openclaw/sandboxes",
  docker: {
    image: "openclaw-sandbox:bookworm-slim",
    network: "none",           // none|bridge
    setupCommand: "apt-get update && apt-get install -y git",
    pidsLimit: 256,
    memory: "1g",
    cpus: 1,
    env: { MY_KEY: "..." }    // 沙箱环境变量
  },
  browser: { enabled: false },
  prune: { idleHours: 24, maxAgeDays: 7 }
}
```

### 沙箱 vs 工具策略 vs 提权
| 层 | 控制什么 | 配置 |
|----|----------|------|
| 沙箱 | 执行环境隔离 | `sandbox.mode` |
| 工具策略 | 哪些工具可用 | `tools.policy/allow/deny` |
| 提权 | 沙箱→主机执行 | `tools.elevated.mode` |

### CLI
```bash
openclaw sandbox list                    # 列出沙箱
openclaw sandbox recreate --all          # 重建所有
openclaw sandbox explain                 # 解释当前配置
```
