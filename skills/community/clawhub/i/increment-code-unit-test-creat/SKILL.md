---
name: increment-code-unit-test-creator
description: Use when generating JUnit 5 + Mockito unit tests for Java/Maven source code, especially for incremental changes on a git branch. Activates when user asks to create unit tests, generate test coverage, add tests for changed code, or write tests for Java classes. Supports full class test generation and incremental diff-based test updates against main/master branch.
---

# Increment Code Unit Test Creator - 增量代码单元测试生成器

> 为 Java/Maven 项目生成 JUnit 5 + Mockito 单元测试，覆盖增量代码变更，目标覆盖率 90%~100%

## 核心特性

**增量代码感知**:
- 自动检测 Git 仓库，对比 `main`（或 `master`）分支获取增量变更
- 精准定位新增/修改的方法、字段、类
- 仅针对变更部分生成或补充测试，不重复已有覆盖

**全量测试生成**:
- 指定类或包路径时，若对应测试类不存在则全量生成
- 目标覆盖率 90%~100%，确保方法级别覆盖

**全 Mock 策略**:
- 所有外部依赖（数据库、Redis、HTTP 调用、消息队列等）使用 Mockito 模拟
- 不编写集成测试，避免数据依赖导致的不稳定性

**源码深度读取**:
- 生成测试前读取依赖的方法、类、对象定义
- 构造真实对象时传入有意义的属性值，不使用空对象

**仅测源码**:
- 绝不针对测试类本身生成单元测试
- 跳过 `*Test.java`、`*Spec.java`、`*TestCase.java` 等文件

---

## 激活条件

当用户提到以下关键词时激活：
- "生成单元测试"
- "为这个类写测试"
- "为增量代码生成测试"
- "补充单元测试"
- "代码变更测试"
- "提高测试覆盖率"
- "incremental test"
- "unit test for changed code"
- "generate tests"

**与全项目测试生成的区别**:
- 本 skill 聚焦于增量变更或指定类的精准测试生成
- 不是全项目批量扫描，而是按需、按需增量覆盖

---

## 依赖检查

### 必需工具

| 工具 | 用途 | 检查方式 |
|------|------|----------|
| **Git** | 获取增量代码差异 | `git --version` |
| **Maven** | 解析依赖、运行测试 | `mvn --version` |

### 必需测试依赖

在生成测试前，检查项目 `pom.xml` 是否包含以下依赖：

**第一步：检测 JDK 版本**

读取 `pom.xml` 中的 `<maven.compiler.source>` 或 `<java.version>` 属性，确定目标 JDK 版本：

| JDK 版本 | junit-jupiter | mockito-core | mockito-junit-jupiter |
|----------|---------------|--------------|----------------------|
| Java 8   | 5.9.x         | 4.11.0       | 4.11.0               |
| Java 11+ | 5.9.x         | 5.5.0        | 5.5.0                |

> **重要**: Mockito 5.x 编译后的 class 文件版本为 55.0 (Java 11+)，在 Java 8 项目中使用会导致编译失败。必须根据 JDK 版本选择对应的 Mockito 版本。

**第二步：检查依赖是否存在**

| 依赖 | 版本（按 JDK） | 作用域 |
|------|---------------|--------|
| `org.junit.jupiter:junit-jupiter` | Java 8→5.9.3 / Java 11+→5.9.3 | `test` |
| `org.mockito:mockito-core` | Java 8→4.11.0 / Java 11+→5.5.0 | `test` |
| `org.mockito:mockito-junit-jupiter` | Java 8→4.11.0 / Java 11+→5.5.0 | `test` |

**可选但推荐**:
- `org.mockito:mockito-inline` — 支持 static/final 方法 mock

**缺失处理**:
1. 提示用户项目缺少 JUnit 5 / Mockito 依赖
2. 展示需要添加的 Maven 依赖片段（见 [references/dependency-config.md](references/dependency-config.md)）
3. 询问用户是否自动添加到 `pom.xml`
4. 用户确认后自动添加并执行 `mvn test-compile` 验证

---

## 完整工作流程

