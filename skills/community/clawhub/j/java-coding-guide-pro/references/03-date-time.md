# 03 · 日期时间

> **优先 JDK `java.time`**（原生完善、线程安全）；处理遗留 `java.util.Date` 用 Hutool `DateUtil`（`cn.hutool.core.date`）。
> **禁 `SimpleDateFormat` 作共享/静态变量**（线程不安全）；**禁 `Calendar` 手算**（月从 0 易错）。
> **`.now()` 必须显式传 `ZoneId` 或 `Clock`**（Sonar java:S8688）；裸 `now()` 隐式依赖 JVM 默认时区，详见 antipattern 6。

## 规范速查

| 场景 | ✗ 禁止 | ✓ 推荐 |
|---|---|---|
| 格式化（现代） | `new SimpleDateFormat(...)` | `DateTimeFormatter` + `LocalDateTime` |
| 格式化（遗留 Date） | 同上 | `DateUtil.format(date, "yyyy-MM-dd")` |
| 解析 | `SimpleDateFormat.parse` | `DateUtil.parse(s)` / `LocalDate.parse(s, fmt)` |
| 当前时间 | `new Date()`；裸 `LocalDateTime.now()` | `DateUtil.date()` / `LocalDateTime.now(ZONE)`（显式 ZoneId/Clock） |
| 当前格式化串 | 手写 format | `DateUtil.now()`（yyyy-MM-dd HH:mm:ss）/ `today()` |
| 加 N 天 | `Calendar` 手动 | `DateUtil.offsetDay(date, n)` / `localDate.plusDays(n)` |
| 加 N 月 | `Calendar` | `DateUtil.offsetMonth(date, n)` / `localDate.plusMonths(n)` |
| 差值（天） | `(b-a)/86400000` 手算 | `DateUtil.between(start, end, DateUnit.DAY)` |
| 当前秒级时间戳 | `System.currentTimeMillis()/1000` | `DateUtil.currentSeconds()` |
| 时间戳→Date | `new Date(ts)` | `DateUtil.date(ts)` |
| 日期范围列表 | 手写循环 | `DateUtil.rangeToList(start, end, DateField.DAY_OF_MONTH)` |
| 当天开始/结束 | 手算 | `DateUtil.beginOfDay(d)` / `endOfDay(d)` |
| 当月开始/结束 | 手算 | `DateUtil.beginOfMonth(d)` / `endOfMonth(d)` |

## 反例详解（antipattern）

### 1. `SimpleDateFormat` 线程不安全（最高危）
```java
// ✗ static 共享或注入 Bean，多线程并发 format/parse 会数据错乱甚至抛异常
//    （内部 Calendar 状态可变）
private static final SimpleDateFormat SDF = new SimpleDateFormat("yyyy-MM-dd");

// ✗ ThreadLocal<SimpleDateFormat> 是 workaround：有线程池复用/内存泄漏隐患，别用

// ✓ 方案A：java.time 的 DateTimeFormatter 本身线程安全，可 static 共享
private static final DateTimeFormatter FMT = DateTimeFormatter.ofPattern("yyyy-MM-dd");
String s = FMT.format(localDate);

// ✓ 方案B：处理遗留 Date，用 DateUtil（内部线程安全）
String s = DateUtil.format(date, "yyyy-MM-dd");
```

### 2. `Calendar` 月份从 0 易错
```java
// ✗ Calendar 月份 0-11，常写错；add 后需 getTime，繁琐
Calendar c = Calendar.getInstance();
c.set(Calendar.MONTH, 11); // 实际是 12 月
c.add(Calendar.DATE, 1);

// ✓ DateUtil 语义清晰
Date tomorrow = DateUtil.offsetDay(new Date(), 1);
// ✓ 或 java.time
LocalDate tomorrow = LocalDate.now(ZONE).plusDays(1);
```

### 3. `rangeToList` 第三参数是 `DateField` 不是 `DateUnit`
```java
// ✗ 第三参数类型错（DateUnit 是 between 用，rangeToList 用 DateField）
List<DateTime> r = DateUtil.rangeToList(start, end, DateUnit.DAY); // 编译错误

// ✓ DateField
List<DateTime> r = DateUtil.rangeToList(start, end, DateField.DAY_OF_MONTH);
// 带步长
List<DateTime> r = DateUtil.rangeToList(start, end, DateField.DAY_OF_MONTH, 7);
```

### 4. `now()` 返回格式化串，不是时间戳
```java
// ✗ 误以为 now() 返回 long 时间戳
long ts = DateUtil.now(); // 实际是 String "yyyy-MM-dd HH:mm:ss"

// ✓ 秒级时间戳用 currentSeconds
long sec = DateUtil.currentSeconds();
long ms  = System.currentTimeMillis();
```

### 5. 时间戳手除 1000 易错
```java
// ✗ int 溢出 + 单位混淆
int sec = (int)(System.currentTimeMillis() / 1000);

// ✓ 语义明确
long sec = DateUtil.currentSeconds();
```

### 6. 裸 `.now()` 隐式依赖 JVM 默认时区（Sonar java:S8688）
```java
// ✗ 裸 now() 用 JVM 默认时区：容器/云主机默认常是 UTC，与开发机（如 GMT+8）不一致，
//    跨天边界（日切、对账、到期判断）相差 8 小时；且无法注入 Clock 做时间相关单测
LocalDateTime now = LocalDateTime.now();
LocalDate today = LocalDate.now();

// ✓ 方案A：应用级统一时区常量，所有 now() 显式传入
public static final ZoneId ZONE = ZoneId.of("Asia/Shanghai");
LocalDateTime now = LocalDateTime.now(ZONE);

// ✓ 方案B（更佳，可测试）：注入 Clock，单测用 Clock.fixed() 冻结时间
@Bean public Clock clock() { return Clock.system(ZoneId.of("Asia/Shanghai")); }
LocalDateTime now = LocalDateTime.now(clock);
```
> 适用于所有 time-based `now()`：`LocalDate`/`LocalDateTime`/`LocalTime`/`ZonedDateTime`/`OffsetDateTime`/`YearMonth` 等。
> `Instant.now()` 不受时区影响可裸用，但为可测试性仍推荐 `Instant.now(clock)`。

## java.time 推荐（现代首选）

```java
// 应用级统一时区（或注入 Clock，见 antipattern 6）
private static final ZoneId ZONE = ZoneId.of("Asia/Shanghai");

// 格式化 / 解析
DateTimeFormatter fmt = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
String s = ldt.format(fmt);
LocalDateTime ldt = LocalDateTime.parse("2026-07-13 10:00:00", fmt);

// 加减
LocalDateTime expire = LocalDateTime.now(ZONE).plusHours(24);
LocalDate lastMonth  = LocalDate.now(ZONE).minusMonths(1);

// 日期差
long days = ChronoUnit.DAYS.between(start, end);

// Date ↔ LocalDateTime 互转（JDK 8+）
LocalDateTime ldt = new Date().toInstant().atZone(ZoneId.systemDefault()).toLocalDateTime();
Date d = Date.from(ldt.atZone(ZoneId.systemDefault()).toInstant());
```

## DateUtil 推荐（遗留 Date 场景）

```java
String s = DateUtil.format(order.getTime(), "yyyy-MM-dd HH:mm:ss");
Date d = DateUtil.parse("2026-07-13");

Date expire   = DateUtil.offsetHour(new Date(), 24);
long days    = DateUtil.between(createTime, now, DateUnit.DAY);

List<DateTime> range = DateUtil.rangeToList(start, end, DateField.DAY_OF_MONTH);
Date dayStart = DateUtil.beginOfDay(new Date());
```
