# JAR 包冲突模式与解决方案参考手册

## 1. 冲突类型分类

### 1.1 版本冲突（Version Conflict）
同一 `groupId:artifactId` 在项目不同模块中被声明为不同版本。

**识别特征：**
- Maven `dependency:tree` 输出中出现 `(version managed from X.Y.Z)`
- 运行时出现 `NoSuchMethodError` / `NoClassDefFoundError` / `ClassNotFoundException`
- 日志出现 `Multiple SLF4J bindings were found`

**解决方案：**
```xml
<!-- 在父 POM 的 dependencyManagement 中统一版本 -->
<dependencyManagement>
  <dependencies>
    <dependency>
      <groupId>com.fasterxml.jackson.core</groupId>
      <artifactId>jackson-databind</artifactId>
      <version>2.15.2</version>
    </dependency>
  </dependencies>
</dependencyManagement>
```

### 1.2 已知不兼容对（Known Incompatible Pairs）
特定版本组合之间存在已知 API 不兼容问题。

**常见不兼容对：**

| 依赖 A | 依赖 B | 问题描述 |
|--------|--------|----------|
| Spring Boot 3.x | Spring Framework 5.x | Boot 3 必须配合 Spring 6 |
| Spring Boot 2.x | javax.servlet 5+ | Boot 2 使用 javax，Boot 3 迁移到 jakarta |
| logback-classic | log4j-slf4j-impl | SLF4J 只允许单一绑定 |
| log4j 1.x | log4j-core 2.x | 新旧 log4j 包名不同，会同时加载 |
| Hibernate 5.x | Spring Boot 3.x | Boot 3 需要 Hibernate 6.x |

### 1.3 重复 JAR（Duplicate JAR）
同一个库被打包进 fat-jar 的多个路径，或 lib 目录中存在两个版本文件。

**识别方法：**
```bash
# 检查 fat jar 内部重复
jar -tf app.jar | grep "\.class$" | sort | uniq -d

# 检查 lib 目录
ls target/dependency/ | sed 's/-[0-9].*//' | sort | uniq -d
```

---

## 2. Spring Boot 版本兼容矩阵

| Spring Boot | Spring Framework | Java | Hibernate | Tomcat |
|-------------|-----------------|------|-----------|--------|
| 3.2.x       | 6.1.x           | 17+  | 6.4.x     | 10.1.x |
| 3.1.x       | 6.0.x           | 17+  | 6.2.x     | 10.1.x |
| 3.0.x       | 6.0.x           | 17+  | 6.1.x     | 10.0.x |
| 2.7.x       | 5.3.x           | 8+   | 5.6.x     | 9.0.x  |
| 2.6.x       | 5.3.x           | 8+   | 5.6.x     | 9.0.x  |
| 2.5.x       | 5.3.x           | 8+   | 5.4.x     | 9.0.x  |

---

## 3. 常见冲突案例与修复

### 案例一：Jackson 版本混乱
**现象：** `InvalidDefinitionException` 或 JSON 序列化异常  
**根因：** 多个子模块引入不同版本的 `jackson-databind`

**修复：**
```xml
<properties>
  <jackson.version>2.15.2</jackson.version>
</properties>
<dependencyManagement>
  <dependencies>
    <dependency>
      <groupId>com.fasterxml.jackson</groupId>
      <artifactId>jackson-bom</artifactId>
      <version>${jackson.version}</version>
      <type>pom</type>
      <scope>import</scope>
    </dependency>
  </dependencies>
</dependencyManagement>
```

### 案例二：SLF4J 多重绑定
**现象：** 启动时打印 `SLF4J: Class path contains multiple SLF4J bindings`  
**根因：** 同时引入了 `logback-classic` 和 `slf4j-log4j12` 或 `log4j-slf4j-impl`

**修复：**
```xml
<!-- 排除多余的 SLF4J 绑定 -->
<dependency>
  <groupId>some-library</groupId>
  <artifactId>some-artifact</artifactId>
  <exclusions>
    <exclusion>
      <groupId>org.slf4j</groupId>
      <artifactId>slf4j-log4j12</artifactId>
    </exclusion>
  </exclusions>
</dependency>
```

### 案例三：javax → jakarta 迁移冲突（Spring Boot 3 升级）
**现象：** `ClassNotFoundException: javax.servlet.http.HttpServletRequest`  
**根因：** 部分依赖仍使用 `javax.*`，而 Spring Boot 3 已切换到 `jakarta.*`

