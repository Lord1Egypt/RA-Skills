# 09 · 现代 Java 语法（版本门控）

> 每个特性都标注**门控 JDK**（以 LTS 为锚点：8/11/17/21/25）。**先用 `SKILL.md` 的 JDK 版本策略确认目标版本**，低于门控的严禁使用。
> JDK 8 是下限——JDK 8 项目**全部禁用本文件特性**（除已属 JDK 8 的 Lambda/Optional/Stream/java.time）。
> **LTS 锚定原则**：22–24 转正的特性统一归入 JDK 25 LTS（括号注明实际转正版本作背景）；非 LTS 不单独门控。preview/incubator 特性不纳入本表。

## 特性门控速查

> 下表 JDK 8–21 行为特性实际转正版本；JDK 25 行按 LTS 锚定统一标注（22–24 转正特性归入 25 LTS，括号注明实际转正版本）。

| 特性 | 门控 JDK | 形态 | 推荐度 |
|---|---|---|---|
| Lambda / 方法引用 / `Optional`/`Stream`/`java.time`/`CompletableFuture` | **8** | 标准 | ✅ JDK 8 即可用 |
| `var` 局部变量类型推断 | **10** | 标准 | ✅ 局部变量类型明显时用 |
| JDK 内置 `HttpClient` | **11** | 标准 | 🟡 但本指南 HTTP 推荐 OkHttp3（一致性） |
| `switch` 表达式（箭头、yield） | **14** | 标准 | ✅ 简化多分支 |
| 文本块 `"""` | **15** | 标准 | ✅ 多行字符串/SQL/JSON |
| `record`（不可变数据载体） | **16** | 标准 | ✅ 纯数据 DTO |
| `Stream.toList()` | **16** | 标准 | ✅ 简化 collect（注意**不可变**） |
| `instanceof` 模式匹配 | **16** | 标准 | ✅ 省强转 |
| `sealed` 密封类 | **17** | 标准 | ✅ 限定继承层级 |
| 虚拟线程 | **21** | 标准 | ✅ IO 密集高并发 |
| `switch` 模式匹配 | **21** | 标准 | ✅ 类型模式 |
| `SequencedCollection` | **21** | 标准 | ✅ 统一首尾访问 |
| 未命名变量 & 模式 `_` | **25** | 标准（22 转正） | ✅ 忽略值时用 |
| Markdown Javadoc | **25** | 标准（23 转正） | ✅ 注释用 Markdown |
| Stream Gatherers | **25** | 标准（24 转正） | ✅ 自定义中间操作 |
| Class-File API | **25** | 标准（24 转正） | 🟡 字节码操作替代 ASM |
| 虚拟线程不再被 synchronized 钉住 | **25** | 标准（24 转正） | ✅ 修正旧建议 |
| Compact Object Headers | **25** | 标准（24 预览→25 转正） | 🟡 JVM 内部 |
| Compact Source Files & Instance Main | **25** | 标准 | 🟡 学习/脚本场景 |
| Flexible Constructor Bodies | **25** | 标准 | ✅ 参数校验前置 |
| Module Import Declarations | **25** | 标准 | 🟡 简化导入 |
| Scoped Values | **25** | 标准 | ✅ ThreadLocal 安全替代 |
| Key Derivation Function API | **25** | 标准 | ✅ 密钥派生 |

## 反例详解（antipattern）

### 1. JDK 8 项目误用高版本语法（编译失败）
```java
// ✗ JDK 8 项目里写 var / record / 文本块 / switch 表达式 → 编译失败
var name = "abc";                         // var 是 JDK 10+
public record Point(int x, int y) {}      // record 是 JDK 16+
String json = """
    {"a":1}
    """;                                  // 文本块是 JDK 15+
String r = switch (day) {                 // switch 表达式 JDK 14+（标准）
    case MON -> "M";
    default -> "?";
};

// ✓ JDK 8 等价写法
String name = "abc";
class Point { private final int x, y; /* ctor+getter */ }
String json = "{\"a\":1}";
String r;
switch (day) { case MON: r = "M"; break; default: r = "?"; }
```

