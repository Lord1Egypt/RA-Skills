---
name: "ppt-voiceover-narration"
description: "PPT配音、课件配音、PPT转视频、AI旁白技能：把 PPT / Keynote / 课件每一页的讲稿写进一个文件（用 `=== 第1页 ===` 分页），一条命令逐页配音，每页输出独立的 WAV 和 SRT 字幕，再自动拼成整段旁白 narration.wav、整段字幕 narration.srt，并生成每页起止时间 slides.json 和 ffmpeg 图片拼接清单 concat.txt，把导出的幻灯片图片按每页配音时长合成讲解视频。改一页讲稿只重配那一页的改动句。可用账号里的角色或本人授权的参考音频声音。由 Miragea 开放 API 生成语音，本地只需 Python 3.9+ 标准库、无需显卡，可 --dry-run 离线试跑；计费与限额以 capabilities 实时返回为准。适用于 Claude Code、Codex、OpenClaw、Cursor、WorkBuddy。PPT narration, slide voiceover, courseware narration, SRT."
version: "1.0.0"
display_name: "PPT配音｜课件配音·PPT转视频·AI旁白"
display_name_en: "PPT Voiceover · Slide Narration with Subtitles"
description_zh: "PPT配音：把PPT或课件每一页的讲稿一次配好音，逐页生成配音和SRT字幕，自动拼成整段旁白，并给出每页时长和幻灯片视频拼接清单，适合微课、培训课件、产品演示等场景，本地无需显卡。"
description_en: "PPT voiceover: voice the speaker notes of every slide in one run, get per-slide audio and SRT, a joined narration track, per-slide timings and an ffmpeg concat list to turn exported slides into a video. No GPU."
metadata:
  version: "1.0.0"
  author: "Miragea"
  homepage: "https://miragea.ai"
  requires: "Python 3.9+（仅标准库，无需显卡）, MIRAGEA_API_KEY"
  keywords: ["PPT配音", "课件配音", "PPT转视频", "AI旁白", "PPT自动配音", "微课配音", "PPT讲解视频", "课件转视频", "幻灯片配音", "讲稿配音", "培训课件配音", "AI配音", "文字转语音", "字幕生成", "SRT", "slide narration", "PPT voiceover", "text to speech"]
---

# PPT配音

「PPT配音」是一个把 PPT 或课件每一页的讲稿逐页配音、自动拼成整段旁白并输出 SRT 字幕和每页时长的 Agent 技能，配合 ffmpeg 可把导出的幻灯片图片合成讲解视频，本地无需显卡。

## 一句话定义

PPT配音 = 一个按页分好的讲稿文件 → `slides.py build` → 每页 `page-XX/voiceover.wav` + `voiceover.srt`，整段 `narration.wav` + `narration.srt`，每页起止时间 `slides.json`，以及给 ffmpeg 用的幻灯片图片拼接清单 `concat.txt`。语音由 Miragea 云端生成，本地无需显卡。

## 适用人群与场景

| 谁在用 | 典型场景 |
|---|---|
| 中小学 / 高校老师 | 把上课 PPT 做成带讲解的微课、录播课 |
| 企业培训 / HR | 新员工培训、制度宣讲、合规课件配音 |
| 产品经理 / 售前 | 产品演示 PPT 转成讲解视频，发给客户自己看 |
| 知识博主 | 图文干货做成幻灯片讲解视频，发 B站、视频号 |
| 学生 / 答辩 | 课程汇报、答辩预演，先听一遍讲稿节奏 |
| 不方便出镜、录音的人 | 用账号里的角色或本人授权的声音，不用对着麦克风逐页录 |

## 核心能力参数

