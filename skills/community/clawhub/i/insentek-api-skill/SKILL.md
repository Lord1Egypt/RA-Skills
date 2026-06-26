---
name: insentek-openapi
version: 1.2.2
description: >
  通过自然语言查询 insentek（东方智感）物联网设备数据。
  支持土壤墒情仪、气象站、见厘液位计等多种设备类型的实时数据、
  历史数据、趋势分析、跨设备对比与数据导出。
api_base_url: https://openapi.ecois.info
author: insentek-api-skills
guardrails:
  raw_data_output: PROHIBITED
  dry_run_preview_rows: 5
  max_chat_rows: 200
  max_export_rows: 50000
---

<!--
  Note: `api_base_url` above is informational only; it is not consumed by
  any script. To override at runtime, set the INSENTEK_API_BASE environment
  variable before invoking scripts/insentek_cli.py.
-->


# Insentek OpenAPI Skill

> 轻量 Runtime Contract。完整交互规范见 `docs/interaction.md`，分析策略见 `docs/analysis.md`。
> 兼容平台：OpenClaw、Hermes-Agent、Claude Code、ChatGPT

---

## 1. Routing

用户意图 → 工具路由：

| L1 意图 | L2 输出 | 调用 |
|---------|---------|------|
| 查询数据 | 对话展示 | `query_device` → `query_data` → 按输出格式回复 |
| 查询数据 | 文件导出 | `query_device` → `export_*` → 返回文件路径 |
| 生成报告 | 文件导出 | `query_device` → `query_data` → 分析 → `write_html` |
| 对比设备 | 对话展示 | `query_device` (xN) → `query_data` (xN) → 对比表格 |
| 对比设备 | 文件导出 | `query_device` (xN) → `query_data` (xN) → `export_excel` |

**任何一层意图不明确时，MUST 向用户确认，不得假设。** 详见 `docs/interaction.md` Section 1。

---

## 2. Tools

**认证约束（MUST）：** Agent **禁止**向用户索要 `appid` 或 `secret`，也 **禁止**在对话中接收、存储或回显这些凭据。凭据仅通过 CLI 在本地配置：

```bash
npx @insentek/openapi-skill login       # 配置（加密保存）
npx @insentek/openapi-skill logout      # 清除
npx @insentek/openapi-skill auth status # 查看连接状态
```

> npm 包名为 `@insentek/openapi-skill`（已发布到 npm registry）。`insentek-api-skill` 是它的可执行别名，**仅在该包已被安装时**可用。**所有 `npx` 调用都应使用 scoped 包名** `@insentek/openapi-skill`，否则未安装的用户机器会得到 "npm ERR! 404"。

### 命令分工（MUST）

| 用途 | 工具 | 示例 |
|------|------|------|
| 安装 / 更新 skill | `npx @insentek/openapi-skill` | `install -r openclaw -s workspace -y` |
| 配置 / 清除凭据 | `npx @insentek/openapi-skill login/logout` | `npx @insentek/openapi-skill login` |
| 查连接状态 | `npx @insentek/openapi-skill auth status` | — |
| 查安装路径 / 脚本位置 | `npx @insentek/openapi-skill info/status/doctor --json` | 见下方「脚本路径解析」 |
| **查询 API** | `python3 <SKILL_ROOT>/scripts/insentek_cli.py` | `python3 .../insentek_cli.py devices` |

### 脚本路径解析（MUST，API 调用前）

Agent 工作目录通常**不是** skill 安装目录。**禁止**使用相对路径 `python3 scripts/insentek_cli.py ...`。

**首次 API 调用前**，或脚本路径未知 / 返回「文件找不到」时，**必须先**查实际安装位置。`info --json` 会列出所有 runtime × scope 的解析结果及 `installed` 标记，无需提前知道用户是哪种安装：

```bash
npx @insentek/openapi-skill info --json
```

