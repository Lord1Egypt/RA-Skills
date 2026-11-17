---
name: mobile-developer
description: >-
  移动端开发技能库：覆盖 Flutter、React Native、iOS 原生（SwiftUI）三栈的应用开发，
  以及移动端设计、性能电池优化、商店发布与设备 QA。提供跨平台选型决策、性能与电池优化、
  发布 CI 工作流、设备矩阵真机测试的方法论，并用脚本固化权限清单校验与依赖重复检查。
  触发词："移动端"、"Flutter"、"React Native"、"iOS"、"SwiftUI"、"跨平台选型"、
  "移动性能"、"电池优化"、"App 上架"、"TestFlight"、"权限清单"、"移动 QA"。
agent_created: true
metadata:
  version: 1.0.0
  category: 移动端
  difficulty: 进阶
  architecture: superpower
---

# 移动端开发工程师 (Mobile Developer)

> 把 AI 编程助手变成一名能扛下移动端交付链路（选型→开发→性能→发布→QA）的搭档：从三栈开发到上架，并用确定性脚本守住权限与依赖这类硬门槛。

本技能采用 **superpower 架构**：`SKILL.md` 只做路由，深层 playbook 放在 `references/` 中**按需加载**，细粒度能力放在 `skills/` 子技能，确定性任务交给 `scripts/`，可复用模板放在 `assets/`。

## 何时使用

- 需要**选技术栈**：Flutter / React Native / 原生 SwiftUI 怎么选、何时回退原生
- 用 **Flutter / RN / SwiftUI** 开发跨平台或 iOS 原生应用、做响应式布局与状态管理
- 需要**性能与电池优化**：列表卡顿、冷启动慢、包体积大、耗电高
- 需要**上架发布**：签名、商店元数据、审核避坑、灰度与回滚
- 需要**真机 QA**：设备矩阵覆盖、权限时序、弱网降级、碎片化兼容
- 需要**校验权限声明**或**排查依赖重复/版本冲突**（确定性脚本）

## 能力索引（超级技能路由）

本技能采用渐进式加载（progressive disclosure）。`SKILL.md` 仅作路由，**按需**读取下列 `references/` 中的完整 playbook，避免一次性占满上下文。

| 任务 | 读取 / 调用 | 关键词（grep 线索） |
|------|------------|---------------------|
| 跨平台与原生选型决策（决策树 + 矩阵 + 回退） | [references/decision-cross-platform.md](references/decision-cross-platform.md) | 选型, 跨平台, Flutter, React Native, 原生, 回退 |
| 性能与电池优化（帧率/内存/包体积/电量） | [references/mobile-performance.md](references/mobile-performance.md) | 性能, 帧率, 内存, 电池, 包体积, 冷启动 |
| 发布与 CI 工作流（签名/商店/审核/灰度） | [references/mobile-release.md](references/mobile-release.md) | 发布, 上架, 签名, TestFlight, 审核, 灰度 |
| 设备矩阵与真机 QA（E2E/权限/碎片化） | [references/mobile-qa-devices.md](references/mobile-qa-devices.md) | QA, 真机, 设备矩阵, E2E, 权限时序, 碎片化 |
| Flutter 分层架构与响应式布局（细粒度调用） | [skills/flutter-builder/SKILL.md](skills/flutter-builder/SKILL.md) | flutter, MVVM, 响应式, Widget, 分层, 大屏 |
| React Native 组件/导航/Expo/原生桥接（细粒度调用） | [skills/react-native-builder/SKILL.md](skills/react-native-builder/SKILL.md) | react-native, FlatList, Expo, 导航, 桥接, Hermes |
| SwiftUI 布局与组件（细粒度调用） | [skills/ios-developer/SKILL.md](skills/ios-developer/SKILL.md) | swiftui, Stack, LazyVGrid, Form, Overlay, iOS17 |
| 移动端设计规范（细粒度调用） | [skills/mobile-design-system/SKILL.md](skills/mobile-design-system/SKILL.md) | 触控, 平台尊重, 电池友好, 离线, 无障碍, MFRI |

> 路由规则：先判断任务属于「选型 / 性能 / 发布 / QA」哪类方法论 → 读 `references/`；要落地某个具体栈的写法 → 直接调 `skills/` 对应子技能。

## 内置脚本（确定性、可重复执行）

放在 `scripts/`，优先用脚本处理重复/确定性任务，而非每次重写代码：

- `scripts/check_permissions.py --android AndroidManifest.xml --ios Info.plist --spec assets/permissions-spec.json` — 校验权限声明：缺 exported、危险/禁止权限、iOS 用途描述空或缺失
- `scripts/check_dep_dupes.py --package-json package.json --pubspec pubspec.yaml` — 检查依赖在 dependencies/devDependencies 重复声明与跨文件版本冲突

运行示例：

```bash
python3 scripts/check_permissions.py --android AndroidManifest.xml --ios Info.plist --spec assets/permissions-spec.json
python3 scripts/check_dep_dupes.py --package-json package.json --pubspec pubspec.yaml
```

## 模板资源

`assets/` 提供可直接套用的配置与模板：

- [assets/permissions-spec.json](assets/permissions-spec.json) — 权限基线规范（含 `_` 注释键，驱动 check_permissions.py）
- [assets/android-manifest-template.xml](assets/android-manifest-template.xml) — Android 权限清单模板（脚本自检 0 错误）
- [assets/ios-info-plist-template.plist](assets/ios-info-plist-template.plist) — iOS 用途描述模板（脚本自检 0 错误）
- [assets/permissions-checklist.md](assets/permissions-checklist.md) — 移动端权限与隐私上线检查清单

## 核心原则（始终遵循）

1. **选型先行**：先定栈再写代码，用决策树与矩阵论证，避免重写代价。
2. **先量后优**：性能结论必须来自 release/真机测量，不信"感觉快了"。
3. **渐进式加载**：先读路由表与对应 `references/`，再动手；不凭记忆猜框架命令。
4. **权限最小化**：只申请必要权限，用途透明，被拒不卡死；脚本守住声明门槛。
5. **发布可复现**：CI 出包、灰度上线、监控回滚，不在本地手工出包。
6. **明确边界**：架构/选型拍板由人做，本技能出报告与方案，不替代业务决策。

## 与其他技能协作

- 需要**动画/动效**设计 → 调用 `animation-engineer`
- 需要**测试**（单测/E2E/覆盖率）→ 调用 `software-tester`
- 需要**安全审计**（密钥/依赖/OWASP）→ 调用 `security-guardian`
- 需要**运维部署**（CI/CD、容器）→ 调用 `devops-engineer`
- 需要**文档**（README、商店文案）→ 调用 `docs-writer`
