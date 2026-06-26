---
name: huo15-img-test
displayName: 火一五文生图提示词
description: 火一五文生图提示词 v2.3 — 文生图&视频六件套：(1) enhance_prompt.py 文生图：88 风格预设 + 混合预设 (-p A+B --mix 0.6) + 五锁一致性 + 角色设定图 + 系列批量 + basic/pro/master 三档；(2) enhance_video.py 视频提示词：9 模型规格（Sora/Kling/Runway/Pika/Luma/Hailuo/即梦/Wan）+ 30 镜头运动 + 关键帧三段式；(3) reverse_prompt.py 参考图反解：A1111/ComfyUI/NovelAI metadata 自动识别 + VLM fallback；(4) render_prompt.py 直出图片：ComfyUI/SD-WebUI/DALL-E 三后端；(5) claude_polish.py ⭐v2.3 Claude API 智能润色：把粗糙描述转专业摄影/绘画术语 + 推荐预设/相机/光影；(6) safety_lint.py ⭐v2.3 平台合规润色：识别会被 SD/MJ/DALL-E 误判的艺术词汇并给出合法艺术化替代（仅服务合规艺术创作，拒绝违法/未成年/真人色情）。适配 Midjourney/SD/SDXL/Flux/DALL-E 3。触发词：文生图、火一五文生图提示词、文生视频、提示词、生成图片、生成视频、img-test、text to image、text to video、enhance prompt、提示词增强、图片一致性、系列图、角色一致、批量出图、混合风格、原神+敦煌、参考图反解、reverse prompt、提示词反解、ComfyUI 直出、SD WebUI、DALL-E、视频提示词、Sora、可灵、Runway、即梦、Hailuo、Claude 润色、智能润色、平台合规、艺术化重写。
version: 2.3.0
aliases:
  - 火一五文生图提示词
  - 火一五文生图技能
  - 火一五文生视频技能
  - 火一五提示词技能
  - 火一五提示词全家桶技能
  - 火一五AI绘画技能
  - 文生图
  - 文生视频
  - 提示词增强
  - 智能润色
  - 平台合规润色
  - img-test
---

# 火一五文生图提示词 v2.3

**一句话描述 → 贴合需求、一致性强的专业 T2I/T2V 提示词，并可直出。**

## v2.3 = 六件套

| 脚本 | 作用 | 一行 demo |
|------|------|-----------|
| `enhance_prompt.py` | 文生图（升级混合 + polish + safety） | `enhance_prompt.py "持剑女侠" -p "赛博朋克+水墨" --mix 0.6` |
| `enhance_video.py` | 视频提示词 | `enhance_video.py "汉服少女转身回眸" -p 汉服写真 -m Kling --duration 6` |
| `reverse_prompt.py` | 参考图反解 | `reverse_prompt.py img.png --mj` |
| `render_prompt.py` | 直出图片 | `render_prompt.py "原神少女" -p 原神 --backend sd-webui` |
| `claude_polish.py` ⭐v2.3 | Claude API 智能润色 | `claude_polish.py "一个温柔的女孩" --pipe` |
| `safety_lint.py` ⭐v2.3 | 平台合规润色 | `safety_lint.py "战士手中沾满鲜血的剑" --target dalle` |

## 版本演进

| 维度 | v2.0 | v2.1 | v2.2 | v2.3 |
|------|------|------|------|------|
| **风格预设** | 56 | 88 | + 混合预设 | 沿用 |
| **一致性** | 四锁 + seed + 系列 | + 角色设定图 | + motion 第六锁 | 沿用 |
| **贴近需求** | 意图+构图+情绪 | + 时间/天气/季节/负向 | + 视频镜头运动+关键帧 | + **Claude API 润色** |
| **生态闭环** | 仅 prompt | 仅 prompt | + 反解 + 直出 | + **平台合规重写** |
| **AI 联动** | 无 | 无 | 无 | + **Claude/GPT/Gemini 协作** |

## 使用方式

### Agent 调用（推荐）

```
用户: 帮我出一张赛博朋克街头的图
```

Agent 识别到"赛博朋克"触发词，自动调用：

```bash
~/workspace/projects/openclaw/huo15-skills/huo15-img-test/scripts/enhance_prompt.py \
    "赛博朋克街头" -p 赛博朋克 -m Midjourney
```

### 直接调用

