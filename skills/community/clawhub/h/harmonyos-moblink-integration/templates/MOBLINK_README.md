# MobLink 集成说明

本文档由 MobLink 集成 skill 生成，用于记录当前项目的 MobLink 接入信息。

## 已完成配置

- ohpm 依赖：`@zztsdk/zztcore`、`@zztsdk/moblink`
- ZztSDK 初始化：`ZztSDK.init(context, appKey, appSecret)`
- 隐私授权提交：`ZztSDK.submitPolicyGrantResult(true)`
- MobLink 初始化：`mobLink.init(context)`
- 场景还原监听：`mobLink.setRestoreSceneListener(receiver)`
- onNewWant 处理：`mobLink.updateNewWant(want)`
- URI scheme 配置：`module.json5` skills 标签

## 关键参数

- appKey：`{appKey}`
- appSecret：已配置，勿在文档中明文扩散
- bundleName：`{bundleName}`
- uriScheme：`{uriScheme}`
- host：`{host}`
- 默认场景路径：`{defaultScenePath}`
- 承接 Ability：`{restoreAbility}`
- AbilityStage 路径：`{abilityStagePath}`

## 已修改文件

- `oh-package.json5`：添加了 @zztsdk/zztcore 和 @zztsdk/moblink 依赖
- `module.json5`：添加了权限和 URI scheme 配置
- `{abilityStageFile}`：添加了全局场景还原监听器
- `{entryAbilityFile}`：添加了 onNewWant 处理
- `{privacyCallbackFile}`：添加了隐私授权回调代码

## 初始化位置

`{abilityStageFile}` 或 `{entryAbilityFile}`

## API 调用位置

- ZztSDK.init：`{initLocation}`
- ZztSDK.submitPolicyGrantResult：`{privacyCallbackLocation}`
- mobLink.init：`{mobLinkInitLocation}`
- mobLink.getMobID：`{getMobIDLocation}`
- mobLink.setRestoreSceneListener：`{abilityStageFile}`
- mobLink.updateNewWant：`{entryAbilityFile}`

## 隐私合规

- 隐私政策展示位置：`{privacyPolicyLocation}`
- 用户同意后调用位置：`{privacyCallbackLocation}`
- 数据采集控制：`{privacyControllerLocation}`

## 后续维护

1. 如需新增业务场景，创建新的 `Scene` 并设置 `path` 与 `params`。
2. 使用 `mobLink.getMobID(scene, listener)` 获取 mobID 后拼接到业务链接。
3. 在承接 Ability 中解析 Scene 数据并跳转业务页面。
4. Ability 必须在 `onNewWant` 中调用 `mobLink.updateNewWant(want)`。
5. 隐私政策变更时，同步确认 `ZztSDK.submitPolicyGrantResult(...)` 的调用时机仍在用户授权之后。

## 官方文档

- HarmonyOS NEXT 集成指南：https://mob.com/wiki/detailed?wiki=731&id=34
- MobLink 后台基本配置：https://mob.com/wiki/detailed?wiki=527&id=34
- MobLink 鸿蒙端合规使用说明：https://mob.com/wiki/detailed?wiki=758&id=34
- 常见问题：https://mob.com/wiki/detailed?wiki=530&id=34
- 扩展业务功能设置：https://www.mob.com/wiki/detailed?wiki=730&id=34
