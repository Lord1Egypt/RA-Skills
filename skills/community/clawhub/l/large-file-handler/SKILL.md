---
name: large-file-handler
description: 大文件异步处理器。当用户发送大文件（>10MB）时自动启用，采用流式保存 + 后台异步处理，避免 Gateway 卡死。支持 PDF、视频、图片、日志、Office 文档等。处理完成后主动推送结果。
author: Leo
license: MIT
---

# large-file-handler - 大文件异步处理技能

## 🎯 功能

接收和处理大文件（PDF、视频、图片、日志、Office 等），采用**异步处理 + 结果推送**模式，避免 Gateway 卡死。

## 📁 文件存储结构

```
tmp/files/
├── pending/      # 待处理文件
├── processing/   # 处理中文件（带锁标记）
└── completed/    # 已完成文件（保留 24 小时后清理）
```

## ⚙️ 配置参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `LARGE_FILE_THRESHOLD` | 10MB | 超过此大小自动切换异步模式 |
| `MAX_FILE_SIZE` | 500MB | 最大接收文件大小 |
| `CHUNK_SIZE` | 5MB | 分块处理大小 |
| `RETENTION_HOURS` | 24 | 完成文件保留时间 |

## 🔄 处理流程

### 1. 文件接收
```
用户发送文件
    ↓
检查文件大小
    ↓
<阈值：直接处理
>阈值：异步模式
    ↓
流式保存到 tmp/files/pending/
    ↓
立即回复"收到，处理中"
```

### 2. 异步处理
```
后台任务启动
    ↓
移动文件到 processing/（加锁）
    ↓
根据文件类型调用对应处理器
    ↓
处理完成 → 移动到 completed/
    ↓
推送结果给用户
```

## 📦 文件类型处理器

| 类型 | 处理器 | 说明 |
|------|--------|------|
| `.pdf` | `pdf-processor` | PDF 提取/OCR/摘要 |
| `.mp4,.mov,.avi` | `video-processor` | 关键帧提取 + 音频转文字 |
| `.jpg,.png,.webp` | `image-processor` | OCR + 内容描述 |
| `.log,.txt` | `log-processor` | 关键字提取 + 错误分析 |
| `.docx,.pptx,.xlsx` | `office-processor` | 转换为 Markdown |
| `.zip,.rar,.7z` | `archive-processor` | 解压 + 选择性提取 |

## 💬 用户交互示例

### 小文件（<10MB）
```
用户：[发送文件]
我：[直接处理并回复结果]
```

### 大文件（>10MB）
```
用户：[发送 50MB PDF]
我：收到文件「xxx.pdf」（50MB），正在后台处理，完成后发你结果 🦁

【3 分钟后】

我：[PDF 处理完成]
📄 文档标题：xxx
📊 共 xx 页
📝 内容摘要：...
```

## 🔧 技术实现

### 文件保存（流式）
```python
def save_file_stream(file_stream, dest_path, chunk_size=5*1024*1024):
    with open(dest_path, 'wb') as f:
        while chunk := file_stream.read(chunk_size):
            f.write(chunk)
    return True
```

### 异步任务启动
```python
import subprocess

def start_async_task(file_path, handler_type):
    # 启动独立子进程，与 Gateway 隔离
    subprocess.Popen([
        'python', 'handlers/{handler_type}.py',
        '--file', file_path,
        '--notify', 'feishu'
    ], cwd=WORKSPACE)
```

### 文件锁机制
```python
def acquire_lock(file_path):
    lock_file = file_path + '.lock'
    try:
        with open(lock_file, 'x') as f:
            f.write(str(os.getpid()))
        return True
    except FileExistsError:
        return False  # 已被其他进程处理
```

## 📝 待办事项

- [ ] 实现文件接收和流式保存
- [ ] 实现大小阈值判断
- [ ] 创建各类型文件处理器
- [ ] 实现结果推送机制
- [ ] 添加定时清理任务（清理 completed/ 超过 24 小时的文件）

## 🚀 使用方法

```python
# 在 Gateway 中调用
from large_file_handler import handle_file

result = handle_file(
    file_stream=request.files['file'],
    file_name='example.pdf',
    user_id='ou_xxx',
    channel='feishu'
)

if result['async']:
    # 异步模式，已自动后台处理
    return "收到文件，处理完成后通知你"
else:
    # 同步模式，直接返回结果
    return result['content']
```

---

**版本**: v0.1  
**创建日期**: 2026-04-03  
**作者**: Leo 🦁
