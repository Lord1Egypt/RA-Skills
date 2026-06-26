---
name: iwatch-swim-tracker
description: 当用户发送的图片为 Apple Watch 健身的泳池游泳记录，或用户消息包含「游泳」关键词并附带图片时触发。识别游泳训练截图，提取距离、配速、心率等结构化数据，保存训练记录并生成趋势分析报告。适用于游泳训练数据追踪、历史对比和个性化建议。
metadata:
  openclaw:
    requires:
      bins:
        - python3
---

# iWatch Swim Tracker

## 触发判断

满足以下任一条件时触发本技能：

1. 当收到用户消息包含图片时，图片内容为 Apple Watch 健身 App 的**泳池游泳**训练记录截图。
2. 当用户消息中包含「游泳」关键词并附带图片时。

## 数据提取

从截图中尽可能提取以下字段。能识别多少就提取多少，不确定的字段不要填。

### 必填字段

- `date`: 训练日期 → 格式 `YYYY-MM-DD`
- `time_range`: 训练时段 → 格式 `HH:MM-HH:MM`
- `pool_length`: 泳池长度（米）
- `total_distance`: 总距离（米）
- `laps`: 趟数
- `strokes`: 各泳姿距离 → `{"freestyle": {"distance": N}, "breaststroke": {"distance": N}}`
  - 自由泳=freestyle、蛙泳=breaststroke、仰泳=backstroke、蝶泳=butterfly、混合泳=medley、浮板=kickboard
- `duration`: 体能训练时间 → 格式 `H:MM:SS`
- `duration_seconds`: 时长转换为秒
- `avg_pace`: 平均配速 → 格式 `M:SS/100m`
- `avg_pace_seconds`: 平均配速转换为秒/100m
- `avg_heart_rate`: 平均心率（次/分）

### 可选字段

- `active_calories`: 动态千卡
- `total_calories`: 总千卡数
- `effort_score`: 耗能评分（1-10）
- `effort_level`: 耗能等级，如「适中」「困难」等
- `session_number`: 第 N 次游泳（如用户提供）
- `auto_sets`: 自动组合数据

### 数据校验

- 泳姿距离之和应等于总距离
- 趟数 × 泳池长度 ≈ 总距离
- 日期年份应为当前年份
- 不确定的值不要猜，宁可不填

## 处理流程

### Step 1：提取数据

从图片中提取上述字段，组装为 JSON 对象。

### Step 2：保存数据

```bash
python3 {baseDir}/scripts/extract_swim_data.py '<json_data>'
```

同一天的数据会自动覆盖更新。

### Step 3：查询历史

```bash
python3 {baseDir}/scripts/query_history.py --days 14 --weeks 4 --date <YYYY-MM-DD>
```

## 回复格式

```
🏊 游泳训练记录

📅 <date> <time_range>
🏊 总距离: <total_distance>m（<laps>趟 × <pool_length>m池）
⏱️ 时长: <duration>
⚡ 平均配速: <avg_pace>
💓 平均心率: <avg_heart_rate> 次/分
🔥 消耗: <active_calories> 动态千卡 / <total_calories> 总千卡

泳姿分布:
- 自由泳: <freestyle_distance>m
- 蛙泳: <breaststroke_distance>m
- 浮板: <kickboard_distance>m

📊 AI 分析:
<基于本次数据和历史趋势，给出 2-3 句个性化分析和建议>

📈 近期趋势:
<与最近几次训练的关键指标对比>
```
