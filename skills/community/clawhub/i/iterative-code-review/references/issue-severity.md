# Issue 严重级别定义

## 级别分类

| Level | Definition | Examples | User Action |
|-------|------------|----------|-------------|
| **P0** | Critical | Runtime errors, security vulnerabilities | 建议立即修复 |
| **P1** | High | Functional defects, missing error handling | 建议修复 |
| **P2** | Medium | Code quality, test coverage gaps | 建议修复 |
| **P3** | Low | Code style, documentation, minor improvements | 可选修复 |

## 各级别示例

### P0 - Critical

- 运行时错误（null pointer、未捕获异常）
- 安全漏洞（SQL 注入、XSS、命令注入）
- 数据丢失风险
- 认证/授权绕过

### P1 - High

- 功能缺陷（逻辑错误、边界未处理）
- 错误处理缺失
- 并发问题（竞态条件、死锁）
- 性能严重下降

### P2 - Medium

- 代码质量问题（重复代码、过长函数）
- 测试覆盖不足
- 注释缺失
- 命名不规范

### P3 - Low

- 代码风格问题
- 文档不完整
- 轻微性能优化
- 日志级别调整

## 用户决策

**所有修复都需要用户确认：**

- 用户决定是否修复某个问题
- 用户决定修复的优先级
- 用户可以跳过任何问题
- 用户可以要求更详细的解释

## 关键规则

- **建议，不强制** - 向用户建议，但最终决定权在用户
- **透明报告** - 清晰解释为什么某个问题是 P0/P1/P2/P3
- **用户控制** - 用户决定修复哪些问题