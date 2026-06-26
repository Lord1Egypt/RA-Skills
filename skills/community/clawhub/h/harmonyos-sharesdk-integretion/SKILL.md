---
name: harmonyos-sharesdk-integretion
description: Interactive guide for integrating MobTech ShareSDK into HarmonyOS NEXT projects. Use when the user wants ShareSDK sharing or Huawei authorization in a HarmonyOS app, and needs help with ohpm dependencies, module.json5 permissions, AppKey/AppSecret setup, privacy compliance, or post-integration ShareSDK extension capability guidance.
tags:
  - harmonyos
  - harmonyos-next
  - sharesdk
  - mobtech
  - sdk-integration
  - social-share
  - privacy
  - arkts
---

# HarmonyOS ShareSDK 集成 Skill

## 适用场景

当用户提到以下任一主题时，使用本 skill：

- HarmonyOS ShareSDK 集成
- 鸿蒙接入 ShareSDK
- HarmonyOS 分享能力接入
- ShareSDK HarmonyOS NEXT
- 华为授权接入
- MobTech ShareSDK 鸿蒙集成
- ShareSDK 隐私合规
- ShareSDK 扩展业务功能后续调整

如果用户的问题明确涉及 HarmonyOS NEXT 工程、`ohpm` 依赖、`module.json5` 权限、MobTech `AppKey` / `AppSecret`、`ZztSDK.submitPolicyGrantResult()` 或分享/授权功能接入，应优先使用本 skill。

## 官方文档来源

- 集成指南：https://www.mob.com/wiki/detailed?wiki=696&id=14
- 扩展业务功能设置：https://www.mob.com/wiki/detailed?wiki=711&id=14
- 鸿蒙端合规使用说明：https://www.mob.com/wiki/detailed?wiki=748&id=14
- 新浪微博授权与分享：https://www.mob.com/wiki/detailed?wiki=722&id=14
- 微信授权与分享：https://www.mob.com/wiki/detailed?wiki=724&id=14

## 已确认的官方信息

- 开发工具：DevEco Studio
- 集成方式：在线集成
- HarmonyOS API 支持：`>= 12`
- 依赖安装方式：
  - `ohpm install @zztsdk/zztcore`
  - `ohpm install @zztsdk/sharesdk`
- 文档明确要求在 `entry` 模块的 `module.json5` 中配置 `ohos.permission.INTERNET`
- 文档明确支持：
  - 分享能力
  - 华为授权
  - 新浪微博授权与分享
  - 微信授权与分享
  - `ZztSDK.submitPolicyGrantResult(...)` 隐私授权回传
  - `ZztCustomController` 主动数据采集控制
  - `setUIAbilityContext(...)` 以支持分享/授权 UI 能力
  - 扩展业务功能后续控制能力

## 基础集成默认策略

本 skill 按你的要求采用“先完成基础接入，再在文档中说明后续扩展”的策略：

- 基础集成阶段只主动声明必需权限
- 不在 Excel 模板中提供“权限/可选能力”开关给开发者选择
- 不在基础集成阶段主动插入 `ZztCustomController` 控制逻辑
- 仅在集成完成后的项目说明文档中描述 `ShareSDK 扩展业务功能设置`，供后期调整

基础集成阶段默认只声明以下必需权限：

- `ohos.permission.INTERNET`
除 `INTERNET` 外，其它权限不主动写入 `module.json5`。如果用户后续需要启用扩展业务功能、设备标识、网络信息、位置或 WiFi 相关能力，再根据实际需求补充。

## 文档未明确的事项

以下内容在官方文档中未给出完整写法，执行时必须先检查实际工程和已安装依赖，不可凭空补全：

- `@zztsdk/zztcore` 和 `@zztsdk/sharesdk` 的 ArkTS 导入语句
- `params` 在 `plat.authorize(params)` 中的字段结构
- 是否必须修改 `oh-package.json5`、`build-profile.json5`、`app.json5`
- 项目中推荐放置初始化代码、分享代码、授权代码的具体文件路径
- 微博 `Scope` 的具体业务取值
- 微信小程序分享涉及的 `miniProgramUserName`、`miniProgramPath`、缩略图资源来源

