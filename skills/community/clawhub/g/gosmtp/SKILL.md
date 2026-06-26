---
name:  Gosmtp
description: Email邮件发送工具
---

# Go 邮件发送工具

## 📦 文件说明

- `mail_sender.exe` - 编译后的可执行文件（5.3MB）
- `main.go` - 源代码
- `go.mod` - Go 模块定义

## ⚙️ 环境变量配置

在 Windows PowerShell 中设置：

```powershell
$env:SMTP_HOST="smtp.qq.com"
$env:SMTP_PORT="587"
$env:SMTP_USERNAME="siysunopcl@qq.com"
$env:SMTP_PASSWORD="wfpjoocjildcbjeh"
$env:FROM_EMAIL="siysunopcl@qq.com"
$env:FROM_NAME="Agent通知系统"
```

或在 CMD 中：

```cmd
set SMTP_HOST=smtp.qq.com
set SMTP_PORT=587
set SMTP_USERNAME=siysunopcl@qq.com
set SMTP_PASSWORD=wfpjoocjildcbjeh
set FROM_EMAIL=siysunopcl@qq.com
set FROM_NAME=Agent通知系统
```

## 🚀 使用方法

### 1. 测试 SMTP 连接

```powershell
cd mail_sender
$env:SMTP_HOST="smtp.qq.com"
$env:SMTP_PORT="587"
$env:SMTP_USERNAME="siysunopcl@qq.com"
$env:SMTP_PASSWORD="wfpjoocjildcbjeh"
./mail_sender.exe
```

### 2. 在代码中调用

```go
import "your-module/mail_sender"

config := mail_sender.NewMailConfig()
email := &mail_sender.Email{
    To:      []string{"recipient@example.com"},
    Subject: "测试邮件",
    Body:    "<h1>HTML内容</h1>",
    Files:   []string{"attachment.pdf"}, // 可选附件
}

err := email.Send(config)
```

### 3. 作为命令行工具

```powershell
# 直接运行（使用默认配置发送测试邮件）
./mail_sender.exe

# 发送自定义邮件（通过修改代码）
```
