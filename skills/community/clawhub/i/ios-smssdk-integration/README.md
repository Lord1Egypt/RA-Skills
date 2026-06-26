# ios-smssdk-integration

这是一个面向 Codex Agent 的 iOS SMSSDK 集成 skill，目标是在真实 iOS 工程里，以最小改动完成依赖接入、隐私合规、短信验证码发送/校验链路和项目内说明文档落地。

## 目录结构

```text
ios-smssdk-integration/
├── SKILL.md
├── README.md
├── assets/
│   ├── SMSSDK_iOS_Config_Template.xlsx
│   └── generate_excel_template.py
└── examples/
    └── example-prompts.md
```

## 这个 skill 会指导 Agent 做什么

- 先扫描工程，再决定接入点
- 默认优先使用 `CocoaPods`
- 默认生成最小配置模板，不收集可从工程推断的信息
- 扫描时记录工程语言形态：Objective-C、Swift 或混编
- 把 `uploadPrivacyPermissionStatus` 放在用户同意隐私政策之后
- 在手机号链路中接入 `getVerificationCodeByMethod` 和 `commitVerificationCode`
- 支持 Objective-C 与 Swift 接入代码，Swift 工程按现有混编方式处理桥接头
- Swift 工程默认通过 Objective-C wrapper 接入 SMSSDK，wrapper 内优先导入 `<SMS_SDK/SMSHeader.h>`
- 识别 CocoaPods workspace 是否有效生成，并处理 `pod install` 后的构建验证
- 遇到 CocoaPods 写入 `~/.cocoapods` 或 Xcode 访问用户目录的权限问题时，按当前环境申请授权后重试
- 语音验证码、本机号码认证和扩展业务主动控制器默认作为可选能力
- 完成后补一份项目内 `SMSSDK_README.md`

## 已固化的关键事实

- 默认 Pod：`pod 'mob_smssdk'`
- 需要 `MOBAppKey`、`MOBAppSecret`、`MOBNetLater = 2`
- 隐私授权回传接口是 `uploadPrivacyPermissionStatus`
- 请求验证码接口是 `getVerificationCodeByMethod`
- 提交验证码接口是 `commitVerificationCode`
- 使用 `SMSSDKAuthToken` 等模型类型时优先导入 `<SMS_SDK/SMSHeader.h>`，避免模块导入顺序错误
- `zone` 不要加 `+`
- 默认签名仅用于测试，不保证到达率；上线前必须申请自定义签名
- 扩展业务主动控制器和本机号码认证属于可选能力

## 参考资料

官方链接：

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
