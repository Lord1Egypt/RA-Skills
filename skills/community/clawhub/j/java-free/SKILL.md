---
slug: "java-free"
name: "java-free"
version: "1.0.0"
displayName: "Java基础版"
summary: "编写健壮 Java 代,提供核心能力"
summary_zh: "编写健壮 Java 代,提供核心能力"
license: "MIT"
description: "|- 编写健壮 Java 代码的基础能力，覆盖空指针防护、相等性判断 与基础异常处理. 核心能力:.该技能适用于相关开发场景,包含结构化的工作流程和配置指引.经过深度差异化处理,针对用户反馈和使用痛点进行了改进,提升了实用性和可操作性.该技能适用于相关开发场景,包含结构化的工作流程和配置指引.经过深度差异化处理,针对用户反馈和使用痛点进行了改进,提升了实用性和可操作性."

  - NullPointerException 防护与 Optional 基础用法

  - equals 与 hashCode 的正确实现

  - try-with-resources 与基础异常处理

  - 基础集合操作与不可变集合

  适用场景:

  - 日常 Java 开发、代码审查、缺陷修复

  - 独立开发者与一人公司效率提升

  - 自动化工作流中的 Java 代码生成

  差异化:基础版聚焦 Java 编程的高频陷阱防护，去除了高级版的并发陷阱、复杂泛型与 JVM 性能调优能力.
tags:
  - Other
  - 工具
  - 效率
  - 写作
  - java
  - equals
  - optional
  - hashcode
tools:
  - read
  - write
  - exec
homepage: ""
category: "Automation"
pricing_tier: free
---
# Java 基础版

## 核心能力

- NullPointerException 防护：识别潜在的空指针风险点，推荐使用 Optional、Objects.requireNonNull 与空值检查
- equals 与 hashCode 规范实现：依据 Object 契约正确实现 equals 与 hashCode，避免对称性、传递性与一致性陷阱
- try-with-resources 资源管理：对 AutoCloseable 资源使用 try-with-resources，确保流、连接、文件句柄正确释放
- 基础集合操作：推荐使用不可变集合（List.of、Map.of、Set.of）与 ArrayList、HashMap 的基础用法
- 基础异常处理：区分受检异常与非受检异常，避免捕获 Throwable 与吞没异常
#
## 快速开始

1. 确认运行环境满足依赖说明中的要求
2. 在AI Agent对话中调用本技能,提供必要的输入参数
3. 检查输出结果,根据需要进行后续处理

> 详细的输入输出格式请参考下方章节说明。

## 适用场景

| 场景 | 输入 | 输出 |
|---|---|---|
| 空指针检查 | 待审查的 Java 方法 | 风险点列表与修复建议 |
| equals 实现 | 类定义与字段 | 规范的 equals 与 hashCode 实现 |
| 资源管理 | 涉及 IO/连接的方法 | try-with-resources 改写建议 |
| 集合初始化 | 集合创建代码 | 推荐的不可变集合或 ArrayList 用法 |
| 异常处理 | try-catch 代码块 | 规范化建议与潜在问题 |

**不适用于**：复杂并发（如 synchronized、ReentrantLock、ConcurrentHashMap 原理）、复杂泛型（如通配符 PECS、类型擦除陷阱）、JVM 性能调优、Spring/Java EE 框架深度问题等场景（请使用高级版）

## 使用流程

1. 确认运行环境满足依赖说明中的要求
2. 读取待审查或待生成的 Java 代码
3. 按核心能力维度逐项分析（空指针、相等性、资源、集合、异常）
4. 给出问题清单与修复建议，必要时生成改写后的代码
5. 输出结果与执行日志

## 输入格式

| 参数名 | 类型 | 必填 | 说明 |
|:-----|:-----|:-----|:-----|
| code | string | 是 | 待审查的 Java 代码片段或文件路径 |
| focus | string | 否 | 关注维度，可选: null/equals/resources/collection/exception/all，默认: all |
| strict_level | string | 否 | 审查严格度，可选: strict/normal/loose，默认: normal |
| output_format | string | 否 | 输出格式，可选: markdown/json/text，默认: markdown |

## 输出格式

