---
name: game-designer
description: 游戏视觉设计与打磨：调色板、粒子特效、动效、UI 评审、游戏手感
source:
  type: derived
  repo: skills-repo/indie-game-developer
  path: skills/game-designer/SKILL.md
  version: 1.0.0
  updated: 2026-07-26
  url: https://skills.sh/opusgamelabs/game-creator/design-game
metadata:
  category: 游戏设计
  platform: Web
  difficulty: 入门
---

# 游戏设计师

> 游戏视觉设计与打磨：对已有游戏进行 UI/UX 审计和视觉升级，提升游戏品质感。

## 能力

- **视觉审计**：背景氛围、色彩调色板、动画补间、粒子特效
- **屏幕过渡**：场景切换动效、渐入渐出、转场效果
- **游戏手感**：屏幕震动、缩放弹跳、打击反馈
- **UI 设计**：排版、按钮状态、游戏结束界面
- **设计系统**：基于 Constants 的样式统一管理

## 使用方式

```
/game-designer 让这个游戏看起来更精致
/game-designer 审查这个游戏的视觉效果并打分
/game-designer 为这个游戏添加粒子爆炸特效
```

## 工作流

1. 读取游戏引擎和当前配置
2. 逐项审计视觉和交互（背景/色彩/动画/粒子/UI/手感）
3. 输出设计报告和评分
4. 实施优先改进项
5. 验证构建无误

## 适用场景

- 游戏视觉升级
- 游戏发布前打磨
- 独立游戏品质提升
- 快速原型美化

## 限制

- 不改变游戏逻辑（物理/得分/控制）
- 不涉及 3D 模型设计
- 不涉及音频设计

> 本子技能属**视觉打磨执行层**（调色板 / 粒子 / 动效 / UI / 手感）；方法层见 reference。

- 游戏视觉 / 手感 QA 基线 → [`references/game-qa-perf.md`](../../references/game-qa-perf.md)
- 选型时的视觉与 2D/3D 维度 → [`references/decision-engine-tech.md`](../../references/decision-engine-tech.md)
- 像素精灵与 sprite sheet 生产 → [skills/pixel-art-studio/SKILL.md](../pixel-art-studio/SKILL.md)