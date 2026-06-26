# `persona/PERSONA_PROFILE.md` 结构约定与消费指南

本文件面向**其他 skill、运行时消费者与维护者**，用于统一理解 `persona/PERSONA_PROFILE.md` 的职责、结构和读取方式。

## 1. 文件定位

`persona/PERSONA_PROFILE.md` 的作用是：

- 给 Timeline 和其他下游提供一份稳定、可消费、可解析的人设档案
- 给人类维护者提供一份比 `IDENTITY.md` 更完整、比 `SOUL.md` 更稳定的结构化人物说明

它**不负责**：

- 承担运行时 prompt 的全部人格表达
- 代替 `SOUL.md` 提供即时互动规则
- 代替 `MEMORY.md` 记录关系过程
- 回答“她现在在哪里”“她今天穿什么”“昨晚发生了什么”

如果一个信息更像“她会怎么回应你”，应优先去 `SOUL.md`。  
如果一个信息更像“她和你之间已经形成了什么稳定模式”，应优先去 `MEMORY.md`。  
如果一个信息更像“这个人稳定是什么样的人”，才应进入 `PERSONA_PROFILE.md`。

## 2. 顶层读取原则

消费 `PERSONA_PROFILE.md` 时，默认遵守以下原则：

- 把它当作**稳定事实源**，不要把它当作文学散文来读
- 优先消费带字段名的短条目
- 优先提取**可外化属性**，不要主动脑补长链心理推理
- 若某段落出现解释性 prose，以其中能够稳定复用的事实和外在特征为准
- 不要从 `PERSONA_PROFILE.md` 反推不存在的关系标签、岗位职责或时间事实
- 不要把 `Scene Anchors` 中的可复用场景误当成已经发生过的历史
- 用户接收偏好不在 `PERSONA_PROFILE.md` 中维护；若需要知道用户更容易接收哪种关心方式，应读取 `USER.md`
- 用户 MBTI、用户职业栈、用户侧配对推导结论都不属于 persona 稳定事实；不要把这些内容反写进 `PERSONA_PROFILE.md`
- 若维护者在 `SOUL.md`、`MEMORY.md`、`IDENTITY.md`、`USER.md` 中改写了稳定 persona 事实，必须同步回写 `PERSONA_PROFILE.md`
- 纯运行时话术、关系过程更新或纯用户侧信息更新，不应反向污染 `PERSONA_PROFILE.md`

## 3. 一级结构约定

`PERSONA_PROFILE.md` 采用“双层合同”：

- 第一层是 **canonical runtime layer**，必须严格对齐 Timeline 真正消费的 8 个一级结构
- 第二层是 **rich profile layer**，允许在这 8 个结构内部保留更完整的人物资料字段，供 persona skill 或其他下游读取

必需一级结构只有以下 8 个：

1. `## Meta`
2. `## Identity`
3. `## Soul`
4. `## Stable Memory`
5. `## Daily Rhythm Tendencies`
6. `## Appearance Tendencies`
7. `## Scene Anchors`
8. `## Constraint Rules`

其他下游不要把额外一级标题当成 runtime contract 的一部分；如果维护者确实增加了额外章节，也只能视为 extension-only 内容，不能假设 Timeline 会消费它们。

## 4. 分段语义约定

### 4.1 `## Meta`

这是最强约束的地理与兼容层。

canonical required：

- `schema_version`
- `home_city`
- `home_country`
- `home_timezone`

common rich extension：

- `persona_id`
- `primary_language`

消费建议：

- `home_city` 是地理锚点，不是“当前就在这里”的时间性声明
- `home_country` 与 `home_timezone` 应与 `home_city` 一致
- 下游时间推理应优先依赖这里的地理与时区信息
- `persona_id` 与 `primary_language` 可以保留，但不要误当作 Timeline runtime 的必需字段

### 4.2 `## Identity`

这里描述**稳定身份与生活基底**。

canonical required：

- `living_style`
- `base_environment`
- `common_zones`
- `routine_context`

common rich extension：

- `display_name`
- `age`
- `gender`
- `mbti`
- `life_stage`
- `mobility_radius`
- `occupation_style`

消费建议：

- 年龄和 `life_stage` 的约束优先级很高，即使它们不是 Timeline canonical contract 的必需字段，也应继续保留在完整人物资料里
- 不要把学生阶段 persona 写成成熟职场高管

### 4.3 `## Soul`

这里描述**稳定气质与体验风格**。

canonical required：

- `temperament`
- `emotional_style`
- `social_style`
- `cognitive_style`
- `values`

common rich extension：

- `aesthetic_bias`

消费建议：

- 它能影响场景氛围、叙事质感和生活纹理
- 它不替代 `SOUL.md` 的运行时规则
- `aesthetic_bias` 很适合保留在 rich profile layer，但不要让它掩盖 canonical 气质字段

### 4.4 `## Stable Memory`

这里描述**长期成立的习惯、偏好、承诺与非时间事实**。

canonical required：

- `long_term_habits`
- `long_term_preferences`
- `durable_commitments`
- `recurring_patterns`
- `important_non_temporal_facts`

消费建议：

- 只把它当成稳定约束，不要把它当成 dated event

### 4.5 `## Daily Rhythm Tendencies`

这里描述**时间段倾向**。

canonical required：

- `weekday_bias`
- `weekend_bias`
- `morning_bias`
- `afternoon_bias`
- `evening_bias`
- `late_night_bias`
- `world_rhythm_constraints` (optional rich extension)

消费建议：

- 它适合指导“什么在这个时段通常更 plausible”
- 它不是精确日程表
- `world_rhythm_constraints` 允许定义强化的时间基线（如 `sleep: { start: '04:00', end: '12:00' }`），用于覆盖系统默认作息。Timeline runtime 在执行合理性校验时应优先读取此字段。

