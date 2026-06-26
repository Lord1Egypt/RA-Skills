---
name: harmonyos-flyverify-integretion
description: Interactive guide for integrating MobTech FlyVerify (秒验/妙验) into HarmonyOS NEXT projects. Use when the user wants one-click verification or one-click login in a HarmonyOS app and needs help with ohpm dependencies, build-profile.json5, module.json5 permissions, privacy timing, preVerify/verify calls, auth page theme customization, or return-code troubleshooting.
tags:
  - harmonyos
  - harmonyos-next
  - flyverify
  - secverify
  - mobtech
  - one-click-login
  - one-click-verify
  - privacy
  - arkts
---

# HarmonyOS FlyVerify 集成 Skill

## 适用场景

当用户提到以下任一主题时，使用本 skill：

- HarmonyOS FlyVerify 集成
- 鸿蒙接入秒验
- 鸿蒙一键登录
- 鸿蒙一键验证
- FlyVerify HarmonyOS NEXT
- MobTech 秒验/妙验 鸿蒙接入
- 秒验隐私合规
- 秒验预取号或取号失败排查
- 秒验授权页 UI 定制

如果用户的问题明确涉及 HarmonyOS NEXT 工程、`ohpm` 依赖、`build-profile.json5`、`module.json5`、MobTech `appKey` / `appSecret`、`ZztSDK.init(...)`、`ZztSDK.submitPolicyGrantResult(...)`、`FlyVerify.preVerify(...)`、`FlyVerify.verify(...)`、`ThemeConfig` 或错误码排查，应优先使用本 skill。

