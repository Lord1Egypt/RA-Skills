---
name: interpretable-attribution
version: 1.0.0
description: |
  可解释归因引擎（model-agnostic）。针对任意模型/规则在单个样本上的预测，给出
  "为什么"：全局排列重要性、局部特征消融、最少特征反事实翻转、自然语言决策理由。
  超越黑箱输出，给出特征级归因，是"s可解释归因"前沿认知能力的实体化落地。
agent_created: true
visibility: public
---

# interpretable-attribution（可解释归因）

> 北极星能力域「前沿认知(下一梯队)·可解释归因」实体化。一线大模型常给出黑箱预测，
> 本技能补上"决策依据与特征归因"，使输出可追溯、可辩护。

## 何时使用
- 需要解释某个分类/回归预测"为什么是这个结果"。
- 需要向人说明模型决策的驱动因素（合规/调试/信任）。
- 需要"如果改了 X，预测会不会变"的反事实追问。

## 工作流
1. **数据/模型接入**：数据集(json list of dicts，含 label 字段) + 预测函数 `predict(r)->val`(py 文件定义)。
2. **全局重要性**：permutation importance —— 打乱某特征，看整体评分下降幅度，排序得全局归因。
3. **局部重要性**：local ablation —— 把待测样本某特征置为基值，看该样本预测变化。
4. **反事实**：counterfactual —— 贪心选"置为极值/离散候选后预测最接近目标"的特征翻转，得最少改动集。
5. **自然语言归因**：top-k 特征 -> 可读决策理由；边界附近样本给出"预测稳健"说明。
6. **可靠自验证**：脚本内置 `--selftest` 实测断言（首要特征=真因、反事实可翻转），reliability<0.8 即回退重做。

## 运行
```bash
# 内置自检（无外部依赖）
python scripts/attributor.py --selftest
# 实际归因
python scripts/attributor.py --data d.json --predict p.py --instance i.json --label label
```

## 增强点（融入元进化闭环）
- 自验证：selftest 断言首要特征与反事实翻转，防表面话术。
- 自进化：已注入 learner，纳入 meta-evolver 的 sense/plan/record 闭环。

## 已知限制
- 排列重要性依赖样本量，小样本方差大（建议 n_perm>=20）。
- 反事实为贪心近似，未必是全局最小改动集（NP 难）。
- 仅支持单样本、扁平特征；嵌套结构需先扁平化。