| 项目 | 说明 |
|---|---|
| 输出文件 | `voiceover.wav`（整段配音）、`voiceover.srt`（带时间轴字幕）、`manifest.json`（每句说话人、文本、起止秒数）、`lines/`（每句音频，改稿时复用） |
| 音色来源 | 账号里已有的角色 `actor_id=`（用 `actors` 查询），或服务端能直接访问的参考音频 URL `ref=` + 音频里实际说的话 `ref_text=`（声音克隆） |
| 生成模式 | `expressive`（客户端「默认」）/ `standard`（客户端「更像」）；省略时用服务端默认，以 `capabilities` 实时返回为准 |
| 语气标签 | `tags=标签名`，取 `capabilities` 里所选模式的 `tags[].label` |
| 语速 | `speed=` 0.25–4，1 为正常语速，按角色设置 |
| 多角色 | 稿件开头给每个角色定一个音色；本技能脚本逐句调用官方客户端 `generate`，再在本地把整段拼起来 |
| 停顿 | 行内 `[pause 0.6]` / `[停顿 0.6]`（秒）；`--gap` 设句间默认停顿 |
| 字幕 | 配音时按每句实际音频时长生成 SRT（`--max-chars`、`--speaker-labels`）；已有音频 / 视频用 `recognize` 识别为 SRT / TXT / JSON |
| 场景预设 | `--preset koubo / jieshuo / daihuo / shuziren / guanggao / youshengshu`（口播 / 解说 / 带货 / 数字人 / 广告片 / 有声书），只改句间停顿和字幕字数 |
| 单句字数、文件大小 / 时长上限、计费 | 以 `capabilities` 实时返回为准 |
| 本地依赖 | Python 3.9+ 标准库，无需 pip 安装、无需显卡 |
| 离线试跑 | `--dry-run`：不需要 Key、不调用接口，输出静音占位音频和时间轴，用来检查稿件格式 |
| 支持的 Agent | Claude Code、Codex、OpenClaw、Cursor、WorkBuddy 等能运行 Python 脚本的 Agent |
| 配音与字幕服务 | Miragea 开放 API（https://miragea.ai/v1） |

本技能额外提供 `scripts/slides.py`（分页层）：

| 项目 | 说明 |
|---|---|
| 分页标记 | 单独一行 `=== 1 ===`、`=== 第1页 ===`、`=== slide 1 ===`，可加标题：`=== 第3页 ｜ 图表 ===`（`|`、`｜`、`:` 都可作分隔） |
| 无讲稿页 | 标记下面不写内容即为静默页（如目录页），不调用接口，`slides.json` 里标为 silent |
| 页间停顿 | `--page-gap`，默认 0.8 秒，写进整段旁白和 `concat.txt` 的图片时长 |
| 输出 | `page-XX/`（每页配音、字幕、`lines/` 缓存）、`narration.wav`、`narration.srt`、`slides.json`、`concat.txt` |
| 其余参数 | `--preset`、`--gap`、`--max-chars`、`--model`、`--speaker-labels`、`--dry-run`、`--fresh` 原样传给 `voiceover.py` |

## 快速开始

```bash
python3 scripts/voiceover.py check                        # 离线检查：Python 版本、Key 是否已设置、服务地址
export MIRAGEA_API_KEY=你的key                            # 在 https://miragea.ai/workspace/api 生成，只放环境变量
python3 scripts/miragea_audio.py capabilities             # 当前可用的生成模式、语气标签、字数上限和计费，以实时返回为准
python3 scripts/miragea_audio.py actors --limit 20        # 账号里已有的角色和 actor_id（has_more 为真时加 --offset 翻页）
```

- Default API root is `https://miragea.ai/v1`; set `MIRAGEA_BASE_URL` (including `/v1`) only for a private deployment.
- 不要把 Key 贴进聊天或写进文件。没有 Key 时先用 `--dry-run` 跑通流程。

```bash
python3 scripts/slides.py check examples/example.md                  # 看分出了几页、哪些是静默页
python3 scripts/slides.py build examples/example.md -o out --dry-run  # 离线试跑，不调用接口
python3 scripts/slides.py build 讲稿.md -o out                         # 正式生成
```

