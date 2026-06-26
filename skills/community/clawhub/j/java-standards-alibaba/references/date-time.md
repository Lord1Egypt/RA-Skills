# 日期时间

> 来源: Java开发手册（嵩山版）— 一(五) 日期时间

## 【强制】规则

### 1. 年份用小写 y

日期格式化时，`yyyy` 表示当天所在年，大写的 `YYYY` 代表 week in which year，跨年时返回下一年。

> **正例**: `new SimpleDateFormat("yyyy-MM-dd HH:mm:ss")`

### 2. 区分 M/m 和 H/h

| 字母 | 含义 |
|------|------|
| `M` | 月份 |
| `m` | 分钟 |
| `H` | 24 小时制 |
| `h` | 12 小时制 |

### 3. 获取毫秒数

`System.currentTimeMillis()`，不是 `new Date().getTime()`。

> **说明**: 纳秒级用 `System.nanoTime()`；JDK8 推荐 `Instant` 类。

### 4. 禁止使用 java.sql.Date/Time/Timestamp

不允许在程序任何地方中使用:
1. `java.sql.Date` — 不记录时间，`getHours()` 抛异常
2. `java.sql.Time` — 不记录日期，`getYear()` 抛异常
3. `java.sql.Timestamp` — 时间比较时触发 JDK BUG（JDK9 已修复）

### 5. 不写死一年为 365 天

避免在公历闰年时出现日期转换错误。

> **正例**: `LocalDate.now().lengthOfYear()`  
> **反例**: `int[] dayArray = new int[365];` 闰年数组越界

## 【推荐】规则

### 6. 注意闰年 2 月问题

闰年的 2 月份有 29 天，一年后的那一天不可能是 2 月 29 日。

### 7. 月份用枚举或 Calendar 常量

Date、Calendar 等月份取值在 0-11 之间（0-based）。

> **正例**: `Calendar.JANUARY` / `Calendar.FEBRUARY`
