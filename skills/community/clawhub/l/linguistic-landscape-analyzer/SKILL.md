---
name: linguistic-landscape-analyzer
description: 语言景观分析 MCP 工具 - 小红书情感分析与关键词提取，支持语言学/社会学研究
homepage: https://github.com/Crystaria/linguistic-landscape-analyzer
tags: [linguistics, sentiment-analysis, mcp, social-media, research]
metadata:
  {
    "openclaw":
      {
        "emoji": "📊",
        "requires": { "bins": ["node"] },
        "install":
          [
            {
              "id": "npm",
              "kind": "npm",
              "package": "linguistic-landscape-analyzer",
              "path": ".",
              "label": "安装语言景观分析 MCP 工具",
            },
          ],
      },
  }
---

# Linguistic Landscape Analyzer

**Version:** 1.0.1 · 安全优化版  
**Author:** 小爪 🦞  
**License:** MIT  
**Tags:** #linguistics #sentiment-analysis #mcp #social-media #research

---

## 📊 语言景观分析 MCP 工具

专业的语言景观分析工具，为语言学和社会学研究提供数据支持。通过情感分析、关键词提取和自动报告生成，帮助研究者快速分析社交媒体文本数据。

## 🎯 这个技能能帮你做什么？

- **如果你是语言学研究者**：分析社交媒体中的语言使用模式、情感倾向和话题演变，支持定量和定性研究。

- **如果你是社会学研究者**：研究网络社区的话语特征、群体情感变化和舆论趋势，获取一手数据支持。

- **如果你是内容运营者**：监控内容情感反馈，提取用户关注热点，优化内容策略。

- **如果你是数据分析师**：快速处理社交媒体文本数据，生成结构化分析报告，提升工作效率。

## 功能特性

- 📊 **情感分析** - 分析文本的情感倾向（支持中文）
- 🔑 **关键词提取** - 从文本中提取核心关键词
- 📝 **笔记列表** - 读取和管理小红书笔记数据
- 📈 **周报生成** - 自动生成语言景观分析周报（Markdown 格式）

## ⚠️ 注意事项

- **当前版本仅处理本地 CSV 数据，不包含任何网络爬虫功能。** 未来若增加此类功能，会另行发布。
- **报告输出路径：** 报告保存在技能目录内的 `reports/` 文件夹下，确保安全性。
- **数据隐私：** 所有数据处理在本地完成，不会上传到外部服务器。

## 快速开始

### 1. 安装 Skill

```bash
clawhub install linguistic-landscape-analyzer
```

或手动安装：

```bash
cd /path/to/skill
npm install
```

### 2. 启动服务器

```bash
npm start
```

### 3. 在 OpenClaw 中调用

通过 mcporter CLI：

```bash
# 列出工具
mcporter list

# 情感分析
mcporter call linguistic-landscape.analyze_sentiment text:"这个产品很好用" language:"zh"

# 关键词提取
mcporter call linguistic-landscape.extract_keywords text:"小红书运营数据分析" limit:5 language:"zh"

# 笔记列表
mcporter call linguistic-landscape.list_notes source:"sample" limit:10 sortBy:"likes" order:"desc"

# 生成周报
mcporter call linguistic-landscape.generate_weekly_report limit:10
```

## 工具说明

### analyze_sentiment

情感分析工具 - 分析文本的情感倾向。

**参数：**
- `text` (string, 必填) - 要分析的文本内容
- `language` (string, 可选) - 语言类型：zh(中文) 或 en(英文)，默认"zh"

**示例：**
```bash
mcporter call linguistic-landscape.analyze_sentiment text:"小红书运营数据很好，推荐" language:"zh"
# 输出：{"score": 2, "sentiment": "positive", "confidence": 0.33}
```

### extract_keywords

关键词提取工具 - 从文本中提取关键词。

**参数：**
- `text` (string, 必填) - 要提取关键词的文本
- `limit` (number, 可选) - 返回关键词数量上限，默认 10
- `language` (string, 可选) - 语言类型，默认"zh"

**示例：**
```bash
mcporter call linguistic-landscape.extract_keywords text:"小红书运营数据分析，内容优化方向明确" limit:5
# 输出：{"keywords": ["小红书运营数据分析", "内容优化方向明确"]}
```

### list_notes

笔记列表工具 - 读取 CSV 文件中的小红书笔记数据。

**参数：**
- `source` (string, 可选) - 数据源类型：csv 或 sample，默认"sample"
- `limit` (number, 可选) - 返回笔记数量上限，默认 10
- `sortBy` (string, 可选) - 排序字段：likes/collects/comments/date，默认"date"
- `order` (string, 可选) - 排序顺序：asc/desc，默认"desc"

**示例：**
```bash
mcporter call linguistic-landscape.list_notes source:"sample" limit:5 sortBy:"likes" order:"desc"
```

### generate_weekly_report

周报生成工具 - 生成语言景观分析周报（Markdown 格式）。

**参数：**
- `startDate` (string, 可选) - 开始日期 (YYYY-MM-DD)
- `endDate` (string, 可选) - 结束日期 (YYYY-MM-DD)
- `outputPath` (string, 可选) - 输出文件路径
- `limit` (number, 可选) - 分析笔记数量上限，默认 10

**示例：**
```bash
mcporter call linguistic-landscape.generate_weekly_report limit:10
# 输出：{"status": "success", "reportPath": "/path/to/report.md"}
```

## 应用场景

### 语言学研究
- 分析网络语言使用模式
- 研究语言变异和变化
- 追踪新词新语的产生和传播

### 社会学研究
- 研究群体情感变化
- 分析舆论趋势
- 探索社会话题演变

### 内容运营
- 监控用户情感反馈
- 提取热点话题
- 优化内容策略

### 数据分析
- 批量处理文本数据
- 生成结构化报告
- 支持决策制定

## 技术栈

- Node.js 22+
- @modelcontextprotocol/sdk (官方 MCP SDK)
- sentiment (情感分析库)
- keyword-extractor (关键词提取)
- zod (参数验证)

## 常见问题

### Q: 这个技能适合哪些研究场景？
A: 适用于语言学、社会学、传播学等领域的社交媒体文本分析研究，支持情感分析、关键词提取和报告生成。

### Q: 情感分析的准确性如何？
A: 当前版本使用基于词典的简单情感分析方法，适合快速原型和初步分析。如需更高精度，可接入专业 NLP API（如阿里云 NLP）。

### Q: 如何替换为自己的数据？
A: 将 CSV 文件放到 `data/` 目录下，格式参考 `sample.csv`，然后在调用 `list_notes` 时指定 `source:"csv"`。

### Q: 支持哪些语言？
A: 当前主要支持中文和英文。中文使用简单分词 + 情感词典，英文使用 sentiment 库。

## 更新日志

### v1.0.1 (2026-03-17)
- 🔒 **安全修复** - 报告输出路径改为技能目录内
- 📝 **文档优化** - 添加注意事项说明
- 🔗 **链接修复** - 移除未创建的 GitHub 仓库链接
- ✨ **标签优化** - 明确指定技能标签

### v1.0.0 (2026-03-17)
- ✅ 初始版本发布
- ✅ analyze_sentiment 工具
- ✅ extract_keywords 工具
- ✅ list_notes 工具
- ✅ generate_weekly_report 工具
- ✅ 完整测试套件

## 许可证

MIT License

---

**作者：** 小爪 🦞  
**GitHub:** （仓库筹备中，敬请期待）  
**ClawHub:** linguistic-landscape-analyzer
