# 详细使用示例

本文档包含各 provider 的完整命令示例，作为 SKILL.md 的补充参考。

## 环境变量

所有直连接口（Gemini 生图、Sora/Veo/Grok/豆包/Vidu 生视频）共用：

```bash
export API_KEY="your-api-key"           # 必填
export API_BASE_URL="https://your-api-host"  # 必填
```

### Provider 模型参数（可选）

```bash
# Gemini
export GEMINI_MODEL="gemini-3-pro-image-preview"

# Sora
export SORA_MODEL="sora-2"
export SORA_SIZE="720x1280"
export SORA_SECONDS="10"

# Veo
export VEO_MODEL="veo_3_1-fast"
export VEO_SIZE="1280x720"
export VEO_SECONDS="8"
export VEO_ENABLE_UPSAMPLE="true"

# Grok
export GROK_MODEL="grok-video-3-pro"
export GROK_SIZE="720P"
export GROK_SECONDS="10"
export GROK_ASPECT_RATIO="2:3"

# 豆包
export DOUBAO_MODEL="doubao-seedance-1-5-pro_720p"
export DOUBAO_SIZE="16:9"
export DOUBAO_SECONDS="4"

# Vidu
export VIDU_MODEL="TC-vidu-q3-turbo"
export VIDU_DURATION="5"
export VIDU_SIZE="720p"
export VIDU_ASPECT_RATIO="16:9"
```

## Gemini 文生图

```bash
# 基础用法
python3 {baseDir}/scripts/gemini_generate_image.py "赛博朋克风格的城市夜景海报" --aspect-ratio 16:9 --image-size 2K

# 指定中转接口
python3 {baseDir}/scripts/gemini_generate_image.py "复古插画风产品海报" --api-key YOUR_KEY --auth-token YOUR_TOKEN --base-url YOUR_BASE_URL
```

- 接口路径：`/v1beta/models/{model}:generateContent`
- API Key 同时用作 query 参数 `key` 和 Bearer 鉴权
- 支持通过 `--aspect-ratio` 控制宽高比，`--image-size` 控制清晰度（512 / 1K / 2K / 4K）

## Sora 文生视频

```bash
python3 {baseDir}/scripts/sora_generate_video.py "猫咪听歌摇头晃脑，下大雨" --model sora-2 --size 720x1280 --seconds 10
```

## Veo 文生视频

```bash
# 通过主入口
python3 {baseDir}/scripts/sora_generate_video.py "城市延时航拍" --model veo_3_1-fast --size 1280x720 --seconds 8

# 通过别名入口（等价）
python3 {baseDir}/scripts/veo_generate_video.py "城市延时航拍" --model veo_3_1-fast --size 1280x720 --seconds 8 --enable-upsample true
```

- Veo 文档建议 `seconds=8`
- `enable_upsample` 仅横屏 1280x720 可用

## Grok 文生视频

```bash
# 通过别名入口
python3 {baseDir}/scripts/grok_generate_video.py "城市延时航拍" --model grok-video-3-pro --size 720P --seconds 10 --aspect-ratio 2:3
```

## 豆包文生视频

```bash
# 通过别名入口
python3 {baseDir}/scripts/doubao_generate_video.py "城市延时航拍" --model doubao-seedance-1-5-pro_720p --size 16:9 --seconds 4
```

## 图生视频（Sora/Veo/Grok/豆包）

```bash
python3 {baseDir}/scripts/sora_generate_video.py "让角色从静止开始微笑并转头" \
  --model sora-2 \
  --input-reference /path/to/ref1.jpg /path/to/ref2.png \
  --seconds 10
```

- 通过 `--input-reference` 传本地图片路径，可传多张

## Vidu 文生/图生视频

```bash
# 文生视频
python3 {baseDir}/scripts/vidu_generate_video.py "一个美女在雨中跳舞" --model TC-vidu-q3-turbo --seconds 5 --size 720p --aspect-ratio 16:9

# 图生视频（1 张图 URL）
python3 {baseDir}/scripts/vidu_generate_video.py "让图片中的人物开始跳舞" --model TC-vidu-q2-pro --image-urls https://example.com/photo.jpg --seconds 5

# 首尾帧生视频（2 张图 URL）
python3 {baseDir}/scripts/vidu_generate_video.py "主角在夜空下奔跑" --model TC-vidu-q2-pro --image-urls https://example.com/start.jpg https://example.com/end.jpg --seconds 4
```

- 接口路径：`POST /v1/video/generations`（JSON 请求体）
- 图生/首尾帧推荐使用 `--image-urls` 传图片 URL 列表

## 查询视频任务

```bash
# 单次查询
python3 {baseDir}/scripts/sora_query_video.py TASK_ID

# 轮询到完成
python3 {baseDir}/scripts/sora_query_video.py TASK_ID --wait --interval 5 --max-wait 900
```

别名查询入口（等价）：

```bash
python3 {baseDir}/scripts/veo_query_video.py TASK_ID
python3 {baseDir}/scripts/grok_query_video.py TASK_ID
python3 {baseDir}/scripts/doubao_query_video.py TASK_ID
python3 {baseDir}/scripts/vidu_query_video.py TASK_ID
```

所有查询入口均支持 `--wait --interval N --max-wait N` 轮询模式。
