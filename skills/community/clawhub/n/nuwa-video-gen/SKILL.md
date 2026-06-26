---
name: nuwa-video-gen
description: 视频生成技能，使用 MiniMax 女娲视频生成 API 创建视频（文生视频/图生视频/首尾帧/主体参考）
metadata:
  openclaw:
    emoji: "🎬"
    requires:
      bins: ["python3"]
      env:
        MINIMAX_API_KEY:
          description: MiniMax API Key（从 platform.minimaxi.com 获取）
---

# Nuwa Video Gen - MiniMax 女娲视频生成

使用 MiniMax 女娲视频生成 API，支持4种生成模式：

1. **文生视频**：根据文本描述生成视频
2. **图生视频**：基于图片 + 文本描述生成视频
3. **首尾帧**：首图 + 尾图 + 文本描述生成视频
4. **主体参考**：人脸照片 + 文本描述，保持人物特征一致

## 前置要求

- **API Key**：从 [platform.minimaxi.com](https://platform.minimaxi.com) 获取
- 安装依赖：`pip3 install requests`
- 设置环境变量：`export MINIMAX_API_KEY="your-key"`

## 使用方法

### Python 脚本（推荐）

```bash
# 文生视频
python3 {baseDir}/scripts/video_gen.py --mode text --prompt "描述文字"

# 图生视频
python3 {baseDir}/scripts/video_gen.py --mode image --prompt "描述文字" --image "图片URL"

# 首尾帧生成
python3 {baseDir}/scripts/video_gen.py --mode start_end --prompt "描述文字" --first "首图URL" --last "尾图URL"

# 主体参考（人脸一致）
python3 {baseDir}/scripts/video_gen.py --mode subject --prompt "描述文字" --subject "人脸图片URL"
```

### 参数说明

| 参数 | 说明 | 必填 |
|------|------|------|
| `--mode` | 模式：text / image / start_end / subject | 是 |
| `--prompt` | 视频描述文本 | 是 |
| `--image` | 图生视频的首帧图片URL | image模式必填 |
| `--first` | 首尾帧模式的首帧图片URL | start_end模式必填 |
| `--last` | 首尾帧模式的尾帧图片URL | start_end模式必填 |
| `--subject` | 主体参考模式的人脸图片URL | subject模式必填 |
| `--duration` | 视频时长：6 或 10（秒） | 否，默认6 |
| `--resolution` | 分辨率：720P / 1080P | 否，默认1080P |
| `--output` | 输出文件名（默认 output.mp4） | 否 |

## 模型说明

| 模式 | 模型 | 说明 |
|------|------|------|
| text（文生视频） | MiniMax-Hailuo-2.3 | 标准文生视频 |
| image（图生视频） | MiniMax-Hailuo-2.3 | 以图为首帧生成视频 |
| start_end（首尾帧） | MiniMax-Hailuo-02 | 开头结尾两图生成视频 |
| subject（主体参考） | S2V-01 | 保持人物特征一致 |

## 输出说明

- 视频文件保存到 `--output` 指定路径（默认为当前目录的 `output.mp4`）
- Agent 负责将生成的视频文件发送给用户

## 注意事项

- 视频生成是**异步过程**，需要轮询等待（约10-60秒）
- 推荐轮询间隔：10秒
- 图片 URL 需要是公开可访问的链接
- **主体参考模式涉及人脸图片**，请确保已获得图片当事人授权

## API 文档

- API Key 管理：https://platform.minimaxi.com
- 接口文档：https://platform.minimaxi.com/docs/llms.txt
