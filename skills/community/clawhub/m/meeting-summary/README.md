# Meeting Summary Skill 🎙️

把会议录音变成**可读、可交付、可复跑**的结构化会议纪要。

> 录音 → 转写 → 说话人分割 → 声纹匹配 → 结构化纪要  
> 为真实工作场景设计，不是只在 demo 里好看。

[![Built for OpenClaw](https://img.shields.io/badge/Built%20for-OpenClaw-blue)](https://github.com/openclaw/openclaw)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](#license)
[![Version](https://img.shields.io/badge/version-2.3.0-orange)](#)

---

## 目录

- [这个 Skill 解决什么问题](#这个-skill-解决什么问题)
- [适合谁 / 不适合谁](#适合谁--不适合谁)
- [核心能力](#核心能力)
- [核心设计思路](#核心设计思路)
- [架构](#架构)
- [效果示例](#效果示例)
- [快速开始](#快速开始)
- [常见用法](#常见用法)
- [声纹管理](#声纹管理)
- [输出格式](#输出格式)
- [缓存机制](#缓存机制)
- [实战踩坑记录](#实战踩坑记录)
- [推荐工作流](#推荐工作流)
- [目录结构](#目录结构)
- [安装与配置](#安装与配置)
- [在 OpenClaw 中使用](#在-openclaw-中使用)
- [常见问题 FAQ](#常见问题-faq)
- [设计哲学](#设计哲学)
- [参与贡献](#参与贡献)
- [License](#license)

---

## 这个 Skill 解决什么问题

现实里的会议录音，通常比想象中脏得多：

- 一场录音 30~60 分钟，甚至更长
- 多人轮流发言、打断、插话
- ASR 能转出文字，但**不一定知道是谁在说**
- pyannote 这类重模型效果更好，但 **CPU 跑整场会慢得离谱**
- 业务上真正需要的，不是"绝对完美"，而是**先拿到可用纪要**

这个 skill 就是为这个矛盾设计的：先稳定出结果，再逐步补精度，支持缓存和增量处理，不用每改一次名字就全量重跑。

一句话概括：

> 这不是"传音频 → 吐一段摘要"的玩具脚本，而是一条能在真实工作流里活下来的会议纪要 pipeline。

---

## 适合谁 / 不适合谁

### ✅ 适合

- **固定团队的周会 / 例会**：可以提前注册声纹，后续每次会议自动匹配说话人
- **一对一访谈 / 用户调研**：两人对话场景，说话人分割效果最好
- **内部讨论会 / 头脑风暴**：多人但轮流发言为主，能有效识别
- **需要先快速交付、再逐步完善的场景**：快速模式是一等公民
- **CPU 机器 / 没有 GPU 的环境**：chunk 化 + 缓存设计就是为 CPU 准备的

### ❌ 不太适合

- **极度嘈杂的环境**：工地、户外、背景音乐很大——ASR 和 diarization 都会受影响
- **大量重叠发言**：5 人以上同时说话、互相打断很严重——pyannote 在这种场景下准确率会显著下降
- **极低音质录音**：电话录音、压缩到 16kbps 以下的音频——转写质量本身就受限
- **需要实时字幕**：这是一个离线处理 pipeline，不是实时转写工具

---

## 核心能力

### 1) Step ASR 转写
使用阶跃星辰（StepFun）的 **`step-asr`** 模型做全文转写，走稳定的文件上传接口，支持缓存。LLM 环节（估人数 + 生成纪要）默认使用 **`step-3.5-flash`** 模型。

> **API Key 申请地址**：https://platform.stepfun.com/interface-key  
> 注册账号后创建 API Key 即可使用。

### 2) 选择性说话人分割
用 pyannote 做说话人分割，但不是整场盲跑，而是按 chunk 选择性处理——只在高价值片段上投入重计算。

### 3) 声纹匹配 / 实名识别
支持给常见参会人注册声纹，把 `Speaker_A/B/C` 映射成真实姓名。适合固定团队、固定会议参与者场景。

> **本地模型说明**：声纹匹配用的 wespeaker 模型和 pyannote 说话人分割模型都需要从 [Hugging Face](https://huggingface.co/) 下载。请先注册 Hugging Face 账号，接受相关模型的使用协议后再下载。详见 [安装指南](references/setup-guide.md)。

### 4) 快速模式
用 `--max-new-chunks` 只跑最关键的新增 chunk，先出一版可用纪要。

### 5) 双层缓存
ASR 缓存 + diarization chunk 缓存。改 speaker map、改纪要格式时不用全量重跑。

### 6) 结构化输出
输出不仅是一篇 markdown，还包含完整 JSON，方便二次处理：结论、决策、行动项、风险、待确认事项、说话人校对视图。

---

## 核心设计思路

这套 skill 的核心不是"把模型堆得更猛"，而是一个朴素的原则：

> **先交付可用结果，再逐步提高精度。**

所以它刻意做了这些事：

- 不整场跑最重的流程，而是 **chunk 化**
- 不按时间顺序傻跑，而是 **按信息量优先级跑**
- 不要求 speaker 100% 准确后再出纪要，而是 **先交付**
- 不因为改人名/改格式就重做全部工作，而是 **靠缓存复用前序结果**

如果你受不了那种"理论上很强，但一小时都出不了结果"的方案，这个设计思路应该很对胃口。

---

## 架构

```text
音频文件
  ↓
ffmpeg 预处理（16kHz / 单声道 / WAV）
  ↓
Step ASR 全文转写（命中缓存则跳过）
  ↓
LLM 估计说话人数
  ↓
切 chunk + 计算信息密度
  ↓
对高价值 chunk 跑 pyannote 说话人分割（命中缓存则跳过）
  ↓
声纹匹配 / speaker-map 映射
  ↓
LLM 生成结构化纪要
  ↓
输出 JSON + Markdown
```

---

## 效果示例

以下是一个虚构的 3 人产品讨论会场景，展示输出的 `summary_markdown` 片段：

```markdown
# 产品方案讨论会 — 会议纪要

**日期**：2026-03-15  
**时长**：约 28 分钟  
**参会人**：张明（产品）、李薇（设计）、王磊（开发）

## 核心结论

1. 首页改版方案确定采用 B 方案（卡片式布局），预计下周三出设计稿
2. 搜索功能优先级从 P2 提升至 P1，原因是用户反馈集中
3. 后端接口需要在 3/20 前完成，前端跟进联调

## 决策

| 议题 | 决策 | 负责人 |
|------|------|--------|
| 首页布局 | 采用 B 方案 | 李薇 |
| 搜索优先级 | 提升至 P1 | 王磊 |
| 设计稿交付 | 下周三 | 李薇 |

## 行动项

- [ ] 李薇：周三前交付首页 B 方案设计稿
- [ ] 王磊：3/20 前完成搜索接口
- [ ] 张明：整理用户反馈原始数据，周五前同步给团队

## 风险

- 后端人力紧张，接口可能延期
- B 方案对低端机型的性能影响待验证

## 待确认

- 是否需要额外的用户测试？张明待确认预算
```

> 以上内容为虚构示例。实际输出取决于录音内容和说话人识别精度。

---

## 快速开始

### 1) 安装最小依赖

```bash
pip3 install numpy scipy soundfile onnxruntime
```

### 2) 配置 StepFun API Key

前往 https://platform.stepfun.com/interface-key 注册并创建 API Key，然后：

```bash
echo "your-stepfun-api-key" > ~/.stepfun_api_key
chmod 600 ~/.stepfun_api_key
```

### 3) 运行完整 pipeline

```bash
python3 scripts/meeting-summarize.py \
  --audio recording.m4a \
  --out /tmp/meeting-summary.json \
  --minutes-out /tmp/meeting-summary.md
```

### 4) 查看结果

- `/tmp/meeting-summary.json` — 结构化输出，方便下游处理
- `/tmp/meeting-summary.md` — 可直接阅读或发送的会议纪要

---

## 常见用法

### 完整会议总结

```bash
python3 scripts/meeting-summarize.py \
  --audio /path/to/meeting.m4a \
  --out /tmp/summary.json \
  --minutes-out /tmp/summary.md
```

### 指定说话人数

已知参会人数时，直接传入往往比让模型猜更稳。

```bash
python3 scripts/meeting-summarize.py \
  --audio /path/to/meeting.m4a \
  --num-speakers 4 \
  --out /tmp/summary.json \
  --minutes-out /tmp/summary.md
```

### 指定 speaker map

把占位名映射成真实姓名。

```bash
python3 scripts/meeting-summarize.py \
  --audio /path/to/meeting.m4a \
  --speaker-map /tmp/speaker-map.json \
  --out /tmp/summary.json \
  --minutes-out /tmp/summary.md
```

`speaker-map.json` 示例：

```json
{
  "Speaker_A": "张明",
  "Speaker_B": "李薇",
  "Speaker_C": "王磊"
}
```

### 快速模式：先出结果，再补精度

```bash
python3 scripts/meeting-summarize.py \
  --audio /path/to/meeting.m4a \
  --max-new-chunks 2 \
  --out /tmp/summary.json \
  --minutes-out /tmp/summary.md
```

适用场景：
- 录音较长
- pyannote 在你的机器上明显偏慢
- 你需要先拿到一版可用纪要

### 仅转写（不做 diarization 和总结）

```bash
python3 scripts/meeting-summarize.py \
  --audio /path/to/meeting.m4a \
  --transcript-only
```

### 参考历史纪要做风格对齐

```bash
python3 scripts/meeting-summarize.py \
  --audio /path/to/meeting.m4a \
  --reference /path/to/older-summary.md \
  --out /tmp/summary.json
```

---

## 声纹管理

### 注册声纹

建议使用 **3~10 秒、清晰、单人、少噪音** 的语音样本。

```bash
python3 scripts/voiceprint-manager.py enroll \
  --name "张明" \
  --audio /path/to/voice.wav
```

### 识别一段音频是谁

```bash
python3 scripts/voiceprint-manager.py identify \
  --audio /path/to/audio.wav \
  --json
```

### 查看已注册声纹

```bash
python3 scripts/voiceprint-manager.py list
```

### 删除声纹

```bash
python3 scripts/voiceprint-manager.py delete --name "张明"
```

---

## 输出格式

完整结果保存在 JSON 中，核心字段如下：

| 字段 | 说明 |
|------|------|
| `audio_file` | 输入音频路径 |
| `speakers` | 说话人列表（姓名、来源、片段数、置信度） |
| `segments` | 带时间戳和说话人的文本片段 |
| `full_text` / `transcript` | 完整转写文本 |
| `summary` | 结构化摘要对象（结论 / 决策 / 行动项 / 风险） |
| `summary_markdown` | 可直接阅读或发送的 markdown 纪要 |
| `open_questions` | 待确认事项 |
| `confidence_flags` | 低置信度提醒 |
| `speaker_review` | 说话人映射校对视图 |
| `speaker_count_estimate` | 估计说话人数 |
| `diarization_meta` | chunk 计划、优先级、命中情况 |

---

## 缓存机制

缓存目录：`cache/meeting-summary/`

### ASR 缓存

```text
<音频哈希>--asr--<语言>.json
```

同一音频不会重复转写。

### Chunk diarization 缓存

```text
<音频哈希>--chunk-diarization--<说话人数>--<chunk序号>--<起始>--<结束>--<模式>.json
```

核心价值：
- 只补跑缺失的 chunk，不重复计算
- 改 speaker map 时不需要重跑 ASR
- 改纪要格式时不需要重跑 diarization
- 增量处理，而不是每次从头来

---

## 实战踩坑记录

这部分是这个 skill 最值钱的地方——都是真实场景里趟出来的。

### 1. 长录音不是"传上去就行"

长录音意味着上传链路更脆弱、转写更慢、重试成本更高。大文件必要时先压缩或分段，不要硬怼一条链路到死。

### 2. pyannote 在 CPU 上是真的慢

不是"有点慢"，是 30 分钟录音可能需要 60 分钟以上的慢。chunk 化、selective diarization、快速模式是应对方案，不是可选优化。

### 3. 说话人数估计会错

LLM 估人数会错，而且可能错得离谱。实战里出现过模型估 2 人、实际 4 人的情况。已知人数就手动传，不已知时也别盲信。

### 4. Unknown 是正常现象

没有注册声纹、录音太短或太吵时，`Unknown` 占比高很正常。这不是 bug，是音频现实。

### 5. "先交付再完善"比"等完美再交付"更对

会议纪要最大的风险不是"不够完美"，而是"来不及用"。先出 80% 质量的纪要，再逐步补 speaker 和 chunk，这是这个 skill 的默认策略。

---

## 推荐工作流

### 场景 A：需要尽快拿到纪要

1. 快速模式 `--max-new-chunks 2`
2. 看 `summary_markdown`
3. 先发出去
4. 需要更高精度时再补跑

### 场景 B：固定团队周会

1. 提前给常见参会人注册声纹
2. 已知人数时传 `--num-speakers`
3. 首次跑完后校正 `speaker-map`
4. 后续会议复用同一套声纹库

### 场景 C：长录音 / CPU 机器

1. 不要追求整场 diarization
2. 先转写
3. 再 selective diarization
4. 只补高价值 chunk

---

## 目录结构

```text
meeting-summary/
├── README.md                    ← 你正在读的文件
├── SKILL.md                     ← OpenClaw agent 调用规范
├── scripts/
│   ├── meeting-summarize.py     ← 主编排脚本
│   ├── pyannote-diarize.py      ← pyannote 说话人分割包装
│   ├── transcribe.py            ← Step ASR 转写
│   └── voiceprint-manager.py    ← 声纹注册 / 识别 / 管理
└── references/
    └── setup-guide.md           ← 完整安装指南
```

---

## 安装与配置

完整安装说明请看 [references/setup-guide.md](references/setup-guide.md)，包含：

- ffmpeg 安装
- StepFun API Key 配置
- wespeaker 声纹模型下载（需 [Hugging Face](https://huggingface.co/) 账号）
- pyannote 独立虚拟环境配置（需 Hugging Face 账号 + 接受模型使用协议）
- Hugging Face 注册与模型协议接受
- 环境变量参考
- 故障排查

---

## 在 OpenClaw 中使用

安装：

```bash
clawhub install meeting-summary
```

也可以从以下平台获取：

- **ClawHub**：`clawhub install meeting-summary`
- **GitHub**：[github.com/Jack-Yang-ai/meeting-summary-skill](https://github.com/Jack-Yang-ai/meeting-summary-skill)
- **OpenClawMP**：[openclawmp.cc/asset/s-a7ea7f3e07f1ffda](https://openclawmp.cc/asset/s-a7ea7f3e07f1ffda)

---

## 常见问题 FAQ

### Q：为什么输出里有很多 Unknown？

声纹匹配需要提前注册参会人的声纹样本。如果没有注册，或者录音中说话人的片段太短、噪音太大，就会被标记为 Unknown。这是正常行为。

**解决办法**：为常见参会人注册 3~10 秒的清晰声纹样本。

### Q：为什么 pyannote 跑了很久还没出结果？

pyannote 在纯 CPU 环境下确实很慢，30 分钟录音可能需要 60 分钟以上。

**解决办法**：
- 使用 `--max-new-chunks 2` 快速模式
- 利用缓存，不要重复跑已经处理过的 chunk
- 如果有 GPU 或 Apple Silicon MPS，PyTorch 会自动加速

### Q：为什么说话人数估计不准？

LLM 估人数基于转写文本推断，在口语化、多人频繁插话的场景容易低估。

**解决办法**：如果你已知参会人数，直接传 `--num-speakers`，效果更稳定。

### Q：长录音怎么处理？

不要默认整场硬跑。推荐策略：
1. 先用快速模式出一版纪要
2. 如果需要更高精度，再补跑更多 chunk
3. 改人名 / 改格式时利用缓存，不需要重头来

### Q：支持哪些音频格式？

ffmpeg 能处理的格式都支持：mp3、wav、ogg、opus、m4a、flac、aac 等。脚本会自动预处理为 16kHz 单声道 WAV。

### Q：可以不装 pyannote 吗？

可以。pyannote 是可选依赖。不装的情况下，skill 会使用轻量 fallback 方案做说话人分割，精度会降低但仍然可用。

### Q：本地模型从哪里下载？

声纹匹配模型（wespeaker）和说话人分割模型（pyannote）都托管在 [Hugging Face](https://huggingface.co/)。你需要：

1. 注册一个 Hugging Face 账号
2. 对 pyannote 模型，需要在模型页面接受使用协议
3. 按照 [安装指南](references/setup-guide.md) 的步骤下载到本地

---

## 设计哲学

这套 skill 追求的不是"最炫"，而是三件很现实的事：

1. **能跑通** — 先稳定产出结果
2. **能迭代** — 缓存、补跑、改名不重来
3. **能交付** — 先给业务可用结果，再补精度

这才是一个真的能用在工作流里的会议总结系统。

---

## 参与贡献

欢迎提交 Issue 和 Pull Request。

- 🐛 **Bug 反馈**：请附上音频格式、时长、错误日志
- 💡 **功能建议**：描述使用场景和预期效果
- 🔧 **代码贡献**：请先开 Issue 讨论方案

仓库地址：[github.com/Jack-Yang-ai/meeting-summary-skill](https://github.com/Jack-Yang-ai/meeting-summary-skill)

---

## License

MIT
