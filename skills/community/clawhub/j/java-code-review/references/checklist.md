# Code Review 完整检查清单

## Security (安全)

### SQL Injection
- [ ] 所有数据库查询使用参数化语句或 ORM 框架
- [ ] 禁止字符串拼接 SQL，特别是用户输入
- [ ] MyBatis 使用 `#{}` 而非 `${}`（除非必要且已转义）

### XSS (跨站脚本)
- [ ] 用户内容在渲染前已转义/净化
- [ ] 前端使用安全的渲染方式
- [ ] API 返回的富文本已过滤危险标签

### CSRF Protection
- [ ] 状态变更请求（POST/PUT/DELETE）需要有效 CSRF 令牌
- [ ] 敏感操作需要二次确认

### Authentication (认证)
- [ ] 每个受保护端点在处理前验证用户身份
- [ ] Token 验证逻辑完整
- [ ] 登录状态检查无遗漏

### Authorization (授权)
- [ ] 资源访问限定在请求用户权限范围内
- [ ] 无 IDOR（Insecure Direct Object Reference）漏洞
- [ ] 权限检查逻辑完整

### Input Validation (输入验证)
- [ ] 所有外部输入在服务端验证
- [ ] 验证类型、长度、格式和范围
- [ ] 使用验证框架而非手动验证

### Secrets Management (密钥管理)
- [ ] 源码中无 API 密钥、密码、令牌或凭证
- [ ] 敏感配置来自环境变量或配置中心
- [ ] 日志中不打印敏感信息

### Dependency Safety (依赖安全)
- [ ] 新依赖来自可信来源
- [ ] 依赖库积极维护
- [ ] 无已知 CVE 漏洞

### Sensitive Data (敏感数据)
- [ ] PII 不记录日志
- [ ] 令牌和秘密不包含在错误消息中
- [ ] API 响应不返回敏感字段

### Rate Limiting (速率限制)
- [ ] 公共端点有速率限制
- [ ] 认证端点有防暴力破解措施
- [ ] 分布式环境下使用分布式限流

### File Upload Safety (文件上传安全)
- [ ] 上传文件验证类型和大小
- [ ] 文件存储在 webroot 外
- [ ] 文件名安全处理，防止路径遍历

### HTTP Security Headers
- [ ] 设置 CSP (Content-Security-Policy)
- [ ] 设置 X-Content-Type-Options: nosniff
- [ ] 设置 HSTS (HTTP Strict Transport Security)

---

## Performance (性能)

### N+1 Queries
- [ ] 数据库访问模式已批量或联接
- [ ] 无循环中单独查询数据库
- [ ] 使用 JOIN 或批量查询替代

### Memory Leaks (内存泄漏)
- [ ] 事件监听器在卸载时移除
- [ ] 订阅在销毁时取消
- [ ] 定时器在不需要时清理

### Caching Strategy (缓存策略)
- [ ] 昂贵计算使用适当缓存
- [ ] API 响应合理缓存
- [ ] 缓存失效策略清晰

### Database Indexing (数据库索引)
- [ ] 查询在索引列上过滤/排序
- [ ] 新查询已用 EXPLAIN 检查执行计划
- [ ] 避免全表扫描

### Pagination (分页)
- [ ] 列表端点使用分页
- [ ] 查询使用 LIMIT
- [ ] 无无界 SELECT *

### Async Operations (异步操作)
- [ ] 长时间运行任务卸载到后台作业
- [ ] 使用消息队列处理异步任务
- [ ] 合理设置超时时间

### **严禁处理文件流**
- [ ] 不允许在系统中处理文件流
- [ ] 文件操作通过专门服务处理
- [ ] 避免大文件读写影响服务稳定性

---

## Correctness (正确性)

### Edge Cases (边界情况)
- [ ] 空数组处理
- [ ] 空字符串处理
- [ ] 零值处理
- [ ] 负数处理
- [ ] 最大值处理

### Null/Undefined Handling
- [ ] 可空值在访问前已检查
- [ ] 使用 Optional 或空对象模式
- [ ] 避免 NPE (NullPointerException)

### Race Conditions (竞态条件)
- [ ] 共享状态的并发访问使用锁
- [ ] 使用事务保证原子性
- [ ] 使用原子操作类

### Timezone Handling (时区处理)
- [ ] 日期以 UTC 存储
- [ ] 显示转换在表示层进行
- [ ] 明确时区设置

### Error Propagation (错误传播)
- [ ] 异步调用的错误已捕获
- [ ] 外部服务的错误已处理
- [ ] 错误信息有意义且安全

### State Consistency (状态一致性)
- [ ] 多步骤变更是事务性的
- [ ] 部分失败有回滚机制
- [ ] 系统处于有效状态

---

## Maintainability (可维护性)

### Naming Clarity (命名清晰)
- [ ] 变量有描述性名称
- [ ] 函数名表达意图
- [ ] 类名符合职责
- [ ] 常量名有意义

### Single Responsibility (单一职责)
- [ ] 每个函数做一件事
- [ ] 每个类有一个变更理由
- [ ] 模块边界清晰

### DRY (Don't Repeat Yourself)
- [ ] 重复逻辑提取到共享工具
- [ ] 复制粘贴代码已合并
- [ ] 使用继承或组合复用代码

### Cyclomatic Complexity (圈复杂度)
- [ ] 函数分支复杂度低于 10
- [ ] 深度嵌套链已重构
- [ ] 使用早返回减少嵌套

### Dead Code Removal (死代码移除)
- [ ] 注释掉的代码已删除
- [ ] 未使用的导入已移除
- [ ] 不可达分支已删除

### Magic Numbers & Strings
- [ ] 字面值提取到命名常量
- [ ] 魔数有意义解释
- [ ] 配置外部化

### **ORM Operation (ORM 操作规范)**
- [ ] ORM 代码只允许在 mapper 层操作
- [ ] MyBatis Plus 调用只能在 mapper 层
- [ ] 其他包下不允许引用 mybatis 相关类

### **Commented Code (注释代码)**
- [ ] 任何地方不允许将原有代码注释掉提交
- [ ] 只能删除，不能注释

### **SQL Business Logic (SQL 业务逻辑)**
- [ ] SQL 中不带业务逻辑
- [ ] 魔数、固定值由业务层传参
- [ ] 复杂逻辑在 Service 层处理

### **包命名规范**
- [ ] 包名以 cn.ctg.travel.{项目名} 为前缀
- [ ] 例如：travel-openapi → cn.ctg.travel.openapi

---

## Testing (测试)

### Test Coverage (测试覆盖)
- [ ] 新逻辑路径有对应测试
- [ ] 覆盖率符合项目标准

### Edge Case Tests (边界测试)
- [ ] 测试覆盖边界值
- [ ] 测试空输入
- [ ] 测试 null 情况
- [ ] 测试错误条件

### No Flaky Tests (测试稳定性)
- [ ] 测试是确定性的
- [ ] 无随机失败
- [ ] 无依赖执行顺序

### Meaningful Assertions (有意义的断言)
- [ ] 测试断言行为和结果
- [ ] 不测试实现细节
- [ ] 断言消息清晰

### Regression Tests (回归测试)
- [ ] Bug 修复包含重现原始 bug 的测试
- [ ] 问题关联测试用例
