---
name: huo15-comic-video
displayName: 火15 漫剧-图生视频
description: 分镜关键帧 → 短视频（Seedance 2.0 图生视频，关键帧做 first_frame，5s/镜，最多 3 并发，开启 return_last_frame 用于下镜衔接）。触发词：图生视频、分镜视频、漫剧视频化。
version: 0.1.0
---

# 火15 漫剧-图生视频 Skill

> 关键帧 → 视频片段。核心复用 `huo15-influencer-video-skill` 的 Seedance 2.0 模式。

---

## 输入 / 输出

```bash
python scripts/video.py \
  --script output/demo/script.json \
  --frame-dir output/demo/storyboard \
  --out-dir output/demo/videos
```

输出：

```
videos/
├── S01.mp4
├── S02.mp4
├── ...
└── last_frames/      # return_last_frame 输出，用于下镜衔接
    ├── S01_last.png
    └── ...
```

## 关键参数

| 参数 | 值 | 说明 |
|---|---|---|
| model | `doubao-seedance-2-0-260128` | 火山方舟 |
| first_frame | `storyboard/{sid}.png` | 关键帧做首帧 |
| ratio | `9:16` | 竖屏 |
| duration | 5 | 每镜 5 秒 |
| return_last_frame | true | 保存 last_frame 供下镜接续 |
| watermark | false | |

## 并发与续跑

- 最多 3 任务并发提交（`DEFAULTS["concurrency"]`），避免限流
- 每镜 checkpoint 独立（`videos.S01=done`），失败只重做失败镜头

## 成本

5s × ¥0.994/s = ¥4.97/镜。48 镜 ≈ ¥239。
