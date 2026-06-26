---
name: custom-clients
description: 列出 E:\work\custom 下所有客户文件夹名称。触发词包括"我的客户"、"列出客户"、"客户有哪些"、"支持的客户"、"客户列表"、"查看客户"、"custom客户"。
user-invocable: true
---

# Custom Clients

列出支持的客户列表。

## 使用方法

当需要列出支持的客户时，执行以下 PowerShell 命令：

```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8; Get-ChildItem -Path "E:\work\custom" -Directory | ForEach-Object { $_.Name }
```

这会返回 E:\work\custom 目录下所有子文件夹的名称（即客户名称）。