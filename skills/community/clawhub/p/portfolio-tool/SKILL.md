---
name: portfolio-tool
description: 通过 portfolio-tool MCP Server 对话式操作 Portfolio_tool 基金组合研究工具的后端。当用户想用自然语言查询基金组合、同步基金净值、查看组合跟踪状态、搜索基金或管理匿名账号时使用。MCP 由后端 FastAPI 应用挂载提供，同时支持 Streamable HTTP 与 SSE 两种传输，无需单独启动服务或 stdio 进程。
agent_created: true
---

# Portfolio_tool MCP 访问 Skill

本 Skill 配合 `portfolio-tool` MCP Server 使用。MCP 端点由**后端 FastAPI 应用自身挂载**——FastMCP 与 REST API 运行在**同一个 uvicorn 进程**，**无需单独启动 MCP 服务，也不提供 stdio 进程**。挂载后同时提供两种传输，客户端任选其一：

- **Streamable HTTP（推荐，MCP 2025 规范，单端点）**：`https://invest.geeyo.com/mcp/http`
- **SSE（兼容旧客户端）**：`https://invest.geeyo.com/mcp/sse`

启用方式：在后端 `.env` 设置 `MCP_ENABLED=True` 并重启后端即可。

MCP 将后端 REST API 封装为结构化工具，Agent 直接调用即可，无需关心底层 HTTP 细节。

## 何时使用

- 用户要求「列出我的组合」「查看组合 12 的详情」「同步基金净值」「搜索基金 000001」「绑定账号」等
- 需要查看某只基金净值、组合跟踪状态（最新净值 / 数据截至日 / 涨跌）
- 需要在新设备通过账号密码找回组合数据

## 身份认证：基于数字指纹的匿名身份

「我的组合」与写操作均需用户身份。本服务采用**数字指纹（Device Fingerprint）**方案：由调用 MCP 的客户端 Agent 在**用户本机**根据固定机器特征计算一个稳定不变的 UUID 作为身份，并在连接时携带。**禁止由后端/服务器代生成**——否则所有用户会变成同一个服务器身份，互相串号。

### 1. 生成数字指纹（本机算法）

在用户本机，用以下固定特征计算稳定 ID（同一机器恒定不变）：

1. 优先读取本机唯一标识（取第一个可读到的）：
   - Linux：`/etc/machine-id`、`/var/lib/dbus/machine-id`、`/etc/hostid`
   - Windows：注册表 `HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Cryptography\MachineGuid`
2. 兜底（上述均不可读时）：拼接 `主机名 + MAC 地址 + 系统用户名 + 操作系统名`
3. 对特征串做 SHA-256，取前 128 bit，格式化为 UUID：`xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`
4. 持久化：首次生成后写入 `~/.portfolio/aid`（一行）；后续所有会话/重启均读取同一 ID，不再生成新的，组合数据始终归属同一用户。

> 此 UUID 同源承担两个角色：**用户身份 `anonymous_id`** 与 **设备指纹 `fingerprint`**，既是 `~/.portfolio/aid` 内容，也是连接 MCP 时 `X-Anonymous-Id` 请求头的值。

伪代码：
```
raw = read_machine_id() or (hostname + mac + username + os)
h   = sha256(raw).hexdigest()
fp  = f"{h[0:8]}-{h[8:12]}-{h[12:16]}-{h[16:20]}-{h[20:32]}"
if not exists("~/.portfolio/aid"):
    write("~/.portfolio/aid", fp)
```

### 2. 自动注册接口

身份就绪后，MCP 会在**首次工具调用（如 `get_me`、`list_portfolios(mine=true)`、`bind_account`）时自动**向后端发起注册请求，无需手动调用；只需保证每次连接都携带同一个 `X-Anonymous-Id`。接口契约：

- 接口：`POST /api/user/init`
- 请求头：`Content-Type: application/json`、`Accept: application/json`
- 请求体：

  | 字段 | 类型 | 说明 |
  |---|---|---|
  | `anonymous_id` | string（≤64） | 数字指纹 UUID（`~/.portfolio/aid` 内容，亦为 `X-Anonymous-Id` 头的值） |
  | `fingerprint` | string（≤256） | 设备指纹哈希，与 `anonymous_id` 同源，当前统一传同一 UUID |

- 响应体：

  | 字段 | 类型 | 说明 |
  |---|---|---|
  | `anonymous_id` | string | 后端确认的用户标识（与请求一致） |
  | `is_new` | bool | `true`=新建；`false`=已存在（仅刷新活跃时间） |
  | `risk_agreed` | bool | 是否已同意风险揭示书 |

