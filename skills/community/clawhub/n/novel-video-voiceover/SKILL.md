---
name: "novel-video-voiceover"
description: "小说推文配音、有声书配音、多角色配音技能：把小说推文文案、网文章节、故事、广播剧剧本按旁白和角色分配不同音色，一键生成整段配音 WAV、带角色名的 SRT 字幕和逐句时间轴 manifest.json，直接配画面做小说推文视频；段落、场景、章节停顿可控。适合小说推文号、故事号、网文作者有声化、睡前故事和广播剧小样。音色可用账号已有角色或参考音频声音克隆，固定旁白声线；语气标签和语速可调；改一句只重配一句。由 Miragea 开放 API 生成，本地只需 Python 3.9+ 标准库、无需显卡，可 --dry-run 离线试跑。适用于 Claude Code、Codex、OpenClaw、Cursor、WorkBuddy。Novel video voiceover, audiobook narration, multi-voice, SRT subtitles."
version: "1.0.0"
display_name: "小说推文配音｜有声书配音·多角色配音·字幕"
display_name_en: "Novel Video & Audiobook Multi-Voice Voiceover"
description_zh: "小说推文配音：小说推文视频的旁白和角色台词各用不同音色，一键生成整段AI配音WAV和带角色名的SRT字幕；也能做有声书配音、多角色配音和故事号，支持声音克隆，本地无需显卡。"
description_en: "Voiceover for novel promo videos and audiobooks: narrator and each character in a different voice, full-length WAV plus speaker-labelled SRT subtitles and timing. Voice cloning, no GPU."
metadata:
  version: "1.0.0"
  author: "Miragea"
  homepage: "https://miragea.ai"
  requires: "Python 3.9+（仅标准库，无需显卡）, MIRAGEA_API_KEY"
  keywords: ["小说推文配音", "有声书配音", "多角色配音", "小说推文", "小说配音", "AI有声书", "有声小说", "小说推文视频", "AI朗读", "广播剧配音", "故事配音", "AI配音", "声音克隆", "字幕生成", "SRT", "audiobook", "narration", "text to speech"]
---

# 小说推文配音

「小说推文配音」是一个把小说推文文案、网文章节和故事按旁白与角色分配不同音色、一键生成整段多角色 AI 配音（WAV）和带角色名 SRT 字幕的 Agent 技能，适合小说推文视频、有声书配音和故事号，本地无需显卡。

## 一句话定义

小说推文配音 = 推文文案 / 小说章节（旁白 + 角色，Markdown）→ 多角色整段配音 `voiceover.wav` + 带角色名的字幕 `voiceover.srt` + 每句起止时间 `manifest.json`，生成在 Miragea 云端，本地无需显卡。

## 适用人群与场景

