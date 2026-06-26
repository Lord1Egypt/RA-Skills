---
name: minimax-music
description: MiniMax AI 音乐生成技能。使用 MiniMax API 生成歌词、合成歌曲、批量生成样本曲目、支持纯音乐和人声歌曲。可用风格：古风、摇滚、流行、钢琴、催眠等。当用户要求"生成音乐"、"写首歌"、"生成歌词"、"合成歌曲"、"批量生成BGM样本"时触发。
---

# MiniMax AI 音乐生成

## 快速开始

### 前置条件

- MiniMax API Key（Token Plan 用户可用 `sk-cp-F-...` Key）
- Python 3.x + `requests` 库
- `ffmpeg`（用于合并曲目）

### 基础调用流程

```
1. 歌词生成（如需要）→ /v1/lyrics_generation
2. 歌曲生成 → /v1/music_generation
3. 下载音频文件
4. ffmpeg 合并多首（如需要）
```

---

## 歌词生成

**接口**: `POST https://api.minimaxi.com/v1/lyrics_generation`

```python
payload = {
    "mode": "write_full_song",      # 写完整歌曲
    "prompt": "主题描述",
    "title": "歌名（可选）"
}
```

**响应**:
```python
{
    "song_title": "歌名",
    "style_tags": "风格标签",
    "lyrics": "带结构的歌词（含 [Verse][Chorus] 等标签）",
    "base_resp": {"status_code": 0, "status_msg": "success"}
}
```

---

## 歌曲生成

**接口**: `POST https://api.minimaxi.com/v1/music_generation`

### 纯音乐（无人声）
```python
payload = {
    "model": "music-2.6",
    "prompt": "风格描述",
    "is_instrumental": True,
    "output_format": "url"     # 返回下载URL
}
```

### 有歌词歌曲
```python
payload = {
    "model": "music-2.6",
    "prompt": "风格描述（与歌词配合）",
    "lyrics": lyrics_text,       # 歌词（带 [Verse][Chorus] 等标签）
    "output_format": "url"
}
```

### 关键参数

| 参数 | 说明 |
|------|------|
| `model` | `music-2.6`（Token Plan推荐）或 `music-2.6-free`（限免，RPM低） |
| `prompt` | 音乐风格描述，1-2000字符，中英均可 |
| `lyrics` | 歌词，结构标签：`[Intro][Verse][Pre-Chorus][Chorus][Hook][Drop][Bridge][Solo][Build-up][Instrumental][Breakdown][Break][Interlude][Outro]` |
| `is_instrumental` | `true`=纯音乐，`false`=有歌词歌曲 |
| `output_format` | `url`（推荐，24小时有效）或 `hex`（返回十六进制字符串） |
| `stream` | `false`=同步等待完成，`true`=流式（仅支持hex格式） |

**生成时间**：通常2-5分钟，`timeout`建议设为 **600秒**

**响应**:
```python
{
    "data": {
        "audio": "https://...mp3",   # 下载URL（output_format=url时）
        "status": 2                  # 1=生成中，2=已完成
    },
    "extra_info": {
        "music_duration": 157335,   # 时长（毫秒）
        "music_sample_rate": 44100,
        "bitrate": 256000,
        "music_size": 5036711       # 文件大小（字节）
    },
    "base_resp": {"status_code": 0, "status_msg": "success"}
}
```

---

## 批量生成脚本

使用 `scripts/generate.py`，支持：
- 单曲生成
- 批量生成多首
- 歌词生成 + 歌曲合成
- 多首合并成一首

```bash
# 查看用法
python scripts/generate.py --help

# 生成纯音乐
python scripts/generate.py --prompt "欢快的流行音乐" --name "01_欢快流行" --save "D:\music_samples"

# 生成带歌词的歌曲（先歌词后歌曲）
python scripts/generate.py --lyrics-prompt "给唐晓加油打气的励志歌曲" --song-title "赠唐晓" --prompt "古风音乐" --name "赠唐晓_古风" --save "D:\music_samples"

# 合并已有文件（先生成多个文件后合并）
python scripts/generate.py --merge "D:\music_samples\01.mp3" "D:\music_samples\02.mp3" --output "D:\music_samples\merged.mp3"
```

**FFmpeg 手动合并**：
```bash
# 创建文件列表
# concat_list.txt 内容（每行 file '路径'）：
file 'D:\music_samples\曲1.mp3'
file 'D:\music_samples\曲2.mp3'
file 'D:\music_samples\曲3.mp3'

# 合并
ffmpeg -y -f concat -safe 0 -i "D:\music_samples\concat_list.txt" -c copy "D:\music_samples\合并版.mp3"
```

---

## 完整工作流示例

### 生成古风励志歌曲《赠唐晓》

```python
import requests
import json

API_KEY = "your_key_here"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

# Step 1: 生成歌词
lyrics_payload = {
    "mode": "write_full_song",
    "prompt": "给唐晓加油打气的古风歌曲，温暖励志",
    "title": "赠唐晓"
}
r = requests.post("https://api.minimaxi.com/v1/lyrics_generation",
    headers=headers, json=lyrics_payload, timeout=60)
lyrics = r.json()["lyrics"]

# Step 2: 生成歌曲（API超时设为600秒）
song_payload = {
    "model": "music-2.6",
    "prompt": "古风音乐，优雅励志，笛子古筝为主",
    "lyrics": lyrics,
    "output_format": "url"
}
r = requests.post("https://api.minimaxi.com/v1/music_generation",
    headers=headers, json=song_payload, timeout=600)
audio_url = r.json()["data"]["audio"]

# Step 3: 下载
audio = requests.get(audio_url, timeout=60)
with open("D:\\music_samples\\赠唐晓.mp3", "wb") as f:
    f.write(audio.content)
```

### 生成催眠钢琴曲（合并成长曲）

```python
# 先生成3首钢琴曲
prompts = [
    "solo piano, slow tempo, sleep aid, relaxing",
    "solo piano, very slow 40-50 BPM, lullaby style",
    "ambient piano, meditative, rain sounds background"
]
urls = []
for p in prompts:
    r = requests.post("https://api.minimaxi.com/v1/music_generation",
        headers=headers,
        json={"model":"music-2.6","prompt":p,"is_instrumental":True,"output_format":"url"},
        timeout=600)
    urls.append(r.json()["data"]["audio"])

# 下载并用ffmpeg合并
```

---

## 常见问题

**Q: 请求超时怎么办？**
A: `music-2.6` 生成需要2-5分钟，务必将 `timeout` 设为 **600秒**，同步等待结果。

**Q: 返回 `RemoteDisconnected`？**
A: 服务器在高负载时会主动断开，保持重试机制，通常2-3次重试后成功。

**Q: 如何生成更长的音乐？**
A: API单次上限约5分钟（157-200秒），可通过 FFmpeg 合并多首生成更长曲目。

**Q: `sk-cp-F-...` Key 是否可用？**
A: 可用，但这是 Token Plan 专属 Key，与普通按量计费 Key 不同，仅限音乐/图像等非文本模型使用。

**Q: URL 有效期多久？**
A: 音频下载 URL 有效期为 **24小时**，生成后请及时下载。

---

## 注意事项

- 纯音乐：设置 `is_instrumental: True`，`prompt` 必填
- 有歌词歌曲：`lyrics` 必填，`prompt` 可选（描述风格）
- 中文歌词标签支持：`[Verse]`、`[Chorus]`、`[Bridge]` 等
- 请求频率：Token Plan 100次/5小时，注意不要超出限额
