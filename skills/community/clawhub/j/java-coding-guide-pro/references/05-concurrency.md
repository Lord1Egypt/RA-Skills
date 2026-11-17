# 05 · 并发与线程池

> JDK `ThreadPoolExecutor` + `CompletableFuture` + `java.util.concurrent`。原生 API 完善→用原生。
> **核心**：禁 `new Thread().start()`；禁 `Executors.newXxx`（无界队列 OOM 风险）。

## 规范速查

| 场景 | ✗ 禁止 | ✓ 推荐 |
|---|---|---|
| 执行并发任务 | `new Thread(r).start()` | `executor.execute(r)` / `submit(r)` |
| 创建线程池 | `Executors.newFixedThreadPool(n)` | `new ThreadPoolExecutor(...)` 显式参数 |
| 异步编排 | 手写 `Thread` + `CountDownLatch` | `CompletableFuture.supplyAsync(...)` |
| 线程命名 | 默认 `pool-1-thread-1` | 自定义 `ThreadFactory`（带业务前缀） |
| 队列 | 无界 `LinkedBlockingQueue` | 有界队列（如 `new LinkedBlockingQueue<>(100)`） |
| 拒绝策略 | 默认不显式 | 显式选择（见下） |
| 锁 | `synchronized` 大范围 | `ReentrantLock`（可超时/可中断）按需 |
| 并发集合 | `HashMap` 多线程写 | `ConcurrentHashMap` |
| 大量短任务（JDK21+） | 平台线程池 | 虚拟线程 `Executors.newVirtualThreadPerTaskExecutor()` |

## 反例详解（antipattern）

### 1. `Executors.newFixedThreadPool` 无界队列 OOM（最高危）
```java
// ✗ 内部用无界 LinkedBlockingQueue，任务堆积导致 OOM
ExecutorService pool = Executors.newFixedThreadPool(10);
// ✗ newCachedThreadPool 最大线程 Integer.MAX_VALUE，同样危险
ExecutorService pool2 = Executors.newCachedThreadPool();

// ✓ 显式 ThreadPoolExecutor + 有界队列 + 手写命名线程工厂（无额外依赖）+ 默认拒绝策略
ThreadPoolExecutor pool = new ThreadPoolExecutor(
    10,                                                 // corePoolSize
    10,                                                 // maxPoolSize（按需可 > core）
    0L, TimeUnit.MILLISECONDS,                          // 空闲存活
    new LinkedBlockingQueue<>(100),                     // 有界队列
    new ThreadFactory() {                               // 手写命名工厂（不依赖 Guava）
        private final AtomicInteger n = new AtomicInteger(1);
        @Override public Thread newThread(Runnable r) {
            return new Thread(r, "biz-pool-" + n.getAndIncrement());
        }
    },
    new ThreadPoolExecutor.CallerRunsPolicy()           // 默认拒绝策略：背压（调用方执行）
);
```

**拒绝策略：默认 `CallerRunsPolicy`**（背压——调用线程自己执行，自动降速、不丢任务）。

| 策略 | 行为 | 何时用它替代默认 |
|---|---|---|
| **`CallerRunsPolicy`（本指南默认）** | 调用线程自己执行（背压降速） | 大多数业务线程池 |
| `AbortPolicy` | 抛 `RejectedExecutionException` | 必须感知拒绝、能接受任务失败 |
| `DiscardOldestPolicy` | 丢最旧任务 | 允许丢旧（如日志/缓存刷新） |
| `DiscardPolicy` | 静默丢弃 | **禁用**（吞任务无感知） |
| 自定义（记日志 + 处理） | 按需 | 需可观测性时 |

> **覆盖默认**：题面或用户**显式指定**拒绝策略时（如"队列满丢弃最旧并记日志"），按显式要求覆盖默认 `CallerRunsPolicy`——用 `DiscardOldestPolicy` 或自定义策略（`getQueue().poll()` 丢最旧 + 日志）。默认仅在"未指定"时生效。

### 2. `new Thread().start()` 直接造线程
```java
// ✗ 线程创建/销毁开销大；无限制；难管理；无命名难排查
new Thread(() -> doWork()).start();

// ✓ 用线程池
executor.submit(() -> doWork());
```

