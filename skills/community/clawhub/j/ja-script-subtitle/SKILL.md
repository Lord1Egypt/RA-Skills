---
name: ja-script-subtitle
slug: ja-script-subtitle
displayName: 日语台本字幕工坊
version: 1.0.0
description: >
  日语有声作品（ASMR / 音声 / 同人音声）字幕流水线：把「日文台本 + 音频」做成
  日文原文 / 纯中文 / 双语 SRT，可选烧录中文竖屏视频。
  当用户提供日语台本(txt)配音频(mp3/wav)、或要求「配字幕 / 做中文字幕 / 生成 SRT /
  烧录中文视频 / 把台本和音对上时间轴」时使用。
  无台本、只有音频时也可用（退化为纯 ASR 转写 + 人工翻译），但精度低于有台本。
  NOT for: 视频字幕的图形化编辑、非日语语种、音乐歌词校对。
metadata:
  emoji: "🎧"
  category: "media"
  tags: ["subtitle", "srt", "whisper", "asmr", "japanese", "ffmpeg", "forced-alignment"]
---

# 日语台本字幕流水线

## 一句话原理

> **字幕文本 100% 取自台本（零识别错误），只让 ASR 负责「什么时候说」。**

台本与 ASR 文本各自归一化成字符流 → 字符级 diff 求匹配 → 把匹配到的字符映射回
ASR 的**词级**时间戳（词内按字符位置线性插值）。既有台本的准确文字，又有词级的时间精度。

## 何时用 / 不用

| 场景 | 用不用 |
|---|---|
| 给日文台本 + 音频，要中文字幕 | ✅ 本流程 |
| 只给音频，要字幕 | ✅ 但退化为纯 ASR（Step 2 用 ASR 分段直接当字幕，翻译后人工润色） |
| 要中文烧录视频 | ✅ Step 4 |
| 要编辑已有视频的字幕样式 | ❌ 走普通 ffmpeg 处理 |

## 环境准备（一次性）

```bash
bash scripts/setup_env.sh
```

三个必须绕过的坑（脚本已处理）：

1. 系统 Python 是 PEP 668 externally-managed → 建 venv `/opt/wenv`，**不要** `--break-system-packages`（会撞 `typing_extensions` RECORD 报错）
2. `huggingface.co` 直连不可达 → `HF_ENDPOINT=https://hf-mirror.com`
3. XET CAS（`cas-server.xethub.hf.co`）返回 401 → `HF_HUB_DISABLE_XET=1`

## 流程

### Step 0 · 取真实文件（附件常是假文件）

附件落在 `/root/uploads/` 的往往是 **10KB 的「资料库占位 HTML」**，不是真文件。
先 `file <路径>` 看一眼，是 HTML 就走资料库 API：

```bash
python3 scripts/fetch_library_file.py ./in \
    <nodeId>:A2.txt \
    <nodeId>:A2.mp3
```

`nodeId` = 资料库链接 `https://www.workbuddy.cn/space/d/<nodeId>` 中 `d/` 后面那串。
拿到的 download_url 是**预签名短期有效**，必须立刻下载。

### Step 1 · 词级 ASR

```bash
/opt/wenv/bin/python scripts/whisper_word_gen.py <audio> <words.txt> [script.txt]
```

产出 TSV：`start<TAB>end<TAB>word`，字数与音频时长成正比（约 45s 音频 / 100 词）。

**参数不可随意改**（见「关键坑」）：`vad_filter=False`、`condition_on_previous_text=False`、
`compression_ratio_threshold=2.4`、`no_speech_threshold=0.85`、`word_timestamps=True`。

> 33 分钟的音频约需 **13 分钟**（CPU int8, 16 线程）；短音频 5 分钟内。长音频务必放后台跑。

### Step 2 · 台本对齐

```bash
/opt/wenv/bin/python scripts/align_gen.py <script.txt> <words.txt> <out_ja.srt>
```

输出 `<out_ja.srt>`：**文本逐字取自台本**，时间轴来自词级对齐。
会打印「字符匹配率」，正常在 **85%–90%**（ASR 与台本不可能 100% 一致）；
若低于 70%，多半是台本与音频不是同一段，先人工核对。

### Step 3 · 翻译 → 三件套

**3a** 导出编号清单（翻译用，杜绝错位）：

```bash
python3 scripts/dump_lines.py <script.txt> 1 60    # 看前 60 条；不带参数看全部
```

**3b** 按清单序号写 `zh.json`：

```json
{ "1": "…啊。", "2": "给我发私信的欧尼桑？", "3": "你有点迟到了呢…喂♡" }
```

