# minimax-mcp 🦞

> 封装 MiniMax Token Plan 内置 web_search, image_understanding 工具，免费、零配置、无 C 盘占用。

---

## 这个 Skill 解决什么问题？

MiniMax Token Plan 订阅自带 web_search 工具，但原生的 `uvx minimax-coding-plan-mcp` 在 Windows 上有 asyncio DLL 问题跑不起来。这个 skill 绕过去，让你直接在 OpenClaw 里用上 MiniMax 搜索。

**特点：**
- 完全免费（用你自己的订阅额度）
- 不占 C 盘（venv + 缓存全在 E 盘）
- 凭证不写死在文件里（通过环境变量注入）
- 订阅失效自动降级 Brave Search / Qwen Chat

---

## 安装前提

### 1. Python 环境（若没有）

```powershell
# 创建 venv（不占 C 盘）
python -m venv E:\.uv-venv

# 安装 MCP 包
E:\.uv-venv\Scripts\pip.exe install minimax-coding-plan-mcp
```

### 2. 配置 API Key

在 `openclaw.json` 的 `env` 块添加：

```json
{
  "env": {
    "MINIMAX_API_KEY": "你的 MiniMax API Key"
  }
}
```

重启 Gateway 使配置生效。

---

## 状态配置

```json
{ "enabled": true }
```

| 值 | 含义 |
|---|---|
| `true` | 使用 MiniMax 搜索 |
| `false` | 降级到 Brave Search / Qwen Chat |

**订阅失效特征：** 报错 `401` / `403` / `authentication failed`
→ 改为 `enabled: false` 激活 Fallback，恢复订阅后改回 `true`

---

## 使用方法

### 网络搜索

```bash
node skills/minimax-mcp/scripts/minimax_mcp.js search "搜索关键词"
```

**输出格式：**

```json
{
  "query": "中国LLM算法薪资 2026",
  "count": 10,
  "results": [
    {
      "title": "...",
      "link": "https://...",
      "snippet": "...",
      "date": "2026-03-24"
    }
  ],
  "related": [{ "query": "相关搜索词" }]
}
```

### 图片理解

```bash
node skills/minimax-mcp/scripts/minimax_mcp.js image "分析要求" "图片路径或URL"
```

**示例：**

```bash
# 本地文件
node skills/minimax-mcp/scripts/minimax_mcp.js image "描述截图内容" "Your_local_image.jpg"

# 网络图片
node skills/minimax-mcp/scripts/minimax_mcp.js image "这张图里有什么？" "https://example.com/image.jpg"
```

**支持格式：** JPEG、PNG、WebP（最大 20MB）
**返回：** 图片内容的文字描述

---

## Fallback 降级链

当 MiniMax 订阅失效时，改为 `enabled: false`，自动切换：

1. **Brave Search** — OpenClaw 内置 `web_search` 工具
2. **Qwen Chat** — Chrome Relay 打开 chat.qwen.ai 搜索

---

## 目录结构

```
skills/minimax-mcp/
├── SKILL.md
├── SKILL_en.md
├── config.json          ← 无 Key，仅存 HOST 默认值
└── scripts/
    └── minimax_websearch.js
```

---

## 技术细节

| 项目 | 说明 |
|------|------|
| Python 环境 | `E:\.uv-venv`（Python 3.11，完全在 E 盘） |
| 包缓存 | `E:\.uv-cache`（不占 C 盘） |
| MCP 包 | `minimax-coding-plan-mcp==0.0.4` |
| 凭证 | 从 `MINIMAX_API_KEY` 环境变量读取，不写文件 ✅ |
| Python 路径 | 从 `MINIMAX_PYTHON` 环境变量读取（默认 `E:\.uv-venv\Scripts\python.exe`） |
| 通信方式 | stdio JSON-RPC，不占用 OpenClaw 进程端口 |
| 工具 | `web_search`（搜索）+ `understand_image`（图片理解） |

---

## 已知问题

### `uvx` 在 Windows 上有 asyncio DLL 问题 🔴

`uvx minimax-coding-plan-mcp` 会报错 `_overlapped import failed`。解决方案是用 `E:\.uv-venv\Scripts\python.exe -m minimax_mcp.server`，不要用 uvx。

### `.uv-venv` SSL 证书问题

某些 Windows 环境下 `.uv-venv` 的 SSL 证书配置可能为空。脚本会自动设置 `REQUESTS_CA_BUNDLE` 环境变量指向 certifi CA 包，无需手动处理。

---

## 更新日志

- **2026-03-24** v2.1：新增 `understand_image` 图片理解工具，支持本地文件和 URL
- **2026-03-24** v2：修复审查问题（凭证移至环境变量、移除硬编码路径、修复 SSL 证书问题）

*🦞 Created by godiao — MIT License*
