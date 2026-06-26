# Kettle SQL提取完整工作流程

## 📋 概述

本工作流程详细说明如何使用Kettle SQL提取工具从Kettle作业中提取SQL脚本，包括批量处理、合并和生成报告。

## 🎯 工作流程概览

```
📁 输入Kettle作业 (.kjb/.ktr)
    │
    ├── 1️⃣ 批量分析
    │     └── 📊 生成HTML报告
    │
    ├── 2️⃣ 批量提取
    │     └── 📝 提取每个作业的SQL
    │
    ├── 3️⃣ 智能合并
    │     └── 🔄 合并单个作业的多个SQL组件
    │
    └── 4️⃣ 输出整理
          ├── 📄 详细SQL文件（每个作业一个）
          ├── 📊 HTML可视化报告
          └── 📋 分析统计
```

## 🔧 详细步骤

### 步骤1：准备工作

#### 1.1 创建输出目录
```bash
# 创建工作目录
mkdir -p /path/to/workdir
cd /path/to/workdir

# 创建输出目录结构
mkdir -p output/{sql_files,reports,analysis}
```

#### 1.2 备份原始文件（建议）
```bash
# 备份Kettle作业文件
cp -r /path/to/kettle/jobs /path/to/kettle/jobs_backup_$(date +%Y%m%d)
```

### 步骤2：批量分析

#### 2.1 生成HTML可视化报告
```bash
python batch_extract_kettle_sql.py --dir /path/to/kettle/jobs --output output/reports
```

#### 2.2 查看报告
```bash
# 打开HTML报告
open output/reports/batch_report.html  # macOS
start output/reports/batch_report.html  # Windows
xdg-open output/reports/batch_report.html  # Linux
```

#### 2.3 查看统计分析
```bash
# 查看统计信息
cat output/reports/batch_summary.txt

# 查看JSON格式统计
cat output/reports/batch_summary.json | python -m json.tool
```

### 步骤3：批量提取SQL

#### 3.1 提取所有作业的SQL
```bash
cd output/sql_files
python merge_kettle_sql.py /path/to/kettle/jobs/*.kjb --simple-output
```

#### 3.2 验证提取结果
```bash
# 统计SQL文件数量
ls -1 *.sql | wc -l

# 查看文件大小
ls -lh *.sql

# 检查第一个SQL文件
head -50 job_*.sql
```

### 步骤4：智能合并（可选）

#### 4.1 生成详细合并SQL
```bash
# 为每个作业生成详细合并SQL
for kettle_file in /path/to/kettle/jobs/*.kjb; do
    job_name=$(basename "$kettle_file" .kjb)
    python merge_kettle_sql.py "$kettle_file" --only-detailed --output "output/merged/${job_name}"
done
```

#### 4.2 生成可执行SQL（带事务）
```bash
# 生成带事务控制的SQL
for kettle_file in /path/to/kettle/jobs/*.kjb; do
    job_name=$(basename "$kettle_file" .kjb)
    python merge_kettle_sql.py "$kettle_file" --executable --output "output/executable/${job_name}"
done
```

### 步骤5：分析整理

#### 5.1 生成分析报告
```bash
# 创建分析报告目录
mkdir -p output/analysis

# 分析所有SQL文件
for sql_file in output/sql_files/*.sql; do
    filename=$(basename "$sql_file")
    echo "=== 分析: $filename ===" >> output/analysis/sql_analysis.txt
    echo "文件大小: $(wc -l < "$sql_file") 行" >> output/analysis/sql_analysis.txt
    echo "文件内容预览:" >> output/analysis/sql_analysis.txt
    head -10 "$sql_file" >> output/analysis/sql_analysis.txt
    echo "" >> output/analysis/sql_analysis.txt
done
```

#### 5.2 提取表名和关键字
```bash
# 提取所有SQL文件中的表名
grep -o -i "FROM \|JOIN \|INTO \|UPDATE " output/sql_files/*.sql | \
    awk '{print $2}' | sort | uniq > output/analysis/tables_mentioned.txt

# 提取SQL关键字
grep -o -i "SELECT\|INSERT\|UPDATE\|DELETE\|CREATE\|DROP\|ALTER" output/sql_files/*.sql | \
    sort | uniq > output/analysis/sql_keywords.txt
```

