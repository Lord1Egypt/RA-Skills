---
name: pindou-skill
description: 拼豆图纸一键生成。用户给一张照片想做成拼豆图纸 / 想做"拼豆"/"perler"/"像素图"/"网格图"/"用豆子拼"时使用。流程:谈风格、生成像素图、提取色块、出可打印的网格图纸 + 色号 + 采购清单。
---

# pindou-skill: 拼豆图纸一键生成

把一张照片(或一段文字描述)做成可打印的拼豆图纸。pipeline 五步:

1. 跟用户聊清楚风格 / 尺寸 / 底色 → 写 `spec.json`
2. 把 spec 翻成中文 prompt
3. **分支:用户给了照片 → `edit.py`(图像编辑);只给文字 → `generate.py`(文生图)** → `ai_pixel.png`
4. **暂停让用户看 `ai_pixel.png`**,不满意就改 prompt 重抽
5. 提取色块 → 量化 → 渲染最终 `pattern.png` + `bom.csv`

---

## 0. 环境准备

依赖:
```bash
pip install openai opencv-python-headless "numpy<2" scipy scikit-image pandas pillow
```

API key / endpoint 配置:`scripts/edit.py` 和 `scripts/generate.py` 顶部的 `API_KEY` 和 `BASE_URL` 直接写在文件里,默认走 `https://api.bianxie.ai/v1`(bianxie 中转的 gpt-image-2)。换 OpenAI 官方就改 `BASE_URL = "https://api.openai.com/v1"`、`DEFAULT_MODEL = "gpt-image-1"`。

工作目录约定: 把当前会话的产物都丢进 `outputs/<run_name>/` 一个目录里(spec、prompt、ai_pixel、raw.svg、grid.json、pattern.png 一起)。`<run_name>` 用语义+模型 tag,别只用时间戳。

---

## 1. 跟用户聊参数(用日常语言,别抛术语)

不要把"spec_lock / commit / palette_id"这种词丢给用户。用日常说法逐个确认:

- **照片**: 让用户给路径(本地图片)。如果用户**只给文字、没有照片**,跳到第 3 步用 `generate.py` 文生图。
- **画风**: 写实 / 卡通 / 扁平纯色 / 黑白二值 (对应 `style`: `realistic` / `cartoon` / `flat` / `binary`)。
- **网格尺寸**: 默认 36×36 左右 或 50×50,按主体长宽比给个估计。"小一点更好拼"就 36×36,"大一点更精细"就 60×60+。**注意**: 这是建议值,真实网格数以 AI 实际画出为准,`svg_to_grid` 会从 SVG 反推。
- **背景怎么处理**: 三选一 —
  - 保留原背景 (`background_mode: keep`)
  - 抠掉换纯色,需要让用户给颜色 (`background_mode: solid`, `background_color: #FFFFFF` 之类)
  - 直接挖空,只拼主体 (`background_mode: remove`)
- **最多几种颜色**: 默认 18 (越少越好买、越好拼;越多越像照片)。
- **保留哪些细节**: 例如"耳朵的粉色一定要在"、"眼睛要亮一点"。
- **要 AI 一次画几张候选给你挑?**: 默认 1。建议问用户:"AI 一次出 1 / 2 / 3 / 4 张候选给你挑一张?多张能减少反复重抽,但每多一张就多一次 token 消耗。" 写到 spec.json 的 `n_candidates`。如果用户没主动选,默认 1。

把上面这些写到 `outputs/<run_name>/spec.json`:

```json
{
  "spec_id": "<run_name>",
  "palette_id": "mard_221",
  "grid_w": 36,
  "grid_h": 54,
  "style": "cartoon",
  "background_mode": "solid",
  "background_color": "#FFFFFF",
  "max_colors": 18,
  "must_include_colors": [],
  "forbid_colors": [],
  "preserve_features": ["眼睛保持高亮", "耳朵内侧的粉色保留"],
  "ai_draws_grid": true,
  "cell_px": 20,
  "show_grid_numbers": true,
  "show_color_codes": true,
  "n_candidates": 1
}
```

