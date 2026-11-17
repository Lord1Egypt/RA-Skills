# 02 · 集合与 Stream

> Hutool `CollUtil`（`cn.hutool.core.collection`）+ `ListUtil`（同包，分块/分页）+ `CollStreamUtil`（分组/转Map 的正确工具）+ JDK `Stream`。
> **默认用 JDK `Stream` + `Collectors`**（原生完善→原生优先，见 SKILL 选型哲学第一档）；仅 `groupByKey`+`toMap` 链式多步组合时才用 `CollStreamUtil`。
> **分块/分页注意**：`partition`/`split`/`page` 在 `ListUtil`（`cn.hutool.core.collection.ListUtil`），**不在 `CollUtil`**——`CollUtil` 无这些方法。

## 规范速查

| 场景 | ✗ 禁止 | ✓ 推荐 |
|---|---|---|
| 判空 | `list == null \|\| list.isEmpty()` | `CollUtil.isEmpty(list)` |
| 判非空 | `list != null && !list.isEmpty()` | `CollUtil.isNotEmpty(list)` |
| 遍历前守卫 | `for(x : list)`（null NPE） | `if (CollUtil.isNotEmpty(list)) {...}` |
| 新建初始化 | `new ArrayList<>(); add(a); add(b);` | `CollUtil.newArrayList(a, b)` |
| 新建 Set | `new HashSet<>()` + add | `CollUtil.newHashSet(a, b)` |
| 分块（每 N 个一组） | `list.subList(from, to)` | `ListUtil.partition(list, size)`（**`CollUtil.partition` 不存在**，分块在 `ListUtil`） |
| 取第几页 | `subList` 手写 | `CollUtil.page(pageNum, pageSize, list)` |
| 按 key 分组 | 手写 `Map`+`for`+`computeIfAbsent` | **`Collectors.groupingBy(Bean::getX)`**（链式组合用 `CollStreamUtil.groupByKey`） |
| 转 Map | 手写 for+put | **Stream `Collectors.toMap(k, v)`**（链式组合用 `CollStreamUtil.toMap`） |
| 交集 | 手写双层循环 | `CollUtil.intersection(a, b)` |
| 并集 | 手写 | `CollUtil.union(a, b)` |
| 差集 | 手写 | `CollUtil.subtract(a, b)` |
| 去重 | 手写 Set 转换 | `CollUtil.distinct(list)` |
| 取字段列表 | 手写 for | `CollUtil.getFieldValues(list, "name")` |
| 是否包含 | `list.contains(x)`（null 不安全） | `CollUtil.contains(list, x)` |
| 排序 | `Collections.sort` + Comparator 冗长 | `CollUtil.sort(list, Comparator.comparing(...))` |
| 反转 | 手写 | `CollUtil.reverse(list)` |
| 取首/尾 | `list.get(0)`/`list.get(size-1)` | `CollUtil.getFirst(list)`/`getLast(list)` |
| 取下标（含负） | `list.get(i)`（越界抛） | `CollUtil.get(list, i)`（-1 表末尾，越界返 null） |

## 反例详解（antipattern）

### 1. `subList` 分页/分块：越界 + 视图耦合
```java
// ✗ subList 是原 List 的视图；越界抛异常；原 List 改动抛 ConcurrentModificationException
int from = page * size;
List<Item> pageItems = list.subList(from, from + size); // from+size 越界？

// ✓ ListUtil.partition 自动处理边界，返回独立子列表（注意：CollUtil 无 partition，在 ListUtil）
List<List<Item>> chunks = ListUtil.partition(list, 50);
// ✓ 取指定页（0 基，CollUtil.page 存在）
List<Item> p = CollUtil.page(0, 50, list);
```

### 2. 分组手写冗长（且 `CollUtil.groupBy` 不存在）
```java
// ✗ 手写 Map + for，null key 需额外判空
Map<String, List<User>> m = new HashMap<>();
for (User u : users) {
    m.computeIfAbsent(u.getDept(), k -> new ArrayList<>()).add(u);
}
// ✗ 错误：CollUtil 没有 groupBy(list, Function) 这个签名
Map<String, List<User>> m = CollUtil.groupBy(users, User::getDept); // 编译错误

// ✓ 默认：JDK 原生 Stream（本指南「原生优先」）
Map<String, List<User>> byDept = users.stream().collect(Collectors.groupingBy(User::getDept));
// 仅 groupByKey + toMap 链式多步组合时才用 CollStreamUtil.groupByKey
// Map<String, List<User>> byDept = CollStreamUtil.groupByKey(users, User::getDept);
```
> 同类「CollUtil 上不存在」的误用：`CollUtil.shuffle`（用 `Collections.shuffle`）、`CollUtil.toMap(list, k, v)`（CollUtil 的 toMap 需传入目标 Map）——遇到编译错误先查签名。

### 3. 转 Map 签名易错
```java
// ✗ CollUtil.toMap 不是这个签名（CollUtil 的 toMap 需要传入目标 Map）
Map<Long, String> idName = CollUtil.toMap(users, User::getId, User::getName); // 编译错误

// ✓ 默认：JDK 原生 Stream
Map<Long, String> idName = users.stream().collect(Collectors.toMap(User::getId, User::getName));
// 链式组合（分组后再转 Map 等）才用 CollStreamUtil.toMap
```

### 4. 遍历前判空遗漏 NPE
```java
// ✗ list 为 null 时 for 抛 NullPointerException
for (Item i : list) { ... }

// ✓ isEmpty 守卫
if (CollUtil.isNotEmpty(list)) {
    for (Item i : list) { ... }
}
```

