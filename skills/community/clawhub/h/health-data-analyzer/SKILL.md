---
name: health-data-analyzer
description: 健康数据分析专家，通过 mcporter 访问 healthdata MCP 服务器进行睡眠、运动、恢复等健康数据的查询和分析。当用户询问健康数据、睡眠质量、运动表现、身体恢复状态、心率变异性、血氧水平等健康相关问题时使用此技能。支持多维度健康数据分析、趋势分析、个性化健康建议。
---

# 健康数据分析器

专业的健康数据分析工具，通过 MCP 服务器访问完整的健康数据库，提供睡眠、运动、恢复等多维度健康分析。

## 核心功能

- **睡眠分析**: 睡眠质量评分、睡眠分期分析、睡眠债务计算
- **运动分析**: 运动负荷评估、训练效果分析、心率区间分析  
- **恢复分析**: 身体恢复状态评估、HRV/RHR/血氧/体温综合分析
- **趋势分析**: 长期健康趋势、个性化基线对比
- **多设备融合**: 支持多设备数据融合分析

## 数据访问流程

### 标准三步流程

所有健康数据查询必须遵循以下三步流程：

1. **列出可用表** - 了解数据库结构
2. **获取表结构** - 理解字段定义
3. **查询数据** - 获取实际数据进行分析

### 基础命令

#### 1. 列出所有数据表
```bash
mcporter call healthdata.list_available_tables
```

#### 2. 获取表字段结构
```bash
mcporter call healthdata.get_table_schema table_list='["table1", "table2"]'
```

**参数格式**:
- `table_list`: JSON 数组格式，用单引号包围
- 示例: `table_list='["sleep_segments", "sleep_calculations"]'`

#### 3. 查询表数据
```bash
mcporter call healthdata.query_table_data table_name=TABLE_NAME start_date=YYYY-MM-DD end_date=YYYY-MM-DD conversation_time="YYYY-MM-DD HH:MM:SS"
```

**参数说明**:
- `table_name`: 要查询的表名
- `start_date`: 开始日期 (YYYY-MM-DD)
- `end_date`: 结束日期 (YYYY-MM-DD)  
- `conversation_time`: 当前对话时间，用引号包围

## 数据表概览

### 用户与设备表
- `users`: 用户基础信息
- `user_data_sources`: 数据源设备信息

### 原始数据表  
- `health_data_numeric`: 原始多设备健康数据
- `fusion_health_data_numeric`: 融合后统一健康数据
- `health_data_workout`: 原始运动数据

### 分段汇总表
- `sleep_segments`: 睡眠分段数据 (一晚完整睡眠)
- `training_segments`: 训练分段数据 (一次完整运动)
- `metrics_segments`: 健康指标分段数据

### 评分计算表
- `sleep_calculations`: 睡眠质量评分
- `strain_calculations`: 运动负荷评分  
- `recovery_calculations`: 身体恢复评分

## 分析工作流程

### 睡眠分析流程
1. 查询 `sleep_segments` 获取睡眠基础数据
2. 查询 `sleep_calculations` 获取睡眠评分
3. 结合数据进行睡眠质量分析和建议

### 运动分析流程  
1. 查询 `training_segments` 获取运动数据
2. 查询 `strain_calculations` 获取负荷评分
3. 分析运动表现和训练建议

### 恢复分析流程
1. 查询 `recovery_calculations` 获取恢复评分
2. 查询 `metrics_segments` 获取生理指标
3. 综合分析身体恢复状态

## 时间范围建议

- **短期分析**: 最近 7-14 天
- **趋势分析**: 最近 30-90 天  
- **基线对比**: 建议向前延伸时间范围以捕获更多历史数据

## 数据质量检查

- 检查 `data_quality_flag` 字段 (normal 为正常)
- 注意设备数据源的一致性
- 识别数据缺失或异常值

## 分析输出格式

### 基础数据摘要
- 数据时间范围和记录数量
- 数据质量状态
- 主要设备来源

### 核心指标分析
- 关键健康指标的当前值和趋势
- 与个人基线的对比
- 异常值识别和说明

### 个性化建议
- 基于数据分析的健康建议
- 改进方向和具体措施
- 需要关注的健康风险

## 常见查询模式

详细的查询模式和示例请参考 [references/query-patterns.md](references/query-patterns.md)

## 数据库架构

完整的数据库表结构和字段说明请参考 [references/database-schema.md](references/database-schema.md)

## 故障排除

如果 mcporter 命令失败：
1. 检查 healthdata 服务器状态: `mcporter list`
2. 验证参数格式，特别是数组和日期格式
3. 确认表名和字段名的正确性
4. 检查时间范围的合理性