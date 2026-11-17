---
name: open-ended-curriculum
version: 1.0.0
description: |
  开放世界无限课程：让智能体自己造越来越难、且彼此不重复的挑战，把能力边界无限推开——课程永不饱和。
  这是决定"能否持续超越"的元能力：一线大模型等人工喂题、题做完了就停，本技能让 agent 自主生成递增强度课程。
  当用户要求永不饱和的课程、自主造题、能力边界无限推开、开放世界自训练时使用。
agent_created: true
visibility: public
---

# open-ended-curriculum —— 开放世界无限课程

目标：把"等人工喂题"升级为"agent 自己造越来越难、且彼此不重复的挑战"，
让能力边界被无限推开——**课程永不饱和**。

## 为什么需要

- 一线大模型：**等人工喂题**，题做完了就停，能力封顶。
- 本技能：**自己造题**，且难度递增、彼此新颖，越迭代越难 → 持续逼近能力上界。

## 闭环（scripts/curriculum.py，真实可跑）

`generate_curriculum(seed, steps)`：

1. **难度递增器**：每升一关，scope 与约束数都加一档（LEVEL_TEMPLATES 循环复用并叠加），
   难度 `difficulty = level + 1` 严格递增 → 课程无上界。
2. **新颖性闸门**：`novelty = 1 - max(char_jaccard(新, 历史))`，
   近重复（jaccard 高）即拒收 → 强制每关彼此不重复。
3. **四维打分**（权重同 open-ended-goal-discovery：价值0.35 / 新颖0.30 / 可行0.25 / 对齐0.10）：
   - 价值随关卡单调上升（`0.6 + 0.035*level`，封顶0.95）
   - 可行：含可验证动作词即高
   - 对齐：始终围绕种子主题，不跑题
4. 返回 `challenges[]`（每关含 level/文本/四维分/难度）+ `saturated=False`。

## 用法

```bash
python scripts/curriculum.py --selftest
python scripts/curriculum.py --seed "实现一个排序函数" --steps 10
```

## 输出

`generate_curriculum` 返回：`seed` / `steps` / `challenges[]` / `saturated`（恒 False）/ `max_difficulty`。

## 设计要点

- **真能跑**：`curriculum.py --selftest` 真实产出 10 关，断言：
  产出数=steps（可任意增大，**永不饱和**）、难度严格递增、每关 novelty≥0.25（无近重复）、
  四维分全健康、价值质量非递减。
- **不空转**：难度是硬递增逻辑（level+1），不是话术；新颖性是硬闸门（jaccard 拒收）。
- **可被度量**：四维分与难度均可量化，使"课程是否在持续变难"可观测。

## 自进化学习系统

本技能自身也遵循自进化：每次使用 `record` 回写成败、用户偏好，并据错误模式自动复盘改进。
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
