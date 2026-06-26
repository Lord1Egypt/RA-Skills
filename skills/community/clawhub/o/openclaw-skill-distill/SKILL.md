---
name: skill-distill
description: Strip any local project into a clean, publishable agent skill. Scan for hardcoded paths and secrets, scaffold standard structure, validate before publish. Use when you need to distill, extract, generalize, package, or publish a skill from an existing project or codebase.
---

# skill-distill

Turn any local project into a clean, publishable ClawHub skill.

Complementary to `skill-creator` (build from scratch) — `skill-distill` extracts from existing code.

## Tools

| Tool | What it does | Command |
|------|-------------|---------|
| `scan` | Detect hardcoded paths, secrets, local config references | `bash skills/skill-distill/scripts/scan.sh <project-dir>` |
| `scaffold` | Generate standard skill directory structure from a project | `bash skills/skill-distill/scripts/scaffold.sh <project-dir> <skill-name>` |
| `validate` | Pre-publish check: structure, frontmatter, no local traces | `bash skills/skill-distill/scripts/validate.sh <skill-dir>` |

## Typical Flow

```
scan → fix issues → scaffold → validate → clawhub publish
```

## Prerequisites

- bash, grep (no external dependencies)
- `clawhub` CLI for the final publish step

---

## Agent Workflow (below this line is for agent consumption)

### 1. Scan — 扫描本地痕迹

```bash
bash skills/skill-distill/scripts/scan.sh <project-dir>
```

扫描硬编码路径、敏感信息、本地配置引用。输出问题列表。

### 2. Fix — 修复发现的问题

根据 scan 输出，逐项修复：
- 硬编码路径 → 参数化 / 环境变量
- 敏感信息 → 移除或占位符替换
- 本地配置引用 → 通用化

### 3. Scaffold — 生成标准骨架

```bash
bash skills/skill-distill/scripts/scaffold.sh <project-dir> <skill-name>
```

从项目目录生成标准 skill 目录结构。

### 4. Validate — 发布前校验

```bash
bash skills/skill-distill/scripts/validate.sh <skill-dir>
```

检查目录结构、frontmatter、无残留本地痕迹。还会检测 frontmatter 的 name/description 是否包含中文字符（ClawHub 要求全英文）。PASS 才可发布。

### 5. Publish

```bash
clawhub publish <skill-dir>
```

## 检查清单

详见 `references/checklist.md`。
