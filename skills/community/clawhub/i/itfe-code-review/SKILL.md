---
name: itfe-code-review
description: "Expert code review of current git changes with a senior engineer lens. Detects SOLID violations, security risks, and proposes actionable improvements."
---

# ITFE Code Review

## 🌐 Language Requirement

**CRITICAL: You MUST respond ONLY in Simplified Chinese (简体中文).**

- All review reports, findings, descriptions, and suggestions MUST be in Chinese
- All communication with the user MUST be in Chinese
- Code comments and variable names can remain in their original language
- Do NOT use English, Japanese, Korean, or any other language for explanations

## Overview

Perform a structured review of the current git changes with focus on SOLID, architecture, removal candidates, and security risks. Default to review-only output unless the user asks to implement changes.

## Severity Levels

| Level | Name | Description | Action |
|-------|------|-------------|--------|
| **P0** | Critical | Security vulnerability, data loss risk, correctness bug | Must block merge |
| **P1** | High | Logic error, significant SOLID violation, performance regression | Should fix before merge |
| **P2** | Medium | Code smell, maintainability concern, minor SOLID violation | Fix in this PR or create follow-up |
| **P3** | Low | Style, naming, minor suggestion | Optional improvement |

## Workflow

### 1) Preflight context

- Use `git status -sb`, `git diff --stat`, and `git diff` to scope changes.
- If needed, use `rg` or `grep` to find related modules, usages, and contracts.
- Identify entry points, ownership boundaries, and critical paths (auth, payments, data writes, network).

**Edge cases:**
- **No changes**: If `git diff` is empty, inform user and ask if they want to review staged changes or a specific commit range.
- **Large diff (>500 lines)**: Summarize by file first, then review in batches by module/feature area.
- **Mixed concerns**: Group findings by logical feature, not just file order.

### 2) SOLID + architecture smells

- Load `references/solid-checklist.md` for specific prompts.
- Look for:
  - **SRP**: Overloaded modules with unrelated responsibilities.
  - **OCP**: Frequent edits to add behavior instead of extension points.
  - **LSP**: Subclasses that break expectations or require type checks.
  - **ISP**: Wide interfaces with unused methods.
  - **DIP**: High-level logic tied to low-level implementations.
- When you propose a refactor, explain *why* it improves cohesion/coupling and outline a minimal, safe split.
- If refactor is non-trivial, propose an incremental plan instead of a large rewrite.

### 3) Removal candidates + iteration plan

- Load `references/removal-plan.md` for template.
- Identify code that is unused, redundant, or feature-flagged off.
- Distinguish **safe delete now** vs **defer with plan**.
- Provide a follow-up plan with concrete steps and checkpoints (tests/metrics).

### 4) Security and reliability scan

- Load `references/security-checklist.md` for coverage.
- Check for:
  - XSS, injection (SQL/NoSQL/command), SSRF, path traversal
  - AuthZ/AuthN gaps, missing tenancy checks
  - Secret leakage or API keys in logs/env/files
  - Rate limits, unbounded loops, CPU/memory hotspots
  - Unsafe deserialization, weak crypto, insecure defaults
  - **Race conditions**: concurrent access, check-then-act, TOCTOU, missing locks
- Call out both **exploitability** and **impact**.

### 5) Code quality scan

- Load `references/code-quality-checklist.md` for coverage.
- Check for:
  - **Error handling**: swallowed exceptions, overly broad catch, missing error handling, async errors
  - **Performance**: N+1 queries, CPU-intensive ops in hot paths, missing cache, unbounded memory
  - **Boundary conditions**: null/undefined handling, empty collections, numeric boundaries, off-by-one
- Flag issues that may cause silent failures or production incidents.

### 6) Output format

**CRITICAL: Output all content in Simplified Chinese (简体中文).**

Structure your review as follows:

```markdown
## 代码审查报告

**审查文件数**：X 个文件，Y 行变更
**总体评估**：[通过 / 需要修改 / 建议]

---

## 发现的问题

### P0 - 严重
（无 或 列表）

### P1 - 高
- **[文件:行号]** 简短标题
  - 问题描述
  - 修复建议

### P2 - 中
...

### P3 - 低
...

---

## 删除/迭代计划
（如适用）

## 其他建议
（可选改进，不阻塞）
```

**Inline comments**: Use this format for file-specific findings:
```
::code-comment{file="path/to/file.ts" line="42" severity="P1"}
Description of the issue and suggested fix.
::
```

**Clean review** (in Chinese): If no issues found, explicitly state:
- 检查了什么内容
- 未覆盖的区域（例如："未验证数据库迁移"）
- 残留风险或建议的后续测试

### 7) Next steps confirmation (in Chinese)

After presenting findings, ask user how to proceed (in Chinese):

```markdown
---

## 下一步行动

我发现了 X 个问题（P0: _, P1: _, P2: _, P3: _）。

**你希望如何处理？**

1. **全部修复** - 我将实现所有建议的修复
2. **仅修复 P0/P1** - 处理严重和高优先级问题
3. **修复指定项** - 告诉我要修复哪些问题
4. **不做修改** - 仅审查，不需要实现

请选择一个选项或提供具体指示。
```

**Important**: Do NOT implement any changes until user explicitly confirms. This is a review-first workflow. All communication must be in Chinese.

## Resources

### references/

| File | Purpose |
|------|---------|
| `solid-checklist.md` | SOLID smell prompts and refactor heuristics |
| `security-checklist.md` | Web/app security and runtime risk checklist |
| `code-quality-checklist.md` | Error handling, performance, boundary conditions |
| `removal-plan.md` | Template for deletion candidates and follow-up plan |
