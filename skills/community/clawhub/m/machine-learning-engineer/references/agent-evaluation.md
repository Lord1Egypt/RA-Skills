# Agent 评估 Playbook（增量方法论）

> 配套子技能 [`skills/agent-evaluation/SKILL.md`](../skills/agent-evaluation/SKILL.md)。
> 本篇是 **L2 方法论层**（决策树 + 命令 + 坑 + 检查清单），[skills/agent-evaluation/](../skills/agent-evaluation/SKILL.md) 是 **L3 可安装单元**（评分器脚手架/模板）。
> **层次边界**：只想看评测方法论 → 只读本篇；要复用评分器骨架/模板才 `npx skills add skills-repo/machine-learning-engineer@agent-evaluation`。默认以 MLflow 3.8+ 为例，其他框架在 §2 给出对照。

## 1. 先决定"要不要评测、评什么"

```
是否要量化 Agent 表现？
├─ 否（一次性手调）→ 直接试，不用评测流水线
└─ 是
   ├─ 上线前验收？            → 全量评测 + 通过率门槛
   ├─ 改了提示词/模型/工具？  → 回归评测（新旧对比）
   └─ 想证明"变好"？         → 固定数据集 + 指标对比
```

评测前先问清三件事（写在 `agent_description` 里，后面生成样本要用）：
1. Agent 做什么？一句话讲清目的。
2. 最该做对的 2–3 件事是什么？
3. 你已经观察到哪些失败模式？

> 这三点只定义"Agent 是什么"，**不够**设计评分器套件。若标准还很模糊（"回答要准"），
> 先和用户敲定 3–5 条原子标准，再进 §3。

## 2. 评测方法 → 工具选择

| 你想测的 | 首选方法 | 代表工具 | 何时用 |
|----------|----------|----------|--------|
| 答案/响应质量、 helpfulness | LLM-as-judge（裁判模型打分） | MLflow `make_judge`、LangSmith Evaluator、DeepEval | 主观质量、无 gold label |
| 工具调用对不对、链路对不对 | 代码规则检查 + trace 断言 | MLflow `@scorer`、自写函数 | 有确定正确/错误标准 |
| RAG 忠实度/上下文利用 | 引用一致性 + 答案对齐 | RAGAS（faithfulness/context precision） | RAG / 检索型 Agent |
| 任务成功率、端到端轨迹 | 轨迹级评分 / 成功率 | Inspect、AgentEval、MLflow trace 评分 | 多步 Agent、tool-use |
| 线上漂移、持续监控 | 在线评分器 + 采样 | LangSmith / Databricks 在线监控 | 已上线服务 |

**不要自造评测框架。** 用成熟库（MLflow/LangSmith/RAGAS/DeepEval）跑数据集+评分器+追踪，
它们把数据集、评分器、trace、结果都落到同一处，自定义循环会丢掉可观测性。

## 3. MLflow 端到端工作流（具体命令）

### 3.1 环境前置

```bash
uv run mlflow --version                 # 需 >= 3.8.0
echo "MLFLOW_TRACKING_URI=$MLFLOW_TRACKING_URI"
echo "MLFLOW_EXPERIMENT_ID=$MLFLOW_EXPERIMENT_ID"
```
两个环境变量都设好了就跳过安装；否则按官方 setup 配置 tracking URI 与 experiment，并接入 tracing
（`@mlflow.trace` 装饰器 / autolog）。**tracing 不通就先停手排障**——没 trace 评测没有上下文。

### 3.2 注册评分器（关键坑见 §5）

```python
from mlflow.genai.judges import make_judge
from mlflow.genai.scorers import BuiltinScorerName

# LLM 裁判：让模型返回 "yes"/"no"（不是 pass/fail，见 §5）
judge = make_judge(name="answer_correct",
                   judge_prompt="...回答是否正确且回答了问题？只回 yes 或 no")
judge.register()

# 内置 / 代码检查
BuiltinScorerName(...).register()
```

