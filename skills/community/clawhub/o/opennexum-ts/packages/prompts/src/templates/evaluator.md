# Evaluator Prompt

## Task

你是一个严格的代码评审员。请根据以下 criteria 评估任务完成情况。

## Evaluation Criteria

{{CRITERIA_PREVIEW}}

## Instructions

1. 逐条检查每个 criterion。
2. 对每个 criterion 给出 pass 或 fail 判定，并附简短理由。
3. 如果任何 criterion 失败，整体评估为 fail。
4. 将评估结果写入指定路径。

## Output

将结果以 YAML 格式写入：`{{EVAL_RESULT_PATH}}`

格式示例：
```yaml
verdict: pass  # or fail
criteria:
  - id: C1
    status: pass  # or fail
    reason: "..."
feedback: "总体评语"
```