从输出中遍历 `runtimes[].scopes[]`，挑选第一个 `installed: true` 的条目，将其 `installDir` 作为 `${SKILL_ROOT}`，将 `scripts.cli` / `scripts.exportExcel` / `scripts.writeHtml` 作为脚本绝对路径，并将 `python.command`（如 `python3` / `py` / `python`）作为 `${PYTHON}`。解析后在**本会话内缓存**，后续 API 调用复用，**不要**重复猜测路径。

如果用户已经明确告诉过你 runtime / scope（例如刚刚 `install -r openclaw -s workspace -y`），也可以用 `status --json` 精确查询：

```bash
npx @insentek/openapi-skill status -r openclaw -s workspace --json
# 或 -r claude -s global / -s project，按用户场景选择
```

OpenClaw workspace 常见路径（仅供参考，**以 info/status 返回为准**）：
`~/.openclaw/workspace/skills/insentek-openapi`

**禁止（MUST NOT）：**
- `python3 scripts/insentek_cli.py ...` — 相对路径在 OpenClaw 等环境下会失败
- `npx insentek-api-skill ...` — npm registry 上没有这个包名，对未安装本包的新用户会 404
- `npx @insentek/openapi-skill devices` — `devices` 不是顶层命令，会被 commander 当成 `install` 的子命令而触发安装流程
- 文件找不到时乱试其它命令 — **应重新 `info --json`**

用户说「配置好了，继续吧」→ 从**中断前的意图**继续；若已有 `${SKILL_ROOT}` 直接调 API，**不要**重新 login。

若工具返回 `authentication_required` 或 HTTP 401/403，**STOP** 并 **原样** 向用户展示以下固定文案（不得改写、不得追加索要 secret）：

```
这台电脑还没有连接 Insentek API，需要先完成一次本地配置，通常 1 分钟就好。

请在终端运行：

npx @insentek/openapi-skill login

按提示输入 appid 和 secret 即可（加密保存在本机，无需发到这个对话）。配置完成后回来继续提问，我接着帮你处理。
```

---

### query_device

查询设备信息：列表、详情、别名解析。

```json
{
  "page": { "type": "integer", "default": 1 },
  "limit": { "type": "integer", "default": 20 },
  "sn": { "type": "string", "description": "设备序列号，与 alias 二选一" },
  "alias": { "type": "string", "description": "设备别名，支持部分匹配" }
}
```

```bash
# 列表（${SKILL_ROOT} / ${PYTHON} 由 info --json 解析，见上方）
${PYTHON} ${SKILL_ROOT}/scripts/insentek_cli.py devices [--page ${page}] [--limit ${limit}]
# 详情
${PYTHON} ${SKILL_ROOT}/scripts/insentek_cli.py device --sn ${sn}
```

> `${PYTHON}` 在 macOS/Linux 默认为 `python3`，Windows 默认为 `python`（亦可为 `py`）；以 `info --json` 输出的 `python.command` 为准。**禁止**使用裸 `python`——在 macOS 系统默认配置、新版 Ubuntu/Fedora 等环境下 `python` 命令不存在或指向 Python 2，会直接失败。

**注意：** `--token` 变为可选。若未提供且已配置持久化凭据，脚本自动获取。

**行为：** alias → 模糊匹配 → 多匹配时反问用户 → 单匹配时缓存 alias→sn 映射。

---

### query_data

查询设备历史数据或实时数据。

```json
{
  "sn": { "type": "string", "required": true },
  "time_expression": { "type": "string", "description": "自然语言时间描述，如'现在'、'昨天'、'最近7天'。不传默认最近24小时。" },
  "range": { "type": "string", "description": "YYYYMMDD,YYYYMMDD，由 time_expression 自动计算" },
  "includeParameters": { "type": "string", "description": "指定参数，逗号分隔，如 moisture,temperature" }
}
```

```bash
# 历史数据
${PYTHON} ${SKILL_ROOT}/scripts/insentek_cli.py data --sn ${sn} --range ${range} [--include-params ${params}]

# 预览（调试/验证用）
${PYTHON} ${SKILL_ROOT}/scripts/insentek_cli.py data --sn ${sn} --range ${range} --dry-run

# 实时数据（latest）
${PYTHON} ${SKILL_ROOT}/scripts/insentek_cli.py latest --sn ${sn}
```

