---
name: pans-lead-miner
description: |
  AI算力销售线索挖掘器。输入行业关键词，自动搜索筛选潜在客户，识别算力需求信号。
  通过SearXNG聚合多数据源（Crunchbase/GitHub/LinkedIn/新闻），按融资和算力需求排序。
  触发词：线索挖掘, 客户发现, AI公司搜索, 融资动态, 算力需求, lead generation, prospect
---

# pans-lead-miner

AI算力销售线索挖掘器

## 功能
输入行业关键词，自动搜索并筛选潜在客户列表，识别算力需求信号。

## 数据源
- **Crunchbase RSS**：公开融资新闻
- **GitHub Trending**：AI 项目检测
- **LinkedIn 公开搜索**：通过 SearXNG 聚合
- **新闻聚合**：通过 SearXNG 搜索融资动态

## 搜索逻辑
1. 输入关键词（如 "AI infrastructure", "LLM startup"）
2. 通过本地 SearXNG 实例搜索（http://127.0.0.1:8888/search?format=json）
3. 解析结果，提取公司名、人名、融资信息
4. 按算力需求信号排序（融资轮次、模型训练关键词、招聘GPU工程师等）

## CLI 参数
- `--keyword`：搜索关键词（必填）
- `--source`：数据源（crunchbase/github/linkedin/news/all）
- `--limit`：结果数量（默认 20）
- `--region`：地区（us/cn/eu/global）
- `--stage`：融资阶段（seed/series-a/series-b/later/all）
- `--json`：JSON 输出
- `--export`：导出 CSV 文件路径

## 输出格式
| 公司 | 融资轮次 | 金额 | 关键人 | 算力信号 | 来源 |

## 示例
```bash
python3.11 ~/.qclaw/skills/pans-lead-miner/scripts/mine.py --keyword "AI infrastructure" --limit 5
python3.11 ~/.qclaw/skills/pans-lead-miner/scripts/mine.py --keyword "LLM startup" --source github --limit 10
python3.11 ~/.qclaw/skills/pans-lead-miner/scripts/mine.py --keyword "AI" --stage series-a --export leads.csv
```

## 依赖
- Python 3.11+
- SearXNG 本地实例（http://127.0.0.1:8888）
- requests
- beautifulsoup4
