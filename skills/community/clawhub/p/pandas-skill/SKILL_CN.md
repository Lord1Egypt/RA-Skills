---
name: pandas-skill
description: 用于数据操作、清洗、分析和转换的专业pandas技能。处理表格数据、CSV/Excel文件、数据分析任务或任何涉及pandas DataFrames的数据处理工作流时使用此技能。提供常用操作的可执行脚本和全面的参考文档。
---

# Pandas 数据处理技能

[English](SKILL.md) | 简体中文

此技能通过可执行脚本和参考文档提供全面的pandas数据处理能力。在涉及表格数据的操作、清洗、分析或转换任务时使用此技能。

## 何时使用此技能

当用户请求以下操作时激活此技能：

- 数据清洗操作（处理缺失值、重复值、异常值）
- 数据分析和统计摘要
- 格式转换（CSV ↔ Excel ↔ JSON ↔ Parquet）
- 数据转换（过滤、排序、聚合、透视）
- 合并或组合多个数据集
- 生成数据质量报告
- 任何pandas DataFrame操作

## 核心能力

### 1. 数据清洗 (`scripts/data_cleaner.py`)

通过单个命令处理常见的数据清洗任务：

**用法：**
```bash
python scripts/data_cleaner.py input.csv output.csv [选项]
```

**可用选项：**
- `--remove-duplicates`: 删除重复行
- `--handle-missing [策略]`: 处理缺失值
  - 策略：`drop`, `fill`, `forward`, `backward`, `mean`, `median`
- `--fill-value [值]`: 自定义缺失数据填充值
- `--remove-outliers`: 使用IQR或Z-score方法删除异常值
- `--outlier-method [方法]`: 选择 `iqr` 或 `zscore`（默认：iqr）
- `--standardize-columns`: 标准化列名（小写、下划线）

**示例：**
```bash
python scripts/data_cleaner.py data.csv cleaned_data.csv \
    --remove-duplicates \
    --handle-missing mean \
    --remove-outliers \
    --standardize-columns
```

### 2. 数据分析 (`scripts/data_analyzer.py`)

生成全面的数据分析报告：

**用法：**
```bash
python scripts/data_analyzer.py input.csv [选项]
```

**可用选项：**
- `--output, -o [文件]`: 将报告保存到文件
- `--format [格式]`: 输出格式（`json` 或 `text`，默认：json）

**报告包含：**
- 基本信息（行数、列数、内存使用）
- 数据类型分布
- 缺失值分析
- 数值列统计（均值、标准差、最小值、最大值、四分位数、偏度、峰度）
- 分类列统计（唯一值、值计数）
- 相关性分析
- 异常值检测

**示例：**
```bash
python scripts/data_analyzer.py sales_data.csv -o report.json --format json
```

### 3. 数据转换 (`scripts/data_transformer.py`)

通过子命令执行各种数据转换操作：

#### 格式转换
```bash
python scripts/data_transformer.py convert input.csv output.xlsx
```
支持：CSV、Excel（.xlsx/.xls）、JSON、Parquet、HTML

#### 合并文件
```bash
python scripts/data_transformer.py merge file1.csv file2.csv file3.csv \
    --output merged.csv \
    --how outer \
    --on key_column
```

#### 过滤数据
```bash
python scripts/data_transformer.py filter data.csv \
    --query "age > 18 and city == 'Beijing'" \
    --output filtered.csv
```

#### 排序数据
```bash
python scripts/data_transformer.py sort data.csv \
    --by sales quantity \
    --descending \
    --output sorted.csv
```

#### 选择列
```bash
python scripts/data_transformer.py select data.csv \
    --columns name age city \
    --output selected.csv
```

## 参考文档

`references/` 目录包含详细文档：

### `references/common_operations.md`

全面的参考指南，涵盖：
- 数据读取/保存（CSV、Excel、JSON、SQL、Parquet）
- 数据探索（head、info、describe、dtypes）
- 数据选择和过滤（loc、iloc、布尔索引、query）
- 数据清洗（处理缺失/重复值、类型转换）
- 数据转换（apply、map、排序、列操作）
- 分组和聚合操作
- 透视表
- 合并和连接（concat、merge、join）
- 时间序列操作
- 字符串操作
- 性能优化技巧

