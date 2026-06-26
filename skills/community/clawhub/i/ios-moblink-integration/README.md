# ios-moblink-integration

这是一个面向 Codex Agent 的 iOS MobLink 集成 skill，目标是在真实 iOS 工程里，以最小改动完成场景还原依赖接入、隐私合规、MobId 制作、场景恢复回调和项目内说明文档落地。

## 目录结构

```text
ios-moblink-integration/
├── SKILL.md
├── README.md
├── assets/
│   ├── MobLink_iOS_Config_Template.xlsx
│   └── generate_excel_template.py
├── examples/
│   └── example-prompts.md
└── templates/
    └── MOBLINK_README.md
```

## 这个 skill 会指导 Agent 做什么

- 先扫描工程，再决定接入点
- 默认优先使用 `CocoaPods`
- 默认生成最小配置模板，不收集可从工程推断的信息
- 最小配置模板不收集扩展业务主动控制器配置
- 扫描时记录工程语言形态：Objective-C、Swift 或混编
- 把 `uploadPrivacyPermissionStatus` 放在用户同意隐私政策之后
- 在 App 启动链路中接入 `MobLink setDelegate:`
- 按需接入 `getMobId` 制作场景
- 按需接入 `IMLSDKWillRestoreScene:Restore:` 场景还原回调
- 支持 Objective-C 与 Swift 工程，Swift 优先复用现有 Bridging Header
- 识别 CocoaPods workspace 是否有效生成，并处理 `pod install` 后的验证
- 可按需扩展 Universal Link、Web 集成和扩展业务主动控制器；主动控制器只在 README 中保留官方文档链接，执行时单独确认
- 完成后补一份项目内 `MobLink_README.md`

## 已固化的关键事实

- 默认 Pod：`pod 'mob_linksdk_pro'`
- 需要 `MOBAppKey`、`MOBAppSecret`
- 合规模式需加 `MOBNetLater = 2`
- 需要在用户同意隐私政策后调用 `uploadPrivacyPermissionStatus`
- 需要 `MobLink setDelegate:` 接入场景恢复代理
- 制作场景使用 `MLSDKScene` 和 `getMobId`
- 场景还原回调 `IMLSDKWillRestoreScene:Restore:` 一旦实现必须执行 `restoreHandler`
- 手动集成需要 `MobLinkPro.framework`、`MOBFoundation.framework`
- 需要链接 `libsqlite3`、`libz1.2.5`、`libc++`

## 参考资料

官方链接：

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

## 说明

这个 skill 只把官方文档中明确的信息固化为执行规则。文档未明确的内容，例如 Swift Package Manager 支持、Privacy Manifest、业务页面 path、Universal Link 域名和 Web 落地页配置，不会被硬编码进流程，而是保留为执行时确认项。
