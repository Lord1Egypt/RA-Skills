---
name: gi-code-review
description: Review code for quality, security, and maintainability following team standards. Use when reviewing pull requests, examining code changes, or when the user asks for a code review.
tags: ["code-review", "quality", "security", "best-practices", "vue", "fastapi", "python"]
---

# Code Review 代码审查

按照团队规范对代码进行质量、安全和可维护性审查。适用于 Vue3、FastAPI、Python 技术栈。

## 何时使用

- 用户请求代码审查
- 审查 Pull Request 或代码变更
- 用户提到「帮我看看这段代码」「review 一下」「代码质量」

## 审查清单

### 1. 正确性与逻辑

- [ ] 逻辑正确，处理边界情况
- [ ] 无明显的空指针/未定义访问
- [ ] 异步逻辑正确（async/await 配对）
- [ ] 错误处理完整，有 try/except 或 .catch()

### 2. 安全

- [ ] 无 SQL 注入（使用参数化查询）
- [ ] 无 XSS（Vue 已转义，注意 v-html）
- [ ] 敏感信息不硬编码（用 get_env 或配置）
- [ ] 接口有权限校验（如需要）

### 3. 代码风格与可维护性

- [ ] 符合项目约定（router/service/dao 分层）
- [ ] 函数职责单一，长度适中
- [ ] 命名清晰（变量、函数、路由）
- [ ] 有必要的注释和日志

### 4. 性能

- [ ] 无 N+1 查询（批量查询或 join）
- [ ] 大列表考虑分页
- [ ] 前端避免不必要的重复渲染

### 5. 测试

- [ ] 关键逻辑有测试覆盖
- [ ] 边界情况有测试

## 反馈格式

- 🔴 **必须修复**：影响正确性、安全或严重性能问题
- 🟡 **建议改进**：可读性、可维护性、最佳实践
- 🟢 **可选优化**：锦上添花

## 项目规范参考

- 后端：app/dao、app/service、app/router、app/model（entity/dto/vo）
- 数据库：使用 AsyncSqlSessionTemplate（insert/update/query_one/query_list）
- 报错：`from tkms.exception.api import ApiException`
- 配置：`from tkms import get_env`
- 前端：Vue3 + Ant Design，components/views/services 分层
