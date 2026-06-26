# SKILL.md — now-practice

## 功能

一分钟清明练习流程引擎。

## 练习流程

每个场景固定4步，总时长60秒：

```json
{
  "steps": [
    { "id": "stop", "name": "停", "duration_seconds": 10, "instruction": "放下手机\n坐直\n看一眼自己" },
    { "id": "breathe", "name": "呼吸", "duration_seconds": 30, "instruction": "知道自己正在吸气\n知道自己正在呼气" },
    { "id": "huatou", "name": "话头", "duration_seconds": 20, "instruction": "{huatou_text}\n\n不要回答\n只是问" },
    { "id": "return", "name": "回", "duration_seconds": 10, "instruction": "我看见了\n继续" }
  ]
}
```

## 场景映射

| 场景ID | 名称 | 话头场景标签 |
|--------|------|-------------|
| anxiety | 😰 焦虑了 | anxiety, fear |
| overthinking | 🤯 想太多 | overthinking |
| decision | 🤔 不知道怎么选 | decision, confusion |
| emotion | 😡 情绪上来了 | anger, sadness, judgment |
| free | 🌱 自由练习 | 全部标签（随机） |

## 话头选取逻辑

1. 根据场景ID，匹配 `data/huatou-templates-v1.0.json` 中 `scene` 数组包含对应标签的模板
2. 从匹配结果中随机选取一条
3. 填充模板变量（如 `{emotion}`）
4. 展示在练习第3步

## 变量填充映射

| 变量 | 场景 → 填充值 |
|------|---------------|
| {emotion} | anxiety→焦虑, anger→生气, fear→害怕, sadness→难过, overthinking→想, confusion→困惑 |
| {time_word} | regret→过去, fear→未来, waiting→等待 |

## 练习记录

练习完成后，前端写入 localStorage：

```json
{
  "date": "2026-05-30",
  "scene": "anxiety",
  "huatou_id": "who_001",
  "completed": true
}
```

连续天数计算：
- 每天至少完成1次练习算1天
- 读取 localStorage 中所有记录，按日期去重，计算连续天数
