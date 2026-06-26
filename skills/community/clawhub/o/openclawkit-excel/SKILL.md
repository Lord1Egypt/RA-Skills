---
name: excel-toolkit
description: "Excel文件操作工具套件，提供基础的Excel文件读写、数据处理和报表生成功能。"
homepage: https://github.com/wanghao20150901/openclawkit-excel.git
metadata: { "openclaw": { "emoji": "📈", "requires": { "bins": [], "python": ["pandas", "openpyxl"] } } }
---

# Excel工具套件 (Excel Toolkit)

## 功能概述

这是一个功能完整的Excel文件操作工具套件，提供基础的Excel文件读写、数据处理和报表生成功能。

### 核心功能
- 📁 **文件操作**：创建、读取、写入、合并Excel文件
- 📊 **数据处理**：数据清洗、转换、分析
- 🔧 **格式设置**：单元格格式、样式、图表
- 📈 **报表生成**：多工作表报表、统计图表
- 🔍 **数据验证**：数据完整性检查、错误处理

## 使用时机

✅ **使用此工具当：**
- 需要批量处理Excel文件
- 需要自动化Excel报表生成
- 需要进行数据清洗和转换
- 需要合并多个Excel文件
- 需要创建复杂的Excel模板

## 环境要求

- Python 3.6+
- 依赖包：
  - `pandas` (数据处理)
  - `openpyxl` (Excel文件操作)

安装依赖：
```bash
pip install pandas openpyxl
```

## 使用方法

### 命令行使用
```bash
# 查看帮助
python scripts/main.py --help

# 合并多个Excel文件
python scripts/main.py merge --input "file1.xlsx,file2.xlsx" --output merged.xlsx

# 转换CSV到Excel
python scripts/main.py convert --input data.csv --output data.xlsx

# 数据清洗
python scripts/main.py clean --input raw_data.xlsx --output clean_data.xlsx

# 生成统计报表
python scripts/main.py report --input sales.xlsx --output sales_report.xlsx
```

### Python API使用
```python
from openclawkit_excel import ExcelToolkit

# 初始化工具
excel = ExcelToolkit(debug=True)

# 创建Excel文件
data = {
    '姓名': ['张三', '李四', '王五'],
    '年龄': [25, 30, 35],
    '部门': ['技术部', '市场部', '销售部']
}
excel.create_excel('员工信息.xlsx', data)

# 读取Excel文件
df = excel.read_excel('员工信息.xlsx')
print(df)

# 数据清洗
cleaned_df = excel.clean_data(df)
excel.write_excel('清洗后数据.xlsx', cleaned_df)
```

## 功能模块

### 1. 文件操作模块
- 创建新Excel文件
- 读取现有Excel文件
- 写入数据到Excel
- 合并多个Excel文件
- 拆分Excel文件

### 2. 数据处理模块
- 数据清洗（去重、填充空值、格式转换）
- 数据转换（类型转换、编码转换）
- 数据筛选（条件筛选、随机抽样）
- 数据聚合（分组统计、透视表）

### 3. 格式设置模块
- 单元格格式（字体、颜色、对齐）
- 数字格式（货币、百分比、日期）
- 条件格式（数据条、色阶、图标集）
- 图表生成（柱状图、折线图、饼图）

### 4. 报表生成模块
- 多工作表报表
- 统计摘要报表
- 数据透视报表
- 可视化报表

### 5. 数据验证模块
- 数据类型验证
- 数据范围验证
- 唯一性验证
- 业务规则验证

## 示例代码

### 基础示例
```python
from openclawkit_excel import ExcelToolkit

# 创建工具实例
excel = ExcelToolkit()

# 检查文件是否存在
if excel.file_exists('data.xlsx'):
    # 读取文件
    df = excel.read_excel('data.xlsx')
    
    # 数据清洗
    df_clean = excel.clean_data(df)
    
    # 保存清洗后的数据
    excel.write_excel('data_clean.xlsx', df_clean)
    
    # 生成统计报表
    excel.generate_report(df_clean, 'report.xlsx')
```

### 高级示例
```python
from openclawkit_excel import ExcelToolkit

excel = ExcelToolkit(debug=True)

# 合并多个文件
files = ['q1.xlsx', 'q2.xlsx', 'q3.xlsx', 'q4.xlsx']
merged_df = excel.merge_files(files, merge_on='日期')
excel.write_excel('年度数据.xlsx', merged_df)

# 创建复杂报表
report_data = {
    'summary': excel.generate_summary(merged_df),
    'monthly': excel.group_by_month(merged_df),
    'top10': excel.get_top_items(merged_df, '销售额', 10),
    'trend': excel.calculate_trend(merged_df, '销售额')
}

excel.create_multi_sheet_report('年度分析报告.xlsx', report_data)
```

## 错误处理

工具包含完善的错误处理机制：
- 文件不存在或损坏处理
- 数据格式错误处理
- 内存不足处理
- 并发访问处理

## 性能优化

- **批量处理**：支持大文件分批处理
- **内存映射**：减少内存占用
- **并行计算**：多核CPU加速
- **缓存机制**：减少重复计算

## 更新日志

### v1.0.1 (2026-03-28)
- 初始版本发布
- 基础文件操作功能
- 数据处理和清洗功能
- 报表生成功能
- 完整的错误处理

## 许可证

MIT License

## 作者

浩哥 (Hao Ge)

## 反馈与贡献

欢迎提交Issue和Pull Request：
- GitHub: https://github.com/wanghao20150901/openclawkit-excel.git
- Email: 512975801@qq.com