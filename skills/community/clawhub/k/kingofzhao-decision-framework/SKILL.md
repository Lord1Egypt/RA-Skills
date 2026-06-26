---
name: kingofzhao-decision-framework
version: 1.0.0
author: KingOfZhao
description: 决策框架 Skill —— 已知/未知驱动的结构化决策系统，置信度加权+红线拦截+决策记忆
tags: [cognition, decision-making, framework, risk-analysis, confidence, trade-offs]
license: MIT
homepage: https://github.com/KingOfZhao/AGI_PROJECT
---

# Decision Framework Skill

## 元数据

| 字段 | 值 |
|------|-----|
| 名称 | decision-framework |
| 版本 | 1.0.0 |
| 作者 | KingOfZhao |
| 发布日期 | 2026-03-31 |
| 置信度 | 96% |

## 来源碰撞
```
self-evolution-cognition (已知/未知分离)
        ⊗
entrepreneur-cognition (商业决策)
        ⊗
ai-growth-engine (度量化)
        ↓
decision-framework (通用决策系统)
```

## 核心哲学

> 好决策 ≠ 好结果。好决策 = 在已知信息下，用结构化方法选择期望值最高的选项。
> 结果可能受运气影响，但决策过程可以优化。

## 四步决策法（KUWR）

```
K — Known 已知:    列出所有已知事实，标注置信度
U — Unknown 未知:  列出所有未知项，评估影响和获取成本
W — Weigh 权衡:    对每个选项做已知/未知加权评分
R — Record 记录:   记录决策+理由+预期结果，事后对比
```

## 决策评分公式

```
Option Score = (Known_Benefit × confidence) - (Known_Cost × confidence) 
               + (Unknown_Upside × probability × 0.5) 
               - (Unknown_Downside × probability × 1.5)

注意: 未知下行风险权重(1.5) > 未知上行收益权重(0.5)
→ 这是"不对称风险偏好": 优先避免灾难性错误
```

## 红线拦截

```
决策前自动检查红线:
  🔴 此决策是否触碰职业红线？→ 如果是，自动拦截
  🔴 此决策是否不可逆？→ 如果是，强制等待24h冷静期
  🔴 此决策是否影响他人？→ 如果是，强制咨询受影响方
  🔴 已知信息置信度是否 <50%？→ 如果是，建议先补充信息
```

## 决策记忆

```
decisions/{date}_{id}.md
  - 问题描述
  - 已知/未知列表
  - 各选项评分
  - 最终选择 + 理由
  - 预期结果
  - [事后] 实际结果 + 偏差分析
  - [事后] 教训（更新决策参数）
```

## 安装命令
```bash
clawhub install decision-framework
```

## 调用方式
```python
from skills.decision_framework import DecisionFramework

df = DecisionFramework(workspace=".")

result = df.decide(
    problem="是否应该切换到新的技术栈？",
    options=["保持现状", "渐进迁移", "完全重写"],
    known=["当前技术栈稳定运行2年", "新栈性能提升40%", "团队3人熟悉新栈"],
    unknown=["迁移周期", "业务中断风险", "学习曲线"],
    redlines=["不中断生产服务"]
)
print(result.rankings)       # 选项排名 + 评分
print(result.redline_check)  # 红线检查结果
print(result.recommendation) # 建议选择 + 理由
```

## 学术参考
1. [A Survey of Self-Evolving Agents](https://arxiv.org/abs/2507.21046) — 决策自进化
2. [SAGE: Multi-Agent Self-Evolution](https://arxiv.org/abs/2603.15255) — 多Agent决策
3. [Memory in the Age of AI Agents](https://arxiv.org/abs/2512.13564) — 决策记忆
