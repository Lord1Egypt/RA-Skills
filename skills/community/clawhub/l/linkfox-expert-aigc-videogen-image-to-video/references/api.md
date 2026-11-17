# 图转视频编排参考

本页只描述 `linkfox-aigc-videogen-image-to-video` 的业务参数与底层 skill 路由。实际工具网关接口、鉴权、响应落盘、视频下载由 `linkfox-aigc-videogen` / `linkfox-aigc-videogen-multi` 维护。

## 路由规则

| 模式 | 模型 | 底层 skill | 传图字段 |
|------|------|------------|----------|
| `reference` | seedance2.0 / SEED | `linkfox-aigc-videogen-multi` | `imageList` |
| `reference` | seedance2.0fast / SEED_FAST | `linkfox-aigc-videogen-multi` | `imageList` |
| `reference` | 可灵Omni / KLING | `linkfox-aigc-videogen-multi` | `imageList` |
| `reference` | HappyHorse | `linkfox-aigc-videogen-multi` | `imageList` |
| `reference` | wan2.6 / WAN | `linkfox-aigc-videogen` | `imageUrl` |
| `reference` | 海螺2.3 / HAILUO | `linkfox-aigc-videogen` | `imageUrl` |
| `first_last_frame` | seedance2.0 / SEED | `linkfox-aigc-videogen` | `imageUrl` + 可选 `lastFrameImageUrl` |
| `first_last_frame` | seedance2.0fast / SEED_FAST | `linkfox-aigc-videogen` | `imageUrl` + 可选 `lastFrameImageUrl` |
| `first_last_frame` | 可灵2.6 / KLING | `linkfox-aigc-videogen` | `imageUrl` + 条件可选 `lastFrameImageUrl` |

## 下游参数映射

### 调 `linkfox-aigc-videogen-multi`

传入：

- `imageList`
- `videoType`
- `videoTime`
- `prompt`
- `promptOptimizer`
- `isPro`
- `voice`
- `camera`
- `aspectRatio`
- `resolution`

### 调 `linkfox-aigc-videogen`

传入：

- `imageUrl`
- `lastFrameImageUrl`（首尾帧模式可选）
- `videoType`
- `videoTime`
- `prompt`
- `promptOptimizer`
- `isPro`
- `voice`
- `camera`
- `aspectRatio`
- `resolution`

说明：

- wan2.6 只走单图 `linkfox-aigc-videogen`，必须传单张 `imageUrl`，不传 `imageList`。
- 海螺2.3 / HAILUO 的短时长有 UI 与底层枚举差异：业务 UI 显示 `5秒`，但底层 `linkfox-aigc-videogen` 合法参数是 `videoTime=6`；`10秒` 对应 `videoTime=10`。收到 `videoTime=6` 时应原样透传，不得修正为 5。
- V 模型当前不对外路由。

## 判定与输出

- 成功：底层 skill stdout 含 `Saved full response: ["...mp4"]`，本 skill 只展示本地视频路径。
- 失败：底层 skill stdout 含 `Saved full response: xxx.json` 或错误说明，按 `errcode` / `errmsg` / `error` 做用户可读解释。
- 禁止读取或输出视频文件正文/base64。
- 禁止把底层 API 临时 URL 直接给用户。
