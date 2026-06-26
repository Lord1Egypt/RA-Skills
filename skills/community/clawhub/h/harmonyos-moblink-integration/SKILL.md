---
name: harmonyos-moblink-integration
description: Interactive guide for integrating MobTech MobLink into HarmonyOS NEXT projects with 6-step workflow. Use when user says "MobLink集成", "Link集成", "鸿蒙深度链接", "场景还原", "一键集成 MobLink", or asks about MobLink ohpm configuration, HarmonyOS URI scheme, AbilityStage restore listener, ZztSDK init, getMobID, scene restore, privacy compliance, or ZztCustomController setup.
tags:
  - harmonyos
  - moblink
  - mobtech
  - deep-link
  - scene-restore
  - ohpm
  - privacy
  - interactive-integration
---

# HarmonyOS MobLink 集成 Skill

## 适用场景

当用户提到以下任一主题时，使用本 skill：

- harmonyos moblink
- MobLink 集成（鸿蒙 / HarmonyOS / 鸿蒙 NEXT）
- 鸿蒙深度链接 / Deeplink
- MobTech MobLink 鸿蒙接入
- 场景还原
- MobLink 的 ohpm 配置
- HarmonyOS URI scheme / host 配置
- ZztSDK.init / ZztSDK.submitPolicyGrantResult
- getMobID / setRestoreSceneListener / Scene
- MobLink 隐私合规
- ZztCustomController 扩展业务功能控制
- **我要在鸿蒙app中增加深度链接能力**
- **我要在HarmonyOS项目中接入MobLink**
- **帮我配置鸿蒙场景还原**
- **一键集成 MobLink**
- **自动配置 MobLink**

如果用户问题明确与 HarmonyOS 的 MobLink 接入、工程配置、场景还原、隐私合规有关，应优先使用本 skill。

## 官方文档依据

使用以下官方文档作为事实来源：

- 文档入口：https://www.mob.com/wiki/detailed?wiki=661&id=34
- HarmonyOS NEXT 集成指南：https://mob.com/wiki/detailed?wiki=731&id=34
- MobLink 后台基本配置：https://mob.com/wiki/detailed?wiki=527&id=34
- MobLink 鸿蒙端合规使用说明：https://mob.com/wiki/detailed?wiki=758&id=34
- 常见问题：https://mob.com/wiki/detailed?wiki=530&id=34
- MobLink 隐私政策：https://mob.com/wiki/detailed?wiki=97&id=34
- 扩展业务功能设置：https://www.mob.com/wiki/detailed?wiki=730&id=34

关键事实：

- 官方 HarmonyOS 集成方式：ohpm 在线安装 `@zztsdk/zztcore` 和 `@zztsdk/moblink`。
- 最低 API version：`12`（首批接口从 OpenHarmony SDK API version 12 开始支持）。
- ohpm 安装命令：`ohpm install @zztsdk/zztcore` 和 `ohpm install @zztsdk/moblink`。
- 导入方式：`import { ZztSDK } from '@zztsdk/zztcore';` 和 `import mobLink from '@zztsdk/moblink';`。
- ZztSDK 初始化：`ZztSDK.init(context, "您的AppKey", "您的AppSecret")`。
- 隐私提交：`ZztSDK.submitPolicyGrantResult(granted)` 或 `ZztSDK.submitPolicyGrantResult(true, new MyCustomController())`。
- MobLink 初始化：`mobLink.init(context)`，需在 ZztSDK 初始化和隐私提交之后调用。
- 场景还原监听器：建议在 AbilityStage 中设置 `mobLink.setRestoreSceneListener(receiver)`。
- onNewWant 处理：在 Ability 的 `onNewWant` 中调用 `mobLink.updateNewWant(want)`。
- 鸿蒙端需配置 `module.json5` 中的 `skills` 标签以支持 URI scheme 唤醒。

## 6 步交互式集成工作流

每步操作前都需要展示内容给用户确认，获得明确同意后再执行。

### 步骤 1：启动流程

#### 1-1 询问项目路径

```
我来帮你集成 MobLink 场景还原功能。

请提供需要集成的 HarmonyOS 项目根路径，例如：
/path/to/your-harmonyos-project

请确保项目包含 build-profile.json5、oh-package.json5 和 module.json5 文件。
```

#### 1-2 验证路径合法性

验证逻辑：

1. 检查路径是否存在。
2. 检查路径下是否有 `build-profile.json5` 或 `app.json5`。
3. 检查是否存在 `oh-package.json5`。
4. 检查是否存在 `module.json5`（或 `entry/src/main/module.json5`）。

如果路径不合法：

