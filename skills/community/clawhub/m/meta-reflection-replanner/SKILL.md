---
name: meta-reflection-replanner
version: 1.0.0
description: |
  由 model-distillation 从教师技能 reflection-replanner 蒸馏并增强的超越型元技能，
  在教师能力之上叠加自验证、自我反思、super-agent 编排与持续自进化闭环，逐步超越教师。
agent_created: true
visibility: public
---
# meta-reflection-replanner（蒸馏超越型元技能）

> 由 `model-distillation` 从教师技能 **reflection-replanner** 蒸馏并增强生成。
> 生成时间：2026-07-23 06:17:10 ｜ 蒸馏机制：跨模型蒸馏（见 meta-evolver 北极星策略）

## 来源能力签名（教师）
- 标题层级：reflection-replanner（反思驱动重规划）, 何时使用, 工作流, 脚本, 自验证, 与四引擎闭环的关系, 已知限制, 自进化学习系统（越用越好用、越用越高效）
- 显性工作流步骤（5 步）：
  1. **收集信号**：拿到原 plan、执行 trace（每步 ok/fail）、verify 结果（passed + issues）。
  2. **反思分类**：`FailureClassifier` 把失败根因归为 missing_step / wrong_assumption / tool_failure / data_issue / verification_gap。
  3. **重规划**：在失败点之前插入针对性补救步骤，并一律在末尾追加「最终验证门」。
  4. **闭环**：修订后的计划交回执行器重跑；仍失败则再次反思（反思驱动重规划可迭代）。
  5. **通过即停**：verify.passed 为真时原样返回，不噪声式改动。

## 增强点（超越教师）
1. **可靠自验证**：每步产出后用 `reason-verify` 做命题一致性/事实锚定校验，reliability<0.8 即回退重做。
2. **自我反思闭环**：执行后写入 `self-reflection-loop`，沉淀失败模式到 learner。
3. **整合进 super-agent**：作为节点接入「感知→规划→执行→自验证→反思→记忆」超级智能体闭环，可被长程任务编排。
4. **对抗验证蒸馏质量**：对蒸馏出的关键决策规则做反例测试，防止只学到表面话术。
5. **持续自进化**：注入 learner，纳入 meta-evolver 的 sense/plan/record 闭环，跨会话越用越强。

## 教师 vs 学生 对比
| 维度 | 教师(reflection-replanner) | 学生(meta-reflection-replanner) |
| --- | --- | --- |
| 能力来源 | 原始 SKILL.md（2232 字符） | 蒸馏提取 + 元进化增强 |
| 工作流 | 5 步显性流程 | 同流程 + 自验证钩子 + 反思步 |
| 工具脚本 | learner.py, replanner.py | 继承 + reason-verify/self-reflection 钩子 |
| 失败防护 | 已识别 1 处 | 显式 limits + 对抗验证 |
| 自进化 | 视技能而定 | 强制注入 learner，纳入 meta-evolver 闭环 |
| 集成 | 单点 | 接入 super-agent 感知→规划→执行→自验证→反思→记忆闭环 |

## 使用
直接调用本技能完成「reflection-replanner」领域的任务；本技能在教师能力之上叠加自验证与反思，输出更可靠、可追溯。

## 已知限制（来自教师蒸馏 + 元进化补充）
- ## 已知限制
- 根因分类基于关键词启发式，复杂失败需结合 LLM 语义判断增强。
- 当前只修订步骤列表，不修改单步内部实现细节。

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
- 蒸馏不保证覆盖教师全部隐式知识，首次使用需对照教师原技能核验关键决策。
