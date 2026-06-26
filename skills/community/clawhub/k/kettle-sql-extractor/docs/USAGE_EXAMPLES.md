# Kettle SQL批量提取功能使用示例

## 概述
`batch_extract_kettle_sql.py` 是一个强大的批量处理工具，用于从多个Kettle作业文件中提取SQL脚本。

## 功能特性
1. **批量处理**：支持目录、文件列表、指定文件三种方式
2. **智能分析**：自动分析SQL内容，提取表名、关键字等
3. **多种输出格式**：JSON、文本、HTML报告
4. **错误隔离**：单个文件失败不影响其他文件
5. **合并输出**：可选生成合并的SQL文件

## 使用场景

### 场景1：处理整个Kettle项目目录
当你有一个包含多个Kettle作业的目录时：

```bash
# 处理目录中所有.kjb和.ktr文件
python batch_extract_kettle_sql.py --dir /path/to/kettle/project

# 处理目录，并生成合并的SQL文件
python batch_extract_kettle_sql.py --dir /path/to/kettle/project --consolidate

# 指定输出目录
python batch_extract_kettle_sql.py --dir /path/to/kettle/project --output my_analysis
```

### 场景2：处理指定的文件列表
当你只需要处理特定的文件时：

```bash
# 直接指定多个文件
python batch_extract_kettle_sql.py --file job1.kjb job2.ktr transformation1.kjb

# 从文件列表读取
echo "/path/to/job1.kjb" > kettle_files.txt
echo "/path/to/transformation1.ktr" >> kettle_files.txt
python batch_extract_kettle_sql.py --list kettle_files.txt
```

### 场景3：处理特定模式的文件
当需要过滤特定类型的文件时：

```bash
# 只处理.kjb文件
python batch_extract_kettle_sql.py --dir /path/to/kettle/project --pattern "*.kjb"

# 处理多种模式
python batch_extract_kettle_sql.py --dir /path/to/kettle/project --pattern "*.kjb" "DWD_*.ktr"
```

## 输出结构

### 批处理目录结构
```
batch_kettle_analysis/
├── batch_20260330_093348/              # 按时间戳命名的批处理目录
│   ├── batch_summary.json              # JSON格式批处理总结
│   ├── batch_summary.txt               # 文本格式批处理总结
│   ├── batch_report.html               # HTML可视化报告
│   ├── all_extracted_sql.txt           # 合并的SQL文件(如指定--consolidate)
│   └── kettle_files/                   # 按目录处理的文件结果
│       ├── job1_kjb/                   # 单个文件结果目录
│       │   ├── basic_info.json         # 文件基本信息
│       │   ├── sql_components.json     # SQL组件(JSON格式)
│       │   ├── extracted_sql.txt       # SQL组件(文本格式，便于查看)
│       │   └── detailed_analysis.json  # 详细分析结果
│       └── transformation1_ktr/
│           └── ...
```

### HTML报告
HTML报告提供可视化展示，包含：
- 处理统计（文件数、SQL组件数等）
- 发现的唯一表名和关键字
- 文件处理状态（成功/失败）
- 点击链接查看详细结果

### 合并SQL文件
当使用 `--consolidate` 参数时，会生成 `all_extracted_sql.txt` 文件，包含所有提取的SQL，格式如下：
```
【文件】job1.kjb
【路径】/path/to/job1.kjb
【SQL组件数】2
--------------------------------------------------------------------------------

组件 1: 建表SQL
长度: 111 字符
操作类型: CREATE TABLE
涉及表: TEST_TABLE1
--------------------------------------------------------------------------------
CREATE TABLE test_table1 (
  id BIGINT,
  name VARCHAR(100),
  amount DECIMAL(18,2),
  create_time TIMESTAMP
);

================================================================================
```

## 实际工作流程

