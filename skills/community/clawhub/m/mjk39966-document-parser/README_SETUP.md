# Document Parser 技能 - 安装与使用指南

## ✅ 技能已创建完成

技能位置：`~/.openclaw/workspace/document_parser/`

## 📋 功能特性

- ✅ 支持 `.docx`、`.pdf`、`.txt` 格式
- ✅ 自动提取纯文本内容
- ✅ 提取文档中的表格（保持结构）
- ✅ JSON 和纯文本两种输出格式
- ✅ 页面/段落/表格数量的元数据

## 🔧 安装步骤

### 前置要求

需要安装 Python 3.7+

**检查 Python 是否已安装：**
```bash
python --version
# 或
python3 --version
```

如果没有安装，请访问：https://www.python.org/downloads/

### 安装依赖包

运行以下命令之一：

**Windows:**
```cmd
cd %USERPROFILE%\.openclaw\workspace\document_parser
scripts\install_dependencies.bat
```

**Linux/macOS:**
```bash
cd ~/.openclaw/workspace/document_parser
bash scripts/install_dependencies.sh
```

**手动安装（如果脚本失败）：**
```bash
pip install python-docx PyPDF2 pdfplumber
```

## 🚀 使用方法

### 基本用法

```bash
# JSON 格式输出（默认）
python scripts/parse_document.py /path/to/document.pdf

# 人类可读格式
python scripts/parse_document.py /path/to/document.docx --format text
```

### 示例场景

#### 1. 提取 PDF 合同条款
```
用户："帮我提取这份 contract.pdf 里的关键条款"
操作：
1. python scripts/parse_document.py contract.pdf
2. 分析提取的文本
3. 总结关键条款
```

#### 2. 分析 Word 文档中的表格
```
用户："这个 report.docx 里第二季度的销售额是多少？"
操作：
1. python scripts/parse_document.py report.docx
2. 从 tables 数组中找到相关表格
3. 计算并回答
```

#### 3. 批量处理多个文档
```
用户："在这3个 PDF 里找所有提到'交付日期'的地方"
操作：
for file in [file1.pdf, file2.pdf, file3.pdf]:
    1. 解析文档
    2. 搜索关键词
    3. 汇总结果
```

## 📤 输出格式

### JSON 输出示例

```json
{
  "text": "这是文档的完整文本内容...",
  "tables": [
    [
      ["产品名称", "单价", "数量"],
      ["商品A", "100", "50"],
      ["商品B", "200", "30"]
    ]
  ],
  "metadata": {
    "format": "pdf",
    "pages": 5,
    "tables": 2
  }
}
```

### 文本输出示例

```
==========================================================
EXTRACTED TEXT:
==========================================================
这是文档的完整文本内容...

==========================================================
TABLES FOUND: 2
==========================================================

Table 1:
产品名称 | 单价 | 数量
商品A | 100 | 50
商品B | 200 | 30
```

## ⚙️ 将技能添加到 OpenClaw

### 方法 1: 直接使用（本地）

技能已在你的 workspace 中，OpenClaw 会自动发现并加载它。

### 方法 2: 打包分发

如果要分享给其他人或上传到 ClawHub：

```bash
# 需要运行打包脚本（如果有 Python）
python ~/AppData/Roaming/npm/node_modules/openclaw/skills/skill-creator/scripts/package_skill.py ~/.openclaw/workspace/document_parser
```

这会生成 `document_parser.skill` 文件，可以通过 ClawHub 分发。

## 🔍 故障排除

### 错误："Python was not found"
- 安装 Python 3.7+：https://www.python.org/downloads/
- Windows 用户记得勾选 "Add Python to PATH"

### 错误："python-docx not installed"
- 运行安装脚本：`scripts\install_dependencies.bat` (Windows) 或 `bash scripts/install_dependencies.sh` (Linux/macOS)

### PDF 表格提取不完整
- PDF 必须是文本型（非扫描件）
- 复杂表格可能需要手动调整
- 尝试将 PDF 另存为更简单的格式

### 大文件处理慢
- 正常现象，>50 页 PDF 需要较长时间
- 可以考虑先转换为文本格式

## 📚 技术细节

**依赖库说明：**
- `python-docx`: 解析 .docx 文件（段落和表格）
- `PyPDF2`: 提取 PDF 文本内容（按页）
- `pdfplumber`: 增强的 PDF 表格检测和提取

**支持的文件特性：**
- .docx: 段落、表格、基本格式
- .pdf: 多页文本、表格（需清晰边框）
- .txt: 纯文本

**不支持：**
- 扫描 PDF 的 OCR（需要可选文本）
- 图片中的文字识别
- 复杂的文档布局保持

## 📝 下一步

现在你可以：
1. 安装 Python 和依赖包
2. 上传文档并让 OpenClaw 帮你分析
3. 询问文档中的任何问题

例如：
- "帮我总结这份 report.pdf"
- "这个合同里的付款条款是什么？"
- "从这个 Excel 导出的 .docx 里提取所有数据"
