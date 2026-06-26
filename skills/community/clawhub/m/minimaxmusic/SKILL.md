---
name: minimax-music-generation
description: 使用 MiniMax API 生成创意音乐。当用户要求生成音乐、创作歌曲、制作背景音乐时使用。支持纯音乐和人声歌曲，可指定风格、情绪和场景。
---

# MiniMax 音乐生成

## 快速开始

### API 端点
```
POST https://api.minimaxi.com/v1/music_generation
```

### 请求格式 (PowerShell)
```powershell
$json = @{
    model = "music-2.6"
    prompt = "音乐描述（风格、情绪、场景）"
    is_instrumental = $true  # $false = 带歌词的人声歌曲
    output_format = "url"   # 返回 URL 而非 hex
    lyrics = "歌词内容"      # 仅非纯音乐时需要
} | ConvertTo-Json -Compress

Invoke-RestMethod -Uri "https://api.minimaxi.com/v1/music_generation" -Method Post -Headers @{
    Authorization = "Bearer <API_KEY>"
} -ContentType "application/json" -Body ([System.Text.Encoding]::UTF8.GetBytes($json)) -TimeoutSec 180
```

### 参数说明

| 参数 | 必填 | 说明 |
|------|------|------|
| model | 是 | 使用 `music-2.6` |
| prompt | 是 | 音乐描述，1-2000字符，如"流行音乐,欢快,适合广告背景" |
| is_instrumental | 否 | `$true`=纯音乐，`$false`=人声歌曲（默认） |
| lyrics | 否 | 歌词，使用`\n`分隔行，支持标签`[Verse]` `[Chorus]`等 |
| output_format | 否 | `url`（推荐）或`hex`，默认hex |
| audio_setting | 否 | 音频设置：sample_rate(44100), bitrate(256000), format(mp3) |

### 响应示例
```json
{
  "data": {
    "audio": "https://...",
    "status": 2
  },
  "extra_info": {
    "music_duration": 142576,  // 毫秒
    "music_sample_rate": 44100,
    "bitrate": 256000
  },
  "base_resp": { "status_code": 0, "status_msg": "success" }
}
```

## 工作流程

1. 构建 JSON 请求体
2. 调用 API（超时建议 180 秒）
3. 检查 `base_resp.status_code === 0`
4. 下载音频文件（URL 有效期 24 小时）
5. 发送给用户

## 常见错误

- `invalid params`: 参数格式错误，检查 JSON 结构和必填字段
- `insufficient balance`: 余额不足
- `model: xxx not support`: Token 未开通该模型权限

## 提示词技巧

- **纯音乐**: `is_instrumental: $true`，prompt 示例：`独立民谣,忧郁,内省,渴望,独自漫步,咖啡馆`
- **人声歌曲**: `is_instrumental: $false`，提供 lyrics，prompt 示例：`流行音乐,欢快,青春校园`
- **歌词标签**: `[Verse]` `[Chorus]` `[Pre-Chorus]` `[Bridge]` `[Interlude]` `[Outro]`