```json
{
  "success": true,
  "data": {
    "overall_grade": "B",
    "total_score": 82,
    "max_score": 100,
    "summary": "发现 2 个空指针风险点与 1 个 equals 实现问题",
    "details": [
      {
        "item": "空指针防护",
        "status": "warn",
        "score": 75,
        "comment": "第 12 行的返回值未做空检查，建议使用 Optional.ofNullable"
      },
      {
        "item": "equals 实现",
        "status": "fail",
        "score": 60,
        "comment": "equals 未先比较引用再比较字段，且未处理 null 情况"
      },
      {
        "item": "资源管理",
        "status": "step_done",
        "score": 95,
        "comment": "已正确使用 try-with-resources"
      }
    ],
    "improvements": [
      {
        "priority": "high",
        "suggestion": "为 getUser 返回值添加 Optional 包装",
        "expected_gain": "+8分"
      },
      {
        "priority": "medium",
        "suggestion": "重写 equals 方法，加入 getClass 与 null 检查",
        "expected_gain": "+5分"
      }
    ]
  },
  "error": null
}
```

## 异常处理

| 错误场景 | 原因 | 处理方式 |
|---:|---:|---:|
| 代码无法解析 | 语法错误或不完整的 Java 代码 | 提示用户修正语法后检查网络连接和配置后重试，标记错误位置 |
| 文件不存在 | code 参数为路径但文件不存在 | 检查路径是否为绝对路径，确认文件存在 |
| focus 维度无效 | focus 参数值不在可选范围内 | 提示可选值列表，建议使用默认值 all |
| 输出格式不支持 | output_format 参数值无效 | 回退为默认 markdown 格式并提示 |

## 依赖说明

### 运行环境
- **Agent平台**: 支持SKILL.md规范的任意AI Agent
- **操作系统**: Windows / macOS / Linux
- **Java 版本**: 建议 JDK 11 及以上（涉及 Optional、List.of 等 API）

### 依赖项
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:---:|:---:|:---:|:---:|
| LLM API | API | 必需 | 由Agent内置LLM提供 |

### API Key 配置
- 本Skill基于指令驱动，无需额外API Key

### 可用性分类
- **分类**: MD+EXEC（）
- **说明**: 基于Markdown的AI Skill，通过自然语言指令驱动Agent执行Java代码审查

## 案例展示

### 示例1：审查一个 Service 方法

```
输入: code=UserServiceImpl.java 片段, focus=null
处理: 识别返回值未包装 Optional -> 标记风险点 -> 给出修复建议
输出: 空指针防护得分 75，建议使用 Optional.ofNullable
```

### 示例2：生成 equals 与 hashCode

```
输入: code=仅包含字段定义的 User 类, focus=equals
处理: 依据字段生成规范的 equals 与 hashCode -> 校验契约
输出: 包含 getClass 检查、null 检查与字段比较的完整实现
```

## 常见问题

### Q1: 如何开始使用 Java 基础版？
A: 查看使用流程章节，准备待审查的 Java 代码，然后按"输入格式"提供 code 与 focus 参数即可.
### Q2: 审查严格度 strict、normal、loose 有何区别？
A: strict 会标记所有潜在风险点（包括风格问题）；normal 聚焦明确的缺陷；loose 仅报告高风险问题。建议初次使用选择 normal.
### Q3: Java 基础版支持并发问题审查吗？
A: 不支持。基础版聚焦空指针、相等性、资源、集合与异常五个维度，如需审查并发陷阱、复杂泛型、JVM 调优，请升级至高级版.
### Q4: 如何获取并发陷阱防护、复杂泛型、JVM 性能调优等高级能力？
A: 这些属于高级版能力。基础版聚焦高频陷阱防护，如需深入并发（synchronized、volatile、ConcurrentHashMap）、泛型（PECS、类型擦除）与 JVM 调优能力，请升级至高级版.
## 错误处理

| 错误场景(续)| 原因 | 处理方式 |
|:---------|---------:|:---------|
| LLM响应超时或无响应 | 网络延迟或模型负载过高 | 检查网络连接和配置后重试；确认Agent平台LLM服务正常 |
| 输入内容格式不正确 | 用户输入不符合skill预期格式 | 检查输入是否符合skill使用说明中的格式要求，参考示例章节 |
| 执行结果与预期不符 | 指令描述不够明确或上下文不足 | 提供更详细的指令描述，补充必要的上下文信息 |
| 命令执行失败 | 运行环境不满足要求或权限不足 | 确认运行环境符合依赖说明中的要求；检查命令权限设置 |

## 已知限制

- 不支持并发问题审查（synchronized、volatile、ReentrantLock、死锁、线程安全集合）
- 不支持复杂泛型分析（通配符 PECS、类型擦除、桥接方法）
- 不支持 JVM 性能调优（GC 策略、内存模型、字节码分析）
- 不支持 Spring、Java EE、JavaFX 等框架深度问题
- 不支持模块化系统（module-info.java）的分析
- equals 与 hashCode 生成仅覆盖基础场景，不涉及继承体系下的复杂实现
