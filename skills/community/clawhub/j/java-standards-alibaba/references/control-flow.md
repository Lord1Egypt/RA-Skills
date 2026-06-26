# 控制语句

> 来源: Java开发手册（嵩山版）— 一(八) 控制语句

## 【强制】规则

### 1. switch 规则

- 每个 case 要么通过 `continue/break/return` 终止，要么注释说明继续执行到哪个 case
- 必须包含 `default` 语句，放在最后

### 2. switch String 外部参数判 null

当 switch 括号内变量为 String 且来自外部参数时，必须先进行 null 判断。

### 3. if/else/for/while/do 必须用大括号

即使只有一行代码，也禁止: `if (condition) statements;`

### 4. 三目运算符注意拆箱 NPE

表达式 1 或 2 中有一个是原始类型，或类型不一致时，会强制拆箱，可能抛 NPE。

> **反例**: `Integer result = (flag ? a * b : c);` 当 c 为 null 时抛 NPE

### 5. 高并发避免等值判断退出

使用大于或小于的区间判断代替"等于"判断。

> **反例**: 判断剩余奖品数量 == 0 终止发放，但并发错误导致数量变成负数，活动无法终止。

## 【推荐】规则

### 6. 中断逻辑后加空行

方法代码超过 10 行时，`return / throw` 等中断逻辑的右大括号后加一个空行。

### 7. 少用 if-else，用卫语句/策略模式

`if-else` 不超过 3 层。

> **正例**:
> ```java
> public void findBoyfriend(Man man) {
>     if (man.isUgly()) { System.out.println("..."); return; }
>     if (man.isPoor()) { System.out.println("..."); return; }
>     if (man.isBadTemper()) { System.out.println("..."); return; }
>     System.out.println("可以先交往一段时间看看");
> }
> ```

### 8. 条件判断中不执行复杂语句

将复杂逻辑判断的结果赋值给有意义的布尔变量名。

### 9. 不在表达式中插入赋值语句

> **反例**: `return (sync = fair) ? new FairSync() : new NonfairSync();`

### 10. 循环体操作移至循环外

定义对象、变量、获取数据库连接、不必要的 try-catch 操作。

### 11. 避免取反逻辑运算符

> **正例**: `if (x < 628)`  
> **反例**: `if (!(x >= 628))`

### 12. 公开接口入参保护

尤其是批量操作的接口。

### 13. 需要参数校验的情形

1. 调用频次低的方法
2. 执行时间开销很大的方法
3. 需要极高稳定性和可用性的方法
4. 对外提供的开放接口（RPC/API/HTTP）
5. 敏感权限入口

### 14. 不需要参数校验的情形

1. 极有可能被循环调用的方法（需注明外部检查）
2. 底层调用频度高的方法
3. private 方法且能确定调用方已检查
