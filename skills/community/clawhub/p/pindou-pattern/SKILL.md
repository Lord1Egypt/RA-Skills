---
name: pindou-pattern
description: 生成拼豆图纸（perler bead pattern，简易版）。把任意图片或像素数据量化为真实拼豆色号的拼豆施工图——输出可缩放/可打印的 SVG 图纸（格内色号、行列坐标、每 10 格加重线、配色清单）+ HTML 预览 + CSV 物料清单 + JSON 网格。内置 205 色 × 5 品牌（MARD/COCO/漫漫/盼盼/咪小窝）色号对照，纯标准库、零外部依赖。当用户提到拼豆、拼豆图纸、色号、把图片转成 N×N 拼豆、像素画导出、串珠/珠子图案、perler bead pattern、bead pattern 时使用。
---

# 拼豆图纸生成（pindou-pattern · 简易版）

把图片或像素数据变成可直接照着拼的拼豆图纸：深色标题栏 + 四周行列坐标 + 网格（格内标品牌色号、每 10 格加重线）+ 配色用量清单 + 可打印/下载的 HTML 预览。

**特性**：纯 Python 标准库实现，无需 `npm install`、无需 Pillow、无需联网。内置 PNG 解码器（图片输入直接用 PNG；装了 Pillow 则额外支持 JPG/WebP 等）。

## 快速开始

```bash
# 图片 → 32×32 MARD 图纸（输出 <输入名>_pattern.svg 与同名 .html）
python pindou-pattern/scripts/pindou.py 卡通猫.png

# 指定品牌、尺寸、标题，近白背景当空格，收敛到 16 色，并导出 CSV 物料清单
python pindou-pattern/scripts/pindou.py 卡通猫.png \
  --size 48 --system 盼盼 --title 卡通猫 --blank-white --max-colors 16 --csv 清单.csv

# JSON 像素数据 → 图纸 + CSV 物料清单
python pindou-pattern/scripts/pindou.py 作品.json --csv 物料.csv
```

> 运行环境：使用本会话管理的 Python 解释器（或任意 `python3`），脚本仅用标准库，开箱即用。

## 输入格式

- **图片**（png 优先；装 Pillow 后支持 jpg/webp/bmp/gif/tiff）或 **JSON**。
- JSON 格式（`gridSize` + 行优先一维 `pixelData`，长度 = gridSize²）：
  ```json
  {
    "gridSize": 16,
    "pixelData": ["#FFFFFF", "#FBED56", "..."]
  }
  ```
  - 图片输入：透明区域合成白底后再量化；非方形图片等比缩放（contain）、空缺补白。
  - `pixelData` 中 `#FFFFFF` 表示空格（不买豆）；非调色板颜色自动吸附到最近色号。
  - 图片近白背景是否当空格，由 `--blank-white` 控制（白底主体图建议开启）。

## 常用选项

| 选项 | 说明 | 默认 |
|------|------|------|
| `--size <n>` | 网格 N×N（4~150，仅图片输入生效） | 32 |
| `--system <name>` | 色号品牌：MARD / COCO / 漫漫 / 盼盼 / 咪小窝 | MARD |
| `--match <mode>` | 颜色匹配：rgb（欧氏）/ lab（感知色差，通常更准） | rgb |
| `--blank-white` | 图片近白色当作空格 | 关 |
| `--white-threshold <n>` | 近白判定阈值（配 --blank-white） | 240 |
| `--max-colors <n>` | 色数收敛：保留用量前 n 色，低频色并入最接近保留色 | 不限制 |
| `--title <text>` | 图纸标题（默认取文件名） | 文件名 |
| `--cell <px>` | SVG 每格像素 | 24 |
| `--interval <n>` | 加重网格线间隔 | 10 |
| `--no-coordinates` `--no-cellnumbers` `--no-stats` | 关闭对应图层 | 全开 |
| `--csv <path>` | 导出色号用量 CSV（Excel 友好带 BOM） | 无 |
| `--json-out <path>` | 导出 JSON 网格数据 | 无 |
| `--out <path>` `--html <path>` | 指定 SVG / HTML 输出位置 | `<输入名>_pattern.*` |

完整选项：`python pindou-pattern/scripts/pindou.py --help`。

## 三种图的出图口诀

| 图片类型 | 是否 `--blank-white` | 例子 |
|----------|----------------------|------|
| 白底主体图（卡通角色、logo） | **要** | 背景留空，只拼主体，省一半豆 |
| 透明背景图（PNG 贴纸） | **要** | 透明区按白底处理，留空不买豆 |
| 满幅图（风景、照片、星空） | **不要** | 天空云朵都是内容，每格都拼 |

## 工作流程

1. 确认用户想要的：网格尺寸（16/24/32/48/100 常用）、品牌色号系统、是否需要背景留空。
2. 运行 `pindou.py`，命令会向 stdout 打印：输出路径、画布规格、用色数、总豆数、每个色号用量。
3. 向用户报告：图纸路径（SVG + HTML 预览）+ 色号用量清单（直接引用 stdout 统计）+ 总豆数；有 CSV 时一并给出。
4. HTML 预览页自带「打印图纸」按钮，可直接打印或另存为 PDF/PNG。

**不做视觉目检**：生成是确定性的，客观指标以脚本 stdout 统计为准；图纸好坏由用户自行查看。

## 回归测试（skill 改动后跑一次）

```bash
python pindou-pattern/scripts/pindou.py pindou-pattern/assets/sample-heart.json --out heart_test.svg
# 预期: 16x16 | 用色 2 种 | 总豆数 128 颗（验证后删除 heart_test.svg / .html）
```

## 色号数据

- `scripts/palette.json`（205 色 × 5 品牌）+ `scripts/palette.py` 已内联在 skill 中，运行不依赖任何外部文件或网络。
- 渲染链路：网格计算 → SVG / HTML / CSV / JSON（纯文本输出，无需 sharp 等图形库）。
