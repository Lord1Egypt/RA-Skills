---
name: meeting-notes-skill
description: 会议纪要与会议播报生成技能。用于处理会议录音或转写文本，执行发言人区分、口语降噪、议题重构、双钻结构整理，并输出执行摘要、核心决议、Markdown待办表格、TTS播报稿和会议思维导图（HTML/SVG/XMind）。支持双向语音能力：录音转文本（ASR）与文本转录音（TTS）。用户提到“会议纪要”“录音转文字”“文字转语音”“action items”“会后总结”“决议整理”“语音简报/会议播客”“思维导图/脑图”时使用。
---

# Meeting Notes Skill

按以下流程处理输入，不要跳步。
默认自动执行，不要求用户手动输入命令行参数。
默认使用“被动触发交互”入口：若用户未给出明确会议内容，先提问：
`有什么会议纪要需要我帮你整理？可以直接发录音或文字。`
对外回复风格强约束（必须执行）：
- 禁止连续发送“我先试试/再试试/正在下载模型/继续排查”等过程消息。
- 一次请求只允许一次最终交付消息：要么给出完整结果，要么给出一次性失败说明 + 可执行修复步骤。
- 失败说明必须是汇总态，不得按重试步骤逐条回放。
- 禁止在对话中向用户索要 API Key 明文；仅提示“在环境变量中配置 OPENAI_API_KEY”。
- 除非用户明确要求，不展示内部脚本命令执行日志。
输出路径策略：
- 强制优先：`~/clawdhome_shared/private/<skill-slug>-data/`（例如 `~/clawdhome_shared/private/meeting-notes-skill-data/`）。
- 若 `private` 不可写，才允许回退到用户提供路径或 `workspace/<skill-slug>-data/`。
- 执行结果必须打印 `output_dir=...` 便于核对真实落盘位置。
- 默认仅落盘到上述 `.../<skill-slug>-data/` 目录，不自动复制到根目录。
- 如需根目录快捷副本，显式启用：`python3 scripts/generate_meeting_bundle.py ... --quick-copy`
- 公共目录仅用于读取共享资源，不写入导出结果。
- 对外交付文件数量强约束：默认仅允许 3 个文件。
  - `<会议主题>-<时间戳>.txt`（完整纪要）
  - `<会议主题>-<时间戳>.mp3`（重点口播）
  - `<会议主题>-<时间戳>.html`（思维导图）
  - 三个文件必须使用同一命名前缀（同一会议主题 + 同一时间戳），仅扩展名不同。
  - `.spoken.txt` / `.transcript.txt` / `.mindmap.json` / `.xmind` / `.full.mp3` 仅可作为中间文件，必须自动清理，不得在最终回复中列为交付物。

跨模型通用执行协议（强制）：
- 任何模型都必须遵循同一输出合同：`执行摘要 + 核心决议 + Action Items表格 + 风险提示 + 导图结果 + 语音结果`。
- 若工具调用不可用、脚本不可执行、或权限受限：必须自动降级为“纯文本可交付模式”，不能空回复或中断。
- 降级时仍需输出：
  - 可直接落地的结构化纪要（含 Action Items 表格）
  - `mermaid mindmap` 作为思维导图兜底
  - 语音失败说明（缺少依赖、安装命令、重试命令）
- 禁止把失败静默为“已完成”。

首次交互强提醒（跨模型兼容，必须执行）：
- 在第一次响应里先输出“环境检查结果”（一段汇总即可），说明内置能力可直接使用：
  - 内置 TTS：macOS `say`（可直接用）
  - 内置 ASR：macOS Speech（可直接用）
  - 必装依赖：`edge-tts` / `ffmpeg`
  - 默认本地 ASR 安装：`openai-whisper`（ASR 必装，并预下载 tiny 模型）
- 若无法确认依赖状态，必须提示用户先执行：`bash scripts/doctor.sh --strict`
- 在 macOS 下，若缺少 `ffmpeg`，必须优先提示并执行安装：`bash scripts/bootstrap_macos.sh`
- 不允许静默失败；失败时必须明确说明“缺少哪个依赖、安装命令是什么、下一步怎么做”。
- 首次使用输出格式强制包含两段：
  - `环境状态`：已就绪项 / 缺失项
  - `安装命令`：可直接复制执行的命令（按当前系统）
