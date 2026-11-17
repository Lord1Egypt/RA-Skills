# 12 · 认知复杂度（Sonar java:S3776）

> **规则**：单方法认知复杂度（Cognitive Complexity）≤ 15（Sonar 默认阈值）。
> **定级 A**：只约束新生成代码；存量超标方法不主动改写（见文末「存量治理」）。
> **核心策略**：Agent 无法边写边跑 Sonar——用「生成时预算」的代理信号预判，命中即先重构再输出。

## 计分规则速查（与圈复杂度的关键差异）

| 结构 | 计分 |
|---|---|
| `if` / `else if` / `else` / 三元 `?:` | 各 +1 |
| `for` / `while` / `do-while` / `catch` | 各 +1 |
| `switch` | **整体 +1**（不按 case 计——这是 switch 优于 else-if 链的原因） |
| **嵌套惩罚** | 嵌套的控制结构**额外 + 当前嵌套深度**（越深越贵） |
| 布尔运算符序列 | 同类连用计 1 次：`a && b && c` +1；每切换一次 +1：`a && b \|\| c` +2 |
| 递归调用 | +1 |
| lambda | 本身不计分，但**加一层嵌套深度**（内部控制结构更贵） |
| 标签 `break` / `continue` | +1（无标签的不计） |

> **嵌套是大头**：同样 4 个 `if`，平铺 = +4；嵌套 4 层 = 1+2+3+4 = **+10**。所以「降嵌套」的收益远大于「减分支」。

## 生成时预算（写代码时的代理信号）

生成/修改方法时自检，**命中任一条 → 先按下方手法重构，再输出**：

1. 嵌套 ≥ 3 层（`if`/循环/lambda 计层，`try` 不计）；
2. `else-if` 链 ≥ 3 连；
3. 单个布尔表达式 `&&`/`||` 混用且 ≥ 3 项；
4. 方法体跨越多个抽象层次（既有流程编排又有细节实现），或超约 60 行。

## 手法 1：卫语句早返回（性价比最高，专治嵌套惩罚）

```java
// ✗ 箭头形嵌套：1 + 2 + 3 = 6 分，主逻辑被推到最深处
public void ship(Order order) {
    if (order != null) {                      // +1
        if (order.isPaid()) {                 // +2（嵌套1层）
            if (!order.isShipped()) {         // +3（嵌套2层）
                doShip(order);
            }
        }
    }
}

// ✓ 卫语句平铺：1 + 1 + 1 = 3 分，主逻辑顶格
public void ship(Order order) {
    if (order == null) return;                // +1
    if (!order.isPaid()) return;              // +1
    if (order.isShipped()) return;            // +1
    doShip(order);
}
```
> 反转条件 + 提前退出，消掉全部嵌套惩罚；`else` 也随之消失（每个 `else` 都是 +1）。

## 手法 2：提炼语义方法（嵌套清零，每个方法独立预算）

```java
// ✗ 一个方法揉进「校验 + 计价 + 通知」三个抽象层次，循环里套 if 再套 if
public void process(List<Order> orders) {
    for (Order o : orders) {                          // +1
        if (o.isValid()) {                            // +2
            if (o.getAmount().signum() > 0) {         // +3
                // 20 行计价细节...
            }
        }
    }
}

// ✓ 按语义边界提炼：外层只剩编排，每个子方法从嵌套深度 0 重新计分
public void process(List<Order> orders) {
    for (Order o : orders) {                          // +1
        if (!isChargeable(o)) continue;               // +2
        applyPricing(o);
    }
}
private boolean isChargeable(Order o) { return o.isValid() && o.getAmount().signum() > 0; } // +1
private void applyPricing(Order o) { /* 计价细节，独立预算 */ }
```
> **提炼必须沿语义边界、方法名表达意图**。禁止为过门禁而 `doPart1()`/`doPart2()` 无语义切块——分数降了，复杂度只是被藏起来，这是 AI 重构最高频的假修复。

## 手法 3：分支分发（else-if 链 → switch / 策略 Map）

```java
// ✗ else-if 链每个分支 +1：4 分支 = +4，还会随业务持续膨胀
if (type == OrderType.NORMAL) { handleNormal(o); }
else if (type == OrderType.PRESALE) { handlePresale(o); }
else if (type == OrderType.GROUP) { handleGroup(o); }
else { handleDefault(o); }

// ✓ switch 整体只 +1（JDK 14+ 用 switch 表达式，JDK 8 用传统 switch + default）
switch (type) {
    case NORMAL  -> handleNormal(o);
    case PRESALE -> handlePresale(o);
    case GROUP   -> handleGroup(o);
    default      -> handleDefault(o);
}

// ✓ 分支会持续新增/各分支逻辑重（>5 行）时，升级为策略 Map 或枚举方法：分发处 0 分
private static final Map<OrderType, Consumer<Order>> HANDLERS = Map.of(
    OrderType.NORMAL, OrderHandlers::normal,
    OrderType.PRESALE, OrderHandlers::presale,
    OrderType.GROUP, OrderHandlers::group);
HANDLERS.getOrDefault(type, OrderHandlers::fallback).accept(o);
```
> 选型：分支固定且轻 → switch；分支持续增长或各分支成块 → 策略 Map / 枚举抽象方法（新增类型零改动分发处）。

## 手法 4：循环体内 continue 早跳过

```java
// ✗ 循环内嵌套 if：+1 +2 +3 = 6 分
for (Item item : items) {              // +1
    if (item.isActive()) {             // +2
        if (item.getStock() > 0) {     // +3
            sell(item);
        }
    }
}

// ✓ continue 平铺（无标签的 continue 不计分）：+1 +2 +2 = 5 分，且不再往深处长
for (Item item : items) {              // +1
    if (!item.isActive()) continue;    // +2
    if (item.getStock() <= 0) continue;// +2
    sell(item);
}
```

## 手法 5：复杂条件谓词化（把布尔逻辑移出方法）

```java
// ✗ 混用 && / || 且多项：+3（切换 2 次），读者需在脑内解括号
if (user != null && user.isActive() && (user.isVip() || user.getPoints() > 1000)) { ... }

// △ 命名局部变量：可读性提升，但分数仍留在本方法（11-conventions 第 15 条的做法）
boolean eligible = user != null && user.isActive() && (user.isVip() || user.getPoints() > 1000);
if (eligible) { ... }

// ✓ 提炼谓词方法：计分整体移出本方法，且可复用、可单测
if (isEligibleForDiscount(user)) { ... }
private boolean isEligibleForDiscount(User user) {
    return user != null && user.isActive() && (user.isVip() || user.getPoints() > 1000);
}
```
> 命名变量降认知负担、谓词方法降 Sonar 分——两者不冲突：条件被 ≥2 处复用或表达业务概念时用谓词方法，一次性条件用命名变量即可。

## 存量治理（审查/修改既有代码时）

- **不主动改写**存量超标方法（A 级）——高复杂度方法往往缺测试，盲目重构比不动更危险。
- 仅当审查发现**严重超标（约 ≥30，2 倍阈值）**且本次任务恰好要改该方法时，才建议重构，且顺序固定：**先补特征测试（characterization test）锁定现有行为 → 再按手法 1~5 拆解**。
- **禁止的假修复**：`// NOSONAR` / `@SuppressWarnings` 压制；调高项目阈值；无语义 `doPart1/doPart2` 切块（复杂度被藏起而非消除）。