```bash
cd ~/workspace/projects/openclaw/huo15-skills/huo15-img-test

# 基础：指定预设
./scripts/enhance_prompt.py "一只猫" -p 动漫 -m Midjourney

# 自动意图（无需 -p，脚本从关键词推断）
./scripts/enhance_prompt.py "为咖啡品牌设计一个logo"   # → 自动选 Logo设计, 1:1
./scripts/enhance_prompt.py "产品白底图：无线耳机"     # → 自动选 产品摄影, 1:1
./scripts/enhance_prompt.py "微距 一滴露珠"            # → 自动选 微距摄影, 1:1

# 系列一致性（4 张共享 seed + camera/lighting/palette 锁）
./scripts/enhance_prompt.py "红发女侠" -p 动漫 -s 4 \
    --variations "持剑站立,骑马奔驰,弯弓射箭,与龙对视" \
    -m Midjourney

# 英文别名 + 多模型输出
./scripts/enhance_prompt.py "spaceship in nebula" -p scifi -m Flux -a 21:9
./scripts/enhance_prompt.py "minimalist camellia logo" -p logo -m SDXL

# JSON 输出（便于集成）
./scripts/enhance_prompt.py "森林少女" -p ghibli -j
```

## 88 款风格预设

### 【摄影 · 13】
写实摄影 / 胶片摄影 / 黑白摄影 / 人像摄影 / 时尚大片 / 美食摄影 / 产品摄影 / 微距摄影 / 航拍摄影 / 街拍纪实 / **暗黑美食 · 日杂 · 街头潮流** ⭐v2.1

### 【动漫 · 10】
动漫 / 新海诚 / 宫崎骏 / 美漫 / Q版 / 童话绘本 / **萌系 · 厚涂 · 轻小说封面 · 赛璐璐** ⭐v2.1

### 【插画 · 7】
水彩 / 油画 / 水墨 / 工笔国画 / 浮世绘 / 线稿 / 像素艺术

### 【3D · 7】
3DC4D / 盲盒手办 / 低多边形 / 等距视图 / 粘土 / 毛毡手工 / 纸艺

### 【设计 · 15】
极简主义 / 平面设计 / Logo设计 / 图标设计 / 信息图 / 品牌KV / 专辑封面 / 复古海报 / 电影海报 / 表情包 / **玻璃拟态 · 新拟态 · 孟菲斯 · 杂志编排 · 包豪斯 · 奶油风** ⭐v2.1

### 【艺术史 · 4】
印象派 / 后印象派 / 新艺术 / 装饰艺术

### 【场景氛围 · 17】
赛博朋克 / 蒸汽朋克 / 科幻 / 奇幻 / 黑暗奇幻 / 国潮 / Y2K / Vaporwave / 霓虹灯牌 / 建筑可视化 / 电影感 / 概念艺术 / **粗野主义 · 北欧极简 · 侘寂 · 疗愈治愈 · 美式复古** ⭐v2.1

### 【游戏艺术 · 7】⭐ v2.1 新类
原神 / 崩铁星穹 / 英雄联盟 / 暗黑4 / Valorant / Pokemon / 暴雪风

### 【东方传统 · 7】⭐ v2.1 新类
敦煌壁画 / 青花瓷 / 民国月份牌 / 年画 / 剪纸 / 和风 / 汉服写真

> 英文别名支持：`anime`、`ghibli`、`shinkai`、`cyberpunk`、`steampunk`、`scifi`、`minimal`、`logo`、`icon`、`3d`、`c4d`、`octane`、`isometric`、`vangogh`、`artdeco`、`neon`、`vapor`、`y2k`、`genshin`、`lol`、`diablo`、`valorant`、`pokemon`、`dunhuang`、`hanfu`、`wafu`、`glassmorphism`、`neumorphism`、`memphis`、`bauhaus`、`brutalism`、`nordic`、`wabisabi`、`healing`、`cozy`、`americana`、`darkfood`、`muji`、`streetwear`… 运行 `./scripts/enhance_prompt.py -l` 查看完整列表。

## 参数说明

