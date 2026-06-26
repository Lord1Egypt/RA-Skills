# ios-sharesdk-integreation

这是一个面向 Codex Agent 的 iOS ShareSDK 集成 skill，默认使用 CocoaPods，把 MobTech ShareSDK 以最小改动方式接入真实 iOS 工程。

## 目标

这个 skill 会指导 Agent：

- 先扫描工程结构，再决定改动点
- 默认沿用 CocoaPods，并按平台最小化引入 Pod
- 把隐私同意与 SDK 初始化顺序放在第一优先级
- 只为当前启用的平台写入 URL Scheme、白名单和 Universal Link 配置
- 在完成后补一份项目内集成说明

## 适用场景

当用户提出以下需求时适用：

- 在 iOS 项目中接入 ShareSDK
- 使用 CocoaPods 集成 MobTech ShareSDK
- 配置微信、QQ、微博分享或第三方登录
- 补充 `MOBAppKey`、`MOBAppSecret`、URL Scheme、白名单、Universal Link
- 处理 ShareSDK iOS 隐私合规和 `uploadPrivacyPermissionStatus`
- 清理旧 ShareSDK demo 残留并整理成正式工程接入

## 官方来源

主文档：

- https://www.mob.com/wiki/detailed?wiki=4&id=14
- https://www.mob.com/wiki/detailed?wiki=500&id=14

关联合规资料：

- https://www.mob.com/wiki/detailed?wiki=499&id=14
- https://www.mob.com/wiki/detailed?wiki=747&id=14
- https://policy.zztfly.com/sdk/share/privacy

## 当前 skill 的默认策略

- 默认集成方式：`CocoaPods`
- 默认不启用所有平台，必须先缩小到本次需要的平台
- 默认把初始化放在隐私同意之后
- 默认只在用户确认后执行 `pod install` / `pod update`

## 目录内容

- `SKILL.md`：Agent 执行流程说明
- `assets/generate_excel_template.py`：生成最小配置模板
- `assets/ShareSDK_Config_Template.xlsx`：配置模板产物
- `examples/example-prompts.md`：示例触发问法

## 这版 skill 已固化的官方关键信息

- `mob_sharesdk` 是主 Pod
- 微信、QQ、微博平台 Pod 可按需单独接入
- `MOBAppKey` 与 `MOBAppSecret` 需要写入 `Info.plist`
- 用户同意隐私政策后，需要调用 `MobSDK uploadPrivacyPermissionStatus`
- `Xcode 15` 下官方要求额外补 `-ld64`
- 微信、QQ、微博在 iOS 13+ 下涉及 Universal Link 配置

## 说明

目录名按你的要求保留为 `ios-sharesdk-integreation`，不修正拼写。
