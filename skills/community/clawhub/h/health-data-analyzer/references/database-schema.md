# 数据库表结构说明文档

## 用户与设备相关表

### users - 用户基础信息表
存储用户的基本信息和账户状态。核心字段包括：
- `id`: 用户唯一标识
- `external_id`: 外部系统用户ID
- `email`, `username`: 账户信息
- `age`, `gender`, `height`, `weight`: 用户生理信息
- `is_deleted`: 软删除标记

### user_data_sources - 用户数据源表
记录用户关联的健康数据来源设备。核心字段：
- `id`: 数据源唯一标识
- `user_id`: 关联用户ID
- `source_platform`: 数据平台（如 appleHealth）
- `source_name`: 设备名称（如 WHOOP、RingConn 健康、华为运动健康等）
- `source_device_id`: 设备唯一标识

---

## 原始数据表

### health_data_numeric - 原始多设备健康数据表
存储来自各个设备的原始数值型健康数据。核心字段：
- `user_id`: 用户ID
- `user_data_sources_id`: 数据源ID
- `type`: 数据类型
  - `HEART_RATE`: 心率
  - `STEPS`: 步数
  - `ACTIVE_ENERGY_BURNED`: 活动消耗
  - `BASAL_ENERGY_BURNED`: 基础代谢消耗
  - `BLOOD_OXYGEN`: 血氧
  - `RESPIRATORY_RATE`: 呼吸率
  - `SLEEP_LIGHT`: 浅睡
  - `SLEEP_DEEP`: 深睡
  - `SLEEP_REM`: 快速眼动睡眠
  - `SLEEP_AWAKE`: 清醒
  - `SLEEP_ASLEEP`: 睡眠
- `value`: 数值
- `unit`: 单位
- `date_from`, `date_to`: 数据时间范围（时间戳）
- `device_model`: 设备型号

### fusion_health_data_numeric - 融合健康数据表
多设备数据融合后的统一健康数据。核心字段：
- `user_id`: 用户ID
- `user_data_sources_id`: 融合设备数据源ID（通常指向"alloop融合设备"）
- `type`: 数据类型
  - `HEART_RATE`: 心率
  - `STEPS`: 步数
  - `BLOOD_OXYGEN`: 血氧
  - `RESPIRATORY_RATE`: 呼吸率
  - `HEART_RATE_VARIABILITY_SDNN`: 心率变异性
  - `BODY_TEMPERATURE`: 体温
  - `RESTING_HEART_RATE`: 静息心率
  - `APPLE_STAND_HOUR`: 站立小时数
- `value`, `unit`: 数值和单位
- `date_from`, `date_to`: 时间范围

### health_data_workout - 原始运动数据表
存储用户的运动锻炼记录。核心字段：
- `user_id`: 用户ID
- `user_data_sources_id`: 数据源ID
- `workout_activity_type`: 运动类型
  - `WALKING`: 步行
  - `RUNNING`: 跑步
  - `RUNNING_TREADMILL`: 跑步机跑步
  - `BIKING`: 骑行
  - `SWIMMING_POOL`: 游泳
  - `TRADITIONAL_STRENGTH_TRAINING`: 传统力量训练
  - `FUNCTIONAL_STRENGTH_TRAINING`: 功能性力量训练
  - `HIGH_INTENSITY_INTERVAL_TRAINING`: 高强度间歇训练
  - `STAIRS`: 爬楼梯
  - `OTHER`: 其他
- `date_from`, `date_to`: 运动时间范围
- `total_energy_burned`: 总消耗能量
- `total_distance`: 总距离
- `total_steps`: 总步数

---

## 分段数据表

### metrics_segments - 健康指标分段表
整合的恢复模块相关的独立健康指标数据。核心字段：
- `user_id`: 用户ID
- `user_data_sources_id`: 数据源ID
- `type`: 指标类型
  - `RESTING_HEART_RATE`: 静息心率
  - `HEART_RATE_VARIABILITY_SDNN`: 心率变异性
  - `BLOOD_OXYGEN`: 血氧
  - `RESPIRATORY_RATE`: 呼吸率
  - `BODY_TEMPERATURE`: 体温
  - `HEART_RATE`: 心率
