# 常量定义

> 来源: Java开发手册（嵩山版）— 一(二) 常量定义

## 【强制】规则

### 1. 禁止魔法值

不允许任何魔法值（即未经预先定义的常量）直接出现在代码中。

> **反例**:
> ```java
> String key = "Id#taobao_" + tradeId;  // 应定义为常量
> cache.put(key, value);
> ```

### 2. Long 赋值使用大写 L

在 `long` 或者 `Long` 赋值时，数值后使用大写字母 `L`，不能是小写字母 `l`。

> **说明**: `Long a = 2l;` 写的是数字的 21，还是 Long 型的 2？

## 【推荐】规则

### 3. 按功能归类维护常量

不要使用一个常量类维护所有常量，要按常量功能进行归类，分开维护。

> **正例**: `CacheConsts` 放缓存常量；`SystemConfigConsts` 放系统配置常量

### 4. 常量复用五层次

1. 跨应用共享常量: 二方库 `client.jar` 的 `constant` 目录
2. 应用内共享常量: 一方库子模块的 `constant` 目录
3. 子工程内部共享常量: 当前子工程的 `constant` 目录
4. 包内共享常量: 当前包下单独的 `constant` 目录
5. 类内共享常量: 类内部 `private static final`

### 5. 固定范围变量用 enum

如果变量值仅在一个固定范围内变化用 `enum` 类型来定义。

> **正例**:
> ```java
> public enum SeasonEnum {
>     SPRING(1), SUMMER(2), AUTUMN(3), WINTER(4);
>     private int seq;
>     SeasonEnum(int seq) { this.seq = seq; }
>     public int getSeq() { return seq; }
> }
> ```
