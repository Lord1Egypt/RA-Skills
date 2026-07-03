---
name: minimax-monitor
description: >
  Use when (1) user says "mmx 仪表盘启动" / "mmx monitor" / "MiniMax 配额查询" / "打开 minimax 监控" and wants a real-time dashboard.
  (2) user wants to check how much of their MiniMax Token Plan quota is left (4h / 24h / weekly windows for M3 / M2.7 / video / music / image models).
  (3) user wants to test MiniMax inference latency (TTFT / P50 / burst) by clicking "开始速率测试" - explicitly opt-in, NOT background.
license: MIT
metadata:
  version: "1.7.0"
  category: dev-tools
  author: wangjipeng
  sources:
    - https://github.com/MiniMax-AI/skills
permissions:
  - read:filesystem       # ~/.mmx/config.json (v1.7.0: 按需读,不缓存)
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

## v1.7.0 主要功能 (v1.6.7 → v1.7.0 增量)

### v1.7.0 安全加固

- 🔒 **凭证不在 server 进程内存中常驻**(v1.6.x → v1.7.0 重大变更)。每次需要 API key 的请求由 `loadKeyForRequest()` 现读 `~/.mmx/config.json`,用完即出栈,Node.js GC 一轮后释放。**进程内存 dump 拿不到完整 key**(lldb 验证: `memory find --string "sk-cp-"` 在 rw 段无命中)。
- 🔒 **`/api/load_cred` 不再写入模块作用域**。仅向前端返回"凭证已就绪"标记 + `keyLength`/`keyPrefix`(前 6 字符)。前端 `credLoaded=true` 现在是 UX 标记,不再控制权限。

### 安全 (v1.6.x 累计)

- 🔒 **本地凭证按需加载**。Server 启动**不读** `~/.mmx/config.json`。用户在仪表盘顶部点 "加载本地凭证" 按钮 + `confirm()` 二次确认后,才通过 `POST /api/load_cred` 读取 API key。Server 重启后 key 丢失(v1.7.0 起 key 也从不进 server 内存,仅磁盘上原生存在的 `~/.mmx/config.json`)。
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

1. **按需读取本地凭证(v1.7.0: 不进内存)**:从 `~/.mmx/config.json` 读取 `api_key`(MiniMax Token Plan key)。**仅在用户主动点击 "加载本地凭证" 按钮时才会读**(`POST /api/load_cred`),server 启动时**不**读。**v1.7.0 起**:读到的 key 不写进 server 进程内存,每次需要时由 `loadKeyForRequest()` 现读磁盘、用完即出栈。`POST /api/load_cred` 仅返回"已就绪"标记 + `keyLength`/`keyPrefix`,不返回完整 key。
2. **定时调用 MiniMax API**:每 60s 调 `https://www.minimaxi.com/v1/token_plan/remains` 拿配额数据。
3. **写入本地采样数据**:每次 `fetchQuota` 后向 `<skill-dir>/history.jsonl` 追加一行 `(timestamp, usedPct, modelSnapshot)`,保留最近 24h 滚动 buffer,供前端画趋势线。不存凭证、不存个人信息。
4. **速率测试需用户主动触发**:v1.6.0 起,仪表盘速率面板**不再自动**调用 chat completion。点 "开始速率测试" 按钮才会发起 5 次真实 chat 请求(约 180 token 上限),UI 会有红字提示 + 二次确认。

**不会做**:

- 不会把 API key 上传到任何远程(仅本地使用)。
- 不会在 `load_cred` 响应里返回 key。
- 不会把 key 存进 server 进程内存(v1.7.0 起);每次现读磁盘用完即出栈。
- 不会允许跨源网页调用本机 server(CORS allowlist 限定 `127.0.0.1 / localhost / file://`)。
- 不会接受空 Referer 调 `load_cred`(强制本机页面发起的请求才放行)。
- 不会在后台悄悄消耗你的 chat 配额(v1.6.0 起 probe 改按需触发;不点不动)。

**操作风险提示**:

- **本地凭证访问**:点击 "加载本地凭证" 按钮会让 server 拥有按需读 `~/.mmx/config.json` 的能力。**v1.7.0 起**:key 不会存进 server 进程内存,每次现读。建议:仅在本机使用本技能,不要把 9877 端口对外暴露。
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

