---
name: pdf-vocab-audio
description: 从 PDF 提取词汇生成朗读音频，每个词组读两遍
author:
  name: Maosi English Team
  github: https://github.com/effecE
homepage: https://clawhub.com
license: Apache-2.0
metadata:
  {
    "openclaw":
      {
        "version": "1.1.0",
        "emoji": "📚",
        "tags": ["english", "vocabulary", "audio", "pdf", "education"],
        "requires": { "bins": ["edge-tts", "ffmpeg"], "packages": ["pymupdf"] },
        "install":
          [
            {
              "id": "pip",
              "kind": "pip",
              "package": "edge-tts",
              "label": "Install edge-tts",
            },
            {
              "id": "pip",
              "kind": "pip",
              "package": "pymupdf",
              "label": "Install pymupdf (for PDF parsing)",
            },
          ],
      },
  }
---

# PDF Vocabulary Audio Generator

从 PDF 词汇表提取英文单词，生成朗读音频。

## 作者
**Maosi English Team**

## 使用方法

```bash
# 指定PDF文件
python3 pdf_vocab_audio.py /path/to/vocabulary.pdf

# 使用最新PDF（inbound目录）
python3 pdf_vocab_audio.py
```

## 输入格式

PDF 文件中每行包含：
- 英文单词/词组 + 中文翻译
- 示例：`tiger 老虎`、`computer game 电脑游戏`

## 处理规则

1. **提取英文** - 每行只提取英文部分
2. **保留词组** - 多个单词的词组保持完整
3. **每个读两遍** - 词组读两遍，中间停1秒
4. **语速** - -20%，英式男声 (en-GB-RyanNeural)

## 音频格式
- 语音：en-GB-RyanNeural
- 语速：-20%
- 停顿：1秒

## 输出
- 保存到：`/tmp/`
- 命名：`{原文件名} 词汇朗读音频.mp3`

## 示例

**输入PDF内容：**
```
tiger 老虎
message 消息
computer game 电脑游戏
```

**输出音频：**
- tiger (第1遍) → 停1秒 → tiger (第2遍) → 停1秒
- message (第1遍) → 停1秒 → message (第2遍) → 停1秒
- computer game (第1遍) → 停1秒 → computer game (第2遍)

## 技术实现

1. **PDF解析**：使用 PyMuPDF 提取文本
2. **依赖检查**：使用 `shutil.which()` 验证工具存在
3. **英文过滤**：正则匹配，只保留英文字母和空格
4. **音频生成**：edge-tts 生成单词/词组音频
5. **静音生成**：ffmpeg 生成1秒静音片段
6. **音频合并**：ffmpeg concat 合并所有片段

## 安全设计

- ✅ **依赖验证**：启动时检查 edge-tts 和 ffmpeg 是否可用
- ✅ **输入验证**：PDF文件存在性和格式检查
- ✅ **路径隔离**：所有操作在临时目录完成
- ✅ **临时目录**：使用系统临时目录，自动清理
- ✅ **subprocess安全**：使用 `shutil.which()` 验证工具路径，参数列表传递
- ✅ **超时保护**：30秒超时防止进程挂起
- ✅ **资源清理**：临时文件自动清理

## License
Apache License 2.0
