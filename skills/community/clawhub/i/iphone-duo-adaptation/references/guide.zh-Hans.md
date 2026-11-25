# iPhone Duo 开发与验收手册

[English](guide.en.md) · [日本語](guide.ja.md) · [工程示例](engineering.md) · [Apple 官方资料](sources.md)

## 1. 确认工程基线

从用户实际进入的页面和目标 Target 开始。记录工程与 Scheme、SwiftUI 或 UIKit 及混用边界、最低支持 iOS、选中的 Xcode 和 SDK、已发布语言与地区、iPad 或 Mac Catalyst 支持范围。选择一条完整核心流程，从列表进入详情、编辑、保存再返回。先用现有版本记录界面和状态，再升级构建 SDK，便于确定回归在哪一步出现。

| 构建 SDK | iPhone Duo 上的表现 |
| --- | --- |
| iOS 26 或更早 | 外屏以兼容方式显示。内屏打开时 App 保留较小的居中窗口，周围有空白。 |
| iOS 27.0 | App 可动态调整大小，使用内屏大部分区域，状态栏所在的侧边仍留出空间。 |
| iOS 27.1 或之后 | App 可延伸到内外屏边缘。标准导航、工具栏及标签栏会在适用情境下垂直布置。 |

用 Xcode 27.1 或支持相应 SDK 的后续版本开启完整适配。构建 SDK 和 deployment target 分开配置。新 API 通过 `#available(iOS 27.1, *)` 等兼容分支接入，旧 iOS 保留基础交互。多平台 Target 还需检查各平台可用性与已知工具链问题。[Apple 准备指南](https://developer.apple.com/iphone-duo/prepare/) · [Xcode 27.1 发行说明](https://developer.apple.com/documentation/xcode-release-notes/xcode-27_1-release-notes)

## 2. 审查现有页面

| 检查点 | 修复方式与验证条件 |
| --- | --- |
| `UIScreen.main`、写死的屏幕宽高、启动时缓存大小 | 从当前容器计算布局。SwiftUI 优先使用自适应容器，确需测量时用 `GeometryReader` 或 `onGeometryChange`。UIKit 使用 Auto Layout、`view.bounds` 或当前窗口，并在布局阶段更新。运行中展开与合起时界面应立即适应。 |
| 通过手机型号、`userInterfaceIdiom` 或方向选择页面 | 用 size class 处理导航结构，用当前容器实际尺寸处理内容是否放得下。全屏内屏可能提供 regular 宽度，内屏也可能旋转，即使 App 声明了支持方向。实际读取 traits，并测试 Split View。拍摄等确需方向的模块继续使用对应框架提供的方向机制。 |
| 自绘底栏、固定右侧工具区、粗暴忽略安全区 | 优先交给系统导航容器。自绘前景按实际安全区与方向边距放置，背景按设计铺到边缘。逐边验证边距，覆盖左右两种分屏位置。 |
| 切换布局丢失正在执行的任务 | 检查视图树的条件分支、`.id(...)`、`UIHostingController` 生命周期、进入页面时启动的请求和重复创建的子控制器。用稳定的项目 ID 和模型保存选择、草稿和任务。 |
| 弹窗、键盘、Web 内容或自绘界面 | 检查 sheet、popover 锚点和悬浮按钮。UIKit 表单使用滚动与键盘布局指南。混合项目还要测试 WKWebView 或跨平台页面的 viewport、CSS 断点和原生安全区是否重复计算。 |

静态命中需要结合调用点确认，优先修公用容器的系统性问题和会阻断核心任务的缺陷。保留现有项目内有业务含义的尺寸或方向判断。[工程扫描命令](engineering.md) · [Apple 技术演讲](https://developer.apple.com/videos/play/tech-talks/111461/)

## 3. 选择实现方案

### 导航与垂直工具栏

- SwiftUI 用 `NavigationStack` 管理单栏流程，列表和详情用 `NavigationSplitView`，标签入口用 `TabView`。在现有导航容器上通过 `.toolbar` 声明动作。详情在宽布局可与列表并排，在窄布局能够返回列表。
- UIKit 用 `UINavigationController`、`UISplitViewController` 和 `UITabBarController` 承接导航。根据现有项目配置 `navigationItem` 或控制器上的 `toolbarItems`。SwiftUI 与 UIKit 混用时，由拥有当前流程的导航容器提供系统栏。
- 优先操作采用语义化位置。提供图标与本地化名称，验证垂直显示、横向显示和溢出菜单。标题专用项与自定义视图项可能无法垂直显示。需要调整时按 SDK 使用 `axisBehavior`、`visibilityPriority` 和溢出菜单 API，并确认返回、关闭、保存及编辑功能始终可达。
- 自绘组件确实需要感知垂直栏时，可读取 SwiftUI `toolbarVerticalEdge` 或 UIKit `verticalBarEdge`。sheet 根据所处显示区域与呈现位置可能采用不同栏方向。先体验系统行为，再决定是否调整呈现位置。

[Apple 开发文档](https://developer.apple.com/documentation/technologyoverviews/preparing-your-app-for-iphone-duo)

### 折痕、摄像头与自绘布局

| 情况 | 选用方案 |
| --- | --- |
| 列表和详情、普通 sheet／alert／popover、连续正文 | 使用原生组件并验证对应行为。连续滚动内容可跨折痕，主要交互控件保持可见和易点按。 |
| 两块内容需根据姿态重新排布 | iOS 27.1 可用 SwiftUI `ArrangementView` 或 UIKit `UIArrangementViewController`。两区需要同时可见时考虑 split。有前后景关系时考虑 overlay。若限制布局轴，给可能隐藏的次要内容保留入口。检查容器嵌套后两块内容是否仍然可达。 |
| 自绘编辑器、网格、浮动播放控件、边缘交互 | 从组件自身几何读取 `.division` 和 `.occlusion`。折痕属于 division，镜头遮挡属于 occlusion。只用 active 区域计算当前避让。在同一坐标系比较候选元素的实际交互框，并避免固定折痕宽度、比例、位置与方向。 |
| 拍照、视频通话或直播功能 | 先验证 Virtual Front Camera 是否满足能力要求。需要选择独立镜头时，以 Apple 的方向协调器和现有相机服务处理切换，检查权限、中断恢复、预览裁切、旋转、镜像以及录制连续性。双屏同时显示属于独立的相机功能，按相应场景与可用性实现。 |

内屏镜头区域会随镜头激活变化，区域变化可能早于尺寸或 size class 变化。UIKit 自绘组件可在自定义视图的 `updateConstraints()` 查询相应区域，以便系统在区域变化时重新调用。SwiftUI 默认对 RTL 区域坐标镜像。自绘使用物理坐标时，依据 API 的 `layoutDirectionBehavior` 对齐坐标。背景装饰可越过安全区，注意交互区域始终有效。[折叠布局演讲](https://developer.apple.com/videos/play/tech-talks/111463/) · [相机适配演讲](https://developer.apple.com/videos/play/tech-talks/111465/)

### 保留任务状态

1. 将选中的对象、导航路径、表单草稿、播放进度和上传任务放在稳定的视图模型、场景或持久化层，依据原有生命周期选择。
2. 将布局变化视作展示变化。SwiftUI 让宽、窄两种布局共享状态和任务。UIKit 尽量复用相关子控制器、模型及正在运行的工作，并按需更新约束。
3. 在输入到一半、键盘可见、语音朗读或正在上传时来回折叠。确认输入、导航、焦点和任务处理符合产品预期。验证迁移途中移除条目或取消请求时有明确的回退行为。

## 4. 多语言与无障碍

- 延续项目现有本地化体系。使用 String Catalog 的项目，将文案放入对应 `.xcstrings`，核对本地化 Key、模块与资源 Bundle。保留完整句子与插值，为译者说明上下文。用复数变体，不同语言按各自的规则处理，用区域感知格式化日期、数字、单位及金额。
- 让文字可以换行、拉伸界面或将操作换到下一行。外屏和分屏尤其容易暴露截断。确认系统栏图标有可读的本地化名称，空态、验证错误、权限提示和溢出菜单也能翻译。
- 使用 `leading`／`trailing` 并尊重 RTL。逐一判断图标是否具有阅读方向含义。检查混排账号、数字及标点，以及自绘折痕坐标与真实遮挡是否对齐。
- 用最大辅助字体尺寸验证阅读与操作，检查 VoiceOver 的顺序、控件名称、焦点连续性和可达性。用 Accessibility Inspector 或 UI 测试的 `performAccessibilityAudit` 补充人工验证。
- 先用 Xcode Scheme 的 App Language 选 Double-Length 和 RTL 伪语言查布局，再用真实目标语言与 App Region 确认渲染和格式。可参考英语、简体中文、日语、德语及阿拉伯语示例，实际发布语言以产品需求为准。

[五语字符串示例](../assets/Localizable.xcstrings) · [Apple 本地化指南](https://developer.apple.com/documentation/xcode/preparing-your-interface-for-localization) · [Apple 无障碍测试指南](https://developer.apple.com/documentation/accessibility/performing-accessibility-audits-for-your-app)

## 5. 验收矩阵

在 Xcode 选择 iPhone Duo 模拟器，打开 Device Hub。用设备上的控制项合起、展开、旋转和半折。每个用例从正常入口进入，记录构建、运行时、设备姿态、窗口位置、语言／地区、字体尺寸与证据。优先跑下表的交叉组合，再按功能补充覆盖。

| ID | 条件与操作 | 通过标准 |
| --- | --- | --- |
| D01 | 外屏竖向和受支持的横向打开核心页面 | 主要按钮可见可用，标签导航与溢出动作可访问，无裁切。 |
| D02 | 内屏全展，切换方向；列表进入详情再返回 | 列宽合适，导航可达，内屏旋转时无空白、跳回首页或重复请求。 |
| D03 | 编辑含未提交草稿的详情，键盘可见时展开、半折、合起 | 原条目与草稿保留，键盘及焦点符合设计，保存只执行一次。 |
| D04 | 内屏做书本式与桌面式半折；打开 sheet、popover、alert 或自绘控件 | 交互控件可见且避开 active 区域，弹层可操作、可关闭。 |
| D05 | 内屏支持 Split View 时，在窗口左右位置各跑一遍导航和滚动 | 侧栏和非对称安全区正确，触控或滚动无冲突。 |
| D06 | 在外屏和至少一个半折姿态测试长伪语言、RTL 与最大辅助字体 | 文案、控件、溢出操作和 VoiceOver 可用。用实际支持的重点语言复验。 |
| D07 | 有相机或录制功能时，在真机切换内外屏并打开、关闭内屏相机 | 镜头、预览、镜像、遮挡与中断恢复正确。保存或取消后的状态一致。 |
| D08 | 最低支持 iOS 的普通 iPhone、当前 iOS 的普通 iPhone；若支持，再跑 iPad／Mac Catalyst | 核心路径和版本回退正常，原平台行为通过回归。 |

可自动化布局计算、导航和输入状态断言，以及现有项目支持的截图回归。折叠姿态切换用 Device Hub 或真机复验。查当前模拟器版本的限制，涉及相机、扩展或姿态相关物理行为时记录真机结果。[Xcode 27.1 发行说明](https://developer.apple.com/documentation/xcode-release-notes/xcode-27_1-release-notes)

## 6. 交付与发布

- 提交审查结果时，每条附严重程度、复现条件、用户影响、文件与行号、修改方案、验收用例和证据。区分运行实测与代码推断。
- 提交实现时，记录变更页面、构建 SDK、最低版本与兼容分支。分别列出构建和界面运行结果，并标注通过、失败、未执行或不适用。草稿丢失、核心入口不可达、崩溃等问题应优先解决。
- 需要上架时，在 App Store Connect 根据当前规则准备内外屏截图及支持语言的商店素材。Apple 当前截图规格列出从 2027 年 4 月起，对使用 iOS 27.1 SDK 或之后版本的 App 要求 iPhone Duo 截图。提交前以当时规格和后台实际要求为准。上传给审核需按用户授权执行。[App Store Connect 截图规格](https://developer.apple.com/help/app-store-connect/reference/app-information/screenshot-specifications/)

报告记录格式

```text
用例 D03 | 构建与 SDK | 运行设备与 iOS | 外屏→内屏→外屏
语言与地区 | 字体尺寸 | 入口与操作步骤 | 预期结果
观察结果 | 通过／失败／未执行／不适用 | 截图、视频或日志
```
