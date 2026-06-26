---
name: mp4-to-srt
description: 將本地 MP4/MKV/AVI 影片用 AI 轉成 SRT 字幕，自動轉為繁體中文！
---

# MP4 轉 SRT 字幕神器 🎬→📝

## 這能做什麼？

✅ 將 MP4/MKV/AVI 轉成 SRT 字幕  
✅ 自動轉為**繁體中文**  
✅ 支援多語言 (中/英/日/韓)  
✅ 自動偵測語言  

## 使用方式

```bash
# 基本轉換 (自動轉繁體)
mp4-to-srt.sh "影片路徑.mp4"

# 指定輸出檔案
mp4-to-srt.sh "影片.mp4" "輸出.srt"

# 指定模型 (tiny, base, small, medium, large)
mp4-to-srt.sh "影片.mp4" "輸出.srt" "small"
```

## 需求

- ffmpeg: `brew install ffmpeg`
- Whisper: `pip3 install openai-whisper`
- opencc: `brew install opencc` (用於轉繁體)

## 輸出

標準 SRT 字幕檔案，可直接匯入 YouTube 或播放器。

## 流程

1. Whisper AI 轉錄影片音頻
2. 自動轉換為繁體中文 (opencc)
3. 輸出標準 SRT 格式

## 備註

- 預設模型: small (速度與準確度平衡)
- 較大的模型較慢但更準確

## 作者

Kuanlin
