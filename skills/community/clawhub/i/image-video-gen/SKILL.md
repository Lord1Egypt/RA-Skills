---
name: ai-image-generator
description: |
  AI 图片与视频异步生成技能，调用 AI Artist API 根据文本提示词生成图片或视频，自动轮询直到任务完成。

  ⚠️ 使用前必须设置环境变量 AI_ARTIST_TOKEN 为你自己的 API Key！
  需要 API Key 授权：已有账号请前往 https://ai.deepsop.com/login?source=2 登录获取；没有账号请前往 https://ai.deepsop.com/register?source=2 注册后获取。

  支持图片模型：**3.1Nano2-Evo（默认）**、S5.0L、N2、W2.7、W2.7Pro、Nano2-Beta-Evo、**Image2（GPTimage-2）**。
  支持视频模型：**V3.1FB（默认）**、S1.5Pro、V3.1PB、V3.1Fast、W2.6t / W2.6i / W2.6r、klingV3Omni、W2.7t / W2.7i / W2.7r。
  查看当前服务端激活的模型请运行：`python3 scripts/generate_image.py --list-models`。

  触发场景：
  - 用户要求生成图片，如"生成一匹狼"、"画一只猫"、"风景画"、"帮我画"等。
  - 用户要求生成视频，如"生成视频"、"文生视频"、"图生视频"、"生成一段...的视频"等。
  - 用户指定模型：N2、S5.0L、W2.7、W2.7Pro、3.1Nano2-Evo、Nano2-Beta-Evo、Image2、GPTimage-2、gpt-image-2、S1.5Pro、V3.1FB、V3.1PB、V3.1Fast、W2.6t、W2.6i、W2.6r、klingV3Omni、W2.7t、W2.7i、W2.7r。
  - 用户上传参考图/参考视频时，自动先调用文件上传 API 转换为可访问 URL。
---

# AI Image Generator

异步生成 AI 图片与视频的技能。

## ⚠️ 首次使用必读

### 1. 获取 API Key

本技能需要 **API Key 授权**才能调用 AI Artist API：

