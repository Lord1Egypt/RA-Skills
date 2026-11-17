---
name: linkfox-expert-aigc-videogen-sale
description: 带货口播视频Skill，把商品图、商品卖点、销售地区、受众、语言和时长组装成跨境电商带货口播MP4，覆盖商品口播、TikTok带货视频、达人种草视频、product talking video、sale video、e-commerce talking head video。用户说"带货口播"、"商品口播"、"帮我做一个产品带货视频"、"生成TikTok口播广告"、"make a product talking video"时触发。即使用户只说"用这些商品图做一个能卖货的视频"、"做跨境短视频素材"或"seller video with speaking model"，也应触发本Skill；普通图转视频、视频剪辑、带货数据分析不在本Skill范围。
---

# 带货口播

## 适用场景

把商品图和商品卖点转成带人设、口播、分镜和促单结构的商品视频。这个 Skill 只负责商品理解、三套口播方案、用户选择和最终视频 prompt 组装；实际视频生成必须委托通用底层能力 `linkfox-aigc-videogen` / `linkfox-aigc-videogen-multi`，不得在本 Skill 重复实现工具网关调用。

| 场景 | 说明 |
|------|------|
| 商品口播视频 | 用户提供商品图和卖点，希望生成真人自拍风格的口播短视频。 |
| 跨境带货素材 | 用户指定销售国家/地区、语言和受众，希望模特人设、背景和口播本土化。 |
| TikTok/短视频广告 | 用户希望生成有视觉钩子、痛点展示、促单话术的商品短视频。 |
| 多图商品输入 | 用户提供多张商品图，先做商品信息分析，再生成口播方案。 |

## 不适用

- 普通图转视频、首尾帧视频、多参考图视频：使用 `linkfox-aigc-videogen-image-to-video`。
- 视频剪辑、拼接、字幕包装、后期转场：需要单独的视频剪辑 Skill。
- TikTok 达人数据、带货销量、榜单分析：这是数据查询能力，不是口播视频生成。
- 数字人直播、长视频脚本、完整广告片项目管理：需要独立 Skill。

## 全局规则

### 方案选择强制约束（最高优先级）

1. **默认必须两阶段执行**：先生成 3 套口播方案并展示给用户选择，再根据用户选择生成视频；不得把方案生成和视频生成合并成一步。
2. **步骤 3 必须停止等待**：输出 3 套候选方案后，必须停止并等待用户回复方案 1/2/3，严禁自动调用底层视频生成能力。
3. **展示给用户的是可读方案，内部必须保留完整结构**：用户只需要选择编号；Agent/调用方必须在上下文中保留完整 `schemes` JSON，用户选择后用 `schemes + selectedSchemeNumber` 或选中的 `selectedScheme` 继续。
4. **禁止静态文本冒充方案**：不得只回填一段“方案一/方案二”文本作为 `selectedScheme`；`selectedScheme` 必须是结构化对象。
5. **直接 prompt 仅作显式跳过**：只有当调用方确认 `prompt` 已经是最终成片提示词，并传入 `skipSchemeSelection: true` 时，才允许跳过方案选择。

给用户展示方案时，必须给出 3 个编号，并以类似以下方式收尾：

```text
请选择要生成视频的方案：回复 1、2 或 3。选择后我会按该方案生成带货口播视频。
```

### 两阶段交互契约

| 阶段 | 触发条件 | 必须做什么 | 严禁做什么 |
|------|----------|------------|------------|
| 方案阶段 | 用户提供商品图、卖点、地区、语言等初始信息 | 生成 `schemes`，向用户展示方案 1/2/3，并在上下文保留完整 `schemes` 对象 | 调用底层视频生成能力直接生成视频 |
| 生成阶段 | 用户回复 1/2/3 或明确选择某个方案 | 用原始 `schemes` + `selectedSchemeNumber`，或选中的 `selectedScheme` 对象调用脚本生成视频 | 把用户看到的静态方案文案当成 `selectedScheme`，或在未传 `skipSchemeSelection: true` 时只传 `prompt` |

如果调用方不是对话式系统，无法保留上下文中的 `schemes`，则第二阶段必须直接传完整的 `selectedScheme` 对象；只传 `"方案一"`、`"方案二"` 这类字符串会被脚本拒绝。

## 输入参数

底层视频生成能力见 `linkfox-aigc-videogen` / `linkfox-aigc-videogen-multi`。本 Skill 的口播业务参数见下表，口播方案生成提示词见 `references/prompt.md`。