- `value`, `unit`: 数值和单位
- `target_date`: 目标日期
- `date_from`, `date_to`: 数据时间范围

### sleep_segments - 睡眠分段表
汇总成一晚上的完整睡眠数据。核心字段：
- `user_id`: 用户ID
- `user_data_sources_id`: 数据源ID
- `type`: 睡眠类型
  - `PRIMARY`: 主睡眠
  - `NAP`: 小睡
- `sleep_date`: 睡眠日期
- `asleep_duration_minutes`: 总睡眠时长
- `deep_duration_minutes`: 深睡时长
- `light_duration_minutes`: 浅睡时长
- `rem_duration_minutes`: REM睡眠时长
- `awake_duration_minutes`: 清醒时长
- `in_bed_duration_minutes`: 在床时长
- `in_bed_start_ts`, `in_bed_end_ts`: 上床/下床时间戳
- `asleep_start_ts`, `asleep_end_ts`: 入睡/醒来时间戳
- `avg_hr`, `avg_hrv`, `avg_spo2`, `avg_rr`, `avg_temp`: 平均心率、心率变异性、血氧、呼吸率、体温
- `sleep_stages`: 睡眠分期详细数据（JSON）
- `data_quality_flag`: 数据质量标记
  - `normal`: 正常

### training_segments - 训练分段表
汇总成一次完整运动的训练数据。核心字段：
- `user_id`: 用户ID
- `user_data_sources_id`: 数据源ID
- `workout_id`: 关联的原始运动数据ID
- `calculation_id`: 关联的运动分数计算ID
- `workout_activity_type`: 运动类型（同 health_data_workout）
- `date_from`, `date_to`: 运动时间范围
- `duration`: 运动时长（分钟）
- `avg_hr`, `max_hr`, `min_hr`: 平均/最大/最小心率
- `user_max_hr`: 用户最大心率
- `rest_hr`: 静息心率
- `hr_zone`: 心率区间分布（JSON）
- `total_energy_burned`: 总消耗能量
- `total_distance`: 总距离
- `total_steps`: 总步数
- `event_load`: 运动负荷

---

## 分数计算表

### sleep_calculations - 睡眠分数表
计算用户的睡眠质量评分和建议。核心字段：
- `calculation_id`: 计算唯一标识
- `user_id`: 用户ID
- `user_data_sources_id`: 数据源ID
- `utc_ts`: 计算时间戳
- `overall_score`: 总体睡眠分数
- `sleep_vs_need_score`: 睡眠时长与需求匹配分数
- `sleep_efficiency_score`: 睡眠效率分数
- `sleep_consistency_score`: 睡眠一致性分数
- `restorative_sleep_score`: 恢复性睡眠分数（深睡+REM）
- `rem_sleep_score`: REM睡眠分数
- `deep_sleep_score`: 深睡分数
- `sleep_debt`: 睡眠债务（分钟）
- `current_sleep_needed_minutes`: 当前所需睡眠时长
- `next_sleep_needed_minutes`: 下次所需睡眠时长
- `personalized_baseline`: 个性化基线
- `time_asleep_baseline`: 睡眠时长基线
- 各项指标的 `_baseline`（基线值）和 `_optimal_range_min/max`（最优范围）

### strain_calculations - 运动负荷分数表
计算用户的运动负荷和活动评分。核心字段：
- `user_id`: 用户ID
- `user_data_sources_id`: 数据源ID
- `utc_ts`: 计算时间戳
- `overall_strain`: 总体负荷值
- `daily_load`: 每日负荷
- `acute_load`: 急性负荷（近期）
- `chronic_load`: 慢性负荷（长期）
- `acwr`: 急慢性负荷比（Acute:Chronic Workload Ratio）
- `strain_zone`: 负荷区间
- `activity_score`: 活动分数
- `basic_activity_score`: 基础活动分数
- `display_percentage`: 显示百分比
- `workout_count`: 运动次数
- `steps_count`: 步数
- `calories_count`: 卡路里消耗
- `move_hours_count`: 活动小时数
- `strength_activity_time_count`: 力量训练时长
- `activity_hr_zone`: 活动心率区间分布（JSON）
- `all_day_hr_zone`: 全天心率区间分布（JSON）
- 各项指标的 `_baseline`（基线值）和 `_optimal_min/max`（最优范围）

