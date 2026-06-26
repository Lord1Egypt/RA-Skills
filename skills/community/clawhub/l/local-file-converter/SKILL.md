---
name: local-file-converter
description: 本地文件转换技能，使用命令行工具实现 1000+ 格式互转。
---

# Local File Converter

本地文件转换技能，使用命令行工具实现 1000+ 格式互转。

## 能力

- **图片**: JPG, PNG, WebP, HEIC, GIF, BMP, TIFF, SVG 等
- **视频**: MP4, AVI, MKV, MOV, WebM, GIF 等
- **音频**: MP3, FLAC, WAV, AAC, OGG, M4A 等
- **文档**: PDF, DOCX, DOC, EPUB, MOBI, TXT, Markdown 等
- **数据**: JSON, YAML, XML, CSV 等

## 底层工具

| 工具 | 用途 |
|------|------|
| `ffmpeg` | 音视频转换 |
| `imagemagick` | 图片转换 |
| `libreoffice` | 文档转换 |
| `pandoc` | 文档/标记转换 |
| `calibre` | 电子书转换（按需安装） |

### 安装命令

```bash
# Debian/Ubuntu
sudo apt install ffmpeg imagemagick libreoffice pandoc calibre

# macOS
brew install ffmpeg imagemagick libreoffice pandoc
brew install --cask calibre
```

## 使用方式

用户说类似：
- "把这个图片转成 WebP"
- "将 video.mp4 转换成 GIF"
- "把 document.docx 转为 PDF"
- "转换这本书为 EPUB 格式"

技能自动：
1. 识别源文件和目标格式
2. 选择合适的转换工具
3. 执行转换命令
4. 返回结果文件路径

## 命令参考

### 图片转换 (ImageMagick)
```bash
convert input.png output.webp
convert image.jpg image.png
mogrify -format webp *.png
convert input.jpg -resize 1920x1080 output.jpg
```

### 视频/音频转换 (FFmpeg)
```bash
ffmpeg -i input.mp4 -vf "fps=10,scale=640:-1" output.gif
ffmpeg -i input.mp4 -c:v libx265 output.mkv
ffmpeg -i video.mp4 -q:a 0 -map a output.mp3
ffmpeg -i input.wav -b:a 320k output.mp3
```

### 文档转换 (LibreOffice)
```bash
libreoffice --headless --convert-to pdf document.docx
libreoffice --headless --convert-to docx document.pdf
```

### 文档/标记转换 (Pandoc)
```bash
pandoc input.md -o output.pdf
pandoc input.md -o output.docx
pandoc input.html -t markdown -o output.md
```

### 电子书转换 (Calibre)
```bash
ebook-convert input.epub output.mobi
ebook-convert input.epub output.pdf
```

## 注意事项

- ⚠️ **大文件转换**可能需要较长时间
- ⚠️ **视频转换**消耗 CPU，建议在空闲时进行
- ⚠️ **有损转换**可能降低质量
- ⚠️ **HEIC 格式**需要 `libheif` 支持

## 状态检查

```bash
ffmpeg -version | head -1
convert --version | head -1
libreoffice --version | head -1
pandoc --version | head -1
```
