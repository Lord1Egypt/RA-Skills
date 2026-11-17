---
name: structured-decision-block
description: "通用结构化决策模块：接收上游分析产出的结构化 findings payload，应用业务上下文（风险偏好、权重、硬约束），输出标准化的决策块（verdict + 维度表 + 反证条件 + 优先级动作）。可被任何分析型 skill 在最后阶段调用，实现决策模板化。"
---

# Structured Decision Block

通用决策合成模块。任何上游分析 agent（Amazon niche-radar、product-selection、monopoly 等，或其他平台）在完成多维挖掘后，组装 payload 调用本模块，即可得到一致的、带反证条件的结构化决策输出。

## 核心原则
- 上游负责**厚挖掘**（维度、证据、potential_reversals）
- 本模块负责**合成判决**（打分、verdict、反证、动作）
- 同一份 findings + 不同 business_context 可得到不同判决
- 输出必须同时包含人类可读报告片段和机器可解析 JSON

## 输入
必须符合 `references/structured-decision-block-input-schema.json`（v0.2）。

推荐使用 `scripts/decision_block.py --payload <json>`

## 输出
- Markdown 片段（可直接注入 report-generator）
- 结构化 JSON（含 verdict、dimensions、counter_evidence、actions 等）

## 使用方式

### 命令行调用
```bash
python scripts/decision_block.py \
  --payload /path/to/findings.json \
  --output decision_block.md \
  --json-out decision_block.json \
  --scenario niche-analysis
```

### 在其他 skill 中集成
1. 上游分析完成后构建 payload（参考 amazon-niche-radar 集成示例）
2. 调用本脚本或直接 import DecisionBlockEngine
3. 将返回的 decision_block 内容塞入最终报告的最后章节

### Python 直接调用（推荐在复杂 pipeline 中）
```python
from scripts.decision_block import DecisionBlockEngine

engine = DecisionBlockEngine()
result = engine.process(payload_dict)
# result['markdown'], result['json'], result['verdict']
```

## 默认权重（scenario 级）
- niche-analysis: profitability 25, market_potential 20, competition 18, entry_barrier 15, trend_momentum 12, risk 10
- product-selection: 类似，可在 business_context 中覆盖

## 判决逻辑（当前版本）
1. 合并 business_context.weights（如果提供）
2. 对每个 dimension 计算/调整 score（0-10）
3. 加权总分 + 硬约束检查 → 初始 verdict（🟢 / 🟡 / 🔴）
4. 结合 risk_preference 微调
5. 从 potential_reversals + aggregates + key_risks 生成反证条件
6. 根据 verdict + 强维度 生成优先级动作

## QA 要求（用于工厂质检）
- 必须输出明确 verdict
- 必须包含至少 3 条结构化反证条件
- 必须有带优先级的 actions
- 所有数字需可追溯到 input 中的 evidence source

## 版本
- v0.1: 初始实现（规则引擎为主 + 简单 LLM 增强可选）
- 未来: 支持更多 scenario 模板、用户画像映射

参考：
- `references/input-schema.json`
- `references/output-example.md`
- `scripts/decision_block.py` (实现)