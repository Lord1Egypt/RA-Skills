# Pandas Skill 使用示例

[English](EXAMPLES.md) | 简体中文

## 示例1: 完整的数据清洗流程

假设你有一个包含销售数据的CSV文件 `sales_data.csv`，包含缺失值、重复行和异常值。

### 步骤1: 分析数据
```bash
python scripts/data_analyzer.py sales_data.csv -o analysis_report.json
```

查看报告了解数据质量问题。

### 步骤2: 清洗数据
```bash
python scripts/data_cleaner.py sales_data.csv cleaned_sales.csv \
    --standardize-columns \
    --remove-duplicates \
    --handle-missing median \
    --remove-outliers \
    --outlier-method iqr
```

### 步骤3: 验证结果
```bash
python scripts/data_analyzer.py cleaned_sales.csv -o final_report.json
```

对比前后报告，确认清洗效果。

---

## 示例2: 格式转换

### CSV转Excel
```bash
python scripts/data_transformer.py convert data.csv report.xlsx
```

### Excel转JSON
```bash
python scripts/data_transformer.py convert input.xlsx output.json
```

### 多格式转换
```bash
python scripts/data_transformer.py convert report.xlsx report.parquet
```

---

## 示例3: 数据过滤和筛选

### 按条件过滤
```bash
python scripts/data_transformer.py filter employees.csv \
    --query "age > 30 and department == 'Engineering'" \
    --output senior_engineers.csv
```

### 多条件过滤
```bash
python scripts/data_transformer.py filter sales.csv \
    --query "amount > 10000 and status in ['completed', 'shipped']" \
    --output high_value_sales.csv
```

---

## 示例4: 合并多个文件

### 垂直合并(追加行)
```bash
python scripts/data_transformer.py merge \
    january.csv february.csv march.csv \
    --output q1_sales.csv
```

### 按键合并(类似SQL JOIN)
```bash
python scripts/data_transformer.py merge \
    customers.csv orders.csv \
    --output customer_orders.csv \
    --how left \
    --on customer_id
```

---

## 示例5: 数据排序

### 单列排序
```bash
python scripts/data_transformer.py sort employees.csv \
    --by salary \
    --descending \
    --output sorted_by_salary.csv
```

### 多列排序
```bash
python scripts/data_transformer.py sort data.csv \
    --by department salary \
    --output sorted.csv
```

---

## 示例6: 选择特定列

```bash
python scripts/data_transformer.py select full_data.csv \
    --columns name email phone department \
    --output contact_list.csv
```

---

## 示例7: 组合多个操作

完整的数据处理管道:

```bash
# 1. 清洗原始数据
python scripts/data_cleaner.py raw_data.csv clean_data.csv \
    --standardize-columns \
    --remove-duplicates \
    --handle-missing mean

# 2. 过滤有效数据
python scripts/data_transformer.py filter clean_data.csv \
    --query "status == 'active'" \
    --output active_data.csv

# 3. 按重要性排序
python scripts/data_transformer.py sort active_data.csv \
    --by priority \
    --descending \
    --output final_data.csv

# 4. 转换为Excel报表
python scripts/data_transformer.py convert final_data.csv report.xlsx

# 5. 生成最终分析报告
python scripts/data_analyzer.py final_data.csv -o final_analysis.json
```

---

## 常见使用场景

### 场景1: 准备机器学习数据
```bash
# 清洗和标准化
python scripts/data_cleaner.py raw_features.csv \
    ml_ready_data.csv \
    --remove-duplicates \
    --handle-missing mean \
    --remove-outliers \
    --standardize-columns
```

### 场景2: 生成数据质量报告
```bash
python scripts/data_analyzer.py monthly_data.csv \
    --output quality_report.json \
    --format json
```

### 场景3: ETL流程
```bash
# Extract: 合并多个源
python scripts/data_transformer.py merge source1.csv source2.csv source3.csv \
    --output extracted.csv

# Transform: 清洗和过滤
python scripts/data_cleaner.py extracted.csv transformed.csv \
    --handle-missing median \
    --remove-duplicates

# Load: 转换为目标格式
python scripts/data_transformer.py convert transformed.csv final_output.parquet
```

---

## 技巧和提示

1. **总是备份原始数据**
2. **使用分析器了解数据**再进行清洗
3. **渐进式清洗**: 一次应用一个操作,验证结果
4. **保存中间结果**: 方便回溯和调试
5. **查阅参考文档**: `references/` 目录包含详细的pandas操作指南

---

## 进阶技巧

### 批量处理多个文件
```bash
# Windows PowerShell
Get-ChildItem *.csv | ForEach-Object {
    python scripts/data_cleaner.py $_.Name "cleaned_$($_.Name)" --remove-duplicates
}

# Linux/Mac
for file in *.csv; do
    python scripts/data_cleaner.py "$file" "cleaned_${file}" --remove-duplicates
done
```

### 在Python代码中使用
```python
import pandas as pd

# 读取分析报告
import json
with open('report.json', 'r') as f:
    report = json.load(f)
    
# 检查缺失值比例
missing_threshold = 0.3
cols_to_drop = [col for col, info in report['missing_values'].items() 
                if info['percentage'] > missing_threshold]

# 使用pandas直接处理
df = pd.read_csv('data.csv')
df = df.drop(columns=cols_to_drop)
```

### 自定义清洗流程
```python
# 基于data_cleaner.py的代码框架
import pandas as pd

df = pd.read_csv('input.csv')

# 自定义业务逻辑
df['amount'] = df['amount'].apply(lambda x: max(0, x))  # 金额不能为负
df['date'] = pd.to_datetime(df['date'], errors='coerce')  # 转换日期

# 保存结果
df.to_csv('output.csv', index=False)
```

---

## 故障排除

### 问题1: 编码错误
```bash
# 尝试指定编码
python scripts/data_analyzer.py data.csv --encoding utf-8
# 或
python scripts/data_analyzer.py data.csv --encoding gbk
```

### 问题2: 内存不足
```python
# 对于大文件,使用分块读取
import pandas as pd

chunks = []
for chunk in pd.read_csv('large_file.csv', chunksize=10000):
    # 处理每个chunk
    processed = chunk.dropna()
    chunks.append(processed)

result = pd.concat(chunks, ignore_index=True)
```

### 问题3: 日期格式问题
```python
# 在脚本中使用显式日期格式
df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
```

---

## 更多资源

- 查看 [SKILL_CN.md](SKILL_CN.md) 获取完整的技能文档
- 参考 [references/common_operations.md](references/common_operations.md) 学习pandas操作
- 阅读 [references/data_cleaning_best_practices.md](references/data_cleaning_best_practices.md) 掌握最佳实践
