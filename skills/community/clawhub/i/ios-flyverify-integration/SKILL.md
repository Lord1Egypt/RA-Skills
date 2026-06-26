---
name: ios-flyverify-integration
description: 面向 iOS 工程的 MobTech FlyVerify(秒验) 集成 skill。默认先扫描工程，优先使用 CocoaPods，以最小改动完成依赖接入、隐私合规、一键登录流程接线和项目内说明文档落地。
tags:
  - ios
  - flyverify
  - 秒验
  - sdk-integration
  - mobtech
  - one-click-login
  - cocoapods
  - privacy
  - objective-c
  - swift
---

# iOS FlyVerify 集成 Skill

当用户希望把 MobTech FlyVerify 集成到 iOS 工程，或者排查已有 FlyVerify 接入问题时，使用本 skill。

## 适用场景

当用户提到以下任一主题时，使用本 skill：

- iOS FlyVerify 集成
- iOS 秒验接入
- iOS 一键登录
- MobTech 秒验一键登录
- FlyVerify CocoaPods 配置
- FlyVerify `Info.plist` 配置
- FlyVerify 隐私合规
- `agreePrivacy` 调用时机
- `preLogin` / `openAuthPageWithModel` 用法
- 秒验授权页自定义
- 秒验 token 置换手机号
- 帮我在 iOS 项目里增加一键登录
- 帮我把 FlyVerify 接进现有 iOS 工程

如果用户问题明确与 iOS 秒验接入、工程配置、隐私合规、一键登录流程或授权页 UI 定制有关，应优先使用本 skill。

## 输出语言

- 默认使用中文与用户沟通
- 代码、配置键名、类名、命令名保持原文
- 回答尽量短，先给结论，再给动作

## 官方资料

优先使用以下线上资料，不依赖本机资料路径：

主文档：