> ⚠️ **序号 = 台本「非空行」连续编号**，不是台本文件的行号（含空行）。
> 这是本项目最容易错位的一处，用 `dump_lines.py` 的编号就不会错。

**3c** 生成 SRT：

```bash
python3 scripts/make_srt.py <out_ja.srt> zh.json <out_dir> <prefix>
# → <prefix>_zh.srt（纯中文）、<prefix>_bilingual.srt（日文+中文两行）
```

### Step 4 · 中文烧录视频（可选）

```bash
cd <srt 所在目录>          # 相对路径最稳，避免冒号转义问题
bash scripts/render_zh_video.sh <prefix>_zh.srt <audio> <prefix>_中文字幕版.mp4
```

产物：720×1280 竖屏、深色背景 `0x141418`、15fps、原声 AAC 192k，约 **35KB/秒**。

## 关键坑（血泪清单，勿重蹈）

| 坑 | 现象 | 正确做法 |
|---|---|---|
| **ASMR 开 VAD** | 7 分钟音频只剩 1 段字幕 | `vad_filter=False`，改用抗幻觉三件套 |
| **Whisper 复读幻觉** | 大段重复乱码（ダマドラ/ジーJ…） | `condition_on_previous_text=False` + `compression_ratio_threshold=2.4` |
| **耳语被判静音** | 整段无输出 | `no_speech_threshold=0.85`（放宽） |
| **MMS_FA 强制对齐** | 72 行回退 58 行，成功的还漂飞几十秒 | ❌ 不要用。uroman 日语音素化丢失长音/促音，短窗口下 CTC 退化成「找相似片段」。**用 Whisper 词级时间戳** |
| **一次性算整段 emission** | 进程被静默杀掉（无 traceback） | cgroup 8GB 限制 → 分段前向，或干脆只用词级 TSV |
| **torchaudio.load** | `TorchCodec is required`（2.11+） | 用 `soundfile.read` 代替 |
| **翻译序号错位** | 提示「缺译文 [3,8,12…]」 | 键必须是「非空行连续序号」，用 `dump_lines.py` 核对 |
| **libass 字号被放大 / 换行错位** | 字幕溢出屏幕 | `force_style` 里**必须**显式 `PlayResX=720,PlayResY=1280` |
| **`Unknown encoder 'libx264'`** | 编码失败 | 本环境用 `-c:v libopenh264` |
| **中文字体** | 方块/豆腐 | `Fontname=Noto Sans CJK SC`（`fc-list :lang=zh` 可查） |
| **长音频同步跑两个** | OOM | 串行跑；单个 ASR 峰值已接近 8GB 上限 |

## 质量自检（交付前必做）

```bash
/opt/wenv/bin/python - <<'PY'
# 时长分布 + 最长行 + 最大空档，判断有无错位
PY
```

合格线（本项目实测基准）：

- 单条最长 **≤ 8 秒**（A1 实测 5.3s / A2 实测 7.7s / B1 实测 6.0s）
- 无 >10s 的单条（有则说明漏了对齐）
- 台词总覆盖率 60%–70%（ASMR 大量呼吸/音效间隙属正常）
- 首行时间 ≈ 音频开头，末行 ≈ 音频结尾

**烧录视频的间接验证**（本模型看不了图片，用像素统计代替目视）：
抽几帧 PNG → 统计亮像素（R/G/B > 200）数量与 bbox，能落在画面内且 y 在底部即正常。

```bash
ffmpeg -v error -ss 60 -i out.mp4 -frames:v 1 /tmp/f.png
python3 -c "from PIL import Image; ..."   # 统计白像素 bbox
```

## 脚本清单

| 脚本 | 作用 |
|---|---|
| `scripts/setup_env.sh` | 一次性环境准备（venv + faster-whisper + 镜像） |
| `scripts/fetch_library_file.py` | 从资料库按 nodeId 下载真实文件 |
| `scripts/whisper_word_gen.py` | Step 1 词级 ASR |
| `scripts/align_gen.py` | Step 2 台本对齐 → 日文 SRT |
| `scripts/dump_lines.py` | Step 3a 导出编号清单供翻译 |
| `scripts/make_srt.py` | Step 3c 生成中文 / 双语 SRT |
| `scripts/render_zh_video.sh` | Step 4 烧录中文竖屏视频 |

## 交付约定

- 交付目录：`/workspace/<作品名>/`，文件名 `<prefix>_ja.srt` / `_zh.srt` / `_bilingual.srt` / `_中文字幕版.mp4`
- 每次交付附：行数、字符匹配率、最长行、覆盖率等**核心数字**，以及失败项的根因
