---
name: hailuo-gyh
description: MiniMax 海螺视频生成技能。支持文生视频、图生视频、首尾帧视频、主体参考视频四种模式。使用前需设置环境变量 MINIMAX_API_KEY。
metadata: {"openclaw":{"emoji":"🎬","requires":{"bins":["python3"]}}}
---

# MiniMax 海螺视频生成

使用 MiniMax 海螺 API 生成视频。支持 4 种模式：

1. **文生视频**：根据文本描述生成视频
2. **图生视频**：基于图片 + 文本描述生成视频
3. **首尾帧**：首图 + 尾图 + 文本生成视频
4. **主体参考**：人脸照片 + 文本，保持人物特征一致

## 前置要求

- Python 3
- `pip3 install requests`

## 使用方法

```bash
# 文生视频
python3 {baseDir}/scripts/video_gen.py --mode text --prompt "描述文字"

# 图生视频（推荐用于小说分镜）
python3 {baseDir}/scripts/video_gen.py --mode image --prompt "描述文字" --image "图片URL或本地路径"

# 首尾帧生成
python3 {baseDir}/scripts/video_gen.py --mode start_end --prompt "描述文字" --first "首图URL" --last "尾图URL"

# 主体参考
python3 {baseDir}/scripts/video_gen.py --mode subject --prompt "描述文字" --subject "人脸图片URL"
```

## 参数说明

| 参数 | 说明 | 必填 |
|------|------|------|
| `--mode` | 模式：text/image/start_end/subject | 是 |
| `--prompt` | 视频描述文本（建议英文，效果更佳） | 是 |
| `--image` | 图生视频的首帧图片 URL（image 模式） | image 模式必填 |
| `--first` | 首尾帧模式的首帧图片 URL | start_end 模式必填 |
| `--last` | 首尾帧模式的尾帧图片 URL | start_end 模式必填 |
| `--subject` | 主体参考模式的人脸图片 URL | subject 模式必填 |
| `--duration` | 视频时长：6 或 10 秒，默认 6 | 否 |
| `--resolution` | 分辨率：720P / 768P / 1080P，默认 768P | 否 |
| `--output` | 输出文件名，默认 output.mp4 | 否 |

## 模型说明

- 文生视频 / 图生视频：`MiniMax-Hailuo-2.3`（支持 768P / 1080P）
- 首尾帧视频：`MiniMax-Hailuo-02`（支持 768P / 1080P）
- 主体参考：`S2V-01`

> ⚠️ 注意：龚云荷的账户不支持 1080P，建议使用 `--resolution 768P`（已设为默认）。

## 示例（小说分镜）

```bash
python3 {baseDir}/scripts/video_gen.py \
  --mode image \
  --prompt "Cinematic winter scene in rural northern China. A young mother washes vegetables in icy well water. A little girl crouches nearby. Muted earth tones, film grain, shallow depth of field, melancholic atmosphere." \
  --image "/Users/gyh/Desktop/obsidian_file/GYH_file/AI小说/情节反转小说/女性向/周桂兰.png" \
  --duration 6 \
  --resolution 768P \
  --output "/Users/gyh/Desktop/obsidian_file/GYH_file/AI小说/情节反转小说/女性向/scene1.mp4"
```

## API 配置

使用前需设置环境变量 `MINIMAX_API_KEY`（从 https://platform.minimax.com 获取）。

```bash
export MINIMAX_API_KEY="你的API Key"
```
