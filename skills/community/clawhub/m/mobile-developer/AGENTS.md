# AGENTS.md — mobile-developer 入口文件

> mobile-developer 仓库的 Agent 入口文件，定义移动端开发技能库的使用规则与 superpower 目录加载顺序。

## 架构与加载顺序（superpower）

本仓库按 skills-repo 的 **superpower 架构**组织，Agent 加载顺序如下：

1. **先读 `SKILL.md`（L1 路由层）** — 只做能力索引，不要在此找方法论正文。
2. **按需读 `references/`（L2）** — 选型决策、性能电池、发布 CI、设备 QA 等完整 playbook，按任务类型加载，不全量读。
3. **落地具体栈时读 `skills/<name>/SKILL.md`（L3）** — Flutter / RN / iOS / 设计规范的细粒度能力。
4. **确定性任务用 `scripts/`（L4）** — 权限清单校验、依赖重复检查，产物可复现。
5. **模板套用看 `assets/`（L5）** — 权限规范、清单与检查清单模板。

渐进式加载原则：先路由、后深度；不凭记忆猜框架命令与 API。

## 触发条件

Agent 在以下场景加载本文件：

1. 用户请求移动端应用开发相关任务
2. 用户提到 Flutter、React Native、iOS 或移动端设计
3. 用户请求跨平台或原生移动端功能实现
4. 用户需要权限声明校验或依赖冲突排查

## 技能清单

| 技能 | 文件 | 用途 |
|------|------|------|
| flutter-builder | skills/flutter-builder/SKILL.md | Flutter Widget、状态管理、响应式布局 |
| react-native-builder | skills/react-native-builder/SKILL.md | React Native 组件、导航、Expo |
| ios-developer | skills/ios-developer/SKILL.md | SwiftUI、Core Data、辅助功能 |
| mobile-design-system | skills/mobile-design-system/SKILL.md | 平台设计规范、手势交互、动效 |

## 行为规则

- 所有技能面向独立开发者/小团队，不涉及企业级移动端架构
- 优先推荐跨平台方案（Flutter/React Native），iOS 原生作为补充
- 移动端设计需同时考虑 iOS 和 Android 平台差异
- 选型类问题先读 [references/decision-cross-platform.md](references/decision-cross-platform.md) 用决策树论证，再落地
- 性能/发布/QA 类问题先读对应 `references/` playbook，再调子技能

## 不做什么

- 不涉及 Android 原生（Kotlin/Jetpack Compose）开发 — 可后续补充
- 不涉及移动端游戏开发 — 归属 indie-game-developer
- 不涉及移动端安全测试 — 归属 security-guardian