### 步骤6：最终整理

#### 6.1 创建最终输出结构
```bash
# 创建最终输出目录
final_output="kettle_sql_extraction_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$final_output"

# 组织文件
mv output/sql_files/*.sql "$final_output/"
mv output/reports/*.html "$final_output/"
mv output/analysis/*.txt "$final_output/"

# 创建README文件
cat > "$final_output/README.md" << EOF
# Kettle SQL提取结果

## 基本信息
- 提取时间: $(date)
- 源文件数量: $(ls /path/to/kettle/jobs/*.kjb 2>/dev/null | wc -l)
- SQL文件数量: $(ls "$final_output"/*.sql 2>/dev/null | wc -l)

## 文件说明
- \`*.sql\` - 提取的SQL文件（每个Kettle作业对应一个）
- \`batch_report.html\` - HTML可视化报告
- \`*.txt\` - 分析报告

## 使用说明
1. 查看HTML报告了解整体情况
2. 检查SQL文件内容
3. 根据需求进一步处理
EOF
```

#### 6.2 生成总结报告
```bash
cat > "$final_output/summary.txt" << EOF
=== Kettle SQL提取总结 ===
提取时间: $(date)
源目录: /path/to/kettle/jobs
输出目录: $final_output

=== 统计信息 ===
SQL文件数: $(find "$final_output" -name "*.sql" | wc -l)
HTML报告: batch_report.html
分析报告: $(find "$final_output" -name "*.txt" | wc -l) 个

=== 注意事项 ===
1. SQL文件保持原样，未做任何修改
2. 所有历史备份组件都已保留
3. 日期函数保持原始格式
4. 执行顺序保持Kettle中的原始顺序

=== 后续建议 ===
1. 检查SQL文件的业务逻辑完整性
2. 根据目标数据库系统进行必要的语法调整
3. 测试SQL在目标环境中的执行
EOF
```

## 📊 输出文件结构

### 最终输出目录
```
kettle_sql_extraction_20260331_114900/
├── README.md                         # 📖 说明文档
├── summary.txt                       # 📋 总结报告
├── batch_report.html                 # 📊 HTML可视化报告
├── job_作业1_merged_detailed.sql     # 📝 详细SQL（作业1）
├── job_作业2_merged_detailed.sql     # 📝 详细SQL（作业2）
├── job_作业3_merged_detailed.sql     # 📝 详细SQL（作业3）
├── sql_analysis.txt                  # 🔍 SQL分析报告
├── tables_mentioned.txt              # 📋 涉及表名
└── sql_keywords.txt                  # 🔑 SQL关键字统计
```

### 中间文件目录（可选保留）
```
output/
├── sql_files/                       # 📄 原始SQL提取
├── reports/                         # 📊 分析报告
├── merged/                          # 🔄 合并SQL文件
├── executable/                      # ⚡ 可执行SQL
└── analysis/                        # 🔍 详细分析
```

## 🎯 使用场景

### 场景1：快速提取和查看
```bash
# 简单提取并查看
python merge_kettle_sql.py job.kjb --simple-output
cat job_*.sql | head -100
```

### 场景2：批量处理和归档
```bash
# 完整工作流程
./complete_workflow.sh /path/to/kettle/jobs
```

### 场景3：团队协作和分享
```bash
# 生成完整的提取包
tar -czf kettle_sql_$(date +%Y%m%d).tar.gz kettle_sql_extraction_*/
```

## 🔧 自动化脚本

