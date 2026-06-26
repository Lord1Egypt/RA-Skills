---
name: kettle-sql-extractor
slug: kettle-sql-extractor
version: 2.1.0
changelog: |
  v2.1.0 (2026-04-03):
  - **新增用户需求总结**：基于用户反馈，明确记录"只要SQL文件"的常见需求
  - **强调简化输出模式**：在文档中突出 `--simple-output` 参数的重要性
  - **使用场景补充**：添加"仅需SQL文件"的使用场景说明
  - **最佳实践更新**：明确推荐简化输出模式作为默认选择
  
  v2.0.0 (2026-03-31):
  - **重构为纯SQL提取工具**：移除所有数据库转换模板和规范
  - **简化核心功能**：专注于Kettle SQL提取，不包含任何转换逻辑
  - **文件清理**：删除config、templates、logs等无关目录
  - **技能重命名**：从"kettle-to-starrocks"重命名为"kettle-sql-extractor"
  
  v1.6.0 (2026-03-30):
  - **新增简化输出模式**：基于用户反馈，添加 `--simple-output` 参数
  - **解决文件夹过多问题**：简化输出模式下直接在当前目录生成SQL文件
  - **用户需求精准满足**：支持"一个作业一个SQL文件，不要多余文件夹"的需求
  
  v1.5.0 (2026-03-30):
  - **重要澄清**：基于用户反馈，明确区分"纯提取模式"和"优化转换模式"
  - **用户需求明确化**：记录核心需求"不需要对原始的sql文件进行任何修改，只需要提取出来总结成一个sql脚本"
  - **技能结构调整**：强调默认行为应为纯提取
  
  v1.4.0 (2026-03-30):
  - 优化：简化输出产物，可根据用户需求只保留核心文件
  - 优化：改进批量处理流程，减少不必要的中间文件
  - 新增：实际生产测试验证，确保功能稳定可靠
  
  v1.3.0 (2026-03-30):
  - 新增：合并单个Kettle作业中多个SQL组件为一个SQL脚本的功能
  - 新增：merge_kettle_sql.py - 智能合并SQL，保持执行顺序
  - 新增：SQL依赖关系分析，自动建议执行顺序
  
  v1.2.0 (2026-03-30):
  - 新增：批量提取多个Kettle作业中SQL脚本的功能
  - 新增：batch_extract_kettle_sql.py - 支持批量处理目录和文件列表
  - 新增：HTML报告生成，可视化展示提取结果
  
  v1.1.0 (2026-03-27):
  - 新增：完整的Kettle SQL提取解决方案，解决XML转义和截断问题
  - 新增：字段完整性验证和业务逻辑保持机制
  - 新增：复杂Kettle作业结构分析方法
  
  v1.0.0 (2026-03-27):
  - 初始版本：Kettle作业SQL提取基础功能
homepage: https://clawhub.com/skills/kettle-sql-extractor
description: 从Kettle作业（.kjb/.ktr）中提取SQL脚本，支持批量提取、合并SQL组件和简洁输出
metadata: {"clawdbot":{"emoji":"📊","requires":{"anyBins":["kettle","pan","kitchen","python3"]},"os":["linux","darwin","win32"]}}
---

# Kettle SQL提取工具

从Kettle ETL作业中提取SQL脚本，支持批量处理和智能合并。

## 🎯 核心功能

### 1. **纯SQL提取**
- 从Kettle XML文件中提取所有SQL组件
- 保持SQL原样，不做任何修改
- 支持.kjb（作业）和.ktr（转换）文件

### 2. **智能合并**
- 将单个Kettle作业中的多个SQL组件合并为一个SQL文件
- 保持SQL执行顺序
- 分析SQL依赖关系

### 3. **批量处理**
- 支持批量提取多个Kettle作业
- 生成HTML可视化报告
- 统计分析SQL组件信息

### 4. **简洁输出**
- 使用`--simple-output`参数，避免多余文件夹
- 直接在当前目录生成SQL文件
- 每个Kettle作业对应一个SQL文件

### 5. **只要SQL文件模式**
- **常见用户需求**：很多用户只需要提取后的SQL文件，不需要HTML报告、JSON总结等额外文件
- **解决方案**：使用 `--simple-output` 参数，只生成SQL文件
- **典型场景**：备份SQL、迁移脚本、代码审查等场景
- **优势**：输出简洁，文件结构清晰，便于版本控制和直接使用

## 📋 使用说明

### 核心原则
**只提取，不修改** - 保持SQL原样，不做优化、转换或重组

### 常见需求场景

#### 🎯 **场景1：只要SQL文件**
**用户需求**：只需要提取后的SQL文件，不需要HTML报告、JSON总结等额外文件
**解决方案**：使用 `--simple-output` 参数
**典型场景**：SQL备份、脚本迁移、代码审查、版本控制
```bash
# 单个文件，只要SQL文件
python merge_kettle_sql.py job.kjb --simple-output

# 批量处理，只要SQL文件
for file in *.kjb; do python merge_kettle_sql.py "$file" --simple-output; done
```

