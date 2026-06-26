# MobPush 集成说明

## 本次改动目标

在当前 iOS 项目中接入 MobTech MobPush，完成最小可运行的推送初始化、隐私合规接线和通知回调落点。

## 本次改动文件

- `Podfile`
- `Podfile.lock`
- `Info.plist`
- App 启动入口文件
- 隐私同意回调文件
- 其他按实际项目补充

## 已接入内容

- `mob_pushsdk` 依赖
- `MOBAppKey`
- `MOBAppSecret`
- `MOBNetLater = 2`
- `setAPNsForProduction:`
- `setupNotification:`
- `uploadPrivacyPermissionStatus`
- `MobPushDidReceiveMessageNotification`

## 仍需开发者确认或补完

- Apple Developer 后台 Push 能力是否已开启
- MobPush 控制台 APNs 鉴权材料是否已配置完成
- 真机推送链路是否已用开发/生产环境分别验证
- 如需 tag、alias、badge、本地通知、Live Activity，是否继续补业务接线

## 官方文档

- 创建应用流程：https://www.mob.com/wiki/detailed?wiki=494&id=136
- 合规指南：https://www.mob.com/wiki/detailed?wiki=501&id=136
- 集成指南：https://www.mob.com/wiki/detailed?wiki=502&id=136
- SDK API：https://www.mob.com/wiki/detailed?wiki=503&id=136
- 证书配置：https://www.mob.com/wiki/detailed?wiki=504&id=136
- App Store Connect 后台隐私数据项配置：https://www.mob.com/wiki/detailed?wiki=570&id=136
- MobPush 扩展业务功能设置：https://www.mob.com/wiki/detailed?wiki=665&id=136
- 其它 App 数据采集主动控制器配置：https://www.mob.com/wiki/detailed?wiki=675&id=714
- MobPush 隐私政策：https://policy.zztfly.com/sdk/mobpush/privacy
