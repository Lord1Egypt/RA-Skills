# MobLink 集成说明

## 本次改动目标

在当前 iOS 项目中接入 MobTech MobLink，完成最小可运行的场景还原 SDK 配置、隐私合规接线、MobId 制作入口和恢复代理回调落点。

## 本次改动文件

- `Podfile`
- `Podfile.lock`
- `Info.plist`
- App 启动入口文件
- 隐私同意回调文件
- 场景制作业务入口文件
- 场景还原代理或路由文件
- 其他按实际项目补充

## 已接入内容

- `mob_linksdk_pro` 依赖
- `MOBAppKey`
- `MOBAppSecret`
- `MOBNetLater = 2`
- `uploadPrivacyPermissionStatus`
- `MobLink setDelegate:`
- `getMobId`
- `IMLSDKWillRestoreScene:Restore:`

## 仍需开发者确认或补完

- MobLink 后台 iOS 页面名称、渠道标识和 path 是否与代码一致
- Web 落地页是否已按官方 Web 集成文档接入
- Universal Link / URL Scheme 是否已在 MobLink 后台和 Apple Developer 后台配置完成
- App Store Connect 后台隐私数据项是否已按官方文档配置
- 真机场景制作、分享链路和恢复链路是否已验证
- 如需扩展业务主动控制器，请先阅读官方文档，再单独确认位置、IDFA、IDFV、WiFi、IP 等数据采集策略

## 官方文档

- MobTech 文档中心：https://www.mob.com/wiki/list
- MobLink 产品简介：https://www.mob.com/wiki/detailed?wiki=161&id=34
- 创建应用流程：https://www.mob.com/wiki/detailed?wiki=478&id=34
- MobLink 后台与项目配置：https://www.mob.com/wiki/detailed?wiki=527&id=34
- iOS 集成指南：https://www.mob.com/wiki/detailed?wiki=83&id=34
- iOS SDK API：https://www.mob.com/wiki/detailed?wiki=553&id=34
- iOS 合规指南：https://www.mob.com/wiki/detailed?wiki=220&id=34
- MobLink 扩展业务功能设置：https://www.mob.com/wiki/detailed?wiki=673&id=34
- Web 集成：https://www.mob.com/wiki/detailed?wiki=525&id=34
- App Store Connect 后台隐私数据项配置：https://www.mob.com/wiki/detailed?wiki=574&id=34
- 其它 App 数据采集主动控制器配置：https://www.mob.com/wiki/detailed?wiki=675&id=714
- MobLink 隐私政策：https://policy.zztfly.com/sdk/link/privacy
