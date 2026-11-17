---
name: kes-java
name_for_command: kes-java
description: 指导用户完成Java连接KingbaseES数据库。当用户提到Java开发、JDBC驱动、Maven依赖、HikariCP连接池、国密算法连接时，必须使用此技能。
---

# KingbaseES Java/JDBC 连接指南

本技能指导用户完成 Java 连接 KingbaseES 的完整流程，涵盖 JDBC 驱动安装、连接参数、连接池配置、SSL/TLS 和国密算法。

## 环境准备

> **重要提示**：KingbaseES JDBC 驱动支持 JDK 1.6 及以上版本。

```bash
java -version
mvn --version
```

## 安装 JDBC 驱动

### Maven（推荐）

```xml
<!-- JDK 1.8+ -->
<dependency>
    <groupId>cn.com.kingbase</groupId>
    <artifactId>kingbase8</artifactId>
    <version>9.0.0</version>
</dependency>

<!-- JDK 1.7+ -->
<dependency>
    <groupId>cn.com.kingbase</groupId>
    <artifactId>kingbase8</artifactId>
    <version>9.0.0.jre7</version>
</dependency>

<!-- JDK 1.6+ -->
<dependency>
    <groupId>cn.com.kingbase</groupId>
    <artifactId>kingbase8</artifactId>
    <version>9.0.0.jre6</version>
</dependency>
```

### 手动添加 JAR 包

驱动 JAR 位于 `$KINGBASE_HOME/Interface/jdbc/`：

| 文件 | JDK 版本 |
|------|----------|
| `kingbase8-9.0.0.jar` | JDK 1.8+ |
| `kingbase8-9.0.0.jre7.jar` | JDK 1.7+ |
| `kingbase8-9.0.0.jre6.jar` | JDK 1.6+ |

### Gradle

```groovy
implementation files('$KINGBASE_HOME/Interface/jdbc/kingbase8-9.0.0.jar')
```

## 基本连接

```java
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.Statement;

public class KesJdbcTest {
    public static void main(String[] args) {
        String driver = "com.kingbase8.Driver";
        String url = "jdbc:kingbase8://127.0.0.1:54321/test";
        String user = "SYSTEM";
        String password = "123456";

        try {
            Class.forName(driver);
            Connection conn = DriverManager.getConnection(url, user, password);
            System.out.println("连接成功！");

            Statement stmt = conn.createStatement();
            ResultSet rs = stmt.executeQuery("SELECT 1 FROM dual");

            if (rs.next()) {
                System.out.println("查询结果: " + rs.getInt(1));
            }

            rs.close();
            stmt.close();
            conn.close();

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

## URL 格式

```
jdbc:kingbase8://host:port/database?initParams=nocount=off;enable_automatic_block=on
```

**常用连接参数**：
- `nocount=off`：不显示影响的行数信息
- `enable_automatic_block=on`：启用自动块传输

## HikariCP 连接池

```java
import com.zaxxer.hikari.HikariConfig;
import com.zaxxer.hikari.HikariDataSource;

HikariConfig config = new HikariConfig();
config.setDriverClassName("com.kingbase8.Driver");
config.setJdbcUrl("jdbc:kingbase8://127.0.0.1:54321/test");
config.setUsername("SYSTEM");
config.setPassword("123456");
config.setMaximumPoolSize(10);
config.setMinimumIdle(2);
config.setConnectionTimeout(30000);
config.setIdleTimeout(600000);
config.setMaxLifetime(1800000);

HikariDataSource dataSource = new HikariDataSource(config);
```

## 国密算法支持

如需使用 SM3/SM4 国密算法，需额外添加 BouncyCastle 依赖：

```xml
<dependency>
    <groupId>org.bouncycastle</groupId>
    <artifactId>bcprov-jdk18on</artifactId>
    <version>1.80</version>
</dependency>
```

## SSL/TLS 安全连接

```java
String url = "jdbc:kingbase8://host:54321/test"
    + "?ssl=true"
    + "&sslcert=/path/to/client.crt"
    + "&sslkey=/path/to/client.key"
    + "&sslrootcert=/path/to/ca.crt";
```

## 高可用主从连接

```java
// 使用 replicationToken 切换连接
String url = "jdbc:kingbase8://primary:54321/test"
    + "?replicationToken=primary:54321,standby:54321";
```

## 常见问题

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| `ClassNotFoundException: com.kingbase8.Driver` | JDBC 驱动未添加 | 检查 Maven 依赖或 CLASSPATH |
| `无法加载 libkci` | 环境变量未设置 | 设置 `LD_LIBRARY_PATH` 指向 `$KINGBASE_HOME/lib` |
| `连接被拒绝` | 端口/地址错误 | 检查端口（默认 54321）和 `sys_hba.conf` |
| `编码错误` | 字符集不匹配 | 确保数据库与客户端编码一致（推荐 UTF-8） |
