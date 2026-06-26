# 第一步：纯SQL提取指南

## 🎯 **核心原则**

**只提取，不修改，保持原样**

## 📋 **使用场景**

### ✅ **适用场景**：
1. 需要完整备份Kettle作业的SQL逻辑
2. 需要分析Kettle作业的历史迭代
3. 需要将SQL迁移到其他系统
4. 只需要查看和了解原有业务逻辑
5. **不打算立即优化或转换**

### ❌ **不适用场景**：
1. 需要立即转换为特定数据库语法
2. 需要删除历史备份组件
3. 需要优化执行顺序
4. 需要统一日期函数

## 🔧 **工具选择**

### 1. **单个文件提取**（推荐）
使用：`merge_kettle_sql.py`
```bash
# 基本用法
python merge_kettle_sql.py job.kjb

# 只生成详细SQL文件（最常用）
python merge_kettle_sql.py job.kjb --only-detailed

# 指定输出目录
python merge_kettle_sql.py job.kjb --output 我的提取结果
```

### 2. **批量文件提取**
使用：`batch_extract_kettle_sql.py`
```bash
# 处理多个文件
python batch_extract_kettle_sql.py --file job1.kjb job2.ktr

# 处理目录
python batch_extract_kettle_sql.py --dir /path/to/kettle/jobs

# 生成HTML报告
python batch_extract_kettle_sql.py --file job.kjb --output html报告
```

## 📊 **输出说明**

### **单个文件提取的输出**：
```
输出目录/
├── job_merged_detailed.sql          # 📝 详细SQL（核心文件）
├── job_executable.sql              # ⚡ 可执行SQL（带事务）
├── job_simple.sql                  # 🧹 简化SQL（无注释）
├── job_components.txt              # 📋 组件详情
└── job_analysis.json               # 📊 分析报告
```

### **批量提取的输出**：
```
输出目录/
├── batch_report.html               # 🌐 HTML可视化报告
├── batch_summary.json              # 📊 批处理统计
└── specified_files/                # 📁 每个文件的详细结果
    └── job/
        ├── basic_info.json
        ├── sql_components.json
        └── extracted_sql.txt
```

## ⚠️ **注意事项**

### 1. **备份组件保留**
- Kettle文件可能包含历史备份组件（如 `bak20250430`、`tmp`）
- **纯提取模式会保留这些组件**
- 如果不需要，请手动删除或使用优化模式

### 2. **日期函数原样保留**
- 可能包含 `now()`（PostgreSQL）或 `sysdate`（Oracle）
- **不会自动转换**
- 如果需要统一，请手动处理

### 3. **执行顺序保持原样**
- 按Kettle中的原始顺序
- **不会优化重组**
- 如果需要优化，请手动调整

## 🔍 **常见问题**

### Q1: 为什么提取的SQL中有备份组件？
**A**: Kettle原文件本身就包含这些组件，提取工具忠实地提取了所有内容。

### Q2: 为什么日期函数没有统一？
**A**: 纯提取模式保持原样，不做修改。如果需要统一，请使用优化模式或手动处理。

### Q3: 如何只保留最新版本，删除备份？
**A**: 有两个选择：
1. 使用优化模式（谨慎）：`--output-files detailed`
2. 手动编辑提取的SQL文件

### Q4: 提取后还需要做什么？
**A**: 根据需求：
1. **直接使用**：如果SQL已经是生产就绪的
2. **手动优化**：删除备份，统一函数，优化顺序
3. **转换为特定数据库**：使用其他工具或手动转换

## 🎯 **最佳实践**

### **推荐工作流**：
```
1. 纯提取所有SQL
   python merge_kettle_sql.py job.kjb --only-detailed

2. 查看和分析提取结果
   检查备份组件、日期函数、业务逻辑

3. 根据需求决定下一步：
   - 直接使用（如果已经满足需求）
   - 手动优化（删除备份，统一函数）
   - 转换为特定数据库语法（如果需要）
```

### **检查清单**：
- [ ] 确认所有业务逻辑都已提取
- [ ] 检查备份组件是否需要保留
- [ ] 验证日期函数的数据库兼容性
- [ ] 确认执行顺序符合业务需求
- [ ] 检查参数（如 `${W_MONTH_WID}`）是否正确

## 📞 **故障排除**

### **问题**：提取的SQL不完整
**解决**：
1. 检查Kettle文件是否有损坏
2. 查看提取工具的日志输出
3. 使用验证脚本检查完整性

### **问题**：有语法错误
**解决**：
1. 检查原始SQL在Kettle中是否能执行
2. 可能是XML转义问题，尝试修复工具

### **问题**：文件太大
**解决**：
1. Kettle文件可能包含多年历史
2. 考虑使用优化模式删除备份
3. 或手动清理不需要的组件

---

**最后更新**: 2026-03-30  
**核心原则**: ✅ 只提取，不修改，保持原样  
**工具定位**: ✅ 纯SQL提取，无数据库转换功能