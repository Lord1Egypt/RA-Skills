---
name: git-commit
description: Generate git commit messages following Conventional Commits specification. Use this skill when users ask to: (1) Create a git commit with a meaningful message, (2) Generate commit messages from git changes, (3) Help write commit messages following best practices, (4) Format or improve existing commit messages. The skill supports both automatic analysis (by examining git diff) and interactive guided generation. Automatically detects project language style (Chinese/English) and adapts commit messages accordingly.
---

# Git Commit Message Generator

Generate conventional commit messages with automatic language style detection.

## Commit Format

```
<type>[optional scope]: <subject>

<body>

[optional footer]
```

**Types**: `feat` `fix` `docs` `style` `refactor` `perf` `test` `build` `ci` `chore` `revert`

**Rules**:
- Type: lowercase English, always
- Subject: <72 chars, imperative mood, no period
- Body: detailed explanation of changed files, core changes, problems solved, or behavior changes
- Footer: `Refs #123`, `BREAKING CHANGE: ...`, etc. Omit if not applicable.

## Output Behavior

**Default (full template)**: Always provide a complete commit command with type, scope, subject, body, and footer. This is the standard behavior unless the user requests otherwise.

```bash
git commit -m "$(cat <<'EOF'
<type>(<scope>): <subject>

<body>

<footer>
EOF
)"
```

**Short mode**: Only when the user explicitly says "简短一点", "只给 commit message", "只给命令", or similar brevity requests — output just the one-line subject:

```bash
git commit -m "<type>(<scope>): <subject>"
```

## Language Detection

Detect project language from multiple signals (in priority order):

1. **Recent commits** (primary): `git log -20 --oneline`
   - Contains Chinese characters → Chinese
2. **README.md**: Check if README is written in Chinese
3. **Default**: Chinese

| Style | Format Example |
|-------|---------------|
| English | `feat(api): add user authentication endpoint` |
| Chinese | `feat(用户管理): 添加登录功能` |

**Language Rules**:
- **Type**: Always English (`feat`, `fix`, `refactor`, etc.)
- **Scope**: Follow project style (English or Chinese)
- **Subject/Body**: Match detected project language

## Workflow

### 1. Parallel Analysis (single response)

Run these in parallel to gather context:

```bash
git status
git diff --staged          # staged changes (primary)
git diff                   # unstaged changes (fallback if nothing staged)
git log -20 --oneline      # recent commits for language + style detection
```

If nothing is staged and nothing is unstaged, check:
```bash
git diff HEAD~1            # show last commit changes
```

### 2. Project Convention Detection

Before generating, check if the project has commit conventions:

1. Look for `.github/COMMIT_CONVENTION.md`, `CONTRIBUTING.md`, or similar
2. Check recent commit patterns for project-specific types or scopes
3. If project uses a convention (e.g., Angular, custom types), follow it **first**

### 3. Smart Type Inference

**Priority: project convention > keyword matching > file pattern matching**

| Pattern | Type |
|---------|------|
| `*.test.*`, `*.spec.*`, `__tests__/`, `*Test.java` | `test` |
| `package.json`, `*.lock`, `Dockerfile`, `Makefile`, `pom.xml`, `build.gradle` | `build` |
| `.github/`, `.gitlab-ci.yml`, `Jenkinsfile`, `*.yml` (CI config) | `ci` |
| `*.md`, `docs/`, `README*`, `CHANGELOG*` | `docs` |
| Only whitespace/formatting changes | `style` |
| Keywords: fix/bug/resolve/repair/patch | `fix` |
| Keywords: add/implement/create/introduce/support | `feat` |
| Keywords: refactor/extract/reorganize/restructure | `refactor` |
| Keywords: optimize/cache/performance/speed | `perf` |
| Keywords: update/upgrade/bump (dependencies) | `chore` |
| Keywords: revert/undo | `revert` |
| Mixed or unclear | `chore` |

### 4. Scope Inference

Extract scope from changed file paths:

**Strategy**: Use the most meaningful directory name under `src/` or project root.

| Path Pattern | Scope |
|-------------|-------|
| `src/api/user/*`, `server/api/*` | `api` or `user` |
| `src/components/Button/*` | `Button` or `components` |
| `src/views/目标管理/*` | `目标管理` |
| `src/utils/*`, `src/lib/*` | `utils` |
| Root config files only | omit scope |
| Mixed across many modules | omit scope or use broad scope |

**Rules**:
- Prefer the module name that best represents the change's impact
- If changes span multiple unrelated modules, omit scope
- If a single file is changed, use the parent directory name
- For monorepos: use package name as scope

### 5. Body Construction

The body must answer **what changed and why**, not how. Structure:

