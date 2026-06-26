## 自訂指令（Commands）

### 建立指令檔案

在 `commands/` 目錄建立 markdown 檔案：

```
.opencode/commands/test.md
```

```markdown
---
description: Run tests with coverage
agent: build
model: anthropic/claude-3-5-sonnet-20241022
---

Run the full test suite with coverage report and show any failures.
Focus on the failing tests and suggest fixes.
```

使用方式：`/test`

### 放置位置

| 範圍 | 路徑 |
|------|------|
| 全域 | `~/.config/opencode/commands/` |
| 專案 | `.opencode/commands/` |

### JSON 格式設定

```json
{
  "command": {
    "test": {
      "template": "Run the full test suite with coverage...",
      "description": "Run tests with coverage",
      "agent": "build",
      "model": "anthropic/claude-haiku-4-5"
    }
  }
}
```

### 參數佔位符

| 佔位符 | 說明 |
|--------|------|
| `$ARGUMENTS` | 整個傳入參數 |
| `$1`, `$2`, `$3` | 位置參數 |

```markdown
---
description: Create a new component
---
Create a new React component named $ARGUMENTS with TypeScript support.
```

執行：`/component Button` → `$ARGUMENTS` = `Button`

### Shell 輸出注入

使用 `!` 前綴注入指令輸出：

```markdown
---
description: Analyze test coverage
---
Here are the current test results:
!`npm test`

Based on these results, suggest improvements to increase coverage.
```

### 檔案參照

使用 `@` 前綴參照檔案：

```markdown
---
description: Review component
---
Review the component in @src/components/Button.tsx.
Check for performance issues and suggest improvements.
```

### subtask 參數

強制作為子代理執行（隔離上下文）：
```json
{
  "command": {
    "analyze": {
      "subtask": true
    }
  }
}
```

### 內建指令（可被覆寫）

可用 `/init`、`/undo`、`/redo`、`/share`、`/help` 等。定義同名的自訂指令會覆寫內建版本。
