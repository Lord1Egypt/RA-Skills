## 內建工具一覽

| 工具 | 功能 | 權限預設 |
|------|------|----------|
| `bash` | 執行 Shell 指令 | allow |
| `edit` | 精確字串替換修改檔案 | allow |
| `write` | 建立新檔案或覆寫 | allow |
| `read` | 讀取檔案內容（支援行範圍）| allow（.env 除外）|
| `grep` | 正規表示式搜尋內容 | allow |
| `glob` | 萬用字元查找檔案 | allow |
| `list` | 列出目錄內容 | allow |
| `lsp`（實驗性）| LSP 查詢（定義跳轉、參考、hover 等）| allow |
| `patch` | 套用補丁 | allow |
| `skill` | 載入 SKILL.md 技能 | allow |
| `todowrite` | 管理待辦事項清單 | allow |
| `webfetch` | 擷取網頁內容 | allow |
| `websearch` | 網路搜尋（Exa AI，無需 API Key）| allow |
| `question` | 向使用者提問 | allow |

### question 工具的特殊用法

適用場景：
- 收集使用者偏好
- 釐清模糊指令
- 取得實作方案決策
- 提供方向選擇

每個問題含標題、正文、選項清單。使用者可選選項或輸入自訂答案。

### 底層實作

- `grep`、`glob`、`list` 底層使用 `ripgrep`
- 預設遵循 `.gitignore` 模式
- 建立 `.ignore` 檔案可覆寫（`!node_modules/`）

### 自訂工具覆寫

自訂工具與內建同名時，**自訂優先**：

```typescript
import { tool } from "@opencode-ai/plugin"

export default tool({
  description: "受限制的 bash",
  args: { command: tool.schema.string() },
  async execute(args) {
    if (args.command.includes("rm -rf")) {
      return "已阻擋危險命令"
    }
    // 執行...
  },
})
```

### MCP 伺服器整合

MCP 工具與內建工具並列。使用萬用字元管理：
```json
{
  "tools": {
    "mcp_*": "ask"
  }
}
```