### Step 0: 项目扫描与依赖检查

```bash
# 1. 确认是 Maven 项目（存在 pom.xml）
# 2. 检查测试依赖是否存在于 pom.xml
# 3. 确认是 Java 项目（src/main/java 目录存在）
```

**输出**: 依赖状态报告（完整 / 缺失需补充）

---

### Step 1: 增量代码分析（Git 仓库模式）

```bash
# 1. 确认默认分支（main 优先，不存在则 master）
git rev-parse --verify main 2>/dev/null || git rev-parse --verify master 2>/dev/null

# 2. 获取增量变更（与默认分支对比）
git diff <default-branch> --name-only --diff-filter=ACMR -- '*.java'

# 3. 排除测试文件
# 过滤掉 src/test/java 路径下的文件

# 4. 获取具体方法级变更
git diff <default-branch> -- src/main/java/包路径/类名.java

# 5. 解析变更类型
# - 新增类
# - 新增方法
# - 修改方法
# - 修改字段/依赖
```

**输出**: 增量变更清单（类 -> 方法 -> 变更类型）

---

### Step 2: 测试类存在性检查

```bash
# 对每个变更的源文件，检查对应测试类是否存在
# 源文件：src/main/java/com/example/service/UserService.java
# 测试文件：src/test/java/com/example/service/UserServiceTest.java

# 规则：
# - 测试类存在且测试方法已覆盖变更方法 -> 跳过
# - 测试类存在但未覆盖变更方法 -> 补充测试方法
# - 测试类不存在 -> 全量生成
```

---

### Step 3: 源码深度读取

在生成测试前，对目标类执行以下读取：

1. **读取目标类源码**：了解字段、依赖注入、方法签名
2. **读取依赖类/接口**：了解注入依赖的类型和方法签名
3. **读取依赖方法的实现**：了解返回类型、可能的异常
4. **读取相关 Entity/DTO/VO**：构造真实测试对象

**构造对象原则**:
- 传入有意义的属性值（非空、非 null、符合业务语义）
- 使用 Builder / 构造器 / 直接 set，遵循类的构造方式
- 对枚举、集合等非空字段赋默认值

**Lombok 特殊处理**（必须检查）:
- 检查目标类是否有 `@Setter(AccessLevel.NONE)` 或 `@Setter(AccessLevel.PROTECTED)` 注解
  - 如果字段被禁用 setter：**不要尝试反射设置该字段**，应检查其 getter 是否为计算型方法
  - 计算型 getter 通常返回多个字段运算后的值（如 `electricityAmount.add(serviceAmount)`），应设置参与计算的源字段
- 检查 `@Accessors(chain = true)` —— 此时 setter 返回自身而非 void，可直接链式调用
- 检查 `@FieldDefaults` —— 可能影响字段访问级别

---

### Step 4: 测试生成 / 补充

根据 Step 2 的结果选择策略：

#### 策略 A：全量生成（测试类不存在）

1. 为类中**每个 public 方法**生成至少一个测试方法
2. 覆盖以下场景：
   - 正常路径（Happy Path）
   - 边界条件（null、空集合、空字符串、极值）
   - 异常路径（抛出异常的情况）
   - 分支覆盖（if/else 各分支）
3. 所有外部依赖使用 `@Mock` + Mockito 模拟
4. 使用 `@InjectMocks` 注入被测实例
5. 目标覆盖率 90%~100%

#### 策略 B：增量补充（测试类已存在）

1. 识别增量代码中**未被现有测试覆盖**的方法
2. 为每个未覆盖方法生成新测试方法
3. 不修改已有通过的测试（除非变更破坏了原有逻辑）
4. 验证新增测试方法与已有测试不冲突

**跳过规则**（满足任一即跳过）：
- 纯 getter/setter 方法
- Lombok 注解生成的方法（`@Data`, `@Getter`, `@Setter`）
- `toString()`、`equals()`、`hashCode()`（除非手动实现且含业务逻辑）
- 仅包含日志输出的方法
- 委托方法（直接转发到另一个方法，无额外逻辑）