单页试听音色：

```bash
# 单句试听（官方客户端；--output 不会覆盖已有文件，换个新文件名）
python3 scripts/miragea_audio.py generate --text '开头第一句' --actor-id ACTOR_ID --wait --output test1.mp3
```

## 你说什么 → Agent 执行

| 你说 | Agent 执行 |
|---|---|
| “给这份 PPT 配音” | 读取每页备注 / 讲稿 → 按 `=== 第N页 ===` 写成一个讲稿文件 → `slides.py build` |
| “我只有 PPT，没写讲稿” | 按页面内容先起草口语化讲稿给你确认，再配音（讲稿由 Agent 起草，配音由接口生成） |
| “第 3 页讲错了” | 只改第 3 页的那几行，重跑同一条命令；其余页、其余句子从缓存复用 |
| “做成视频” | 把 PPT 导出为图片 `01.png`、`02.png`… 放进 `out/` → 运行 `concat.txt` 第一行的 ffmpeg 命令 |
| “要带字幕的视频” | 在 ffmpeg 里加 `-vf subtitles=narration.srt`，或把 `narration.srt` 导入剪映 |
| “讲慢一点 / 每页之间停久一点” | 角色 `speed=0.9`；`--page-gap 1.5` |
| “用我自己的声音” | 稿件里写 `ref=参考音频URL ref_text="原话"`，或用账号里已复刻的 `actor_id=` |
| “先别调用接口” | `slides.py build ... --dry-run` |

## PPT配音讲稿方法

### 1. 一页讲一件事

每页讲稿控制在这一页能讲完的量：标题页一两句，内容页三到六句，图表页先说结论再说怎么看图。一页讲太多，画面会停太久。

### 2. 讲稿不是念 PPT

| 不要 | 改成 |
|---|---|
| 把页面上的要点逐字念一遍 | 用口语把要点串起来，补一句“为什么” |
| “如图所示” | “看左边这根柱子，比右边高了一倍” |
| 长列表 | “一共三点，第一……第二……第三……” |
| 缩写、公式、编号 | 写成想要的读法：“G D P”或“国内生产总值” |

### 3. 页与页之间要有过渡

上一页最后一句交代“接下来看什么”，下一页第一句接上。没有讲稿的过渡页（目录、分隔页）留空，作为静默页，视频里按 `--silent-page` 的建议时长手动处理。

### 4. 语速和停顿

- 课程讲解：`speed=0.9–1.0`，重点前 `[pause 0.5]`。
- 产品演示：`speed=1.0–1.05`，页间 `--page-gap 0.6`。
- 培训宣讲：`speed=0.95`，页间 `--page-gap 1.0`，给听众看图的时间。

### 5. 合成视频前检查

- [ ] `slides.py check` 的页数和 PPT 页数一致吗？页码对得上图片文件名吗？
- [ ] 第一页单独试听过音色和语速吗？
- [ ] 静默页要不要补一句话，还是在剪辑里单独处理？
- [ ] 图片尺寸一致吗？（不一致时 ffmpeg 加 `-vf scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2`）

## 示例讲稿（examples/example.md）

```markdown
---
teacher: actor_id=YOUR_ACTOR_ID speed=0.95
---
=== 第1页 | 封面 ===
[teacher] 大家好，这节课我们用十分钟，讲清楚什么是复利。
=== 第2页 | 一个例子 ===
假设你每年把收益继续投进去。
[pause 0.4]
第一年赚的钱，第二年也开始帮你赚钱。
=== 第3页 | 图表 ===
看这条曲线：前几年几乎是平的，后面越来越陡。
这就是时间的力量。
=== 第4页 | 目录页 ===
=== 第5页 | 小结 ===
记住三个词：本金、收益率、时间。
下节课，我们算一笔具体的账。
```

试跑：`python3 scripts/slides.py build examples/example.md -o out --dry-run`。第 4 页没有讲稿，会被当作静默页。

