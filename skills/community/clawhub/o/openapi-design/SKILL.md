---
name: api-design
description: >
  API design specification and best practices skill.
  Use when: designing new APIs, reviewing existing APIs, generating API documentation,
  standardizing interface specifications.
  Chinese triggers: API设计, 接口规范, REST API, OpenAPI, 接口文档, API审查.
  English triggers: design API, REST API, OpenAPI, API documentation, API review, endpoint design.
  Provides: design principles, naming conventions, HTTP status codes, error formats,
  versioning strategy, OpenAPI templates, and review checklists.
---

# API Design Skill

API 设计规范与最佳实践技能，提供从设计到文档生成的完整指导。

## 核心能力

1. **API 设计原则** — RESTful 设计最佳实践
2. **命名规范** — 资源、端点、参数命名标准
3. **HTTP 状态码** — 完整状态码参考
4. **错误响应格式** — 统一错误结构
5. **版本管理** — URL 版本策略
6. **OpenAPI 模板** — 快速生成 API 文档
7. **审查清单** — 设计审查检查点

## 使用场景

### 场景 1: 设计新 API

1. 读取 `references/common/design-principles.md` 了解设计原则
2. 读取 `references/design/resource-modeling.md` 进行资源建模
3. 读取 `references/design/endpoint-design.md` 设计端点
4. 使用 `references/templates/openapi3-template.md` 生成 OpenAPI 文档
5. 使用 `references/review/api-review-checklist.md` 自查

### 场景 2: 审查现有 API

1. 读取 `references/review/api-review-checklist.md`
2. 按清单逐项审查
3. 输出审查报告

### 场景 3: 规范化接口

1. 读取 `references/common/naming-conventions.md` 检查命名
2. 读取 `references/common/error-response-format.md` 检查错误格式
3. 读取 `references/common/versioning-strategy.md` 检查版本策略
4. 生成整改建议

## 文件结构

```
api-design/
├── SKILL.md
└── references/
    ├── common/
    │   ├── design-principles.md
    │   ├── naming-conventions.md
    │   ├── http-status-codes.md
    │   ├── error-response-format.md
    │   └── versioning-strategy.md
    ├── design/
    │   ├── resource-modeling.md
    │   ├── endpoint-design.md
    │   └── security-best-practices.md
    ├── templates/
    │   └── openapi3-template.md
    ├── review/
    │   └── api-review-checklist.md
    └── documentation/
        └── doc-generation-guide.md
```
