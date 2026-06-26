Changelog
=========

[1.2.2] - 2026-05-26
--------------------

Changed
-------

- **统一 `npx` 调用为 scoped 包名 `@insentek/openapi-skill`**
  - `NOT_CONNECTED_MESSAGE`（Python + Node 两份）、SKILL.md 固定文案、`docs/interaction.md`、`docs/getting-started.md` 中所有 `npx insentek-api-skill ...` 改为 `npx @insentek/openapi-skill ...`，避免未安装包的新用户被引导执行不存在的 npm 包名
  - README 新增「命名约定」表，说明 Skill ID / ClawHub slug / npm 包名 / CLI 二进制名各自用途
  - SKILL.md MUST NOT 列表更正描述：`npx insentek-api-skill ...` 实际会以 npm 404 失败，而 `npx @insentek/openapi-skill devices` 才是会误触 `install` 默认命令的形态

- **`python3` 显式化 + JSON 中暴露 `python.command`**
  - SKILL.md / docs 中所有 `python ${SKILL_ROOT}/...` 改为 `${PYTHON} ${SKILL_ROOT}/...`，并明确 `${PYTHON}` 来自 `npx @insentek/openapi-skill info --json` 的 `python.command`（macOS/Linux 默认 `python3`，Windows 默认 `python` / `py`）
  - `lib/output.js` 的 `serializeStatus` / `serializeInstallLocation` / `buildInfoPayload` 输出新增 `python` 对象（`ok` / `command` / `version`），每个 scope 条目还额外暴露 `installed` 布尔，让 Agent 通过 `info --json` 一次性发现安装位置而无需先猜 runtime/scope
  - `scripts/insentek_cli.py` 的 `check` 把 Python 最低版本要求从 `>=3.8` 修正为 `>=3.10`（脚本实际使用了 PEP 604 `int | None` 联合类型，3.10 之前会语法错误）；同时 doctor 的 Python 检测 message 同步更新
  - SKILL.md 新增 Python 未安装时的固定引导文案，让 Agent 不要在无 Python 环境下反复尝试

- **所有 API 调用切换到 HTTPS**
  - 默认 `API_BASE_URL` 从 `http://openapi.ecois.info` 改为 `https://openapi.ecois.info`（`scripts/insentek_cli.py` / `scripts/export_excel.py` / `lib/core/credentials.js` / SKILL.md frontmatter / README / docs / `reference/api-doc.md` 16 处）
  - `docs/platform-setup.md` 的环境变量示例顺手修正：`INSENTEK_BASE_URL` → `INSENTEK_API_BASE`（脚本实际读取的变量名）

Added
-----

- **`latest` 子命令**：`scripts/insentek_cli.py` 新增 `latest --sn SN`，统一走加密凭据 + 自动刷新 token，取代 SKILL.md 之前不可执行的 `curl /v3/device/{sn}/latest` 示例（Agent 无法从加密凭据中拿到明文 token）
- **统一错误信封 `normalize_error`**：`cmd_data` / `get_latest` 现在把内部 `_validation_error` / `_http_error` / `authentication_required` 统一转换为 `{success: false, error: <kind>, message: ...}`，并对上游 WAF HTML 错误页截断到 500 字符

Fixed
-----

- `docs/platform-setup.md` 中 OpenClaw 小节里两个同名的「方式二」标题（重命名为「方式三/四」）
- README 项目结构里把 `skill.md` 修正为 `SKILL.md`（Linux 大小写敏感），删除已不存在的 `ref/` 和 `PLATFORM-TEST.md` 引用
- `lib/commands/doctor.js` 移除与 skill 功能无关的 `git` 检测，避免最小化容器环境 doctor 报红
- SKILL.md frontmatter 的 `api_base_url` 注明为信息字段（脚本实际通过 `INSENTEK_API_BASE` 环境变量切换 base URL）
- `write_html.py` 调用示例从易丢换行/引号的 `echo | python ...` 改为推荐 `--input-file <tmpfile>` 模式

[1.2.1] - 2026-05-26
--------------------

Added
-----

- **`@insentek/openapi-skill` CLI 凭据管理**
  - `login` — 交互式配置 appid/secret，AES-256-GCM 加密保存至 `~/.config/insentek/credentials.json`
  - `logout` — 清除本地凭据
  - `auth status` — 查看连接状态（脱敏展示）
  - 安装流程检测凭据，未配置时引导 `login`

