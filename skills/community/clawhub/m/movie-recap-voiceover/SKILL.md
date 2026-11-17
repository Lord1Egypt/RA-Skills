---
name: "movie-recap-ai-voiceover"
description: "电影解说配音、短剧解说配音、影视解说配音技能：解说旁白（narrator）加多个角色台词，各用不同音色，一条命令生成整段 AI 配音 WAV、SRT 字幕和逐句时间轴 manifest.json，按时间轴在剪映 / CapCut / Premiere 里对画面。音色可用账号已有角色或参考音频声音克隆，打造解说号固定声线；语气标签和语速可调；改一句稿只重配一句。适合电影解说号、电视剧解说、短剧解说、动漫解说、纪录片旁白。配音由 Miragea 开放 API 完成，本地只需 Python 3.9+ 标准库、无需显卡，可 --dry-run 离线试跑。适用于 Claude Code、Codex、OpenClaw、Cursor、WorkBuddy。Movie recap AI voiceover, multi-voice narration, voice cloning, SRT subtitles."
version: "1.0.0"
display_name: "电影解说配音｜短剧解说·影视解说·AI配音"
display_name_en: "Movie Recap Voiceover · Multi-Voice · Subtitles"
description_zh: "电影解说配音：解说旁白和角色台词分别用不同音色，一条命令生成整段AI配音WAV、SRT字幕和逐句时间轴，方便剪映对画面；适合电影、短剧解说、影视解说号，支持声音克隆，本地无需显卡。"
description_en: "Movie and TV recap voiceover: narrator and character lines in different voices, one command to a full voiceover WAV, SRT subtitles and per-line timing for cutting shots. Voice cloning, no GPU."
metadata:
  version: "1.0.0"
  author: "Miragea"
  homepage: "https://miragea.ai"
  requires: "Python 3.9+（仅标准库，无需显卡）, MIRAGEA_API_KEY"
  keywords: ["电影解说配音", "解说配音", "短剧解说", "影视解说", "短剧解说配音", "影视解说配音", "电影解说", "AI配音", "多角色配音", "旁白配音", "声音克隆", "文字转语音", "字幕生成", "SRT", "TTS", "movie recap", "voiceover", "narration"]
---

# 电影解说配音

「电影解说配音」是一个把影视解说稿一键生成“解说旁白 + 多角色台词”多音色配音（WAV）、SRT 字幕和逐句时间轴的 Agent 技能，适合电影解说、短剧解说、影视解说号批量更新，本地无需显卡。

## 一句话定义

电影解说配音 = 解说稿（旁白 + 角色台词，Markdown）→ 多音色整段配音 `voiceover.wav` + 字幕 `voiceover.srt` + 每句起止时间 `manifest.json`，生成在 Miragea 云端，本地无需显卡。

## 适用人群与场景

