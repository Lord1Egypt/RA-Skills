# 06 · 工具落地（设计 → 代码的最小映射）

> 本文件只固化"用错不报错但埋雷"的隐蔽型 API 坑（如测试假绿、污染其他测试、掩盖耦合）——查文档也未必意识到严重性的那种。即时报错型坑（注解拼错等）查文档 30 秒可得，不收录。

## §1 依赖：一句话定基线

**Spring Boot 项目**（第 0 步探测到 `spring-boot-starter-test` 或 parent）→ 什么都不用加，自带 JUnit 5 + Mockito：

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-test</artifactId>
    <scope>test</scope>
</dependency>
<!-- starter-test 还传递了 AssertJ / Hamcrest。断言默认用 JUnit 原生，仅在"集合内容断言/字段分组断言（同一逻辑组）"时升级到 AssertJ（见 SKILL.md"断言库策略"） -->
```

**非 Spring Boot 项目** → 逐库声明（仅项目无时；按需取用，不强加）：

```xml
<dependency><groupId>org.junit.jupiter</groupId><artifactId>junit-jupiter</artifactId><version>5.10.2</version><scope>test</scope></dependency>
<dependency><groupId>org.mockito</groupId><artifactId>mockito-core</artifactId><version>5.11.0</version><scope>test</scope></dependency>
<!-- 断言默认 JUnit 原生，集合内容断言/字段分组断言（同一逻辑组）时才升级 AssertJ；ArchUnit 仅"架构守护询问"（见 SKILL.md）触发时引入 -->
```

> 下面写法以 JUnit 5（Jupiter）为主；项目已有 TestNG / JUnit 4 → 跟随既有（栈中立，见 SKILL 铁律 3），JUnit 4 差异见 §4。

## §2 设计用例 → 测试代码：映射表

| 用例设计形态（01-05） | 落地代码 | 关键点 |
|---|---|---|
| 正向用例（有效等价类） | `assertEquals(expected, actual)` | 一个用例一个断言焦点 |
| 反向/异常用例（无效等价类） | `assertThrows(XxxException.class, () -> ...)` | 验异常**类型 + 消息**，不止类型 |
| 同方法多输入（等价类代表/边界） | `@ParameterizedTest` + `@CsvSource`/`@MethodSource` | 用例即数据，设计意图显式化 |
| 决策表每列（03） | 一个 `@Test`，或并入 `@ParameterizedTest` | 列=用例，不要塞进单个测试 |
| 状态机合法迁移（04） | `assertEquals(终态, obj.getState())` | 通过业务方法触发，不直接 setStatus |
| 状态机非法迁移（04） | `assertThrows(IllegalStateException.class, obj::op)` | 这是状态机测试的核心 |
| 需固定外部依赖 | Mock（见 §3） | 只 mock 外部依赖，不 mock 被测对象 |

## §3 Mock 边界（最易错处）

**只 Mock 外部依赖**（DB / RPC / 时间 / 第三方服务），**绝不 Mock**：
- 被测对象自身。
- 被测类**内部 `new` 出来的对象**（这是头号陷阱，见下）。

### 标准注入式 Mock（推荐）

```java
class OrderServiceTest {
    @Mock OrderRepository repo;      // 外部依赖：mock
    @Mock PaymentClient client;      // 外部依赖：mock
    @InjectMocks OrderService service; // 被测对象：真实，依赖被注入

    @BeforeEach void setup() { MockitoAnnotations.openMocks(this); }

    @Test void should_save_when_valid() {
        when(repo.existsById(anyLong())).thenReturn(false);  // stub
        service.create(order);
        verify(repo).save(order);                             // verify
    }
}
```

### 何时改用手工构造注入

`@InjectMocks` 是默认写法（简洁、和构造器注入天然适配）。以下场景手工 `new` 构造更清晰，跟随项目既有风格即可：

- 被测类有**多个构造器**或字段/构造器注入混用 → `@InjectMocks` 注入行为难预测，手工 `new` 传 mock 更可靠。
- 需要在构造时传入**非 mock 的真实值**（如固定 `Clock`、真实 `ObjectMapper`）→ 手工构造显式可控。
- 团队既有测试统一用手工构造 → 跟随，不为"统一"而迁移。

> 除上述"手工 `new` 构造"外，项目既定的**容器装配模式**（如 TestConfig 手写 `@Bean` mock 轻量容器 + `@Import` + `@Autowired` 真实被测对象）同样优先于 `@InjectMocks` 默认——跟随项目，见 SKILL.md S 级表「@MockBean 用于纯单元测试」行的说明。

> 状态机非法转移的异常类型（`IllegalStateException` vs 自定义业务异常）跟随项目既有，不强加。

### 头号陷阱：被测类内部 new 的对象不能 mock

```java
// ✗ 被测类自己 new 依赖
class BadService {
    public void doWork() {
        PaymentClient c = new PaymentClient();  // 内部 new，无法 mock
        c.pay();
    }
}
// 测试时无法干预 c → 测了等于没测，或要用 PowerMock 反射强插（坏味道）