- 幂等性：同一 `anonymous_id` 重复调用返回已存在用户（`is_new=false`），不重复建号。
- 传递方式：`anonymous_id` 既作为 `X-Anonymous-Id` 请求头在每个 MCP/REST 请求携带，也作为 init 请求体字段；`fingerprint` 仅作为 init 请求体字段。`X-Anonymous-Id` 是后续所有写操作与「我的组合」的身份凭证。

### 3. 将数字指纹传给 MCP（HTTP 与 SSE 均必须）

本 MCP 挂载在共享后端（多用户共用同一进程），后端不生成任何 ID，仅读取连接时携带的 `X-Anonymous-Id` 头并原样转发给 REST。因此：

- **两种传输都必须在连接时携带 `X-Anonymous-Id` 头**（身份凭证，非可选项）：
  - **Streamable HTTP**（`/mcp/http`）：在连接级 headers 设置 `X-Anonymous-Id: <本机数字指纹UUID>`
  - **SSE**（`/mcp/sse`）：同样在连接级 headers 设置 `X-Anonymous-Id: <本机数字指纹UUID>`
- 缺失该头时，后端无法识别用户，写操作与「我的组合」返回 401；后端不会自动补身份，避免串号。
- 跨设备恢复 / 强制换 ID：将旧机器的 `~/.portfolio/aid` 内容复制过来，或设置环境变量 `PORTFOLIO_AID` 为旧 ID 后重连。

> 该 ID 为机器级（同机共享），与浏览器端 `localStorage` 的 `aid` 机制不同但效果一致（首次生成、之后复用）。跨设备恢复组合请使用账号体系（`bind_account` / `login_account`）。

## 调用策略：优先 MCP，回退 pf.py

1. **默认走 MCP 工具**（如 `mcp__portfolio-tool-http-stream__list_portfolios`）。连接器连上后直接调用，身份头由连接器注入（localhost 自动注入；生产需在 `mcp.json` 对应条目配置 `headers.X-Anonymous-Id`）。
2. **仅当 MCP 不可连时回退 `scripts/pf.py`**（直连 REST 兜底）。出现以下任一即判定 MCP 不可用并切换：工具索引中找不到 `mcp__portfolio-tool__*`；调用返回连接错误/超时；返回 `400 缺少 X-Anonymous-Id` 且无法快速修复。
3. **两通道等价**：MCP 与 pf.py 最终都打到同一后端 REST，结果完全一致。
4. **MCP 恢复后切回**，勿长期依赖 pf.py。

## MCP 工具清单（19 个，直接调用）

### 组合
| 工具 | 说明 |
|---|---|
| `list_portfolios(mine: bool)` | 列出组合；mine=true 我的组合，false 公开组合 |
| `get_portfolio(portfolio_id: int)` | 详情：持仓（含最新净值/最近涨跌）、回测曲线、跟踪状态 |
| `get_tracking(portfolio_id: int)` | 提取跟踪状态（数据截至日/最新净值/当日涨跌/成立以来收益） |
| `create_portfolio(name, risk_level, holdings, ...)` | 创建组合 |
| `update_portfolio(portfolio_id, name, risk_level, holdings, ...)` | 编辑组合 |
| `delete_portfolio(portfolio_id: int)` | 删除组合 |
| `clone_portfolio(portfolio_id: int)` | 克隆公开组合到当前用户 |
| `trigger_backtest(portfolio_id: int)` | 触发回测（重算曲线与跟踪） |

`create_portfolio` / `update_portfolio` 参数：
- `risk_level`: `low` | `medium` | `high`
- `holdings`: 持仓列表，每项 `{fund_code, weight, note?}`；权重总和须为 1.0（±0.0001）、单只 ≤ 0.8、代码不重复、权重范围 (0,1]
- 可选：`description`、`is_public`、`rebalance_freq`(none|monthly|quarterly)、`benchmark_type`(csi300|csi_bond|custom)

### 基金
| 工具 | 说明 |
|---|---|
| `search_funds(q: str)` | 按代码/名称模糊搜索 |
| `get_fund_detail(fund_code: str)` | 基金基本信息 |
| `get_fund_nav(fund_code: str, start_date?, end_date?)` | 净值历史（YYYY-MM-DD，留空返回全部；先增量同步再返回） |

