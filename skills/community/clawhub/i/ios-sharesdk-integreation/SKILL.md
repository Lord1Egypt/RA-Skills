---
name: ios-sharesdk-integreation
description: 面向 iOS 工程的 MobTech ShareSDK 集成 skill。默认优先使用 CocoaPods，先扫描工程，再串行确认阻塞项，最后以最小改动完成接入、隐私合规与项目内说明文档落地。
tags:
  - ios
  - sharesdk
  - sdk-integration
  - mobtech
  - cocoapods
  - privacy
  - objective-c
  - swift
---

# iOS ShareSDK 集成 Skill

当用户希望把 MobTech ShareSDK 集成到 iOS 工程，或希望把已有工程整理成可接入 ShareSDK 的状态时，使用本 skill。

## 适用场景

当用户提到以下任一主题时，使用本 skill：

- iOS ShareSDK 集成
- MobTech ShareSDK iOS 接入
- iOS 社交分享 SDK 配置
- CocoaPods 集成 ShareSDK
- ShareSDK 的 `Podfile` 配置
- ShareSDK 的 `Info.plist` 配置
- ShareSDK 的 `MOBAppKey` / `MOBAppSecret` 配置
- ShareSDK iOS 隐私合规
- `uploadPrivacyPermissionStatus` 调用时机
- 微信 / QQ / 微博分享或登录在 ShareSDK 中的平台注册
- URL Scheme、`LSApplicationQueriesSchemes`、Universal Link、Associated Domains 配置
- iOS 项目里增加分享能力
- 帮我配置微信分享 / QQ 分享 / 微博分享
- 迁移或清理旧 ShareSDK demo 残留

如果用户问题明确与 iOS 的 ShareSDK 接入、工程配置、平台参数、隐私合规、社交分享或第三方授权登录有关，应优先使用本 skill。

## 输出语言

- 默认使用中文与用户沟通
- 代码、配置键名、类名、命令名保持原文
- 回答要短，先给结论，再给动作

## 官方资料

主文档：

- https://www.mob.com/wiki/detailed?wiki=4&id=14
- https://www.mob.com/wiki/detailed?wiki=500&id=14

执行时高频需要参考的关联官方页面：

- https://www.mob.com/wiki/detailed?wiki=499&id=14
- https://www.mob.com/wiki/detailed?wiki=747&id=14
- https://policy.zztfly.com/sdk/share/privacy

## 已确认的官方事实

以下信息已经可以作为本 skill 的执行依据，不需要再假设：

- 官方推荐的 iOS 集成方式包含 CocoaPods 与手动集成
- 默认开发环境要求为 `Xcode 9.1.0+`、`iOS 8.0+`
- 用户未特别指定时，默认走 CocoaPods 集成
- Pod 主模块是 `pod 'mob_sharesdk'`
- UI 模块是 `pod 'mob_sharesdk/ShareSDKUI'`
- 常见平台模块包括：
  - `pod 'mob_sharesdk/ShareSDKPlatforms/QQ'`
  - `pod 'mob_sharesdk/ShareSDKPlatforms/SinaWeibo'`
  - `pod 'mob_sharesdk/ShareSDKPlatforms/WeChat'`
  - `pod 'mob_sharesdk/ShareSDKPlatforms/WeChatFull'`
- `WeChat` 与 `WeChatFull` 不能共存，只能选一个
- 如需分享菜单 UI，除 `ShareSDKUI` 外还可能需要 `pod 'mob_sharesdk/ShareSDKExtension'`
- 可选配置文件分享模块是 `pod 'mob_sharesdk/ShareSDKConfigFile'`
- `Info.plist` 里需要配置 `MOBAppKey` 与 `MOBAppSecret`
- 隐私同意后、在使用 SDK 能力前，需要调用 `MobSDK uploadPrivacyPermissionStatus`
- 第三方平台注册通常在 `application:didFinishLaunchingWithOptions:` 中调用 `[ShareSDK registPlatforms:^{}]`
- 微信、QQ、微博在当前官方示例里都带有 `universalLink` 参数
- `Other Linker Flags` 需要添加 `-ObjC`
- 使用 `Xcode 15` 编译时，官方文档额外要求在 `Other Linker Flags` 中添加 `-ld64`
- 微博需要补 ATS 配置
- 如果要强制 HTTPS，可在 `Info.plist` 中配置 `MOBForceHttps = YES`
- iOS 13+ 下，微博、微信、QQ、Line 需要校验 Universal Link，并在工程中配置 `Associated Domains`
- **`showShareActionSheet` 的 `onStateChanged` 回调共 6 个参数**：`(SSDKResponseState, SSDKPlatformType, [AnyHashable: Any]?, SSDKContentEntity?, (any Error)?, Bool)`
- **`showShareActionSheet` 必须传 `sheetConfiguration:` 参数**（不能省略），类型为 `SSUIShareSheetConfiguration *`，需先 `#import <ShareSDKUI/ShareSDKUI.h>`
- **`SSDKContentType` 的自动判断枚举值为 `.auto`**（不是 `.typeAuto`）
- **纯 Swift 工程须创建 ObjC 桥接头**导入 `<ShareSDK/ShareSDK.h>`、`<MOBFoundation/MOBFoundation.h>`