如果用户要求你写这些部分，先扫描工程现状、已安装依赖和类型声明；若仍无法确认，明确告诉用户“官方文档未明确”。

## 6 步交互式集成工作流

所有写文件和改文件操作前，都必须先展示计划修改内容并等待用户确认。

### 步骤 1：启动流程

#### 1-1 询问项目路径

主动询问用户提供 HarmonyOS 项目根路径，例如：

```text
/Users/xxx/your-harmony-project
```

#### 1-2 验证项目结构

至少检查以下文件中的一种或多种是否存在：

- `build-profile.json5`
- `oh-package.json5`
- `entry/src/main/module.json5`
- 其他模块下的 `src/main/module.json5`

优先识别 `entry` 模块的 `module.json5`。

如果路径不合法或不像 HarmonyOS 工程，提示：

```text
路径验证失败，未识别到有效的 HarmonyOS 工程结构。

请确认项目根目录下至少存在以下文件之一：
- build-profile.json5
- oh-package.json5
- entry/src/main/module.json5
```

### 步骤 2：生成并填写配置模板

#### 2-1 生成 Excel 模板

执行：

1. 运行 `assets/generate_excel_template.py`
2. 生成 `assets/ShareSDK_HarmonyOS_Config_Template.xlsx`
3. 复制到用户项目根目录并命名为 `ShareSDK_HarmonyOS_Config.xlsx`

#### 2-2 告知用户填写内容

明确要求用户填写：

- MobTech `appKey`
- MobTech `appSecret`
- HarmonyOS 包名（或应用标识）
- 是否启用华为授权
- 如启用华为授权，则填写 `client_id`
- 是否启用微博授权/分享
- 如启用微博，则填写：
  - 微博 `AppKey`
  - `RedirectURI`
  - `CallbackAbilityName`
  - `Scope`（如项目需要）
- 是否启用微信授权/分享
- 如启用微信，则填写：
  - 微信 `AppKey`
  - 微信 `AppSecret`

等待用户回复“填好了”后再继续。

#### 2-3 校验规则

读取 `ShareSDK_HarmonyOS_Config.xlsx` 后，至少校验：

- `appKey`：必填，不能为空
- `appSecret`：必填，不能为空
- `bundleName`：必填，不能为空
- `apiVersion`：如填写，必须是整数且应 `>= 12`
- `enableHuaweiAuth`：必须可转换为 `true` / `false`
- `clientId`：当 `enableHuaweiAuth=true` 时必填
- `enableWeibo`：必须可转换为 `true` / `false`
- `weiboAppKey`：当 `enableWeibo=true` 时必填
- `weiboRedirectUrl`：当 `enableWeibo=true` 时必填
- `weiboCallbackAbilityName`：当 `enableWeibo=true` 时必填
- `enableWechat`：必须可转换为 `true` / `false`
- `wechatAppKey`：当 `enableWechat=true` 时必填
- `wechatAppSecret`：当 `enableWechat=true` 时必填

类型转换规则：

- `appKey`、`appSecret`、`clientId`、`bundleName` 一律按字符串处理
- `weiboAppKey`、`weiboRedirectUrl`、`weiboCallbackAbilityName`、`weiboScope`、`wechatAppKey`、`wechatAppSecret` 一律按字符串处理
- 开关字段统一转为 `true` / `false`
- `apiVersion` 统一转为整数

若校验失败：

- 列出全部问题
- 不修改用户项目
- 让用户修正 Excel 后重新回复“填好了”

### 步骤 3：完成依赖与配置修改

确认后再执行以下修改。

#### 3-1 依赖安装

官方文档给出的安装命令是：

```bash
ohpm install @zztsdk/zztcore
ohpm install @zztsdk/sharesdk
```

如果用户希望你代执行，应先说明将运行上述命令；如果项目已有依赖，则以实际工程为准，不重复破坏性修改。

