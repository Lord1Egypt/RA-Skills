# ios-flyverify-integration

这是一个面向 Codex Agent 的 iOS FlyVerify(秒验) 集成 skill，目标是在真实 iOS 工程里，以最小改动完成依赖接入、隐私合规、一键登录链路接线和项目内说明文档落地。

## 目录结构

```text
ios-flyverify-integration/
├── SKILL.md
├── README.md
├── assets/
│   ├── FlyVerify_iOS_Config_Template.xlsx
│   └── generate_excel_template.py
└── examples/
    └── example-prompts.md
```

## 这个 skill 会指导 Agent 做什么

- 先扫描工程，再决定接入点
- 默认优先使用 `CocoaPods`
- 默认生成最小配置模板，不收集可从工程推断的信息
- 扫描时记录工程语言形态：Objective-C、Swift 或混编
- 把 `agreePrivacy` 放在用户同意隐私政策之后
- 在登录链路中接入 `preLogin`、授权页拉起和 token 成功回调
- 支持 Objective-C 与 Swift 接入代码，Swift 工程通过桥接头调用官方 API
- 识别 CocoaPods workspace 是否有效生成，并处理 `pod install` 后的构建验证
- 优先用真机目标验证 FlyVerify；部分运营商 SDK 可能不支持模拟器链接
- 扩展业务主动控制器不作为前置问询，只在最终项目文档中说明
- 完成后补一份项目内 `FlyVerify_README.md`

## 已固化的关键事实

- 默认 Pod：`pod 'FlyVerify'`
- 需要 `flyverifykey`、`flyverifysecret`、`FlyVerifyPLevel = 2`
- 需要 `-ObjC`
- 依赖移动蜂窝网络取号
- SDK 成功后只返回 token，手机号置换属于后续服务端步骤，客户端先保留注释占位
- Swift 调用授权页 API 时，`openAuthPageWithModel` 对应首参标签是 `withModel:`
- Xcode 15+ 遇到 CocoaPods 资源脚本被 sandbox 拦截时，可设置 `ENABLE_USER_SCRIPT_SANDBOXING = NO`
- 扩展业务控制器和复杂授权页定制都属于可选能力

## 参考资料

官方链接：

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

## 说明

仓库里原有一个 `ios-flyverify-integreation` 目录，内容是误拷贝的 ShareSDK skill，且目录名拼写也有误。这版新目录不覆盖旧目录，避免破坏已有历史。
