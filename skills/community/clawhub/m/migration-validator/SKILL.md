---
name: migration-validator
description: Validates SQL syntax of pending database migration files before execution
tags:
  - database
  - sql
  - migration
  - validation
category: database
version: 1.0.0
---

# 迁移验证器

## 概述

扫描迁移目录中的 SQL 文件，验证语法的正确性，记录已应用和待应用的迁移状态。确保只有语法正确的迁移才会进入执行管道。

## 使用场景

- 变更管控：在迁移执行前发现 SQL 语法错误
- CI/CD 集成：作为部署流水线中的门控步骤
- 多环境一致性：验证迁移文件跨环境兼容

## 使用方法

1. 扫描 migrations 目录获取所有 SQL 文件。
2. 使用 SQLite PRAGMA 或语法解析器验证每个文件。
3. 记录已执行的迁移和待执行的迁移。
4. 输出验证报告 JSON。

## 输出格式

```json
{
  "validation_timestamp": "2026-06-01T12:00:00",
  "migrations_found": ["001_initial.sql", "002_create_orders.sql"],
  "pending_migrations": [],
  "validation_errors": [],
  "status": "completed"
}
```

## 实现代码

见 `scripts/validate.py`。
