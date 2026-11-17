# 故障排查指南

## 构建阶段错误

### `mvn clean package` 报错：无法解析依赖

**症状**：`Could not resolve dependencies` 或 `Failed to read artifact descriptor`

**原因**：
- Maven 仓库连接问题
- Jenkins 版本对应的 Parent POM 不存在

**解决**：
1. 检查 `pom.xml` 中 `<repositories>` 是否指向 `https://repo.jenkins-ci.org/public/`
2. 确认 Parent POM 版本是否真实存在：访问 https://github.com/jenkinsci/plugin-pom/tags
3. 如果网络环境受限，可改用代理或本地 Nexus：
   ```xml
   <url>https://mirrors.aliyun.com/nexus/content/groups/public/</url>
   ```

### `mvn clean package` 报错：Unsupported class file major version

**症状**：`java.lang.UnsupportedClassFileVersionError`

**原因**：`pom.xml` 中 `<java.level>` 设置的 Java 版本与本地 JDK 不匹配。

**解决**：
1. 运行 `java -version` 确认本地 JDK 版本
2. 确保 `pom.xml` 中 `<java.level>` 不超过本地 JDK 版本
3. Jenkins 2.401+ 要求 JDK 11+，Jenkins 2.426+ 要求 JDK 17+

### `mvn hpi:run` 报错：端口被占用

**症状**：`Address already in use` 或 `Port 8080 is already in use`

**解决**：
```bash
mvn hpi:run -Djetty.port=9090
```

---

## 版本兼容性

### Jenkins 版本与 JDK 对照

| Jenkins 版本 | 最低 JDK |
|-------------|---------|
| 2.361 - 2.419 | JDK 11 |
| 2.420 - 2.462 | JDK 17 |
| 2.463+ | JDK 17 或 JDK 21 |

### Jenkins 版本与 Plugin Parent 对照

| Jenkins 版本 | Plugin Parent 版本 |
|-------------|-------------------|
| 2.361.x | 4.66 |
| 2.401.x | 4.75 |
| 2.426.x | 4.80 |
| 2.440.x | 4.83 |
| 2.462.x | 4.85 |

> 完整对照表：https://github.com/jenkinsci/plugin-pom#changelog

---

## 安装阶段错误

### 上传 .hpi 后 Jenkins 提示「找不到依赖」

**原因**：生成的 `pom.xml` 中 `jenkins.version` 高于当前运行的 Jenkins 版本。

**解决**：确保 `jenkins.version` ≤ 实际运行的 Jenkins 版本。

### 插件安装后不显示

**解决**：
1. 进入 **Manage Jenkins** → **Manage Plugins** → **Installed**，搜索插件名称
2. 检查 Jenkins 日志（**Manage Jenkins** → **System Log**）是否有异常
3. 确认扩展点类型对应的 UI 入口（Builder 在项目配置中，Publisher 在构建后操作中）

---

## 运行时错误

### 配置界面不显示或报错

**症状**：保存配置时报错 `java.lang.NullPointerException` 或页面空白

**解决**：
1. 检查 `config.jelly` 中 `field` 属性是否与 Java 类中 getter/setter 一致
2. 检查 `@DataBoundConstructor` 参数是否与 `config.jelly` 字段匹配
3. 查看 Jenkins 日志确认具体堆栈

### 异步任务未执行

**解决**：
1. 检查 `getRecurrencePeriod()` 返回值单位（`MIN` = 分钟），默认 5 分钟触发一次
2. 确认类上是否有 `@Extension` 注解
3. 进入 **Manage Jenkins** → **System Log** 查看是否有相关日志
