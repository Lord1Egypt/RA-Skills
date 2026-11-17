---
name: git-commit
description: Use when the user explicitly asks to prepare, review, or create a Git commit, including "提交", "提交代码", "帮我提交", "commit", "git commit", "确认提交", or requests a commit message.
---

# Git Commit

基于仓库规则和全部未提交改动生成 Conventional Commit 计划。核心原则是：**先按业务意图形成可独立审查、可独立回滚的原子变更，再用该组的主要意图确定 type。**

## Hard Gate

Skill 首次被调用时只执行准备阶段：读取、分析、分组并展示提交消息。完成展示后必须停止，等待用户确认。

- 准备阶段不得执行 `git add`、`git commit`、`git reset`、`git restore` 或其他写操作。
- 只有当前对话中已经展示过完整提交计划，且用户随后明确回复“确认提交”“按方案提交”等确认表达，才能进入执行阶段。
- “直接提交”出现在首次调用中时仍先展示计划；它不能跳过确认门禁。
- 如果没有可核对的当前计划，“确认提交”只触发重新准备，不直接提交。

## Workflow

### 1. Validate Repository State

先确认仓库根目录、当前分支和 Git 操作状态。检查是否存在未完成的 merge、rebase、cherry-pick、revert 或冲突；存在时停止并说明，不能生成可执行提交计划。

收集全部非忽略改动，而不是只看暂存区：

```bash
git rev-parse --show-toplevel
git status --short --branch
git status --porcelain=v1 -z
git diff --cached --name-status
git diff --name-status
git ls-files --others --exclude-standard
```

随后读取：

- staged 文件的完整文本 diff；
- unstaged 文件的完整文本 diff；
- untracked 文本文件的内容；
- 删除、重命名、类型变化、子模块和冲突状态；
- 二进制、大文件和敏感文件的路径与元数据，不在输出中暴露其内容。

如果 staged、unstaged、untracked 都为空，报告“没有可提交的改动”并停止。不得使用 `git diff HEAD~1` 代替当前改动。

### 2. Read Repository Rules

读取与改动文件适用的仓库规则，优先级如下：

1. 用户本次明确要求；
2. 适用的 `AGENTS.md`、`CLAUDE.md`；
3. `.github/COMMIT_CONVENTION.md`、`CONTRIBUTING.md`、README 中的提交约定；
4. `.commitlintrc*`、`commitlint.config.*`、`package.json` 中的 commitlint 配置；
5. `git config --get commit.template` 指向的模板和相关 commit hook；
6. 最近 20 条非 merge 提交：`git log --no-merges -20 --pretty=format:%s`；
7. 本 Skill 的默认 Conventional Commits 规则。

报告实际采用了哪些规则来源。仓库规则不能覆盖确认门禁和敏感文件保护。

### 3. Account for Every Changed Path

建立完整改动清单。按去重后的仓库相对路径计数：同一路径同时包含 staged 和 unstaged 内容时只计一次；rename 作为一个改动条目记录旧、新路径。每个改动条目必须且只能出现在以下一个位置：

- 某个原子提交组；
- 明确排除清单；
- 待用户决定清单。

完成分组前核对：

```text
检测到的改动路径数 = 已归组路径数 + 排除路径数 + 待决定路径数
```

如果等式不成立、路径重复归组、untracked 文件尚未检查或存在无法读取的内容，不得声称计划完成。

### 4. Group by Business Intent

先判断每项改动解决的业务问题或交付目标，再形成原子组：

- 同一功能的实现、类型定义、测试、mock、文档、迁移、配置和国际化资源放在同一组。
- 缺陷修复与证明该缺陷的回归测试放在同一组。
- 无关功能、独立重构、依赖升级、纯格式化或工具链调整拆成不同组。
- 同为 `feat` 或同为 `fix` 不代表属于同一组；业务意图不同仍要拆分。
- 文件类型只是证据，不能主导分组。不得因为文件是 `*.spec.*` 或 `*.md` 就把它从所属功能组拆走。
- 一个文件包含多个无法安全分离的业务意图时，列入“待用户决定”；不得自行使用交互式 hunk staging 猜测边界。

每个原子组应满足：有一个清晰意图，可以独立说明、独立审查，并能安全地独立回滚。

### 5. Choose Type From the Primary Intent

先形成原子组，再选择 type。项目约定优先；没有约定时使用：

| Primary intent | Type |
|---|---|
| 增加或扩展用户可用能力 | `feat` |
| 修复错误行为 | `fix` |
| 只调整内部结构且不改变外部行为 | `refactor` |
| 主要改善性能 | `perf` |
| 只新增或修改测试 | `test` |
| 只修改文档 | `docs` |
| 只修改格式且不改变语义 | `style` |
| 构建系统、构建依赖或打包 | `build` |
| CI/CD 配置 | `ci` |
| 其他维护工作 | `chore` |
| 回退既有提交 | `revert` |