**必须测试**（满足任一即生成）：
- 包含条件判断（if/switch）的方法
- 包含循环遍历的方法
- 调用外部依赖的方法
- 包含异常处理（try/catch）的方法
- 包含数据转换/校验的方法
- 包含状态变更的方法

---

### Step 5: 测试编译验证

```bash
# 1. 编译测试代码
mvn test-compile -q

# 2. 如果编译失败，检查并修复
# - 导入缺失
# - 方法签名不匹配
# - 类型不匹配

# 3. 运行单个测试类验证
mvn test -Dtest=ClassNameTest -q
```

---

### Step 6: 覆盖率验证（可选）

```bash
# 使用 JaCoCo 验证覆盖率
mvn test jacoco:report -q

# 检查覆盖率报告
# target/site/jacoco/index.html

# 目标：方法覆盖率 >= 90%
```

**未达标处理**:
1. 识别未覆盖的方法/分支
2. 补充对应测试方法
3. 重新运行覆盖率检查
4. 重复直到达标

---

## 测试生成规则

### 测试类命名

```
源类名：UserService.java
测试类名：UserServiceTest.java

源类名：OrderServiceImpl.java
测试类名：OrderServiceImplTest.java
```

### 测试方法命名

```java
// 格式：[方法名]_[场景描述]_[期望结果]
@Test
void createOrder_validInput_returnsCreatedOrder() { }

@Test
void createOrder_nullInput_throwsIllegalArgumentException() { }

@Test
void getUser_notFound_returnsEmptyOptional() { }
```

### Mock 策略

```java
@ExtendWith(MockitoExtension.class)
class UserServiceTest {

    @Mock
    private UserRepository userRepository;

    @Mock
    private EmailService emailService;

    @Mock
    private RedisTemplate<String, Object> redisTemplate;

    @InjectMocks
    private UserService userService;

    // 所有外部依赖都 @Mock，不写真实调用
}
```

### 测试方法覆盖清单

对每个被测 public 方法，至少覆盖：

| 场景 | 优先级 |
|------|--------|
| 正常输入，正常返回 | P0 |
| 输入为 null | P0 |
| 输入为空集合/空字符串 | P1 |
| 依赖抛出异常 | P1 |
| 分支条件各路径 | P0 |
| 边界值（0、-1、MAX） | P1 |
| 并发/线程安全（如适用） | P2 |

---

## 测试模板

详见 [references/test-template.md](references/test-template.md)

### 核心结构

```java
package com.example.service;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.BeforeEach;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.junit.jupiter.api.extension.ExtendWith;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
@DisplayName("UserService 单元测试")
class UserServiceTest {

    @Mock
    private UserRepository userRepository;

    @InjectMocks
    private UserService userService;

    @BeforeEach
    void setUp() {
        // 通用 mock 设置（如有）
    }

    @Test
    @DisplayName("创建用户 - 正常路径")
    void createUser_validInput_returnsUser() {
        // Given
        UserDTO dto = new UserDTO();
        dto.setName("test");
        dto.setEmail("test@example.com");
        when(userRepository.save(any(User.class))).thenReturn(new User("test"));

        // When
        User result = userService.createUser(dto);

        // Then
        assertNotNull(result);
        assertEquals("test", result.getName());
        verify(userRepository).save(any(User.class));
    }
}
```

---

## 常见问题排查

### Getter 返回 `null` 或 `0`，但字段已设置

**症状**: 测试中通过 `setField(value)` 设置了值，但 `obj.getField()` 返回 `null` 或默认值。

**排查步骤**:
1. 检查该 getter 是否为 **Lombok 自动生成**（简单返回字段值）还是 **手动实现的计算型方法**
2. 检查字段是否有 `@Setter(AccessLevel.NONE)` —— 如果有，getter 很可能也是计算型的
3. 读取 getter 的实现，找到它实际计算的源字段
4. 设置参与计算的源字段而非目标字段