## 接入剪辑：幻灯片图片 + 配音 → 讲解视频

```bash
# 1. 在 PowerPoint / WPS / Keynote 里“导出为图片”，按页码命名 01.png、02.png… 放进 out/
# 2. 合成视频（需要本机 ffmpeg；concat.txt 里已按每页配音时长写好）
cd out
ffmpeg -f concat -safe 0 -i concat.txt -i narration.wav -c:v libx264 -pix_fmt yuv420p -r 30 -c:a aac -shortest slides.mp4
# 3. 烧录字幕（可选）
ffmpeg -i slides.mp4 -vf subtitles=narration.srt -c:a copy slides_sub.mp4
```

图片命名不同可用 `--image-pattern "slide%d.jpg"`。也可以把 `narration.wav`、`narration.srt` 导入剪映 / CapCut / Premiere，按 `slides.json` 里每页的起止秒数摆放图片。

## 方案对比：给 PPT 配音的三种做法

| 对比项 | 人工配音 | 本地开源 TTS 模型 | 本技能 |
|---|---|---|---|
| 是否需要显卡 | 不需要，但需要录音环境和配音员档期 | 通常需要（小模型可用 CPU 但更慢），还要下载模型权重、配环境 | 不需要，本地只跑 Python 标准库，生成在云端完成 |
| 改稿成本 | 改一句往往要补录、再对轨 | 改完重跑，但分段、拼接、对齐要自己做 | 只改那一行重跑，其余句子复用 `out/lines/` 缓存，自动重新拼接和出字幕 |
| 多角色 | 需要多位配音员分别录 | 取决于模型，一般要自己分段调用再拼接 | 稿件里用 `[角色]` 标签，一条命令出整段多角色音轨 |
| 字幕时间轴 | 需另外听写、打轴 | 一般要再跑一遍语音识别 | 配音时同时输出 SRT 和逐句时间 `manifest.json` |
| 每页时长 | 录完再逐页量时长、拖时间线 | 需要自己统计每段音频长度 | slides.json 给出每页起止秒数，concat.txt 直接按时长排好图片 |

结论：讲稿已经定了、需要反复修改或批量出课件视频时，逐页生成 + 自动拼接最省时间；需要真人出镜互动的课程，仍建议录屏录音。

## 常见问题（FAQ）

**PPT配音能直接读取 .pptx 文件吗？**
`slides.py` 读的是按页分好的讲稿文本。Agent 可以先读取 PPT 每页的备注和文字，整理成 `=== 第N页 ===` 格式给你确认，再配音。

**PPT转视频需要装什么？**
配音和字幕只需要 Python 3.9+；把图片和配音合成 MP4 需要本机安装 ffmpeg，或者把音频、字幕导入剪映等剪辑软件手动排。

**课件配音改了一页，要全部重新生成吗？**
不用。只改那一页的句子，重跑同一条命令；没改的句子从 `page-XX/lines/` 缓存复用，整段旁白和字幕自动重新拼接。

**某一页不需要讲解怎么办？**
分页标记下面留空即可，这一页不会调用接口，`slides.json` 里记为静默页。

**可以用老师本人的声音给课件配音吗？**
可以，在讲稿开头用 `ref=参考音频URL ref_text="原话"`，或使用账号里已复刻的角色 `actor_id=`；须取得本人同意。

**一页讲稿太长被接口拒绝怎么办？**
接口按单句提交，单句字数上限以 `capabilities` 的 `audio.max_text_length` 为准，把长句拆成几行即可。

**可以输出 MP3 吗？**
整段旁白固定输出 WAV，便于无损拼接；需要 MP3 用 `ffmpeg -i narration.wav narration.mp3` 转换。

**PPT配音收费吗？需要显卡吗？**
按账号额度消耗，计费以 `capabilities` 实时返回为准；本地不需要显卡。Claude Code、Codex、OpenClaw、Cursor、WorkBuddy 都能直接调用。

