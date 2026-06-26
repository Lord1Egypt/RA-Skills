---
name: harmonyos-mobpush-integration
description: Interactive guide for integrating MobTech MobPush into HarmonyOS NEXT projects with 6-step workflow. Use when user says "我要在鸿蒙app中增加推送能力", "MobPush集成", "鸿蒙推送功能", "配置推送通知", or asks about MobPush setup, ohpm configuration, Huawei push channel, push message handling, alias/tags management, or privacy compliance. Supports step-by-step interactive integration with user confirmation at each step.
tags:
  - harmonyos
  - mobpush
  - mobtech
  - push-notification
  - ohpm
  - privacy
  - interactive-integration
  - huawei-push
---

# HarmonyOS MobPush 集成 Skill

## 适用场景

当用户提到以下任一主题时，使用本 skill：

- 鸿蒙 MobPush 集成
- 鸿蒙推送通知配置
- MobPush 推送 SDK 接入（鸿蒙）
- MobPush appKey / appSecret 配置
- MobPush 隐私合规（鸿蒙端）
- 华为推送通道配置（鸿蒙）
- 推送消息接收与处理（鸿蒙）
- 别名/标签/角标设置（鸿蒙）
- **我要在鸿蒙app中增加推送能力**
- **我要在鸿蒙项目中接入推送功能**
- **帮我配置鸿蒙推送通知**
- **一键集成 MobPush（鸿蒙）**
- **自动配置 MobPush（鸿蒙）**

---

## 6 步交互式集成工作流

当用户表达集成 MobPush 的意图时，执行以下 6 步交互式流程。每步操作前都需要展示内容给用户确认，获得明确同意后再执行。

---

### 步骤 1：启动流程

#### 1-1 询问项目路径

**主动询问用户**：

```
我来帮你集成 MobPush 推送功能到鸿蒙项目。

请提供需要集成的鸿蒙项目根路径，例如：
/Users/xxx/your-harmonyos-project

请确保项目是有效的鸿蒙项目（包含 build-profile.json5 或 oh-package.json5 文件）。
```

#### 1-2 验证路径合法性

**验证逻辑**：
1. 检查路径是否存在
2. 检查路径下是否有 `build-profile.json5` 或 `oh-package.json5`
3. 检查是否为有效的鸿蒙 Stage 模型项目结构

**如果不合法**：

```
路径验证失败：
- 路径不存在或未找到 build-profile.json5 / oh-package.json5 文件
- 请确认这是鸿蒙项目根目录

请重新提供正确的项目路径。
```

**如果合法**：进入步骤 2

---

### 步骤 2：注册 MobPush 配置信息

#### 2-1 生成配置模板文件

**操作**：
1. 执行 `assets/generate_excel_template.py`，生成 `assets/MobPush_Config_Template.xlsx`
2. 将生成的模板复制到 鸿蒙项目根目录下，命名为 `MobPush_Config.xlsx`

**告知用户**：

```
已在你项目的根目录生成 {path}/MobPush_Config.xlsx 配置文件。

请打开文件填写：
1. "基础信息"：appKey、appSecret、鸿蒙包名
   （appKey/appSecret 从 https://www.mob.com/ 注册应用获取）
2. "华为推送"：如需使用华为推送通道，填写 Client ID
   （从 AppGallery Connect 获取，不需要可填写"否"）
3. "隐私合规" 和 "填写说明" 有详细指引

填写完成后告诉我"填好了"。
```

#### 2-2 等待用户填写 → 读取并验证

**验证规则**：

| 检查项       | 规则       | 不通过时的提示                       |
| --------- | -------- | ----------------------------- |
| appKey    | 必填       | "基础信息 Sheet 中的 appKey 未填写"    |
| appSecret | 必填       | "基础信息 Sheet 中的 appSecret 未填写" |
| 包名        | 必填，反域名格式 | "包名格式不正确"                     |

**类型转换**：appKey、appSecret、包名、Client ID 等标识符字段强制转为字符串。

如果合法，提取配置信息，进入步骤 3。

---

### 步骤 3：完成 SDK 集成

#### 3-1 安装 ohpm 依赖

**展示命令**：

```bash
ohpm install @zztsdk/zztcore
ohpm install @zztsdk/mobpush
```

**询问**："以上命令将安装 MobPush 鸿蒙 SDK 依赖，是否确认？"

执行后确认安装成功。如失败则提示用户检查 ohpm 环境，或通过 DevEco Studio 依赖管理面板手动添加。

#### 3-2 工程级 build-profile.json5 配置

**展示修改内容**：

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

**询问**："以上内容将合并到项目级 build-profile.json5，是否确认修改？"

#### 3-3 entry模块 module.json5 权限配置

**展示添加的权限**：

```json5
"requestPermissions": [
  { "name": "ohos.permission.INTERNET" },
  { "name": "ohos.permission.GET_NETWORK_INFO" }
]
```

