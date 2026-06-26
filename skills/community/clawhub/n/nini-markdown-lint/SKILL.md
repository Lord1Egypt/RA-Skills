---
name: markdown-lint
description: >-
  Use this skill immediately when the user needs to: set up markdownlint-cli2 and
  pre-commit hooks in a repository, fix or batch-repair markdownlint errors like
  MD013/MD040/MD060, configure .markdownlint.json rules, remove horizontal rules
  from markdown files while preserving YAML frontmatter, or run markdown format
  checking in a monorepo. Trigger on: markdownlint 报错, 设置 markdown lint,
  格式化 markdown, 检查 md 格式, 设置 pre-commit, markdownlint error,
  MD013/MD040/MD060 violations. Do NOT use for general article proofreading,
  writing new markdown content, or YAML/JSON linting.
metadata: {"openclaw":{"emoji":"📋","requires":{"bins":["markdownlint-cli2"],"anyBins":["pre-commit"],"install":[{"type":"node","pkg":"markdownlint-cli2"}]}}}
---

# Markdown Lint

为仓库配置 markdown 格式检查（markdownlint + 水平线禁止）和 pre-commit hook。

## Prerequisites

| Tool | Type | Required | Install |
|------|------|----------|---------|
| Node.js | cli | Yes | `brew install node` or [nodejs.org](https://nodejs.org/) |
| markdownlint-cli2 | cli | Yes | `npx markdownlint-cli2` (no install needed) |
| pre-commit | cli | No | `uv tool install pre-commit --with pre-commit-uv` or `pipx install pre-commit` or `brew install pre-commit` |

> Do NOT proactively verify these tools on skill load. If a command fails due to a missing tool, directly guide the user through installation and configuration step by step.

## When to Use

- **新仓库初始化**：第一次为仓库添加 markdown 格式标准
- **检查/修复**：运行格式检查或批量修复现有文件
- **迁移**：将格式标准复制到另一个仓库

**不适用：**

- **单文件检查**：直接运行 `npx markdownlint-cli2 file.md`，不需要走 setup 流程
- **文章内容审校**：使用 writing-proofreading skill（步骤 6 会引用本 skill）

## Setup 流程

### 1. 检查仓库状态

```bash
# 已有配置？跳到「检查/修复」
ls .markdownlint.json .pre-commit-config.yaml 2>/dev/null
```

### 2. 创建配置文件

**`.markdownlint.json`：**

```json
{
  "default": true,
  "MD013": false,
  "MD024": { "siblings_only": true },
  "MD033": false,
  "MD035": false,
  "MD036": false,
  "MD041": false,
  "MD060": false
}
```

关闭规则说明：

| 规则 | 理由 |
|------|------|
| MD013 | CJK 文本和表格不适合行长度限制 |
| MD033 | 允许 `<br>`, `<small>` 等 inline HTML |
| MD035 | 水平线完全禁止，由独立脚本检查 |
| MD036 | 允许 bold 作视觉标题 |
| MD041 | YAML frontmatter 导致首行非标题 |
| MD060 | 表格管道符间距样式过于严格 |

**按需追加禁用**（根据仓库内容酌情添加）：

| 规则   | 场景                       | 理由                                 |
| ------ | -------------------------- | ------------------------------------ |
| MD025  | 仓库含导入/vendor 文档     | 协议文档常有多个 H1                  |
| MD045  | 仓库含导入/vendor 文档     | vendor 文档图片无 alt text           |
| MD051  | CJK 锚点链接              | `#_中文标题` 格式的片段不被识别      |
| MD056  | 复杂参考表格               | 合并行/变长列的表格触发误报          |

**`.pre-commit-config.yaml`：**

```yaml
repos:
  - repo: https://github.com/DavidAnson/markdownlint-cli2
    rev: v0.21.0  # 运行 pre-commit autoupdate 获取最新
    hooks:
      - id: markdownlint-cli2
  - repo: local
    hooks:
      - id: no-horizontal-rules
        name: no horizontal rules outside frontmatter
        entry: scripts/check-horizontal-rules.sh
        language: script
        types: [markdown]
```

> 创建后必须运行 `pre-commit autoupdate`，上面的 rev 可能已过时。

**`scripts/check-horizontal-rules.sh`：**

从 [scripts/check-horizontal-rules.sh](scripts/check-horizontal-rules.sh) 复制，然后 `chmod +x`。

> **Windows 用户**：`.sh` 脚本需要在 Git Bash 或 WSL 中运行。

**`.gitignore`**（如果没有）：

```text
node_modules/
.mypy_cache/
__pycache__/
```

### 3. 移除现有 `---` 分隔线

保留 YAML frontmatter 的 `---`，删除其余所有水平线：

```bash
# 找出违规文件
bash scripts/check-horizontal-rules.sh $(find . -name '*.md' -not -path './node_modules/*')

# 提取违规文件列表（仅匹配 .md: 格式的行，避免捕获错误消息）
files=$(bash scripts/check-horizontal-rules.sh \
  $(find . -name '*.md' -not -path './node_modules/*') 2>&1 \
  | grep -E '\.md:[0-9]+:' | grep -oE '^[^:]+' | sort -u)

# 批量移除（保留 frontmatter）
for file in $files; do
  awk 'NR == 1 && /^---[[:space:]]*$/ { print; fm = 1; next } fm && /^---[[:space:]]*$/ { print; fm = 0; next } !fm && /^[[:space:]]*[-*_][[:space:]]*[-*_][[:space:]]*[-*_][-*_ ]*$/ { next } { print }' "$file" > "$file.tmp" && mv "$file.tmp" "$file"
  echo "Fixed: $file"
done
```

> **注意**：grep 必须用 `\.md:[0-9]+:` 过滤，否则脚本末尾的 "Error: ..." 错误消息会被当成文件名。

### 4. 格式化全部文件

```bash
# 单仓库
npx markdownlint-cli2 --fix "**/*.md"
npx markdownlint-cli2 "**/*.md"

# monorepo（排除子仓库和依赖目录）
npx markdownlint-cli2 --fix "**/*.md" "#repos" "#node_modules"
npx markdownlint-cli2 "**/*.md" "#repos" "#node_modules"
```

### 4a. 处理无法自动修复的错误

`--fix` 无法修复的常见错误：

- **MD040**（代码块缺少语言）：给 ` ``` ` 加上语言标识（`python`、`bash`、`yaml`、`text` 等）
- **MD025/MD045/MD051/MD056**：如果大量出现在 vendor 文档中，在 `.markdownlint.json` 中禁用对应规则

先分析错误分布再决定策略：

```bash
# 按规则统计
npx markdownlint-cli2 "**/*.md" "#repos" "#node_modules" 2>&1 \
  | grep -oE 'MD[0-9]+' | sort | uniq -c | sort -rn

# 按文件统计
npx markdownlint-cli2 "**/*.md" "#repos" "#node_modules" 2>&1 \
  | grep -oE '^[^:]+' | sort | uniq -c | sort -rn | head -10
```

### 5. 安装 hook

```bash
pre-commit install
```

### 6. 验证

```bash
# 两项检查全部通过（monorepo 加 "#repos" 排除子仓库）
npx markdownlint-cli2 "**/*.md" "#repos" "#node_modules"
bash scripts/check-horizontal-rules.sh $(find . -name '*.md' -not -path './repos/*' -not -path './node_modules/*')
# 测试 hook: 故意加 --- 到某 md 文件，git add + commit，应被拦截
```

## 检查/修复（已有配置的仓库）

```bash
npx markdownlint-cli2 "**/*.md" "#repos" "#node_modules"            # 检查
npx markdownlint-cli2 --fix "**/*.md" "#repos" "#node_modules"      # 自动修复
bash scripts/check-horizontal-rules.sh $(find . -name '*.md' -not -path './repos/*' -not -path './node_modules/*')
```

> 单仓库项目去掉 `"#repos"` 即可。

## 常见问题

| 问题 | 原因 | 修复 |
|------|------|------|
| `pre-commit: command not found` | 未安装 | `uv tool install pre-commit --with pre-commit-uv`（推荐）或 `pipx install pre-commit` / `brew install pre-commit` |
| markdownlint 大量 MD060 错误 | 表格管道符间距 | `.markdownlint.json` 中 `"MD060": false` |
| 大量 MD056 错误 | vendor 文档复杂表格 | `.markdownlint.json` 中 `"MD056": false` |
| 大量 MD051 错误 | CJK 锚点链接 | `.markdownlint.json` 中 `"MD051": false` |
| `.sh` 脚本在 Windows 无法执行 | Windows 不原生支持 Bash | 使用 Git Bash 或 WSL |
| frontmatter `---` 被误删 | awk 脚本问题 | 确认文件第 1 行是 `---` 且紧接 YAML 内容 |
| 批量删除 HR 产生垃圾 `.tmp` 文件 | grep 捕获了脚本错误消息作为文件名 | 用 `grep -E '\.md:[0-9]+:'` 过滤，仅匹配文件路径行 |
| `--fix` 未修复所有问题 | 部分规则无法自动修复 | 手动修复（通常是 MD040 缺少代码块语言，加 ` ```text ` 等） |
