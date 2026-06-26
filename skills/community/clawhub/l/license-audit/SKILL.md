---
name: license-audit
description: >
  Multi-language license compliance audit powered by Trivy.
  Detects GPL/AGPL/LGPL/MPL/BSL and other risky licenses across Node.js, Python,
  Java, C#/.NET, Go, Rust, Ruby, PHP, and C/C++. Outputs to terminal, Markdown,
  HTML, JSON, Feishu Doc, and Feishu Base. Supports NuGet API enrichment for C#
  projects and automatic stack detection with pre-scan guidance.
license: MIT
tags: [license, compliance, security, trivy, open-source, feishu]
metadata:
  requires:
    bins: [trivy, python3, git]
  optional_bins: [lark-cli]
  version: "2.0.0"
  author: Theo / Nanshe
---

# License Audit (Trivy-based) · 开源许可证合规扫描

> Scan any codebase for commercially risky licenses in seconds.
> 几秒钟内扫描任意代码库的商业风险许可证。

---

## Overview · 概述

**English**: A CLI tool that runs [Trivy](https://github.com/aquasecurity/trivy) under the hood to detect open-source dependencies with licenses that may block commercial use (GPL, AGPL, SSPL, etc.). It automatically identifies the project's tech stack, pre-warns when dependencies need to be installed first, enriches C#/.NET results via the NuGet API, and outputs reports in six formats — including Feishu Doc and Feishu Base for team collaboration.

**中文**: 基于 [Trivy](https://github.com/aquasecurity/trivy) 的命令行工具，自动扫描开源依赖的许可证风险（GPL、AGPL、SSPL 等商业限制许可证）。支持自动识别技术栈、扫描前预警、C#/.NET 项目自动通过 NuGet API 补全许可证信息，输出六种格式报告，包括飞书文档和飞书多维表格，便于团队协作审查。

---

## Requirements · 环境要求

| Tool | Purpose | Install |
|------|---------|---------|
| `python3` (≥ 3.9) | Run the script | Built-in on macOS/Linux |
| `trivy` | License scanning engine | `brew install trivy` |
| `git` | Clone remote repos | Built-in on most systems |
| `lark-cli` | Feishu output only · 仅飞书输出需要 | See Feishu Setup below |

---

## Quick Start · 快速开始

```bash
SCRIPT=~/.hermes/skills/dev-tools/license-audit/scripts/audit.py

# Scan local project (terminal table output)
# 扫描本地项目（终端表格输出）
python3 $SCRIPT /path/to/project

# Scan a remote git repo
# 扫描远程 Git 仓库
python3 $SCRIPT https://github.com/user/repo.git

# Private repo with token · 私有仓库带 Token
python3 $SCRIPT https://user:TOKEN@git.company.com/org/repo

# Save as Markdown (timestamped filename auto-generated)
# 保存为 Markdown（文件名自动带时间戳）
python3 $SCRIPT --format markdown /path/to/project

# Save as HTML · 保存为 HTML
python3 $SCRIPT --format html /path/to/project

# Save as JSON · 保存为 JSON
python3 $SCRIPT --format json /path/to/project

# Output to Feishu Doc · 输出到飞书文档
python3 $SCRIPT --format feishu-doc /path/to/project

# Output to Feishu Base (multi-dim table) · 输出到飞书多维表格
python3 $SCRIPT --format feishu-base /path/to/project

# Skip NuGet/API enrichment (offline mode) · 跳过 API 补全（离线模式）
python3 $SCRIPT --no-enrich /path/to/project

# Specify output path explicitly · 手动指定输出路径
python3 $SCRIPT --format html -o /tmp/my-report.html /path/to/project
```

---

## Output Formats · 输出格式

| Format | Flag | File naming | Best for |
|--------|------|-------------|----------|
| Terminal table | _(default)_ | stdout | Quick local checks · 快速本地检查 |
| Markdown | `--format markdown` | `license-audit-<project>-<timestamp>.md` | PR comments, docs · PR 评审、文档 |
| HTML | `--format html` | `license-audit-<project>-<timestamp>.html` | Dark-themed standalone report · 暗色主题报告 |
| JSON | `--format json` | `license-audit-<project>-<timestamp>.json` | CI/CD pipelines · CI/CD 集成 |
| Feishu Doc | `--format feishu-doc` | Cloud URL | Team review · 团队协作审查 |
| Feishu Base | `--format feishu-base` | Cloud URL | Filterable records · 可筛选多维表格 |

> File formats (markdown/html/json) auto-generate a timestamped filename in the current directory when `--output` is not specified, so repeated scans never overwrite each other.
>
> 文件格式（markdown/html/json）在不指定 `--output` 时自动生成带时间戳的文件名，多次扫描不会互相覆盖。

---

## Risk Tiers · 风险等级

| Tier | Licenses | Commercial impact |
|------|----------|-------------------|
| 🔴 HIGH | GPL-2/3, AGPL-1/3, EUPL | Strong copyleft — likely forces your code open-source · 强 Copyleft，可能导致代码被迫开源 |
| 🟡 MEDIUM | LGPL, MPL, EPL, CDDL, BSL, BUSL, SSPL | Conditional copyleft — review usage terms · 条件性 Copyleft，需审查使用条款 |
| 🟢 LOW | MIT, Apache-2.0, BSD, ISC, CC0 | Commercial-friendly · 商业友好 |
| ⚠️ UNKNOWN | Not identified | Manual verification needed · 需人工核查 |

---

## Stack Support · 技术栈支持

| Stack | Manifest files | Trivy support | Auto-enrichment |
|-------|---------------|---------------|-----------------|
| Node.js | `package.json`, `pnpm-lock.yaml`, `yarn.lock` | ✅ needs `node_modules` | — |
| Python | `pyproject.toml`, `requirements.txt`, `poetry.lock`, `Pipfile.lock` | ✅ | — |
| Java / Maven | `pom.xml` | ✅ | — |
| Java / Gradle | `build.gradle`, `build.gradle.kts` | ✅ | — |
| C# / .NET | `packages.config`, `*.csproj` | ⚠️ names only | ✅ NuGet API |
| Go | `go.mod` | ✅ | — |
| Rust | `Cargo.toml` | ✅ | — |
| C/C++ (Conan) | `conanfile.txt`, `conanfile.py` | ✅ | — |
| C/C++ (CMake) | `CMakeLists.txt` | ❌ no standard manifest | — |
| Ruby | `Gemfile.lock` | ✅ | — |
| PHP | `composer.lock` | ✅ | — |

The script **auto-detects stacks** before scanning and prints targeted guidance:
- Node.js: warns if `node_modules` is missing and tells you which install command to run
- C#/.NET: automatically calls the NuGet v3 registration API to fill in license info that Trivy can't read from `packages.config`

脚本**自动检测技术栈**，扫描前给出针对性提示：
- Node.js：若缺少 `node_modules` 则提前报警并给出安装命令
- C#/.NET：自动调用 NuGet v3 API 补全 `packages.config` 中 Trivy 无法读取的许可证信息

---

## Feishu Setup · 飞书配置

> Feishu output uses **personal user identity** — created docs and bases appear directly in your own Feishu cloud drive, no permission requests needed.
>
> 飞书输出使用**个人用户身份**，创建的文档和多维表格直接出现在你自己的云空间，无需向机器人申请权限。

### Step 1 — Install lark-cli · 安装 lark-cli

```bash
# macOS
brew install nousresearch/tap/lark-cli

# Or via pip
pip install lark-cli
```

### Step 2 — Configure Feishu App · 配置飞书应用

1. Go to [open.feishu.cn](https://open.feishu.cn) → Create an **Internal App** (企业自建应用)
2. Apply for these API scopes (功能权限):
   - `bitable:app` (多维表格)
   - `docx:document:create` (云文档)
3. Enterprise admin approves the scopes
4. Copy **App ID** and **App Secret** → run:

```bash
lark-cli config set app-id YOUR_APP_ID
lark-cli config set app-secret YOUR_APP_SECRET
```

### Step 3 — Authenticate as User · 用户授权

```bash
# Start device auth (get the URL)
# 启动设备授权（获取登录链接）
lark-cli auth login --no-wait --domain base,docs

# Open the printed URL in your browser and confirm login
# 在浏览器打开链接并确认登录

# Complete auth with the device code shown
# 用页面上显示的 device code 完成授权
lark-cli auth login --device-code <device_code>
```

> Device codes expire in ~10 minutes. If you see "expired", re-run step 3 from the start.
> Device code 有效期约 10 分钟，过期重新执行步骤 3。

### Optional: specify a folder · 可选：指定存储文件夹

```bash
# Docs/bases will be created inside the specified folder
# 文档/表格将创建在指定文件夹下
python3 $SCRIPT --format feishu-doc --feishu-folder fldcnXXXXXXXX /path/to/project
```

---

## How It Works · 工作原理

```
Input (local path / git URL)
        │
        ▼
Stack Detection  →  pre-scan warnings (node_modules missing, etc.)
        │
        ▼
Trivy fs/repo scan  →  JSON with package names, versions, licenses
        │
        ▼
parse_results()  →  classify into HIGH / MEDIUM / LOW / UNKNOWN
        │
        ▼
NuGet API enrichment (C#/.NET only)  →  fill UNKNOWN via nuget.org
        │
        ▼
Output: table | markdown | html | json | feishu-doc | feishu-base
```

---

## Common High-Risk Replacements · 常见高风险依赖替换建议

| Risky package | License | Safe alternative |
|--------------|---------|-----------------|
| iText 7 | AGPL-3.0 | Apache PDFBox (Apache-2.0) |
| MySQL Connector/J | GPL-2.0 | MariaDB Connector/J (LGPL) |
| XXL-JOB | GPL-3.0 | PowerJob / DolphinScheduler (Apache-2.0) |
| Logback | EPL-1.0 / LGPL | Log4j2 (Apache-2.0) |
| MongoDB driver | SSPL-1.0 | Use as external service; don't embed |

---

## CI/CD Integration · CI/CD 集成

```yaml
# GitHub Actions example · GitHub Actions 示例
- name: License Audit
  run: |
    pip install trivy  # or: brew install trivy
    python3 audit.py --format json -o license-report.json .
  # Exit code 1 if any HIGH-risk license is found
  # 发现高风险许可证时退出码为 1
```

---

## Known Limitations · 已知限制

- Only scans manifest files; runtime/dynamic dependencies not covered · 仅扫描 manifest 文件，运行时动态依赖不在范围内
- NuGet enrichment: very old package versions or private NuGet feeds may still show UNKNOWN · NuGet 补全：极旧版本或私有 Feed 仍可能显示 UNKNOWN
- C/C++ with CMake only: no standard manifest, Trivy finds nothing · CMake 纯 C/C++ 项目无标准 manifest，Trivy 无法扫描
- Large repos: scan may take 2–5 minutes · 大型仓库扫描可能需要 2–5 分钟

---

## Code Review Reference

When reviewing or extending `scripts/audit.py`, load `references/code-review-checklist.md` — it lists security checks, dead-code signals, error-handling invariants, and Feishu-specific API gotchas discovered during audit sessions.

---

## Pitfalls · 常见陷阱

### Node.js: all UNKNOWN without node_modules

Trivy scanning lockfiles (`pnpm-lock.yaml`, `yarn.lock`, `package-lock.json`) without `node_modules` returns packages with no license data. Always install first:

```bash
pnpm install  # or: npm install / yarn
```

The script detects this and warns you before scanning.

### C#/.NET: packages.config has no license data

`packages.config` only stores package IDs and versions; license info is not embedded. The script automatically queries the NuGet v3 API to fill this in. Very old packages (pre-2017) or packages with GitHub raw `licenseUrl` may still be UNKNOWN — check the printed nuget.org link manually.

### lark-cli: enterprise app approval required

`--as user` auth requires an internal enterprise Feishu app. Personal Feishu accounts cannot grant `bitable` and `docx` scopes without admin approval. Auth will fail with `authorization failed: The app is pending approval` until the admin approves.

### lark-cli response envelope

All responses are `{"ok": true, "data": {...}}`. Key paths:
- `docs +create` → `data.doc_url`
- `base +base-create` → `data.base.base_token`, `data.base.url`
- `base +table-create` → `data.table.id` (not `table_id`)
- `base +table-list` → `data.tables[].id`

### Batch writes need a delay

`+record-batch-create` batches must be serial with 0.6 s between calls. Parallel writes cause conflict error `1254291`.

### `publish_feishu_doc` failure returns raw markdown (historical, fixed)

On lark-cli failure the original code did `return md` — the entire markdown content string. `main()` then either wrote it to a file or printed hundreds of lines to the terminal. Fixed to `return ""` so a failed Feishu publish is silent after the error message.

### `ensure_trivy()` was dead code (historical, fixed)

The function existed but `run_trivy()` hard-coded `"trivy"` as `cmd[0]`. Fixed: `run_trivy()` now calls `ensure_trivy()` and substitutes the resolved path, so trivy is auto-installed if missing.

### HTML output lacked entity escaping (historical, fixed)

Package names and license strings in the HTML renderer were interpolated raw. Fixed: `.replace("&","&amp;").replace("<","&lt;")` applied to both fields before insertion.

### Dead condition in `enrich_nuget` (historical, fixed)

The enrichment filter checked `item["license"] == "(no license info — run with node_modules present)"` — a placeholder string from an older version that was never produced by `parse_results`. The condition was dead. Simplified to `not item["license"] or not item.get("all_licenses")`.

### `from datetime import datetime` inside function body (historical, fixed)

Was placed inside `main()` for the timestamp logic. Moved to the top-level import block for consistency.

### `rstrip(".git")` bug (historical, fixed)

`str.rstrip(chars)` strips individual characters, not a suffix. `"digital_agent".rstrip(".git")` → `"digital_agen"` because `t` is in the char set. Fixed by using `endswith(".git")` + `[:-4]` slice.
