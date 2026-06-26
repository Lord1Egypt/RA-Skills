# harmonyos-mobpush-integration

一个面向 OpenClaw / ClawHub 的 HarmonyOS NEXT MobPush 集成 Skill，采用 6 步交互式工作流程。

## 用途

当用户提到以下主题时触发：

- "我要在鸿蒙app中增加推送能力"
- "帮我集成 MobPush 到鸿蒙项目"
- "帮我配置鸿蒙推送通知"
- harmonyos mobpush
- 鸿蒙 MobPush 集成
- MobPush 推送 SDK 接入（鸿蒙端）
- MobPush ohpm 配置
- MobPush 隐私合规（鸿蒙端）
- 华为推送通道配置

## 目录结构

```
harmonyos-mobpush-integration/
├── SKILL.md                              # 核心 Skill 定义（6步交互式工作流程）
├── README.md                             # 本文件
├── assets/
│   ├── MobPush_Config_Template.xlsx      # Excel 配置模板（供用户填写）
│   └── generate_excel_template.py        # 生成 Excel 模板的脚本
└── examples/
    └── example-prompts.md                # 示例触发问法
```

## 6 步交互式集成工作流

本 Skill 采用交互式工作流程，每步操作前都会展示内容给用户确认：

1. **启动流程**：询问并验证鸿蒙项目路径
2. **注册配置信息**：生成 Excel 配置模板，用户填写后读取验证
3. **完成 SDK 集成**：ohpm 依赖安装、build-profile.json5 配置、module.json5 权限与 metadata 配置、项目同步提示
4. **插入隐私授权回调**：询问回调位置，展示代码后插入
5. **SDK API 接入**：推送监听、别名、标签、通知点击回执等功能
6. **补充说明**：生成项目级 README 文档

## 支持功能

- HarmonyOS NEXT (API >= 12) Stage 模型 + ArkTS
- ohpm 依赖管理（@zztsdk/zztcore + @zztsdk/mobpush）
- MobTech MobPush appKey / appSecret 配置
- 华为推送通道（Huawei Push Kit）
- 首次冷启动隐私授权回传（ZztSDK.submitPolicyGrantResult）
- 推送消息接收处理
- 别名与标签管理

## 建议放置位置

将此目录放入 OpenClaw workspace 的 `skills/` 目录中。

## 参考资料

- [Mob 文档中心](https://www.mob.com/wiki/list)
- [鸿蒙集成指南](https://www.mob.com/wiki/detailed?wiki=697&id=136)
- [SDK API 参考](https://www.mob.com/wiki/detailed?wiki=698&id=136)
- [后台配置指南](https://www.mob.com/wiki/detailed?wiki=560&id=136)
- [鸿蒙端合规说明](https://www.mob.com/wiki/detailed?wiki=745&id=136)
