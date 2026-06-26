---
name: ios-smssdk-integration
description: 面向 iOS 工程的 MobTech SMSSDK 短信验证集成 skill。默认先扫描工程，优先使用 CocoaPods，以最小改动完成依赖接入、隐私合规、短信验证码发送/校验链路和项目内说明文档落地。
tags:
  - ios
  - smssdk
  - sms
  - 短信验证
  - sdk-integration
  - mobtech
  - cocoapods
  - privacy
  - objective-c
  - swift
---

# iOS SMSSDK 集成 Skill

当用户希望把 MobTech SMSSDK 集成到 iOS 工程，或者排查已有 SMSSDK 接入问题时，使用本 skill。

## 适用场景

当用户提到以下任一主题时，使用本 skill：

- iOS SMSSDK 集成
- iOS 短信验证码接入
- MobTech 短信验证
- `mob_smssdk` CocoaPods 配置
- SMSSDK `Info.plist` 配置
- SMSSDK 隐私合规
- `uploadPrivacyPermissionStatus` 调用时机
- `getVerificationCodeByMethod` 用法
- `commitVerificationCode` 用法
- 语音验证码
- 手机号码认证 Token
- 验证手机号是否本机号码
- SMSSDK 错误码排查
- 帮我在 iOS 项目里增加短信验证码登录
- 帮我把 SMSSDK 接进现有 iOS 工程

如果用户问题明确与 iOS 短信验证接入、工程配置、隐私合规、验证码发送/提交、本机号码认证或错误码排查有关，应优先使用本 skill。

## 输出语言

- 默认使用中文与用户沟通
- 代码、配置键名、类名、命令名保持原文
- 回答尽量短，先给结论，再给动作

## 官方资料

