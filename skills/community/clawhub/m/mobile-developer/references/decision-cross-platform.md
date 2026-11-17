# 跨平台与原生选型决策（Mobile Cross-Platform Decision）

> 子技能 `flutter-builder` / `react-native-builder` / `ios-developer` 各自讲"怎么写"，
> 本篇讲"先选哪条路"——这是子技能装不下的决策方法论。选错技术栈的代价是重写，
> 不是补丁。先用决策树定位，再用选型矩阵对比，最后用清单收口。

## 1. 一维决策树（先定性）

```
Q0 目标平台只有 iOS 吗？
├─ 是 → Q0a 需要深度系统能力（Metal/ARKit/Widgets/Live Activities/后台音频）吗？
│       ├─ 是 → 原生 SwiftUI（ios-developer），别用跨平台
│       └─ 否 → SwiftUI 仍是最优；跨平台反而增加桥接成本
└─ 否（含 Android / Web / 桌面）→ Q1

Q1 团队有 React/Web 背景吗？
├─ 是 → Q1a 需要原生模块（蓝牙/Camera2/特定 SDK）的深度可控性吗？
│       ├─ 是 → React Native（react-native-builder）+ 原生桥接，
│       │        但要评估桥接成本（见 §4 陷阱）
│       └─ 否 → React Native（react-native-builder），复用 Web 心智
└─ 否 → Q2

Q2 追求极致一致 UI + 单一代码库 + 自绘渲染吗？
├─ 是 → Flutter（flutter-builder），Skia 自绘，iOS/Android 像素一致
└─ 否 → 回到 Q1，选团队最易招到人的栈
```

判定原则：**平台唯一且要系统能力 → 原生；多端 + Web 背景 → RN；多端 + 一致 UI
优先 → Flutter**。不要因为"听说 Flutter 快"就无视团队技能，栈的迁移成本远高于
运行时性能差。

## 2. 选型矩阵（定量对比）

| 维度 | Flutter | React Native | 原生 SwiftUI | 原生 Kotlin |
|------|---------|--------------|--------------|-------------|
| 代码复用率 | 高（iOS/Android/Web/桌面） | 中（JS 共享，原生 UI） | 低（仅 iOS） | 低（仅 Android） |
| 渲染一致性 | 像素级一致（自绘） | 接近（原生组件映射） | 系统原生 | 系统原生 |
| 系统 API 访问 | 需 plugin，覆盖滞后 | 需 bridge，覆盖滞后 | 首发即支持 | 首发即支持 |
| 热重载 | 优秀 | 优秀 | 有限（Preview） | 有限 |
| 包体积增量 | 较大（引擎 ~4-5MB） | 中（桥 + JS 运行时） | 无 | 无 |
| 招人难度 | 中（Dart 小众） | 低（JS 海量） | 中 | 中 |
| 生态成熟度 | 高（pub.dev 丰富） | 高（npm 海量） | 最高 | 最高 |
| 适合团队 | 0→1 独立开发者、设计驱动 | Web 背景、快速迭代 | iOS 专属、系统深度 | Android 专属 |

**取舍口诀**：一致性 > 原生感 选 Flutter；招人 > 一致 选 RN；系统深度 > 一切 选原生。

## 3. 何时从跨平台回退到原生

出现以下任一信号，停止用跨平台硬扛，改原生桥接或整段重写：

- 某平台功能**只能**通过原生 API 实现，且 plugin 缺失或年久失修
- 列表/滚动出现跨平台框架特有的卡顿，且 profiling 指向框架层（非业务层）
- 包体积成为应用商店下载转化的硬约束（低带宽地区用户）
- 需要 Live Activities / 灵动岛 / 系统级 Share Extension 等平台独占能力

回退策略：**渐进式**，先桥接单点原生模块（RN 的 Native Module / Flutter 的
Platform Channel），验证可行后再决定是否整段迁移，不要一次性重写。

## 4. 典型坑与规避

- **坑：RN 桥接爆发的隐性成本**。以为"RN 能调原生"就万事大吉，结果 30% 功能
  都要写双端原生桥，等于维护两套代码。
  *规避*：选型前先列"必须原生"的功能清单，估算桥接行数；超过 5 个深原生功能，
  直接原生更省。
- **坑：Flutter 插件 Android/iOS 行为不一致**。同一 plugin 两端实现不同，UI 错位。
  *规避*：锁定 plugin 版本，CI 里两端各跑一次 golden 截图比对（见 mobile-qa-devices.md）。
