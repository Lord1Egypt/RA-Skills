---
name: high-end-product-video
slug: high-end-product-video
version: 2.2.0
displayName: 高品质短视频制作 · 声画同步工业级流水线
summary: 用旁白真实波形反推画面时长，根除抢拍与空转。一条脚本化流水线从旁白直达成片：确定性帧渲染、侧链闪避混音、BS.1770-4 响度母带（-16 LUFS / -1.0 dBTP）、九项可执行质量门禁，交付前硬性失败即阻断。不限题材，产品宣传、知识讲解、教程演示、品牌故事通用。
description: 高品质短视频工业级制作工作流，适用于一切旁白驱动的短视频：产品宣传片（任意品类，不限科技）、知识讲解、教程演示、品牌故事、活动回顾、个人 IP 口播。以声音时钟逆推为核心，用 TTS 实际波形反推画面时长，消除抢拍与空转；含动量连续性视觉规范、确定性帧渲染、侧链闪避混音、BS.1770-4 响度母带、可机械执行的质量门禁。当需要制作宣传片、讲解视频、教程视频、发布会特性视频、需要声画精确对齐的短视频时使用。触发词包括「做宣传片」「产品视频」「讲解视频」「教程视频」「短视频制作」「声画同步」「混音」「视频流水线」「product video」「promotional video」。
tags: [ai, video, short-video, product-video, promo, tts, loudness, lufs, bs1770, playwright, ffmpeg, skill, agent]
license: MIT
---

# 高品质短视频制作工作流

核心主张只有一条：**画面时长不能拍脑袋定，必须由旁白的真实波形反推。**

绝大多数短视频的抢拍、空转、人声被 BGM 盖住，根源都是顺序反了——先定画面再拿音频硬凑。本工作流把顺序倒过来，并用四个脚本把整条流水线固化下来，每个环节都有可度量的质量基线。

**不限题材。** 产品宣传（任意品类）、知识讲解、教程演示、品牌故事、活动回顾、个人 IP 口播——只要是「旁白驱动」的短视频，流程完全一样，变的只有旁白文本和镜头类型。

---

## 一、五个阶段与对应脚本

| 阶段 | 做什么 | 用什么 |
|---|---|---|
| 1. 时间轴 | 生成/提取旁白，用真实波形算出每个镜头的画面时长 | `scripts/tts_timeline.py` |
| 2. 渲染 | 按时间轴驱动 HTML 模板逐帧截图，动量规范全部内置 | `scripts/render_frames.py`（需 Playwright）|
| 3. 混音 | 人声铺轨 + BGM 侧链闪避 + 响度母带处理 | `scripts/audio_engine.py` |
| 4. 合成 | 帧序列 + 母带 → H.264 成片 | `scripts/assemble_video.py`（需 FFmpeg）|
| 5. 门禁 | 交付前拦截硬伤，全绿才许交付 | `scripts/verify_quality.py` |

`media_lib.py`（WAV/PNG/灰度解码等共享原语）和 `loudness.py`（BS.1770-4 响度与真峰值）是被依赖的库，不单独运行。

---

## 二、开工前先对齐四件事

不同题材只影响这四件事的答案，不影响流程：

1. **受众**：给谁看（消费者 / 开发者 / 学生 / 客户）
2. **平台与画幅**：小红书/抖音/视频号（9:16）、B站/公众号/官网（16:9）、方形（1:1）
3. **核心记忆点（Hook）**：观众看完必须记住的那一句话
4. **题材类型**：宣传 / 讲解 / 教程 / 故事——决定旁白写法与镜头类型搭配

旁白写法按题材调整，原则不变：**大白话拆解，别堆术语**。讲解类用「X 分钟讲透」结构，宣传类用「痛点 → 方案 → 证据 → 行动」结构，教程类用「步骤 → 演示 → 验收」结构。

---

## 三、声音时钟逆推（本工作流的核心）

### 为什么

