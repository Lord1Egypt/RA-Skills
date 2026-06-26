# openclaw-flutter-animations

Flutter 流畅动画实现指南 - OpenClaw Skill 版本

## 概述

本技能是从 [skills.sh](https://skills.sh/madteacher/mad-agents-skills/flutter-animations) 的 `madteacher/mad-agents-skills` 项目改编而来，为 OpenClaw Agent 提供 Flutter 动画开发指南。

## 原作者

- **原作者**: madteacher
- **来源**: [mad-agents-skills](https://github.com/madteacher/mad-agents-skills)
- **原始项目**: https://skills.sh/madteacher/mad-agents-skills/flutter-animations

## 改编内容

本技能保留了原 skill 的核心内容，包括：

1. **隐式动画 (Implicit Animations)** - AnimatedContainer, AnimatedOpacity, TweenAnimationBuilder 等
2. **显式动画 (Explicit Animations)** - AnimationController, Tween, CurvedAnimation, AnimatedWidget, AnimatedBuilder
3. **Hero 动画** - 页面间共享元素过渡动画
4. **交错动画 (Staggered Animations)** - 使用 Interval 实现多动画协调
5. **物理动画 (Physics-Based Animations)** - SpringSimulation, Fling 等
6. **最佳实践** - 性能优化和注意事项

## OpenClaw 使用说明

### 安装

将 skill 复制到 OpenClaw 工作区：

```bash
mkdir -p ~/.openclaw/workspace/skills/openclaw-flutter-animations
cp -r ./openclaw-flutter-animations/* ~/.openclaw/workspace/skills/openclaw-flutter-animations/
```

### 使用方式

当 OpenClaw 提示需要 Flutter 动画相关帮助时，此 skill 将自动加载并提供：

- 动画类型选择建议（隐式 vs 显式 vs Hero vs 交错 vs 物理）
- 常用动画 widget 的代码示例
- 性能优化建议
- 最佳实践指南

### 环境要求

- **Flutter SDK**: 必须安装
- **Dart**: 随 Flutter 一起安装

## 目录结构

```
openclaw-flutter-animations/
├── SKILL.md              # 主技能文件
├── README.md             # 本文件
└── references/           # 参考文档目录
    ├── implicit.md       # 隐式动画详细参考
    ├── explicit.md       # 显式动画详细参考
    ├── hero.md           # Hero 动画指南
    ├── staggered.md      # 交错动画模式
    ├── physics.md        # 物理动画
    └── curves.md         # 动画曲线参考
```

## 许可证

本技能遵循原项目 [mad-agents-skills](https://github.com/madteacher/mad-agents-skills) 的许可证。

---

*改编自 madteacher/mad-agents-skills (https://github.com/madteacher/mad-agents-skills)*
