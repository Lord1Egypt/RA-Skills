# 带货口播编排参考

本页只描述 `linkfox-aigc-videogen-sale` 的业务参数与底层 skill 路由。实际视频工具网关接口、鉴权、响应落盘、视频下载由 `linkfox-aigc-videogen` / `linkfox-aigc-videogen-multi` 维护。

## 流程边界

| 阶段 | 职责 | 是否调用底层视频 skill |
|------|------|------------------------|
| 方案阶段 | 商品图理解、商品卖点整理、生成 3 套口播方案并展示给用户选择 | 否 |
| 生成阶段 | 校验用户选择的结构化方案，合成最终视频 prompt | 是，按模型调用 `linkfox-aigc-videogen` 或 `linkfox-aigc-videogen-multi` |

## 下游参数映射

生成阶段按模型调用底层视频 skill：

- seedance2.0、seedance2.0fast、HappyHorse 调用 `linkfox-aigc-videogen-multi`，传 `imageList`。
- wan2.6 调用 `linkfox-aigc-videogen`，传单张 `imageUrl`；如果上游只有 `imageList`，只能取单张主商品图，不能传多图。
- `videoType`：`SEED` / `SEED_FAST` / `WAN` / `HAPPY_HORSE`。
- `videoTime`：由 `videoDuration` 归一。
- `prompt`：由选中方案的剧情、环境、分镜 prompt、口播稿、负向提示词合成；若显式 `skipSchemeSelection=true`，可使用最终确认的 `prompt`。
- `promptOptimizer`
- `aspectRatio`
- `isPro`
- `voice`：固定按口播视频打开，传 `true`。
- `camera`
- `resolution`

## 关键约束

- 正常流程必须先生成 3 套方案，并等待用户回复 1/2/3。
- 生成阶段必须传完整 `selectedScheme`，或传 `schemes + selectedSchemeNumber` / `selectedSchemeIndex`。
- 不接受 `"方案一"` 这类静态文本冒充结构化方案。
- 未显式 `skipSchemeSelection=true` 时，不接受只传最终 `prompt` 直接生成。
- 生成阶段只调用 `linkfox-aigc-videogen` / `linkfox-aigc-videogen-multi`，禁止改用脚本、HTTP 或其它视频 skill。

## 判定与输出

- 成功：底层 skill stdout 含 `Saved full response: ["...mp4"]`，本 skill 只展示本地视频路径。
- 失败：底层 skill stdout 含 `Saved full response: xxx.json` 或错误说明，按 `errcode` / `errmsg` / `error` 做用户可读解释。
- 禁止读取或输出视频文件正文/base64。
- 禁止把底层 API 临时 URL 直接给用户。

## 已知局限

- 本 Skill 不直接依赖视频生成后端接口；带货口播是“商品图理解 + 三套口播方案 + 委托底层视频 Skill 生成视频”的业务编排。
- `SEED` 可理解为 seedance2.0，`SEED_FAST` 可理解为 seedance2.0fast，`WAN` 可理解为 wan2.6，`HAPPY_HORSE` 可理解为 HappyHorse。
- 底层视频 endpoint 由 `linkfox-aigc-videogen` / `linkfox-aigc-videogen-multi` 维护；本 Skill 不维护 endpoint 覆盖逻辑。
- 本 Skill 不负责上传本地图片；进入脚本前，前端或上游 Agent 需要先把图片转换成可访问的 http(s) URL。
- 本 Skill 不做输入图片比例校验、裁切、拼图或补边；`aspectRatio` / `resolution` 按图转视频参考图模式做输出参数校验。
- 真实视频生成由底层能力完成，需要有效 `LINKFOX_AGENT_API_KEY`，并可能耗时 100-600 秒。