| 参数 | 作用 | 示例 |
|------|------|------|
| `subject` | 主体描述（必填） | `"一只猫"` |
| `-p, --preset` | 风格预设（中文 / 英文别名） | `-p 赛博朋克` / `-p cyberpunk` |
| `-m, --model` | 目标模型 | `Midjourney` / `SD` / `SDXL` / `Flux` / `DALL-E` / `通用` |
| `-a, --aspect` | 画幅 | `1:1` / `3:4` / `16:9` / `21:9` / `9:16` |
| `-t, --tier` ⭐v2.1 | 质量档位 | `basic` / `pro`(默认) / `master` |
| `-cs, --character-sheet` ⭐v2.1 | 角色设定图 T-pose 多视图 | - |
| `--avoid` ⭐v2.1 | 额外负面词，逗号分隔 | `--avoid "cluttered, people"` |
| `--mood` | 情绪覆盖（不给则从主体自动抽） | `--mood 神秘` |
| `--composition` | 构图覆盖 | `--composition 俯拍` |
| `--seed` | 种子（不给则按 subject+preset 哈希生成稳定 seed） | `--seed 42` |
| `-s, --series` | 系列张数 | `-s 4` |
| `--variations` | 系列变体，逗号分隔 | `--variations "A,B,C,D"` |
| `-l, --list` | 列出所有预设 | - |
| `-j, --json` | JSON 输出 | - |

## 自动抽词（v2.1 扩展）

脚本会从主体描述中自动识别以下字段，无需显式参数：

| 维度 | 关键词示例 |
|------|-----------|
| **意图** | logo / 产品 / 海报 / 头像 / 美食 / 汉服 / 敦煌 / 原神 / 玻璃拟态 ... |
| **构图** | 特写 / 近景 / 中景 / 全身 / 俯拍 / 仰拍 / 鸟瞰 / 航拍 / 侧面 / 背面 |
| **情绪** | 温暖 / 冷峻 / 神秘 / 梦幻 / 欢快 / 忧郁 / 史诗 / 高级 / 治愈 / 浪漫 ⭐v2.1：紧张 |
| **时间** ⭐v2.1 | 清晨 / 早晨 / 正午 / 下午 / 黄昏 / 日落 / 夜晚 / 深夜 / 黎明 / 蓝调时刻 |
| **天气** ⭐v2.1 | 晴天 / 多云 / 阴天 / 下雨 / 雨天 / 大雨 / 下雪 / 雪天 / 雾天 / 风暴 / 雷雨 |
| **季节** ⭐v2.1 | 春/夏/秋/冬 / 樱花季 / 枫叶季 |
| **负向需求** ⭐v2.1 | 不要X / 没有X / 避免X / no X / avoid X / without X → 自动入负面 |

## 一致性四锁（核心机制）

每个预设内置以下锁项，所有系列张图共享 ⇒ 风格漂移大幅下降：

| 锁项 | 作用 | 示例（赛博朋克） |
|------|------|----------------|
| `camera` | 镜头焦段 / 视角 | `low angle wide, 24mm anamorphic` |
| `lighting` | 光源 / 光质 | `neon magenta and cyan rim, wet reflective streets` |
| `palette` | 色板 | `magenta cyan black, neon highlights` |
| `aspect` | 画幅 | `21:9` |

系列模式 (`-s N --variations ...`) 额外锁定 **seed**，变换仅发生在主体描述，框架完全不变。

## 模型适配细节

| 模型 | 输出格式 | 特有提示 |
|------|---------|---------|
| **Midjourney** | `主体, 风格, 光影, 色板, 画质 --ar X:Y --stylize 250` | `--cref <url>` 锁角色、`--sref <url>` 锁风格图 |
| **Stable Diffusion** | `(subject:1.2), 风格, ..., 质量` + 负面 | 权重语法 `(word:1.3)`、减弱 `[word]`、DPM++ 2M Karras |
| **SDXL** | 同 SD，尺寸建议 `1024x1024 / 1216x832 / 1536x640 ...` | Refiner 0.2-0.3 |
| **DALL-E 3** | 自然语言段落（已内化负面） | 连续对话中用 "same character / same scene" |
| **Flux** | 长句描述 | guidance 3.5（Dev） / 0（Schnell） |
| **通用** | 逗号分隔 tags | 三大模型通用骨架 |

## 完整示例

```bash
./scripts/enhance_prompt.py "一只戴墨镜的猫在霓虹街头" -p 赛博朋克 -m Midjourney
```

输出：