#### 3-2 `module.json5` 修改

必须优先在 `entry` 模块的 `module.json5` 中处理。

官方文档明确要求：

- 增加 `requestPermissions`
- 至少包含 `ohos.permission.INTERNET`

本 skill 的默认策略是：基础集成阶段仅主动声明 `ohos.permission.INTERNET`，不把其它权限预置到 `module.json5` 中。

#### 3-3 华为 `client_id` 配置

仅当用户启用华为授权时，在 `module.json5` 的 `metadata` 中增加：

```json5
{
  "name": "client_id",
  "value": "用户填写的Client ID"
}
```

如工程已存在 `metadata`，应在原结构中合并，而不是覆盖。

#### 3-4 平台 `querySchemes` 配置

如果启用了对应平台能力，在 `entry` 模块 `module.json5` 的 `module.querySchemes` 中按需增量合并：

- 启用微博：增加 `sinaweibo`
- 启用微信：增加 `weixin`

示例：

```json5
{
  "module": {
    "querySchemes": [
      "sinaweibo",
      "weixin"
    ]
  }
}
```

不要覆盖工程中原有的 `querySchemes`。

### 步骤 4：插入初始化与隐私授权代码

#### 4-1 初始化

在使用 SDK 功能前，需先调用：

```ts
ZztSDK.init(context, "您的AppKey", "您的AppSecret")
```

优先把初始化放在应用启动路径或用户功能入口前的稳定位置。

如果工程入口无法快速确认，先扫描以下位置：

- `entry/src/main/ets/entryability/EntryAbility.ets`
- `entry/src/main/ets/app.ets`
- 其他 `UIAbility` / `AppAbility` / 启动页文件

如果仍无法判断，向用户展示候选位置并让其确认。

#### 4-2 说明合规原因

向用户说明：

```text
根据 MobTech 隐私合规要求，使用 ShareSDK 需要在用户同意隐私政策后才能回传授权结果。

你需要在 App 中：
1. 首次启动时展示《隐私政策》弹窗
2. 用户点击“同意”按钮后，调用隐私授权代码
3. 用户点击“不同意”则不应调用

请告知我：用户点击隐私政策“同意”按钮的回调代码在哪个文件、哪个方法中？
例如：EntryAbility.ets 的 onPrivacyAgreed() 方法，或具体位置如 entry/src/main/ets/entryability/EntryAbility.ets:80
```

#### 4-3 询问回调位置

等待用户告知具体的文件路径和方法名。

#### 4-4 隐私授权回传

文档要求：只有在用户同意隐私政策后，才能调用：

```ts
ZztSDK.submitPolicyGrantResult(isGranted)
```

要求：

- 在用户点击隐私弹窗“同意”后调用
- 在用户拒绝前，不得调用
- 基础集成阶段默认不插入 `ZztCustomController` 代码
- 如果后续用户要控制扩展业务功能，再通过项目内说明文档引导其使用 `ZztCustomController` 或 `ZztSDK.updateZztCustomController(...)`

#### 4-5 展示并确认插入代码

展示要插入的代码：

```ts
// 用户同意隐私政策后调用
ZztSDK.submitPolicyGrantResult(true)
```

完整示例：

```ts
onPrivacyAgreed() {
  // 用户点击同意按钮

  // === ShareSDK 隐私授权 ===
  ZztSDK.submitPolicyGrantResult(true)
  // ========================

  // 其他业务逻辑...
}
```

询问：

```text
以上代码将插入到 {文件} 的 {方法} 中，是否确认？
```

### 步骤 5：插入分享与授权示例

#### 5-1 收集分享与授权落点

主动询问用户：

