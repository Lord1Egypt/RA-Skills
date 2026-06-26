---
name: okx-agent-tradekit
description: >
  Setup, install, and use OKX Agent Trade Kit — the official OKX toolkit for AI-powered trading.
  Use this skill whenever the user mentions: OKX trading, agent tradekit, okx-trade-mcp, okx Skills,
  installing OKX on OpenClaw, configuring OKX API keys, trading BTC/ETH/crypto with natural language,
  spot/futures/options/grid bots on OKX, or wants to connect an AI agent to OKX exchange.
  Trigger this skill even if the user just says "想用 OKX 交易" or "幫我裝 OKX" or "OKX MCP".
  Covers: installation (OpenClaw Skills or MCP), API key config, natural language trading commands,
  demo mode setup, and explaining what the toolkit does and how it works.
---

# OKX Agent Trade Kit Skill

OKX Agent Trade Kit 係 OKX 官方出嘅 open-source toolkit，讓 AI agent 直接用自然語言執行交易。

## Overview

三種使用方式：
1. **Skills（OpenClaw 用戶首選）** — `npx skills add okx/agent-skills`，一行搞掂
2. **MCP Server** — 適合 Claude Desktop、Claude Code、Cursor、VS Code
3. **CLI** — terminal 直接落指令，可以 pipe 入 script

---

## 流程判斷

```
用戶係用 OpenClaw？
  ├─ Yes → 用 Skills 安裝方式（最快，一行指令）
  └─ No  → 用 MCP 安裝方式（npm install + setup）

用戶想交易？
  ├─ 先確認有無配置 API key
  ├─ 建議先用 demo 模式測試
  └─ 提醒用 sub-account API key，唔好用 main account
```

---

## 安裝：OpenClaw（Skills 方式）⭐ 推薦

### Step 1 — 安裝 Skills

直接係 **OpenClaw chat 入面** 貼呢句（唔係 terminal）：

```
Run `npx skills add okx/agent-skills`, resolve any issues you encounter, then check the BTC price.
```

呢個會自動裝好四個 skills：
| Skill | Package | 功能 | 需要 API Key？ |
|-------|---------|------|--------------|
| Market Data | `okx-cex-market` | 實時行情、K 線、資金費率、未平倉量 | ❌ 唔需要 |
| Trading | `okx-cex-trade` | Spot、合約、期權、Algo 訂單、Grid Bot | ✅ 需要 |
| Portfolio | `okx-cex-portfolio` | 餘額、持倉、P&L、帳單、手續費率 | ✅ 需要 |
| Bots | `okx-cex-bot` | Grid Bot（現貨/合約）、DCA 策略 | ✅ 需要 |

### Step 2 — 配置 API Key

打開 **Terminal**，執行：

```bash
mkdir -p ~/.okx && cat > ~/.okx/config.toml << 'EOF'
default_profile = "demo"

[profiles.live]
api_key    = "your-live-api-key"
secret_key = "your-live-secret-key"
passphrase = "your-live-passphrase"

[profiles.demo]
api_key    = "your-demo-api-key"
secret_key = "your-demo-secret-key"
passphrase = "your-demo-passphrase"
demo       = true
EOF
```

之後用文字編輯器開 `~/.okx/config.toml`，填入真實嘅 API credentials。

**去哪攞 API Key？** → https://www.okx.com/account/my-api
- ✅ 建議先攞 **demo key** 試用
- ✅ 用 **sub-account** 嘅 API key，唔好用 main account
- ⚠️ 永遠唔好將 API key 貼入 chat 入面

---

## 安裝：MCP Clients（Claude Desktop / Cursor / VS Code）

詳細步驟見 → [references/mcp-setup.md](references/mcp-setup.md)

---

## 自然語言交易指令示例

裝好之後，可以直接係 AI chat 入面講：

```
# 行情查詢（唔需要 API key）
What's the BTC price on OKX?
Show BTC-USDT order book
BTC-USDT-SWAP 嘅資金費率係幾多？

# 帳戶（需要 API key）
Show my account balance
我而家有咩持倉？

# 交易（demo 模式，無風險）
Buy 100 USDT of BTC at market on demo
Set a limit buy for 0.01 BTC at 80000 on demo
Place a stop-loss at 84000 for my BTC-USDT-SWAP long

# Grid Bot
Create a BTC grid bot between 80000 and 100000 with 10 grids and 100 USDT
```

---

## 安全提示（每次涉及交易時都要提醒）

1. **永遠唔好** 將 API Key 貼入 chat — 只放喺 `~/.okx/config.toml`
2. 用 **sub-account** 專門做 AI trading，唔好用 main account，**唔好開 withdrawal 權限**
3. 先用 **demo mode** 測試，確認無問題先 switch 去 live
4. 只開放需要嘅 API 權限（唔需要提款權限就唔開）
5. AI 係 non-deterministic，**唔可以完全依賴**，重大決策要人工確認

Agent Trade Kit 有 **4 層內建安全保護**：
- `--demo` Demo 模式 — 模擬資金，唔會動真錢
- `--read-only` 只讀模式 — 只能查數據，無法下單
- **Smart Registration** — 啟動時自動檢查 API Key 權限，Key 唔能交易嘅話 order tools 根本唔會顯示畀 AI
- **Risk Labels** — 所有涉及金錢操作嘅 tool 都標 `[CAUTION]`，AI 會先確認再執行

---

## 常見問題

**Q: 點解 market data 唔需要 API key？**
A: OKX 市場數據係公開嘅，`market` module 直接 call 公開 API。

**Q: demo 同 live 有咩分別？**
A: demo 用模擬資金，config.toml 入面 `demo = true` 就係 demo 模式。

**Q: 我係歐洲用戶 / 美國用戶點辦？**
A: 要係 config.toml 加 `site = "eea"` (歐洲) 或 `site = "us"` (美國)。

**Q: 裝唔到 / 有 error 點辦？**
A: 確認 Node.js 已安裝（`node --version`），要求 Node.js 18+。

---

## 參考資料

- 官方文檔：https://www.okx.com/docs-v5/agent_en/
- GitHub：https://github.com/okx/agent-trade-kit
- 完整 tool 列表：見 [references/tools-reference.md](references/tools-reference.md)
- MCP 安裝詳細步驟：見 [references/mcp-setup.md](references/mcp-setup.md)