### 数据同步（两步）
1. `sync_fund_data(force: bool = False)` → 返回 `job_id`（后台异步，HTTP 202）
2. `get_sync_status(job_id)` → 轮询直到 `status=completed`/`failed`（含 `synced_funds`/`updated_navs`/`tracking_updated` 计数）

### 用户/账号
| 工具 | 说明 |
|---|---|
| `get_me()` | 当前用户信息（是否绑定账号） |
| `bind_account(username, password)` | 为当前匿名用户绑定登录账号 |
| `login_account(username, password)` | 账号密码登录，返回 `anonymous_id`（用于跨设备恢复） |
| `change_password(old_password, new_password)` | 改密码 |
| `unbind_account()` | 解绑账号（保留组合数据） |
| `health_check()` | 后端健康检查 |

## 典型对话流程

**同步我的组合基金数据并刷新跟踪状态：**
1. 调用 `sync_fund_data()` → 取得 `job_id`
2. 调用 `get_sync_status(job_id)` 轮询至完成
3. 调用 `get_portfolio(<id>)` 或 `list_portfolios(mine=true)` 查看最新净值/数据截至日

**新设备找回组合：** `login_account(username, password)` 拿 `anonymous_id` → 写入 `~/.portfolio/aid`（并设 `PORTFOLIO_AID`）→ 列组合。

## 回退 CLI：scripts/pf.py

MCP 连不上时使用。用法：
```
python <skill_dir>/scripts/pf.py METHOD PATH [--data '{"k":"v"}'] [--q key=value]
```
示例：
```
python scripts/pf.py GET  portfolios?mine=true
python scripts/pf.py GET  portfolios/12
python scripts/pf.py POST sync/portfolio-funds --data '{}'
python scripts/pf.py GET  sync/portfolio-funds/status/<job_id>
python scripts/pf.py POST user/login --data '{"username":"alice","password":"secret"}'
```
脚本自动补 `/api/` 前缀、附加 `X-Anonymous-Id`（读 `~/.portfolio/aid` 或 `PORTFOLIO_AID`），输出格式化 JSON。

## 连接配置与注意事项

- 后端地址由环境变量 `PORTFOLIO_API` 决定：`scripts/pf.py` 默认 `http://localhost:8000`（本地开发）；生产 MCP 端点为 `https://invest.geeyo.com`。
- 数字指纹（`~/.portfolio/aid`）生成并作为 `X-Anonymous-Id` 传入后，写操作与「我的组合」即可正常工作，无需在 Skill 内额外指定 ID。仅以下情况需手动覆盖：
  - 强制换成本机 ID：设置环境变量 `PORTFOLIO_AID=<id>`
  - 跨设备迁移：复制旧设备 `~/.portfolio/aid` 内容，或设 `PORTFOLIO_AID` 为旧 ID

### 生产连接注意事项

- **远程 URL 不会自动注入 `X-Anonymous-Id`**：WorkBuddy 连接器仅在 `localhost` 自动读取 `~/.portfolio/aid` 注入身份头，对 `https://invest.geeyo.com` 等远程地址不会自动注入，导致写操作返回 `400 缺少 X-Anonymous-Id`。须在 `~/.workbuddy/mcp.json` 对应条目增加 `"headers": {"X-Anonymous-Id": "<本机aid>"}`，并在连接器面板重新信任/连接使配置生效。
- **`headers` 仅在 streamable-http 传输生效**：`portfolio-tool-http-stream`（`/mcp/http`，streamable-http）能正确带身份头；`portfolio-tool-http`（`/mcp/sse`，SSE）在连接器侧不注入自定义 headers，认证接口仍报 `400`。生产请使用 `portfolio-tool-http-stream` 这套工具（`mcp__portfolio-tool-http-stream__*`）；公开组合列表（`mine=false`）两种传输均可取，因其无需身份头。
- **数据按后端隔离，不跨环境同步**：组合数据存于各自后端数据库。localhost 与 `invest.geeyo.com` 为两套独立库——同一匿名 ID 在生产查询「我的组合」可能为空。将本地组合迁移至生产：在 localhost 后端 `bind_account` 绑定账号，再于生产用同一账号 `login_account` 恢复（纯匿名 ID 不会自动迁移）。
- **pf.py 经 Cloudflare 可能被拦截**：pf.py 使用 Python-urllib（默认 UA）发起请求，生产环境 Cloudflare 可能返回 `403 Error 1010`；本地/可信后端无此问题。
