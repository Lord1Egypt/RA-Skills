# Agent 引导剧本

给 Codex / Claude 等 Agent 使用。格式：用户可能问什么 → 先调用哪些工具 → 怎么回答 → 不能做什么。

完整工具表见同目录 `TOOLS.md`。安装步骤见同目录 `INSTALL.md`。经验说明见同目录 `EXPERIENCE.md`。

---

## 对用户说话的总原则

1. 用户常见说法是「帮我启动这个机器人」，不是「请检查虚拟环境」。
2. 密钥保护是你的硬规则，不要让用户念「不要读取或展示任何密钥值」。
3. 必须保留策略预览：先问交易所、问策略（默认推荐趋势），再 `preview_bot_config`，确认后才启动。
4. 不要静默默认 OKX；网络探测用 www.okx.com 只判断代理，不等于选用 OKX。
5. 首次配置成功后，主动问要不要开本地网页；登录用 `ADMIN_USERNAME` / `ADMIN_PASSWORD`（常见默认 `admin` / `ChangeMe123!`），不要用 `CLIENT_USERNAME`。
6. `API_ENCRYPTION_KEY` 新手留空即可；不回显、保存凭证后不乱改。
7. 配 MCP 时用用户已 clone 的运行时仓库 `examples/mcp/` 与 `docs/MCP_SETUP.md`，`cwd` 改成本机 `backend` 绝对路径。

---

## 场景 A：这份代码 / 技能是干嘛的？

**用户可能问**

- “这份技能是做什么的？”
- “Helix Trader 能帮我赚钱吗？”

**应怎么回答**

- 定位：本地加密货币策略控制工具；从 GitHub 下载机器人，在用户本机安全使用（非云端代盘、不承诺收益）。
- 交易始终在用户本机；不是收益承诺产品。
- 下一步：直接说可以帮他完成首次配置并做测试网预览。

**不能做什么**

- 不承诺收益。密钥不回显（无需用户提醒）。

---

## 场景 B：支持什么策略？

**应先调用**

1. `list_strategies`
2. 如需参数细节：`explain_parameters`

**应怎么回答**

- `trend_following_core`（趋势跟随，**默认推荐**）
- `trend_breakout_accel`（突破动量）
- 说明风险与适用行情；不保证盈利。

---

## 场景 C：帮我启动机器人（最常见）

**用户可能问**

- “帮我启动这个机器人”
- “我要怎么启动”
- “帮我启动，策略你推荐一个，先预览”

**必须顺序**

1. `doctor`
2. 缺环境则跑 `bash scripts/setup_backend.sh` / 启动后端
3. 必要时 `login`
4. **问交易所**：OKX 还是 Binance
5. `get_runtime_mode`；未配置则按所选交易所保存测试网凭证（Path A：`.env`+save，或 Path B：`--prompt`；以 doctor/mode 为准，勿 grep `.env`）
6. `list_strategies`；**推荐趋势**，也可选突破
7. **`preview_bot_config`（必做）**，展示摘要
8. 用户确认后 `start_bot`（默认测试网）
9. 主动问要不要启动本地网页（`frontend/`）

**不能做什么**

- 跳过 preview
- 不询问就默认 OKX 或某个策略并直接启动

---

## 场景 D：需要哪些配置？ / Passphrase

用人话列缺口：登录账号、交易所 API（先问用哪家）、凭证要保存进后端、网络代理（按 doctor.network）。  
OKX Passphrase 是创建 API 时自己设的短语，不是登录密码。

---

## 场景 E：报错了？

| 现象 | 优先工具 | 恢复方向 |
|------|----------|----------|
| 首次还不能跑 | `doctor` | setup + 起后端 |
| Missing access token | `login` | 重新登录 |
| mode=`not_configured` | `get_runtime_mode` | 保存凭证到后端（`--prompt` 或 `.env`+save；勿看 `.env` 空值误判） |
| 访问不了交易所网络 | `doctor.network` | 直连→7890→问代理 |
| 交易对不可用 | `list_markets` | 换符号后再 preview |
| 用户说停止/关掉策略 | 先 `get_bot_status`；有仓且未说平仓 → **先问**只停还是停并平 | 勿默认 `close_all=true` |
| stop 后账户仍有仓 | `get_bot_status` | 只平机器人仓 |

---

## 场景 F：停止机器人（未说是否平仓）

**用户可能问**

- “停止机器人”
- “关掉策略”
- “停一下”

**应先调用**

1. `get_bot_status`（看是否有仓）

**应怎么回答**

- 若有仓且用户没说平仓：明确问「只停止策略、保留仓位，还是同时平掉机器人管理的仓位？」
- 用户选保留：`stop_bot(close_all=false, confirm_stop_keep_positions=true)`
- 用户选平仓：说明只平机器人仓 → 确认后 `stop_bot(close_all=true, confirm_close_all=true)`
- 无仓：可直接 `stop_bot(close_all=false)`

**不能做什么**

- 把「停止」理解成默认平仓
- 未询问就传 `close_all=true` / `confirm_close_all=true`

---

## 用户常说的话（示例）

```text
帮我启动这个机器人
```

```text
帮我启动机器人，先预览配置；策略你推荐一个就行
```

```text
现在是模拟盘还是实盘？
```
