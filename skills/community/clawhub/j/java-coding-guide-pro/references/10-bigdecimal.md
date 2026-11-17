# 10 · 浮点数与 BigDecimal

> **金额/利率/单价必须 `java.math.BigDecimal`**（JDK 原生，禁 `double`/`float` 算钱——二进制浮点无法精确表示十进制小数）。
> **浮点比较禁 `==`**；**舍入用 `RoundingMode` 枚举**（禁 `BigDecimal.ROUND_*` 废弃常量）。纯 JDK，无第三方依赖。

## 规范速查

| 场景 | ✗ 禁止 | ✓ 推荐 |
|---|---|---|
| 金额/单价/利息计算 | `double total = price * qty` | `BigDecimal` 运算 |
| 构造 BigDecimal | `new BigDecimal(0.1)` | `BigDecimal.valueOf(0.1)` / `new BigDecimal("0.1")` |
| 除法 | `bd1.divide(bd2)` 裸除 | `bd1.divide(bd2, scale, RoundingMode.HALF_UP)` |
| 相等比较 | `bd1.equals(bd2)` | `bd1.compareTo(bd2) == 0` |
| 舍入模式 | `BigDecimal.ROUND_HALF_UP` | `RoundingMode.HALF_UP` |
| 浮点相等 | `if (d == 0.1)` | `Math.abs(d - 0.1) < 1e-9` 或用 BigDecimal |
| 金额格式化 | 手拼字符串 | `bd.setScale(2, RoundingMode.HALF_UP).toPlainString()` |
| 取整 | `(int) x` 截断 | `bd.setScale(0, RoundingMode.HALF_UP)` |

## 反例详解（antipattern）

### 1. `double`/`float` 算钱（最高危）
```java
// ✗ 二进制浮点无法精确表示 0.1（如同十进制无法精确表示 1/3）；累计放大误差
double total = 0.1 + 0.2;          // 0.30000000000000004
double sum = 19.99 * 3;            // 59.970000000000006

// ✓ BigDecimal 精确十进制
BigDecimal total = BigDecimal.valueOf(0.1).add(BigDecimal.valueOf(0.2)); // 0.3
BigDecimal sum = new BigDecimal("19.99").multiply(BigDecimal.valueOf(3)); // 59.97
```
> 金额、利率、单价一律 BigDecimal。超大规摸对性能敏感时可用 `long` 分存储（见文末选型）。

### 2. `new BigDecimal(double)` 带入误差
```java
// ✗ double 的二进制误差原样带进 BigDecimal，得到超长近似值
BigDecimal bd = new BigDecimal(0.1);  // 0.1000000000000000055511151231257827021181583404541015625

// ✓ valueOf 内部先 Double.toString 再构造，符合直觉
BigDecimal bd = BigDecimal.valueOf(0.1); // 0.1
// ✓ 字符串字面量最稳（首选）
BigDecimal bd = new BigDecimal("0.1");   // 0.1
```

### 3. 除法不指定 scale → `ArithmeticException`
```java
// ✗ 除不尽（非终止小数）直接抛 Non-terminating decimal expansion
BigDecimal r = BigDecimal.ONE.divide(BigDecimal.valueOf(3)); // 抛异常

// ✓ 显式 scale + 舍入
BigDecimal r = BigDecimal.ONE.divide(BigDecimal.valueOf(3), 2, RoundingMode.HALF_UP); // 0.33
```

### 4. `equals` 比较 scale（陷阱）
```java
// ✗ equals 同时比较值与 scale：1.0 ≠ 1.00
new BigDecimal("1.0").equals(new BigDecimal("1.00"));  // false

// ✓ compareTo 只比值，是金额比较的正确语义
new BigDecimal("1.0").compareTo(new BigDecimal("1.00")) == 0; // true
```

### 5. 不可变——运算返回新对象
```java
// ✗ BigDecimal 不可变，add 不改变原对象；不接返回值等于没算
BigDecimal price = new BigDecimal("19.99");
price.add(BigDecimal.ONE);          // 结果丢弃，price 仍是 19.99

// ✓ 接住返回值
price = price.add(BigDecimal.ONE);  // 20.99
```

### 6. 废弃的 `ROUND_*` 常量
```java
// ✗ BigDecimal.ROUND_HALF_UP 等整型常量自 JDK 1.5 起废弃，无类型安全
bd.setScale(2, BigDecimal.ROUND_HALF_UP);

// ✓ RoundingMode 枚举
bd.setScale(2, RoundingMode.HALF_UP);
```

