# MCP Client Setup（Claude Desktop / Cursor / VS Code / Windsurf）

## Step 1 — Install

```bash
npm install -g @okx_ai/okx-trade-mcp @okx_ai/okx-trade-cli
```

驗證安裝成功（唔需要 API key）：
```bash
okx market ticker BTC-USDT
```

## Step 2 — 配置 API Credentials

```bash
okx config init
```

呢個係互動式 wizard，跟住做就係。完成之後會係 `~/.okx/config.toml` 生成設定檔。

或者手動建立 `~/.okx/config.toml`：

```toml
default_profile = "demo"

[profiles.demo]
api_key    = "your-demo-api-key"
secret_key = "your-demo-secret-key"
passphrase = "your-demo-passphrase"
demo       = true

[profiles.live]
api_key    = "your-live-api-key"
secret_key = "your-live-secret-key"
passphrase = "your-live-passphrase"
# 歐洲用戶加: site = "eea"
# 美國用戶加: site = "us"
```

## Step 3 — 連接 AI Client

```bash
okx-trade-mcp setup --client <client>
```

| Client | `<client>` 值 |
|--------|--------------|
| Claude Desktop | `claude-desktop` |
| Claude Code | `claude-code` |
| Cursor | `cursor` |
| VS Code | `vscode` |
| Windsurf | `windsurf` |
| Windsurf | `windsurf` |

## 4 層安全保護

| Layer | 說明 |
|-------|------|
| `--demo` | 模擬資金，零真錢風險 |
| `--read-only` | 只能查數據，禁止下單 |
| Smart Registration | 啟動時驗 API 權限，無權限嘅 tools 唔顯示 |
| Risk Labels | 涉錢 tools 標 `[CAUTION]`，AI 會先確認 |


| 需求 | 指令 |
|------|------|
| 只要行情（唔需要 key） | `okx-trade-mcp --modules market` |
| Demo 模式，全功能 | `okx-trade-mcp --profile demo --modules all` |
| Live，只讀監控 | `okx-trade-mcp --profile live --read-only` |
| Live，只做 Spot | `okx-trade-mcp --profile live --modules market,spot` |
| Live，合約 + 期權 | `okx-trade-mcp --profile live --modules market,swap,option` |
