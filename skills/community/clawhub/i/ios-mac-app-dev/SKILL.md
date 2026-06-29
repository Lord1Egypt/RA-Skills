---
name: ios-mac-app-dev
description: |
  iOS/macOS 应用全生命周期开发技能包。覆盖从需求分析到上架发布的完整流程，包括：工程工作流（需求澄清、PRD生成、任务拆解、Swift TDD、Bug诊断、架构改进）、政策合规监控与动态学习、智能代码生成（Swift/SwiftUI/UIKit）、UI设计系统与美学规范（12大设计法则、631配色、8点网格）、多语言国际化（50+语言）、深色模式适配、架构模式库（MVVM/TCA/VIPER）、性能优化、无障碍、Apple Intelligence集成、App Store上架检查。

  触发场景：
  - 用户问"在iOS/macOS做个App"、"帮我写个SwiftUI视图"、"创建Xcode项目"
  - 用户需要App Store上架检查、审核指南合规检查、出口合规声明
  - 用户询问UI设计规范、配色方案、深色模式适配方案
  - 用户需要国际化/本地化支持、多语言切换
  - 用户需要代码生成、架构设计、性能优化建议
  - 任何涉及Apple开发政策、审核指南、API废弃通知的问题
  - 用户说"开发技能"、"应用开发skill"、"iOS开发"、"mac开发"
  - 用户说"需求分析"、"生成PRD"、"拆任务"、"TDD"、"诊断bug"、"架构改进"
---

# iOS/macOS 应用全生命周期开发技能包

> 基于 Swift 6.0 / SwiftUI / iOS 15+ / macOS 14+，覆盖从需求分析到 App Store 发布的全链路 AI 辅助开发。

## 核心能力总览

本技能包通过 **16 大核心模块** 提供 iOS/macOS 应用开发的 AI 辅助：

```
┌─────────────────────────────────────────────────────┐
│  ios-mac-app-dev                                    │
├─────────────────────────────────────────────────────┤
│  【工程工作流】                                      │
│  11 需求澄清 ─ 烤问式对话，深挖需求边界              │
│  12 PRD生成 ─ 将对话转为产品需求文档                 │
│  13 任务拆解 ─ 垂直切片拆解为独立开发任务             │
│  14 Swift TDD ─ 测试驱动开发（XCTest）              │
│  15 Bug诊断 ─ 六阶段 disciplined debugging           │
│  16 架构改进 ─ 浅模块深化，提升可测试性             │
├─────────────────────────────────────────────────────┤
│  【领域知识】                                       │
│  01 政策合规 ─ 自动追踪 Apple 政策变更、审核指南     │
│  02 代码生成 ─ 智能 Swift/SwiftUI 代码生成         │
│  03 UI设计   ─ 12大法则 + 631配色 + 8点网格      │
│  04 本地化   ─ 50+语言全流程支持                   │
│  05 深色模式 ─ 自动检测 + 自适应方案                 │
│  06 架构模式 ─ MVVM/TCA/VIPER 模板库             │
│  07 性能优化 ─ 启动速度、内存、渲染优化              │
│  08 无障碍   ─ VoiceOver + Dynamic Type + WCAG     │
│  09 AI集成   ─ App Intents + Writing Tools         │
│  10 上架检查 ─ 完整发布就绪清单                    │
└─────────────────────────────────────────────────────┘
```

## 快速路由

| 用户需求 | 参考模块 |
|----------|----------|
| 需求澄清/烤问对话 | 11 需求澄清 → `references/10-requirements-analysis.md` |
| 生成PRD/产品需求文档 | 12 PRD生成 → `references/11-prd-generation.md` |
| 任务拆解/分Issue | 13 任务拆解 → `references/12-task-breakdown.md` |
| Swift TDD/测试驱动 | 14 Swift TDD → `references/13-tdd-swift.md` |
| Bug诊断/调试 | 15 Bug诊断 → `references/14-bug-diagnosis.md` |
| 架构改进/重构 | 16 架构改进 → `references/15-architecture-improvement.md` |
| 查政策/合规/审核指南 | 01 政策合规 → `references/00-policy-compliance.md` |
| 写代码/生成视图/网络层 | 02 代码生成 → `references/01-code-generation.md` |
| 设计UI/配色/排版/规范 | 03 UI设计 → `references/02-ui-design.md` |
| 多语言/国际化/翻译 | 04 本地化 → `references/03-localization.md` |
| 深色模式适配 | 05 深色模式 → `references/04-dark-mode.md` |
| 架构设计/模式选择 | 06 架构模式 → `references/05-architecture.md` |
| 性能优化/卡顿排查 | 07 性能优化 → `references/06-performance.md` |
| 无障碍/VoiceOver | 08 无障碍 → `references/07-accessibility.md` |
| 集成AI/App Intents | 09 AI集成 → `references/08-ai-integration.md` |
| 上架检查/发布清单 | 10 上架发布 → `references/09-release-checklist.md` |
| 设计质量自动检查 | `scripts/design_quality_checker.py` |
| 政策变更监控 | `scripts/policy_monitor.py` |

