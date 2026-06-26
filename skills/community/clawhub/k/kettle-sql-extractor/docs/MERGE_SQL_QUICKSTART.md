# Kettle SQL合并功能 - 快速入门

## 🎯 一句话总结
`merge_kettle_sql.py` 将**一个Kettle作业中的多个SQL组件合并成一个SQL脚本**，支持智能依赖分析和多种输出格式。

## 📋 核心功能
- ✅ **智能合并**：分析SQL依赖关系，保持正确执行顺序
- ✅ **多种输出**：详细版、可执行版、简化版三种SQL格式
- ✅ **事务支持**：生成包含事务控制的SQL，适合生产环境
- ✅ **批量处理**：一次处理多个Kettle作业
- ✅ **详细分析**：自动生成SQL组件分析报告

## 🚀 快速开始

### 基本用法（最简单）
```bash
# 1. 合并一个Kettle作业的所有SQL
python merge_kettle_sql.py 你的作业.kjb

# 2. 查看生成的SQL文件
ls merged_kettle_sql/你的作业/
```

### 常用命令速查
```bash
# 合并单个文件（默认输出到 merged_kettle_sql/）
python merge_kettle_sql.py job.kjb

# 生成简化的SQL（只包含语句，无注释）
python merge_kettle_sql.py job.kjb --simple

# 生成可执行的SQL（带事务控制）
python merge_kettle_sql.py job.kjb --executable

# 批量处理多个文件
python merge_kettle_sql.py job1.kjb job2.ktr --batch

# 指定输出目录
python merge_kettle_sql.py job.kjb --output 我的输出目录
```

## 📁 输出文件说明

处理一个Kettle作业后，你会得到5个文件：

### 1. **详细合并SQL** (`作业名_merged_detailed.sql`)
- 包含完整的注释和分析
- 显示每个SQL组件的信息
- 包含依赖关系和执行顺序建议
- **用途**：查看完整的合并过程和SQL结构

### 2. **可执行SQL** (`作业名_executable.sql`)
- 包含事务控制（BEGIN/COMMIT/ROLLBACK）
- 适合在生产数据库直接执行
- 包含错误处理建议
- **用途**：在生产环境执行

### 3. **简化SQL** (`作业名_simple.sql`)
- 只包含SQL语句，无额外注释
- 用简单的分隔线分开每个组件
- **用途**：快速查看SQL内容，或作为其他脚本的输入

### 4. **组件信息** (`作业名_components.txt`)
- 列出所有SQL组件的详细信息
- 包括类型、表、长度等
- **用途**：了解作业的SQL组成

### 5. **分析报告** (`作业名_analysis.json`)
- JSON格式的详细分析数据
- 包含依赖关系、表使用情况等
- **用途**：程序化处理或进一步分析

## 🔍 快速查看结果

```bash
# 1. 查看生成的SQL（简化版）
cat merged_kettle_sql/作业名/作业名_simple.sql

# 2. 查看可执行SQL（带事务控制）
cat merged_kettle_sql/作业名/作业名_executable.sql

# 3. 查看组件信息
cat merged_kettle_sql/作业名/作业名_components.txt

# 4. 查看有多少个SQL组件
grep "SQL组件数" merged_kettle_sql/作业名/作业名_components.txt
```

## 💡 使用场景示例

### 场景1：快速合并Kettle作业
```bash
# 假设你有一个DWH_ORDER.kjb文件
python merge_kettle_sql.py DWH_ORDER.kjb

# 查看结果
ls merged_kettle_sql/DWH_ORDER/
# DWH_ORDER_merged_detailed.sql
# DWH_ORDER_executable.sql
# DWH_ORDER_simple.sql
# DWH_ORDER_components.txt
# DWH_ORDER_analysis.json
```

### 场景2：生成可直接执行的SQL
```bash
# 生成带事务控制的SQL
python merge_kettle_sql.py 生产作业.kjb --executable

# 在数据库执行（示例，根据你的数据库调整）
# sqlcmd -S 服务器名 -d 数据库名 -i merged_kettle_sql/生产作业/生产作业_executable.sql
```

### 场景3：批量处理多个作业
```bash
# 批量处理所有.kjb文件
python merge_kettle_sql.py *.kjb --batch

# 查看批处理总结
cat merged_kettle_sql/batch_summary.txt
```

### 场景4：作为转换流程的一部分
```bash
# 1. 合并Kettle SQL
python merge_kettle_sql.py kettle_job.kjb --simple

# 2. 进一步处理
python convert_to_starrocks.py merged_kettle_sql/kettle_job/kettle_job_simple.sql

# 3. 执行转换后的SQL
# starrocks-client -e "source converted_starrocks.sql"
```

## 🐛 常见问题

### Q1: 合并后的SQL执行顺序正确吗？
**A**: 工具会自动分析表依赖关系，建议最优执行顺序。例如：
- 先创建表，再插入数据
- 先创建基础表，再创建引用它的表
- 在详细合并SQL中有依赖分析报告

### Q2: 事务控制是否必要？
**A**: 取决于使用场景：
- **开发测试**：可以使用简化版 (`--simple`)
- **生产环境**：建议使用可执行版 (`--executable`)，包含事务控制
- **数据迁移**：建议使用可执行版，确保数据一致性

### Q3: 如何处理复杂的Kettle作业？
**A**: 工具支持：
- 包含多个SQL组件的复杂作业
- 嵌套SQL、CTE、子查询等
- 跨多个表的复杂依赖关系
如果遇到问题，查看 `作业名_analysis.json` 中的详细分析。

### Q4: 输出文件太多怎么办？
**A**: 你可以选择只生成需要的文件：
```bash
# 只生成简化SQL
python merge_kettle_sql.py job.kjb --simple
# 然后手动复制需要的文件

# 或者使用专门的输出目录
python merge_kettle_sql.py job.kjb --output 专门目录
```

## 🚀 生产环境使用建议

### 最佳实践1：测试后再生产
```bash
# 1. 测试环境生成可执行SQL
python merge_kettle_sql.py 生产作业.kjb --executable --output 测试输出

# 2. 在测试数据库执行
# 执行测试输出/生产作业/生产作业_executable.sql

# 3. 验证无误后，在生产环境使用
```

### 最佳实践2：版本控制
```bash
# 将生成的SQL纳入版本控制
git add merged_kettle_sql/重要作业/重要作业_executable.sql
git commit -m "添加重要作业的合并SQL"
```

### 最佳实践3：集成到CI/CD
```yaml
# GitLab CI示例
merge_kettle_sql:
  stage: merge
  script:
    - python merge_kettle_sql.py src/*.kjb --batch --output artifacts/merged_sql
  artifacts:
    paths:
      - artifacts/merged_sql/
```

## 📞 获取帮助

```bash
# 查看完整帮助
python merge_kettle_sql.py --help

# 查看使用示例
python merge_kettle_sql.py --help | tail -20

# 查看版本信息
grep "version" SKILL.md | head -1
```

## 🎯 下一步

合并SQL后，你可以：
1. **直接执行**：使用可执行SQL在生产环境运行
2. **进一步处理**：将提取的SQL用于特定需求
3. **代码审查**：查看合并后的SQL，进行优化
4. **文档生成**：基于分析报告生成技术文档

---
**提示**: 合并功能是Kettle迁移的关键步骤，确保SQL逻辑正确且执行顺序合理！