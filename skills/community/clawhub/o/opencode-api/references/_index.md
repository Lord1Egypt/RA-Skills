# references/ 索引

所有 OpenCode 詳細功能說明。按需讀取，不需要全部注入。

| 檔案 | 主題 | 大小參考 |
|------|------|----------|
| `agents.md` | 四種內建代理 + 自訂代理 + 溫度/max_steps | ~5KB |
| `sdk.md` | SDK 完整 API（端點表 + Python 對照 + 結構化輸出/事件監聽）| ~10KB |
| `formatters.md` | Formatters 格式化器 + Share 分享 + Keybinds 快捷鍵 | ~4KB |
| `config.md` | Config 完整 schema + 變數替換 + 環境變數 | ~5KB |
| `permissions.md` | Permissions 權限系統（細粒度規則 + 預設值）| ~4KB |
| `commands.md` | Commands 自訂指令（Markdown/JSON 格式 + 參數/Shell）| ~3KB |
| `tools.md` | Tools 內建工具一覽（14種工具 + question 工具用法）| ~3KB |
| `mcp.md` | MCP 伺服器（本地/遠端 + OAuth + 常見設定）| ~4KB |
| `lsp.md` | LSP 整合（27種內建 LSP + 設定方式）| ~4KB |
| `providers.md` | Provider 設定（LM Studio / Ollama / 自訂 Provider）| ~4KB |
| `server.md` | Server 部署（HTTP Server + 認證 + API 端點總表）| ~6KB |
| `code-review-prompt.md` | Code Review 完整 Prompt（11 面向 + Minecraft-Translate 專用語境）| ~5KB |

## 快速參考

### Agents → `agents.md`
- 四種內建代理（build/plan/general/explore）
- 自訂代理（JSON / Markdown）
- 溫度 / max_steps / default_agent

### SDK → `sdk.md`
- 所有 HTTP API 端點
- Python 對照表
- 結構化輸出（JSON Schema）
- noReply 模式
- 事件監聽（SSE）
- session 管理（abort/share/revert）

### Config → `config.md`
- 設定檔位置優先順序
- 所有 schema 欄位
- 變數替換（{env:VAR} / {file:path}）
- compaction / watcher 設定

### Permissions → `permissions.md`
- 細粒度物件語法
- 所有權限鍵
- 萬用字元模式
- 預設值（.env 預設拒絕）
- 按代理覆寫

### Commands → `commands.md`
- Markdown 格式（frontmatter）
- 參數佔位符（$ARGUMENTS / $1/$2）
- Shell 輸出注入（!`cmd`）
- subtask 隔離

### Tools → `tools.md`
- 14 種內建工具
- question 工具（向使用者提問）
- ripgrep 底層 + .ignore 覆寫

### MCP → `mcp.md`
- 本地 / 遠端 MCP
- OAuth 認證流程
- Sentry / Context7 / GitHub Grep 設定範例
- 按代理啟用策略

### LSP → `lsp.md`
- 27 種內建 LSP 伺服器
- goToDefinition / findReferences 等操作
- 環境變數 / 初始化選項

### Server → `server.md`
- HTTP Server 部署
- Basic Auth 認證
- 所有 API 端點（完整表）
- TUI 控制端點

### Formatters → `formatters.md`
- ruff / biome / prettier 等設定
- 分享模式（manual/auto/disabled）
- 常用快捷鍵速查

### Code Review → `code-review-prompt.md`
- 11 面向審查框架（正確性/邏輯/可讀性/可維護性/效能/安全/可觀測性/向後相容/相依性/歸屬/測試）
- 結構化輸出格式（Blocking / Non-blocking / Optional）
- Minecraft-Translate 專用注入語境
- 使用方式：直接注入 session 或作為自訂 agent system prompt
