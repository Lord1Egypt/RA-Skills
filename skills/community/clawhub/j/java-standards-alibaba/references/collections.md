# 集合处理

> 来源: Java开发手册（嵩山版）— 一(六) 集合处理

## 【强制】规则

### 1. hashCode 和 equals

1. 覆写 `equals` 必须覆写 `hashCode`
2. Set 存储的对象必须覆写这两种方法
3. 自定义对象作为 Map 的键，必须覆写 `hashCode` 和 `equals`

### 2. isEmpty() 判空

判断集合是否为空，使用 `isEmpty()`，不是 `size()==0`。

### 3. Collectors.toMap() 必须用 mergeFunction

否则出现相同 key 会抛 `IllegalStateException`。

> **正例**: `Collectors.toMap(Pair::getKey, Pair::getValue, (v1, v2) -> v2)`

### 4. Collectors.toMap() value 为 null 会抛 NPE

> **说明**: HashMap 的 merge 方法中会检查 `value == null`。

### 5. subList 不可强转

`ArrayList.subList()` 返回的是内部类 SubList，强转 ArrayList 抛 `ClassCastException`。

### 6. keySet/values/entrySet 不可 add

使用 Map 的 `keySet()/values()/entrySet()` 返回的集合对象，不可以对其进行添加元素操作。

### 7. Collections.empty 不可修改

`Collections.emptyList()/singletonList()` 等都是 immutable list。

### 8. subList 场景注意父集合变更

对父集合元素的增加或删除，会导致子列表产生 `ConcurrentModificationException`。

### 9. 集合转数组用 toArray(T[])

必须使用集合的 `toArray(T[] array)`，传入类型一致、长度为 0 的空数组。

> **正例**: `String[] array = list.toArray(new String[0]);`

### 10. addAll() 前检查 NPE

在使用 `Collection` 实现类的 `addAll()` 方法时，都要对输入的集合参数进行 NPE 判断。

### 11. Arrays.asList() 不可修改

不能使用其 `add/remove/clear` 方法，会抛 `UnsupportedOperationException`。

### 12. 泛型通配符 PECS 原则

- `<? extends T>` — 不能 add（适合往外读取）
- `<? super T>` — 不能 get（适合往里插入）

### 13. 非泛型集合赋值给泛型集合需 instanceof

> **反例**: `List<String> generics = notGenerics;` 取元素抛 `ClassCastException`

### 14. foreach 中禁止 remove/add

remove 元素请使用 `Iterator` 方式，并发操作需对 Iterator 加锁。

> **正例**:
> ```java
> Iterator<String> iterator = list.iterator();
> while (iterator.hasNext()) {
>     String item = iterator.next();
>     if (删除条件) { iterator.remove(); }
> }
> ```

### 15. Comparator 三个条件

JDK7+，Comparator 实现类必须满足:
1. x, y 的比较结果与 y, x 相反
2. x>y, y>z, 则 x>z
3. x=y, 则 x,z 比较结果与 y,z 相同

> **反例**: `return o1.getId() > o2.getId() ? 1 : -1;` 没有处理相等

## 【推荐】规则

### 16. Diamond 语法

JDK7+ 使用 `<>` 或全省略。

> **正例**: `HashMap<String, String> cache = new HashMap<>(16);`

### 17. 集合初始化指定大小

> **说明**: `initialCapacity = (元素个数 / 0.75) + 1`。未确定时设为 16。

### 18. entrySet 遍历 Map

使用 `entrySet` 遍历 Map，而不是 `keySet`（keySet 遍历了 2 次）。JDK8 使用 `Map.forEach`。

### 19. Map K/V null 值注意

| 集合类 | Key | Value | 说明 |
|--------|-----|-------|------|
| Hashtable | 不允许 null | 不允许 null | 线程安全 |
| ConcurrentHashMap | 不允许 null | 不允许 null | JDK8: CAS |
| TreeMap | 不允许 null | 允许 null | 线程不安全 |
| HashMap | 允许 null | 允许 null | 线程不安全 |

### 20. 有序性与稳定性

- `ArrayList`: order/unsort
- `HashMap`: unorder/unsort
- `TreeSet`: order/sort

### 21. Set 去重优于 List.contains

利用 Set 元素唯一特性快速去重，避免使用 List 的 `contains()` 遍历。
