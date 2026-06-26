# Code Review Checklist

## 0. ⚠️ 新增代码审查（必须检查！）

> **历史教训**：PR #64 经过 7 轮 review 后，重新审查仍发现 22 个新问题。
> 原因：只关注"修复了什么"，忽略"新增了什么"。

### 新增代码识别
- [ ] 识别本次 PR 新增的代码范围（`git diff --stat`）
- [ ] 识别新增的文件（`git diff --name-only --diff-filter=A`）

### 新增代码安全性
- [ ] 加密算法使用正确（使用 HMAC 而非 Hash）
- [ ] 密钥管理安全（零填充、安全存储）
- [ ] 输入验证完整
- [ ] 权限检查到位
- [ ] 无注入漏洞

### 新增代码测试覆盖
- [ ] 新增函数有对应单元测试
- [ ] 边界条件测试覆盖
- [ ] 错误路径测试覆盖
- [ ] 测试资源正确清理

### 新增代码边界条件
- [ ] 空值/undefined 检查
- [ ] 极端情况处理
- [ ] 错误处理完整
- [ ] 异步操作正确（Promise/async-await）

### 新增代码资源清理
- [ ] 定时器正确清理
- [ ] 内存正确释放
- [ ] 连接正确关闭
- [ ] 事件监听器移除

---

## 1. Code Quality

### Logic Correctness
- [ ] Business logic correct
- [ ] Condition checks complete
- [ ] Loop termination correct
- [ ] Boundary values handled

### Error Handling
- [ ] All error paths handled
- [ ] Error messages clear
- [ ] Appropriate retry mechanisms
- [ ] Errors propagated/logged correctly

### Edge Cases
- [ ] Null/undefined checks
- [ ] Array bounds checks
- [ ] Number overflow checks
- [ ] String length limits

### Readability
- [ ] Variable names clear
- [ ] Functions not too long (<50 lines)
- [ ] No duplicate code
- [ ] Adequate comments

## 2. Concurrency & Race Conditions

### Race Conditions
- [ ] Shared resources lock-protected
- [ ] File operations atomic
- [ ] Database operations in transactions
- [ ] No TOCTOU issues

### Idempotency
- [ ] Repeated calls safe
- [ ] State changes idempotent
- [ ] External calls deduplicated
- [ ] Retries don't cause duplication

### Thread Safety
- [ ] No deadlock risk
- [ ] Lock granularity appropriate
- [ ] No resource leaks
- [ ] Async operations awaited correctly

## 3. Security

### Input Validation
- [ ] All external input validated
- [ ] Parameter types checked
- [ ] Parameter ranges validated
- [ ] No injection vulnerabilities (SQL/XSS/command)

### Permission Checks
- [ ] Permission verification present
- [ ] Permission checks complete
- [ ] No unauthorized access
- [ ] Sensitive operations require confirmation

### Data Handling
- [ ] Sensitive data encrypted
- [ ] Keys stored securely
- [ ] Logs don't leak sensitive info
- [ ] Config not tamperable

## 4. Test Coverage

### Testing Principles
- [ ] Tests verify actual behavior, not mock behavior
- [ ] Business boundaries covered
- [ ] Error paths tested
- [ ] Concurrent scenarios tested

### Boundary Testing
- [ ] Normal value boundaries
- [ ] Extreme values (max/min)
- [ ] Null/empty tests
- [ ] Type error tests

### Business Logic Testing
- [ ] Main business flows
- [ ] Exception business flows
- [ ] Business rule validation
- [ ] Business boundary conditions

### Avoid Meaningless Mocks
- [ ] Mock return values match real behavior
- [ ] Tests verify function calls and parameters
- [ ] Don't just test that mock was called
- [ ] Integration tests use real dependencies

## 5. Performance

### Performance Issues
- [ ] No obvious bottlenecks
- [ ] No unnecessary operations in loops
- [ ] No N+1 query issues
- [ ] Large data handling optimized

### Resource Management
- [ ] Files/connections closed properly
- [ ] Memory released timely
- [ ] Timers cleaned up
- [ ] Event listeners removed

## 6. Code Style

### Formatting
- [ ] Consistent indentation
- [ ] Consistent spacing/line breaks
- [ ] Naming follows conventions
- [ ] Comments clear

### Organization
- [ ] Functions have single responsibility
- [ ] Modules well-organized
- [ ] Dependencies clear
- [ ] No dead code

## 7. Documentation

### README/API Docs
- [ ] README updated for new features
- [ ] API docs synchronized
- [ ] Config items documented
- [ ] Environment variables explained

### Code Comments
- [ ] New functions have comments
- [ ] Complex logic explained
- [ ] TODOs addressed timely
- [ ] Outdated comments removed

### Changelog
- [ ] CHANGELOG updated
- [ ] Breaking changes marked
- [ ] Version numbers correct