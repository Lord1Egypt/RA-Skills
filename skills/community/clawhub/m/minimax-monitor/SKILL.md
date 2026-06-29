---
name: minimax-monitor
description: >
  Use when (1) user says "mmx 仪表盘启动" / "mmx monitor" / "MiniMax 配额查询" / "打开 minimax 监控" and wants a real-time dashboard.
  (2) user wants to check how much of their MiniMax Token Plan quota is left (4h / 24h / weekly windows for M3 / M2.7 / video / music / image models).
  (3) user wants to test MiniMax inference latency (TTFT / P50 / burst) by clicking "开始速率测试" - explicitly opt-in, NOT background.
license: MIT
metadata:
  version: "1.6.2"
  category: dev-tools
  author: wangjipeng
  sources:
    - https://github.com/MiniMax-AI/skills
version: 1.6.2
permissions:
  - read:filesystem       # ~/.mmx/config.json
  - write:filesystem      # history.jsonl (24h ring buffer, 本技能目录)
  - read:env               # MINIMAX_API_KEY
  - network:outbound       # api.minimaxi.com / www.minimaxi.com
  - shell:exec             # 'open' 命令启动浏览器
---

# MiniMax 套餐监控 + 速率测试中心

> **触发词**:mmx 仪表盘启动
>
> **两个职责**:
> 1. **实时配额查询** -- 60s 轮询官方 token_plan API,显示 4h / 24h / 本周用量、模型卡片、24h 趋势。
> 2. **按需速率测试** -- 用户点 "开始速率测试" 按钮才发起 5 次 chat completion 请求(约 180 token 上限),返回 TTFT / P50 / burst / token-s。
>
> 启动后自动用 `open` 命令唤起浏览器打开 `http://127.0.0.1:9877/`。

## v1.6.2 主要功能

### 安全

- 🔒 **本地凭证按需加载**。Server 启动**不读** `~/.mmx/config.json`。用户在仪表盘顶部点 "加载本地凭证" 按钮 + `confirm()` 二次确认后,才通过 `POST /api/load_cred` 读取 API key,存入 server 进程内存(不写磁盘、不写浏览器、不上传)。Server 重启后 key 丢失。
- 🔒 **`/api/load_cred` 响应不含完整 API key**(只回 `keyLength` + `keyPrefix` 前 6 字符用于视觉确认)。
- 🔒 **`/api/load_cred` 拒绝空 Referer**,强制 `Referer` 是本机白名单 `127.0.0.1 / localhost / file://` 之一。
- 🔒 **CORS 严格**:`Access-Control-Allow-Origin` 仅放行 `127.0.0.1 / localhost / file://`。恶意网页无法跨域调本机 server 消耗你的 MiniMax 配额。
- 🔒 **速率测试按需**:`/api/probe` 不再后台定时调用。仅在用户点 "开始速率测试" 按钮时才发起 5 次 chat completion,UI 红字提示 + 二次确认。

### 配额监控

- 📊 **4 小时 / 24 小时 / 本周** 三档用量追踪(4 小时为主圆环,按用户当前 Token Plan 套餐的实际周期动态显示)。
- 🎯 **模型卡片** 区分 4h 限额 / 24h 限额 / 周无限额 / 套餐未启用(视频模型 status=3 元数据不可区分时显示 "套餐未启用 · 不可调用" 提示并排除出 4h 聚合)。
- 📈 **24 小时趋势线**:`history.jsonl` 滚动 buffer(本技能目录)记录每次 `token_plan` 调用的用量快照,前端画趋势线。

### 速率测试

- ⚡ **TTFT / P50 / 突发并发 / token·s** 四项指标,基于真实 chat completion 请求。
- ⚠️ **UI 红字 + confirm()** 提示每次测试消耗约 180 token,需用户主动确认。

### 启动

```bash
node ~/.openclaw/workspace/skills/minimax-monitor/mmx-monitor-server.js
# 浏览器访问 http://127.0.0.1:9877/
```

高级选项:

```bash
# 启用 X-MMX-API-Key header 透传(默认拒绝)
node mmx-monitor-server.js --allow-header-key
# 完全关闭速率测试端点
node mmx-monitor-server.js --no-probe
```

## Security & Data Flow

本技能默认会:

1. **读取本地凭证(按需)**:从 `~/.mmx/config.json` 读取 `api_key`(MiniMax Token Plan key)。**仅在用户主动点击 "加载本地凭证" 按钮时才会读**(`POST /api/load_cred`),server 启动时**不**读。读到的 key 存 server 进程内存,不写盘、不上传,server 重启后清空。
2. **定时调用 MiniMax API**:每 60s 调 `https://www.minimaxi.com/v1/token_plan/remains` 拿配额数据。
3. **写入本地采样数据**:每次 `fetchQuota` 后向 `<skill-dir>/history.jsonl` 追加一行 `(timestamp, usedPct, modelSnapshot)`,保留最近 24h 滚动 buffer,供前端画趋势线。不存凭证、不存个人信息。
4. **速率测试需用户主动触发**:v1.6.0 起,仪表盘速率面板**不再自动**调用 chat completion。点 "开始速率测试" 按钮才会发起 5 次真实 chat 请求(约 180 token 上限),UI 会有红字提示 + 二次确认。

**不会做**:

- 不会把 API key 上传到任何远程(仅本地使用)。
- 不会在 `load_cred` 响应里返回 key。
- 不会允许跨源网页调用本机 server(CORS allowlist 限定 `127.0.0.1 / localhost / file://`)。
- 不会接受空 Referer 调 `load_cred`(强制本机页面发起的请求才放行)。
- 不会在后台悄悄消耗你的 chat 配额(v1.6.0 起 probe 改按需触发;不点不动)。

