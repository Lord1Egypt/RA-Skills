---
name: panda-git-commit
description: >-
  智能生成符合 Conventional Commits 规范的 Git Commit Message。
  自动检测 monorepo scope，支持将变更按功能拆分为多个 commit。
  触发词："commit"、"提交"、"生成 commit message"、"拆分提交"、
  "split commits"、"git commit"。
version: 1.0.1
metadata:
  openclaw:
    homepage: https://github.com/hash-panda/panda-skills#panda-git-commit
    requires:
      anyBins:
        - bun
        - npx
---

# panda-git-commit

智能 Git Commit Message 生成器。自动检测项目已有的 commit 规范配置（commitlint / commitizen / git history 模式），在严格遵守项目规范的前提下融合最佳实践。支持 monorepo scope 自动检测、变更智能拆分、语言自动适配。

## Script Directory

脚本位于本 SKILL.md 所在目录的 `scripts/` 子目录中。

**Agent 执行指引**：
1. 确定本 SKILL.md 文件所在目录路径为 `{baseDir}`
2. 脚本路径 = `{baseDir}/scripts/<script-name>.ts`
3. 解析 `${BUN_X}` 运行时：如果 `bun` 已安装 → `bun`；如果 `npx` 可用 → `npx -y bun`；否则提示安装 bun
4. 将本文档中所有 `{baseDir}` 和 `${BUN_X}` 替换为实际值

**脚本清单**：

| Script | Purpose |
|--------|---------|
| `scripts/main.ts` | CLI 入口，分析 git 变更并输出结构化结果 |
| `scripts/analyzer.ts` | Git diff 分析、语言检测 |
| `scripts/scope-detector.ts` | Monorepo 结构检测、scope 推导 |
| `scripts/convention-detector.ts` | 项目 commit 规范检测（commitlint / commitizen / git history） |
| `scripts/splitter.ts` | 按功能维度拆分变更 |
| `scripts/extend-generator.ts` | EXTEND.md 解析、生成、合并（`--init` 命令支持） |

## Preferences (EXTEND.md)

检查 EXTEND.md 是否存在（按优先级顺序）：

```bash
test -f .panda-skills/panda-git-commit/EXTEND.md && echo "project"
test -f "${XDG_CONFIG_HOME:-$HOME/.config}/panda-skills/panda-git-commit/EXTEND.md" && echo "xdg"
test -f "$HOME/.panda-skills/panda-git-commit/EXTEND.md" && echo "user"
```

| Path | Location |
|------|----------|
| `.panda-skills/panda-git-commit/EXTEND.md` | 项目目录（团队共享） |
| `$XDG_CONFIG_HOME/panda-skills/panda-git-commit/EXTEND.md` | XDG 配置 |
| `$HOME/.panda-skills/panda-git-commit/EXTEND.md` | 用户主目录 |

| Result | Action |
|--------|--------|
| 找到（含 Convention 区块） | 直接读取缓存，跳过 convention/monorepo 检测脚本 |
| 找到（无 Convention 区块） | 读取已有设置，仍运行检测脚本补充缺失信息 |
| 未找到 | 运行全部检测脚本，提示用户执行 `--init` 缓存结果 |

**自动生成**：运行 `--init` 可自动检测项目信息并生成 EXTEND.md（写入项目级路径）。`--init` 只补充缺失区块，不覆盖用户手动配置；`--refresh` 强制重新检测并覆盖。

**EXTEND.md 支持的配置**：语言 | subject 最大长度 | body 换行宽度 | emoji 开关 | 项目规范缓存 | 自定义 type | scope 映射 | scope 别名 | 消息模板

详细格式：[references/extend-schema.md](references/extend-schema.md)

## Defaults

所有可配置项及默认值。EXTEND.md 覆盖这些默认值；CLI 参数覆盖 EXTEND.md。

| Setting | Default | EXTEND.md key | CLI flag | Description |
|---------|---------|---------------|----------|-------------|
| 语言 | `auto` | `language` | `--lang` | auto = 从 git log 自动检测 |
| Subject 最大长度 | `72` | `max_subject_length` | — | subject 行最大字符数 |
| Body 换行 | `80` | `body_wrap` | — | body 自动换行宽度 |
| Emoji | `false` | `emoji` | `--emoji` | type 前是否添加 emoji |

## Usage

```
/panda-git-commit [options]
```

| Option | Description |
|--------|-------------|
| `--init` | 检测项目信息并生成 EXTEND.md，缓存语言/规范/scope 映射 |
| `--refresh` | 强制重新检测并覆盖 EXTEND.md 中的所有检测结果 |
| `--split` | 强制分析并建议将变更拆分为多个 commit |
| `--scope <scope>` | 手动指定 scope，跳过自动检测 |
| `--type <type>` | 手动指定 commit type |
| `--lang <lang>` | 本次手动指定语言（zh / en / ja 等） |
| `--dry-run` | 仅预览生成的 commit message，不执行 git commit |
| `--emoji` | 在 type 前添加 emoji |
| `--with-diff` | 在 JSON 输出中包含原始 diff 内容 |

