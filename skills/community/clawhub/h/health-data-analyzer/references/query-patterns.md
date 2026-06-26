# 健康数据查询模式和示例

## 基础查询模式

### 1. 睡眠分析查询模式

#### 基础睡眠数据查询
```bash
# 第一步：列出表
mcporter call healthdata.list_available_tables

# 第二步：获取睡眠相关表结构
mcporter call healthdata.get_table_schema table_list='["sleep_segments", "sleep_calculations"]'

# 第三步：查询最近一周睡眠数据
mcporter call healthdata.query_table_data table_name=sleep_segments start_date=2026-02-27 end_date=2026-03-06 conversation_time="2026-03-06 01:00:00"

# 查询睡眠评分数据
mcporter call healthdata.query_table_data table_name=sleep_calculations start_date=2026-02-27 end_date=2026-03-06 conversation_time="2026-03-06 01:00:00"
```

#### 睡眠趋势分析（30天）
```bash
mcporter call healthdata.query_table_data table_name=sleep_segments start_date=2026-02-05 end_date=2026-03-06 conversation_time="2026-03-06 01:00:00"
```

### 2. 运动分析查询模式

#### 基础运动数据查询
```bash
# 获取运动相关表结构
mcporter call healthdata.get_table_schema table_list='["training_segments", "strain_calculations", "health_data_workout"]'

# 查询训练分段数据
mcporter call healthdata.query_table_data table_name=training_segments start_date=2026-02-27 end_date=2026-03-06 conversation_time="2026-03-06 01:00:00"

# 查询运动负荷评分
mcporter call healthdata.query_table_data table_name=strain_calculations start_date=2026-02-27 end_date=2026-03-06 conversation_time="2026-03-06 01:00:00"
```

#### 特定运动类型分析
```bash
# 查询原始运动数据（可按运动类型筛选）
mcporter call healthdata.query_table_data table_name=health_data_workout start_date=2026-02-27 end_date=2026-03-06 conversation_time="2026-03-06 01:00:00"
```

### 3. 恢复状态分析查询模式

#### 综合恢复分析
```bash
# 获取恢复相关表结构
mcporter call healthdata.get_table_schema table_list='["recovery_calculations", "metrics_segments"]'

# 查询恢复评分数据
mcporter call healthdata.query_table_data table_name=recovery_calculations start_date=2026-02-27 end_date=2026-03-06 conversation_time="2026-03-06 01:00:00"

# 查询健康指标数据
mcporter call healthdata.query_table_data table_name=metrics_segments start_date=2026-02-27 end_date=2026-03-06 conversation_time="2026-03-06 01:00:00"
```

### 4. 多维度健康分析查询模式

#### 完整健康画像
```bash
# 获取所有核心表结构
mcporter call healthdata.get_table_schema table_list='["users", "user_data_sources", "sleep_segments", "sleep_calculations", "recovery_calculations", "strain_calculations"]'

# 查询用户基础信息
mcporter call healthdata.query_table_data table_name=users start_date=2026-03-06 end_date=2026-03-06 conversation_time="2026-03-06 01:00:00"

# 查询数据源信息
mcporter call healthdata.query_table_data table_name=user_data_sources start_date=2026-03-06 end_date=2026-03-06 conversation_time="2026-03-06 01:00:00"
```

## 常见分析场景

### 场景1：睡眠质量评估
**用户问题**: "我最近的睡眠质量怎么样？"

**查询流程**:
1. 查询最近2周的 `sleep_segments` 数据
2. 查询对应的 `sleep_calculations` 评分数据
3. 分析睡眠时长、深睡比例、REM比例、睡眠效率等指标
4. 对比个人基线和最优范围

### 场景2：运动表现分析
**用户问题**: "我的运动强度是否合适？"

**查询流程**:
1. 查询最近1个月的 `training_segments` 数据
2. 查询对应的 `strain_calculations` 负荷数据
3. 分析运动频率、强度分布、心率区间
4. 评估急慢性负荷比（ACWR）

### 场景3：身体恢复状态
**用户问题**: "我的身体恢复状态如何？"

**查询流程**:
1. 查询最近1周的 `recovery_calculations` 数据
2. 查询对应的 `metrics_segments` 生理指标
3. 分析HRV、静息心率、血氧、体温等指标
4. 评估整体恢复水平和趋势

### 场景4：健康趋势分析
**用户问题**: "我的健康状况有什么变化趋势？"

**查询流程**:
1. 查询最近3个月的核心数据表
2. 计算各项指标的移动平均和趋势
3. 识别改善或恶化的指标
4. 提供个性化建议

## 数据解读要点

### 睡眠数据解读
- **睡眠效率**: (总睡眠时长 / 在床时长) × 100%，正常应 > 85%
- **深睡比例**: 深睡时长 / 总睡眠时长，正常约15-20%
- **REM比例**: REM时长 / 总睡眠时长，正常约20-25%
- **睡眠债务**: 负值表示睡眠不足，正值表示睡眠充足

### 运动数据解读
- **心率区间**: Zone 1-5 对应不同强度，Zone 2-3 适合日常训练
- **运动负荷**: 急慢性负荷比 0.8-1.3 为理想范围
- **恢复时间**: 高强度训练后需要充分恢复

### 恢复数据解读
- **HRV**: 心率变异性，数值越高通常表示恢复越好
- **静息心率**: 应保持稳定，持续升高可能表示疲劳或疾病
- **血氧饱和度**: 正常应 > 95%
- **体温**: 基线体温的变化可能反映恢复状态

## 时间范围建议

### 不同分析目的的时间范围
- **当前状态评估**: 最近3-7天
- **短期趋势分析**: 最近2-4周  
- **长期趋势分析**: 最近2-3个月
- **基线建立**: 最近6个月或更长

### 数据完整性考虑
- 优先选择数据完整的时间段
- 避免设备更换或数据缺失期间
- 考虑季节性因素对健康指标的影响

## 错误处理和数据验证

### 常见错误
1. **参数格式错误**: 检查日期格式和数组语法
2. **表名错误**: 确认表名拼写正确
3. **时间范围无效**: start_date 必须 <= end_date
4. **服务器离线**: 检查 healthdata 服务状态

### 数据质量检查
1. 检查 `data_quality_flag` 字段
2. 验证数据的时间连续性
3. 识别异常值和缺失值
4. 确认设备数据源的一致性

### 结果验证
1. 检查返回数据的记录数量
2. 验证时间范围是否符合预期
3. 确认关键字段不为空
4. 对比不同数据源的一致性