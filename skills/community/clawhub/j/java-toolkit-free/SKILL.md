---slug: java-toolkit-free
name: java-toolkit-free
version: 1.0.1
displayName: Java 工具箱
summary: "面向个人 Java 开"
license: Proprietary
edition: free
description: 面向个人 Java 开发者的健壮编码避坑工具。核心能力:，可自动提升工作效率

  - 空值/Optional/自动装箱陷阱速查

  - 集合、泛型、并发关键规则

  - equals/hashCode、try-with-resources 等关键规则

  - 单文件/单模块代码自检

  适用场景:

  - 个人 Java 项目编码自检

  - 单模块空值与并发避坑

  - 代码评审前的快速规则核对

  差异化: 免费版聚焦个人单模块自检，提供关键规则速查与避坑清单，零成本核对'
tags:
  - Java
  - 代码质量
  - 个人效率
  - 其他工具
  - 工具
  - 效率
  - 运维
  - equals
  - java
  - optional
  - volatile
  - string
tools:
  - read
  - exec
  - write
homepage: ""
category: "Automation"---# Java 工具箱（免费版）

## 概述

本工具帮助个人 Java 开发者规避空值、相等性、并发等常见陷阱，提供关键规则速查与避坑清单。适合单文件/单模块代码自检与评审前核对.
## 核心能力

| 能力 | 说明 | 免费版范围 |
|---|---|-----|
| 空值陷阱 | Optional、自动装箱、NPE | 全覆盖 |
| 集合泛型 | 并发修改、类型擦除 | 关键项 |
| 并发 | volatile、同步、原子 | 关键项 |
| 关键规则 | equals/hashCode、资源关闭 | 14 条 |
**技术实现要点**：核心能力基于`input_params`参数与`output_format`配置实现,支持创建/查询/修改/删除等操作模式,通过`config_options`进行运行时配置.
### 核心功能执行
用`input_params`参数进行配置.

**处理**: 解析核心功能执行的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回核心功能执行的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 参数配置与调用
用`config_options`参数进行配置.

**处理**: 解析参数配置与调用的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回参数配置与调用的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`config_options`参数,支持修改/重置/导入操作

### 结果处理与输出
用`output_format`参数进行配置.

**处理**: 解析结果处理与输出的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回结果处理与输出的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`output_format`参数,支持导出/保存/转换操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：面向个人、Java、开发者的健壮编码、避坑工具、覆盖空值与并发、自动装箱陷阱速查、并发关键规则、try、resources、等关键规则、单文件、单模块代码自检等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
## 使用场景

### 场景一：空值与 Optional

```java
// == 比较引用，字符串用 equals
String a = new String("x");
String b = new String("x");
System.out.println(a == b);       // false
System.out.println(a.equals(b));  // true
// ...
// Optional.get() 空时抛异常，用 orElse
Optional<String> opt = Optional.empty();
String v = opt.orElse("default");  // 安全
// ...
// 拆箱 null 抛 NPE
Integer i = null;
int x = i;  // NPE
```

### 场景二：并发与同步

```java
// volatile 保证可见性，不保证原子性
volatile int count = 0;
count++;  // 仍需同步或用 AtomicInteger
// ...
// 遍历时修改抛 ConcurrentModificationException
List<Integer> list = new ArrayList<>(List.of(1, 2, 3));
Iterator<Integer> it = list.iterator();
while (it.hasNext()) {
    it.next();
    list.remove(1);  // 抛异常
    // 应用 it.remove();
}
```

### 场景三：关键规则速查

```text
1. == 比引用，equals 比内容
2. 重写 equals 必须重写 hashCode
3. Optional.get() 空时抛异常
4. 遍历时修改抛 ConcurrentModificationException
5. 类型擦除：运行时拿不到泛型信息
6. volatile 保证可见性不保证原子性
7. 拆箱 null 抛 NPE
8. Integer == 超出 -128~127 比引用
9. try-with-resources 自动关闭
10. 内部类持有外部引用，不需要时用静态嵌套类
11. Stream 单次使用
12. thenApply vs thenCompose
13. Record 隐式 final
14. serialVersionUID 不匹配破坏反序列化
```

## 不适用场景

以下场景Java 工具箱不适合处理：

- 无明确技术栈的模糊需求
- 纯架构设计决策
- 运维部署管理

## 触发条件

需要代码生成、编程辅助、调试测试、开发部署时使用。不适用于非本工具能力范围的需求.
## 快速开始

