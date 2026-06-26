# Increment Code Unit Test Creator

为 Java/Maven 项目生成 JUnit 5 + Mockito 单元测试，覆盖增量代码变更，目标覆盖率 90%~100%。

## 功能

- **增量代码感知**：自动对比 `main`/`master` 分支，识别新增/修改的方法
- **全量测试生成**：为指定类全量生成单元测试，覆盖率 90%~100%
- **全 Mock 策略**：所有外部依赖使用 Mockito 模拟，不编写集成测试
- **源码深度读取**：生成测试前读取依赖类，构造有意义的测试对象
- **跳过测试类**：不对测试类本身生成测试

## 依赖

### 工具
- Git（增量代码对比）
- Maven（项目构建、测试运行）

### Maven 依赖
- JUnit 5 (junit-jupiter 5.9+)
- Mockito (mockito-core 5.x)
- Mockito JUnit Jupiter (mockito-junit-jupiter 5.x)

## 使用

当需要为 Java 类生成单元测试时，激活此 skill：
- "为 UserService 生成单元测试"
- "为增量代码生成测试"
- "补充 OrderService 的测试覆盖"

## 版本

| 版本 | 日期 | 作者 | 变更 |
|------|------|------|------|
| 1.0.0 | 2026-04-15 | endcy | 初始版本 |
