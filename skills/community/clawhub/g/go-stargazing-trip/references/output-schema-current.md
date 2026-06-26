# go-stargazing 当前输出结构（2026-03-28）

本文档描述 `scripts/go_stargazing.py` 当前主要输出层次，供后续 skill 接入、调试和回归测试使用。

说明：
- `scripts/go_stargazing.py`：当前推荐的稳定入口
- `scripts/dynamic_sampling_prototype.py`：当前主要实现文件

---

## 一、单模型输出顶层

主要字段：

- `mode`
- `target_datetime`
- `weather_model`
- `forecast_confidence`
- `scope_mode`
- `scope_coverage`
- `scope_reduction_reason`
- `scope_guardrail`
- `decision_summary`
- `top_region_advice`
- `timing`
- `confidence_note`
- `budget`
- `polygon_filtering`
- `generated_before_filter`
- `remaining_after_filter`
- `stage1_survivors`
- `stage2_points`
- `deduped_survivors`
- `region_labels`

### 说明
- **决策层**：`decision_summary`、`top_region_advice`
- **明细层**：`region_labels`、`stage1_survivors`、`stage2_points`、`deduped_survivors`
- **范围层**：`scope_mode`、`scope_coverage`、`scope_reduction_reason`、`scope_guardrail` 用于说明本次到底扫描了什么范围，防止把局部范围误当成全国结论

---

## 二、decision_summary（用户决策层）

主要字段：

- `primary_region`：当前主区域
- `primary_advice`：当前主区域短建议
- `backup_regions`：备选区域列表
- `confidence_note`：置信度提醒
- `risk_note`：主要风险提醒
- `third_model_note`：是否触发第三模型复核
- `joint_note`：联合判断短建议（compare 模式下）
- `one_line`：一句话结论
- `final_reply_draft`：接近可直接发送的完整回复骨架
- `reply_drafts.concise`：简短版
- `reply_drafts.standard`：标准版
- `reply_drafts.detailed`：详细版

### 使用建议
- 聊天场景：优先使用 `reply_drafts.standard`
- 极短回复：使用 `reply_drafts.concise`
- 需要完整说明：使用 `reply_drafts.detailed`

---

## 三、region_labels（单模型区域摘要）

每个 region 典型字段：

- `label`
  - 现在默认会补上省 / 自治区 / 直辖市前缀，避免出现“承德东北部”这类脱离上下文难判断的名字
  - 对新疆 / 西藏 / 青海 / 内蒙古等偏远大区，会优先补到“省/自治区 + 地区/州/盟 + 县/旗 + 方位”层级，提升可理解性
- `provinces`
- `cluster_size`
- `lat` / `lng`
- `best_point_id`
- `final_score`
- `best_score`
- `night_avg_cloud`
- `night_worst_cloud`
- `night_avg_humidity`
- `night_avg_visibility_m`
- `night_avg_wind_kmh`
- `moon_interference`
- `usable_hours`
- `longest_usable_streak_hours`
- `best_window_start`
- `best_window_end`
- `best_window_segment`
- `cloud_stddev`
- `cloud_stability` (`stable` / `mixed` / `volatile`)
- `worst_cloud_segment`
- `avg_moonlight_score`
- `avg_cloud_cover`
- `avg_elevation_m`
- `members`
- `brief_advice`
- `display_label`
  - 面向当前输出阶段优先展示的标签
  - 大范围/粗筛时可能会保守成“某地一带”
- `anchor_label`
  - 范围锚点标签，例如 `山西大同一带`
- `refined_label`
  - 更细一级的落点标签，例如 `山西大同西南部`
- `refinement_note`
  - 用来解释“粗筛锁定哪一片、细筛后更偏哪一侧”，避免前后像打架
- `human_view`
  - 面向用户的“人话视图”，以后**优先给对话层 / 上层调用方使用**
  - 典型字段包括：
    - `推荐级别`
    - `联合判断`
    - `模型支持`
    - `可拍窗口`
    - `最长连续窗口`
    - `平均云量`
    - `最差时段云量`
    - `云量走势`
    - `夜间平均风速`
    - `月光影响`
    - `亮点摘要`
    - `风险摘要`

### 面向用户时，字段翻译建议
- `usable_hours` → **可拍窗口**
- `longest_usable_streak_hours` → **最长连续可拍窗口**
- `night_worst_cloud` → **最差时段云量**
- `cloud_stability` → **云量走势 / 云量稳不稳**
- `qualification` → **推荐级别**
- `decision_rank_score` → **内部排序分**（不要直接念给用户）
- `avg_score` → **综合分**（如非必要，也不要直接拿字段名说）
- `evidence_type` / `model_coverage` → **模型支持情况**

---

## 四、compare-models 输出顶层

主要字段：

- `comparison_target_datetime`
- `forecast_confidence`
- `scope_mode`
- `scope_coverage`
- `scope_reduction_reason`
- `scope_guardrail`
- `compare_models`
- `model_results`
- `joint_judgement`
- `third_model_recheck`
- `decision_summary`
- `timing`

### 说明
- `model_results`：每个模型各跑一遍完整单模型输出
- `joint_judgement`：模型联合判断层
- `third_model_recheck`：争议区自动第三模型复核状态

---

## 五、joint_judgement（联合判断层）

主要字段：

- `summary`
  - `consensus_count`
  - `single_model_count`
  - `candidate_count`
  - `disputed_count`
  - `reject_count`
- `top_joint_advice`
- `consensus_regions`

### consensus_regions 每项典型字段

- `label`
- `provinces`
- `judgement`
  - `共识推荐`
  - `单模型亮点`
  - `备选`
  - `争议区`
  - `不建议`
- `dispute_type`
  - `强分歧区`
  - `单模型乐观区`
  - `窗口不稳区`
  - `null`
- `evidence_type`
  - `single_model`
  - `dual_model`
  - `multi_model`
- `model_coverage`
- `avg_score`
- `score_spread`
- `avg_night_cloud`
- `per_model`
  - 每个模型下现在也会带一份 `human_view`，方便直接转成人话
- `human_view`
  - 联合判断层的人话摘要
- `joint_brief_advice`

---

## 六、当前设计原则

### 1. 决策层 / 明细层分离
- 决策层给用户或上层调用方直接使用
- 明细层保留调试和精修所需细节
- 面向用户时，优先使用 `brief_advice` / `joint_brief_advice` / `human_view`，不要生硬复述内部变量名
- 面向用户的最终文案必须做一次可读性自检：
  - 禁止混入意外外语碎片（尤其是俄文）
  - 禁止把调试字段、变量名、枚举值直接当正文输出
  - 禁止出现“像日志而不像人话”的表达

### 2. 夜间窗口语义固定
- 统一按 **目标当晚 → 次日早晨** 处理
- 内部标准化窗口为 `18 → 30`

### 3. 第三模型只在争议时触发
- 默认主流程：`gfs_global + ecmwf_ifs`
- 若争议 / 单模型偏强：可用 `--auto-third-model icon_global`

---

## 七、当前已知注意事项

- 天文 twilight 原始结果可能出现反向/白天窗口，现已通过 `normalize_night_window()` 统一纠正
- 部分 Open-Meteo 小时值可能为 `null`，现已做 `safe_float()` 保护
- `reply_drafts` 属于用户友好层，不应替代底层调试字段
