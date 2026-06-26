# Maven 依赖配置参考

## 必需依赖

### JUnit 5

```xml
<dependency>
    <groupId>org.junit.jupiter</groupId>
    <artifactId>junit-jupiter</artifactId>
    <version>5.9.3</version>
    <scope>test</scope>
</dependency>
```

### Mockito

```xml
<dependency>
    <groupId>org.mockito</groupId>
    <artifactId>mockito-core</artifactId>
    <version>4.11.0</version>
    <scope>test</scope>
</dependency>
<dependency>
    <groupId>org.mockito</groupId>
    <artifactId>mockito-junit-jupiter</artifactId>
    <version>4.11.0</version>
    <scope>test</scope>
</dependency>
```

> **注意**: 如果项目使用 Java 11+，可升级 Mockito 到 5.x。Java 8 项目必须使用 Mockito 4.11.x 或更低版本。

### Mockito Inline（可选，用于 mock static/final 方法）

```xml
<dependency>
    <groupId>org.mockito</groupId>
    <artifactId>mockito-inline</artifactId>
    <version>5.2.0</version>
    <scope>test</scope>
</dependency>
```

## 构建插件配置

### Maven Surefire（JUnit 5 测试运行器）

```xml
<build>
    <plugins>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-surefire-plugin</artifactId>
            <version>3.1.2</version>
        </plugin>
    </plugins>
</build>
```

### JaCoCo 覆盖率插件（可选）

```xml
<build>
    <plugins>
        <plugin>
            <groupId>org.jacoco</groupId>
            <artifactId>jacoco-maven-plugin</artifactId>
            <version>0.8.11</version>
            <executions>
                <execution>
                    <goals>
                        <goal>prepare-agent</goal>
                    </goals>
                </execution>
                <execution>
                    <id>report</id>
                    <phase>test</phase>
                    <goals>
                        <goal>report</goal>
                    </goals>
                </execution>
            </executions>
        </plugin>
    </plugins>
</build>
```

## 完整配置示例

将以下内容添加到 `pom.xml` 的 `<dependencies>` 和 `<build>` 部分：

```xml
<!-- 在 <dependencies> 中添加 -->
<dependencies>
    <!-- 其他现有依赖 ... -->

    <!-- 单元测试依赖 -->
    <dependency>
        <groupId>org.junit.jupiter</groupId>
        <artifactId>junit-jupiter</artifactId>
        <version>5.9.3</version>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>org.mockito</groupId>
        <artifactId>mockito-core</artifactId>
        <version>4.11.0</version>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>org.mockito</groupId>
        <artifactId>mockito-junit-jupiter</artifactId>
        <version>4.11.0</version>
        <scope>test</scope>
    </dependency>
</dependencies>

<!-- 在 <build><plugins> 中添加 -->
<build>
    <plugins>
        <!-- 其他现有插件 ... -->

        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-surefire-plugin</artifactId>
            <version>3.1.2</version>
        </plugin>
    </plugins>
</build>
```

## 验证安装

添加依赖后，执行以下命令验证：

```bash
# 编译测试代码
mvn test-compile

# 运行所有测试
mvn test

# 生成覆盖率报告（如果配置了 JaCoCo）
mvn test jacoco:report
```

## 版本兼容性

| JUnit 5 | Mockito | Mockito Inline | Java 版本 |
|---------|---------|----------------|-----------|
| 5.9.x | 4.11.x | 4.11.x | Java 8+ |
| 5.9.x | 5.5.x | 5.2.x | Java 11+ |

Java 8 项目必须使用 Mockito 4.11.x 或更低版本（Mockito 5.x 需要 Java 11+）。
