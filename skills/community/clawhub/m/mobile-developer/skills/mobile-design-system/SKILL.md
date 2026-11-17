---
name: mobile-design-system
description: 移动端设计规范：触控优先、平台尊重、电池友好、离线可用
source:
  type: derived
  repo: skills-repo/mobile-developer
  path: skills/mobile-design-system/SKILL.md
  version: 1.0.0
  updated: 2026-07-26
  url: https://skills.sh/sickn33/antigravity-awesome-skills/mobile-design
metadata:
  category: 设计
  platform: Mobile
  difficulty: 进阶
---

# 移动端设计规范

> 触控优先、平台尊重、电池友好。移动端不是缩小版桌面——先考虑约束，再考虑美学。

## 能力

- **移动可行性评估（MFRI）**：平台清晰度、交互复杂度、性能风险、离线依赖、无障碍风险五维评分
- **触控优先设计**：44pt 最小触控目标、手势冲突处理、拇指热区
- **平台尊重**：iOS HIG vs Material Design 3 差异对照，不跨平台混用 UI 模式
- **电池友好**：暗色模式适配、减少不必要的动画和轮询
- **离线可用**：离线状态 UI 提示、本地缓存策略、同步冲突处理

## 使用方式

```
/mobile-design-system 为我的应用做移动可行性评估
/mobile-design-system 这个页面在 iOS 和 Android 上表现不一致，帮我统一平台差异
/mobile-design-system 审查这个设计方案的触控可达性
```

## 工作流

1. 描述应用类型和目标用户群
2. 运行 MFRI 五维评分，识别风险点
3. 分析 iOS/Android 平台差异需求
4. 输出触控、导航、反馈的设计建议
5. 检查离线和无障碍兼容性

## 适用场景

- 新应用移动端设计评审
- iOS/Android 平台一致性审查
- 触控交互方案设计
- 移动端无障碍合规检查

## 限制

- 不涉及设计工具（Figma/Sketch）的具体操作
- 不涉及品牌视觉设计（Logo/插画/品牌色）
- 复杂动效实现建议配合 design-studio 的 motion-design

## 相关参考（Playbook）

本子技能落地"移动端设计原则"，与之配合的跨栈方法论见下列 `references/`（按需读取）：

- 平台尊重与选型中的设计语言策略：[references/decision-cross-platform.md](../../references/decision-cross-platform.md)（§4 跨平台混用坑、§5 收口清单）
- 电池友好与暗色模式实现：[references/mobile-performance.md](../../references/mobile-performance.md)（§3 电池友好硬性规则）
- 触控热区与无障碍 QA 真机核查：[references/mobile-qa-devices.md](../../references/mobile-qa-devices.md)（§3 真机必查清单、§7 无障碍 QA）