**注意：** `--token` 变为可选。若未提供且已配置持久化凭据，脚本自动获取。

时间表达式解析见 `docs/interaction.md` Section 2。

---

### export_csv / export_excel / export_json

用户意图明确为"导出/下载"时调用，而非 `query_data`。

```bash
# CSV
${PYTHON} ${SKILL_ROOT}/scripts/insentek_cli.py export --sn ${sn} --range ${range} --format csv --output ${file}.csv

# Excel
${PYTHON} ${SKILL_ROOT}/scripts/export_excel.py --sn ${sn} --range ${range} --output ${file}.xlsx

# JSON
${PYTHON} ${SKILL_ROOT}/scripts/insentek_cli.py export --sn ${sn} --range ${range} --format json --output ${file}.json
```

**注意：** `--token` 变为可选。若未提供且已配置持久化凭据，脚本自动获取。

所有导出脚本均支持 `--dry-run`。

---

### write_html

Agent 完成数据分析后，将动态生成的 HTML 内容写入文件。**推荐**使用 `--input-file` 避免 shell 转义吞掉换行 / 引号 / 反斜杠：

```bash
# 1. 先把 HTML 内容写到临时文件（写文件工具按平台决定）
#    e.g. write to /tmp/report.html or %TEMP%\report.html
# 2. 然后调用 write_html.py 落盘
${PYTHON} ${SKILL_ROOT}/scripts/write_html.py --input-file ${tmp_html} --output ${file}.html

# 也支持 stdin（注意 echo 会破坏 HTML 中的换行/引号，仅用于简单片段）：
echo "${html_content}" | ${PYTHON} ${SKILL_ROOT}/scripts/write_html.py --output ${file}.html
```

---

## 3. Guardrails

### 3.1 硬限制

| 限制项 | 规则 | 超限处理 |
|--------|------|----------|
| 单次查询跨度 | ≤ 365 天 | 拒绝，提供拆分选项 |
| 历史回溯 | ≤ 3 年 | 拒绝，提示最早日期 |
| 对话展示 | ≤ 200 条 | 展示摘要 + 首尾各 10 条抽样 |
| 文件导出 | ≤ 50,000 条 | 拒绝，建议缩小范围或分批 |

### 3.2 数据可用性校验（MUST）

`query_data` 返回后，检查实际数据范围 vs 请求范围：

```
requested_days = 用户请求的天数
actual_days    = 实际返回数据的天数
coverage       = actual_days / requested_days

IF coverage < 0.5 OR actual_days < 7:
  → STOP
  → 告知用户实际范围，询问是否继续
  → 等待确认后才可生成报告/分析
ELSE IF actual_range < requested_range:
  → 继续，但报告 MUST 使用 actual_range 标注
```

### 3.3 原始数据输出禁令（MUST）

Agent **禁止**将原始传感器全量数据输出到对话中。

| 场景 | 处理 |
|------|------|
| "看看数据" | 统计摘要 + 首尾各 5 条 |
| "调试" | `--dry-run` 预览 |
| "给我原始数据" | 引导导出 CSV/Excel |
| "全部发给我" | 拒绝，解释 Token 限制 |

完整输出格式规范见 `docs/interaction.md` Section 4。

---

## 4. Authentication

### 4.1 CLI 本地凭据（唯一方式）

用户 **必须** 通过 CLI 在本地配置凭据，Agent **不得** 在对话中收集 appid/secret：

```bash
npx @insentek/openapi-skill login
npx @insentek/openapi-skill logout
npx @insentek/openapi-skill auth status
```

凭据加密保存在 `~/.config/insentek/credentials.json`（文件权限 600）。

### 4.2 Agent 行为约束（MUST）

| 场景 | Agent 行为 |
|------|-----------|
| 用户首次使用 / 未连接 | 展示 Section 2 固定引导文案，**禁止**索要 secret |
| 用户主动发送 appid/secret | **拒绝接收**，说明请改用 CLI login |
| 401/403 / `authentication_required` | 展示 Section 2 固定引导文案，STOP |
| 用户要求"重新认证" | 引导 `npx @insentek/openapi-skill login`（更新）或 `logout` 后再 `login` |