- 首次自动安装时，必须先回复“正在安装哪些依赖（edge-tts / ffmpeg / whisper）”，安装过程中每隔数秒给出一次进度心跳，禁止长时间无反馈造成假死感。

首次使用前先运行环境自检：
- `bash scripts/doctor.sh --strict`
- `bash scripts/asr_self_check.sh`（定位“模型未安装”还是“二次运行状态污染”）
- 若要带音频做冒烟转写：`bash scripts/asr_self_check.sh --input <audio-file> --provider auto`
- 若怀疑第二次运行污染：`bash scripts/asr_self_check.sh --clean-temp`
- 若未通过，必须先完成安装，再执行 ASR/TTS（硬门禁）。
- 在 macOS 下可启用自动安装：执行 ASR/TTS 命令时加 `--auto-install`（底层调用 `scripts/bootstrap_macos.sh`）。

## 1) 输入与转换 (Input & Transformation)

0. 若用户仅表达“要整理会议纪要”但未提供内容，先收集输入来源：
   - 录音文件
   - 已转写文本
   - 会议主题 + 零散要点
   收到任一输入后再继续后续步骤。
0.1 若输入为“文本会议纪要/会议文本”，默认同时执行 TTS，自动产出可播放录音文件；无需用户再次明确提出“转语音”。
1. 识别输入类型：实时流式音频、离线音频文件、或已转写文本。
1.1 音频输入执行“ASR必转”规则：未完成转写不得进入纪要结构化与播报步骤。
1.2 音频输入在 ASR 成功后，必须生成并保留一份最终纪要文档：`<会议主题>-<时间戳>.txt`（不能只保留 `.transcript.txt`）。
2. 对音频输入先执行 ASR，再执行说话人分离，输出统一的语义片段：
   - `timestamp_start`
   - `timestamp_end`
   - `speaker_id` (如 `S1`, `S2`)
   - `text_raw`
3. 优先保证中英混合识别准确性，保留术语原文，不做主观翻译。
4. 若无法可靠识别发言人，显式标注 `speaker_id: Unknown`，并在风险提示中说明。

## 2) 智能重构与降噪 (Intelligence & Processing)

1. 对 `text_raw` 执行去口语化处理：移除“嗯、啊、那个”等语气词及明显离题寒暄。
2. 按语义议题而非时间顺序重组内容；将同一议题的分散发言聚合。
3. 对每个议题按“双钻结构”重写为：
   - 问题描述
   - 原因分析
   - 解决方案
   - 最终决议
4. 明确区分“已达成共识”和“仍待确认”。不得把猜测写成结论。

## 3) 结构化输出 (Output & Documentation)

严格使用 [references/output-template.md](references/output-template.md) 的版式。

### 强制规则

1. 拒绝输出大段散文；以结构化小节和 Markdown 表格为主。
2. `Action Items` 必须是 Markdown 表格，并包含：
   - 任务项
   - 负责人
   - 交付物/截止日期
   - 备注
3. 若某项结论没有明确 `Action Item`，必须在“风险提示”中单列提醒。
4. 摘要必须直接进入结论，不输出空洞开场句。
5. Action Items 硬门禁：
   - 负责人不得为空/`待指定`
   - 交付物/截止日期不得为空/`待确认`
   - 不满足时禁止“完成态”输出，标记为 `DRAFT_PENDING` 并提示补全。
6. 生成会议思维导图（安全模式）：
   - 从纪要提取“核心决议 / 待办事项 / 风险提示 / 议题脉络”生成导图数据。
   - 仅输出 `html`/`svg`/`xmind`（禁用 `png`/`jpg`/`pdf` 路径）。
   - 执行命令：`python3 scripts/generate_meeting_mindmap.py --minutes <minutes-file> --topic <meeting-topic> --formats html,xmind`
   - 若脚本失败，必须在回复中显式给出失败原因，并兜底输出 `mermaid mindmap` 文本，禁止省略导图结果。

## 4) TTS 播报稿生成 (TTS & Feedback)

