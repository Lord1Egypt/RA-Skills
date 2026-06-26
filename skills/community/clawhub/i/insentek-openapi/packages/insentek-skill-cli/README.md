# @insentek/openapi-skill

Bootstrap the **insentek-openapi** skill for **OpenClaw** and **Claude Code**.

| 类型 | 名称 |
|------|------|
| npm package | `@insentek/openapi-skill` |
| skill id | `insentek-openapi` |
| 安装目录 | `insentek-openapi` |
| CLI 命令 | `insentek-openapi` |
| ClawHub slug | `insentek-openapi` |

安装路径由 CLI **按 runtime + scope 动态解析**。用 `info` / `doctor` 查看本机实际路径。

## Quick Start

```bash
npx @insentek/openapi-skill
```

## OpenClaw 用户：ClawHub 安装（独立方式）

OpenClaw 用户也可通过 ClawHub 单独安装，与本 CLI 无关：

```bash
openclaw skills install insentek-openapi
openclaw skills remove insentek-openapi
```

## Commands

| Command | Description |
|---------|-------------|
| `install` | 安装 skill（默认命令，可交互选择 runtime） |
| `login` | 配置 Insentek API 凭据（加密本地保存） |
| `logout` | 清除已保存的凭据 |
| `auth status` | 查看凭据连接状态 |
| `update` | 更新已安装 skill 到当前包版本（默认扫描全部 runtime × scope，多个匹配时交互多选；`-y` 自动全选） |
| `uninstall` | 卸载 |
| `status` | 查看安装状态 |
| `doctor` | 诊断路径、manifest、脚本与环境 |
| `info` | 查看 package / skill / 动态解析路径 |

## Options

| Option | Description |
|--------|-------------|
| `-r, --runtime` | `claude`, `openclaw`, `all` |
| `-s, --scope` | 见下方 Scope 说明 |
| `-f, --force` | 覆盖已有安装 |
| `-y, --yes` | 非交互（需配合 `-r`） |
| `--json` | 输出 JSON（`install`/`update`/`uninstall` 需配合 `-y`） |

### Scope 说明

| Runtime | 支持的 scope |
|---------|-------------|
| Claude Code | `global`（默认）, `project` |
| OpenClaw | `global`, `project`, `workspace` |

`workspace` 仅 OpenClaw 支持；Claude Code 没有 workspace 概念。OpenClaw `workspace` 安装路径为 `~/.openclaw/workspace/skills`（Windows: `%USERPROFILE%\.openclaw\workspace\skills`）。

## Examples

```bash
# 交互式安装
npx @insentek/openapi-skill

# 安装到 Claude Code（global）
npx @insentek/openapi-skill install -r claude -s global -y

# 安装到 OpenClaw workspace
npx @insentek/openapi-skill install -r openclaw -s workspace -y

# 查安装路径与脚本位置（Agent 应用此解析 SKILL_ROOT）
npx @insentek/openapi-skill status -r openclaw -s workspace --json

# 更新 skill（默认扫描所有 runtime × scope，多个匹配时交互多选）
npx @insentek/openapi-skill update
# 非交互：自动全选所有已安装位置（含 OpenClaw workspace）
npx @insentek/openapi-skill update -y
# 精确单点更新（已装则覆盖，未装则按 force 创建）
npx @insentek/openapi-skill update -r openclaw -s workspace -y

# 凭据 / 诊断
npx @insentek/openapi-skill doctor
npx @insentek/openapi-skill login
npx @insentek/openapi-skill logout
npx @insentek/openapi-skill auth status
npx @insentek/openapi-skill info

# 脚本 / CI 使用 JSON 输出
npx @insentek/openapi-skill status -r claude --json
npx @insentek/openapi-skill install -r claude -s global -y --json
npx @insentek/openapi-skill doctor --json
```

## Development / 本地测试

包尚未发布到 npm 时，`npx @insentek/openapi-skill` 会失败。本地请用下面任一方式：

```powershell
cd packages/insentek-skill-cli
npm install
npm run sync-assets
npm test
```

**方式一：直接跑（最简单）**

```powershell
node bin/insentek-openapi.js info
node bin/insentek-openapi.js
node bin/insentek-openapi.js install -r claude -s global -y
```

**方式二：模拟 npx（在 CLI 目录下）**

```powershell
npx . info
npx .
npx . install -r claude -s global -y
```

**方式三：全局 link 后按发布命令测**

```powershell
npm link
npx @insentek/openapi-skill info
insentek-openapi doctor
```

**方式四：模拟正式发布**

```powershell
npm run sync-assets
npm pack
npm install -g .\insentek-openapi-skill-1.2.4.tgz
insentek-openapi info
```

修改 `SKILL.md` / `scripts/` 后需重新 `npm run sync-assets` 再测。

## Requirements

- Node.js 18+
- Python 3.10+（用于运行 `scripts/insentek_cli.py` 等脚本；CLI 会通过 `findPythonCommand()` 在 macOS/Linux 上优先选择 `python3`，Windows 上优先 `python` / `py`）

`info --json` 输出会在 `environment.python` 以及每个 `runtimes[].scopes[]` 条目下暴露 `python.command`，Agent 应以该值作为脚本调用前缀，而不是裸用 `python`。
