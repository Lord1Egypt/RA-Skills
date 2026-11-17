---
name: ins-style-img-bulk-gen
description: Generate batches of Instagram-aesthetic photos (INS-style / Xiaohongshu / lifestyle flat-lay) by randomly composing prompts from an 80+ element library, then dispatching them in parallel to image generation skills and archiving to ~/Download/ins-image-{timestamp}/. Use when the user wants bulk INS-style images, lifestyle flat-lays, Xiaohongshu or WeChat cover art, or scene-based marketing visuals — even if they don't say 'Instagram' explicitly.
allowed-tools: Read, Bash
author: JackyShen
argument-hint: "[-s SCENE] [-c COUNT] [-t TEXT]"
---

## 硬性要求 / Hard Requirements

执行本 skill 时必须满足以下规范（任何一条不达标 = 产出不合格）：

| # | 规范 | 约束值 / 操作 | 出处 |
|---|---|---|---|
| 1 | **封面字号（cover 模式）** | base = `0.07 × 图片高`（≈ 70px @ 1024h，比最初 80px 还小一点），下限 `0.05`，**行距 `0.18 × 字号`**（紧凑）；**2 行结构**（最长行 ≤ 8 字，按重要性递减排列，具体内容由领域决定） — 让标题横向占图宽 ≥ 70% | 2026-09-20 迭代 |
| 2 | **Shell `\n` 必须是真换行** | 用 `$'…\n…'`（ANSI-C）或 `printf '%b'`；**禁止**普通双引号（会把字面 `\n` 画进图） | 上轮反馈 #1 |
| 3 | **生图模型优先级** | 首选 `huny-img`（腾讯混元 3.0） → 备选 `mmx` → 最后才用其他模型；huny-img **串行**提交（账号 JobNumExceed 上限 1，并发会限流） | 上轮反馈 #2 |
| 4 | **内页图（`mode=ins`）body 必须 ≥ 3 行** | 不含 title 的正文至少 3 行，画面才饱满；用户原文不够时主动从他给的文案里拆 3-4 个短句 | 上轮反馈 #3 |
| 5 | **内页正文 < 标题**（提高对比） | `INS_BODY_RATIO = 0.020`（标题 = 0.035），标题/正文 ≈ 1.75×，层级清晰 | 2026-09-20 迭代 |
| 6 | **Cover 必须是 2x2 宫格**（4 张拼 1 张） | 4 张图用 `scripts/compose_collage.py` 拼成 `--layout 2x2`，cell 之间建议 `--gap 20~40px`、背景色用 `245,240,232`（暖白，与 INS 色调一致）；4 张图共享视觉风格（色温 / 色调 / 质感）但呈现**不同元素/视角**，避免 4 张图重复 | 2026-09-20 迭代 |
| 7 | **Cover / 内页默认符合小红书尺寸**（**3:4 竖图**） | `compose_collage.py` 默认 `--cell-aspect 3:4` → cell 居中裁剪到 3:4，再拼成 2x2 → 整体 ≈ **3:4 竖图**；最终输出尺寸默认 `--target-size 1080x1440`（小红书 cover 标准），用 `add_ins_overlay.py` 加标题后直接上传即可。内页图（ins 模式）也按 3:4 生成，单图 768:1024（huny-img 默认 3:4 比例）。如要 4:3 横图或 1:1 方图，传 `--cell-aspect` / `--target-size` 覆盖即可 | 2026-09-20 迭代 |

脚本默认常量已同步：`scripts/add_ins_overlay.py` 的 `COVER_TITLE_RATIO / FLOOR / LINE_GAP` 与本表一致。

---

## ins-style-image [-s SCENE] [-c COUNT] [-t TEXT]

1. Read `./references/ins-style-elements.md` to understand the available element library
2. Compose prompts. Default to **5 prompts** if the user doesn't specify a `{COUNT}`. Each prompt randomly draws **12 elements** (1-2 per category, no duplicates within one prompt) for `{SCENE}` if specified.
   - **Cover 模式**（硬性）：**4 个 prompt**，每个对应 1 个宫格 cell（2x2 = 4 格）。4 张图共享视觉风格（同一色温 / 色调 / 质感 / 光照方向）但展示**不同元素或视角**（例如音乐主题：①唱片堆叠 ②耳机特写 ③黄铜烛台与干花 ④复古相机与乐谱），避免 4 张图内容雷同
   - **内页模式**：1 prompt 1 张，按用户需要的内页数生成；单图默认 3:4 竖图（小红书内页标准），与 cover 视觉风格一致（色温 / 色调 / 质感统一）
   - User may also ask for 3x3 or other collage layouts or customize with given images — calculate count accordingly.