**示例**:
```java
// 实际代码中:
// @Setter(AccessLevel.NONE)
// private BigDecimal chargeMoneyAmount;
// public BigDecimal getChargeMoneyAmount() {
//     return electricityAmount.add(serviceAmount);  // 计算型 getter
// }

// ❌ 错误：设置目标字段无效，因为 getter 不读它
field.set(order, BigDecimal.valueOf(6.0));

// ✅ 正确：设置参与计算的源字段
order.setElectricityAmount(BigDecimal.valueOf(6.0));
order.setServiceAmount(BigDecimal.ZERO);
```

### `any()` 匹配器导致 `NullPointerException`

**症状**: `when(mock.method(any(SomeClass.class))).thenReturn(...)` 在 stub 注册阶段抛出 NPE。

**原因**: 某些接口（特别是外部模块的接口）的方法在接收 null 参数时会直接抛出异常，而 `any()` 在 stub 注册阶段会先以 null 参数试探性调用。

**解决**: 使用 `doReturn()` + `nullable(Class)` 匹配器:
```java
doReturn(result).when(mockService).method(
    ArgumentMatchers.<SomeClass>nullable(SomeClass.class)
);
```

### Stubbing 参数数量不匹配

**症状**: `PotentialStubbingProblem` 异常，提示实际调用的参数数量与 stub 不一致。

**解决**:
- 确保 mock 的 `when()` 参数数量与实际调用一致
- 对于可能有多参数重载的方法，使用 `nullable()` 匹配器覆盖所有参数

### `@MockitoSettings(LENIENT)` vs `lenient().when()`

**原则**: 优先使用 `lenient().when()` 针对个别 stub，避免全局 `LENIENT`。

```java
// ✅ 推荐：仅对特定 stub 放宽
lenient().when(redisUtils.set(anyString(), any())).thenReturn(true);

// ⚠️ 谨慎使用：全局 lenient 会隐藏其他 stubbing 问题
@MockitoSettings(strictness = Strictness.LENIENT)
```

只有当多个 stub 存在参数数量/类型差异且难以精确匹配时，才使用全局 `LENIENT`。

---

## 错误处理

### pom.xml 找不到

```
问题：项目中不存在 pom.xml

解决:
1. 确认当前目录是否为 Maven 项目根目录
2. 如果是子模块，找到对应的 pom.xml
3. 如果确实不是 Maven 项目，提示用户本 skill 仅支持 Java/Maven
```

### Git 仓库不存在

```
问题：当前目录不是 Git 仓库

解决:
1. 如果用户指定了具体类/包路径，跳过增量分析，直接全量生成
2. 如果用户要求"增量测试"但无 Git，提示用户初始化 git 仓库
```

### main 和 master 分支都不存在

```
问题：git rev-parse --verify main 和 master 都失败

解决:
1. 列出所有远程分支：git branch -r
2. 询问用户应对比哪个分支
3. 或使用 git diff HEAD~1 作为替代（最近一次提交）
```

### 测试编译失败

```
问题：mvn test-compile 失败

解决:
1. 检查生成的测试代码导入是否正确
2. 检查方法签名是否与源类匹配
3. 检查 Mockito when/thenReturn 的返回类型
4. 修复后重新编译
```

### 覆盖率未达标

```
问题：JaCoCo 报告显示覆盖率低于 90%

解决:
1. 读取 JaCoCo 报告，识别未覆盖的方法/分支
2. 为每个未覆盖点生成补充测试
3. 重新运行覆盖率检查
4. 若仍有无法覆盖的分支（如防御性代码），在报告中说明原因
```

### 依赖类/方法不存在

```
问题：源码引用的依赖类在类路径中找不到

解决:
1. 检查是否为外部依赖（需 mvn dependency:resolve）
2. 检查是否为同项目其他模块（需先编译依赖模块）
3. 对找不到的依赖，使用 mock 占位，在测试注释中说明
```

---

## 使用示例

### 示例 1：为指定类生成全量单元测试