### 完整的Kettle迁移工作流程
```bash
# 1. 批量提取所有Kettle作业的SQL
python batch_extract_kettle_sql.py --dir /path/to/kettle/project --consolidate

# 2. 查看提取报告
open batch_kettle_analysis/batch_*/batch_report.html

# 3. 分析提取结果
cat batch_kettle_analysis/batch_*/batch_summary.txt
cat batch_kettle_analysis/batch_*/all_extracted_sql.txt

# 4. 针对每个作业进行进一步处理
for job_dir in batch_kettle_analysis/batch_*/kettle_files/*/; do
    job_name=$(basename $job_dir)
    echo "处理作业: $job_name"
    
    # 进一步处理提取的SQL
    # 例如：转换为特定数据库语法，或进行SQL优化
    # python process_sql.py "$job_dir/extracted_sql.txt" \
    #     --output "processed_output/${job_name}_processed.sql"
done

# 5. 验证处理结果
# python validate_processing.py processed_output/*.sql
```

### 增量处理工作流程
当有新增或修改的Kettle文件时：

```bash
# 创建新增文件列表
find /path/to/kettle/project -name "*.kjb" -newer last_run.timestamp > new_files.txt
find /path/to/kettle/project -name "*.ktr" -newer last_run.timestamp >> new_files.txt

# 仅处理新增文件
if [ -s new_files.txt ]; then
    python batch_extract_kettle_sql.py --list new_files.txt --output incremental_analysis
    
    # 更新时间戳
    touch last_run.timestamp
fi
```

## 高级用法

### 1. 集成到CI/CD流水线
```yaml
# .gitlab-ci.yml 示例
stages:
  - kettle-analysis
  - sql-conversion
  - validation

kettle-analysis:
  stage: kettle-analysis
  script:
    - python batch_extract_kettle_sql.py --dir kettle_jobs --consolidate
    - cp batch_kettle_analysis/batch_*/batch_summary.json $CI_PROJECT_DIR/artifacts/
    - cp batch_kettle_analysis/batch_*/batch_report.html $CI_PROJECT_DIR/artifacts/
  artifacts:
    paths:
      - batch_kettle_analysis/
      - artifacts/

sql-conversion:
  stage: sql-conversion
  script:
    - python convert_to_starrocks.py batch_kettle_analysis/batch_*/all_extracted_sql.txt
  artifacts:
    paths:
      - starrocks_output/
```

### 2. 定期监控Kettle作业
```bash
#!/bin/bash
# monitor_kettle_changes.sh

PROJECT_DIR="/path/to/kettle/project"
OUTPUT_BASE="kettle_monitoring"
LAST_RUN_FILE="$OUTPUT_BASE/last_run"

# 检查是否有新文件
if [ ! -f "$LAST_RUN_FILE" ] || find "$PROJECT_DIR" -name "*.kjb" -o -name "*.ktr" -newer "$LAST_RUN_FILE" | grep -q .; then
    echo "检测到Kettle文件变更，开始分析..."
    
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    OUTPUT_DIR="$OUTPUT_BASE/analysis_$TIMESTAMP"
    
    # 批量提取
    python batch_extract_kettle_sql.py --dir "$PROJECT_DIR" --output "$OUTPUT_DIR" --consolidate
    
    # 发送通知
    SUMMARY=$(cat "$OUTPUT_DIR/batch_*/batch_summary.txt" | head -20)
    echo "Kettle作业分析完成：$SUMMARY" | mail -s "Kettle作业变更报告" admin@example.com
    
    # 更新最后运行时间
    touch "$LAST_RUN_FILE"
else
    echo "未检测到Kettle文件变更"
fi
```