- **坑：iOS 上 Flutter 引擎启动慢于原生**。冷启动体验差。
  *规避*：用 `FlutterFragment` 懒加载、预初始化引擎池，或首屏用原生占位。
- **坑：跨平台统一了代码，没统一设计语言**，结果两套 HIG 混用（见 mobile-design-system）。
  *规避*：先定平台尊重策略，再写代码。

## 5. 收口清单

- [ ] 用 §1 决策树得出主选栈，并写下"为什么不选另外两个"的反向论证
- [ ] 用 §2 矩阵确认 3 个最关键的取舍维度与团队现状匹配
- [ ] 列出"必须原生"的功能清单，评估桥接成本是否可控
- [ ] 确认目标平台覆盖率（iOS/Android/Web/桌面）与栈能力匹配
- [ ] 确定包体积预算，粗估引擎增量是否在阈值内
- [ ] 对回退信号（§3）建立监控，触发即启动渐进式原生化
- [ ] 设计语言策略已定（平台尊重 vs 统一自绘），下游 `mobile-design-system` 对齐

## 6. 与子技能的衔接

- 选定 Flutter → 调 [skills/flutter-builder/SKILL.md](../skills/flutter-builder/SKILL.md)（分层架构 / 响应式布局）
- 选定 RN → 调 [skills/react-native-builder/SKILL.md](../skills/react-native-builder/SKILL.md)（导航 / Expo / 原生桥接）
- 仅 iOS 原生 → 调 [skills/ios-developer/SKILL.md](../skills/ios-developer/SKILL.md)（SwiftUI 布局组件）
- 任何栈都要 → 调 [skills/mobile-design-system/SKILL.md](../skills/mobile-design-system/SKILL.md)（触控优先 / 平台尊重 / 电池友好）
- 性能落地 → 见 [references/mobile-performance.md](mobile-performance.md)
- 发布落地 → 见 [references/mobile-release.md](mobile-release.md)

## 7. 团队技能 → 栈映射表

选型不只是技术对比，更是"谁来做"。用团队现有技能反推，比追新栈更稳：

| 团队现状 | 首选 | 次选 | 避免 |
|----------|------|------|------|
| 全是 Web/前端（React） | React Native | Flutter | 纯原生（招人难） |
| 设计/产品驱动、0→1 | Flutter | RN | 原生（慢） |
| 已有 iOS 工程师、只做 iOS | 原生 SwiftUI | — | 跨平台（多余成本） |
| 后端转移动、JS 熟 | React Native | Flutter | 原生 |
| 要桌面+移动统一 | Flutter | RN(实验性) | 原生 |

**反向论证模板**（收口时必写）：
> 我选 X 不选 Y，因为：① Y 在〔维度〕上不满足〔约束〕；② 团队有〔技能〕可立刻上手 X；
> ③ X 在〔风险维度〕上有〔缓解措施〕。若未来出现〔触发条件〕，则回退到 §3 流程。

## 8. 迁移与回退的实操步骤

从跨平台回退到原生（渐进式，避免一次性重写）：

1. **探针**：先用 Platform Channel（Flutter）/ Native Module（RN）把单点原生能力暴露给跨平台层，验证桥接可行。
2. **隔离**：把该能力相关的 UI 与状态从跨平台层切到原生容器（如 Flutter 的 `FlutterFragment` / RN 的 `RCTViewManager`）。
3. **灰度**：原生容器先覆盖 10% 用户，对比崩溃率/帧率，无回归再扩。
4. **收口**：确认稳定后，才把剩余依赖该能力的模块迁移；保留跨平台层做非关键路径。

**整段重写的触发条件**（不要硬扛的信号同时满足 ≥2）：
- 桥接原生功能 > 团队人月 30%
- 框架层卡顿无法在业务层规避（profiling 指向框架而非业务）
- 包体积超商店转化阈值且无法靠动态下发缓解

## 9. 反向：原生 → 跨平台

已有原生双端、想统一代码库时的次序：
1. 先统一设计语言（mobile-design-system），否则统一代码也统一不了体验
2. 用跨平台层重写**非差异化的通用模块**（网络/存储/路由/埋点）
3. 平台独占能力（系统 UI / 深度原生）保留原生，跨平台层通过桥接调用
4. 逐屏切换，AB 对比留存与崩溃，确认无劣化再全量