### Swift 注意事项

#### 1. 纯 Swift / SwiftUI 工程需创建 ObjC 桥接头

纯 Swift 工程需要创建 `{Target}-Bridging-Header.h`，导入 ObjC 头文件后才可调用 MobSDK / ShareSDK API：

```objc
#import <ShareSDK/ShareSDK.h>
#import <ShareSDKUI/ShareSDKUI.h>
#import <MOBFoundation/MOBFoundation.h>
```

并在 `project.pbxproj` 的目标 build settings 中添加：

```
SWIFT_OBJC_BRIDGING_HEADER = {Target}/{Target}-Bridging-Header.h;
```

#### 2. `onStateChanged` 回调签名

`showShareActionSheet` 的 `onStateChanged` 回调包含 **6 个参数**（不是 4 个）：

```swift
onStateChanged: { state, platformType, userData, entity, error, flag in
    switch state {
    case .success:
        print("分享成功")
    case .fail:
        print("分享失败: \(error?.localizedDescription ?? "")")
    case .cancel:
        print("分享取消")
    default:
        break
    }
}
```

参数含义：`(SSDKResponseState, SSDKPlatformType, [AnyHashable: Any]?, SSDKContentEntity?, (any Error)?, Bool)`

#### 3. SSDKContentType 枚举

正确的自动类型枚举值为 `.auto`（不是 `.typeAuto`，该case不存在）：

```swift
let shareParams = NSMutableDictionary()
shareParams.ssdkSetupShareParams(
    byText: "分享文本",
    images: nil,
    url: URL(string: "https://example.com"),
    title: "标题",
    type: .auto  // ✅ 正确
)
```

## 不编造规则

不要编造以下内容：

- 依赖坐标之外的版本号
- 平台凭证
- 未启用平台的 URL Scheme、白名单和回调逻辑
- 项目里不存在的初始化入口
- 用户实际业务里的分享按钮落点

如果文档没有明确说明，或者当前工程无法安全推断，必须写：

`文档未明确，需向用户确认`

## 默认执行策略

- 默认集成方式：`CocoaPods`
- 默认先生成覆盖 iOS Share 支持平台的完整配置模板，不先追问“要接哪些平台”
- 默认以用户填写的 `ShareSDK_Config.xlsx` 为准决定平台范围：填写则集成，未填写则默认不集成
- 默认不把未填写的平台写进工程
- 默认不运行 `pod install` / `pod update`，先给用户看计划，再执行
- 默认把 SDK 初始化放在用户隐私同意之后

## 执行流程

严格按以下顺序推进：

1. 先扫描工程，再给方案。
2. 先生成配置模板，再等用户填写。
3. 先读取并校验 Excel，再确定平台范围。
4. 修改前先给最小改动计划。
5. 依赖安装前先征求用户确认。
6. 完成后生成项目内说明文档。

## 第一步：扫描工程

优先扫描以下内容：

- `.xcodeproj` / `.xcworkspace`
- `Podfile`
- `Package.swift`
- `AppDelegate` / `SceneDelegate` / SwiftUI `@main`
- `Info.plist`
- 是否已有 `ShareSDK`、`MobSDK`、`MOBAppKey`、`LSApplicationQueriesSchemes`、`CFBundleURLTypes`
- 是否已有 `Associated Domains`
- 当前 `Bundle Identifier`

推荐命令：

