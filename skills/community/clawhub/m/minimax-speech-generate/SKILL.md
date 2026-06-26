---
name: minimax-speech
description: MiniMax 语音合成技能 - 支持同步/异步文本转语音(T2S)、音色克隆(Voice Clone)、音色设计(Voice Design)、音色查询与删除。使用模型 speech-2.8-hd，输出 mp3/wav/pcm 格式音频文件到本地。
version: 1.0.0
author: laowang
tags:
  - minimax
  - speech
  - tts
  - voice-clone
  - voice-design
  - audio
---

# MiniMax Speech Skill

使用 MiniMax API 进行语音合成、语音克隆和音色设计。支持同步/异步文本转语音、音色克隆、音色设计、音色查询与删除。使用模型 speech-2.8-hd，输出 mp3/wav/pcm 格式音频文件。

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

### text_to_speech(text, voice_id, output_file)
同步文本转语音

**参数**:
- `text`: 要转换的文本
- `voice_id`: 音色ID（默认: `female-tianmei`）
- `output_file`: 输出文件路径

**示例**: `text_to_speech("你好世界", "female-tianmei", "hello.mp3")`

### text_to_speech_async(text, voice_id)
异步文本转语音，返回任务ID

**参数**:
- `text`: 要转换的文本
- `voice_id`: 音色ID

**返回**: 任务ID

### query_speech_task(task_id)
查询异步任务状态

**参数**:
- `task_id`: 任务ID

**返回**: 任务状态信息

### clone_voice(audio_file_path, title)
音色快速复刻

**参数**:
- `audio_file_path`: 参考音频文件路径
- `title`: 新音色名称

**返回**: 新音色的 voice_id

### design_voice(text, style)
音色设计

**参数**:
- `text`: 音色描述文本
- `style`: 音色风格

**返回**: 设计生成的 voice_id

### list_voices()
获取音色列表

**返回**: 音色列表

### get_voice(voice_id)
获取单个音色信息

**参数**:
- `voice_id`: 音色ID

### delete_voice(voice_id)
删除音色

**参数**:
- `voice_id`: 音色ID

**返回**: 是否成功

## 常用音色

| 音色ID | 描述 |
|--------|------|
| female-tianmei | 女声甜美 |
| male-yunyang | 男声播音 |
| female-badu | 女声巴度 |
| male-shawn | 男声 Shawn |
| female-shanshan | 女声杉杉 |

## 使用示例

### 同步语音合成

```
python scripts/speech.py tts "欢迎使用 MiniMax 语音服务" -v female-tianmei -o output.mp3
```

### 异步语音合成

```
python scripts/speech.py tts-async "这是一段较长的文本" -v male-yunyang
```

### 查询任务

```
python scripts/speech.py query <task_id>
```

### 克隆音色

```
python scripts/speech.py clone reference_audio.mp3 -t "我的音色"
```

### 音色设计

```
python scripts/speech.py design "温柔的女性声音，适合朗读" -s gentle
```

### 删除音色

```
python scripts/speech.py delete <voice_id>
```

## 注意事项

1. 同步语音合成适合短文本（< 60秒音频）
2. 长文本建议使用异步接口
3. 音色克隆需要清晰、无噪音的参考音频
4. 克隆和设计的音色需要审核后才能使用