| 参数 | 类型 | 必填 | 默认 | 说明 |
|------|------|------|------|------|
| imageList | array[string] | 条件必填 | - | 商品图/实拍图列表。未传时可用 `imageUrl`；每项必须是 http(s) 可访问 URL。 |
| imageUrl | string | 条件必填 | - | 单张商品图，脚本会归一成 `imageList[0]`；必须是 http(s) 可访问 URL。 |
| customer_keywords | string | 是 | - | 用户卖点、痛点、商品信息补充，驱动脚本重点。正常两阶段流程必须作为顶层结构化字段传入，不得只揉进 `prompt`。 |
| language | string | 否 | 英语 | `talk` 字段的口播语言；未传时默认英语。 |
| salesRegion | string | 否 | 美国 | 销售国家/地区，最高优先级，决定人种、肤色、环境；未传时默认美国。 |
| targetAudience | string | 是 | - | 目标受众，决定年龄层、穿衣风格和精神面貌。正常两阶段流程必须作为顶层结构化字段传入；不明确时调用方也应传“泛人群”等明确值。 |
| videoDuration | integer | 是 | - | 期望视频时长。正常两阶段流程必须作为顶层结构化字段传入。 |
| videoType | string | 否 | SEED | 参考图模式模型：`SEED` / `SEED_FAST` / `WAN` / `HAPPY_HORSE`。脚本可接受 `seedance2.0`、`seedance2.0fast`、`wan2.6`、`happyhorse` 等别名。 |
| aspectRatio | string | 否 | 按模型默认 | 视频输出比例，沿用图转视频参考图模式：SEED 支持 `16:9`/`9:16`/`adaptive`，SEED_FAST 支持 `16:9`/`9:16`，WAN 不支持比例字段，HAPPY_HORSE 支持 `16:9`/`9:16`；不传或传 `default` / `默认` / `按模型` 表示使用模型默认，不等于自适应。明确自适应必须传 `adaptive` 或 `自适应`。 |
| resolution | string | 否 | 按模型 | 生成分辨率，沿用图转视频参考图模式：SEED 支持 `480p`/`720p`/`1080p`，SEED_FAST 支持 `480p`/`720p`，HAPPY_HORSE 支持 `720p`/`1080p`，WAN 透传。 |
| schemes | array[object] | 条件必填 | - | 3 套候选口播方案数组。与 `selectedSchemeIndex` / `selectedSchemeNumber` 配合使用；如果已直接传 `selectedScheme` 或最终 `prompt`，可不传。 |
| selectedSchemeIndex | integer | 条件必填 | - | 从 `schemes` 选择方案的 0 基下标：0/1/2。 |
| selectedSchemeNumber | integer | 条件必填 | - | 从 `schemes` 选择方案的 1 基序号：1/2/3。与 `selectedSchemeIndex` 二选一。 |
| selectedScheme | object | 条件必填 | - | 用户选中的 3 套方案之一，必须是结构化对象，包含 `plan`、`language_instruction`、`visual_anchors.person_anchor`、`visual_anchors.product_anchor`、`shots[].visual`、`shots[].talk`、`shots[].prompt`。只有调用方传 `skipSchemeSelection: true` 且已直接给最终 `prompt` 时，才可跳过选择步骤。 |
| prompt | string | 条件必填 | - | 最终视频生成提示词。默认不能单独用于生成；只有传 `skipSchemeSelection: true` 明确跳过方案选择时才接受。 |
| skipSchemeSelection | boolean | 否 | false | 是否显式跳过 3 套方案选择。默认 `false`；仅当调用方已确认 `prompt` 是最终成片提示词时可设为 `true`。 |
| hiddenPrompt | string | 否 | - | 内部强化提示词，和 `prompt` 合并提交。 |
| voice | boolean | 否 | true | 带货口播模型默认提交 `voice=true`。调用方传入的 `voice=false` 不会关闭口播声音。 |

### 结构化字段约束

正常两阶段口播流程必须传 `customer_keywords`、`targetAudience`、`videoDuration` 这 3 个顶层字段。`language` 和 `salesRegion` 保留默认值，未传时分别按英语、美国处理。脚本会拒绝“只把必填业务信息写进 prompt”的调用，错误信息为 `Missing required structured parameter: ...`。只有 `skipSchemeSelection: true` 且 `prompt` 已经是最终确认提示词时，才允许绕过这组结构化字段校验。

## 模型路由

底层能力和图片字段由 `videoType` 决定，两者绑定，不可拆开：

| videoType | 底层能力 | 图片字段 | 图片数量 |
|-----------|----------|----------|----------|
| `SEED` / `SEED_FAST` / `HAPPY_HORSE` | `linkfox-aigc-videogen-multi` | `imageList` | 最多 9 张 |
| `WAN` | `linkfox-aigc-videogen` | `imageUrl` | 仅 1 张 |

图片字段固定规则：

- 走 `linkfox-aigc-videogen-multi` 时提交 `imageList`。
- 走 `linkfox-aigc-videogen` 时只提交单张 `imageUrl`，不提交 `imageList`，也不提交 `ignoredImageCount`。
- 选择 wan2.6 时，如果上游给了多张图，必须先让用户保留 1 张主商品图，不得自行截取。

