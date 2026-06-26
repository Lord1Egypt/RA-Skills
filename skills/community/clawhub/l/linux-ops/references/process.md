# 进程管理

## 查看进程

```bash
ps aux                      # 所有进程
ps -ef                      # 另一种格式
ps aux | grep nginx         # 查找进程
pgrep nginx                 # 按名称查找
pgrep -f "python app.py"    # 按命令行查找
pstree -p                   # 进程树
```

## 管理进程

```bash
kill PID                    # SIGTERM
kill -9 PID                 # SIGKILL 强制
kill -HUP PID               # SIGHUP 重载配置
pkill nginx                 # 按名称终止
killall nginx               # 按名称终止

# 后台运行
nohup python app.py &
nohup python app.py > output.log 2>&1 &
```

## 系统服务

```bash
systemctl status nginx
systemctl start nginx
systemctl stop nginx
systemctl restart nginx
systemctl reload nginx
systemctl enable nginx      # 开机启动
systemctl disable nginx

# 查看服务
systemctl list-units --type=service
```

## 日志

```bash
journalctl -u nginx
journalctl -u nginx -f                      # 实时
journalctl -u nginx --since "1 hour ago"
journalctl -u nginx -u mysql                # 多个服务
```

## 动态监控

```bash
top                         # 基础监控
htop                        # 更友好
top -o %CPU                 # 按 CPU 排序
top -o %MEM                 # 按内存排序
```
