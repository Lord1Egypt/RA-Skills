---
name: language-helper
description: "Use this skill whenever the user wants to learn how to say something in another language. Triggers include: language tags like 【日语】【英语】【韩语】【法语】【西班牙语】【德语】 followed by a Chinese sentence, or phrases like '用日语怎么说', '这句话用英语怎么说', 'how do you say X in Japanese', '翻译成日语', '日语翻译'. The skill translates the input, generates pronunciation audio via SenseAudio TTS, and provides grammar analysis with key vocabulary. Do NOT use for general translation without voice, music generation, or non-language-learning tasks."
requires:
  env:
    - SENSEAUDIO_API_KEY
  bins:
    - ffmpeg
---

# language-helper

将中文句子翻译为目标语言，并提供发音语音、简要语法说明和重点词汇。

## 触发方式

- `【日语】我今天很累`
- `【英语】这个说法太生硬了`
- `【简洁】【韩语】谢谢你的帮助`
- "用日语怎么说……"
- "翻译成英语并朗读"

## 模式

### 默认模式
返回：
- 翻译结果
- 发音语音
- 简要语法说明
- 重点词汇
- 可选替代表达

### 简洁模式
当用户添加 `【简洁】` 时，仅返回：
- 翻译结果
- 发音语音
- 关键词注释

## 环境检查

先检查环境变量 `SENSEAUDIO_API_KEY`。如果已经存在，直接使用；如果不存在，再提示用户提供 API Key 或先在终端设置环境变量。不要把密钥写进 `SKILL.md`、脚本源码或提交记录。

首次运行前检查：

1. 首次运行时 skill 会自动创建 `skills/language-helper/.env` 模板，用户需填写对应的值
2. 确认 `ffmpeg` 已安装

`.env` 示例：

```bash
SENSEAUDIO_API_KEY=your_key

# 以下为飞书语音条功能（可选，不用飞书可不填）
FEISHU_APP_ID=cli_xxx
FEISHU_APP_SECRET=xxx
FEISHU_CHAT_ID=oc_xxx
```

检查 ffmpeg：

```bash
which ffmpeg
# 若未安装：
# macOS: brew install ffmpeg
# Linux: sudo apt install ffmpeg
```

## 内置音色映射

始终优先使用用户显式指定的 `voice_id`。未指定时，根据目标语言选择默认音色。

在当前 SenseAudio key 权限有限时，仅默认使用已确认可用的以下音色：

- `child_0001_b`：可爱萌娃，平稳
- `male_0004_a`：儒雅道长，平稳
- `male_0018_a`：沙哑青年，深情

不要默认选择未确认授权的 VIP / SVIP 音色。若接口返回 `403 no access to the specified voice`，优先回退到 `child_0001_b`，而不是重复尝试未授权音色。

```yaml
LANG_VOICE_MAP:
  ja: male_0004_a
  en: male_0004_a
  zh: male_0004_a
  ko: male_0004_a
  fr: male_0004_a
  es: male_0004_a
  de: male_0004_a
```

## 输入解析

从用户输入中提取：

- 目标语言
- 是否为 【简洁】 模式
- 待翻译文本
- 解释语言

解释语言默认跟随用户输入语言：

- 用户用中文提问 → 中文解释
- 用户用英文提问 → 英文解释

语言代码映射：

| 标签 | 代码 |
|------|------|
| 日语 | ja |
| 英语 | en |
| 韩语 | ko |
| 法语 | fr |
| 西班牙语 | es |
| 德语 | de |

## 执行流程

一次完成以下内容：

1. 翻译文本
2. 生成并发送语音
3. 输出文字讲解

### 语音发送

优先发送飞书语音条：

```bash
python3 skills/language-helper/scripts/main.py send-voice \
  --text "{translated_text}" \
  --lang {lang_code}
```

若飞书配置缺失，则降级为本地播报：

```bash
python3 skills/language-helper/scripts/main.py speak \
  --text "{translated_text}" \
  --lang {lang_code}
```

若 TTS 失败，继续返回纯文本结果，并说明语音不可用。

## API 请求模板

API 地址固定为：

```text
https://api.senseaudio.cn/v1/t2a_v2
```