### 2. `Stream.toList()` 返回不可变（JDK 16+）
```java
// JDK 16+ 可用 toList()，但返回不可变列表
List<String> names = users.stream().map(User::getName).toList(); // 不可变
names.add("x"); // ✗ UnsupportedOperationException

// 需要可变列表用 Collectors.toList()
List<String> mutable = users.stream().map(User::getName).collect(Collectors.toList());
```

### 3. 虚拟线程 + synchronized 的 LTS 版本陷阱（JDK 21 vs 25）
```java
// JDK 21 LTS：虚拟线程遇到 synchronized 会被钉住载体线程（pin），失去并发优势
// 旧建议：JDK 21 虚拟线程代码中禁用 synchronized，改用 ReentrantLock
public void fetch() {
    synchronized (this) {   // ✗ JDK 21：pin 住载体线程
        doBlockingIO();
    }
}

// JDK 25 LTS（吸收 JEP 491）：synchronized 不再 pin 虚拟线程，可直接使用
public void fetch() {
    synchronized (this) {   // ✓ JDK 25：不再 pin，无需改 ReentrantLock
        doBlockingIO();
    }
}
```
> 不一刀切：JDK 21 虚拟线程避免 synchronized（改 `ReentrantLock`），JDK 25 不再 pin 可直接用——按目标 LTS 版本判断。

### 4. Scoped Values vs ThreadLocal（JDK 25+）
```java
// ✗ ThreadLocal 传请求上下文（可变、内存泄漏、线程池复用串值）
private static final ThreadLocal<RequestContext> CTX = new ThreadLocal<>();
CTX.set(context);
try { handle(); } finally { CTX.remove(); }

// ✓ JDK 25 ScopedValue（不可变、作用域绑定、自动清理）
ScopedValue.where(CTX, context).run(() -> handle());
```
> API 细节、与 ThreadLocal 的对比表、嵌套绑定示例见 `05-concurrency.md`「Scoped Values」。**仅 JDK 25+ 可用**；JDK 21 及以下仍用 ThreadLocal（务必 finally remove）。

### 5. Flexible Constructor Bodies 误用（JDK 25+）
```java
// ✗ 在 super() 前做可观测副作用（构造未完成即暴露 this）
public class Child extends Parent {
    public Child(int x) {
        this.registry = EventBus.register(this);  // this 未完全构造！
        super(x);
    }
}

// ✓ 仅用于参数校验 / 防御性拷贝（无副作用、不暴露 this）
public class Child extends Parent {
    public Child(int x) {
        if (x < 0) throw new IllegalArgumentException("x must be >= 0");
        super(x);  // 校验后再调用
    }
}
```
> Flexible Constructor Bodies（JEP 513）允许 super()/this() 前执行语句，但**仅限无副作用的准备逻辑**（参数校验、防御性拷贝、字段计算）。禁止在 super() 前暴露 `this` 或触发可观测副作用——此时对象尚未完全构造。

### 6. sun.misc.Unsafe / Security Manager 依赖（JDK 25 移除）
```java
// ✗ 依赖 Unsafe 内存操作
sun.misc.Unsafe unsafe = ...;
unsafe.putLong(address, value);   // JDK 25 已移除

// ✗ 依赖 Security Manager
System.setSecurityManager(new MySecurityManager());  // JDK 25 已永久禁用

// ✓ 迁移至官方 API
// 内存操作 → Foreign Function & Memory API（JEP 454，JDK 25 转正）
// 安全管理 → 应用级沙箱（容器/OS 级隔离），不再依赖 JVM Security Manager
```
> JDK 25 LTS 永久移除 Security Manager（JEP 486）并废弃 `sun.misc.Unsafe` 内存方法（JEP 471/498）。依赖这些内部 API 的代码将无法运行。迁移到 FFM API（`java.lang.foreign`）替代 Unsafe 内存操作；用容器/OS 级隔离替代 Security Manager。

