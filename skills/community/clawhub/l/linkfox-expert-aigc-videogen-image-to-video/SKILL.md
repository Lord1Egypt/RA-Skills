---
name: linkfox-expert-aigc-videogen-image-to-video
description: 图转视频Skill，把图片生成短视频，覆盖参考图模式和首尾帧模式。参考图模式支持 seedance2.0、seedance2.0fast、可灵Omni、HappyHorse、海螺2.3、wan2.6；首尾帧模式支持 seedance2.0、seedance2.0fast、可灵2.6。用户说"图转视频"、"图片转视频"、"把这张图动起来"、"参考图生成视频"、"首尾帧视频"、"image to video"、"reference image video"、"first last frame video"时触发；带货口播、数字人讲解、完整广告成片不在本Skill范围。
---

# 图转视频

## 适用场景

把图片素材生成短视频。这个 Skill 只负责视频 agent 内的业务模式识别、参数校验和底层能力路由；实际网关调用、响应处理与媒体转存必须委托通用底层能力 `linkfox-aigc-videogen` / `linkfox-aigc-videogen-multi`，不得在本 Skill 重复实现。

| 业务模式 | 说明 |
|----------|------|
| 参考图模式 | 用户提供一张或多张参考图，希望模型参考主体、风格或构图生成视频。海螺2.3和 wan2.6 只支持 1 张参考图。 |
| 首尾帧模式 | 用户提供首帧 `imageUrl`，可选提供尾帧 `lastFrameImageUrl`，希望控制视频开始和结束画面。 |

## 不适用

- 带货口播、真人自拍口播、达人讲解视频：使用 `linkfox-aigc-videogen-sale`。
- 图片生成或改图：使用对应图片 Skill。
- 文本生成、商品文案、脚本方案：使用文本或编排 Skill。
- 复杂剪辑、字幕、配乐、转场包装：需要单独的视频编排 Skill。

## 输入参数

完整工具网关接口字段、模型支持与响应结构见 `references/api.md`。

| 参数 | 类型 | 必填 | 默认 | 说明 |
|------|------|------|------|------|
| entry | string | 是 | - | 调用入口保护字段。必须严格传 `img2video`；若缺失或为 `productDynamic`、`livestream`、`图转视频` 等其它值，脚本会直接报错，避免误路由到本 Skill。 |
| mode | string | 否 | 自动判断 | `reference` / `first_last_frame`。旧值 `single`、`multi_reference` 兼容为 `reference`。 |
| imageList | array[string] | 参考图模式推荐 | - | 参考图列表；每项必须是 http(s) URL。海螺2.3、wan2.6 只允许 1 张。 |
| imageUrl | string | 首尾帧必填；参考图单图可用 | - | 首帧图或单张参考图；必须是 http(s) URL。 |
| lastFrameImageUrl | string | 否 | - | 尾帧图；首尾帧模式下选填，传入时必须是 http(s) URL。KLING 2.6 只有 `resolution=1080p` 且 `voice=false` 时允许传。 |
| videoType | string | 是 | - | 业务模型名或 API 枚举。脚本会把 `seedance2.0`、`seedance2.0fast`、`可灵Omni`、`可灵2.6`、`happyhorse`、`海螺`、`wan2.6` 等归一成工具网关枚举。 |
| videoTime | integer | 是 | - | 视频时长，需匹配所选模型支持范围。海螺2.3 特例：业务 UI 显示 `5秒` 档，但底层 `HAILUO` API 的合法短时长是 `videoTime=6`；收到 `videoTime=6` 时必须原样透传，不得修正为 5。 |
| prompt | string | 否 | - | 动态效果描述。 |
| promptOptimizer | boolean | 否 | false | 是否开启提示词优化，按平台实际能力透传。 |
| isPro | boolean | 否 | false | Pro/高质量模式，按模型能力生效。 |
| voice | boolean | 否 | 按模式/模型 | 是否生成声音。参考图模式 SEED/SEED_FAST/WAN 可选，默认 `true`；HappyHorse 不提供选择，固定 `true`；可灵Omni、海螺2.3 不提供选择，固定 `false`。首尾帧模式 SEED/SEED_FAST/KLING 可选，默认 `true`。KLING 2.6 只有 `resolution=1080p` 时可选声音，720p 固定 `false`。 |
| aspectRatio | string | 否 | 按模型默认 | 视频比例，按模型支持 `16:9` / `9:16` / `1:1` / `adaptive`；不传或传 `default` / `默认` / `按模型` 表示使用模型默认，不等于自适应。明确自适应必须传 `adaptive` 或 `自适应`。 |
| camera | string | 否 | single | 运镜参数：`single` / `multi`。 |
| resolution | string | 否 | 按模型 | 分辨率，按模型支持 `480p` / `720p` / `768p` / `1080p`。 |

