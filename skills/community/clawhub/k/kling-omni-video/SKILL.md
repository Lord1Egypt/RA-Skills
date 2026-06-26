---
name: kling-video
description: 使用可灵 Omni-Video API 生成或编辑视频。凡是涉及可灵视频的操作都应触发此 skill，包括但不限于：可灵生成视频、kling视频、文生视频(可灵)、图生视频(可灵)、视频编辑(可灵)、视频参考。当用户明确提到"可灵"或"kling"并需要视频生成/编辑时触发。配置：环境变量 HSAI_API_KEY。
---

# 可灵 Omni-Video 视频生成与编辑

通过 `scripts/generate_video.sh` 完成视频全流程（提交任务 → 轮询状态 → 下载文件）。

## 使用方式

```bash
bash <skill-dir>/scripts/generate_video.sh \
  --prompt "视频描述" \
  [--model kling-video-o1] \
  [--output ./output.mp4] \
  [--aspect-ratio 16:9|9:16|1:1] \
  [--duration 5] \
  [--mode pro|std] \
  [--sound on|off] \
  [--image <url-or-base64>] \
  [--image-type first_frame|end_frame] \
  [--image2 <url-or-base64>] \
  [--image2-type first_frame|end_frame] \
  [--video <url>] \
  [--video-refer-type base|feature] \
  [--video-keep-sound yes|no] \
  [--poll-interval 10] \
  [--timeout 900]
```

### 参数说明

| 参数 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `--prompt` | 是 | - | 视频描述文本，最多 2500 字符。可用 `<<<image_1>>>`、`<<<video_1>>>` 引用图片/视频 |
| `--model` | 否 | `kling-v3-omni` | 模型名称，可选 `kling-video-o1` |
| `--output` | 否 | `./kling_video_<ts>.mp4` | 输出文件路径 |
| `--aspect-ratio` | 条件 | - | 画面比例：`16:9`、`9:16`、`1:1`。纯文生视频时必填；有首帧图或视频编辑时不需要 |
| `--duration` | 否 | `5` | 时长（秒），可选 3-15。视频编辑模式下无效 |
| `--mode` | 否 | `pro` | 生成模式：`pro`（高品质）、`std`（标准，性价比高） |
| `--sound` | 否 | `off` | 是否同时生成声音：`on`/`off` |
| `--image` | 否 | - | 参考图片 URL（或 Base64）。可作为普通参考、首帧或尾帧 |
| `--image-type` | 否 | - | 图片帧类型：`first_frame` 或 `end_frame`，不设则为普通参考图 |
| `--image2` | 否 | - | 第二张参考图片 URL |
| `--image2-type` | 否 | - | 第二张图片帧类型 |
| `--video` | 否 | - | 参考视频 URL（MP4/MOV，≤200MB） |
| `--video-refer-type` | 否 | `base` | 视频类型：`base`（待编辑/指令变换）、`feature`（特征参考） |
| `--video-keep-sound` | 否 | `no` | 是否保留视频原声：`yes`/`no` |
| `--poll-interval` | 否 | `10` | 轮询间隔秒数 |
| `--timeout` | 否 | `900` | 最长等待秒数 |

## 常用场景

### 1. 文生视频
```bash
bash <skill-dir>/scripts/generate_video.sh \
  --prompt "一只猫在沙滩上奔跑" \
  --aspect-ratio "16:9" --duration 7 --mode pro
```

### 2. 图生视频（首帧）
```bash
bash <skill-dir>/scripts/generate_video.sh \
  --prompt "让画面中的人物向镜头挥手" \
  --image "https://example.com/photo.jpg" \
  --image-type first_frame --mode pro
```

### 3. 视频编辑（指令变换）
```bash
bash <skill-dir>/scripts/generate_video.sh \
  --prompt "给<<<video_1>>>中的人戴上墨镜" \
  --video "https://example.com/input.mp4" \
  --video-refer-type base --video-keep-sound yes
```

### 4. 视频参考（生成下一个镜头）
```bash
bash <skill-dir>/scripts/generate_video.sh \
  --prompt "基于<<<video_1>>>，生成下一个镜头" \
  --video "https://example.com/input.mp4" \
  --video-refer-type feature --aspect-ratio "16:9" --duration 5
```

## 注意事项

- 环境变量 `HSAI_API_KEY` 必须设置；依赖 `curl` 和 `python3`
- 视频生成耗时较长（通常 3-10 分钟），脚本会自动轮询等待
- 如果用户未指定 prompt，先向用户询问要生成什么内容的视频
- 如果用户提供的描述比较简短，可以帮助扩展为更详细的 prompt
- 有参考视频时，`--sound` 只能为 `off`
- 视频编辑模式（`--video-refer-type base`）下，输出视频时长与输入视频相同，`--duration` 和 `--aspect-ratio` 无效
- 视频生成完成后，告知用户文件路径，询问是否需要移动/复制
