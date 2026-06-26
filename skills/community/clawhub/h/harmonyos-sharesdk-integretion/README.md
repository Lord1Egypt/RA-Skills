# harmonyos-sharesdk-integretion

用于协助 Agent 在 HarmonyOS NEXT 项目中集成 MobTech ShareSDK。

## 能做什么

- 识别并校验 HarmonyOS 项目结构
- 生成 `ShareSDK_HarmonyOS_Config_Template.xlsx`
- 引导填写 `appKey`、`appSecret`、`client_id`
- 引导填写微博、微信平台所需参数
- 按官方文档修改 `module.json5` 权限和 `metadata`
- 按需增量合并 `querySchemes`
- 插入 `ZztSDK.init(...)`、`submitPolicyGrantResult(...)`、分享和授权示例
- 插入微博/微信 `setPlatformDevInfoAsync(...)` 与 `handlerWant(...)` 示例
- 在集成完成后的文档中补充 `ZztCustomController` 和扩展业务功能的后续调整方式

## 官方依据

- 集成指南：https://www.mob.com/wiki/detailed?wiki=696&id=14
- 扩展业务功能设置：https://www.mob.com/wiki/detailed?wiki=711&id=14
- 鸿蒙端合规使用说明：https://www.mob.com/wiki/detailed?wiki=748&id=14
- 新浪微博授权与分享：https://www.mob.com/wiki/detailed?wiki=722&id=14
- 微信授权与分享：https://www.mob.com/wiki/detailed?wiki=724&id=14

## 目录结构

```text
harmonyos-sharesdk-integretion/
├── SKILL.md
├── README.md
├── examples/
│   └── example-prompts.md
└── assets/
    └── generate_excel_template.py
```

## 适用范围

- HarmonyOS NEXT
- DevEco Studio
- 在线 `ohpm` 集成
- ShareSDK 基础分享
- 华为授权
- 新浪微博授权与分享
- 微信授权与分享
- 隐私授权回传
- 扩展业务功能后续调整说明

## 已知官方要求

- HarmonyOS API 支持：`>= 12`
- 安装命令：
  - `ohpm install @zztsdk/zztcore`
  - `ohpm install @zztsdk/sharesdk`
- 基础集成默认仅声明必需权限：`ohos.permission.INTERNET`
- 其余权限不主动写入 `module.json5`，如后续需要扩展业务能力，再按项目实际需求补充
- 启用微博时，需在 `module.json5` 的 `querySchemes` 中增加 `sinaweibo`
- 启用微信时，需在 `module.json5` 的 `querySchemes` 中增加 `weixin`

## 文档未明确项

以下事项需要以实际工程或已安装依赖为准：

- ArkTS 导入语句
- `authorize(params)` 参数结构
- 是否必须修改 `oh-package.json5`、`build-profile.json5`、`app.json5`
- 推荐的初始化文件路径和业务落点

## 建议使用方式

让 Agent 按交互流程执行：

1. 提供 HarmonyOS 项目路径
2. 生成并填写 Excel 配置模板
3. 让 Agent 读取模板并校验
4. 通过对话询问隐私回调位置、分享落点和授权落点
5. 让 Agent 生成项目内 README，并在文档中说明后续如何调整 ShareSDK 扩展业务功能