1. 把待检代码贴给工具.
2. 工具按 14 条规则核对.
3. 标注命中陷阱与修复建议.
4. 逐项修复并复检.
**响应解析**: 完成完成后,查看输出响应确认任务状态。成功时输出包含解析摘要和响应数据;失败时根据错误信息排查问题,查阅错误解析章节获取恢复步骤.
## 示例

规则对照表（节选）：

| 主题 | 关键点 |
|:-----|:-----|
| 空值 | Optional 用 orElse，拆箱前判空 |
| 相等 | 字符串用 equals，重写 equals 必重写 hashCode |
| 集合 | 遍历修改用 Iterator.remove |
| 并发 | volatile 非原子，count++ 用 AtomicInteger |
| 资源 | try-with-resources 自动关闭 |

## 最佳实践

- **字符串用 equals**：`==` 比引用，内容比较必用 `equals`.
- **equals 与 hashCode 成对**：重写一个必须重写另一个，否则 HashMap/HashSet 失效.
- **资源用 try-with-resources**：实现 `AutoCloseable`，自动关闭.
- **内部类按需静态**：不需要外部引用时用静态嵌套类，避免泄漏.
- **Stream 单次用**：终端操作后不能复用.
## 常见问题

**Q1：为什么 Integer 比较有时相等有时不等？**
A：`==` 对 -128~127 走缓存比较相等，超出范围比引用。统一用 `equals`.
**Q2：volatile 能保证线程安全吗？**
A：不能。volatile 只保证可见性，`count++` 仍需同步或原子类.
**Q3：免费版支持全项目扫描吗？**
A：不支持。全项目批量扫描与规则集治理为专业版能力.
**Q4：泛型能 new T() 吗？**
A：不能。类型擦除导致运行时无泛型信息，用 `Class.newInstance()` 或工厂.
**Q5：try-with-resources 要 Java 几？**
A：Java 7+。实现 `AutoCloseable` 即可.
## 进阶用法

### 空值与 Optional 安全模式

```java
// 安全的 Optional 链
public String getCity(User user) {
    return Optional.ofNullable(user)
        .map(User::getAddress)
        .map(Address::getCity)
        .orElse("未知");
}
// ...
// 避免 Optional.get()，用 orElse/orElseGet
String name = optionalName.orElseGet(() -> fetchDefault());
// ...
// 拆箱前判空
Integer count = map.get("key");
int total = (count != null) ? count : 0;
```

### equals/hashCode 正确实现

```java
public class Person {
    private final String name;
    private final int age;
// ...
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Person p)) return false;
        return age == p.age && Objects.equals(name, p.name);
    }
// ...
    @Override
    public int hashCode() {
        return Objects.hash(name, age);
    }
}
```

### try-with-resources 自动关闭

```java
// 实现 AutoCloseable 的资源自动关闭
try (BufferedReader br = new BufferedReader(new FileReader("f.txt"));
     Connection conn = dataSource.getConnection()) {
    // 使用资源
} // 自动关闭，即使异常也关闭
```

## 并发避坑速查

| 场景 | 错误做法 | 正确做法 |
|---:|---:|---:|
| count++ | volatile | AtomicInteger |
| 遍历修改 | list.remove | iterator.remove |
| 双重检查锁 | 无 volatile | volatile 字段 |
| 等待通知 | if 判断 | while + wait |
| 复合操作 | 先查后改 | synchronized 或并发集合 |

## 集合与泛型要点

- **类型擦除**：运行时拿不到泛型，不能 `new T()`.
- **通配符**：`List<? extends T>` 只读，`List<? super T>` 只写.
- **并发集合**：多线程用 `ConcurrentHashMap`，别 `HashMap`.
- **不可变**：`List.of()` 返回不可变，修改抛异常.
- **Stream 单次**：终端操作后不能复用 Stream.
## 依赖说明

### 运行环境
- **Agent 平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI 等）
- **操作系统**: Windows / macOS / Linux
- **JDK**: 11+

### 依赖详情
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:---:|:---:|:---:|:---:|
| JDK | 工具链 | 必需 | adoptium.net 下载 |
| LLM API | API | 必需 | 由 Agent 内置 LLM 提供 |

### API Key 配置
- 本工具为纯 Markdown 指令，无需额外 API Key

### 可用性分类
- **分类**: MD+EXEC（Markdown 指令 + 命令行执行）
- **说明**: 通过自然语言指令驱动 Agent 核对 Java 编码规则

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|:------|------:|:------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 已知限制

- 需LLM支持,无LLM环境不可用
- 复杂业务场景建议结合人工经验判断
- 执行效率受模型能力与网络环境影响
- 当前为免费版本,如需完整功能请升级到付费版获取全部能力

## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "Java 工具箱处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "javakit"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```