- `rg --files -g '*.xcodeproj' -g '*.xcworkspace' -g 'Podfile' -g 'Package.swift'`
- `rg -n 'ShareSDK|MobSDK|MOBAppKey|MOBAppSecret|LSApplicationQueriesSchemes|CFBundleURLTypes|Associated Domains|uploadPrivacyPermissionStatus|registPlatforms'`

扫描后先给出一段简短结论，包含：

- 当前工程的依赖方式
- 当前入口结构
- 是否已有 ShareSDK 残留
- 下一步是生成配置模板还是直接读取已有 `ShareSDK_Config.xlsx`

## 第二步：注册社交平台信息

### 2-1 生成配置模板文件

扫描工程后，如未发现用户项目根目录已有 `ShareSDK_Config.xlsx`，执行：

1. 运行本 skill 目录下的 `assets/generate_excel_template.py`。
2. 使用脚本生成或更新本 skill 目录下的 `assets/ShareSDK_Config_Template.xlsx`。
3. 将 `assets/ShareSDK_Config_Template.xlsx` 复制到用户项目根目录。
4. 在用户项目根目录命名为 `ShareSDK_Config.xlsx`。

模板必须包含：

- `基础信息` Sheet
- `平台申请地址` Sheet
- 每个平台独立 Sheet

支持的 iOS Share 平台至少包含以下这些，模板中都要出现：

国内平台：

- 抖音
- 新浪微博
- QQ
- 微信
- 企业微信
- 有道云笔记
- 印象笔记
- 易信好友
- 明道
- 人人网
- 开心网
- 钉钉(DingTalk)
- 美拍
- 中国移动
- 中国电信（天翼）
- 快手
- 支付宝

国外平台：

- Line
- Facebook
- Twitter
- Google+
- LinkedIn
- Flickr
- Pinterest
- Tumblr
- Dropbox
- Instagram
- VKontakte
- Kakao
- YouTube
- Telegram
- Reddit
- TikTok
- SnapChat

复制完成后，必须告知用户：

```text
已在你项目的根目录生成 {path}/ShareSDK_Config.xlsx 配置文件。

请打开该文件，按以下步骤填写：
1. 在"基础信息"Sheet 中填写 MobTech 的 appKey 和 appSecret
   （从 https://www.mob.com/ 注册应用获取）
2. 在相应平台的 Sheet 中填写需要启用的平台配置
   （填写则集成，不填写则默认不集成）
3. "平台申请地址"Sheet 中有各开放平台的申请链接

填写完成后告诉我"填好了"，我将继续下一步。
```

### 2-2 等待用户填写完成

生成 `ShareSDK_Config.xlsx` 后必须暂停，不要继续修改工程。

等待用户回复：

- `填好了`
- `已填写`
- `配置好了`
- 或其它明确表示 Excel 已填写完成的表达

用户未明确表示填写完成前，不读取配置、不改 `Podfile`、不改 `Info.plist`、不写初始化代码。

不要在这一步先问用户“你想集成哪些平台”。

### 2-3 读取并验证配置

用户表示填写完成后，读取用户项目根目录的 `ShareSDK_Config.xlsx`。

平台启用规则：

- 某个平台 Sheet 中只要用户填写了有效平台凭证或关键配置字段，就视为“要集成”
- 某个平台 Sheet 完全留空，则视为“不集成”
- 不要要求用户额外再口头确认平台列表

验证规则：

| 检查项 | 规则 | 不通过时的提示 |
| --- | --- | --- |
| `appKey` | 必填，不能为空字符串 | `基础信息 Sheet 中的 appKey 未填写，请从 MobTech 官网获取` |
| `appSecret` | 必填，不能为空字符串 | `基础信息 Sheet 中的 appSecret 未填写` |
| 微信 `appId` | 如填写，必须以 `wx` 开头 | `微信 appId 格式不正确，应以 wx 开头（如 wx1234567890abcdef）` |
| 微信 `appSecret` | 如填写，长度应为 32 位 | `微信 appSecret 格式不正确，应为 32 位字符串` |
| QQ `appId` | 如填写，必须为纯数字 | `QQ appId 格式不正确，应为纯数字（如 100371282）` |
| QQ `appKey` | 如填写，长度应为 16 位 | `QQ appKey 格式不正确，应为 16 位字符串` |
| 微博 `appKey` | 如填写，不能为空 | `微博 appKey 未填写` |

