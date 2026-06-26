---
name: mimotts25-plus
description: 小米 MiMo TTS 2.5 Plus — 增强版语音合成。兼容官方接口，支持预置音色/声音设计/克隆/导演模式。
metadata:
  openclaw:
    requires:
      env:
        - MIMO_API_KEY
    primaryEnv: MIMO_API_KEY
    emoji: 🎙️
  compat:
    official: "XiaomiMiMo/MiMo-Skills"
    scripts:
      - mimo_tts.py
      - mimo_tts_voicedesign.py
      - mimo_tts_voiceclone.py
---

# MiMo TTS 2.5 Plus

> **核心原则：** 情感/语气指令放 `user` 消息（`--context`），要念的文字放 `assistant` 消息（`--text`）。指令越具体越有画面感，声音越自然。

## 铁律：--context 永远不留空

没有情感指令 = 机器人朗读。哪怕用户只说"念一句你好"，也必须推断情感写进 `--context`。

**推断方法：** 想象真人在什么场景说这句话，用画面感描述（情绪底色 + 语速节奏 + 声音质感，至少两项）：
- "说早上好" → `--context "刚睡醒的慵懒带元气，语速偏慢，声音柔和温暖"`
- "念：对不起" → `--context "真诚道歉，声音低沉柔和，语速放慢，尾音下沉"`
- 长文本（超2句）→ 描述段落内的情绪变化走向

**文本增强：** 在 `--text` 合适位置插入音频标签（每2-3句一个，不过度）：
`对不起，我来晚了` → `（歉意）对不起……[轻叹]我来晚了`

**完整示例：**
```bash
python3 scripts/mimo_tts.py \
  --text "（温柔）晚安……[轻声]今天辛苦了，好好休息。" \
  --voice "冰糖" \
  --context "深夜安慰，像在耳边轻声说话，语速很慢，声音轻柔绵软，带一丝让人安心的倦意"
```

## 环境变量

| 变量 | 说明 | 必需 |
|---|---|---|
| `MIMO_API_KEY` | API 密钥 | 是 |
| `MIMO_API_BASE` | API 端点（默认 `https://token-plan-cn.xiaomimimo.com/v1`） | 可选 |
| `MIMO_OUTPUT` | 默认输出路径 | 可选 |

已知集群：中国 `https://token-plan-cn.xiaomimimo.com/v1`（默认）、公网 `https://api.xiaomimimo.com/v1`、海外以官方公布为准。可通过环境变量或 `tts.py --base-url` 切换。

## 模型与脚本

| 模型 | 脚本 | 用途 |
|---|---|---|
| `mimo-v2.5-tts` | `mimo_tts.py` | 预置音色（支持唱歌） |
| `mimo-v2.5-tts-voicedesign` | `mimo_tts_voicedesign.py` | 文本描述定制音色 |
| `mimo-v2.5-tts-voiceclone` | `mimo_tts_voiceclone.py` | 音频样本复刻音色 |
| 统一入口 | `tts.py` | 增强快捷模式（`--design` / `--clone` / `--base-url`） |

选择：描述音色形象→voicedesign，给音频文件→voiceclone，其他→预置音色，复杂角色→导演模式。

### 用法

```bash
# 预置音色
python3 scripts/mimo_tts.py --text "你好" --voice "冰糖" --context "温柔，语速稍慢"
# 声音设计
python3 scripts/mimo_tts_voicedesign.py --context "青年女性，活泼元气" --text "你好呀！"
# 声音克隆
python3 scripts/mimo_tts_voiceclone.py --voice-file sample.mp3 --text "你好"
# 统一入口
python3 scripts/tts.py "你好" -v 冰糖
python3 scripts/tts.py "你好呀" --design "22岁女性，声音甜美"
python3 scripts/tts.py "你好" --clone sample.mp3
python3 scripts/tts.py "你终于来了" --user-msg "角色：22岁活泼少女..."
```

## 预置音色

| Voice ID | 语言/性别 | 风格 |
|---|---|---|
| `冰糖`（默认） | 中文女 | 活泼少女 |
| `茉莉` | 中文女 | 知性女声 |
| `苏打` | 中文男 | 阳光少年 |
| `白桦` | 中文男 | 成熟男声 |
| `Mia` | EN Female | Lively |
| `Chloe` | EN Female | Sweet Dreamy |
| `Milo` | EN Male | Sunny |
| `Dean` | EN Male | Steady Gentle |

## 音频标签（放在 --text 中）

**整体风格**（文本开头 `(风格)`）：`开心` `悲伤` `愤怒` `温柔` `慵懒` `磁性` `高冷` `活泼` `东北话` `粤语` `唱歌` `夹子音` `御姐音` `正太音`

**行内标签** `[标签]`：`[停顿]` `[长停顿]` `[语速加快]` `[语速放缓]` `[轻声]` `[低语]` `[叹气]` `[深呼吸]` `[哽咽]` `[笑]` `[大笑]` `[抽泣]` `[颤抖]` `[气声]` `[激动]` `[疲惫]` `[撒娇]`

示例：`（紧张）呼……冷静。[深呼吸]不就是面试吗……[语速加快]自我介绍背了五十遍了。`

## 导演模式（高级）

在 `--context` 中写角色、场景、指导三要素，用于复杂情感/角色配音：
- **角色**：身份、性格、说话习惯
- **场景**：发生了什么、和谁说话、情绪位置
- **指导**：语速、气息、停顿、重音、音色质感、情绪起伏

## 音色描述（Voicedesign）

`--context` 必写四维度：性别+年龄、声音质感、情绪底色、语速节奏。可选：角色人设、说话风格、场景。1-4句即可。
注意：避免矛盾特征、音质效果词（混响/EQ）、模糊词（普通的/正常的）。合成文本要贴合音色。

## 交付

生成后：`MEDIA:output.mp3`

## 配置

1. 获取密钥：[小米 MiMo 开放平台](https://platform.xiaomimimo.com/)
2. `export MIMO_API_KEY=your-key` 或 `openclaw config set skills.entries.mimotts25-plus.apiKey "your-key"`
