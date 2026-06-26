# Kettle SQL Extractor

一个专业的Kettle ETL作业SQL提取工具，支持从Kettle作业（.kjb/.ktr）文件中提取SQL脚本，保持SQL原样不做任何修改。

## 📋 功能特性

### 核心功能
- **纯SQL提取**: 从Kettle XML文件中提取所有SQL组件，保持SQL原样
- **智能合并**: 将单个Kettle作业中的多个SQL组件合并为一个SQL文件
- **批量处理**: 支持批量提取多个Kettle作业，生成HTML可视化报告
- **简洁输出**: 使用 `--simple-output` 参数，只生成SQL文件，避免多余文件夹
- **跨平台支持**: 支持Linux、macOS和Windows系统

### 解决的关键问题
- ✅ **XML转义字符处理**: 自动处理 `&lt;`, `&gt;` 等XML特殊字符
- ✅ **SQL完整性保证**: 完整提取跨行SQL内容，正确处理CDATA标记
- ✅ **错误处理**: 单个文件错误不影响其他文件处理
- ✅ **性能优化**: 批量处理，平均1秒/文件的处理速度

## 🚀 快速开始

### 安装依赖
```bash
# 确保已安装Python 3.x
python3 --version

# 安装必要的Python库
pip install lxml beautifulsoup4
```

### 基本使用

#### 场景1：只要SQL文件（日常使用推荐）
```bash
# 单个文件提取
python scripts/merge_kettle_sql.py job.kjb --simple-output

# 批量处理
for file in *.kjb; do
    python scripts/merge_kettle_sql.py "$file" --simple-output
done
```

#### 场景2：需要完整分析报告
```bash
# 批量分析Kettle作业
python scripts/batch_extract_kettle_sql.py --dir /path/to/kettle/jobs --output 分析报告

# 查看HTML报告
open 分析报告/batch_report.html
```

## 📁 项目结构

```
kettle-sql-extractor/
├── SKILL.md                    # 技能核心配置文件
├── README.md                   # 项目详细说明文档
├── scripts/                    # 所有脚本文件
│   ├── merge_kettle_sql.py     # 核心合并工具
│   ├── batch_extract_kettle_sql.py # 批量提取工具
│   ├── kettle_xml_parser.py    # XML解析器
│   ├── extract_kettle_sql_simple.sh   # Linux简化提取脚本
│   ├── extract_kettle_sql_simple.bat  # Windows简化提取脚本
│   └── fix_kettle_extract.sh   # 修复脚本
├── docs/                       # 文档目录
│   ├── 只要SQL文件需求指南.md   # "只要SQL文件"需求专门指南
│   ├── QUICK_START.md          # 快速开始指南
│   ├── USAGE_EXAMPLES.md       # 使用示例
│   ├── MERGE_SQL_QUICKSTART.md # 合并SQL快速指南
│   ├── BATCH_EXTRACT_QUICKSTART.md # 批量提取快速指南
│   ├── COMPLETE_WORKFLOW.md    # 完整工作流程
│   ├── OPTIMIZATION_SUMMARY.md # 优化总结
│   ├── SKILL_STATUS_SUMMARY.md # 技能状态总结
│   └── troubleshooting_case_kettle_extract.md # 故障排除案例
└── ...
```

## 🔧 工具脚本说明

### 1. **merge_kettle_sql.py** (核心合并工具)
将单个Kettle作业中的多个SQL组件合并为一个SQL文件。

**常用参数**:
- `--simple-output`: 简化输出模式，只生成SQL文件
- `--batch`: 批量处理多个文件
- `--executable`: 生成可执行SQL（带事务控制）
- `--simple`: 生成简化SQL（只包含语句）

### 2. **batch_extract_kettle_sql.py** (批量提取工具)
批量提取多个Kettle作业中的SQL脚本，生成HTML报告。

**常用参数**:
- `--dir`: 指定目录，提取所有Kettle文件
- `--file`: 指定单个或多个文件
- `--list`: 从文件列表批量提取
- `--consolidate`: 生成合并的SQL文件

### 3. **简化提取脚本**
- `extract_kettle_sql_simple.sh`: Linux/Mac一键提取脚本
- `extract_kettle_sql_simple.bat`: Windows一键提取脚本

## 📊 使用场景

### 1. **SQL备份与迁移**
- 备份Kettle作业的业务逻辑
- 迁移SQL到其他数据库系统
- 文档化ETL流程

### 2. **代码分析与审查**
- 分析SQL组件依赖关系
- 审查业务逻辑完整性
- 识别潜在的性能问题

### 3. **批量处理与自动化**
- 批量提取多个作业的SQL
- 自动化文档生成
- 代码仓库管理

### 4. **只要SQL文件场景**
基于用户反馈的常见需求："我只要提取之后的sql文件，不要给我其他东西"

**解决方案**: 使用 `--simple-output` 参数
```bash
python scripts/merge_kettle_sql.py job.kjb --simple-output
```

## 📝 最佳实践

### 1. **备份原始文件**
```bash
cp -r /path/to/kettle/jobs /path/to/kettle/jobs_backup_$(date +%Y%m%d)
```

### 2. **逐步验证**
```bash
# 先测试单个文件
python scripts/merge_kettle_sql.py test.kjb --simple-output

# 检查输出
cat job_test_merged_detailed.sql

# 确认无误后批量处理
python scripts/merge_kettle_sql.py *.kjb --simple-output
```

### 3. **使用版本控制**
```bash
python scripts/merge_kettle_sql.py *.kjb --simple-output
git add *.sql
git commit -m "提取Kettle作业SQL: $(date)"
```

## 🎯 输出文件

### 简化输出模式（推荐）
```
当前目录/
├── job_作业名称1_merged_detailed.sql
├── job_作业名称2_merged_detailed.sql
└── job_作业名称3_merged_detailed.sql
```

### 完整分析报告模式
```
batch_kettle_analysis/
├── batch_report.html              # HTML可视化报告
├── batch_summary.json             # JSON格式总结
├── batch_summary.txt              # 文本格式总结
└── kettle_files/                  # 单个文件分析结果
    ├── job1_kjb/
    │   ├── basic_info.json       # 基本信息
    │   ├── sql_components.json   # SQL组件列表
    │   └── extracted_sql.txt     # 提取的SQL
    └── job2_ktr/
        └── ...
```

## 🔍 故障排除

### 常见问题1：SQL提取不完整
**症状**: 提取的SQL内容被截断
**解决**: 工具内置了XML字符处理功能

### 常见问题2：特殊字符问题
**症状**: SQL中包含 `&lt;`, `&gt;` 等字符
**解决**: 工具自动处理XML转义字符

### 常见问题3：文件格式问题
**症状**: 无法解析.kjb或.ktr文件
**解决**: 检查文件是否为有效的Kettle XML格式

## 📈 性能指标

基于实际生产测试验证：
- ✅ **处理速度**: 平均1秒/文件
- ✅ **成功率**: 100%（26个文件测试）
- ✅ **SQL组件**: 最多处理过14个SQL组件的复杂作业
- ✅ **输出质量**: 保持SQL原样，格式规范

## 📄 许可证

本项目遵循开源许可证。详细信息请查看LICENSE文件。

## 🤝 贡献

欢迎提交Issue和Pull Request来改进这个工具。

## 📞 支持

如有问题，请查看：
- [故障排除文档](docs/troubleshooting_case_kettle_extract.md)
- [使用示例](docs/USAGE_EXAMPLES.md)
- [快速开始指南](docs/QUICK_START.md)

---

**核心原则**: **只提取，不修改** - 保持SQL原样，不做优化、转换或重组