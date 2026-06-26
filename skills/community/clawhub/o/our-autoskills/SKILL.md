---
name: our-autoskills
description: AutoSkills - 智能AgentSkills自动检测与安装系统。自动检测项目类型（Web/Python/学术/金融等），推荐并安装对应的AgentSkills。触发词：autoskills、项目类型检测、智能安装。
metadata:
  openclaw:
    homepage: https://github.com/adamwgp/our-autoskills
---

# AutoSkills - 智能AgentSkills系统

## 功能

### 1. 项目技术栈自动检测
支持检测以下项目类型：
- 🌐 **Web项目**: React/Vue/Angular/Next.js/Nuxt.js
- 🐍 **Python项目**: Django/Flask/FastAPI/Pandas
- 📚 **学术项目**: LaTeX论文/ArXiv/Thesis
- 💰 **金融项目**: 股票/加密货币/量化交易
- 📈 **营销项目**: CRM/Sales/Pipeline
- 🎬 **媒体项目**: 视频/音频/字幕处理

### 2. 智能Skills匹配
根据检测到的项目类型，自动推荐最合适的AgentSkills：
- Web → agent-reach, playwright-scraper, web-research-assistant
- Python → csv-analyzer, stock-analysis, pymupdf-pdf-parser
- Academic → phd-revision-agent, humanizer-pipeline, verification-gate-phd
- Finance → jarvis-invest, stock-analysis, yahoo-finance-cli, personal-cfo
- Marketing → sains-crm, sales-pipeline-tracker, social-media-manager

### 3. 一键安装
```bash
npx our-autoskills
```

### 4. 与Hunter Agent集成
- Finance项目自动激活Jarvis-Invest
- Marketing项目自动激活Sains CRM

## 命令

```bash
npx our-autoskills        # 完整检测+推荐+集成
npx our-autoskills detect # 仅检测项目类型
npx our-autoskills install # 安装推荐的Skills
npx our-autoskills list   # 查看所有可用Skills
npx our-autoskills doctor # 系统检查
```

## 系统检查

```bash
npx our-autoskills doctor
```

检查项：
- Node.js 版本
- ClawHub CLI 状态
- Skills 目录状态
- 已安装Skills统计

## 安装

```bash
npm install -g our-autoskills
# 或
npx our-autoskills
```

## 技术栈检测算法

检测器使用多维度评分：
1. **文件模式匹配** (权重: 2)
   - package.json → Web项目
   - requirements.txt → Python项目
   - *.tex, *.bib → 学术项目
2. **关键词扫描** (权重: 1)
   - README.md内容分析
   - 代码文件关键词

## Skills注册表

内置27+个预配置Skills：
- System级: token-manager, model-router, structured-context-compressor, clawflow
- Web级: agent-reach, web-research-assistant, playwright-scraper
- Academic级: phd-revision-agent, humanizer-pipeline, verification-gate-phd
- Finance级: jarvis-invest, stock-analysis, yahoo-finance-cli
- Marketing级: sains-crm, sales-pipeline-tracker, closing-deals
