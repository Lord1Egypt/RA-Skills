# 故障排除

## Gmail

### 认证失败
- 确保已安装 `gog` CLI
- 运行 `gog gmail auth` 重新认证
- 检查 OAuth 2.0 凭证是否过期

## Outlook

### 认证失败
- 检查 Microsoft Graph API 凭证
- 确认应用权限包含 `Mail.ReadWrite` 和 `Mail.Send`
- 重新运行 `bash scripts/setup.sh` 获取新的 refresh token

### 附件发送失败
- 文件大小限制 3MB
- 检查文件路径和权限

## 网易邮箱（163.com / 126.com）

### 连接失败
- 确认已在网易邮箱设置中启用 IMAP/SMTP 服务
- 使用应用专用密码（不是登录密码）
- 检查防火墙是否放行 993（IMAP）和 465（SMTP）端口

### IMAP ID 命令失败
- 网易邮箱要求客户端发送 ID 命令标识
- 163.sh 已内置 ID 命令支持，如仍失败检查网络连接

### 应用密码获取
1. 登录网易邮箱网页版
2. 设置 → POP3/SMTP/IMAP → 开启 IMAP
3. 获取授权码（即应用密码）

## 通用问题

### 配置文件损坏
- 配置文件：`~/.onemail/config.json`
- 凭证文件：`~/.onemail/credentials.json`
- 可删除后重新运行 `bash scripts/setup.sh`

### JSON 解析错误
- 确保已安装 `jq`
- 检查配置文件是否为有效 JSON：`jq . ~/.onemail/config.json`