## 模型路由

| 业务模式 | 业务模型 | API 枚举 | 底层能力 |
|----------|----------|----------|-----|
| 参考图模式 | seedance2.0 | `SEED` | `linkfox-aigc-videogen-multi` |
| 参考图模式 | seedance2.0fast | `SEED_FAST` | `linkfox-aigc-videogen-multi` |
| 参考图模式 | 可灵Omni | `KLING` | `linkfox-aigc-videogen-multi` |
| 参考图模式 | HappyHorse | `HAPPY_HORSE` | `linkfox-aigc-videogen-multi` |
| 参考图模式 | 海螺2.3 | `HAILUO` | `linkfox-aigc-videogen` |
| 参考图模式 | wan2.6 | `WAN` | `linkfox-aigc-videogen` |
| 首尾帧模式 | seedance2.0 | `SEED` | `linkfox-aigc-videogen` |
| 首尾帧模式 | seedance2.0fast | `SEED_FAST` | `linkfox-aigc-videogen` |
| 首尾帧模式 | 可灵2.6 | `KLING` | `linkfox-aigc-videogen` |

## 模型参数

| 业务模式 | 业务模型 | 时长 | 分辨率 | 比例 | 声音 | 图片数量 |
|----------|----------|------|--------|------|------|----------|
| 参考图模式 | seedance2.0 | 5/10/15 秒 | 480p/720p/1080p | 16:9/9:16/adaptive | 可选，默认 true | 最多 9 张 |
| 参考图模式 | seedance2.0fast | 5/10/15 秒 | 480p/720p | 16:9/9:16 | 可选，默认 true | 最多 9 张 |
| 参考图模式 | 可灵Omni | 5/10/15 秒 | 720p/1080p | 16:9/9:16/1:1 | 固定 false | 最多 7 张 |
| 参考图模式 | HappyHorse | 5/10/15 秒 | 720p/1080p | 16:9/9:16 | 固定 true | 最多 9 张 |
| 参考图模式 | 海螺2.3 | UI 显示 5/10 秒；底层实际 `videoTime=6/10`；1080p 只能 UI 5 秒档（实际 `videoTime=6`） | 768p/1080p | 透传 | 固定 false | 仅 1 张 |
| 参考图模式 | wan2.6 | 5/10/15 秒 | 透传 | 不支持 | 可选，默认 true | 仅 1 张 |
| 首尾帧模式 | seedance2.0 | 5/10/15 秒 | 480p/720p/1080p | 16:9/9:16/adaptive | 可选，默认 true | 首帧 + 可选尾帧 |
| 首尾帧模式 | seedance2.0fast | 5/10/15 秒 | 480p/720p | 16:9/9:16 | 可选，默认 true | 首帧 + 可选尾帧 |
| 首尾帧模式 | 可灵2.6 | 5/10 秒 | 720p/1080p | adaptive | 1080p 可选且默认 true；720p 固定 false | 首帧 + 可选尾帧；仅 `1080p + voice=false` 可传尾帧 |

### 声音与尾帧规则

