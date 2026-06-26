---
name: vscode-copilot
description: Bridge between OpenClaw and VS Code Copilot — dispatch coding tasks from any OpenClaw channel to VS Code for execution.
version: 0.2.0
homepage: https://marketplace.visualstudio.com/items?itemName=wodeapp.openclaw-chat
metadata:
  openclaw:
    emoji: "💻"
    requires:
      bins: ["curl"]
---

# VS Code Copilot Bridge

Dispatch coding tasks from OpenClaw to VS Code Copilot for execution. When the user asks you to write, edit, review, or debug code, send the task to VS Code where Copilot will execute it — editing files, running commands, creating code, and more.

将编码任务从 OpenClaw 分发到 VS Code Copilot 执行。当用户要求编写、编辑、审查或调试代码时，将任务发送到 VS Code，由 Copilot 代为执行——编辑文件、运行命令、创建代码等。

## Setup / 安装

Install the OpenClaw Chat extension from VS Code Marketplace:
从 VS Code 扩展商店安装 OpenClaw Chat 扩展：

```bash
code --install-extension wodeapp.openclaw-chat
```

Or search **"OpenClaw Chat"** in VS Code Extensions panel.
或在 VS Code 扩展面板搜索 **"OpenClaw Chat"** 安装。

The extension starts automatically with VS Code. No manual launch needed.
扩展会随 VS Code 自动启动，无需手动操作。

## External Endpoints / 端点

| Endpoint | Method | Data Sent / 发送数据 |
|---|---|---|
| `http://localhost:19836/trigger` | POST | `{"prompt":"..."}` — the coding task / 编码任务 |
| `http://localhost:19836/health` | GET | None / 无 |

All traffic is local (127.0.0.1). No data leaves the machine.
所有流量均在本地（127.0.0.1），不会发送到外部。

## Workflow / 工作流程

1. Check if the extension is running / 检查扩展是否运行：

```bash
curl -s http://localhost:19836/health
```

If not running, guide the user through Setup above.
如未运行，引导用户完成上方安装步骤。

2. Send the coding task / 发送编码任务：

```bash
curl -s -X POST http://localhost:19836/trigger \
  -H "Content-Type: application/json" \
  -d '{"prompt":"<TASK_DESCRIPTION>"}'
```

3. The response JSON contains a `response` field with Copilot's reply. Display it to the user.
返回的 JSON 包含 `response` 字段，内含 Copilot 的回复。将其展示给用户。

## Example / 示例

User says / 用户说: "帮我写一个防抖函数"

```bash
curl -s -X POST http://localhost:19836/trigger \
  -H "Content-Type: application/json" \
  -d '{"prompt":"在当前打开的文件里写一个 TypeScript 防抖函数"}'
```

Response / 返回：
```json
{"ok":true,"prompt":"...","response":"Here is a debounce function..."}
```

## Security & Privacy / 安全与隐私

- All HTTP traffic stays on localhost (127.0.0.1:19836) / 所有流量仅在本地
- No data is sent to external servers by this skill / 此 skill 不会向外部发送数据
- Copilot processes the request using GitHub's API (standard Copilot behavior) / Copilot 通过 GitHub API 处理请求（标准行为）

## Notes / 注意事项

- VS Code must be open / VS Code 必须处于打开状态
- Copilot Chat should be in **Agent mode** for full execution / Copilot Chat 应切换到 **Agent 模式**以获得完整执行能力
- Always run health check before dispatching if unsure / 不确定时先执行健康检查
- Always show the response to the user / 始终将回复展示给用户