## 模型参数

| 模型 | API 枚举 | 底层能力 | 时长 | 分辨率 | 比例 | 声音 | 图片数量 |
|------|----------|-----|------|--------|------|------|----------|
| seedance2.0 | `SEED` | `linkfox-aigc-videogen-multi` | 5/10/15 秒 | 480p/720p/1080p | 16:9/9:16/adaptive | 默认 true | 最多 9 张 |
| seedance2.0fast | `SEED_FAST` | `linkfox-aigc-videogen-multi` | 5/10/15 秒 | 480p/720p | 16:9/9:16 | 默认 true | 最多 9 张 |
| HappyHorse | `HAPPY_HORSE` | `linkfox-aigc-videogen-multi` | 5/10/15 秒 | 720p/1080p | 16:9/9:16 | 默认 true | 最多 9 张 |
| wan2.6 | `WAN` | `linkfox-aigc-videogen` | 5/10/15 秒 | 透传 | 不支持 | 默认 true | 仅 1 张 |

### 比例默认值与自适应

- `aspectRatio` 不传，或传 `default` / `默认` / `按模型`：使用脚本内置模型默认比例；当前默认是 SEED、SEED_FAST 和 HAPPY_HORSE 为 `9:16`。WAN 不支持比例字段，不应传 `aspectRatio`。
- `aspectRatio` 传 `adaptive` / `自适应` / `auto` / `adapt`：明确请求自适应，只在该模型支持 `adaptive` 时通过校验。
- `aspectRatio` 传 `16:9` / `9:16`：表示用户明确选择该比例，Skill 不会自动改成 `adaptive`。

## 流水线步骤

### 步骤 1：整理输入图片

- **输入**：`imageList` / `imageUrl`。
- **操作**：确认至少有一张商品图，且图片已经是可访问 URL；单张图归一为 `imageList[0]`。不执行图片上传、比例校验、裁切、拼图或补边。
- **输出**：规范化后的图片列表和主图。
- **用途**：被步骤 2 的商品信息分析和步骤 5 的视频接口调用复用。

### 步骤 2：自动生成商品信息

- **输入**：步骤 1 的商品图片，以及用户补充的 `customer_keywords`。
- **操作**：使用 `linkfox-aigc-textgen` 的图文理解能力，结合 `references/prompt.md` 的“第一步：自动生成商品信息”提示词，生成 `product_name`、`target_audience`、`selling_points_description`、`craftsmanship_details`、`usage_method`、`category_path`。
- **输出**：商品信息 JSON。
- **用途**：补全卖点少、用户描述不足时的口播方案输入。

### 步骤 3：生成 3 套带货口播方案

- **输入**：步骤 2 商品信息、`language`、`salesRegion`、`targetAudience`、`videoDuration`、`customer_keywords`。
- **操作**：读取 `references/prompt.md` 的“第二步：带货口播”提示词，生成严格 JSON，包含 `schemes[0..2]`、`visual_anchors`、`plot`、`environment_setup`、`bgm`、`shots[]`、`negative_prompt`。
- **输出**：3 个候选方案，并向用户展示方案 1/2/3。
- **用途**：回填给用户/调用方并等待选择。此步骤完成后必须停止，不得继续生成视频。

### 步骤 4：选择方案并合成最终视频提示词

- **输入**：用户选择后的某一个 `selectedScheme`，或 `schemes` + `selectedSchemeIndex` / `selectedSchemeNumber`。只有 `skipSchemeSelection: true` 时，才允许用户直接提供最终 `prompt`。
- **操作**：先校验选中方案是结构化对象，再把剧情、环境、BGM、分镜 prompt、口播稿、负向提示词合成为最终视频提示词；保留人种锁定、手机前置自拍、口型活跃、真实皮肤纹理、产品锚点一致性等约束。
- **输出**：最终 `prompt` 和 `hiddenPrompt`。
- **用途**：提交给步骤 5 的底层视频生成能力。

### 步骤 5：委托底层能力生成视频

- **输入**：步骤 1 图片列表、步骤 4 最终提示词、模型参数。
- **操作**：按模型调用底层 skill（唯一调用方式，禁止改用脚本、HTTP 或其它视频 skill）：
  - seedance2.0、seedance2.0fast、HappyHorse 调用 `linkfox-aigc-videogen-multi`，传 `imageList`。
  - wan2.6 调用 `linkfox-aigc-videogen`，传单张 `imageUrl`，不得传 `imageList`。
  - `videoType`：`SEED` / `SEED_FAST` / `WAN` / `HAPPY_HORSE`
  - `videoTime`：步骤 4 归一后的时长
  - `prompt`：步骤 4 合成的最终视频提示词，可叠加 `hiddenPrompt`
  - `promptOptimizer`、`aspectRatio`、`isPro`、`voice:true`、`camera`、`resolution`
  - **skill 输出原封不动透传**：底层 `linkfox-aigc-videogen` / `linkfox-aigc-videogen-multi` 自行完成网关调用、响应落盘和视频下载，本 Skill 不做二次包装、不截取、不重新输出。