评测前验证：`uv run mlflow scorers list -x $MLFLOW_EXPERIMENT_ID` 应列出你的评分器。

### 3.3 数据集：先 5 条 sanity，再放量

```python
from mlflow.genai.datasets import create_dataset
sanity = create_dataset(
    name="sanity-5q",
    records=[
        {"inputs": {"query": "<访谈第1问>"}, "expected_response": "<期望答案>"},
        # ... 5 条，直接从 §1 访谈推导
    ],
)
```
- **永远先跑 `list_datasets.py` 发现已有数据集**，别重复造。
- 量纲参考：<30 条无统计意义；50–100 条够抓回归；200+ 条适合比模型/比维度。
- RAG/文档型 Agent：用 `ragas.testset.TestsetGenerator` 或 Databricks `generate_evals_df` 从真实语料合成 100 条，比凭空编更真实。

### 3.4 Dry-run 3 条（强制门禁）

全量前先拿 3 条跑 `mlflow.genai.evaluate`，逐条检查：
1. **工具调用**——该检索的题却 0 工具调用 → 工具多半挂了（403 / 限流 / 缺凭证）。
2. **响应质量**——空响应 / "我无法帮助" → 全量会全部 0 分，先修。
3. **评分器输出**——3 条全 `0` 或 `None` → 评分器配错，查返回值（§5）。

> 一条 100 题评测跑完才发现所有工具 403、响应全空，纯属浪费。dry-run 一分钟拦住。

### 3.5 全量执行 + 结果分析

```bash
uv run python scripts/run_evaluation_template.py --module your_agent --entry-point run_agent
# 大数据集（50+）建议放后台子 agent 跑，主会话轮询结果文件，不要阻塞
uv run python scripts/analyze_results.py evaluation_results.csv
```
`predict_fn` 签名必须匹配数据集输入键：`{"inputs": {"query": "..."}}` → `def wrapper(query):`，
不要把 `inputs` 整个当 dict 传进去（常见错误）。

## 4. 常见坑（踩坑表）

| 坑 | 现象 | 根因 | 对策 |
|----|------|------|------|
| 评分器返回值被静默转 None | 指标里某评分器整列消失、结果偏低 | LLM 裁判返回 `"pass"/"fail"` 被 `_cast_assessment_value_to_float` 转 None，无报错 | 一律让裁判返回 `"yes"/"no"` 或布尔/数值 |
| 工具 403 / 限流 | dry-run 空响应、全量全 0 | 凭证缺失或 GitHub API 限流 | dry-run 门禁拦截；先修 auth/工具配置 |
| 数据集未先发现 | 重复造轮子 | 跳了 `list_datasets` | 永远先 `list_datasets.py` |
| wrapper 签名错 | 评测直接报错 | `predict_fn(inputs)` 而非 `predict_fn(query=...)` | 按输入键定义参数 |
| 评判模型太慢 | 100 题估时几十分钟 | Opus 级裁判 ~45–90s/题 | 先告知时长；用 Sonnet 级裁判 + 并行 4–8x |
| gold label 缺失硬编 | 只覆盖有标签子集 | 没 gold 就退化成纯 LLM 裁判 | LLM-as-judge 配代码检查双轨 |

## 5. 交付检查清单

- [ ] `agent_description` 写清目的 + 2–3 个最该做对的点 + 已知失败模式
- [ ] 评分器套件已注册（`mlflow scorers list` 可见），每条标准实现选型合理
- [ ] 评分器返回值只用 `yes/no`/布尔/数值（无 `pass/fail`）
- [ ] 数据集已发现现有 / 已 sanity-5q 通过 / 放量 ≥50 条
- [ ] dry-run 3 条：工具被调用、响应非空、评分器非零
- [ ] 全量 `mlflow.genai.evaluate` 跑通，结果落 experiment
- [ ] `analyze_results.py` 产出通过率 + 失败模式 + 改进项
- [ ] 若做回归：新旧版本用**同一固定数据集**对比，结论可复现
