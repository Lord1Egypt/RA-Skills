---
name: minimax-music
description: MiniMax 音乐生成技能 - 支持歌词生成(Lyrics Generation)、音乐生成(Music Generation)。支持自定义歌词段落结构(verse/chorus/bridge/intro/outro)，异步生成 MP3 格式音乐，自动下载保存到本地。
version: 1.0.0
author: laowang
tags:
  - minimax
  - music
  - lyrics
  - music-generation
  - lyrics-generation
---

# MiniMax Music Skill

使用 MiniMax API 进行音乐生成和歌词创作。支持歌词生成、音乐生成，支持自定义歌词段落结构，异步生成 MP3 格式音乐，可自动下载保存到本地。

## 环境配置

```json
{
  "MINIMAX_API_KEY": "your-api-key",
  "MINIMAX_REGION": "cn" | "int"
}
```

- `MINIMAX_API_KEY`: MiniMax API 密钥
- `MINIMAX_REGION`: 区域设置，`cn` 为中国，`int` 为国际（默认 `cn`）

## 可用函数

### generate_music(lyrics, description, model)
音乐生成

**参数**:
- `lyrics`: 歌词内容
- `description`: 音乐描述/风格
- `model`: 音乐模型（默认: `music-01`）

**返回**: 任务ID列表

**示例**: `generate_music("[verse]\n蓝天白云下\n我们在奔跑\n[chorus]\n青春就是这样", "欢快的流行歌曲")`

### generate_lyrics(description, keywords, model)
歌词生成

**参数**:
- `description`: 歌曲描述/主题
- `keywords`: 关键词列表（可选）
- `model`: 歌词模型（默认: `lyrics-01`）

**返回**: 生成的歌词文本

**示例**: `generate_lyrics("一首关于梦想的歌", ["坚持", "希望", "前行"])`

### query_music_task(task_id)
查询音乐生成任务状态

**参数**:
- `task_id`: 任务ID

**返回**: 任务状态信息 `{status, music_url, ...}`

**状态值**: `Pending`, `Processing`, `Success`, `Fail`

### wait_for_music(task_id, poll_interval, max_wait)
等待音乐生成完成（轮询）

**参数**:
- `task_id`: 任务ID
- `poll_interval`: 轮询间隔秒数（默认: 10）
- `max_wait`: 最大等待时间（默认: 600）

**返回**: 最终任务状态信息

### download_music(music_url, output_path)
下载音乐到本地

**参数**:
- `music_url`: 音乐下载URL
- `output_path`: 保存路径

**返回**: 保存的文件路径

## 使用示例

### 直接生成音乐

```
python scripts/music.py generate "[verse]\n月亮挂在天上\n星星闪闪发光\n[chorus]\n夜空中最亮的星" -d "温柔的民谣歌曲"
```

### 先生成歌词，再生成音乐

```
# 先生成歌词
python scripts/music.py lyrics "一首关于夏天的歌" -k 阳光 沙滩 海浪

# 使用生成的歌词创建音乐
python scripts/music.py generate "<生成的歌词>" -d "欢快的夏季主题歌曲"
```

### 查询任务状态

```
python scripts/music.py query <task_id>
```

### 等待音乐完成

```
python scripts/music.py wait <task_id> -i 10
```

### 下载音乐

```
python scripts/music.py download <music_url> -o song.mp3
```

## 歌词格式说明

歌词按段落返回，使用空行分隔不同段落。可用的段落标记：
- `[verse]` - 主歌
- `[chorus]` - 副歌/高潮
- `[bridge]` - 桥段
- `[intro]` - 前奏
- `[outro]` - 尾奏

## 注意事项

1. 歌词越详细，生成的音乐效果越好
2. 可以不提供歌词，仅通过 description 生成音乐
3. 音乐生成是异步的，需要通过 task_id 查询状态
4. 建议使用 `wait_for_music` 函数自动等待完成
5. 音乐生成可能需要几分钟时间，请耐心等待