先定画面时长再塞音频，必然出现两种翻车：话没说完画面已经切走，或者画面还在播但话已经说完空转两秒。

正确顺序：生成旁白 → 提取真实波形起止点 → 反推画面时长。

$$T_{\text{scene}} = T_{\text{voice}} + T_{\text{pre-padding}} + T_{\text{post-padding}}$$

- $T_{\text{pre-padding}} = 0.6\text{s}$：让观众看清标题和画面，BGM 铺底起手，**根除抢跑**
- $T_{\text{post-padding}} = 0.4\text{s}$：留出纯净缝隙触发转场音效，不压迫人声

### 怎么做

```bash
# 1. 准备旁白文本，每行一句（examples/narration.txt 有样例）
# 2. 生成音频并算时间轴（离线模式，不需要任何 API Key）
python3 scripts/tts_timeline.py narration.txt --mode offline --out timeline.json

# 3. 看一眼时间轴对不对
cat timeline.json
```

输出时间轴包含每个镜头的 `voice_start/voice_end/voice_duration`（VAD 提取）与 `scene_start/scene_end/scene_duration`（反推结果）。渲染时每个镜头按 `scene_duration` 截帧，人声在镜头开始 0.6 秒后进入。

### 语音引擎

| 模式 | 说明 | 依赖 |
|---|---|---|
| `offline`（默认）| 本地合成占位音频（机器人嗡鸣，波形时长与字数成正比），用于跑通流水线与测试 | 无 |
| `edge` | edge-tts 高质量语音 | `pip install edge-tts` |
| `existing` | 用你已有的 wav 文件，只算时间轴 | 无 |

**密钥一律从环境变量读取，脚本里不出现任何明文 key。** 接第三方 TTS（MiniMax、Azure、OpenAI 等）时，用 `--tts-cmd` 指定命令，密钥走你自己的环境变量，本脚本不接触：

```bash
python3 scripts/tts_timeline.py narration.txt --mode edge --voice zh-CN-YunxiNeural
python3 scripts/tts_timeline.py narration.txt --mode existing --audio-dir ./my_voice
python3 scripts/tts_timeline.py narration.txt \
  --tts-cmd 'your-tts-cli --text {text} --out {out}'   # 任意 TTS，密钥在它的环境变量里
```

---

## 四、镜头类型与题材搭配

默认模板内置四种镜头类型，`--visuals` 每镜头指定一个：

| 类型 | 长什么样 | 适合 |
|---|---|---|
| `title` | 大标题 + 标签 + 说明，词级遮罩 reveal | 开场钩子、章节页、金句收尾 |
| `feature` | 左文右卡（产品卡/界面 mockup + 标签）| 卖点讲解、功能演示、步骤说明 |
| `metric` | 巨大数字 + 单位 + 说明 | 数据证据、成绩展示、前后对比 |
| `outro` | Logo 落版 + 标语，缓慢推镜 | 结尾行动号召、品牌收尾 |

按题材搭配：

- **产品宣传**：title → feature ×2~3 → metric → outro
- **知识讲解**：title（抛问题）→ feature ×2~3（拆概念）→ metric（一个震撼数字）→ outro
- **教程演示**：title（目标）→ feature ×N（步骤）→ metric（成果）→ outro
- **活动回顾/故事**：title → feature ×N（事件）→ outro

---

## 五、渲染：确定性帧序列

```bash
python3 scripts/render_frames.py \
  --timeline timeline.json \
  --template templates/scenes.html \
  --visuals visuals.json \
  --out frames --fps 30
```

三个设计要点：

1. **确定性优先**。每帧时间戳就是 `t = n/fps`，模板的 `__render(t)` 是纯函数——同样 t 在任何机器上画出同一帧。不依赖真实时钟，不会掉帧，可复现。
2. **契约简单**。模板从 URL 参数拿场景数据，暴露 `window.__render(t)`，渲染器逐帧调用。改造模板只需要守这个契约（详见 `references/design-system.md` 第八节）。
3. **自适应并发**。多个 Page 并行，按镜头聚合任务摊薄导航开销；白屏（截图体积过小）自动重试。

