---
name: steam-launch
description: Steam 游戏发行：商店页审查、愿望单诊断、Demo 就绪、Next Fest 规划、发行清单
source:
  type: derived
  repo: skills-repo/indie-game-developer
  path: skills/steam-launch/SKILL.md
  version: 1.0.0
  updated: 2026-07-26
  url: https://skills.sh/akillness/oh-my-skills/steam-store-launch-ops
metadata:
  category: 游戏发行
  platform: Steam
  difficulty: 进阶
---

# Steam 游戏发行

> Steam 商店发行操作：页面对赌审计、愿望单诊断、Demo 就绪检查、Next Fest 规划、发行清单。

## 能力

- **商店页审计**：胶囊图、截图、预告片、短描述、标签优化
- **愿望单诊断**：流量与转化分离分析，定位愿望单增长瓶颈
- **Demo 就绪检查**：Demo 质量评估，判断公开暴露风险
- **Next Fest 规划**：活动时间线、准备清单、预期管理
- **发行 Runbook**：从 Coming Soon 到正式上线的操作清单

## 使用方式

```
/steam-launch 审查我的 Steam 商店页
/steam-launch 诊断为什么愿望单增长缓慢
/steam-launch 帮我评估 Demo 是否准备好公开
```

## 工作流

1. 分类 Steam 需求到对应数据包
2. 对商店页进行逐项审查
3. 分离流量、转化、信任度、时机问题
4. 输出一次性检查清单
5. 路由非 Steam 问题到对应技能

## 适用场景

- 独立游戏 Steam 发行准备
- 商店页优化
- 愿望单策略
- Demo/Next Fest 规划

## 限制

- 仅覆盖 Steam 平台，不涉及 Epic/Itch.io/主机
- 不涉及社区管理和公关
- 不涉及游戏内容开发

> 本子技能属**Steam 发行执行层**（商店页审计 / 愿望单 / Demo / Next Fest）；方法层见 reference。

- 发行方法论（时间线 / 愿望单漏斗 / 定价 / Next Fest）→ [`references/steam-launch-playbook.md`](../../references/steam-launch-playbook.md)
- 选型与 Web → Steam 发布路径 → [`references/decision-engine-tech.md`](../../references/decision-engine-tech.md) §8