### 4.6 `## Appearance Tendencies`

这里描述**外观延续与换装逻辑**。

canonical required：

- `default_home_style`
- `default_outing_style`
- `default_exercise_style`
- `change_triggers`
- `non_triggers`
- `style_constraints`

common rich extension：

- `appearance_priority`

消费建议：

- 它适合支持 same-day appearance continuity
- 不要把这里误读成“当前穿着状态”
- `appearance_priority` 很有价值，但它属于 rich profile layer，而不是 Timeline runtime 的必需字段

### 4.7 `## Scene Anchors`

这里描述**生活场景先验**。

canonical required：

- `plausible_locations`
- `plausible_activities`
- `rare_but_possible_scenes`
- `implausible_or_rare_locations`
- `implausible_or_rare_activities`

消费建议：

- 它适合让生成结果更具体、更像这个人
- 不要过度重复同一场景模板

### 4.8 `## Constraint Rules`

这里描述**硬边界和软约束**。

canonical required：

- `must`
- `should`
- `avoid`

编码要求：

- 必须使用 parser 可读的键值形式，例如 `- must: [a, b]` 或 `- must:` 后接缩进列表
- 不要再用 `### must` / `### should` / `### avoid` 这种小标题形式，因为 Timeline parser 不会把它们映射进 canonical contract

消费建议：

- `must` 约束最强
- `avoid` 代表低 plausibility 或明显不合人设的方向

## 5. 推荐读取顺序

如果其他 skill 只需要快速消费 `PERSONA_PROFILE.md`，建议先读 canonical runtime layer，再按需补读 rich profile layer：

1. `Meta`
2. `Identity`
3. `Constraint Rules`
4. `Appearance Tendencies`
5. `Scene Anchors`
6. `Stable Memory`
7. `Daily Rhythm Tendencies`
8. `Soul`

补充建议：

- 如果任务在问“她是谁”，再读 `Identity` 里的 rich extension 字段
- 如果任务在问“她的表达或审美质地”，再读 `Soul` 和 `Appearance Tendencies` 里的 rich extension 字段
- 不要让 rich profile layer 反过来覆盖 canonical runtime layer 的约束判断

## 6. 推荐消费方式

推荐把 `PERSONA_PROFILE.md` 消费成以下两类结构化对象：

- `canonical_contract`
  - 只包含 Timeline runtime 真正消费的字段子集
- `rich_profile_overlay`
  - 只包含完整人物资料所需、但不属于 canonical runtime contract 的补充字段

一个实用的读取拆分通常是：

- `meta`
  - schema、城市、国家、时区
- `identity`
  - 生活方式、底层环境、常见活动区、日常语境
- `stable_memory`
  - 长期习惯、偏好、承诺、非时间事实
- `daily_rhythm`
  - 工作日、周末和时间段倾向
- `appearance`
  - 默认风格、换装触发器、非触发器、风格边界
- `scene_anchors`
  - 可行场景、低频场景、不合理场景
- `constraints`
  - `must / should / avoid`
- `identity_overlay`
  - 名字、年龄、性别、MBTI、生命阶段、移动半径、职业风格
- `meta_overlay`
  - persona id、主语言
- `soul_overlay`
  - 审美取向
- `appearance_overlay`
  - 外观优先级

## 7. 与其他文件的边界

### 相对 `SOUL.md`

- `PERSONA_PROFILE.md` 回答：她稳定是什么样的人
- `SOUL.md` 回答：她在运行时应该怎样对待你
- 若两者出现冲突，运行时以 `SOUL.md` 为准
- 若运行时 agent 只需要轻量身份摘要，先看 `IDENTITY.md`；若 `IDENTITY.md` 不足以回答稳定人物细节，再补读 `PERSONA_PROFILE.md`

### 相对 `MEMORY.md`

- `PERSONA_PROFILE.md` 回答：她稳定拥有什么生活纹理、人际倾向和场景约束
- `MEMORY.md` 回答：她与你之间已经形成了哪些持续模式和注意事项

### 相对 `IDENTITY.md`

- `PERSONA_PROFILE.md` 是完整档案
- `IDENTITY.md` 是轻量卡片加基础资料摘要，通常只投影 `display_name`、`home_city`、`home_country`、`home_timezone`、`age`、`gender`、`primary_language`、`mbti` 等高稳定字段，不承载完整人物档案

### 相对 `USER.md`

- `PERSONA_PROFILE.md` 描述 persona
- `USER.md` 描述用户侧稳定信息

## 8. 禁止性消费方式

其他 skill 读取 `PERSONA_PROFILE.md` 时，不应：

- 把它解析成“岗位说明书”或关系角色
- 把长段 prose 中的情绪渲染误当作硬事实
- 把 `Soul` 膨胀成未经明示的深层病理或创伤解释
- 用单一字段覆盖整个人物，例如只拿 `MBTI` 或只拿 `home_city`
- 忽略生命阶段，把学生期 persona 写成成熟职场型人格
- 把 `Scene Anchors` 或 rich extension 里的补充资料当成已经发生过的共同记忆
- 用 `Appearance Tendencies` 直接回答“她现在穿什么”

## 9. 对其他 skill 的一句建议

如果你需要：

- “她是谁” -> 读 `PERSONA_PROFILE.md`
- “她现在该怎么说、怎么回” -> 读 `SOUL.md`
- “她和用户之间已经形成了什么模式” -> 读 `MEMORY.md`

不要试图让 `PERSONA_PROFILE.md` 一份文件承担全部运行时文件的工作。