**修复：**
```xml
<!-- 排除旧版 servlet -->
<dependency>
  <groupId>old-library</groupId>
  <artifactId>old-artifact</artifactId>
  <exclusions>
    <exclusion>
      <groupId>javax.servlet</groupId>
      <artifactId>javax.servlet-api</artifactId>
    </exclusion>
  </exclusions>
</dependency>
<!-- 显式引入 jakarta servlet -->
<dependency>
  <groupId>jakarta.servlet</groupId>
  <artifactId>jakarta.servlet-api</artifactId>
  <scope>provided</scope>
</dependency>
```

### 案例四：Guava 版本不兼容
**现象：** `NoSuchMethodError: com.google.common.collect.ImmutableList.of`  
**根因：** 不同子服务混用 Guava 18.x 和 30.x

**修复：**
```xml
<properties>
  <guava.version>32.1.3-jre</guava.version>
</properties>
<dependencyManagement>
  <dependencies>
    <dependency>
      <groupId>com.google.guava</groupId>
      <artifactId>guava</artifactId>
      <version>${guava.version}</version>
    </dependency>
  </dependencies>
</dependencyManagement>
```

### 案例五：Spring Cloud 与 Spring Boot 版本不匹配
**现象：** 启动失败，Bean 无法注入，Feign/Ribbon 异常

**兼容矩阵：**

| Spring Cloud | Spring Boot |
|--------------|-------------|
| 2023.0.x (Leyton) | 3.2.x |
| 2022.0.x (Kilburn) | 3.0.x / 3.1.x |
| 2021.0.x (Jubilee) | 2.6.x / 2.7.x |
| 2020.0.x (Ilford)  | 2.4.x / 2.5.x |
| Hoxton              | 2.2.x / 2.3.x |

**修复：使用官方 BOM**
```xml
<dependencyManagement>
  <dependencies>
    <dependency>
      <groupId>org.springframework.cloud</groupId>
      <artifactId>spring-cloud-dependencies</artifactId>
      <version>2023.0.1</version>
      <type>pom</type>
      <scope>import</scope>
    </dependency>
  </dependencies>
</dependencyManagement>
```

---

## 4. 最佳实践：微服务项目依赖管理

### 4.1 统一父 POM 策略
```
parent-pom/
  pom.xml  ← 声明所有三方依赖版本（dependencyManagement）
service-a/
  pom.xml  ← 继承 parent-pom，只声明需要的依赖（无版本号）
service-b/
  pom.xml  ← 同上
```

### 4.2 推荐使用 BOM（Bill of Materials）
```xml
<!-- Spring Boot BOM 自动管理数百个依赖版本 -->
<parent>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-parent</artifactId>
  <version>3.2.5</version>
</parent>
```

### 4.3 依赖冲突排查命令速查

```bash
# Maven: 查看完整依赖树
mvn dependency:tree

# Maven: 分析冲突（Enforcer 插件）
mvn enforcer:enforce

# Maven: 查找指定 artifact 来源
mvn dependency:tree -Dincludes=com.fasterxml.jackson.core:jackson-databind

# Gradle: 查看冲突解析
./gradlew dependencies --configuration compileClasspath

# Gradle: 强制统一版本
configurations.all {
    resolutionStrategy.force 'com.google.guava:guava:32.1.3-jre'
}
```

### 4.4 Maven Enforcer 插件（CI 强制检测）
```xml
<plugin>
  <groupId>org.apache.maven.plugins</groupId>
  <artifactId>maven-enforcer-plugin</artifactId>
  <executions>
    <execution>
      <id>enforce-dependency-convergence</id>
      <goals><goal>enforce</goal></goals>
      <configuration>
        <rules>
          <dependencyConvergence/>  <!-- 强制版本收敛 -->
          <bannedDependencies>      <!-- 禁止特定依赖 -->
            <excludes>
              <exclude>log4j:log4j</exclude>
            </excludes>
          </bannedDependencies>
        </rules>
      </configuration>
    </execution>
  </executions>
</plugin>
```

---

## 5. 常见异常与对应冲突原因速查

| 异常信息 | 可能的冲突原因 |
|----------|---------------|
| `NoSuchMethodError` | 运行时加载了旧版本 JAR（版本冲突） |
| `ClassNotFoundException` | 依赖被 exclusion 掉或 scope 不对 |
| `NoClassDefFoundError` | 类存在于编译期但运行时找不到 |
| `LinkageError` | 同一类被不同 ClassLoader 加载两次 |
| `IllegalAccessError` | Java 模块系统（JPMS）访问权限冲突 |
| `SLF4J multiple bindings` | 多个 SLF4J 实现同时存在 |
| `BeanDefinitionOverrideException` | Spring Boot 2.1+ 禁止 Bean 覆盖 |
| `HibernateException: Named query not found` | Hibernate 版本变更 API 不兼容 |
