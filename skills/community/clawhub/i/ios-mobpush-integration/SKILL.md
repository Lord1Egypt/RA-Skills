---
name: ios-mobpush-integration
description: 面向 iOS 工程的 MobTech MobPush 集成 skill。默认先扫描工程，优先使用 CocoaPods，以最小改动完成推送依赖接入、APNs 配置、隐私合规、回调接线和项目内说明文档落地。
tags:
  - ios
  - mobpush
  - push
  - apns
  - sdk-integration
  - mobtech
  - cocoapods
  - privacy
  - objective-c
  - swift
---

# iOS MobPush 集成 Skill

当用户希望把 MobTech MobPush 集成到 iOS 工程，或者排查已有 MobPush 接入问题时，使用本 skill。

## 适用场景

当用户提到以下任一主题时，使用本 skill：

- iOS MobPush 集成
- iOS 推送接入
- iOS MobTech 推送
- MobPush CocoaPods 配置
- MobPush `Info.plist` 配置
- MobPush APNs 配置
- MobPush 隐私合规
- `uploadPrivacyPermissionStatus` 调用时机
- `setupNotification` / `setAPNsForProduction` 用法
- MobPush tag / alias 设置
- MobPush Live Activity 接入
- 帮我在 iOS 项目里增加推送
- 帮我把 MobPush 接进现有 iOS 工程

如果用户问题明确与 iOS MobPush 接入、工程配置、证书鉴权、隐私合规、通知接收、Tag/Alias 或 Live Activity 扩展能力有关，应优先使用本 skill。

## 输出语言

- 默认使用中文与用户沟通
- 代码、配置键名、类名、命令名保持原文
- 回答尽量短，先给结论，再给动作

## 官方资料

优先使用以下线上资料，不依赖本机资料路径：

主文档：

