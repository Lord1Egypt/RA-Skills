# rclone 操作参考

## rclone Remote 配置

```ini
# ~/.config/rclone/rclone.conf 中已配置
[nas]
type = smb
host = <NAS_TAILSCALE_IP>
user = openclaw
pass = <ENCRYPTED>
```

## 常用命令

```bash
# 搜索文件
rclone lsf nas:<SHARE> --recursive --include "*关键词*"

# 按扩展名 + 关键词
rclone lsf nas:<SHARE> --recursive --include "*关键词*.pdf"

# 按修改时间过滤（最近 N 天）
rclone lsf nas:<SHARE> --recursive --include "*关键词*" --max-age 30d

# 列出目录结构
rclone tree nas:<SHARE> --max-depth 2

# 获取文件详情
rclone lsl nas:<SHARE>/path/to/file.pdf

# 获取文件大小
rclone size nas:<SHARE>/path --json

# 下载到临时目录
rclone copy "nas:<SHARE>/path/to/file.pdf" /tmp/nas-courier/
```

## 错误处理

| 问题 | 排查命令 |
|------|---------|
| rclone 连接失败 | `tailscale status` |
| rclone 认证失败 | 提示用户检查 NAS 账户密码 |
| 文件不存在 | 重新搜索或让用户确认路径 |
| 磁盘空间不足 | `df -h /tmp`，提示清理后重试 |
