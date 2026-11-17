# linkfox-aigc-videogen-image-to-video 编排用例

## 正常用例

- 输入 `entry=img2video`、`mode=reference`、`imageList` 多张、`videoType=seedance2.0`、`videoTime=5` -> 应调用 skill `linkfox-aigc-videogen-multi`，传 `videoType=SEED`、`imageList`、`videoTime=5`。
- 输入 `entry=img2video`、`mode=reference`、`imageList` 多张、`videoType=seedance2.0fast`、`videoTime=5` -> 应调用 skill `linkfox-aigc-videogen-multi`，传 `videoType=SEED_FAST`、`voice=true`。
- 输入 `entry=img2video`、`mode=reference`、单张 `imageUrl`、`videoType=海螺2.3`、前端选择 `5秒` 并传入 `videoTime=6` -> 应调用 skill `linkfox-aigc-videogen`，传 `videoType=HAILUO`、`imageUrl`，并保持 `videoTime=6`。
- 输入 `entry=img2video`、`mode=first_last_frame`、`imageUrl`、`lastFrameImageUrl`、`videoType=seedance2.0`、`videoTime=10` -> 应调用 skill `linkfox-aigc-videogen`，传首帧和尾帧。
- 输入 `entry=img2video`、有 `lastFrameImageUrl` 且未显式传 `mode` -> 自动按 `first_last_frame` 处理，并调用 skill `linkfox-aigc-videogen`。
- 输入 `entry=img2video`、`mode=reference`、单张 `imageUrl`、`videoType=wan2.6` -> 应调用 skill `linkfox-aigc-videogen`，传 `videoType=WAN`、`imageUrl`，不得传 `imageList`。

## 错误用例

- 缺少 `entry=img2video` -> 本 skill 直接报参数错误，不调用底层 skill。
- 缺少图片 URL -> 本 skill 直接报参数错误，不调用底层 skill。
- 本地图片路径未先上传为 http(s) URL -> 本 skill 直接报参数错误。
- 首尾帧模式使用 `videoType=wan2.6` -> 本 skill 直接报模型不支持，不调用底层 skill。
- 参考图模式使用 `videoType=wan2.6` 且传入多张图片 -> 本 skill 直接报图片数量不支持，不调用底层 skill。
- 使用 V 模型 -> 当前不对外路由，应要求用户改选 seedance2.0/seedance2.0fast/可灵2.6。
- 可灵2.6 首尾帧传尾帧但不满足 `resolution=1080p` 且 `voice=false` -> 本 skill 直接报参数组合不支持。

## 覆盖点

这些用例覆盖入口保护、模式识别、业务模型名归一、底层 skill 路由、图片 URL 校验和模型组合校验。实际网关调用、响应落盘、视频下载由 `linkfox-aigc-videogen` / `linkfox-aigc-videogen-multi` 自行验证。
