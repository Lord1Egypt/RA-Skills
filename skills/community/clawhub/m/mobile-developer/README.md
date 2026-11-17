# Mobile Developer — 移动端开发技能库

> 面向独立开发者的移动端技能集，覆盖 Flutter、React Native、iOS 原生和移动端设计。

## 架构说明（superpower）

本仓库采用 skills-repo 的 **superpower 架构**（五层）：

- `SKILL.md` — L1 路由层，只做能力索引，不写方法论
- `references/` — L2 深层 playbook（选型决策、性能电池、发布 CI、设备 QA），按需加载
- `skills/` — L3 细粒度子技能（Flutter / RN / iOS / 设计规范），可单独安装
- `scripts/` — L4 确定性脚本（权限清单校验、依赖重复检查）
- `assets/` — L5 可复用模板（权限规范、清单模板、检查清单）

## 技能列表

| 技能 | 描述 | 难度 | 来源 |
|------|------|------|------|
| [flutter-builder](skills/flutter-builder/SKILL.md) | Flutter 分层架构（UI/Logic/Data）、MVVM、响应式布局 | 进阶 | [衍生](https://skills.sh/flutter/skills/flutter-apply-architecture-best-practices) |
| [react-native-builder](skills/react-native-builder/SKILL.md) | React Native 组件开发、导航、Expo 工具链与性能优化 | 入门 | [衍生](https://skills.sh/google-labs-code/stitch-skills/stitch::react-components) |
| [ios-developer](skills/ios-developer/SKILL.md) | SwiftUI 布局与组件：Stack/Grid/List/ScrollView、Form、Overlay | 进阶 | [衍生](https://skills.sh/dpearson2699/swift-ios-skills/swiftui-layout-components) |
| [mobile-design-system](skills/mobile-design-system/SKILL.md) | 移动端设计规范：触控优先、平台尊重、电池友好 | 进阶 | [衍生](https://skills.sh/sickn33/antigravity-awesome-skills/mobile-design) |

## 安装

```bash
# 整库安装（推荐）—— 拿到路由层 + 全部 references/scripts/assets
npx skills add skills-repo/mobile-developer -g -y

# 单技能安装 —— 只要某一个细粒度能力，例如只要 Flutter 构建能力
npx skills add skills-repo/mobile-developer@flutter-builder -g -y
```

> 也可直接克隆源码使用：

```bash
git clone https://github.com/skills-repo/mobile-developer.git
```

## 内置脚本与模板

```bash
# 校验 Android / iOS 权限声明（期望 0 error）
python3 scripts/check_permissions.py \
  --android AndroidManifest.xml --ios Info.plist --spec assets/permissions-spec.json

# 检查依赖重复声明与版本冲突
python3 scripts/check_dep_dupes.py --package-json package.json --pubspec pubspec.yaml
```

详见 `SKILL.md` 的「内置脚本」与「模板资源」两节。

## 贡献

欢迎提交 Issue 或 PR 补充新的移动端技能。请参考 [CONTRIBUTING.md](../skills-repo-admin/rules/skill-format.md) 的格式规范。