## 参考文档:
- [集成指南](https://www.mob.com/wiki/detailed?wiki=717&id=78)
- [秒验鸿蒙端合规指南](https://www.mob.com/wiki/detailed?wiki=754&id=78)

## 已确认的官方信息

- 开发工具：DevEco Studio
- 集成方式：在线集成
- HarmonyOS API 支持：`>= 12`
- 安装命令：
  - `ohpm install @zztsdk/zztcore`
  - `ohpm install @zztsdk/flyverify`
- 项目级 `build-profile.json5` 需要：
  - `compatibleSdkVersion: "5.0.0(12)"`
  - `buildOption.strictMode.useNormalizedOHMUrl: true`
- `entry` 模块 `module.json5` 需要的权限：
  - `ohos.permission.INTERNET`
  - `ohos.permission.GET_NETWORK_INFO`
- 使用 SDK 前必须先初始化：
  - `ZztSDK.init(context, "您的AppKey", "您的AppSecret")`
- 隐私授权必须在用户同意隐私政策后回传：
  - `ZztSDK.submitPolicyGrantResult(true)`
  - 或 `ZztSDK.submitPolicyGrantResult(true, controller)`
- 页面 `context` 获取方式：
  - 在 `@Component` 页面中通过 `getContext(this)` 获取
  - 文档明确提示：不要在 `UIAbility` 中使用 `this.context` 作为 `init` / `verify` 的 UI 上下文，否则可能影响主题设置
- 预取号 API：
  - `FlyVerify.preVerify(callback)`
  - `FlyVerify.preVerifySync()`
- 取号 API：
  - `FlyVerify.verify(uiContext, callback)`
  - `FlyVerify.verifySync(uiContext)`
- 预取号超时设置：
  - `FlyVerify.setPreVerifyTimeout(timeout)`
  - 建议值 `3000-5000` 毫秒
- 授权页 UI 定制入口：
  - `FlyVerify.setTheme(theme)`
  - `ThemeConfig`
- 文档明确支持的授权页能力：
  - 状态栏配置
  - 自定义组件
  - 手机号码样式与位置
  - 登录按钮文本、颜色、图片、宽高
  - 勾选框
  - 隐私协议文本和页面
  - 弹窗模式
  - 全屏模式适配
  - 关闭授权页
  - 授权页返回键监听事件

## 需要谨慎处理的文档歧义

扩展业务文档里存在命名不一致：

- 集成指南使用 `ZztSDK` / `ZztCustomController`
- 扩展业务文档使用 `MobSDK` / `MobCustomController`

执行规则：

- 基础集成默认以 `集成指南` 和 `SDK API` 中的 `ZztSDK` / `FlyVerify` 为准
- 若要接入扩展业务控制器，必须先检查实际依赖导出的类型声明和工程可编译性，再决定是使用 `ZztCustomController` 还是 `MobCustomController`
- 不要直接照抄扩展业务文档中的类名落工程，必须二次核验

## 6 步交互式集成工作流

所有写文件和改文件操作前，都必须先展示计划修改内容并等待用户确认。

## 交互约束

为了避免在 OpenClaw 中一次性追问太多问题，执行本 skill 时必须遵守以下规则：

- 一次只问一个阻塞问题
- 如果当前问题不解决，后续步骤无法安全推进，就不要同时再问第二个问题
- 能从工程中自动推断的配置，先扫描再推断，不直接问用户
- `bundleName` 优先从工程配置读取；只有在读取失败、存在多个候选值或发现冲突时才询问用户
- 是否代执行 `ohpm install` 只在以下条件都满足后再问：
  - `appKey` / `appSecret` 已齐
  - 工程结构已确认
- 如果发现某一步无需修改，直接说明“无需修改”，然后进入下一步，只问下一步唯一的阻塞问题

推荐输出顺序：

1. 当前步骤结果
2. 哪些项已自动确认
3. 下一步唯一需要开发者回答的问题

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
2. 生成 `assets/FlyVerify_HarmonyOS_Config_Template.xlsx`
3. 复制到用户项目根目录并命名为 `FlyVerify_HarmonyOS_Config.xlsx`

#### 2-2 告知用户填写内容

明确要求用户填写：

- MobTech `appKey`
- MobTech `appSecret`
- 是否需要预取号
- 是否需要一键验证
- 是否需要一键登录
- 是否需要授权页 UI 自定义

等待用户回复“填好了”后再继续。

#### 2-3 校验规则

读取 `FlyVerify_HarmonyOS_Config.xlsx` 后，至少校验：

- `appKey`：必填，不能为空
- `appSecret`：必填，不能为空
- `needPreVerify`：必须可转换为 `true` / `false`
- `needVerify`：必须可转换为 `true` / `false`
- `needOneClickLogin`：必须可转换为 `true` / `false`
- `needCustomTheme`：必须可转换为 `true` / `false`
- `preVerifyTimeoutMs`：如填写，必须是整数，建议 `3000-5000`

类型转换规则：

- `appKey`、`appSecret` 一律按字符串处理
- 布尔字段统一转为 `true` / `false`
- `preVerifyTimeoutMs` 统一转为整数

若校验失败：

- 列出全部问题
- 不修改用户项目
- 让用户修正 Excel 后重新回复“填好了”

#### 2-4 `appKey` / `appSecret` 硬性规则

如果 `appKey` 或 `appSecret` 缺失，流程必须在这里直接停止，并明确告知用户：

```text
当前缺少 MobTech 的 appKey 或 appSecret，按本 skill 规则不继续执行后续工程修改、联调或验收。

请先前往 Mob 开发者后台申请并获取应用配置：
https://new.dashboard.mob.com/#/summary

拿到 appKey 和 appSecret 后再继续。
```

停止规则：

- 不安装依赖
- 不修改 `build-profile.json5`
- 不修改 `module.json5`
- 不插入初始化、隐私授权、预取号、取号或 UI 定制代码
- 可以保留模板填写结果和待改清单，但不得继续落地

### 步骤 3：完成依赖与工程配置修改

确认后再执行以下修改。

#### 3-1 依赖安装

官方安装命令：

```bash
ohpm install @zztsdk/zztcore
ohpm install @zztsdk/flyverify
```

如果用户希望你代执行，应先展示完整命令并说明会修改依赖文件。

#### 3-2 `build-profile.json5` 修改

在项目级 `build-profile.json5` 中确认或补齐：

```json5
{
  "app": {
    "products": [
      {
        "compatibleSdkVersion": "5.0.0(12)",
        "buildOption": {
          "strictMode": {
            "useNormalizedOHMUrl": true
          }
        }
      }
    ]
  }
}
```

执行规则：

- 只增量修改目标 `product`
- 不覆盖现有其它 `buildOption`
- 若工程已有更高兼容版本，优先保留更高版本并仅补齐 `useNormalizedOHMUrl`

#### 3-3 `module.json5` 修改

必须优先在 `entry` 模块的 `module.json5` 中处理。

文档明确要求增加：

```json5
"requestPermissions": [
  { "name": "ohos.permission.INTERNET" },
  { "name": "ohos.permission.GET_NETWORK_INFO" }
]
```

执行规则：

- 采用增量合并，不覆盖已有 `requestPermissions`
- 不重复写入相同权限

### 步骤 4：插入初始化与隐私授权代码

#### 4-1 初始化落点

初始化代码：

```ts
ZztSDK.init(context, "您的AppKey", "您的AppSecret")
```

执行规则：

- `context` 优先来自 `@Component` 页面中的 `getContext(this)`
- 不在 `UIAbility` 中直接使用 `this.context` 作为页面 UI 上下文去做 `verify` 或主题配置
- 初始化务必早于 `submitPolicyGrantResult(...)`、`preVerify(...)`、`verify(...)`

如果工程入口无法快速确认，先扫描以下位置：

- `entry/src/main/ets/pages/*.ets`
- `entry/src/main/ets/entryability/EntryAbility.ets`
- `entry/src/main/ets/app.ets`

#### 4-2 隐私回调位置

**向用户说明**：
```
根据 MobTech 隐私合规要求和中国区 App 上架规范，使用 FlyVerify 需要在用户同意隐私政策后才能初始化 SDK。

你需要在 App 中：
1. 首次启动时展示《隐私政策》弹窗
2. 用户点击"同意"按钮后，调用隐私授权代码
3. 用户点击"不同意"则不应调用

请告知我：用户点击隐私政策"同意"按钮的回调代码在哪个文件、哪个方法中？
例如：LoginPage.ets 的 onPrivacyAgreed() 方法或者具体位置如:com/kit/app/LoginPage.ets:80
```


#### 4-3 隐私授权代码

通用方案：

```ts
ZztSDK.submitPolicyGrantResult(true)
```

带主动控制器方案：

```ts
ZztSDK.submitPolicyGrantResult(true, controller)
```

执行规则：

- 只能在用户点击“同意”后调用
- 用户拒绝前不得调用
- 如果用户后续要求扩展业务控制器，再结合实际依赖核验 `ZztCustomController`

### 步骤 5：插入预取号、取号与 UI 定制代码

#### 5-1 收集业务落点

不要一次性把所有问题都抛给用户。按下面顺序逐个确认：

1. 先确认隐私同意回调位置
2. 再确认初始化落点
3. 再确认预取号落点
4. 再确认取号/一键登录落点
5. 如果 `needCustomTheme=true`，最后才确认 UI 定制细节

主动询问用户时，每次只问当前一个问题。例如：

```text
下一步需要确认预取号落点。
请告诉我：`FlyVerify.preVerify(...)` 想放在哪个页面、哪个方法中？
例如：`LoginPage.ets` 的 `aboutToAppear()`
```

#### 5-2 预取号

异步方式：

```ts
let callback: OperationCallback<void> = {
  onSuccess: () => {},
  onFailure: (e) => {}
};
FlyVerify.preVerify(callback);
```

同步方式：

```ts
FlyVerify.preVerifySync().then(() => {
}).catch((e: VerifyException) => {
});
```

规则：

- 文档明确要求：如果后续要 `verify`，应先调用 `preVerify`
- 推荐在登录页展示前、页面 `aboutToAppear()` 或用户点击登录前的预热阶段调用

#### 5-3 预取号超时

```ts
FlyVerify.setPreVerifyTimeout(timeout);
```

建议值：`3000-5000`

#### 5-4 取号

异步方式：

```ts
let callback: OperationCallback<VerifyResult> = {
  onSuccess: (data) => {
    // data.operator 运营商名称: CUCC / CTCC / CMCC
    // data.opToken  token
    // data.token    运营商 token
  },
  onFailure: (error) => {}
};
FlyVerify.verify(uiContext, callback);
```

同步方式：

```ts
FlyVerify.verifySync(uiContext).then((data) => {
}).catch((e: VerifyResult) => {
});
```

执行规则：

- `uiContext` 必须来自组件页面可用的上下文
- 成功回调后要立刻把 `opToken` / `token` 交给业务服务端校验
- 不把运营商 token 当成最终登录态直接落本地

#### 5-5 授权页 UI 定制

入口：

```ts
let theme = new ThemeConfig().setNumberSize(18).setLogBtnText('本机号码一键登录');
FlyVerify.setTheme(theme);
```

可按需配置：

- 状态栏：`setSystemBarProperties(...)`
- 自定义组件：`setLoginPageComponent(...)`
- 手机号码字号、偏移、颜色、对齐规则
- 登录按钮文本、字号、颜色、背景色、背景图、宽高

所有 UI 定制代码都应先展示给用户确认再写入。

### 步骤 6：返回码排查与项目文档

完成集成后，在用户项目中生成一份 `FLYVERIFY_HARMONYOS_README.md`，至少包含：

- 官方文档地址：
  - `https://www.mob.com/wiki/detailed?wiki=717&id=78`
  - `https://www.mob.com/wiki/detailed?wiki=754&id=78`
- 已安装依赖
- `build-profile.json5` 修改结果
- `module.json5` 权限修改结果
- 初始化代码插入位置
- 隐私授权回调位置
- 预取号 / 取号落点
- 是否启用授权页 UI 定制
- 服务端校验对接说明
- 常见错误码与排查建议

至少收录以下错误码：

- `6119108`：运营商配置为空
- `6119121`：功能关闭
- `6119000`：未知运营商
- `6119127` / `6119128` / `6119129`：移动/联通/电信预取号失败
- `6119123`：预取号代码抛异常
- `6119124`：预取号超时
- `6119170`：运营商无配置
- `6119167` / `6119168` / `6119169`：移动/联通/电信取号失败
- `6119165`：取号代码抛异常
- `6119164`：取号超时
- `6119171`：取号前未调预取号
- `6119172`：调用过于频繁

## 默认输出风格

执行这个 skill 时，优先输出：

1. 已确认的文档事实
2. 待修改文件清单
3. 拟插入的代码片段
4. 风险和注意事项
5. 若涉及扩展业务控制器，明确说明当前使用的类名依据