#### 📊 **场景2：需要完整分析报告**
**用户需求**：需要详细的HTML报告和统计分析
**解决方案**：使用 `batch_extract_kettle_sql.py` 工具
**典型场景**：项目分析、文档生成、团队分享
```bash
# 生成完整分析报告
python batch_extract_kettle_sql.py --dir /path/to/kettle/jobs --output 分析报告
```

### 使用步骤

#### 1. **基本用法（单个文件）**
```bash
# 提取单个Kettle作业中的SQL
python merge_kettle_sql.py job.kjb

# 简化输出模式（推荐，只要SQL文件）
python merge_kettle_sql.py job.kjb --simple-output
```

#### 2. **批量处理（多个文件）**
```bash
# 批量提取目录中所有Kettle作业
python batch_extract_kettle_sql.py --dir /path/to/kettle/jobs

# 批量处理指定文件
python batch_extract_kettle_sql.py --file job1.kjb job2.ktr
```

#### 3. **输出控制**
```bash
# 指定输出目录
python merge_kettle_sql.py job.kjb --output 提取结果

# 批量处理并生成HTML报告
python batch_extract_kettle_sql.py --dir /path/to/kettle/jobs --output 分析报告
```

## 📁 输出文件

### 模式1：只要SQL文件（推荐用于日常使用）
**使用参数**: `--simple-output`
**适用场景**: SQL备份、脚本迁移、代码审查、版本控制
```
当前目录/
├── job_作业名称1_merged_detailed.sql
├── job_作业名称2_merged_detailed.sql
└── job_作业名称3_merged_detailed.sql
```

**特点**：
- ✅ 只生成SQL文件，没有额外文件
- ✅ 每个Kettle作业对应一个SQL文件
- ✅ 文件结构简洁，便于管理
- ✅ 适用于大多数日常使用场景

### 模式2：完整分析报告
**使用参数**: `--output 分析报告`
**适用场景**: 项目分析、文档生成、团队分享、审计检查
```
batch_kettle_analysis/
├── batch_report.html              # 📊 HTML可视化报告
├── batch_summary.json             # 📋 JSON格式总结
├── batch_summary.txt              # 📝 文本格式总结
└── kettle_files/                  # 📂 单个文件分析结果
    ├── job1_kjb/
    │   ├── basic_info.json       # 🔍 基本信息
    │   ├── sql_components.json   # 📊 SQL组件列表
    │   └── extracted_sql.txt     # 📄 提取的SQL
    └── job2_ktr/
        └── ...
```

**特点**：
- 📊 提供HTML可视化报告
- 📋 包含详细的JSON和文本总结
- 🔍 每个文件的详细分析结果
- 🎯 适合需要全面分析的项目场景

## 🔧 工具脚本

### 1. **scripts/merge_kettle_sql.py**（核心合并工具）
将单个Kettle作业中的多个SQL组件合并为一个SQL文件

```bash
# 基本用法：合并SQL
python scripts/merge_kettle_sql.py job.kjb

# 简化输出：在当前目录生成SQL文件
python scripts/merge_kettle_sql.py job.kjb --simple-output

# 批量处理多个文件
python scripts/merge_kettle_sql.py *.kjb --batch

# 生成可执行SQL（带事务控制）
python scripts/merge_kettle_sql.py job.kjb --executable

# 生成简化SQL（只包含语句）
python scripts/merge_kettle_sql.py job.kjb --simple
```

**输出文件**：
- `job_名称_merged_detailed.sql` - 详细合并SQL（带注释和分析）
- `job_名称_executable.sql` - 可执行SQL（带事务控制）
- `job_名称_simple.sql` - 简化SQL（只包含语句）

### 2. **scripts/batch_extract_kettle_sql.py**（批量提取工具）
批量提取多个Kettle作业中的SQL脚本

```bash
# 批量提取目录中所有文件
python scripts/batch_extract_kettle_sql.py --dir /path/to/kettle/jobs

# 批量提取指定文件
python scripts/batch_extract_kettle_sql.py --file job1.kjb job2.ktr

# 从文件列表批量提取
echo "/path/to/job1.kjb" > kettle_files.txt
echo "/path/to/job2.ktr" >> kettle_files.txt
python scripts/batch_extract_kettle_sql.py --list kettle_files.txt

# 生成合并的SQL文件便于查看
python scripts/batch_extract_kettle_sql.py --dir /path/to/kettle/jobs --consolidate
```

### 3. **scripts/kettle_xml_parser.py**（核心解析器）
XML解析模块，解决SQL提取的常见问题：
- XML特殊字符处理（&lt;, &gt;等）
- SQL内容跨行匹配
- CDATA标记清理

