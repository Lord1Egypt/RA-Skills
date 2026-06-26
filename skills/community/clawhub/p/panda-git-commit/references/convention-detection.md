# 项目 Commit 规范检测策略

## 核心原则

**项目规范是硬约束，最佳实践是软增强。**

- 如果项目配置了 commit 规范（commitlint / commitizen 等），严格遵守
- 在不违反项目规范的前提下，融合我们的最佳实践
- 如果没有任何规范配置，使用 Conventional Commits 最佳实践作为兜底

## 检测优先级

按以下顺序检测，命中即采用（后续检测跳过）：

| 优先级 | Source        | 检测方式                             |
| ------ | ------------- | ------------------------------------ |
| 1      | `commitlint`  | 配置文件或 package.json 字段         |
| 2      | `commitizen`  | 配置文件或 package.json 字段         |
| 3      | `git-hooks`   | commit-msg hook 中引用了规范检查工具 |
| 4      | `git-history` | 分析最近 50 条 commit 的模式         |
| 5      | `default`     | 使用 Conventional Commits 最佳实践   |

## 1. commitlint 检测

### 配置文件（按顺序扫描）

- `commitlint.config.js` / `.cjs` / `.mjs` / `.ts`
- `.commitlintrc` / `.commitlintrc.json` / `.commitlintrc.yml` / `.commitlintrc.yaml` / `.commitlintrc.js` / `.commitlintrc.cjs` / `.commitlintrc.ts`
- `package.json` → `commitlint` 字段

### 提取的规则

| commitlint 规则             | 映射到                                |
| --------------------------- | ------------------------------------- |
| `type-enum`                 | `rules.types` — 允许的 type 列表      |
| `scope-enum`                | `rules.scopeEnum` — 允许的 scope 列表 |
| `scope-empty: [2, 'never']` | `rules.scopeRequired = true`          |
| `header-max-length`         | `rules.subjectMaxLength`              |
| `subject-case`              | `rules.subjectCase`                   |
| `body-max-line-length`      | `rules.bodyMaxLineLength`             |

### 示例

项目 `.commitlintrc.json`：

```json
{
  "extends": ["@commitlint/config-conventional"],
  "rules": {
    "type-enum": [2, "always", ["feat", "fix", "docs", "chore"]],
    "scope-empty": [2, "never"],
    "header-max-length": [2, "always", 100]
  }
}
```

检测结果：

```json
{
  "source": "commitlint",
  "format": "conventional-commits",
  "rules": {
    "types": ["feat", "fix", "docs", "chore"],
    "scopeRequired": true,
    "subjectMaxLength": 100
  },
  "bestPractices": [
    "body 每行建议不超过 80 字符",
    "subject 使用祈使语气",
    "body 解释「为什么」变更，而非「做了什么」",
    "不相关的变更应拆分为独立 commit",
    "BREAKING CHANGE 应在 footer 中声明或在 type 后加 !",
    "关联 issue 使用 Closes #N 或 Fixes #N"
  ]
}
```

注意 `bestPractices` 中只包含项目未配置的部分（body 换行、祈使语气等），不包含已被项目配置覆盖的部分。

## 2. commitizen 检测

### 配置文件

- `.czrc`
- `.cz-config.js` / `.cz-config.cjs`
- `package.json` → `config.commitizen` 字段

### 行为

检测到 commitizen 配置说明项目使用交互式 commit 工具，通常遵循 Conventional Commits 格式。检测结果的 `format` 设为 `conventional-commits`。

## 3. git hooks 检测

### 检测路径

- `.git/hooks/commit-msg`
- `.husky/commit-msg`
- `.githooks/commit-msg`

### 行为

检查 hook 脚本内容是否引用了 `commitlint` 或类似的规范检查工具。如果有，说明项目通过 hook 强制执行规范。

## 4. git history 模式分析

当没有找到任何配置文件时，分析最近 50 条 commit message 来推断项目实际使用的格式。

### 识别的模式

| 模式                   | 正则特征                                   | 示例                       |
| ---------------------- | ------------------------------------------ | -------------------------- |
| `conventional-commits` | `^(feat\|fix\|docs\|...)(\(scope\))?!?:\s` | `feat(auth): add login`    |
| `angular`              | `^(feat\|fix\|...)(\(scope\)):\s`          | `fix(core): resolve issue` |
| `emoji-prefix`         | `^(:emoji:\|emoji)\s`                      | `✨ add new feature`       |
| `jira-prefix`          | `^\[?[A-Z]+-\d+\]?\s*:?\s`                 | `[PROJ-123] fix bug`       |
| `free-form`            | 无固定模式                                 | `Fixed the login bug`      |

### 置信度

- 计算每种模式在 50 条 commit 中的占比
- 占比 >= 30% 的最高模式被采纳
- 低于 30% 说明项目没有统一规范，回退到 default

### Jira 前缀模式下的最佳实践融合

即使项目使用 Jira 前缀，以下最佳实践仍然适用（不冲突）：

- Subject 使用祈使语气
- Body 解释变更原因
- Body 每行不超过 80 字符
- 不相关的变更拆分为独立 commit

## 5. 合并策略

### 不冲突的最佳实践（始终应用）

无论检测到什么规范，以下最佳实践在不与项目规则冲突时自动生效：

| 最佳实践                | 何时不应用                               |
| ----------------------- | ---------------------------------------- |
| Subject 使用祈使语气    | 项目 `subject-case` 规则指定了其他格式   |
| Body 每行不超过 80 字符 | 项目 `body-max-line-length` 指定了其他值 |
| Subject 不超过 72 字符  | 项目 `header-max-length` 指定了其他值    |
| 标准 10 个 type         | 项目 `type-enum` 指定了自定义列表        |
| 不相关变更应拆分        | 从不冲突，始终适用                       |
| BREAKING CHANGE 声明    | 从不冲突，始终适用                       |
| 关联 issue 格式         | 从不冲突，始终适用                       |

### 优先级总览

```text
CLI 参数 --type/--scope/--lang
    ↓ 覆盖
EXTEND.md 自定义配置
    ↓ 覆盖
项目 commit 规范（commitlint / commitizen / git history）
    ↓ 增强（不冲突时）
我们的最佳实践
    ↓ 兜底
Conventional Commits 默认值
```
