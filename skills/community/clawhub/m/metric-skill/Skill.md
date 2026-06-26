---
name: metric-log
description: 分析 Java 代码，识别业务指标项并提供监控建议。触发词: "指标日志"、"metric log"、"业务指标"、"指标识别"。
---

# Metric Log Skill

分析 Java 业务代码，识别可监控的指标项，提供指标定义和采集建议。

## 触发

- 用户请求: "业务指标"、"metric log"、"指标识别"、"添加监控"
- 文件: `**/*Service.java`, `**/*Controller.java`, `**/*Manager.java`, `**/*Facade.java`

## 核心思路

本 skill 不预设具体业务领域的指标，而是基于**代码模式**识别指标特征，由用户根据业务定义具体指标名。

## 执行步骤

1. **读取用户提供分析的文件**
   - 解析类名（推断业务领域）
   - 扫描所有 public 方法

2. **询问用户**
   > 是否需要扫描项目中的 AOP 类？（可选）
   >
   > - **是**：扫描项目中已有的 Aspect/Interceptor/Filter，作为补充参考
   > - **否**：仅分析用户提供的文件

3. **指标识别与分析**
   - 根据方法名前缀推断操作类型
   - 根据返回类型推断结果指标
   - 根据参数类型推断维度标签
   - 扫描异常处理块
   - 扫描耗时计算点
   - 如有 AOP：结合 AOP 分析已有的采集情况

4. **生成识别报告**（统一输出格式）
   - 按方法列出识别依据
   - 提供建议的指标名模板
   - 标注建议的标签
   - 如有 AOP：标注已有的采集情况

## 通用识别模式

### 1. 方法命名识别 (CRUD + 业务动作)

方法名是识别指标的最重要线索：

| 方法名模式 | 识别为 | 指标类型建议 |
|------------|--------|--------------|
| `createXxx` | Xxx 创建 | Counter |
| `saveXxx` / `addXxx` | Xxx 保存 | Counter |
| `deleteXxx` / `removeXxx` | Xxx 删除 | Counter |
| `updateXxx` / `modifyXxx` | Xxx 更新 | Counter |
| `getXxx` / `queryXxx` | Xxx 查询 | Counter / Histogram |
| `listXxx` | Xxx 列表 | Histogram |
| `countXxx` | Xxx 计数 | Gauge |

**业务动作识别**：

| 方法名模式 | 识别为 | 指标类型建议 |
|------------|--------|--------------|
| `login` / `logout` | 登录/登出 | Counter |
| `pay` / `refund` | 支付/退款 | Counter + Amount Gauge |
| `approve` / `reject` | 审批 | Counter (带状态标签) |
| `send` / `receive` | 发送/接收 | Counter |
| `execute` / `run` | 执行 | Counter + Histogram |
| `handle` / `process` | 处理 | Counter + Histogram |
| `sync` | 同步 | Counter + Histogram |

```java
// 识别: 方法名包含 create/add/save → 增量计数器
public User createUser(UserRequest request) { } → 建议指标: xxx_created_total

// 识别: 方法名包含 pay/refund → 交易类指标
public PayResult pay(PayRequest request) { } → 建议指标: xxx_pay_total + xxx_pay_amount

// 识别: 方法名包含 login → 登录类指标
public LoginResult login(String username) { } → 建议指标: login_attempts_total

// 识别: 方法名包含 get/find/query → 查询类指标
public Order getOrder(Long id) { } → 建议指标: xxx_query_total + xxx_query_duration_ms
```

### 2. 参数特征识别

根据参数类型推断指标：

| 参数特征 | 识别为 | 指标建议 |
|----------|--------|----------|
| `Pageable` / `PageRequest` | 分页查询 | 添加 page/size 标签 |
| `List<XxxRequest>` | 批量操作 | 记录批量大小 |
| `Date` / `LocalDateTime` | 时间敏感 | 添加时间维度标签 |
| `BigDecimal` / `Double`(金额) | 金额类 | 记录金额 sum/avg |
| `Long`(ID) | 实体操作 | 可添加 ID 前缀标签 |