### 4.3 Token 获取策略

脚本**管理 token 生命周期**，实现缓存 + 自动刷新机制：
- CLI `login` 验证凭据后，凭据和 token 一并加密保存
- 后续各命令 `--token` 参数变为可选
- 未提供 `--token` 时，脚本**优先从配置文件读取缓存的 token**
- 请求 API 时如果返回 401/403，脚本**自动刷新 token** 并重试一次
- 刷新失败则返回 `authentication_required`，Agent 引导用户重新 `login`
- 不检查 token 过期时间，靠 HTTP 401/403 触发刷新

### 4.4 Token 缓存流程

```
请求 API
  ├── 使用缓存 token
  ├── 成功 → 返回数据
  └── 401/403 → 调用 /v3/token 获取新 token → 更新配置文件 → 重试请求
        └── 仍失败 → 返回 authentication_required → 引导 CLI login
```

### 4.5 安全说明

- Secret **绝不**出现在对话、日志或 Agent 上下文中
- 凭据文件权限 600，内容 AES-256-GCM 加密（机器绑定密钥）
- Token 缓存有效期约 2 小时，靠 HTTP 401/403 触发自动刷新

---

**向后兼容：** 所有命令仍支持 `--token` 参数，现有调用方式不受影响。

---

## 5. Environment Check

首次交互前，在解析 `${SKILL_ROOT}` / `${PYTHON}` 后执行：

```bash
${PYTHON} ${SKILL_ROOT}/scripts/insentek_cli.py check
```

关键项失败时 STOP，可选项失败时降级运行并告知用户。

若 `${PYTHON}` 解析失败（`info --json` 的 `python.ok` 为 `false`），说明本机没有可用的 Python 3.10+，**STOP** 并原样向用户展示：

```
当前电脑没有可用的 Python（需要 3.10 或更高版本）。请先安装 Python：

- macOS: brew install python
- Ubuntu/Debian: sudo apt install python3 python3-pip
- Fedora: sudo dnf install python3
- Windows: 到 https://www.python.org/downloads/ 下载安装包，安装时勾选 "Add Python to PATH"

安装完成后请回来继续提问，我接着帮你处理。
```

若 `checks.credentials.ok` 为 `false`，展示 Section 2 固定引导文案，**禁止**继续调用 API 或向用户索要 secret。

---

## 6. Error Handling

| HTTP | 处理 |
|------|------|
| 200 | 正常处理 |
| 400 | 检查参数格式后重试 |
| 401/403 | **STOP**，展示 CLI login 引导文案，**禁止**向用户索要 secret |
| 脚本找不到 / ENOENT | **STOP**，执行 `status --json` 或 `info --json` 解析 `${SKILL_ROOT}`，**禁止**乱试 npx 子命令 |
| 404 | 确认设备 SN/别名 |
| 429 | 限流，等待后重试 |
| 500 | 指数退避重试 3 次 |

脚本返回 `"success": false` 且 `error` 为 `authentication_required` 时，展示 Section 2 固定引导文案并 STOP。其他错误解析 `error`/`message` 字段：含"范围/限制"则解释护栏，否则展示友好错误。

---

## Notes

- **Pagination**: `page` starts at 1.
- **Values**: Nested `{node_name: {parameter_code: value}}`
- **Alias**: Case-insensitive partial match on `alias`.
- **Param names**: Use Chinese names from `/description` endpoint for display.
- **Script-first**: API 用 `${PYTHON} ${SKILL_ROOT}/scripts/insentek_cli.py`；`${SKILL_ROOT}` 和 `${PYTHON}` 由 `info --json` 解析（`runtimes[].scopes[]` 中 `installed: true` 的条目对应 `installDir` / `scripts.cli` / `python.command`）
- **Dry-run**: Append `--dry-run` for preview; never output raw data to chat.
- **Reference**: Edge cases → `reference/api-doc.md` (OpenAPI v3.1.9).
