# 只要SQL文件需求指南

## 📋 需求背景

基于用户反馈，很多用户在使用Kettle SQL提取工具时有一个明确的需求：
**"我只要提取之后的sql文件，不要给我其他东西"**

这个需求在以下场景中非常常见：
1. SQL备份和迁移
2. 代码审查和验证
3. 版本控制管理
4. 日常维护工作

## 🎯 解决方案

### 核心参数：`--simple-output`

使用 `--simple-output` 参数可以满足"只要SQL文件"的需求：

```bash
# 单个文件处理，只要SQL文件
python merge_kettle_sql.py job.kjb --simple-output

# 批量处理，只要SQL文件
for file in *.kjb; do
    python merge_kettle_sql.py "$file" --simple-output
done
```

## 📁 输出对比

### 模式1：只要SQL文件（使用 `--simple-output`）
```
当前目录/
├── job_作业名称1_merged_detailed.sql
├── job_作业名称2_merged_detailed.sql
└── job_作业名称3_merged_detailed.sql
```

**特点**：
- 只生成SQL文件
- 没有HTML报告、JSON总结等额外文件
- 文件结构简洁
- 便于管理和版本控制

### 模式2：完整分析报告（不使用 `--simple-output`）
```
batch_kettle_analysis/
├── batch_report.html
├── batch_summary.json
├── batch_summary.txt
└── kettle_files/
    ├── job1_kjb/
    │   ├── basic_info.json
    │   ├── sql_components.json
    │   └── extracted_sql.txt
    └── ...
```

**特点**：
- 包含完整的分析报告
- 适合项目分析和文档生成
- 文件较多，结构复杂

## 🚀 使用示例

### 示例1：提取单个Kettle作业，只要SQL文件
```bash
# 提取单个文件
python merge_kettle_sql.py /path/to/job.kjb --simple-output

# 输出：在当前目录生成 job_名称_merged_detailed.sql
```

### 示例2：批量提取目录中所有Kettle作业，只要SQL文件
```bash
# 进入目标目录
cd /path/to/output

# 批量处理
for file in /path/to/kettle/jobs/*.kjb; do
    python merge_kettle_sql.py "$file" --simple-output
done

# 将SQL文件复制到指定目录
cp *.sql /path/to/target/directory/
```

### 示例3：指定输出目录，只要SQL文件
```bash
# 创建目标目录
mkdir -p /path/to/sql_output

# 进入目标目录
cd /path/to/sql_output

# 处理文件
python merge_kettle_sql.py /path/to/kettle/job.kjb --simple-output
```

## 🔧 实际案例

### 案例：用户需求"只要SQL文件"
**用户要求**：
- 提取 `C:\Users\13802\Desktop\DWS\MAINTENANCE` 目录下的Kettle作业
- 将SQL文件存放到 `C:\Users\13802\Desktop\DWS原sql提取\MAINTENANCE`
- 只要提取之后的SQL文件，不要其他东西

**解决方案**：
```bash
# 创建目标目录
mkdir -p "C:\Users\13802\Desktop\DWS原sql提取\MAINTENANCE"

# 进入目标目录
cd "C:\Users\13802\Desktop\DWS原sql提取\MAINTENANCE"

# 批量处理，只要SQL文件
for file in "C:\Users\13802\Desktop\DWS\MAINTENANCE"/*.kjb; do
    python merge_kettle_sql.py "$file" --simple-output
done
```

**结果**：
```
C:\Users\13802\Desktop\DWS原sql提取\MAINTENANCE\
├── job_DWS_ELEVATOR_MAINTENANCE_F_merged_detailed.sql
├── job_DWS_INQUIRY_REPORT_PR_HANDLE_merged_detailed.sql
├── job_DWS_MAINT_ITEM_BUSINESS_CLUES_F_merged_detailed.sql
└── job_DWS_REMAKE_WG_TARGET1_merged_detailed.sql
```

## 📝 最佳实践

### 1. **明确用户需求**
- 如果用户说"只要SQL文件"，就使用 `--simple-output`
- 如果用户需要分析报告，就使用完整模式

### 2. **简化文件管理**
- 使用 `--simple-output` 可以减少文件数量
- 便于版本控制（git add *.sql）
- 便于文件传输和共享

### 3. **批量处理策略**
```bash
# 推荐：逐个文件处理，保持输出简洁
for file in *.kjb; do
    python merge_kettle_sql.py "$file" --simple-output
done

# 不推荐：使用批量工具，会生成额外文件
python batch_extract_kettle_sql.py --dir /path/to/kettle/jobs
```

### 4. **文件命名规范**
- 简化模式下生成的文件名格式：`job_作业名称_merged_detailed.sql`
- 文件名清晰，便于识别原始Kettle作业

## ❓ 常见问题

### Q1：如何只获取SQL文件，不要其他文件？
A：使用 `--simple-output` 参数

### Q2：批量处理时如何只要SQL文件？
A：使用循环逐个处理文件，而不是使用批量工具

### Q3：生成的SQL文件包含什么内容？
A：包含从Kettle作业中提取的所有SQL组件，保持原样，未做任何修改

### Q4：如何将SQL文件保存到指定目录？
A：先进入目标目录，再执行提取命令

## 📊 总结

"只要SQL文件"是一个常见的用户需求，通过使用 `--simple-output` 参数可以完美满足这个需求。这个模式适用于：
- 日常SQL备份
- 脚本迁移
- 代码审查
- 版本控制
- 快速验证

**核心建议**：对于大多数日常使用场景，推荐使用 `--simple-output` 模式，输出简洁，便于管理。