3. Iterate the prompt queue and dispatch them **in parallel** to image generation skills in the following priority order:
   - **🥇 首选 `huny-img`**（腾讯混元生图 3.0）— 详情见 `~/.agents/skills/huny-img/SKILL.md`。`hunyuan3-text-to-image.py` 或 `hunyuan3-batch.py`（多 prompt 调度）
   - **🥈 备选 `mmx`**（MiniMax 多模态 CLI，`mmx image generate`）— 仅当 huny-img 不可用、缺凭证、或 JobNumExceed 限流时
   - **🥉 其他模型**（如 `image-01-live` / Midjourney 等）— 最后才考虑
   
   ⚠️ **huny-img 串行提交**：腾讯云账户默认 1 个并发任务上限，并发提交会触发 `RequestLimitExceeded.JobNumExceed`。多 prompt 串行调度用 `hunyuan3-batch.py`（内置 5 次退避重试）。
4. Save all generated images to `~/Download/ins-image-{timestamp}/`
5. If user specifies `{TEXT}` (or provides a quote/aphorism), you must execute `scripts/add_ins_overlay.py` (using libraries Pillow) to post-process the generated single image or collage. There are **two modes** — pick per the user's intent:

   ### 5A. `mode=ins` (default) — 灰蒙版 + 标题 + 正文

   - **CLI usage**: `python scripts/add_ins_overlay.py -i input.jpg -o output.jpg -t "title" -b "body" -p {bottom|auto|center}` (use `--body-file` for longer text)
   - **Default position is `bottom`** — protects top-region visual focal points in collage/single-image scenes, matching INS aesthetic conventions. Override with `--position auto` if the user explicitly wants auto blank-space detection.
   - **Smart Adaptive Layout**: Automatically analyze the image composition and visual weight to determine the optimal placement for a semi-transparent text box (overlay). Position it in natural blank/negative spaces (留白) if available. If the text is exceptionally long or content density is high, dynamically expand the overlay to cover the full width or entire page.
   - **Overlay Style**: Apply a neutral gray semi-transparent mask with an opacity of around 0.65-0.7 (matching an elegant lifestyle magazine aesthetic, as referenced in style guides).
   - **Typography & Hierarchy**:
     - **Title/Heading**: Bold, clean sans-serif or elegant serif font, crisp white color, accented with a subtle leading symbol (e.g., "❤" or numbering like "3、") if present in the text.
     - **Body Text**: Regular weight, smaller font size, comfortable line spacing (leading) for readability, soft off-white or light gray color.
   - **Drop Shadow & Depth**: Both title and body text carry a soft Gaussian-blurred drop shadow (offset 2–3 px down-right, alpha ≈ 120, blur radius 1.2–2.0 px). The shadow is intentionally subtle — never a hard-edged duplicate — so the white text reads as floating slightly above the gray mask rather than pasted onto it.
   - **Execution**: Save the processed final image back to the target directory, ensuring high visual quality and natural blending.
   - 🔴 **【硬性要求】正文 ≥ 3 行**（不含 title）。少于 3 行画面空、信息密度不够。如用户原文 < 3 句，**主动从他给的文案里拆 3-4 个语义完整的短句**（每行 ≤ 18 字，标点收尾），不要默默把短文硬塞进 1-2 行。

   ### 5B. `mode=cover` — 社媒封面：**2x2 宫格 + 无蒙版大字标题**

   Use when the user asks for a **封面 / cover / 社媒封面 / 头图**, or says the image is destined to be a 小红书 / 公众号 / 视频号 cover.

   **两步走**：

   **Step 1：4 张图拼 2x2 宫格**（硬性）：
   ```bash
   python scripts/compose_collage.py \
     -i cell_topleft.jpg cell_topright.jpg cell_bottomleft.jpg cell_bottomright.jpg \
     -o cover_grid.jpg \
     --layout 2x2 \
     --gap 24 \
     --bg 245,240,232 \
     --cell-aspect 3:4 \
     --target-size 1080x1440
   ```
   - `--cell-aspect 3:4` 默认就是 3:4（小红书标准竖图），cell 会先按此比例居中裁剪再拼图
   - `--target-size 1080x1440` 默认就是小红书 cover 标准尺寸；省略则保留拼图自然尺寸
   - `--gap 20~40px` 视观感调整（0 = 无缝拼接；推荐 24 让宫格感更明显）
   - `--bg 245,240,232` 暖白与 INS 色调一致（也可用纯白 `255,255,255`）
   - 如果要 4:3 横图或 1:1 方图：传 `--cell-aspect 4:3` + `--target-size 1440x1080` 或 `--cell-aspect 1:1` + `--target-size 1080x1080`

   **Step 2：在 2x2 拼图上加 cover 文字**：
   ```bash
   python scripts/add_ins_overlay.py \
     -i cover_grid.jpg \
     -o cover_with_title.jpg \
     -m cover \
     -t $'第一句\n第二句'
   ```
   - 字号自动按拼图尺寸缩放（cover 字号 = `0.07 × 拼图高`），拼图比单图大 → 字号同比放大；如觉得太大，把标题改成更短/调 `--bg`/或在拼图前 resize
   - 🔴 **只有 title，没有 body**。cover 模式**忽略** `-b` / `--body-file`。不要把金句正文塞进封面。
   - 🔴 **只有 title，没有 body**。cover 模式**忽略** `-b` / `--body-file`，CLI 在 cover 模式下也不再强制要求正文。不要把金句正文塞进封面。
   - **不加灰色蒙版** —— 改为**居中大字标题 + 黑白描边 + 加强阴影**，靠粗描边保证在任何背景上都读得清（这是封面图与内页图的根本区别）。
   - **【硬性】字号规格**（与 `scripts/add_ins_overlay.py` 常量一致）：
     - base = `0.07 × 图片高`（≈ 70px @ 1024h，比最初 80px 还小一点，更克制）
     - floor = `0.05 × 图片高`（≈ 51px @ 1024h，下限保护）
     - **行距 = `0.18 × 字号`**（紧凑，约 13px @ 70px；三行收紧成块，避免"太大太松"）
     - 实际字号随图片宽高自动在 base ↔ floor 之间缩档
   - **【硬性】2 行结构**（与具体领域无关 — 音乐 / 美食 / 旅行 / 商业皆适用）：
     - **2 行**，最长行 ≤ 8 字（按 base ratio 0.07 的实测上限；超过会被脚本自动缩档）
     - 行间排序按重要性：第 1 行 = 最核心标识符（品牌 / 主体 / 人名 / 概念名等），第 2 行 = 关键信息 / 钩子 / 金句
     - 长关键词必须单独成行，**绝不**挤压到上一行末尾（这会触发脚本的语义断行猜错）
     - **目标：最长行占图宽 ≥ 70%**（保证标题"横向撑得开"，不被夹在中间像孤岛）
     - 例外：标题 ≤ 8 字 → 1 行；标题过长（> 16 字）→ 3 行（仍是上限）
   - **位置恒为居中**（水平+垂直），`-p/--position` 被忽略。
   - 🔴 **Shell 调用必须把 `\n` 传成真换行**。zsh / bash 普通双引号里的 `\n` 是字面量（两个字符 `\` + `n`），脚本会把它们原样画进图里。正确写法：
     - ✅ zsh / bash ANSI-C 引号：`$'背叛情歌\n电吉他\n比牛仔还忙'`
     - ✅ `printf '%b' '背叛情歌\n电吉他\n比牛仔还忙'`
     - ❌ 普通双引号：`"背叛情歌\n电吉他\n比牛仔还忙"`（实测渲染出可见的 `\n` 字符）
   - 🔴 **你必须自己用 `\n` 指定断行**。脚本**不做语义断句** —— 它只会在你没给 `\n` 时按显示宽度均衡切分，并保证禁则不出错（不断标点、不切断 `40+` 这类数字串）。像「40+后才明白 ｜ 女人越来越差的9个原因」这种主谓边界，脚本**猜不出来**（实测它会断成「40+后才明白女人 ｜ 越来越差的9个原因」）。**判断语义是你的职责**：
     - 标题 ≤ 8 字 → 一行，不写 `\n`
     - 更长 → 切成 2 行（最多 3 行），在**语义完整处**断开
     - 每行显示宽度尽量接近（CJK 算 2，ASCII 算 1）
     - 正例：`-t "40+后才明白\n女人越来越差的9个原因"`
     - 反例：`-t "40+后才明白女人越来越差的9个原因"`（全靠脚本猜 → 断得不好看）

## Font Recommendations

- **Title (Bold)**: PingFang SC Semibold, Microsoft YaHei Bold, Source Han Sans CN Bold, Hiragino Sans GB W6.
- **Body (Regular)**: Source Han Serif CN, LXGW WenKai (霞鹜文楷), Songti SC, Arial, SimHei.
- **Cross-platform fallback**: `Arial Unicode MS` — pre-installed on both macOS (`/Library/Fonts/Arial Unicode.ttf`) and Windows (`C:\Windows\Fonts\Arialuni.ttf`). Covers nearly all Unicode including ❤ ★ ♡ → and full CJK.
- The script auto-detects platform fonts via `ImageFont.truetype(...)` and runs a CJK width sanity check (`textlength("中文") >= 1.2 × textlength("AA")`) to skip fonts that would render tofu boxes. Pass `title_font_path` / `body_font_path` to override.
  - ⚠️ The threshold is **1.2, not 1.5**. Measured at 40 px, real CJK fonts score 1.33–1.50 (Hiragino 1.333, Songti 1.443, Arial Unicode 1.499) while a tofu font scores ≈0.95 (Helvetica 0.950). A 1.5 threshold rejects *every* real CJK font — don't "tighten" it back.

### ⚠️ Pillow Gotcha — No automatic cross-font fallback

Pillow's `ImageDraw.text()` renders every character in a run using **the same font**. It does NOT perform Unicode-fallback (unlike CSS font-family stacks). Practical consequences:

- CJK fonts (Hiragino Sans GB / Source Han Sans / 思源黑体) often lack decorative symbols: `❤ ★ ♡ → ◆ ✓` — Pillow renders them as a tofu rectangle with an X (a "missing glyph box"), which looks like garbage on top of an otherwise clean image.
- Detection is non-trivial: `font.getmask(ch).getbbox()` returns non-None for tofu; alpha values are non-zero. The only reliable signal is **checking the character class** and explicitly routing decorative symbols to a font that contains them.
- The script implements this via `_pick_font_for_char(ch, main_font, sym_font)`: CJK / ASCII / digits / Latin → main font; anything outside those ranges (decorative Unicode blocks) → symbol font (`Arial Unicode MS` first, then Apple Symbols / Segoe UI Symbol / Noto Sans Symbols 2).

**Rule of thumb when adding new glyphs**: don't trust "looks fine in my test image" — always verify by rendering `font.getmask(ch)` and comparing the mask to a known-good one. Or just route anything outside Latin/CJK through `symbol_font`.

## Prompt Skeleton

Fill each prompt using the following template:

```
[Subject scene, 3-4 sentences, incorporating elements 1-12]. Unified Morandi / cream / wood-tone palette. 3:4 aspect ratio. Relaxed INS aesthetic.
```

## setup python library

```bash
pip install --break-system-packages Pillow
```

## Gotchas

- **Must return to this flow** ⚠️: The image generation skill is only a sub-step. After generation completes, return to this skill and execute step 4 (archiving). Do not leave control inside the sub-skill.
- **Avoid duplicate elements**: Don't repeat the same element within one prompt (e.g. "vintage book stack" + "open book").
- **Sub-skill failures**: Skip the failed prompt and continue with the remaining queue. Don't abort the entire batch.
- **Shell `\n` 字面量陷阱**：调用 `add_ins_overlay.py` 时，**务必**用 `$'…'` 把 `\n` 传成真换行（详见 5B 的硬性要求第 1 条）。普通双引号会把字面 `\n` 字符画进图里。

## 小红书尺寸速查（默认即下表第一行）

| 用途 | 比例 | 像素尺寸 | 备注 |
|---|---|---|---|
| **Cover（默认）** | **3:4** | **1080x1440** | 小红书主页封面/头图推荐尺寸，最常见 |
| 内页（默认） | 3:4 | 768x1024 | huny-img 3:4 默认输出，单图直接发 |
| 视频封面 | 1:1 | 1080x1080 | 方图，少见但合法 |
| 横图（少见） | 4:3 | 1440x1080 | 横幅，需要 `--cell-aspect 4:3` |

调用 `compose_collage.py` 时不传 `--target-size` 会保留拼图自然尺寸（按 cell 实际像素算），如要严格 1080x1440 必须显式传。
