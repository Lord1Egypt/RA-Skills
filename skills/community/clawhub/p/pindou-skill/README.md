<div align="center">

<img src="assets/logo.png" alt="pindou-skill logo" width="320">

# pindou-skill · 拼豆 skill

> *"拼豆 skill:一句话选色、一句话映色号、一句话出图纸 —— Photo to Pattern, in one breath."*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://python.org)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![Model](https://img.shields.io/badge/Model-gpt--image--2-black)](https://platform.openai.com/docs/guides/images)
[![Palette](https://img.shields.io/badge/Palette-MARD%20221-ff69b4)](palettes/mard_221.csv)

<br>

📷 拍一张猫 / 选一个动漫人物 / 选一个游戏 IP / 喂一段文字描述<br>
告诉 skill 你要什么画风、要不要保留背景、最多用几种豆子<br>
**直接拿走可打印图纸 + 采购清单**

<br>

不用先 PS、不用手画像素图、不用查色号 —— 一切交给 skill。

[ Pipeline ](#pipeline) · [ Install ](#install) · [ Usage ](#usage) · [ License ](#license)

</div>

---

<!-- ![teaser-v1](assets/teaser_v1.webp) -->

![teaser-v2](assets/teaser_v2.webp)

![teaser-latte](assets/teaser_latte.webp)

## Features

- **参考图直出图纸** — 不需要先 PS、不需要手画像素图,聊几句风格就行
- **照片 / 纯文字两条入口** — 给照片走 `edit.py`(图像编辑),只给文字走 `generate.py`(文生图),后半段管线一致
- **AI 出图 + 程序提取双保险** — gpt-image-2 负责生图,Python 按网格中位数取色 + Lab/CIEDE2000 映射到色板
- **可编辑 SVG** — 最终图纸是真 SVG (cells / grid_lines / color_codes / bom 各一组),想改色号、调字号、换调色板都可以
- **可换调色板** — 当前支持 MARD 系列豆子,后续会支持更多拼豆色板

## Pipeline

![pipeline](assets/pipeline.png)

一句话:`照片 / 文字` → `spec.json + 中文 prompt` → `gpt-image-2 (edit / generate)` → `ai_pixel.png 带网格的 AI 像素图` → 反推网格 + Lab/CIEDE2000 映射 MARD 色板 → `pattern.png` + `pattern.svg` + `bom.csv`。

中间还会落地几个产物作为 pivot —— `raw.svg`(每格 RGB 中位数,未 snap)、`grid.json`(snap 完的 cell 矩阵 + bg mask + bom),都是图纸生成阶段的内部交接格式,不是终态交付物。SVG 在这里只是顺手做了一份可编辑矢量,真正给你打印的是 `pattern.png` 和 `bom.csv`。

## Install

把这个目录放到 `~/.claude/skills/pindou-skill/`,然后安装基础环境(让 AI 辅助安装 anaconda 环境或者 venv 均可):

```bash
pip install openai opencv-python-headless "numpy<2" scipy scikit-image pandas pillow cairosvg
```

API key 和 endpoint 直接写在 `scripts/edit.py` 和 `scripts/generate.py` 顶部:

```python
API_KEY = "xxx"                              # 把 xxx 换成你的真实 key
BASE_URL = "https://api.bianxie.ai/v1"       # 默认走 bianxie 中转,可自行替换
DEFAULT_MODEL = "gpt-image-2"                # bianxie 的 gpt-image-2,与 gpt-image-1 调用方式一致
```

想换 OpenAI 官方就把 `BASE_URL` 改成 `https://api.openai.com/v1`。bianxie 注册见 https://api.bianxie.ai 。

## Usage

在 Claude Code 里直接说"帮我把这张照片做成拼豆图纸"就会触发,skill 会主动跟你确认画风 / 尺寸 / 底色 / 颜色数。

也可以脚本化跑,完整命令见 [`SKILL.md`](SKILL.md)。

## Layout

```
pindou-skill/
├── SKILL.md                # Claude Code 触发入口 + pipeline 说明
├── README.md               # 本文件
├── assets/
│   ├── logo.png
│   ├── teaser_v1.webp
│   ├── teaser_v2.webp
│   └── pipeline.png
├── scripts/
│   ├── generate.py         # 文生图: prompt -> png (没有照片走这条)
│   ├── edit.py             # 图编辑: photo + prompt -> png (有照片走这条)
│   ├── spec_to_prompt.py   # spec.json -> 中文 prompt
│   ├── extract_svg.py      # ai_pixel.png -> raw.svg (按网格中位数取色)
│   ├── svg_to_grid.py      # raw.svg + palette -> grid.json (Lab/CIEDE2000 snap + bg 检测)
│   ├── quantize.py         # snap / bg 检测 / max_colors 工具(被 svg_to_grid 复用)
│   ├── render_pattern.py   # grid.json -> pattern.svg + pattern.png + bom.csv
│   └── make_teaser.py      # 拼三栏 teaser webp(参考图 + AI 像素图 + 拼豆图纸)
└── palettes/
    └── mard_221.csv        # MARD 标准 221 色
```

## License

MIT
