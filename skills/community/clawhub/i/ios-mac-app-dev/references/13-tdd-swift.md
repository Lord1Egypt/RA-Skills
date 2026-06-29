# Swift TDD 工作流

> 基于 matt pocock `tdd` 改写，适配 Swift/XCTest 测试驱动开发。

## 核心理念

**核心原则**：测试应通过公共接口验证行为，而非实现细节。代码可以完全重写；测试不应随之失效。

## 什么是好测试

**好测试**是集成风格的：通过公共 API 演练真实代码路径。它们描述系统**做什么**，而非**怎么做**。好测试在重构后仍然通过——因为它们不关心内部结构。

**坏测试**与实现耦合：mock 内部协作者、测试私有方法、或通过外部手段验证（如直接查数据库而非用接口）。警告信号：重构后测试失败但行为没变。

## 反模式：水平切片

**禁止先写完全部测试，再写完全部实现。** 这是「水平切片」——把 RED 当「写所有测试」，GREEN 当「写所有代码」。

这会产生**烂测试**：
- 批量写的测试验证的是「想象中的行为」，不是真实行为
- 你最终测试的是「形状」（数据结构、函数签名），不是用户可感知的行为
- 测试对真实变化不敏感——行为坏了还通过了，行为没问题却失败了

**正确做法**：通过 tracer bullet 垂直切片。一个测试 → 一个实现 → 重复。

## 工作流

### 1. 规划

探索代码库时，先读 `CONTEXT.md`（如有），让测试名和接口词汇与项目领域语言一致，并尊重相关区域的 ADR。

写代码前确认：
- [ ] 与用户确认需要哪些接口变更
- [ ] 与用户确认要测试哪些行为（优先级）
- [ ] 寻找深模块机会（小接口，深实现）—— 如有必要运行 `/codebase-design`
- [ ] 列出要测试的行为（不是实现步骤）
- [ ] 获得用户对计划的批准

问：「公共接口应该长什么样？哪些行为最重要需要测试？」

**你无法测试所有东西。** 与用户确认哪些行为最重要。把测试精力集中在关键路径和复杂逻辑上。

### 2. Tracer Bullet

写一个测试确认系统的一件事：

```
RED:   写第一个行为的测试 → 测试失败
GREEN: 写最少代码让它通过 → 测试通过
```

这是你的 tracer bullet——证明路径端到端可行。

### 3. 增量循环

对每个剩余行为：

```
RED:   写下一个测试 → 失败
GREEN: 最少代码让它通过 → 通过
```

规则：
- 一次一个测试
- 仅写足够让当前测试通过的代码
- 不要预判未来测试
- 保持测试聚焦在可观察行为上

### 4. 重构

所有测试通过后，寻找重构候选：
- [ ] 提取重复
- [ ] 加深模块（把复杂度移到简单接口后面）
- [ ] 在自然的地方应用 SOLID 原则
- [ ] 思考新代码揭示了现有代码的什么
- [ ] 每次重构后运行测试

**RED 状态永远不要重构。先到 GREEN。**

## Swift/XCTest 实践要点

```swift
// ✅ 好测试：通过公共接口验证行为
func test_userCanLoginWithValidCredentials() async throws {
    let authService = AuthService()
    let result = try await authService.login(
        username: "test@example.com",
        password: "validPassword"
    )
    XCTAssertEqual(result.status, .loggedIn)
    XCTAssertNotNil(result.user)
}

// ❌ 坏测试：测试实现细节
func test_authServiceCallsKeychain() {
    // 不应该测试内部是否调用了 Keychain
    // 应该测试「登录后 token 可用」这个行为
}
```

### 测试命名规范

```
test_[行为描述]_[预期结果]()

例：
test_loginWithValidCredentials_returnsLoggedInUser()
test_loginWithInvalidCredentials_throwsAuthenticationError()
test_notesListLoadsFromSwiftData_whenDatabaseHasRecords()
```

### 每个循环的核对清单

```
[ ] 测试描述行为，不是实现
[ ] 测试仅使用公共接口
[ ] 测试在内部重构后仍然通过
[ ] 代码对此测试是最小的
[ ] 没有添加投机性功能
```
