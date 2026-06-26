---
name: Page Agent Claw Controller
slug: page-agent-claw
version: 1.0.0
homepage: https://github.com/page-agent-claw
description: 通过本地 page-agent 服务（运行在 http://localhost:4222）执行浏览器自动化任务。当用户指令中包含 "page-agent" 或需要调用本地浏览器时使用,该服务可以打开网页、执行页面操作、提取信息等。
metadata: {"clawdbot":{"emoji":"🕸️","requires":{"bins":["npm","node","curl"]},"os":["linux","darwin","win32"],"configPaths":[]}}
---

## When to Apply

用户需要控制浏览器打开页面、执行浏览操作时使用此skill。

## Prerequisites

确保page-agent-claw npm包已安装，并运行在端口4222。

## Workflow

### 1. 检查服务状态

```bash
curl http://localhost:4222/api/status
```

**响应示例**:
```json
{"code":100,"message":"请打开 localhost:4222 页面","connectedNumber":0}
{"code":105,"message":"page-agent 未连接","connectedNumber":1}
{"code":200,"message":"正常","connectedNumber":1,"pageAgentCount":1}
```

| 状态码 | 说明 |
|--------|------|
| 100 | 无WebSocket连接，需打开 http://localhost:4222 |
| 105 | 有连接但page-agent未连接 |
| 200 | 正常，可以执行任务 |

### 2. 启动服务（如未运行）

```bash
# 检查服务是否运行
curl http://localhost:4222/health

# 如未运行，启动服务
page-agent-claw
```

### 3. 提交浏览任务

```bash
curl -X POST http://localhost:4222/api/task \
  -H "Content-Type: application/json" \
  -d '{"task": "打开 https://www.example.com"}'
```

**⚠️ 超时设置提示**

复杂任务（如多步骤操作、大量数据提取）可能需要较长时间，建议设置 curl 超时参数：

```bash
# 设置最大执行时间为 120 秒
curl -X POST http://localhost:4222/api/task \
  -H "Content-Type: application/json" \
  --max-time 180 \
  -d '{"task": "复杂的浏览任务"}'
```

| 参数 | 说明 |
|------|------|
| `--max-time <seconds>` | 设置整个操作的最大允许时间 |
| `--connect-timeout <seconds>` | 仅设置连接超时时间 |

**任务示例**:
- `"打开 https://www.example.com"`
- `"在当前页面搜索 Claude"`
- `"访问 Google，搜索 page-agent，然后点击第一个结果"`

## API Reference

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/status` | GET | 获取服务状态 |
| `/api/task` | POST | 提交浏览任务 |
| `/health` | GET | 健康检查 |

## Requirements

- Node.js + npm
- page-agent-claw: `npm install -g page-agent-claw`
- page-agent Chrome扩展（用于控制浏览器）
