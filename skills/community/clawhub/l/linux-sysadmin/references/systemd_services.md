# systemd 服务与软件包管理

## 目录

- [1. systemd 服务管理](#1-systemd-服务管理)
- [2. Unit 文件编写](#2-unit-文件编写)
- [3. Timer 定时任务](#3-timer-定时任务)
- [4. Journal 日志管理](#4-journal-日志管理)
- [5. 软件包管理](#5-软件包管理)
- [6. 启动项与目标管理](#6-启动项与目标管理)
- [7. 常见故障排查](#7-常见故障排查)

---

## 1. systemd 服务管理

### 1.1 基本操作

```bash
# 启动/停止/重启/重载
systemctl start nginx
systemctl stop nginx
systemctl restart nginx    # 先停后启
systemctl reload nginx     # 不停止进程，重新加载配置

# 开机自启
systemctl enable nginx
systemctl disable nginx
systemctl enable --now nginx   # 启用并立即启动

# 查看状态
systemctl status nginx
systemctl is-active nginx      # 是否运行
systemctl is-enabled nginx     # 是否开机自启
systemctl is-failed nginx      # 是否失败
```

### 1.2 查看服务列表

```bash
# 所有运行中的服务
systemctl list-units --type=service --state=running

# 所有失败的服务
systemctl list-units --type=service --state=failed

# 所有已安装的服务
systemctl list-unit-files --type=service

# 查看服务依赖
systemctl list-dependencies nginx
systemctl list-dependencies --reverse nginx   # 谁依赖此服务
```

### 1.3 服务控制

```bash
# 屏蔽服务（彻底禁止启动，即使被依赖）
systemctl mask nginx
systemctl unmask nginx

# 查看服务的完整配置
systemctl cat nginx

# 编辑服务（创建 override）
systemctl edit nginx           # 创建 drop-in 文件
systemctl edit --full nginx    # 编辑完整 unit 文件

# 重新加载 systemd 配置（修改 unit 文件后必须执行）
systemctl daemon-reload
```

---

## 2. Unit 文件编写

### 2.1 基本结构

```ini
# /etc/systemd/system/myapp.service

[Unit]
Description=My Application Server
Documentation=https://docs.example.com/myapp
After=network.target postgresql.service
Requires=postgresql.service
Wants=redis.service

[Service]
Type=simple
User=myapp
Group=myapp
WorkingDirectory=/opt/myapp
ExecStartPre=/opt/myapp/bin/check-config
ExecStart=/opt/myapp/bin/server --config /etc/myapp/config.yaml
ExecReload=/bin/kill -HUP $MAINPID
ExecStop=/bin/kill -TERM $MAINPID
Restart=on-failure
RestartSec=5
TimeoutStartSec=30
TimeoutStopSec=30

# 资源限制
LimitNOFILE=65536
LimitNPROC=4096

# 环境变量
Environment=NODE_ENV=production
EnvironmentFile=/etc/myapp/env

# 安全加固
NoNewPrivileges=yes
ProtectSystem=strict
ProtectHome=yes
ReadWritePaths=/var/lib/myapp /var/log/myapp
PrivateTmp=yes

[Install]
WantedBy=multi-user.target
```

### 2.2 Service Type 说明

```ini
# simple（默认）— ExecStart 启动的进程就是主进程
Type=simple

# forking — 进程会 fork 子进程，父进程退出
Type=forking
PIDFile=/var/run/myapp.pid

# oneshot — 一次性任务，执行完就退出
Type=oneshot
RemainAfterExit=yes   # 退出后仍标记为 active

# notify — 进程通过 sd_notify() 通知 systemd 已就绪
Type=notify

# exec — 类似 simple，但在 exec() 成功后才算启动成功
Type=exec
```

### 2.3 Restart 策略

```ini
# 重启条件
Restart=no              # 不重启
Restart=on-success      # 正常退出时重启
Restart=on-failure      # 异常退出时重启（推荐）
Restart=on-abnormal     # 信号/超时/看门狗时重启
Restart=on-abort        # 信号退出时重启
Restart=always          # 总是重启

# 重启间隔
RestartSec=5            # 重启前等待 5 秒

# 重启频率限制
StartLimitIntervalSec=300   # 在 300 秒内
StartLimitBurst=5           # 最多重启 5 次
```

### 2.4 Drop-in 文件（覆盖配置）

```bash
# 创建 drop-in 目录
mkdir -p /etc/systemd/system/nginx.service.d/

# 添加覆盖配置
cat > /etc/systemd/system/nginx.service.d/override.conf << 'EOF'
[Service]
LimitNOFILE=65536
Environment=WORKER_PROCESSES=auto
EOF

# 或使用 systemctl edit
systemctl edit nginx
# 编辑器中输入覆盖内容

# 重载
systemctl daemon-reload
systemctl restart nginx
```

---

## 3. Timer 定时任务

### 3.1 创建 Timer

```ini
# /etc/systemd/system/backup.timer
[Unit]
Description=Daily backup timer

[Timer]
OnCalendar=*-*-* 02:00:00    # 每天凌晨 2 点
Persistent=true                # 错过的任务在启动后补执行
RandomizedDelaySec=300         # 随机延迟 0-300 秒（避免集中执行）
AccuracySec=1min               # 精度

[Install]
WantedBy=timers.target
```

```ini
# /etc/systemd/system/backup.service
[Unit]
Description=Daily backup

[Service]
Type=oneshot
ExecStart=/opt/scripts/backup.sh
User=backup
```

```bash
# 启用 timer
systemctl daemon-reload
systemctl enable --now backup.timer

# 查看 timer 状态
systemctl list-timers --all
systemctl status backup.timer
```

### 3.2 Timer 时间表达式

```ini
# OnCalendar 格式：DayOfWeek Year-Month-Day Hour:Minute:Second

OnCalendar=hourly              # 每小时
OnCalendar=daily               # 每天 00:00
OnCalendar=weekly              # 每周一 00:00
OnCalendar=monthly             # 每月 1 号 00:00
OnCalendar=*-*-* 02:00:00     # 每天 02:00
OnCalendar=Mon *-*-* 09:00:00 # 每周一 09:00
OnCalendar=*-*-01 00:00:00    # 每月 1 号
OnCalendar=*:0/15              # 每 15 分钟

# 相对时间
OnBootSec=5min                 # 启动后 5 分钟
OnUnitActiveSec=1h             # 上次激活后 1 小时

# 验证时间表达式
systemd-analyze calendar "*-*-* 02:00:00"
```

### 3.3 Timer vs Cron 对比

| 特性 | systemd Timer | cron |
|------|--------------|------|
| 依赖管理 | ✅ 支持 | ❌ |
| 日志 | ✅ journalctl | 需手动 |
| 错过补执行 | ✅ Persistent | ❌ |
| 资源限制 | ✅ cgroup | ❌ |
| 随机延迟 | ✅ | ❌ |
| 简单语法 | ❌ 较复杂 | ✅ 简洁 |

---

## 4. Journal 日志管理

### 4.1 查看日志

```bash
# 查看服务日志
journalctl -u nginx                    # 指定服务
journalctl -u nginx -f                 # 实时跟踪
journalctl -u nginx -n 100            # 最近 100 行
journalctl -u nginx --no-pager        # 不分页

# 时间范围
journalctl -u nginx --since "2026-04-01 00:00:00"
journalctl -u nginx --since "1 hour ago"
journalctl -u nginx --since yesterday --until today

# 按优先级
journalctl -u nginx -p err            # 只看错误
journalctl -p warning                  # 警告及以上

# 按进程
journalctl _PID=1234
journalctl _COMM=sshd

# 内核日志
journalctl -k
journalctl -k -b -1   # 上次启动的内核日志

# 启动日志
journalctl -b          # 当前启动
journalctl -b -1       # 上次启动
journalctl --list-boots # 列出所有启动记录
```

### 4.2 日志管理

```bash
# 查看日志磁盘占用
journalctl --disk-usage

# 清理日志
journalctl --vacuum-size=500M    # 保留 500M
journalctl --vacuum-time=30d     # 保留 30 天
journalctl --vacuum-files=5      # 保留 5 个文件

# 持久化配置（/etc/systemd/journald.conf）
[Journal]
Storage=persistent         # 持久化存储（默认 volatile）
SystemMaxUse=1G           # 最大占用 1G
SystemMaxFileSize=100M    # 单文件最大 100M
MaxRetentionSec=30day     # 保留 30 天
Compress=yes              # 压缩

# 重启 journald
systemctl restart systemd-journald
```

### 4.3 日志转发

```bash
# 转发到 syslog
# /etc/systemd/journald.conf
ForwardToSyslog=yes

# 转发到远程 syslog 服务器（通过 rsyslog）
# /etc/rsyslog.d/50-remote.conf
*.* @syslog-server:514        # UDP
*.* @@syslog-server:514       # TCP
```

---

## 5. 软件包管理

### 5.1 APT（Ubuntu/Debian）

```bash
# 更新索引
apt update

# 安装/卸载
apt install nginx
apt remove nginx           # 卸载（保留配置）
apt purge nginx            # 卸载（删除配置）
apt autoremove             # 清理不再需要的依赖

# 搜索
apt search nginx
apt show nginx             # 查看包信息

# 升级
apt upgrade                # 升级所有包
apt full-upgrade           # 升级（允许移除旧包）

# 版本锁定
apt-mark hold nginx        # 锁定版本
apt-mark unhold nginx      # 解锁
apt-mark showhold          # 查看锁定的包

# 查看已安装
dpkg -l | grep nginx
dpkg -L nginx              # 查看包安装了哪些文件
dpkg -S /usr/sbin/nginx    # 查看文件属于哪个包

# 清理缓存
apt clean                  # 清理所有缓存
apt autoclean              # 清理过时缓存
```

### 5.2 YUM/DNF（RHEL/CentOS）

```bash
# 安装/卸载
yum install nginx          # 或 dnf install nginx
yum remove nginx
yum autoremove

# 搜索
yum search nginx
yum info nginx

# 升级
yum update                 # 升级所有包
yum update nginx           # 升级指定包

# 版本锁定
yum install yum-plugin-versionlock
yum versionlock add nginx
yum versionlock list
yum versionlock delete nginx

# 查看已安装
rpm -qa | grep nginx
rpm -ql nginx              # 查看包文件
rpm -qf /usr/sbin/nginx    # 查看文件属于哪个包

# 仓库管理
yum repolist               # 查看启用的仓库
yum-config-manager --add-repo https://example.com/repo
yum-config-manager --enable repo-name
yum-config-manager --disable repo-name

# 清理缓存
yum clean all
```

### 5.3 仓库源配置

```bash
# Ubuntu 添加 PPA
add-apt-repository ppa:nginx/stable
apt update

# Ubuntu 添加自定义仓库
cat > /etc/apt/sources.list.d/custom.list << 'EOF'
deb [signed-by=/usr/share/keyrings/custom.gpg] https://repo.example.com/apt stable main
EOF
# 导入 GPG 密钥
curl -fsSL https://repo.example.com/gpg | gpg --dearmor -o /usr/share/keyrings/custom.gpg

# RHEL 添加仓库
cat > /etc/yum.repos.d/custom.repo << 'EOF'
[custom]
name=Custom Repository
baseurl=https://repo.example.com/yum/el$releasever/$basearch
enabled=1
gpgcheck=1
gpgkey=https://repo.example.com/gpg
EOF
```

---

## 6. 启动项与目标管理

### 6.1 启动目标（Target）

```bash
# 查看当前目标
systemctl get-default

# 设置默认目标
systemctl set-default multi-user.target    # 命令行模式
systemctl set-default graphical.target     # 图形界面

# 切换目标（不重启）
systemctl isolate multi-user.target
systemctl isolate rescue.target            # 救援模式

# 常用目标
# poweroff.target   — 关机
# rescue.target     — 救援模式（单用户）
# multi-user.target — 多用户命令行
# graphical.target  — 图形界面
# reboot.target     — 重启
```

### 6.2 启动分析

```bash
# 查看启动耗时
systemd-analyze
systemd-analyze blame          # 各服务启动耗时排序
systemd-analyze critical-chain # 关键链路

# 生成启动时序图
systemd-analyze plot > boot.svg
```

---

## 7. 常见故障排查

### 服务启动失败

```bash
# 1. 查看详细状态
systemctl status myapp -l

# 2. 查看日志
journalctl -u myapp -n 50 --no-pager

# 3. 检查 unit 文件语法
systemd-analyze verify /etc/systemd/system/myapp.service

# 4. 手动执行 ExecStart 命令测试
su - myapp -c "/opt/myapp/bin/server --config /etc/myapp/config.yaml"

# 5. 检查权限
ls -la /opt/myapp/bin/server
namei -l /opt/myapp/bin/server

# 6. 检查端口冲突
ss -tlnp | grep :8080

# 7. 检查资源限制
systemctl show myapp | grep -E "Limit|Memory|CPU"
```

### 服务反复重启

```bash
# 1. 查看重启记录
journalctl -u myapp --since "1 hour ago" | grep -E "Started|Stopped|Failed"

# 2. 查看退出码
systemctl show myapp -p ExecMainStatus

# 3. 检查重启策略
systemctl show myapp -p Restart,RestartSec,StartLimitBurst,StartLimitIntervalSec

# 4. 临时禁用自动重启调试
systemctl edit myapp
# [Service]
# Restart=no
```

### 软件包安装失败

```bash
# APT 修复
apt --fix-broken install
dpkg --configure -a
apt update --fix-missing

# YUM 修复
yum clean all
yum makecache
rpm --rebuilddb
```
