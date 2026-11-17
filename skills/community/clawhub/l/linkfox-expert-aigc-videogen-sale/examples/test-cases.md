# linkfox-aigc-videogen-sale 编排用例

## 正常用例

- 用户提供商品图、卖点、目标受众、时长、语言/地区 -> 本 skill 先生成 3 套口播方案，展示后停止等待用户选择，不调用视频生成底层 skill。
- 用户选择方案 1，且上下文保留完整 `schemes` -> 本 skill 取 `schemes[0]` 合成最终 prompt，按模型调用底层视频 skill。
- 调用方直接传完整 `selectedScheme` -> 本 skill 校验结构后合成最终 prompt，按模型调用底层视频 skill。
- 调用方显式传 `skipSchemeSelection=true` 且 `prompt` 已是最终成片提示词 -> 本 skill 可跳过方案选择，直接按模型调用底层视频 skill。
- 用户选择 seedance2.0fast -> 调用 `linkfox-aigc-videogen-multi`，传 `videoType=SEED_FAST`、`voice=true`。
- 用户选择 wan2.6 且只传 `imageUrl` -> 调用 `linkfox-aigc-videogen`，传 `videoType=WAN`、`imageUrl`，不得传 `imageList`。

## 错误用例

- 方案阶段缺少商品图、卖点、目标受众或时长 -> 先补参，不生成方案。
- 生成阶段只传 `"方案一"` 这类静态文本 -> 拒绝，要求传完整 `selectedScheme` 或 `schemes + selectedSchemeNumber`。
- 未显式 `skipSchemeSelection=true` 却只传 `prompt` -> 拒绝，避免跳过方案选择。
- `videoType` 不能归一到 `SEED` / `SEED_FAST` / `WAN` / `HAPPY_HORSE` -> 直接报参数错误，不调用底层 skill。
- `videoType=WAN` 但传入多张图片 -> 要求用户保留 1 张主商品图，不调用底层 skill。
- `imageList` 为空或图片不是 http(s) URL -> 直接报参数错误，不调用底层 skill。

## 覆盖点

这些用例覆盖两阶段口播约束、结构化方案选择、prompt 合成、WAN 单图传参和底层 skill 路由。实际网关调用、响应落盘、视频下载由 `linkfox-aigc-videogen` / `linkfox-aigc-videogen-multi` 自行验证。
