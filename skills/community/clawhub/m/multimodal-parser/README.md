# 📄 多模态内容解析器
## 核心亮点
1. 🔄 **统一接口**：一套API支持图片/PDF/Word/音频4大类格式解析，不需要对接多个服务
2. 🚀 **开箱即用**：内置OCR、音频转文字、文档解析能力，零配置即可使用
3. 📝 **多格式输出**：支持纯文本/Markdown/结构化JSON三种输出格式，适配不同LLM处理需求
4. 💡 **友好错误提示**：依赖缺失时自动给出安装命令，新手也能快速上手

## 🎯 适用场景
- 多模态Agent的内容解析层
- 文档问答、知识库构建场景的文件预处理
- 图片OCR识别、语音转文字需求
- 批量文档解析与结构化处理

## 📝 参数说明
| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| file_path | string | 是 | - | 要解析的文件路径 |
| file_type | string | 否 | auto | 文件类型：image/pdf/docx/audio/auto |
| output_format | string | 否 | text | 输出格式：text/markdown/structured |
| options.ocr_lang | string | 否 | chi_sim+eng | OCR识别语言 |
| options.audio_model | string | 否 | base | Whisper模型大小（base/small/medium/large） |
| options.pdf_page_range | tuple | 否 | undefined | PDF解析页码范围，如[1, 10]表示解析第1-10页 |

## 💡 开箱即用示例
### 图片OCR识别
```typescript
const result = await skills.multimodalParser({
  file_path: "./resume.jpg",
  file_type: "image",
  output_format: "markdown"
});
```

### PDF解析（指定页码范围）
```typescript
const result = await skills.multimodalParser({
  file_path: "./document.pdf",
  output_format: "structured",
  options: {
    pdf_page_range: [1, 50] // 只解析前50页
  }
});
```

### 音频转文字
```typescript
const result = await skills.multimodalParser({
  file_path: "./meeting.mp3",
  options: { 
    audio_model: "small" // 用small模型，速度更快
  }
});
```

## 🔧 依赖安装
根据需要解析的文件类型安装对应依赖：
```bash
# 全量安装所有依赖（推荐）
## macOS
brew install tesseract tesseract-lang poppler pandoc
pip install openai-whisper ffmpeg

## Ubuntu/Debian
apt install tesseract-ocr tesseract-ocr-chi-sim poppler-utils pandoc ffmpeg
pip install openai-whisper
```

## 技术实现说明
- 基于成熟的开源工具链（Tesseract/Poppler/Whisper/Pandoc）
- 自动文件类型检测，无需手动指定格式
- 模块化设计，可轻松扩展支持更多格式
- 输出格式标准化，直接可被LLM处理
