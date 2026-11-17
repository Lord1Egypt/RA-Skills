---
name: kes-devguide
name_for_command: kes-devguide
description: KingbaseES 应用开发最佳实践。当用户提到应用设计原则、连接池配置、OLTP 性能基准、客户端接口选型、开发规范时，必须使用此技能。
---

# KingbaseES 应用开发指南

本技能提供 KingbaseES 应用开发的最佳实践，涵盖客户端接口选型、连接池配置和应用设计原则。

## 客户端接口选型

| 语言 | 接口 | 技能 |
|------|------|------|
| Java | JDBC | kes-java |
| Python | ksycopg2 | kes-python |
| Go | gokb | kes-go |
| Node.js | kb | kes-nodejs |
| C/C++ | KCI / ODBC | kes-c-odbc |
| PHP | pdo_kdb | kes-php |
| Perl | DBD::KB | kes-perl |
| .NET | KDBNDP | kes-dotnet |
| Qt | qkingbase | kes-qt |

## 框架集成

| 框架 | 技能 |
|------|------|
| Hibernate / MyBatis / Flyway / Liquibase | kes-hibernate |
| SQLAlchemy / Django | kes-sqlalchemy |
| EF6 / EF Core | kes-dotnet |

## 应用设计原则

### 简洁性原则

- 表设计过于复杂即为不良设计
- SQL 过长无法被优化器处理说明存在问题
- 同一列上的重复索引表示索引设计不当
- 过多抽象层封装数据库调用是不良实践

### 表与索引设计

- 规范化到 3NF 保证灵活性，关键表选择性反规范化提升性能
- 索引设计是迭代过程：从 PK 和基础索引开始，测试阶段逐步优化
- 索引代价估算：在已索引键上的 INSERT/DELETE/UPDATE 代价约为实际 DML 的 3 倍。3 个索引时写入速度降至无索引表的约 1/10

### SQL 执行效率

- **连接管理**：最小化并发连接，复用连接
- **游标管理**：使用绑定变量启用软解析和 SQL 共享

```sql
-- 字符串字面量（每次硬解析）
SELECT * FROM employees WHERE first_name LIKE 'KING';

-- 绑定变量（启用软解析）
PREPARE em_plan(VARCHAR) AS SELECT * FROM employees WHERE first_name LIKE $1;
EXECUTE em_plan('KING');
```

### 实现指南（8 条规则）

1. 选择支持性能设计的开发环境
2. 专注于实现组件自身功能，而非其他组件的功能
3. 不忽略任何特性 — 数据归档和清理是最常被忽视的
4. 用过程语言（C、Java、PL/SQL）处理流程逻辑；用 SQL 处理数据访问
5. 缓存高频访问、低频变更的数据（如当前日期、用户名、税率、折扣率）
6. 优化组件间接口
7. 使用数据库外键约束而非应用层强制引用完整性
8. 配置操作名和模块标识以便端到端追踪

## 连接池配置

### 通用原则

1. **连接池大小**：根据并发量调整，一般为 CPU 核心数的 2-4 倍
2. **空闲超时**：设置合理的 `idleTimeout`，避免长时间空闲连接
3. **最大生命周期**：设置 `maxLifetime`，定期回收连接（建议 30 分钟）
4. **连接测试**：启用连接有效性检查
5. **数据库侧配置**：`max_connections` 和 `superuser_reserved_connections` 需预留足够连接数

```ini
# kingbase.conf
max_connections = 100
superuser_reserved_connections = 3
```

### HikariCP（推荐）

```xml
<bean id="dataSource_hikari" class="com.zaxxer.hikari.HikariDataSource" destroy-method="close">
    <property name="driverClassName" value="${jdbc.driver}" />
    <property name="jdbcUrl" value="${jdbc.url}" />
    <property name="username" value="${jdbc.username}" />
    <property name="password" value="${jdbc.password}" />
    <property name="minimumIdle" value="5" />
    <property name="maximumPoolSize" value="50" />
    <property name="connectionTimeout" value="10000" />
    <property name="idleTimeout" value="600000" />
    <property name="maxLifetime" value="1800000" />
    <property name="connectionTestQuery" value="SELECT 1" />
</bean>
```

### Druid

> **注意**：`wall` 过滤器（SQL 注入防御）**不支持**国产数据库，不要启用。

### 连接数计算公式

```
max_connections >= sum(各应用连接池 maximumPoolSize) × 实例数 + superuser_reserved_connections
```

示例：3 个应用实例，每实例 HikariCP maximumPoolSize=50
```
max_connections >= 50 × 3 + 3 = 153
```
建议设置 `max_connections = 200` 预留缓冲。

## OLTP 性能基准

测试结果（4 CPU 机器）：

| 测试场景 | 支持用户数 |
|---------|-----------|
| 无解析（全部缓存） | 270 |
| 全部软解析 | 150 |
| 全部硬解析 | 60 |
| 每次事务重新连接 | 30 |

## 参考文档

```
kes-devguide/
├── SKILL.md                    # 本文件
├── ref/
│   ├── development-spec.md     # 应用设计原则与规范
│   └── connection-pool.md      # 连接池配置（DBCP/C3P0/Druid/HikariCP）
└── test-cases.md
```