```text
现在来配置分享和授权功能，请告诉我：

1. 希望在哪个位置执行分享？
   - 例如：ArticlePage.ets 的分享按钮点击事件
   - 或：SharePage.ets 的 onShareClick() 方法

2. 如需华为授权，希望在哪个位置执行授权？
   - 例如：LoginPage.ets 的 onHuaweiLoginClick() 方法

3. 如启用了微博授权或分享，希望在哪个位置执行微博能力？
   - 例如：LoginPage.ets 的 onWeiboLoginClick() 方法
   - 例如：SharePage.ets 的 onShareToWeibo() 方法

4. 如启用了微信授权或分享，希望在哪个位置执行微信能力？
   - 例如：LoginPage.ets 的 onWechatLoginClick() 方法
   - 例如：SharePage.ets 的 onShareToWechat() 方法

5. 分享内容是什么？
   - 文本内容：
   - 标题（如有）：
   - 链接 URL（如有）：
   - 图片（如有）：

6. 分享方式：
   - A. 使用系统分享能力
   - B. 使用指定平台能力（微博 / 微信 / 微信朋友圈）
```

#### 5-2 设置 `UIAbilityContext`

在使用分享/授权 UI 前，先设置：

```ts
await mobShare.ShareSDK.getInstance().setUIAbilityContext(getContext() as common.UIAbilityContext)
```

#### 5-3 分享示例

可按官方示例插入基础分享流程：

- 构造 `mobShare.SharedParam[]`
- 获取平台实例 `mobShare.Platform.SYSTEM`
- 设置 `PlatformActionListener`
- 调用 `share(...)`

#### 5-4 华为授权示例

可按官方示例插入：

- `getPlatformAsync(mobShare.Platform.HUAWEI)`
- `setPlatformActionListener(...)`
- `authorize(params)`
- `showUser()`
- `isAuthValid()`
- `removeAccount()`

注意：`authorize(params)` 的 `params` 字段结构官方文档未明确，不能自行编造。若需要落业务代码，先在本地依赖类型或官方 API 文档中确认。

#### 5-5 微博平台能力

如果启用了微博授权/分享，必须补充以下平台初始化：

- 在使用前调用 `setPlatformDevInfoAsync(mobShare.Platform.SinaWeibo, map)`
- `map` 至少包含：
  - `mobShare.Platform_Info.APP_KEY`
  - `mobShare.Platform_Info.REDIRECT_URL`
  - `mobShare.Platform_Info.CALLBACK_ABILITY_NAME`
- 如项目需要，可额外传入 `Scope`

示例：

```ts
let map = new HashMap<string, Object>()
map.set(mobShare.Platform_Info.APP_KEY, "weibo_app_key")
map.set(mobShare.Platform_Info.REDIRECT_URL, "weibo_redirect_url")
map.set(mobShare.Platform_Info.CALLBACK_ABILITY_NAME, "EntryAbility")
let isSuccess = await mobShare.ShareSDK.getInstance().setPlatformDevInfoAsync(mobShare.Platform.SinaWeibo, map)
```

微博授权示例：

```ts
let plat = await mobShare.ShareSDK.getInstance().getPlatformAsync(mobShare.Platform.SinaWeibo)
plat.setPlatformActionListener(receive)
plat.authorize()
```

微博取用户信息示例：

```ts
let plat = await mobShare.ShareSDK.getInstance().getPlatformAsync(mobShare.Platform.SinaWeibo)
plat.setPlatformActionListener(receive)
plat.showUser()
```

微博分享示例能力范围：

- 文本分享
- 图片分享

图片分享时，官方文档明确说明目前只能分享沙盒路径图片。

#### 5-6 微信平台能力

如果启用了微信授权/分享，必须补充以下平台初始化：

- 在使用前调用 `setPlatformDevInfoAsync(mobShare.Platform.Wechat, map)`
- `map` 至少包含：
  - `mobShare.Platform_Info.APP_KEY`
  - `mobShare.Platform_Info.APP_SECRET`

示例：

```ts
let map = new HashMap<string, Object>()
map.set(mobShare.Platform_Info.APP_KEY, "wechat_app_key")
map.set(mobShare.Platform_Info.APP_SECRET, "wechat_app_secret")
let isSuccess = await mobShare.ShareSDK.getInstance().setPlatformDevInfoAsync(mobShare.Platform.Wechat, map)
```

微信授权示例：