- [MobTech 文档中心](https://www.mob.com/wiki/list)
- [SDK 下载中心](https://www.mob.com/download)
- [创建应用](https://www.mob.com/wiki/detailed?wiki=539&id=23)
- [集成指南](https://www.mob.com/wiki/detailed?wiki=110&id=23)
- [SDK API 文档](https://www.mob.com/wiki/detailed?wiki=467&id=23)
- [合规指南](https://www.mob.com/wiki/detailed?wiki=211&id=23)
- [SMSSDK 扩展业务功能设置](https://www.mob.com/wiki/detailed?wiki=671&id=23)
- [错误码](https://www.mob.com/wiki/detailed?wiki=468&id=23)
- [App Store Connect 后台隐私数据项配置](https://www.mob.com/wiki/detailed?wiki=573&id=23)
- [其它 App 数据采集主动控制器配置](https://www.mob.com/wiki/detailed?wiki=675&id=714)
- [SMSSDK 隐私政策](https://policy.zztfly.com/sdk/sms/privacy)

## 已确认的官方事实

以下信息已经可作为执行依据，不需要再猜测：

- 默认开发环境要求为 `Xcode 9.1.0+`、`iOS 8.0+`
- 官方支持 `CocoaPods` 和手动导入两种集成方式
- 默认 Pod 为 `pod 'mob_smssdk'`
- 手动导入时需要加入 `MOBFoundation.framework` 与 `SMS_SDK.framework`
- 官方列出的必要依赖库包括 `libz.tbd`、`libicucore.tbd`、`MessageUI.framework`、`JavaScriptCore.framework`、`libc++.tbd`
- Xcode 7 运行报错时，官方说明还需要增加 `SystemConfiguration.framework`、`CoreTelephony.framework`、`AdSupport.framework`
- `Info.plist` 需要配置 `MOBAppKey` 与 `MOBAppSecret`
- 合规指南要求在项目默认 `plist` 中添加 `MOBNetLater = 2`
- `uploadPrivacyPermissionStatus` 是 MobSDK 隐私授权回传接口，必须在用户同意隐私政策之后、使用 SDK 功能之前调用
- 用户不同意 App 隐私政策时，不能调用 `uploadPrivacyPermissionStatus` 回传同意结果，也不能继续使用 SMSSDK 能力
- 请求短信验证码使用 `getVerificationCodeByMethod:phoneNumber:zone:template:result:`
- `SMSGetCodeMethodSMS` 表示文本短信验证码，`SMSGetCodeMethodVoice` 表示语音验证码
- 提交验证码验证使用 `commitVerificationCode:phoneNumber:zone:result:`
- `zone` 是区域号，不要加 `+`
- `template` 参数不能乱填，没有模板时可以先传空字符串或 `nil`
- 自定义短信模板需要在官网后台 SMSSDK 产品下的短信模板里添加，且需要申请过自定义短信签名的应用才能添加短信模板
- 默认签名仅用于测试，不保证到达率；上线前必须申请自定义签名
- SDK API 文档还提供 `getMobileAuthTokenWith:` 和 `verifyMobileWithPhone:token:completion:` 用于本机号码认证相关流程
- `SMS_SDK.framework` 的 module umbrella header 是 `SMSHeader.h`；当代码直接使用 `SMSSDKAuthToken` 等类型时，应优先导入 `<SMS_SDK/SMSHeader.h>`，避免只导入 `<SMS_SDK/SMSSDK.h>` 触发模块导入顺序错误
- 扩展业务主动控制器可通过实现 `MOBFoundationPrivacyDelegate` 控制地理位置、WiFi、IP 等扩展业务相关数据采集
- 扩展业务主动控制器可以通过 `uploadPrivacyPermissionStatus:privacyDataDelegate:onResult:` 传入，也可以通过 `[MobSDK setPrivacyDataDelegate:]` 设置

## 文档未明确，需向用户确认

以下内容在当前资料里没有被稳定、明确地定义，禁止猜：

- 是否支持 Swift Package Manager
- 是否需要 `-ObjC`、Bitcode、Privacy Manifest 或额外苹果隐私文件
- CocoaPods 方式是否仍需要手动添加官方列出的系统库
- Swift 工程应直接通过模块导入还是必须桥接 Objective-C 头文件
- 项目是否要接入语音验证码
- 项目是否要接入本机号码认证 Token 与手机号验证流程
- 是否需要启用扩展业务主动控制器
- App Store Connect 隐私标签的最终选择是否已由法务或隐私负责人确认

如果缺这些信息且会阻塞安全修改，必须明确写：

`文档未明确，需向用户确认`

## 默认执行策略

- 默认集成方式：`CocoaPods`
- 默认先扫描工程，再给改动方案
- 默认优先复用工程已有隐私弹窗、手机号输入页和验证码提交入口，不新造完整登录页
- 默认先生成最小 Excel 模板，再等用户填写
- 默认不在 Excel 中收集 `Bundle ID`、Target 名称、入口类名、`Info.plist` 路径，因为这些应由扫描工程自动推断
- 默认只把短信验证码发送和验证码提交接入本轮主流程
- 语音验证码、本机号码认证和扩展业务主动控制器默认作为可选能力记录在项目文档里，只有用户明确要求时再接入
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
- 手机号登录页、验证码发送按钮、验证码提交逻辑
- Objective-C / Swift / 混编类型，以及是否已有 Bridging Header
- 是否已有 `SMSSDK`、`SMS_SDK`、`MOBFoundation`、`MOBAppKey`、`MOBAppSecret`、`MOBNetLater`
- `.gitignore` 是否忽略 `Pods/`
- `.xcworkspace` 是否包含 `contents.xcworkspacedata`

推荐命令：

- `rg --files -g '*.xcodeproj' -g '*.xcworkspace' -g 'Podfile' -g 'Podfile.lock' -g 'Package.swift' -g '*Info.plist' -g '.gitignore'`
- `rg --files -g '*.m' -g '*.h' -g '*.mm' -g '*.swift'`
- `rg -n 'SMSSDK|SMS_SDK|MOBFoundation|MOBAppKey|MOBAppSecret|MOBNetLater|uploadPrivacyPermissionStatus|getVerificationCodeByMethod|commitVerificationCode|SWIFT_OBJC_BRIDGING_HEADER'`

扫描后先给一段简短结论，至少包含：

- 当前工程依赖方式
- 当前入口结构
- 当前代码语言形态：Objective-C / Swift / 混编
- Swift 工程是否已有 Bridging Header
- 是否已有 SMSSDK 残留
- 是否已经有隐私同意链路
- 是否已经有手机号输入、验证码发送和验证码提交链路
- CocoaPods 状态：是否有有效 `Podfile`、`Podfile.lock`、`Pods/`、`*.xcworkspace/contents.xcworkspacedata`
- 下一步是生成模板还是读取已有 `SMSSDK_iOS_Config.xlsx`

## 第二步：生成并读取配置模板

### 2-1 模板生成

如果用户项目根目录还没有 `SMSSDK_iOS_Config.xlsx`：

1. 运行本 skill 目录下的 `assets/generate_excel_template.py`
2. 将生成的 `assets/SMSSDK_iOS_Config_Template.xlsx` 复制到用户项目根目录
3. 在用户项目根目录命名为 `SMSSDK_iOS_Config.xlsx`

### 2-2 向用户说明填写项

必须明确告诉用户只需要填写这些最小字段：

- `appKey`
- `appSecret`
- 短信签名是否已申请
- 是否需要语音验证码
- 是否需要本机号码认证

同时明确说明以下内容不需要填表：

- `Bundle ID`
- `Target`
- `Info.plist` 路径
- 隐私弹窗类名
- 手机号输入框路径
- 验证码按钮落点
- 是否启用扩展业务主动控制器

其中工程信息应由 Agent 扫描后推断；扩展业务主动控制器不作为前置配置项，只在最终文档中说明。

### 2-3 配置校验

读取 `SMSSDK_iOS_Config.xlsx` 后，至少校验：

- `appKey`：必填，按字符串处理，不做数值推断
- `appSecret`：必填，按字符串处理，不做数值推断
- `短信签名是否已申请`：必须明确是 `是` / `否`
- `是否需要语音验证码`：必须明确是 `是` / `否`
- `是否需要本机号码认证`：必须明确是 `是` / `否`

如不合法，列出具体问题并要求用户修正，不要继续改工程。

如果 `短信签名是否已申请 = 否`，仍可继续做技术接入，但必须提醒：默认签名仅用于测试，不保证到达率，上线前必须申请自定义签名。

## 第三步：扫描后推断工程接入点

读取配置后，再次结合工程做推断：

- 优先识别主要 App Target
- 推断 Objective-C / Swift / 混编
- 记录当前工程要使用 Objective-C 示例、Swift 示例还是两者都需要
- Swift 工程需检查是否已有 `{Target}-Bridging-Header.h` 与 `SWIFT_OBJC_BRIDGING_HEADER`
- 定位疑似隐私同意回调位置，后续仍必须向用户确认
- 定位手机号输入框、验证码发送按钮、验证码提交按钮或 ViewModel 方法
- 推断当前是否已有 CocoaPods 体系

如果无法稳定定位隐私同意回调，且需要写代码，只问一个阻塞问题：

`请告诉我用户点击同意隐私政策后会进入哪个文件或方法，我会把 uploadPrivacyPermissionStatus 接在那里。`

如果无法稳定定位验证码发送入口，且用户要求自动接线，只问一个阻塞问题：

`请告诉我验证码发送按钮或对应 ViewModel 方法在哪个文件，我会把 getVerificationCodeByMethod 接在那里。`

不要同时问多个阻塞问题。

## 第四步：展示改动计划

修改前必须展示最小改动计划，包含：

- 需要修改的文件
- `Podfile` 是否会加入 `pod 'mob_smssdk'`
- `Info.plist` 将写入或校正的键：`MOBAppKey`、`MOBAppSecret`、`MOBNetLater`
- 隐私同意后调用 `uploadPrivacyPermissionStatus` 的位置
- 请求验证码调用 `getVerificationCodeByMethod` 的位置
- 提交验证码调用 `commitVerificationCode` 的位置
- 是否需要桥接头
- 是否会生成 `SMSSDK_README.md`
- 哪些动作需要用户确认后才执行，例如 `pod install` 或构建验证

如果某一步无需修改，应直接说明“无需修改”，然后进入下一步。

## 第五步：执行集成

### 5-1 依赖接入

默认优先 `CocoaPods`：

- 在正确的 target 下加入 `pod 'mob_smssdk'`
- 如项目没有有效 workspace，运行 `pod install` 后确认 `*.xcworkspace/contents.xcworkspacedata` 已生成
- `pod install` 可能需要写用户级 CocoaPods cache 或 spec repo；如遇 `~/Library/Caches/CocoaPods`、`~/.cocoapods/repos/trunk`、`Operation not permitted @ rb_sysopen` 等权限错误，应按当前执行环境申请授权后重试
- 若 `pod install` 修改 `.xcodeproj`，不要再手写重复的 Pods framework、xcconfig、shell script phase
- 只有用户确认后才执行 `pod install`
- 如果用户没有 CocoaPods 环境，引导用户安装 CocoaPods；不要编造本机安装路径

如果用户明确要求手动导入：

- 按官方资料从 [SDK 下载中心](https://www.mob.com/download) 下载 SDK
- 将 `MOBFoundation.framework` 与 `SMS_SDK.framework` 加入工程
- 检查并补官方列出的系统库与 `Info.plist`

### 5-2 `Info.plist` 配置

默认写入或校正：

- `MOBAppKey`
- `MOBAppSecret`
- `MOBNetLater = 2`

不要把 `appKey`、`appSecret` 写进源代码，除非用户明确要求代码初始化且官方资料确认支持。

### 5-3 隐私合规接入

在用户同意隐私政策后、首次使用 SMSSDK 能力前接入：

```objective-c
#import <MOBFoundation/MobSDK+Privacy.h>

[MobSDK uploadPrivacyPermissionStatus:YES onResult:^(BOOL success) {
    // 注意业务逻辑不要依赖 success，建议业务逻辑在调用该接口之后继续执行。
}];
```

如果用户明确需要扩展业务主动控制器，再接入：

```objective-c
#import <MOBFoundation/MOBFoundation.h>

MobCustomController *privacyDataService = [MobCustomController new];
[MobSDK uploadPrivacyPermissionStatus:YES privacyDataDelegate:privacyDataService onResult:^(BOOL success) {
}];
```

若项目不是每次启动都会调用隐私提交接口，但又需要每次启动设置主动控制器，可按官方资料使用：

```objective-c
[MobSDK setPrivacyDataDelegate:privacyDataService];
```

### 5-4 短信验证码流程接入

建议流程：

1. 用户同意隐私政策后调用 `uploadPrivacyPermissionStatus`
2. 用户输入手机号和区号
3. 点击获取验证码时调用 `getVerificationCodeByMethod`
4. 用户输入验证码
5. 点击提交时调用 `commitVerificationCode`

Objective-C 请求验证码示例：

```objective-c
#import <SMS_SDK/SMSHeader.h>

[SMSSDK getVerificationCodeByMethod:SMSGetCodeMethodSMS
                         phoneNumber:phoneNumber
                                zone:zone
                            template:@""
                              result:^(NSError *error) {
    if (!error) {
        // 请求成功
    } else {
        // 处理 error
    }
}];
```

Objective-C 提交验证码示例：

```objective-c
[SMSSDK commitVerificationCode:code
                   phoneNumber:phoneNumber
                          zone:zone
                        result:^(NSError *error) {
    if (!error) {
        // 验证成功
    } else {
        // 处理 error
    }
}];
```

Swift 工程：

- 优先检查项目是否已有桥接头
- 如需要桥接头，最小加入一个 Objective-C wrapper，让 Swift 只调用 wrapper；不要在 Swift 中猜 Objective-C API 的自动桥接命名
- wrapper 内使用 `<SMS_SDK/SMSHeader.h>` 和 `<MOBFoundation/MobSDK+Privacy.h>`
- wrapper 暴露给 Swift 的参数类型应尽量使用 `NSString`、`BOOL`、`NSError` 信息字符串或 `id`，避免在 Swift 接口中直接暴露 SDK 私有模型类型
- 如果接入本机号码认证，wrapper 内部再把 `id` 校验并转换为 `SMSSDKAuthToken *`
- 文档未明确 Swift 原生导入方式，需向用户确认或按工程已有混编模式处理；默认不要直接写 `import SMS_SDK`

桥接头示例：

```objc
#import "SMSSDKBridge.h"
```

Objective-C wrapper 导入示例：

```objective-c
#import <MOBFoundation/MobSDK+Privacy.h>
#import <SMS_SDK/SMSHeader.h>
```

### 5-5 可选能力

只有用户明确需要时，才继续接入以下能力：

- 语音验证码：把 `SMSGetCodeMethodSMS` 改为 `SMSGetCodeMethodVoice`
- 本机号码认证 Token：调用 `getMobileAuthTokenWith:`
- 验证手机号是否本机号码：调用 `verifyMobileWithPhone:token:completion:`
- 扩展业务主动控制器：实现 `MOBFoundationPrivacyDelegate`

可选能力修改前仍需展示计划，不要在主流程里默认加入。

## 第六步：验证与说明文档

完成改动后，按条件执行：

- 若用户确认，可运行 `pod install`
- `pod install` 成功后，记录 `Podfile.lock` 中实际安装的 `mob_smssdk`、`MOBFoundation` 以及传递依赖版本
- `pod install` 成功后，确认根目录或项目目录下生成的 `*.xcworkspace/contents.xcworkspacedata` 指向真实 `.xcodeproj` 与 `Pods/Pods.xcodeproj`
- 构建前可先运行 `xcodebuild -list -workspace <workspace>` 检查 workspace 是否能被 Xcode 解析
- 若环境允许，可运行一次构建验证
- 如果普通沙箱下 `xcodebuild` 无法访问 CoreSimulator、Xcode 用户目录或 `~/Library/Logs/CoreSimulator`，应按当前环境申请授权后重试
- 如果普通沙箱下 `xcodebuild` 报 `'<name>.xcworkspace' is not a workspace file`，但 `contents.xcworkspacedata` 存在且 XML 正常，应先用授权后的 `xcodebuild -list -workspace <workspace>` 复核；不要直接改 workspace
- 如果授权后的 `xcodebuild -list` 能列出 schemes，说明 workspace 本身有效，继续使用授权后的构建命令验证
- 若无法构建，明确说明未验证的原因

然后生成项目内 `SMSSDK_README.md`，至少包含：

- 本次改动点
- `appKey` / `appSecret` 的配置位置
- `MOBNetLater = 2` 的配置位置
- `uploadPrivacyPermissionStatus` 的调用位置
- 验证码发送和提交的接入位置
- Objective-C / Swift 支持情况与桥接头配置情况
- CocoaPods 版本信息：`Podfile`、`Podfile.lock`、实际安装的 SMSSDK 版本
- 构建验证结果与剩余 warning
- 默认签名仅用于测试，上线前必须申请自定义签名
- 语音验证码、本机号码认证和扩展业务主动控制器属于可选能力
- 常见错误码排查入口
- 官方文档链接清单

## 常见错误排查原则

遇到失败时优先检查：

- 是否已在用户同意隐私政策后调用 `uploadPrivacyPermissionStatus`
- `MOBNetLater` 是否已配置为 `2`
- `MOBAppKey` / `MOBAppSecret` 是否和 MobTech 后台一致
- `phoneNumber`、`zone`、`code` 是否为空或格式错误
- `zone` 是否误加了 `+`
- `template` 是否填写了不存在、未审核或非 SDK 模板
- 是否仍在使用默认签名做线上验证
- 当前手机号或设备是否触发发送频率限制
- 是否未开启网络
- 是否有 612 / 6119103 这类未授权 MobTech 隐私协议错误
- 是否有 300483 这类 `AppSecret` 错误
- 是否有 300484 / 300206 这类模板错误
- CocoaPods workspace 是否有效生成
- 编译报 `Definition of 'SMSSDKAuthToken' must be imported from module 'SMS_SDK.SMSSDKAuthToken' before it is required` 时，把 SMSSDK 相关导入改为 `<SMS_SDK/SMSHeader.h>`，并确保 wrapper 使用该 umbrella header
- `xcodebuild` 在普通沙箱下误报 workspace 无效时，先检查 `contents.xcworkspacedata`，再授权运行 `xcodebuild -list -workspace` 复核

## 与用户沟通的硬约束

- 一次只问一个阻塞问题
- 没有阻塞就不要追问，直接推进
- 每次修改前先展示计划
- 执行 `pod install` 或构建前先征求确认
- 如果某项无需修改，要明确说“无需修改”
