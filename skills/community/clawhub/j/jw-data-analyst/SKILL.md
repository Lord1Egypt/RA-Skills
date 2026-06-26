---
name: JW Data Analyst
description: 数据分析助手 - 自动生成Python数据处理脚本、可视化图表、统计报告。支持Excel/CSV/JSON/数据库。觸發詞：数据分析、图表、统计、报表、可视化。
version: 1.0.0
author: 贾维斯
slug: jw-data-analyst
---

# JW Data Analyst

数据分析智能助手，自动处理数据并生成洞察。

## 功能

### 1. 数据加载
- Excel (.xlsx/.xls)
- CSV/TSV
- JSON
- SQLite/MySQL/PostgreSQL
- API数据源

### 2. 数据清洗
- 缺失值处理（填充/删除/插值）
- 重复值检测与去除
- 异常值检测（IQR/Z-score）
- 数据类型转换
- 格式标准化

### 3. 统计分析
- 描述性统计（均值/中位数/标准差）
- 相关性分析
- 趋势分析
- 分组聚合
- 时间序列分析

### 4. 可视化
- 折线图（趋势）
- 柱状图（对比）
- 饼图（占比）
- 散点图（相关性）
- 热力图（矩阵）
- 箱线图（分布）

## 使用方式

### 分析Excel文件
```
帮我分析这个Excel文件：[路径]
```

### 生成图表
```
用这个数据生成一个柱状图：[数据]
```

### 统计报告
```
生成数据的统计报告：[数据]
```

## 输出格式

- 分析报告：Markdown格式
- 图表：PNG/SVG
- 处理后的数据：Excel/CSV
- Python脚本：可复用的.py文件

## 技术栈

- Python 3.10+
- pandas（数据处理）
- matplotlib/seaborn（可视化）
- numpy（数值计算）
- openpyxl（Excel读写）
- sqlalchemy（数据库连接）

## 注意事项

- 大文件（>100MB）需要分批处理
- 敏感数据需脱敏后分析
- 生成的图表默认保存到D盘
