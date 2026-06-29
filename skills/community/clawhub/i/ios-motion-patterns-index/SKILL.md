---
name: ios-motion-patterns-index
description: >-
  Index of ready-to-run Swift animation code examples organized by category (Menu, Transition, Indicator, Alert, Animation, Tableview, Collectionview, UI) sourced from the MotionBook collection. Use this skill whenever the user is writing iOS animations or building SwiftUI/UIKit interactive motion effects and wants a runnable reference to adapt — fetch a working example first instead of inventing motion from scratch. This is a runnable-code index, not a how-to; pair with swiftui-design-skill / twostraws SwiftUI for principles.
---

# iOS 动画可跑实例索引

来自 MotionBook 的 Swift 动画合集索引：按分类指向可直接 clone 运行的开源项目。这是「现成可跑实例目录」——给现成可跑代码的入口，不是动画写法教程。写法教程见 twostraws SwiftUI 教程、`apple-skills:guide-swiftui-animations`、`swiftui-design-skill`。

条目来自开源合集 [younatics/MotionBook](https://github.com/younatics/MotionBook)，按原 8 个分类整理，本索引在其中精选 + 完整条目分文件存放。项目以可直接 clone 运行的 demo 为主（多为 Swift，部分 Objective-C），条目描述为中文、链接与代码为英文原文。

本索引不收录：SwiftUI 原生 `.animation` / `withAnimation` 写法、Lottie / Rive 动画文件、Core Animation 层级教程。需要这些请走 twostraws SwiftUI、`apple-skills:core-animation`、或对应官方文档。

## 如何使用本索引

本文件是调度索引层：8 个分类各列 2-3 条最经典可跑项目，并写清「这是什么、什么时候去读哪个 reference 文件」。其余条目在 `references/` 下按分类拆成单独文件，references 只一层深。

工作流：

1. 先按需求定位下面 8 个分类之一（可用下方「按任务找分类」速查），看精选条目是否够用。
2. 不够或想比较更多实现，打开分类对应的 `references/<分类>.md`，那是该分类完整条目表。
3. 找到目标项目后 clone 跑起来看真实行为，再决定是否搬进自己代码。
4. Tableview 与 Collectionview 条目较少，合并进同一文件 `references/tableview-collectionview.md`，打开后按文件内「表格 / 集合视图」两个小标题分块阅读。

这些项目多为 UIKit 时期的成熟开源库，交互模式与动效曲线已被大量 App 验证；SwiftUI 实现可借鉴其时序与曲线参数。

reference 文件与分类对应：`menu.md` / `animation.md` / `transition.md` / `tableview-collectionview.md`（表格+集合视图合并）/ `indicator.md` / `alert.md` / `ui-controls.md`。

## 按任务找分类

不知道该开哪个 reference 时，先按任务关键词对号入座：

- 侧边 / 底部 / 展开 / 动画 TabBar 菜单 → Menu
- 通用动画库、骨架屏、GIF、文字 / 天气特效 → Animation
- 页面切换、模态、卡片展开转场、引导页 → Transition
- 列表单元格交互、下拉刷新、折纸展开 → Tableview
- 卡片滑动 / 层叠、视差 Sticky / 拉伸头、表格布局 → Collectionview
- loading、分页点、导航栏加载、HUD → Indicator
- 通知横幅、自定义 Alert、顶部提示、蜂群 / 毛玻璃弹窗 → Alert
- 分段控件、滑块、卡片、夜间模式、搜索、Markdown → UI

## 菜单 / Menu

下拉、侧滑、圆形放射、断头台、动画 TabBar 等菜单形态与交互动画。做导航栏 / 侧边栏 / 展开菜单 / 底部 Tab 切换动效时来这里。

- [SideMenu](https://github.com/jonkykong/SideMenu) - Facebook 风格左右侧滑菜单
- [GuillotineMenu](https://github.com/Yalantis/GuillotineMenu) - 断头台式菜单转场动画
- [circle-menu](https://github.com/Ramotion/circle-menu) - 圆形按钮展开成放射状菜单

需要下拉菜单、滑动菜单控制器、动画 TabBar 等更多实现，见 `references/menu.md`（共 7 条）。

## 动画 / Animation

通用动画库、骨架屏、矢量 SVG、启动屏、文字 / GIF / 天气特效等基础动画能力。先看精选，要特定动效（GIF 引擎、闪光文字、天气叠加）再翻 reference。

- [Spring](https://github.com/MengTo/Spring) - 简化 iOS 动画的通用库
- [SkeletonView](https://github.com/Juanpe/SkeletonView) - 骨架屏加载占位动画
- [Macaw](https://github.com/exyte/Macaw) - 支持 SVG 的矢量图形动画库

Pastel、Stellar、RevealingSplashView、Gecco、GlitchLabel，以及 Highlighter、FLAnimatedImage、Ease 等共 18 条见 `references/animation.md`。

## 转场 / Transition

控制器转场、模态气泡、弹性拖拽、滚动转场、引导页 等过渡动画。涉及页面切换 / 卡片展开 / 转场合辑时来这。

- [Hero](https://github.com/lkzhao/Hero) - 视图控制器转场框架
- [BubbleTransition](https://github.com/andreamazz/BubbleTransition) - 气泡展开式模态转场
- [Gemini](https://github.com/shoheiyokoyama/Gemini) - 基于滚动的丰富转场框架

ElasticTransition、AnimatedTransitionGallery、JTMaterialTransition、Pinterest、Walkthrough 等共 14 条见 `references/transition.md`。

## 表格 / Tableview

可展开单元格、下拉刷新、滑动操作、折纸展开、伸缩预览 等 UITableViewCell 实例。做列表交互 / 刷新动效时来这。

- [SwipeCellKit](https://github.com/jerkoch/SwipeCellKit) - Mail.app 风格滑动操作单元格
- [folding-cell](https://github.com/Ramotion/folding-cell) - 折纸展开式单元格

表格与集合视图实例合并存放，YNExpandableCell、Pull-to-Refresh、elongation-preview 等 11 条见 `references/tableview-collectionview.md`。

## 集合视图 / Collectionview

卡片滑动 / 层叠、视差 Sticky Header、弹性拉伸头、电子表格 等 UICollectionView 布局实例。

- [Koloda](https://github.com/Yalantis/Koloda) - Tinder 风格卡片滑动
- [expanding-collection](https://github.com/Ramotion/expanding-collection) - 卡片展开成详情的集合视图

集合视图实例与表格合并：MMCardView、CSStickyHeaderFlowLayout、GSKStretchyHeaderView、SwiftSpreadsheet 等 11 条见 `references/tableview-collectionview.md`。

## 指示器 / Indicator

加载动画、分页指示、导航栏加载、HUD 弹出 等状态指示。做 loading / 分页点 / 进度提示时来这。

- [NVActivityIndicatorView](https://github.com/ninjaprox/NVActivityIndicatorView) - 海量加载动画合集
- [PKHUD](https://github.com/pkluz/PKHUD) - Apple HUD 风格弹出指示

TKRubberIndicator、SpringIndicator、BusyNavigationBar 等共 5 条见 `references/indicator.md`。

## 弹窗 / Alert

通知横幅、自定义 Alert、弹窗替换、顶部通知、蜂群 / 毛玻璃弹窗 等提示形态。

- [NotificationBanner](https://github.com/Daltron/NotificationBanner) - 可定制的应用内通知横幅
- [PopupDialog](https://github.com/Orderella/PopupDialog) - 替代 UIAlertController 的弹窗
- [SDCAlertView](https://github.com/sberrevoets/SDCAlertView) - 支持自定义内容的 Alert

CDAlertView、CRToast、TKSwarmAlert、MIBlurPopup、SweetAlert 等共 9 条见 `references/alert.md`。

## 界面控件 / UI

IB 设计动画、文字变形、分段控件、卡片、流体滑块、搜索、夜间模式 等通用控件实例。

- [IBAnimatable](https://github.com/IBAnimatable/IBAnimatable) - Interface Builder 内设计动画与转场
- [LTMorphingLabel](https://github.com/lexrus/LTMorphingLabel) - 文字变形演化 UILabel
- [fluid-slider](https://github.com/Ramotion/fluid-slider) - 带气泡数值的流体滑块

Segmentio、Cards、StarWars、YNSearch、DKNightVersion、MarkdownView 等 13 条见 `references/ui-controls.md`。

完整 MotionBook 见 https://github.com/younatics/MotionBook
条目随上游更新，缺失或链接失效可向 MotionBook 仓库反馈。