### 5. 取首元素不判空
```java
// ✗ 空列表 get(0) 抛 IndexOutOfBoundsException
Item first = list.get(0);

// ✓ getFirst null 安全；CollUtil.get 支持负索引
Item first = CollUtil.getFirst(list);
Item last  = CollUtil.get(list, -1); // -1 = 末尾
```

### 6. `Arrays.asList` 返回固定大小（SonarQube）
```java
// ✗ Arrays.asList 返回 Arrays$ArrayList（固定大小，非 java.util.ArrayList）
List<String> list = Arrays.asList("a", "b", "c");
list.add("d");  // UnsupportedOperationException

// ✓ 需要可变列表用 new ArrayList 包装，或 Hutool
List<String> list = new ArrayList<>(Arrays.asList("a", "b", "c"));
list.add("d");  // ✓
List<String> list2 = CollUtil.newArrayList("a", "b", "c"); // ✓ Hutool
```
> `Arrays.asList` 返回的是 `Arrays$ArrayList`（内部类，固定大小），**不是** `java.util.ArrayList`。支持 `set`（替换元素）但不支持 `add`/`remove`（结构变更）。需可变列表必须包装：`new ArrayList<>(Arrays.asList(...))` 或直接用 `CollUtil.newArrayList`。

### 7. `isEmpty()` 优于 `size() == 0`（SonarQube S2200）
```java
// ✗ size()==0 语义不直观；对 ConcurrentLinkedQueue 等集合 size() 是 O(n)
if (list.size() == 0) { ... }
if (map.size() == 0) { ... }

// ✓ isEmpty() 语义明确，通常 O(1)；CollUtil.isEmpty null 安全
if (list.isEmpty()) { ... }
if (CollUtil.isEmpty(list)) { ... }  // null 安全
```
> `isEmpty()` 语义比 `size() == 0` 更清晰，且对 `ConcurrentLinkedQueue` 等并发集合 `size()` 是 O(n) 操作（需遍历），`isEmpty()` 只检查首节点 O(1)。**统一用 `isEmpty()` 或 `CollUtil.isEmpty()`**。

### 8. `foreach` 中 `remove` → `ConcurrentModificationException`（阿里）
```java
// ✗ 增强 for（foreach）中 remove → ConcurrentModificationException
for (User u : users) {
    if (u.getAge() < 18) {
        users.remove(u);  // CME！modCount 不一致
    }
}

// ✓ Iterator.remove() 或 JDK 8+ removeIf
Iterator<User> it = users.iterator();
while (it.hasNext()) {
    if (it.next().getAge() < 18) it.remove();
}
// 或更简洁
users.removeIf(u -> u.getAge() < 18);
```
> 增强 for 内部用 Iterator 遍历，`remove` 走的是 `Collection.remove`（不走 Iterator），导致 `modCount` 不一致抛 `ConcurrentModificationException`。**遍历中删除用 `Iterator.remove()` 或 `removeIf`**，不要在 foreach 中直接 `remove`。

### 9. `HashMap` 已知大小时不预设容量（阿里）
```java
// ✗ 已知约 1000 条但不预设容量，默认 16 → 多次扩容（rehash 性能损耗）
Map<Long, User> map = new HashMap<>();

// ✓ 预设容量（减少扩容）
Map<Long, User> map = new HashMap<>(1024);
// 或 Hutool
Map<Long, User> map = MapUtil.newHashMap(1024);
```
> `HashMap` 默认初始容量 16，负载因子 0.75，超过 12 条就触发扩容。已知大小时预设容量避免多次 rehash。**精确公式**：`capacity = (expectedSize / 0.75) + 1`（向上取 2 的幂），但实际 `new HashMap<>(expectedSize)` 会自动向上取 2 的幂，直接传 expectedSize 即可。

## Stream 常用规范（JDK 8+）

```java
// 过滤 + 映射 + 收集
List<String> names = users.stream()
    .filter(u -> u.getAge() > 18)
    .map(User::getName)
    .collect(Collectors.toList());          // JDK 8

// JDK 16+ 可用 .toList()（返回不可变）
// List<String> names = users.stream().map(User::getName).toList();

// 转 Map（key 重复时保留前者）
Map<Long, User> byId = users.stream()
    .collect(Collectors.toMap(User::getId, u -> u, (a, b) -> a));

// 拼接字符串
String csv = list.stream().map(String::valueOf).collect(Collectors.joining(","));
```

> `Stream.toList()`（JDK 16+）返回**不可变**列表；`Collectors.toList()` 返回可变。按需选择，JDK 8 项目只能用后者。
> **Stream Gatherers（JDK 25+）**：JDK 25 LTS 提供 `java.util.stream.Gatherer`，支持自定义中间操作（弥补 `Collectors` 只能做终端操作的不足）。如 `Gatherers.windowFixed(n)` 固定窗口分组。详见 `09-modern-java.md`。

## 推荐示例

```java
// 判空守卫
if (CollUtil.isNotEmpty(orders)) { ... }

// 新建初始化
List<String> tags = CollUtil.newArrayList("a", "b", "c");

// 分块处理（ListUtil.partition，非 CollUtil）
List<List<Order>> chunks = ListUtil.partition(orders, 20);

// 分组（默认 JDK Collectors；链式组合才用 CollStreamUtil.groupByKey）
Map<Long, List<Order>> byUser = orders.stream().collect(Collectors.groupingBy(Order::getUserId));

// 交并差
List<Integer> both = new ArrayList<>(CollUtil.intersection(listA, listB));

// 取字段值列表
List<Object> names = CollUtil.getFieldValues(users, "name");
```