// ✓ 重构为构造器注入，再 mock
class GoodService {
    private final PaymentClient client;          // 注入
    public GoodService(PaymentClient client) { this.client = client; }
}
```

### 静态方法 mock（最后手段）

```java
@Test void should_useMockedId() {
    try (MockedStatic<IdUtil> m = mockStatic(IdUtil.class)) {   // 必须 try-with-resources
        m.when(IdUtil::getId).thenReturn("FAKE_ID");
        assertEquals("FAKE_ID", service.genOrderId());
    }  // 离开块自动释放，不污染其他测试
}
```

- `mockStatic` 需 Mockito 3.4+。**工件坑**：Mockito 4.x 需额外引入 `mockito-inline`（仅 `mockito-core` 不够）；5.x 起默认 inline mock maker，`mockito-core` 即可。第 0 步探测 Mockito 版本时一并确认工件。
- **必须**包在 `try-with-resources`，否则静态 mock 泄漏到同线程其他测试。
- 优先重构为可注入实例方法；确需静态 mock 才用。

### 链式调用 / 参数对象 mock（MyBatis-Plus、JPA Query）

被测方法内部 `new` 查询条件对象（`LambdaQueryWrapper`/`Criteria`/`Specification`）再传给 mapper，是 ORM 场景常态。**这类"被测代码自构造的参数对象"不是外部依赖**——别去 mock wrapper 本身，直接对 mapper 方法用 `any()` 忽略参数内容：

```java
// 被测：service.findActive(name) 内部 new LambdaQueryWrapper().eq(...).eq(...) 再 selectOne(wrapper)
@Test void should_returnNull_when_notFound() {
    // ✗ 不要 when(mapper.selectOne(specificWrapper))...——wrapper 是被测方构造的，你重建不出同一实例
    // ✓ 用 any() 忽略 wrapper 内容，只 stub mapper 的返回
    when(mapper.selectOne(any(LambdaQueryWrapper.class))).thenReturn(null);
    assertNull(service.findActive("nobody"));
}
```

> 判别：wrapper 是被测代码 `new` 出来当**参数**传给 mapper 的（查询条件），属被测逻辑，不 mock——用 `any()` 放行。（区别于"内部 new 的依赖"如 `new PaymentClient()`，那个要重构注入。）
>
> **但 `any()` 会放过 wrapper 自身的构造 bug**（如 `.eq(User::getId, id)` 写错字段）。应用 `ArgumentCaptor` 捕获并 `verify(mapper).selectOne(captor.capture())` 确认调用；wrapper 内部条件断言较脆（lambda 序列化不稳），可退一步断言 `captor.getValue()` 非空 + 下游返回值处理正确。

### 静态方法：重构为可注入实例（"优先重构"的具体落地）

`mockStatic` 是兜底；首选把静态调用包进接口注入。前后对照：

```java
// ✗ 静态调用难测：每次跑结果不同（UUID），不 mockStatic 无法断言
class OrderService {
    public String genId() { return IdUtil.getId(); }   // 静态，难测
}

// ✓ 抽接口 + 构造器注入：可 mock、可固定值，与"构造器注入"主张一致
interface IdGenerator { String next(); }
class OrderService {
    private final IdGenerator idGen;
    public OrderService(IdGenerator idGen) { this.idGen = idGen; }
    public String genId() { return idGen.next(); }
}
// 测试：@Mock IdGenerator idGen; when(idGen.next()).thenReturn("FAKE");
```

> 仅在静态调用的代码你够不着时（调用点在第三方库内部）才退回 `mockStatic`。
>
> **常见误判**：`LocalDate.now()` / `UUID.randomUUID()` 看似"来自 JDK 改不了源"，但**调用点在你自己代码里**——首选 `Clock` 注入（`Clock.fixed(...)`）或 `IdGenerator` 接口注入（本节上方范例），不走 `mockStatic`。能改调用点就不算"够不着"。

### Mockito stubbing / verify 隐蔽坑（用错不报错但埋雷）

以下三个坑都"查文档未必意识到严重性、用错了测试照样过"，是技能固化的价值点：

**① 对 `spy` 用 `when().thenReturn()` 会先触发真实方法**

```java
List<Object> real = spy(new ArrayList<>());

