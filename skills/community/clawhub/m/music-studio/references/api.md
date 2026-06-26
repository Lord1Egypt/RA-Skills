# MiniMax 音乐 API 参考（以当前实测链路为准）

> 这份参考是针对当前 `music-studio` 实际接入方式整理的，重点记录**已实测跑通**的链路。
> 若官方文档后续更新，应以最新官方文档为准，并重新验证。

## 基础信息

- **Base URL**: `https://api.minimaxi.com/v1/`
- **认证**: Bearer Token (API Key)
- **返回格式**: JSON

---

## 作词 `/v1/lyrics_generation`

生成完整歌曲歌词，或编辑/续写已有歌词。

### 请求参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `mode` | string | 模式：`write_full_song`（完整歌曲，默认）/ `edit`（编辑/续写） |
| `prompt` | string | 主题/风格描述，最多 2000 字符 |
| `lyrics` | string | 现有歌词，仅 `edit` 模式有效，最多 3500 字符 |
| `title` | string | 指定歌曲标题（可选） |

### 响应

| 字段 | 说明 |
|------|------|
| `song_title` | 歌曲标题 |
| `style_tags` | 风格标签，逗号分隔 |
| `lyrics` | 歌词，含结构标签 |

---

## 文本生成音乐 `/v1/music_generation`

### 当前实测可用模型

| 模型 | 用途 | 备注 |
|------|------|------|
| `music-2.6` | 文本生成音乐 | 已实测通过 |
| `music-cover` | **不要直接用于最终翻唱生成** | 当前在 `music-studio` 中只用于前处理 |

### 请求参数（文本生成音乐）

| 参数 | 类型 | 说明 |
|------|------|------|
| `model` | string | `music-2.6` |
| `prompt` | string | 风格/情绪/场景描述 |
| `lyrics` | string | 非纯音乐时可传歌词 |
| `is_instrumental` | bool | 纯音乐 |
| `lyrics_optimizer` | bool | 自动根据 prompt 生成歌词 |
| `output_format` | string | `url` 或 `hex` |
| `audio_setting.sample_rate` | int | 采样率：16000/24000/32000/44100 |
| `audio_setting.bitrate` | int | 比特率：32000/64000/128000/256000 |
| `audio_setting.format` | string | 格式：mp3/wav/pcm |

### 响应

```json
{
  "data": {
    "audio": "https://...",
    "status": 2
  },
  "base_resp": {
    "status_code": 0,
    "status_msg": "success"
  }
}
```

---

## 翻唱前处理 `/v1/music_cover_preprocess`

> 当前实测通过。用于从参考音频提取 `cover_feature_id`、自动歌词和结构信息。

### 请求参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `model` | string | 固定为 `music-cover` |
| `audio_url` | string | 参考音频 URL |
| `audio_base64` | string | 参考音频 Base64，与 `audio_url` 二选一 |

### 实测返回字段

| 字段 | 说明 |
|------|------|
| `cover_feature_id` | 后续翻唱生成要用的特征 ID |
| `formatted_lyrics` | 从参考音频提取并格式化的歌词 |
| `structure_result` | 歌曲结构分析结果（JSON 字符串） |
| `audio_duration` | 参考音频时长 |

---

## 翻唱最终生成 `/v1/music_generation`

> 当前 `music-studio` **已实测跑通** 的方式是：
>
> - 前处理：`music_cover_preprocess(model=music-cover)`
> - 最终生成：`music_generation(model=music-2.6)`
>
> 即：**前处理模型与最终生成模型不同**。

### 当前实测可用请求方式

| 参数 | 类型 | 说明 |
|------|------|------|
| `model` | string | `music-2.6` |
| `prompt` | string | 目标翻唱风格描述 |
| `cover_feature_id` | string | 前处理返回 |
| `lyrics` | string | 手动提供或使用前处理返回的 `formatted_lyrics` |
| `output_format` | string | `url` |
| `audio_setting.*` | object | 音频输出设置 |

### 说明

- 当前 `music-studio` **不再使用**旧的 `reference_audio_url` / `reference_audio_base64` 字段。
- 当前 `music-studio` 也**不直接用 `music-cover` 做最终生成**，因为这一条在实测中不稳定/报错，而“`music-cover` 前处理 + `music-2.6` 最终生成”已实测通过。

---

## 状态码（通用）

| status_code | 说明 |
|-------------|------|
| 0 | 成功 |
| 1002 | 触发限流 |
| 1004 | API Key 错误 |
| 1008 | 余额不足 |
| 1026 | 内容涉及敏感 |
| 2013 | 参数异常 |
| 2049 | 无效 API Key |
