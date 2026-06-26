# MiniMax 音乐 API 参考

## 基础信息

- **Base URL**: `https://api.minimaxi.com/v1`
- **认证**: `Authorization: Bearer {API_KEY}`
- **Content-Type**: `application/json`

## 可用模型

| 模型 | 说明 | 可用范围 |
|------|------|----------|
| `music-2.6` | 文本生成音乐（推荐） | Token Plan 用户 + 付费用户 |
| `music-cover` | 参考音频翻唱 | Token Plan 用户 + 付费用户 |
| `music-2.6-free` | 限免版 music-2.6 | 所有用户，RPM较低 |
| `music-cover-free` | 限免版 music-cover | 所有用户，RPM较低 |

## Token Plan 限额

- 刷新周期：每5小时
- 每次刷新：100次调用
- 日均可用：约480次（扣除刷新间隙）

---

## 接口1：歌词生成

**POST** `/lyrics_generation`

### 请求参数

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `mode` | string | ✅ | `write_full_song`=完整歌曲，`edit`=编辑/续写 |
| `prompt` | string | ✅ | 歌曲主题/风格描述，≤2000字符 |
| `title` | string | ❌ | 指定歌名，输出保持一致 |
| `lyrics` | string | ❌ | 现有歌词，edit模式时必填，≤3500字符 |

### 响应

```json
{
  "song_title": "歌名",
  "style_tags": "Pop, Upbeat, Romantic",
  "lyrics": "[Intro]\n\n[Verse]\n...歌词内容...\n[Chorus]\n...",
  "base_resp": {
    "status_code": 0,
    "status_msg": "success"
  }
}
```

### 支持的歌词结构标签

`[Intro]` `[Verse]` `[Pre-Chorus]` `[Chorus]` `[Hook]` `[Drop]`
`[Bridge]` `[Solo]` `[Build-up]` `[Instrumental]` `[Breakdown]`
`[Break]` `[Interlude]` `[Outro]` `[Post-Chorus]`

---

## 接口2：歌曲生成

**POST** `/music_generation`

### 请求参数

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | ✅ | `music-2.6` 或 `music-2.6-free` |
| `prompt` | string | ✅* | 风格描述，纯音乐时必填，≤2000字符 |
| `lyrics` | string | ✅* | 歌词，有歌词歌曲时必填，≤3500字符 |
| `is_instrumental` | bool | ❌ | `true`=纯音乐，`false`=有歌词，默认false |
| `output_format` | string | ❌ | `url`（默认，24h有效）或 `hex` |
| `stream` | bool | ❌ | `true`=流式（仅支持hex），默认false |
| `audio_setting` | object | ❌ | 音频设置，见下方 |
| `aigc_watermark` | bool | ❌ | 是否添加水印，默认false |

### audio_setting

```json
{
  "sample_rate": 44100,    // 可选 16000/24000/32000/44100
  "bitrate": 256000,       // 可选 32000/64000/128000/256000
  "format": "mp3"           // 可选 mp3/wav/pcm
}
```

### 响应

```json
{
  "data": {
    "audio": "https://...mp3",   // output_format=url时
    "status": 2                   // 1=生成中，2=已完成
  },
  "trace_id": "xxx",
  "extra_info": {
    "music_duration": 157335,     // 时长（毫秒）
    "music_sample_rate": 44100,
    "music_channel": 2,
    "bitrate": 256000,
    "music_size": 5036711         // 文件大小（字节）
  },
  "base_resp": {
    "status_code": 0,
    "status_msg": "success"
  }
}
```

---

## 错误码

| 错误码 | 含义 | 解决方法 |
|--------|------|----------|
| 0 | 成功 | - |
| 1002 | 频率超限 | 稍后再试 |
| 1004 | 未授权/Key无效 | 检查API Key |
| 1008 | 余额不足 | 检查账户余额 |
| 1026 | 输入内容涉敏 | 调整prompt/lyrics |
| 1027 | 输出内容涉敏 | 调整prompt/lyrics |
| 2056 | 超出Token Plan限制 | 等待额度刷新 |

---

## prompt 风格参考

### 中文风格关键词
- 古风、摇滚、流行、爵士、电子、民谣，抒情
- 欢快、治愈、热血、史诗、梦幻、轻松
- 励志、浪漫、孤独、激昂、宁静

### 英文风格关键词
- Mandopop, Rock, Jazz, Electronic, Folk, Ambient
- Upbeat, Melancholic, Anthemic, Chill, Dreamy
- Motivational, Romantic, Energetic, Meditation

### 纯音乐场景描述
```
Solo piano, slow tempo, sleep aid, relaxing
Epic orchestral, cinematic trailer music, powerful
Cyberpunk electronic, futuristic, strong beat
Chinese traditional instruments, guzheng, elegant
```

### 带歌词歌曲描述
```
古风音乐，优雅励志，笛子古筝为主，温暖有力
摇滚风格，激情澎湃，电吉他为主，贝斯强劲
流行音乐，明快节奏，适合短视频背景
浪漫爵士风格，夜晚氛围，适合情侣视频
```

---

## URL 有效期

- 音频下载 URL 有效期：**24小时**
- 生成后请及时下载保存
