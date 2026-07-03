---
name: tdd
description: >
  Test-driven development with red-green-refactor loop. Build features or fix bugs one
  vertical slice at a time. 当用户说"写测试"、"测试先行"、"TDD"、"红绿重构"、
  "red-green-refactor"、"先写测试"、"写功能"、"实现"、"开发"，或提到"测试"、
  "test-first"、"unit test"、"integration test"时触发。强制垂直切片：一次一个测试，
  只写让它通过的最少代码，严禁水平切片（先写所有测试再写所有实现）。
---

# TDD — 测试驱动开发

> 原始理念来自 Matt Pocock，源自《The Pragmatic Programmer》和 Kent Beck。
> 在 Kimi 生态中，此 skill 为 model-invoked，在编码时自动触发。

## 核心原则

**测试应该验证行为，而不是实现。** 内部实现可以全改，测试不应该崩。

好的测试是**集成风格**的：它们通过公共 API exercising 真实代码路径。描述的是**系统做什么**，不是**怎么做**。

坏的测试绑定到实现：mock 内部协作者、测试私有方法、通过外部手段验证（如直接查数据库而不是走接口）。警告信号：重构后测试崩了，但行为没变。

## 反模式：水平切片

**绝对不要先写所有测试，再写所有实现。** 这是"水平切片"——把 RED 当成"写所有测试"，把 GREEN 当成"写所有代码"。

这会产生**垃圾测试**：
- 批量写的测试验证的是**想象的行为**，不是**实际的行为**
- 你最终测试的是**形状**（数据结构、函数签名），而不是用户-facing 的行为
- 测试对真实变化不敏感——行为崩了测试还过，行为没问题测试却崩了

### 正确方式：垂直切片（Tracer Bullets）

```
WRONG (水平):
  RED:   test1, test2, test3, test4, test5
  GREEN: impl1, impl2, impl3, impl4, impl5

RIGHT (垂直):
  RED→GREEN: test1→impl1
  RED→GREEN: test2→impl2
  RED→GREEN: test3→impl3
  ...
```

每个测试回应你从上一个循环中学到的东西。因为你刚写完代码，所以你知道什么行为重要、怎么验证。

## 工作流

### 1. 规划

写代码前：
- [ ] 与用户确认需要哪些接口变化
- [ ] 与用户确认哪些行为要测试（优先排序）
- [ ] 识别深模块机会（小接口，深实现）
- [ ] 列出要测试的行为（不是实现步骤）
- [ ] 获取用户批准计划

**问用户**："公共接口应该长什么样？哪些行为最重要？"

### 2. Tracer Bullet（第一枪）

写一个测试，确认系统的一个行为：

```
RED:   写第一个行为的测试 → 测试失败
GREEN: 写最少代码让它通过 → 测试通过
```

这是你的 tracer bullet，证明路径端到端能走通。

### 3. 增量循环

对每个剩余行为：

```
RED:   写下一个测试 → 失败
GREEN: 写最少代码让它通过 → 通过
```

规则：
- 一次一个测试
- 只写当前测试通过所需的最少代码
- 不要预测未来的测试
- 测试聚焦在**可观察行为**

### 4. Refactor（重构）

所有测试通过后：
- [ ] 提取重复
- [ ] 深化模块（把复杂度移到简单接口后面）
- [ ] 自然地应用 SOLID 原则
- [ ] 考虑新代码揭示了什么关于旧代码的信息
- [ ] 每次重构后运行测试

**RED 时绝不重构。** 先变绿。

## 每循环检查清单

```
[ ] 测试描述行为，不是实现
[ ] 测试只使用公共接口
[ ] 测试在内部重构后能存活
[ ] 代码是当前测试所需的最少
[ ] 没有添加推测性功能
```

## 测试运行（Kimi 生态适配）

在 Kimi Work 中：
- 用 `Bash` 或 `PythonRun` 运行测试命令
- 用 `Read` 查看测试文件和源码

在 Kimi Claw / OpenClaw 中：
- 描述为"执行项目测试命令"，由 OpenClaw 环境解析执行
- 如果无法直接执行，AI 生成测试代码，用户手动运行后反馈结果

## 触发场景（中文关键词）

- "写测试"
- "测试先行"
- "TDD"
- "红绿重构"
- "red-green-refactor"
- "先写测试"
- "写功能"
- "实现"
- "开发"
- "测试"
- "test-first"
- "unit test"
- "integration test"
- "重构"
- "加功能"
- "修 Bug"

## 关联技能

- 前置：`codebase-design`（设计接口时确定测试面）
- 配合：`domain-modeling`（测试命名使用项目术语）
- 被 `diagnosing-bugs` 调用（修 Bug 时按 TDD 流程）
- 被 `implement` 调用（实现代码时）
