# 📈 智能投资简报生成器

基于 Tavily AI 搜索的股票投资分析工具，自动生成专业投资简报。

## ✨ 功能特点

- 🔍 **AI 智能搜索** - 使用 Tavily API 获取实时股票数据
- 📊 **个股深度分析** - 自动生成包含价格、消息、研报的分析报告
- 🎯 **多维度数据** - 整合行情、新闻、机构观点
- 📄 **专业输出** - 生成格式化的 Markdown 投资简报
- ⚡ **一键生成** - 简单命令即可获取完整报告

## 🚀 快速开始

### 前置要求

- Node.js 18+
- Tavily API Key ([获取地址](https://tavily.com))
- OpenClaw 环境

### 安装

```bash
# 通过 ClawHub 安装
clawhub install investment-brief-generator
```

### 配置

设置 Tavily API Key：

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

## 📖 使用指南

### 分析个股

```bash
node scripts/generate-brief.mjs --stock 002837 --name 英维克
```

### 生成市场简报

```bash
node scripts/generate-brief.mjs --market
```

### 保存到文件

```bash
node scripts/generate-brief.mjs --stock 002837 --name 英维克 --output ~/report.md
```

## 📋 输出示例

```markdown
# 📊 英维克(002837) 投资简报

**生成时间**: 2026/3/20 19:58:00

---

## 💰 行情概览

[AI 搜索获取的实时股价数据...]

---

## 📰 最新消息

[相关新闻和公告...]

---

## 📈 机构观点

[券商研报和评级...]

---

## 🤖 AI 分析总结

基于 Tavily AI 搜索的综合分析...
```

## 🛠️ 技术架构

- **搜索引擎**: Tavily AI Search API
- **数据整合**: Node.js + ES Modules
- **输出格式**: Markdown
- **运行环境**: OpenClaw

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交 Issue 和 PR！

## 📝 更新日志

### v1.0.0 (2026-03-20)
- ✨ 初始版本发布
- 🔍 支持个股分析
- 📊 支持市场热点简报
- 📄 Markdown 格式输出
