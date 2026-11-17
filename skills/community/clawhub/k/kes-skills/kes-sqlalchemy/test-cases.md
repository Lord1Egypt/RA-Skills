---
name: kes-sqlalchemy
description: KingbaseES Python 框架集成 — 测试用例
---

# KingbaseES Python 框架测试用例

## 测试用例 1: SQLAlchemy 连接

**场景**：使用 SQLAlchemy 连接金仓

**输入问题**："SQLAlchemy 怎么连接金仓数据库？"

**期望答案要点**：
- `create_engine("kingbase://SYSTEM:123456@127.0.0.1:54321/test")`
- declarative_base 定义模型

**验证方法**：答案包含 kingbase:// URL 格式

---

## 测试用例 2: Django 配置

**场景**：Django 项目使用金仓

**输入问题**："Django 怎么配置金仓数据库？"

**期望答案要点**：
- ENGINE: `django.db.backends.kingbase`
- 端口 54321
- 需使用第三方后端或 PostgreSQL 兼容模式

**验证方法**：答案包含 Django DATABASES 配置
