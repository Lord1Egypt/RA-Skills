# 安装指引：GitHub 下载 → 本地运行

目标：在 **10–15 分钟** 内帮用户完成测试网配置预览。默认不下单、不进实盘。

> 对用户用人话推进「帮我启动机器人」；密钥不要读取或展示。环境、代理等问题尽量自行处理。

## 0. 先确认两件事

1. 用户是否已有 GitHub 仓库副本（clone / download zip）
2. 本机是否可运行 **Python 3.10+**（推荐 3.12；勿用 macOS 自带常为 3.9 的 `python3`）

仓库地址：

```text
https://github.com/trade-upnow/helix-trader
```

若用户还没有仓库，引导：

```bash
git clone https://github.com/trade-upnow/helix-trader.git
cd helix-trader
```

## 1. 首次配置（推荐）

在仓库根目录：

```bash
bash scripts/setup_backend.sh
```

脚本会：

- 优先用 `python3.12` / `3.11` / `3.10` 创建虚拟环境（**不用** macOS 自带常为 3.9 的 `python3`，否则 ccxt 等依赖可能装失败）
- 按「直连 www.okx.com → 试 7890 → 再问用户」决定 pip 是否走代理  
  （OKX 探测只用于判断网络/代理，**不等于**默认选用 OKX 交易所）

若本机只有 3.9：

```bash
brew install python@3.12
HELIX_PYTHON=python3.12 bash scripts/setup_backend.sh
# 或：python3.12 -m venv backend/.venv
```

请用户**本地**编辑 `backend/.env`：

| 变量 | 说明 |
|------|------|
| `HELIX_USERNAME` / `HELIX_PASSWORD` | Agent CLI 登录用；也可用 `ADMIN_*` |
| `ADMIN_USERNAME` / `ADMIN_PASSWORD` | **前端登录用这对**（默认常见 `admin` / `ChangeMe123!`）；不要引导用 `CLIENT_*` |
| `JWT_SECRET` | 改成长随机串 |
| `API_ENCRYPTION_KEY` | 可选，新手留空（由 `JWT_SECRET` 派生）；已保存交易所凭证后不要乱改、不要回显 |
| `EXCHANGE_PROXY_URL` | 可选；直连通时可留空 |

## 2. 启动后端

```bash
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

验证：访问 `http://127.0.0.1:8000/health` 应返回 `{"status":"ok"}`。

## 3. 连接本机 MCP（可选）

要通过 Agent 调机器人工具，需在本机配置 MCP。模板在**用户 clone 的运行时仓库**里（不在本技能目录内）：

1. 确认用户已 clone 运行时并启动后端（见上文）  
2. 参考运行时 `examples/mcp/README.md`，选用对应宿主模板：  
   - `examples/mcp/claude_desktop.example.json`  
   - `examples/mcp/codex.example.toml`  
   - `examples/mcp/.mcp.json.example`（Claude Code；Cursor 可复制内容到 `.cursor/mcp.json`）  
   - 说明：`docs/MCP_SETUP.md`  
3. 把 `cwd` 改成该机器上 `.../helix-trader/backend` 的绝对路径，重启宿主后先 `doctor`

## 4. 最小闭环（CLI）

另开终端：

```bash
cd backend
source .venv/bin/activate
python -m app.agent doctor
python -m app.agent login
python -m app.agent mode
python -m app.agent strategies
# 对话里先问用户：交易所 okx/binance；策略默认推荐 trend_following_core
python -m app.agent preview \
  --strategy trend_following_core \
  --exchange okx \
  --symbol BTC/USDT:USDT \
  --testnet
```

说明：

- `login` 会把 token 缓存到 `backend/.helix-agent-token`（已 gitignore）
- **preview 不能省**；用户确认预览前不要 start
- CLI 里的 `--exchange okx` 只是示例，Agent 要先问用户选哪个交易所

## 5. 保存测试网交易所凭证

先问用户用 **OKX 还是 Binance**，再保存。凭证以**后端数据库**为准；填进 `.env` ≠ 已保存。

```bash
# 路径 A（长期复用）：.env 作输入源，再写入后端
# 编辑 backend/.env：HELIX_EXCHANGE_API_KEY / SECRET（OKX 还需 PASSPHRASE）
python -m app.agent save-credentials --exchange okx --testnet --confirm-save-credentials

# 路径 B（首次推荐）：交互输入，可不写 .env 交易所密钥
python -m app.agent save-credentials --exchange okx --testnet --prompt --confirm-save-credentials
```

`--prompt` 成功后 `.env` 里 `HELIX_EXCHANGE_*` 为空也正常。判断是否配好：用 `doctor` / `mode`，**禁止 grep .env**。  
OKX Passphrase = 创建 API Key 时设置的 API 密码短语，不是登录密码或资金密码。  
测试网与实盘是两套 Key。

## 6. 用户常说的话

```text
帮我启动这个机器人
```

```text
帮我启动机器人，先预览配置；策略你推荐一个就行
```

```text
现在是模拟盘还是实盘？
```

## 7. 启动策略时的强制顺序

`doctor` → `login`（如需）→ **问交易所** → `get_runtime_mode` → 保存凭证（如需）→ `list_strategies` → **问策略（默认推荐趋势）** → **`preview_bot_config`** → **用户确认** → `start_bot` → **主动问要不要开本地网页**

实盘额外要求：本地 `HELIX_ALLOW_LIVE_TRADING=true` + `confirm_live_trading=true` + 用户明确确认。

## 卡住了

引导用户查看仓库内：

- `docs/TROUBLESHOOTING.md`
- `docs/OKX_CREDENTIALS.md`
- `docs/MCP_SETUP.md`
- `docs/OPERATIONS.md`（可选网页）
