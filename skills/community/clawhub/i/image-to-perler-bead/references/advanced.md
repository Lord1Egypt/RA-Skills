# 进阶用法

## 1. 编程式调用（作为 Python 模块使用）

`perler_converter.py` 暴露了一组纯函数，可以直接在 Python 中调用：

```python
import sys
sys.path.insert(0, "scripts/")  # 指向 skill 目录下的 scripts/

from perler_converter import (
    load_and_resize,
    quantize,
    count_materials,
    generate_html,
    generate_png,
    PERLER_PALETTE,
)

# 1) 加载并缩放
img, w, h = load_and_resize("photo.jpg", target_w=29, mode="fit")
# img 是 PIL.Image, w/h 是目标珠子数

# 2) 量化
pattern, w, h = quantize(img, dither=True)

# 3) 统计材料
materials = count_materials(pattern)
for idx, cnt in materials:
    code, name_cn, name_en, rgb = PERLER_PALETTE[idx]
    print(f"{code} {name_cn}: {cnt} 颗")

# 4) 生成输出
generate_html(pattern, w, h, materials, "photo.jpg", "out.html",
              cell_px=18, show_codes=True, title="我的拼豆")
generate_png(pattern, w, h, cell_px=20, output_path="out.png")
```

## 2. 批量处理

写一个简单的 shell 循环就能批处理：

```bash
# Linux / macOS / Git Bash
for img in photos/*.jpg; do
  python perler_converter.py "$img" --width 50 --output ./out
done
```

```powershell
# Windows PowerShell
Get-ChildItem photos/*.jpg | ForEach-Object {
  python perler_converter.py $_.FullName --width 50 --output ./out
}
```

## 3. 自定义调色板

复制 `scripts/perler_converter.py` 到你自己的项目目录，编辑 `PERLER_PALETTE` 即可：

```python
# 简化为 24 色版本
PERLER_PALETTE = [
    ("P01", "白", "White", (255,255,255)),
    ("P02", "黑", "Black", (20,20,20)),
    # ... 24 个你最常用的颜色
]
PALETTE_RGB = [item[3] for item in PERLER_PALETTE]
```

或者从 CSV 加载：

```python
import csv
PERLER_PALETTE = []
with open("my_palette.csv", encoding="utf-8") as f:
    reader = csv.reader(f)
    for row in reader:
        code, cn, en, r, g, b = row
        PERLER_PALETTE.append((code, cn, en, (int(r), int(g), int(b))))
PALETTE_RGB = [item[3] for item in PERLER_PALETTE]
```

CSV 示例：
```csv
P01,白,White,255,255,255
P02,黑,Black,20,20,20
P03,红,Red,220,40,40
```

## 4. 解析 JSON 数据

带 `--json` 输出时会得到 `xxx_pattern.json`，结构：

```json
{
  "width": 29,
  "height": 29,
  "total_beads": 841,
  "colors_used": 14,
  "palette": [
    { "code": "P01", "name_cn": "白色", "name_en": "White", "rgb": [255, 255, 255] },
    ...
  ],
  "materials": [
    { "code": "P01", "name_cn": "白色", "rgb": [255, 255, 255], "count": 388 },
    ...
  ],
  "pattern": [
    ["P01", "P01", "P29", ...],
    ["P01", "P24", "P11", ...],
    ...
  ]
}
```

可基于此做二次开发：成本估算、颜色推荐、AR 预览、跨品牌色号映射等。

## 5. 接入其他品牌的色号映射

如果你已确定使用某个品牌（如 Artkal C 系列），可以在 `count_materials` 后加一步映射，把通用编号转成品牌编号：

```python
BRAND_MAP = {
    "P01": "C01",  # 白色
    "P08": "C44",  # 黑色
    "P12": "C06",  # 正红
    "P20": "C13",  # 正黄
    "P25": "C24",  # 正绿
    "P32": "C32",  # 正蓝
    # ... 补完
}

# 改写生成函数, 把材料清单中的 code 换成品牌编号
```

## 6. 性能

- 50×50 量化耗时 < 0.5 秒
- 100×100 量化耗时 < 2 秒
- 生成 HTML 几乎瞬时
- 批量处理百张图 < 5 分钟

瓶颈在加载图片（I/O）和缩放（CPU），不依赖 GPU。Python 单进程即可。

## 7. 自动化建议

如果你有大量照片想批量转拼豆图纸，可以：

1. 跑一遍 `for img in photos/*; do python perler_converter.py "$img"; done`
2. 输出目录里每个图都有 `{name}_pattern.html` 和 `{name}_preview.png`
3. 用 HTML 列表页 + 缩略图做总览

也可以加 `--width 50` `--dither` `--codes` 当成固定模板，每次出图风格统一。