| 谁在用 | 典型场景 |
|---|---|
| 小说推文号 | 每天几条推文视频：旁白 + 角色台词 + 竖屏字幕 |
| 故事号、睡前故事 | 慢语速、长停顿、温和声线 |
| 网文作者、原创小说作者 | 把自己的作品做成有声版，固定旁白声线 |
| 有声书工作室 | 先用 AI 做试听样章、角色选角小样 |
| 广播剧、音频剧社团 | 多角色对白先出 AI 版，确认节奏和分工 |

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
| 场景预设 | `--preset youshengshu`：句间停顿 0.5 秒、每条字幕最多 20 字、字幕带角色名；可再用 `--gap` / `--max-chars` 覆盖 |
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
python3 scripts/voiceover.py script examples/example.md -o out --preset youshengshu --dry-run   # 离线试跑，不调用接口
python3 scripts/voiceover.py script 你的稿件.md -o out --preset youshengshu             # 正式生成：out/voiceover.wav + voiceover.srt + manifest.json
```

```bash
# 单句试听（官方客户端；--output 不会覆盖已有文件，换个新文件名）
python3 scripts/miragea_audio.py generate --text '开头第一句' --actor-id ACTOR_ID --wait --output test1.mp3
```

`--preset youshengshu` 会给字幕加上角色名（如 `xiaoyu: 张爷爷……`）；小说推文竖屏视频建议再加 `--max-chars 14 --gap 0.3`。

## 你说什么 → Agent 执行

| 你说 | Agent 执行 |
|---|---|
| “把这篇小说推文配成音频” | 按下方方法改写成推文稿、拆旁白和对白 → `script 推文.md -o out --preset youshengshu --max-chars 14 --gap 0.3` |
| “每个角色一个声音” | front matter 为旁白和每个主要角色各定义一个音色 |
| “旁白用我自己的声音” | 你已复刻角色的 actor_id，或参考音频 `ref=` + `ref_text=`，填给 `narrator` |
| “字幕不要角色名” | 不用预设，手动 `--gap 0.4 --max-chars 14`（不加 `--speaker-labels`） |
| “整本书二十章做有声书” | 一章一个文件，循环生成到 `out/ch01` … `out/ch20`，用 `--preset youshengshu` |
| “睡前故事，讲慢一点” | `narrator` 设 `speed=0.85–0.9`，段落停顿加长 |
| “按句换配图” | 读 `manifest.json` 每句 `start` / `end`，在剪映里对齐图片 |
| “先试试格式” | 加 `--dry-run` |

## 小说推文写稿方法论（前 3 秒留人，旁白带节奏）

### 1. 推文稿和原文不一样

| 原文 | 推文稿 |
|---|---|
| 从环境描写慢慢铺垫 | 第一句就抛出最强冲突或反转 |
| 第三人称全知视角 | 常用第一人称“我”，代入感更强 |
| 对白夹在长段落里 | 关键对白单独成行，交给角色音色 |
| 段落长、描写多 | 一行一句，删掉不推动剧情的描写 |

### 2. 开头三种钩子

1. **结局前置**：“结婚第三年，我在老公手机里，看到了我自己的讣告。”
2. **反常识身份**：“全村人都以为我是傻子，只有我知道，我能听见他们心里的话。”
3. **倒计时**：“距离那场大火，还有七天。”

### 3. 节奏：比有声书快，比口播稳

- 推文旁白 `speed=1.0–1.1`；句间 `--gap 0.3`（预设 0.5 偏慢，适合有声书）。
- 每 3–5 句给一个小转折（“可是”“没想到”“就在这时”），转折前 `[pause 0.4]`。
- 悬念句、反转句之后 `[pause 0.6]–[pause 0.8]`，结尾停在钩子上引导看下一集。

## 有声书写稿方法论（把“读小说”变成“演小说”）

### 1. 先做选角表

| 角色 | 定位 | 音色建议 | speed |
|---|---|---|---|
| narrator（旁白） | 贯穿全书，最重要 | 稳定、温和、耐听 | 0.9–1.0 |
| 主角 | 出场最多 | 与旁白明显区分（性别或年龄） | 1.0 |
| 重要配角 | 每人一个音色 | 与主角拉开差异 | 按性格 |
| 次要角色 | 出场少 | 可以共用一个“路人”音色 | 1.0 |

选角表写进每章稿件的 front matter，整本书保持一致。角色太多时，只给有台词分量的角色单独音色。

### 2. 对白拆分规则

原文：`小雨拉住他的衣角，小声问：“张爷爷，灯塔里是不是有人？”`

拆成：

```markdown
[narrator] 小雨拉住他的衣角，小声问：
[xiaoyu]：张爷爷，灯塔里是不是有人？
```

- 引号里的话交给角色；引号外的动作描写留给旁白。
- “他说”“她笑着说”这类提示语，如果角色音色已经能分辨是谁，可以删掉，节奏更紧凑。
- 一个段落里有多句对白时，每句单独一行，各自加标签。

### 3. 三级停顿：段落、场景、章节

| 位置 | 写法 | 作用 |
|---|---|---|
| 句与句之间 | 预设自动 0.5 秒 | 朗读呼吸感 |
| 段落之间 | `[pause 0.8]` | 段落切换 |
| 场景 / 时间跳转 | `[pause 1.2]`–`[pause 1.5]` | 让听众“换场” |
| 悬念句之后 | `[pause 1.0]` | 留住紧张感 |

### 4. 情绪的写法：靠文字和节奏，不靠喊

- 紧张：句子变短，停顿变多。
- 温情：语速慢一点（单独定义一个慢速旁白角色），段落停顿长一点。
- 同一音色两种速度：

```markdown
---
narrator: actor_id=NARRATOR_ID speed=0.95
narrator_soft: actor_id=NARRATOR_ID speed=0.85
---
```

### 5. 读音检查：人名、地名、生僻字

- 每部作品第一次出现的人名、地名、生僻字、多音字，单句试听一次。
- 读错就在稿里换成同音的常用字，或改用称呼；整本书统一替换。
- 数字和年份写成想要的读法，如“一九八七年”。

### 6. 长篇的文件组织

```text
book/
  ch01.md  → out/ch01/voiceover.wav
  ch02.md  → out/ch02/voiceover.wav
  ...