## Workflow

### Step 0: --init / --refresh 模式

如果用户传入 `--init` 或 `--refresh`：

1. 运行所有检测脚本（语言、规范、monorepo）
2. 生成 EXTEND.md 写入 `.panda-skills/panda-git-commit/EXTEND.md`
3. `--init`：只补充缺失区块，不覆盖用户手动配置
4. `--refresh`：强制重新检测并覆盖所有检测结果
5. 输出摘要后退出，不进入 commit 流程

### Step 1: 加载配置

1.1 检查 EXTEND.md（见 Preferences 章节）

1.2 **缓存判断**：如果 EXTEND.md 存在且包含 `## Convention` 区块：
- 直接从 EXTEND.md 读取语言、规范、scope 映射
- **跳过 Step 2、3、4** 的检测脚本执行
- 仅运行 `analyzeDiff()`（Step 5，每次必须执行）

1.3 如果 EXTEND.md 不存在或缺少 Convention 区块：
- 运行全部检测脚本（Step 2、3、4）
- 在输出中附带提示：「运行 /panda-git-commit --init 可缓存项目配置」

1.4 合并配置优先级：CLI 参数 > EXTEND.md > 自动检测 > 默认值

### Step 2: 检测 Commit 语言（可由缓存跳过）

语言无需手动设置，自动从 git history 推断。**若 EXTEND.md 已缓存 language 设置，跳过本步骤。**

**检测逻辑**（`scripts/analyzer.ts`）：

1. 运行 `git log --oneline -20` 获取最近 20 条 commit message
2. 分析每条 message 的语言特征：
   - 含中文字符（`\u4e00-\u9fff`）→ `zh`
   - 含日文假名（`\u3040-\u309f\u30a0-\u30ff`）→ `ja`
   - 含韩文字符（`\uac00-\ud7af`）→ `ko`
   - 纯 ASCII → `en`
3. 按比例投票，取占比最高的语言
4. 全新仓库（无历史 commit）→ 默认 `en`

**优先级**（高 → 低）：

1. `--lang` CLI 参数 — 用户本次显式指定
2. EXTEND.md `language` 设置（非 `auto`）— 用户持久化偏好
3. git log 自动检测 — 零配置自动适配
4. 兜底默认值 — `en`

### Step 3: 检测项目 Commit 规范（可由缓存跳过）

**若 EXTEND.md 已缓存 Convention 区块，跳过本步骤，直接使用缓存值。**

运行 `${BUN_X} {baseDir}/scripts/convention-detector.ts` 检测项目规范。

**检测策略**（详见 [references/convention-detection.md](references/convention-detection.md)）：

按优先级检测，命中即采用：

1. **commitlint 配置** — `.commitlintrc.*`、`commitlint.config.*`、`package.json` commitlint 字段
2. **commitizen 配置** — `.czrc`、`.cz-config.js`、`package.json` config.commitizen 字段
3. **git hooks** — `.husky/commit-msg`、`.git/hooks/commit-msg` 中引用了 commitlint
4. **git history 模式分析** — 分析最近 50 条 commit，识别 Conventional Commits / Jira 前缀 / Emoji 前缀等模式
5. **默认规范** — 使用 Conventional Commits 最佳实践

**合并策略**（项目规范 + 最佳实践）：

项目配置是「硬约束」，我们的最佳实践是「软增强」。二者合并，不冲突的最佳实践自动生效：

| 项目已配置 | 我们的最佳实践 | 结果 |
|-----------|--------------|------|
| `types: [feat, fix, docs, chore]` | 建议使用标准 10 个 type | **遵守项目配置**，只用 4 个 type |
| `header-max-length: 100` | 建议 72 字符 | **遵守项目配置**，使用 100 字符 |
| 未配置 body 换行 | 建议 body 每行不超过 80 字符 | **应用最佳实践**，80 字符换行 |
| 未配置 subject 风格 | 使用祈使语气 | **应用最佳实践**，祈使语气 |
| Jira 前缀模式 `[PROJ-123]` | Conventional Commits 格式 | **遵守项目模式**，但补充 body/footer 最佳实践 |

**输出结构**：

```json
{
  "convention": {
    "source": "commitlint",
    "format": "conventional-commits",
    "rules": {
      "types": ["feat", "fix", "docs", "chore"],
      "scopeRequired": false,
      "subjectMaxLength": 100
    },
    "bestPractices": [
      "body 每行建议不超过 80 字符",
      "subject 使用祈使语气",
      "body 解释「为什么」变更，而非「做了什么」"
    ]
  }
}
```

AI agent 在生成 commit message 时：
- **必须**遵守 `rules` 中的所有约束
- **应当**遵循 `bestPractices` 中的建议（不与 rules 冲突时）
- 如果 `format` 不是 `conventional-commits`（如 `jira-prefix`），按检测到的格式生成

