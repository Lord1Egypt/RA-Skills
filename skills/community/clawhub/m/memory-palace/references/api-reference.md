# API 完整参数参考

## 基础操作

### memory_palace_write

写入新记忆。

**必填参数：**
- `content`: 记忆内容（你想记住什么）

**可选参数：**
- `tags`: 标签数组，方便分类检索，如 `["用户", "偏好", "重要"]`
- `importance`: 重要性 0-1，建议 0.7+ 表示重要记忆
- `location`: 存储位置，默认 "default"，如 "用户"、"项目A"、"日程"
- `type`: 类型
  - `fact` - 事实（默认）
  - `experience` - 经验
  - `lesson` - 教训
  - `preference` - 偏好
  - `decision` - 决策
- `summary`: 可选摘要

**返回：** Memory 对象（含 id）

---

### memory_palace_get

获取单条记忆。

**必填参数：**
- `id`: 记忆 ID

**返回：** Memory 对象或 null

---

### memory_palace_update

更新记忆。

**必填参数：**
- `id`: 记忆 ID

**可选参数：**
- `content`: 新内容
- `tags`: 新标签（替换原有）
- `importance`: 新重要性
- `summary`: 新摘要
- `appendTags`: true 时追加标签而非替换

**返回：** 更新后的 Memory 对象或 null

---

### memory_palace_delete

删除记忆。

**必填参数：**
- `id`: 记忆 ID

**可选参数：**
- `permanent`: true 时永久删除，false（默认）时移入回收站

**返回：** void

---

### memory_palace_search

搜索记忆。

**必填参数：**
- `query`: 搜索关键词（支持自然语言）

**可选参数：**
- `tags`: 只搜索特定标签
- `topK`: 返回数量，默认 10
- `location`: 过滤位置
- `minImportance`: 最低重要性
- `includeArchived`: 包含已归档记忆

**返回：** SearchResult 数组，每个包含：
- `memory`: Memory 对象
- `score`: 相关性分数 0-1
- `highlights`: 匹配片段
- `isFallback`: 是否降级到文本搜索

---

### memory_palace_list

列出记忆。

**可选参数：**
- `location`: 过滤位置
- `tags`: 过滤标签
- `status`: 过滤状态（active/archived/deleted）
- `limit`: 返回数量
- `offset`: 分页偏移
- `sortBy`: 排序字段（createdAt/updatedAt/importance）
- `sortOrder`: 排序方向（asc/desc）

**返回：** Memory 数组

---

### memory_palace_stats

获取统计信息。

**返回：**
```json
{
  "total": 100,
  "active": 95,
  "archived": 3,
  "deleted": 2,
  "byLocation": { "default": 50, "projects": 45 },
  "byTag": { "用户": 20, "项目": 30 },
  "avgImportance": 0.65,
  "storagePath": "/path/to/memory/palace",
  "vectorSearch": { "enabled": true }
}
```

---

### memory_palace_restore

从回收站恢复记忆。

**必填参数：**
- `id`: 记忆 ID

**返回：** 恢复的 Memory 对象或 null

---

## 批量操作

### memory_palace_store_batch

批量存储记忆。

**参数：**
- `items`: StoreParams 数组

**返回：** Memory 数组

---

### memory_palace_get_batch

批量获取记忆。

**参数：**
- `ids`: ID 数组

**返回：** (Memory | null) 数组

---

### memory_palace_delete_batch

批量删除记忆。

**参数：**
- `ids`: ID 数组
- `permanent`: 是否永久删除

**返回：** 删除结果对象

---

## 经验管理

### memory_palace_record_experience

记录可复用经验。

**必填参数：**
- `content`: 经验内容
- `applicability`: 适用场景描述
- `source`: 来源标识（如任务 ID）

**可选参数：**
- `category`: 类别
  - `development` - 开发
  - `operations` - 运维
  - `product` - 产品
  - `communication` - 沟通
  - `general` - 一般
- `tags`: 标签
- `importance`: 重要性（默认 0.7）
- `location`: 存储位置（默认 "experiences"）

**返回：** Memory 对象（type=experience）

---

### memory_palace_get_experiences

查询经验。

**可选参数：**
- `category`: 过滤类别
- `applicability`: 过滤适用场景（部分匹配）
- `verified`: 只返回已验证经验
- `limit`: 返回数量
- `sortByVerified`: 按验证次数排序

**返回：** Memory 数组

---

### memory_palace_verify_experience

验证经验有效性。

**必填参数：**
- `id`: 经验 ID
- `effective`: 是否有效（true/false）

**返回：** 更新后的 Memory 对象，含快捷字段：
- `verified`: 是否已验证
- `verifiedCount`: 验证次数
- `verifiedAt`: 最后验证时间

---

### memory_palace_get_relevant_experiences

获取相关经验。

**必填参数：**
- `context`: 当前上下文描述

**可选参数：**
- `limit`: 返回数量（默认 5）

**返回：** Memory 数组

---

### memory_palace_experience_stats

获取经验统计。

**返回：**
```json
{
  "total": 20,
  "byCategory": { "development": 10, "operations": 5 },
  "verified": 8,
  "avgEffectiveness": 0.65
}
```

---

## 记忆关联

### memory_palace_link

关联两条记忆。

**必填参数：**
- `sourceId`: 源记忆 ID
- `targetId`: 目标记忆 ID
- `type`: 关系类型
  - `relates_to` - 相关
  - `refines` - 细化
  - `contradicts` - 矛盾

**可选参数：**
- `note`: 关系说明

---

### memory_palace_get_related

获取关联记忆。

**必填参数：**
- `id`: 记忆 ID

**可选参数：**
- `type`: 过滤关系类型

**返回：** 关联记忆数组

---

## LLM 增强

### memory_palace_summarize

智能总结长记忆。

**必填参数：**
- `id`: 记忆 ID

**可选参数：**
- `saveSummary`: 是否保存摘要到记忆

**返回：** 总结结果

---

### memory_palace_parse_time

解析时间表达式。

**必填参数：**
- `expression`: 时间表达式（如"明天"、"下周三"）

**返回：**
```json
{
  "hasTimeReasoning": true,
  "keywords": ["3月25日"],
  "resolvedDate": "2026-03-25"
}
```

---

### memory_palace_expand_concepts

语义扩展搜索词。

**必填参数：**
- `query`: 原始查询

**返回：**
```json
{
  "originalQuery": "健康",
  "expandedKeywords": ["健康", "运动", "健身", "体检"],
  "relatedConcepts": ["医疗", "锻炼"]
}
```

---

### memory_palace_compress

智能压缩记忆。

**必填参数：**
- `memory_ids`: 要压缩的记忆 ID 数组（至少 2 条）

**返回：** 压缩结果