# linkfox-aigc-videogen-viral-replicate 编排用例

## 正常用例

- 输入 `entry=viralReplica`、参考视频 URL、商品图 URL、`target_duration=15S`、`sales_country=US(美国)`、`target_language=英语` -> 应先调用 `linkfox-aigc-textgen`，传 `imageUrls=[reference_video_url]`、`model=GEM_3_1_PRO` 获得 `video_analysis`，再做商品图分析和 prompt 替换，最终调用 `linkfox-aigc-videogen-multi`。
- 输入 `entry=viralReplica`、参考视频 URL、商品图 URL，且视频 URL 直分析返回 `10005` / 视频不可读 / 内容为空 -> 应使用 `scripts/extract_video_frames.py` 抽取 8-10 张 JPG，调用 `linkfox-file-upload` 上传帧图，再调用 `linkfox-aigc-textgen`，传 `imageUrls=[frame_image_urls]`、`model=GEM_3_FLASH`、Step 1F prompt 获得 `video_analysis`，继续后续流程。
- 输入 `videoType=seedance2.0fast` -> 最终调用 `linkfox-aigc-videogen-multi` 时，`videoType` 必须为 `SEED_FAST`，且默认 `voice=true`。
- 输入已包含 `video_analysis` -> 可跳过 `linkfox-aigc-textgen` 参考视频分析，从商品图分析继续。
- 输入已包含 `video_analysis`，且参考视频 URL 也是 http(s) -> 不再调用 `linkfox-aigc-textgen` 分析参考视频，直接从商品图分析继续。
- 输入 `extra_product_image_urls` 多张同商品细节图 -> 最终调用 `linkfox-aigc-videogen-multi` 时，`imageList` 必须为 `[product_image_url, ...extra_product_image_urls]`。
- `target_duration=Auto` 且原视频时长超过 15 秒 -> `videoTime` 解析为 15，并在 Step 2 prompt 中加入截断或压缩指令。

## 错误用例

- `entry` 不是 `viralReplica` -> 直接报参数错误，不调用底层 skill。
- 缺少 `reference_video_url` 或 `product_image_url` -> 先补参，不调用底层 skill。
- 图片或视频是本地路径，不是 http(s) URL -> 要求先上传成公网 URL。
- 未提供 `video_analysis`，且 `linkfox-aigc-textgen` 分析参考视频失败 -> 必须先执行标准抽帧兜底；只有抽帧、帧图上传或帧序列分析也失败时，才停止并说明具体失败点。
- 参考视频是 MP4 URL -> 应调用 `linkfox-aigc-textgen` 且传 `imageUrls=[reference_video_url]`、`model=GEM_3_1_PRO`。
- 参考视频直分析失败后 -> 不得把 MP4 URL 改写进 prompt 或试探其它字段；只能按标准抽帧兜底，用帧图 `imageUrls` 调 `GEM_3_FLASH`。
- 参考视频是 MP4 URL -> 不得把 URL 只写进 prompt 后要求模型读取。
- `linkfox-aigc-textgen` 视频分析失败 -> 不得临时写脚本绕过；只能使用本 skill 自带的 `scripts/extract_video_frames.py`。
- `target_duration` 不是 `Auto` / `5S` / `10S` / `15S` -> 直接报参数错误。

## 覆盖点

这些用例覆盖入口保护、视频理解能力缺口、商品图分析、prompt 替换、时长适配、最终委托 `linkfox-aigc-videogen-multi` 和媒体路径交付。
