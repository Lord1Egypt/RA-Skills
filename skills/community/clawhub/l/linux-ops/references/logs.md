# 日志分析

## 系统日志

```bash
# 日志位置
/var/log/syslog             # Debian/Ubuntu
/var/log/messages           # CentOS/RHEL
/var/log/auth.log           # 认证日志
/var/log/kern.log           # 内核日志

# 查看日志
tail -f /var/log/syslog     # 实时
tail -100 /var/log/syslog   # 最后 100 行
head -50 /var/log/syslog    # 前 50 行

# 搜索日志
grep "error" /var/log/syslog
grep -i "error\|fail" /var/log/syslog
grep -A 5 "error" /var/log/syslog   # 显示后 5 行
grep -B 5 "error" /var/log/syslog   # 显示前 5 行
grep -C 5 "error" /var/log/syslog   # 前后各 5 行
```

## Nginx 日志分析

```bash
# 实时监控
tail -f /var/log/nginx/access.log | grep "404\|500"

# 统计访问量
wc -l /var/log/nginx/access.log

# 按时间过滤
grep "27/Apr/2026" /var/log/nginx/access.log

# 统计 IP 访问
awk '{print $1}' /var/log/nginx/access.log | sort | uniq -c | sort -rn | head

# 统计状态码
awk '{print $9}' /var/log/nginx/access.log | sort | uniq -c | sort -rn

# 统计 URL 访问
awk '{print $7}' /var/log/nginx/access.log | sort | uniq -c | sort -rn | head

# 分析慢请求
awk '$NF > 1 {print $0}' /var/log/nginx/access.log
```

## journalctl

```bash
journalctl                  # 所有日志
journalctl -n 100           # 最后 100 条
journalctl -f               # 实时
journalctl --since "1 hour ago"
journalctl --since "2026-04-27 10:00:00"
journalctl -u nginx         # 指定服务
journalctl -p err           # 按优先级
```
