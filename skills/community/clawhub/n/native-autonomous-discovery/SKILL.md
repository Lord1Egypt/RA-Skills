---
name: native-autonomous-discovery
version: 1.0.0
description: |
  原生自主发现：超越"被动接任务问答"，对开放问题自主完成"假设->设计判别性实验->评估证据->收敛"
  的科研闭环。给定搜索空间与观测器，自动生成候选假设、用观测器打分、按证据累加择优、对低证据
  假设再生或剪枝，直到收敛到高置信结论。纯标准库、零依赖、可本地实跑(--selftest 自带样例)。
agent_created: true
visibility: public
---

# native-autonomous-discovery（原生自主发现）

> 蒸馏工程化与可信代理域的高价值空白之一，也是一线大模型仍薄弱的"主动科研"能力：
> 不是回答已知，而是**发现未知**——自主提出并验证假设，逼近真因。

## 何时用
- 开放性问题没有标准答案（"哪个参数组合最优""根因可能是哪几个"）。
- 需要 agent 自主探索而非依赖用户一步步喂指令。
- 与 `hypothesis-driven-inquiry`（溯因）互补：本技能偏"主动生成-实验-收敛"的闭环控制。

## 核心循环
1. **生成假设**：从搜索空间抽样/枚举候选（支持约束与多样性）。
2. **实验设计**：为待验假设选判别性观测（最小化歧义，最大化信息增益）。
3. **评估证据**：用观测器 `observe(hypothesis) -> score∈[0,1]` 打分。
4. **收敛判定**：证据累加达阈值→收敛；长期低证据→再生/剪枝。
5. **输出**：Top 假设 + 证据轨迹 + 置信度。

## 用法
```bash
python scripts/discover.py --selftest
# 或对接真实观测器：
python scripts/discover.py --space space.json --observe my_observer.py
```

## 输出
```json
{
  "best": "候选H",
  "confidence": 0.93,
  "rounds": 7,
  "trajectory": [{"hyp": "候选H", "score": 0.91}, ...],
  "converged": true
}
```

## 与其他能力关系
- ← `hypothesis-driven-inquiry`：提供溯因假设；本技能负责"实验-收敛"控制层。
- → `open-ended-goal-discovery`：目标发现后，本技能执行发现过程。
- → `active-curiosity`：探索顺序可由新颖性/信息增益驱动。

## 已知限制
- 收敛质量完全取决于观测器真实性；观测器有偏，结论就有偏（建议配蒸馏质量对抗验证）。
- 大搜索空间需配采样预算，否则可能未收敛就耗尽轮次（返回 best-effort + 置信度标注）。

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
