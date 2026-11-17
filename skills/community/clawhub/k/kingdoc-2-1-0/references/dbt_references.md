# 多维表格 API 参考

> 轻维表（dbt）完整操作 API，对标腾讯文档智能表格。

---

## 1. 创建多维表格

```
POST /dbt/tables

Body:
{
  "name": "项目管理",
  "description": "团队项目跟踪",
  "folder_id": "可选"
}
```

**响应**：

```json
{
  "code": 0,
  "data": {
    "table_id": "dbt_abc123",
    "name": "项目管理"
  }
}
```

---

## 2. 字段管理

### 2.1 添加字段

```
POST /dbt/fields

Body:
{
  "table_id": "dbt_abc123",
  "name": "优先级",
  "type": "select",
  "options": ["P0", "P1", "P2"],
  "required": true
}
```

### 2.2 修改字段

```
PUT /dbt/fields/:field_id
```

### 2.3 删除字段

```
DELETE /dbt/fields/:field_id
```

### 2.4 列出字段

```
GET /dbt/fields/:table_id
```

---

## 3. 视图管理

### 3.1 添加视图

```
POST /dbt/views

Body:
{
  "table_id": "dbt_abc123",
  "name": "按优先级分组",
  "type": "group",
  "config": {
    "field": "优先级",
    "order": ["P0", "P1", "P2"]
  }
}
```

---

## 4. 记录操作

### 4.1 新增记录

```
POST /dbt/records

Body:
{
  "table_id": "dbt_abc123",
  "fields": {
    "项目名称": "知识库建设",
    "负责人": "张三",
    "优先级": "P1"
  }
}
```

### 4.2 批量新增（推荐）

```
POST /dbt/records/batch

Body:
{
  "table_id": "dbt_abc123",
  "records": [
    {"fields": {...}},
    {"fields": {...}},
    ...
  ]
}
```

### 4.3 更新记录

```
PUT /dbt/records/:record_id
```

### 4.4 删除记录

```
DELETE /dbt/records/:record_id
```

### 4.5 查询记录

```
GET /dbt/records/:table_id?filter={...}&offset=0&limit=100
```

---

## 5. Webhook

### 5.1 设置 Webhook

```
POST /dbt/webhooks

Body:
{
  "table_id": "dbt_abc123",
  "callback_url": "https://your-app.com/webhook",
  "events": ["record.add", "record.update", "record.delete"],
  "secret": "可选，用于签名验证"
}
```

### 5.2 列出 Webhook

```
GET /dbt/webhooks/:table_id
```

---

## 6. 错误码

| 错误码 | 含义 |
|--------|------|
| 字段已存在 | 尝试添加重复名称的字段 |
| 字段被视图依赖 | 删除字段前需先删除依赖的视图 |
| 记录不存在 | record_id 不存在 |
| 表格不存在 | table_id 不存在 |
| Webhook 回调失败 | 回调 URL 返回非 2xx 状态码 |
