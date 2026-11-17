---
name: meta-constitutional-self-alignment
version: 1.0.0
description: |
  由 model-distillation 从教师技能 constitutional-self-alignment 蒸馏并增强的超越型元技能，
  在教师能力之上叠加自验证、自我反思、super-agent 编排与持续自进化闭环，逐步超越教师。
agent_created: true
visibility: public
---
# meta-constitutional-self-alignment（蒸馏超越型元技能）

> 由 `model-distillation` 从教师技能 **constitutional-self-alignment** 蒸馏并增强生成。
> 生成时间：2026-07-23 21:29:49 ｜ 蒸馏机制：跨模型蒸馏（见 meta-evolver 北极星策略）

## 来源能力签名（教师）
- 标题层级：constitutional-self-alignment —— 宪法式自我对齐, 何时使用, 宪法结构, 工作流（critique → revise 闭环）, 命令, 判定规则, 安全边界, 与 meta-evolver / super-agent 的协同
- 显性工作流步骤（4 步）：
  1. **critique**：逐条原则检查文本——`forbid_patterns` 命中即违宪；`require_patterns` 在
  2. **revise**：按严重级顺序自动修订——forbid 命中片段删除或替换为 `replace_with`；
  3. **loop**：修订后重新 critique，直到 0 违宪或达 `max_iters`（默认 5）。
  4. **audit**：输出对齐分 `alignment=1-加权违宪率`、每轮修订动作、最终判决 ALIGNED/UNALIGNED。

## 增强点（超越教师）
1. **可靠自验证**：每步产出后用 `reason-verify` 做命题一致性/事实锚定校验，reliability<0.8 即回退重做。
2. **自我反思闭环**：执行后写入 `self-reflection-loop`，沉淀失败模式到 learner。
3. **整合进 super-agent**：作为节点接入「感知→规划→执行→自验证→反思→记忆」超级智能体闭环，可被长程任务编排。
4. **对抗验证蒸馏质量**：对蒸馏出的关键决策规则做反例测试，防止只学到表面话术。
5. **持续自进化**：注入 learner，纳入 meta-evolver 的 sense/plan/record 闭环，跨会话越用越强。

## 教师 vs 学生 对比
| 维度 | 教师(constitutional-self-alignment) | 学生(meta-constitutional-self-alignment) |
| --- | --- | --- |
| 能力来源 | 原始 SKILL.md（2716 字符） | 蒸馏提取 + 元进化增强 |
| 工作流 | 4 步显性流程 | 同流程 + 自验证钩子 + 反思步 |
| 工具脚本 | align.py, learner.py | 继承 + reason-verify/self-reflection 钩子 |
| 失败防护 | 已识别 1 处 | 显式 limits + 对抗验证 |
| 自进化 | 视技能而定 | 强制注入 learner，纳入 meta-evolver 闭环 |
| 集成 | 单点 | 接入 super-agent 感知→规划→执行→自验证→反思→记忆闭环 |

## 使用
直接调用本技能完成「constitutional-self-alignment」领域的任务；本技能在教师能力之上叠加自验证与反思，输出更可靠、可追溯。

## 已知限制（来自教师蒸馏 + 元进化补充）
- "trigger_patterns": ["投资", "收益"]}
]}
```

## 工作流（critique → revise 闭环）
1. **critique**：逐条原则检查文本——`forbid_patterns` 命中即违宪；`require_patterns` 在
   `trigger_patterns` 命中时缺失即违宪。violations 按 severity（critical>major>minor）排序。
2. **revise**：按严重级顺序自动修订——forbid 命中片段删除或替换为 `replace_with`；
   require 缺失则在文末插入 `require_insert`。
3. **loop**：修订后重新 critique，直到 0 违宪或达 `max_iters`（默认 5）。
4. **audit**：输出对齐分 `alignment=1-加权违宪率`、每轮修订动作、最终判决 ALIGNED/UNALIGNED。

## 命令
```bash
python scripts/align.py check --constitution C.json --text T.txt
python scripts/align.py selftest   # 全链路自测
```

## 判定规则
- 任一 critical 违宪未修复 → 最终判决 UNALIGNED，禁止交付。
- alignment ≥ 0.99 且 0 违宪 → ALIGNED 可交付。
- 修订轮数触顶仍有违宪 → 升级人工审核（对接 human-in-loop-review）。

## 安全边界
- 只读宪法/文本，仅输出修订后文本与审计轨迹；不修改宪法本身（宪法修订需人工确认）。
- 自动修订只做**保守替换/删除/插入**，不生成新的实质性主张。

## 与 meta-evolver / super-agent 的协同
- 作为「认知架构元整合(元之元·二阶)」域实体化技能 #5：与 value-alignment（价值评估）、
  safety-guardrails（行为门控）、redteam-selfattack（对抗测试）构成"评估-门控-对抗-自修"对齐纵深。
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
