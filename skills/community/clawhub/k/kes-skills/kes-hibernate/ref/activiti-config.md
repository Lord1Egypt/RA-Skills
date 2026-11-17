# Activiti 工作流适配配置

## 概述

Activiti 工作流引擎可适配 KingbaseES 作为底层数据库，需使用 PostgreSQL 形态配置。

## Spring Boot + Activiti 配置

### application.yml

```yaml
spring:
  datasource:
    driver-class-name: com.kingbase8.Driver
    url: jdbc:kingbase8://localhost:54321/test
    username: SYSTEM
    password: 123456

  activiti:
    # 自动创建/更新工作流表
    database-schema-update: true
    # 数据库类型设置为 postgres
    database-type: postgres
    # 检查流程部署
    check-process-definitions: false
```

### Maven 依赖

```xml
<dependencies>
    <!-- Spring Boot Activiti Starter -->
    <dependency>
        <groupId>org.activiti</groupId>
        <artifactId>activiti-spring-boot-starter</artifactId>
        <version>7.1.0.M1</version>
    </dependency>

    <!-- KingbaseES JDBC -->
    <dependency>
        <groupId>cn.com.kingbase</groupId>
        <artifactId>kingbase8</artifactId>
        <version>9.0.0</version>
    </dependency>
</dependencies>
```

## 纯 Activiti 配置（非 Spring Boot）

### activiti.cfg.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans">

    <bean id="processEngineConfiguration"
          class="org.activiti.engine.impl.cfg.StandaloneProcessEngineConfiguration">

        <property name="jdbcDriver" value="com.kingbase8.Driver"/>
        <property name="jdbcUrl" value="jdbc:kingbase8://localhost:54321/test"/>
        <property name="jdbcUsername" value="SYSTEM"/>
        <property name="jdbcPassword" value="123456"/>

        <!-- 数据库类型设为 postgres -->
        <property name="databaseType" value="postgres"/>

        <!-- 自动建表 -->
        <property name="databaseSchemaUpdate" value="true"/>

    </bean>

</beans>
```

## 工作流表说明

Activiti 会自动创建 25 张表（ACT_ 前缀）：

| 表前缀 | 用途 |
|--------|------|
| ACT_RE_* | 资源库表，存储流程定义 |
| ACT_RU_* | 运行时表，存储流程实例、任务 |
| ACT_HI_* | 历史表，存储历史流程实例 |
| ACT_GE_* | 通用表，存储通用数据 |
| ACT_ID_* | 身份表，存储用户、组信息 |

## 注意事项

1. 必须使用 `databaseType=postgres`，不可使用 `oracle` 或 `mssql`
2. `databaseSchemaUpdate=true` 会在无表时自动创建
3. KingbaseES 兼容模式需关闭（Oracle 模式可能导致语法冲突）
4. 大对象（BLOB/CLOB）存储流程定义时需确保类型映射正确
5. 长事务流程需注意连接池 `maxLifetime` 设置

## 常见问题

### 问题1：建表失败

**原因**：数据库类型设置错误或驱动不兼容

**解决**：确认 `databaseType=postgres` 且使用 KingbaseES JDBC 驱动

### 问题2：流程定义无法部署

**原因**：BLOB 类型不兼容或兼容模式开启

**解决**：关闭 Oracle 兼容模式，使用标准 PostgreSQL 语法
