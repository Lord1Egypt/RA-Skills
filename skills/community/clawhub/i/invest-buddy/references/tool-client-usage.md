# tool Client 使用指南

本指南说明如何在 OpenClaw Agent 中使用 tool Investment Research Tools 的 HTTP API 客户端。

## 快速开始

### 1. 环境配置

确保 tool 服务正在运行，并设置 API Token：

```bash
# 方法 1: 设置环境变量
export TOOL_API_TOKEN=your_token_here
```

### 2. 可用工具

| 工具名 | 用途 | 参数 |
|--------|------|------|
| `extract_assets` | 从文本提取资产 | `--text` |
| `investment_search_pro` | 检索专业投资信息 | `--query` |
| `get_asset_overview` | 获取资产快速概览 | `--symbol` (必带后缀) |
| `analyze_fundamentals_financial` | 分析基本面-财务 | `--symbol` (必带后缀) |
| `analyze_fundamentals_valuation` | 分析基本面-估值 | `--symbol` (必带后缀) |
| `analyze_technical` | 分析技术面 | `--symbol` (必带后缀) |
| `analyze_capital_flow` | 分析资金面 | `--symbol` (必带后缀) |
| `analyze_market_sentiment` | 分析市场观点 | `--symbol` (必带后缀) |

**重要说明**：
- **symbol 必须带市场后缀**：
  - A股深交所（0/3开头）：`300750.SZ`
  - A股上交所（6开头）：`600519.SH`
  - 港股：`00700.HK`
- 调用 `extract_assets` 会返回带后缀的 symbol，可以直接使用

### 3. 基础调用示例

```bash
# 提取资产（返回带后缀的 symbol）
python scripts/tool_client.py --tool extract_assets --text "分析下茅台"

# 获取资产概览
python scripts/tool_client.py --tool get_asset_overview --symbol 600519.SH

# 分析技术面
python scripts/tool_client.py --tool analyze_technical --symbol 600519.SH

# 分析宁德时代
python scripts/tool_client.py --tool analyze_technical --symbol 300750.SZ
```

## 在 Agent 工作流中使用

### 示例 1: 资产提取

当用户输入"分析下茅台"时：

```bash
# Agent 执行
cd /Users/edy/.openclaw/workspace/skills/investment-research
python scripts/tool_client.py --tool extract_assets --text "分析下茅台"
```

**输出示例**：
```json
{
  "success": true,
  "assets": [
    {
      "name": "贵州茅台",
      "symbol": "600519.SH",
      "market": "A股",
      "confidence": 0.98
    }
  ],
  "ambiguous": [],
  "suggestions": []
}
```

### 示例 2: 单维度分析

```bash
# 用户: "看看茅台的技术面"
python scripts/tool_client.py --tool analyze_technical --symbol 600519.SH
```

**输出**：Markdown 格式的技术面分析

### 示例 3: 深度分析（5 维度并行）

使用 bash 并行调用多个工具：

```bash
cd /Users/edy/.openclaw/workspace/skills/investment-research

# 并行调用 5 个分析工具
tools=(
  "analyze_fundamentals_financial"
  "analyze_fundamentals_valuation"
  "analyze_technical"
  "analyze_capital_flow"
  "analyze_market_sentiment"
)

for tool in "${tools[@]}"; do
  python scripts/tool_client.py --tool "$tool" --symbol 600519.SH &
done

wait
```

## 输出格式

tool 工具返回的格式为：

```json
{
  "success": true,
  "result": "Markdown 格式的分析内容",
  "metadata": {
    "tool": "analyze_technical",
    "symbol": "600519.SH",
    "timestamp": "2024-03-15T12:00:00Z"
  }
}
```

其中 `result` 字段包含 Markdown 格式的分析内容，可以直接在报告中使用。

## 错误处理

### 常见错误

| 错误 | 原因 | 解决方法 |
|------|------|----------|
| `tool_API_TOKEN is required` | 未设置 API Token | 设置环境变量或在 .env 文件中配置 |
| `HTTP 401 Unauthorized` | Token 无效 | 检查 Token 是否正确 |
| `HTTP 404 Not Found` | API URL 错误 | 检查 tool 服务是否运行 |
| `Request timeout` | 服务响应超时 | 增加 `--timeout` 参数或检查服务状态 |
| `HTTP 500 Internal Server Error` | 服务端错误 | 检查 tool 服务日志 |

### 在 Agent 中的错误处理

Agent 在调用脚本后应检查返回值：

```bash
result=$(python scripts/tool_client.py --tool extract_assets --text "分析下茅台" 2>&1)

if echo "$result" | grep -q "Error:"; then
  # 处理错误
  echo "无法连接到 tool 服务: $result"
else
  # 处理正常结果
  echo "$result"
fi
```

## 高级用法

### 输出原始内容（非 JSON）

```bash
python scripts/tool_client.py --tool analyze_technical --symbol 600519 --output raw
```

### 自定义超时时间

```bash
python scripts/tool_client.py --tool get_asset_overview --symbol 600519 --timeout 120
```

服务默认运行在 `http://api.facaidazi.com/api/tools/call`。

## 参考资源

- **Tool 规范**: `references/tool-specs.md`
- **原客户端代码**: `../scripts/tool_client.py`