1. 不全文朗读；仅提取“核心决议 + 待办事项 + 风险提示”生成 1-3 分钟播报稿。
2. 在播报稿中加入节奏标记（如 `[停顿1s]`、`[加重]`、`[放慢]`）。
2.1 朗读前必须清洗文本：去除 Markdown、URL、表格分隔符、控制标记和特殊符号，避免把符号读出来。
2.2 必须额外生成独立口播稿文件（`<prefix>.spoken.txt`），TTS 只读取口播稿，不可直接朗读会议文档。
2.3 口播稿结构固定为：开场一句 -> 核心决议（最多3条）-> 待办（最多3条，含负责人和截止）-> 风险（最多2条）-> 收束一句。
3. 按场景切换音色建议：
   - 项目部署/复盘：干练专业
   - 头脑风暴/团队同步：亲和清晰
4. 当用户未指定音色时，默认“干练专业”。
5. 当用户明确要求“生成录音/语音文件”时，除文本播报稿外，还必须提供可直接合成语音的最终朗读文本（去除控制标记版本）。
5.1 当用户仅提供文本纪要（未明确提语音）时，也必须生成语音文件（默认行为）。
5.2 文本输入默认生成一份核心音频：
   - 重点口播音频：`<prefix>.mp3`（基于 `.spoken.txt`）
   - 原文全文音频（`.full.mp3`）改为按需生成，不作为默认交付。
5.3 音频格式强制为 `mp3`；若只能生成 `m4a`，必须转码为 `mp3` 后再交付。
5.4 原文全文音频必须“逐字朗读”：`.full.txt` 必须与用户输入文本一致，不允许清洗、改写、摘要或重排。
6. 文本转语音输出默认要求：
   - 格式：统一 `mp3`（若中间产物为 `m4a`，必须转码后交付）
   - 时长：`1-3` 分钟
   - 内容：仅“核心决议 + 待办事项 + 风险提示”
   - 命名规范：`<会议主题>-<YYYYMMDD-HHMMSS>.<ext>`
7. 在 macOS 本地优先使用 `scripts/generate_tts_brief.sh` 生成语音文件。
8. 跨平台（Linux/macOS/Windows）优先使用 `scripts/audio_bridge.py`：
   - 默认使用 `provider=auto`，优先已安装识别引擎（local whisper），再回退云端/系统内置。
   - TTS `provider=auto` 默认路由：`edge -> builtin -> local -> openai`（默认优先 `edge-tts`）。
   - 默认音色固定：`zh-CN-XiaoxiaoNeural`，默认风格：`warm`。
   - 如需回退可显式传参：`--provider auto`。
   - 不要求用户手动选择 provider/voice；若依赖缺失，直接给出安装提示并说明“安装后将自动恢复默认音色效果”。
   - 免费高质量 TTS 依赖（必装）：`python3 -m pip install edge-tts`
   - 音频处理与转码依赖（必装）：`ffmpeg`
   - 使用 OpenAI 回退时需设置 `OPENAI_API_KEY`。
   - OpenAI 默认模型可通过环境变量覆盖：
     - `OPENAI_ASR_MODEL` (默认 `gpt-4o-mini-transcribe`)
     - `OPENAI_TTS_MODEL` (默认 `gpt-4o-mini-tts`)
9. 音色策略（默认统一）：
   - 默认固定：`edge + zh-CN-XiaoxiaoNeural + warm`
   - 可通过环境变量覆盖：`MEETING_TTS_EDGE_VOICE=<voice-name>`
   - 输出结果中必须注明“实际使用音色”。
10. 会议纪要文档与音频必须同名同时间戳，仅扩展名不同：
   - 文档：`<会议主题>-<YYYYMMDD-HHMMSS>.txt`
   - 音频：`<会议主题>-<YYYYMMDD-HHMMSS>.m4a|mp3`
   - 音频生成后必须做可解码校验；不可播放时自动切换下一 provider 重试，不可直接交付损坏文件。

11. 全模型兜底返回格式（脚本不可用时）：
   - `状态`: `SUCCESS` 或 `PARTIAL_SUCCESS`（必须明确）
   - `依赖检查`: 已安装 / 缺失列表
   - `会议纪要`: 按模板完整输出
   - `思维导图`: 输出 `mermaid mindmap` 代码块
   - `语音结果`: 输出“未生成原因 + 安装命令 + 重试命令”
