# Phase D: Experiment Design (S9-S11)

## S9: EXPERIMENT_DESIGN — 实验设计

### 输入
- `stage-7/synthesis.md` — 研究综述
- `stage-8/hypotheses.md` — 研究假设

### 产出
- `stage-9/exp_plan.yaml` — 实验方案（YAML 格式）

### System Prompt

```
You are a principal investigator designing rigorous research experiments.
```

### User Prompt 模板

```
Design an experiment plan as YAML.
Required keys: objectives, datasets, baselines, proposed_methods, ablations, metrics, risks, compute_budget.

NAMING REQUIREMENT (CRITICAL):
- Every condition name MUST be a DESCRIPTIVE algorithm name derived from the hypotheses, NOT generic labels.
- WRONG: baseline_1, method_variant_1
- RIGHT: names reflecting specific methods/algorithms in the hypotheses

BASELINE & BENCHMARK MODERNITY:
- Baselines MUST be modern methods from recent top-venue papers (2023-2026).
- Include at LEAST one strong baseline representing current SOTA.
- For each baseline, cite the original paper.

HYPOTHESIS ALIGNMENT:
- Experiment plan MUST directly test the hypotheses.
- Each hypothesis should map to at least one comparison between conditions.

STATISTICAL POWER:
- AT LEAST 5 random seeds per condition (10 preferred)
- Report: mean ± std, 95% bootstrap CI
- Use paired bootstrap or Wilcoxon signed-rank test

COMPUTE BUDGET:
- Design experiments that can run on a single machine.
- Total conditions (baselines + methods + ablations) should not exceed 8.

IMPLEMENTATION SPECIFICATION:
For each method/baseline include:
  - class_name: Python class name
  - key_methods: list of methods to implement
  - algorithm_steps: pseudocode (3-10 steps)
  - loss_function: mathematical formula
  - key_hyperparameters: dict of name -> default value

Hypotheses:
{hypotheses}

Synthesis context:
{synthesis}
```

### 执行步骤

1. 读取 `stage-8/hypotheses.md` 和 `stage-7/synthesis.md`
2. 发送 LLM 请求
3. 从响应中提取 YAML 内容（可能包裹在 ```yaml 代码块中）
4. 验证 YAML 格式是否合法，不合法则要求 LLM 修复（最多重试 2 次）
5. 写入 `stage-9/exp_plan.yaml`
6. 推送中文摘要

---

## S10: CODE_GENERATION — 代码生成

### 输入
- `stage-9/exp_plan.yaml` — 实验方案

### 产出
- `stage-10/experiment.py` — 主实验代码
- `stage-10/` 下可能有多个 .py 文件（models.py, config.py 等）

### System Prompt

```
You are a computational scientist who writes real, runnable experiments. Your code implements actual algorithms with real mathematical operations. You NEVER fake results with random number generators. Always use the ```filename:xxx.py format for each file. Use numpy for numerical computation. Keep code self-contained.
```

### User Prompt 模板（核心要求摘要）

```
Generate a Python experiment project for the following research topic.

CRITICAL REQUIREMENTS:
1. Implement the ACTUAL experiment described in the plan.
2. Use proper mathematical models appropriate for the domain.
3. Produce REAL NUMERICAL METRICS as JSON to stdout.
4. Code must be SELF-CONTAINED — no external datasets to download.
5. NEVER use random.random() as a substitute for real computation.
6. Output format: print(json.dumps({"metrics": {...}, "condition": "...", "seed": N}))
7. Total runtime must complete within 300 seconds.
8. Use numpy, scipy, sklearn only (no torch/tensorflow unless GPU available).

Experiment plan:
{exp_plan}
```

### ⚠️ 代码验证循环

生成代码后需要验证：
1. 用 `exec` 运行 `python3 -c "import ast; ast.parse(open('experiment.py').read())"` 检查语法
2. 如果语法错误，把错误信息发回 LLM 修复（最多 3 轮）
3. 可选：在沙盒中试运行 30 秒检查是否崩溃

### 执行步骤

1. 读取 `stage-9/exp_plan.yaml`
2. 发送 LLM 请求（max_tokens=8192）
3. 从响应中提取代码块（按 ```filename:xxx.py 格式分割）
4. 写入 `stage-10/` 目录
5. 语法验证 → 修复循环（最多 3 轮）
6. 推送中文摘要

---

## S11: RESOURCE_PLANNING — 资源规划

### 输入
- `stage-9/exp_plan.yaml` — 实验方案
- `stage-10/` — 生成的代码文件

### 产出
- `stage-11/schedule.json` — 任务调度计划

### System Prompt

```
You are an experiment scheduler.
```

### User Prompt 模板

```
Create schedule JSON with GPU/time estimates.
Schema: {tasks:[{id, name, depends_on, gpu_count, estimated_minutes, priority}], total_gpu_budget, generated}.

Experiment plan:
{exp_plan}
```

### 执行步骤

1. 读取 `stage-9/exp_plan.yaml`
2. 发送 LLM 请求（json_mode=true）
3. 解析 JSON，写入 `stage-11/schedule.json`
4. 推送中文摘要