画幅 `--preset landscape|vertical|square|wide` 或自定义宽高；主题 `--theme editorial|dark`；`--dry-run` 每镜头只渲 1 帧快速验证。

**帧格式默认 JPEG q92**：单帧 50ms/93KB，比 PNG 快 15 倍。成片是 4500kbps H.264，JPEG q92 中间帧对它完全透明。要像素级无损就加 `--format png`（慢 15 倍，门禁的死帧检查无需转码）。

---

## 六、视觉规范：动量连续性

画面任何一帧都不允许完全静止。主体进场用 Apple 标准流体曲线 `easeOutExpo`（0.9s），停稳后进入漂移巡航态。**原始公式的 Scale 项会无限增长，必须改成有界振荡**，而且要叠双频率：

```javascript
// 错误：t 增大时 scale 会一直变大，长镜头下元素会飞出画面
// scale = baseScale + t * 0.012

// 正确：双不可通约频率叠加 + clamp。单正弦在极值点速度为零，
// 逐帧检测会抓到"几乎静止"的帧；叠一个频率后合速度永不为零。
const drift  = Math.sin(t * 0.8) * 0.013 + Math.sin(t * 1.37) * 0.008;
const driftY = clamp(Math.cos(t * 1.2) * 5 + Math.sin(t * 0.93) * 4, -10, 10);
```

其余规范（景深视差、字体排版、质感三件套、性能基线）见 `references/design-system.md`，默认模板全部内置，改造模板时对照修改。

---

## 七、声学：侧链闪避混音 + 响度母带

```bash
python3 scripts/audio_engine.py \
  --timeline timeline.json \
  --bgm ./bgm.wav \
  --out master.wav
```

脚本做的事：

1. 按时间轴把各段人声铺到正确位置（镜头起点 + 0.6s）
2. 计算人声能量包络，生成 BGM 闪避增益曲线：人声期间衰减到 **18%**，停顿后 **250ms** 内平滑恢复到 **35%**
3. 母带处理（默认 `--lufs-mode lufs`）：K 加权测量集成响度 → 静态增益归一到 **-16 LUFS** → 前瞻限幅把真峰值压到 **-1.0 dBTP** → 复测补偿，最多 4 轮收敛

响度标准（全文统一，不再前后打架）：

- 集成响度 **-16 LUFS**（±1 LU 容差）
- 真实峰值上限 **-1.0 dBTP**（4x 过采样测量）
- 采样率 **48kHz**

要旧行为就加 `--lufs-mode peak --target -1.0`（峰值归一）。

### 关于 BGM

脚本不自带 BGM，也不联网下载。你需要自备一个无版权风险的音频文件。没有 BGM 时可以加 `--no-bgm`，只输出人声母带。

---

## 八、合成

```bash
python3 scripts/assemble_video.py --frames frames --audio master.wav --out final.mp4 --verify
```

编码参数：`libx264 -crf 16 -maxrate 4500k -bufsize 9000k -preset slow -pix_fmt yuv420p -profile:v high -level 4.1 -movflags +faststart`，音频 `aac 192k 48kHz`。`-t` 以帧序列时长为准。

`--verify` 会把成片音轨解码回 WAV，跑一遍 BS.1770-4 复测（AAC 通常让响度掉 0.1~0.3 LU，在容差内算达标）。**不要跳过**：它抓的是「母带达标、成片却漂了」的静默失败。

---

## 九、质量门禁

交付前必须跑，任一硬性检查失败即阻断：

```bash
python3 scripts/verify_quality.py \
  --timeline timeline.json --audio master.wav \
  --frames frames --fps 30 --lufs -16 --strict
```

