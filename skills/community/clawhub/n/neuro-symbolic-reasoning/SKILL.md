---
name: neuro-symbolic-reasoning
description: 神经符号统一推理——把"神经(连续表征+相似度=可泛化但不可验证)"与"符号(Horn子句前向链+不变量=可证但脆弱)"熔于一炉。同一查询同时走两侧：符号可证结论优先(verifiable=True)，神经近邻结论作为带置信度的软证据，两侧冲突显式标注供上层裁决。适用于需要"既能泛化到未见样本、又能给出可审计/可反例证伪推导"的推理场景（关系推理、知识补全、可信问答、反幻觉）。
metadata:
  agent_created: true
  version: 1.0.0
  domain: 涌现超智能与自主科学发现(元之三阶)
  capability: 神经符号统一推理
---

# neuro-symbolic-reasoning · 神经符号统一推理

> 元之三阶能力：一线大模型是"纯神经"——能泛化但会幻觉、无法证明；纯符号系统精确
> 但脆弱、不泛化。本技能**同时拥有可泛化(神经)与可验证(符号)两种推理**，并用统一层
> 择优，兼得两者之长——这是当前主流大模型架构性缺失的能力。

## 何时使用
- 既要对未见样本泛化推断，又要对关键结论给出**可机器验证/可审计**的推导链。
- 反幻觉：让"可证的符号结论"覆盖"貌似合理的神经猜测"。
- 关系推理 / 知识补全 / 规则约束下的语义检索。

## 核心机制
1. **神经侧 Neural**：连续向量 + 余弦相似度做最近邻泛化，输出 `label + confidence`。
2. **符号侧 Symbolic**：Horn 子句前向链（多原子变量 join 合一，跑到不动点），
   结论可 `entails()` 精确判定、可反例证伪。
3. **统一层 Unify**：符号可证 → `decision=symbolic, verifiable=True, confidence=1.0`
   并附神经软证据；符号不可证 → 回落神经泛化；两侧都无 → `unknown`。冲突显式标 `conflict`。

## 用法
```bash
python scripts/neuro_symbolic.py --selftest   # 4 场景：神经泛化/符号前向链/统一择优/回落，全 PASS
python scripts/neuro_symbolic.py --demo
```

编程调用：
```python
from neuro_symbolic import Neural, Symbolic, query
nn = Neural(); nn.add("cat", [1,0.1,0]); nn.add("dog", [0.1,1,0])
sy = Symbolic()
sy.add_fact("父", ("a","b")); sy.add_fact("父", ("b","c"))
sy.add_rule("祖父", ["?x","?z"], [("父",["?x","?y"]),("父",["?y","?z"])])
sy.forward()
q = query(nn, sy, [0.9,0.2,0], lambda: sy.entails("祖父", ("a","c")))
# -> {'decision':'symbolic','verifiable':True,'confidence':1.0,'neural_hint':{...}}
```

## 边界
- 符号侧当前支持 Horn 子句 + `?var` 变量合一（够做关系/传递推理）；否定/函数项需扩展。
- 神经侧向量由外部编码器提供；此处用可验证手工向量演示，接入真实 embedding 即可泛化。

---

## 自进化学习系统（越用越好用、越用越高效）

本技能内置通用学习模块 `scripts/learner.py`。每次使用后自动复盘、积累经验，逐步提升输出质量与执行效率，无需人工维护。

### 记忆文件
`learned_patterns.json`（位于本技能目录）记录：操作总数、各能力使用频次、错误模式、用户偏好、改进建议。

### 使用后请调用（Bash）

```bash
# 记录一次成功使用（--capability 填本次主要能力名，如「简历优化」「比价」）
python scripts/learner.py record <本技能目录> --capability 简历优化
# 记录一次失败/异常
python scripts/learner.py record <本技能目录> --capability 简历优化 --fail --error 格式识别失败 --note "用户上传了非标准文件"
# 记录用户偏好（下次直接使用）
python scripts/learner.py prefer <本技能目录> --key 输出语言 --val 中文
# 查看累计洞察（高频能力 / 反复错误）
python scripts/learner.py insight <本技能目录>
# 自动复盘（错误≥3次 或 操作≥10次 时给出改进建议）
python scripts/learner.py reflect <本技能目录>
```

### 迭代规则
- **错误累计 ≥3 次** → 主动增加预检/兜底步骤，并将经验回写本 SKILL.md。
- **操作数 ≥10 次** → 分析高频能力优先打磨示例与质量，低频能力评估精简或合并。
- **重要用户偏好** → 写入 `learned_patterns.json`，下次调用直接采用，减少重复询问。

> 越用越懂你：第一次用是通用能力，第十次用已沉淀为你专属的最佳实践。