```
路径验证失败，可能原因：
- 路径不存在：{path}
- 未找到 build-profile.json5 / app.json5
- 未找到 oh-package.json5
- 未找到 module.json5

请重新提供正确的 HarmonyOS 项目根路径。
```

如果路径合法：进入步骤 2。

### 步骤 2：注册 MobLink 配置信息

#### 2-1 生成配置模板文件

**操作**：
1. 执行 `assets/generate_excel_template.py`，生成 `assets/MobLink_Config_Template.xlsx`
2. 将生成的 `assets/MobLink_Config_Template.xlsx` 复制到 `{path}` 下
3. 在 `{path}` 下命名为 `MobLink_Config.xlsx`

**告知用户**：

```
已在你项目的根目录生成 {path}/MobLink_Config.xlsx 配置文件。

请打开该文件，按以下步骤填写：
1. 在"基础信息"Sheet 中填写 MobTech 的 appKey、appSecret 和鸿蒙包名
2. 在"MobLink配置"Sheet 中填写 uriScheme、host 和默认场景路径
3. 在"隐私合规"Sheet 中确认隐私政策、授权回调和扩展采集控制配置
4. "填写说明"Sheet 中有官方文档链接和字段说明

填写完成后告诉我"填好了"，我将继续下一步。
```

#### 2-2 等待用户填写完成

等待用户回复"填好了""已填写"或类似表达。

#### 2-3 读取并验证配置

**操作**：读取 `{path}/MobLink_Config.xlsx`。

验证规则：

| 检查项                | 规则                       | 不通过时的提示                                  |
| ------------------ | ------------------------ | ---------------------------------------- |
| appKey             | 必填，不能为空字符串               | "基础信息 Sheet 中的 appKey 未填写，请从 MobTech 官网获取" |
| appSecret          | 必填，不能为空字符串               | "基础信息 Sheet 中的 appSecret 未填写"            |
| bundleName         | 必填，建议符合 `com.xxx.xxx` 格式 | "鸿蒙包名格式不正确，应类似 com.example.app"          |
| uriScheme          | 建议填写，来自 MobLink 后台配置     | "MobLink uriScheme 未填写，可能影响 scheme 唤醒"   |
| host               | 建议填写，来自 MobLink 后台配置     | "MobLink host 未填写，可能影响 AppLink 唤醒"       |
| defaultScenePath   | 如填写，建议以 `/` 开头           | "场景路径建议以 / 开头，例如 /demo/a"                |
| privacyPolicyReady | 转为布尔值                    | "隐私合规配置请填写 是/否 或 true/false"             |
| 隐私合规布尔项            | 转为布尔值                    | "隐私合规配置请填写 是/否 或 true/false"             |

类型转换规则：

- `appKey`、`appSecret`、`bundleName`、`uriScheme`、`host`、`defaultScenePath`、`restoreAbility` 等标识符字段强制转为字符串。
- `privacyPolicyReady`、`useZztCustomController`、`allowLocationData`、`allowDeviceIdData`、`allowAppListData`、`allowNetworkData` 转为 `true` / `false`。

如果不合法：

```
配置信息验证失败，请修正以下问题：

{具体问题列表}

请修改 Excel 文件后保存，然后重新告诉我"填好了"。
```

如果合法：提取配置信息，进入步骤 3。

### 步骤 3：完成 SDK 集成

#### 3-1 ohpm 安装依赖

**操作**：在项目根目录执行以下命令：

```bash
ohpm install @zztsdk/zztcore
ohpm install @zztsdk/moblink
```

验证 `oh-package.json5` 中是否已添加依赖：

```json5
"dependencies": {
  "@zztsdk/zztcore": "^x.x.x",
  "@zztsdk/moblink": "^x.x.x"
}
```

**注意**：需要访问https://ohpm.openharmony.cn/ohpm 获取最新依赖包的版本。

#### 3-2 权限配置

在 `module.json5` 中添加权限：

**必需权限**：

```json5
"reqPermissions": [
  {
    "name": "ohos.permission.INTERNET"
  }
]
```

**建议权限**：

```json5
{
  "name": "ohos.permission.APP_TRACKING_CONSENT"
},
{
  "name": "ohos.permission.GET_NETWORK_INFO"
}
```

**注意：**

APP_TRACKING_CONSENT 是 user_grant 权限，需要补 `reason` 和 `usedScene`。

示例：
```
{
  "name": "ohos.permission.APP_TRACKING_CONSENT",
  "reason": "用于为您提供个性化的内容推荐服务",
  "usedScene": {
    "abilities": ["EntryAbility"],
    "when": "inuse"
  }
}
```

#### 3-3 URI scheme 配置

在 `module.json5` 的对应 Ability 的 `skills` 中添加 skill 对象：

