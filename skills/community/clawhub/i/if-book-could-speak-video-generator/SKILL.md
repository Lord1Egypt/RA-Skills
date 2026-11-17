---
name: if-book-could-speak
slug: if-book-could-speak
version: 2.2.2
displayName: 假如书籍会说话视频生成器
description: 假如书籍会说话视频生成器。输入书名+作者，一键生成3分钟第一人称书籍自述视频（书以拟人化口吻亲自讲述→AI扁平卡通插图→TTS配音→逐句字幕动画→画板背景+抠图叠加→BGM+转场音效→最终合成MP4）。触发词：假如书籍会说话、书籍会说话、书会说话、if book could speak、做读书视频。跨平台兼容 WorkBuddy / OpenClaw / Codex CLI / TRAE Work。
---

# 假如书籍会说话 视频生成器

## 概述

以**第一人称自述视角**，生成一个约 3 分钟的"假如书籍会说话"视频。书以拟人化的口吻亲自登场，向观众讲述自己的故事——书中主角的经历、情感的起伏、智慧与感悟，仿佛这本书真的活了过来、开口说话。配以扁平卡通风格的 AI 插图、画板背景叠加抠图前景、字幕入场出场动画、背景音乐与转场音效。

本 Skill 对齐扣子工作流《假如书籍会说话》的完整视觉与听觉风格，遵循 [Agent Skills 开放标准](https://agentskills.io)，跨平台兼容 WorkBuddy、OpenClaw、Codex CLI、TRAE Work。

### 与原扣子工作流的一致性（7 项核心风格）

| # | 维度 | 规格 |
|---|------|------|
| 1 | 创意方向 | 第一人称自述（"假如书籍会说话"） |
| 2 | 图像风格 | 扁平卡通风，主角上衣 `#FF7F72`、裤子 `#243139` |
| 3 | 语速 | 固定 1.2x |
| 4 | 字幕动画 | 入场（飞入/放大/淡入交替）+ 出场（淡出）+ 循环微动 |
| 5 | 转场音效 | 有（翻页转场音效 `transition_sound.mp3`，每 3 个分镜边界插入） |
| 6 | 背景音乐 | 有（固定读书 BGM `bgm_reading.mp3`，循环铺底，音量 20%） |
| 7 | 抠图 | 有（rembg AI 抠图，透明前景叠加在画板背景上） |

使用本地开源工具替代扣子插件：剪映小助手 → ffmpeg，扣子图像生成 → 平台图像生成工具，扣子 TTS → 火山引擎 TTS（默认）/ edge-tts（备选），扣子 drawing_board → `generate_background.py`，扣子 cutout → `cutout.py`（rembg）。

## 平台工具映射

本 Skill 的工作流涉及 3 个平台相关工具，各平台替代方案如下。执行时根据当前运行平台选择对应工具。

### 联网搜索（阶段 1 用于搜索书籍信息）

| 平台 | 工具 | 说明 |
|------|------|------|
| WorkBuddy | `WebSearch` | 内置工具，直接调用 |
| OpenClaw | 内置 web search | 自动可用 |
| Codex CLI | `shell: curl` 或 MCP 搜索插件 | 通过 shell 命令或安装搜索 MCP |
| TRAE Work | 内置联网搜索 | 自动可用 |

### 图像生成（阶段 4a 用于生成分镜插图）

| 平台 | 工具 | 说明 |
|------|------|------|
| WorkBuddy | `ImageGen` | 内置延迟工具，调用 DeferExecuteTool |
| OpenClaw | `tools` 声明 或 插件 | 在 frontmatter 中声明图像生成 tool，或安装图像插件 |
| Codex CLI | 外部脚本调用 API | 用 Python 脚本调用 DALL-E / Stability AI / 火山引擎等 API |
| TRAE Work | MCP 图像生成服务 | 通过 MCP 接入火山引擎、通义万相等 |

> 无论使用哪个平台，图像生成的 prompt 统一使用分镜中的 `desc_promopt` 字段，并在末尾追加扁平卡通风格后缀（见阶段 4a）。

### LLM 调用（阶段 1-3 用于生成文案和分镜）

所有平台均内置 LLM 对话能力，直接将 `references/prompts.md` 中的 System Prompt 发送给当前平台的 LLM 即可。

## 输入

| 参数 | 说明 | 必填 |
|------|------|------|
| `book_name` | 书籍名称 | 是 |
| `author_name` | 作者名称 | 是 |
| `ip_name` | 账号名称（用于封面图底部水印） | 否，默认不显示 |

> 语速固定为 1.2x，无需用户指定；音色默认使用知性女声，无需用户指定。

## 环境准备

执行前确保以下 Python 依赖已安装：

```bash
pip install edge-tts imageio-ffmpeg pillow rembg onnxruntime
```

> 脚本会在首次运行时自动安装缺失的依赖，但建议预先安装以避免中断。
>
> `rembg` + `onnxruntime` 用于阶段 4e 的 AI 抠图（U2Net 模型），首次使用时会自动下载模型（约 170MB）。若无法安装 rembg，抠图脚本会自动回退到 PIL 颜色阈值法。

ffmpeg 由 `imageio-ffmpeg` 包自动提供二进制，无需单独安装系统级 ffmpeg。

### TTS 引擎配置

| 引擎 | 凭证 | 时间戳 | 说明 |
|------|------|--------|------|
| 火山引擎 TTS（默认） | API Key | 基于音频时长估算 | 豆包语音合成 2.0，中文自然度最高，可商用，需在[火山引擎控制台](https://console.volcengine.com/speech/new)获取 API Key |
| edge-tts（备选） | 无需配置 | WordBoundary 原生精确 | 微软免费 TTS，pip 安装即用，无凭证时自动回退 |

**配置火山引擎 API Key**（三选一，按优先级生效）：

1. **配置文件**（推荐，一次配置永久生效）：将 API Key 写入技能目录下 `.tts_key` 文件
   ```bash
   echo "your-api-key" > ~/.workbuddy/skills/if-book-could-speak/.tts_key
   ```

2. **环境变量**（临时使用）：
   ```bash
   export VOLC_TTS_API_KEY="your-api-key"
   ```

3. **不配置**：自动回退到 edge-tts（免费，功能完整）

> 火山引擎 TTS 2.0 不原生支持词级时间戳，脚本基于返回的音频时长按字符均匀估算时间戳（标点符号占比较短时间），字幕同步精度略低于 edge-tts 但完全可用。
>
> `.tts_key` 文件包含敏感凭证，分享技能时请勿包含此文件。

### 资源文件（需下载）

音频素材因体积较大，未随 SkillHub 包打包。请从 GitHub 仓库下载并放入 `assets/` 目录：

```bash
# 在技能目录下执行
mkdir -p assets
# 从 GitHub 仓库下载
curl -fsSL -o assets/bgm_reading.mp3 https://github.com/chenjun198711/if-book-could-speak-video-generator/raw/main/assets/bgm_reading.mp3
curl -fsSL -o assets/transition_sound.mp3 https://github.com/chenjun198711/if-book-could-speak-video-generator/raw/main/assets/transition_sound.mp3
```

| 文件 | 说明 | 对应扣子节点 |
|------|------|--------------|
| `assets/bgm_reading.mp3` | 固定读书背景音乐（9.3MB），循环铺底，音量 20% | 背景音乐 OSS URL |
| `assets/transition_sound.mp3` | 翻页转场音效（2.8KB），每 3 个分镜边界插入 | zc_mp3 转场音效 |

> **提示**：若未下载音频素材，视频仍可生成，仅无 BGM 和转场音效（不影响其他功能）。也可使用自己的 mp3 文件替换，路径在 `segments.json` 的 `bgm` 和 `transition_sound` 字段指定。

## 完整工作流（5 个阶段）

### 阶段 1：生成书评文案

**目标**：根据书名+作者，用 LLM 生成约 1000 字的第三人称书评文案。

**操作**：
1. 用当前平台的**联网搜索工具**搜索书籍真实信息（简介、解读、出版年份、核心观点）
2. 使用 system prompt（见 `references/prompts.md` 第 1 节），要求 LLM 以第三人称书评视角输出 JSON：

```json
{
  "book_name": "...",
  "author_name": "...",
  "year": "yyyy-MM",
  "content": "1000+字第三人称书评文案（含书籍解读+核心故事+智慧感悟+情感共鸣）",
  "category": "图书分类"
}
```

**要点**：
- 全文使用第一人称，书自己是讲述者，以拟人化方式直接与观众对话
- 文案需满足约 3 分钟口播时长（约 700-1000 字）
- 开篇须以"你好，我是《书名》"开始，书向观众问好并介绍自己
- 信息来源需通过搜索获取，确保内容准确

### 阶段 2：生成分镜脚本

**目标**：将书评文案拆分为 8-50 个分镜，每个分镜包含字幕文案、画面描述、AI 图像提示词。

**操作**：
使用 system prompt（见 `references/prompts.md` 第 2 节），输入阶段 1 的 content，输出：
```json
{
  "list": [
    {
      "story_name": "分镜名称",
      "desc": "画面描述",
      "cap": "字幕文案（一句话，第三人称）",
      "desc_promopt": "图像生成提示词"
    }
  ],
  "keywords": ["重点词1", "重点词2"]
}
```

然后在 list 开头插入引言分镜：
```python
list.insert(0, {
    "story_name": "开场白",
    "desc": "一本被翻开的书，旁边放着咖啡杯和眼镜",
    "cap": f"你好，我是《{book_name}》，今天让我亲自为你讲述我的故事。",
    "desc_promopt": "一本翻开的书放在木桌上，旁边有咖啡杯和眼镜，明亮温暖的阅读氛围，扁平卡通风格"
})
```

**风格约束**：扁平卡通画风，简洁线条，柔和明亮低饱和度色彩，人物卡通化，符号化背景，主角上衣 `#FF7F72`、裤子 `#243139`。

### 阶段 3：生成标题进度条

**目标**：根据文案内容划分为 4 个情感板块，每板块 6 字以内标题，用于视频顶部进度条显示。

**操作**：
使用 system prompt（见 `references/prompts.md` 第 3 节），输出 4 个标题（title1-title4）。

**使用方式**：4 个标题通过 `segments.json` 的 `chapter_titles` 字段传入 `compose_video.py`，在视频顶部渲染为进度条（当前板块活力橙色高亮 + 底部进度线）。同时需要 `segment_chapters` 字段指定每个分镜所属的板块索引（0-3），未指定时自动均匀分配。

### 阶段 4：生成素材（并行）

本阶段生成视频所需的全部素材：

#### 4a. AI 插图生成

对每个分镜的 `desc_promopt`，调用当前平台的**图像生成工具**生成插图。

**统一风格参数**（扁平卡通风）：
- 尺寸：1024x768
- 风格：扁平卡通（flat cartoon）
- 主角配色：上衣 `#FF7F72`（活力橙）、裤子 `#243139`（深墨蓝）
- 画面氛围：简洁线条、柔和明亮色彩、低饱和度、表现力强的人物、极简背景
- 风格后缀（自动追加到每个 desc_promopt 末尾）：

```
，扁平风，主角上衣颜色#FF7F72，裤子颜色#243139，Transparent glass with 30% opacity，flat cartoon style, simple lines, soft bright colors, low saturation, expressive characters, minimalist background
```

**各平台调用方式**：

- **WorkBuddy**：调用 `ImageGen` 工具（通过 DeferExecuteTool），参数 `prompt` = desc_promopt + 风格后缀，`size` = "1024x768"
- **OpenClaw**：调用 frontmatter 中声明的图像生成 tool
- **Codex CLI**：运行 `python3 scripts/generate_image.py --prompt "<desc_promopt>" --output "scene_001.png"`（需自备 API Key）
- **TRAE Work**：通过 MCP 调用已接入的图像生成服务

> 生成的图片统一命名为 `scene_000.png` ~ `scene_NNN.png`，存放到 `output/{book_name}/images/` 目录。

#### 4b. TTS 语音合成

对每个分镜的 `cap`（字幕文案），使用 TTS 引擎生成 MP3 音频，同时生成词级时间戳（保存为同名 `.words.json` 文件，用于阶段 5 的逐句字幕精确同步）。

**双引擎架构**：
- **火山引擎 TTS**（默认）：V1 API + X-Api-Key 认证，豆包语音合成 2.0 音色，中文自然度最高，可商用，API Key 通过配置文件 `.tts_key` 或环境变量 `VOLC_TTS_API_KEY` 提供
- **edge-tts**（备选）：免费无需配置，原生 WordBoundary 词级时间戳，未配置火山引擎凭证时自动回退

**默认音色**（知性女声，适合第三人称书评解读）：
- 火山引擎：`zh_female_zhixingnv_uranus_bigtts`（知性女声 2.0，专业沉稳，适合书籍自述）
- edge-tts：`zh-CN-XiaoxiaoNeural`（晓晓，女声，知性自然）

**语速固定 1.2x**：
- 火山引擎：`speed_ratio = 1.2`（`DEFAULT_SPEED_RATIO` 常量）
- edge-tts：`rate = "+20%"`（`EDGE_DEFAULT_RATE` 常量）

查看所有可用音色：`python3 scripts/generate_audio.py --list-voices`

运行（所有平台通用，自动选择引擎，语速固定 1.2x）：
```bash
python3 scripts/generate_audio.py --text "<字幕>" --output "audio_001.mp3"
```

指定引擎或音色（语速仍固定 1.2x）：
```bash
# 强制使用火山引擎
python3 scripts/generate_audio.py --text "<字幕>" --output "audio_001.mp3" --engine volcano --voice zh_female_zhixingnv_uranus_bigtts

# 强制使用 edge-tts
python3 scripts/generate_audio.py --text "<字幕>" --output "audio_001.mp3" --engine edge --voice zh-CN-XiaoxiaoNeural
```

批量模式：
```bash
python3 scripts/generate_audio.py --batch captions.json --output-dir audio/ --voice "zh_female_zhixingnv_uranus_bigtts"
```

#### 4c. 开场封面图

为视频第一帧生成专属封面图（1920x1080），包含书名、作者、品牌文字。

**操作**：运行 `python3 scripts/generate_cover.py`

```bash
# 用第一张分镜图做模糊背景（推荐，与视频风格一致）
python3 scripts/generate_cover.py \
  --book-name "活着" \
  --author "余华" \
  --output output/活着/images/cover.png \
  --bg output/活着/images/scene_000.png

# 无背景图，使用深蓝渐变
python3 scripts/generate_cover.py \
  --book-name "活着" \
  --author "余华" \
  --output output/活着/images/cover.png
```

**封面布局**（活力橙 + 深蓝主题）：
- 顶部：「假如书籍会说话」品牌文字 + 活力橙色分隔线（#FF7F72）
- 中部：书名大字（自动换行居中，80pt，冷白色 #F0F0FA）
- 中下：作者名（42pt）
- 底部：账号名称水印（**可选**，通过 `--ip-name` 指定，不传则不显示）
- 背景：深蓝渐变（#0F1726 → #1E293B）或分镜图模糊 + 深蓝遮罩

**字体**：自动检测系统中文字体（Windows: 微软雅黑 / macOS: PingFang SC / Linux: Noto Sans CJK），无需手动修改。

> 封面图在阶段 5 合成时，通过 segments.json 中的 `cover` 字段指定。若提供 cover，第一分镜会全屏展示封面图作为视频开场（不叠加抠图）。

#### 4d. 画板背景生成（模拟扣子 drawing_board）

**目标**：生成一张 1920x1080 画板背景图，作为每个分镜的底层背景，抠图后的透明前景叠加在其上方，模拟扣子工作流中 drawing_board + cutout 的分层视觉效果。

**操作**：运行 `python3 scripts/generate_background.py`

```bash
python3 scripts/generate_background.py \
  --book-name "活着" \
  --author "余华" \
  --year "1993-06" \
  --category "当代文学" \
  --titles "初见,故事,感悟,共鸣" \
  --output output/活着/images/background.png
```

> `--titles` 支持逗号分隔字符串 `"初见,故事,感悟,共鸣"` 或空格分隔多个参数 `初见 故事 感悟 共鸣`。

**画板布局**（深蓝渐变背景 + 活力橙点缀）：
- 顶部：「假如书籍会说话」品牌文字 + 活力橙色分隔线
- 上部：书名大字（居中）
- 左侧：4 个板块标题（带活力橙编号圆点）
- 右侧：作者 / 年份 / 分类信息
- 背景：深蓝渐变（#0F1726 → #1E293B）

> 画板背景通过 `segments.json` 的 `background` 字段指定。若提供了 background，视频合成时会启用"抠图叠加模式"：背景图 + 透明前景（62% 缩放居中偏上）+ Ken Burns + 进度条 + 淡入淡出。

#### 4e. AI 抠图（模拟扣子 cutout）

**目标**：将每个分镜的 AI 插图移除背景，生成透明前景 PNG，叠加在画板背景图上方，实现分层视觉。

**操作**：运行 `python3 scripts/cutout.py`

```bash
# 单张抠图
python3 scripts/cutout.py --input images/scene_001.png --output cutouts/scene_001.png

# 批量抠图（处理 images/ 下所有 scene_*.png）
python3 scripts/cutout.py --batch images/ --output-dir cutouts/

# 指定抠图方法（auto/rembg/pil）
python3 scripts/cutout.py --input scene_001.png --output scene_001_cutout.png --method rembg
```

**双方案抠图**：
- **主方案 `rembg`**：基于 U2Net 模型的 AI 抠图，精确识别前景主体，效果最佳。首次使用自动下载模型（约 170MB）。需安装 `rembg` + `onnxruntime`。
- **备选方案 `pil`**：PIL 颜色阈值法，将亮度高于阈值（默认 240）的像素设为透明，适用于背景为浅色/白色的扁平卡通图片。无需额外依赖。
- **自动选择 `auto`**（默认）：优先使用 rembg，未安装时回退到 PIL。

> 抠图后的透明前景通过 `segments.json` 中每个 segment 的 `cutout` 字段指定。若提供了 cutout 路径且同时提供了 background，视频合成时使用抠图叠加模式。

### 阶段 5：视频合成

**目标**：将所有素材合成为最终 MP4 视频，包含 BGM、转场音效、字幕动画、抠图叠加。

**操作**：运行 `python3 scripts/compose_video.py`，该脚本执行：

1. 计算每个分镜时长（基于 TTS 音频时长 + 0.3s 间隔）
2. 图片缩放/裁剪为 1920x1080（16:9）
3. **两种渲染模式**：
   - **封面开场**（第一分镜）：若提供了 `cover`，第一分镜全屏展示封面图（不叠加抠图），作为视频开场
   - **抠图叠加模式**（后续分镜，提供了 `background` + `cutout`）：画板背景图 + 透明前景（62% 缩放，居中偏下约 28% 高度处）
   - **普通模式**（无 background/cutout）：分镜图全屏展示
4. 为每个分镜添加 **0.3s 淡入淡出转场**（dip-to-black）
5. 使用 ffmpeg 将图片+音频合成为视频片段
6. **进度条 overlay**：顶部显示板块标题（当前板块活力橙色高亮+实心圆点，其余灰色+空心圆点），底部进度线显示总体播放进度
7. 生成**逐句单行 ASS 字幕**（基于 TTS 词级时间戳精确同步语音，按标点+字数拆分为单行短句，白色加粗文字+黑色描边，**关键词活力橙色高亮**，**入场/出场动画交替**）
8. **音频三路混合 + 响度归一化**：TTS 人声 + BGM（循环铺底，音量 20%）+ 转场音效（每 3 个分镜边界插入翻页音效），混合后经 `loudnorm` 归一化到 -16 LUFS
9. 拼接所有片段为完整视频

**字幕动画参数**（对齐扣子工作流）：
- 入场动画（按分镜序号交替）：
  - 飞入：`{\fad(150,0)\move(960,1080,960,1020,0,200)}`（从屏幕底部下方飞入到底部区域，200ms）
  - 放大：`{\fad(100,0)\fscx0\fscy0\t(0,200,\fscx100\fscy100)}`（从 0% 放大到 100%，底部区域，200ms）
  - 淡入：`{\fad(200,0)}`（纯淡入，200ms）
- 出场动画：淡出 150ms（`\fad` 出场段）
- 循环动画：通过淡入脉冲模拟微动效果

**字幕参数**：
- 字体颜色：白色 (#FFFFFF)
- 关键词高亮：活力橙色 (#FF7F72)，通过 ASS 内联颜色标签 `{\c&H727FFF&}` 实现
  > 注意：ASS 颜色为 BGR 格式，#FF7F72 → B=72, G=7F, R=FF → `&H727FFF&`
- 边框颜色：黑色 (#000000)
- 字号：64pt（加粗）
- 位置：底部居中（MarginV=30）
- 字体：**自动检测**系统可用中文字体
- 字幕格式：**ASS**（Advanced SubStation Alpha）
- **逐句单行显示**：利用 TTS 词级时间戳，将长字幕按标点拆分为单行短句

**进度条参数**：
- 位置：画面顶部（80px 高度）
- 背景：半透明深色（alpha=130）
- 当前板块：活力橙色 (#FF7F72) 文字 + 实心圆点
- 非当前板块：灰色 (#AAAAAA) 文字 + 空心圆点
- 底部进度线：活力橙色填充 + 深灰底色

**音频混合参数**：
- BGM：循环到视频总时长，音量降至 20%（`volume=0.20`）
- 转场音效：每 3 个分镜边界插入一次翻页音效（`adelay` 延迟到对应时间点 + `amix` 混合）
- TTS 人声：原音量，作为主音轨
- 响度归一化：混合后经过 `loudnorm=I=-16:TP=-1.5:LRA=7` 归一化到 -16 LUFS，避免音量忽大忽小

**动态效果参数**：
- 转场淡入淡出时长：0.3s（短于 0.6s 的分镜自动减半）

### segments.json 格式

```json
{
  "output": "output/书名_假如书籍会说话.mp4",
  "cover": "output/书名/images/cover.png",
  "background": "output/书名/images/background.png",
  "bgm": "assets/bgm_reading.mp3",
  "transition_sound": "assets/transition_sound.mp3",
  "chapter_titles": ["初见", "故事", "感悟", "共鸣"],
  "segment_chapters": [0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3],
  "keywords": ["活着", "福贵", "命运"],
  "segments": [
    {
      "image": "images/scene_000.png",
      "audio": "audio/audio_000.mp3",
      "caption": "你好，我是《活着》，今天让我亲自为你讲述我的故事。",
      "cutout": "cutouts/scene_000.png"
    },
    {
      "image": "images/scene_001.png",
      "audio": "audio/audio_001.mp3",
      "caption": "字幕文本",
      "cutout": "cutouts/scene_001.png"
    }
  ]
}
```

字段说明：
- `cover`：可选，封面图路径。若提供，第一分镜会全屏展示封面图作为开场（保持第一分镜音频和字幕不变）
- `background`：可选，画板背景图路径，启用抠图叠加模式（对应扣子 drawing_board）
- `bgm`：可选，背景音乐路径，默认使用 `assets/bgm_reading.mp3`（对应扣子固定 OSS BGM）
- `transition_sound`：可选，转场音效路径，默认使用 `assets/transition_sound.mp3`（对应扣子 zc_mp3）
- `chapter_titles`：可选，板块标题列表，用于顶部进度条显示
- `segment_chapters`：可选，每个分镜所属板块索引（0-based），未提供时自动均匀分配
- `keywords`：可选，关键词列表，字幕中匹配到的关键词显示为活力橙色高亮
- `segments[].cutout`：可选，抠图后的透明前景路径，启用抠图叠加模式（对应扣子 cutout）

> 若同时提供 `background` 和 `cutout`，启用抠图叠加模式；否则使用普通全屏模式。`bgm` 和 `transition_sound` 未提供时自动使用内置 assets 资源。

### 输出

最终输出：`output/{book_name}_假如书籍会说话.mp4`

## 跨平台安装

### WorkBuddy

技能已安装在 `~/.workbuddy/skills/if-book-could-speak/`，直接使用。

### OpenClaw

```bash
cp -r ~/.workbuddy/skills/if-book-could-speak ~/.openclaw/skills/
```

### Codex CLI

```bash
# 1. 开启 Skills 功能
cat >> ~/.codex/config.toml << 'EOF'
[features]
skills = true
EOF

# 2. 复制技能目录
cp -r ~/.workbuddy/skills/if-book-could-speak ~/.codex/skills/
```

### TRAE Work

```
1. 打开 TRAE Work → 规则和技能 → 技能 → 创建 → 导入文件
2. 上传 SKILL.md 文件
3. 确保 scripts/、references/、assets/ 目录也复制到技能目录
```

## 原工作流参考

原始扣子工作流文件位于 `references/workflow-original.yaml`，包含 30+ 节点的完整链路。本 Skill 对齐其完整视觉与听觉风格：第一人称自述创意方向、扁平卡通图像风格（主角上衣 #FF7F72、裤子 #243139）、1.2x 语速、字幕入场出场动画、转场音效、背景音乐、抠图叠加。

## 快速使用示例

用户说："帮我生成《活着》的假如书籍会说话视频"

执行流程：
1. 搜索"活着 余华 简介 解读 核心观点"
2. 用阶段 1 prompt 生成第一人称书籍自述文案（"你好，我是《活着》…"）
3. 用阶段 2 prompt 生成分镜脚本（扁平卡通画风描述）
4. 用阶段 3 prompt 生成 4 个情感板块标题
5. 对每个分镜：图像生成工具生成扁平卡通插图 + TTS 生成配音（知性女声，1.2x 语速）
6. 生成封面图（活力橙深蓝主题）
7. 生成画板背景图（`generate_background.py`）
8. 对每张分镜图进行 AI 抠图（`cutout.py`，rembg）
9. `compose_video.py` 合成最终视频（画板背景+抠图前景+BGM+转场音效+字幕动画）
10. 输出 `output/活着_假如书籍会说话.mp4`

## 资源文件

- `references/prompts.md` — 所有 LLM 提示词原文（第三人称书评视角，平台无关）
- `references/workflow-original.yaml` — 原始扣子工作流（完整 YAML 备份）
- `references/CROSS_PLATFORM.md` — 跨平台适配详细指南
- `assets/bgm_reading.mp3` — 固定读书背景音乐（对应扣子 OSS BGM）
- `assets/transition_sound.mp3` — 翻页转场音效（对应扣子 zc_mp3）
- `scripts/compose_video.py` — 视频合成脚本（活力橙主题 + BGM + 转场音效 + 字幕动画 + 抠图叠加）
- `scripts/generate_audio.py` — TTS 语音生成脚本（知性女声默认，1.2x 语速固定）
- `scripts/generate_cover.py` — 封面图生成脚本（活力橙深蓝主题）
- `scripts/generate_background.py` — 画板背景图生成脚本（对应扣子 drawing_board）
- `scripts/generate_image.py` — 跨平台 AI 图像生成脚本（扁平卡通风格后缀）
- `scripts/cutout.py` — AI 抠图脚本（rembg 主方案 + PIL 备选，对应扣子 cutout）