**说明**：INTERNET 用于网络连接和推送，GET_NETWORK_INFO 用于检测网络状态。

**询问**："以上权限将添加到 entry/src/main/module.json5，是否确认修改？"

#### 3-4 华为 Client ID 配置（可选）

如果用户在 Excel 中启用了华为推送并填写了 Client ID：

```json5
"metadata": [
  {
    "name": "client_id",
    "value": "{用户填写的Client ID}"
  }
]
```

**说明**：如使用华为推送，需在 AppGallery Connect 获取 Client ID 并配置到此。

**询问**："是否在 module.json5 中添加以上华为 Client ID 配置？"

#### 3-5 项目同步提示

```
工程配置文件已修改，请在 DevEco Studio 中执行 Build -> Build Hap(s) 同步项目。
⚠️ 确保 ohpm 依赖已正确安装后再编译。
```

进入步骤 4

---

### 步骤 4：插入初始化与隐私授权代码

#### 5-1 说明合规原因

```
根据 MobTech 隐私合规要求，使用 MobPush 需在用户同意隐私政策后才能初始化。

你需要：
1. 首次启动时展示《隐私政策》弹窗
2. 用户点击"同意"后调用初始化和隐私授权代码
3. 用户不同意则不调用

请告知：SDK 初始化代码应放在哪个文件、哪个方法中？
以及用户点击"同意"的回调位置？
```

#### 5-2 等待用户告知 → 展示确认代码

**初始化代码**：

```typescript
import { ZztSDK } from '@zztsdk/zztcore';
import mobPush from '@zztsdk/mobpush';

ZztSDK.init(getContext(this), "{appKey}", "{appSecret}");
mobPush.init(getContext(this), "{appKey}", "{appSecret}");
```

**隐私授权代码**：

```typescript
// 用户同意隐私政策后调用
ZztSDK.submitPolicyGrantResult(true);
```

**询问**："以上代码将插入到 {用户指定的位置}，是否确认？"

用户确认后执行插入，进入步骤 5。

---

### 步骤 5：SDK API 接入

#### 6-1 推送监听

建议在 AbilityStage 中设置，确保消息不丢失：

```typescript
import mobPush from '@zztsdk/mobpush';

let receiver: mobPush.MobPushReceiver = {
  onCustomMessageReceive: (message: mobPush.MobPushCustomMessage) => {
    // 透传消息：message.getMessageId()、message.getContent()
  },
  onNotifyMessageReceive: (message: mobPush.MobPushNotifyMessage) => {
    // 通知到达：message.getMobNotifyId()、message.getMessageId()、message.getTitle()、message.getContent()
  },
  onNotifyMessageOpenedReceive: (message: mobPush.MobPushNotifyMessage) => {
    // 通知点击（需配合 notificationClickAck）：message.getMobNotifyId()、message.getTitle()、message.getContent()
  },
  onCommandReceive: (type: number, map: HashMap<string, Object>) => {
    // type=1: RID更新  type=2: 厂商deviceToken更新
    let channel = map.get(mobPush.KEY_CHANNEL);  // channel: mobpush/harmony
    let token = map.get(mobPush.KEY_TOKEN);      // 对应channel的更新token
  }
};
mobPush.addPushReceiver(receiver);
// 页面销毁时：mobPush.removePushReceiver(receiver);
```

#### 6-2 通知点击回执上报

必须在 UIAbility 的 `onCreate` 和 `onNewWant` 中调用：

```typescript
export default class EntryAbility extends UIAbility {
  onCreate(want: Want, launchParam: AbilityConstant.LaunchParam): void {
    mobPush.notificationClickAck(want);
  }
  onNewWant(want: Want, launchParam: AbilityConstant.LaunchParam): void {
    mobPush.notificationClickAck(want);
    // 获取推送附加数据: want?.parameters?.["pushData"]
  }
}
```

#### 6-3 别名与标签

```typescript
// 别名
mobPush.setAlias("alias").then((data: mobPush.AliasResult) => console.log(data.errorCode, data.alias));
mobPush.getAlias().then((data: mobPush.AliasResult) => console.log(data.alias, data.errorCode));
mobPush.deleteAlias().then((data: mobPush.AliasResult) => console.log(data.errorCode));

// 标签
mobPush.addTags(["tag"]).then((data: mobPush.TagsResult) => console.log(data.errorCode, data.tags));
mobPush.getTags().then((data: mobPush.TagsResult) => console.log(data.tags, data.errorCode));
mobPush.deleteTags(["tag"]).then((data: mobPush.TagsResult) => console.log(data.errorCode, data.tags));
mobPush.cleanTags().then((data: mobPush.TagsResult) => console.log(data.errorCode, data.tags));
```

#### 6-4 其他 API

