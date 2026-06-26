# pdf-converter

PDF 转 PPTX/Word 转换器 - 将 PDF 文件转换为 PowerPoint 或 Word 格式，支持文件大小限制。

## 功能

- ✅ PDF → PPTX（每页 PDF 转为幻灯片，图片嵌入）
- ✅ PDF → DOCX（保留文本和图片结构）
- ✅ 文件大小控制（自动压缩以确保 ≤ 指定大小）
- ✅ 批量转换支持
- ✅ 可配置图片质量和 DPI

## 安装依赖

```bash
pip3 install --break-system-packages pdf2image python-pptx pdf2docx Pillow
```

**注意**: `pdf2image` 需要系统安装 `poppler`：
```bash
# macOS
brew install poppler

# Ubuntu/Debian
sudo apt-get install poppler-utils
```

## 使用方法

### 基本用法

```bash
# 转换为 PPTX（默认）
python3 skills/pdf-converter/scripts/convert.py /path/to/file.pdf

# 转换为 Word
python3 skills/pdf-converter/scripts/convert.py /path/to/file.pdf --format docx

# 指定最大文件大小（MB）
python3 skills/pdf-converter/scripts/convert.py /path/to/file.pdf --max-size 30

# 指定输出路径
python3 skills/pdf-converter/scripts/convert.py /path/to/file.pdf --output /path/to/output.pptx
```

### 高级选项

```bash
# 调整 DPI（影响质量和大小，默认 150）
python3 skills/pdf-converter/scripts/convert.py file.pdf --dpi 200

# 调整图片质量（1-100，默认 85）
python3 skills/pdf-converter/scripts/convert.py file.pdf --quality 75

# 批量转换整个目录
python3 skills/pdf-converter/scripts/convert.py /path/to/pdfs/ --batch

# 静默模式（仅输出最终结果）
python3 skills/pdf-converter/scripts/convert.py file.pdf --quiet
```

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `input` | PDF 文件路径或目录（批量模式） | 必需 |
| `--format` | 输出格式：`pptx` 或 `docx` | `pptx` |
| `--max-size` | 最大文件大小（MB），超过会尝试压缩 | `30` |
| `--output` | 输出文件路径 | 与 PDF 同目录 |
| `--dpi` | 渲染 DPI（影响质量和大小） | `150` |
| `--quality` | JPEG 图片质量（1-100） | `85` |
| `--batch` | 批量转换目录中的所有 PDF | `False` |
| `--quiet` | 静默模式，仅输出结果 | `False` |

## 示例

### 示例 1: 转换单个 PDF 为 PPTX

```bash
python3 skills/pdf-converter/scripts/convert.py "/Users/admin/Desktop/中金公司 2026 年度公关服务响应方案 -0318.pdf"
```

输出：
```
📄 源文件：中金公司 2026 年度公关服务响应方案 -0318.pdf
📊 源大小：21.91 MB
🔄 开始转换...
✓ 共 118 页
📊 创建幻灯片...
  已处理 20/118 页
  已处理 40/118 页
  ...
✅ 转换成功！
📊 输出大小：22.51 MB
✓ 大小限制：≤30 MB - ✅ 符合
📍 保存位置：/Users/admin/Desktop/中金公司 2026 年度公关服务响应方案 -0318.pptx
```

### 示例 2: 转换为 Word 并限制大小

```bash
python3 skills/pdf-converter/scripts/convert.py file.pdf --format docx --max-size 20
```

### 示例 3: 批量转换

```bash
python3 skills/pdf-converter/scripts/convert.py /path/to/pdfs/ --batch --format pptx
```

## 输出格式说明

### PPTX 格式
- 每页 PDF 转为一张幻灯片
- 幻灯片尺寸：16:9 宽屏（13.333" x 7.5"）
- 图片格式：JPEG（可配置质量）
- 适合：演示文稿、报告展示

### DOCX 格式
- 保留 PDF 文本和图片结构
- 可编辑文本内容
- 适合：文档编辑、内容提取

## 性能参考

| PDF 大小 | 页数 | DPI | 转换时间 | PPTX 大小 |
|---------|------|-----|---------|----------|
| 5 MB | 20 | 150 | ~15 秒 | ~8 MB |
| 20 MB | 100 | 150 | ~60 秒 | ~20 MB |
| 50 MB | 200 | 150 | ~120 秒 | ~45 MB |

## 故障排除

### 问题 1: `pdf2image` 报错 "unable to get page count"

**原因**: 缺少 poppler 工具

**解决**:
```bash
# macOS
brew install poppler

# Ubuntu/Debian
sudo apt-get install poppler-utils
```

### 问题 2: 转换后文件太大

**解决**:
1. 降低 DPI：`--dpi 100`
2. 降低图片质量：`--quality 60`
3. 启用自动压缩：`--max-size 30`

### 问题 3: 中文文件名乱码

**解决**: 使用完整路径，确保文件系统支持 UTF-8

## 文件结构

```
skills/pdf-converter/
├── SKILL.md              # 本文件
├── scripts/
│   └── convert.py        # 转换脚本
└── README.md             # 详细文档（可选）
```

## 更新日志

- **2026-03-18**: 初始版本，支持 PDF→PPTX 和 PDF→DOCX
