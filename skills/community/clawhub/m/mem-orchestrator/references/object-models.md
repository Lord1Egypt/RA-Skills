# Object Models

## 目标

定义当前 memory system 中主要文件类型的字段语义，便于后续继续开发。

---

## 1. Topic Card

路径：`memory/topics/<slug>.yaml`

建议字段：

```yaml
id: research
name: 科研 / 论文 / 方法论
summary: 一句话说明这个主题对用户意味着什么
subtopics: []
recent_objects: []
linked_topics: []
stable_preferences: []
priority_rules: []
```

### 字段说明
- `id`：稳定标识
- `name`：人类可读标题
- `summary`：主题摘要，应该尽量短
- `subtopics`：子话题列表
- `recent_objects`：最近相关对象
- `linked_topics`：相邻主题
- `stable_preferences`：该主题下已经稳定的偏好
- `priority_rules`：何时优先激活这个主题

---

## 2. Generic Object

路径：`memory/objects/<type-dir>/<slug>.yaml`

建议字段：

```yaml
id: paper/constitutional-ai
type: paper
domain: research
title: Constitutional AI
summary: 对象的一句话摘要
why_it_matters: 为什么这条对象值得未来召回
tags: []
status: draft|discussed|stable|archived
confidence: low|medium|high
last_discussed: YYYY-MM-DD
relations: {}
user_takeaways: []
created_at: ISO8601
updated_at: ISO8601
```

### 字段说明
- `id`：稳定对象标识
- `type`：对象类型
- `domain`：归属领域
- `title`：标题
- `summary`：summary-first recall 的主字段
- `why_it_matters`：帮助未来判断是否值得召回
- `tags`：轻量标注
- `status`：当前状态
- `confidence`：当前对象质量
- `last_discussed`：最近讨论时间
- `relations`：和其它对象的关系
- `user_takeaways`：对用户有价值的提炼

---

## 3. Session State

路径：`memory/session-state.yaml`

```yaml
session_id: auto
active_domains: []
active_objects: []
current_goal: ""
recent_constraints: []
last_updated: ""
```

### 用途
- 当前回合或最近几轮的工作态
- 不等于长期记忆
- 可覆盖、可重写

---

## 4. Daily Log

路径：`memory/daily/YYYY-MM-DD.md`

用途：
- 保存当天的重要事件
- 为反思器提供原材料
- 不应该直接充当主召回层

---

## 5. Reflection Note

路径：`memory/reflections/YYYY-MM-DD.md`

用途：
- 记录最近整理过什么
- 哪些偏好被提升
- 哪些对象被合并、降权、更新

---

## 6. Index Files

路径：
- `memory/indexes/manifest.json`
- `memory/indexes/README.md`

用途：
- `manifest.json` 给脚本消费
- `README.md` 给人阅读

---

## 可扩展原则

1. 不要把当前 topic 看成封闭分类
2. 不要把当前 object type 看成封闭分类
3. 扩新类型时，优先保证：
   - 文件可读
   - 字段可解释
   - 索引能覆盖
   - README 有说明
