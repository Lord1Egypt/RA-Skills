---
name: minimax-pdf-ocr
version: 1.0.0
description: 使用 MiniMax Vision API 识别 PDF/图片中的文字
emoji: 🔍
tags:
  - pdf
  - ocr
  - minimax
  - recognition
---

# MiniMax OCR Skill

使用 MiniMax Vision API 识别 PDF/图片中的文字内容，支持中文和英文。

## 功能

- PDF 转图片（使用 poppler）
- MiniMax Vision API 文字识别
- 输出 Markdown 格式

## 依赖

```bash
# 安装 Node.js 依赖
cd minimax-pdf-ocr
npm install openai pdf2image

# 安装系统依赖
brew install poppler
```

## 使用方法

### 命令行

```bash
# 设置 API Key
export MINIMAX_API_KEY="your-api-key"

# 运行 OCR
node pdf-ocr-minimax.js <pdf文件路径> [输出目录]

# 示例
node pdf-ocr-minimax.js ./document.pdf ./output/
```

### 作为 Skill 使用

在 JavaScript 代码中调用：

```javascript
const { recognizePdf } = require('./pdf-ocr-minimax.js');

await recognizePdf('/path/to/document.pdf', './output/');
```

## 环境变量

| 变量 | 说明 | 必填 |
|------|------|------|
| MINIMAX_API_KEY | MiniMax API Key (从 platform.minimaxi.com 获取) | 是 |
| OUTPUT_DIR | 输出目录 | 否（默认当前目录） |

## 输出

- 识别结果保存为 `.md` 文件
- 包含所有页面的文字内容
- 保持原有格式和段落结构

## 示例输出

```markdown
# 文档名称

## 第 1 页

这里是第一页的文字内容...

## 第 2 页

这里是第二页的文字内容...
```

## 注意事项

- MiniMax M2.5 模型支持视觉理解
- 每页识别约消耗 100-500 次 token
- 建议批量处理时添加适当延迟避免限流
- API Key 获取: https://platform.minimaxi.com/user-center/basic-information/interface-key