- **Multiple files**: Use numbered list (`1. 2. 3.`), each item specifies the file/module and the change
- **Single file**: One concise paragraph explaining the change
- **Bug fix**: Describe the problem, root cause, and solution
- **New feature**: Describe what it does and the use case

### 6. Breaking Changes

When changes break backward compatibility:

- Add `!` after type/scope: `feat(api)!: change response format`
- Add footer: `BREAKING CHANGE: <description of what breaks and migration path>`

### 7. Present & Confirm

When changes include multiple distinct categories (for example: docs + fix + feat), the skill will split them into multiple commits by responsibility and present a batch of commit commands for user approval.

Behavior:
- Group changed files by inferred type (project convention > keyword matching > path patterns).
- For each group generate a complete commit (type, optional scope, subject, body) and the corresponding `git add <files>` + `git commit` command using HEREDOC.
- If a file matches multiple groups, assign it to the highest-priority inferred type; if still ambiguous, place it in a `mixed` group and flag for interactive review.
- Small formatting/whitespace-only changes across many files may be squashed into a single `style` commit to avoid noise.
- Present all proposed commit commands together with a short summary of which files belong to each commit and the rationale for grouping.

Confirmation step:
- Show the user the list of proposed commands and ask which commits to execute (all, subset, or none).
- If anything is unclear (ambiguous grouping, unclear scope, files assigned to multiple types, presence of sensitive files like .env, or any other ambiguity), immediately pause and ask the user clarifying question(s); do NOT proceed until clarified.
- Do NOT run any `git` commands until explicit user approval is given.

Example (two commits):

```bash
# Commit 1 - bug fix
git add src/payment/*.ts
git commit -m "$(cat <<'EOF'\nfix(payment): 修复订单金额计算错误\n\n1. 调整 OrderService.calculateTotal 中折扣优先级，先应用商品折扣再叠加优惠券。\n2. 新增 utils/discount.ts 及单元测试。\n\nFixes #456\nEOF\n)"

# Commit 2 - docs
git add docs/CHANGELOG.md README.md
git commit -m "$(cat <<'EOF'\ndocs: 更新变更日志和 README\n\n1. 增加 2026-06-08 发布条目。\nEOF\n)"
```

Always await user approval before executing any of the above commands.

## Examples

### Full Template — Chinese (default)

```bash
git commit -m "$(cat <<'EOF'
feat(用户管理): 添加登录功能

1. AuthService 实现基于JWT的用户认证，支持登录和登出。
2. TokenManager 添加令牌刷新机制和会话管理。
3. routes/auth.ts 更新API路由增加认证中间件。

关联 #123
EOF
)"
```

### Full Template — English

```bash
git commit -m "$(cat <<'EOF'
feat(api): add user authentication endpoint

1. Implement JWT-based authentication in AuthService for login/logout.
2. Add token refresh mechanism and session management in TokenManager.
3. Update routes/auth.ts with authentication middleware.

Closes #123
EOF
)"
```

### Bug Fix — Chinese

```bash
git commit -m "$(cat <<'EOF'
fix(支付模块): 修复订单金额计算错误

问题：当商品包含折扣时，总价计算未考虑优惠券叠加，导致金额偏高。
修复：OrderService.calculateTotal() 中调整折扣优先级，先应用商品折扣再叠加优惠券。
新增：utils/discount.ts 添加折扣计算工具函数及对应单元测试。

Fixes #456
EOF
)"
```

### Breaking Change

```bash
git commit -m "$(cat <<'EOF'
feat(api)!: 更改用户接口响应格式

将用户列表接口的响应结构从数组改为分页对象，包含 data、total、page 字段。
前端分页组件需同步更新以适配新格式。

BREAKING CHANGE: GET /api/users 响应格式从 User[] 变为 { data: User[], total: number, page: number }，所有消费该接口的客户端需更新解析逻辑。
EOF
)"
```

### Revert

```bash
git commit -m "$(cat <<'EOF'
revert: 回退用户头像上传功能

回退 commit abc1234 中引入的头像上传功能，原因是文件存储服务迁移中，
待迁移完成后重新引入。

Refs #789
EOF
)"
```

### Short Mode (only when user explicitly requests)

```bash
git commit -m "feat(api): add user authentication endpoint"
```

## Git Safety

- NEVER use `--no-verify` unless explicitly requested
- NEVER amend commits unless explicitly requested — create NEW commits
- NEVER force push without explicit request
- ALWAYS use HEREDOC for commit messages to preserve formatting
- Prefer `git add <specific-files>` over `git add .` — avoid accidentally staging sensitive files
- Warn user if staged files include `.env`, credentials, or large binaries
