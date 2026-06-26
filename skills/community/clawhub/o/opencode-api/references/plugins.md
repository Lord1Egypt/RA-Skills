## Plugins 外掛系統

Plugin 透過事件鉤子擴展 OpenCode。

### 放置位置

| 範圍 | 路徑 |
|------|------|
| 全域 | `~/.config/opencode/plugins/` |
| 專案 | `.opencode/plugins/` |

### 基本結構

```javascript
// .opencode/plugins/my-plugin.js
export default async ({ project, client, $, directory, worktree }) => {
  console.log("Plugin initialized!")
  return {
    // === 工具鉤子 ===
    "tool.execute.before": async (input, output) => {
      if (input.tool === "bash" && output.args.command?.includes("rm -rf")) {
        throw new Error("已阻擋危險的 rm -rf 命令")
      }
      if (input.tool === "read" && output.args.filePath?.includes(".env")) {
        throw new Error("不允許讀取 .env 檔案")
      }
    },

    // === 工作階段鉤子 ===
    "session.created": async ({ session }) => {
      // 新 Session 啟動時
      if (session.parentID) {
        // 是子代理，注入專案上下文
        await client.session.prompt({
          path: { id: session.id },
          body: {
            noReply: true,
            parts: [{
              type: "text",
              text: "工作目錄：C:\\Users\\admin\\Desktop\\minecraft_translator_flet\npytest：.venv\\Scripts\\python.exe -m pytest"
            }]
          }
        })
      }
    },

    "session.idle": async ({ session }) => {
      await $`echo "Session ${session.id} 完成"`
    },

    // === Shell 鉤子 ===
    "shell.env": async (input, output) => {
      output.env.MC_TRANSLATE_ROOT = "C:/Users/admin/Desktop/minecraft_translator_flet"
    },

    // === 權限鉤子 ===
    "permission.asked": async ({ permission, agent }) => {
      if (permission === "bash" && agent === "plan") {
        return "deny"  // plan 代理一律拒絕 bash
      }
      return "ask"
    },

    // === 訊息鉤子 ===
    "message.updated": async ({ message }) => {},
  }
}
```

### 完整事件鉤子清單

| 類別 | 事件 | 觸發時機 |
|------|------|----------|
| 工具 | `tool.execute.before` | 工具執行前 |
| 工具 | `tool.execute.after` | 工具執行後 |
| 工作階段 | `session.created` | 新 session 建立 |
| 工作階段 | `session.idle` | session 閒置 |
| 工作階段 | `session.error` | session 錯誤 |
| 工作階段 | `session.updated` | session 更新 |
| 工作階段 | `session.deleted` | session 刪除 |
| 工作階段 | `session.diff` | session diff 可用 |
| 工作階段 | `session.compacted` | session 壓縮後 |
| 訊息 | `message.updated` | 訊息更新 |
| 訊息 | `message.removed` | 訊息刪除 |
| 訊息 | `message.part.updated` | 訊息部分更新 |
| 權限 | `permission.asked` | 請求權限 |
| 權限 | `permission.replied` | 權限回覆 |
| Shell | `shell.env` | Shell 環境變數 |
| TUI | `tui.prompt.append` | prompt 附加 |
| TUI | `tui.command.execute` | TUI 命令執行 |
| TUI | `tui.toast.show` | Toast 顯示 |
| 檔案 | `file.edited` | 檔案編輯後 |
| 檔案 | `file.watcher.updated` | 檔案監控更新 |
| LSP | `lsp.updated` | LSP 更新 |
| LSP | `lsp.client.diagnostics` | LSP 診斷 |
| 待辦 | `todo.updated` | 待辦更新 |
| 安裝 | `installation.updated` | 安裝更新 |
| 指令 | `command.executed` | 指令執行後 |

### Plugin 環境

Plugin 函式接收的上下文物件：

| 屬性 | 說明 |
|------|------|
| `project` | 目前專案資訊 |
| `directory` | 目前工作目錄 |
| `worktree` | Git worktree 根目錄 |
| `client` | OpenCode SDK 用戶端 |
| `$` | Bun Shell API |

### NPM 依賴

在設定目錄建立 `package.json`：

```json
{
  "dependencies": {
    "shescape": "^2.1.0"
  }
}
```

OpenCode 啟動時自動執行 `bun install`。

### MCP 工具

Plugin 也可以匯出工具：

```javascript
import { tool } from "@opencode-ai/plugin"

export default async (ctx) => {
  return {
    tool: {
      my_tool: tool({
        description: "自訂工具",
        args: { foo: tool.schema.string() },
        async execute(args, context) {
          return `Hello ${args.foo}`
        },
      }),
    },
  }
}
```

### 日誌記錄

使用 `client.app.log()` 而非 `console.log`：

```javascript
await client.app.log({
  body: {
    service: "my-plugin",
    level: "info",
    message: "Plugin initialized",
    extra: { project: project.name },
  },
})
```

### 壓縮鉤子（實驗性）

```javascript
"experimental.session.compacting": async (input, output) => {
  output.context.push(`
## Custom Context
- Current task status
- Important decisions made
- Files being actively worked on
  `)
}
```

### 實用 Plugin 範例

**安全保護**（阻擋危險操作）：
```javascript
export default async (ctx) => {
  return {
    "tool.execute.before": async (input, output) => {
      const dangerous = ["rm -rf", "git push --force", "DROP TABLE"]
      for (const cmd of dangerous) {
        if (output.args.command?.includes(cmd)) {
          throw new Error(`已阻擋危險命令：${cmd}`)
        }
      }
    },
  }
}
```

**自動化通知**（session 完成時通知）：
```javascript
export default async ({ client }) => {
  return {
    "session.idle": async ({ session }) => {
      await client.showToast?.(`Session ${session.id} 完成`, "info")
    },
  }
}
```
