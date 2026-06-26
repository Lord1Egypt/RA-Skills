# Pandas 数据处理技能

[English](README.md) | 简体中文

一个全面的基于pandas的数据操作、清洗、分析和转换技能包。

## 功能特性

- **数据清洗**: 处理缺失值、重复值、异常值和数据标准化
- **数据分析**: 生成详细的统计报告和数据质量评估
- **数据转换**: 格式转换、文件合并、过滤、排序和重塑数据
- **参考文档**: 全面的pandas操作指南和最佳实践

## 安装

```bash
pip install -r requirements.txt
```

## 快速开始

### 分析数据
```bash
python scripts/data_analyzer.py your_data.csv -o report.json
```

### 清洗数据
```bash
python scripts/data_cleaner.py raw_data.csv clean_data.csv \
    --remove-duplicates \
    --handle-missing mean \
    --standardize-columns
```

### 转换数据
```bash
# 格式转换
python scripts/data_transformer.py convert data.csv data.xlsx

# 过滤数据
python scripts/data_transformer.py filter data.csv \
    --query "age > 18" \
    --output filtered.csv

# 合并文件
python scripts/data_transformer.py merge file1.csv file2.csv \
    --output merged.csv
```

## 目录结构

```
pandas-skill/
├── SKILL.md                      # 主技能文档
├── SKILL_CN.md                   # 主技能文档(中文)
├── README.md                     # 英文说明
├── README_CN.md                  # 本文件
├── EXAMPLES.md                   # 英文示例
├── EXAMPLES_CN.md                # 中文示例
├── requirements.txt              # Python依赖
├── scripts/
│   ├── data_cleaner.py          # 数据清洗工具
│   ├── data_analyzer.py         # 数据分析工具
│   └── data_transformer.py      # 数据转换工具
└── references/
    ├── common_operations.md     # Pandas操作参考
    └── data_cleaning_best_practices.md  # 最佳实践指南
```

## 文档

- **SKILL.md / SKILL_CN.md**: 完整的技能文档，包含所有功能和工作流程
- **references/common_operations.md**: pandas操作快速参考
- **references/data_cleaning_best_practices.md**: 数据清洗策略和模式

## 使用场景

- ✅ 分析前清洗混乱的数据集
- ✅ 生成数据质量报告
- ✅ 在数据格式间转换 (CSV、Excel、JSON、Parquet)
- ✅ 合并多个数据源
- ✅ 过滤和聚合数据
- ✅ 检测和处理异常值
- ✅ 为机器学习标准化数据

## 系统要求

- Python 3.8+
- pandas 2.0+
- numpy 1.24+

## 许可证

MIT License
