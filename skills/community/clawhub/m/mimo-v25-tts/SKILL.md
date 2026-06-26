---
name: mimo-v2-5-tts
description: "MiMo V2.5 TTS 语音合成。使用小米 MiMo V2.5 TTS 系列模型生成语音。当需要将文字转为语音、发送语音消息、朗读内容、或用户要求「说出来」「语音回复」时激活此 skill。支持预置音色、音色设计、音色克隆三种模式，支持自然语言控制、导演模式，支持语气、情绪、方言的风格标签控制，预置音色支持唱歌。"
license: MIT
metadata:
  version: 0.1.2
---

# MiMo V2.5 TTS 语音合成 / Speech Synthesis (中文/English)

> 使用小米 MiMo V2.5 TTS 系列模型生成语音。支持中英文、预置音色、音色设计、音色克隆、情绪风格、方言、唱歌。
> Generate speech using Xiaomi MiMo V2.5 TTS models. Supports Chinese/English, preset voices, voice design, voice cloning, emotion, dialect, and singing.

脚本目录 / Scripts path: `$SKILLS_PATH/mimo-v2-5-tts/scripts/`

> **`$SKILLS_PATH` 说明 / Note:** skills 目录路径，因部署环境而异 / Path varies by deployment environment.

## 模型选择 / Model Selection

V2.5 系列提供三种模型，根据使用场景选择：
The V2.5 series offers three models for different use cases:

| 模型 ID / Model ID | 用途 / Purpose | 音色来源 / Voice Source | 特殊能力 / Special |
|---|---|---|---|
| `mimo-v2.5-tts` | 预置音色语音合成 / Preset voice TTS | 内置精品音色 / Built-in high-quality | 支持唱歌 / Singing |
| `mimo-v2.5-tts-voicedesign` | 文本描述定制音色 / Voice design via text | 文本描述生成 / Text description | — |
| `mimo-v2.5-tts-voiceclone` | 音频样本复刻音色 / Voice cloning | 音频样本 / Audio sample | — |

**选择建议 / Recommendation:**

- 快速生成语音、唱歌 → `mimo-v2.5-tts`（预置音色 / preset voice）
- 需要独特音色 → `mimo-v2.5-tts-voicedesign`（文本生成 / text-to-voice）
- 模仿特定声音 → `mimo-v2.5-tts-voiceclone`（样本复刻 / sample cloning）

> **注意 / Note:** TTS 有随机性，同样输入效果可能不同，可以多生成几次挑选 / TTS has randomness — generate multiple times to pick the best result.

## 环境依赖 / Dependencies

| 环境变量 / Env Var | 说明 / Description | 必需 / Required |
|---|---|---|
| `MIMO_API_KEY` | MiMo API 密钥 / MiMo API key | 是 / Yes |

| 依赖 / Dependency | 说明 / Description | 必需 / Required |
|---|---|---|
| `python3` | 运行脚本 / Run scripts | 是 / Yes |
| `openai` | `pip install openai` | 是 / Yes |
| `ffmpeg` | 格式转换、长文本拼接 / Format conversion, long text concat | 仅拼接 / Concat only |
| `curl` | 飞书 API 调用 / Feishu API calls | 仅飞书 / Feishu only |

## 预置音色 / Preset Voices

使用 `mimo-v2.5-tts` 模型时必须明确指定音色。
Must specify a voice when using the `mimo-v2.5-tts` model.

| 音色名 / Name | Voice ID | 语言 / Lang | 性别 / Gender | 风格 / Style |
|---|---|---|---|---|
| 冰糖 | `冰糖` | 中文 / Chinese | 女性 / Female | 活泼少女 / Lively girl |
| 茉莉 | `茉莉` | 中文 / Chinese | 女性 / Female | 知性女声 / Elegant woman |
| 苏打 | `苏打` | 中文 / Chinese | 男性 / Male | 阳光少年 / Sunny youth |
| 白桦 | `白桦` | 中文 / Chinese | 男性 / Male | 成熟男声 / Mature man |
| Mia | `Mia` | English | Female | Lively girl |
| Chloe | `Chloe` | English | Female | Sweet Dreamy |
| Milo | `Milo` | English | Male | Sunny boy |
| Dean | `Dean` | English | Male | Steady Gentle |

