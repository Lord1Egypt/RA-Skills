---
name: local-file-sender
version: 1.0.1
description: 本地文件发送工具。用户通过自然语言指定本地文件路径，将文件上传到云存储并发送下载链接。支持 Windows/Linux/macOS 路径格式。⚠️ 仅适用于本地部署的 OpenClaw，云端部署无法访问用户本地文件。
requires:
  deployment: local
  platforms:
    - Windows
    - Linux
    - macOS
  tools:
    - lightclaw_upload_file
---

# 本地文件发送工具

## ⚠️ 重要说明

**此 skill 仅适用于本地部署的 OpenClaw！**

- ✅ **本地部署**：可以访问本地文件系统，支持此功能
- ❌ **云端部署**：无法访问用户本地文件，不支持此功能

**云端用户替代方案**：
1. 直接在聊天中上传文件
2. 使用飞书/企业微信自带的文件发送功能

---

## 功能说明

将本地文件上传到云存储并发送下载链接，用户只需通过自然语言指定文件路径。

## 触发场景

当用户说以下类似语句时触发：
- "把 E:\校对\报告.xlsx 发给飞书"
- "发送 C:\Users\Documents\report.pdf 到飞书"
- "把 /home/user/report.xlsx 发给我"
- "发送这个文件到飞书：D:\项目\数据.xlsx"

## 执行步骤

当收到用户的文件发送请求时，按以下步骤处理：

### 步骤 1：识别文件路径

从用户消息中提取文件路径，支持以下格式：

**Windows 路径**：
- `E:\校对\报告.xlsx`
- `C:\Users\用户名\Documents\file.pdf`
- `D:\项目\2024\数据.xlsx`

**Linux/macOS 路径**：
- `/home/user/report.xlsx`
- `/Users/用户名/Documents/file.pdf`
- `~/Documents/report.xlsx`

### 步骤 2：规范化路径

```python
import os

# 处理用户目录
if path.startswith('~'):
    path = os.path.expanduser(path)

# Windows 路径处理
path = os.path.normpath(path)

# 获取绝对路径
path = os.path.abspath(path)
```

### 步骤 3：检查文件

使用 `exec` 工具检查文件是否存在：

**Windows PowerShell**：
```powershell
Test-Path "E:\校对\报告.xlsx"
Get-Item "E:\校对\报告.xlsx" | Select-Object Name, Length, LastWriteTime
```

**Linux/macOS**：
```bash
ls -la "/home/user/report.xlsx"
```

### 步骤 4：上传文件到云存储

**重要**：飞书等平台不支持直接发送本地文件路径，必须先上传到云存储。

使用 `lightclaw_upload_file` 工具上传文件：

```json
{
  "paths": ["E:\\校对\\报告.xlsx"]
}
```

该工具会返回公开的下载链接。

### 步骤 5：发送下载链接

上传成功后，发送包含下载链接的消息：

```
📄 文件已上传，请点击下载：
[报告.xlsx](下载链接)
```

---

## 完整示例

### 用户请求
```
把 E:\校对\报告.xlsx 发给飞书
```

### AI 处理流程

1. **识别路径**：`E:\校对\报告.xlsx`

2. **检查文件**：
   ```powershell
   Test-Path "E:\校对\报告.xlsx"
   ```

3. **上传文件**：
   ```json
   {
     "paths": ["E:\\校对\\报告.xlsx"]
   }
   ```

4. **发送结果**：
   ```
   ✅ 文件已上传，请点击下载：
   [报告.xlsx](https://xxx.lightclaw.com/xxx)
   ```

---

## 错误处理

### 文件不存在
```
❌ 文件不存在: E:\校对\报告.xlsx
请检查路径是否正确。
```

### 权限不足
```
❌ 无法读取文件: C:\System\config.dat
权限不足，请检查文件访问权限。
```

### 文件过大
```
⚠️ 文件较大 (150MB)，上传可能需要较长时间...
正在上传中...
```

### 云端部署提示
```
⚠️ 当前为云端部署，无法访问您的本地文件。

替代方案：
1. 直接在聊天中上传文件
2. 使用飞书自带的文件发送功能
```

---

## 技术说明

### 为什么不能直接用 message 发送本地文件？

飞书、企业微信等平台的 Bot API 不支持直接发送本地文件路径。必须通过以下方式之一：

1. **上传到云存储**（本 skill 采用的方式）
   - 使用 `lightclaw_upload_file` 上传
   - 返回公开下载链接
   - 用户点击链接下载

2. **使用平台专用上传 API**
   - 飞书：需要先调用文件上传 API 获取 file_key
   - 企业微信：需要调用媒体文件上传接口

本 skill 选择方案 1，因为它：
- 不需要各平台专用的 API 配置
- 支持所有平台（飞书、企业微信、Telegram 等）
- 用户可以通过链接重复下载

---

## 注意事项

1. **必须本地部署**：此 skill 需要在能够访问本地文件系统的环境中运行
2. **文件大小限制**：上传服务可能有大小限制
3. **路径格式**：Windows 路径使用反斜杠 `\`，Linux/macOS 使用正斜杠 `/`
4. **中文路径**：支持中文路径和文件名
5. **云端限制**：云端部署无法访问用户本地文件，需使用替代方案
6. **链接有效期**：下载链接可能有时效限制，建议及时下载
