# MiniMax 音乐 API 参考

## 基础配置

- **国内用户**: `https://api.minimaxi.com/v1`
- **国际用户**: `https://api.minimax.io/v1`
- **认证方式**: `Authorization: Bearer $MINIMAX_API_KEY`

## API 端点

### 1. 音乐生成 (Music Generation) - 同步

```
POST /v1/music_generation
```

**请求体**:
```json
{
  "model": "music-2.5",
  "lyrics": "歌词内容",
  "description": "音乐描述"
}
```

**响应** (同步返回，直接包含音频数据):
```json
{
  "data": {
    "audio": "hex编码的音频数据",
    "status": "success"
  },
  "base_resp": {
    "status_code": 0,
    "status_msg": "success"
  }
}
```

**注意**: 音频数据是 hex 编码的 MP3 数据，需要用 `bytes.fromhex()` 解码

### 2. 歌词生成 (Lyrics Generation)

```
POST /v1/lyrics_generation
```

**请求体**:
```json
{
  "model": "lyrics-01",
  "description": "歌曲描述/主题",
  "keywords": ["关键词1", "关键词2"]
}
```

**响应**:
```json
{
  "lyrics": "生成的歌词内容",
  "base_resp": {
    "status_code": 0,
    "status_msg": "success"
  }
}
```

## 音乐模型

- `music-2.5` - 音乐生成模型
- `lyrics-01` - 歌词生成模型

## 歌词格式说明

歌词按段落返回，使用 `\n\n` 分隔不同段落。歌词中可以使用 `[verse]`、`[chorus]`、`[bridge]` 等标记标注段落类型。

## 使用流程

1. (可选) 使用歌词生成API生成歌词
2. 调用音乐生成API，传入歌词和描述
3. API 同步返回 hex 编码的 MP3 音频数据
4. 解码并保存为本地文件