- **输出**：底层 skill stdout；成功通常包含 `Saved full response: ["...mp4"]`，失败可能包含 `Saved full response: xxx.json` 或错误说明。
- **用途**：业务层不接触工具网关鉴权、HTTP 请求、响应落盘和视频下载细节。

### 步骤 6：返回交付 JSON

- **输入**：步骤 5 的底层 skill stdout。
- **操作**：成功时收集 `Saved full response:` 后的本地媒体路径；失败时读取底层能力落盘 JSON 中的 `errcode` / `errmsg` / `error` / `status` / `errorMsg` 并做用户可读说明。若响应出现 `status=FAILED`，视为当前任务终态，不自动重试、不换模型、不重建任务；其中 `errorMsg` 为“图片审核不通过”或其它审核、侵权、人脸、明星/名人肖像相关失败时，立即停止；不得重新生成方案、重新上传同一素材、换模型、换底层 skill、改 prompt 或继续调用工具绕过。
- **输出**：`media_paths`。
- **用途**：Agent 收尾时只展示本地 MP4 路径。

## 调用示例

两阶段完整 JSON、三种合法写法、WAN 单图差异、会被拒绝的反例：见 [`references/call-examples.md`](references/call-examples.md)。接入或排查传参问题时读。

## 输出规则

- 只向用户展示 `media_paths` 中的本地视频路径。
- 不要读取或输出视频文件正文/base64。
- 不要把原始 API 返回的临时 URL 直接给用户。
- 图片审核不通过是终止型业务失败；只提示用户更换有授权、无明星/名人肖像或侵权风险的合规图片。

## 常见失败与排查

现象、原因、处理的完整对照表：见 [`references/troubleshooting.md`](references/troubleshooting.md)。先分清是参数契约问题（本 Skill 直接拒绝）还是底层任务失败（已调到底层）。

## 执行自检

每次执行后，Agent 在收尾时确认：

- [ ] 最终生成时按模型调用 `linkfox-aigc-videogen` 或 `linkfox-aigc-videogen-multi`。
- [ ] 成功时 seedance2.0、seedance2.0fast、HappyHorse 使用 `imageList`；wan2.6 使用单张 `imageUrl`。
- [ ] 成功时 `voice` 为 `true`；带货口播模型默认都开声音。
- [ ] 成功时优先展示底层 skill 返回的本地视频路径；若为空，说明底层能力未返回本地视频路径，并提示用户查看底层 skill 的落盘 JSON。
- [ ] 图片审核不通过时立即停止，并返回用户可读的合规换图提示；服务器繁忙等 `FAILED` 也不重试、不绕路。
- [ ] 生成方案时 `schemes` 正好 3 个，`shots` 为数组，`language_instruction` 写成“整个视频使用[language]来进行口播”。
- [ ] 正常两阶段流程必须收到结构化 `customer_keywords`、`targetAudience`、`videoDuration`；`language` / `salesRegion` 未传时使用默认英语/美国，不得只从 `prompt` 里猜必填业务字段。
- [ ] 展示 3 套方案后必须停止等待用户选择，严禁自动进入视频生成。
- [ ] 最终生成时如果使用方案选择，传 `selectedScheme` 对象，或传 `schemes` + `selectedSchemeIndex` / `selectedSchemeNumber`；不要只传静态方案文本。
- [ ] 每个 shot 的 `prompt` 保留人种关键词、产品锚点、清晰开口、手机自拍、手持呼吸感。
- [ ] 错误时按底层 skill 返回的业务原因说明，不展示 Python traceback。
- [ ] 没有读取或输出视频文件正文/base64。

## 配套文件

| 文件 | 内容 | 何时读 |
|------|------|--------|
| `references/prompt.md` | 第一步商品信息生成提示词、第二步带货口播方案生成提示词 | 执行流水线步骤 2、步骤 3 前必读 |
| `references/call-examples.md` | 两阶段完整调用 JSON、三种合法写法、拒绝反例 | 接入或排查传参问题时读 |
| `references/troubleshooting.md` | 常见失败现象 → 原因 → 处理对照表 | 生成失败时读 |
| `references/api.md` | 业务参数边界、下游参数映射、判定与输出约定、已知局限 | 确认调用底层能力的传参时读 |
| `examples/test-cases.md` | 正常用例、错误用例、覆盖点 | 自测时读 |