## 自然语言控制 / Natural Language Control

所有模型都支持自然语言控制。
All models support natural language style control.

通过自然语言描述调整语气、情绪等风格。所有模型均可通过 `--context` 参数传入指令：
Use natural language to control tone, emotion, etc. Pass via `--context` parameter:
- `mimo-v2.5-tts` / `mimo-v2.5-tts-voiceclone`: 调整指定音色下的风格 / Adjust style within a voice
- `mimo-v2.5-tts-voicedesign`: 同时控制音色和风格 / Control both voice and style

**能力特点 / Capabilities:**

- **多风格切换 / Multi-style switching**: 同一段语音内完成播报→低语→嘶吼 / switch between announcement, whisper, and roar
- **多情绪混合 / Mixed emotions**: "压抑的愤怒" suppressed anger、"带着哽咽的笑意" tearful smile
- **多粒度控制 / Multi-granularity**: 段落→句子→词→字 / paragraph → sentence → word → character

**示例 / Examples:**

```
用轻快上扬的语调向领导报喜，语速稍快，带着查到成绩后压抑不住的激动与小骄傲，声音明亮有活力。
Speak to your boss with a cheerful, upward tone, slightly fast, with barely contained excitement and pride.

看着刚解决的难题成果忍不住得意忘形地惊呼，声音高亢明亮，语速偏快，语气中带着满满的自信与难以置信。
Can't help but exclaim triumphantly at the solved problem — bright, high-pitched, confident, disbelieving.
```

### 导演模式 / Director Mode

自然语言控制的特殊用法「导演模式」：从角色、场景、指导三个维度刻画人物与声线。
A special form of natural language control — describe character, scene, and direction.

- **【角色 / Character】** 人物身份、性格底色 / Identity, personality traits, speaking habits
- **【场景 / Scene】** 此刻发生了什么 / What's happening, who they're talking to
- **【指导 / Direction】** 语速、气息、停顿、重音 / Speed, breath, pauses, emphasis, resonance

**示例 / Example:**

```
角色：百年门阀岑家的现任大当家。自出生便被过继给祖庙的守门老人抚养，被塑造成一尊完美无瑕、绝情断欲的家族图腾。
Character: The current head of the ancient Cen family clan. Raised by a temple keeper to become a flawless, emotionless family icon.

场景：在祠堂的阴影里引诱着那个不顾一切来找她的男人。她要用最冷硬的阶级壁垒，绞杀对方也绞杀自己刚刚萌芽的感情。
Scene: In the ancestral hall's shadows, tempting the man who came for her despite everything. She will use cold class barriers to kill both him and her budding feelings.

指导：冰冷、慵懒却极具威压的低音御姐。
Direction: Cold, lazy but oppressive low-toned voice.
```

## 音频标签控制 / Audio Tag Control

`mimo-v2.5-tts` 和 `mimo-v2.5-tts-voiceclone` 支持音频标签。在文本任意位置用括号描述语气/情绪/声音动作。
`mimo-v2.5-tts` and `mimo-v2.5-tts-voiceclone` support audio tags. Use brackets anywhere in text to describe tone/emotion/sound.

中文支持全角 `（）`、半角 `()`、方括号 `[]` / Chinese supports （） () []；英文支持 `()` `[]` / English supports () [].

```text
（紧张，深呼吸）呼……冷静，冷静。不就是一个面试吗……
Nervous, deep breath... Calm down. It's just an interview...

（极其疲惫，有气无力）师傅……到地方了叫我一声……
Exhausted, weak: Driver... wake me up when we arrive...

(heavy breathing) Just... give me... a second.
（喘着粗气）等...等我一下...
```

### 整体风格标签 / Global Style Tags

在文本开头添加 `(风格)` 标签指定整体风格。
Add a style tag at the beginning to set the overall style.

**唱歌 / Singing:** 必须 `(唱歌)歌词` / Must start with `(singing)lyrics`

