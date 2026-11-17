# SVG Editing Tools / SVG 编辑工具

| 工具 | 适用场景 | 获取方式 |
|------|----------|----------|
| **PowerPoint / Word 2016+** | 直接拖入编辑（右键→取消组合，可修改文字/颜色/形状） | 已有 Office 即可 |
| **Inkscape** | 开源矢量编辑，调整布局、导出 PDF/EPS/高DPI TIFF | [inkscape.org](https://inkscape.org/)（免费） |
| **Adobe Illustrator** | 出版级精细调整（字体、配色、图层） | Adobe 订阅 |
| **Affinity Designer** | 一次性购买，功能接近 AI | Microsoft Store |

## 投稿格式转换 / Submission Format Conversion

（Inkscape 命令行）：

```bash
# SVG → EPS（多数医学期刊要求）
inkscape input.svg --export-type=eps --export-filename=input.eps

# SVG → PDF（JAMA/The Lancet 等）
inkscape input.svg --export-type=pdf --export-filename=input.pdf

# SVG → TIFF 600dpi（NEJM/British Medical Journal 等）
inkscape input.svg --export-type=png --export-dpi=600 --export-filename=input.tiff
```
