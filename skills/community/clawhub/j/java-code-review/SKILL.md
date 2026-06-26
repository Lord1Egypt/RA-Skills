---
name: java-code-review
description: Java 代码质量保障技能。用于 GitLab 项目分支合并前的 Code Review，支持：(1) 指定项目从 A 分支合并到 B 分支的代码变更审查；(2) 基于 Security/Performance/Correctness/Maintainability/Testing 五大维度进行代码质量检查；(3) 生成 CR 报告并追踪问题修复状态；(4) 用户确认后执行分支合并。触发词：code review、代码审查、合并代码、cr报告、分支合并。
---

# Java Code Review - 代码质量保障

作为 Java 资深专家，保障合并代码的质量。

## 工作流程

### 1. 接收任务

用户指定：

- **项目名称/ID**：GitLab 项目标识
- **源分支 (A)**：变更来源分支
- **目标分支 (B)**：合并目标分支

### 2. 获取代码变更

调用 GitLab API 获取差异 commits：

```
GET /api/v4/projects/{project_id}/repository/compare?from={目标分支}&to={源分支}
```

获取每个 commit 的 diff：

```
GET /api/v4/projects/{project_id}/repository/commits/{sha}/diff
```

### 3. 执行 Code Review

按以下维度逐项检查：

## Review 维度

| 维度              | 关注点                           | 优先级      |
| --------------- | ----------------------------- | -------- |
| Security        | SQL注入、XSS、CSRF、认证授权、密钥管理、敏感数据 | Critical |
| Performance     | N+1查询、内存泄漏、缓存策略、分页、文件流        | High     |
| Correctness     | 边界情况、空值处理、竞态条件、时区处理、错误传播      | High     |
| Maintainability | 命名规范、单一职责、DRY、复杂度、ORM规范       | Medium   |
| Testing         | 测试覆盖、边界测试、回归测试                | Medium   |

## Security Checklist

- [ ] SQL Injection — 所有查询使用参数化语句或ORM；无用户输入字符串拼接
- [ ] XSS — 用户内容在渲染前已转义/净化
- [ ] CSRF Protection — 状态变更请求需要有效CSRF令牌
- [ ] Authentication — 每个受保护端点在处理前验证用户身份
- [ ] Authorization — 资源访问限定在请求用户权限范围内；无IDOR漏洞
- [ ] Input Validation — 所有外部输入在服务端验证类型、长度、格式和范围
- [ ] Secrets Management — 源码中无API密钥、密码、令牌或凭证；秘密来自环境变量或vault
- [ ] Dependency Safety — 新依赖来自可信来源，积极维护，无已知CVE
- [ ] Sensitive Data — PII、令牌和秘密不记录日志、不包含在错误消息中、不在API响应中返回
- [ ] Rate Limiting — 公共和认证端点有速率限制
- [ ] File Upload Safety — 上传文件验证类型和大小，存储在webroot外
- [ ] HTTP Security Headers — 设置CSP、X-Content-Type-Options、HSTS

## Performance Checklist

- [ ] N+1 Queries — 数据库访问模式已批量或联接；无循环单独查询
- [ ] Memory Leaks — 事件监听器、订阅、定时器在卸载/销毁时清理
- [ ] Caching Strategy — 昂贵计算和API响应使用适当缓存
- [ ] Database Indexing — 查询在索引列上过滤/排序；新查询已用EXPLAIN检查
- [ ] Pagination — 列表端点和查询使用分页；无无界SELECT *
- [ ] Async Operations — 长时间运行任务卸载到后台作业或队列
- [ ] **严禁处理文件流** — 不允许在该系统中处理文件流，会影响整体服务的稳定性

## Correctness Checklist

- [ ] Edge Cases — 空数组、空字符串、零值、负数和最大值已处理
- [ ] Null/Undefined Handling — 可空值在访问前已检查
- [ ] Race Conditions — 共享状态的并发访问使用锁、事务或原子操作
- [ ] Timezone Handling — 日期以UTC存储；显示转换在表示层进行
- [ ] Error Propagation — 异步调用和外部服务的错误已捕获和处理
- [ ] State Consistency — 多步骤变更是事务性的；部分失败使系统处于有效状态

## Maintainability Checklist

