# 并发处理

> 来源: Java开发手册（嵩山版）— 一(七) 并发处理

## 【强制】规则

### 1. 单例线程安全

获取单例对象需要保证线程安全，其中的方法也要保证线程安全。

### 2. 线程命名

创建线程或线程池时请指定有意义的线程名称。

> **正例**: 自定义 ThreadFactory，按外部特征分组命名。

### 3. 线程池创建线程

线程资源必须通过线程池提供，不允许在应用中自行显式创建线程。

### 4. ThreadPoolExecutor 创建线程池

线程池**不允许**使用 `Executors` 创建，而是通过 `ThreadPoolExecutor`。

> **Executors 弊端**:
> - `FixedThreadPool`/`SingleThreadPool`: 请求队列长度 `Integer.MAX_VALUE`，可能 OOM
> - `CachedThreadPool`: 创建线程数 `Integer.MAX_VALUE`，可能 OOM

### 5. SimpleDateFormat 线程不安全

一般不要定义为 static 变量。如果定义为 static，必须加锁或使用 `DateUtils`。

> **正例**: `ThreadLocal<DateFormat>` 或 JDK8 `DateTimeFormatter`

### 6. ThreadLocal 必须回收

尤其在线程池场景下，线程会被复用，必须清理自定义的 ThreadLocal 变量。

> **正例**:
> ```java
> objectThreadLocal.set(userInfo);
> try { /* ... */ }
> finally { objectThreadLocal.remove(); }
> ```

### 7. 锁粒度最小化

能用无锁数据结构，就不要用锁；能锁区块，就不要锁整个方法体；能用对象锁，就不要用类锁。

### 8. 多资源加锁顺序一致

对多个资源、数据库表、对象同时加锁时，需要保持一致的加锁顺序，否则可能造成死锁。

### 9. 阻塞锁在 try 外获取

在使用阻塞等待获取锁的方式中，必须在 `try` 代码块之外加锁，且加锁方法与 try 之间无可能抛异常的方法调用。

> **正例**:
> ```java
> lock.lock();
> try { doSomething(); }
> finally { lock.unlock(); }
> ```

### 10. 尝试锁判断持有状态

进入业务代码块之前，必须先判断当前线程是否持有锁。

> **正例**:
> ```java
> boolean isLocked = lock.tryLock();
> if (isLocked) {
>     try { doSomething(); }
>     finally { lock.unlock(); }
> }
> ```

### 11. 并发更新加锁

并发修改同一记录时，需要加锁。冲突概率 < 20% 用乐观锁，否则悲观锁。乐观锁重试次数 ≥ 3。

### 12. 定时任务用 ScheduledExecutorService

`Timer` 中一个异常未捕获会导致其它任务全部终止。

## 【推荐】规则

### 13. 金融信息用悲观锁

乐观锁校验逻辑容易出现漏洞，资金相关建议使用悲观锁。

### 14. CountDownLatch 注意 countDown

每个线程退出前必须调用 `countDown`，注意 catch 异常确保 `countDown` 被执行。

### 15. 避免 Random 多线程共享

JDK7+ 使用 `ThreadLocalRandom`。

### 16. 双重检查锁用 volatile

> **正例**:
> ```java
> private volatile Helper helper = null;
> public Helper getHelper() {
>     if (helper == null) {
>         synchronized (this) {
>             if (helper == null) { helper = new Helper(); }
>         }
>     }
>     return helper;
> }
> ```

### 17. volatile 一写多读

一写多读可以解决变量同步，多写无法解决线程安全。`count++` 用 `AtomicInteger`。JDK8 推荐 `LongAdder`。

### 18. HashMap resize 并发风险

高并发时可能出现死链，导致 CPU 飙升。

### 19. ThreadLocal static 修饰

ThreadLocal 针对线程内共享，设为静态变量。无法解决共享对象的更新问题。
