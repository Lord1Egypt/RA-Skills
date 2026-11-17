---
name: meta-evolver
version: 1.0.14
description: |
  递归自进化元引擎。在单技能学习器(skill-self-improve)之上，构建「全局能力感知 → 自定策略 →
  自找资源 → 自改自身 → 元反思」的循环，使技能生态持续自我增强、逼近并超越一线大模型能力。
  当希望让 agent 长期自主迭代、自动发现并填补能力缺口、自己制定进化路线时使用。
agent_created: true
visibility: public
---
# meta-evolver —— 递归自进化元引擎

目标：把"技能集合"升级为一个**会自己变强**的系统。每一轮迭代都让下一轮起点更高。

## 核心循环（六步）
1. **Sense（感知）**：聚合所有技能的 `learned_patterns.json`，形成全局能力图
   （成功率、是否有学习器），并扫描本地可用工具二进制（7z/unrar/ffmpeg…）。
2. **Plan（自定策略）**：对照「期望能力矩阵」检测缺口（缺能力 / 低成功率 / 无学习器），
   按权重打分，自选出本轮 Top3 聚焦项，写入 `strategy.md`。**策略由引擎自己定，不靠人工列清单。**
3. **Acquire（自找资源）**：缺口标 `needs_web` 的，由 agent 上下文做 WebSearch 检索最佳实践；
   本地已有工具/技能直接复用（如用 skill-self-improve 给新技能注入学习器）。
4. **Act（自改自身）**：构建新技能 / 修复低成功率技能 / 升级 learner / 改进 evolver 自身逻辑。
   只写 `skills/` 与自身 JSON 记忆，不碰系统文件。
5. **Verify（验证）**：用 `package_skill.py` 校验打包；关键脚本本地实跑验证。
6. **Record + Reflect（记忆与元反思）**：回写迭代动作；`reflect` 根据近期成败动态调权重
   （build 类更出活 → 提升 web_trend_weight / novelty_bias），形成自我调参。

## 运行方式
```bash
python scripts/evolver.py sense     # 刷新全局能力图
python scripts/evolver.py plan      # 自定本轮策略 -> strategy.md
python scripts/evolver.py reflect   # 元反思调权
python scripts/evolver.py status    # 查看状态
python scripts/evolver.py record --move "..." --effect "..." [--gap <id>] [--closed true] [--kind build]
```
状态持久化在 `evolver_patterns.json`，跨轮累积；`strategy.md` 是人类可读的当前进化路线。

## 与 skill-self-improve 的关系
- `skill-self-improve` 解决**单技能**的复盘迭代（learner.py）。
- `meta-evolver` 解决**全局**的能力增长与路线图制定，并调用前者给新技能装学习器。
- 二者构成「技能内闭环 + 生态级闭环」的双层自进化。

## 设计原则
- **递归自举**：evolver 用同一套「感知-计划-反思」来改进它自己（`self_patches` 记录）。
- **资源自律**：优先复用本地已探明的工具/技能，外部知识按需检索，不盲目堆依赖。
- **安全边界**：所有写操作限定在 `skills/` 与自身记忆文件，绝不动系统/个人文件。
- **可观测**：每轮策略与动作都落盘，evolution 轨迹可追溯、可审计。

## 自进化学习系统
本技能自身也遵循自进化：每次迭代后 `record`，`reflect` 调权重；若发现 evolver 逻辑短板
（如缺口检测噪声大、权重漂移），应直接改进 `evolver.py` 并记入 `self_patches`，实现元层面的越用越好用。
