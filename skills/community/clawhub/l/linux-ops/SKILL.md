---
name: linux-ops
description: Linux 运维速查。当需要：(1) 进程管理 (2) 日志分析 (3) 网络诊断 (4) 性能监控 (5) 用户管理时使用。
---

# Linux Operations

Linux 运维命令速查手册。

## 快速参考

### 进程管理
```bash
ps aux | grep nginx          # 查找进程
kill -9 PID                  # 终止进程
systemctl status nginx       # 服务状态
journalctl -u nginx -f       # 服务日志
```

### 系统资源
```bash
top / htop                   # CPU/内存
free -h                      # 内存
df -h                        # 磁盘
du -sh /var/log              # 目录大小
```

### 网络
```bash
ip addr                      # 网络接口
netstat -tuln                # 监听端口
ss -tun                      # 连接状态
ping -c 5 host               # 测试连通
curl -v https://example.com  # HTTP 测试
```

### 日志
```bash
tail -f /var/log/syslog      # 实时查看
grep "error" /var/log/syslog # 搜索日志
journalctl -u nginx --since "1 hour ago"
```

### 文件查找
```bash
find /path -name "*.py"      # 按名称查找
find / -size +100M           # 按大小查找
grep -r "pattern" /path      # 递归搜索
```

## 详细参考

- **进程管理**: [references/process.md](references/process.md) - 进程查看、管理、服务
- **系统资源**: [references/system.md](references/system.md) - CPU、内存、磁盘
- **网络诊断**: [references/network.md](references/network.md) - 连接、端口、抓包
- **日志分析**: [references/logs.md](references/logs.md) - 系统日志、nginx 日志
- **用户权限**: [references/users.md](references/users.md) - 用户、组、权限

## 常用命令

### 查找大文件
```bash
find / -type f -size +100M 2>/dev/null
du -ah / | sort -rh | head -20
```

### 统计访问
```bash
awk '{print $1}' access.log | sort | uniq -c | sort -rn | head
awk '{print $9}' access.log | sort | uniq -c | sort -rn
```

### 排查端口占用
```bash
lsof -i :80
netstat -tlnp | grep 80
```

## 文档

- TLDR: `tldr command`
- Linux 命令速查: https://cheatography.com/davechild/cheat-sheets/linux-command-line/
