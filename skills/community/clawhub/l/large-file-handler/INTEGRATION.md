# 🚀 大文件处理器 - 集成指南 | Integration Guide

## 当前状态 | Current Status

✅ 技能已创建并可用 | Skill created and ready  
✅ 脚本可以正常运行 | Scripts working  
✅ 文件保存和异步处理框架完成 | File save and async processing framework complete  

---

## 📋 如何在 Gateway 中使用 | How to Use in Gateway

### 方法 1：通过技能调用（推荐）| Method 1: Via Skill Call (Recommended)

当用户发送文件时，在 Gateway 中调用此技能：
When user sends a file, call this skill in Gateway:

```python
# 在 Gateway 的文件处理逻辑中 | In Gateway file processing logic
import subprocess
import sys

def handle_incoming_file(file_path: str, user_id: str, channel: str):
    """处理接收到的文件 | Handle incoming file"""
    
    skill_script = r"E:\ai\openclaw\.openclaw\workspace\skills\large-file-handler\scripts\handle_file.py"
    
    # 启动处理进程 | Start processing process
    subprocess.Popen([
        sys.executable,
        skill_script,
        file_path,
        '--user-id', user_id,
        '--channel', channel
    ])
    
    # 立即返回确认消息 | Return confirmation immediately
    return "收到文件，正在处理... | File received, processing..."
```

### 方法 2：直接调用处理函数 | Method 2: Direct Function Call

```python
import sys
sys.path.insert(0, r"E:\ai\openclaw\.openclaw\workspace\skills\large-file-handler\scripts")

from handle_file import process_file

# 处理文件 | Process file
process_file(
    file_path="C:/Users/test/document.pdf",
    user_id="ou_xxx",
    channel="feishu"
)
```

---

## 📊 文件大小阈值 | File Size Thresholds

| 文件大小 | 处理模式 | 响应方式 |
|---------|---------|---------|
| <10MB | 同步 | 立即处理并返回结果 |
| 10-500MB | 异步 | 立即确认，后台处理，完成后推送 |
| >500MB | 拒绝 | 返回错误提示 |

| File Size | Mode | Response |
|-----------|------|----------|
| <10MB | Sync | Process and return immediately |
| 10-500MB | Async | Confirm immediately, process in background, push when done |
| >500MB | Reject | Return error |

---

## 🔧 配置选项 | Configuration Options

编辑 `handle_file.py` 修改配置：
Edit `handle_file.py` to modify configuration:

```python
LARGE_FILE_THRESHOLD = 10 * 1024 * 1024  # 10MB - 异步阈值 | Async threshold
MAX_FILE_SIZE = 500 * 1024 * 1024        # 500MB - 最大支持 | Max supported
```

---

## 📁 文件存储位置 | File Storage Locations

```
E:/ai/openclaw/.openclaw/workspace/tmp/files/
├── pending/      # 待处理 | Pending
├── processing/   # 处理中 | Processing
└── completed/    # 已完成 | Completed (cleaned after 24h)
```

---

## ⚠️ 注意事项 | Notes

1. **编码问题** - Windows PowerShell 默认使用 GBK 编码，脚本已避免使用 emoji
   **Encoding** - Windows PowerShell uses GBK by default, scripts avoid emoji

2. **路径格式** - 使用正斜杠 `/` 或原始字符串 `r""` 避免转义问题
   **Path Format** - Use forward slashes `/` or raw strings `r""`

3. **异步进程** - 后台处理使用独立子进程，不影响 Gateway 主进程
   **Async Process** - Background processing uses independent subprocess, no impact on Gateway

4. **文件清理** - 需要定期清理 `completed/` 目录（可设置定时任务）
   **File Cleanup** - Need periodic cleanup of `completed/` directory (can use scheduled tasks)

---

## 🧪 测试方法 | Testing Methods

```bash
# 测试小文件（同步模式）| Test small file (sync mode)
python "E:\ai\openclaw\.openclaw\workspace\skills\large-file-handler\scripts\handle_file.py" "测试文件.txt" --user-id "ou_xxx" --channel "feishu"

# 测试大文件（异步模式）| Test large file (async mode)
# 创建一个大于 10MB 的文件 | Create a file larger than 10MB
fsutil file createnew "large_test.zip" 15000000
python "E:\ai\openclaw\.openclaw\workspace\skills\large-file-handler\scripts\handle_file.py" "large_test.zip" --user-id "ou_xxx" --channel "feishu"
```

---

## 📝 待完善功能 | TODO

- [ ] PDF 内容提取（集成 PyPDF2/pdfplumber）| PDF content extraction
- [ ] 视频关键帧提取 | Video keyframe extraction
- [ ] 图片 OCR | Image OCR
- [ ] 真实的消息推送（目前使用 print 占位）| Real message push (currently using print placeholder)
- [ ] 定时清理任务 | Scheduled cleanup task

---

**创建日期 | Created**: 2026-04-03  
**版本 | Version**: v1.0.0  
**作者 | Author**: Leo 🦁
