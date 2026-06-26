# 📦 large-file-handler

> **大文件异步处理器 | Async Large File Processor** - 解决大文件导致 Gateway 卡死的问题 | Solve the problem of Gateway crashes caused by large files

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)]()
[![Author](https://img.shields.io/badge/author-Leo 🦁-green.svg)]()

---

## 🎯 功能特性 | Features

- ✅ **流式保存** - 边接收边写磁盘，不占用大量内存
- ✅ **Stream Save** - Write to disk while receiving, no large memory usage

- ✅ **异步处理** - 后台独立进程处理，不阻塞 Gateway
- ✅ **Async Processing** - Background independent process, no Gateway blocking

- ✅ **大小阈值** - >10MB 自动切换异步模式
- ✅ **Size Threshold** - Auto switch to async mode for files >10MB

- ✅ **结果推送** - 处理完成后主动推送结果给用户
- ✅ **Result Push** - Actively push results to users after processing

- ✅ **多类型支持** - PDF、视频、图片、日志、Office 文档等
- ✅ **Multi-type Support** - PDF, video, images, logs, Office documents, etc.

- ✅ **自动清理** - 已完成文件 24 小时后自动清理
- ✅ **Auto Cleanup** - Completed files automatically cleaned up after 24 hours

---

## 📊 文件大小处理策略 | File Size Processing Strategy

| 文件大小 | 处理模式 | 响应时间 | 用户体验 |
|---------|---------|---------|---------|
| <10MB | 同步 | 秒级 | 即时回复 |
| 10-100MB | 异步 | 分钟级 | 先确认，后推送结果 |
| 100-500MB | 异步 + 分块 | 分钟级 | 先确认，后推送结果 |
| >500MB | 拒绝 | 即时 | 提示文件过大 |

| File Size | Processing Mode | Response Time | User Experience |
|-----------|-----------------|---------------|-----------------|
| <10MB | Sync | Seconds | Instant reply |
| 10-100MB | Async | Minutes | Confirm first, push result later |
| 100-500MB | Async + Chunked | Minutes | Confirm first, push result later |
| >500MB | Reject | Instant | File too large error |

---

## 🚀 快速开始 | Quick Start

### 方法 1：命令行调用 | Method 1: Command Line

```bash
python "E:\ai\openclaw\.openclaw\workspace\skills\large-file-handler\scripts\handle_file.py" "文件路径 | file_path" --user-id "用户 ID | user_id" --channel "渠道 | channel"
```

### 方法 2：在 Gateway 中集成 | Method 2: Integrate in Gateway

```python
import subprocess
import sys

def handle_incoming_file(file_path: str, user_id: str, channel: str):
    """处理接收到的文件 | Handle incoming file"""
    
    skill_script = r"E:\ai\openclaw\.openclaw\workspace\skills\large-file-handler\scripts\handle_file.py"
    
    # 启动处理进程（异步）| Start processing process (async)
    subprocess.Popen([
        sys.executable,
        skill_script,
        file_path,
        '--user-id', user_id,
        '--channel', channel
    ])
    
    # 立即返回确认消息 | Return confirmation message immediately
    return "收到文件，正在处理... | File received, processing..."
```

---

## 📁 目录结构 | Directory Structure

```
large-file-handler/
├── SKILL.md              # 技能说明 | Skill description
├── _meta.json            # 元数据 | Metadata
├── README.md             # 完整文档 | Full documentation (this file)
├── README.zh-CN.md       # 中文文档 | Chinese documentation
├── INTEGRATION.md        # 集成指南 | Integration guide
├── PUBLISH.md            # 发布指南 | Publishing guide
├── handler.py            # 核心处理模块 | Core processing module
├── generic_processor.py  # 通用处理器 | Generic processor
├── pdf-processor.py      # PDF 处理器 | PDF processor
├── scripts/
│   └── handle_file.py    # 命令行脚本 | Command line script
└── processors/           # 专用处理器目录 | Specialized processors directory
```

---

## ⚙️ 配置选项 | Configuration Options

编辑 `scripts/handle_file.py` 修改配置 | Edit `scripts/handle_file.py` to modify configuration:

```python
LARGE_FILE_THRESHOLD = 10 * 1024 * 1024  # 10MB - 异步阈值 | Async threshold
MAX_FILE_SIZE = 500 * 1024 * 1024        # 500MB - 最大支持 | Maximum supported
```

---

## 📊 支持的文件类型 | Supported File Types

| 类型 | 扩展名 | 处理器 |
|------|--------|--------|
| **PDF** | `.pdf` | pdf-processor |
| **视频 | Video** | `.mp4`, `.mov`, `.avi` | video-processor |
| **图片 | Image** | `.jpg`, `.png`, `.webp` | image-processor |
| **日志 | Logs** | `.log`, `.txt` | log-processor |
| **Office** | `.docx`, `.pptx`, `.xlsx` | office-processor |
| **压缩包 | Archives** | `.zip`, `.rar`, `.7z` | archive-processor |

---

## 🔄 工作流程 | Workflow

```
用户发送文件 | User sends file
    ↓
Gateway 接收并保存 | Gateway receives and saves
    ↓
检查文件大小 | Check file size
    ↓
<10MB: 同步处理 → 立即返回结果 | <10MB: Sync → Return result immediately
>10MB: 异步处理 → 立即确认"处理中" | >10MB: Async → Confirm "processing" immediately
    ↓
后台子进程处理 | Background subprocess processing
    ↓
处理完成 → 推送结果给用户 | Complete → Push result to user
```

---

## 🧪 测试 | Testing

```bash
# 测试小文件（同步模式）| Test small file (sync mode)
echo "测试内容 | Test content" > test.txt
python "E:\ai\openclaw\.openclaw\workspace\skills\large-file-handler\scripts\handle_file.py" "test.txt" --user-id "ou_xxx" --channel "feishu"

# 测试大文件（异步模式）| Test large file (async mode)
# 创建 15MB 测试文件 | Create 15MB test file
fsutil file createnew "large_test.zip" 15000000
python "E:\ai\openclaw\.openclaw\workspace\skills\large-file-handler\scripts\handle_file.py" "large_test.zip" --user-id "ou_xxx" --channel "feishu"
```

---

## ⚠️ 注意事项 | Notes

1. **消息推送** - 当前使用 `print()` 占位，需要集成飞书 API 实现真实推送
   **Message Push** - Currently uses `print()` as placeholder, need to integrate Feishu API for real push

2. **PDF 处理** - 框架已创建，需要安装 `PyPDF2` 或 `pdfplumber` 实现实际提取
   **PDF Processing** - Framework created, need to install `PyPDF2` or `pdfplumber` for actual extraction

3. **编码问题** - Windows PowerShell 默认使用 GBK 编码，脚本已避免使用 emoji
   **Encoding** - Windows PowerShell uses GBK by default, scripts avoid emoji

4. **路径格式** - 使用正斜杠 `/` 或原始字符串 `r""` 避免转义问题
   **Path Format** - Use forward slashes `/` or raw strings `r""` to avoid escape issues

---

## 📝 依赖 | Dependencies

- Python 3.7+
- 无额外依赖（基础功能）| No extra dependencies (basic features)
- 可选 | Optional:
  - `PyPDF2`、`pdfplumber`（PDF 处理 | PDF processing）
  - `pytesseract`、`pdf2image`（图片 OCR | Image OCR）

---

## 📄 许可证 | License

MIT License - 详见 LICENSE 文件 | See LICENSE file for details

---

## 👤 作者 | Author

**Leo 🦁**

---

## 🤝 贡献 | Contributing

欢迎提交 Issue 和 Pull Request！
Issues and Pull Requests are welcome!

---

**版本 | Version**: 1.0.0  
**创建日期 | Created**: 2026-04-03  
**更新日期 | Updated**: 2026-04-03