类型转换规则：

- `appId`、`appKey`、`appSecret`、`userName`、`path` 等标识符字段，强制转为字符串，即使 Excel 中填写的是数字，如 `12345`，也要转为 `"12345"`。
- `withShareTicket`、`bypassApproval`、`shareByAppClient` 等布尔字段，转为 `true` / `false`，不加引号。
- `miniprogramType` 等数字字段，转为整数，不加引号。

如果不合法，必须停止并提示：

```text
配置信息验证失败，请修正以下问题：

{具体问题列表}
- 第 1 条：{问题描述}
- 第 2 条：{问题描述}

请修改 Excel 文件后保存，然后重新告诉我"填好了"。
```

如果合法，提取配置信息，进入第三步。

## 第三步：提取集成配置

从已验证通过的 `ShareSDK_Config.xlsx` 提取后续集成所需配置。

基础信息：

- `mobAppKey`
- `mobAppSecret`
- `bundleIdentifier`
- `teamId`
- `integrationMode`
- `needShareUI`
- `needAuth`
- 已启用平台集合

按平台提取时，遵守：

- 平台是否启用，以对应 Sheet 是否填写为准
- 未填写的平台，不进入后续 `Podfile`、`Info.plist`、URL Scheme、白名单、平台注册代码

按平台提取：

- WeChat：`appId`、`appSecret`、`universalLink`、`useWeChatFull`
- QQ：`appId`、`appKey`、`enableUniversalLink`、`universalLink`
- SinaWeibo：`appKey`、`appSecret`、`redirectUrl`、`universalLink`

其它平台：

- 只提取模板里该平台 Sheet 中实际填写的字段
- 若文档未明确某平台 iOS 所需字段，写 `文档未明确，需向用户确认`

扫描工程后再确认：

- 初始化落点文件
- 分享按钮或服务层落点
- 是否需要 `Associated Domains`
- 是否已有隐私弹窗与同意回调

## 第四步：改动前计划

修改任何文件前，先给出最小改动计划。典型涉及：

- `Podfile`
- `Info.plist`
- `AppDelegate.*`
- `SceneDelegate.*`
- SwiftUI App 入口文件
- 独立的 `ShareSDKRegister` 或 `ShareSDKService`
- 业务层分享入口
- 项目内说明文档，例如 `ShareSDKIntegrationNotes.md`

计划应说明：

- 每个文件为什么改
- 哪些配置来自官方文档
- 哪些值仍需用户提供

## 第五步：实施规则

### A. CocoaPods 依赖

默认按 CocoaPods 集成。

Pod 选择规则：

- 必选：`pod 'mob_sharesdk'`
- 需要官方分享 UI：`pod 'mob_sharesdk/ShareSDKUI'`
- 需要弹出官方分享菜单能力时，补 `pod 'mob_sharesdk/ShareSDKExtension'`
- 需要配置文件分享能力时，按需补 `pod 'mob_sharesdk/ShareSDKConfigFile'`
- 微信按需求二选一：
  - `pod 'mob_sharesdk/ShareSDKPlatforms/WeChat'`
  - `pod 'mob_sharesdk/ShareSDKPlatforms/WeChatFull'`
- QQ：`pod 'mob_sharesdk/ShareSDKPlatforms/QQ'`
- 微博：`pod 'mob_sharesdk/ShareSDKPlatforms/SinaWeibo'`

依赖安装动作规则：

- 改 `Podfile` 之前先告知用户
- 运行 `pod install` 或 `pod update` 前先询问用户
- 若 `mob_sharesdk` 搜索不到，可建议：
  - `pod setup`
  - 再执行依赖更新
- 如果本机 Ruby 版本 ≥ 4.0，`pod install` 可能遇到 `Encoding::CompatibilityError`（Unicode Normalization 兼容问题），需要先设置：
  ```bash
  export LANG=en_US.UTF-8
  pod install
  ```
- 不要在 skill 中默认删除 CocoaPods 缓存；如必须清缓存，先征求用户确认

### B. 初始化与隐私

**向用户说明**

```
根据 MobTech 隐私合规要求和中国区 App 上架规范，使用 ShareSDK 需要在用户同意隐私政策后才能初始化 SDK。

你需要在 App 中：

1. 首次启动时展示《隐私政策》弹窗
2. 用户点击"同意"按钮后，调用隐私授权代码
3. 用户点击"不同意"则不应调用
```