## 完整开发工作流

**推荐按以下顺序执行完整功能开发：**

```
1. 需求澄清 (11)
   ↓
2. 生成PRD (12)
   ↓
3. 任务拆解 (13) → 得到可独立开发的垂直切片
   ↓
4. 架构设计 → 选择模式 (06) + 必要时架构改进 (16)
   ↓
5. Swift TDD (14) → 垂直切片逐个：RED→GREEN→REFACTOR
   ↓
6. 代码生成 (02) → 遵守质量门禁
   ↓
7. UI设计检查 (03) → 用设计质量检查器验证
   ↓
8. Bug诊断 (15) → 如遇到问题
   ↓
9. 上架检查 (10) → 准备发布
```

## 核心质量门禁

无论生成什么代码，必须遵守以下规则：

1. **🖼️ SF Symbols** — 所有图标使用 SF Symbols，禁止使用 emoji 作为功能图标
2. **🌗 深色模式** — 所有颜色在 Asset Catalog 中定义 Light/Dark 变体，禁止硬编码颜色值
3. **🌐 本地化** — 所有用户可见文本使用 `NSLocalizedString` + String Catalog
4. **📱 动态字体** — 支持 `Dynamic Type`，加 `.dynamicTypeSize(...DynamicTypeSize.xLarge)`
5. **✅ 系统字体** — 使用 SF Pro / PingFang，禁止 Inter/Roboto 等非系统字体
6. **🎨 命名颜色** — 所有颜色值通过 Asset Catalog 的命名颜色管理
7. **🚫 反模式** — 避免紫蓝渐变背景、emoji图标、Inter字体（见 `references/02-ui-design.md#反AI流行模式检查清单`）
8. **📋 出口合规** — Info.plist 必须包含 `ITSAppUsesNonExemptEncryption = false`
9. **🧪 TDD** — 先写失败测试，再写实现（见 `references/13-tdd-swift.md`）
10. **🏗️ 深模块** — 追求「小接口，深实现」（见 `references/15-architecture-improvement.md`）

## 脚本

- `scripts/design_quality_checker.py` — 设计质量自动检查（颜色、字体、间距、深色模式、按钮层级）
- `scripts/policy_monitor.py` — 政策变更监控脚本

## 参考文档

### 工程工作流

- `references/10-requirements-analysis.md` — 需求澄清工作流（烤问式对话，深挖需求边界）
- `references/11-prd-generation.md` — PRD 生成工作流（将对话转为产品需求文档）
- `references/12-task-breakdown.md` — 任务拆解工作流（垂直切片，端到端路径）
- `references/13-tdd-swift.md` — Swift TDD 工作流（RED-GREEN-REFACTOR，XCTest）
- `references/14-bug-diagnosis.md` — Bug 诊断工作流（六阶段：反馈循环→复现→假设→插桩→修复→清理）
- `references/15-architecture-improvement.md` — 架构改进工作流（浅模块深化，HTML报告）

### 领域知识

- `references/00-policy-compliance.md` — 政策合规与动态学习（AI/ML条款、4.3条款、敏感内容、未成年保护）
- `references/01-code-generation.md` — 智能代码生成（结构化提示词、生成-测试-修复闭环、多模型协同）
- `references/02-ui-design.md` — UI设计系统（12大法则、631配色、8点网格、圆角规范、排版系统、反模式清单）
- `references/03-localization.md` — 国际化与本地化（50+语言支持、RTL、文化敏感性、设备端翻译）
- `references/04-dark-mode.md` — 深色模式适配（自适应颜色、图片变体、对比度检查）
- `references/05-architecture.md` — 架构模式库（MVVM/TCA/VIPER 模板）
- `references/06-performance.md` — 性能优化（启动优化、内存管理、渲染性能）
- `references/07-accessibility.md` — 无障碍支持（VoiceOver、Dynamic Type、WCAG）
- `references/08-ai-integration.md` — Apple Intelligence 集成（App Intents 2.0、Writing Tools、Image Playground）
- `references/09-release-checklist.md` — App Store 上架发布就绪清单