> `cell_px` 是最终图纸里每格画多大(像素),不是网格数。建议 20-40,A4 打印用 40 比较舒服。

> **调色板**: 默认用 `${SKILL_DIR}/palettes/mard_221.csv` (MARD 标准 221 色)。用户提供别的就换。

---

## 2. spec → 中文 prompt

```bash
python ${SKILL_DIR}/scripts/spec_to_prompt.py \
    outputs/<run_name>/spec.json \
    -o outputs/<run_name>/image_prompt.txt
```

不需要修改 prompt 文本。

---

## 3. 生成候选像素图(带网格)

**分支**:

`--n` 取自 spec.json 的 `n_candidates`(用户在第 1 步选的)。一次出 N 张候选,用户在第 4 步挑一张。

### 3a. 用户给了照片 → 走 `edit.py`(图像编辑)

```bash
PROMPT="$(cat outputs/<run_name>/image_prompt.txt)"
N=$(python -c "import json; print(json.load(open('outputs/<run_name>/spec.json')).get('n_candidates', 1))")
python ${SKILL_DIR}/scripts/edit.py \
    <user_photo> "$PROMPT" \
    --size 1024x1536 --quality medium \
    --n $N \
    --tag <run_name> \
    --out-dir outputs/<run_name>
# 输出会是 *_edit_<run_name>_0.png ... *_edit_<run_name>_<N-1>.png 一共 N 张
```

### 3b. 用户只给文字、没有照片 → 走 `generate.py`(文生图)

```bash
PROMPT="$(cat outputs/<run_name>/image_prompt.txt)"
N=$(python -c "import json; print(json.load(open('outputs/<run_name>/spec.json')).get('n_candidates', 1))")
python ${SKILL_DIR}/scripts/generate.py \
    "$PROMPT" \
    --size 1024x1536 --quality medium \
    --n $N \
    --tag <run_name> \
    --out-dir outputs/<run_name>
# 输出会是 <run_name>_0.png ... <run_name>_<N-1>.png
```

> 生成的图必须是带可见网格线的像素图(每格内部基本纯色)。提取脚本依赖网格线的存在,这是 prompt 已经强约束的部分。

---

## 4. **暂停让用户看图 → 挑一张作为 ai_pixel.png(STOP)**

**这一步必须 STOP**,不要绕过。

- N=1: 把唯一一张候选给用户看,问一句:**"这张像素图你 OK 吗?要不要重抽 / 改风格 / 改色数?"**
- N>1: 把 N 张候选并排给用户看(可以用 `make_teaser.py` 或者直接附图),问:**"这几张里你最喜欢哪张?(也可以全部不要,我们重抽)"**

用户挑中之后,把那张 cp 成 `outputs/<run_name>/ai_pixel.png`:

```bash
cp outputs/<run_name>/*<run_name>*_<idx>.png outputs/<run_name>/ai_pixel.png
```

如果用户说全部不满意要重抽:**先问用户调什么再抽,不要默默重抽**。可调项:
- 改 spec.json 里的 `style` / `max_colors` / `preserve_features` / `background_mode`
- 改 prompt(让用户口述调整方向,你修订 image_prompt.txt 后再跑 3)
- 增加 `n_candidates` 一次多抽几张

---

## 5. 提取色块 → 量化 → 出图

### 5a. 从 ai_pixel.png 按网格线取每格中位数色 → raw.svg

```bash
RUN=outputs/<run_name>
python ${SKILL_DIR}/scripts/extract_svg.py \
    $RUN/ai_pixel.png \
    $RUN/raw.svg \
    --debug-dir $RUN/debug
```

debug 阶段两张图人眼校验:
- `$RUN/debug/grid_lines.png`: 红/绿线压在网格上,如果偏移就说明 adaptiveThreshold 参数对这张图不对路。
- `$RUN/debug/cells.png`: 每格中央的黄色框是采样区,要在格内、不压网格线。

### 5a-check. **AI 实际画出的网格数 ≠ spec.grid_w/h 时必须 STOP 询问用户**

extract_svg 的输出会打印类似 `[extract] grid 30 x 30 = 900 cells`。如果这个 grid 数与 spec.json 的 `grid_w` / `grid_h` 不一致,**绝对不要默默重抽消耗 token**,把情况摆给用户:

> "你要求的是 36×36,但 AI 实际画成了 44×44。两个走法选一个:
> ① 接受 44×44 直接出图(豆数会变多)
> ② 重新让 AI 画一次,prompt 加强网格数约束(会再花一次 API 费用)
> ③ 改 spec 把目标改成 44×44(等于承认 AI 画的)"

只有用户明确说"重抽"才回 Step 3。如果用户没回应或者回应模糊,**默认接受当前网格继续走 5b**,不要擅自重抽。注意:gpt-image 对精确网格数的控制力本身有限,1-3 格的偏差很常见,不一定是失败 — 让用户判断。

### 5b. raw.svg + spec + palette → grid.json + quantized.png

```bash
python ${SKILL_DIR}/scripts/svg_to_grid.py \
    --svg $RUN/raw.svg \
    --spec $RUN/spec.json \
    --palette ${SKILL_DIR}/palettes/mard_221.csv \
    --out-dir $RUN/
```

### 5c. grid.json → 最终 pattern.png + pattern.svg + bom.csv

```bash
python ${SKILL_DIR}/scripts/render_pattern.py \
    --grid $RUN/grid.json \
    --palette ${SKILL_DIR}/palettes/mard_221.csv \
    --out-dir $RUN/ \
    --cell-px 40
```

---

## 6. 把结果给用户

最终交付:
- `outputs/<run_name>/pattern.png` — 主图,带行列号 + 每格色号 + 右侧采购清单
- `outputs/<run_name>/bom.csv` — 色号清单和数量

---

## 关键约束(改 prompt 或脚本前必读)

- **背景语义 = 不拼**: 当 `background_mode` 是 `solid` 或 `remove` 时,bg 格子在最终图纸里要留空、不进采购清单,**不要**把它当成"白豆 H1"算进去。`quantize.py` 里的 `detect_bg_and_pure_fg_masks` 用 connected-component 分"真背景 (连图边)"和"主体内部白窟窿"。
- **颜色聚类必须在 Lab 空间**: 别在 RGB 里做 K-Means,会把暖棕+暗影合成中性灰然后映射到橄榄绿。`quantize.py` 已经走 CIEDE2000 ΔE,不要绕开。
- **vision 阶段不做 snap**: `extract_svg.py` 只产 raw.svg(每格 RGB 中位数,floating-point 颜色),色板 snap / max_colors / must_include 都是 `svg_to_grid.py` 的事。两个阶段解耦,不要在 extract 阶段提前 snap。
- **图像后处理 (icons / crop / aspect 修正)**: 留给未来 SAM+扩散+占位符 pipeline,纯 SVG 主线不要主动挂这些。
- **不要默默重抽烧 token**: 任何"AI 出图与 spec 不一致"的情况(网格数偏差、构图不对、色调跑偏),都先停下问用户怎么办,提供"接受 / 重抽 / 改 spec"三选,绝对不要为了"修对"擅自再调一次 API。多张候选用 `n_candidates` 一次性出比反复重抽便宜。

---

## 文件结构

```
${SKILL_DIR}/
├── SKILL.md             (本文件)
├── README.md            (开源说明)
├── scripts/
│   ├── generate.py         # 文生图: prompt -> png(没有照片走这条)
│   ├── edit.py             # 图编辑: photo + prompt -> png(有照片走这条)
│   ├── spec_to_prompt.py   # spec.json -> 中文 prompt
│   ├── extract_svg.py      # ai_pixel.png -> raw.svg(按网格中位数取色)
│   ├── svg_to_grid.py      # raw.svg + palette -> grid.json(Lab/CIEDE2000 snap)
│   ├── quantize.py         # snap/bg-detect/max-colors 工具(被 svg_to_grid 调)
│   ├── render_pattern.py   # grid.json -> pattern.png + pattern.svg + bom.csv
│   └── make_teaser.py      # 拼三栏 teaser webp(参考图 + AI 像素图 + 拼豆图纸)
└── palettes/
    └── mard_221.csv     # MARD 标准 221 色
```