## 推荐示例（按版本）

### JDK 10+ `var`（仅局部变量，类型明显时）
```java
var users = new ArrayList<User>();   // ✓ 右侧类型明显
var name = user.getName();           // 🟡 可读性视情况，简单赋值可省
// ✗ 不要作字段/方法签名/参数（var 仅限局部变量）
```

### JDK 14+ `switch` 表达式
```java
// ✓ 箭头语法，无 fall-through，直接返回值
String label = switch (status) {
    case ACTIVE -> "活跃";
    case INACTIVE -> "停用";
    case PENDING -> "待审";
    default -> {
        log.warn("未知状态: {}", status);
        yield "未知";
    }
};
```

### JDK 15+ 文本块（多行 SQL/JSON/模板）
```java
String sql = """
    SELECT id, name
    FROM users
    WHERE dept = ?
    ORDER BY id
    """;
```

### JDK 16+ `record`（纯数据载体）
```java
public record Point(int x, int y) {}
// 等价于：final 类 + private final 字段 + 全参构造 + getter（x()/y()）+ equals/hashCode/toString
// 适用：DTO、值对象、配置项；不适用：可变状态、需继承
```

### JDK 16+ `instanceof` 模式匹配
```java
// ✗ 旧：强转冗长
if (obj instanceof String) {
    String s = (String) obj;
    use(s);
}
// ✓ 新：模式绑定
if (obj instanceof String s) {
    use(s);
}
```

### JDK 17+ `sealed`（限定继承）
```java
public sealed interface Shape permits Circle, Square, Triangle {}
record Circle(double r) implements Shape {}
record Square(double side) implements Shape {}
// 编译期保证 Shape 的实现类封闭，配合 switch 模式匹配穷尽检查
```

### JDK 21+ 虚拟线程（IO 密集高并发，详见 `05-concurrency.md`）
```java
try (var exec = Executors.newVirtualThreadPerTaskExecutor()) {
    tasks.forEach(exec::submit);
} // 每个 IO 阻塞任务一个虚拟线程，无需手调池大小
// ✗ 不适用 CPU 密集；不要池化虚拟线程
```

### JDK 21+ `switch` 模式匹配
```java
String desc = switch (shape) {
    case Circle c  -> "圆 r=" + c.r();
    case Square s  -> "方 side=" + s.side();
    case null      -> "空";        // null 模式
    // sealed 下编译器检查穷尽，无需 default
};
```

### JDK 25+ 未命名变量 `_`（忽略值时用）
```java
// ✓ 用 _ 显式标记忽略值，消除未使用变量警告
try (var conn = dataSource.getConnection()) {
    var _ = conn.getAutoCommit();  // 明确表示不关心返回值
}
// catch 也可用 _ 忽略异常变量
try { ... } catch (TimeoutException _) { log.warn("timeout, ignore"); }
```

### JDK 25+ Scoped Values（ThreadLocal 安全替代，详见 `05-concurrency.md`）
```java
private static final ScopedValue<UserContext> USER_CTX = ScopedValue.newInstance();
// 绑定作用域
ScopedValue.where(USER_CTX, currentUser).run(() -> {
    UserContext ctx = USER_CTX.get();  // 作用域内只读访问
    handle(ctx);
});
// 作用域结束自动清理，无需 remove
```

### JDK 25+ Flexible Constructor Bodies（参数校验前置）
```java
public class Sub extends Base {
    public Sub(String input) {
        Objects.requireNonNull(input, "input");  // super() 前校验
        super(input);
    }
}
// 仅限无副作用准备逻辑（校验、防御性拷贝）；禁暴露 this
```

### JDK 25+ Stream Gatherers（自定义中间操作）
```java
// Stream Gatherers 补充 Collectors 能力，支持自定义中间操作
// 例：固定窗口分组（每 3 个元素一组）
List<List<Integer>> windows = numbers.stream()
    .gather(Gatherers.windowFixed(3))
    .toList();
// 更多自定义 Gatherer 见 java.util.stream.Gatherer
```