```json5
"skills": [
  {
    "entities": ["entity.system.home"],
    "actions": ["action.system.home"]
  },
  {
    "actions": ["your.custom.action"],
    "uris": [
      {
        "scheme": "{uriScheme}",
        "host": "{host}"
      }
    ]
  }
]
```

> 如果存在多个跳转场景，需配置多个 skill 对象。actions 不能为空，否则会造成目标方匹配失败。

### 步骤 4：插入隐私授权回调

#### 4-1 说明合规原因

```
根据 MobTech 合规要求，MobLink 需要在用户同意隐私政策后才能提交授权结果并使用 SDK 功能。

ZztSDK.init() 内部会做隐私授权状态的判断，在应用向 ZztSDK 提交隐私授权同意状态之前不会做任何业务的初始化。

请告知用户点击隐私政策"同意"按钮的回调代码在哪个文件、哪个方法中？
例如：EntryAbility.ts 的 onPrivacyAgreed() 方法，或具体位置如 entry/src/main/ets/ability/EntryAbility.ts:80
```

#### 4-2 展示并确认插入代码

普通方案：

```typescript
import { ZztSDK } from '@zztsdk/zztcore';

// 用户同意隐私政策后调用
ZztSDK.submitPolicyGrantResult(true);
```

如果用户启用 `ZztCustomController`，展示：

```typescript
import { ZztSDK, ZztCustomController } from '@zztsdk/zztcore';

export class MyCustomController extends ZztCustomController {
  // TODO 重写控制器方法
}

ZztSDK.submitPolicyGrantResult(true, new MyCustomController());
```

用户确认后再执行插入。

### 步骤 5：插入场景还原与制链代码

#### 5-1 收集业务信息

询问用户：

```
现在配置 MobLink 场景还原，请告诉我：

1. 需要在哪个 Ability 承接还原后的场景？（例如 EntryAbility 或其他 Ability）
2. 场景路径是什么？例如 /demo/a
3. 需要携带哪些业务参数？例如 testKey、testValue
4. 是否需要生成 mobID 并拼接到分享链接？
5. 是否已有 AbilityStage 类？如果有，请提供路径。
```

#### 5-2 设置全局场景还原监听器

官方建议在 AbilityStage 中设置。

监听器示例：

```typescript
import mobLink from '@zztsdk/moblink';

let receiver: mobLink.RestoreSceneListener = {
  completeRestore: (scene: mobLink.Scene) => {
    // 在"拉起"处理场景的 ability 之后调用
    // 处理跳转
    if (scene) {
      console.log("scene path:" + scene.path);
      let action = scene.path;
      if (action == "xxx") {
        // 逻辑处理
      }
    }
  },
  notFoundScene: (scene: mobLink.Scene) => {
    // 未找到处理 scene 的 ability 时回调
  }
};

mobLink.setRestoreSceneListener(receiver);
```

#### 5-3 修改 Ability 处理 onNewWant

在承接场景还原的 Ability 中添加：

```typescript
import mobLink from '@zztsdk/moblink';

export default class EntryAbility extends UIAbility {
  onNewWant(want: Want, launchParam: AbilityConstant.LaunchParam): void {
    console.log("EntryAbility onNewWant");
    mobLink.updateNewWant(want);
  }
}
```

#### 5-4 获取场景还原内容

在 Ability 的 `onCreate` 或 `onNewWant` 中获取：

```typescript
import mobLink from '@zztsdk/moblink';

mobLink.getSceneFromWant(want).then((scene) => {
  if (scene) {
    console.log("scene path:" + scene.path);
    // 逻辑处理
  } else {
    console.log("scene undefined");
  }
});
```

#### 5-5 生成 mobID 示例

```typescript
import mobLink from '@zztsdk/moblink';

let scene = new mobLink.Scene();
scene.path = "{defaultScenePath}";
scene.params.set("testKey", "testValue");

let receiver: mobLink.MobIDListener = {
  onResult: (mobid: string) => {
    console.log("mobId:" + mobid);
    // 根据 mobID 拼接分享链接
  },
  onError: (e: Error) => {
    console.log("onError:" + e.message);
  }
};

mobLink.getMobID(scene, receiver);
```

所有代码修改前先展示完整 diff 计划，用户确认后再写入。

### 步骤 6：生成集成说明

**操作**：在 `{path}` 下生成 `MOBLINK_README.md`。

内容应包含：

- 已修改文件列表。
- ohpm 依赖安装信息。
- `uriScheme` 和 `host` 来源。
- 权限配置位置。
- 隐私授权回调位置。
- 场景还原监听器位置（AbilityStage）。
- 承接 Ability 和 `onNewWant` 处理位置。
- `getMobID` 使用方式。
- 常见问题和官方文档链接。

生成前展示内容，用户确认后写入。
