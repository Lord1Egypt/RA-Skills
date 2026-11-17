# 花花日记 MCP 服务（HuahuaDaily）

通过 MCP 让 Codex、Codex CLI、Claude Code、Claude Code CLI、Claude Desktop、Cursor、Windsurf、OpenClaw 以及其他支持 MCP 的 Agent 读取花花日记后端数据、查询市场行情，并向 App 发送待确认交易或导入请求；配套有限 CLI 负责本地文件和完整导出。

交易和导入不会由 Agent 直接写入。Agent 只负责识别、轻确认和发起请求，最终写入必须回到花花日记 App 的现有确认页。

社区授权、取消授权、关注/取消关注、社区收益同步属于直接后端写操作，不走 App 待确认页；Agent 只有在用户明确确认该社区操作后才应调用。

MCP 可读取完整持仓、交易流水、云端实时同步主数据和截图内容，可能包含金额、成本、收益率等敏感投资数据。生成 Agent Token 即表示授权所接入的 Agent 在其权限范围内读取这些数据。

## 前置条件

- 花花日记账号已开通 PRO。
- 在 App「小窝 / 设置 → Agent 访问令牌」生成新的 Agent Token。
- Token 只显示一次；远程模式填入客户端 Auth Token，本地模式配置为环境变量 `HUAHUA_AGENT_TOKEN`。
- 只有本地 stdio/CLI 模式需要 **Python 3.10+**；手机远程模式不需要 Python。

官方 API 默认地址：`https://api.huahuadaily.cn`，可通过 `HUAHUA_API_BASE` 覆盖。

MCP 启动时会在后台读取公开仓库中的版本声明，不延迟协议初始化；标准 MCP
`instructions` 会要求 Agent 仅在首次接入、配置变更或排障时调用 `get_tool_manifest()`，
普通会话不重复调用。
首次查询最多等待 2 秒，成功结果在当前进程缓存 6 小时，失败结果 15 分钟后重试。
检查失败只返回 `updateCheck.status=unavailable`，不会阻断其他工具；发现新版时返回
`updateAvailable=true` 和分安装方式的更新步骤。该机制只提示，不会自行安装或覆盖
用户环境。特殊离线环境可设置 `HUAHUA_MCP_UPDATE_CHECK=0` 关闭。

## 安装方式

### 方式一：官方远程 MCP（手机或无 Python 环境）

支持第三方 MCP URL 的客户端可直接连接，无需在手机安装 Python：

```text
名称：花花日记
服务器 URL：https://mcp.huahuadaily.cn/mcp
Auth Token：Bearer 你的花花日记 Agent Token
```

`Bearer ` 前缀必须保留。每位用户填写自己的 Token；服务端按请求验证并转发，
不配置或保存某个固定用户 Token。远程端使用 Streamable HTTP；客户端把它统称为
HTTP/SSE 不影响连接，但是否自动加载 MCP Prompts 由客户端决定。

普通问题直接依靠工具描述调用。复杂任务可调用
`get_skill_context(topic="portfolio")`、`date-safety`、`quant` 等单一主题；
不要默认加载 `full`。支持 MCP Prompts 的客户端也可显式选择
`huahua_daily_expert` 获取完整上下文。

官方远程入口当前使用 `full` 工具面。若自行部署，可用
`HUAHUA_MCP_PROFILE=core` 减少工具 schema，或使用 `full` 暴露全部能力。

### 方式二：uvx（推荐的本地 stdio 模式）