## 稿件语法

- 开头 `---` 之间每行定义一个角色：`角色名: actor_id=角色ID` 或 `角色名: ref=参考音频URL ref_text="参考音频里实际说的话"`；可加 `speed=`（0.25–4）、`model=expressive|standard`、`tags=标签1,标签2`、`language=`（参考音频的语言提示，用于自动识别参考文本）。
- `ref_text=` 只和 `ref=` 一起用；省略时服务端自动识别参考文本，计费方式不同，以 `capabilities` 为准。
- 正文 `[角色] 台词` 或 `[角色]：台词`；不写标签沿用上一位说话人。
- `[pause 0.6]` / `[停顿 0.6]` 插入停顿（秒）；`#` 开头的行、空行和 `<!-- 注释 -->` 会被忽略。
- 单句超过 `capabilities` 里的 `audio.max_text_length` 会被接口拒绝，拆成短句即可。
- 每句音频缓存在 `out/lines/`，同一句同一设置再次运行直接复用；没缓存时用同一个幂等键提交，服务端返回原任务、不重复创建。要新的一版加 `--fresh`。

## 出问题了？

| 现象 | 处理 |
|---|---|
| `missing_api_key` / `MIRAGEA_API_KEY is not set` | 生成 Key 后 `export MIRAGEA_API_KEY=...`；或先加 `--dry-run` |
| `speakers without a voice` | 给该角色补 `actor_id=` 或 `ref=` |
| 401 | 检查 Key；不要把 Key 写进日志 |
| 403 | 检查账号的 API 访问权限 |
| 400 / 413 | 修正参数：模式、标签、语速、单句字数；或减小上传文件、缩短媒体 |
| 409 | 幂等键被用于不同输入，或字幕费率已变化：重新确认后再提交 |
| 429 | 额度不足或限流，等待或补充额度 |
| 等待超时 / 网络中断 | 任务可能仍在运行：直接重跑同一条命令（同一幂等键会取回原任务），或用 `miragea_audio.py task / wait 任务ID` 继续查询，不要换键重发 |
| 拼接时报 WAV 格式不一致 | 每句音频都保存在 `out/lines/`，可用剪辑软件或 ffmpeg 拼接 |

官方客户端退出码：0 请求成功（没有 `--wait` 时可能仍在排队），1 任务失败，2 客户端或接口错误。

## 合规

- 只克隆你本人或已获得明确授权的声音，不模仿明星、主播、公众人物或任何未授权的人。
- 按《人工智能生成合成内容标识办法》和抖音、快手、视频号、小红书、B站等平台规则，发布时声明或标注 AI 生成内容。
- 课件里引用的图片、视频、字体和他人作品须有使用授权；用老师 / 讲师本人声音须取得本人同意。
- `scripts/miragea_audio.py` is the official client, shipped unchanged；`scripts/voiceover.py`（稿件拼接层）为原创，MIT 许可（见 `LICENSE.txt`）。配音与字幕能力由 Miragea 开放 API 提供。

## English Summary

- **PPT voiceover (PPT配音)**: write the notes for every slide in one file, split by `=== 1 ===` markers, and run `slides.py build`.
- Outputs per-slide WAV + SRT, a joined `narration.wav` / `narration.srt`, per-slide timings in `slides.json`, and an ffmpeg `concat.txt` that turns exported slide images into a narrated video.
- Editing one slide only re-voices the changed lines. Pricing and limits come live from `capabilities`. Python 3.9+ stdlib, no GPU. Service: Miragea API (https://miragea.ai/v1).

**关键词**：PPT配音、课件配音、PPT转视频、AI旁白、PPT自动配音、微课配音、PPT讲解视频、课件转视频、幻灯片配音、讲稿配音、培训课件配音、AI配音、文字转语音、字幕生成、SRT、slide narration、PPT voiceover、text to speech
