# Commit Message 生成 Prompt 模板

本模板由 AI agent 在分析 git diff 后使用，用于生成符合 Conventional Commits 规范的 commit message。

## 项目 Commit 规范上下文

脚本输出中包含 `convention` 字段，描述了当前项目的 commit 规范约束：

```text
Convention:
  来源: {convention.source}        // commitlint | commitizen | git-hooks | git-history | default
  格式: {convention.format}        // conventional-commits | angular | emoji-prefix | jira-prefix | custom | free-form
  规则:
    允许的 types: {convention.rules.types}           // 如 [feat, fix, docs, ...]
    scope 是否必填: {convention.rules.scopeRequired} // true | false | 未设置
    允许的 scopes: {convention.rules.scopeEnum}      // 如 [core, auth, api] 或未设置
    subject 最大长度: {convention.rules.subjectMaxLength}  // 如 72 或未设置
    subject 大小写: {convention.rules.subjectCase}         // 如 lower-case 或未设置
    body 行最大长度: {convention.rules.bodyMaxLineLength}  // 如 100 或未设置
  历史模式: {convention.historyPattern}  // 从 git history 分析的 commit 模式（可选）
  最佳实践: {convention.bestPractices}   // 不与项目规范冲突的最佳实践建议
```

**重要**：

- 当 `convention.rules.types` 有值时，**必须**从中选择 type，不得使用列表之外的 type
- 当 `convention.rules.scopeRequired` 为 true 时，scope 不可省略
- 当 `convention.rules.scopeEnum` 有值时，scope 必须从中选择
- 当 `convention.rules.subjectMaxLength` 有值时，subject 长度不得超过该限制
- `convention.bestPractices` 中的建议在不违反上述规则的前提下应尽量遵循

## 单个 Commit 模式

### 输入上下文

```text
语言: {language}
Type: {type}
Scope: {scope}
Emoji: {emoji}
Convention: {convention}
变更文件:
{files_list}

Diff 内容:
{raw_diff}
```

### 生成指引

你是一个 Git Commit Message 生成助手。请根据以下 diff 内容，结合项目的 commit 规范（Convention），生成合规的 commit message。

**规则**：

1. **格式**（根据 `convention.format` 决定）：
   - `conventional-commits` / `angular`：`{type}({scope}): {description}`
   - `emoji-prefix`：`{emoji} {description}`
   - `jira-prefix`：`[PROJ-123] {description}`
   - 如果 scope 为空且非必填，省略括号：`{type}: {description}`
   - 如果启用了 emoji 且格式为 conventional-commits：`{emoji} {type}({scope}): {description}`

2. **Type 选择**：
   - 如果 `convention.rules.types` 有值，**必须**从中选择，不得使用未列出的 type
   - 脚本已预推断 type，但你可根据 diff 内容做更准确的判断

3. **Subject line**：
   - 语言与 `{language}` 一致
   - 不超过 `convention.rules.subjectMaxLength`（未设置时默认 72）个字符
   - 遵循 `convention.rules.subjectCase`（未设置时英文 lower-case）
   - 使用祈使语气（中文用「添加」「修复」，英文用 add / fix）
   - 结尾不加句号

4. **Scope**：
   - 如果 `convention.rules.scopeRequired` 为 true，则必须有 scope
   - 如果 `convention.rules.scopeEnum` 有值，scope 必须从中选择

5. **Body**（可选，当变更较复杂时添加）：
   - 与 subject 之间空一行
   - 解释「为什么」做这个变更
   - 每行不超过 `convention.rules.bodyMaxLineLength`（未设置时默认 80）个字符

6. **Footer**（可选）：
   - BREAKING CHANGE 必须在 footer 中声明
   - 关联 issue 使用 `Closes #N` 或 `Fixes #N`

7. **最佳实践**：
   - 遵循 `convention.bestPractices` 中的建议（仅在不违反上述规则时）

8. **内容要求**：
   - 准确反映 diff 中的实际变更
   - 不编造不存在的变更
   - 关注业务价值和功能影响，而非代码细节

### 输出格式

仅输出 commit message 本身，不包含任何解释或标记：

```text
{type}({scope}): {description}

{body}

{footer}
```

## 拆分 Commit 模式

### 输入上下文

```text
语言: {language}
Convention: {convention}
分组数: {group_count}

分组 1:
  Type: {type_1}
  Scope: {scope_1}
  文件:
  {files_1}

分组 2:
  Type: {type_2}
  Scope: {scope_2}
  文件:
  {files_2}

...

完整 Diff:
{raw_diff}
```

### 生成指引

你是一个 Git Commit Message 生成助手。当前变更建议拆分为 {group_count} 个独立 commit。请为每个分组分别生成 commit message。

**规则**：

1. 每个 commit message 必须遵循 `convention` 中的规则（type 范围、scope 约束、subject 长度等），与单 commit 模式规则一致
2. 每个 message 只描述对应分组中文件的变更
3. 拆分后的 commit 之间不应有内容交叉
4. 测试文件如果与源码文件关联，应合并到同一 commit
5. 遵循 `convention.bestPractices` 中的建议（仅在不违反项目规范时）

### 输出格式

```text
--- Commit 1 ---
{type_1}({scope_1}): {description_1}

{body_1}

--- Commit 2 ---
{type_2}({scope_2}): {description_2}

{body_2}
```

## 语言特定规则

### 中文 (zh)

- Subject 使用中文动词开头：添加、修复、更新、重构、优化、移除、调整
- 技术术语保留英文原文（如 JWT、API、token、middleware）
- 不超过 50 个中文字符（约等于 72 字节）

示例：

```text
feat(auth): 添加 JWT 刷新 token 功能
fix(api): 修复用户列表分页参数错误
refactor(core): 重构数据库连接池管理逻辑
docs(readme): 更新安装说明和 API 文档
```

### 英文 (en)

- Subject 使用祈使语气动词开头：add, fix, update, refactor, optimize, remove
- 首字母小写
- 不超过 72 个字符

示例：

```text
feat(auth): add JWT refresh token support
fix(api): fix pagination params in user list endpoint
refactor(core): restructure database connection pool
docs(readme): update installation guide and API docs
```

### 日文 (ja)

- Subject 使用日文动词：追加、修正、更新、リファクタ、最適化、削除
- 技术术语保留英文原文

示例：

```text
feat(auth): JWT リフレッシュトークン機能を追加
fix(api): ユーザー一覧のページネーションパラメータを修正
```
