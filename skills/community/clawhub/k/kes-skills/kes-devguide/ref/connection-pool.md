# 连接池配置

## 概述

连接池是应用和数据库之间的中间层，通过复用连接减少建立/关闭连接的开销。合理配置连接池对数据库性能至关重要。

## 通用原则

1. **连接池大小**：根据并发量调整，一般为 CPU 核心数的 2-4 倍
2. **空闲超时**：设置合理的 `idleTimeout`，避免长时间空闲连接
3. **最大生命周期**：设置 `maxLifetime`，定期回收连接（建议 30 分钟）
4. **连接测试**：启用连接有效性检查，避免使用已断开的连接
5. **数据库侧配置**：`max_connections` 和 `superuser_reserved_connections` 需预留足够连接数

```ini
# kingbase.conf
max_connections = 100
superuser_reserved_connections = 3
```

## HikariCP

HikariCP 是性能最优的 Java 连接池，推荐作为默认选择。

### Spring XML 配置

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
    <property name="validationTimeout" value="5000" />
    <property name="connectionTestQuery" value="SELECT 1" />
</bean>
```

### 参数说明

| 参数 | 说明 | 推荐值 |
|------|------|--------|
| maximumPoolSize | 最大连接数 | CPU 核心数 × 2-4 |
| minimumIdle | 最小空闲连接 | 5-10 |
| connectionTimeout | 获取连接超时（毫秒） | 30000 |
| idleTimeout | 空闲连接超时（毫秒） | 600000（10 分钟） |
| maxLifetime | 连接最大生命周期（毫秒） | 1800000（30 分钟） |
| connectionTestQuery | 连接测试 SQL | `SELECT 1` |

## Druid

Druid 提供完善的监控和 SQL 防火墙功能。

### Spring XML 配置

```xml
<bean id="dataSource_druid" class="com.alibaba.druid.pool.DruidDataSource" init-method="init" destroy-method="close">
    <property name="driverClassName" value="${jdbc.driver}" />
    <property name="url" value="${jdbc.url}" />
    <property name="username" value="${jdbc.username}" />
    <property name="password" value="${jdbc.password}" />
    <property name="initialSize" value="5" />
    <property name="maxActive" value="50" />
    <property name="minIdle" value="5" />
    <property name="timeBetweenEvictionRunsMillis" value="60000" />
    <property name="minEvictableIdleTimeMillis" value="1800000" />
    <property name="validationQuery" value="SELECT 'x'" />
    <property name="filters" value="stat,log4j" />
</bean>
```

### 注意事项

- `wall` 过滤器（SQL 注入防御）**不支持**国产数据库，不要启用
- 必须显式配置 `driverClassName`

### 参数说明

| 参数 | 说明 | 推荐值 |
|------|------|--------|
| initialSize | 初始化连接数 | 5 |
| maxActive | 最大活跃连接数 | 50 |
| minIdle | 最小空闲连接数 | 5 |
| timeBetweenEvictionRunsMillis | 检测间隔（毫秒） | 60000 |
| minEvictableIdleTimeMillis | 最小空闲时间（毫秒） | 1800000 |
| validationQuery | 连接验证 SQL | `SELECT 'x'` |
| filters | 监控过滤器 | `stat,log4j` |

## DBCP

Apache Commons DBCP，基础连接池实现。

### Spring XML 配置

```xml
<bean id="dataSource_dbcp" class="org.apache.commons.dbcp.BasicDataSource" destroy-method="close">
    <property name="driverClassName" value="${jdbc.driver}" />
    <property name="url" value="${jdbc.url}" />
    <property name="username" value="${jdbc.username}" />
    <property name="password" value="${jdbc.password}" />
    <property name="initialSize" value="5" />
    <property name="maxTotal" value="50" />
    <property name="minIdle" value="5" />
    <property name="timeBetweenEvictionRunsMillis" value="60000" />
    <property name="minEvictableIdleTimeMillis" value="1800000" />
    <property name="validationQuery" value="SELECT 'x'" />
</bean>
```

## C3P0

C3P0 是成熟的开源连接池。

### c3p0-config.xml 配置

```xml
<c3p0-config>
    <named-config name="database">
        <property name="user">SYSTEM</property>
        <property name="password">MANAGER</property>
        <property name="driverClass">com.kingbase8.Driver</property>
        <property name="jdbcUrl">jdbc:kingbase8://127.0.0.1:54321/TEST</property>
        <property name="initialPoolSize">5</property>
        <property name="maxPoolSize">50</property>
        <property name="minPoolSize">5</property>
        <property name="maxIdleTime">1800</property>
        <property name="preferredTestQuery">select 1</property>
        <property name="idleConnectionTestPeriod">10</property>
        <property name="acquireIncrement">3</property>
    </named-config>
</c3p0-config>
```

### 参数说明

| 参数 | 说明 | 推荐值 |
|------|------|--------|
| initialPoolSize | 初始连接数 | 5 |
| maxPoolSize | 最大连接数 | 50 |
| minPoolSize | 最小连接数 | 5 |
| maxIdleTime | 最大空闲时间（秒） | 1800 |
| idleConnectionTestPeriod | 空闲检测周期（秒） | 10 |
| acquireIncrement | 连接不足时增量 | 3 |

## Node.js 连接池

使用 `kb` 包内置的 Pool。

```javascript
const { Pool } = require('kb');

const pool = new Pool({
    user: 'SYSTEM',
    host: '127.0.0.1',
    database: 'TEST',
    password: '123456',
    port: 54321,
    max: 20,
    idleTimeoutMillis: 30000,
    connectionTimeoutMillis: 2000,
});
```

## 连接数计算公式

```
max_connections >= sum(各应用连接池 maximumPoolSize) × 实例数 + superuser_reserved_connections
```

示例：3 个应用实例，每实例 HikariCP maximumPoolSize=50

```
max_connections >= 50 × 3 + 3 = 153
```

建议设置 `max_connections = 200` 预留缓冲。
