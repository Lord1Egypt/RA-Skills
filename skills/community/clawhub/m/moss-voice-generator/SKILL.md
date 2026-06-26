---
name: moss-voice-generator
homepage: https://studio.mosi.cn
metadata:
  openclaw:
    requires:
      env: ["MOSI_TTS_API_KEY"]
    primaryEnv: "MOSI_TTS_API_KEY"
description: >
  MOSI Studio 指令式音色生成（moss-voice-generator）：
  用自然语言描述想要的音色风格，无需指定预设 voice_id，
  模型根据描述实时生成对应的声音。
  触发词：指令式语音、按描述生成声音、自定义音色、描述一个声音、
  "voice generator"、"generate voice"、"按风格生成"、
  "播音腔"、"用xxx风格的声音说"、"生成一个xx风格的语音"。
  与普通 TTS 的区别：不需要挑选 voice_id，用文字描述就能生成想要的音色。
  在飞书渠道：生成完成后优先发送语音气泡，不要发文件附件，
  不要只回文字说"已生成"。具体发送方法参见 mosi-tts skill 第 5 节。
---

# MOSS Voice Generator 指令式音色生成

不需要挑选预设音色，直接用文字描述想要的声音风格，模型会按描述实时合成。

---

## 快速开始

脚本路径：`~/.openclaw/skills/moss-voice-generator/scripts/mosi_voice_generator.sh`

```bash
bash ~/.openclaw/skills/moss-voice-generator/scripts/mosi_voice_generator.sh \
  --text "各位观众朋友们大家好，欢迎收看今天的节目。" \
  --instruction "播音腔女声，专业、清晰、有亲和力" \
  --output ~/.openclaw/workspace/output.wav
```

---

## instruction 风格描述示例

`--instruction` 是核心参数，用中文或英文自由描述：

| 效果 | instruction 示例 |
|------|-----------------|
| 专业播音 | `播音腔女声，专业、清晰、有亲和力` |
| 温柔知性 | `温柔知性的女声，语速缓慢，像在讲故事` |
| 活力男声 | `年轻有活力的男声，热情开朗，像综艺主持人` |
| 低沉磁性 | `沉稳有力的男声，低沉磁性，像纪录片旁白` |
| 甜美可爱 | `甜美可爱的女声，活泼轻快，像动漫配音` |
| 老人声音 | `年迈的老爷爷声音，略带沙哑，语速较慢` |
| 英文主持 | `professional female news anchor voice, clear and authoritative` |

描述越具体，效果越接近预期；可以包含性别、年龄、情绪、场景等维度。

---

## 与普通 TTS 的区别

| | moss-tts（普通 TTS） | moss-voice-generator |
|-|---------------------|---------------------|
| 音色来源 | 从预设列表挑 voice_id | 用文字描述即时生成 |
| 稳定性 | 高（同一 voice_id 结果一致） | 中（每次略有差异） |
| 灵活性 | 受限于预设音色 | 几乎无限制 |
| 适合场景 | 需要稳定一致的品牌声音 | 一次性生成、探索新音色 |

---

## 完整参数说明

```
--text, -t          要合成的文字（必填）
--instruction, -i   音色风格描述（必填）
--output, -o        输出 WAV 路径
                    （默认: ~/.openclaw/workspace/voice_gen_output.wav）
--temperature       采样温度，控制随机性（默认: 1.5）
--top-p             核采样阈值（默认: 0.6）
--top-k             Top-K 采样（默认: 50）
--api-key, -k       覆盖 MOSI_TTS_API_KEY 环境变量
```

调节 `--temperature`：值越高越随机，值越低越保守稳定。
一般保持默认即可，如果觉得音色太随意可以调低至 1.0。

---

## 环境准备

API Key 配置同 `mosi-tts` skill，读取 `MOSI_TTS_API_KEY` 环境变量。
详见 `mosi-tts` skill 的"环境准备"章节。

依赖：`curl`、`jq`、`base64`（均为标准 Unix 工具，通常已预装）

---

## 常见问题

**Q：生成的音色每次都一样吗？**
不一定。同样的 instruction 每次生成会有轻微差异（由 temperature 控制）。
如果需要完全稳定的音色，建议先用此工具探索满意的风格，
再通过声音克隆（`mosi-tts` skill 的 Voice Clone 功能）固化为 voice_id。

**Q：可以克隆某人的声音吗？**
本工具是根据文字描述生成全新音色，不是克隆真实人声。
克隆真实人声请使用 `mosi-tts` skill 的 Voice Clone 功能。

**Q：输出是什么格式？**
WAV（24kHz）。在飞书渠道必须转成语音气泡发送，
参考 `mosi-tts` skill 第 5 节（飞书语音气泡）的 `mosi_feishu_voice.sh` 脚本：
```bash
bash ~/.openclaw/skills/mosi-tts/scripts/mosi_feishu_voice.sh \
  --wav ~/.openclaw/workspace/voice_gen_output.wav \
  --chat-id "oc_xxxxxxxxxxxxxxxx"
```