- 参考图模式：seedance2.0、seedance2.0fast、wan2.6 允许传 `voice`，不传默认 `true`；HappyHorse 不给用户选择声音，脚本固定提交 `voice=true`；可灵Omni、海螺2.3 不给用户选择声音，脚本固定提交 `voice=false`。
- 首尾帧模式：seedance2.0、seedance2.0fast、可灵2.6 允许传 `voice`，不传默认 `true`。
- 首尾帧模式所有模型的 `lastFrameImageUrl` 都是选填；如果没有尾帧但需要进入首尾帧模式，调用方必须显式传 `mode:"first_last_frame"`。
- 可灵2.6 首尾帧特殊规则：只有 `resolution=1080p` 时可选择声音；`resolution=720p` 固定 `voice=false`。尾帧选填，但只有 `resolution=1080p` 且 `voice=false` 时允许传 `lastFrameImageUrl`。
- 若要在可灵2.6 首尾帧模式下开声音，调用方需显式传 `mode:"first_last_frame"`、`resolution:"1080p"`、`voice:true`，且不要传 `lastFrameImageUrl`。

### 比例默认值与自适应

- `aspectRatio` 不传，或传 `default` / `默认` / `按模型`：使用脚本内置模型默认比例；当前默认是参考图 wan2.6 和首尾帧可灵2.6 为 `adaptive`，其它模型为 `9:16`。
- `aspectRatio` 传 `adaptive` / `自适应` / `auto` / `adapt`：明确请求自适应，只在该模型支持 `adaptive` 时通过校验。
- `aspectRatio` 传 `16:9` / `9:16` / `1:1`：表示用户明确选择该比例，Skill 不会自动改成 `adaptive`。

## 已有任务查询

当用户询问“刚才那个视频的进度 / 状态 / 是否完成 / 结果 / 失败原因”时，必须先走已有任务查询，**不得进入下方生成流水线**。