### 4. **scripts/extract_kettle_sql_simple.sh**（简化提取脚本）
一键提取脚本，专门满足"只要SQL文件"的需求：
```bash
# 使用方法
./scripts/extract_kettle_sql_simple.sh <源目录> <目标目录>

# 示例
./scripts/extract_kettle_sql_simple.sh "/path/to/kettle/jobs" "/path/to/sql/output"
```

### 5. **scripts/extract_kettle_sql_simple.bat**（Windows简化提取脚本）
Windows版本的一键提取脚本：
```batch
REM 使用方法
scripts\extract_kettle_sql_simple.bat <源目录> <目标目录>

REM 示例
scripts\extract_kettle_sql_simple.bat "C:\Users\13802\Desktop\DWS\MAINTENANCE" "C:\Users\13802\Desktop\DWS原sql提取\MAINTENANCE"
```

## 📊 功能特点

### 1. **完整性保证**
- ✅ 解决XML转义字符问题
- ✅ 完整提取跨行SQL内容
- ✅ 正确处理CDATA标记

### 2. **错误处理**
- ✅ 单个文件错误不影响其他文件处理
- ✅ 友好的错误提示
- ✅ 详细的提取日志

### 3. **性能优化**
- ✅ 批量处理，提高效率
- ✅ 内存使用优化
- ✅ 处理速度快（平均1秒/文件）

### 4. **用户体验**
- ✅ HTML可视化报告
- ✅ 简洁的命令行界面
- ✅ 灵活的输出控制

## 📈 使用场景

### 1. **SQL备份与迁移**（推荐使用`--simple-output`模式）
- 备份Kettle作业的业务逻辑
- 迁移SQL到其他数据库系统
- 文档化ETL流程
- **特点**: 只需要SQL文件，便于存储和迁移

### 2. **代码分析与审查**
- 分析SQL组件依赖关系
- 审查业务逻辑完整性
- 识别潜在的性能问题
- **特点**: 可以使用简化模式或完整报告模式

### 3. **批量处理与自动化**
- 批量提取多个作业的SQL
- 自动化文档生成
- 代码仓库管理
- **特点**: 推荐使用`--simple-output`模式，便于自动化脚本处理

### 4. **故障排查与调试**
- 快速定位SQL提取问题
- 分析Kettle作业结构
- 验证字段完整性
- **特点**: 可能需要完整报告模式进行深度分析

### 5. **只要SQL文件场景**
- **典型需求**: "我只要提取之后的sql文件，不要给我其他东西"
- **解决方案**: 使用 `--simple-output` 参数
- **应用场景**:
  - 日常SQL备份：只需要SQL脚本，不需要分析报告
  - 脚本迁移：将SQL迁移到其他系统或版本控制
  - 代码审查：直接查看SQL内容，不需要额外文件
  - 快速验证：快速获取SQL进行验证测试
- **优势**:
  - 输出简洁，只有一个SQL文件
  - 便于文件管理和版本控制
  - 减少不必要的文件存储
  - 符合大多数用户的日常需求

## 🚀 快速开始

### 安装依赖
```bash
# 确保已安装Python 3.x
python3 --version

# 安装必要的Python库
pip install lxml beautifulsoup4
```

### 基本使用示例
```bash
# 1. 准备输出目录
mkdir -p /path/to/output
cd /path/to/output

# 2. 提取SQL（简化模式）
python scripts/merge_kettle_sql.py /path/to/kettle/job.kjb --simple-output

# 3. 验证结果
ls -la *.sql
head -20 job_*.sql
```

### 批量处理示例
```bash
# 1. 批量分析Kettle作业
python scripts/batch_extract_kettle_sql.py --dir /path/to/kettle/jobs --output 批量分析

# 2. 查看HTML报告
open 批量分析/batch_report.html

# 3. 批量合并SQL
cd /path/to/output
python scripts/merge_kettle_sql.py /path/to/kettle/jobs/*.kjb --simple-output
```

## 🔍 故障排除

### 常见问题1：SQL提取不完整
**症状**：提取的SQL内容被截断
**解决**：使用内置的XML字符处理功能

### 常见问题2：特殊字符问题
**症状**：SQL中包含`&lt;`, `&gt;`等字符
**解决**：工具自动处理XML转义字符

### 常见问题3：文件格式问题
**症状**：无法解析.kjb或.ktr文件
**解决**：检查文件是否为有效的Kettle XML格式

## 📝 最佳实践

### 1. **根据需求选择模式**
```bash
# 场景1：只要SQL文件（日常使用推荐）
python scripts/merge_kettle_sql.py job.kjb --simple-output

# 场景2：需要完整分析报告（项目分析使用）
python scripts/batch_extract_kettle_sql.py --dir /path/to/kettle/jobs --output 分析报告
```

