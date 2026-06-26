# Coding Task: {{TASK_NAME}}

## Scope

### Allowed Files
{{SCOPE_FILES}}

## Task Deliverables

{{DELIVERABLES}}

## Criteria Preview

{{CRITERIA_PREVIEW}}

## Cognitive Mode

**开工前：先探索，后动手。**
1. 阅读 scope 内的现有文件，理解当前实现和项目约定。
2. 确认理解任务意图后，再开始修改。

工作中：
- 只完成 Contract 直接要求的工作，不主动扩展需求。
- 优先复用现有代码、模式和项目约定，不要为展示能力引入额外复杂度。
- 如果发现问题超出 Contract 范围，停止扩写范围，改为在 Field Report 中说明。

## Relevant Lessons

{{RELEVANT_LESSONS}}

## Field Report

完成后，将以下内容填写完整，并写入文件 `nexum/runtime/field-reports/{{TASK_ID}}.md`（evaluator 会直接读取此文件进行评审，不写入则评审无上下文）：

```markdown
## Field Report
- task: {{TASK_NAME}}
- iteration: [当前迭代次数，首次为 1]
- changed_files: [列出实际修改的文件]
- deliverables_done: [逐条对应 deliverables 说明完成情况]
- tests_or_checks: [运行过的测试、命令或人工检查]
- blockers: [若无则写 none]
- notes_for_evaluator: [提醒 evaluator 关注的实现点；若无则写 none]
```

## Commit & Callback Instructions

完成实现后，依次执行以下命令：

```bash
# 1. commit + push（命令已预生成为英文，直接运行，不要修改 commit message）
{{GIT_COMMIT_CMD}}

# 2. 通知编排者（替换 <> 内的实际值）
nexum callback {{TASK_ID}} --project {{PROJECT_DIR}} \
  --model <当前使用的模型名，如 gpt-5.4 或 claude-sonnet-4-6> \
  --input-tokens <本次对话 input token 数量> \
  --output-tokens <本次对话 output token 数量>
```

## Completeness Principle

- 交付必须可运行、可验证，不要留下"下一步再补"的半成品。
- 必须覆盖所有 deliverables；完成一部分不算完成。
- 改动应保持最小且闭合：代码、测试、文档更新应与任务边界一致。
- 不要为了通过评估伪造结果、跳过失败路径或隐藏已知问题。
