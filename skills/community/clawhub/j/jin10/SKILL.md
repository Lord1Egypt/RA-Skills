---
name: jin10
description: |
  金十数据财经信息查询 skill。查询黄金/白银/原油等行情报价、K线、最新财经快讯、资讯新闻、财经日历数据时使用。
  触发场景：问"黄金价格"、"XAUUSD报价"、"黄金1小时K线"、"原油快讯"、"财经日历"、"非农什么时候"、"资讯详情"等。
  本 skill 包含 Python 代码（jin10/ 模块 + scripts/jin10.py），非纯指令型 skill。
metadata:
  openclaw:
    skillKey: jin10
    primaryEnv: JIN10_API_TOKEN
    envVars:
      - name: JIN10_API_TOKEN
        description: 金十数据 API Token，必需。获取方式见 https://mcp.jin10.com/app
        required: true
    configPaths:
      - ~/.openclaw/.env  # 可选，token 也可直接通过环境变量传入
---

# Jin10 金十数据 Skill

> 致谢：感谢金十数据提供 MCP 服务。本 skill 仅进行使用方式转换，无意替代或模仿金十数据官方服务。

本 skill 内部沿用金十官方 MCP 端点 `https://mcp.jin10.com/mcp`，但对 OpenClaw 暴露的是随 skill 一起分发的本地脚本接口。

运行前提：
- 宿主机需要可用的 `python3`
- 必须提供环境变量 `JIN10_API_TOKEN`

不要在对话中手写 `initialize`、`tools/call`、`resources/read`、`Mcp-Session-Id` 等 MCP 细节。统一通过本地 CLI 调用：

```bash
python3 scripts/jin10.py ...
```

CLI 会自动完成：
- Bearer Token 鉴权
- `initialize -> notifications/initialized -> tools/list/resources/list`
- `tools/call` / `resources/read`
- 优先读取 `structuredContent`
- 协议错误与业务错误处理

## 配置

**方式一：写入配置文件（推荐）**

OpenClaw 运行时加载 `~/.openclaw/.env` 并将变量注入环境：

```bash
echo 'JIN10_API_TOKEN="sk-xxxxxxx"' >> ~/.openclaw/.env
```

**方式二：直接设置环境变量**

```bash
export JIN10_API_TOKEN="sk-xxxxxxx"
```

> 注意：Python 代码只读取环境变量（`os.environ`），不直接解析 `.env` 文件。确保 OpenClaw 运行时已加载配置。

如果未配置 token，命令会直接失败并返回明确错误。

## 规则

1. 默认使用 `python3 scripts/jin10.py --format json ...`，优先读取 JSON 输出。
2. 只有在需要给用户展示更自然的可读文本时，才使用 `--format text`。
3. 用户问“某个品种报价或 K 线”时，如果代码不明确，先执行 `python3 scripts/jin10.py --format json codes` 查代码，再执行 `quote` 或 `kline`。
4. 用户问“某个主题的最新快讯”时，优先用 `flash search <关键词>`；若要顺序浏览，再用 `flash list` 和 `--cursor` 翻页。
5. 用户问“某个主题的深度文章”时，先用 `news search` 或 `news list` 找 `id`，再用 `news get <id>` 取详情。
6. 用户问“财经日历 / 本周数据”时，直接用 `calendar`。
7. 详细命令和字段约定见 [references/api-contract.md](references/api-contract.md)。

## 命令接口

### 报价与代码

```bash
python3 scripts/jin10.py --format json codes
python3 scripts/jin10.py --format json quote XAUUSD
python3 scripts/jin10.py --format text quote XAUUSD
python3 scripts/jin10.py --format json kline XAUUSD --time 1h --count 20
python3 scripts/jin10.py --format text kline XAUUSD --time 1d --count 5
```

### 快讯

```bash
python3 scripts/jin10.py --format json flash list
python3 scripts/jin10.py --format json flash list --cursor "<next_cursor>"
python3 scripts/jin10.py --format json flash search "美联储"
```

### 资讯

```bash
python3 scripts/jin10.py --format json news list
python3 scripts/jin10.py --format json news list --cursor "<next_cursor>"
python3 scripts/jin10.py --format json news search "原油"
python3 scripts/jin10.py --format json news search "非农" --cursor "<next_cursor>"
python3 scripts/jin10.py --format json news get 123456
```

### 财经日历

```bash
python3 scripts/jin10.py --format json calendar
python3 scripts/jin10.py --format json calendar --keyword "非农"
python3 scripts/jin10.py --format json calendar --high-importance
python3 scripts/jin10.py --format text calendar --high-importance
```

## 数据来源

内部使用金十 MCP 端点：`https://mcp.jin10.com/mcp`
