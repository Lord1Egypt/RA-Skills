# EXAMPLES

## 示例 1：写入偏好

输入：

```text
/remember 以后长文默认发飞书文档，日报没内容就不要硬写
```

预期效果：
- gate 判断为 write
- 写 daily log
- 更新 session-state
- 可能 materialize 为 preference object
- 更新 memory index

---

## 示例 2：召回历史偏好

输入：

```text
/recall 日报要求
```

或：

```text
你还记得我上次说的日报要求吗
```

预期效果：
- gate 判断为 recall
- 从 topic/meta 与相关 preference/decision 对象中 summary-first 召回
- 返回紧凑 JSON

---

## 示例 3：整理记忆

输入：

```text
/reflect
```

或：

```text
整理记忆
```

预期效果：
- 运行 reflection
- 生成 `memory/reflections/YYYY-MM-DD.md`
- 更新 memory index

---

## 示例 4：新建主题

```bash
python3 skills/memory-orchestrator/scripts/memory_cli.py new-topic \
  --slug entrepreneurship \
  --title "创业 / 商业模式" \
  --summary "当用户反复讨论创业、产品验证、商业模式时启用。"
```

生成：
- `memory/topics/entrepreneurship.yaml`
- `memory/indexes/README.md` 更新

---

## 示例 5：新建对象

```bash
python3 skills/memory-orchestrator/scripts/memory_cli.py new-object \
  --type project \
  --domain technology \
  --slug memory-orchestrator \
  --title "Memory Orchestrator" \
  --summary "OpenClaw 白盒记忆系统实现项目。"
```

生成：
- `memory/objects/projects/memory-orchestrator.yaml`
- `memory/indexes/README.md` 更新

---

## 示例 6：低成本 turn

输入：

```bash
python3 skills/memory-orchestrator/scripts/memory_cli.py turn "ok"
```

预期效果：
- gate 直接跳过
- 不 recall
- 不 write

输入：

```bash
python3 skills/memory-orchestrator/scripts/memory_cli.py turn "你还记得我上次说的日报要求吗"
```

预期效果：
- gate 命中 recall
- 调用 recall_memory.py
- 返回 meta 相关 topic 和 object summaries