| 类别 / Category | 常用风格 / Common Styles |
|---|---|
| **基础情绪 / Basic emotion** | `开心 happy` `悲伤 sad` `愤怒 angry` `恐惧 fearful` `惊讶 surprised` `兴奋 excited` `委屈 wronged` `平静 calm` `冷漠 cold` |
| **复合情绪 / Compound** | `怅然 wistful` `欣慰 relieved` `无奈 helpless` `愧疚 guilty` `释然 resigned` `动情 emotional` |
| **整体语调 / Tone** | `温柔 gentle` `高冷 aloof` `活泼 lively` `严肃 serious` `慵懒 lazy` `俏皮 playful` `深沉 deep` |
| **音色定位 / Voice** | `磁性 magnetic` `醇厚 mellow` `清亮 clear` `空灵 ethereal` `甜美 sweet` `沙哑 hoarse` |
| **人设腔调 / Character** | `夹子音 baby voice` `御姐音 mature woman` `正太音 boyish` `大叔音 uncle` `台湾腔 Taiwanese accent` |
| **方言 / Dialect** | `东北话 Dongbei` `四川话 Sichuan` `河南话 Henan` `粤语 Cantonese` |
| **唱歌 / Singing** | `唱歌` `sing` `singing` |

**经典组合 / Classic combos:**
`(怅然/wistful) 这么多年过去了...` `(慵懒/lazy) 再让我睡五分钟...` `(东北话/Dongbei) 哎呀妈呀...`

## 音色描述编写 / Voice Description Guide

当使用 `mimo-v2.5-tts-voicedesign` 进行文本描述定制音色时：
When using `mimo-v2.5-tts-voicedesign` to design a voice via text:

音色描述是嗓子的身份卡，只描写声音本身。
A voice description is the identity card of a voice — describe the voice itself, not the scene or action.

**必写项 / Required:**
1. **身份锚点 / Identity anchor**: 年龄段+性别 / Age + gender
2. **声音质感 / Voice quality**: 气息、共鸣、吐字 / Breath, resonance, articulation
3. **语速节奏 / Pace**: 稳/快/慢 / Steady/fast/slow
4. **情绪底色 / Emotional baseline**: 高亢/松弛/温软/克制 / Bright/relaxed/warm/restrained

**推荐 / Recommended:**
5. **风格标签 / Style tag**: 拍卖师/美食评论家/播音员 / Auctioneer/food critic/announcer
6. **辨识度小癖好 / Signature quirk**: 闭眼吸气/字尾颤音 / Eyes-closed inhale/trembling endings

**硬约束 / Rules:**
- 一到两句话，白描式 / 1-2 sentences, plain description
- 不写场景、动作 / No scenes or actions
- 不用真实演员或 IP 角色名 / No real actors or IP character names
- 默认普通话或英文 / Default Mandarin or English

**样例 / Examples:**
```
中年男性，节奏极快，情绪高亢，拍卖师风格。
Middle-aged male, very fast pace, excited tone, auctioneer style.

青年男性，电竞解说风格，语速极快且连贯。
Young male, esports commentator style, extremely fast and fluent.

中年男性，法庭陈词风格，声线沉稳偏正式。
Middle-aged male, courtroom speech style, steady and formal.
```

## 内容与标签增强 / Content & Tag Enhancement

当用户没有直接提供文本时，应自行编写；当只有文本没有情绪细节时，应插入合适的标签。
When the user doesn't provide text, write it yourself. When text has no emotion details, add appropriate tags.

**硬规则 / Hard rules:**
1. 文本情绪必须和音色契合 / Text emotion must match the voice
2. 长度 2-5 句 / 2-5 sentences, one paragraph
3. 标签是调味，不是主菜 / Tags are seasoning, not the main dish
4. 标点有表演意义 / Punctuation has performance meaning
5. 标签语言跟随正文 / Tag language follows the text language

**推荐标签（中文）/ Recommended Tags (Chinese):**
| 类别 / Category | 标签 / Tags |
|---|---|
| 节奏 / Pacing | `[停顿 pause]` `[长停顿 long pause]` `[急促 urgent]` `[语速加快 speed up]` |
| 情绪 / Emotion | `[轻声 whisper]` `[低语 murmur]` `[叹气 sigh]` `[哽咽 choked]` `[强调 emphasis]` `[笑 laugh]` |

