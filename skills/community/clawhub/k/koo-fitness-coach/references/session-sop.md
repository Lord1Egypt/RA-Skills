# 课程 SOP

## 首次评估课（60-90 分钟）
- [ ] 5' 了解来意、运动史、目标
- [ ] 10' PAR-Q+ 签署 + 风险告知
- [ ] 20' 体测 + 动作筛查（记录基线，见 assessment.md）
- [ ] 10' 目标设定（SMART）与计划方向沟通
- [ ] 15' 动作体验（低强度，评估动作学习能力）
- [ ] 5' 总结：评估结论、分级、后续计划安排

## 备课检查清单
- [ ] 上次训练记录已回顾（负荷、RPE、反馈）
- [ ] 本次目标动作、组数、负荷/%1RM/RPE 已确定
- [ ] 退阶 / 进阶备选动作已准备
- [ ] 客户反馈（疼痛 / 疲劳 / 睡眠）已确认
- [ ] 大重量主项的保护安排已确认

## 训练日志模板
日期：
- 主项：动作 | 组×次 | 负荷 | %1RM/RPE | RIR | 备注
- 辅助：……
- 有氧/体能：……
- 客户反馈：睡眠 / 疲劳度 / 疼痛（部位+评分 0-10）
- 下次调整：

## 跟进节奏
- 每次课后：更新日志
- 每 4 周：复测体测指标，对比基线；检查计划执行率
- 每 12 周：全面评估，更新长期目标与专项方向

## 数据结构化（用于小程序 / 表格 / 系统化记录）

训练日志如需落库，建议使用以下字段结构：

**会员 member**
| 字段 | 类型 | 说明 |
|---|---|---|
| member_id | string | 主键 |
| name | string | 姓名 |
| sex | enum | M/F |
| birth_year | int | 出生年 |
| height_cm | float | 身高 |
| level | enum | novice / intermediate / advanced |
| goals | string[] | 增肌/减脂/力量/体能 |
| parq_flags | string[] | PAR-Q+ 阳性项 |
| consent_signed_at | datetime | 知情同意书签署时间 |

**训练记录 session**
| 字段 | 类型 | 说明 |
|---|---|---|
| session_id | string | 主键 |
| member_id | string | 外键 |
| date | date | 训练日期 |
| duration_min | int | 时长 |
| rpe_session | float | 本次课整体 RPE |
| note | string | 备注 |

**组记录 set_log**
| 字段 | 类型 | 说明 |
|---|---|---|
| set_id | string | 主键 |
| session_id | string | 外键 |
| exercise_id | string | 动作 ID（对应动作库） |
| set_index | int | 第几组 |
| reps | int | 次数 |
| load_kg | float | 负荷 |
| pct_1rm | float | %1RM（可空） |
| rpe | float | 本组 RPE（可空） |
| rir | int | 剩余次数（可空） |
| is_warmup | bool | 是否热身组 |

**体测记录 measurement**
| 字段 | 类型 | 说明 |
|---|---|---|
| measure_id | string | 主键 |
| member_id | string | 外键 |
| date | date | 测量日期 |
| weight_kg | float | 体重 |
| waist_cm | float | 腰围 |
| bodyfat_pct | float | 体脂率（可空） |
| pushup_max | int | 俯卧撑最大次数（可空） |
| plank_sec | int | 平板支撑时长（可空） |

**疼痛记录 pain_log**
| 字段 | 类型 | 说明 |
|---|---|---|
| pain_id | string | 主键 |
| member_id | string | 外键 |
| date | date | 记录日期 |
| location | string | 部位 |
| score | int | 0-10 分 |
| traffic_light | enum | green / yellow / red |
| referred | bool | 是否已转介 |

**派生指标（供看板展示）**
- 周容量 = Σ(reps × load_kg)，按肌群聚合
- 进阶检测：同动作同次数的 load_kg 是否连续 2 周上升
- 疼痛趋势：14 天内 pain score 是否上升或黄灯未转绿 → 触发转介提醒
- 粘性指标：周训练次数、执行率（计划组数 vs 实际组数）