// ✗ 对 spy 用 when()：会先调用 real.size() 真实方法，若真实方法有副作用/NPE 就已经发生
when(real.size()).thenReturn(10);

// ✓ 对 spy 一律用 doReturn().when()：跳过真实方法直接返回桩值
doReturn(10).when(real).size();
```

规则：**stubbing `spy` 或会抛异常的方法，必须用 `doReturn/doThrow().when(obj)`**（"do 先行"），不能用 `when(obj).thenReturn()`。后者是先执行真实调用再回放，对 spy 会产生副作用。

**② `verify` 不传 times 默认 = 1，且是"恰好"不是"至少"**

```java
verify(repo).save(order);         // 等价于 verify(repo, times(1))，必须恰好 1 次
verify(repo, never()).save(any()); // 0 次
verify(repo, atLeast(2)).save(any()); // ≥2 次（注意 atLeast vs times 的语义差）
// 误以为"不写 times = 至少 1 次" → 实际被调 2 次时这个 verify 会失败
```

**③ 严格桩模式（`@MockitoSettings`/MockitoExtension）下多余 stub 抛异常**

```java
@ExtendWith(MockitoExtension.class)   // 严格模式
class XTest {
    @Mock Repo repo;
    @Test void t() {
        when(repo.findById(1L)).thenReturn(o);  // 若被测代码没调 findById(1L) → UnnecessaryStubbingException
    }
}
```

这是好事（逼桩值有用），但**调试式补的 stub 忘删**会让测试红。排查：确认桩值是否真被消费；确需"可能不用"的桩用 `lenient().when(...)` 显式标注（仅在必要时，别滥用）。

### `@MockBean` vs `@Mock`（关键区分）

| | `@Mock` | `@MockBean` |
|---|---|---|
| 范围 | 纯单元测试 | Spring 切片/集成测试 |
| 开销 | 毫秒，不起容器 | **启动/重建 Spring Context** |
| 用于 | 本技能的主战场 | `@WebMvcTest`/`@DataJpaTest` 等 |

## §4 JUnit 4 项目的写法差异（跟随既有）

探测到 JUnit 4（`junit:junit` / `@RunWith`）时，跟随既有，不强升。差异：

| 概念 | JUnit 5（默认） | JUnit 4（跟随） |
|---|---|---|
| 测试注解 | `@Test`（org.junit.jupiter） | `@Test`（org.junit，**勿混用**） |
| 前置 | `@BeforeEach` | `@Before` |
| 断言 | `Assertions.assertEquals` | `Assert.assertEquals` |
| 异常断言 | `assertThrows(...)` | `@Test(expected=...)` 或 `try/catch fail()` |
| 参数化 | `@ParameterizedTest` | `@RunWith(Parameterized.class)` |
| Mockito 注解 | `MockitoAnnotations.openMocks` | `@RunWith(MockitoJUnitRunner.class)` |

> 同一模块禁止 JUnit 4 与 5 混用——生命周期注解不互通。

## §5 覆盖率工具（仅项目无且用户问时）

JaCoCo 接入见 `references/05-coverage-and-quantity.md`。**不要主动推覆盖率接入**——只在用户问"测够没/覆盖率"时提，且强调它是反向诊断而非合格证。

## §6 范围边界

本技能只覆盖**纯单元测试**（`@Mock`+`@InjectMocks`，毫秒级，不起容器）。以下不在本技能范围：

- 集成测试 / `@SpringBootTest` 全量上下文 / 切片测试（`@WebMvcTest`/`@DataJpaTest`）—— 这些里 `@MockBean` 才适用。
- TestNG —— 跟随项目既有；项目无则不主动推荐引入。
- 性能测试、前端测试。

用户问及以上时，说明超出本技能范围，建议走对应专门资料。