- 先在 workspace 的 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/` 查找底层任务记录：`linkfox-aigc-videogen-task-*.json` 或 `linkfox-aigc-videogen-multi-task-*.json`。
- 根据任务记录里的 `skill` 字段，委托对应底层能力的查询模式：`linkfox-aigc-videogen` 用 `--query-task`，`linkfox-aigc-videogen-multi` 用 `--query-task`。
- 若用户直接提供 `taskId`，只调用底层能力的查询模式；不得重新提交图片、prompt 或模型参数。
- 查询返回 `PROCESSING` 时只说明仍在生成；`SUCCESS` 时展示底层返回的本地视频路径；`FAILED` 时读取 `errorMsg` 做用户可读说明，不自动重试、不换模型、不重建任务。

## 流水线步骤

### 步骤 1：识别模式

- **输入**：用户提供的 JSON 参数。
- **操作**：先确认 `entry` 严格等于 `img2video`；缺失或其它入口直接报错。然后优先读取 `mode`；没有 `mode` 时，存在 `lastFrameImageUrl` 判为 `first_last_frame`，否则存在 `imageList` 或 `imageUrl` 判为 `reference`。
- **输出**：`reference`、`first_last_frame`，或 `{ "error": true, "message": "..." }`。
- **用途**：被步骤 2 用来选择模型校验规则、图片校验规则和底层 skill。

### 步骤 2：校验并规范化参数

- **输入**：步骤 1 的模式和用户参数。
- **操作**：校验必填字段、字段类型、模型枚举、时长范围、图片数量和图片 URL；把业务模型名归一成工具网关枚举。
- **输出**：合法参数对象，或 `{ "error": true, "message": "..." }`。
- **用途**：合法参数进入步骤 3；错误对象直接返回给 Agent 做用户可读说明。

### 步骤 3：调用通用底层视频能力

- **输入**：步骤 2 的合法参数。
- **操作**：按模式和模型直接调用底层 skill（唯一调用方式，禁止改用脚本、HTTP 或其它视频 skill）：
  1. 参考图模式中，seedance2.0、seedance2.0fast、可灵Omni、HappyHorse 调用 skill `linkfox-aigc-videogen-multi`，传 `imageList`、`videoType`、`videoTime`、`prompt`、`promptOptimizer`、`isPro`、`voice`、`camera`、`aspectRatio`、`resolution`。
  2. 参考图模式海螺2.3、wan2.6 调用 skill `linkfox-aigc-videogen`，传单张 `imageUrl`、对应 `videoType`、`videoTime`、`prompt`、`promptOptimizer`、`isPro`、`voice`、`camera`、`aspectRatio`、`resolution`；wan2.6 不传 `imageList`。
  3. 首尾帧模式调用 skill `linkfox-aigc-videogen`，传 `imageUrl`，可选 `lastFrameImageUrl`，以及 `videoType`、`videoTime`、`prompt`、`promptOptimizer`、`isPro`、`voice`、`camera`、`aspectRatio`、`resolution`。
  4. **底层 skill 输出原封不动透传**：`linkfox-aigc-videogen` / `linkfox-aigc-videogen-multi` 自行完成网关调用、响应落盘和视频下载，本 Skill 不做二次包装、不截取、不重新输出。
- **输出**：底层 skill stdout；成功通常包含 `Saved full response: ["...mp4"]`，失败可能包含 `Saved full response: xxx.json` 或错误说明。
- **用途**：业务层只负责选择底层 skill 和组装参数，不接触工具网关鉴权、HTTP 请求、响应落盘和视频下载细节。

### 步骤 4：读取底层能力交付结果

- **输入**：步骤 3 的底层 skill stdout。
- **操作**：按底层 skill 输出判定成败；成功则收集 `Saved full response:` 后的本地视频路径，失败则读取其落盘 JSON 中的 `errcode` / `errmsg` / `error` / `status` / `errorMsg` 做用户可读说明。若响应出现 `status=FAILED` 且 `errorMsg` 为“图片审核不通过”或其它审核、侵权、人脸、明星/名人肖像相关失败，立即停止；不得重新上传同一素材、换模型、换底层 skill、改 prompt 或继续调用工具绕过。
- **输出**：`media_paths`。
- **用途**：Agent 只把本地视频路径展示给用户。

### 步骤 5：返回最终交付

- **输入**：步骤 4 的 `media_paths` 或失败原因。
- **操作**：成功时只展示本地视频路径、所用模式/模型和必要说明；失败时简短说明原因和可修正参数。
- **输出**：面向用户的短回复。
- **用途**：完成交付，不生成报告，不输出原始响应。

## 输出规则

- 只向用户展示 `media_paths` 中的本地视频路径。
- 不要 Read 视频文件，不要展示 base64 内容。
- 不要把原始 API 返回的临时 URL 直接给用户。
- 图片审核不通过是终止型业务失败；只提示用户更换有授权、无明星/名人肖像或侵权风险的合规图片。

## 执行自检

每次执行后，Agent 在收尾时确认：

- [ ] 成功时 `mode` 与用户输入一致。
- [ ] 已按当前模型调用对应的 `linkfox-aigc-videogen` 或 `linkfox-aigc-videogen-multi` skill。
- [ ] 成功时 `voice` 符合声音与尾帧规则；尤其可灵2.6 只有 `1080p + voice=false` 才能带 `lastFrameImageUrl`。
- [ ] 成功时优先展示底层 skill 返回的本地视频路径；若为空，说明视频 URL 缺失或下载失败，并提示用户查看底层 skill 的落盘 JSON。
- [ ] 图片审核不通过时立即停止，并返回用户可读的合规换图提示；不重试、不绕路。
- [ ] 用户询问已有任务进度时，已使用 task 记录或 taskId 查询，没有重新调用生成流程。
- [ ] 错误时按底层 skill 返回的业务原因说明，不展示 Python traceback。
- [ ] 没有读取或输出视频文件正文/base64。

## 已知局限

- 本 Skill 不负责上传本地图片；进入脚本前，前端或上游 Agent 需要先把图片转换成可访问的 http(s) URL。
- 真实视频生成由底层能力完成，需要有效 `LINKFOX_AGENT_API_KEY`，并可能耗时 100-600 秒。
- 本 Skill 不包含带货口播、数字人、配音、字幕、剪辑包装。
- 失败时不自动重试。