- ❌ **Do not** auto-read `~/.mmx/config.json` on server startup. The credential is read **only** when the user explicitly clicks "加载本地凭证" (v1.6.0+).
- ❌ **Do not** cache the API key in module scope or process memory. `loadKeyForRequest()` must read from disk on every call (v1.7.0+).
- ❌ **Do not** return the API key in any HTTP response body. `POST /api/load_cred` returns `keyLength` + `keyPrefix` only (v1.6.1+).
- ❌ **Do not** accept empty `Referer` on `/api/load_cred`. Curl / CLI calls must include `-H 'Referer: http://127.0.0.1:9877/'` (v1.6.1+).
- ❌ **Do not** run the inference probe in the background or on a timer. Probe is button-only, confirm-required, ~180 token cost per click (v1.6.0+).
- ❌ **Do not** allow cross-origin web pages to reach the local server. CORS allowlist is `127.0.0.1 / localhost / file://` only (v1.4.0+).
- ❌ **Do not** claim "auto-read" or "in-memory" in any documentation. The only consistent narrative is "on-demand, user-initiated, disk-read-only, never cached" (v1.7.0+).

---

## Good vs. Bad Examples

| Scenario | ❌ Bad (v1.5.x and earlier) | ✅ Good (v1.7.0+) |
|----------|---------------------------|------------------|
| Server startup | Reads `~/.mmx/config.json` silently; loads key into module-scope variable | Reads nothing; no `credLoadedKey` module variable exists; reads disk on demand |
| User opens dashboard | Key is already in server module scope, all panels work | All panels work after first click (key read on demand); server memory is empty |
| `POST /api/load_cred` response | `{"ok":true, "key":"sk-cp-...real-key-here..."}` | `{"ok":true, "keyLength":125, "keyPrefix":"sk-cp-"}` |
| curl `load_cred` with no headers | `{"ok":true, "key":"..."}` (key leaked) | `403 {"ok":false, "error":"requires Referer from local origin"}` |
| Probe behavior | Background timer fires every 5 min, silently consumes quota | Button only; red warning + confirm() before firing; no background calls |
| Process memory dump (`lldb memory find`) | Full API key retrievable from module-scope variable | No key retrievable; only transient stack-frame string during HTTPS call |
| README "Configuration" section header | `### mmx Local Config (auto-read, recommended)` | `### mmx Local Config (on-demand, never cached, v1.7.0+)` |
| Frontend localStorage | Key persisted 24h via "Remember" toggle | No localStorage; user re-pastes key per session |

---

## Quality Bar

A **good** v1.7.0+ deploy of this skill satisfies:

- ✅ Server starts and listens on port 9877 without reading any local credentials (verify with `pgrep -fl mmx-monitor` then `lsof -p <pid> -P -n` shows no `~/.mmx/config.json` open).
- ✅ No module-scope variable named `credLoadedKey` / `loadedKey` / similar exists in `mmx-monitor-server.js`. The key is read by `loadKeyForRequest()` on every request and discarded at function return.
- ✅ `lldb -p <pid>` then `memory find --string "sk-cp-" <start> <size>` returns "data not found" in the process's writable memory regions (after at least one token_plan call has exercised the read path).
- ✅ Empty-Refefer `POST /api/load_cred` returns 403, not 200.
- ✅ Valid-Refefer `POST /api/load_cred` returns 200 with `key` field absent (only `keyLength` + `keyPrefix`).
- ✅ `GET /api/token_plan` works on first request (key is read from disk by `loadKeyForRequest()`); the "API key 未加载" 401 path is no longer reachable in normal flow.
- ✅ `<skill-dir>/history.jsonl` is created on first `token_plan` poll and is mentioned in `SKILL.md` Security section + this file.
- ✅ `SKILL.md` frontmatter `permissions:` lists `write:filesystem` (not just `read:filesystem`).
- ✅ No "auto-read" or "in-memory" wording remains in `README.md` / `README_zh.md` / `SKILL.md` after v1.7.0 changes.
- ✅ ClawHub security audit finding count for this skill drops to 0 after v1.7.0 publish (target).

A **bad** deploy:

- ❌ `key` field still in `load_cred` response (regression to v1.6.0 bug).
- ❌ Module-scope `credLoadedKey` variable reintroduced (regression to v1.6.x).
- ❌ `permissions:` missing `write:filesystem` (regression to v1.5.x).
- ❌ README still says "auto-read" or "in-memory" anywhere (audit trigger).
- ❌ Empty-Refefer `load_cred` returns 200 (regression).