### Step 4: 检测仓库结构（可由缓存跳过）

**若 EXTEND.md 已缓存 Scope Mapping 区块，跳过本步骤，直接使用缓存的映射。**

运行 `${BUN_X} {baseDir}/scripts/scope-detector.ts` 检测项目结构。

**检测策略**（详见 [references/monorepo-detection.md](references/monorepo-detection.md)）：

1. 检查 monorepo 配置文件：`package.json` workspaces、`pnpm-workspace.yaml`、`lerna.json`、`nx.json`、`turbo.json`
2. 如果是 monorepo → 遍历 workspace 目录，读取每个子包的 `package.json`（Nx 优先读 `project.json`）的 `name` 字段作为 scope
3. 如果 `name` 字段不存在 → 兜底使用目录名
4. 如果不是 monorepo → 按目录结构推导 scope

### Step 5: 分析 Git Diff

运行 `${BUN_X} {baseDir}/scripts/analyzer.ts` 分析变更。

1. 解析 `git diff --staged --stat` 获取变更文件列表
2. 解析 `git diff --staged` 获取详细 diff 内容
3. 如果没有 staged 变更，分析 unstaged 变更并提示用户先 `git add`
4. 根据变更文件路径，结合 Step 4 的结构信息推导 scope
5. 根据 diff 内容分析变更类型（feat / fix / refactor 等）
6. 如果 Step 3 检测到 `rules.types`，仅在允许的 type 中选择

### Step 6: 生成 Commit Message

根据 Step 3 检测到的规范和变更分析结果生成 commit message。

**生成原则**：
- 如果 `convention.format` 为 `conventional-commits` 或 `angular` → 使用 `type(scope): description` 格式
- 如果为 `jira-prefix` → 使用检测到的 Jira 前缀模式（如 `[PROJ-123] description`）
- 如果为 `emoji-prefix` → 使用 emoji 前缀模式
- 如果为 `free-form` → 使用 Conventional Commits 最佳实践（兜底）
- `convention.rules` 中的约束（types / scopeRequired / subjectMaxLength 等）必须严格遵守
- `convention.bestPractices` 中的建议在不冲突时应用

**6a. 单个 commit**（变更集中在同一 scope 和 type）：

直接生成符合项目规范的 message：

```
type(scope): description

可选的 body 内容，描述变更的原因和影响。

可选的 footer，如 BREAKING CHANGE 等。
```

**6b. 建议拆分**（变更跨越多个 scope 或 type）：

运行 `${BUN_X} {baseDir}/scripts/splitter.ts` 生成拆分建议：

```
建议拆分为 N 个 commit：

1. type(scope): description
   - path/to/file1.ts (新增)
   - path/to/file2.ts (修改)

2. type(scope): description
   - path/to/file3.ts (修改)
```

使用 `--split` 参数可强制进入拆分分析模式。

### Step 7: 用户确认

将生成的 commit message 展示给用户：

- 用户确认 → 进入 Step 8
- 用户修改 → 应用修改后进入 Step 8
- 拆分模式下用户可合并或调整分组
- 如果检测到项目规范（source 非 default），提示：「已遵循项目 {source} 规范」

### Step 8: 执行 Commit

- 单个 commit：执行 `git commit -m "<message>"`
- 拆分 commit：按顺序执行 `git add <files> && git commit -m "<message>"` 逐个提交
- `--dry-run` 模式：仅输出 message，不执行 git 命令

### Step 9: 输出摘要

```
Commit 完成

规范: commitlint (项目配置)
类型: feat(auth)
语言: zh (自动检测)
Message: feat(auth): 添加 JWT 刷新 token 功能
```

如果使用默认规范：

```
Commit 完成

规范: Conventional Commits (最佳实践)
类型: feat(auth)
语言: zh (自动检测)
Message: feat(auth): 添加 JWT 刷新 token 功能
```

拆分模式下输出每个 commit 的摘要。

## Conventional Commits 规范

详见 [references/conventional-commits.md](references/conventional-commits.md)

格式：`<type>(<scope>): <description>`

**内置 types**（详见 [references/commit-types.md](references/commit-types.md)）：

| Type | Emoji | Description |
|------|-------|-------------|
| `feat` | ✨ | 新功能 |
| `fix` | 🐛 | Bug 修复 |
| `docs` | 📝 | 文档变更 |
| `style` | 💄 | 代码格式（不影响逻辑） |
| `refactor` | ♻️ | 重构（非 feat、非 fix） |
| `perf` | ⚡ | 性能优化 |
| `test` | ✅ | 测试相关 |
| `chore` | 🔧 | 构建/工具链变更 |
| `ci` | 👷 | CI/CD 配置 |
| `build` | 📦 | 构建系统变更 |

支持 `!` 表示 BREAKING CHANGE：`feat(api)!: 移除废弃的 v1 接口`

## Extension Support

自定义配置通过 EXTEND.md 实现。详见 **Preferences** 章节了解路径和支持的选项。