重要：先按最小请求体调用官方接口，不要一开始就附带全部可选字段。若接口返回 `400 input content type is not supported`，优先怀疑请求体结构与官方当前协议不一致，而不是继续切换音色。

## 语音生成

使用 `helper.py synthesize` 发送 TTS 请求并把 `hex` 音频保存到本地。

`helper.py` 内置以下健壮机制（参考 VoiceMaster 模式）：

1. **文本变体**：自动对输入文本生成多种规范化变体（去角色前缀、标点规范化、去特殊标点、纯文本等），依次尝试直到成功。
2. **请求体变体**：对每种文本变体，依次尝试 full → no-audio-setting → no-speed-pitch → minimal 四种请求体。
3. **自动重试**：对 5xx 及网络错误自动重试最多 3 次，带指数退避。
4. **音色降级**：若 `403 no access to the specified voice`，自动回退到 `child_0001_b` / `male_0004_a` / `male_0018_a`。
5. **调试日志**：仅在显式传入 `--debug-log` 参数时才生成 `.debug.json`，默认不写入任何日志文件。

### 方式一：直接文本播报（推荐）

```bash
python3 skills/language-helper/scripts/main.py speak \
  --text "{translated_text}" \
  --lang {lang_code} \
  --speed 1.0 \
  --pitch 0
```

`speak` 命令会自动：
1. 将文本写入临时文件
2. 调用 `helper.py synthesize` 生成音频
3. 使用系统播放器（macOS afplay / ffplay）播放

### 方式二：文件输入合成

```bash
python3 skills/language-helper/scripts/main.py synthesize \
  --text-file segment.txt \
  --voice-id male_0004_a \
  --speed 1.0 \
  --pitch 0 \
  --format wav \
  --sample-rate 24000 \
  --output outputs/reply.wav
```

### 方式三：多段合并

```bash
python3 skills/language-helper/scripts/main.py concat \
  --output outputs/final.wav \
  outputs/segment-01.wav outputs/segment-02.wav
```

## SenseAudio 响应处理

SenseAudio 非流式 TTS 的成功响应为 JSON，其中 `data.audio` 是 `hex` 编码的音频数据。处理规则如下：

1. 先检查 `base_resp.status_code` 是否为 `0`。
2. 若成功，读取 `data.audio` 并按十六进制解码为二进制音频文件。
3. 使用 `extra_info.audio_length`、`extra_info.audio_sample_rate` 作为结果回执。
4. 若 `data.audio` 为空或 `status_code` 非 `0`，直接返回 `base_resp.status_msg`。

响应结构参考：

```json
{
  "data": {
    "audio": "hex编码音频",
    "status": 2
  },
  "extra_info": {
    "audio_length": 3500,
    "audio_sample_rate": 44100
  },
  "base_resp": {
    "status_code": 0,
    "status_msg": "success"
  }
}
```

## 输出格式

### 默认模式

```
🗣 {翻译结果}（{发音}）

📝 语法解析
• {语法点1}
• {语法点2}

📖 重点词汇
| 单词 | 读音 | 词性 | 释义 |
|------|------|------|------|
| ... | ... | ... | ... |

💡 其他表达
• {替代表达}
```

### 简洁模式

```
🗣 {翻译结果}（{发音}）

📖 {词1}={含义} | {词2}={含义}
```

## 输出要求

- 翻译应自然、口语化
- 保留原句语气和语域
- 日语可附罗马音
- 韩语可附罗马字
- 说明语言默认跟随用户输入语言
- 不展示本地文件路径
- 若 TTS 失败，继续返回纯文本结果，并说明语音不可用
- 如果因为套餐权限限制降级到授权音色，明确写出降级原因与最终使用的 `voice_id`

## 运行要求

- 已配置 `.env`（含 `SENSEAUDIO_API_KEY`）
- 系统可用 `ffmpeg`
- 需要联网调用语音服务
- 飞书语音条需额外配置 `FEISHU_APP_ID`、`FEISHU_APP_SECRET`、`FEISHU_CHAT_ID`

## 限制

- 当前默认使用单一音色
- 专业或冷门表达可能不够完全地道
- 飞书语音条依赖机器人权限
