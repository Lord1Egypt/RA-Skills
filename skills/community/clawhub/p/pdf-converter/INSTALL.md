# PDF 转换器 - 安装指南

## 🚀 快速安装

### 步骤 1: 安装系统依赖

**macOS:**
```bash
brew install poppler
```

**Ubuntu/Debian:**
```bash
sudo apt-get install poppler-utils
```

**Windows:**
1. 下载 poppler: https://github.com/oschwartz10612/poppler-windows/releases
2. 解压到 `C:\Program Files\poppler`
3. 添加 `C:\Program Files\poppler\Library\bin` 到系统 PATH

### 步骤 2: 安装 Python 库

```bash
pip3 install --break-system-packages pdf2image python-pptx pdf2docx Pillow
```

### 步骤 3: 验证安装

```bash
python3 skills/pdf-converter/scripts/check_deps.py
```

看到所有 ✅ 即表示安装成功。

---

## 📋 完整依赖列表

| 依赖 | 用途 | 必需 |
|------|------|------|
| **poppler** | PDF 渲染引擎 | ✅ 必需 |
| **pdf2image** | Python PDF 渲染库 | ✅ 必需 |
| **python-pptx** | PowerPoint 生成 | ✅ 必需 (PPTX) |
| **pdf2docx** | Word 生成 | ✅ 必需 (DOCX) |
| **Pillow** | 图片处理 | ✅ 必需 |

---

## 🔧 故障排除

### 问题 1: `pdf2image` 报错 "unable to get page count"

**原因**: poppler 未安装或不在 PATH 中

**解决**:
```bash
# 检查是否安装
which pdfinfo

# macOS 重新安装
brew reinstall poppler

# Ubuntu 重新安装
sudo apt-get install --reinstall poppler-utils
```

### 问题 2: `pip install` 权限错误

**解决**:
```bash
# 使用 --break-system-packages 标志
pip3 install --break-system-packages pdf2image python-pptx pdf2docx Pillow

# 或使用虚拟环境
python3 -m venv venv
source venv/bin/activate
pip install pdf2image python-pptx pdf2docx Pillow
```

### 问题 3: 导入错误 `No module named 'pptx'`

**解决**:
```bash
# 确认安装
pip3 list | grep pptx

# 重新安装
pip3 install --break-system-packages --force-reinstall python-pptx
```

### 问题 4: 中文支持问题

**解决**:
```bash
# macOS 确保系统字体完整
# 无需额外操作

# Ubuntu/Debian 安装中文字体
sudo apt-get install fonts-wqy-zenhei fonts-wqy-microhei
```

---

## ✅ 验证安装

运行检查脚本：

```bash
python3 skills/pdf-converter/scripts/check_deps.py
```

预期输出：
```
🔍 检查 PDF 转换器依赖...

✅ pdf2image            - PDF 渲染
✅ python-pptx          - PowerPoint 生成
✅ pdf2docx             - Word 生成
✅ Pillow               - 图片处理
✅ poppler-utils       - PDF 渲染引擎

✅ 所有依赖已安装，可以开始使用！
```

---

## 📖 使用指南

安装完成后，查看：

- **SKILL.md** - 完整功能说明
- **EXAMPLES.md** - 使用示例
- **帮助信息**: `python3 scripts/convert.py --help`

---

## 🎯 快速测试

```bash
# 转换测试文件
python3 skills/pdf-converter/scripts/convert.py \
  "/path/to/test.pdf" \
  --format pptx \
  --max-size 30
```

---

## 📞 需要帮助？

1. 查看 `SKILL.md` 了解完整功能
2. 查看 `EXAMPLES.md` 了解使用示例
3. 运行 `check_deps.py` 检查依赖状态
