---
name: ios-developer
description: SwiftUI 布局与组件：Stack/Grid/List/ScrollView、Form、Searchable、Overlay
source:
  type: derived
  repo: skills-repo/mobile-developer
  path: skills/ios-developer/SKILL.md
  version: 1.0.0
  updated: 2026-07-26
  url: https://skills.sh/dpearson2699/swift-ios-skills/swiftui-layout-components
metadata:
  category: 原生开发
  platform: iOS
  difficulty: 进阶
---

# SwiftUI 布局与组件

> 使用 SwiftUI 构建 iOS 原生界面，覆盖布局、列表、表单、搜索和浮层模式。目标 iOS 17+。

## 能力

- **Stack 布局**：VStack/HStack/ZStack 用于小规模固定内容
- **Lazy 布局**：LazyVStack/LazyHStack 在 ScrollView 中按需渲染大量数据
- **Grid 布局**：LazyVGrid/LazyHGrid 实现自适应网格
- **List 模式**：Section、swipeActions、selection、下拉刷新
- **ScrollView**：ScrollPosition 跟踪、滚动驱动动画
- **Form 与控件**：表单验证、Toggle/Picker/Slider、.searchable 修饰符
- **Overlay 浮层**：sheet、popover、自定义浮层组件

## 使用方式

```
/ios-developer 帮我设计一个设置页面的 SwiftUI Form 布局
/ios-developer 这个列表有 1000 条数据，帮我改成 LazyVStack 优化性能
/ios-developer 实现一个带搜索和 swipe 操作的列表页
```

## 工作流

1. 描述页面功能和数据需求
2. AI 选择合适的布局容器（Stack/List/Grid/ScrollView）
3. 设计数据流和状态管理
4. 实现搜索、导航和交互
5. 检查常见错误（ScrollView 内非 lazy stack、缺少 id 等）

## 适用场景

- SwiftUI 页面从零搭建
- 列表性能优化（非 lazy → lazy）
- Form 表单和设置页面
- 搜索界面和浮层交互

## 限制

- 不涉及 UIKit 深度集成
- 不涉及 Core Data / SwiftData 数据持久化
- 不涉及 App Store 审核流程

## 相关参考（Playbook）

本子技能落地"怎么写 SwiftUI"，跨栈方法论见下列 `references/`（按需读取）：

- 何时选原生 iOS / 系统能力取舍：[references/decision-cross-platform.md](../../references/decision-cross-platform.md)（§1 Q0、§3 回退信号）
- SwiftUI 性能（LazyVStack / 主线程）：[references/mobile-performance.md](../../references/mobile-performance.md)（§2 iOS 段、§7 帧率定位）
- iOS 签名与上架 TestFlight：[references/mobile-release.md](../../references/mobile-release.md)（§2 iOS 构建、§8 分阶段发布）
- iOS 真机 XCTest 与设备矩阵：[references/mobile-qa-devices.md](../../references/mobile-qa-devices.md)（§2 iOS/原生 测试命令、§7 无障碍 QA）