- **`scripts/credential_store.py`**
  - 与 CLI 加密格式兼容，供 `insentek_cli.py` 读取本地凭据
  - 修复 `AESGCM.decrypt()` 缺少 `associated_data=None` 导致解密失败的问题

- **CLI `status` / `info --json` 脚本路径**
  - JSON 输出新增 `scripts.cli`、`scripts.exportExcel`、`scripts.writeHtml`，便于 Agent 解析 `${SKILL_ROOT}`

Changed
-------

- **认证安全模型（skill.md / docs）**
  - Agent **禁止**在对话中索要或接收 appid/secret
  - 401/403 / `authentication_required` 时展示固定引导文案，引导 `npx insentek-api-skill login`
  - API 调用使用 `python ${SKILL_ROOT}/scripts/insentek_cli.py`；`${SKILL_ROOT}` 由 `status/info --json` 解析，**禁止**相对路径 `scripts/...`
  - 文件找不到时先查安装路径，**禁止**乱试 `npx insentek-api-skill devices` 等错误命令

- **OpenClaw workspace 安装路径**
  - `workspace` scope 修正为 `~/.openclaw/workspace/skills/insentek-openapi`（Windows: `%USERPROFILE%\.openclaw\workspace\skills\...`）

- **Windows 覆盖安装**
  - `--force` 安装时在 Windows 上改为原地覆盖文件，避免 OpenClaw 占用目录导致 `rename` EPERM

- **`insentek_cli.py`**
  - 移除对话侧 `auth --appid/--secret` 写入能力；凭据仅通过 CLI `login` 配置
  - `check` 增加 `credentials` 检查项

- **文档**
  - 更新 `docs/getting-started.md`、`docs/interaction.md`、`docs/platform-setup.md`、`examples/queries.md`
  - CLI README 补充 scope 路径说明与凭据命令

Fixed
-----

- OpenClaw workspace 目录解析错误（此前误用项目根目录下的 `skills/`）
- Python 无法解密 Node CLI 写入的加密凭据
- Agent 在 login 后误用 `npx insentek-api-skill devices`（非顶层命令）或相对路径脚本

[1.1.0] - 2026-05-22
--------------------

Changed
-------

- **结构性重构: skill.md 模块化拆分**
  - 主 `skill.md` 从 1100+ 行瘦身至 ~250 行 (Runtime Contract 风格)
  - 新增 `docs/interaction.md` — 意图解析、时间表达式、输出格式、确认策略
  - 新增 `docs/analysis.md` — 分析策略、报告生成、告警规则、行业参数
  - 新增 `examples/flows.md` — 3 个核心交互示例（查询/导出/报告含数据校验）
  - 删除 `examples/alerts.md`（内容合并至 docs/analysis.md）

- **MUST → SHOULD 降级**
  - 安全/护栏类保持 MUST（raw_data_output, span limit, auth security）
  - 分析类降级为 SHOULD / RECOMMENDED / PREFER
  - 模型分析创造力不再被规则过度压制

- **三层职责分离**
  - Runtime Contract（skill.md）: 工具、护栏、认证、路由
  - Interaction Policy（docs/interaction.md）: UX、确认、输出格式
  - Analysis Engine（docs/analysis.md）: 动态分析、报告、可视化

- **新增 Routing 决策表**
  - skill.md Section 1: L1意图 × L2输出 → 工具路由矩阵
  - Agent 无需逐行阅读即可快速定位调用路径

- **版本号统一 bumped 1.0.3 → 1.1.0**
  - skill.md, README.md, PLATFORM-TEST.md, docs/platform-setup.md

[1.0.3] - 2026-05-22
--------------------

Added
-----

- 数据可用性校验 (skill.md Section 2.5)
  - `query_data` 返回后 Agent 必须检查实际数据范围 vs 用户请求范围
  - 若实际覆盖比例 < 50% 或天数 < 7 天，必须 STOP 并向用户确认
  - 确认消息包含：请求范围、实际范围、可能原因（设备未部署/离线）
  - 用户确认后才允许继续生成报告

- 报告时间范围标注规范 (skill.md Section 8.3)
  - 实际范围 = 请求范围：正常标注
  - 实际范围 < 请求范围：必须注明 "基于实际可用数据: [actual_range]"
  - 绝不允许用请求范围替代实际范围，避免误导用户

- Flow 7 数据范围不匹配处理示例 (skill.md Section 12)
  - 新增完整交互示例：用户请求近3个月，实际仅13天
  - 展示 Agent 如何向用户说明情况并等待确认

