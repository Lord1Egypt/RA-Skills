# MCP / Agent 接口

本技能为 Agent/上层应用提供两种稳定接口：**CLI JSON** 与 **stdio MCP**。凭据一律不出口：系统凭据库密码、Cookie、Token 不会出现在任何 JSON/text 输出里。

## 1. CLI JSON（开箱即用，无外部依赖）

| 子命令 | 说明 |
|---|---|
| `pan.py doctor --json` | 环境与依赖检查 |
| `pan.py detect <url> [--json]` | 识别网盘（默认即 JSON） |
| `pan.py dirs --json` | 默认下载目录 |
| `pan.py secret check --json` | 凭据引用状态 |
| `pan.py secret list --json` | 配置中的凭据引用清单（不打码） |
| `pan.py remote list --json` | 远程设备状态 |
| `pan.py remote check <name> --json` | 远程连通性检查 |
| `pan.py remote deploy <name> --json` | 部署计划（不执行上传） |
| `pan.py get <url> --dry-run --json` | 下载计划（只读） |
| `pan.py get <url> --events` | 实际下载时逐步 JSON 事件流 |

## 2. stdio MCP 服务器

脚本：`scripts/pan_mcp.py`（纯 Python，无第三方依赖）。

暴露工具：
- `pan_doctor`：环境检查 JSON
- `pan_detect`：识别网盘
- `pan_dirs`：默认下载目录
- `pan_get_plan`：生成 dry-run 下载计划（只读，不回传凭据）

一键得到注册片段：`python3 scripts/pan.py mcp guide`（加 `--json` 取机器可读）。

注册到 Codex `$CODEX_HOME/config.toml`（`[mcp_servers]` 段）：

```toml
[mcp_servers.pan-cloud-drive]
command = "$CODEX_HOME/skills/pan-hub/scripts/pan_mcp.py"
enabled = true
# type 默认 stdio；如被 Agent 配置切换工具 覆盖，需重新注册并重启 App
```

注册后需在运行中的 App 重启生效；本机 skill 原版保持完整，平台/App 专用配置不回写 skill。

## 3. 安全边界

- `pan_get_plan` 只生成计划，不执行下载、不读取系统凭据明文。
- `--events` 输出步骤参数全部打码；`content` 内不含密码/Token/Cookie。
- 参数中的 `pwd` 是分享提取码（非账号密码），仍按最小必要原则传递。
- 实际下载仍只在本机 CLI 完成；MCP 工具不做上传、不做转发。

## 只读状态页

`python3 scripts/pan.py serve --reports-dir <报告目录>` 启动本地只读页面（默认 127.0.0.1:17890）：
- `/` 简单 HTML 报告列表
- `/api/reports` JSON（汇总 `下载报告.json`）
- `/api/status` 基本状态
只本机可访问、不读取凭据、不写文件。