```
📌 原始描述   : 一只戴墨镜的猫在霓虹街头
🎨 风格预设   : 赛博朋克
🤖 目标模型   : Midjourney
📐 画幅       : 21:9
🎲 种子建议   : 1873940236

✅ 正向提示词：
一只戴墨镜的猫在霓虹街头, cyberpunk, neon-soaked, blade runner aesthetic,
megacity dystopia, holographic ads, low angle wide, 24mm anamorphic,
neon magenta and cyan rim, wet reflective streets,
magenta cyan black, neon highlights,
detailed cyberpunk cityscape, rainy night ambiance,
masterpiece, best quality, ultra detailed, 8k
--ar 21:9 --stylize 250

❌ 负向提示词：
--no rustic, medieval, natural countryside, low quality, worst quality, ...

🔒 一致性锁：
   camera  : low angle wide, 24mm anamorphic
   lighting: neon magenta and cyan rim, wet reflective streets
   palette : magenta cyan black, neon highlights
   aspect  : 21:9

💡 Midjourney tips：
  • 角色/产品系列一致：加 --cref <url> 或 --sref <url>
  • 想要更风格化加 --stylize 500~750；更写实降到 --stylize 50
  • 建议 seed 锁定：--seed 1873940236
```

## v2.3 新功能 ⭐

### 5. Claude API 智能润色 `--polish`

```bash
# 直接润色（独立调用）
export ANTHROPIC_API_KEY=sk-ant-xxx
./scripts/claude_polish.py "一个温柔的女孩在花丛中"
./scripts/claude_polish.py "敦煌神女" --pipe   # 输出可直接喂给 enhance_prompt.py 的命令

# 在 enhance_prompt.py 里串联使用（润色 → 88 预设 → 输出）
./scripts/enhance_prompt.py "一个温柔的女孩在花丛中" --polish
./scripts/enhance_prompt.py "雪山下的小屋" --polish --safety MJ -m Midjourney
```

利用 Claude prompt engineering 优势：
- **Prompt caching**：system prompt 用 ephemeral cache，省 90% input token
- **Prefill `{`**：assistant 起手 `{` 强制 JSON 输出，无需 tool use
- **XML 思维链**：让 Claude 内部分步骤（refine/style/camera/safety/negatives）
- **88 预设嵌入 system**：Claude 从清单里挑，不凭记忆
- **零 SDK 依赖**：纯 urllib，避免企业扫描器拦截 anthropic 包

### 6. 平台合规润色 `--safety`

**只做合法艺术创作的平台误判规避，不做 jailbreak。**

```bash
# 独立调用
./scripts/safety_lint.py "战士手中沾满鲜血的剑" --target dalle
./scripts/safety_lint.py "古典维纳斯雕像 nude figure" --target MJ --apply
./scripts/safety_lint.py "如何制作炸弹"   # 命中红线 → exit 2

# 在 enhance_prompt.py 里串联
./scripts/enhance_prompt.py "古风战场鲜血飞溅" --safety dalle
./scripts/enhance_prompt.py "黑暗骑士斩杀恶魔" --safety MJ -p 黑暗奇幻
```

**红线（直接拒答）**：
- ✗ CSAM（未成年 + 性化任意组合）
- ✗ 真人 + 色情/政治污蔑
- ✗ 武器/毒品/爆炸物**制作方法/教程**
- ✗ 自残/自杀**方法诱导**

**黄区（艺术化重写）**：
| 类别 | 例子 | 重写策略 |
|------|------|----------|
| violence | 血、伤口、kill、weapon | crimson splash / battle-scarred / vanquish / ceremonial blade |
| nudity | 裸、naked、sexy | classical figure study / fine art reference / fashion editorial |
| horror | horror、gore、demon | gothic atmospheric tension / mythical creature |
| death | dead、skeleton、skull | memento mori / classical allegory / vanitas |
| real-person | celebrity、明星、politician | fictional character / 80s aesthetic |
| brand | marvel、disney、nike | superhero comic style / classic animated |

**平台分级**：
- DALL-E `max` 严格度
- MJ `high` 中等
- SD/SDXL/Flux `low` 宽松（开源本地）

### 7. Polish + Safety 串联（最强组合）

```bash
# Claude 智能润色 → 平台合规重写 → 88 预设增强
./scripts/enhance_prompt.py "战士在血战之后凝视远方" --polish --safety dalle -j
```

输出 JSON 包含 `claude_polish` 和 `safety_lint` 两个完整 meta 块，可追溯每一步改写过程。

## v2.2 新功能详解

### 1. 混合预设 `-p A+B --mix 0.6`

```bash
# 主预设 60% 权重，副预设 40%
enhance_prompt.py "持剑女侠" -p "赛博朋克+水墨" --mix 0.6 -m Midjourney
enhance_prompt.py "山中神女" -p "原神+敦煌壁画" --mix 0.5 -m SDXL
enhance_prompt.py "极简卡片" -p "玻璃拟态+侘寂" --mix 0.7 -m SD
```

