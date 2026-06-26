# Creative Writing Task: {{TASK_NAME}}

## Cognitive Mode

先准确理解创作意图，再动手写作。
- 只完成 Contract 直接要求的内容，不主动扩展主题或风格。
- 如果发现问题超出 Contract 范围，停止扩写范围，改为在 field report 中说明。
- 优先保持一致的风格和语调，不要为展示能力引入不必要的复杂度。

## Scope

### Output Files
{{SCOPE_FILES}}

## Task Deliverables

{{DELIVERABLES}}

## Criteria Preview

{{CRITERIA_PREVIEW}}

## Relevant Lessons

{{RELEVANT_LESSONS}}

## Commit Instructions

完成后执行以下提交命令：

```bash
{{GIT_COMMIT_CMD}}
```

## Completeness Principle

- 交付必须完整可读，不要留下"下一步再补"的半成品。
- 必须覆盖所有 deliverables；完成一部分不算完成。
- 改动应保持最小且闭环。
- 不要为了通过评估伪造结果或隐藏已知问题。

## Field Report

完成后填写：

```markdown
## Field Report
- task: {{TASK_NAME}}
- changed_files: [列出实际修改文件]
- deliverables_done: [逐条对应 deliverables 说明完成情况]
- tests_or_checks: [运行过的测试、命令或人工检查]
- blockers: [若无则写 none]
- notes_for_evaluator: [提醒 evaluator 关注的实现点；若无则写 none]
```