Changed
-------

- 报告生成流程 (skill.md Section 8.3)
  - 在 `query_data` 与 `Agent analyzes data` 之间插入数据可用性校验步骤
  - Flow 6 增加 `[数据可用性校验] → PASS` 标注

- 版本号统一 bumped 1.0.2 → 1.0.3
  - skill.md, README.md, PLATFORM-TEST.md, docs/platform-setup.md

Why
---

- 用户实际测试发现：请求近3个月数据时，设备仅有13天数据
- 旧版本直接生成报告并标注"近3个月"，对用户产生严重误导
- 新增校验机制确保报告时间范围真实反映数据可用性

[1.0.2] - 2026-05-21
--------------------

Added
-----

- `scripts/write_html.py` — HTML file writer utility
  - Receives AI-generated HTML content and writes it to disk
  - No templating or data processing; purely a safe file-writing tool
  - Supports `--content`, `--input-file`, and stdin input
  - Minimal HTML structure validation (warnings only, non-blocking)
  - Structured JSON output for Agent consumption

Changed
-------

- Removed deprecated `report` / `chart` / `export --format html` from `scripts/insentek_cli.py`
  - Deleted `generate_report()`, `generate_chart()`, `get_device_info()`, `extract_param_names()` (~480 lines)
  - HTML reports are now fully Agent-generated; no hard-coded templates
  - Updated docstring and argparse to reflect only csv/json export

- Updated `skill.md`
  - Replaced Section 6.4 `generate_report (DEPRECATED)` with 6.4 `write_html`
  - Added `write_html.py` to environment check items (non-critical)
  - Changed API doc reference from active guidance to fallback note in Notes
  - Updated `--dry-run` note to remove `report` and `chart`

- Updated `.planning/STATE.md`
  - Added `write_html.py` to Utility Scripts list
  - Removed HTML export from `insentek_cli.py` description

Why
---

- User requirements for reports are diverse; fixed templates cannot cover all scenarios
- Delegate report generation to AI for flexibility (dynamic analysis, custom visualizations)
- Provide a clean, single-purpose tool for HTML file output rather than monolithic report generators

[1.0.1] - 2026-05-21
--------------------

Added
-----

- --dry-run preview mode (scripts/insentek_cli.py)
  - data, export (csv/json/html), report, chart subcommands all support --dry-run
  - Only outputs record count, time range, field summary (nodes/parameters), and first 5 sample rows
  - Does not write files or output full data, preventing context explosion during debugging

- --dry-run preview mode (scripts/export_excel.py)
  - Added --dry-run parameter, behavior consistent with CLI script
  - Does not generate Excel file, only returns structured JSON preview

- Raw data output prohibition (skill.md)
  - Added Section 2.4 "Raw Data Output Prohibition"
  - Explicitly prohibits Agent from outputting raw sensor full data directly into conversation
  - Specifies handling for four common scenarios: summary sampling, --dry-run, guided export, direct refusal

- YAML Guardrails declaration (skill.md frontmatter)
  - Added guardrails.raw_data_output: PROHIBITED
  - Added guardrails.dry_run_preview_rows: 5
  - Added guardrails.max_chat_rows: 200
  - Added guardrails.max_export_rows: 50000

- Dry-run documentation (skill.md)
  - Added Section 6.0 "dry-run preview mode (common to all export scripts)"
  - Added --dry-run example in query_data Agent Action
  - Added "Dry-run first" and "Raw data prohibition" development guidelines in Notes

Changed
-------

- Version bumped from 1.0.0 to 1.0.1 (skill.md, README.md, PLATFORM-TEST.md, .planning/STATE.md)

Why
---

- Prevent accidental full sensor data injection into conversation context
- Save Token consumption and improve model processing efficiency
- Promote as Skill development standard: summaries in chat, full data in files


[1.0.0] - 2026-05-14
--------------------

Added
-----

- Initial release with intent resolution, query guardrails, and export scripts
- Three-layer intent model (L1 core -> L2 output -> L3 format)
- Query guardrails: max 365 days span, max 3 years history, max 200 chat rows, max 50000 export rows
- Utility scripts: insentek_cli.py (unified CLI), export_excel.py (Excel export)
- Environment prerequisites check command
- Session-based authentication caching
- Multi-industry adaptation (agriculture, meteorology, industrial level monitoring)
