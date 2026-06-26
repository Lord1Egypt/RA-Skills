---
name: minimax-music-gyh
description: MiniMax 音乐生成模型，支持 Music-2.5/Music-2 等模型，根据文本描述生成音乐。使用 MINIMAX_API_KEY 环境变量。
metadata: {"openclaw":{"emoji":"🎵","requires":{"bins":["python3"]}}}
---

# MiniMax 音乐生成

使用 MiniMax 音乐生成 API，根据文本描述生成音乐。

## 支持的模型

| 模型 | 说明 |
|------|------|
| `music-02` | 最新音乐生成模型，支持多种风格 |
| `music-2.5+` | 乐器解锁，跨风格融合 |
| `music-2.5` | 人声+多乐器，专业录音棚质量 |

## 前置要求

- Python 3
- `pip3 install requests`
- 设置环境变量 `MINIMAX_API_KEY`

## 使用方法

```bash
# 生成音乐
python3 {baseDir}/scripts/music_gen.py \
  --prompt "A relaxing piano melody with soft strings, classical style, peaceful morning" \
  --output relax_music.mp3

# 指定模型和歌词
python3 {baseDir}/scripts/music_gen.py \
  --model music-02 \
  --prompt "欢快的中国风音乐，二胡和笛子合奏" \
  --lyrics "春风吹过来，百花盛开" \
  --output chinese_music.mp3
```

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--model` | 模型名称 | `music-02` |
| `--prompt` | 音乐描述文本 | - |
| `--lyrics` | 歌词（可选） | - |
| `--output` | 输出文件路径 | `output.mp3` |
