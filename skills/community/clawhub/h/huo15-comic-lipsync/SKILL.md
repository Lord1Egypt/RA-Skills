---
name: huo15-comic-lipsync
displayName: 火15 漫剧-对口型
description: 给视频镜头+对白音频做口型同步（Kling 2.5 Lip Sync）。没有对白的镜头跳过。触发词：对口型、lipsync、口型同步。
version: 0.1.0
---

# 火15 漫剧-对口型 Skill

> 视频 + 音频 → 口型同步后的视频。

---

## 输入 / 输出

```bash
python scripts/lipsync.py \
  --video-dir output/demo/videos \
  --audio-dir output/demo/audio \
  --out-dir output/demo/lipsync
```

每个镜头取该镜第一条对白的音频做口型同步；无对白直接复制原视频。

## API

```
POST https://api.kling.com/v1/videos/lip-sync
Headers: Authorization: Bearer {KLING_API_KEY}
Body:
{
  "video_url": "...",
  "audio_url": "...",
  "mode": "kling-v2.5"
}
```

## 注意

- 视频最短 3s，如果对白音频 <3s 自动补静默
- 单镜成本 ¥3，48 镜 = ¥144（可通过 `--no-lipsync` 关闭省钱）