初始化顺序必须遵守：

1. 用户阅读并同意隐私政策
2. 调用 `MobSDK uploadPrivacyPermissionStatus:YES ...`
3. 再进入 ShareSDK 初始化与业务调用

可使用的官方接口：

```objective-c
+ (void)uploadPrivacyPermissionStatus:(BOOL)isAgree
                             onResult:(void (^_Nullable)(BOOL success))handler;
```

或：

```objective-c
+ (void)uploadPrivacyPermissionStatus:(BOOL)isAgree
                  privacyDataDelegate:(id<MOBFoundationPrivacyDelegate> _Nullable)privacyDataDelegate
                             onResult:(void (^_Nullable)(BOOL success))handler;
```

如果工程已有统一隐私网关，优先挂到已有同意回调之后。

如果工程没有隐私弹窗，不要直接帮用户创建完整产品方案；先明确指出这是阻塞项。

### C. 平台注册

平台注册优先放在启动阶段，并保持集中管理。

可采用：

- 独立 Objective-C / Swift 注册辅助类
- AppDelegate 内单点封装方法

官方示例可确认的平台注册方法包括：

- `setupQQWithAppId:appkey:enableUniversalLink:universalLink:`
- `setupWeChatWithAppId:appSecret:universalLink:`
- `setupSinaWeiboWithAppkey:appSecret:redirectUrl:universalLink:`

只注册当前启用的平台。

### D. Info.plist

至少校验并按需写入：

- `MOBAppKey`
- `MOBAppSecret`
- `CFBundleURLTypes`
- `LSApplicationQueriesSchemes`

可按需写入：

- ATS 配置
- `MOBTwitterVer`
- `MOBForceHttps`

**⚠️ 物理 Info.plist 要点（替代 GENERATE_INFOPLIST_FILE 时）**

如果工程使用 `GENERATE_INFOPLIST_FILE = YES`（Xcode 自动生成），而你需要改为物理 Info.plist 文件，务必在 Info.plist 中包含以下关键键，否则安装会失败：

```xml
<key>CFBundleIdentifier</key>
<string>$(PRODUCT_BUNDLE_IDENTIFIER)</string>
<key>CFBundlePackageType</key>
<string>APPL</string>
<key>CFBundleExecutable</key>
<string>$(EXECUTABLE_NAME)</string>
<key>CFBundleVersion</key>
<string>$(CURRENT_PROJECT_VERSION)</string>
<key>CFBundleShortVersionString</key>
<string>$(MARKETING_VERSION)</string>
```

同时，在 `project.pbxproj` 中将目标的：
- `GENERATE_INFOPLIST_FILE = YES` → 删除
- 新增 `INFOPLIST_FILE = {Target}/Info.plist;`
- 删除所有 `INFOPLIST_KEY_*` 条目（因为它们已被物理文件覆盖）

URL Scheme 规则，当前官方已明确：

- 微博：`wb{appKey}`
- 微信：`{wxAppId}`
- Facebook：`fb{apiKey}`
- Twitter：`twitterkit-{consumerKey}`
- QQ / QZone：
  - `tencent{appId}`
  - `QQ{appId的8位大写十六进制}`

如果只启用微信 / QQ / 微博，就不要把 Facebook / Twitter 相关项写进工程。

### E. 白名单

`LSApplicationQueriesSchemes` 只加入当前启用平台需要的条目。

官方文档已列出常见平台白名单，尤其关注：

- 微博：`sinaweibo`、`sinaweibohd`、`sinaweibosso`、`sinaweibohdsso`、`weibosdk`、`weibosdk2.5`、`weibosdk3.3`
- 微信：`weixin`、`weixinULAPI`、`weixinURLParamsAPI`
- QQ / QZone：`mqqOpensdkSSoLogin`、`mqqopensdkapiV2`、`tim`、`mqq`、`mqqapi`、`mqqopensdknopasteboard`、`mqqopensdknopasteboardios16`、`mqqopensdkminiapp`、`mqzone`、`mqqopensdkapiV4` 等

不要在未启用平台时预埋其白名单。

### F. Universal Link 与能力开关

当启用微博、微信、QQ、Line 时，优先检查是否需要：