- [ ] Naming Clarity — 变量、函数和类有描述性名称
- [ ] Single Responsibility — 每个函数/类/模块做一件事
- [ ] DRY — 重复逻辑提取到共享工具；复制粘贴块已合并
- [ ] Cyclomatic Complexity — 函数分支复杂度低；深度嵌套链已重构
- [ ] Dead Code Removal — 注释掉的代码、未使用的导入、不可达分支已删除
- [ ] Magic Numbers & Strings — 字面值提取到命名常量
- [ ] **ORM Operation** — ORM代码只允许在mapper层操作，包括mybatis plus的调用也只能在mapper层，其他包下不允许引用mybatis
- [ ] **Commented Code** — 任何地方不允许将原有代码注释掉提交，只能删除
- [ ] **SQL Business Logic** — sql里面不要带业务逻辑，包括魔数、固定值等，需由业务层传参进来
- [ ] **包命名规范** — 包名需要以 cn.ctg.travel.{项目名} 为前缀

## Testing Checklist

- [ ] Test Coverage — 新逻辑路径有对应测试
- [ ] Edge Case Tests — 测试覆盖边界值、空输入、null和错误条件
- [ ] No Flaky Tests — 测试是确定性的
- [ ] Meaningful Assertions — 测试断言行为和结果，而非实现细节
- [ ] Regression Tests — Bug修复包含重现原始bug的测试

### 4. 生成 CR 报告

报告格式：

```markdown
# CR Report - {项目名}

## 变更概述
- 源分支：{A}
- 目标分支：{B}
- Commits 数量：{N}
- 涉及文件数：{M}
- Commit Authors：{作者列表}

## 问题清单

### Critical (必须修复)
| 序号 | 问题描述 | 文件:行号 | Author | 建议修复方案 |
|------|---------|----------|--------|-------------|
| 1 | ... | ... | ... | ... |

### High (强烈建议)
...

### Medium (建议优化)
...

### Low (可选优化)
...

## 通过项
- [x] Security - 无安全漏洞
- [x] Performance - 性能可接受
...

## 总结与建议
...

## 合并建议
- [ ] 建议合并（无 Critical/High 问题）
- [ ] 修复后合并（存在 Critical/High 问题需修复）
- [ ] 不建议合并（存在严重问题）
```

### 5. 用户确认与合并

询问用户是否执行合并：

> CR 报告已生成。是否执行分支合并？
> 
> - 确认合并：将 `{源分支}` 合并到 `{目标分支}`
> - 取消：不执行合并

**用户确认后**，执行合并 API：

```
POST /api/v4/projects/{project_id}/merge_requests
{
  "source_branch": "{源分支}",
  "target_branch": "{目标分支}",
  "title": "Merge {源分支} into {目标分支}"
}
```

或直接合并：

```
POST /api/v4/projects/{project_id}/repository/commits
{
  "branch": "{目标分支}",
  "commit_message": "Merge branch '{源分支}'",
  "actions": []
}
```

## GitLab 配置

默认配置（可通过用户指定覆盖）：

| 配置项       | 值                                     |
| --------- | ------------------------------------- |
| GitLab 地址 | https://git.xxx.com                   |
| 认证方式      | PRIVATE-TOKEN 或 Authorization: Bearer |
| Token 来源  | TOOLS.md 或用户指定                        |

## 使用示例

### 示例 1：指定项目分支合并

```
用户：帮我 review openapi 项目，从 release-20260324 合并到 test 分支
```

执行步骤：

1. 获取 compare：`from=test&to=release/release-20260324`
2. 获取差异 commits 和 diffs
3. 执行 CR 检查
4. 生成报告
5. 询问是否合并

### 示例 2：查看特定 commit 变更

```
用户：帮我检查 ctg-travel-order 项目的 commit abc123
```

执行步骤：

1. 获取该 commit 的 diff
2. 执行 CR 检查
3. 生成单 commit 报告

## 注意事项

1. **安全优先**：Critical 问题必须修复才能合并
2. **责任追溯**：每个问题都关联 Commit Author
3. **追踪闭环**：记录问题并在后续 CR 中检查修复状态
4. **报告存档**：CR 报告保存到 `task/codereview/{日期}/` 目录

## 相关文件

- [checklist.md](references/checklist.md) - 完整检查清单