### 2. **备份原始文件**
```bash
# 处理前备份原始Kettle文件
cp -r /path/to/kettle/jobs /path/to/kettle/jobs_backup_$(date +%Y%m%d)
```

### 3. **逐步验证**
```bash
# 先测试单个文件
python scripts/merge_kettle_sql.py test.kjb --simple-output

# 检查输出
cat job_test_merged_detailed.sql

# 确认无误后批量处理
python scripts/merge_kettle_sql.py *.kjb --simple-output
```

### 4. **使用版本控制**
```bash
# 将提取的SQL纳入版本控制（使用简化输出模式）
python scripts/merge_kettle_sql.py *.kjb --simple-output
git add *.sql
git commit -m "提取Kettle作业SQL: $(date)"
```

### 5. **定期清理**
```bash
# 清理旧的批处理结果
find . -name "batch_*" -type d -mtime +7 -exec rm -rf {} \;
```

### 6. **"只要SQL文件"的最佳实践**
- **默认使用简化模式**: 日常使用推荐 `--simple-output` 参数
- **明确需求**: 如果用户明确说"只要SQL文件"，就使用简化模式
- **文件命名清晰**: 简化模式下生成的SQL文件名称清晰，便于识别
- **批量处理策略**: 对于批量处理，可以循环使用简化模式
```bash
# 批量处理，只要SQL文件
for file in *.kjb; do
    echo "处理: $file"
    python scripts/merge_kettle_sql.py "$file" --simple-output
done

# 复制SQL文件到目标目录
cp *.sql /path/to/target/directory/
```

## 📚 相关文件

### 文档文件 (位于 `docs/` 目录)
- **docs/第一步_纯SQL提取指南.md** - 纯提取模式详细说明
- **docs/troubleshooting_case_kettle_extract.md** - 故障排除案例
- **docs/只要SQL文件需求指南.md** - 专门针对"只要SQL文件"需求的使用指南

### 使用指南 (位于 `docs/` 目录)
- **docs/QUICK_START.md** - 快速开始指南
- **docs/USAGE_EXAMPLES.md** - 使用示例
- **docs/MERGE_SQL_QUICKSTART.md** - 合并SQL快速指南
- **docs/BATCH_EXTRACT_QUICKSTART.md** - 批量提取快速指南

### 总结报告 (位于 `docs/` 目录)
- **docs/OPTIMIZATION_SUMMARY.md** - 优化总结
- **docs/SKILL_STATUS_SUMMARY.md** - 技能状态总结
- **docs/COMPLETE_WORKFLOW.md** - 完整工作流程

## 📈 技能验证

基于实际生产测试验证：
- ✅ **处理速度**：平均1秒/文件
- ✅ **成功率**：100%（26个文件测试）
- ✅ **SQL组件**：最多处理过14个SQL组件的复杂作业
- ✅ **输出质量**：保持SQL原样，格式规范

## 📌 "只要SQL文件"需求总结

### 需求背景
基于用户反馈，很多用户在使用Kettle SQL提取工具时有一个明确的需求：
**"我只要提取之后的sql文件，不要给我其他东西"**

### 解决方案
使用 `--simple-output` 参数可以完美满足这个需求：
```bash
# 单个文件
python scripts/merge_kettle_sql.py job.kjb --simple-output

# 批量处理
for file in *.kjb; do
    python scripts/merge_kettle_sql.py "$file" --simple-output
done
```

### 典型使用场景
1. **SQL备份**：只需要SQL脚本进行备份
2. **脚本迁移**：将SQL迁移到其他系统
3. **代码审查**：直接查看SQL内容
4. **版本控制**：将SQL纳入git管理
5. **日常维护**：快速获取SQL进行验证

### 文件输出对比
- **简化模式**（使用 `--simple-output`）：只生成SQL文件
- **完整模式**（不使用 `--simple-output`）：生成HTML报告、JSON总结等额外文件

### 最佳实践建议
- 对于日常使用，推荐使用 `--simple-output` 模式
- 如果用户明确说"只要SQL文件"，就使用简化模式
- 对于项目分析和文档生成，可以使用完整模式

## 🔄 后续计划

### 短期优化
- 添加进度条显示
- 支持更多输出格式
- 改进错误提示信息

### 长期规划
- 支持自定义提取规则
- 集成到CI/CD流程
- 添加API接口

### "只要SQL文件"优化
- 进一步简化输出格式
- 提供更多的批量处理选项
- 优化文件命名规则

---

**注意**：此工具专注于SQL提取功能，不包含任何数据库特定的转换逻辑。提取的SQL保持原样，适用于各种数据库系统。

**重要提醒**：如果用户的需求是"只要SQL文件"，请使用 `--simple-output` 参数，这是满足这个需求的最直接方式。