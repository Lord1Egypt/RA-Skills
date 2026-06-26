---
name: data-analysis-operation
description: 全面的数据分析和操作工具集，支持 Excel/CSV 文件的数据分析、列对比、数据清洗和报告生成。
---

# 数据分析和操作技能

## 概述

data-analysis-operation 技能提供了一个全面的数据分析和操作工具箱，专门用于处理和分析各种数据文件（Excel、CSV、TSV等）。它集成了数据分析、数据清洗、列对比和报告生成等功能，适用于数据质量评估、业务分析、数据清洗和洞察发现等场景。

## 触发关键词

当用户提到以下关键词时，此技能会自动触发：
- "数据分析"、"数据清洗"、"数据质量检查"
- "分析 CSV 文件"、"分析 Excel 数据"、"生成数据报告"
- "对比两列数据"、"找出数据差异"、"清理重复数据"
- "处理缺失值"、"异常值检测"、"数据统计"
- "查看数据摘要"、"数据分布分析"、"数据洞察"

## 核心功能

### 1. 全面数据分析
- **数据质量评估**: 检查缺失值、重复数据、数据类型
- **统计摘要**: 计算均值、中位数、标准差、最小值、最大值
- **数据分布分析**: 分析数值分布、频率分布、类别分布
- **异常值检测**: 使用 IQR 方法自动检测异常值

### 2. 智能列对比
- **列对比**: 对比任意两列数据，找出差异、共同值和唯一值
- **多种引用方式**: 支持列名、列字母、列索引引用
- **详细差异报告**: 生成包含详细对比结果的报告

### 3. 自动数据清洗
- **缺失值处理**: 自动填充或删除缺失值
- **重复数据清理**: 识别并清理重复行
- **数据格式标准化**: 统一日期格式、数值格式
- **编码问题修复**: 自动检测和修复文件编码问题

### 4. 详细报告生成
- **Excel 报告**: 生成包含多个工作表的详细分析报告
- **文本摘要**: 生成关键发现和洞察的文本摘要
- **可视化图表**: 生成数据分布图表（直方图、箱线图等）

## 使用方式

### 通过主脚本使用
```bash
# 数据分析模式
python scripts/data_analysis_operations.py analyze <文件路径> [选项]

# 列对比模式
python scripts/data_analysis_operations.py compare <文件路径> <列1> <列2>

# 数据清洗模式
python scripts/data_analysis_operations.py clean <文件路径> [选项]

# 查看帮助
python scripts/data_analysis_operations.py --help
```

### 独立脚本使用
```bash
# 详细数据分析
python scripts/analyze_data.py <文件路径> [--focus <重点关注列>]

# 列对比分析
python scripts/compare_columns.py <文件路径> <列1> <列2>
```

### 常用选项
- `--sheet <工作表名>`: 指定 Excel 工作表
- `--encoding <编码>`: 指定文件编码（默认自动检测）
- `--output <输出目录>`: 指定输出目录
- `--focus <列名>`: 重点关注特定列
- `--format <格式>`: 输出格式（excel/text/markdown）

## 脚本说明

### scripts/data_analysis_operations.py
**主脚本** - 提供统一的命令行界面，包含所有核心功能：
- `analyze`: 完整的数据分析
- `compare`: 列对比分析
- `clean`: 数据清洗操作
- `report`: 生成分析报告

### scripts/analyze_data.py
**详细数据分析脚本** - 提供深度数据分析功能：
- 数据质量评分
- 统计摘要生成
- 异常值检测
- 数据分布分析
- 自动报告生成

### scripts/compare_columns.py
**列对比脚本** - 专门用于列对比分析：
- 找出列间差异
- 识别共同值
- 发现唯一值
- 生成对比矩阵

## 编码支持

自动检测和处理的编码：
- UTF-8（推荐）
- GBK/GB2312（中文）
- Latin1（ISO-8859-1）
- CP936（Windows 中文）
- UTF-8-SIG（带 BOM 的 UTF-8）

## 输出格式

### Excel 报告 (`_analysis.xlsx`)
- **Summary**: 文件摘要和关键指标
- **Columns**: 列详细信息
- **Statistics**: 统计摘要
- **Quality**: 数据质量评估
- **Distribution**: 数据分布分析
- **Raw Data**: 原始数据（可选）

### 文本摘要 (`_analysis_summary.txt`)
- 关键发现
- 数据摘要
- 建议和洞察

### Markdown 报告 (`_analysis_report.md`)
- 完整的数据分析报告
- 详细的分析结果
- 可视化描述
- 行动建议

## 使用示例

### 示例 1: 数据分析
```bash
# 分析 CSV 文件
python scripts/data_analysis_operations.py analyze sales_data.csv --focus "Sales" "Profit"

# 分析 Excel 文件指定工作表
python scripts/data_analysis_operations.py analyze sales.xlsx --sheet "Q1" --output reports/
```

### 示例 2: 列对比
```bash
# 对比两列数据
python scripts/data_analysis_operations.py compare customers.csv "Customer_ID" "Email"

# 使用列索引对比
python scripts/data_analysis_operations.py compare data.xlsx "A" "B"
```

### 示例 3: 数据清洗
```bash
# 清理数据并生成清洗报告
python scripts/data_analysis_operations.py clean messy_data.csv --output cleaned/

# 处理编码问题并清理
python scripts/data_analysis_operations.py clean data.csv --encoding gbk --remove-duplicates
```

## 依赖环境

- Python 3.8+
- pandas >= 1.5.0
- numpy >= 1.21.0
- openpyxl >= 3.0.0（Excel 支持）
- matplotlib >= paper>=2.0.0（可视化，可选）

安装依赖：
```bash
pip install pandas numpy openpyxl matplotlib
```

## 最佳实践

1. **数据备份**: 在进行数据清洗前备份原始文件
2. **编码测试**: 如果遇到编码问题，尝试使用 `--encoding` 参数
3. **增量分析**: 对于大数据集，使用 `--sample` 参数先分析样本
4. **结果验证**: 查看生成的报告验证分析结果
5. **参数调优**: 根据数据类型和大小调整分析参数

## 故障排除

### 常见问题

1. **编码错误**
   - 尝试: `--encoding gbk` 或 `--encoding latin1`
   - 检查文件是否损坏

2. **内存不足**
   - 使用 `--sample 1000` 先分析样本
   - 分批处理大数据集

3. **列名不匹配**
   - 使用 `--list-columns` 查看所有列名
   - 检查列名中的空格和特殊字符

4. **Excel 格式问题**
   - 确保安装了 openpyxl
   - 检查文件是否受密码保护

## 支持的文件格式

- **Excel**: .xlsx, .xls, .xlsm
- **CSV**: .csv, .tsv, .txt
- **文本文件**: 逗号分隔、制表符分隔、分号分隔

## 更新日志

- v1.0.0 (2026-06-03): 初始版本，整合数据分析、列对比和数据清洗功能
- v1.0.1 (2026-06-03): 添加编码自动检测和更多输出格式支持

## 联系方式

如需帮助或发现问题，请参考技能文档或联系技能开发者。