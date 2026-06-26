# HarmonyOS MobLink 集成 Skill

用于协助 Agent 在 HarmonyOS NEXT 项目中集成 MobTech MobLink，覆盖 ohpm 依赖安装、ZztSDK 初始化、隐私合规、场景还原监听和 mobID 生成代码。

## 能做什么

- 生成 `MobLink_Config_Template.xlsx` 配置模板。
- 引导用户填写 appKey、appSecret、包名、uriScheme、host、隐私合规等配置。
- 根据配置安装 ohpm 依赖、配置权限和 URI scheme。
- 插入 ZztSDK 初始化、隐私授权回调、场景还原监听和 mobID 生成代码。
- 生成项目内 `MOBLINK_README.md` 集成说明。

## 使用前准备

- 在 MobTech 后台创建好应用，获取 appKey 和 appSecret。
- 在 MobLink 后台完成 scheme、AppLink Host 等配置。
- 目标 HarmonyOS 项目路径。
- 已确认的隐私政策展示和用户授权流程。
- 承接场景还原的 Ability。
- AbilityStage 类（用于设置全局场景还原监听器）。

## 运行流程

1. 提供项目根路径，Agent 验证项目结构。
2. 生成并填写 `MobLink_Config.xlsx` 配置模板。
3. Agent 安装 ohpm 依赖、配置权限和 URI scheme。
4. 插入 ZztSDK 初始化和隐私授权回调代码。
5. 插入场景还原监听器和 mobID 生成代码。
6. 生成项目内集成说明文档。

## 需要用户准备的信息

- HarmonyOS 项目根路径
- MobTech 后台获取的 `appKey` 和 `appSecret`
- 鸿蒙应用包名（bundleName）
- MobLink 后台配置的 `uriScheme`
- MobLink 后台开启 AppLink 后生成的 `host`
- 承接场景还原的 Ability
- 隐私政策同意按钮的回调位置
- AbilityStage 类路径（用于全局场景还原监听器）

## 生成文件

集成流程会先执行：

```bash
python3 assets/generate_excel_template.py
```

生成：

```text
assets/MobLink_Config_Template.xlsx
```

然后复制到用户 HarmonyOS 项目根目录并命名为：

```text
MobLink_Config.xlsx
```

用户填写完成后，Agent 读取该 Excel 并继续后续集成。

## 官方文档

- 文档入口：https://www.mob.com/wiki/detailed?wiki=661&id=34
- HarmonyOS NEXT 集成指南：https://mob.com/wiki/detailed?wiki=731&id=34
- MobLink 后台基本配置：https://mob.com/wiki/detailed?wiki=527&id=34
- MobLink 鸿蒙端合规使用说明：https://mob.com/wiki/detailed?wiki=758&id=34
- 常见问题：https://mob.com/wiki/detailed?wiki=530&id=34
- MobLink 隐私政策：https://mob.com/wiki/detailed?wiki=97&id=34
- 扩展业务功能设置：https://www.mob.com/wiki/detailed?wiki=730&id=34

## 注意事项

- Agent 修改项目文件前会先展示修改计划并等待确认。
- 如果官方文档没有明确说明某个字段或版本要求，skill 会要求用户确认，不会猜测。
- MobLink SDK 首批接口从 OpenHarmony SDK API version 12 开始支持。
- ZztSDK.init() 内部会做隐私授权判断，提交隐私授权前不会初始化业务。
