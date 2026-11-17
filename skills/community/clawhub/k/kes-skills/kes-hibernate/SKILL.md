---
name: kes-hibernate
name_for_command: kes-hibernate
description: KingbaseES Java 框架集成指南。当用户提到 Hibernate、MyBatis、MyBatis-Plus、Flyway、Liquibase、Activiti、JPA 方言配置时，必须使用此技能。
---

# KingbaseES Java 框架集成指南

本技能指导用户完成 KingbaseES 与 Java 框架的集成，涵盖 Hibernate、MyBatis/MyBatis-Plus、Flyway、Liquibase 和 Activiti。

## JDBC 基础配置

### Maven 依赖

```xml
<!-- JDK 1.8+ -->
<dependency>
    <groupId>cn.com.kingbase</groupId>
    <artifactId>kingbase8</artifactId>
    <version>9.0.0</version>
</dependency>
```

JDK 1.7 使用 `9.0.0.jre7`，JDK 1.6 使用 `9.0.0.jre6`。

### 连接参数

| 参数 | 说明 |
|------|------|
| driver | `com.kingbase8.Driver` |
| url | `jdbc:kingbase8://host:54321/database` |

### 国密支持

```xml
<dependency>
    <groupId>org.bouncycastle</groupId>
    <artifactId>bcprov-jdk18on</artifactId>
    <version>1.80</version>
</dependency>
```

### SSL 连接

```java
String url = "jdbc:kingbase8://host:54321/test" +
    "?ssl=true" +
    "&sslcert=/path/to/client.crt" +
    "&sslkey=/path/to/client.key" +
    "&sslrootcert=/path/to/ca.crt";
```

### 高可用连接

```java
String url = "jdbc:kingbase8://primary:54321/test?nodelist=primary:54321,standby:54321";
```

## Hibernate

### 基本配置

在 `persistence.xml` 或 `hibernate.cfg.xml` 中配置：

```xml
<property name="connection.driver_class">com.kingbase8.Driver</property>
<property name="connection.url">jdbc:kingbase8://host:54321/test</property>
<property name="connection.username">SYSTEM</property>
<property name="connection.password">123456</property>
```

### 注意事项

- 确保 Hibernate 版本与 KingbaseES 兼容
- 方言配置参考 KingbaseES 官方文档
- 验证 HQL 到 SQL 的转换正确性

## MyBatis / MyBatis-Plus

### 数据源配置

```xml
<dataSource type="POOLED">
    <property name="driver" value="com.kingbase8.Driver"/>
    <property name="url" value="jdbc:kingbase8://host:54321/test"/>
    <property name="username" value="SYSTEM"/>
    <property name="password" value="123456"/>
</dataSource>
```

### 动态 SQL

MyBatis 支持 `<if>`、`<choose>`、`<foreach>` 等动态标签，与 KingbaseES SQL 语法配合使用。

### MyBatis-Plus

配置与 MyBatis 相同，额外引入 MyBatis-Plus 依赖即可使用增强功能。

## Flyway

### 配置

```properties
flyway.url=jdbc:kingbase8://host:54321/test
flyway.user=SYSTEM
flyway.password=123456
flyway.locations=classpath:db/migration
```

### 迁移脚本命名

遵循 `V{版本号}__{描述}.sql` 格式：

```sql
-- V1__create_users_table.sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
```

## Liquibase

### 配置

```xml
<databaseChangeLog>
    <changeSet id="1" author="admin">
        <createTable tableName="users">
            <column name="id" type="INTEGER" autoIncrement="true">
                <constraints primaryKey="true"/>
            </column>
            <column name="username" type="VARCHAR(50)">
                <constraints nullable="false"/>
            </column>
        </createTable>
    </changeSet>
</databaseChangeLog>
```

## Activiti

### 数据源配置

Activiti 使用标准 JDBC 数据源，替换为 KingbaseES 驱动即可。注意验证 Activiti 内置表创建脚本与 KingbaseES 语法的兼容性。

## 参考文档

```
kes-hibernate/
├── SKILL.md             # 本文件
├── ref/
│   └── activiti-config.md   # Activiti 工作流适配配置
└── test-cases.md
```
