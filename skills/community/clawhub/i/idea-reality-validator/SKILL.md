---
name: idea-reality-validator
version: 1.0.0
description: Pre-build idea validator that checks competition across GitHub, Hacker News, npm, PyPI, and Product Hunt before writing code.
author: sunnyhot
license: MIT
keywords:
  - idea-validation
  - competition-analysis
  - market-research
  - mcp
---

# Idea Reality Validator - 开发前创意验证器

**在写代码之前，自动检查你的创意是否已经存在**

---

## ✨ 核心功能

### 🔍 **多数据源扫描**
- ✅ GitHub - 检查开源项目
- ✅ Hacker News - 技术社区热度
- ✅ npm - Node.js 包
- ✅ PyPI - Python 包
- ✅ Product Hunt - 新产品

### 📊 **竞争度评分**
- ✅ reality_signal (0-100分)
- ✅ 头部竞品展示
- ✅ Star 数统计
- ✅ 项目描述

### 💡 **差异化建议**
- ✅ 自动建议差异化方向
- ✅ 细分市场机会
- ✅ 蓝海领域识别

### 🇨🇳 **中国市场验证**
- ✅ 百度指数
- ✅ 微信指数
- ✅ V2EX
- ✅ 少数派
- ✅ 36氪

---

## 🚀 使用方法

### **1. 安装 MCP 服务器**

```bash
uvx idea-reality-mcp
```

---

### **2. 配置 OpenClaw**

在 `~/.openclaw/openclaw.json` 中添加：

```json
{
  "mcpServers": {
    "idea-reality": {
      "command": "uvx",
      "args": ["idea-reality-mcp"]
    }
  }
}
```

---

### **3. 使用示例**

**你**: "帮我做一个 AI 代码审查的 CLI 工具"

**OpenClaw** 会运行 `idea_check("AI code review tool")` 并回复：

```
reality_signal: 90/100（非常高）

头部竞品：
1. Gitea — 53,940 stars
2. reviewdog — 9,104 stars
3. Danger (Ruby) — 5,649 stars

该领域有 143,000+ 个相关仓库。

差异化建议：
- 聚焦特定语言（Rust/Go 专用）
- 针对特定框架（React/Vue 组件）
- 针对特定行业（金融/医疗合规）
```

---

## 📋 规则

### **reality_signal 评分规则**

| 分数 | 行动 |
|------|------|
| **> 70** | ⚠️ STOP - 报告头部竞品，询问是否继续、转型或放弃 |
| **30-70** | 💡 显示结果和差异化建议，推荐细分市场角度 |
| **< 30** | ✅ PROCEED - 提及领域开放，直接开发 |

---

## 🔧 配置文件

### `config/settings.json`

```json
{
  "mcp": {
    "server": "idea-reality",
    "command": "uvx",
    "args": ["idea-reality-mcp"]
  },
  "rules": {
    "stopThreshold": 70,
    "pivotThreshold": 30,
    "showTopCompetitors": 3
  },
  "chinaMarket": {
    "enabled": true,
    "sources": ["baidu-index", "wechat-index", "v2ex", "sspai", "36kr"]
  }
}
```

---

## 🌍 中国市场验证

### **补充数据源**

| 国际数据源 | 国内对应平台 |
|-----------|-------------|
| Product Hunt | V2EX, 少数派 |
| Hacker News | V2EX, 掘金, CSDN |
| GitHub | Gitee |
| npm / PyPI | Gitee 镜像 |

### **市场验证工具**

- **百度指数** - 搜索趋势
- **微信指数** - 微信生态热度
- **巨量算数** - 抖音/头条数据
- **阿里指数** - 电商需求
- **36氪、IT桔子** - 融资项目

---

## 📝 更新日志

### v1.0.0 (2026-03-14)
- ✅ 初始版本
- ✅ 5大数据源扫描
- ✅ 竞争度评分
- ✅ 差异化建议
- ✅ 中国市场验证

---

**🚀 避免重复造轮子，找到真正的蓝海机会！**