- `Associated Domains`
- `applinks:xxxx`
- 工程证书 `Team ID`
- 正确的 `Bundle ID`

只有在用户已经提供 Universal Link，或工程中已有明确值时，才直接落地。

如果缺少 Universal Link，先告诉用户该项会阻塞对应平台在 iOS 13+ 的正常能力。

### G. 业务调用

如果用户要求接分享功能，可基于官方 API 接入：

- 菜单分享：`showShareActionSheet:customItems:shareParams:sheetConfiguration:onStateChanged:`
- 直接分享：`share:parameters:onStateChanged:`
- 第三方登录：`authorize:settings:onStateChanged:`

**⚠️ `showShareActionSheet` 完整签名（含 `sheetConfiguration:`）**

```swift
let config = SSUIShareSheetConfiguration()
ShareSDK.showShareActionSheet(
    nil,                           // view (iPad 弹出参照视图)
    customItems: nil,              // items (nil 显示所有已集成平台)
    shareParams: shareParams,      // 分享参数
    sheetConfiguration: config     // 必传，不可省略
) { state, platformType, userData, entity, error, flag in
    // state: SSDKResponseState (.success / .fail / .cancel)
    // error: (any Error)? — 失败时才有值
    switch state {
    case .success:
        print("分享成功")
    case .fail:
        print("失败: \(error?.localizedDescription ?? "")")
    case .cancel:
        print("已取消")
    default:
        break
    }
}
```

**⚠️ `onStateChanged` 回调签名（6 个参数）**

```swift
onStateChanged: { state, platformType, userData, entity, error, flag in
```

**⚠️ ssdkSetupShareParams 的 type 参数**

官方支持的枚举值为 `SSDKContentType`，正确 case 是 `.auto`（不要写 `.typeAuto`，该值不存在）：

```swift
shareParams.ssdkSetupShareParams(
    byText: "文本",
    images: nil,
    url: URL(string: "https://example.com"),
    title: "标题",
    type: .auto  // ✅
)
```

但默认不要擅自把测试文案、测试图片 URL、测试标题直接写进正式业务代码。

## 第六步：校验

完成修改后至少做这些校验：

- `Podfile` 语法看起来无破坏
- `Info.plist` 中关键键存在且结构未损坏：
  - 如果是物理 Info.plist，确认包含 `CFBundleIdentifier`、`CFBundlePackageType`、`CFBundleExecutable`
  - 确认 `MOBAppKey` / `MOBAppSecret` 已填入
  - 确认 `LSApplicationQueriesSchemes` 只包含已启用平台的白名单
  - 确认 `CFBundleURLTypes` 中 URL Scheme 格式正确
- 入口文件已调用隐私同意后的初始化逻辑（先 `uploadPrivacyPermissionStatus`，再 `registPlatforms`）
- 注册代码只包含本次启用的平台
- 未把无关 demo 平台带入工程
- 如果是纯 Swift 工程，确认已创建 ObjC 桥接头并配置了 `SWIFT_OBJC_BRIDGING_HEADER`
- 确认 `project.pbxproj` 中已删除 `GENERATE_INFOPLIST_FILE` 和 `INFOPLIST_KEY_*`（当使用物理 Info.plist 时）

如用户允许安装依赖，再补：

- `pod install`
- 必要时最小构建校验

如果失败，要区分：

- 代码配置问题
- 本机 CocoaPods / Xcode / 签名环境问题

## 第七步：交付内容

完成后最终输出至少包含：

- 改了什么
- 还缺哪些平台凭证或 Universal Link
- 隐私同意后的初始化落点在哪
- 写入了哪些 `Info.plist` 键
- 使用了哪些官方链接

如用户允许，额外生成项目内说明文档，例如：

- `ShareSDKIntegrationNotes.md`

建议说明文档内容：

- 已启用的平台
- Pod 依赖清单
- 必填凭证清单
- URL Scheme 清单
- 白名单清单
- Universal Link / Associated Domains 清单
- 初始化入口
- 隐私接口调用时机
- 官方文档链接

## 边界

不要做这些事：

- 默认启用全部平台
- 未经确认就切换到 SPM 或手动集成
- 在用户未同意前自动执行 `pod install`
- 把测试分享代码直接塞进生产页面
- 在没有隐私同意链路时直接初始化 ShareSDK
- 把官方文档里无关平台的配置一并写入工程