| 检查项 | 判定标准 | 级别 |
|---|---|---|
| `AUDIO_DECODABLE` | WAV 可读、时长 > 0、采样率/位宽合法 | 硬 |
| `TRUE_PEAK_CEILING` | 真峰值（4x 过采样）<= -1.0 dBTP | 硬 |
| `LOUDNESS_TARGET` | 集成响度（门控）命中目标 ±1 LU | 硬（需 `--lufs`）|
| `NO_SPEECH_OVERLAP` | 相邻人声间隙 >= 0.3s | 硬 |
| `TIMELINE_CONTINUOUS` | 时间轴无断档、无重叠、总时长自洽 | 硬 |
| `NO_TOFU_CHARS` | 字幕不含乱码方块字符 | 硬（需 `--subtitle`）|
| `FRAME_SEQUENCE` | 帧数/编号连续性/尺寸一致 | 硬（需 `--frames`）|
| `MOTION_ALIVE` | 两帧跨度灰度差 >= 阈值（排除转场窗口）| 软（需 `--frames`）|
| `AUDIO_COVERS_TIMELINE` | 母带不短于时间轴总时长 | 软 |

**这些是可机械执行的检查，替代「严禁偷懒」这类口号。** 约束写进脚本才会真正生效，写在文档里只会被跳过。

### 已修正的原版缺陷

1. `NO_TOFU_CHARS` 原版写作「不得含 '▢', '', '?'」，其中**空字符串 `''` 会让检查 100% 误报**。现在用明确的乱码字符集：`\uFFFD`（替换字符）、`\u25A1`、`\u25A0`（方块）等，不再用空串。
2. 原版同时出现「True Peak -1.0 dBFS」和「门禁 Max Peak <= -0.5 dB」、「4.5+ Mbps」和「>= 3500 kbps」两组互相矛盾的数字。现在全文统一为 **-1.0 dBTP** 和 **4500 kbps**。
3. 原版硬编码了 MiniMax API Key（`os.environ.get('MM_KEY', 'sk-...')`）。现在脚本内无任何明文 key，第三方 TTS 通过 `--tts-cmd` 接入，密钥只存在于你的环境变量里。
4. 动量公式 `scale = baseScale + t * 0.012` 无界，长镜头元素飞出画面；改为双频有界振荡 + clamp。
5. 原版只有口号没有门禁。现在九项检查全部可执行，且 `MOTION_ALIVE` 用两帧跨度比对（单帧比对会把振荡极值点的正常微动误判成死帧）。

---

## 十、执行 SOP

1. **对齐方向** — 问清受众、平台、画幅、核心记忆点、题材类型，再动工
2. **写旁白** — 按题材选结构，大白话拆解，每行一句
3. **跑时间轴** — `tts_timeline.py`，拿到真实波形时长
4. **配视觉** — 写 `visuals.json`（每镜头的类型与文案），`--dry-run` 验证
5. **渲染帧序列** — `render_frames.py`，JPEG 默认
6. **混音** — `audio_engine.py` 生成 -16 LUFS / -1.0 dBTP 母带
7. **合成** — `assemble_video.py --verify`
8. **过门禁** — `verify_quality.py --strict`，全绿才交付
9. **交付** — 成片；讲解/教程类建议附上交互演示页或源码，形成「看视频 → 玩页面 → 转化」闭环

---

## 十一、能力边界（说清楚，别吹）

- 本工作流**不生成视频素材**：画面来自你写的 HTML 模板 + Playwright 截帧，不是文生视频。要 AI 生成画面请另配工具，把结果当帧序列喂给 `assemble_video.py`
- 标称能力是**声画精确对齐 + 可度量交付基线**（-16 LUFS / -1.0 dBTP / 4500kbps / 无死帧 / 无人声重叠），不是「Apple 级」「广播级」。Playwright 截帧很难稳定跑满 60fps，离广播级有距离
- 脚本不联网、不内置密钥、不自带 BGM 和字体；唯一的外部依赖是 Playwright（渲染）与 FFmpeg（合成），都需要你自己装
