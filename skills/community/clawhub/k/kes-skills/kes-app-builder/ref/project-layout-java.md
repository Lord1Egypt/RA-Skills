# Java 项目结构参考（KingbaseES）

标准的 Spring Boot + MyBatis 项目布局，适用于 KingbaseES 集成。

## 目录结构

```
myapp/
├── pom.xml
├── src/
│   ├── main/
│   │   ├── java/com/example/myapp/
│   │   │   ├── MyApplication.java          # 启动类
│   │   │   ├── config/
│   │   │   │   ├── DataSourceConfig.java   # 数据源配置
│   │   │   │   └── KesConfig.java          # KingbaseES 特定配置
│   │   │   ├── controller/
│   │   │   │   └── EmployeeController.java
│   │   │   ├── service/
│   │   │   │   ├── EmployeeService.java
│   │   │   │   └── impl/
│   │   │   │       └── EmployeeServiceImpl.java
│   │   │   ├── mapper/                     # MyBatis Mapper
│   │   │   │   └── EmployeeMapper.java
│   │   │   ├── model/
│   │   │   │   ├── Employee.java           # 实体
│   │   │   │   └──.dto/                    # 数据传输对象
│   │   │   └── exception/
│   │   │       └── GlobalExceptionHandler.java
│   │   ├── resources/
│   │   │   ├── application.yml             # 主配置
│   │   │   ├── application-dev.yml         # 开发环境
│   │   │   ├── application-prod.yml        # 生产环境
│   │   │   ├── mapper/                     # MyBatis XML
│   │   │   │   └── EmployeeMapper.xml
│   │   │   └── db/migration/               # Flyway 迁移
│   │   │       ├── V1__init.sql
│   │   │       └── V2__add_index.sql
│   └── test/
│       └── java/com/example/myapp/
│           └── MyApplicationTests.java
└── README.md
```

## Maven 依赖

```xml
<dependencies>
    <!-- Spring Boot -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>

    <!-- KingbaseES JDBC -->
    <dependency>
        <groupId>cn.com.kingbase</groupId>
        <artifactId>kingbase8</artifactId>
        <version>9.0.0</version>
    </dependency>

    <!-- MyBatis -->
    <dependency>
        <groupId>org.mybatis.spring.boot</groupId>
        <artifactId>mybatis-spring-boot-starter</artifactId>
        <version>3.0.3</version>
    </dependency>

    <!-- HikariCP (Spring Boot 内置) -->
    <!-- Flyway -->
    <dependency>
        <groupId>org.flywaydb</groupId>
        <artifactId>flyway-core</artifactId>
    </dependency>
</dependencies>
```

## application.yml 示例

```yaml
spring:
  datasource:
    driver-class-name: com.kingbase8.Driver
    url: jdbc:kingbase8://localhost:54321/test
    username: SYSTEM
    password: 123456
  flyway:
    enabled: true
    locations: classpath:db/migration

mybatis:
  mapper-locations: classpath:mapper/*.xml
  type-aliases-package: com.example.myapp.model
```
