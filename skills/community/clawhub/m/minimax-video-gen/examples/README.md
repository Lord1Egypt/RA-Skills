# MiniMax 视频生成示例

本目录存放使用 MiniMax Hailuo 生成的视频示例。

## 示例视频

| 文件 | Prompt | 模型 | 说明 |
|------|--------|------|------|
| video1.mp4 | "A little girl grow up." | MiniMax-Hailuo-02 | 首尾帧模式：小女孩成长 |
| video2.mp4 | "On an overcast day, in an ancient cobbled alleyway..." | MiniMax-Hailuo-02 | 时尚街拍风格 |
| video3.mp4 | "A little girl grow up." | MiniMax-Hailuo-02 | 同video1的另一版本 |

## 生成参数

```javascript
{
  prompt: "A little girl grow up.",
  first_frame_image: "https://filecdn.minimax.chat/public/fe9d04da-f60e-444d-a2e0-18ae743add33.jpeg",
  last_frame_image: "https://filecdn.minimax.chat/public/97b7cd08-764e-4b8b-a7bf-87a0bd898575.jpeg",
  model: "MiniMax-Hailuo-02",
  duration: 6,
  resolution: "1080P"
}
```

## 生成时间

2026-03-21 20:02 (北京时间)
