# PDF 转 Word 技能

[English](SKILL.md)

这是一个使用**免费**的本地 OCR 引擎 `docr` 将扫描版 PDF 文档提取并转换为可编辑的 Word (`.docx`) 文件的技能。

## 准备工作

1. 下载并初始化 OCR 引擎二进制文件：
   ```bash
   bash scripts/install.sh
   ```
2. 安装所需的 Python 依赖项：
   ```bash
   pip install -r scripts/requirements.txt
   ```

## 使用方法

运行 Python 脚本，传入输入的 PDF 文件路径和期望输出的 `.docx` 文件路径。您还可以在最后附加 `docr` 支持的其他参数（如引擎选择）。

```bash
python scripts/pdf2word.py <输入.pdf> <输出.docx> [docr参数...]
```

### 示例

使用默认的本地引擎转换单个文件：
```bash
python scripts/pdf2word.py sample.pdf sample_output.docx
```

### 使用其他 API 引擎

默认情况下，脚本使用本地的 `RapidOCR` 引擎。底层的 `docr` 工具也支持使用其他引擎（如 Google Gemini API），这可以在处理复杂排版时提供更高的识别准确率。

要使用 Gemini，请先配置您的 API 密钥：
```bash
mkdir -p ~/.ocr
echo "gemini_api_key=your_gemini_key" > ~/.ocr/config
```

然后在运行脚本时传入 `-engine gemini` 参数：
```bash
python scripts/pdf2word.py sample.pdf sample_output.docx -engine gemini
```

如果您的文档中包含**表格**，您可以利用 prompt 功能强制 Gemini 输出 Markdown 格式的表格，脚本会自动将它们转换回原生的 Word 表格：
```bash
python scripts/pdf2word.py sample.pdf sample_output.docx -engine gemini -prompt "请提取所有文本，务必使用 | 符号将表格保持为 Markdown 格式输出。"
```

### 工作原理
1. 脚本调用 `docr`，使用指定的 OCR 模型（默认为 RapidOCR）从扫描的 PDF 中读取文本。
2. 提取的文本被临时存储。
3. 使用 `python-docx` 库读取临时文本内容，并构建为格式化的 Word 文档。
4. 自动清理临时文件。