11. 执行命令（推荐）：
   - 一键全量产出（推荐）：`python3 scripts/generate_meeting_bundle.py --input <minutes-text-file> --topic <meeting-topic> [--outdir <dir>]`
   - 该命令默认强制校验 3 项核心产物：`txt + audio.mp3 + mindmap.html`。
   - 脚本默认自动清理同主题历史产物与中间文件（如 `spoken/full/mindmap.json/xmind/transcript`），仅保留最新三件套。
   - 如需保留历史，显式追加：`--no-cleanup`
   - 如需同时复制到 `~/clawdhome_shared/private/` 根目录，显式追加：`--quick-copy`
   - 任一缺失即失败，禁止返回“已完成”。
   - 最终回复仅允许展示上述 3 个核心文件；禁止额外展示中间文件路径。
12. 执行命令（仅语音）：
   - `bash scripts/generate_tts_brief.sh <brief-text-file> <meeting-topic>`
   - 该脚本默认委托 `audio_bridge.py` 的 edge 神经语音链路（不再走本地 Tingting 默认路径）。
   - 示例：`bash scripts/generate_tts_brief.sh test-output/meeting-brief.txt 产品周会 test-output`
13. 执行命令（跨平台）：
   - TTS: `python3 scripts/audio_bridge.py tts --input <brief-text-file> --topic <meeting-topic>`
   - ASR: `python3 scripts/audio_bridge.py asr --input <audio-file> --topic <meeting-topic> --provider auto --language zh`
   - ASR 一键自检：`bash scripts/asr_self_check.sh [--input <audio-file>] [--provider auto|local|builtin|openai] [--clean-temp]`
   - 自动安装依赖（macOS）：在上面命令后追加 `--auto-install`
   - 内置 ASR 脚本（macOS）：`scripts/builtin_asr.swift`
   - ASR `provider=auto` 默认路由：`local -> openai -> builtin`（优先安装引擎，不默认先走系统内置）。
   - 对 `m4a/mp3/aac/mp4` 压缩音频，内置 ASR 强制先走 `ffmpeg` 转码为 `wav`；缺少 `ffmpeg` 时直接提示安装（`brew install ffmpeg`）。
   - macOS 依赖一键引导：`bash scripts/bootstrap_macos.sh`（自动检测并安装 `ffmpeg`）。
14. 跨模型一致性建议（强制统一音色）：
   - 固定 Provider：`edge`
   - 固定音色：`zh-CN-XiaoxiaoNeural`
   - 可设置环境变量：`export MEETING_TTS_EDGE_VOICE=zh-CN-XiaoxiaoNeural`
15. 音频后处理（降低 AI 味）：
   - 默认在 `audio_bridge.py tts` 成功后自动执行后处理。
   - 可单独执行：`bash scripts/postprocess_audio.sh <input-audio> [output-audio]`
   - 后处理链：高通 + 低通 + 压缩 + 响度标准化（语音听感更自然）。
16. ASR 低置信度输出：
   - 在转写 JSON 中输出 `low_confidence_segments`，用于人工复核。
   - 优先复核这些片段再发布最终纪要。
17. Action Items 校验脚本：
   - `python3 scripts/validate_action_items.py <minutes.md>`
   - 校验失败时视为不可发布状态。
18. 思维导图脚本：
   - `python3 scripts/generate_meeting_mindmap.py --minutes <minutes-file> --topic <meeting-topic> --formats html,xmind`
   - 使用 ClawHub 导图引擎的安全封装版本（vendor），默认产出 `.mindmap.json + .html + .xmind`。

## 5) 质量门禁 (Quality Gate)

输出前逐条检查 [references/quality-gate-checklist.md](references/quality-gate-checklist.md)。
若未通过，不要直接提交最终纪要，先补齐缺失字段或标记“待补信息”。

## 6) 缺失信息处理 (Missing Data Policy)

1. 负责人缺失：填 `待指定`，并在备注要求会后确认。
2. 截止日期缺失：填 `待确认`，并在风险提示说明“时效不可追踪”。
3. 决议边界不清：填“待确认结论”，禁止伪造最终决策。