### 3. 不优雅关闭线程池
```java
// ✗ 不 shutdown，JVM 不退出；或强行 shutdownNow 丢任务
pool.shutdownNow();

// ✓ 优雅关闭
pool.shutdown();
if (!pool.awaitTermination(60, TimeUnit.SECONDS)) {
    pool.shutdownNow();
}
```

### 4. `HashMap` 多线程写
```java
// ✗ 并发写 HashMap 可能死循环（JDK7）/ 数据丢失（JDK8）
static Map<String, User> cache = new HashMap<>();

// ✓ ConcurrentHashMap
static Map<String, User> cache = new ConcurrentHashMap<>();
```

### 5. ThreadLocal 传不可变上下文 → ScopedValue（JDK 25+）
```java
// ✗ ThreadLocal 传请求上下文（可变、内存泄漏、线程池复用串值）
private static final ThreadLocal<UserContext> CTX = new ThreadLocal<>();
CTX.set(context);
try { handle(); } finally { CTX.remove(); } // 忘记 remove → 内存泄漏

// ✓ JDK 25 ScopedValue（不可变、作用域绑定、自动清理）
private static final ScopedValue<UserContext> CTX = ScopedValue.newInstance();
ScopedValue.where(CTX, context).run(() -> handle()); // 作用域结束自动清理
```
> ThreadLocal 的问题：可变（随时 set 覆盖）、忘记 remove 导致内存泄漏、线程池复用时串值。ScopedValue 不可变、作用域绑定、自动清理。**仅 JDK 25+ 可用**；JDK 21 及以下仍用 ThreadLocal（务必 finally remove）。详见下方「Scoped Values」段。

### 6. 无名线程 / 线程池未命名 ThreadFactory（阿里规约）
```java
// ✗ 线程池未命名，线程默认名 pool-1-thread-1，排查无从下手
ThreadPoolExecutor pool = new ThreadPoolExecutor(
    10, 10, 0L, TimeUnit.MILLISECONDS, new LinkedBlockingQueue<>(100));
// 线程名：pool-1-thread-1, pool-1-thread-2 ... → 线程 dump 无法区分业务

// ✓ 必须自定义 ThreadFactory 命名线程（带业务前缀）
ThreadPoolExecutor pool = new ThreadPoolExecutor(
    10, 10, 0L, TimeUnit.MILLISECONDS, new LinkedBlockingQueue<>(100),
    new ThreadFactory() {
        private final AtomicInteger n = new AtomicInteger(1);
        @Override public Thread newThread(Runnable r) {
            return new Thread(r, "order-pool-" + n.getAndIncrement());
        }
    });
// 线程名：order-pool-1, order-pool-2 ... → 线程 dump 一眼定位
```
> **阿里规约**：线程必须有业务语义命名。禁用默认 `pool-x-thread-y`；必须通过 `ThreadFactory` 设置 `线程名前缀-序号`。线程 dump、日志、APM 追踪都依赖线程名定位问题。

### 7. 非线程安全对象 `static` 共享（SonarQube S6373）
```java
// ✗ SimpleDateFormat 非线程安全，static 共享 → 多线程数据错乱
static SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
// 多线程并发调用 sdf.format() → 内部 Calendar 互相覆盖，结果错乱

// ✓ 用线程安全替代
// 日期格式化 → java.time.DateTimeFormatter（线程安全，JDK 8+）
static DateTimeFormatter dtf = DateTimeFormatter.ofPattern("yyyy-MM-dd");
// 或 Hutool DateUtil（内部线程安全）
String formatted = DateUtil.format(new Date(), "yyyy-MM-dd");
```
> **SonarQube S6373**：`SimpleDateFormat`、`ArrayList`、`HashMap` 等非线程安全对象禁 `static` 共享。多线程并发访问会产生数据错乱/死循环/`ConcurrentModificationException`。用线程安全替代（`DateTimeFormatter`/`ConcurrentHashMap`）或实例化（每线程一份）。

## CompletableFuture 异步编排（JDK 8+）