**使用时机：** 当Claude需要理解pandas语法或查找特定操作的正确方法时。

### `references/data_cleaning_best_practices.md`

最佳实践指南，涵盖：
- 数据质量检查清单
- 带决策树的缺失值处理策略
- 异常值检测方法（IQR、Z-Score、百分位数）
- 数据类型优化以提高内存效率
- 字符串清洗技术
- 日期/时间标准化
- 完整的清洗管道模板
- 常见问题和解决方案
- 数据验证方法

**使用时机：** 设计数据清洗工作流程或决定特定数据质量问题的最佳方法时。

## 工作流指南

### 步骤1: 初始评估
始终从分析数据开始：
```bash
python scripts/data_analyzer.py input_file.csv -o analysis_report.json
```
查看报告以了解数据质量、类型、缺失值和潜在问题。

### 步骤2: 规划清洗策略
基于分析报告：
- 确定缺失值策略（参考：`data_cleaning_best_practices.md`）
- 确定是否应删除重复项
- 决定异常值处理方法
- 规划任何必要的类型转换

### 步骤3: 执行清洗
使用适当的选项运行数据清洗器：
```bash
python scripts/data_cleaner.py input.csv cleaned.csv [选项]
```

### 步骤4: 按需转换
应用任何转换（过滤、排序、格式转换、合并）：
```bash
python scripts/data_transformer.py [子命令] [选项]
```

### 步骤5: 验证结果
重新对清洗后的数据运行分析以验证改进：
```bash
python scripts/data_analyzer.py cleaned.csv -o final_report.json
```

## 常见模式

### 模式1: 快速数据质量报告
```bash
python scripts/data_analyzer.py data.csv --format text
```

### 模式2: 标准清洗管道
```bash
python scripts/data_cleaner.py raw_data.csv clean_data.csv \
    --standardize-columns \
    --remove-duplicates \
    --handle-missing median \
    --remove-outliers
```

### 模式3: Excel转CSV并过滤
```bash
# 转换
python scripts/data_transformer.py convert data.xlsx data.csv

# 过滤
python scripts/data_transformer.py filter data.csv \
    --query "status == 'active'" \
    --output filtered.csv
```

### 模式4: 合并多个CSV
```bash
python scripts/data_transformer.py merge *.csv \
    --output combined.csv
```

## 依赖

确保安装了pandas：
```bash
pip install pandas numpy openpyxl
```

特定格式的可选依赖：
```bash
pip install pyarrow  # Parquet支持
pip install xlrd     # 旧版Excel文件(.xls)
```

## 有效使用提示

1. **从分析开始：** 始终先运行分析器以了解数据
2. **增量清洗：** 逐步应用清洗操作，验证每一步
3. **保留原始数据：** 永远不要覆盖原始数据文件
4. **查阅参考：** 咨询参考文档以了解复杂操作或最佳实践
5. **验证结果：** 使用分析器验证清洗效果
6. **内存效率：** 对于大文件，考虑使用参考文档中的数据类型优化技术
7. **组合操作：** 将多个转换器命令链接起来以实现复杂工作流

## 局限性

- 脚本在单机内存限制下工作（对于非常大的数据集，考虑使用Dask）
- 时间序列重采样和滚动操作需要自定义pandas代码
- 超出基本描述性统计的复杂统计建模需要额外的库
- 对于高级可视化，直接使用matplotlib/seaborn

## 故障排除

**导入错误：** 确保已安装pandas和依赖项
**内存错误：** 分块处理数据或优化dtypes（见参考文档）
**编码问题：** 加载CSV时添加 `encoding='utf-8'` 参数
**日期解析问题：** 使用带显式格式字符串的 `pd.to_datetime()`

有关详细的pandas操作和故障排除，请始终参考 `references/common_operations.md` 和 `references/data_cleaning_best_practices.md`。
