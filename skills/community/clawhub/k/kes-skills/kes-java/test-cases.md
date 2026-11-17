---
name: kes-java
description: KingbaseES Java/JDBC 连接 — 测试用例
---

# KingbaseES Java/JDBC 测试用例

## 测试用例 1: Java JDBC 基础连接

**场景**：用户需要在 Java 项目中连接 KingbaseES 数据库

**输入问题**："Java 怎么连接金仓数据库？用 Maven"

**期望答案要点**：
- Maven 依赖：`cn.com.kingbase:kingbase8:9.0.0`
- 驱动类名：`com.kingbase8.Driver`
- JDBC URL 格式：`jdbc:kingbase8://host:port/db`
- 默认端口：54321

**验证方法**：答案包含正确的 Maven 坐标、驱动类名和 URL 前缀

---

## 测试用例 2: JDK 版本兼容性

**场景**：用户使用 JDK 1.7，不确定用哪个驱动版本

**输入问题**："我用 JDK 1.7，金仓 JDBC 驱动用哪个版本？"

**期望答案要点**：
- 使用 `kingbase8-9.0.0.jre7.jar`
- Maven 坐标：`cn.com.kingbase:kingbase8:9.0.0.jre7`
- JDK 1.6 用 `.jre6`，JDK 1.8+ 用默认版本

**验证方法**：答案正确匹配 JDK 版本与驱动版本

---

## 测试用例 3: JDBC 国密算法

**场景**：用户需要在 Java 项目中使用国密算法连接

**输入问题**："金仓数据库 Java 连接怎么用 SM3/SM4 国密算法？"

**期望答案要点**：
- 添加 BouncyCastle 依赖：`org.bouncycastle:bcprov-jdk18on:1.80`
- JDBC 驱动本身已支持国密

**验证方法**：答案提及 BouncyCastle 依赖

---

## 测试用例 4: HikariCP 连接池

**场景**：生产环境需要配置 HikariCP 连接池

**输入问题**："HikariCP 怎么配置金仓数据库连接池？"

**期望答案要点**：
- `setDriverClassName("com.kingbase8.Driver")`
- `setJdbcUrl("jdbc:kingbase8://...")`
- 建议参数：maximumPoolSize、minimumIdle、connectionTimeout

**验证方法**：答案包含完整的 HikariCP 配置