```java
// 识别: 分页参数 → 分页指标
public Page<Order> listOrders(Pageable pageable) {
    // 建议添加标签: page, size
}

// 识别: 批量参数 → 批量大小指标
public void batchImport(List<ImportData> dataList) {
    // 建议指标: batch_size (记录 dataList.size())
}

// 识别: 金额参数 → 金额类指标
public void charge(BigDecimal amount) {
    // 建议指标: xxx_amount_total (Sum)
}
```

### 3. 返回值特征识别

| 返回值特征 | 识别为 | 指标建议 |
|------------|--------|----------|
| `boolean` / `Result<T>` | 操作结果 | 区分 success/failed |
| `Page<T>` | 分页结果 | 记录 total 字段 |
| `List<T>` | 列表结果 | 记录 size |
| `Optional<T>` | 空值判断 | 记录 hit/miss |
| `ResponseEntity` | HTTP 结果 | 记录 status code |

```java
// 识别: boolean 返回 → 成功/失败分离
public boolean createXxx(XxxRequest req) {
    // 建议: success_counter + failed_counter (而非 total)
}

// 识别: Result 类 → 状态标签
public Result<Order> createOrder(OrderRequest req) {
    // 建议: status={success/failed} 标签
    // 建议: error_code 标签
}
```

### 4. 状态变化识别

| 代码模式 | 识别为 | 指标建议 |
|----------|--------|----------|
| `status = XxxStatus.Y` | 状态变更 | 状态分布 Gauge |
| `if (condition) { ... } else { ... }` | 分支逻辑 | 分支计数器 |
| `switch (status)` | 多状态 | 各状态计数 |
| `boolean flag` | 开关 | 当前状态 Gauge |

```java
// 识别: 状态赋值 → 状态分布指标
public void updateStatus(Long id, OrderStatus status) {
    // 指标: 各状态订单数量 (Gauge)
    // 标签: status
}

// 识别: 分支逻辑 → 分支计数
if (vipUser) {
    // 会员分支
} else {
    // 普通用户分支
}
// 建议: user_type 分支计数
```

### 5. 异常处理识别

| 代码模式 | 识别为 | 指标建议 |
|----------|--------|----------|
| `catch (Exception e)` | 异常 | errors_total |
| `throw new XxxException` | 业务异常 | biz_errors_total (带 error_code) |
| `retry` / `fallback` | 重试/降级 | retry_count / fallback_count |
| `timeout` | 超时 | timeout_count |

```java
// 识别: catch 块 → 错误计数
try {
    // ... business logic
} catch (BusinessException e) {
    // 建议: biz_errors_total{error_code=xxx}
    throw e;
} catch (Exception e) {
    // 建议: system_errors_total
    throw e;
}
```

### 6. 耗时计算识别

| 代码模式 | 识别为 | 指标建议 |
|----------|--------|----------|
| `System.currentTimeMillis()` | 手动耗时 | Histogram |
| `@Cacheable` | 缓存 | cache_hit_rate |
| `for` 循环 | 循环处理 | 处理计数 + 耗时 |

```java
// 识别: 手动计时 → 耗时指标
long start = System.currentTimeMillis();
// ... logic ...
long cost = System.currentTimeMillis() - start;
// 建议: xxx_duration_ms (Histogram)

// 识别: 循环 → 批量计数
for (Item item : items) {
    process(item);
}
// 建议: batch_process_total + batch_process_duration_ms
```

### 7. 外部调用识别

| 代码模式 | 识别为 | 指标建议 |
|----------|--------|----------|
| `restTemplate.exchange()` | HTTP 调用 | http_calls_total + duration |
| `xxxClient.call()` | RPC 调用 | rpc_calls_total + duration |
| `repository.save()` | DB 操作 | db_calls_total + duration |
| `redisTemplate.opsForXxx()` | Redis 操作 | redis_ops_total + hit_rate |

```java
// 外部调用 → 独立耗时指标
Result result = remoteService.call(param);
// 建议: remote_service_call_duration_ms
// 建议: remote_service_call_total{status=success/failed}
```

### 8. 业务语义推断

根据方法上下文推断业务指标：