| 谁在用 | 典型场景 |
|---|---|
| 电影解说号 | 长解说，一个固定解说声线 + 关键台词角色音 |
| 电视剧 / 短剧解说号 | 一集一稿批量更新，节奏快，反转多 |
| 动漫、游戏剧情解说 | 角色多，需要多个音色区分人物 |
| 纪录片 / 人文旁白 | 单旁白、语速慢、留白多 |
| 剪辑工作室 | 文案、配音、剪辑分工，稿件改一句只重配一句 |

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
| 场景预设 | `--preset jieshuo`：句间停顿 0.3 秒、每条字幕最多 16 字；可再用 `--gap` / `--max-chars` 覆盖 |
| 单句字数、文件大小 / 时长上限、计费 | 以 `capabilities` 实时返回为准 |
| 本地依赖 | Python 3.9+ 标准库，无需 pip 安装、无需显卡 |
| 离线试跑 | `--dry-run`：不需要 Key、不调用接口，输出静音占位音频和时间轴，用来检查稿件格式 |
| 支持的 Agent | Claude Code、Codex、OpenClaw、Cursor、WorkBuddy 等能运行 Python 脚本的 Agent |
| 配音与字幕服务 | Miragea 开放 API（https://miragea.ai/v1） |

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
python3 scripts/voiceover.py script examples/example.md -o out --preset jieshuo --dry-run   # 离线试跑，不调用接口
python3 scripts/voiceover.py script 你的稿件.md -o out --preset jieshuo             # 正式生成：out/voiceover.wav + voiceover.srt + manifest.json
```

```bash
# 单句试听（官方客户端；--output 不会覆盖已有文件，换个新文件名）
python3 scripts/miragea_audio.py generate --text '开头第一句' --actor-id ACTOR_ID --wait --output test1.mp3
```

## 你说什么 → Agent 执行

| 你说 | Agent 执行 |
|---|---|
| “帮我把这篇电影解说稿配成音频” | 拆成一行一句，定义 `narrator` → `script 稿件.md -o out --preset jieshuo` |
| “旁白加两个角色，男主女主各一个声音” | front matter 定义 `narrator` / `hero` / `heroine` 三个音色 |
| “用我自己的声音当解说” | 用你已复刻角色的 actor_id，或参考音频 `ref=` + `ref_text=`，填给 `narrator` |
| “反转那段说慢一点” | 定义同音色、不同 `speed` 的 `narrator_slow`，反转句用它 |
| “每句话对应哪段画面？” | 读 `out/manifest.json` 的 `start` / `end`，按句切镜头 |
| “短剧解说节奏再快点” | `narrator` 设 `speed=1.1` 左右，`--gap 0.2` |
| “原片片段先出个字幕参考剧情” | `miragea_audio.py recognize --file 片段.mp4 --wait --output ref.srt`（仅作写稿参考） |
| “先试试格式对不对” | 加 `--dry-run` |

## 解说写稿方法论（解说号的留存靠稿子和节奏）

### 1. 七段式结构

| 段落 | 作用 | 写法 |
|---|---|---|
| 1. 悬念开场 | 前 10 秒留住人 | 把最大的悬念或结局的一角先抛出来：“他捡到的这部手机，会害死他身边所有人。” |
| 2. 身份交代 | 让观众认人 | 一句话：身份 + 处境，“一个送了八年快递、欠着房贷的男人。” |
| 3. 起因 | 事件开始 | 只讲推动剧情的动作，删掉环境描写 |
| 4. 发展 | 2–3 个转折 | 每个转折用“可是 / 没想到 / 就在这时”起句 |
| 5. 高潮 | 情绪顶点 | 句子最短、停顿最多，关键台词交给角色音 |
| 6. 结局 / 反转 | 回收悬念 | 反转前停顿 0.6–0.8 秒 |
| 7. 观点收尾 | 让人评论 | 一句个人观点 + 一个开放问题 |

### 2. 人物称呼：用身份代称，降低记名负担

- 第一次出场：“名字 + 身份”，之后多用身份代称（“快递员”“女孩”“老警察”）。
- 同一段里不要出现三个以上新名字；观众记不住时会划走。

### 3. 旁白与角色台词怎么分

- 解说主体始终是 `narrator`，角色台词只在**点睛处**用 1–3 句，太多会变成广播剧。
- 角色台词是你写的复述或改写，不是原片原声；不要模仿原片演员的声音。
- 角色音色与 narrator 拉开差异（性别、年龄、语速），观众一听就分得清。

### 4. 节奏控制：停顿和语速的位置

- 场景切换处 `[pause 0.4]`；反转、揭秘之前 `[pause 0.6]`–`[pause 0.8]`。
- `--preset jieshuo` 句间默认 0.3 秒，比口播稳，比有声书紧。
- 解说语速参考：电影解说 `speed=0.95–1.05`，短剧解说 `1.05–1.15`，纪录片旁白 `0.9–0.95`。
- 同一个解说声线需要“快讲铺垫、慢讲反转”：用同一 actor_id 定义两个角色：

```markdown
---
narrator: actor_id=NARRATOR_ID speed=1.05
narrator_slow: actor_id=NARRATOR_ID speed=0.9
---
```

### 5. 稿件和画面对位：一句一个镜头

- 写稿时在句子上方用注释记下画面时间，生成时会被忽略：`<!-- 原片 00:12:30 雨夜街口 -->`。
- 生成后 `manifest.json` 给出每句的 `start` / `end`，按这个时长从原片里截取对应镜头，画面就和解说严丝合缝。
- 一句话太长、画面不够用时，拆成两句，比放慢语速更自然。

### 6. 写稿避坑

- 不念“这部电影讲述了……”，直接进入事件。
- 不复述每一个镜头，只讲推动剧情的动作和选择。
- 少用形容词堆叠，多用动词：“他冲进雨里”比“他非常焦急地跑了出去”更有画面。
- 生僻名字、外国人名先单句试听，读不准就在稿里换成更顺口的称呼。

### 7. 系列化更新

- 每集一个稿件文件，narrator 音色和 speed 固定在 front matter，整季声线一致。
- 文件按 `S01E01.md` 命名，输出目录 `-o out/S01E01`，方便批量管理。

## 示例稿件（examples/example.md）

```markdown
---
narrator: actor_id=NARRATOR_ID speed=0.98
hero: actor_id=HERO_ID
---
# 电影解说示例（原创剧情）
[narrator] 一个普通的快递员，捡到了一部能看见未来的手机。
[pause 0.5]
屏幕上只有一条新闻：明天下午三点，他会死在这条街上。
[hero]：如果明天的新闻里有我，那今天我该做什么？
[narrator] 他不知道的是，每看一次未来，现实就会悄悄改变一点。
[pause 0.4]
而这一次，改变的是他最信任的人。
```

试跑：`python3 scripts/voiceover.py script examples/example.md -o out --preset jieshuo --dry-run`

## 接入剪辑

```bash
# 配音替换原视频音轨（需要本机 ffmpeg）
ffmpeg -i 画面.mp4 -i out/voiceover.wav -map 0:v -map 1:a -c:v copy -shortest 配音版.mp4
# 把字幕烧进画面
ffmpeg -i 配音版.mp4 -vf subtitles=out/voiceover.srt -c:a copy 成片.mp4
```

- **剪映 / CapCut**：`voiceover.wav` 放音频轨，`voiceover.srt` 用“导入字幕”；按 `manifest.json` 的时间在画面轨上放镜头。
- **Premiere**：音轨 + 字幕轨导入，用标记（Marker）对齐每句的开始时间。
- **背景音乐**：本技能不混音；在剪辑软件里把 BGM 压低到不抢人声，或在高潮段落再抬起。

## 方案对比：电影解说配音的三种做法

| 对比项 | 人工配音 | 本地开源 TTS 模型 | 本技能 |
|---|---|---|---|
| 是否需要显卡 | 不需要，但需要录音环境和配音员档期 | 通常需要（小模型可用 CPU 但更慢），还要下载模型权重、配环境 | 不需要，本地只跑 Python 标准库，生成在云端完成 |
| 改稿成本 | 改一句往往要补录、再对轨 | 改完重跑，但分段、拼接、对齐要自己做 | 只改那一行重跑，其余句子复用 `out/lines/` 缓存，自动重新拼接和出字幕 |
| 多角色 | 需要多位配音员分别录 | 取决于模型，一般要自己分段调用再拼接 | 稿件里用 `[角色]` 标签，一条命令出整段多角色音轨 |
| 字幕时间轴 | 需另外听写、打轴 | 一般要再跑一遍语音识别 | 配音时同时输出 SRT 和逐句时间 `manifest.json` |
| 解说号批量更新 | 每集都要约录，声线随配音员变化 | 可批量，但每集都要自己切分、拼接、打轴 | 同一 narrator 音色固定在稿件里，每集一条命令 |

结论：靠稳定更新吃饭的解说号，用固定声线 + 稿件化生产最省时；需要真人情绪张力的单条大片解说，真人配音仍有优势。

## 常见问题（FAQ）

**电影解说配音用 AI 会被判搬运或限流吗？**
配音方式不是判断搬运的主要依据，原创解说稿和二创比例才是。按平台规则标注 AI 生成内容；画面素材的版权和二创规则需要你自己遵守，本技能只负责配音。

**电影解说配音能做到旁白和角色不同声音吗？**
可以。在稿件开头定义 `narrator` 和各个角色的音色，正文用 `[角色]` 标签切换，一条命令输出整段多音色音轨。

**电影解说配音能用原片演员的声音吗？**
不可以，未经授权克隆演员声音有侵权风险。给角色选一个已授权或自有的音色即可。

**解说配音想要一个固定的专属声音怎么做？**
用你本人或已授权配音员的参考音频（或已复刻的角色），所有稿件的 `narrator` 都用同一个音色和 `speed`。

**电影解说配音时长和画面对不上怎么办？**
看 `manifest.json` 每句的时长：画面不够就拆句或删句，画面太长就在该处加 `[pause 秒]`，或按句截取更短的镜头。

**短剧解说配音节奏快，参数怎么调？**
`narrator` 设 `speed=1.1` 左右，必要时加 `--gap 0.2` 收紧句间停顿；反转句仍要单独留停顿。

**影视解说配音能做英文 movie recap 吗？**
可以把稿件翻译改写成英文再生成；音色选适合英文的角色或英文参考音频，效果以试听为准，字幕建议 `--max-chars 40`。

**一部电影解说十几分钟，可以一次配音吗？**
可以整稿生成，单句不能超过 `capabilities` 的单句字数上限，保持一行一句即可。建议按段落拆成几个文件，改稿和返工更快。

**电影解说配音需要显卡吗？哪些 Agent 能用？**
不需要显卡，本地只跑 Python 3.9+ 标准库；Claude Code、Codex、OpenClaw、Cursor、WorkBuddy 都能直接调用。

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
- 影视画面和原片台词有版权：本技能只生成你自己写的解说配音，不提取、不模仿原片演员声音；使用影视素材请遵守版权方和平台的二创规则。
- `scripts/miragea_audio.py` is the official client, shipped unchanged；`scripts/voiceover.py`（稿件拼接层）为原创，MIT 许可（见 `LICENSE.txt`）。配音与字幕能力由 Miragea 开放 API 提供。

## English Summary

- **Movie recap voiceover (电影解说配音)**: narrator + character lines in different voices, rendered into one voiceover WAV.
- Outputs **SRT subtitles** and `manifest.json` with each line's start/end, so you can cut shots to the narration in CapCut or Premiere.
- Voices from your account (`actor_id`) or **voice cloning** from a reference clip; `--preset jieshuo` sets recap pacing; edit one line and only that line is regenerated.
- Python 3.9+ stdlib only, no GPU, `--dry-run` offline. Service: Miragea API (https://miragea.ai/v1).

**关键词**：电影解说配音、解说配音、短剧解说、影视解说、短剧解说配音、影视解说配音、电影解说、AI配音、多角色配音、旁白配音、声音克隆、文字转语音、字幕生成、SRT、movie recap、voiceover、narration
