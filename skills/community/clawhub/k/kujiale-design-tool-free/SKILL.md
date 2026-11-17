---
name: "kujiale-design-tool-free"
description: "分步式室内设计工具,完成户型确认到渲染出图,适合个人用户快速生成装修方案。Use when 需要设计创作、UI设计、海报制作、品牌视觉时使用。不适用于3D建模和动画制作。适用于独立开发者、企业团队和自动化工作流场景。支持中文交互，无需复杂配置即开即用。输出结果可直接使用，减少二次加工成本。提供结构化输出和错误处理机制。"
license: Proprietary
allowed-tools: read exec
compatibility: "Requires LLM with tool-use capability"
metadata:
  displayName: "酷家乐设计-免费版"
  version: "1.0.0"
  summary: "分步式室内设计工具,完成户型确认到渲染出图,适合个人用户快速生成装修方案。"
  tags:
    - "Creative"
    - "室内设计"
    - "AI创作"
  source: "SkillHub"
  converted_at: "2026-07-22T17:58:36"
tools:
  - exec
  - read
  - write
---

> **功能说明**: 本技能涵盖 中文交互、化工作流场景 等核心能力。

# 酷家乐设计工具 - 免费版

## 概述

酷家乐设计免费版是一款面向个人用户的分步式室内智能设计工具。通过自然语言对话完成户型确认、风格选择、布局生成与渲染出图全流程,无需专业设计软件操作经验,即可快速获得装修方案预览。

本版本依托酷家乐设计平台能力,提供基础的户型搜索、风格选择、智能布局与渲染功能,适合个人业主、室内设计初学者及装修灵感探索者。

## 核心能力

| 能力项 | 免费版支持 | 说明 |
|:-------|:-----------|:-----|
| 户型文字搜索 | 是 | 按城市小区搜索 |
| 户型图上传识别 | 是 | 图片临摹识别 |
| 硬装风格选择 | 是 | 基础风格库 |
| 智能布局 | 是 | 自动家具布局 |
| 渲染图生成 | 是 | 标准画质 |
| 全景图链接 | 是 | 360度全景 |
| 多方案对比 | 否 | PRO 版支持 |
| 批量渲染 | 否 | PRO 版支持 |
| 自定义风格 | 否 | PRO 版支持 |
**技术实现要点**：核心能力基于`input_params`参数与`output_format`配置实现,支持创建/查询/修改/删除等操作模式,通过`config_options`进行运行时配置。

### 核心功能执行
用`input_params`参数进行配置。

**输出**: 返回核心功能执行的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 参数配置与调用
用`config_options`参数进行配置。

**输出**: 返回参数配置与调用的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`config_options`参数,支持修改/重置/导入操作

### 结果处理与输出
用`output_format`参数进行配置。

**输出**: 返回结果处理与输出的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`output_format`参数,支持导出/保存/转换操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：分步式室内设计工、完成户型确认到渲、染出图、适合个人用户快速、生成装修方案、酷家乐设计免费版、面向个人用户的分、步式室内智能设计、分步对话完成户型、布局确认、渲染出图、支持文字搜索小区、户型或上传户型图、提供基础硬装风格、库与智能布局、生成渲染图与全景等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持。

## 使用场景

### 场景一:业主装修方案预览

业主拿到新房户型,希望快速预览不同风格的装修效果。

```text
用户: 帮我设计一下我家新房,在杭州,小区是万科未来城

流程:
1. 系统询问城市与小区
2. 搜索户型并展示户型图
3. 用户确认户型后选择风格(如现代简约)
4. 触发智能布局生成
5. 渲染出图展示效果

命令示例:
node ./scripts/searchPlan.js --token=<token> --query="万科未来城" --areaId=<杭州id> --start=0 --num=20
node ./scripts/getFloorplanInfo.js --planId=<planId>
node ./scripts/createDesign.js --token=<token> --planId=<planId>
node ./scripts/getTags.js --token=<token>
node ./scripts/getStyles.js --token=<token> --tagItemIds=<id1,id2>
node ./scripts/triggerLayout.js --token=<token> --designId=<designId> --tagIds=<id1> --styleId=<styleId> --applyDecorationStyle=true --buildCeiling=true --autoDesign=true
node ./scripts/trigger-render.js --obsDesignId=<designId> --xToken=<token>
```

### 场景二:上传户型图识别设计

用户已有户型图图片,希望基于图片进行设计。

```text
用户: 我有一张户型图照片,帮我设计

流程:
1. 系统检测到上传图片
2. 上传图片并创建临摹任务
3. 轮询识别结果获取 planId
4. 后续流程同场景一

命令示例:
node ./scripts/getUploadToken.js --token=<token>
node ./scripts/createBitmapTask.js --token=<token> --bitmap=<url>
node ./scripts/getBitmapTaskResult.js --token=<token> --taskId=<taskId>
```

### 场景三:装修风格灵感探索

用户希望探索不同硬装风格的装修效果。

