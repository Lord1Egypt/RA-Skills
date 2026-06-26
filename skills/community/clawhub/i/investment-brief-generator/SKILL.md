---
name: investment-brief-generator
description: 股票分析 AI 工具 | 智能投资简报生成器 - 自动生成个股分析报告、市场热点追踪、持仓监控。支持 A股/港股/美股，实时股价查询，技术分析，研报生成。一键生成专业 Markdown 投资报告。
homepage: https://github.com/openclaw/investment-brief-generator
metadata:
  openclaw:
    emoji: 📈
    requires:
      bins: ["node"]
      env: ["TAVILY_API_KEY"]
    primaryEnv: "TAVILY_API_KEY"
    tags: ["股票", "投资", "分析", "A股", "港股", "美股", "财报", "研报", "Tavily"]
---

# 智能投资简报生成器

基于 Tavily AI 搜索的股票投资分析工具，自动生成专业投资简报。

## 功能特点

- 🔍 **AI 智能搜索** - 使用 Tavily API 获取实时股票数据和市场信息
- 📊 **个股深度分析** - 自动生成包含价格、估值、技术形态的分析报告
- 🎯 **持仓股监控** - 支持多只股票同时监控，自定义提醒价位
- 📄 **专业简报输出** - 生成格式化的 Markdown 投资简报
- ⚡ **一键生成** - 简单命令即可获取完整分析报告

## 使用方法

### 生成个股分析报告

```bash
node {baseDir}/scripts/generate-brief.mjs --stock 002837 --name 英维克
```

### 生成市场热点简报

```bash
node {baseDir}/scripts/generate-brief.mjs --market
```

### 监控持仓股

```bash
node {baseDir}/scripts/generate-brief.mjs --portfolio
```

## 配置

需要设置 Tavily API Key：

```bash
export TAVILY_API_KEY=your_api_key_here
```

或在 OpenClaw 配置中添加：

```json
{
  "env": {
    "vars": {
      "TAVILY_API_KEY": "your_api_key_here"
    }
  }
}
```

## 输出示例

简报包含以下内容：
- 股票基本信息（价格、涨跌幅、成交量）
- 技术面分析（支撑/阻力位）
- 基本面亮点
- 市场情绪
- 操作建议

## 依赖

- Node.js 18+
- Tavily API Key
- OpenClaw 环境

## License

MIT
