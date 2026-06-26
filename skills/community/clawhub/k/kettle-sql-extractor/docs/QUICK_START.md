# Kettle SQL提取工具 - 快速开始指南

## 概述

本工具用于从Kettle ETL作业中提取SQL脚本，支持批量处理和智能合并。

## 🚀 一分钟上手

### 1. **单个文件提取**
```bash
# 基本用法：提取SQL
python merge_kettle_sql.py job.kjb

# 简化输出（推荐）
python merge_kettle_sql.py job.kjb --simple-output

# 检查结果
ls -la *.sql
cat job_*.sql | head -20
```

### 2. **批量处理**
```bash
# 批量提取目录中所有文件
python batch_extract_kettle_sql.py --dir /path/to/kettle/jobs

# 批量处理指定文件
python batch_extract_kettle_sql.py --file job1.kjb job2.ktr
```

### 3. **查看可视化报告**
```bash
# 生成HTML报告
python batch_extract_kettle_sql.py --dir /path/to/kettle/jobs --output 分析报告

# 打开报告
open 分析报告/batch_report.html  # macOS
start 分析报告/batch_report.html  # Windows
xdg-open 分析报告/batch_report.html  # Linux
```

## 📋 核心功能

### **merge_kettle_sql.py** - 合并SQL工具
将单个Kettle作业中的多个SQL组件合并为一个SQL文件

```bash
# 基本合并
python merge_kettle_sql.py job.kjb

# 简化输出（无多余文件夹）
python merge_kettle_sql.py job.kjb --simple-output

# 批量处理
python merge_kettle_sql.py *.kjb --batch

# 生成不同格式
python merge_kettle_sql.py job.kjb --executable  # 带事务
python merge_kettle_sql.py job.kjb --simple      # 简化版
```

### **batch_extract_kettle_sql.py** - 批量提取工具
批量提取多个Kettle作业中的SQL脚本

```bash
# 目录批量处理
python batch_extract_kettle_sql.py --dir /path/to/kettle/jobs

# 文件列表处理
echo "/path/to/job1.kjb" > files.txt
echo "/path/to/job2.ktr" >> files.txt
python batch_extract_kettle_sql.py --list files.txt

# 合并所有SQL便于查看
python batch_extract_kettle_sql.py --dir /path/to/kettle/jobs --consolidate
```

## 🎯 实用示例

### 示例1：提取单个作业
```bash
# 1. 准备输出目录
mkdir -p /tmp/kettle_output
cd /tmp/kettle_output

# 2. 提取SQL
python merge_kettle_sql.py ~/kettle_jobs/job.kjb --simple-output

# 3. 验证结果
ls -la *.sql
wc -l job_*.sql
```

### 示例2：批量处理并生成报告
```bash
# 1. 批量分析
python batch_extract_kettle_sql.py --dir ~/kettle_jobs --output 我的分析

# 2. 查看统计信息
cat 我的分析/batch_summary.txt

# 3. 打开HTML报告
open 我的分析/batch_report.html
```

### 示例3：简化工作流
```bash
#!/bin/bash
# 简化的工作流脚本

# 设置变量
INPUT_DIR="/path/to/kettle/jobs"
OUTPUT_DIR="/tmp/kettle_sql_$(date +%Y%m%d_%H%M%S)"

# 创建输出目录
mkdir -p "$OUTPUT_DIR"
cd "$OUTPUT_DIR"

# 批量提取并生成报告
python batch_extract_kettle_sql.py --dir "$INPUT_DIR" --output 分析报告

# 批量合并SQL
python merge_kettle_sql.py "$INPUT_DIR"/*.kjb --simple-output

# 显示结果
echo "=== 提取完成 ==="
echo "HTML报告: $OUTPUT_DIR/分析报告/batch_report.html"
echo "SQL文件数: $(ls -1 *.sql | wc -l)"
```

## 🔧 安装配置

### Python环境要求
```bash
# 检查Python版本
python3 --version  # 需要Python 3.6+

# 安装依赖库
pip install lxml beautifulsoup4
```

### 文件权限设置
```bash
# 设置执行权限
chmod +x merge_kettle_sql.py
chmod +x batch_extract_kettle_sql.py
```

## 📊 输出说明

### 简化模式输出（推荐）
```
当前目录/
├── job_作业1_merged_detailed.sql  # 详细SQL（带注释）
├── job_作业2_merged_detailed.sql  # 详细SQL（带注释）
└── job_作业3_merged_detailed.sql  # 详细SQL（带注释）
```

### 批量处理输出
```
batch_kettle_analysis/
├── batch_report.html      # 📊 HTML可视化报告
├── batch_summary.json     # 📋 JSON统计
├── batch_summary.txt      # 📝 文本统计
└── kettle_files/          # 📁 单个文件结果
    ├── job1_kjb/
    │   ├── basic_info.json
    │   ├── sql_components.json
    │   └── extracted_sql.txt
    └── job2_ktr/
        └── ...
```

## ⚠️ 注意事项

### 1. **文件备份**
建议在处理前备份原始Kettle文件：
```bash
cp -r /path/to/kettle/jobs /path/to/kettle/jobs_backup_$(date +%Y%m%d)
```

### 2. **逐步验证**
```bash
# 先测试单个文件
python merge_kettle_sql.py test.kjb --simple-output

# 检查输出
cat job_test_merged_detailed.sql

# 确认无误后批量处理
python merge_kettle_sql.py *.kjb --simple-output
```

### 3. **磁盘空间**
批量处理可能生成较多文件，确保有足够的磁盘空间。

## 🔍 故障排除

### 问题1：无法解析Kettle文件
```bash
# 检查文件格式
file job.kjb  # 应该显示XML文档

# 检查文件内容
head -5 job.kjb  # 应该包含XML声明
```

### 问题2：Python库缺失
```bash
# 安装缺失的库
pip install lxml beautifulsoup4

# 或者使用系统包管理器
sudo apt-get install python3-lxml python3-bs4  # Ubuntu/Debian
```

### 问题3：权限问题
```bash
# 设置执行权限
chmod +x merge_kettle_sql.py batch_extract_kettle_sql.py

# 或者直接使用Python运行
python3 merge_kettle_sql.py job.kjb
```

## 📞 获取帮助

### 查看帮助信息
```bash
# 查看工具帮助
python merge_kettle_sql.py --help
python batch_extract_kettle_sql.py --help
```

### 查看版本信息
```bash
# 查看工具版本
python merge_kettle_sql.py --version
```

### 测试工具
```bash
# 运行内置测试
python -c "from kettle_xml_parser import test_parser; test_parser()"
```

## 🎯 核心特点

1. **✅ 纯提取** - 保持SQL原样，不做修改
2. **✅ 批量处理** - 支持多个文件同时处理
3. **✅ 智能合并** - 自动合并多个SQL组件
4. **✅ 可视化报告** - 生成HTML报告便于分析
5. **✅ 简洁输出** - 避免多余文件夹，直接生成SQL文件

---

**快速开始完成！** 现在你可以开始提取Kettle作业中的SQL了。

如需更多信息，请查看其他文档：
- `USAGE_EXAMPLES.md` - 使用示例
- `MERGE_SQL_QUICKSTART.md` - 合并SQL指南
- `BATCH_EXTRACT_QUICKSTART.md` - 批量提取指南