**推荐标签（英文）/ Recommended Tags (English):**
| Category | Tags |
|---|---|
| Pacing | `[pause]` `[long pause]` `[fast]` `[drawn out]` |
| Emotion | `[whispering]` `[sighs]` `[inhale]` `[choked up]` `[emphasis]` `[laughs]` |

---

## Python 脚本用法 / Python Script Usage

| 脚本 / Script | 模型 / Model | 用途 / Purpose |
|---|---|---|
| `mimo_tts.py` | `mimo-v2.5-tts` | 预置音色语音合成 / Preset voice TTS |
| `mimo_tts_voicedesign.py` | `mimo-v2.5-tts-voicedesign` | 文本描述定制音色 / Voice design via text |
| `mimo_tts_voiceclone.py` | `mimo-v2.5-tts-voiceclone` | 音频样本复刻音色 / Voice cloning |

### 预置音色 / Preset Voice TTS (mimo_tts.py)

```bash
python3 mimo_tts.py --text "你好，今天天气真不错。" --voice "冰糖"

python3 mimo_tts.py --context "用温柔的语气，语速稍慢" --text "没关系，慢慢来，我等你。" --voice "冰糖" --output comfort.wav

python3 mimo_tts.py --text "（紧张，深呼吸）呼……冷静，冷静。" --voice "冰糖" --output interview.wav

python3 mimo_tts.py --text "(唱歌)原谅我这一生不羁放纵爱自由" --voice "冰糖" --output singing.wav

python3 mimo_tts.py --text "I just... (sighs deeply) I don't know anymore." --voice "Mia" --output english.wav
```

### 音色设计 / Voice Design (mimo_tts_voicedesign.py)

```bash
python3 mimo_tts_voicedesign.py --context "Give me a young male tone." --text "Yes, I had a sandwich."
```

### 音色克隆 / Voice Cloning (mimo_tts_voiceclone.py)

```bash
python3 mimo_tts_voiceclone.py --voice-file voice.mp3 --text "Yes, I had a sandwich." --output clone.wav

python3 mimo_tts_voiceclone.py --voice-file voice.mp3 --context "用温柔的语气" --text "没关系" --output directed.wav
```

### 长文本处理 / Long Text Handling

V2.5 常规场景无需分段，仅超过 **2500 字**才需分段拼接。
No need to split for most cases. Only split when exceeding **2500 characters**.

```bash
# 拼接方案 / Concatenation:
echo "file 'part1.wav'" > list.txt && echo "file 'part2.wav'" >> list.txt
ffmpeg -y -f concat -safe 0 -i list.txt -c copy combined.wav
```

---

## 飞书语音消息发送 / Feishu Voice Message

> 仅当需要将 TTS 语音发送到飞书时才用 / Only use when sending TTS audio to Feishu.

### 环境依赖 / Dependencies

| 环境变量 / Env Var | 来源 / Source | 说明 / Description |
|---|---|---|
| `FEISHU_APP_ID` | 飞书开放平台 / Feishu Open Platform | 应用 App ID |
| `FEISHU_APP_SECRET` | 飞书开放平台 / Feishu Open Platform | 应用 App Secret |

| 依赖 / Dep | 说明 / Description | 必需 / Required |
|---|---|---|
| `ffmpeg` | WAV 转 Opus + 获取音频时长 / Convert WAV to Opus + get duration | 是 / Yes |
| `curl` | 调用飞书 API / Call Feishu API | 是 / Yes |

### 私聊发送 / Private Chat (open_id)

```bash
python3 $SKILLS_PATH/mimo-v2-5-tts/scripts/mimo_tts.py --text "好的" --voice "冰糖" --output /tmp/voice.wav
bash $SKILLS_PATH/mimo-v2-5-tts/scripts/feishu_send_audio.sh /tmp/voice.wav open_id ou_xxxxxx
```

### 群聊发送 / Group Chat (chat_id)

```bash
bash $SKILLS_PATH/mimo-v2-5-tts/scripts/feishu_send_audio.sh /tmp/voice.wav chat_id oc_xxxxxx
```

`feishu_send_audio.sh` 内部流程 / Internal flow: `wav → opus (ffmpeg)` → `获取 token` → `上传文件` → `发送 audio 消息`