- [MobTech 文档中心](https://www.mob.com/wiki/list)
- [秒验产品页](https://www.mob.com/mobService/secverify)
- [SDK 下载中心](https://www.mob.com/download)
- [集成指南](https://www.mob.com/wiki/detailed?wiki=531&id=78)
- [SDK API 文档](https://www.mob.com/wiki/detailed?wiki=297&id=78)
- [合规指南](https://www.mob.com/wiki/detailed?wiki=217&id=78)
- [秒验隐私政策](https://policy.zztfly.com/sdk/verify/privacy)
- [创建应用流程](https://www.mob.com/wiki/detailed?wiki=538&id=78)
- [秒验审核流程](https://www.mob.com/wiki/detailed?wiki=159&id=78)
- [服务端接入文档](https://www.mob.com/wiki/detailed?wiki=157&id=78)
- [秒验 SDK 扩展业务功能设置](https://www.mob.com/wiki/detailed?wiki=669&id=78)
- [其它 App 数据采集主动控制器配置](https://www.mob.com/wiki/detailed?wiki=675&id=714)
- [App Store Connect 后台配置参考文档](https://www.mob.com/wiki/detailed?wiki=289&id=172)
- [秒验 Demo](https://github.com/MobClub/FlyVerify_For_iOS)

如果某个深链失效，先从 [MobTech 文档中心](https://www.mob.com/wiki/list) 搜索对应标题，不要回退到本机绝对路径。

## 已确认的官方事实

以下信息已经可作为执行依据，不需要再猜测：

- 默认开发环境要求为 `Xcode 9.1.0+`、`iOS 8.0+`
- 官方支持 `CocoaPods` 和手动导入两种集成方式
- 默认 Pod 为 `pod 'FlyVerify'`
- 工程需要链接 `libsqlite3.tbd`、`libc++.tbd`、`libz.1.2.5.tbd`
- `Other Linker Flags` 需要添加 `-ObjC`
- `Info.plist` 需要配置 `flyverifykey` 与 `flyverifysecret`
- 严格隐私模式需要在默认 `plist` 中添加 `FlyVerifyPLevel = 2`
- 如果项目全局禁止 HTTP，需要为以下域名配置 ATS 白名单：
  - `zzx9.cn`
  - `cmpassport.com`
  - `id6.me`
  - `wostore.cn`
  - `mdn.open.wo.cn`
- `agreePrivacy` 是 FlyVerify 业务起点，必须在用户同意隐私政策后、使用 SDK 能力前调用
- `preLogin` 回调在全局队列，`error == nil` 才视为成功
- `openAuthPageWithModel` 的 `uiConfigure.currentViewController` 为必传
- 授权页关闭可由 SDK 自动处理，也可通过 `manualDismiss = @(YES)` 后手动调用 `finishLoginVcAnimated:Completion:`
- 一键登录成功后 SDK 返回 `opToken`、`operator`、`token`
- 真实手机号需要开发者服务端调用秒验服务端接口完成置换，客户端不能直接得到手机号
- 一键登录能力依赖运营商网关取号，必须在手机开启移动蜂窝网络时使用
- 文档明确建议授权页 UI 定制参考官方 Demo
- 严格隐私模式和隐私 API 支持情况必须结合线上合规文档与当前 `Podfile.lock` 中实际安装版本确认，不要只凭本地缓存判断
- 接入代码必须同时支持 Objective-C 与 Swift 工程；Swift 工程优先通过桥接头调用官方 Objective-C API

## 文档未明确，需向用户确认

以下内容在当前资料里没有被稳定、明确地定义，禁止猜：

- 是否支持 Swift Package Manager
- 是否需要 Bitcode、Privacy Manifest 或额外苹果隐私文件
- 用户项目应该使用 `Info.plist` 配置读取，还是代码显式 `initKey:secret:privacyLevel:`
- 用户具体要不要开启授权页自定义

如果缺这些信息且会阻塞安全修改，必须明确写：

`文档未明确，需向用户确认`

## 默认执行策略

- 默认集成方式：`CocoaPods`
- 默认先扫描工程，再给改动方案
- 默认优先复用工程已有隐私弹窗和登录入口，不新造页面
- 默认先生成最小 Excel 模板，再等用户填写
- 默认不在 Excel 中收集 `Bundle ID`、Target 名称、入口类名、`Info.plist` 路径，因为这些应由扫描工程自动推断
- 默认把 FlyVerify 能力接入放在用户已同意隐私政策之后
- 默认不主动询问是否启用扩展业务主动控制器；仅在最终项目文档中说明这项可选能力
- 服务端 token 置换接口属于后续业务步骤，本轮客户端集成只保留注释占位，不追问接口域名、鉴权方式或返回结构
- 默认不运行 `pod install`、`xcodebuild` 或其他会改动依赖状态的命令，先展示计划，再执行
- 默认不把 `Pods/` 提交进项目；如项目未忽略 `Pods/`，补充 `.gitignore`，保留 `Podfile` 与 `Podfile.lock`
- 一次只问用户一个阻塞问题

## 执行流程

严格按以下顺序推进：

1. 先扫描工程，再判断接入方式。
2. 先生成或读取配置模板，再确定静态配置。
3. 先展示最小改动计划，再修改文件。
4. 依赖安装前先征求确认。
5. 完成后补项目内说明文档。

## 第一步：扫描工程

优先扫描以下内容：

- `.xcodeproj` / `.xcworkspace`
- `Podfile`
- `Podfile.lock`
- `Package.swift`
- `AppDelegate` / `SceneDelegate` / SwiftUI `@main`
- `Info.plist`
- 隐私政策弹窗或同意回调位置
- 登录页、手机号登录页、现有一键登录入口
- Objective-C / Swift / 混编类型，以及是否已有 Bridging Header
- 是否已有 `FlyVerify`、`FVSDKHyVerify`、`FlyVerifyC`、`flyverifykey`、`flyverifysecret`、`FlyVerifyPLevel`
- `.gitignore` 是否忽略 `Pods/`
- `.xcworkspace` 是否包含 `contents.xcworkspacedata`

推荐命令：

- `rg --files -g '*.xcodeproj' -g '*.xcworkspace' -g 'Podfile' -g 'Podfile.lock' -g 'Package.swift' -g '*Info.plist' -g '.gitignore'`
- `rg --files -g '*.m' -g '*.h' -g '*.mm' -g '*.swift'`
- `rg -n 'FlyVerify|FVSDKHyVerify|FlyVerifyC|flyverifykey|flyverifysecret|FlyVerifyPLevel|agreePrivacy|preLogin|openAuthPageWithModel|SWIFT_OBJC_BRIDGING_HEADER'`

扫描后先给一段简短结论，至少包含：

- 当前工程依赖方式
- 当前入口结构
- 当前代码语言形态：Objective-C / Swift / 混编
- Swift 工程是否已有 Bridging Header
- 是否已有 FlyVerify 残留
- 是否已经有隐私同意链路
- CocoaPods 状态：是否有有效 `Podfile`、`Podfile.lock`、`Pods/`、`*.xcworkspace/contents.xcworkspacedata`
- 下一步是生成模板还是读取已有 `FlyVerify_iOS_Config.xlsx`

## 第二步：生成并读取配置模板

### 2-1 模板生成

如果用户项目根目录还没有 `FlyVerify_iOS_Config.xlsx`：

1. 运行本 skill 目录下的 `assets/generate_excel_template.py`
2. 将生成的 `assets/FlyVerify_iOS_Config_Template.xlsx` 复制到用户项目根目录
3. 在用户项目根目录命名为 `FlyVerify_iOS_Config.xlsx`

### 2-2 向用户说明填写项

必须明确告诉用户只需要填写这些最小字段：

- `appKey`
- `appSecret`
- 秒验审核是否已通过
- 是否需要自定义授权页

同时明确说明以下内容不需要填表：

- `Bundle ID`
- `Target`
- `Info.plist` 路径
- 隐私弹窗类名
- 授权页按钮落点
- 是否启用扩展业务主动控制器

其中工程信息应由 Agent 扫描后推断；扩展业务主动控制器不作为前置配置项，只在最终文档中说明。

### 2-3 配置校验

读取 `FlyVerify_iOS_Config.xlsx` 后，至少校验：

- `appKey`：必填，按字符串处理，不做数值推断
- `appSecret`：必填，按字符串处理，不做数值推断
- `秒验审核`：必须明确是 `是` / `否`
- `授权页自定义`：必须明确是 `是` / `否`

如不合法，列出具体问题并要求用户修正，不要继续改工程。

## 第三步：扫描后推断工程接入点

读取配置后，再次结合工程做推断：

- 优先识别主要 App Target
- 推断 Objective-C / Swift / 混编
- 记录当前工程要使用 Objective-C 示例、Swift 示例还是两者都需要
- Swift 工程需检查是否已有 `{Target}-Bridging-Header.h` 与 `SWIFT_OBJC_BRIDGING_HEADER`
- 定位疑似隐私同意回调位置，后续仍必须向用户确认
- 推断一键登录入口页或手机号登录页
- 推断当前是否已有 CocoaPods 体系
- 推断是否已有 ATS 配置、`-ObjC`、系统库链接
- 判断已有 `*.xcworkspace` 是否有效；只有目录但缺少 `contents.xcworkspacedata` 时，应运行 `pod install` 重新生成
- 判断已有 `Pods/` 是否完整；如果只有空 framework 目录或缺少 `Info.plist`、Headers、binary，不要按手动 SDK 接入硬改工程，应优先重新 `pod install`

以下信息必须分两类处理：

### 必须在修改前确认的信息

- 多 Target 时应该接入哪个 App Target
- 用户同意隐私政策后的回调位置。即使扫描到疑似隐私弹窗，也要让用户确认 `agreePrivacy` 应插入到哪个“同意”回调
- 用户明确不想用 CocoaPods，必须改走手动导入

### 可以在扫描后逐步确认的信息

- 是否需要自定义授权页样式
- `preLogin` 放在 `viewDidLoad`、按钮前预热还是其他业务时机

如果必须确认，串行一次只问一个问题。

## 第四步：展示最小改动计划

修改前必须向用户展示本次最小改动计划，通常包括：

- `Podfile`：按需加入 `pod 'FlyVerify'`
- `.gitignore`：按需加入 `Pods/`
- `Info.plist`：写入 `flyverifykey`、`flyverifysecret`、`FlyVerifyPLevel`
- Xcode 构建设置：补 `-ObjC`
- Swift 工程：新增或复用 Bridging Header，并配置 `SWIFT_OBJC_BRIDGING_HEADER`
- 视情况补 ATS 白名单或提示用户已有配置可复用
- 在隐私同意后插入 `agreePrivacy`
- 在登录链路中接入 `preLogin` 与 `openAuthPageWithModel`
- 在 token 成功回调后保留服务端置换手机号逻辑注释占位
- 生成项目内 `FlyVerify_README.md`

没有确认前，不要直接改。

## 第五步：执行工程修改

### 5-1 依赖接入

默认优先 `CocoaPods`：

- 在正确的 target 下加入 `pod 'FlyVerify'`
- 如项目没有有效 workspace，运行 `pod install` 后确认 `*.xcworkspace/contents.xcworkspacedata` 已生成
- `pod install` 可能需要写用户级 CocoaPods cache；如遇 `~/Library/Caches/CocoaPods` 权限错误，应按当前执行环境申请授权后重试
- 若 `pod install` 修改 `.xcodeproj`，不要再手写重复的 Pods framework、xcconfig、shell script phase
- 只有用户确认后才执行 `pod install`

如果用户明确要求手动导入：

- 按官方资料把下载的 SDK 拖入工程
- 检查并补系统库、`-ObjC` 与 `Info.plist`

### 5-2 `Info.plist` 配置

默认写入或校正：

- `flyverifykey`
- `flyverifysecret`
- `FlyVerifyPLevel = 2`

ATS 处理规则：

- 若工程已全局允许 HTTP，不重复扩大权限
- 若工程禁用 HTTP，则按官方域名白名单最小化添加
- 若工程已有等价白名单，复用现有配置，不重复写

### 5-3 隐私合规接入

在用户同意隐私政策后、首次使用 FlyVerify 能力前接入：

```objective-c
#import <FlyVerifyCSDK/FlyVerifyCSDK.h>
[FlyVerifyC agreePrivacy:YES onResult:nil];
```

Swift 工程必须先确保桥接头可访问 SDK 头文件：

```objc
#import <FlyVerifyCSDK/FlyVerifyCSDK.h>
#import <FlyVerify/FVSDKHyVerify.h>
```

然后在用户同意隐私政策后的 Swift 回调中调用：

```swift
FlyVerifyC.agreePrivacy(true, onResult: nil)
```

如果用户明确采用代码初始化方案，才补：

```objective-c
[FlyVerifyC initKey:@"<appKey>" secret:@"<appSecret>" privacyLevel:2];
```

否则优先沿用 `Info.plist` 配置，不同时强塞两套初始化方案。

### 5-4 登录流程接入

建议流程：

1. 用户同意隐私政策后调用 `agreePrivacy`
2. 在即将进入一键登录前调用 `preLogin`
3. 在主线程拉起 `openAuthPageWithModel`
4. 成功返回 `token` / `opToken` 后保留服务端置换手机号注释占位

接入时必须注意：

- `preLogin` 成功判断以 `error == nil` 为准
- `preLogin` 回调不是主线程，涉及 UI 必须切回主线程
- `currentViewController` 必须传当前页面或顶层页面
- 如果 `manualDismiss = @(YES)`，成功或失败后按业务自行关闭授权页
- Objective-C 与 Swift 工程都要提供对应语言代码；Swift 工程通过桥接头调用 `FVSDKHyVerify` 与 `FVSDKHyUIConfigure`
- Swift 调用 `openAuthPageWithModel:openAuthPageListener:cancelAuthPageListener:oneKeyLoginListener:` 时，首参标签应为 `withModel:`，不是 `with:`
- 服务端 token 置换接口的具体域名、鉴权方式、返回结构不在当前客户端集成步骤中追问，只在代码中以 `TODO` 注释标明

### 5-5 授权页 UI 定制

只有用户明确需要时，才继续改 UI。

优先通过以下方式做最小定制：

- `FVSDKHyUIConfigure` 基本属性
- `FVSDKVerifyDelegate`
- `fvVerifyAuthPageViewDidLoad:userInfo:` 中设置布局或自定义控件

若用户要复杂弹窗、暗黑模式、横竖屏、自定义 loading、协议页接管，优先提示参考官方 Demo 与线上文档：

- [秒验 Demo](https://github.com/MobClub/FlyVerify_For_iOS)
- [MobTech 文档中心](https://www.mob.com/wiki/list)

## 第六步：验证与说明文档

完成改动后，按条件执行：

- 若用户确认，可运行 `pod install`
- 若环境允许，可运行一次构建验证；FlyVerify 依赖运营商库，优先验证 `generic/platform=iOS` 真机目标
- 不要把模拟器构建失败直接等同于集成失败；若错误类似 `building for 'iOS-simulator', but linking in object file ... built for 'iOS'`，说明某运营商 framework 只有真机切片，应改用真机目标验证
- Xcode 15+ 如遇 CocoaPods `[CP] Copy Pods Resources` 被 User Script Sandboxing 拦截，可在目标 Build Settings 中将 `ENABLE_USER_SCRIPT_SANDBOXING = NO`，或用等价命令行参数验证
- 如果普通沙箱下 `xcodebuild` 无法访问 CoreSimulator 或 Xcode 用户目录，应按当前环境申请授权后重试
- 若无法构建，明确说明未验证的原因

然后生成项目内 `FlyVerify_README.md`，至少包含：

- 本次改动点
- `appKey` / `appSecret` 的配置位置
- `agreePrivacy` 的调用位置
- `preLogin` 与授权页拉起位置
- Objective-C / Swift 支持情况与桥接头配置情况
- CocoaPods 版本信息：`Podfile`、`Podfile.lock`、实际安装的 FlyVerify / FlyVerifyCSDK 版本
- 构建验证结果：真机目标、模拟器限制、剩余 warning
- 服务端 token 置换属于后续业务步骤，当前只保留注释占位
- 扩展业务主动控制器是可选能力；如未来需要控制地理位置、WiFi、IP 等扩展业务数据采集，可参考官方扩展业务文档接入 `FlyVerifyCPrivacyDelegate`
- 常见错误码排查入口
- 官方文档链接清单

## 常见错误排查原则

遇到失败时优先检查：

- 秒验审核是否已通过
- 手机是否开启移动蜂窝网络
- `agreePrivacy` 是否在隐私同意后已调用
- `currentViewController` 是否为当前顶层可 `present` 的 VC
- `flyverifykey` / `flyverifysecret` 是否和后台一致
- ATS 是否拦截了运营商或 SDK 请求
- Swift 首参标签是否使用了 `withModel:`
- 是否用真机目标验证，而不是只看模拟器构建结果
- CocoaPods workspace 是否有效生成

## 与用户沟通的硬约束

- 一次只问一个阻塞问题
- 没有阻塞就不要追问，直接推进
- 每次修改前先展示计划
- 执行 `pod install` 或构建前先征求确认
- 如果某项无需修改，要明确说“无需修改”
