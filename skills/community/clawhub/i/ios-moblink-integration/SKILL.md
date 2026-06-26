---
name: ios-moblink-integration
description: 面向 iOS 工程的 MobTech MobLink 集成 skill。默认先扫描工程，优先使用 CocoaPods，以最小改动完成场景还原依赖接入、Info.plist 配置、隐私合规、getMobId 制作场景、恢复代理回调和项目内说明文档落地。
tags:
  - ios
  - moblink
  - deeplink
  - scene-restore
  - mobtech
  - sdk-integration
  - cocoapods
  - privacy
  - objective-c
  - swift
---

# iOS MobLink 集成 Skill

当用户希望把 MobTech MobLink 集成到 iOS 工程，或者排查已有 MobLink 接入问题时，使用本 skill。

## 适用场景

当用户提到以下任一主题时，使用本 skill：

- iOS MobLink 集成
- MobTech MobLink 接入
- iOS 深度链接 / Deeplink
- iOS 场景还原
- `mob_linksdk_pro`
- MobLink `Info.plist` 配置
- MobLink 隐私合规
- `uploadPrivacyPermissionStatus` 调用时机
- `getMobId` / `MLSDKScene` / `MobLink setDelegate:`
- `IMLSDKWillRestoreScene` / `UIViewController+MLSDKRestore`
- MobLink 扩展业务主动控制器
- 帮我在 iOS 项目里增加场景还原能力
- 帮我把 MobLink 接进现有 iOS 工程

如果用户问题明确与 iOS MobLink 接入、工程配置、场景制作、场景还原、隐私合规或扩展业务采集控制有关，应优先使用本 skill。

## 输出语言

- 默认使用中文与用户沟通
- 代码、配置键名、类名、命令名保持原文
- 回答尽量短，先给结论，再给动作

## 官方资料

优先使用以下线上资料，不依赖本机资料路径：