```java
ExecutorService pool = ...; // 自定义线程池，不要用 ForkJoinPool.commonPool 跑阻塞 IO

// 异步 + 链式
CompletableFuture<User> future = CompletableFuture
    .supplyAsync(() -> fetchUser(id), pool)
    .thenApplyAsync(this::enrich, pool)
    .exceptionally(ex -> { log.error("failed", ex); return fallbackUser(); });

User u = future.get(5, TimeUnit.SECONDS); // 显式超时
```

**注意**：`supplyAsync` 不传 `executor` 时用 `ForkJoinPool.commonPool()`——**不要在 commonPool 跑阻塞 IO**（拖垮全局），务必传自定义线程池。

## 虚拟线程（JDK 21+，版本门控）

```java
// JDK 21+：大量 IO 密集短任务用虚拟线程，无需手调线程池大小
try (ExecutorService vt = Executors.newVirtualThreadPerTaskExecutor()) {
    List<Future<?>> futures = tasks.stream().map(vt::submit).toList();
    for (Future<?> f : futures) f.get();
}
// 注意：虚拟线程不适用 CPU 密集任务；不要池化虚拟线程（每任务一线程）
```

> JDK 8/11/17 项目**禁用**虚拟线程。检测到 JDK < 21 时跳过本节。
> **synchronized 与虚拟线程（LTS 版本差异）**：JDK 21 LTS 中虚拟线程遇到 `synchronized` 会被钉住载体线程（pin），失去并发优势——建议改用 `ReentrantLock`。JDK 25 LTS（吸收 JEP 491）已修复，synchronized 不再 pin，可直接使用。按目标 LTS 版本判断，不一刀切。详见 `09-modern-java.md` antipattern 3。

## Scoped Values（JDK 25+，ThreadLocal 安全替代）

> JDK 25 LTS 转正（JEP 506）。用于在作用域内传递**不可变**上下文（请求上下文、用户身份、链路 ID）。
> **仅 JDK 25+ 可用**；JDK 21 及以下仍用 ThreadLocal（务必 finally remove）。

```java
// ✓ 基本用法
private static final ScopedValue<UserContext> USER_CTX = ScopedValue.newInstance();
ScopedValue.where(USER_CTX, currentUser).run(() -> {
    UserContext ctx = USER_CTX.get();  // 作用域内只读
    handle(ctx);
});
// 作用域结束自动清理，无需 remove

// ✓ 嵌套绑定
ScopedValue.where(REQ_ID, requestId).run(() ->
    ScopedValue.where(USER_CTX, user).run(() -> {
        // 同时访问 REQ_ID 和 USER_CTX
    })
);
```

| 特性 | ThreadLocal | ScopedValue |
|---|---|---|
| 可变性 | 可变（随时 set 覆盖） | **不可变**（绑定后只读） |
| 生命周期 | 手动 remove，易泄漏 | **作用域自动清理** |
| 线程池复用 | 串值风险 | **无串值**（作用域隔离） |
| JDK 门控 | 8+ | **25+** |

## 推荐示例

```java
public class TaskRunner {
    private static final Logger log = LoggerFactory.getLogger(TaskRunner.class);

    public void processAll(List<Runnable> tasks) {
        if (CollUtil.isEmpty(tasks)) return;
        ThreadPoolExecutor pool = new ThreadPoolExecutor(
            10, 10, 0L, TimeUnit.MILLISECONDS,
            new LinkedBlockingQueue<>(100),
            new ThreadFactory() {                                   // 手写命名工厂（不依赖 Guava）
                private final AtomicInteger n = new AtomicInteger(1);
                @Override public Thread newThread(Runnable r) {
                    return new Thread(r, "task-" + n.getAndIncrement());
                }
            },
            new ThreadPoolExecutor.CallerRunsPolicy());            // 默认拒绝策略：背压

        try {
            for (int i = 0; i < tasks.size(); i++) {
                final int idx = i;
                pool.submit(() -> {
                    try { tasks.get(idx).run(); }
                    catch (Throwable t) { log.error("任务 #{} 失败", idx, t); } // 异常隔离
                });
            }
            pool.shutdown();
            pool.awaitTermination(Long.MAX_VALUE, TimeUnit.NANOSECONDS);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
}
```

## 依赖

命名线程工厂**手写匿名 `ThreadFactory`**（见上，纯 JDK，无额外依赖）。**不引入 Guava** `ThreadFactoryBuilder`（本指南栈不含 Guava）。

