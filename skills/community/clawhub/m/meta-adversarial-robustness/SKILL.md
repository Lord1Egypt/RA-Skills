---
name: meta-adversarial-robustness
version: 1.0.0
description: |
  由 model-distillation 从教师技能 adversarial-robustness 蒸馏并增强的超越型元技能，
  在教师能力之上叠加自验证、自我反思、super-agent 编排与持续自进化闭环，逐步超越教师。
agent_created: true
visibility: public
---
# meta-adversarial-robustness（蒸馏超越型元技能）

> 由 `model-distillation` 从教师技能 **adversarial-robustness** 蒸馏并增强生成。
> 生成时间：2026-07-23 03:58:28 ｜ 蒸馏机制：跨模型蒸馏（见 meta-evolver 北极星策略）

## 来源能力签名（教师）
- 标题层级：adversarial-robustness（对抗鲁棒性）, 何时使用, 核心机制, 使用, 自进化学习系统, 已知限制, 自进化学习系统（越用越好用、越用越高效）, 记忆文件
- 显性工作流步骤（0 步）：
  （教师未显式编号工作流）

## 增强点（超越教师）
1. **可靠自验证**：每步产出后用 `reason-verify` 做命题一致性/事实锚定校验，reliability<0.8 即回退重做。
2. **自我反思闭环**：执行后写入 `self-reflection-loop`，沉淀失败模式到 learner。
3. **整合进 super-agent**：作为节点接入「感知→规划→执行→自验证→反思→记忆」超级智能体闭环，可被长程任务编排。
4. **对抗验证蒸馏质量**：对蒸馏出的关键决策规则做反例测试，防止只学到表面话术。
5. **持续自进化**：注入 learner，纳入 meta-evolver 的 sense/plan/record 闭环，跨会话越用越强。

## 教师 vs 学生 对比
| 维度 | 教师(adversarial-robustness) | 学生(meta-adversarial-robustness) |
| --- | --- | --- |
| 能力来源 | 原始 SKILL.md（2097 字符） | 蒸馏提取 + 元进化增强 |
| 工作流 | 0 步显性流程 | 同流程 + 自验证钩子 + 反思步 |
| 工具脚本 | learner.py, robustness.py | 继承 + reason-verify/self-reflection 钩子 |
| 失败防护 | 已识别 1 处 | 显式 limits + 对抗验证 |
| 自进化 | 视技能而定 | 强制注入 learner，纳入 meta-evolver 闭环 |
| 集成 | 单点 | 接入 super-agent 感知→规划→执行→自验证→反思→记忆闭环 |

## 使用
直接调用本技能完成「adversarial-robustness」领域的任务；本技能在教师能力之上叠加自验证与反思，输出更可靠、可追溯。

## 已知限制（来自教师蒸馏 + 元进化补充）
- - 默认扰动为词法级（不依赖语义模型），对深层语义对抗（释义改写）覆盖有限。
- 归一化加固仅覆盖"可逆无歧义"的形近对（o→0/e→3/a→4/s→5/b→8/t→7/z→2）；i/l↔1 因歧义不纳入，仍可能致翻。
- 鲁棒性评分依赖 `predict` 的可复现性；随机扰动用固定种子保证可重跑。
- 不替代领域安全审核，仅做"输入抗扰动"的初筛与加固提示。

## 自进化学习系统（越用越好用、越用越高效）

本技能内置通用学习模块 `scripts/learner.py`。每次评估后自动复盘、积累经验。

### 记忆文件
`learned_patterns.json` 记录：操作总数、各扰动类型命中率、成功翻转记录、用户偏好、改进建议。

### 使用后请调用（Bash）

```bash
# 记录一次评估（--capability 填本次主扰动族，如「char_swap」「confusable」）
python scripts/learner.py record <本技能目录> --capability char_swap
# 记录一次成功翻转（说明某决策被攻破）
python scripts/learner.py record <本技能目录> --capability char_swap --fail --error 决策翻转 --note "allow->all0w 击穿"
# 记录用户偏好（下次直接采用）
python scripts/learner.py prefer <本技能目录> --key 加固策略 --val 归一化去形近
# 查看累计洞察（高频致翻扰动族 / 反复失败）
python scripts/learner.py insight <本技能目录>
# 自动复盘（错误≥3次 或 操作≥10次 时给出改进建议）
python scripts/learner.py reflect <本技能目录>
```

### 迭代规则
- **成功翻转累计 ≥3 次** → 主动扩展归一化映射或建议业务侧加预处理，并回写本 SKILL.md。
- **操作数 ≥10 次** → 分析高频致翻扰动族优先打磨检测，低频评估精简。
- **重要用户偏好** → 写入 `learned_patterns.json`，下次调用直接采用。

> 越用越懂你：第一次评估是通用探针，第十次已沉淀为你专属的"抗欺骗加固清单"。
- 蒸馏不保证覆盖教师全部隐式知识，首次使用需对照教师原技能核验关键决策。
