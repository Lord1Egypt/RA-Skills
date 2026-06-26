# 批量提取Kettle SQL脚本 - 快速入门

## 🚀 一句话总结
`batch_extract_kettle_sql.py` 让你一次性从多个Kettle作业中提取所有SQL脚本！

## 📋 主要功能
- ✅ **批量处理**：目录、文件列表、指定文件三种方式
- ✅ **智能分析**：自动提取表名、关键字、SQL统计
- ✅ **多种报告**：JSON、文本、HTML可视化报告
- ✅ **合并输出**：可选生成统一的SQL文件
- ✅ **错误隔离**：单个文件失败不影响其他

## 🎯 常用命令

### 基本用法
```bash
# 1. 处理整个目录
python batch_extract_kettle_sql.py --dir /path/to/kettle/jobs

# 2. 处理指定文件
python batch_extract_kettle_sql.py --file job1.kjb job2.ktr

# 3. 从列表处理
echo "/path/to/job1.kjb" > my_files.txt
python batch_extract_kettle_sql.py --list my_files.txt
```

### 高级选项
```bash
# 生成合并的SQL文件
python batch_extract_kettle_sql.py --dir /path/to/jobs --consolidate

# 指定输出目录
python batch_extract_kettle_sql.py --dir /path/to/jobs --output my_analysis

# 只处理特定模式
python batch_extract_kettle_sql.py --dir /path/to/jobs --pattern "DWD_*.kjb"
```

## 📁 输出结构
处理完成后，你会得到这样的目录结构：
```
batch_kettle_analysis/
└── batch_20260330_093348/          # 批处理目录（按时间戳）
    ├── batch_summary.txt           # 📊 文本总结（先看这个！）
    ├── batch_report.html           # 🌐 HTML可视化报告
    ├── all_extracted_sql.txt       # 📦 合并的SQL（如指定--consolidate）
    └── kettle_files/               # 📁 每个文件的详细结果
        ├── job1_kjb/
        │   ├── extracted_sql.txt   # 📝 该文件的SQL（文本格式）
        │   └── basic_info.json     # 📋 文件信息
        └── ...
```

## 🔍 快速查看结果
```bash
# 1. 查看处理总结
cat batch_kettle_analysis/batch_*/batch_summary.txt

# 2. 打开HTML报告（如果有浏览器）
open batch_kettle_analysis/batch_*/batch_report.html

# 3. 查看合并的SQL
cat batch_kettle_analysis/batch_*/all_extracted_sql.txt

# 4. 查看单个文件的SQL
cat batch_kettle_analysis/batch_*/kettle_files/job1_kjb/extracted_sql.txt
```

## 💡 实用技巧

### 技巧1：快速检查SQL提取情况
```bash
# 查看提取了多少SQL组件
grep "总SQL组件数:" batch_kettle_analysis/batch_*/batch_summary.txt

# 查看发现了哪些表
grep -A5 "唯一表名:" batch_kettle_analysis/batch_*/batch_summary.txt
```

### 技巧2：批量处理后的转换工作流
```bash
# 批量提取
python batch_extract_kettle_sql.py --dir kettle_jobs --consolidate

# 查看哪些作业有SQL
BATCH_DIR=$(ls -td batch_kettle_analysis/batch_*/ | head -1)
for job_dir in $BATCH_DIR/kettle_files/*/; do
    if [ -f "$job_dir/extracted_sql.txt" ]; then
        job_name=$(basename $job_dir)
        echo "✅ $job_name 有SQL可转换"
    fi
done
```

### 技巧3：创建简单的监控脚本
```bash
#!/bin/bash
# monitor_and_extract.sh

JOBS_DIR="/path/to/kettle/jobs"
OUTPUT_BASE="kettle_extractions"

# 运行提取
python batch_extract_kettle_sql.py --dir "$JOBS_DIR" --output "$OUTPUT_BASE" --consolidate

# 获取最新结果
LATEST=$(ls -td "$OUTPUT_BASE"/batch_*/ | head -1)

# 显示关键信息
echo "📊 提取完成!"
echo "目录: $LATEST"
echo ""
cat "$LATEST/batch_summary.txt" | grep -E "(总文件数|总SQL组件数|唯一表名)"
```

## 🐛 常见问题

### Q1: 为什么有些文件没有提取到SQL？
**A**: 检查Kettle文件的XML结构。确保：
- 文件是有效的XML
- SQL内容在 `<sql>` 标签中
- 文件编码是UTF-8或GBK

### Q2: 输出目录太多了怎么办？
**A**: 定期清理或使用统一的输出目录：
```bash
# 使用固定输出目录
python batch_extract_kettle_sql.py --dir kettle_jobs --output "latest_analysis"

# 清理7天前的输出
find batch_kettle_analysis -type d -name "batch_*" -mtime +7 -exec rm -rf {} \;
```

### Q3: 如何处理大量文件？
**A**: 分批处理：
```bash
# 每次处理50个文件
find kettle_jobs -name "*.kjb" | split -l 50 - batch_part_
for part in batch_part_*; do
    python batch_extract_kettle_sql.py --list "$part" --output "batch_${part}"
done
```

## 🚀 下一步
提取SQL后，你可以：
1. **进一步处理**：将提取的SQL用于特定需求
2. **数据库迁移**：将SQL迁移到目标数据库系统
3. **验证转换结果**：使用 `validate_conversion.py`

## 📞 获取帮助
```bash
# 查看完整帮助
python batch_extract_kettle_sql.py --help

# 查看版本信息
grep "version" SKILL.md | head -1

# 查看使用示例
cat USAGE_EXAMPLES.md | head -50
```

---
**提示**: 批量提取是Kettle迁移的第一步，先确保SQL提取完整，再进行后续转换！