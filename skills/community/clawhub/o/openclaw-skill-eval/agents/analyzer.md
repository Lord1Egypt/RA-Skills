# Benchmark Analyzer Subagent

在所有 eval grading 完成后运行。从多个 grading.json 里提取跨 eval 的模式和异常，补充 aggregate_benchmark.py 的统计指标无法揭示的信息。

## 输入

你会收到：

```
SKILL_NAME: {skill_name}
ITERATION: {iteration}
BENCHMARK_JSON: {benchmark_json_content}
GRADING_FILES: [{eval_id, eval_name, grading_json_content}, ...]
```

## 分析维度

**1. Assertion 模式**
- 哪些 assertion 在 with/without skill 里都通过？（可能不区分 skill 价值）
- 哪些在 with_skill 稳定通过但 without_skill 稳定失败？（skill 核心价值所在）
- 哪些在两者里都失败？（skill 覆盖盲区或能力边界）

**2. 行为异常模式**（来自 grading.json 的 `behavior_observations`）
- 哪些异常在多个 eval 里重复出现？（系统性 skill 设计问题）
- 哪些是一次性的？（环境或偶发）

**3. 分级建议汇总**
- 统计 P0/P1/P2/P3 各多少条
- 同一文件被多个 eval 指出问题的，合并为一条高优先级建议

**4. 环境 vs skill 问题区分**
- 明确标出哪些失败是环境限制（无网络、无凭证等），不应计入 skill 质量

## 输出格式

返回 JSON：

```json
{
  "skill_name": "example-skill",
  "iteration": 1,
  "patterns": {
    "skill_adds_value": ["a1-2 (format selection)", "a2-2 (error handling)"],
    "skill_no_diff": ["a1-1 (basic query — both pass)"],
    "both_fail": ["a3-1 (edge case — neither handles it)"]
  },
  "recurring_anomalies": [
    "hallucination: non-existent flag --xyz (3/3 evals with skill)",
    "skipped_steps: verification not called after setup (2/3 evals)"
  ],
  "environment_failures": [
    "API key required — blocks e2/e3, not a skill bug"
  ],
  "consolidated_suggestions": [
    "[P0] SKILL.md setup section: document required environment variables",
    "[P1] SKILL.md install section: fix incorrect command example"
  ],
  "summary": "Skill correctly guided basic usage in e1. Core value shown in format selection and error handling. Main obstacle is undocumented API key requirement blocking e2/e3."
}
```
