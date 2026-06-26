---
name: git-commit-helper
description: Generate conventional commit messages from code changes or diff.
version: 1.0.0
author: Hazy
triggers:
  - commit message
  - git commit
  - 提交信息
  - 生成提交消息
  - write a commit
---

# Git Commit Helper

## 目标

根据用户提供的代码变更内容（git diff 输出或口头描述），智能分析改动范围和类型，生成符合 **Conventional Commits** 规范的提交消息候选方案。

## 触发条件

当用户请求生成 Git 提交消息时激活，常见触发语句包括：
- "commit message for this change"
- "帮我写一个 commit"
- "生成 Git 提交信息"
- "为这次改动写提交消息"

## Conventional Commits 规范参考

提交消息格式：
```
<type>(<scope>): <short description>

[optional body]

[optional footer(s)]
```

### 类型（type）定义

| 类型 | 说明 | 示例 |
|------|------|------|
| `feat` | 新功能 | `feat(auth): add OAuth2 login support` |
| `fix` | 修复 bug | `fix(api): handle null pointer in user endpoint` |
| `docs` | 文档变更 | `docs(readme): update installation instructions` |
| `style` | 代码格式（不影响功能） | `style(lint): fix indentation in utils.ts` |
| `refactor` | 重构（非新功能、非修复） | `refactor(database): simplify query builder` |
| `perf` | 性能优化 | `perf(render): reduce re-renders in list component` |
| `test` | 测试相关 | `test(auth): add unit tests for login flow` |
| `chore` | 构建过程或辅助工具变动 | `chore(deps): update react to v18.2.0` |
| `ci` | CI/CD 配置变更 | `ci(github): add automated testing workflow` |

### 破坏性变更标识

如果改动包含 **BREAKING CHANGE**，需在类型后添加 `!` 或在正文/脚注中明确标注：
```
feat(api)!: change authentication endpoint response format

BREAKING CHANGE: The /api/auth/login endpoint now returns a different JSON structure.
```

## 操作指南

### 步骤 1：接收输入

询问用户提供以下任一形式的输入：
- **git diff 输出**：用户粘贴 `git diff` 或 `git diff --staged` 的完整输出
- **口头描述**：用户用自然语言描述本次改动的内容

如果用户未提供具体内容，主动询问：
> "请提供 git diff 输出，或描述本次代码改动的内容（例如：添加了用户登录功能、修复了空指针异常等）。"

### 步骤 2：分析改动

基于用户输入，执行以下分析：

#### 2.1 识别改动文件与模块
- 提取被修改的文件路径
- 推断所属模块/范围（scope），如：`auth`, `ui`, `api`, `database`, `config` 等
- 如果涉及多个模块，选择最主要的一个或使用通用范围（如 `core`）

#### 2.2 判断改动类型
根据改动内容确定 type：
- **新增功能/接口/组件** → `feat`
- **修复错误/异常/bug** → `fix`
- **更新 README/注释/文档** → `docs`
- **调整代码格式/空格/缩进** → `style`
- **代码结构优化（无功能变化）** → `refactor`
- **提升性能/减少资源消耗** → `perf`
- **新增/修改测试用例** → `test`
- **依赖更新/配置文件调整** → `chore`
- **CI/CD 脚本变更** → `ci`

#### 2.3 检测破坏性变更
检查是否存在以下情况：
- API 接口签名变更（参数、返回值）
- 数据库 schema 重大调整
- 移除已公开的功能或配置项
- 行为逻辑发生不兼容改变

如果存在，标记为 **BREAKING CHANGE**。

### 步骤 3：生成提交消息候选

生成 **3 条**不同详细程度的推荐提交消息：

#### 候选 1：简洁版（单行）
格式：`<type>(<scope>): <short description>`
- 短描述不超过 50 字符
- 使用祈使句（如 "add" 而非 "added"）
- 首字母小写，末尾无句号

#### 候选 2：标准版（含正文）
格式：
```
<type>(<scope>): <short description>

<detailed body explaining what and why>
```
- 正文解释改动的背景和原因
- 每行不超过 72 字符
- 与短描述之间空一行

#### 候选 3：完整版（含脚注）
格式：
```
<type>(<scope>): <short description>

<detailed body>

BREAKING CHANGE: <description of breaking change>

Closes #123
```
- 包含破坏性变更说明（如适用）
- 包含关联的 issue/pr 编号（如适用）

### 步骤 4：呈现结果

