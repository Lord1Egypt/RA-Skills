# pptx-to-image

将 PowerPoint (PPTX) 演示文稿转换为高质量图片（JPG/PNG），支持自定义 DPI 和保持原始比例。

## 快速开始

```bash
# 安装依赖
pip install pywin32

# 基础使用
py pptx_to_image.py -i presentation.pptx -o ./slides

# 高清输出 (600 DPI)
py pptx_to_image.py -i presentation.pptx -o ./slides --dpi 600

# PNG 格式
py pptx_to_image.py -i presentation.pptx -o ./slides --format png
```

## 参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `-i, --input` | (必填) | 输入 PPTX 文件 |
| `-o, --output` | `./output` | 输出文件夹 |
| `--dpi` | `300` | 输出 DPI (72-600) |
| `--format` | `jpg` | 输出格式 (jpg/png) |
| `--quality` | `95` | JPG 质量 (1-100) |
| `-v, --verbose` | - | 详细输出 |

## 系统要求

- Windows 10/11
- Python 3.10+
- Microsoft PowerPoint 2010+
- pywin32 库

## 许可证

MIT License