```ts
let plat = await mobShare.ShareSDK.getInstance().getPlatformAsync(mobShare.Platform.Wechat)
plat.setPlatformActionListener(receive)
plat.authorize()
```

微信取用户信息示例：

```ts
let plat = await mobShare.ShareSDK.getInstance().getPlatformAsync(mobShare.Platform.Wechat)
plat.setPlatformActionListener(receive)
plat.showUser()
```

微信分享示例能力范围：

- 微信好友：文本、图片、网页、文件、视频、小程序分享、打开小程序
- 微信朋友圈：文本、图片

微信朋友圈分享时，按官方示例在分享参数中设置 `scene: 1`。

#### 5-7 第三方回调处理

如果启用了微博或微信授权/分享，需要在回呼 Ability 的 `onCreate` 和 `onNewWant` 中调用：

```ts
mobShare.ShareSDK.getInstance().handlerWant(want, this.context)
```

插入前必须先确认用户指定的回呼 Ability 文件与方法位置。

#### 5-8 展示并确认插入代码

在生成分享或授权代码后，必须先向用户展示将插入的代码和目标位置，再询问：

```text
以上是生成的 ShareSDK 代码，将插入到 {文件} 的 {方法} 中，是否确认？
```

### 步骤 6：补充项目内说明文档

完成集成后，在用户项目中生成一份 `SHARESDK_HARMONYOS_README.md`，至少包含：

- 已安装依赖
- 修改过的 `module.json5` 配置
- `appKey` / `appSecret` 来源
- 是否启用华为授权及 `client_id` 来源
- 隐私弹窗回调位置
- 基础集成阶段默认添加的权限清单（仅 `ohos.permission.INTERNET`）
- 已配置的平台能力：
  - 华为授权
  - 新浪微博授权/分享（如启用）
  - 微信授权/分享（如启用）
- 分享与授权能力入口位置
- `querySchemes` 配置结果
- 第三方平台 `setPlatformDevInfoAsync(...)` 配置结果
- 回呼 Ability 中 `handlerWant(...)` 插入位置
- ShareSDK 扩展业务功能设置说明：
  - `ZztCustomController` 的用途
  - 哪些能力可在后期关闭或改为 App 回传
  - `ZztSDK.submitPolicyGrantResult(true, controller)` 的使用场景
  - `ZztSDK.updateZztCustomController(...)` 的补充用法
- 仍待确认的文档未明确项

## 代码修改规则

- 所有修改前必须先展示 diff 计划或代码片段并等待确认
- 不要覆盖用户已有 `requestPermissions`、`metadata`、初始化逻辑或隐私弹窗逻辑
- 对已有权限和 `metadata` 做增量合并
- 若工程已存在 MobTech 相关依赖或旧版 ShareSDK 代码，先停下来说明冲突点，再让用户决定是否替换
- 若发现导入语句、类型声明或 API 名称与官方页面示例不一致，以本地实际依赖导出为准，并向用户说明
- 不要在基础集成阶段主动插入 `ZztCustomController` 控制逻辑，除非用户明确要求

## 隐私与合规要求

- 用户首次冷启动并同意隐私政策后，才可回传授权结果
- 未同意前，不得调用 ShareSDK 业务能力
- App 应向终端用户披露 ShareSDK：
  - SDK 名称：ShareSDK
  - 第三方主体：上海掌之淘信息技术有限公司
  - 使用目的：提供社会化登录和分享服务
  - 隐私政策链接：https://policy.zztfly.com/sdk/share/privacy
- 如果后续启用了扩展业务功能控制，应为用户提供退出能力

## 后续调整说明

如果用户在集成完成后要求严格控制可选信息采集，再建议实现 `ZztCustomController`，并根据官方文档控制以下能力：

- 地理位置信息
- OAID
- WiFi 信息
- 本地 IP 信息
- 运营商信息
- 社交平台信息
- 厂商 / 设备 / 系统 / 屏幕信息

基础集成默认先完成最小必需权限接入；扩展能力、附加权限和数据采集控制放到后续调整阶段处理。