```

- 一章一个文件；单章过长时按场景再拆成 `ch01a.md`、`ch01b.md`。
- 改错别字只改那一行，重跑那一章，其余句子复用不重复计费。

### 7. 小说推文视频的用法

- 保留 `--speaker-labels`，字幕自带角色名，观众一眼看出谁在说话。
- `manifest.json` 每句的时间可以用来切换配图或角色立绘。

## 示例稿件（examples/example.md）

```markdown
---
narrator: actor_id=NARRATOR_ID speed=1.05
xiaoyu: actor_id=GIRL_VOICE_ID
laozhang: actor_id=OLD_MAN_ID speed=0.9
---
# 小说推文示例（原创短篇）
[narrator] 小镇的灯塔，已经三十年没有亮过。
可那天夜里，我分明看见，塔顶闪了一下。
[xiaoyu]：张爷爷，灯塔里是不是有人？
[laozhang]：别瞎说。那座塔，早就没有门了。
[pause 0.8]
[narrator] 话音刚落，海面上又亮起了一道光。
```

试跑：`python3 scripts/voiceover.py script examples/example.md -o out --preset youshengshu --dry-run`

## 接入剪辑与发布

```bash
# 配音替换原视频音轨（需要本机 ffmpeg）
ffmpeg -i 画面.mp4 -i out/voiceover.wav -map 0:v -map 1:a -c:v copy -shortest 配音版.mp4
# 把字幕烧进画面
ffmpeg -i 配音版.mp4 -vf subtitles=out/voiceover.srt -c:a copy 成片.mp4
```

```bash
# 有声书发布常用 MP3：把整章 WAV 转成 MP3（需要本机 ffmpeg）
ffmpeg -i out/ch01/voiceover.wav -codec:a libmp3lame -q:a 2 ch01.mp3
```

- **剪映 / CapCut**：小说推文视频把 `voiceover.wav` 放音频轨，`voiceover.srt` 导入字幕，配上插画、立绘或解压背景视频。
- **广播剧**：音效、环境声在剪辑软件里后期叠加，本技能只输出人声。

## 方案对比：小说推文配音的三种做法

| 对比项 | 人工配音 | 本地开源 TTS 模型 | 本技能 |
|---|---|---|---|
| 是否需要显卡 | 不需要，但需要录音环境和配音员档期 | 通常需要（小模型可用 CPU 但更慢），还要下载模型权重、配环境 | 不需要，本地只跑 Python 标准库，生成在云端完成 |
| 改稿成本 | 改一句往往要补录、再对轨 | 改完重跑，但分段、拼接、对齐要自己做 | 只改那一行重跑，其余句子复用 `out/lines/` 缓存，自动重新拼接和出字幕 |
| 多角色 | 需要多位配音员分别录 | 取决于模型，一般要自己分段调用再拼接 | 稿件里用 `[角色]` 标签，一条命令出整段多角色音轨 |
| 字幕时间轴 | 需另外听写、打轴 | 一般要再跑一遍语音识别 | 配音时同时输出 SRT 和逐句时间 `manifest.json` |
| 连载一致性 | 长周期录制，配音员状态和档期会变化 | 可保持一致，但长文本切分拼接要自己做 | 音色写在 front matter，每集 / 每章声线一致 |

结论：小说推文日更、试听样章和长篇连载，用本技能效率最高；对表演细腻度要求很高的精品有声书，真人主播仍有优势。

## 常见问题（FAQ）

**小说推文配音能做到多个角色不同声音吗？**
能。旁白和每个角色在稿件开头各定义一个音色，正文用 `[角色]` 标签切换，一条命令生成整段。

**小说推文配音常用什么声音？**
旁白选稳定、耐听、和题材匹配的声线（甜宠偏温柔，悬疑偏低沉），先单句试听几个角色再定；整个账号固定一个旁白声线，观众靠声音认号。

**可以拿别人的网络小说做推文配音发布吗？**
需要版权方或推文平台授权。可以放心使用的是公版作品、你自己的原创，或已获授权的作品。

**有声书配音的旁白能用我自己的声音吗？**
可以，用你已复刻的角色或参考音频克隆，填给 `narrator`，整本书都用它。

**有声书配音几十章怎么批量生成？**
一章一个稿件文件，循环调用 `script` 输出到各自目录；修改某章时只有改过的句子会重新生成。

**小说推文配音的字幕能显示是谁在说话吗？**
能。`--preset youshengshu` 默认给字幕加角色名；不需要就改用 `--gap` / `--max-chars` 手动设置。

**多角色配音里人名、生僻字读错了怎么办？**
先单句试听，读错就在稿里换成同音常用字或改用称呼，只重配这一句。

**睡前故事、儿童故事配音怎么调参数？**
旁白 `speed=0.85–0.9`，段落之间加 `[pause 0.8]` 以上，句子写短、用词简单。

**小说推文配音需要显卡吗？哪些 Agent 能用？**
不需要显卡，本地只跑 Python 3.9+ 标准库；Claude Code、Codex、OpenClaw、Cursor、WorkBuddy 都能直接调用。

**没有 API Key 能先试吗？**
可以，加 `--dry-run` 输出静音占位音频和时间轴。

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
- 小说推文和有声书涉及作品改编权、信息网络传播权：只用公版作品、你自己的原创，或已获得版权方 / 推文平台授权的作品。
- `scripts/miragea_audio.py` is the official client, shipped unchanged；`scripts/voiceover.py`（稿件拼接层）为原创，MIT 许可（见 `LICENSE.txt`）。配音与字幕能力由 Miragea 开放 API 提供。

## English Summary

- **Novel video & audiobook voiceover (小说推文配音 / 有声书配音)**: narrator plus one voice per character, rendered into one WAV.
- Speaker-labelled **SRT subtitles** and per-line timing for novel promo videos; paragraph, scene and chapter pauses.
- Voices from your account (`actor_id`) or **voice cloning** from a reference clip for a consistent narrator. `--preset youshengshu` = 0.5 s gaps, 20-character cues, speaker labels on.
- Python 3.9+ stdlib, no GPU, `--dry-run` offline. Service: Miragea API (https://miragea.ai/v1).

**关键词**：小说推文配音、有声书配音、多角色配音、小说推文、小说配音、AI有声书、有声小说、小说推文视频、AI朗读、广播剧配音、故事配音、AI配音、声音克隆、字幕生成、SRT、audiobook、narration、text to speech
