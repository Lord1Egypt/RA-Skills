---
name: meta-autonomous-research-scale
version: 1.0.0
description: |
  由 model-distillation 从教师技能 autonomous-research-scale 蒸馏并增强的超越型元技能，
  在教师能力之上叠加自验证、自我反思、super-agent 编排与持续自进化闭环，逐步超越教师。
agent_created: true
visibility: public
---
# meta-autonomous-research-scale（蒸馏超越型元技能）

> 由 `model-distillation` 从教师技能 **autonomous-research-scale** 蒸馏并增强生成。
> 生成时间：2026-07-23 08:23:15 ｜ 蒸馏机制：跨模型蒸馏（见 meta-evolver 北极星策略）

## 来源能力签名（教师）
- 标题层级：autonomous-research-scale（自主科研规模化）, 何时使用, 工作流, 用法, 集成（超越单次研究）, 已知限制, 自进化学习系统（越用越好用、越用越高效）, 记忆文件
- 显性工作流步骤（4 步）：
  1. **分解（decompose）**：把研究主题拆成 N 条并行假设线程（子问题 + 候选假设）。
  2. **派发（dispatch）**：每条线程交给可插拔 researcher（默认确定性 mock；真实部署可换检索/工具链/文献 API）。
  3. **聚合（aggregate）**：识别收敛（≥2 线程支持同 claim）、冲突（不支持）、不确定（低置信），算总体置信。
  4. **元综合（meta-synthesis）**：给出主结论 + 总体置信 + 知识增量，并落盘跨战役知识库。

## 增强点（超越教师）
1. **可靠自验证**：每步产出后用 `reason-verify` 做命题一致性/事实锚定校验，reliability<0.8 即回退重做。
2. **自我反思闭环**：执行后写入 `self-reflection-loop`，沉淀失败模式到 learner。
3. **整合进 super-agent**：作为节点接入「感知→规划→执行→自验证→反思→记忆」超级智能体闭环，可被长程任务编排。
4. **对抗验证蒸馏质量**：对蒸馏出的关键决策规则做反例测试，防止只学到表面话术。
5. **持续自进化**：注入 learner，纳入 meta-evolver 的 sense/plan/record 闭环，跨会话越用越强。

## 教师 vs 学生 对比
| 维度 | 教师(autonomous-research-scale) | 学生(meta-autonomous-research-scale) |
| --- | --- | --- |
| 能力来源 | 原始 SKILL.md（2086 字符） | 蒸馏提取 + 元进化增强 |
| 工作流 | 4 步显性流程 | 同流程 + 自验证钩子 + 反思步 |
| 工具脚本 | campaign.py, learner.py | 继承 + reason-verify/self-reflection 钩子 |
| 失败防护 | 已识别 1 处 | 显式 limits + 对抗验证 |
| 自进化 | 视技能而定 | 强制注入 learner，纳入 meta-evolver 闭环 |
| 集成 | 单点 | 接入 super-agent 感知→规划→执行→自验证→反思→记忆闭环 |

## 使用
直接调用本技能完成「autonomous-research-scale」领域的任务；本技能在教师能力之上叠加自验证与反思，输出更可靠、可追溯。

## 已知限制（来自教师蒸馏 + 元进化补充）
- - 默认 researcher 为确定性 mock，仅供本地实跑与管线验证；真实科研需替换 researcher 接入检索/工具。
- 总体置信为启发式（支持面 × 平均置信 × 冲突折扣），非严格贝叶斯；高 stakes 结论须人工核验。
- 收敛识别基于 claim 文本完全匹配，语义近似但表述不同的收敛会被漏判。
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
- 蒸馏不保证覆盖教师全部隐式知识，首次使用需对照教师原技能核验关键决策。