不要把含义不明确的组自动降级为 `chore`；说明歧义并等待用户决定。

Scope 遵循项目历史和 commitlint 规则；否则选择最能表示业务模块的简短名称。跨多个无共同模块的改动省略 scope。

### 6. Construct the Message

格式：

```text
<type>[optional scope][optional !]: <subject>

[optional body]

[optional footer]
```

默认规则：

- type 始终使用小写英文；
- 中文 subject 使用简洁动宾结构，英文 subject 使用 imperative mood；
- subject 不加句号，默认不超过 72 个字符；
- body 说明这组改动做了什么、为什么需要，避免机械复述文件清单；
- 简单改动允许省略 body；
- footer 使用机器可读格式，如 `Refs #123`、`Fixes #456`；
- breaking change 使用 `!` 和 `BREAKING CHANGE: ...`，并在计划中醒目标记风险。

消息语言优先遵循仓库规则，其次参考最近非 merge 提交；无法判断时默认中文。

### 7. Present the Plan and Stop

按以下结构展示，不输出依赖特定 shell 的 Bash HEREDOC：

```text
提交计划

仓库：<name>
分支：<branch>
规则来源：<files/config/history>

提交组 1：<业务意图>
文件：
- <status> <path>

Commit message:
<完整消息>

分组原因：<为什么这些文件构成一个原子变更>

风险或待决定项：<无，或具体说明>

覆盖核对：
- 检测到：N
- 已归组：N
- 排除：N
- 待决定：N

回复“确认提交”后执行；也可以要求调整分组或消息。
```

存在多个组时逐组展示，并说明建议提交顺序。展示完成后停止，不执行任何 Git 写操作。

## Execute After Confirmation

收到有效确认后：

1. 重新执行仓库状态和全部改动检查。
2. 将当前路径、状态和 diff 与已确认计划逐项比较。
3. 只要出现新增、删除、内容变化、暂存状态变化或规则变化，旧确认立即失效；重新生成计划并再次等待确认。
4. 记录执行前的 staged 路径和 staged diff 快照，并标明它们属于哪个计划组。
5. 如果当前 index 的全部内容只属于一个计划组，优先提交该组；按组使用 `git add -A -- <exact-paths>` 精确暂存，不使用 `git add .`。rename 必须同时包含旧、新路径。
6. 已暂存与未暂存内容共存于同一文件时，确保计划包含整份文件；否则停止并请用户决定，不能意外扩大提交范围。
7. 每组提交前重新检查当前组的 staged diff 和整个 index：
   - index 不含其他组内容时，才可使用普通 `git commit`；
   - index 同时包含其他组内容时，禁止普通 `git commit`，使用 `git commit --only -- <current-group-exact-paths>` 隔离当前组；
   - 如果精确 pathspec 不能安全表示当前组，停止并请用户决定，不得通过 reset、restore 或交互式 staging 猜测处理。
8. 使用适合当前 shell 的安全多行输入提交消息；PowerShell 不得生成 Bash HEREDOC。需要跨 shell 时优先使用 `git commit -F -` 配合当前 shell 的标准输入方式。
9. 每次提交后验证退出码、commit hash 和实际文件清单；如果使用 `--only`，还要比较其余 staged diff 与提交前快照，确认其他组的暂存内容没有丢失或改变。
10. 验证通过后再继续下一组；最终报告每个 commit hash、消息、文件，以及剩余未提交改动。

如果某组失败，停止后续提交并报告已经成功的提交和当前仓库状态；不得自动 amend、reset 或回滚。

## Safety

- 敏感路径或内容（如 `.env*`、credentials、secrets、`*.pem`、`*.key`、令牌、证书）默认排除；只有用户明确点名包含后才可暂存。
- 大型或未知二进制文件必须在计划中标出大小并等待明确确认。
- 不输出检测到的秘密值。
- 不使用 `--no-verify`，除非用户明确要求并已获准。
- 不 amend、不 force push，不修改或删除用户未授权的改动。
- Commit hook 修改工作区或提交失败时立即停止并报告，不自动修复或重试。

## Completion Criteria

准备阶段只有在以下条件全部满足时才完成：

- 仓库规则已读取并报告来源；
- staged、unstaged、untracked 等全部路径均已检查；
- 每个路径恰好归入一个组、排除项或待决定项；
- 原子组按业务意图形成，type 只表示主要意图；
- 每组完整 commit message 已展示；
- 尚未执行任何 Git 写操作；
- 已明确等待用户确认。

执行阶段只有在每个成功提交都完成 hash/文件验证，并报告剩余工作区状态后才完成。

## Example

以下文件共同交付“用户登录”能力：

```text
src/auth/login.ts
tests/auth/login.spec.ts
docs/auth.md
```

它们应形成一个原子组，而不是拆成 `feat`、`test`、`docs` 三个提交：

```text
feat(auth): 增加用户登录能力

实现登录认证及回归测试，并补充使用说明。
```