[uv](https://docs.astral.sh/uv/) 是快速的 Python 包管理器，`uvx` 可直接运行 Python 工具，无需手动安装依赖。

**安装 uv**（如果尚未安装）：

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**MCP 配置**：

```json
{
  "mcpServers": {
    "huahua-daily": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/baiye1997/HuaHuaDailyMCP",
        "huahua-daily"
      ],
      "env": {
        "HUAHUA_API_BASE": "https://api.huahuadaily.cn",
        "HUAHUA_AGENT_TOKEN": "粘贴你的 Agent Token"
      }
    }
  }
}
```

### 方式三：pip 安装

如果不想安装 uv，可以用 pip 全局安装：

```bash
pip install git+https://github.com/baiye1997/HuaHuaDailyMCP
```

**MCP 配置**：

```json
{
  "mcpServers": {
    "huahua-daily": {
      "command": "huahua-daily",
      "env": {
        "HUAHUA_AGENT_TOKEN": "粘贴你的 Agent Token"
      }
    }
  }
}
```

### 方式四：本地运行

```bash
# 克隆仓库
git clone https://github.com/baiye1997/HuaHuaDailyMCP.git
cd HuaHuaDailyMCP

# 安装依赖
pip install -r requirements.txt

# 运行
HUAHUA_AGENT_TOKEN=你的Token python server.py
```

HuahuaDaily 主仓库联调使用工作区 MCP，避免调用已安装的生产版本。启动本地 PostgreSQL、Redis 和后端后运行：

```bash
./scripts/dev-mcp.sh
```

该脚本只在 development/test 环境为本地内置 `admin` 账号创建 token，并直接执行当前目录的 `mcp-server/server.py`。若该账号尚无持仓，会写入确定性的两基金验收样例；已有持仓不会被覆盖。自动验收量化工具可运行：

```bash
.venv/bin/python scripts/test-local-quant-mcp.py
```

### 工具面 profile

MCP 提供两档工具面，通过环境变量 `HUAHUA_MCP_PROFILE` 选择，默认 `full`：

- `full`（默认，76 个工具）：全部能力，兼容历史配置。
- `core`（33 个工具）：仅高频日常能力（持仓、行情、交易请求、结构化导入、量化上下文），
  适合希望减少工具 schema 注入与选择成本的 Agent。core 下取消的工具会返回
  unknown-tool 错误；manifest 的 `capabilities` 与 `safety` 会同步收窄。

本地截图不要转 Base64 交给模型。安装同一 Python 包后使用有限文件 CLI：

```bash
huahua import screenshots --type transactions --file /path/trade.png --result /path/result.json
huahua import review --type transactions --input /path/result.json
```

CLI 只负责文件、完整导出和诊断；普通持仓、基金、市场、交易和量化交互继续使用 MCP。
若 MCP 仅通过 `uvx` 临时运行且 PATH 中没有 `huahua`，使用
`uvx --from git+https://github.com/baiye1997/HuaHuaDailyMCP huahua ...`。

```json
{
  "mcpServers": {
    "huahua-daily": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/baiye1997/HuaHuaDailyMCP", "huahua-daily"],
      "env": {
        "HUAHUA_API_BASE": "https://api.huahuadaily.cn",
        "HUAHUA_AGENT_TOKEN": "你的Token",
        "HUAHUA_MCP_PROFILE": "core"
      }
    }
  }
}
```

`get_tool_manifest()` 返回当前 profile、可用能力清单和覆盖全部活跃工具的 `toolScopes`，Agent 可在调用前区分本地工具、公开接口及精细 Agent Token 权限。

### 版本 4.1.14 变更

- 统一百分比解析、有效零份额和净值变化容差，修复 MCP 组合计算与后端/App 口径漂移；估算帧继续拒绝非法或非有限百分比。

### 版本 4.1.13 变更

- 远程认证使用不返回个人资料的 `/api/auth/agent-token/validate`，支持不含 `profile:read` 的细粒度 Token；各工具仍按后端 scope 和会员规则校验。
- 个人报告所需权限统一为 `messages:write`，默认 `agent:full` Token 已包含该权限。
- 部署时先更新后端，再更新远程 MCP；旧后端缺少新接口时，远程入口返回 503，不回退读取个人资料。

### 版本 4.1.12 变更

- 夜盘项目显式区分 view、estimateMode 与旧 forecast 标记，保留计算证据与质量说明。
- 配合后端紧凑上下文补齐净值位置、适用指数估值、来源与本地待确认状态；不以在途交易禁止同基金操作。

### 版本 4.1.11 变更

- 夜盘逐只返回 `usable`，与 App 的 ready 涨幅口径对齐；整批刷新、旧帧、汇率缺失和 NAV 为空不再被解释为整只不可用。时间、阶段和质量证据继续保留。
- 涨幅明确使用百分点（0.0582 = +0.0582%），持仓覆盖为披露权重；夜盘请求只读共享帧，不触发预热。

### 版本 4.1.10 变更

- 明确分时走势可包含最新报价点，并保留实际观察时间；旧帧状态继续原样传递，避免误读为实时行情。
- 工具参数、返回字段与权限契约保持兼容。

### 版本 4.1.9 变更

- 统一持仓流水的同日排序：没有顺序号的交易排在已明确排序的持仓校准之后，避免较大顺序号导致 MCP 与 App 计算不一致。
- 工具接口和同步协议保持兼容。

### 版本 4.1.8 变更

- 官方净值不会因为估值链路的 stale 标记而被清空，行情工具与组合收益使用统一判断。
- 普通过期估值仍不作为完整的当前行情；QDII 缺少可靠收益归属日时仍保持未归属。

### 版本 4.1.7 变更

- 基金板块人工调整后，MCP 会读取最新估算帧，避免继续返回调整前的旧板块结果。
- 基金历史与量化工具会识别陈旧数据，触发后端刷新并给 Agent 明确的重试提示；仅来自数据库的原始快照会标明尚未校验新鲜度。
- 询问“当前”“最新”或“刚刚修改”的内容时，Agent 会在当前轮次重新读取数据，减少长会话上下文陈旧造成的误答。

### 版本 4.1.6 变更

- 新增 Zeabur Streamable HTTP 部署入口，手机端以自己的花花 Agent Token 作为 Bearer Token 接入。
- 远程请求使用上下文级 Token 转发和缓存代际隔离，不在 MCP 服务端保存固定用户 Token。
- 远程服务同时暴露完整 Skill Prompt 和按主题渐进加载 Tool；普通查询不预加载完整上下文，兼容不会自动注入 MCP Prompts 的客户端并降低额度消耗。

### 版本 4.1.5 变更

- Skill 元数据现在显式声明版本，并与 MCP 运行时版本保持一致。

### 版本 4.1.4 变更

- 批量阶段排名校验与完整性汇总收敛到独立实现，保留最多 50 只、代码去重和缺失项显式报告契约。

### 版本 4.1.3 变更

- 经权威注册表确认的纯场内 ETF 在收盘后优先返回日期和代码均校验通过的收盘行情，并通过 `frameSemantics=exchange_close_price` 与盘中参考净值估算严格区分。
- MCP 明确禁止把收盘价称为基金官方净值或用户成交价；场内标的仍只允许查询与自选。

### 版本 4.1.2 变更

- 基金历史工具启用严格新鲜度契约；缺少权威确认天数时仍会触发历史净值上游刷新，且不会用陈旧副本冒充最新数据。
- 场内能力限制同步覆盖 MCP 持仓操作；经权威注册表确认的纯场内标的只允许查询、自选和参考估算。

### 版本 4.1.1 变更

- 历史量化上下文只回放可靠的新版组合记录；永久删除的基金或交易不会在旧日期重新出现。
- 对早于可靠数据起点或最近一次重置、恢复的数据请求保持拒绝，并返回可核对的原因和可靠起始日期。

### 版本 4.1.0 变更

- 新增有限 `huahua` CLI，直接处理截图文件、完整导出、报告文件和连接诊断；图片不再经过模型 Base64。
- 新增 `/api/agent/import-reviews` 结构化导入契约，文字/表格/JSON 直接使用 `import:request` scope。
- 新增独立 `/api/agent/capabilities` 契约握手，量化与 Agent 导入兼容状态分域报告。
- MCP 工具元数据收敛到 ToolSpec；core 调整为 33 个工具，旧 Base64 截图工具仅在 full 兼容并标记弃用。
- HuahuaDaily Skill 改为短路由器，领域规则按需加载 references。

### 版本 4.0.2 变更

- 单基金量化结果新增指数 PE、历史分位、官方 PE 基准日及盘中估算口径。
- 非指数基金新增近 250 个官方净值点的位置分位，支持传入有效盘中估算帧计算今日位置。
- 指数估值复用后端共享缓存与短暂保留帧；批量量化工具不会触发第三方指数估值源。

### 版本 4.0.1 变更

- 持仓记录的基金类型和行业改由后端估算/基础信息 overlay 补全。
- 未知 `confirmDays` 不再猜测为 T+1，避免 QDII/T+N 收益归属错误。
- 明确原始同步工具默认返回兼容投影，按需才附带底层 JSON。

### 版本 4.0.0 变更

- 组合读取协议强制切换到 PowerSync v3，只接受 `protocolVersion=3` 的规范化组合接口。
- 组合新鲜度统一为 `portfolioUpdatedAt`，删除旧 `dataUpdatedAt` 别名和多层旧同步载荷解包逻辑。
- MCP 与 App、Web/PWA、Android 同批强制升级，不保留 v2 同步协议兼容路径。

### 版本 3.5.6 变更

- 修复 3.5.5 发布门禁：拆分基金工具传输辅助逻辑，保持公开工具签名、描述与严格新鲜度语义不变。

### 版本 3.5.5 变更

- 基金量化指标、策略上下文与组合回放新增官方净值 freshness 契约；过期、缺失或无法验证的数据不再被标记为可分析，并会受控触发后台刷新。
- 基金历史、基准历史和指数/ETF 日线在 MCP 中启用严格新鲜度模式；只能取得旧兜底时直接报错，不再向 Agent 返回过期量化输入。
- 回测新增尾部历史完整性审计，补数未完成时不会再报告完整覆盖。

### 版本 3.5.4 变更

- 对齐 MCP 全量工具、权限 scope、QDII D→G 日期归属、夜盘默认池与 pending 分类契约；与 App 一致地拒绝空名称的限购观察项。

### 版本 3.5.3 变更

- 夜盘自选和限购观察现在返回与 App 一致的实际生效默认池，并同时保留原始配置与迁移状态；限购检查快照改为读取 App 的 `lastSnapshot`，`snapshot` 仅作为兼容别名。
- 夜盘批量响应补齐 `timeoutPendingCodes`；QDII D→G 归属对非法确认天数严格保持未归属，不再误降级成 T+1。

### 版本 3.5.2 变更

- 交易截图确认条目现在强制携带布尔匹配状态；后端会再次核验基金代码与标准名称，避免正确代码因 Agent 二次交接缺字段而被稳定误判为“未匹配”。

### 版本 3.5.1 变更

- 指数直估审计新增官方指数代码、跟踪标的、行情 provider/日期、目标净值 D 日及 ETF/板块降级证据，普通估值来源仍保持 `index_direct_estimate`。

### 版本 3.5.0 变更

- 日盘与夜盘估值统一返回校准状态、目标净值 D 日和证据完整度；可靠收益归属 G 日仅由 `get_records().returnAttributionDate` 提供且可能为空。汇率缺失时保留本币估值，不再误报整只基金不可用。
- 夜盘批量上限、`force` 兼容语义、刷新中状态与历史收盘视图已和后端契约对齐。
- QDII 市场代理、市场因子代理及组合审计会保留来源、覆盖谱系和部分证据状态；市场行情明确区分源行情时间与后台采集时间。

### 版本 3.4.0 变更

- 修复组合估值滞后：`marketValue` 会在云端组合快照与行情帧的官方净值锚点中选取更新者，盘中 `estimatedNav` 仍与官方市值严格分离。
- 新增 `portfolioUpdatedAt`、估值完整度与每只持仓的估值来源/净值日期；明确原始负载 `timestamp` 不是同步新鲜度。
- 对齐 App 的现金分红、红利再投和 QDII D→G 当日收益口径。
- 修复社区关注列表和用户搜索的响应解包；加固 Token 切换并发隔离、上传资源限制和量化/路径输入校验。

### 版本 3.3.2 变更

- 安全修复：截图工具的 `image_paths` 本地路径读取已禁用（防止读取并上传任意本地文件），一律改用 `images_base64` 传图片内容；传入 `image_paths` 会直接报错。
- 其余工具的名称、参数与语义不变。

### 版本 3.3.0 变更

- 取消工具：`get_app_versions`、`get_indices`、`get_danmaku`、`send_danmaku`、
  `get_notices`、`get_community_notices`（不再注册）。
- 新增 `HUAHUA_MCP_PROFILE`（core/full）工具面过滤。
- 其余 76 个工具的名称、参数与语义不变。

### 包结构

发行物由兼容入口和 runtime package 共同组成，不支持 `server.py` 单文件分发：

```text
mcp-server/
├── server.py                    # 兼容 facade 与 huahua-daily 控制台入口
├── pyproject.toml               # 同时打包 server 与 runtime packages
└── huahua_mcp_runtime/
    ├── cli.py                   # 有限文件/大结果 CLI
    ├── client.py                # HTTP、认证、会话与缓存
    ├── facade_helpers.py        # facade 的估算/组合 helper
    ├── import_contract.py       # MCP 与 CLI 共用的结构化导入契约
    ├── manifest.py              # 工具 manifest
    ├── update_check.py          # 有界、可降级的版本检查
    ├── version.py               # MCP 运行时版本单一来源
    ├── portfolio_adapter.py     # 云端组合适配
    ├── portfolio_math.py        # 组合计算兼容函数
    ├── tool_registry.py         # ToolSpec 单源与 core/full 过滤（默认 76 个，core 33 个）
    ├── validation.py            # 输入校验
    └── tools/                   # fund/market/portfolio/community/quant 等领域工具
```

`server.py` 保留历史导出和 monkeypatch 兼容；工具实现位于 `huahua_mcp_runtime`。本地开发安装完整包：

```bash
python -m pip install -e ./mcp-server
huahua-daily
```

发布前从主仓库运行：

```bash
npm run mcp:version:check
npm run backend:lint
.venv/bin/python -m pytest \
  backend/tests/test_mcp_server_surface.py \
  backend/tests/test_mcp_portfolio_adapter.py
```

修改 `server.py`、runtime package、MCP 依赖或 `SKILL.md` 契约时，必须先提升
`huahua_mcp_runtime/version.py` 中的版本。仓库质量门会比较 Git 基线并阻止遗漏；
单纯修改 README 不要求提升运行时版本。

MCP surface 测试构建 wheel，校验 runtime/tools、console entry point 和默认 76 个工具，并在隔离目录完成安装导入。测试产物写入临时目录；`mcp-server/` 不保留 `build/`、`dist/`、`*.egg-info` 或 wheel。MCP 独立发布，`mcp-server/**` 变更归入人工发布复核。

## 各 Agent 配置示例

### Claude Code

```bash
claude mcp add huahua-daily \
  -e HUAHUA_AGENT_TOKEN=你的Token \
  -- uvx --from git+https://github.com/baiye1997/HuaHuaDailyMCP huahua-daily
```

或手动编辑 `~/.claude.json`：

```json
{
  "mcpServers": {
    "huahua-daily": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/baiye1997/HuaHuaDailyMCP", "huahua-daily"],
      "env": {
        "HUAHUA_API_BASE": "https://api.huahuadaily.cn",
        "HUAHUA_AGENT_TOKEN": "你的Token"
      }
    }
  }
}
```

### Claude Desktop

编辑 `~/Library/Application Support/Claude/claude_desktop_config.json`（macOS）或 `%APPDATA%\Claude\claude_desktop_config.json`（Windows）：

```json
{
  "mcpServers": {
    "huahua-daily": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/baiye1997/HuaHuaDailyMCP", "huahua-daily"],
      "env": {
        "HUAHUA_AGENT_TOKEN": "你的Token"
      }
    }
  }
}
```

### Cursor

编辑 `~/.cursor/mcp.json`：

```json
{
  "mcpServers": {
    "huahua-daily": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/baiye1997/HuaHuaDailyMCP", "huahua-daily"],
      "env": {
        "HUAHUA_AGENT_TOKEN": "你的Token"
      }
    }
  }
}
```

### Windsurf

编辑 `~/.windsurf/mcp.json`，格式同上。

## OpenClaw / ClawHub

```bash
clawhub install huahua-daily
```

然后配置环境变量 `HUAHUA_AGENT_TOKEN`。

## System Prompt 模板

```text
你可以使用花花日记 HuahuaDaily MCP 工具查询用户基金持仓、交易流水、云同步状态、市场行情和公告，也可以把用户提供的文字、表格、JSON 或截图整理成批量导入请求，发送到 App 确认页。

调用规则：
- 会话开始可调用 get_tool_manifest 自检能力和安全边界。
- 查询资产概况优先调用 get_summary；需要明细再调用 get_records。
- 需要审计交易流水或重算收益时，调用 get_transactions 或 get_records(include_transactions=true)。
- 需要完整云端实时同步主数据时，调用 get_raw_sync_data；不要默认请求 include_json_text=true。
- 若 `get_sync_meta` / `get_raw_sync_data.meta` 返回 `empty_portfolio_confirmed=true` 且 `has_restorable_sync_payload=true`，表示这是用户在 App 确认过的空组合主数据，不是云端损坏。
- 查询某只基金行情：已知代码直接 get_item_estimate；未知代码先 search_item。
- 对比单只基金不同行情源：调用 get_fund_source_previews。
- 用户想买入/卖出时，必须先确认基金名称、代码、金额或份额、卖出模式和分组，再调用 request_transaction；指定分组时优先传稳定的 `group_id`。
- request_transaction 只发送待确认信号，必须明确告知用户需要打开 App 确认。
- 7 天内重试同一交易或导入请求时必须复用 `client_request_id`，服务端会保留该窗口内的幂等记录，避免产生重复待确认 Banner；超过窗口请生成新的请求 ID。
- 用户明确要求生成并保存个人报告时，调用 `submit_personal_strategy_report` 投递到当前 Token 所属用户的报告中心；重试同一报告必须复用 `client_message_id`。
- Pro 用户创建的默认 Agent Token 已支持个人报告写入；不能指定其他用户或广播。
- 不得调用 /api/hermes/reports；公开 MCP 不提供管理员公共报告写入能力。
- 用户已用文字、表格或 JSON 给出批量记录时，校验字段后直接调用 request_import_review，不需要经过截图识别接口。
- 只有用户输入是图片时才使用 `huahua import screenshots`；不得为新调用选择 MCP Base64 截图工具。
- 对 unmatched / ambiguous 条目只做轻确认，补齐基金代码、日期、金额、份额等识别歧义。
- 轻确认后调用 request_import_review，把整批结果发送到 App 现有导入确认页。
- 不要直接写云同步，不要声称导入已完成；用户必须在 App 批量确认后才会写入。
- 数据来自云端实时同步主数据，MCP 固定读取结构化组合接口，不读取旧同步大包或云端历史备份快照。若用户刚在 App 操作，提醒其确认实时同步已完成再查询。
- `get_records` 的市值/持有收益只按 App 云端主数据中的官方 `lastNav` 计算；盘中估算只用于今日收益，不用于持仓市值。
- QDII/T+N 最新官方净值缺少可靠 G 日时，`todayProfit` 和归属日分母不会提前计入；检查 `summary.displayedDayCompleteness.complete` 与 `pendingAttributionCount`，不得把残缺组合描述成完整当日收益。
- `summary.estimateCompleteness.complete=false`、`timeoutCount>0` 或 `staleCount>0` 表示至少一只持仓缺少可用估值帧；`complete=true` 也只代表有可用数值。`evidenceComplete`、`partialCodes`、汇率与代理证据用于防止 Agent 虚构“完整覆盖”，但普通回答不要主动逐只传播这些技术状态；只有用户明确询问诊断、证据或估算口径时才展开。0 元不能表述为真实零涨跌；过期 last-good 仅供审计，不参与今日收益。
- `huahua` 是稳定的花花托管策略身份，不承诺固定内部实现。`get_records` 的 holdings/watchlist `estimateAudit` 保留实际 provider、engine、proxyCoverage、fxDegraded、partial、evidenceComplete、fallback 等审计字段；`coverage` 仅在后端审计传输实际提供时存在，普通公开估值接口会隐藏内部覆盖率。日常回答只说明稳定的估值类型、来源、时间、涨幅与净值；只有用户明确要求审计时才解释代理范围，且不能把代理估算描述成持仓股票完整覆盖。
- 查询 QDII 夜盘估值时，先调用 get_night_watchlist 获取 App 实际生效列表（可能来自默认池），再调用 get_night_estimate。
- 查询资金流向时调用 get_fund_flow（需 PRO 会员）。
- 社区授权/关注/同步等写操作须向用户确认后再执行。
- 社区写操作会直接生效，不是 App 待确认请求；收益同步不要凭空编造收益率，通常交给 App 自动同步。
- full profile 中的旧截图工具仅作兼容且已弃用；新调用使用 `huahua import screenshots` 直接上传显式文件路径，不传 Base64。
- 用户完成 JCTI 答题后可调用 analyze_jcti 获取 AI 人格分析。
- 查询 App 版本信息使用 get_app_version。
```

## 工具能力

认证与自检：

- `set_token(token)`：运行时设置 Agent Token。
- `get_tool_manifest()`：返回能力边界、认证方式、安全说明、MCP 更新预检和 `backendCompatibility.components` 后端分域契约握手。Agent 在每个会话首次使用 HuahuaDaily 时调用；若 `runtime.updateCheck.updateAvailable=true`，应按 `updateInstructions` 提示用户更新并重启 MCP；量化与 Agent 导入分别按自己的 component 判断，不能互相误伤。
- `get_current_user()`：读取当前账号和会员信息。

云端实时同步与持仓：

- `get_sync_meta()`：读取云端实时同步主数据更新时间、etag、大小，并返回最新云端历史快照摘要。新鲜度以 `portfolio_updated_at` 为准。
- `get_raw_sync_data(include_json_text=false)`：读取完整云端实时同步主数据的兼容投影，优先结构化组合接口；名称中的 `raw` 为兼容保留。默认复用会话内 30 秒组合缓存；只有 `include_json_text=true` 才会为导出/迁移审计绕过缓存并附带底层接口原始 JSON。`data.timestamp`/`meta.payload_timestamp` 只是客户端快照谱系或迁移元数据，不是同步时间。
- `get_records(include_transactions=false)`：读取持仓、App 中可见的自选、估算收益和汇总；不返回已送养隐藏项，同代码的显式自选优先；会自动使用云端主数据里的全局/单基金行情源偏好，并在已配置时返回 `autoInvestPlans`。官方市值会选取组合快照与行情帧中更新的官方净值锚点，并通过 `valuationNavDate`/`valuationSource` 公示；盘中估值只进入 `estimatedMarketValue`。holdings/watchlist 都返回 source、freshness、estimateAudit，以及 `targetNavDate`/`latestOfficialNavDate`（D 日）、`estimateDisplayDate` 和可靠时才存在的 `returnAttributionDate`（G 日）。
- `get_summary()`：读取资产摘要。
- `get_transactions(code="", include_pending=true)`：读取交易流水。
- `get_transaction_ledger(start_date="", end_date="", codes?, transaction_types?, statuses?, group_id="", cursor="", limit=100, order="desc")`：读取服务端完整交易账本，含金额、份额、费用、净值日和确认日；可按持仓分组筛选；筛选与排序按 `effectiveDate = confirmDate || tradeDate`；永久删除基金不再出现。
- `get_groups()`：读取持仓分组和自选分组。
- `get_tags()`：读取全局标签和基金标签。
- `get_portfolio_preferences(include_night_watch=true, include_purchase_limit=true, include_auto_invest=true, include_disciplines=true, code="")`：一次读取夜盘自选、限购观察、定投计划和止盈止损纪律四个 section（共享同一快照缓存，不产生额外网络请求）。core profile 推荐使用本聚合工具；旧单工具在 full profile 保留。
- `get_purchase_limit_watchlist()`：按 App 迁移规则读取实际生效的限购观察列表；`lastSnapshot` 是最近检查结果，`snapshot` 是兼容别名。
- `get_auto_invest_plans(code="")`：只读查询 App 定投计划，兼容旧版单计划和新版多计划；可按基金代码筛选，不提供任何写入能力。
- `get_fund_disciplines(code="")`：只读查询 App 中设置的基金止盈止损纪律及触发状态；可按基金代码筛选，不提供任何写入能力。

策略实验室：

- `get_portfolio_nav_history(start_date="", end_date="", benchmark_code="000300", group_id="")`：真实组合单位净值、累计收益、每日收益和回撤；当前区间必须检查 `complete` 与 `navFreshness.complete/staleCodes/missingCodes/unverifiedCodes`，共同停在旧日期的组合不会再报告完整。存在 `navFreshness.retryAfterMs` 时按该间隔有界重取，最多 3 次。
- `get_portfolio_trade_review(start_date, end_date, benchmark_code="000300", group_id="")`：读取与 App 相同的加减仓复盘，以及 T1/T7/T20/T60 后续表现。
- `get_batch_fund_nav_history(codes, start_date="", end_date="", order="asc")`：一次读取最多 20 只基金的官方历史净值，DB-only，不逐只请求上游；顶层 `freshnessMode=unchecked_db_snapshot` 明确表示未核验当前公布进度。每只基金返回 `coverageStart/coverageEnd/baselineDate/complete`，`complete` 仅在请求区间首尾严格覆盖时为 true。当前量化优先使用会主动校验 freshness 的量化端口，不得把 DB-only 历史的旧 `coverageEnd` 当作当前数据。
- `get_quant_strategy_context(as_of_date="", group_id="", mode="live", history_window="1y", benchmark_code="000300", view="compact")`：一次返回真实持仓、D 日基金指标、G 日组合风险、实时估值、QDII 夜盘执行参考、交易门禁、有效定投、在途金额和服务端预计算市场结果。必须检查 `readyForAnalysis`、`blockingReasons` 和 `dataQuality.fundOfficialNavFreshness`；基金 NAV 过期、缺失或无法证明新鲜时会 fail-closed，存在 `retryAfterMs` 时按该间隔有界重取，最多 3 次。历史模式只使用可靠区间内的 v3 正版本日志，永久删除的基金或交易不会在旧日期复活；早于迁移或最近 reset/restore 的请求会 fail-closed，并在 `dataQuality.historicalPositionReconstruction.structure` 给出 `reliableFrom` 和原因。上下文缓存绑定同一次 v3 读取的 etag、NAV revision 与基金调优 generation。MCP 默认 `view="compact"`；需要完整份额、成本、官方净值、全部指数明细和下钻引用时使用 `view="full"`。
- `run_portfolio_backtest(funds, start_date, end_date, initial_capital=100000, strategy_type="target_rebalance", rebalance_frequency="monthly", take_profit_rate=0.15, stop_loss_rate=0.10, reentry_rate=0.05, benchmark_code="000300", name="Agent 回测", client_run_id="", group_id="")`：运行并保存零费率历史试算；`funds` 为 `[{"code":"000001","name":"基金名称","weight":0.5}, ...]`，`name` 可选，权重和必须为 1。必须检查 `coverageRatio == 1` 和 `metrics.dataQuality.historyComplete`；尾部补数未完成时不得解释为完整回测。
- `get_portfolio_backtest(run_id, trade_offset=0, trade_limit=100, max_series_points=300)`：按 `run_portfolio_backtest` 返回的 `run_id` 读取已保存结果；走势最多抽样 500 点，交易按 offset/limit 分页，使用 `nextTradeOffset` 继续读取，适合审计长周期结果。
- `save_quant_snapshot(snapshot_key, snapshot_date, strategy_id, data_cutoff_at, strategy_version="", fund_signals?, market_mode?, features?, risk?, data_quality?, group_id="")`：幂等归档当天策略观察；`data_cutoff_at` 必填。可传资产分组 ID，将真实持仓和逐基金判断限定在该分组；真实持仓、组合版本和内容哈希由服务端捕获。不接受历史回填、虚拟持仓、建议金额或收益字段。
- `get_quant_snapshots(strategy_id="", latest_only=false, limit=50, cursor="", start_date="", end_date="", snapshot_id=0, group_id="")`：分页读取不可变信号档案；传 `group_id` 只读取以该分组保存的判断，旧快照归入全部持仓；列表返回摘要，传 `snapshot_id` 读取完整内容。
- `get_quant_snapshot_review(snapshot_id, benchmark_code="000300")`：读取与 App 相同的不可变信号快照 T1/T7/T20/T60 权威复盘。

回测与信号档案是研究和复盘记录，不会直接下单。基金“清仓”保留真实交易历史；App 永久删除基金后，真实组合账本及引用该真实组合的信号档案视为从未拥有，独立历史试算结果不受影响。

市场与基金：

- `search_item(query)`
- `get_item_estimate(codes, default_data_source_mode="source_a", data_source_mode_by_code?)`：最多 50 只；行情源只支持 `source_a/source_b/huahua`，默认 A，只有 Pro 可切换。检查 `complete`、`evidenceComplete`、`missingCodes`、`invalidCodes`、`unavailableCodes`、`timeoutCodes`、`staleCodes`、`decisionUnavailableCodes`、`partialCodes` 和 `fxDegradedCodes`，用于避免把不完整帧误说成完整结果。每项可含 `estimateEvidence.proxyCoverage/fxStatus/fxDegraded/coverage`，其中 coverage 仅在审计传输实际提供时存在；QDII 持仓帧还会统一返回 `estimateEvidence.calibration{applied,reason,weight,modelVersion}`。`fxStatus=omitted` 时本地资产涨幅仍可用。同一时刻的重叠请求会合并为一次后端读取，但不会跨调用缓存完整估值帧，避免基金调优后继续返回旧板块、确认天数或估算路由。普通回答不主动枚举 partial、FX 或覆盖率；用户明确要求诊断时才展开，并且不能把市场/板块代理冒充持仓股票完整覆盖。`display_date` 是估算展示/T 帧日期，`target_nav_date` 与 `last_nav_date` 是净值 D 日；可靠收益 G 日只能读取 `get_records().returnAttributionDate`，为 null 时不得用 D 日代替。
- `get_fund_source_previews(code)`：单只基金 `source_a/source_b/huahua` 来源预览，用于解释或选择数据源。净值公布后，各来源可能返回收盘前归档估值、当前接口已切换的官方值或权威官方净值；同时检查 `source` 和 `last_estimate_snap.source`。`data` 允许缺少未覆盖或无归档的 A/B，这不代表整个请求失败。
- `get_daily_rank()`：返回已形成当日估值或官方净值快照的活跃基金池排行，不代表全市场全量基金。
- `get_item_detail(code)`：读取单基金基础详情与持仓信息，不触发量化计算。
- `get_item_history(code)`：严格 freshness 模式；后端只能取得过期兜底时会报错，不向 Agent 返回旧历史。
- `get_item_dividends(code)`
- `get_fund_timeline(code, source_mode="source_a")`：仅用于展示当前交易展示日曲线；当前量化结论必须另取 `get_item_estimate` 并检查 freshness，不能把曲线尾点当作新鲜行情证明。
- `get_fund_fees(code)`：确认天数、申购状态、QDII/限大额日累计限购金额等交易规则。
- `get_batch_fund_fees(codes)`：批量获取费率/申购状态/限购规则，最多 50 只；检查 `complete` 和 `missingCodes`。
- `get_fund_period_rank(code)`
- `get_batch_fund_period_ranks(codes)`：批量获取多只基金排名，最多 50 只；结果位于 `data`，检查 `complete` 和 `missingCodes`。
- `get_night_estimate(codes, force=false, view="forecast")`：最多 30 只，读取 QDII 夜盘最近已物化帧（需会员）。`force` 是废弃兼容参数，true/false 都不会穿透共享缓存或触发上游抓取。forecast 逐只按 `usable` 判断涨幅可用性（ready + 有限涨幅）；`estimatedNav=null` 不阻断。`currentComplete`、`warming`、`frameRefreshing` 和 `staleCodes` 是时效审计，保留时间说明，不据此否决 usable 单只。pending 只影响对应基金。涨幅单位为百分点（0.0582 = +0.0582%），coverage 是披露权重；`item.fxStatus=omitted` 时本地涨幅仍可 ready/current，但 `evidenceComplete=false`；持仓模型帧的 `item.calibration` 统一给出 `applied/reason/weight/modelVersion`，夜盘只读模型、不训练。last_close 的 stale 是历史收盘快照的正常语义，检查 `complete`，其 `currentComplete=false`。`actual_session_date` 是海外行情交易日，`date` 是北京时间响应日，item 的 `navRequiredDate/lastNavDate` 才是净值 D 日，均不是收益 G 日。
- `get_night_watchlist()`：读取 App 夜盘估值页实际生效的基金列表；未自定义时 `codes` 已包含默认池，`configuredCodes=[]`、`source=default`，通常作为 `get_night_estimate` 的前置工具。
- `get_purchase_limit_watchlist()`：按 App 迁移规则返回实际生效的限购观察列表；`lastSnapshot` 是最近检查结果，`snapshot` 是兼容别名，可配合 `get_fund_fees` 检查当前申购状态和限购额度。
- `get_status()`
- `get_overview()`
- `get_sector_wind()`：板块风向，返回领涨/领跌板块和数据时间。
- `get_index_metrics(codes=None)`：不依赖持仓，返回全部或指定指数的服务端 MA、收益、趋势、回撤、波动和强弱排名；例如 `codes=["KS11"]` 直接取得韩国指数 MA20。`historyExpectedAsOf` 与 `historyFreshness` 按所属市场时区、收盘时刻和交易日历判定日线是否到位，`historyFreshnessBasis` 会显式标记交易日历或市场配置不可用的降级，`historyLagCalendarDays` 仅作跨度展示。
- `get_sector_metrics()`：全部行业/主题 ETF 代理的服务端 MA、收益、回撤、波动和强弱排名；同样返回独立历史新鲜度，Agent 不再自行计算。
- `get_yesterday_rank()`：上一交易日基金涨跌榜。
- `get_fund_flow()`：资金流向数据（需 PRO 会员）；`sectorFlow` 非空时同时提供 industry 与 concept，分类由 last-good 补齐时返回 `categoryFreshness`、`categoryPolledAt`。
- `get_benchmark_history(code="sh000300")`
- `calculate_trading_dates(date, time_mode="PRE_MARKET", confirm_days=1)`：返回的 `data_date` 是按 `nav_date` 与 `confirm_days` 反推的估值反映日，并以 `data_date_inferred=true`、`data_date_basis=nav_date_minus_confirm_days_offset` 公示来源；它不是上游已观察到的官方净值 D 日、公布日或收益归属 G 日。
- `get_next_trading_day(date)`
- `get_fund_profile(code)`：基金画像（综合信息）。
- `get_batch_fund_profiles(codes)`：批量基金画像，最多 20 只；非法代码直接报错；返回 `data`、`complete`、`missingCodes`、`timedOut`，服务端总预算 20 秒。
- `get_fund_quant_metrics(code, view, ...)`：按需读取后端统一计算的单基金量化数据。`technical` 返回技术卡、位置分位与历史统计：可精确关联境内指数时 `current.indexValuation` 给出指数 PE 与历史分位，其他基金用近 250 个官方净值点的 `navPositionPercentilePct`。指数结果还需检查 `peBasis`：`live_index_price_estimate` 以 `officialPeAsOf` 的官方 PE 为基准、按今日指数点位估算，`official_daily` 直接使用 `dataAsOf` 当日官方 PE；`estimateStale=true` 是估值同款的短暂保留帧，后台正在刷新。`momentum` 返回短中期收益/均线偏离/连跌，`risk` 返回中长期收益/回撤/波动，`full` 才组合全部数据。必须检查 `historyFreshness/historyExpectedAsOf`、`current.status`、`current.valueBasis` 与数据日期。传入有效盘中估算帧时，非指数基金的位置分位使用实时估算值；实时估算帧只适用于 `technical/full`。官方口径不接受客户端自定义净值，不输出买卖建议。
- `get_batch_fund_quant_metrics(codes, view, current_frames=None)`：按相同语义视图批量取数；`technical/momentum/risk` 最多 50 只，`full` 最多 10 只。为避免批量触发第三方估值源，批量结果不包含详情按需字段 `current.indexValuation`；需要指数 PE 时只查询用户正在查看的单只基金。Agent 不应并发调用多次单只接口，也不应重复拉 NAV 历史计算。必须同时检查顶层 `complete/staleCodes/unverifiedCodes/refreshingCodes`、`item.historyFreshness/historyExpectedAsOf`、指标 `metrics.complete` 和 `current.status`；过期或无法证明新鲜的数据会 fail-closed，并在可行时后台刷新。
- `get_holder_ranking()`：App 内持有人数排行榜。
- `get_instrument_catalog()`：指数/ETF 目录。
- `get_instrument_quotes(codes)`：严格按目录标准代码返回指数/ETF最近物化行情快照，不补默认标的；最多20个。`updatedAt/quoteDate` 是源行情时点，`polledAt` 是缓存采集时点；必须检查 `cacheMeta.freshness/missingCodes/staleCodes/repairingCodes`，repairing 表示后台正在补帧而非本次请求直抓 Yahoo。
- `get_instrument_timeline(code, range="1d")`：使用目录标准代码读取指数/ETF分时走势，例如 `000300`、`399006`、`KS11`；检查 `latestQuote.freshness`。
- `get_instrument_history(code, period="1m")`：使用目录标准代码读取指数/ETF 日线历史；周期仅支持 `1m/3m/6m/1y`。MCP 使用严格 freshness 模式，stale/unknown 时直接报错，不向 Agent 返回旧日线。

交易请求：

- `request_transaction(item_code, item_name, record_type, amount=0, date="", note="", group_name="", group_id="", sell_mode="AMOUNT", shares=0, client_request_id="")`：买入使用 `amount`；卖出明确选择 `AMOUNT` 或 `SHARES`。指定分组优先传 `group_id`；7 天内重试必须复用 `client_request_id`。
- `get_agent_requests()`
- `update_agent_request(request_id, status="DISMISSED")`：只允许撤回待确认提示；`PROCESSED` 必须由 App 在用户确认后设置。

个人报告：

- `submit_personal_strategy_report(title, summary, payload, client_message_id="")`：将当前 Agent 生成的报告保存到 Token 所属用户自己的报告中心。默认 Agent Token 即可使用，只能自投递；不得调用管理员 `/api/hermes/reports` 接口。

批量导入：

- `request_import_review(import_type, items, source_note="Agent 整理的批量导入", client_request_id="", source_kind="text")`：把文字、表格或 JSON 的结构化记录发送到 App 批量确认页；`source_kind` 支持 `text/table/json/screenshot/file`，7 天内重试必须复用 `client_request_id`。
- `import_holding_screenshots` / `import_transaction_screenshots`：只在 full profile 为旧调用兼容，已弃用，不属于 core；新截图工作流使用 `huahua import screenshots`，避免 Base64 经过模型上下文。

社区：

- `get_community_ranking(tab="weekly", page=1, page_size=50)`：收益率排行榜（周/月/总）。
- `get_community_my_rank()`：我的排名。
- `get_community_user(uid)`：用户详情（十大重仓前5）。
- `get_community_stats()`：关注/粉丝数。
- `get_community_following()`：关注列表。
- `search_community_users(query)`：搜索用户（UID/昵称）。
- `get_community_authorization()`：查询社区授权状态。
- `authorize_community(show_amount, anonymous)`：授权参与喵舍排行，直接生效，调用前必须确认。
- `revoke_community_authorization()`：取消授权，退出排行，直接生效，调用前必须确认。
- `follow_community_user(target_uid)`：关注/取消关注用户（取反操作），直接生效，调用前必须确认。

JCTI 投资人格：

- `analyze_jcti(personality_id, ye, wen, sui, duan)`：提交四维分数，获取 AI 个性化投资人格分析。

版本信息：

- `get_app_version()`：最新版本号、更新日志、下载地址。

## 批量导入流程

1. 文字、表格或 JSON 直接整理为 items，并调用 `request_import_review`。
2. 本地截图使用 `huahua import screenshots` 写入结构化结果文件，不经过 Base64。
3. Agent 只对识别歧义做轻确认，再用 `huahua import review` 创建批量导入请求。
4. App 展示一个 Agent Banner。
5. 用户点击后进入现有确认页：
   - `IMPORT_HOLDINGS` → 持仓截图导入确认页
   - `IMPORT_WATCHLIST` → 自选截图导入确认页
   - `IMPORT_TRANSACTIONS` → 交易记录截图导入确认页
6. 用户在 App 中批量编辑、分组、去重并确认后才写入。

## 数据完整性说明

云端实时同步主数据用于多端一致，包含：

- `funds`：基金、自选、持仓、成本、交易记录、标签、纪律、定投、基金级 `dataSourceMode`，以及恢复前展示所需的最后官方净值基线。
- `groups` / `watchlistGroups`：分组。
- `globalTags`：全局标签注册表。
- `fieldConfigs` / `watchlistFieldConfigs`：字段显示配置。
- `nightWatchCodes`：夜盘估值自选基金。
- `purchaseLimitWatchItems`：限购观察列表。
- `purchaseLimitWatchNightDefaultsMigrated`：限购观察是否已并入夜盘默认基金的迁移标记。
- `marketIndexSelection`：市场指数/ETF 看板选择。
- `userPreferences.fundDataSourceMode`：全局基金估值行情源模式。
- `userPreferences.strategyMaxDrawdownLimitPct`：策略实验室组合回撤阈值百分数，`0` 表示未启用；`get_records.strategyPreferences` 会向 Agent 返回该值。
- `emptyPortfolioConfirmed` / `clearedAt`：用户确认清空组合后生成的空组合主数据标记；这类主数据可恢复为空组合，不应当作异常空数据。
- `timestamp` / `version`：客户端导出时间和数据版本。

云端实时同步主数据只保留已删除基金不可重建的归档账本；当前基金的收益日历会用交易记录和历史净值重建。手动本地备份包含并恢复完整 ledger 和基金元数据，可离线恢复。

Agent 如需完整审计，应优先读取 `get_transactions` 和 `get_raw_sync_data`，不要只依赖 `get_summary`。

## 安全边界

- Agent Token 存储为 SHA256，不保存明文。
- Token 可设置有效期，可在 App 内撤销。
- 后端对 AgentToken 使用权限白名单。
- Agent Token 需要 PRO 会员；过期、撤销或会员状态不满足时会被拒绝。
- MCP 可读取敏感投资数据，包括持仓金额、交易流水和原始云端实时同步主数据；请只授权可信 Agent。
- 交易类能力只创建待确认请求，不直接写入交易。
- 批量导入只创建 App 确认请求，不直接写入数据。
- full profile 旧截图工具的 `image_paths` 仍禁用；新工作流由 CLI 读取显式文件路径。
- 社区授权、取消授权、关注/取消关注、社区收益同步是直接写操作，不经过 App 确认页。
- MCP 不提供云同步覆盖写入工具。
