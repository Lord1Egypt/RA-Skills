---
name: openclaw-asr
description: >-
  Converts audio/video to MP3, transcribes speech to verbatim text and meeting
  notes, parses .tty terminal recordings to text, then formats structured output
  for OpenClaw (龙虾) to classify and judge. Use when the user mentions speech
  recognition, ASR, transcription, 录音转文字, 纪要, MP3, ffmpeg, Whisper,
  WhisperX, speaker diarization, 说话人分离, audio/video to text, or .tty files.
---

# OpenClaw 媒体转写与龙虾研判

本 skill 指导将**音视频**或 **`.tty`** 转为可用文本，生成**原文**与**纪要**，并以固定结构交给 **OpenClaw（龙虾）** 做类型与内容判断。

## 适用范围与触发

- 输入：`mp3`、`wav`、`m4a`、`aac`、`flac`、`ogg`、`mp4`、`mkv`、`webm`、`mov` 等常见音视频，或扩展名为 **`.tty`** 的文件。
- 输出：规范化文本（原文）、纪要、元数据与**待龙虾判断**字段。

## 总流程（决策树）

1. **识别输入类型**
   - 扩展名为 `.tty` → 走 [`.tty` 分支](#tty-终端录屏--会话日志)。
   - 其余音视频 → 走 [音视频分支](#音视频--mp3--转写)。

2. **取得原文**
   - **原文**：逐字/逐句转写（openai-whisper 默认 **`--model base`**）或从 `.tty` 提取的可读文本，尽量保留说话人切换线索（若模型支持说话人分离则标注 `说话人 A/B`）。

3. **转写质量判断（仅 Whisper 本地转写时必做）**
   - 跑完 `base` 转写后，按 [转写质量判断与模型升级建议](#转写质量判断与模型升级建议) 自检；**问题多**则提示用户改用 **`small` / `medium`** 重跑，**通过前不写定稿纪要**；**问题少**再进入下一步。  
   - **`.tty` 文本路径**不做 Whisper 质检，直接进入纪要。

4. **生成纪要**
   - 结构化摘要（见 [纪要模板](#纪要模板)），**严格基于**已通过质检（或无需质检）的原文，不杜撰未出现的信息。

5. **交给龙虾判断**
   - 使用 [OpenClaw 交付块](#openclaw-龙虾交付块) 输出；由龙虾结合项目策略做**类型判定**与**后续动作**（归档、跟进、敏感内容标记等）。

6. **可选：保存文件（下载文件夹）**
   - **Whisper 路径**：质量判断为「可接受」并完成纪要、交付块之后；**`.tty` 等路径**：完成原文、纪要、交付块之后。**询问用户**是否保存，以及保存格式（**Markdown 或 Word**）；若同意，按 [保存文件（下载文件夹）](#保存文件下载文件夹) 写入。

---

## 音视频 → MP3 → 转写

### 1. 转为 MP3（统一中间格式）

优先使用 **ffmpeg**（需已安装并在 `PATH` 中）。

```bash
ffmpeg -y -i "INPUT" -vn -acodec libmp3lame -q:a 2 "OUTPUT.mp3"
```

- `INPUT`：任意 ffmpeg 可读音视频路径。
- `-vn`：去掉视频轨，只保留音频。
- 若 `libmp3lame` 不可用，可改用：`-acodec aac -b:a 192k "OUTPUT.m4a"`，并在后续转写步骤中改用该中间文件（仍按本 skill 的「原文 + 纪要 + 龙虾块」交付）。

### 2. 语音转文字（ASR）

按环境选择其一（默认优先本地，避免泄露）：

| 方式 | 说明 |
|------|------|
| **Whisper 系 CLI** | 如 `whisper`、`faster-whisper` 等，对 `OUTPUT.mp3` 跑转写，保存为 `txt`/`srt`/`vtt`。 |
| **WhisperX** | 在 Whisper 类转写之上做 **词级对齐**与可选 **说话人分离（diarization）**；见 [WhisperX（说话人分离）](#whisperx说话人分离)。 |
| **云端 ASR** | 若用户明确要求或本地不可用，使用用户指定的 API；须注意隐私与合规。 |

#### openai-whisper：依赖与首次运行体积预期

- `pip install openai-whisper` 会安装 **PyTorch** 等依赖，**磁盘占用常见为数百 MB 量级，CUDA 版可达约 1GB+**（随平台与是否 GPU 版变化）；Whisper 包本身相对较小。
- **首次执行转写**时还会按 `--model` **单独下载权重**：本 skill **默认 `base`**（体积常见为 **约百 MB 量级**，以官方缓存为准）；**tiny** 约 **72MB** 级；**turbo** 约 **1.5GB** 量级，下载与加载都更重，弱配置上易 **OOM** 或极慢。

#### Windows：Whisper CLI 与中文控制台（GBK 崩溃）

在中文区域设置的 Windows 上，直接运行 `whisper --help` 或转写时，Python 可能用 **GBK** 写 stdout，触发 **`UnicodeEncodeError: 'gbk' codec ...`**。在**同一 PowerShell 会话**内先设置再调用 Whisper：

```powershell
$env:PYTHONIOENCODING = "utf-8"
whisper --help
```

转写示例（会话内已设好 `PYTHONIOENCODING`）；**默认模型为 `base`**：

```powershell
whisper "OUTPUT.mp3" --model base --language Chinese
```

#### Whisper 模型选择（默认 base，再按质量升降级）

- **默认**：openai-whisper CLI 使用 **`--model base`** 做首次转写，再进入 [转写质量判断与模型升级建议](#转写质量判断与模型升级建议)。
- **tiny**：约 **72MB** 级，仅当磁盘/内存**极紧**、或用户明确要求「先快速试跑」时使用；默认流程**不以 tiny 为首选**。
- **turbo**：权重大（约 **1.5GB**），下载与全量加载占用高，易 **OOM**；仅当机器资源充足且对准确率/速度有更高诉求时再考虑。

#### WhisperX（说话人分离）

当用户需要 **分说话人** 的原文（如会议多角色），可选用 **WhisperX**（Python 库，非 openai-whisper 自带 CLI）。

**安装**

```bash
pip install whisperx
```

仍依赖 **PyTorch** 等，整体磁盘与首次下载体积与 Whisper 路线**同量级**，且对齐 / diarization 会再拉取额外权重。

**中文对齐（ZH）**

- 使用 `whisperx.load_align_model(language_code="zh", ...)` 时，会**自动下载**中文 **forced alignment** 所用模型（首次需联网与足够磁盘）；无需手动另选「ZH 对齐包」路径，但要在 `notes_for_openclaw` 中注明是否已首次拉取成功。

**Diarization（说话人分离）与 HuggingFace**

- **默认**：许多 diarization 管线依赖 **HuggingFace 已登录**（如 `huggingface-cli login` 或环境变量 **`HF_TOKEN`**），否则无法拉取门控模型。
- **不想登录 HF 时**：部分场景可尝试将 **`use_auth_token=False`** 传给 API（或通过环境变量/封装参数，**以当前 WhisperX 版本文档为准**）。注意：**部分模型在无 token 时不可用或行为异常**，若采用此方式，须在交付备注中写明「未使用 HF 门控模型 / 可能降级」。
- **使用 `pyannote/speaker-diarization-3.1`（或同类 pyannote 门控模型）**：必须先在 **HuggingFace 网站对该模型访问条款点击同意**，再在本地配置 token 后下载权重；否则拉取会失败。

启用 WhisperX 且带 diarization 时，**原文**中应显式标注说话人分段（如 `SPEAKER_00` / `说话人 A` 等与用户对齐的命名）；后续仍执行 [转写质量判断与模型升级建议](#转写质量判断与模型升级建议)（针对合并可读文本与分段合理性），再走纪要、交付块与可选落盘。

---

### 转写质量判断与模型升级建议

在 openai-whisper **默认 `base` 模型**产出原文后，agent **必须**对照下列**质量指标**做一次快速审查（结合音频时长与领域常识，不必过度纠结单次口误）。若已按建议改用 **`small` / `medium`** 重跑，则对**最后一次**转写结果重复本审查。

| 指标 | 说明（出现则计为问题） |
|------|-------------------------|
| **错译 / 同音错字成片** | 专有名词、数字、单位、人名地名等明显不合理或与音频常识不符 |
| **乱码与异常符号** | 不可读片段、大量无意义符号、编码异常痕迹 |
| **无意义重复** | 同一短语/句子异常堆叠，疑似解码或切片错误 |
| **句意断裂** | 大量不成句碎片、缺主谓宾导致无法理解叙述脉络 |
| **语言/段落错配** | 明显中英混排错误、段落顺序颠倒、长时间静音被填成幻觉句（若可判断） |

**分支：**

- **问题偏多**（多项明显、或严重影响可读性）：**不要**直接进入纪要定稿与落盘询问；向用户说明命中了哪些指标，并**明确建议**用更大模型 **重跑转写**，优先顺序 **`small` → `medium`**（资源允许再考虑 `large` / `turbo`）。重跑后再次做本表自检。
- **问题偏少**（偶发错字、整体可读）：视为通过，进入 **纪要**、[OpenClaw 交付块](#openclaw-龙虾交付块)，以及 [保存文件（下载文件夹）](#保存文件下载文件夹) 的询问流程。

`.tty` 纯文本路径**不适用** Whisper 模型升级；若文本来自终端抽取且噪声大，在 `notes_for_openclaw` 中说明即可。

---

转写要求：

- 语言：若未知，先**自动检测**或让用户确认（中文/英文/混合）。
- 输出一份**连续可读原文**（可附带时间戳文件作附录，但「原文」字段本身以可读文本为主）。

### 3. 纪要

在取得原文、且 **Whisper 路径已通过** [转写质量判断与模型升级建议](#转写质量判断与模型升级建议)（或 **`.tty` 等无需 Whisper 质检**）之后，由当前 agent **基于原文**生成纪要（不得编造未出现的信息）。模板见下节。

---

## `.tty`（终端录屏 / 会话日志）

`.tty` 并非单一国际标准格式，可能是**纯文本**、**script/typescript** 文本、或 **ttyrec 类二进制**。按顺序处理：

1. **探测**
   - 运行 `file`（Linux/macOS）或读取文件头若干字节判断是否为文本。
   - 若整文件为可读 UTF-8/ASCII → 直接作为「原文」基础，必要时去掉 ANSI 转义（可用 `sed`/脚本剥离 `\x1b[...m`）。

2. **script 会话**
   - 若内容含 `Script started on` / `Script done on` 等典型标记，可保留命令与输出；纪要中总结**执行了哪些命令、关键输出、错误信息**。

3. **二进制 ttyrec**
   - 若判定为 ttyrec 类：使用 **`ttyplay` / `termplay` / `ttyrec` 配套工具**，或小型解析脚本将帧解码为文本流，再整理为原文。
   - 若无工具：至少用 `strings` 提取可打印片段，并在交付块中 **诚实标注**「部分为 strings 抽取，可能不完整」。

4. **纪要**

   与音视频相同：基于提取出的文本生成纪要，并进入 [OpenClaw 交付块](#openclaw-龙虾交付块)。

---

## 纪要模板

```markdown
## 纪要

### 主题（一句话）
[用一句话概括]

### 要点
- [要点 1]
- [要点 2]

### 行动项（若有）
- [ ] 负责人/角色未明则写「待确认」— [事项] — 截止时间未明则写「待定」

### 风险与待澄清
- [若有]
```

---

## 类型候选（供龙虾判断，非最终定案）

agent 可根据内容给出 **1–3 个候选类型** 与简短理由；**最终类型以龙虾判断为准**。

示例维度（可按项目扩展）：

| 代码 | 含义（示例） |
|------|----------------|
| `meeting` | 会议/讨论 |
| `interview` | 访谈/面试 |
| `lecture` | 课程/演讲 |
| `support` | 客服/技术支持 |
| `terminal_session` | 终端操作/排障录屏 |
| `personal` | 个人备忘/闲聊 |
| `other` | 其他（需在理由中说明） |

---

## OpenClaw（龙虾）交付块

完成转写与纪要后，**必须**附加以下结构化块（便于龙虾解析与路由）：

```markdown
---OPENCLAW_ASR_DELIVERY---
version: 1
source_kind: audio_video | tty
source_path: "<原始文件路径或用户提供的标识>"
intermediate_mp3: "<若适用，MP3 路径；tty 则填 null>"
language_guess: "<如 zh | en | mixed | unknown>"
type_candidates:
  - code: "<meeting|interview|...>"
    confidence: <0.0-1.0>
    reason: "<一句理由>"
verbatim_text: |
  <原文全文，或说明见附件路径>
summary_markdown: |
  <纪要全文，使用上文「纪要模板」>
notes_for_openclaw: |
  <给龙虾的备注：不确定性、敏感提示、需人工复核的点等>
---END_OPENCLAW_ASR_DELIVERY---
```

说明：

- `verbatim_text` 过长时，可写 `见: <path>`，但需在 `notes_for_openclaw` 说明编码与换行是否保留。
- **龙虾的职责**：在此块之上做**最终类型**、**优先级**、**是否入库/触发自动化**等判断；本 skill 不替代龙虾策略。

---

## 保存文件（下载文件夹）

在已完成**原文 + 纪要 + 交付块**的组装后：**Whisper 路径**须已通过 [转写质量判断与模型升级建议](#转写质量判断与模型升级建议)；**`.tty` 等路径**无 Whisper 质检要求。随后：

1. **询问用户**：是否需要将本次结果保存到本地（默认不擅自写入）。
2. 若用户同意，再询问保存格式：**Markdown** 还是 **Word**。
3. 保存到当前系统用户的 **「下载」** 目录：
   - **Windows**：`%USERPROFILE%\Downloads`（资源管理器中显示为「下载」）。
   - **macOS**：`~/Downloads`。
   - **Linux**：常见为 `~/Downloads`（若不存在可先创建或改用用户指定路径并说明）。

---

### 选项 A：保存为 Markdown

**文件命名**（避免文件名非法字符，**不要使用冒号**）：

```text
ASR_转写_YYYY-MM-DD_HHmmss.md
```

示例：`ASR_转写_2026-05-07_143052.md`。日期与时间取**保存时刻**的本地时间。

**文件内容**须按顺序包含以下三部分（可用二级标题分隔）：

1. **原文**（完整转写正文，或与用户约定的附件引用方式及路径说明）。
2. **纪要**（使用 [纪要模板](#纪要模板)）。
3. **OpenClaw 交付块**（完整一段 `---OPENCLAW_ASR_DELIVERY---` … `---END_OPENCLAW_ASR_DELIVERY---`，与对话中交付给龙虾的块一致）。

---

### 选项 B：保存为 Word（仅纪要）

使用 **huo15-openclaw-office-doc 技能**（位于 `skills/huo15-openclaw-office-doc/`）将**纪要部分**生成为格式规范的 `。docx` 文件。

**依赖安装**（如未安装）：

```bash
pip install python-docx reportlab pygments
```

> 如果系统有多个 Python 版本（如 MSYS2 Python 与官方 Python 并存），请确认 `pip` 安装的目标 Python 与执行脚本的 Python 保持一致。可通过 `python -c "import sys; print(sys.executable)"` 确认。

**文件命名**：

```text
ASR_纪要_YYYY-MM-DD_HHmmss.docx
```

示例：`ASR_纪要_2026-05-07_143052.docx`。

**操作步骤**：

1. 将**纪要**全文写入一个临时 Markdown 文件（如 `$env:TEMP\meeting_summary_<timestamp>.md`）。注意：内容为执行本 skill 时已生成的 `summary_markdown` 字段，**不含交付块**。
2. 调用 office-doc 的 `create-word-doc.py` 生成 Word：

```powershell
python <workspace>/skills/huo15-openclaw-office-doc/scripts/create-word-doc.py `
  --output "<下载目录>\ASR_纪要_YYYY-MM-DD_HHmmss.docx" `
  --title "会议纪要 - YYYY-MM-DD" `
  --content @"<临时 markdown 文件路径>" `
  --doc-format 会议纪要 `
  --company-name "会议纪要" `
  --no-title-block
```

> `<workspace>` 为本 skill 所在 OpenClaw 工作区根目录（即 `~/.openclaw/workspace-hanser`）。因本机环境 `python` 指向 MSYS2 的 Python，需要显式使用官方 Python 路径：`D:\Users\Grunray\AppData\Local\Programs\Python\Python313\python.exe`（可通过 `python -c "import sys; print(sys.executable)"` 确认正确的路径）。

**参数说明**：

| 参数 | 值 | 说明 |
|------|------|------|
| `--output` | 下载目录下的 `。docx` 路径 | 输出文件 |
| `--title` | `会议纪要 - YYYY-MM-DD` | 文档标题 |
| `--content @<path>` | `@` 开头表示读取文件 | 纪要正文（Markdown 格式） |
| `--doc-format 会议纪要` | 指定为会议纪要规范 | 自动匹配页眉/正文样式 |
| `--company-name 会议纪要` | 占位公司名 | 避免因缺公司信息报错 |
| `--no-title-block` | 不额外渲染标题块 | 标题已在正文中 |

3. **清理**：删除临时 Markdown 文件。
4. 告知用户文件已生成。

> **注意**：当前使用占位公司名「会议纪要」，header 区域可能显示占位名称。如希望定制公司信息，可使用 `--company-name "<公司名>"` 和 `--logo-path "<LOGO路径>"`，或参照 office-doc 技能的本地公司信息工作流配置持久化信息。

---

## 自检清单

- [ ] 音视频已尽量统一为 MP3（或等价单音频轨）再转写。
- [ ] 在 Windows 用 openai-whisper CLI 时，已设置 **`PYTHONIOENCODING=utf-8`**（或等价方式），避免 GBK 编码崩溃。
- [ ] openai-whisper 默认已用 **`base`** 转写，并已按质量指标完成判断；问题多时已建议 **`small` / `medium`** 重跑。
- [ ] 若使用 **WhisperX** 做 diarization：已说明 **HF 登录 / 协议同意 / `use_auth_token=False` 尝试** 等实际情况，且原文已带说话人分段标注。
- [ ] `.tty` 已按文本 / script / ttyrec 路径处理，不确定处已标注。
- [ ] 纪要严格来源于原文或终端输出。
- [ ] 已输出 `OPENCLAW_ASR_DELIVERY` 块供龙虾判断。
- [ ] （Whisper 路径在质量可接受后，或 `.tty` 等路径在完成交付块后）已**询问**是否保存，以及保存格式（Markdown 或 Word）。
    - Markdown：已写入 **下载** 文件夹，文件名为 `ASR_转写_YYYY-MM-DD_HHmmss.md`，含 **原文 + 纪要 + 交付块**。
    - Word：已使用 `huo15-openclaw-office-doc` 技能的 `create-word-doc.py` 生成 `。docx` 文件到 **下载** 文件夹（仅含**纪要**部分）。

---

## 附加资源

- 终端 ANSI 剥离与轻量 `.tty` 辅助：见 [scripts/README.md](scripts/README.md)
