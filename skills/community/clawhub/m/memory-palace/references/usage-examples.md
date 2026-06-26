# 使用场景示例

## 场景 1：记住用户偏好

用户说：「我叫张三，喜欢深色模式」

```
memory_palace_write: {
  "content": "用户名叫张三，偏好深色模式",
  "tags": ["用户", "偏好", "UI"],
  "importance": 0.9,
  "type": "preference"
}
```

下次用户问：「我之前说我喜欢什么来着？」

```
memory_palace_search: { "query": "用户偏好" }
```

---

## 场景 2：记录项目状态

项目里程碑完成。

```
memory_palace_write: {
  "content": "MiroFish 项目已完成 MVP 开发，API 模块已上线，数据库使用 PostgreSQL",
  "location": "MiroFish",
  "tags": ["项目", "状态", "里程碑"],
  "importance": 0.8,
  "type": "fact"
}
```

---

## 场景 3：记录技术决策

用户做了技术选型。

```
memory_palace_write: {
  "content": "决定使用 Redis 作为缓存层，预期 QPS 10000+",
  "location": "MiroFish",
  "tags": ["技术决策", "缓存", "Redis"],
  "importance": 0.8,
  "type": "decision"
}
```

---

## 场景 4：记录可复用经验

完成任务后学到教训。

```
memory_palace_record_experience: {
  "content": "TypeScript 的 as const 可以让类型推断更精确",
  "category": "development",
  "applicability": "需要精确类型推断的场景，如配置对象、常量定义",
  "source": "MiroFish-dev-task-042"
}
```

---

## 场景 5：验证经验有效性

之前记录的经验在类似场景下验证。

```
memory_palace_verify_experience: {
  "id": "exp-uuid",
  "effective": true
}
```

---

## 场景 6：查找相关经验

开始新任务时参考过去经验。

```
memory_palace_get_relevant_experiences: {
  "context": "需要为新项目设计 REST API",
  "limit": 3
}
```

---

## 场景 7：智能总结长记忆

用户分享了一段很长的需求描述。

```
memory_palace_summarize: {
  "id": "memory-uuid",
  "saveSummary": true
}
```

---

## 场景 8：解析时间表达

用户提到「下周三」。

```
memory_palace_parse_time: {
  "expression": "下周三"
}
// 返回: { hasTimeReasoning: true, resolvedDate: "2026-04-09" }
```

---

## 场景 9：扩展搜索词

搜索"健康"想找相关内容。

```
memory_palace_expand_concepts: {
  "query": "健康"
}
// 返回: { expandedKeywords: ["健康", "运动", "健身", "体检"] }
```

---

## 场景 10：关联相关记忆

将两条记忆关联起来。

```
memory_palace_link: {
  "sourceId": "uuid-1",
  "targetId": "uuid-2",
  "type": "relates_to",
  "note": "两个决策相互影响"
}
```

---

## 场景 11：批量管理

批量存储多条记忆。

```
memory_palace_store_batch: {
  "items": [
    { "content": "会议记录 1", "tags": ["会议"] },
    { "content": "会议记录 2", "tags": ["会议"] },
    { "content": "会议记录 3", "tags": ["会议"] }
  ]
}
```

---

## 场景 12：统计与监控

查看记忆库健康度。

```
memory_palace_stats: {}
memory_palace_experience_stats: {}
```