以清晰的结构化格式输出：

```markdown
## 📝 推荐的提交消息

### 选项 1：简洁版
```
<commit message>
```

### 选项 2：标准版
```
<commit message with body>
```

### 选项 3：完整版
```
<commit message with body and footer>
```

## 🔍 分析说明
- **改动类型**：<type> - <解释为什么选择此类型>
- **影响范围**：<scope> - <解释如何确定此范围>
- **破坏性变更**：是/否 - <如有，说明原因>
```

### 步骤 5：交互优化

提供后续操作建议：
- "需要我将某条消息复制到剪贴板吗？"
- "是否需要调整某个选项的描述？"
- "是否要生成英文版本的提交消息？"

## 示例对话

### 示例 1：用户提供 git diff

**用户**：
```
commit message for this change

diff --git a/src/auth/login.ts b/src/auth/login.ts
index abc123..def456 100644
--- a/src/auth/login.ts
+++ b/src/auth/login.ts
@@ -10,6 +10,15 @@ export class AuthService {
+  async loginWithOAuth2(provider: string): Promise<User> {
+    // implementation
+  }
```

**助手**：
```markdown
## 📝 推荐的提交消息

### 选项 1：简洁版
```
feat(auth): add OAuth2 login support
```

### 选项 2：标准版
```
feat(auth): add OAuth2 login support

Implement OAuth2 authentication flow to allow users to login with third-party providers like Google and GitHub.
```

### 选项 3：完整版
```
feat(auth): add OAuth2 login support

Implement OAuth2 authentication flow to allow users to login with third-party providers like Google and GitHub.

- Add loginWithOAuth2 method to AuthService
- Support multiple provider configurations
- Handle token exchange and user profile retrieval

Closes #42
```

## 🔍 分析说明
- **改动类型**：feat - 新增了 OAuth2 登录功能
- **影响范围**：auth - 改动集中在认证模块
- **破坏性变更**：否 - 仅新增方法，未修改现有接口
```

### 示例 2：用户口头描述

**用户**：
```
帮我写一个 commit，我修复了一个 bug，当用户输入为空时，搜索功能会崩溃
```

**助手**：
```markdown
## 📝 推荐的提交消息

### 选项 1：简洁版
```
fix(search): handle empty input to prevent crash
```

### 选项 2：标准版
```
fix(search): handle empty input to prevent crash

Add input validation to search function to gracefully handle empty or null queries instead of throwing an exception.
```

### 选项 3：完整版
```
fix(search): handle empty input to prevent crash

Add input validation to search function to gracefully handle empty or null queries instead of throwing an exception.

- Check for empty/null input before processing
- Return empty results array for invalid queries
- Add unit tests for edge cases

Fixes #156
```

## 🔍 分析说明
- **改动类型**：fix - 修复了导致崩溃的 bug
- **影响范围**：search - 问题出现在搜索功能
- **破坏性变更**：否 - 仅增强健壮性，未改变接口行为
```

## 注意事项

1. **语言一致性**：如果代码库主要使用英文注释/文档，提交消息使用英文；否则可使用中文
2. **范围可选性**：如果无法明确范围，可省略 `(scope)` 部分
3. **避免冗余**：短描述不要重复类型信息（如不要写 "feat: add new feature"）
4. **时态规范**：使用祈使句现在时（"add" 而非 "added" 或 "adds"）
5. **特殊字符**：避免在短描述中使用句号、感叹号等标点

## 常见问题处理

### 问题 1：改动涉及多个模块
**解决方案**：
- 选择最主要的模块作为 scope
- 或使用通用范围如 `core`, `app`, `multiple`
- 在正文中详细说明各模块的改动

### 问题 2：无法确定改动类型
**解决方案**：
- 优先询问用户意图（"这是新功能还是修复？"）
- 根据代码上下文推断
- 默认使用 `chore` 作为保守选择

### 问题 3：用户提供的 diff 不完整
**解决方案**：
- 基于已有信息做出最佳推断
- 明确告知用户分析的局限性
- 建议提供更完整的 diff 以获得更准确的结果

## 扩展功能（可选）

如果环境支持，可实现以下增强：

1. **自动复制**：调用系统剪贴板 API 复制选中的提交消息
2. **Git 集成**：直接执行 `git commit -m "<message>"`
3. **模板保存**：允许用户保存常用的提交消息模板
4. **历史建议**：基于项目历史提交记录优化推荐风格
