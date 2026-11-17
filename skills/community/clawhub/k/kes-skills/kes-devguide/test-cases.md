---
name: kes-devguide
description: KingbaseES 应用开发指南 — 测试用例
---

# KingbaseES 应用开发指南测试用例

## 测试用例 1: 客户端接口选型

**场景**：用户需要选择适合的开发接口

**输入问题**："我的项目用 Spring Boot + Vue，金仓用什么连接？"

**期望答案要点**：
- Java → kes-java (JDBC)
- Spring Boot → kes-hibernate (MyBatis/Hibernate)
- Vue → 无直接连接，通过后端 API

**验证方法**：答案给出正确的技能引用

---

## 测试用例 2: 连接池配置

**场景**：需要配置 HikariCP 连接池

**输入问题**："连接池 max_connections 怎么算？"

**期望答案要点**：
- `max_connections >= sum(m maximumPoolSize) × 实例数 + superuser_reserved_connections`
- 3 实例 × 50 = 153，建议 200

**验证方法**：答案使用正确的计算公式
