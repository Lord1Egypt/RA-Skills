# PDF 转换器 - 使用示例

## 快速开始

### 1. 安装依赖

```bash
# 安装 Python 库
pip3 install --break-system-packages pdf2image python-pptx pdf2docx Pillow

# 安装 poppler（PDF 渲染引擎）
brew install poppler  # macOS
# 或
sudo apt-get install poppler-utils  # Ubuntu/Debian
```

### 2. 基本使用

```bash
# 转换为 PPTX（默认）
python3 skills/pdf-converter/scripts/convert.py "/path/to/file.pdf"

# 转换为 Word
python3 skills/pdf-converter/scripts/convert.py "/path/to/file.pdf" --format docx

# 指定最大文件大小
python3 skills/pdf-converter/scripts/convert.py "/path/to/file.pdf" --max-size 20

# 调整质量以减小文件大小
python3 skills/pdf-converter/scripts/convert.py "/path/to/file.pdf" --dpi 100 --quality 70
```

## 实际案例

### 案例 1: 中金公司公关方案转换

```bash
# 转换 PDF 为 PPTX，限制 30MB
python3 skills/pdf-converter/scripts/convert.py \
  "/Users/admin/Desktop/中金公司 2026 年度公关服务响应方案 -0318.pdf" \
  --format pptx \
  --max-size 30
```

**结果**:
- ✅ 转换成功
- 📊 输出大小：22.51 MB
- 📄 页数：118 页
- 📍 保存位置：同目录下的.pptx 文件

### 案例 2: 批量转换多个 PDF

```bash
# 转换目录下所有 PDF 为 PPTX
python3 skills/pdf-converter/scripts/convert.py \
  "/Users/admin/Downloads/" \
  --batch \
  --format pptx \
  --max-size 30
```

### 案例 3: 高质量转换（用于打印）

```bash
# 高 DPI 高质量转换
python3 skills/pdf-converter/scripts/convert.py \
  "report.pdf" \
  --dpi 300 \
  --quality 95 \
  --max-size 100
```

### 案例 4: 小文件转换（用于邮件发送）

```bash
# 低质量小文件转换
python3 skills/pdf-converter/scripts/convert.py \
  "document.pdf" \
  --dpi 100 \
  --quality 60 \
  --max-size 10
```

## 在 Python 代码中使用

```python
from skills.pdf-converter.scripts.convert import PDFConverter

# 创建转换器
converter = PDFConverter(dpi=150, quality=85, max_size_mb=30)

# 转换为 PPTX
success = converter.convert("input.pdf", "pptx", "output.pptx")

# 转换为 Word
success = converter.convert("input.pdf", "docx", "output.docx")

# 批量转换
success = converter.batch_convert("/path/to/pdfs/", "pptx")
```

## 性能优化建议

### 文件大小过大

如果转换后的文件超过大小限制，可以尝试：

1. **降低 DPI**（默认 150）:
   ```bash
   --dpi 100  # 适合屏幕查看
   --dpi 72   # 最小，文件最小
   ```

2. **降低图片质量**（默认 85）:
   ```bash
   --quality 70  # 良好质量
   --quality 50  # 可接受质量
   ```

3. **组合使用**:
   ```bash
   --dpi 100 --quality 60 --max-size 20
   ```

### 转换速度慢

1. 减少 DPI（渲染更快）
2. 减少页数（只转换需要的页面）
3. 使用 SSD 存储

### 内存不足

1. 降低 DPI
2. 分批转换大文件
3. 关闭其他应用程序

## 常见问题

### Q: 为什么 PPTX 文件比 PDF 还大？

A: PPTX 将每页 PDF 渲染为高清图片，如果 PDF 本身是矢量图或文字，转换后会变大。解决方法：
- 降低 `--dpi` 参数
- 降低 `--quality` 参数
- 使用 `--max-size` 自动压缩

### Q: 转换后文字无法编辑？

A: PPTX 格式是图片形式，文字不可编辑。如需可编辑文字：
- 使用 `--format docx` 转换为 Word
- Word 格式会尝试保留文字结构

### Q: 中文文件名无法识别？

A: 使用引号包裹文件路径：
```bash
python3 convert.py "文件名称.pdf"
```

或使用完整路径：
```bash
python3 convert.py /完整/路径/文件名称.pdf
```

## 输出对比

| 格式 | 优点 | 缺点 | 适用场景 |
|------|------|------|---------|
| **PPTX** | 保持原貌、适合演示 | 文字不可编辑、文件较大 | 演示文稿、展示报告 |
| **DOCX** | 文字可编辑、文件较小 | 排版可能变化 | 文档编辑、内容提取 |

## 技术支持

如有问题，请查看：
- SKILL.md - 完整技能文档
- 日志输出 - 详细错误信息
