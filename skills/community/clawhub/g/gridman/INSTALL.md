# 古立特 Gridman — MCP 工具层安装（BIOS 固件）

> **读者：AI Agent。** 无论你是 Kiro、Cursor、Claude Code、Codex、OpenClaw、Workbuddy 还是其他任何 AI 助手——读到这份文件，就按步骤执行安装。
>
> 用户只需说一句"装古立特"或"安装 MCP"，你就启动这个流程。

---

## POST 自检（第 1 步）

检测当前环境是否已有 `uv`：

```bash
uv --version
```

- ✅ 输出版本号 → 跳到第 2 步
- ❌ 命令不存在 → 安装 uv：

**Windows（PowerShell）：**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS / Linux：**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

安装后若 `uv --version` 仍报错，提示用户重启终端后再继续。

---

## 找启动盘（第 2 步）

**你（AI）自己探测 whl 的绝对路径，不要让用户手填。**

whl 文件在本文件同级的 `payload/` 目录下：

```
payload/gridman_mcp-*.whl
```

你知道自己正在读的这份 INSTALL.md 所在的目录路径，往下拼 `payload/gridman_mcp-1.9.0-py3-none-any.whl` 即可。

如果找不到 payload/ 或里面没有 whl 文件，问用户："whl 安装包放在哪了？告诉我路径。"

---

## 写入引导配置（第 3 步）

根据**当前 AI Agent 平台**，把下面的配置写入对应位置。

### 配置内容

将 `<WHL路径>` 替换为第 2 步的绝对路径（Windows 路径用 `\\` 转义）：

```json
{
  "mcpServers": {
    "gridman": {
      "command": "uvx",
      "args": ["--from", "<WHL路径>", "gridman-mcp"]
    }
  }
}
```

### 各平台配置位置

| 平台 | 配置文件 |
|------|---------|
| **Kiro** | `.kiro/settings/mcp.json`（工作区）或 `~/.kiro/settings/mcp.json`（用户级） |
| **Cursor** | `~/.cursor/mcp.json` 或项目内 `.cursor/mcp.json` |
| **Claude Code** | 执行 `claude mcp add gridman -- uvx --from "<WHL路径>" gridman-mcp`，或编辑 `~/.claude.json` |
| **Codex** | 项目内 `.codex/mcp.json` 或平台约定的 MCP 配置入口 |
| **OpenClaw** | 平台 MCP 设置面板 |
| **Workbuddy** | `.workbuddy/mcp.json` 或平台约定位置 |
| **Cline** | VS Code Cline 的 `cline_mcp_settings.json` |
| **Windsurf** | Cascade 的 MCP 配置文件 |

### 合并规则

- 配置文件已存在且有 `mcpServers` → **只新增 `gridman` 这一项**，不覆盖其他 server
- 文件不存在 → 创建并写入完整结构
- 写之前先读现有内容，确保合法 JSON

---

## 启动验证（第 4 步）

1. 提示用户**重启 Agent**（或在 MCP 面板点 Reconnect）
2. 首次连接 uvx 会自动下载依赖（10–60 秒），正常现象
3. 成功标志：MCP 面板显示 **gridman** 已连接，约 **35 个工具**
4. 快速验证：调用 `materiality_calculator` 或问"帮我算重要性水平"

---

## 可选扩展

### A. 市场数据（A股行情/K线/财务）

需要 `akshare` 依赖。改 args 为：
```json
"args": ["--from", "<WHL路径>[market]", "gridman-mcp"]
```

### B. OCR 文档识别

需要 MinerU API Token。加 env：
```json
"env": { "MINERU_API_TOKEN": "你的Token" }
```
Token 获取：https://mineru.net → 登录 → API → 智能解析 → API 管理 → 创建

### C. uv 缓存迁移（C 盘空间紧张时）

Windows PowerShell：
```powershell
[Environment]::SetEnvironmentVariable("UV_CACHE_DIR", "D:\uv\cache", "User")
[Environment]::SetEnvironmentVariable("UV_TOOL_DIR", "D:\uv\tools", "User")
```

---

## 故障排查

| 现象 | 原因 | 处理 |
|------|------|------|
| Connection Failed / closed | uv 没装好或不在 PATH | 验证 `uv --version`；重启终端 |
| 首次连接超时 | 下载依赖中 | 等待或重试 |
| No such file | whl 路径错 | 用绝对路径；Windows 用 `\\` |
| 工具数不对 | 旧版缓存 | `uvx --refresh --from "<whl>" gridman-mcp` |
| akshare 未安装 | 没加 `[market]` | 按扩展 A 修改 |

---

## 安装来源说明

当前用本地 whl 文件安装。未来 GitHub 上线后可改为远程源，其余步骤完全不变：

```json
"args": ["--from", "git+https://github.com/ZXCharlotte486/Gridman.git", "gridman-mcp"]
```

---

*古立特 Gridman v1.9.0 · 35 个 MCP 工具 · Access Flash.*