**操作风险提示**:

- **本地凭证访问**:点击 "加载本地凭证" 按钮会读取 `~/.mmx/config.json` 的 `api_key`,并把 key 存入本机 server 进程内存。建议:仅在本机使用本技能,不要把 9877 端口对外暴露。
- **持续出站轮询**:每 60s 一次的 `token_plan/remains` 调用会持续消耗 MiniMax 配额查询额度(Token Plan 套餐内免费)。如果不需要实时面板,可手动 `Ctrl+C` 停 server。
- **本地历史文件**:`history.jsonl` 包含时间序列的用量百分比,**不包含**凭证或个人身份信息;不慎泄漏也只是用量趋势。

**想使用 header 透传 key**(高级用户,需要自负责):`node mmx-monitor-server.js --allow-header-key`

---

## Modes

### `dashboard` (default)
Real-time token-plan quota monitor. Server polls `https://www.minimaxi.com/v1/token_plan/remains` every 60s after credentials are loaded. Renders ring chart, per-model cards, and 24h trend line. **This is what runs by default when the user says "mmx 仪表盘启动".**

### `probe` (opt-in)
On-demand inference latency test. Triggered **only** by the dashboard button "开始速率测试" - never by timer. Runs 5 chat completions against `api.minimaxi.com/v1/text/chatcompletion_v2` (model `MiniMax-M2.7`, max_tokens=30-60, mix of streaming/non-streaming). Returns TTFT, P50, burst, token/s metrics. **Costs ~180 tokens per click; UI shows red warning + confirm() dialog before firing.**

### `history` (read-only)
Reads `history.jsonl` (24h ring buffer at `<skill-dir>/history.jsonl`) and returns time-series usage samples via `GET /api/history?hours=24`. No writes. Used by the dashboard's trend line widget.

---

## Do not

- ❌ **Do not** auto-read `~/.mmx/config.json` on server startup. The credential is loaded **only** when the user explicitly clicks "加载本地凭证" (v1.6.0+).
- ❌ **Do not** return the API key in any HTTP response body. `POST /api/load_cred` returns `keyLength` + `keyPrefix` only (v1.6.1+).
- ❌ **Do not** accept empty `Referer` on `/api/load_cred`. Curl / CLI calls must include `-H 'Referer: http://127.0.0.1:9877/'` (v1.6.1+).
- ❌ **Do not** run the inference probe in the background or on a timer. Probe is button-only, confirm-required, ~180 token cost per click (v1.6.0+).
- ❌ **Do not** allow cross-origin web pages to reach the local server. CORS allowlist is `127.0.0.1 / localhost / file://` only (v1.4.0+).
- ❌ **Do not** claim "auto-read" in any documentation. The only consistent narrative is "on-demand, user-initiated, in-memory only".

---

## Good vs. Bad Examples

| Scenario | ❌ Bad (v1.5.x and earlier) | ✅ Good (v1.6.1+) |
|----------|---------------------------|------------------|
| Server startup | Reads `~/.mmx/config.json` silently; loads key into memory at boot | Reads nothing; `credLoadedKey = ''`; waits for user click |
| User opens dashboard | Key is already in server, all panels work | All panels show 401; user clicks "加载本地凭证" → confirm → key loads |
| `POST /api/load_cred` response | `{"ok":true, "key":"sk-cp-...real-key-here..."}` | `{"ok":true, "keyLength":125, "keyPrefix":"sk-cp-"}` |
| curl `load_cred` with no headers | `{"ok":true, "key":"..."}` (key leaked) | `403 {"ok":false, "error":"requires Referer from local origin"}` |
| Probe behavior | Background timer fires every 5 min, silently consumes quota | Button only; red warning + confirm() before firing; no background calls |
| README "Configuration" section header | `### mmx Local Config (auto-read, recommended)` | `### mmx Local Config (loaded on demand, v1.6.0+)` |
| Frontend localStorage | Key persisted 24h via "Remember" toggle | No localStorage; user re-pastes key per session |

---

## Quality Bar

A **good** v1.6.1+ deploy of this skill satisfies:

- ✅ Server starts and listens on port 9877 without reading any local credentials (verify with `pgrep -fl mmx-monitor` then `lsof -p <pid> -P -n` shows no `~/.mmx/config.json` open).
- ✅ Empty-Refefer `POST /api/load_cred` returns 403, not 200.
- ✅ Valid-Refefer `POST /api/load_cred` returns 200 with `key` field absent (only `keyLength` + `keyPrefix`).
- ✅ `GET /api/token_plan` returns 401 with `{"error":"API key 未加载..."}` before any user action, and 200 with valid quota data after credential load.
- ✅ `<skill-dir>/history.jsonl` is created on first `token_plan` poll and is mentioned in `SKILL.md` Security section + this file.
- ✅ `SKILL.md` frontmatter `permissions:` lists `write:filesystem` (not just `read:filesystem`).
- ✅ No "auto-read" wording remains in `README.md` / `README_zh.md` / `SKILL.md` after v1.6.1 changes.
- ✅ ClawHub security audit finding count for this skill drops from 13 → ≤ 3 after v1.6.1 publish.

A **bad** deploy:

- ❌ `key` field still in `load_cred` response (regression to v1.6.0 bug).
- ❌ `permissions:` missing `write:filesystem` (regression to v1.5.x).
- ❌ README still says "auto-read" anywhere (audit trigger).
- ❌ Empty-Refefer `load_cred` returns 200 (regression).