```
用户：为 UserService 生成单元测试

AI: 收到！开始执行单元测试生成流程：

Step 0: 项目扫描...
  ✅ Maven 项目确认
  ✅ JUnit 5 + Mockito 依赖存在

Step 1: 目标类分析...
  📄 com.example.service.UserService (120 行, 8 个 public 方法)

Step 2: 测试类存在性检查...
  ❌ UserServiceTest.java 不存在 -> 全量生成

Step 3: 源码深度读取...
  📖 UserService.java - 8 个 public 方法
  📖 UserRepository.java - 依赖接口
  📖 User.java - Entity 定义
  📖 UserDTO.java - 参数对象

Step 4: 全量测试生成...
  ✅ 生成 12 个测试方法（覆盖 8 个 public 方法）
  📝 UserServiceTest.java (350 行)

Step 5: 编译验证...
  ✅ mvn test-compile 通过
  ✅ mvn test -Dtest=UserServiceTest 通过（12/12 passed）

Step 6: 覆盖率验证...
  ✅ 方法覆盖率：95%（19/20 方法已覆盖）
  ✅ 分支覆盖率：88%

✅ 完成！测试类已生成：src/test/java/com/example/service/UserServiceTest.java
```

### 示例 2：增量代码测试补充

```
用户：为这次的增量代码生成单元测试

AI: 收到！开始执行增量测试流程：

Step 0: 项目扫描...
  ✅ Maven 项目确认
  ✅ 测试依赖存在

Step 1: 增量代码分析（对比 main 分支）...
  📊 发现 3 个变更文件：
    - UserService.java (+2 个方法)
    - OrderController.java (修改 1 个方法)
    - PaymentHelper.java (新增类)

Step 2: 测试类存在性检查...
  ✅ UserServiceTest.java 存在 -> 检查覆盖
  ✅ OrderControllerTest.java 存在 -> 检查覆盖
  ❌ PaymentHelperTest.java 不存在 -> 全量生成

Step 3: 增量方法覆盖分析...
  UserServiceTest:
    ❌ verifyEmail() - 未覆盖 -> 补充
    ❌ batchUpdate() - 未覆盖 -> 补充
  OrderControllerTest:
    ❌ updateOrderStatus() - 已修改，现有测试不覆盖新逻辑 -> 补充
  PaymentHelperTest:
    -> 全量生成（5 个 public 方法）

Step 4: 测试生成...
  ✅ UserServiceTest.java 补充 2 个测试方法
  ✅ OrderControllerTest.java 补充 1 个测试方法
  ✅ PaymentHelperTest.java 全量生成 8 个测试方法

Step 5: 编译验证...
  ✅ 全部通过

Step 6: 覆盖率验证...
  ✅ 变更方法覆盖率：100%

✅ 完成！共补充/生成 11 个测试方法
```

### 示例 3：缺少测试依赖

```
用户：为 OrderService 生成单元测试

AI: 收到！开始执行单元测试生成流程：

Step 0: 项目扫描...
  ✅ Maven 项目确认
  ❌ 缺少 JUnit 5 依赖
  ❌ 缺少 Mockito 依赖

⚠️ 检测到项目缺少单元测试必需依赖：

需要在 pom.xml 中添加以下依赖：
<dependencies>
    <dependency>
        <groupId>org.junit.jupiter</groupId>
        <artifactId>junit-jupiter</artifactId>
        <version>5.9.3</version>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>org.mockito</groupId>
        <artifactId>mockito-core</artifactId>
        <version>5.5.0</version>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>org.mockito</groupId>
        <artifactId>mockito-junit-jupiter</artifactId>
        <version>5.5.0</version>
        <scope>test</scope>
    </dependency>
</dependencies>

是否自动添加到 pom.xml？(y/n)

用户：y

AI: ✅ 依赖已添加到 pom.xml
    ✅ mvn test-compile 验证通过

继续生成 OrderService 单元测试...
```

---

## 配置项

### Maven Surefire 插件配置

为确保 JUnit 5 正确运行，检查 `pom.xml` 中是否配置了 Surefire 插件：

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
```

---

## 版本

| 版本 | 日期 | 作者 | 变更 |
|------|------|------|------|
| 1.0.0 | 2026-04-15 | endcy | 初始版本，支持 JUnit 5 + Mockito 增量/全量单元测试生成 |