### 7. 浮点 `==` 比较
```java
// ✗ 浮点精度误差，== 不可靠
if (amount * 0.1 == 1.0) { ... }    // 数学上相等也可能 false

// ✓ 容差比较；或直接用 BigDecimal
if (Math.abs(amount * 0.1 - 1.0) < 1e-9) { ... }
```

### 8. `Math.abs(Integer.MIN_VALUE)` 仍为负（SonarQube S2133）
```java
// ✗ Math.abs(Integer.MIN_VALUE) == Integer.MIN_VALUE（仍为负！）
int x = Integer.MIN_VALUE;
int absX = Math.abs(x);  // -2147483648，仍为负 → 逻辑错误

// ✓ 边界处理：用 long 或显式判断
long absX = Math.abs((long) x);           // 2147483648L ✓
// 或
if (x == Integer.MIN_VALUE) {
    // 特殊处理边界值
}
```
> `Integer.MIN_VALUE` 是 `-2147483648`，其绝对值 `2147483648` 超过 `Integer.MAX_VALUE`（`2147483647`），`Math.abs` 对 `MIN_VALUE` 返回自身（仍为负）。同理 `Long.MIN_VALUE`。**对 `MIN_VALUE` 取绝对值时转 `long` 或显式边界处理**。`Math.absExact`（JDK 15+）会抛异常而非返回负值，适合需要严格正确性的场景。

### 9. 位运算 `byte` 符号扩展（SonarQube S3037）
```java
// ✗ byte 转 int 时高位符号扩展，导致拼接结果错误
byte b = (byte) 0xFF;        // -1
int result = b << 8;         // 0xFFFFFF00（符号扩展），不是 0x0000FF00

// ✓ 先 & 0xff 转 unsigned 再位移
int result = (b & 0xFF) << 8;  // 0x0000FF00 ✓
```
> `byte` 是有符号类型，`0xFF` 表示 `-1`。转 `int` 时 Java 做符号扩展：`0xFF` → `0xFFFFFFFF`（-1），位移后高位全是 1。**`byte` 参与位运算/拼接时先 `& 0xFF` 转无符号**（`0xFF & 0xFF = 0x000000FF`）。协议解析、二进制 IO、哈希计算等场景高发。

## 推荐示例

```java
// 金额计算：构造 → 运算 → 定精度 → 比较/格式化
BigDecimal price    = new BigDecimal("19.99");
BigDecimal qty      = new BigDecimal("3");
BigDecimal subtotal = price.multiply(qty);                          // 59.97
BigDecimal discount = new BigDecimal("0.05");                       // 5%
BigDecimal total = subtotal.multiply(BigDecimal.ONE.subtract(discount))
                             .setScale(2, RoundingMode.HALF_UP);    // 56.97

// 除法：显式 scale + 舍入
BigDecimal avg = total.divide(qty, 2, RoundingMode.HALF_UP);

// 比较：compareTo，不是 equals
if (total.compareTo(BigDecimal.ZERO) > 0) { ... }

// 确定性格式化（无 locale 依赖）
String s = total.setScale(2, RoundingMode.HALF_UP).toPlainString(); // "56.97"
// 千分位金额（显式 Locale，避免欧洲逗号小数点）
String money = String.format(java.util.Locale.US, "%,.2f", total);   // "56.97"
```

> **String.format 边界**：`String.format(Locale, pattern)` 用于 locale 数字/货币格式化是**允许**的（`StrUtil.format` 不支持 locale）；`01` 禁的是 `String.format` 做**字符串插值**（`%s` 占位），该场景用 `StrUtil.format("{}")` 更安全。

## 选型：BigDecimal（默认）与 `long` 分（仅超大规模性能场景）

```java
// 多数业务：BigDecimal（直观、精度可控，默认）
BigDecimal amount = new BigDecimal("100.50");

// 超大规模/对性能敏感：内部用 long 分存储，展示时还原
long cents = 10050L;                                       // = ¥100.50
BigDecimal display = BigDecimal.valueOf(cents).movePointLeft(2); // 100.50
```
> `long` 分方案无精度损失、运算快，但需统一约定单位、小心溢出。**除非有明确性能要求，默认 BigDecimal**。