### 3. 批量提取与数据目录集成
```python
#!/usr/bin/env python3
"""
集成批量提取到数据目录系统
"""

import json
import yaml
from batch_extract_kettle_sql import BatchKettleSQLExtractor

def integrate_with_data_catalog(kettle_dir, catalog_file="data_catalog.yaml"):
    """将Kettle提取结果集成到数据目录"""
    
    # 批量提取
    extractor = BatchKettleSQLExtractor()
    summary = extractor.process_directory(kettle_dir)
    
    # 读取或创建数据目录
    try:
        with open(catalog_file, 'r') as f:
            catalog = yaml.safe_load(f) or {}
    except FileNotFoundError:
        catalog = {'tables': [], 'etl_jobs': []}
    
    # 更新数据目录
    for file_info in summary['file_summaries']:
        if file_info['status'] == 'success':
            job_entry = {
                'name': file_info['file_name'],
                'type': file_info['file_type'],
                'sql_count': len(file_info['sql_components']),
                'tables': [],
                'extraction_time': summary['batch_id']
            }
            
            # 提取表信息
            for analysis in file_info['analysis']['sql_analyses']:
                job_entry['tables'].extend(analysis['tables'])
            
            catalog['etl_jobs'].append(job_entry)
    
    # 更新表信息
    for table in summary['unique_tables']:
        if not any(t['name'] == table for t in catalog['tables']):
            catalog['tables'].append({
                'name': table,
                'source': 'kettle',
                'first_seen': summary['batch_id']
            })
    
    # 保存数据目录
    with open(catalog_file, 'w') as f:
        yaml.dump(catalog, f, default_flow_style=False)
    
    print(f"数据目录已更新: {catalog_file}")
    print(f"作业数: {len(catalog['etl_jobs'])}")
    print(f"表数: {len(catalog['tables'])}")

if __name__ == "__main__":
    integrate_with_data_catalog("/path/to/kettle/jobs")
```

## 故障排除

### 常见问题1：没有提取到SQL组件
**可能原因**：
1. Kettle文件格式不正确
2. XML结构不符合预期
3. 文件编码问题

**解决方法**：
```bash
# 检查文件内容
head -50 problem_file.kjb

# 尝试不同编码
iconv -f GBK -t UTF-8 problem_file.kjb > problem_file_utf8.kjb
python batch_extract_kettle_sql.py --file problem_file_utf8.kjb

# 使用调试模式
python -c "
import re
with open('problem_file.kjb', 'r', encoding='utf-8') as f:
    content = f.read()
    
# 查找<sql>标签
sql_tags = re.findall(r'<sql[^>]*>.*?</sql>', content, re.DOTALL)
print(f'找到 {len(sql_tags)} 个<sql>标签')
for i, tag in enumerate(sql_tags[:3]):
    print(f'标签 {i+1}: {tag[:100]}...')
"
```

### 常见问题2：内存不足
**解决方法**：
```bash
# 分批处理
find /path/to/kettle/jobs -name "*.kjb" | split -l 10 - batch_
for batch in batch_*; do
    python batch_extract_kettle_sql.py --list "$batch" --output "batch_${batch}"
done
```

### 常见问题3：输出文件太大
**解决方法**：
```bash
# 不生成合并文件
python batch_extract_kettle_sql.py --dir /path/to/kettle/jobs

# 只生成HTML报告
python batch_extract_kettle_sql.py --dir /path/to/kettle/jobs --output compact_output
rm compact_output/batch_*/all_extracted_sql.txt 2>/dev/null || true
```

## 性能优化建议

1. **批量大小**：一次处理100-500个文件最佳
2. **输出管理**：定期清理旧的批处理目录
3. **内存使用**：大文件单独处理
4. **并行处理**：多个目录可并行处理

```bash
# 并行处理示例
for dir in kettle_jobs/*/; do
    (python batch_extract_kettle_sql.py --dir "$dir" --output "output_$(basename $dir)") &
done
wait
```

## 总结

`batch_extract_kettle_sql.py` 是Kettle SQL批量提取工作流中的重要工具，它提供了：

1. **效率提升**：批量处理替代手动单个处理
2. **质量保证**：统一的分析和报告
3. **可追溯性**：详细的日志和结果文件
4. **灵活性**：支持多种输入方式和输出格式

通过合理使用这个工具，可以显著提高Kettle作业迁移的效率和可靠性。