```java
// 从类名推断业务领域
class OrderService { }  // 订单业务 → orders_xxx
class UserService { }   // 用户业务 → users_xxx
class PaymentService { } // 支付业务 → payments_xxx

// 从复合方法名推断
public int getTodayActiveUsers() {
    // 指标: daily_active_users (Gauge)
}

public double calculateConversionRate() {
    // 指标: conversion_rate (Computed/Ratio)
}

public BigDecimal getTotalRevenue() {
    // 指标: total_revenue (Gauge)
}
```

## 项目中现有 AOP 类的补充分析（可选）

### 何时使用

当用户选择扫描项目中的 AOP 类时，作为补充参考，避免指标重复采集。

### 扫描目标

| 类型 | 识别特征 | 作用 |
|------|----------|------|
| Aspect | `@Aspect` + `@Component` | 已有切面逻辑 |
| Interceptor | `implements HandlerInterceptor` | Web 层拦截 |
| Filter | `@Component` + `doFilter` | 请求过滤器 |

### 扫描步骤

1. 搜索项目中 `**/*Aspect.java`
2. 搜索 `**/*Interceptor.java`
3. 搜索 `**/*Filter.java`

### 分析输出

如扫描到 AOP，输出补充信息：

```markdown
### 补充参考：项目中已有 AOP

| AOP 类 | 切点范围 | 已有采集 |
|--------|----------|----------|
| LoggingAspect | 所有 Service | method_entry, method_exit |
| PerformanceAspect | @Monitor 注解 | method_duration_ms |

### 建议

- 已有指标可复用，无需重复定义
- 建议在现有切面中扩展 Counter 类型指标
```

## 指标输出格式

无论是否扫描 AOP，最终输出的指标格式统一：

```markdown
## {ClassName}.java 指标识别结果

### 识别的指标项

| 方法 | 识别依据 | 建议指标名 | 类型 | 建议标签 |
|------|----------|------------|------|----------|
| createXxx | 方法名 | xxx_created_total | Counter | - |
| deleteXxx | 方法名 | xxx_deleted_total | Counter | - |
| getXxxById | 方法名 | xxx_query_total | Counter | - |
| getXxxById | 方法名 | xxx_query_duration_ms | Histogram | - |
| listXxx | 方法名 | xxx_query_duration_ms | Histogram | page, size |
| createXxx | 返回 Result<T> | xxx_success_total | Counter | status=success |
| createXxx | 返回 Result<T> | xxx_failed_total | Counter | status=failed |

### 采集建议

| 指标名 | 建议采集方式 | 说明 |
|--------|--------------|------|
| xxx_created_total | 手动埋点 / 注解 | 用户自行选择 |
| xxx_query_duration_ms | AOP 切面 | 通用耗时采集 |
```

### 采集方式参考

用户可根据项目情况选择采集方式：

| 方式 | 适用场景 | 示例 |
|------|----------|------|
| 手动埋点 | 关键业务指标 | 直接注入 Counter |
| 注解 + 通用切面 | 需要灵活控制 | @Metric + Aspect |
| 复用现有 AOP | 项目已有切面 | 扩展现有逻辑 |

```java
// 方式一：手动埋点
private final Counter counter = Counter.builder("xxx").register(registry);
counter.increment();

// 方式二：注解标记
@Metric("xxx_total")
public void method() { }

// 方式三：复用现有 AOP
// 在项目已有的 LoggingAspect 中添加 Counter 采集
```

## 指标命名建议

用户根据识别的特征自定义指标名：

| 规则 | 示例 |
|------|------|
| `{业务域}_{动作}_{实体}_total` | orders_create_total |
| `{业务域}_{动作}_{实体}_duration_ms` | user_query_duration_ms |
| `{业务域}_{状态}_current` | order_status_current |
| `{动作}_attempts_total` | login_attempts_total |

## 标签建议

基于代码特征自动推断：

| 代码特征 | 建议标签 |
|----------|----------|
| 返回 Result/Response | status=success/failed |
| 异常 catch | error_code |
| Pageable 参数 | page, size |
| 用户相关 | user_type, vip_level |
| 设备相关 | device_type, os_version |

## 注意

- 本 skill 识别的是**代码模式**，而非预设业务指标
- 指标名由用户根据实际业务定义
- 方法命名规范有助于更准确的识别
- 识别结果需要用户确认和调整
- 扫描 AOP 类仅为补充参考，不影响核心指标输出
- 用户可根据实际情况选择采集方式
