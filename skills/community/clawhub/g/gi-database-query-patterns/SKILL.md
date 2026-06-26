---
name: gi-database-query-patterns
description: Write database queries using tkms AsyncSqlSessionTemplate. Use when implementing dao layer, writing SQL, or when the user asks for database operations with insert/update/query_one/query_list.
tags: ["database", "dao", "tkms", "mysql", "async", "sql"]
---

# Database Query Patterns 数据库查询规范

使用 tkms 的 AsyncSqlSessionTemplate 进行数据库操作。适用于 app/dao 层，MySQL 8.0，UTF8 字符集。

## 何时使用

- 用户请求「写 dao」「写数据库操作」「查表」
- 实现 app/dao 下的数据访问逻辑
- 设计表结构、索引、SQL 语句

## 核心 API

```python
from tkms.database.async_template import AsyncSqlSessionTemplate

# 插入
await session.insert(table="t_user", params=entity, primary_key="tid")

# 更新
await session.update(table="t_user", params=entity, primary_key="tid")

# 查询单条
row = await session.query_one("SELECT * FROM t_user WHERE id = :id", {"id": user_id})

# 查询列表
rows = await session.query_list("SELECT * FROM t_user WHERE status = :status", {"status": 1})
```

## 操作规范

### 1. 插入

```python
async def add_user(self, user: UserEntity):
    await self.session.insert(table="t_user", params=user, primary_key="tid")
```

- `params`：实体或字典，字段名与表列对应
- `primary_key`：主键字段名，用于自增主键

### 2. 更新

```python
async def update_user(self, user: UserEntity):
    await self.session.update(table="t_user", params=user, primary_key="tid")
```

- 按主键更新，需包含主键值

### 3. 查询单条

```python
async def get_by_id(self, user_id: int) -> UserEntity | None:
    row = await session.query_one(
        "SELECT * FROM t_user WHERE id = :id",
        {"id": user_id}
    )
    return UserEntity(**row) if row else None
```

### 4. 查询列表（含分页）

```python
async def get_list(self, status: int, page: int, page_size: int):
    offset = (page - 1) * page_size
    rows = await session.query_list(
        "SELECT * FROM t_user WHERE status = :status ORDER BY id DESC LIMIT :limit OFFSET :offset",
        {"status": status, "limit": page_size, "offset": offset}
    )
    return [UserEntity(**r) for r in rows]
```

### 5. 统计

```python
async def count_by_status(self, status: int) -> int:
    row = await session.query_one(
        "SELECT COUNT(*) as cnt FROM t_user WHERE status = :status",
        {"status": status}
    )
    return row["cnt"] if row else 0
```

## SQL 规范

- **参数化**：一律用 `:param` 占位，禁止字符串拼接
- **表名**：项目约定表前缀（如 `t_`）
- **索引**：WHERE、ORDER BY 常用列建索引
- **避免 N+1**：批量查询用 IN 或 JOIN，避免循环单条查

## 建表规范

- 主键必建
- 按查询需求建索引（单列、复合）
- 字符集 UTF8
- 时间字段：`create_time`、`update_time`，类型 DATETIME

```sql
CREATE TABLE t_user (
    tid BIGINT PRIMARY KEY AUTO_INCREMENT,
    id VARCHAR(64) NOT NULL UNIQUE,
    name VARCHAR(128),
    status TINYINT DEFAULT 1,
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_status (status),
    INDEX idx_create_time (create_time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

## 事务

若框架支持事务，批量操作应包裹在事务内，保证原子性。