### 完整工作流程脚本
```bash
#!/bin/bash
# complete_workflow.sh

set -e  # 遇到错误立即退出

# 参数检查
if [ $# -ne 1 ]; then
    echo "用法: $0 <Kettle作业目录>"
    exit 1
fi

INPUT_DIR="$1"
OUTPUT_DIR="kettle_sql_extraction_$(date +%Y%m%d_%H%M%S)"
WORK_DIR="work_$(date +%Y%m%d_%H%M%S)"

echo "=== 开始Kettle SQL提取工作流程 ==="
echo "输入目录: $INPUT_DIR"
echo "输出目录: $OUTPUT_DIR"
echo "工作目录: $WORK_DIR"

# 创建工作目录
mkdir -p "$WORK_DIR"
cd "$WORK_DIR"

echo "=== 步骤1: 批量分析 ==="
mkdir -p reports
python batch_extract_kettle_sql.py --dir "$INPUT_DIR" --output reports
echo "✅ HTML报告已生成"

echo "=== 步骤2: 批量提取SQL ==="
mkdir -p sql_files
cd sql_files
python merge_kettle_sql.py "$INPUT_DIR"/*.kjb --simple-output
cd ..
echo "✅ SQL文件已提取"

echo "=== 步骤3: 分析整理 ==="
mkdir -p analysis

# 分析SQL文件
echo "分析SQL文件..." > analysis/analysis.txt
for sql_file in sql_files/*.sql; do
    echo "=== $(basename "$sql_file") ===" >> analysis/analysis.txt
    echo "行数: $(wc -l < "$sql_file")" >> analysis/analysis.txt
    echo "" >> analysis/analysis.txt
done

echo "=== 步骤4: 创建最终输出 ==="
cd ..
mkdir -p "$OUTPUT_DIR"

# 复制文件
cp -r "$WORK_DIR/sql_files"/*.sql "$OUTPUT_DIR/"
cp -r "$WORK_DIR/reports"/batch_report.html "$OUTPUT_DIR/"
cp -r "$WORK_DIR/analysis"/*.txt "$OUTPUT_DIR/"

# 创建README
cat > "$OUTPUT_DIR/README.md" << EOF
# Kettle SQL提取结果

## 基本信息
- 提取时间: $(date)
- 源文件目录: $INPUT_DIR
- 输出目录: $OUTPUT_DIR

## 文件清单
- SQL文件: $(ls -1 "$OUTPUT_DIR"/*.sql 2>/dev/null | wc -l) 个
- 报告文件: batch_report.html
- 分析文件: $(ls -1 "$OUTPUT_DIR"/*.txt 2>/dev/null | wc -l) 个

## 使用说明
1. 打开 \`batch_report.html\` 查看可视化报告
2. 检查 \`*.sql\` 文件内容
3. 查看 \`*.txt\` 分析文件
EOF

echo "=== 步骤5: 清理工作目录 ==="
rm -rf "$WORK_DIR"

echo "=== 工作流程完成 ==="
echo "输出目录: $OUTPUT_DIR"
echo "总SQL文件数: $(ls -1 "$OUTPUT_DIR"/*.sql 2>/dev/null | wc -l)"
```

## ⚠️ 注意事项

### 1. **文件备份**
建议在处理前备份原始Kettle文件：
```bash
cp -r "$INPUT_DIR" "${INPUT_DIR}_backup_$(date +%Y%m%d)"
```

### 2. **磁盘空间**
批量处理可能生成大量文件，确保有足够的磁盘空间。

### 3. **逐步验证**
```bash
# 先测试单个文件
python merge_kettle_sql.py test.kjb --simple-output

# 验证输出
head -20 job_test_merged_detailed.sql

# 确认无误后批量处理
python merge_kettle_sql.py *.kjb --simple-output
```

### 4. **错误处理**
如果处理过程中出现错误：
1. 检查原始文件是否损坏
2. 查看错误日志
3. 尝试单独处理有问题的文件

## 📈 性能优化

### 大文件处理
```bash
# 分批处理大量文件
find /path/to/kettle/jobs -name "*.kjb" | split -l 10 - file_batch_
for batch in file_batch_*; do
    python merge_kettle_sql.py $(cat "$batch") --simple-output
done
```

### 内存优化
```bash
# 使用Python的内存优化选项
PYTHONUNBUFFERED=1 python merge_kettle_sql.py job.kjb --simple-output
```

## 📞 技术支持

### 常见问题解决
1. **文件解析错误**: 检查Kettle文件是否为有效的XML格式
2. **SQL提取不完整**: 使用`kettle_xml_parser.py`进行详细分析
3. **性能问题**: 分批处理大文件

### 获取帮助
```bash
# 查看工具帮助
python merge_kettle_sql.py --help
python batch_extract_kettle_sql.py --help

# 查看版本信息
python -c "import kettle_xml_parser; print('版本: 2.0.0 - 纯SQL提取工具')"
```

---

**工作流程完成！** 现在你已经成功提取了Kettle作业中的所有SQL脚本。

如需进一步处理，请根据目标数据库系统的要求进行相应的语法调整。