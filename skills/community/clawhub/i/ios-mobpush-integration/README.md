# ios-mobpush-integration

这是一个面向 Codex Agent 的 iOS MobPush 集成 skill，目标是在真实 iOS 工程里，以最小改动完成推送依赖接入、APNs 前置准备、隐私合规、通知回调接线和项目内说明文档落地。

## 目录结构

```text
ios-mobpush-integration/
├── SKILL.md
├── README.md
├── assets/
│   ├── MobPush_iOS_Config_Template.xlsx
│   └── generate_excel_template.py
├── examples/
│   └── example-prompts.md
└── templates/
    └── MOBPUSH_README.md
```

## 这个 skill 会指导 Agent 做什么

- 先扫描工程，再决定接入点
- 默认优先使用 `CocoaPods`
- 默认生成最小配置模板，不收集可从工程推断的信息
- 扫描时记录工程语言形态：Objective-C、Swift 或混编
- 把 `uploadPrivacyPermissionStatus` 放在用户同意隐私政策之后
- 在 App 启动链路中接入 `setAPNsForProduction:` 与 `setupNotification:`
- 接入 `MobPushDidReceiveMessageNotification` 通知监听
- 支持 Objective-C 与 Swift 工程，Swift 优先复用现有 Bridging Header
- 识别 CocoaPods workspace 是否有效生成，并处理 `pod install` 后的验证
- 可按需扩展 tag、alias、badge、本地通知和 Live Activity 能力
- 完成后补一份项目内 `MobPush_README.md`

## 已固化的关键事实

- 默认 Pod：`pod 'mob_pushsdk'`
- 需要 `MOBAppKey`、`MOBAppSecret`
- 合规模式需加 `MOBNetLater = 2`
- 需要开启 `Push Notifications`
- 需要开启 `Background Modes > Remote notifications`
- 依赖 `libc++.tbd`、`libz.1.2.5.tbd`
- `uploadPrivacyPermissionStatus` 是 MobSDK 业务起点
- `.p12` 和 `.p8` 鉴权都支持
- Live Activity 需要 `iOS 16.1+`、`SwiftUI`、`ActivityKit`

## 参考资料

官方链接：

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

## 说明

这个 skill 只把官方文档中明确的信息固化为执行规则。文档未明确的内容，例如 SPM 支持、完整 Live Activity 官方深链地址、Notification Service Extension 必需性，不会被硬编码进流程，而是保留为执行时确认项。

