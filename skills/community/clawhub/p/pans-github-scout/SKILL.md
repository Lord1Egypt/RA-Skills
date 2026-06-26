---
name: pans-github-scout
description: |
  扫描 GitHub 寻找潜在 AI 公司客户。支持按 AI/ML repos、大模型项目、训练代码
  等维度搜索，筛选 star 数、活跃度、公司规模，输出 CSV 或 JSON 格式线索列表。
  触发词：GitHub扫描, AI公司线索, 客户发现, github scout, AI startup discovery,
  算力需求信号
---

# pans-github-scout

扫描 GitHub 寻找潜在 AI 公司客户。

## 功能

- 搜索维度：AI/ML repos、大模型项目、训练代码
- 筛选：star数、活跃度、公司规模
- CLI：--search, --filter, --export

## 使用

```bash
# 搜索 AI/ML 仓库
python3 scripts/scout.py --search "machine learning" --min-stars 100

# 筛选活跃项目
python3 scripts/scout.py --filter --min-stars 500 --updated-within 30

# 导出结果
python3 scripts/scout.py --export leads.csv
```

## 依赖

- Python 3.8+
- requests
