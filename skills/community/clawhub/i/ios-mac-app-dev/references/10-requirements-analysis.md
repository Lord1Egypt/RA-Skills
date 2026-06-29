# 需求澄清工作流

> 基于 matt pocock `grill-me` 理念改写，适配 iOS/macOS 开发场景。

## 核心理念

**大多数开发失败的根源是需求未对齐。** 在写第一行代码之前，先用「烤问式对话」把需求挖透。

烤问的目标：
1. **功能边界** — 这个 App/功能到底要解决什么问题？
2. **用户故事** — 谁用？在什么场景下用？
3. **技术约束** — 最低部署版本？现有架构（MVVM/TCA）？
4. **设计语言** — 是否已有 Design System？配色方案？
5. **边缘情况** — 离线怎么办？数据为空怎么办？权限被拒怎么办？

## 烤问流程

```
第1轮：问题定义
  → 这个功能的本质是什么？
  → 没有这个功能，用户现在怎么解决同样的问题？

第2轮：用户与场景
  → 目标用户是谁？（普通用户 / 专业用户 / 企业内部）
  → 使用场景？（通勤时单手操作 / 桌面多窗口 / iPad 分屏）

第3轮：技术决策
  → 最低部署版本？（iOS 15+ 可用 SwiftUI 全量特性）
  → 现有架构？（在 MVVM 里加 / 新建 TCA feature / 用 UIKit）
  → 数据持久化？（SwiftData / Core Data / UserDefaults / CloudKit）

第4轮：设计约束
  → 是否已有品牌规范？（颜色、字体、图标风格）
  → 需要适配 iPad / macOS / visionOS？
  → 深色模式必须的吗？

第5轮：边缘情况与风险
  → 网络失败怎么处理？（重试 / 离线缓存 / 错误提示）
  → 数据为空时显示什么？（Skeleton / Empty State）
  → 需要权限的功能，用户拒绝后怎么办？
```

## 输出物

烤问结束后，输出以下内容：

```
## 需求摘要
- 问题：...
- 目标用户：...
- 核心用户故事：...
- 技术栈：Swift 6.0, SwiftUI, iOS 16+
- 设计语言：[引用项目 Design System 或提出新建]

## 功能范围
- ✅ 包含：...
- ❌ 明确不包含（本次）：...

## 技术决策
- 架构：MVVM + Observation
- 网络层：URLSession + async/await
- 持久化：SwiftData
- 导航：NavigationStack

## 风险与假设
- 假设1：...
- 风险1：...
```

## 与后续工作流衔接

烤问输出直接作为以下工作的输入：
- `references/11-prd-generation.md` — 生成正式 PRD
- `references/12-task-breakdown.md` — 拆解开发任务
- `references/01-code-generation.md` — 开始代码生成
