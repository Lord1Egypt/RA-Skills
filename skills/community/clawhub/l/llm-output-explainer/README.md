# llm-output-explainer

**Turn complex LLM/technical output into audience-fit explanations — 5 mechanism modules, one routing skill.**

[English](#english) · [中文](#中文)

---

<a id="english"></a>
## English

An [OpenClaw](https://github.com/openclaw/openclaw) skill that turns "explain this to someone" from a vibe exercise into an engineering pipeline. Before any artifact is generated, the skill forces an **audience-four-questions** pass (who are they / what biases do they hold / what do we already agree on / what should they do), picks a delivery mechanism from a decision matrix, then decomposes the content into four layers — one-sentence → three-sentence → sectioned → support layer.

### The five modules

| Module | Mechanism | When |
|---|---|---|
| A | Controlled writing (STE100-style) | Broad audience / translation / safety docs |
| B | Diagram-first (speaker-view graphics) | Technical content to non-experts |
| C | Self-contained single-file HTML | Decisions / exec briefings / anyone who forwards |
| D | Narrated video (Manim + edge-tts) | Oral briefing / social / boardroom screens |
| E | Disposable tool artifact | "What does this money/risk look like" challenges |

Module D is **script-first by law**: narration is written and confirmed before a single frame renders; scene durations are derived from actual TTS audio lengths, so A/V never drifts.

### Install

```bash
# OpenClaw
cp -r llm-output-explainer ~/.openclaw/workspace/skills/
# or clone straight into your skills dir
```

Module D requirements (video): `manim`, `edge-tts`, `ffmpeg`, a CJK font. Run the bundled check:

```bash
python3 scripts/env_check.py
```

### Use

Trigger phrases: *"把 X 讲给 Y 听"*, *"make this explainer"*, *"STE100"*, *"讲解视频"*. The skill self-routes; plain "summarize this" requests do **not** trigger it.

### Credits & inspirations

- Methodology riff on Andrej Karpathy's LLM-output explainer video pipeline (script-first, visual-as-annotation), generalized into a five-module router.
- Module C's four-layer HTML structure owes a debt to [html-it](https://github.com/RoboNuggets/html-it).
- Module D stands on [3b1b/manim](https://github.com/3b1b/manim) and [edge-tts](https://github.com/rany2/edge-tts).
- Module A's controlled-language discipline follows Simplified Technical English (ASD-STE100) practice, with a Chinese counterpart list.

### License

MIT. See [LICENSE](LICENSE).

---

<a id="中文"></a>
## 中文

这是一个 [OpenClaw](https://github.com/openclaw/openclaw) skill：把"帮我把这个讲给人听"从玄学变成工程管线。生成任何工件之前，强制过**受众四问**（他是谁/带什么成见/已有共识/应做什么），用决策矩阵选定交付机制，再把内容拆成四层：一句话版 → 三句话版 → 分段版 → 支撑层。

### 五个模块

| 模块 | 机制 | 适用场景 |
|---|---|---|
| A | 受控写作（STE100 风格） | 大众受众/翻译/安全文档 |
| B | 图解优先（讲者视图） | 技术内容讲给非专家 |
| C | 单文件 HTML | 决策汇报/高管简报/会被转发的内容 |
| D | 配音视频（Manim + edge-tts） | 口头汇报/会议室投屏/社交媒体 |
| E | 一次性工具工件 | "这笔钱/这个风险是什么形状"的追问 |

模块 D **脚本先行是铁律**：旁白脚本先于画面写成并确认；场景时长由 TTS 配音的实际长度推导，音画零漂移。

### 安装与依赖

```bash
cp -r llm-output-explainer ~/.openclaw/workspace/skills/
python3 scripts/env_check.py   # 视频模块环境自检
```

视频模块依赖：`manim`、`edge-tts`、`ffmpeg`、CJK 字体（模块 D 内部脚本先行有完整降级路线：无声字幕版 → 纯场景 → 放弃动画退模块 B/C）。

### 使用

触发词："把 X 讲给 Y 听"、"做个讲解"、"STE100"、"讲解视频"。普通"总结一下"不会误触发。

### 致谢

方法论受 Andrej Karpathy 的 LLM 输出讲解视频流水线启发（脚本先行、画面为旁白做注），泛化为五模块路由器；模块 C 的四层 HTML 结构参考 [html-it](https://github.com/RoboNuggets/html-it)；模块 D 基于 [3b1b/manim](https://github.com/3b1b/manim) 与 [edge-tts](https://github.com/rany2/edge-tts)；模块 A 遵循简化技术英语（ASD-STE100）实践并配中文对应清单。

### 许可

MIT，见 [LICENSE](LICENSE)。
