# Kiro Spec 模板

## 标准结构

每个 Spec 位于 `.kiro/specs/<feature-name>/` 目录下，包含三个核心文件：

```
.kiro/specs/user-authentication/
├── requirements.md    # 需求定义
├── design.md          # 技术设计
└── tasks.md           # 实现任务
```

---

## requirements.md 模板

```markdown
# Requirements Document

## Introduction

[1-2 段描述这个功能是什么，解决什么问题，为谁解决]

## Glossary

- **术语 1** - 定义
- **术语 2** - 定义

## Requirements

### Requirement 1: [功能名称]

**User Story:** As a [角色], I want [功能], so that [价值].

#### Acceptance Criteria

1. WHEN [条件], THE system SHALL [行为]
2. WHEN [条件], THE system SHALL [行为]
3. IF [边界条件], THE system SHALL [处理]

### Requirement 2: [功能名称]

**User Story:** As a [角色], I want [功能], so that [价值].

#### Acceptance Criteria

1. ...
```

---

## design.md 模板

```markdown
# Design Document

## Architecture Overview

[系统架构图或文字描述]

## Technical Decisions

### Decision 1: [技术选型]

**Options Considered:**
- Option A: [优缺点]
- Option B: [优缺点]

**Decision:** [最终选择 + 理由]

## Data Models

[数据库表结构/接口定义]

## API Design

[API 端点、请求/响应格式]

## Security Considerations

[认证、授权、数据保护措施]
```

---

## tasks.md 模板

```markdown
# Tasks

## Implementation Plan

### Phase 1: 基础架构
- [ ] Task 1.1: [具体任务描述]
  - 文件：`src/auth/login.ts`
  - 验收：通过单元测试
- [ ] Task 1.2: [具体任务描述]

### Phase 2: 核心功能
- [ ] Task 2.1: [具体任务描述]
- [ ] Task 2.2: [具体任务描述]

### Phase 3: 测试与优化
- [ ] Task 3.1: 编写集成测试
- [ ] Task 3.2: 性能优化

## Dependencies

- Task 2.1 依赖 Task 1.1 完成
- Task 3.1 依赖所有 Phase 2 任务完成

## Notes

[实现过程中的注意事项]
```

---

## 示例：完整 Spec

参考 Kiro 官方示例：
- `.kiro/specs/github-issue-automation/requirements.md`
- `.kiro/specs/github-issue-automation/design.md`
- `.kiro/specs/github-issue-automation/tasks.md`

---

## Spec 编写检查清单

创建 Spec 后，对照检查：

- [ ] 用户故事清晰（As a... I want... so that...）
- [ ] 验收标准可测试（WHEN/THE system SHALL 格式）
- [ ] 技术设计包含选型理由
- [ ] 任务拆解到可独立完成（<4 小时/任务）
- [ ] 依赖关系明确
- [ ] 包含安全考虑（如适用）
