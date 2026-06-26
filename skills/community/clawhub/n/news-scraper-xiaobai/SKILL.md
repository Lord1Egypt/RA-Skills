---
name: news-scraper
description: [user] 从AI新闻网站爬取最新资讯。用于AI新闻采集、内容聚合、舆情监控。
---

# 新闻爬取 Skill

## 快速开始

```bash
python scripts/crawl.py --site aibase --limit 20
```

## 编程调用

```python
import sys
sys.path.insert(0, "news-scraper")
from scripts.crawl import crawl_and_return_json

result = crawl_and_return_json(site="aibase", limit=20)
# AI自行处理返回数据
# 原文链接使用中文路径: https://www.aibase.com/zh/news/xxxxx
```

## 分类与标签

每条新闻需要添加分类和标签，便于后续筛选和整理。

### 分类

| 分类 | 说明 |
|------|------|
| 大模型 | 基础模型、LLM、多模态等 |
| AI应用 | 产品、工具、平台 |
| 企业商业 | 公司动态、财报，合作 |
| 安全合规 | 安全漏洞、政策法规 |
| 开源社区 | 开源项目，社区动态 |
| 硬件芯片 | GPU、AI芯片、硬件 |
| 学术研究 | 论文、突破 |
| 智能体 | Agent技术 |

### 标签

| 标签 | 说明 |
|------|------|
| OpenAI | OpenAI相关 |
| Google | 谷歌相关 |
| NVIDIA | 英伟达相关 |
| Meta | Meta相关 |
| Microsoft | 微软相关 |
| 阿里巴巴 | 阿里相关 |
| 中国 | 国内动态 |
| 国际 | 国外动态 |
| Agent | 智能体 |
| 多模态 | 多模态技术 |
| 安全 | 安全相关 |

### 使用方式

在总结输出中添加分类和标签。

## 总结输出格式

AI在总结新闻时，使用以下markdown格式：

```markdown
📅 2026-03-17 AI资讯

---

🧠 **智能体**

> 📌 标题：英伟达发布 NemoClaw
> 🏷️ 分类：智能体 | 标签：NVIDIA、Agent
> 📝 概要：英伟达发布企业级AI智能体平台NemoClaw，为OpenClaw提供企业级安全盔甲
> 🔗 链接：https://www.aibase.com/zh/news/26291

> 📌 标题：钉钉发布"悟空"AI原生平台
> 🏷️ 分类：智能体 | 标签：阿里巴巴、Agent
> 📝 概要：阿里B端AI Agent战略落地，支持PC与移动端双端运行
> 🔗 链接：https://www.aibase.com/zh/news/26285

---

🔒 **安全合规**

> 📌 标题：国安部发布OpenClaw安全养殖手册
> 🏷️ 分类：安全合规 | 标签：中国、安全、Agent
> 📝 概要：提醒用户警惕主机接管、数据窃取、言论篡改四大安全风险
> 🔗 链接：https://www.aibase.com/zh/news/26298
```