- [MobTech 文档中心](https://www.mob.com/wiki/list)
- [MobPush 产品页](https://www.mob.com/mobService/mobpush)
- [SDK 下载中心](https://www.mob.com/download)
- [创建应用流程](https://www.mob.com/wiki/detailed?wiki=494&id=136)
- [合规指南](https://www.mob.com/wiki/detailed?wiki=501&id=136)
- [集成指南](https://www.mob.com/wiki/detailed?wiki=502&id=136)
- [SDK API 文档](https://www.mob.com/wiki/detailed?wiki=503&id=136)
- [证书配置](https://www.mob.com/wiki/detailed?wiki=504&id=136)
- [App Store Connect 后台隐私数据项配置](https://www.mob.com/wiki/detailed?wiki=570&id=136)
- [MobPush 扩展业务功能设置](https://www.mob.com/wiki/detailed?wiki=665&id=136)
- [其它 App 数据采集主动控制器配置](https://www.mob.com/wiki/detailed?wiki=675&id=714)
- [MobPush 隐私政策](https://policy.zztfly.com/sdk/mobpush/privacy)

扩展资料：

- [iOS 实时活动说明](https://www.mob.com/wiki/list)

如果某个深链失效，先从 [MobTech 文档中心](https://www.mob.com/wiki/list) 搜索对应标题，不要回退到本机绝对路径。

## 已确认的官方事实

以下信息已经可作为执行依据，不需要再猜测：

- 默认开发环境要求为 `Xcode 9.1.0+`、`iOS 8.0+`
- 官方支持 `CocoaPods` 和手动导入两种集成方式
- 默认 Pod 为 `pod 'mob_pushsdk'`
- 工程需要链接 `libc++.tbd`、`libz.1.2.5.tbd`
- `Info.plist` 需要配置 `MOBAppKey` 与 `MOBAppSecret`
- 需要开启 `Push Notifications`
- 需要开启 `Background Modes` 并勾选 `Remote notifications`
- `uploadPrivacyPermissionStatus` 是 MobSDK 业务起点，必须在用户同意隐私政策后、使用 SDK 能力前调用
- 严格合规方案要求默认 `plist` 中增加 `MOBNetLater = 2`
- 推送环境应通过 `setAPNsForProduction:` 在开发与生产间切换
- 通知权限申请与推送注册通过 `setupNotification:` 配置
- 收到推送或自定义消息后，应监听 `MobPushDidReceiveMessageNotification`
- **Swift API 注意**：`MobPushDidReceiveMessageNotification` 在 Swift 中被重命名为 `NSNotification.Name.MobPushDidReceiveMessage`
- `MPushMessage` 的 `msg` 和 `isCustomMessage` 属性在 4.x 中已移除，改用 `messageType`（`MPushMessageType.custom`）和 `message.notification.body`
- 自定义消息内容存于 `message.notification.userInfo["mobpushCustomTitle"]` / `["mobpushCustomType"]`
- `MPushAuthorizationOptions` 在 Swift 中以 `OptionSet` 形式可用：`MPushAuthorizationOptions.badge.union(.sound).union(.alert)`
- 纯 Swift 工程必须创建 Bridging Header 并添加 `#import <MobPush/MobPush.h>` 和 `#import <MOBFoundation/MOBFoundation.h>`
- Bridging Header 路径需在 `.xcodeproj` 的 Debug 和 Release 构建配置中设置 `SWIFT_OBJC_BRIDGING_HEADER`
- `getRegistrationID` 必须在推送设置接口之后调用
- SDK 支持 tag、alias、本地通知、badge 同步等能力
- iOS 端扩展业务能力仅支持“基于地域更精准推送”和“网络链路优化/特定区域服务”两类
- 扩展业务主动控制器应通过 `MOBFoundationPrivacyDelegate` 自定义类接入
- 证书鉴权支持 `.p12` 与 `APNs Auth Key(.p8)` 两种方式
- `.p8` 鉴权需要 `Key ID`、`Team ID`、`Bundle ID`
- Live Activity 功能需 `iOS 16.1+`、`SwiftUI`、`ActivityKit`，且需要 App 运行态配合

## 文档未明确，需向用户确认

以下内容在当前资料里没有被稳定、明确地定义，禁止猜：

- 是否支持 Swift Package Manager
- 是否需要 Bitcode、Privacy Manifest 或额外苹果隐私文件
- 用户项目应该使用 CocoaPods 还是已存在的手动导入体系
- 用户是否本次就要接入 Notification Service Extension
- Live Activity 官方独立文档深链地址在当前资料中未提供，若用户要正式启用该能力，需先确认要以当前资料版本为准还是由用户补充最新官方页面

如果缺这些信息且会阻塞安全修改，必须明确写：

`文档未明确，需向用户确认`

## 默认执行策略

- 默认集成方式：`CocoaPods`
- 默认先扫描工程，再给改动方案
- 默认优先复用工程已有推送能力、隐私弹窗和 App 启动入口
- 默认先生成最小 Excel 模板，再等用户填写
- 默认不在 Excel 中收集 `Bundle ID`、Target 名称、`Info.plist` 路径、入口类名，因为这些应由扫描工程自动推断
- 默认不主动询问是否启用扩展业务主动控制器；仅在最终项目文档中说明这项可选能力
- 默认不主动启用 Live Activity；仅当用户明确需要时才进入该分支
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
- 现有通知权限申请、APNs 注册、UNUserNotificationCenter 代理代码
- 隐私政策弹窗或同意回调位置
- Objective-C / Swift / 混编类型，以及是否已有 Bridging Header
- 是否已有 `MobPush`、`MOBAppKey`、`MOBAppSecret`、`MOBNetLater`、`uploadPrivacyPermissionStatus`
- `.gitignore` 是否忽略 `Pods/`
- `.xcworkspace` 是否包含 `contents.xcworkspacedata`

推荐命令：

- `rg --files -g '*.xcodeproj' -g '*.xcworkspace' -g 'Podfile' -g 'Podfile.lock' -g 'Package.swift' -g '*Info.plist' -g '.gitignore'`
- `rg --files -g '*.m' -g '*.h' -g '*.mm' -g '*.swift'`
- `rg -n 'MobPush|MOBAppKey|MOBAppSecret|MOBNetLater|uploadPrivacyPermissionStatus|setAPNsForProduction|setupNotification|MobPushDidReceiveMessageNotification|UNUserNotificationCenter|didRegisterForRemoteNotificationsWithDeviceToken|SWIFT_OBJC_BRIDGING_HEADER'`

扫描后先给一段简短结论，至少包含：

- 当前工程依赖方式
- 当前入口结构
- 当前代码语言形态：Objective-C / Swift / 混编
- Swift 工程是否已有 Bridging Header
- 是否已有 MobPush 残留
- 是否已经有隐私同意链路
- 是否已经有推送能力接线
- CocoaPods 状态：是否有有效 `Podfile`、`Podfile.lock`、`Pods/`、`*.xcworkspace/contents.xcworkspacedata`
- 下一步是生成模板还是读取已有 `MobPush_iOS_Config.xlsx`

## 第二步：生成并读取配置模板

### 2-1 模板生成

如果 `{path}` 下还没有 `MobPush_iOS_Config.xlsx`：

1. 运行本 skill 目录下的 `assets/generate_excel_template.py`
2. 将生成的 `assets/MobPush_iOS_Config_Template.xlsx` 复制到 `{path}` 下
3. 在 `{path}` 下命名为 `MobPush_iOS_Config.xlsx`

### 2-2 向用户说明填写项

必须明确告诉用户只需要填写这些最小字段：

- `appKey`
- `appSecret`
- `apnsAuthMode`
- `needLiveActivity`

同时明确说明以下内容不需要填表：

- `Bundle ID`
- `Target`
- `Info.plist` 路径
- App 启动入口类名
- 隐私弹窗类名
- 推送回调方法名
- `Key ID` / `Team ID` / `.p12` 文件路径

其中工程信息应由 Agent 扫描后推断；鉴权材料属于控制台与苹果后台准备项，不应默认塞进最小模板。

### 2-3 配置校验

读取 `MobPush_iOS_Config.xlsx` 后，至少校验：

- `appKey`：必填，按字符串处理，不做数值推断
- `appSecret`：必填，按字符串处理，不做数值推断
- `apnsAuthMode`：必须明确是 `p12` / `p8` / `已存在`
- `needLiveActivity`：必须明确是 `是` / `否`

如不合法，列出具体问题并要求用户修正，不要继续改工程。

## 第三步：扫描后推断工程接入点

读取配置后，再次结合工程做推断：

- 优先识别主要 App Target
- 推断 Objective-C / Swift / 混编
- 记录当前工程要使用 Objective-C 示例、Swift 示例还是两者都需要
- Swift 工程需检查是否已有 `{Target}-Bridging-Header.h` 与 `SWIFT_OBJC_BRIDGING_HEADER`
- 定位疑似隐私同意回调位置，后续仍必须向用户确认
- 推断当前是否已有 CocoaPods 体系
- 推断是否已有 `Push Notifications` / `Background Modes` 相关工程配置说明或脚本
- 推断是否已有 APNs 注册代码、通知代理、启动回调
- 判断已有 `*.xcworkspace` 是否有效；只有目录但缺少 `contents.xcworkspacedata` 时，应运行 `pod install` 重新生成
- 判断已有 `Pods/` 是否完整；如果只有空 framework 目录或缺少 `Info.plist`、Headers、binary，不要按手动 SDK 接入硬改工程，应优先重新 `pod install`

以下信息必须分两类处理：

### 必须在修改前确认的信息

- 多 Target 时应该接入哪个 App Target
- 用户同意隐私政策后的回调位置。即使扫描到疑似隐私弹窗，也要让用户确认 `uploadPrivacyPermissionStatus` 应插入到哪个“同意”回调
- 用户明确不想用 CocoaPods，必须改走手动导入

### 可以在扫描后逐步确认的信息

- 是否需要启用 Live Activity
- 是否需要添加 tag / alias 业务接线
- 是否需要接入扩展业务主动控制器

如果必须确认，串行一次只问一个问题。

## 第四步：展示最小改动计划

修改前必须向用户展示本次最小改动计划，通常包括：

- `Podfile`：按需加入 `pod 'mob_pushsdk'`
- `.gitignore`：按需加入 `Pods/`
- `Info.plist`：写入 `MOBAppKey`、`MOBAppSecret`、`MOBNetLater = 2`
- Xcode 工程能力：提醒用户检查或手动开启 `Push Notifications` 与 `Background Modes > Remote notifications`
- 系统库：补 `libc++.tbd`、`libz.1.2.5.tbd`
- App 启动入口：接入 `setAPNsForProduction:`、`setupNotification:`
- 隐私同意后：接入 `uploadPrivacyPermissionStatus`
- 通知回调：注册 `MobPushDidReceiveMessageNotification`
- 视情况增加 `getRegistrationID` 示例或落点
- 如用户明确需要 Live Activity，再进入额外分支
- 生成项目内 `MobPush_README.md`

没有确认前，不要直接改。

## 第五步：执行工程修改

### 5-1 依赖接入

默认优先 CocoaPods：

- `Podfile` 中加入 `pod 'mob_pushsdk'`
- 若项目是 Swift 且需桥接 Objective-C API，优先复用已有 Bridging Header
- 若无 Bridging Header，创建 `{Target}/mobpush_bridge.h` 并写入：
```objc
#import <MobPush/MobPush.h>
#import <MOBFoundation/MOBFoundation.h>
```
- 同时在 `.xcodeproj` 的 Debug 和 Release 构建配置中设置 `SWIFT_OBJC_BRIDGING_HEADER = "{Target}/mobpush_bridge.h"`
- 若项目没有 `Podfile`，先说明将新增，再等待确认

如果用户明确要求手动导入：

- 只给出最小手动导入计划
- 不凭空修改 `.xcodeproj` 二进制文件
- 需要用户确认 SDK 解压目录和目标 Target

### 5-2 `Info.plist`

至少处理以下键：

- `MOBAppKey`
- `MOBAppSecret`
- `MOBNetLater = 2`

如果工程里已有同名键：

- 先展示现值
- 与 Excel 配置冲突时停止并询问用户

### 5-3 启动入口接线

根据工程入口类型选择落点：

- Objective-C：`AppDelegate`
- UIKit Swift：`AppDelegate` / `SceneDelegate`
- SwiftUI：`@main App` 对应的 `UIApplicationDelegateAdaptor`

最小接线包括：

- 按 `DEBUG` / 非 `DEBUG` 设置 `setAPNsForProduction:`
- 构造 `MPushNotificationConfiguration`
- 调用 `setupNotification:`
- 注册通知监听

**Swift 示例（AppDelegate 核心接线）**：
```swift
import UIKit
import UserNotifications

func application(_ application: UIApplication, didFinishLaunchingWithOptions: ...) -> Bool {
    #if DEBUG
    MobPush.setAPNsForProduction(false)
    #else
    MobPush.setAPNsForProduction(true)
    #endif

    let config = MPushNotificationConfiguration()
    config.types = MPushAuthorizationOptions.badge.union(.sound).union(.alert)
    MobPush.setupNotification(config)

    // ⚠️ 注意使用 Swift 重命名后的常量名
    NotificationCenter.default.addObserver(
        self,
        selector: #selector(didReceiveMobPushMessage(_:)),
        name: NSNotification.Name.MobPushDidReceiveMessage,
        object: nil
    )
    return true
}
```

如果工程已有自己的通知权限申请逻辑：

- 优先复用，不重复申请
- 仅补 SDK 必需部分

### 5-4 隐私合规接线

必须在用户同意隐私政策后插入：

- `MobSDK uploadPrivacyPermissionStatus:YES onResult:...`

如果用户拒绝隐私政策：

- 不得接入会实际调用 MobPush 能力的初始化流程

如果用户明确需要控制扩展业务数据采集：

- 再增加 `MobCustomController` 与 `MOBFoundationPrivacyDelegate`
- 否则不要提前写复杂隐私控制器

### 5-5 通知与业务回调

最小落地包括：

- 注册 `MobPushDidReceiveMessageNotification`
- 预留 `didReceiveMessage:` 或 Swift 等价方法
- 按需输出 `MPushMessage` 关键字段日志或注释

**Swift 回调示例（注意 4.x 属性变化）**：
```swift
@objc private func didReceiveMobPushMessage(_ notification: Notification) {
    guard let message = notification.object as? MPushMessage else { return }

    switch message.messageType {
    case .custom:
        // 自定义消息：notification.userInfo["mobpushCustomTitle"] / ["mobpushCustomType"]
        let body = message.notification.body ?? "自定义消息"
        // App 内展示
    default:
        // 推送通知 / APNs / 本地通知
        print(message.notification.body ?? "")
    }
}
```

如果用户明确需要：

- 再接 tag / alias / badge / local notification
- 这些能力默认不作为首轮硬接线项

### 5-6 Live Activity 可选分支

只有当用户明确要求并且工程满足 `iOS 16.1+`、`SwiftUI`、扩展 Target 条件时才执行：

- 提示添加 `NSSupportsLiveActivities = YES`
- 提示添加 `ActivityKit.framework` 与 `SwiftUI.framework`
- 提示新增 Live Activity Extension
- 接入 `registerLiveActivityWithID:pushToken:completion:`

Live Activity UI 与业务状态模型默认不代写完整业务实现，只保留官方能力落点和最小示例。

## 第六步：安装依赖与验证

在用户确认后才执行：

- `pod install` 或 `pod update`
- **注意**：Ruby 4.0+ 环境下 `pod install` 可能因编码问题失败，需先设置环境变量：
  ```bash
  export LANG=en_US.UTF-8 && export LC_ALL=en_US.UTF-8
  pod install
  ```
- 必要时打开 `*.xcworkspace`

验证优先级：

1. `Podfile.lock` 中确认 `mob_pushsdk`
2. `Info.plist` 键值存在
3. 入口代码已接线
4. 代码搜索可命中 `uploadPrivacyPermissionStatus`、`setupNotification`
5. 如能编译，再做编译验证

如果不能实际运行真机推送测试，要明确说明：

- APNs 收包、证书有效性、后台推送链路未在当前环境完成验证

## 第七步：生成项目内说明文档

完成后在 `{path}` 下生成 `MobPush_README.md`，至少包含：

- 本次修改了哪些文件
- `MOBAppKey` / `MOBAppSecret` 放在哪里
- 隐私同意后调用链路在哪里
- 推送初始化入口在哪里
- APNs 鉴权材料还需用户在哪个平台完成
- 如果启用了 Live Activity，还需哪些额外工程配置
- 官方文档地址清单

优先使用本 skill 内的 `templates/MOBPUSH_README.md` 作为骨架，再结合实际项目修改点渲染。

## 交互约束

- 一次只问一个阻塞问题
- 自动可推断项优先从工程读取
- 只有当推断失败、存在多个候选值或发现冲突时才询问开发者
- 依赖安装是否代执行放到最后再问
- 如果某一步无需修改，应直接进入下一步
- 不要一次性抛出长问题清单

## 常用搜索关键字

- `MobPush`
- `MOBAppKey`
- `MOBAppSecret`
- `MOBNetLater`
- `uploadPrivacyPermissionStatus`
- `setAPNsForProduction`
- `setupNotification`
- `MobPushDidReceiveMessageNotification`
- `getRegistrationID`
- `MOBFoundationPrivacyDelegate`
- `registerLiveActivityWithID`