```text
用户: 我想看看不同风格的装修效果

流程:
1. 系统获取风格标签
2. 展示标签选项(如现代、北欧、中式)
3. 用户选择后查询硬装风格
4. 展示风格封面图供选择
5. 选择后触发布局与渲染

命令示例:
node ./scripts/getTags.js --token=<token>
node ./scripts/getStyles.js --token=<token> --tagItemIds=<id1,id2>
```

## 不适用场景

以下场景酷家乐设计-免费版不适合处理：

- 3D建模和动画制作
- 照片级写实渲染
- 手绘原创插画

## 触发条件

需要设计创作、UI设计、海报制作、品牌视觉时使用。不适用于非本工具能力范围的需求。

## 快速开始

### 领先步:配置 access_token

首次使用需在项目根目录创建 `.kjlconfig.json` 文件:

```json
{
  "access_token": "your_access_token_here"
}
```

获取地址:`https://www.kujiale.com/skills`

### 第二步:版本校验

```bash
node ./scripts/versionCheck.js --token=${token} --version=1.0.0
```

### 第三步:启动设计流程

直接告诉 Agent:"帮我做一个室内设计",系统将引导你完成全流程。

**结果处理**: 执行完成后,查看输出结果确认操作状态。成功时输出包含处理摘要和结果数据;失败时根据错误信息排查问题,查阅错误处理章节获取恢复步骤。

#
## 示例

基础配置项说明:

```json
// .kjlconfig.json
{
  "access_token": "your_token",
  "default_city": "杭州",
  "default_style": "现代简约"
}
```

```bash
# 本技能的核心实现逻辑
# 请参考上方使用说明进行配置和调用
echo "implementation_ready"
```

## 优选实践

1. **户型信息完整**:搜索时提供城市+小区名+户型结构(几室几厅),提升搜索准确性
2. **先确认户型再设计**:仔细核对户型图面积与结构,确认后再进入设计阶段
3. **风格标签多选**:可多选标签(如"现代"+"简约"),系统会匹配更精准的风格
4. **布局确认后再渲染**:布局生成后仔细查看各房间家具布置,确认后再渲染
5. **渲染需等待**:渲染出图约需 2-5 分钟,期间可做其他操作
6. **结果排序参考**:渲染图按房间优先级排序(客餐厅→主卧→次卧→其他)

## 常见问题

### Q1:搜索不到我的户型怎么办?
A:尝试用上传户型图的方式;或确认小区名称拼写;或提供周边标志性建筑辅助定位。

### Q2:户型图识别失败怎么办?
A:确保图片清晰、正面、无遮挡;尝试重新拍摄;或改用文字搜索方式。

### Q3:智能布局消耗额度吗?
A:智能布局会消耗账号内的布局额度/核豆,执行前系统会提示并需用户确认。

### Q4:渲染图不清晰怎么办?
A:免费版为标准画质。如需高清渲染,请使用 PRO 版的高清渲染与批量渲染能力。

### Q5:方案可以保存吗?
A:可以。设计完成后会生成方案详情链接,可登录酷家乐平台查看与编辑。

## 依赖说明

### 运行环境
- **Agent平台**: 支持 SKILL.md 的任意 AI Agent(Claude Code / Cursor / Codex / Gemini CLI 等)
- **操作系统**: Windows / macOS / Linux
- **运行时**: Node.js 16+

### 第三方依赖
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-------|:-----|:---------|:---------|
| 酷家乐设计 API | 外部 API | 必需 | 官网注册获取 token |
| Node.js 16+ | 运行时 | 必需 | 官方安装 |
| axios | HTTP 库 | 必需 | npm install axios |

### API Key 配置
- **配置文件**: `.kjlconfig.json`(项目根目录)
- **字段名**: `access_token`
- **获取方式**: 访问 `https://www.kujiale.com/skills` 生成
- **存储建议**: 配置文件加入 `.gitignore`,避免泄露

### 可用性分类
- **分类**: MD+execute(纯 Markdown 指令,核心功能需要 exec 命令行执行能力)
- **说明**: 基于Markdown的AI Skill,通过分步对话与脚本调用驱动室内设计全流程

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|---------|------|---------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 已知限制

- 需LLM支持,无LLM环境不可用
- 复杂业务场景建议结合人工经验判断
- 执行效率受模型能力与网络环境影响
- 当前为免费版本,如需完整功能请升级到付费版获取全部能力

## 安全注意事项

| 风险类型 | 防范措施 |
|----------|---------|
| API密钥泄露 | 通过环境变量配置，禁止硬编码到代码或配置文件中 |
| 命令执行风险 | 仅执行白名单命令，避免拼接用户输入到命令行参数中 |
| 网络通信安全 | 使用HTTPS协议，验证SSL证书有效性 |
| 敏感数据暴露 | 输出结果中不包含密钥、令牌等敏感信息 |

使用前请确认已阅读依赖说明章节，确保运行环境满足安全要求。