---
name: game-developer
description: Three.js 浏览器游戏开发：游戏循环、物理、3D 资产、UI、QA 全流程
source:
  type: derived
  repo: skills-repo/indie-game-developer
  path: skills/game-developer/SKILL.md
  version: 1.0.0
  updated: 2026-07-26
  url: https://skills.sh/majidmanzarpour/threejs-game-skills/threejs-game-director
metadata:
  category: 游戏开发
  platform: Web
  difficulty: 进阶
---

# 游戏开发者

> Three.js 浏览器游戏全流程开发：从游戏循环搭建到 3D 资产、UI 设计、调试分析、QA 发布。

## 能力

- **游戏循环**：核心循环架构、实体系统、输入处理、物理选型
- **3D 渲染**：模型加载、材质、着色器、灯光、后期特效
- **游戏 UI**：HUD、菜单、覆盖层、响应式适配
- **调试与性能**：Canvas 检查、性能分析、移动端适配
- **QA 与发布**：浏览器兼容测试、截图验证、生产构建、Release Notes

## 使用方式

```
/game-developer 创建一个跑酷游戏原型
/game-developer 为这个游戏添加粒子特效和后处理
/game-developer 分析这个游戏的性能瓶颈
```

## 工作流

1. 设计游戏概念和核心循环
2. 搭建 Three.js 项目脚手架
3. 实现游戏机制和实体
4. 迭代视觉和特效
5. 性能分析和 QA 测试
6. 构建发布版本

## 适用场景

- 浏览器 3D 游戏开发
- 游戏原型快速验证
- 游戏性能优化
- 独立游戏制作

## 限制

- 仅覆盖 Three.js/Web 游戏，不涉及 Unity/Unreal
- 不涉及多人联机
- 不涉及移动端原生发布

> 本子技能属**Three.js 开发执行层**（游戏循环 / 物理 / 3D 资产 / UI / QA）；方法层见 reference。

- 引擎选型决策树 → [`references/decision-engine-tech.md`](../../references/decision-engine-tech.md)
- 资源管线（glb / 精灵表 / 引用完整性）→ [`references/asset-pipeline.md`](../../references/asset-pipeline.md)
- 性能与 QA 基线 → [`references/game-qa-perf.md`](../../references/game-qa-perf.md)