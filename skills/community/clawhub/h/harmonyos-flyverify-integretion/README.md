# harmonyos-flyverify-integretion

用于协助 Agent 在 HarmonyOS NEXT 项目中集成 MobTech FlyVerify（秒验/妙验）。

## 能做什么

- 识别并校验 HarmonyOS 项目结构
- 生成 `FlyVerify_HarmonyOS_Config_Template.xlsx`
- 校验 `appKey`、`appSecret`、功能开关和超时
- 修改 `build-profile.json5`
- 修改 `entry/src/main/module.json5`
- 插入 `ZztSDK.init(...)`
- 插入 `ZztSDK.submitPolicyGrantResult(...)`
- 插入 `FlyVerify.preVerify(...)` / `FlyVerify.verify(...)`
- 配置 `FlyVerify.setPreVerifyTimeout(...)`
- 生成授权页 `ThemeConfig` 定制代码
- 汇总错误码排查说明

## 文档依据

- [集成指南](/Users/haodongling/.ai/skills/资料/harmony-flyverify/集成指南.md)
- [SDK API](/Users/haodongling/.ai/skills/资料/harmony-flyverify/SDK%20API.md)
- [SDK返回码](/Users/haodongling/.ai/skills/资料/harmony-flyverify/SDK返回码.md)
- [秒验SDK扩展业务功能设置](/Users/haodongling/.ai/skills/资料/harmony-flyverify/秒验SDK扩展业务功能设置.md)
- 官方集成指南：`https://www.mob.com/wiki/detailed?wiki=717&id=78`
- 秒验鸿蒙端合规指南：`https://www.mob.com/wiki/detailed?wiki=754&id=78`

## 已确认要求

- API 支持：`>= 12`
- 依赖：
  - `ohpm install @zztsdk/zztcore`
  - `ohpm install @zztsdk/flyverify`
- `build-profile.json5`：
  - `compatibleSdkVersion: "5.0.0(12)"`
  - `useNormalizedOHMUrl: true`
- `module.json5` 权限：
  - `ohos.permission.INTERNET`
  - `ohos.permission.GET_NETWORK_INFO`
- 初始化：
  - `ZztSDK.init(context, appKey, appSecret)`
- 隐私授权：
  - `ZztSDK.submitPolicyGrantResult(true)`
- 预取号：
  - `FlyVerify.preVerify(...)`
- 取号：
  - `FlyVerify.verify(uiContext, ...)`

## 应用配置前置规则

- 如果缺少 `appKey` 或 `appSecret`，skill 必须直接停止
- 不继续执行依赖安装、工程改动、联调或验收
- 只允许保留配置收集结果，等待用户先去 Mob 开发者后台申请配置后再继续
- 申请地址：`https://new.dashboard.mob.com/#/summary`

## 唯一主要风险

扩展业务控制器文档存在命名不一致：

- 一处写 `ZztCustomController`
- 一处写 `MobCustomController`

因此基础接入没有问题，但如果要接扩展业务控制器，Agent 需要先检查实际依赖导出的类名再落代码。

## 建议使用方式

1. 提供 HarmonyOS 项目路径
2. 生成并填写 Excel 配置模板
3. 让 Agent 读取模板并校验
4. 先确认 `build-profile.json5`、`module.json5`
5. 再通过对话告知隐私回调位置
6. 再落 `preVerify` / `verify` / UI 定制代码

## 交互要求

- 一次只问开发者一个阻塞问题
- `bundleName` 优先从工程推断，不要放进 Excel，也不要先问
- `ohpm install` 是否代执行放到最后再问，不要与隐私回调、业务落点并行追问