- [MobTech 文档中心](https://www.mob.com/wiki/list)
- [MobLink 产品简介](https://www.mob.com/wiki/detailed?wiki=161&id=34)
- [创建应用流程](https://www.mob.com/wiki/detailed?wiki=478&id=34)
- [MobLink 后台与项目配置](https://www.mob.com/wiki/detailed?wiki=527&id=34)
- [iOS 集成指南](https://www.mob.com/wiki/detailed?wiki=83&id=34)
- [iOS SDK API](https://www.mob.com/wiki/detailed?wiki=553&id=34)
- [iOS 合规指南](https://www.mob.com/wiki/detailed?wiki=220&id=34)
- [MobLink 扩展业务功能设置](https://www.mob.com/wiki/detailed?wiki=673&id=34)
- [Web 集成](https://www.mob.com/wiki/detailed?wiki=525&id=34)
- [App Store Connect 后台隐私数据项配置](https://www.mob.com/wiki/detailed?wiki=574&id=34)
- [其它 App 数据采集主动控制器配置](https://www.mob.com/wiki/detailed?wiki=675&id=714)
- [MobLink 隐私政策](https://policy.zztfly.com/sdk/link/privacy)


## 已确认的官方事实

以下信息已经可作为执行依据，不需要再猜测：

- 官方支持手动导入 SDK 和 CocoaPods 两种集成方式
- 默认开发环境要求为 `Xcode 9.1.0+`、`iOS 8.0+`
- CocoaPods 依赖为 `pod 'mob_linksdk_pro'`
- 手动导入需要 `MobLinkPro.framework` 与 `MOBFoundation.framework`
- 工程需要链接 `libsqlite3`、`libz1.2.5`、`libc++`
- `Info.plist` 需要配置 `MOBAppKey` 与 `MOBAppSecret`
- 严格合规方案要求默认 `plist` 中增加 `MOBNetLater = 2`
- `uploadPrivacyPermissionStatus` 是 MobSDK 业务起点，必须在用户同意隐私政策后、使用 SDK 能力前调用
- 可通过 `uploadPrivacyPermissionStatus:onResult:` 回传隐私授权结果
- 可通过 `uploadPrivacyPermissionStatus:privacyDataDelegate:onResult:` 同时接入 `MOBFoundationPrivacyDelegate` 主动控制器
- 需要在 App 启动链路中调用 `[MobLink setDelegate:self]` 设置场景恢复代理
- 制作场景使用 `MLSDKScene` 和 `[MobLink getMobId:result:]`
- iOS 3.0.0 以上推荐使用 `[MLSDKScene sceneForPath:params:]`
- 需要恢复的控制器可实现 `UIViewController+MLSDKRestore` 中的 `initWithMobLinkScene:`
- 场景还原回调 `IMLSDKWillRestoreScene:Restore:` 一旦实现，必须执行 `restoreHandler`
- MobLink iOS 扩展业务支持地域精细化运营、脱敏设备唯一性标识、网络链路选择与优化
- 扩展业务主动控制器通过自定义类遵守 `MOBFoundationPrivacyDelegate` 实现

## 文档未明确，需向用户确认

以下内容在当前资料里没有被稳定、明确地定义，禁止猜：

- 是否支持 Swift Package Manager
- 是否需要 Privacy Manifest 或额外苹果隐私文件
- 用户项目应该使用 CocoaPods 还是已存在的手动导入体系
- 用户是否本次就要配置 URL Scheme、Universal Link 或 Associated Domains
- MobLink 后台里的 iOS 页面名称、渠道标识、路径与业务控制器映射关系
- 项目中应该在哪个业务入口制作 MobId 和拼接分享链接
- Web 端是否已经集成 MobLink JS 模块

如果缺这些信息且会阻塞安全修改，必须明确写：

`文档未明确，需向用户确认`

## 默认执行策略

- 默认集成方式：`CocoaPods`
- 默认先扫描工程，再给改动方案
- 默认优先复用工程已有隐私弹窗、App 启动入口和路由体系
- 默认先生成最小 Excel 模板，再等用户填写
- 默认不在 Excel 中收集 `Bundle ID`、Target 名称、`Info.plist` 路径、入口类名，因为这些应由扫描工程自动推断
- 默认不在 Excel 中收集业务控制器路径、分享入口、Web 落地页和恢复路由位置，这些必须结合工程扫描后逐步确认
- 默认不在 Excel 中收集扩展业务主动控制器配置；仅在 README 中保留官方文档链接，真正需要时再串行确认
- 默认不主动启用扩展业务主动控制器；仅当用户明确需要限制位置、IDFA、IDFV、WiFi、IP 等采集时才进入该分支
- 默认不运行 `pod install`、`xcodebuild` 或其他会改动依赖状态的命令，先展示计划，再执行
- 默认不把 `Pods/` 提交进项目；如项目未忽略 `Pods/`，补充 `.gitignore`，保留 `Podfile` 与 `Podfile.lock`
- 一次只问用户一个阻塞问题

## 执行流程

严格按以下顺序推进：

1. 先扫描工程，再判断接入方式。
2. 先生成或读取配置模板，再确定静态配置。
3. 先展示最小改动计划，再修改文件。
4. 依赖安装前先征求确认。
5. 基础 SDK 与隐私合规完成后，再进入场景制作和场景还原业务接线。
6. 完成后补项目内说明文档。

## 第一步：扫描工程

优先扫描以下内容：

- `.xcodeproj` / `.xcworkspace`
- `Podfile`
- `Podfile.lock`
- `Package.swift`
- `AppDelegate` / `SceneDelegate` / SwiftUI `@main`
- `Info.plist`
- 现有 URL Scheme、Associated Domains、Universal Link 配置
- 现有路由、分享、网页落地页、深链处理代码
- 隐私政策弹窗或同意回调位置
- Objective-C / Swift / 混编类型，以及是否已有 Bridging Header
- 是否已有 `MobLink`、`MobLinkPro`、`MOBAppKey`、`MOBAppSecret`、`MOBNetLater`、`uploadPrivacyPermissionStatus`
- `.gitignore` 是否忽略 `Pods/`
- `.xcworkspace` 是否包含 `contents.xcworkspacedata`

推荐命令：

- `rg --files -g '*.xcodeproj' -g '*.xcworkspace' -g 'Podfile' -g 'Podfile.lock' -g 'Package.swift' -g '*Info.plist' -g '*.entitlements' -g '.gitignore'`
- `rg --files -g '*.m' -g '*.h' -g '*.mm' -g '*.swift'`
- `rg -n 'MobLink|MobLinkPro|MLSDKScene|IMLSDKRestoreDelegate|IMLSDKWillRestoreScene|UIViewController\\+MLSDKRestore|MOBAppKey|MOBAppSecret|MOBNetLater|uploadPrivacyPermissionStatus|CFBundleURLSchemes|com.apple.developer.associated-domains|SWIFT_OBJC_BRIDGING_HEADER'`

扫描后先给一段简短结论，至少包含：

- 当前工程依赖方式
- 当前入口结构
- 当前代码语言形态：Objective-C / Swift / 混编
- Swift 工程是否已有 Bridging Header
- 是否已有 MobLink 残留
- 是否已经有隐私同意链路
- 是否已有深链、Universal Link 或路由体系
- CocoaPods 状态：是否有有效 `Podfile`、`Podfile.lock`、`Pods/`、`*.xcworkspace/contents.xcworkspacedata`
- 下一步是生成模板还是读取已有 `MobLink_iOS_Config.xlsx`

## 第二步：生成并读取配置模板

### 2-1 模板生成

如果 `{path}` 下还没有 `MobLink_iOS_Config.xlsx`：

1. 运行本 skill 目录下的 `assets/generate_excel_template.py`
2. 将生成的 `assets/MobLink_iOS_Config_Template.xlsx` 复制到 `{path}` 下
3. 在 `{path}` 下命名为 `MobLink_iOS_Config.xlsx`

### 2-2 向用户说明填写项

必须明确告诉用户只需要填写这些最小字段：

- `appKey`
- `appSecret`
- `needUniversalLink`

同时明确说明以下内容不需要填表：

- `Bundle ID`
- Target
- `Info.plist` 路径
- App 启动入口类名
- 隐私弹窗类名
- 场景恢复代理方法位置
- 业务控制器路径
- `getMobId` 调用入口
- Web 落地页地址
- 扩展业务主动控制器配置

其中工程信息应由 Agent 扫描后推断；业务落点、页面路径和 Web 配置必须在基础接入完成后按单个阻塞问题逐步确认。

### 2-3 配置校验

读取 `MobLink_iOS_Config.xlsx` 后，至少校验：

- `appKey`：必填，按字符串处理，不做数值推断
- `appSecret`：必填，按字符串处理，不做数值推断
- `needUniversalLink`：必须明确是 `是` / `否`

如不合法，列出具体问题并要求用户修正，不要继续改工程。

## 第三步：扫描后推断工程接入点

读取配置后，再次结合工程做推断：

- 优先识别主要 App Target
- 推断 Objective-C / Swift / 混编
- 记录当前工程要使用 Objective-C 示例、Swift 示例还是两者都需要
- Swift 工程需检查是否已有 `{Target}-Bridging-Header.h` 与 `SWIFT_OBJC_BRIDGING_HEADER`
- 定位疑似隐私同意回调位置，后续仍必须向用户确认
- 推断当前是否已有 CocoaPods 体系
- 推断当前是否已有 URL Scheme、Associated Domains、Universal Link 或 App 内路由代码
- 推断最合适的场景恢复代理持有者，优先为 App 启动入口或现有深链路由中心

如果存在多个候选入口，只问一个阻塞问题：

`我找到多个可能的场景恢复入口：A、B。你希望 MobLink 恢复回调接到哪一个？`

## 第四步：展示最小修改计划

修改前必须展示计划并等待用户确认。

计划至少覆盖：

- `Podfile`：添加 `pod 'mob_linksdk_pro'`
- `Info.plist`：添加或更新 `MOBAppKey`、`MOBAppSecret`、`MOBNetLater = 2`
- 系统库：提示 Xcode 需链接 `libsqlite3`、`libz1.2.5`、`libc++`
- App 启动入口：导入 MobLink/MobSDK 头文件，设置 `MobLink` delegate
- 隐私同意回调：在用户同意后调用 `uploadPrivacyPermissionStatus`
- 场景恢复代理：实现或接线 `IMLSDKRestoreDelegate`
- 项目内说明文档：生成 `MobLink_README.md`

如果用户选择 `needUniversalLink = 是`，计划中只写“检查并补充 Associated Domains / URL Scheme 的项目配置建议”，不要猜具体域名；具体 Host 必须从 MobLink 后台配置或用户提供的信息确认。

## 第五步：执行基础 SDK 接入

### 5-1 Podfile

优先在已有 App Target 的 `target` 块中添加：

```ruby
pod 'mob_linksdk_pro'
```

如果已有该依赖，不重复添加。

如果项目没有 `Podfile`，先说明将创建最小 `Podfile`，并展示内容等待确认。

如果项目明确使用手动导入，不强行改为 CocoaPods；改为输出手动集成检查清单：

- `MobLinkPro.framework`
- `MOBFoundation.framework`
- `libsqlite3`
- `libz1.2.5`
- `libc++`

### 5-2 Info.plist

写入或更新：

- `MOBAppKey` = Excel 中的 `appKey`
- `MOBAppSecret` = Excel 中的 `appSecret`
- `MOBNetLater` = `2`

保留已有无关配置。

### 5-3 App 启动入口

Objective-C 工程优先使用：

```objc
#import <MobLinkPro/MobLink.h>
#import <MobLinkPro/IMLSDKRestoreDelegate.h>
```

在合适入口调用：

```objc
[MobLink setDelegate:self];
```

如果 AppDelegate 需要承载恢复代理，声明应包含：

```objc
<IMLSDKRestoreDelegate>
```

Swift 工程若需要调用 Objective-C SDK：

- 优先复用现有 Bridging Header
- 没有 Bridging Header 时，先展示新增方案并等待确认
- Header 中只加入实际需要的 MobLink 头文件，不导入无关 SDK

## 第六步：隐私合规接线

必须在用户同意隐私政策后、使用 MobLink 能力前调用。

在插入任何隐私授权代码前，必须先向用户说明：

```text
根据 MobTech 隐私合规要求和中国区 App 上架规范，使用 MobLink 需要在用户同意隐私政策后才能初始化或使用 SDK。

你需要在 App 中：
1. 首次启动时展示《隐私政策》弹窗
2. 用户点击“同意”按钮后，调用隐私授权代码
3. 用户点击“不同意”则不应调用 MobLink SDK

请告知我：用户点击隐私政策“同意”按钮的回调代码在哪个文件、哪个方法中？
```

如果扫描工程已经找到明显候选位置，只能问：

`我找到疑似隐私同意回调：{file}:{method}。是否把 MobLink 隐私授权回传放在这里？`

用户未确认前，不得把 `uploadPrivacyPermissionStatus` 接入按钮、启动入口或任何占位方法。

通用方案：

```objc
#import <MOBFoundation/MobSDK+Privacy.h>

[MobSDK uploadPrivacyPermissionStatus:YES onResult:^(BOOL success) {
    // 业务逻辑不要依赖 success，建议调用后继续业务流程
}];
```

如果用户明确需要限制扩展业务数据采集，再接入主动控制器：

```objc
#import <MOBFoundation/MOBFoundation.h>

MobCustomController *privacyDataService = [MobCustomController new];
[MobSDK uploadPrivacyPermissionStatus:YES privacyDataDelegate:privacyDataService onResult:^(BOOL success) {
}];
```

主动控制器可覆盖的数据项包括：

- 地理位置：`isLocInfoEnable` / `getLoc`
- IDFA：`isIdfaEnable` / `getIdfa`
- IDFV：`isIdfvEnable` / `getIdfv`
- WiFi：`isWiFiInfoEnable` / `getSSID` / `getBSSID`
- IP：`isIpEnable` / `getCellIpv4` / `getCellIpv6` / `getWifiIpv4` / `getWifiIpv6`

如果项目已有隐私同意链路，应先向用户确认“是否把调用放在这里”，不要同时再问别的问题。

## 第七步：制作场景

基础 SDK 接入完成后，才进入业务接线。

如果用户尚未指定制作 MobId 的业务入口，先问一个问题：

`请告诉我哪个页面或按钮需要生成 MobLink 场景链接。`

用户未确认 API 插入位置前，不得把 `getMobId` 接入示例按钮、占位方法或任意业务方法。确认后再展示将要修改的文件和方法。

获取 MobId 的核心示例：

```objc
#import <MobLinkPro/MobLink.h>
#import <MobLinkPro/MLSDKScene.h>

NSMutableDictionary *customParams = [NSMutableDictionary dictionary];
customParams[@"key"] = @"value";
MLSDKScene *scene = [MLSDKScene sceneForPath:@"已在 MobLink 后台配置的渠道标识" params:customParams];

[MobLink getMobId:scene result:^(NSString *mobId, NSString *domain, NSError *error) {
    if (mobId.length > 0) {
        // mobId 可拼接到推广链接；domain 为后台生成的 Universal Link
    }
}];
```

注意：

- `sceneForPath:` 的 path 必须与 MobLink 后台配置一致
- `params` 用于场景还原时回传业务参数
- Web 落地页必须按官方 Web 集成文档接入 JS 模块，才能实现网页到 App 的场景衔接

## 第八步：场景还原

### 8-1 控制器恢复初始化

需要恢复的控制器可实现：

```objc
#import <MobLinkPro/MLSDKScene.h>
#import <MobLinkPro/UIViewController+MLSDKRestore.h>

- (instancetype)initWithMobLinkScene:(MLSDKScene *)scene
{
    if (self = [super init]) {
        self.scene = scene;
    }
    return self;
}
```

如果控制器使用 xib 初始化，必须用对应 xib 初始化方式，不要直接套用默认 `init`。

### 8-2 恢复代理回调

实现代理时，一旦实现 `IMLSDKWillRestoreScene:Restore:`，必须执行 `restoreHandler`：

```objc
- (void)IMLSDKWillRestoreScene:(MLSDKScene *)scene Restore:(void (^)(BOOL isRestore, RestoreStyle style))restoreHandler
{
    NSLog(@"MobLink restore path: %@", scene.path);
    restoreHandler(YES, MLDefault);
}
```

可选实现：

- `IMLSDKCompleteRestore:`
- `IMLSDKNotFoundScene:`

如果用户希望自行路由恢复场景，可将 `restoreHandler(NO, MLDefault)` 与项目路由逻辑结合，但必须先展示方案并等待确认。

## 第九步：依赖安装与验证

如果改了 `Podfile`，先问用户是否运行：

```sh
pod install
```

运行后验证：

- `.xcworkspace` 是否生成或更新
- `Podfile.lock` 是否包含 `mob_linksdk_pro`
- Xcode 工程是否从 `.xcworkspace` 打开

如用户允许构建，再运行合适的 `xcodebuild` 命令；否则只给手动验证清单。

## 第十步：生成项目内说明文档

完成后在用户项目根目录生成 `MobLink_README.md`，内容至少包括：

- 本次修改文件
- 已配置的 `Info.plist` 项
- 隐私同意调用位置
- 场景制作入口
- 场景还原入口
- 仍需在 MobLink 后台、Web 端或 Apple Developer 后台确认的事项
- 官方文档地址清单

## 验收清单

交付前至少检查：

- `Podfile` 中 `mob_linksdk_pro` 未重复
- `Info.plist` 中存在 `MOBAppKey`、`MOBAppSecret`、`MOBNetLater = 2`
- 用户拒绝隐私政策时不会调用 MobLink 能力
- 用户同意隐私政策后先调用 `uploadPrivacyPermissionStatus`
- `MobLink setDelegate:` 已接入
- `IMLSDKWillRestoreScene:Restore:` 如已实现，必定调用 `restoreHandler`
- Swift 工程的 Bridging Header 配置有效
- `MobLink_README.md` 已写入官方文档链接

## 常见问题处理

- 如果场景恢复失败，优先检查后台 iOS 页面名称、渠道标识、path 和控制器恢复实现是否一致。
- 如果回调没有触发，优先检查 `setDelegate:` 是否在启动早期执行，delegate 生命周期是否有效。
- 如果 `mobId` 为空，检查 `appKey`、`appSecret`、隐私授权回传和网络请求结果。
- 如果 Web 到 App 无法衔接，检查 Web 集成文档、落地页 JS 模块、Universal Link 或 Scheme 配置。
- 如果合规检查失败，优先检查隐私政策文本、首次冷启动弹窗、`MOBNetLater = 2` 和 `uploadPrivacyPermissionStatus` 时机。
