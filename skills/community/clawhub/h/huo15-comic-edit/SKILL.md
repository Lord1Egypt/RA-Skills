---
name: huo15-comic-edit
displayName: 火15 漫剧-成片拼接
description: FFmpeg 把 lipsync 视频按顺序 concat + 叠 BGM + 烧字幕 + 0.3s 淡入淡出，输出 final.mp4。触发词：视频拼接、成片合成、FFmpeg 拼接。
version: 0.1.0
---

# 火15 漫剧-成片拼接 Skill

> 所有片段 → 一条 final.mp4。纯本地 FFmpeg，无 API 成本。

---

## 输入 / 输出

```bash
python scripts/edit.py --project-dir output/demo
```

读取：
- `lipsync/S*.mp4`（或 fallback 到 `videos/S*.mp4`）
- `audio/S*_*.wav`（对白，与视频混入）
- `bgm.mp3`（整片 BGM）
- `script.json`（取对白文本+时间戳生成字幕）

输出：`final.mp4`

## 工作流

1. **拼接视频**：ffmpeg concat demuxer，按 scene id 顺序
2. **生成字幕**：从 script.json 计算每条对白的起止时间（按镜头 5s 均摊）→ `subtitle.srt`
3. **混音**：对白 + BGM（-20dB） + 原视频音轨（-6dB）
4. **烧字幕**：ffmpeg `subtitles` filter，国风样式（宋体/描边）
5. **转场**：相邻镜头 0.3s crossfade（可选）

## 字幕样式（subtitle.ass）

```
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, Bold, Outline, Alignment, MarginV
Style: Default,Source Han Serif SC,48,&H00FFFFFF,&H00000000,1,3,2,120
```

## 依赖

- 系统装 `ffmpeg` ≥ 5.0
- 字体：`Source Han Serif SC`（思源宋体）
