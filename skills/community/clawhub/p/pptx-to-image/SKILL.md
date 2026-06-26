# pptx-to-image Skill

将 PowerPoint (PPTX) 演示文稿转换为高质量图片（JPG/PNG），支持自定义 DPI 和保持原始比例。

---

## 功能

- **高 DPI 输出**：支持 72-600 DPI 自定义，默认 300 DPI
- **保持比例**：自动检测原 PPT 页面尺寸，保持原始宽高比
- **方向自适应**：横版/竖版自动识别
- **多格式支持**：JPG、PNG 可选
- **批量转换**：支持多页幻灯片批量导出
- **质量检查**：输出前自动验证 DPI 和尺寸

---

## 使用方式

### 作为 Python 脚本调用

```bash
py pptx_to_image.py --input presentation.pptx --output ./slides --dpi 300 --format jpg
```

### 参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--input` / `-i` | (必填) | 输入的 PPTX 文件路径 |
| `--output` / `-o` | `./output` | 输出文件夹路径 |
| `--dpi` | `300` | 输出图片 DPI (72-600) |
| `--format` | `jpg` | 输出格式：`jpg` 或 `png` |
| `--quality` | `95` | JPG 质量 (1-100) |
| `--verbose` / `-v` | `False` | 显示详细信息 |

---

## 示例

### 基础转换（300 DPI）
```bash
py pptx_to_image.py -i my_presentation.pptx -o ./slides
```

### 高清转换（600 DPI，PNG 格式）
```bash
py pptx_to_image.py -i my_presentation.pptx -o ./slides --dpi 600 --format png
```

### 快速预览（150 DPI）
```bash
py pptx_to_image.py -i my_presentation.pptx -o ./preview --dpi 150
```

---

## 依赖

- Python 3.10+
- Windows 系统（需要 PowerPoint COM 接口）
- `pywin32` 库

安装依赖：
```bash
pip install pywin32
```

---

## 输出示例

```
============================================================
PPTX → JPG | 保持原始比例 | 300 DPI
============================================================
原始尺寸：1700.75 x 2267.75 点
原始比例：0.7500
方向：竖版 (Portrait)

目标 DPI: 300
目标尺寸：7086 x 9448 像素
实际 DPI X: 300.0
实际 DPI Y: 300.0

幻灯片数量：5

[OK] 已导出第 1 页
  路径：./slides/slide_001.jpg
  尺寸：7086 x 9448 像素
  大小：6117.7 KB

...

============================================================
[DONE] 完成！共导出 5 张图片
  slide_001.jpg: 5.97 MB
  slide_002.jpg: 4.23 MB
  slide_003.jpg: 5.81 MB
  slide_004.jpg: 3.92 MB
  slide_005.jpg: 6.15 MB
```

---

## 技术细节

### DPI 计算
```python
# 1 点 = 1/72 英寸
# 像素 = 点 × (DPI / 72)
scale_factor = dpi / 72.0
target_width = int(orig_width * scale_factor)
target_height = int(orig_height * scale_factor)
```

### 导出方法
使用 PowerPoint COM 接口的 `Slide.Export()` 方法，直接指定像素尺寸，确保精确的 DPI 输出。

---

## 注意事项

1. **Windows 专用**：依赖 PowerPoint COM 接口，仅支持 Windows
2. **需要安装 PowerPoint**：必须有 Microsoft PowerPoint 2010+
3. **窗口可见**：转换时 PowerPoint 窗口会短暂显示（COM 限制）
4. **大文件处理**：高 DPI 转换可能产生大文件（单页 5-10 MB）

---

## 常见问题

**Q: 为什么输出 DPI 不是 300？**
A: 确保使用 `--dpi 300` 参数，脚本会自动计算正确的像素尺寸。

**Q: 可以批量转换多个 PPTX 吗？**
A: 当前版本单文件处理，可配合批处理脚本使用。

**Q: 支持 Mac 吗？**
A: 不支持，Mac 需要不同的实现方式（AppleScript）。

---

## 版本历史

- **v1.0.0** (2026-03-20) - 初始版本
  - 基础 PPTX → JPG/PNG 转换
  - 自定义 DPI 支持
  - 自动比例保持
  - 详细输出报告

---

## License

MIT License