融合策略：
- **tags**：主预设标签前置，副预设按权重补充；SD 自动加权重语法 `(tag:1.16)`
- **camera**：取主预设（避免镜头语言混乱）
- **lighting**：叠加 `主光照, blended with 副光照`
- **palette**：拼接两者
- **aspect**：取主预设默认画幅
- **neg**：合并去重 + PRESET_NEG_EXCLUDE 主辅都生效（避免 logo/text/signature 自我否定）
- **seed**：mix_label `A+B@0.60` 参与 hash，相同混合每次同 seed

### 2. 视频提示词 `enhance_video.py`

```bash
# Sora 8 秒赛博朋克
enhance_video.py "雨夜霓虹街头一只猫漫步" -p 赛博朋克 -m Sora --duration 8

# Kling 慢速跟拍
enhance_video.py "汉服少女转身回眸" -p 汉服写真 -m Kling --motion 慢速跟拍

# 史诗节奏 + 自定义动作
enhance_video.py "宇宙飞船穿越星云" -p scifi -m Runway --pacing 史诗 --action "ship accelerates, lens flare"

# 混合风格 + 海螺 MiniMax
enhance_video.py "山中神女腾云" -p "原神+敦煌壁画" --mix 0.6 -m Hailuo

# 列出所有视频模型规格
enhance_video.py --list-models
```

支持的视频模型：

| 模型 | 上限时长 | 默认画幅 | 提示词风格 |
|------|---------|---------|-----------|
| Sora | 20s (Sora 2 Pro) | 16:9 | 长自然语言 |
| Kling 可灵 | 10s (1080p Pro) | 16:9 | 中文优秀，前置主体 |
| Runway Gen-3/4 | 10s | 16:9 | 英文最佳 |
| Pika | 10s | 16:9 | 标签式 + `-gs/-motion` |
| Luma DreamMachine | 9s | 16:9 | 自然语言 + 关键帧 |
| Hailuo MiniMax | 10s | 16:9 | 中英双语 + 参考人物 |
| 即梦 Seedance | 12s | 16:9 | 中文多镜头剧情 |
| 通义 Wan2.1 | 8s | 16:9 | 阿里开源 14B/1.3B |

输出包含：正向 / 负向（视频专属：flicker、motion blur、identity drift）/ 三段式关键帧 / 一致性六锁（+ motion）。

### 3. 参考图反解 `reverse_prompt.py`

```bash
# 自动识别 A1111/ComfyUI/NovelAI metadata
reverse_prompt.py /path/to/image.png

# 远程 URL
reverse_prompt.py https://example.com/img.png

# 直接给 Midjourney 复用 prompt（一行）
reverse_prompt.py img.png --mj

# 强制 VLM 模板（图无 metadata）
reverse_prompt.py img.png --vlm

# JSON pipe 给 enhance_prompt.py
reverse_prompt.py img.png -j > recipe.json
```

三层反解：
1. **PNG metadata**：手写 `tEXt`/`iTXt` 解析，零 PIL 依赖
2. **A1111 / ComfyUI / NovelAI 三大格式自动识别**
3. **VLM fallback**：图无 metadata 时输出标准 prompt 给 GPT-4o/Claude/Gemini/Qwen-VL

启发式预设猜测：35+ 关键词映射（cyberpunk → 赛博朋克 / ghibli → 宫崎骏 / dunhuang → 敦煌壁画 ...）。

### 4. 直出图片 `render_prompt.py`

```bash
# Dry-run（只输出 recipe，不出图）
render_prompt.py "敦煌神女" -p 敦煌壁画 --backend none -j

# AUTOMATIC1111 / Forge SD WebUI
render_prompt.py "赛博朋克猫" -p 赛博朋克 --backend sd-webui

# ComfyUI（用内置 SDXL workflow）
render_prompt.py "原神少女" -p 原神 --backend comfyui

# ComfyUI（自定义 workflow）
render_prompt.py "原神少女" -p 原神 --backend comfyui --workflow ./workflows/sdxl.json

# DALL-E 3
render_prompt.py "极简logo" -p Logo设计 --backend dalle --size 1024x1024
```

特点：
- **零第三方依赖**：纯 urllib，避免企业扫描器命中
- **环境变量覆盖**：`COMFYUI_URL` / `SDWEBUI_URL` / `OPENAI_API_KEY`
- **支持混合预设直出**

## 参考文档

`references/t2i-guide.md` — 提示词要素表 / 88 预设对照 / 模型差异 / 一致性技巧。

## 版本历史

见 `CHANGELOG.md`。
