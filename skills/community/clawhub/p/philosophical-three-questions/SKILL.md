---
name: philosophical-three-questions
description: "A structured decision framework for embodied navigation using Goal Tree, Current State Tree, and Future Tree analysis. Use when: making navigation decisions in Habitat-GS, planning multi-step actions, evaluating progress toward goals, or when stuck and needing to re-evaluate strategy. This is the core reasoning loop for the embodied agent."
metadata:
  version: "0.1.0"
  author: "zhangjinkai"
  tags: ["reasoning", "navigation", "planning", "embodied-ai"]
---

# 哲学三问 — 导航决策框架

每次在 Habitat-GS 环境中做决策前，执行"哲学三问"分析。这是龙虾在虚拟世界中进化的核心推理循环。

## 三棵树

### 🎯 目标树 (Goal Tree) — "我要去哪？"

分析并维护目标层次结构：

```
终极目标
├── 当前主目标（例：到达目标位置 [-3.62, -3.61, 3.18]）
│   ├── 子目标 1：离开当前房间
│   ├── 子目标 2：穿过走廊
│   └── 子目标 3：进入目标房间
└── 约束条件
    ├── 最大步数限制
    └── 避免碰撞
```

要回答的问题：
- 我的最终目标是什么？（目标位置 / EQA 问题 / 操控任务）
- 当前最紧迫的子目标是什么？
- 有没有子目标完成的先后顺序？

### 📍 现状树 (Current State Tree) — "我在哪？"

分析当前感知到的所有信息：

```
当前状态
├── 位置信息
│   ├── 坐标：[x, y, z]
│   ├── 朝向：quaternion → 面朝方向
│   └── 距目标距离：N 米
├── 视觉观测
│   ├── 前方场景描述（从 RGB 图像推断）
│   ├── 深度信息（最近/最远障碍物距离）
│   └── 关键物体/地标
├── 历史信息
│   ├── 已走步数
│   ├── 近几步的动作和结果
│   ├── 是否刚发生碰撞
│   └── 距离目标是在变近还是变远
└── 环境模型
    ├── 已探索区域的心智地图
    └── 未探索的方向
```

要回答的问题：
- 我的精确位置和朝向是什么？
- 我前方看到了什么？有障碍物吗？
- 和上一步比，我离目标更近了吗？
- 我已经探索了哪些方向？

### 🔮 未来树 (Future Tree) — "我该怎么做？"

评估每个可选动作的预期结果：

```
可选动作
├── move_forward
│   ├── 预期：前进 0.25m
│   ├── 风险：可能碰撞（如果前方深度很小）
│   └── 收益：如果面朝目标方向，距离减少
├── turn_left
│   ├── 预期：左转 10°
│   ├── 风险：可能偏离目标方向
│   └── 收益：可以看到新的区域，避开障碍物
├── turn_right
│   ├── 预期：右转 10°
│   ├── 风险：可能偏离目标方向
│   └── 收益：可以看到新的区域，避开障碍物
└── stop
    ├── 预期：结束 episode
    ├── 风险：如果未到达目标，任务失败
    └── 收益：如果已到达目标，任务成功
```

要回答的问题：
- 哪个动作最可能让我接近目标？
- 前方有障碍物吗？需要先转向吗？
- 我是否已经足够接近目标可以停下？
- 是否需要大幅改变方向？（连续转弯）

## 执行流程

每步决策时，按以下格式输出简要分析（不需要冗长，关键信息即可）：

```
[三问分析 - Step N]
目标：距目标 X.Xm，当前子目标是 XXX
现状：位置 [x,y,z]，朝向 XXX，上步 XXX 结果 XXX
决策：选择 XXX，因为 XXX
```

## 经验积累规则

### 写入 Memory 的时机

1. **Episode 结束时**：记录本次导航的总结
   - 成功/失败
   - 总步数 vs 最优步数
   - 关键决策点及其结果

2. **发现新模式时**：
   - 碰撞后的有效脱困策略
   - 特定场景的高效路径
   - 反复出现的错误决策

3. **跨 Episode 模式**：
   - 某类场景的通用策略
   - 值得提取为新 Skill 的经验

### 写入格式

记录到 `~/.openclaw/workspace/memory/YYYY-MM-DD.md`：

```markdown
## [NAV] Episode <id> in <scene_name>
- Result: success/fail (N steps, optimal: M steps)
- Key decisions: ...
- Lesson learned: ...
```

## 自我进化

当积累了足够多的导航经验后（5+ episodes），回顾 memory 文件，提取通用策略，更新到：
- 本 skill 文件中（添加新的决策启发式）
- 或创建新的专门 skill（如"走廊导航策略"、"大房间探索策略"）
