---
name: kes-hibernate
description: KingbaseES Java 框架集成 — 测试用例
---

# KingbaseES Java 框架测试用例

## 测试用例 1: MyBatis 数据源配置

**场景**：Spring Boot + MyBatis 连接金仓

**输入问题**："MyBatis 怎么配置金仓数据源？"

**期望答案要点**：
- driver: `com.kingbase8.Driver`
- url: `jdbc:kingbase8://host:54321/test`

**验证方法**：答案包含正确的驱动和 URL

---

## 测试用例 2: Flyway 迁移

**场景**：使用 Flyway 管理数据库迁移

**输入问题**："Flyway 怎么连接金仓数据库？"

**期望答案要点**：
- `flyway.url=jdbc:kingbase8://host:54321/test`
- 脚本命名 `V{版本号}__{描述}.sql`

**验证方法**：答案包含 Flyway 配置和命名规范
