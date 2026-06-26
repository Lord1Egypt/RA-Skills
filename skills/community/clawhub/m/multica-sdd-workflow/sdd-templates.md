# SDD Document Templates

Step 0-A 新建规范时使用的文档格式。

---

## spec.md

```markdown
# Feature NNN: <功能名>

## 概述
一段话说明这个功能做什么、为什么做。

## 用户故事
- As a <用户>, I want <能力>, so that <价值>

## 功能需求
- FR-1: ...
- FR-2: ...

## 非功能需求
- NFR-1: 性能（如启动 < 2s）
- NFR-2: 安全（如无网络调用）

## 验收标准
- [ ] 条件1
- [ ] 条件2
```

---

## plan.md

```markdown
# Technical Plan: <功能名>

## 架构决策
说明技术选型理由（对应宪法 Article IV § 4.2 依赖审查）

## 模块划分
- src/lib/<module>/ — 职责描述（宪法 Article I Library-First）
- src/main/<file>  — 职责描述

## 接口定义（宪法 Article II Interface Clarity）
每个公开函数的签名、输入/输出、错误条件

## 实现阶段
Phase N → Phase N+1 的依赖关系
```

---

## tasks.md — 单个 Task 格式

```markdown
### Task N.X: <标题> [RED/GREEN/REFACTOR]

**Owner**: _Unassigned_
**Estimated Time**: 1 hour
**Dependencies**: Task N.(X-1)
**Priority**: Critical / High / Medium
**TDD Phase**: RED 🔴 / GREEN 🟢

**Steps**:
1. 文件路径
2. 具体操作

**Acceptance Criteria**:
- [ ] 条件1（可验证）
- [ ] 条件2
```

> **规则**：RED 任务（写测试）必须在对应 GREEN 任务（写实现）之前，且分别提交。
