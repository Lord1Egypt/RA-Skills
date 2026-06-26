# Review Guidelines

When reviewing code as part of the gitlab-auto-review skill, evaluate the following aspects:

## Severity Levels

### Critical (Must Fix)
- **Security vulnerabilities**: SQL injection, XSS, command injection, hardcoded secrets, insecure deserialization
- **Data loss risks**: Missing transactions, race conditions, unhandled errors that could corrupt data
- **Authentication/Authorization flaws**: Missing permission checks, token leaks

### Important (Should Fix)
- **Bug-prone patterns**: Off-by-one errors, null pointer risks, unhandled edge cases, incorrect type usage
- **Performance issues**: N+1 queries, unnecessary loops, missing indexes, memory leaks
- **Error handling**: Swallowed exceptions, missing error propagation, unclear error messages

### Suggestions (Nice to Have)
- **Code clarity**: Confusing naming, overly complex logic, missing context for non-obvious code
- **Best practices**: Framework-specific anti-patterns, deprecated API usage
- **Maintainability**: Code duplication that could be reasonably abstracted

## What NOT to Comment On
- Style/formatting issues (leave these to linters)
- Minor naming preferences
- Adding comments to self-explanatory code
- Changes outside the diff context

## Inline Comment JSON Format (Critical)

⚠️ 写入 /tmp/comment-N.json 时必须严格使用以下格式，每个问题一个文件：

```json
{
  "body": "**[Critical/Important/Suggestion]** 问题标题\n\n问题描述和建议",
  "position": {
    "base_sha": "从 get-changes 输出的 diff_refs.base_sha 获取",
    "start_sha": "从 get-changes 输出的 diff_refs.start_sha 获取",
    "head_sha": "从 get-changes 输出的 diff_refs.head_sha 获取",
    "new_path": "文件路径",
    "new_line": 新文件中的实际行号
  }
}
```

**绝对禁止：**
- ❌ 包在数组里 `[{}, {}]`
- ❌ 包在额外对象里 `{"inline_comments": [{...}]}`
- ❌ 使用 `file_path` / `comment` 等自定义字段名（必须是 `body` + `position`）
- ❌ 编造 SHA 值（必须从 diff_refs 获取）

## Line Number Calculation (Critical)

When posting inline comments, the `new_line` field must be the **actual line number in the new version of the file**, not the line number in the diff text.

How to calculate `new_line` from a unified diff:
1. Find the hunk header containing the target line: `@@ -old_start,old_count +new_start,new_count @@`
2. Start counting from `new_start`
3. For each line in the hunk:
   - Lines starting with ` ` (context) → increment counter
   - Lines starting with `+` (addition) → increment counter
   - Lines starting with `-` (deletion) → do NOT increment
4. The counter value when you reach the target line IS the `new_line`

Example:
```
@@ -10,4 +10,5 @@
 context line     → new_line = 10
-old line         → skip (no increment)
+added line       → new_line = 11
+another add      → new_line = 12
 context line     → new_line = 13
```

⚠️ Common mistake: counting all diff lines (including `-` lines) or counting from 1 instead of the hunk offset. Double-check your math before posting!

## Output Format

For each issue found, format your inline comment as:

```markdown
**[severity]** brief_title

description of the issue and why it matters.

suggestion or fix (if applicable):
\`\`\`language
suggested code
\`\`\`
```

Where `severity` is one of: `Critical`, `Important`, `Suggestion`.

## Summary Format

After reviewing all files, post a summary note using the `post-note` command:

```markdown
## MR Code Review Summary

**Result**: ✅ Approved / ⚠️ Changes Requested

**Overview**: Brief description of what this MR does (1-2 sentences based on the diff content).

**Stats**: X files reviewed, Y issues found (Z critical, W important, V suggestions)

### Issues Found (if any)
- `file_path:line` — brief description of each issue

### Highlights (if any)
- Notable positive aspects of the code changes
```

If no issues are found, approve the MR and provide a concise summary of the changes.