完整 API 参考[官方文档](https://www.mob.com/wiki/detailed?wiki=698&id=136)，包括：
- `getRegistrationId(callback)` / `getRegistrationId(): Promise<string>` — 获取注册 ID（Callback/Promise 两种方式）
- `setShowBadge(show: boolean)` — 设置是否显示角标
- `getShowBadgeAsync(): Promise<boolean>` — 获取是否显示角标
- `setBadgeCounts(count: number)` — 设置角标数
- `stopPush()` — 停止推送（仅可通过 restartPush 重新打开）
- `restartPush()` — 重新打开推送服务
- `isPushStoppedAsync(): Promise<boolean>` — 判断推送是否已停止
- `clearAllNotification()` — 清除所有通知
- `getDeviceTokenAsync(): Promise<string>` — 获取厂商 token
- `isNotificationEnabled(callback)` / `isNotificationEnabled(): Promise<boolean>` — 判断通知权限是否开启
- `checkTcpStatus(callback)` / `checkTcpStatus(): Promise<boolean>` — 检测 TCP 连接状态
- `removePushReceiver(receiver)` — 移除推送监听（页面销毁时调用）

进入步骤 6

---

### 步骤 6：补充说明

#### 7-1 生成项目级 README

在用户项目根目录生成 `MOBPUSH_README.md`，包含集成说明、关键文件位置、后续修改指引。

#### 7-2 完成告知

```
MobPush 鸿蒙端集成已完成！

📁 生成的文件：
- {project_path}/MOBPUSH_README.md — 集成说明文档
- {project_path}/MobPush_Config.xlsx — 项目配置文件

📝 关键文件位置：
- SDK 配置：EntryAbility.ets 中的 ZztSDK.init()
- 隐私授权：用户隐私同意回调中的 ZztSDK.submitPolicyGrantResult(true)
- 华为推送：entry/src/main/module.json5 中的 client_id metadata
- 编译配置：项目级 build-profile.json5 中的 buildOption

📖 官方文档：
- 集成指南：https://www.mob.com/wiki/detailed?wiki=697&id=136
- SDK API：https://www.mob.com/wiki/detailed?wiki=698&id=136
- 后台配置：https://www.mob.com/wiki/detailed?wiki=560&id=136
- 合规说明：https://www.mob.com/wiki/detailed?wiki=745&id=136
- 隐私政策：https://policy.zztfly.com/sdk/mobpush/privacy

⚠️ 重要提醒：
1. 包名与 MobTech 后台配置一致
2. 华为推送需在 AppGallery Connect 正确配置
3. 用户同意隐私政策后才能调用 ZztSDK.submitPolicyGrantResult(true)
4. 通知点击回执必须在 UIAbility 的 onCreate 和 onNewWant 中调用
```

---

## 附录：技术参考

### A. 工程配置

#### build-profile.json5
```json5
{
  "app": {
    "products": [{
      "compatibleSdkVersion": "5.0.0(12)",
      "buildOption": { "strictMode": { "useNormalizedOHMUrl": true } }
    }]
  }
}
```

#### module.json5 权限
```json5
"requestPermissions": [
  { "name": "ohos.permission.INTERNET" },
  { "name": "ohos.permission.GET_NETWORK_INFO" }
]
```

#### module.json5 华为推送 metadata
```json5
"metadata": [
  { "name": "client_id", "value": "华为Client ID" }
]
```

#### ohpm 依赖
```bash
ohpm install @zztsdk/zztcore
ohpm install @zztsdk/mobpush
```

### B. 华为推送通道配置

1. 登录 [AppGallery Connect](https://developer.huawei.com/consumer/cn/service/josp/agc/index.html)
2. "我的项目" → 目标应用 → "项目设置 > 常规 > 应用" 获取 **Client ID**
3. 在 entry 的 `module.json5` 中配置 metadata
4. 在 MobTech 后台配置鸿蒙厂商参数

### C. 隐私合规

- 首次冷启动展示隐私政策 → 用户同意 → 调用 `ZztSDK.submitPolicyGrantResult(true)`
- 可选使用 `ZztCustomController` 自定义数据采集控制器
- 隐私政策中需披露：SDK 名称 MobPush、第三方主体"上海掌之淘信息技术有限公司"、链接 https://policy.zztfly.com/sdk/mobpush/privacy
- 完整合规说明：https://www.mob.com/wiki/detailed?wiki=745&id=136

### D. 常见问题

| 问题        | 可能原因                                    |
| --------- | --------------------------------------- |
| 收不到推送     | 包名不一致、appKey/appSecret 错误               |
| 华为推送失败    | Client ID 未配置或错误                        |
| 无点击回调     | 未在 UIAbility 中调用 notificationClickAck() |
| 别名/标签操作失败 | errorCode 非 0，检查 SDK 初始化状态              |
| 通知权限未开启   | 引导用户在系统设置中开启                            |

---

## 回答边界

- 仅聚焦 HarmonyOS NEXT Stage 模型 + ArkTS 的 MobPush 集成与合规
- 不扩展到 Android、iOS、服务端、非 MobTech SDK
- 不伪造真实账号、密钥、签名值