- **已有账号** → 前往 [https://ai.deepsop.com/login?source=2](https://ai.deepsop.com/login?source=2) 登录获取
- **没有账号** → 前往 [https://ai.deepsop.com/register?source=2](https://ai.deepsop.com/register?source=2) 注册后获取

登录后在复制您的 API Key（`sk-` 开头）。

### 2. 设置环境变量

**在使用前，你必须先设置自己的 API Key：**

```bash
# Linux/macOS/Git Bash (Windows)
export AI_ARTIST_TOKEN="sk-your_api_key_here"

# Windows PowerShell
$env:AI_ARTIST_TOKEN="sk-your_api_key_here"
```

或在项目根目录放一个 `.env` 文件（需 `pip install python-dotenv`，脚本会自动加载）：

```ini
AI_ARTIST_TOKEN=sk-your_api_key_here
FEISHU_WEBHOOK_URL=  # 可选，用于结果通知
```

### 3. 验证配置

**验证配置是否正确：**

```bash
python3 scripts/test_config.py
```

详细配置说明请查看下方"环境配置"章节。

## 快速开始

```bash
python3 scripts/generate_image.py "提示词"
```

## 意图澄清指南（重要）

**调用前必须做的事**：当用户的请求涉及参数复杂的模型，或关键信息缺失时，**先向用户提问确认意图**，再执行生成，避免浪费配额生成不符合预期的作品。

### 通用判断流程

1. **先分辨媒介**：图片 vs 视频（关键词："画/生成图片/海报/插画" → 图片；"视频/动画/片段/动起来" → 视频）。
2. **判断输入材料**：
   - 纯文字 → 文生模式（TEXT）
   - 有一张首帧图 → 首帧图生视频（FIRST&LAST）
   - 有首尾两张图 → 首尾帧控制（FIRST&LAST，需首帧+尾帧）
   - 有参考视频 → 续写（CONTINUATION）、编辑（EDIT）、参考生成（FEATURE/REFERENCE）
   - 有多张参考图（要求角色/元素一致性） → 参考图模式（REFERENCE）
3. **若用户意图不明确或关键材料缺失，必须提问**，不要擅自假设。

### 按模型列出"必须澄清的关键点"

**所有视频模型通用**：
- 时长（秒）？ 比例？（16:9 横屏 / 9:16 竖屏 / 1:1 正方）
- 是否需要生成声音 / 配音 / 音乐？
- 提示词含有人物时，是否希望保持角色一致性？

**`klingV3Omni`（最复杂）**：5 种生成类型 + 多镜头模式，务必确认：
- **生成类型**：文生（TEXT）/ 首尾帧（FIRST&LAST）/ 参考图生视频（REFERENCE）/ 编辑已有视频（EDIT）/ 参考视频再创作（FEATURE）？
- **镜头模式**：单镜头（single）/ 智能多镜头（multi）/ 自定义分镜（customize，需要用户给出每个分镜的描述 + 时长）？
- **生成模式**：`std` 标准 / `pro` 专家级？
- 若是 EDIT/FEATURE：需要参考视频 URL，并确认"是否保留原音"（`keep_original_sound` yes/no）

**`W2.6r` / `W2.7r`（参考视频模式）**：
- 参考图片 + 参考视频的总数 ≤ 5，询问用户是否都准备好了 URL / 本地文件
- 是否想保留原视频的角色音色？
- 希望迁移到什么场景？迁移的主体是什么？（让用户把场景描述写进 prompt）

**`W2.7i`（图生视频，支持续写）**：
- 输入是"一张首帧图"要让它动起来？→ FIRST&LAST（可选提供尾帧，让首尾过渡更可控）
- 输入是"一段已有视频"要让它继续播？→ CONTINUATION（需要 `first_clip_url`）
- 动作/运镜希望如何展开？请用户描述（写进 prompt）

**`W2.6t` / `W2.7t`（文生视频）**：
- 是否需要多镜头叙事？若是 → `shot_type="multi"`（智能分镜）
- 是否有反向提示词（不希望出现的内容）？
- 是否需要智能改写提示词（`prompt_extend=True`，默认 false）？
- 是否需要传入自定义音频？

**`V3.1Fast`（V3.1 系列的复杂款）**：
- 是否需要翻译为英文提示词（`enhance_prompt`）？
- 是否允许生成人物（`personGeneration=allow_adult/dont_allow`）？
- 图像缩放模式（`resize_mode=pad/crop`）？
- 时长 4 秒还是 8 秒？

**`V3.1FB` / `V3.1PB`**：时长固定 8 秒，不必问；但要确认比例 / 分辨率。

**`S1.5Pro`（影视级）**：
- 是否追求"音画同步 + 口型对齐"？（说明场景是否包含对话）
- 时长在 4-12 秒之间，默认 10 秒，可问用户。

**图片复杂款 `W2.7` / `W2.7Pro` / `N2` / `3.1Nano2-Evo`**：
- 有无参考图？做"风格迁移"、"角色一致性"、"文字渲染"时参考图能显著提升质量。
- 是否需要特定比例？（默认 1:1，横图/竖图需指定）
- 质量档位（1K/2K/4K，详见每个模型表）

**`Image2`（GPTimage-2，OpenAI gpt-image-2 接入）**：
- 渲染质量预设？`low`（最快）/ `medium`（平衡，默认）/ `high`（质量）——用 `--ratiocination`
- 一次出几张？1–10，用 `--n`
- 是否需要参考图？支持最多 16 张参考图、单张 ≤50MB；提示词上限 16000 字
- 默认尺寸 `auto`（智能比例），可改为 `1:1 / 3:4 / 4:3 / 16:9 / 9:16` 等（**禁用** `1:4 / 4:1 / 1:8 / 8:1`）
- 该模型 **不接受 `webSearch`、不接受 `imageSearch`**；仅 `3.1Nano2-Evo` 支持 `imageSearch`

### 提问姿态（给 Claude 的指令）

- **一次最多问 2-3 个最关键的问题**，别堆 10 个选项让用户懵。
- **优先问对画面/成本影响最大的参数**（生成类型 > 时长 > 分辨率 > 次要参数）。
- **提供默认建议**，让用户说"就这样"也能继续，不要强制用户全部自选。
  示例："我打算用 `klingV3Omni` 做参考图生视频，比例 16:9、时长 10s、生成声音。你有几张想作为参考的图片吗？要不要保留原音？"
- **材料缺失时必须停下来要素材**（URL / 本地文件路径），不要用占位符或假 URL 代替。
- 用户若说"随便/都行"，按默认值直接执行，并在生成后告知用了哪些默认。

### 何时可以不提问直接执行

- 用户请求非常明确（提示词清晰 + 指定了模型 + 提供了必要的参考材料 URL）
- 用户明确说"快速来一张就行" / "随便出个视频"：用默认模型与默认参数，生成后告知用了什么。
- 用户只要一张插画/头像/风景图 → 直接用默认 `3.1Nano2-Evo` 图片模型。

## 参考图/视频上传流程

当用户提供本地文件作为参考图或参考视频时，需要先调用文件上传 API 转换为可访问的 URL：

### 文件上传 API

```bash
curl --location --request POST 'https://ai.deepsop.com/prod-api/system/fileUpload/upload' \
--header 'x-api-key: sk-your_api_key_here' \
--form 'file=@"C:\\Users\\admin\\Downloads\\image.png"'
```

**返回结果：**
```json
{
  "msg": "操作成功",
  "fileName": "image.png",
  "code": 200,
  "url": "https://kocgo-ai-sales-test.oss-cn-hangzhou.aliyuncs.com/material/100/xxx.png"
}
```

### 使用上传后的 URL

获取到 `url` 后，可作为 `firstImageUrl`、`lastImageUrl` 或其他图片参数传入生成接口。

## 在对话中直接返回图片

### 方式 1: Markdown 图片语法（推荐）

生成图片后，直接在回复中使用 Markdown 语法：

```markdown
![描述](图片URL)
```

**平台支持情况：**
- ✅ WebChat、Discord、Telegram：完全支持
- ✅ 飞书：支持（需公开 URL）
- ❌ WhatsApp：不支持

### 方式 2: 下载后发送（需要 message 工具）

使用 `--download` 参数下载图片，然后通过 message 工具发送：

```bash
python3 scripts/generate_image.py "风景画" --download
```

然后在代码中读取图片并发送：

```python
from scripts.generate_image import generate_image
import base64

result = generate_image(prompt="风景画", download=True)

if result and result["status"] == "SUCCESS":
    # 方式 A: 使用 data URI
    image_uri = result["data_uri"]  # data:image/png;base64,...
    
    # 方式 B: 读取本地文件
    with open(result["local_path"], "rb") as f:
        image_data = f.read()
        base64_data = base64.b64encode(image_data).decode()
```

## 参数说明

### 通用参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `prompt` | 必填 | 生成提示词（图片或视频描述）|
| `--model` | 自动推断 | 生成模型。**未指定时根据 prompt 关键词自动推断**：包含 `视频/动画/短片/动起来/镜头/clip/motion/video` 等 → `V3.1FB`；其余 → `3.1Nano2-Evo`。图片：`3.1Nano2-Evo`、`S5.0L`、`N2`、`W2.7`、`W2.7Pro`、`Nano2-Beta-Evo`；视频：`V3.1FB`、`S1.5Pro`、`V3.1PB`、`V3.1Fast`、`W2.6t`、`W2.6i`、`W2.6r`、`klingV3Omni`、`W2.7t`、`W2.7i`、`W2.7r` |
| `--list-models` | - | 列出当前服务端激活的模型（hiddenState=0）后退出，不需 prompt |
| `--dry-run` | - | 仅构建并打印最终 payload，不提交任务（调试用）|
| `--json-output` | - | 以单行 JSON 向 **stdout** 输出最终结果 `{status,url,message,local_path?}`，便于 openclaw 等编排器解析 |
| `--interval` | `5` | 轮询间隔(秒) |
| `--max-wait` | 图片 600 / 视频 1200 | 任务轮询最长等待秒数 |

#### 输出契约（给编排器/openclaw）

- **stdout**：任务完成后**恰好一行**最终结果
  - 默认：成功时输出 `URL`，失败时留空
  - `--json-output`：始终输出一行 JSON，形如 `{"status":"SUCCESS","url":"https://...","message":"..."}`
  - `--markdown-output`：成功时输出 `![prompt](url)`
- **stderr**：所有人类可读进度日志（`[auto]`、`[upload]`、预估费用、任务 ID、轮询状态变化、`⚠️` 警告、错误说明）
- **退出码**：`0` = 成功，`1` = 失败/超时

脚本会**始终轮询到终态（SUCCESS / FAILED / TIMEOUT）才退出**，无需调用方自己再查询结果。

### 图片专属参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--quality` | `2K` | 图片质量 (2K/4K) |
| `--size` | 模型默认值 | 图片尺寸。`S5.0L` / `W2.7` / `W2.7Pro`: `2048x2048`，`N2` / `3.1Nano2-Evo` / `Nano2-Beta-Evo`: `1:1` |
| `--download` | - | 下载图片到本地 |
| `--output-dir` | `workspace/images` | 图片保存目录 |
| `--markdown-output` | - | 以 Markdown 格式输出图片链接 |
| `--reference-image` | - | 参考图本地路径，自动上传后作为 image-to-image 参考 |
| `--reference-image-url` | - | 已上传的参考图 URL（跳过上传流程）|
| `--web-search` / `--no-web-search` | - | 启用/关闭联网搜索（仅 `S5.0L`、`3.1Nano2-Evo`）|
| `--image-search` / `--no-image-search` | - | 启用/关闭图像搜索（仅 `3.1Nano2-Evo`）|
| `--ratiocination` | `medium` | 渲染质量预设（仅 `Image2`）：`low` / `medium` / `high` |
| `--n` | `1` | 生成数量（图片 `Image2` 1–10；视频 `V3.1Fast` 1–4）|

### 视频专属参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--ratio` | `16:9` | 画面比例，如 `16:9`、`9:16`、`1:1` |
| `--resolution` | `720p` | 视频分辨率，如 `720p`、`1080p` |
| `--duration` | `10` | 视频时长（秒）|
| `--first-image-url` | - | 首帧参考图 URL |
| `--last-image-url` | - | 尾帧参考图 URL |
| `--first-image` | - | 首帧参考图本地路径，自动上传后转换为 URL |
| `--last-image` | - | 尾帧参考图本地路径，自动上传后转换为 URL |
| `--generate-audio` | - | 开启音频生成（按模型能力生效） |
| `--no-audio` | - | 关闭音频生成（按模型能力生效） |

## 支持的模型

### 图片模型

| 模型 | sourceName | methodType | 默认尺寸 | 特点 |
|------|-----------|-----------|---------|------|
| `S5.0L` | DeepSop·S5.0L | `4` | `2048x2048` | 默认模型，质量 2K/3K，支持联网，像素尺寸 WxH |
| `N2` | DeepSop·Nano1 Pro | `2` | `1:1` | 多模态输入，精细参数调节，卓越文字渲染与角色一致性（比例格式；服务端已重命名为 Nano1 Pro）|
| `W2.7` | DeepSop.W2.7 | `6` | `2048*2048` | 文生图/图生图多模态输入，质量 1K/2K，size 用 `*` 分隔 |
| `W2.7Pro` | DeepSop.W2.7Pro | `7` | `2048*2048` | 精准控图与风格迁移，质量 1K/2K，size 用 `*` 分隔 |
| `3.1Nano2-Evo` | DeepSop·Nano2 | `8` | `1:1` | N2 Evo 版（服务端称 Nano2），支持 `imageSearch` 与 `webSearch` |
| `Nano2-Beta-Evo` | DeepSop·Nano2 Beta-Evo | `9` | `1:1` | N2 Beta Evo 版，多模态输入、文字渲染与角色一致性 |
| `Image2` | DeepSop·Image2 | `10` | `auto` | **GPTimage-2** 接入；支持 `ratiocination`(low/medium/high)、`n`(1–10)；提示词 16000 字；参考图 ≤50MB×16 张；禁用 1:4/4:1/1:8/8:1 |

### 视频模型

| 模型 | sourceName | methodType | 默认比例 | 默认分辨率 | 默认时长 | 特点 |
|------|-----------|-----------|---------|-----------|---------|------|
| `S1.5Pro` | DeepSop·S1.5Pro | `2` | `16:9` | `720p` | 10s | 影视级连贯叙事，音画同步与精准口型对齐 |
| `V3.1FB` | DeepSop·V3.1FB | `3` | `16:9` | `1080p` | 8s | 快速生成，**时长固定 8 秒** |
| `V3.1PB` | DeepSop·V3.1PB | `4` | `adaptive` | `720p` | 8s | V3.1Pro 多图参考，**时长固定 8 秒** |
| `V3.1Fast` | DeepSop·V3.1Fast | `5` | `16:9` | `720p` | 8s | 快速生成，音画同步，时长 4s/8s |
| `W2.6t` | DeepSop·W2.6t | `7` | `16:9` | `720p` | 10s | 文生视频，3-15s，size 用 `*` 像素，15s 1080P |
| `W2.6i` | DeepSop·W2.6i | `8` | `16:9` | `720p` | 10s | 图生视频，3-15s，size 用 ratio，无尾帧支持 |
| `W2.6r` | DeepSop·W2.6r | `9` | `16:9` | `720p` | 10s | 参考视频，**3-10s**，size 用 `*` 像素 |
| `klingV3Omni` | DeepSop.klingV3Omni | `10` | `16:9` | `720p` | 10s | 多模态融合，**3-15s**，按张计费，支持分镜 |
| `W2.7i` | DeepSop·W2.7i | `14` | `16:9` | `720p` | 10s | 图生视频，首尾帧平滑过渡，动作延展与视频续写 |
| `W2.7t` | DeepSop.W2.7t | `15` | `16:9` | `720p` | 10s | 文生视频，智能多镜头剪辑，自动配音，2K 高清 |
| `W2.7r` | DeepSop.W2.7r | `16` | `16:9` | `720p` | 10s | 参考视频生成，保留角色音色，多模态融合编辑 |

**V3.1 系列时长（来自前端 `matchVideoDurationInfo`）：**
- `V3.1FB` / `V3.1PB`：**时长固定为 8 秒**
- `V3.1Fast`：4 秒 或 8 秒
- 分辨率可选：720p / 1080p / 4K；比例 16:9 / 9:16 / adaptive

**WAN2.6 / WAN2.7 / klingV3Omni 系列：**
- `*t`：纯文生视频  ·  `*i`：首帧图生视频  ·  `*r`：参考图/视频生成
- 时长范围：`W2.6r` 为 **3-10s**；其余（包含 `klingV3Omni`）为 **3-15s**
- `size` 序列化规则：**仅 `W2.6t` / `W2.6r`** 使用 `宽*高` 像素格式；`W2.6i` / `W2.7t/i/r` / `klingV3Omni` 的 `size` 为比例字符串（如 `16:9`）
- 分辨率可选：720p / 1080p（`klingV3Omni` 无分辨率选项）
- 比例：`W2.6t` / `W2.6r` / `W2.7t` / `W2.7r` 支持 1:1 / 3:4 / 4:3 / 16:9 / 9:16；`W2.6i` / `W2.7i` 不可选比例（由首帧决定）；`klingV3Omni` 仅 1:1 / 16:9 / 9:16
- `W2.6i` / Sora2 系列不支持尾帧图片（仅 `W2.7i` 支持）
- `W2.6t` / `W2.6i` / `W2.7*` 支持传入自定义音频（`audioUrl`）

## 使用示例

```bash
# 查看当前服务端激活的模型
python3 scripts/generate_image.py --list-models

# 基础用法 - 默认图片模型 3.1Nano2-Evo
python3 scripts/generate_image.py "一匹狼"

# 使用 N2 模型（比例尺寸）
python3 scripts/generate_image.py "生成一只狗" --model N2 --size "16:9"

# W2.7 图片模型
python3 scripts/generate_image.py "复古海报" --model W2.7 --quality "4K"

# W2.7Pro 精准控图
python3 scripts/generate_image.py "角色三视图" --model W2.7Pro

# 3.1Nano2-Evo / Nano2-Beta-Evo（N2 进化版）
python3 scripts/generate_image.py "赛博朋克街景" --model 3.1Nano2-Evo --size "16:9"
python3 scripts/generate_image.py "少女肖像" --model Nano2-Beta-Evo --size "3:4"

# Image2（GPTimage-2）—— 默认 auto 比例，medium 渲染质量
python3 scripts/generate_image.py "一只可爱的柯基犬坐在草地上" --model Image2
# Image2 出 4 张高质量图片
python3 scripts/generate_image.py "产品宣传图 4 种风格" --model Image2 --n 4 --ratiocination high --size "1:1"
# 3.1Nano2-Evo 启用图像搜索 + 联网搜索
python3 scripts/generate_image.py "帮我画一种雨季仅出现三天的菌菇" --model 3.1Nano2-Evo --image-search --web-search

# 下载图片
python3 scripts/generate_image.py "风景画" --download

# 高质量生成（S5.0L）
python3 scripts/generate_image.py "风景画" --quality "4K" --size "4096x4096"

# 直接输出 Markdown 图片链接
python3 scripts/generate_image.py "一只可爱的猫" --markdown-output

# 使用参考图生成（自动上传本地图片并转换为 URL）
python3 scripts/generate_image.py "基于这张图生成变体" --reference-image "./reference.png"

# 生成视频 - 默认 V3.1FB（快速、固定 8 秒）
python3 scripts/generate_image.py "现代轻奢吊灯" --model V3.1FB

# 生成视频 - S1.5Pro（默认 16:9 / 720p / 10s）
python3 scripts/generate_image.py "小骏马祝福大家新年快乐" --model S1.5Pro

# 生成视频 - 指定比例和分辨率
python3 scripts/generate_image.py "海边日落风景" --model S1.5Pro --ratio "9:16" --resolution "1080p"

# V3.1FB - 快速基础（8 秒）
python3 scripts/generate_image.py "现代轻奢吊灯" --model V3.1FB --ratio "16:9" --resolution "1080p" --duration 8

# V3.1PB - 自适应比例（8 秒）
python3 scripts/generate_image.py "水晶灯特写" --model V3.1PB --ratio "adaptive" --resolution "720p" --duration 8

# V3.1Fast - 首帧图生视频（4 秒）
python3 scripts/generate_image.py "灯具展示" --model V3.1Fast --first-image "./lamp.jpg" --duration 4

# klingV3Omni - 多模态融合（按张计费）
python3 scripts/generate_image.py "多模态融合镜头" --model klingV3Omni --ratio "16:9" --duration 8

# W2.6t / W2.7t - 文生视频（10 秒）
python3 scripts/generate_image.py "现代轻奢吊灯宣传" --model W2.6t --ratio "16:9" --resolution "1080p" --duration 10
python3 scripts/generate_image.py "品牌短片自动配音 2K" --model W2.7t --ratio "16:9" --resolution "1080p" --duration 10

# W2.6i / W2.7i - 首帧图生视频（8 秒）
python3 scripts/generate_image.py "水晶灯展示" --model W2.6i --first-image "./lamp.jpg" --ratio "9:16" --resolution "720p" --duration 8
python3 scripts/generate_image.py "角色动作延展" --model W2.7i --first-image "./char.jpg" --last-image "./char_end.jpg" --duration 8

# W2.6r / W2.7r - 参考视频生成（CLI 需传已上传 URL，或使用程序化调用）
python3 scripts/generate_image.py "参考素材风格生成" --model W2.6r --ratio "16:9" --resolution "720p" --duration 10
python3 scripts/generate_image.py "保留角色音色迁移场景" --model W2.7r --ratio "16:9" --resolution "720p" --duration 10
```

## 程序化调用

```python
from scripts.generate_image import generate_image, generate_video

# 图片 - 默认 3.1Nano2-Evo
result = generate_image(prompt="一只可爱的猫咪")

# 查询当前激活模型（预览用）
from scripts.generate_image import list_active_models
print(list_active_models())

# 图片 - N2（比例尺寸）
result = generate_image(prompt="生成一只狗", model="N2", size="16:9")

# 图片 - W2.7Pro 精准控图
result = generate_image(prompt="角色三视图", model="W2.7Pro", quality="4K")

# 图片 - 下载到本地
result = generate_image(prompt="风景画", model="S5.0L", download=True, output_dir="./images")

# V3.1FB - 文生视频
result = generate_video(
    prompt="现代轻奢吊灯",
    model="V3.1FB",
    ratio="16:9",
    resolution="1080p",
    duration=8
)

# V3.1Fast - 首帧图生视频
result = generate_video(
    prompt="灯具展示",
    model="V3.1Fast",
    first_image_url="https://example.com/lamp.jpg",
    ratio="9:16",
    resolution="1080p",
    duration=8
)

# V3.1PB - 首尾帧控制
result = generate_video(
    prompt="灯具变形动画",
    model="V3.1PB",
    first_image_url="https://example.com/start.jpg",
    last_image_url="https://example.com/end.jpg",
    ratio="16:9",
    resolution="1080p",
    duration=8
)

# W2.7r - 参考视频生成（多模态融合）
result = generate_video(
    prompt="保留角色音色迁移到新场景",
    model="W2.7r",
    image_url_list=["https://example.com/ref1.jpg", "https://example.com/ref2.jpg"],
    video_url_list=["https://example.com/ref.mp4"],
    ratio="16:9",
    resolution="720p",
    duration=10
)

# klingV3Omni - 多模态融合（按张计费）
result = generate_video(
    prompt="镜头一致性多图融合",
    model="klingV3Omni",
    image_url_list=["https://example.com/scene1.jpg", "https://example.com/scene2.jpg"],
    ratio="16:9",
    duration=8
)

if result and result["status"] == "SUCCESS":
    print(f"链接: {result['url']}")

# 视频 - 默认 V3.1FB
result = generate_video(prompt="小骏马祝福大家新年快乐")

# 视频 - 指定比例、分辨率、时长
result = generate_video(
    prompt="海边日落风景",
    model="S1.5Pro",
    ratio="9:16",
    resolution="1080p",
    duration=5
)

if result and result["status"] == "SUCCESS":
    print(f"视频链接: {result['url']}")
```

## 返回字段

| 字段 | 说明 |
|------|------|
| `status` | SUCCESS / FAILED / TIMEOUT |
| `url` | 图片URL |
| `message` | 状态描述 |
| `local_path` | 本地保存路径（需 --download） |
| `data_uri` | Base64 Data URI（需 --download） |
| `image_data` | 原始图片字节（需 --download） |

## 环境配置

### 必需配置 - API Key

**重要：使用前必须设置你自己的 API Key！**

#### 获取 API Key

本技能需要 **API Key 授权**：

1. 访问入口：
   - **已有账号** → [https://ai.deepsop.com/login?source=2](https://ai.deepsop.com/login?source=2) 登录获取
   - **没有账号** → [https://ai.deepsop.com/register?source=2](https://ai.deepsop.com/register?source=2) 注册获取
2. 登录后在复制您的 API Key
3. 复制生成的 API Key（格式：`sk-xxxxxx...`）

#### 方式 1：使用 .env 文件（推荐）

1. 复制 `.env.example` 为 `.env`：
   ```bash
   cp .env.example .env
   ```

2. 编辑 `.env` 文件，填入你的 API Key：
   ```bash
   AI_ARTIST_TOKEN=sk-your_api_key_here
   ```

3. 在运行脚本前加载环境变量：
   ```bash
   # Linux/macOS/Git Bash
   source .env

   # 或使用 export
   export $(cat .env | xargs)
   ```

#### 方式 2：直接设置环境变量

##### Linux / macOS / Git Bash (Windows)

```bash
export AI_ARTIST_TOKEN="sk-your_api_key_here"
```

为了永久生效，将上述命令添加到 `~/.bashrc` 或 `~/.zshrc` 文件中。

##### Windows PowerShell

```powershell
$env:AI_ARTIST_TOKEN="sk-your_api_key_here"
```

永久设置（系统级）：
```powershell
[System.Environment]::SetEnvironmentVariable('AI_ARTIST_TOKEN', 'sk-your_api_key_here', 'User')
```

##### Windows CMD

```cmd
set AI_ARTIST_TOKEN=sk-your_api_key_here
```

#### 验证配置

运行以下命令验证 API Key 是否设置成功：

```bash
# Linux/macOS/Git Bash
echo $AI_ARTIST_TOKEN

# Windows PowerShell
echo $env:AI_ARTIST_TOKEN

# Windows CMD
echo %AI_ARTIST_TOKEN%
```

如果输出为空或显示默认值，说明环境变量未正确设置。

#### 测试配置（推荐）

运行配置测试脚本，验证 API Key 是否正确设置：

```bash
python3 scripts/test_config.py
```

该脚本会检查：
- API Key 是否已设置
- 是否使用了默认 Key（需要替换为你自己的）
- 配置是否可以正常使用

### 可选配置 - 飞书通知

```bash
export FEISHU_WEBHOOK_URL="https://open.feishu.cn/open-apis/bot/v2/hook/xxx"
```

## 相关文件

- `scripts/generate_image.py` - 主脚本
- `references/api.md` - API 详细文档