### recovery_calculations - 恢复分数表
计算用户的身体恢复状态评分。核心字段：
- `calculation_id`: 计算唯一标识
- `user_id`: 用户ID
- `user_data_sources_id`: 数据源ID
- `utc_ts`: 计算时间戳
- `overall_recovery`: 总体恢复分数
- `overall_z_score`: 总体Z分数
- `metrics_count`: 参与计算的指标数量
- `interpretation`: 恢复状态解释
- `warning`: 警告信息
- `optimal_range_min`, `optimal_range_max`: 最优范围

**HRV（心率变异性）相关**:
- `hrv`: 心率变异性值
- `hrv_score`: HRV分数
- `hrv_level`: HRV水平
- `hrv_baseline`: HRV基线
- `hrv_baseline_variance`: HRV基线方差
- `hrv_optimal_range_min/max`: HRV最优范围
- `hrv_details`: HRV详细信息（JSON）

**RHR（静息心率）相关**:
- `rhr`: 静息心率值
- `rhr_score`: RHR分数
- `rhr_level`: RHR水平
- `rhr_baseline`: RHR基线
- `rhr_baseline_variance`: RHR基线方差
- `rhr_optimal_range_min/max`: RHR最优范围
- `rhr_details`: RHR详细信息（JSON）

**RR（呼吸率）相关**:
- `rr`: 呼吸率值
- `rr_score`: RR分数
- `rr_level`: RR水平
- `rr_baseline`: RR基线
- `rr_baseline_variance`: RR基线方差
- `rr_optimal_range_min/max`: RR最优范围
- `rr_details`: RR详细信息（JSON）

**SPO2（血氧）相关**:
- `spo2`: 血氧值
- `spo2_score`: SPO2分数
- `spo2_level`: SPO2水平
- `spo2_baseline`: SPO2基线
- `spo2_baseline_variance`: SPO2基线方差
- `spo2_optimal_range_min/max`: SPO2最优范围
- `spo2_details`: SPO2详细信息（JSON）

**TEMP（体温）相关**:
- `temp`: 体温值
- `temp_score`: 体温分数
- `temp_level`: 体温水平
- `temp_baseline`: 体温基线
- `temp_baseline_variance`: 体温基线方差
- `temp_optimal_range_min/max`: 体温最优范围
- `temp_details`: 体温详细信息（JSON）

**睡眠分数相关**:
- `sleep_score_val`: 睡眠分数值
- `sleep_score`: 睡眠分数
- `sleep_score_baseline`: 睡眠分数基线
- `sleep_score_baseline_variance`: 睡眠分数基线方差
- `sleep_score_optimal_range_min/max`: 睡眠分数最优范围
- `sleep_details`: 睡眠详细信息（JSON）

---

## 数据流向关系

```
1. 原始数据采集
各设备数据 → health_data_numeric (原始数值数据)
各设备数据 → health_data_workout (原始运动数据)

2. 数据融合
多设备数据 → fusion_health_data_numeric (融合设备数据)

3. 指标提取
多设备数据/融合设备数据 → metrics_segments (独立健康指标)

4. 分段汇总
睡眠数据 → sleep_segments (一晚睡眠)
运动数据 → training_segments (一次运动)

5. 分数计算
sleep_segments → sleep_calculations (睡眠分数)
training_segments → strain_calculations (运动负荷分数)
metrics_segments + sleep_calculations → recovery_calculations (恢复分数)
```

## 时间字段说明

不同表使用不同的时间字段进行过滤：
- `users`, `user_data_sources`: 不过滤时间
- `health_data_numeric`, `fusion_health_data_numeric`: 使用 `date_from`/`date_to`（秒级时间戳）
- `sleep_segments`: 使用 `in_bed_end_ts`（下床时间戳）
- `sleep_calculations`, `strain_calculations`, `recovery_calculations`: 使用 `utc_ts`（计算时间戳）
- `health_data_workout`, `training_segments`: 使用 `date_from`/`date_to`（秒级时间戳）
- `metrics_segments`: 使用 `target_date`（日期字段）