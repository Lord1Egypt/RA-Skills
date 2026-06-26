---
slug: journal-intel-extractor
name: Journal Deep Intel Intelligence Station
version: 1.8.0
description: 专业的学术情报提取工具。支持 Nature/Science/Cell 等全球主流期刊，自动化抓取过去 N 天内新增的 Article 或 Review，并深度提取 PMID 与 Abstract 全文，为 AI 科普总结提供核心数据源。
author: xch
type: python_skill
entry: venv/bin/python3 main.py --journal "$journal" --type "$type" --days $days
arguments:
  - name: journal
    type: string
    description: "目标期刊全名（如 Nature, Science, Cell, NEJM, The Lancet）"
    required: true
  - name: type
    type: string
    description: "文献筛选类型：Article (原始论文) 或 Review (综述)"
    default: "Article"
  - name: days
    type: number
    description: "回溯天数：建议设为 7 天以生成周报"
    default: 7
---

# 🎓 Journal Deep Intel Intelligence Station

这是一个为医学与生命科学科研人员定制的自动化情报工具。它解决了“只看标题不了解实质内容”的痛点，通过模拟深度访问，为每一篇新文献建立完整的摘要档案。

### 🌟 核心功能
* **深度抓取**：不同于常规爬虫，本工具会逐一进入 PubMed 详情页提取 **Abstract (摘要)**。
* **精准过滤**：利用 PubMed 官方 Publication Type 标签，自动剔除新闻、社论和简报，只留硬核干货。
* **时间窗口监控**：基于 `[pdat]` 逻辑，支持按周或按月生成定制化文献简报。
* **AI 友好型输出**：生成结构化的 JSON 数据，完美适配 OpenClaw 内部的 LLM 总结流程。

### 🛠️ 技术实现
1. **引擎**：基于 Python 3.x 配合 BeautifulSoup4 处理 HTML 解析。
2. **频率控制**：内置 0.5s 的抓取延迟（Rate Limiting），保护您的 IP 不被 PubMed 临时封禁。
3. **本地归档**：数据自动保存至 `~/Documents/Journal_Intel/` 目录下，按日期和期刊名分类存储。

### 📖 使用场景示例
* **场景一：Nature 周报**
  参数：`journal="Nature", type="Article", days=7`
* **场景二：顶级综述追踪**
  参数：`journal="Science", type="Review", days=30`

### ⚠️ 运行提示
由于需要进行深度详情页抓取，运行速度约为 **1秒/篇**。若当周更新较多（如超过 50 篇），请耐心等待脚本运行结束。
