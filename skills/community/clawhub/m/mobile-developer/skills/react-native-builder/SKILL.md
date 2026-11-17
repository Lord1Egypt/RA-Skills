---
name: react-native-builder
description: React Native 组件开发、导航、原生模块、Expo 工具链与性能优化
source:
  type: derived
  repo: skills-repo/mobile-developer
  path: skills/react-native-builder/SKILL.md
  version: 1.0.0
  updated: 2026-07-26
  url: https://skills.sh/google-labs-code/stitch-skills/stitch::react-components
metadata:
  category: 跨平台
  platform: Mobile
  difficulty: 入门
---

# React Native 应用开发

> 使用 React Native 构建跨平台移动应用，覆盖组件开发、导航、原生模块和 Expo 工具链。

## 能力

- **组件开发**：核心组件（View/Text/Image/ScrollView）、自定义组件、StyleSheet 样式系统
- **导航**：React Navigation 栈/标签/抽屉导航、深层链接配置
- **Expo 工具链**：Expo SDK、EAS Build、OTA 更新、expo-dev-client
- **原生模块**：原生模块桥接模式、第三方原生库集成
- **性能优化**：FlatList 优化（getItemLayout、windowSize）、图片缓存、JS 线程优化

## 使用方式

```
/react-native-builder 帮我搭建一个带底部标签导航的 Expo 项目
/react-native-builder 这个 FlatList 滚动卡顿，帮我优化性能
/react-native-builder 我需要调用一个原生 SDK，帮我写桥接模块
```

## 工作流

1. 描述应用功能和目标平台（iOS/Android/Web）
2. AI 选择 Expo 或裸工作流作为起点
3. 设计组件树和导航结构
4. 实现功能组件和屏幕
5. 性能审查和优化建议

## 适用场景

- 从零搭建 React Native 项目
- 已有项目迁移到 Expo
- 性能问题排查和优化
- 原生模块集成

## 限制

- 不涉及原生 iOS/Android 完整开发（仅桥接层面）
- 不涉及 React Native 新架构（Fabric/TurboModules）深度定制
- 复杂动画建议配合 design-studio 的 motion-design

## 相关参考（Playbook）

本子技能落地"怎么写 React Native"，跨栈方法论见下列 `references/`（按需读取）：

- 为何选 RN / 桥接成本评估：[references/decision-cross-platform.md](../../references/decision-cross-platform.md)（§1 Q1、§4 桥接坑）
- RN 性能（FlatList / Hermes）：[references/mobile-performance.md](../../references/mobile-performance.md)（§2 React Native 段、§4 典型坑）
- RN 出包与 EAS / CodePush：[references/mobile-release.md](../../references/mobile-release.md)（§2 Android 构建、§8 回滚）
- RN 真机 Detox / Maestro 测试：[references/mobile-qa-devices.md](../../references/mobile-qa-devices.md)（§2 React Native 测试命令）