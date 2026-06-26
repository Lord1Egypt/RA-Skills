---
name: music-composer
description: 专业音乐创作规划 Skill。基于 mmx-cli（MiniMax AI）生成高质量音乐和歌曲。自动规划曲风（Genre）、节奏（Tempo）、乐器编配（Instrumentation）、人声特色（Vocal），将用户的模糊需求转化为精准的生成 Prompt。支持：纯器乐（instrumental）、中文歌词歌曲、英文歌词歌曲、音乐封面翻唱。当用户提到创作音乐、生成歌曲、制作音乐、写歌、制作 BGM、需要音乐素材时触发此 Skill。
---

# 🎵 Music Composer — 专业音乐创作规划

## 依赖项

**必需二进制：** `mmx`（MiniMax AI CLI）

> ⚠️ **安全声明：** 本 Skill 依赖 `mmx` CLI（MiniMax AI 音乐生成工具）。执行任何生成命令前，**必须先验证 mmx 可用且来源可信**。

### 安装 mmx

```bash
# macOS / Linux
npm install -g @aivcore/mmx-cli

# 或通过官方渠道安装（请勿从未知来源安装）
# 访问 https://www.minimax.io 确认官方渠道
```

### 前置检查（必须执行）

在运行任何 `mmx music generate` 命令之前，**必须**执行以下检查：

```bash
# 1. 检查 mmx 是否存在
which mmx || { echo "错误：mmx 未安装，请先运行: npm install -g @aivcore/mmx-cli"; exit 1; }

# 2. 验证 mmx 版本（确认为 MiniMax 官方 CLI，非仿冒）
mmx --version
# 预期输出包含 "mmx" 和版本号，如 "mmx/1.x.x"
# 若输出异常（不包含 mmx 关键字，或行为不符），立即停止并报告
```

**风险提示：** 若 `mmx` 命令不存在、或 `mmx --version` 输出不包含 `mmx` 关键字，**不要执行任何生成命令**，告知用户安装缺失的依赖。

---

## 核心原则

**用户说"帮我写首歌" → 先规划，再生成。**

规划流程：**曲风 → 情绪/主题 → 节奏速度 → 乐器编配（重点：过渡与层次）→ 人声特色（如有）→ 生成 Prompt**

**核心品质要求（本次升级重点）：**
- ✅ **乐器过渡自然**：避免生硬切入，用渐进引入、渐隐淡出
- ✅ **层次感丰富**：前景/中景/背景三层分离，不混在一起
- ✅ **活人感**：有呼吸感、轻微不完美、自然律动，模拟真实乐手演奏
- ✅ **感情细腻**：情感起伏贴合歌词，不flatline

---

## 标准生成命令

> ⚠️ **执行前提：** 完成上方「前置检查」，确认 mmx 可用且版本正常。

```bash
# 纯器乐
mmx music generate \
  --model music-2.6 \
  --prompt "<英文 Prompt>" \
  --instrumental \
  --out ~/video/<filename>.mp3

# 带歌词歌曲
mmx music generate \
  --model music-2.6 \
  --prompt "<英文 Prompt>" \
  --lyrics "<歌词>" \
  --out ~/video/<filename>.mp3

# 翻唱
mmx music cover \
  --prompt "<目标风格描述>" \
  --audio-file /path/to/reference.mp3 \
  --out ~/video/<filename>.mp3
```

---

## 规划流程（详细版）

### Step 1：确认用户需求
至少确认：
| 维度 | 问题 | 示例 |
|------|------|------|
| 类型 | 纯音乐还是带人声？ | instrumental / 中文歌 / 英文歌 |
| 曲风 | 什么音乐风格？ | Jazz, Lo-Fi, Cinematic... |
| 情绪 | 什么情感氛围？ | 温暖治愈 / 忧伤 / 活力... |
| 场景 | 用在什么场景？ | 咖啡馆 / 视频bgm / 睡前... |
| 人声（如有）| 想要什么音色？ | 磁性男声 / 清亮女声... |

### Step 2：组合 Prompt（含活人感关键词）

**Prompt 核心公式：**
```
[情绪] + [曲风] + [层次描述] + [过渡描述] + [活人感关键词] + [场景/用途]
```

**必须包含的质感关键词：**
- `organic` — 有机感、真实乐器
- `human feel` / `breathable` — 活人感、呼吸感
- `natural dynamics` — 自然动态，不呆板
- `smooth instrument transitions` — 乐器间平滑过渡
- `layered arrangement` — 分层编曲
- `subtle imperfection` — 轻微不完美（太完美反而假）
- `slight swing / groove` — 轻微摇摆感
- `room ambience` — 空间残响，录音棚感
- `tender emotional depth` — 细腻情感
- `swell and release` — 起伏与释放

### Step 3：歌词结构（如需）
参考 `references/lyrics-structures.md`

### Step 4：生成并记录
- 文件名：`{序号}_{风格}_{主题}.mp3`
- 完成后汇报文件名

## 快速推荐（预设 Prompt）

| 场景 | 推荐 Prompt 关键词 |
|------|-----------------|
| 咖啡馆 | `warm jazz, upright bass, smooth piano, coffee shop ambience, human feel, natural dynamics, breathable` |
| 电影感 | `cinematic orchestra, layered strings, brass swell, smooth transitions, tender emotional depth, room ambience` |
| 夜晚独处 | `ambient piano, reverb, intimate, slight pedal noise, organic, tender` |
| 活力运动 | `upbeat indie rock, real drums, electric guitar, layered, groove, natural energy` |
| 失眠放松 | `ambient soundscape, soft pad, slow breathing rhythm, human feel, dreamlike` |

## 关联文件
- `references/music-genres.md` — 曲风/乐器/节奏/人声完整参数库
- `references/lyrics-structures.md` — 歌词结构模板库
