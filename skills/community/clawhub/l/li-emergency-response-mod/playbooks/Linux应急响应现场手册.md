# Linux 应急响应现场手册（企业版）

> 来源吸收：`NOPTrace-Linux-应急响应手册-整理版`  
> 目标：把 Linux 现场排查动作沉淀成“低误用、可执行、可审计”的企业 SOP。

## 1. 常见事件类型
- 挖矿病毒
- 远控后门 / 木马
- 勒索病毒
- 暴力破解 / 未授权访问（SSH / MySQL / FTP / Redis / MongoDB）
- 非持续性事件（偶发外联/执行）
- 恶意软件包 / 供应链攻击
- 隧道（SSH / DNS / ICMP / HTTP(S) / SSL / Socks）

## 2. Linux 现场通用顺序
1. 二次研判告警真实性
2. 固定最小证据集
3. 由 IOC / 文件路径 / 连接 / 资源异常反查 PID
4. 由 PID 反查：
   - 可执行文件
   - 当前工作目录
   - 命令行
   - 父子进程 / 线程
   - 启动时间
   - 打开的文件/端口
5. 先暂停验证，再决定是否清除
6. 删除/隔离前先确认文件占用、属性、挂载与隐藏点
7. 做持久化、系统命令、系统包、SSH key、计划任务、systemd、sudo/PAM、内核模块等常规安全检查
8. 善后扩面

## 3. 高频命令清单

### 3.1 资源异常与进程树
```bash
top -c -o %CPU
top -c -o %MEM
ps -w -eo pid,ppid,%mem,%cpu,cmd --sort=-%cpu | head -n 5
ps -w -eo pid,ppid,%mem,%cpu,cmd --sort=-%mem | head -n 5
ps -w ajfx
pstree -agplU
```

### 3.2 连接与外联
```bash
ss
netstat -pantu
lsof -i:<port>
```

### 3.3 由 pid 反查文件、线程、映射、服务
```bash
lsof -p <pid>
pwdx <pid>
systemctl status <pid>
cat /proc/<pid>/maps
ls -al /proc/<pid>/exe
ps -w -Lf <pid>
top -H -p <pid>
pstree -agplU <pid>
```

### 3.4 时间线与文件
```bash
ps -w -eo pid,lstart,etime,cmd | grep <pid>
stat <file>
ls -al <file>
find /path/to/search -type f -newerat "开始时间" ! -newermt "结束时间" 2>/dev/null
```

### 3.5 账号与登录
```bash
w
who
last -awF
lastlog
lslogins
awk -F: '$3==0 {print $1}' /etc/passwd
awk -F: '$2 != "x" { print $0 }' /etc/passwd
```

### 3.6 SSH / cron / 自启动 / 关键配置
重点检查：
- `/var/log/auth.log` 或 `/var/log/secure`
- `/etc/crontab`
- `/etc/cron.d/*`
- `/var/spool/cron/*`
- `/etc/rc.local`
- `/etc/profile`
- `/etc/profile.d/*`
- `~/.bashrc`
- `~/.bash_profile`
- `~/.profile`
- `/root/.ssh/authorized_keys`
- `~/.ssh/authorized_keys`
- `/etc/ssh/sshd_config`
- `/etc/ld.so.preload`
- `/etc/sudoers`
- `/etc/sudoers.d/`

### 3.7 权限提升与内核层
```bash
find / -perm /4000
find / -perm /2000
find / -perm /6000
getcap -r / 2>/dev/null
sudo iptables -L
lsmod
modinfo <module_name>
sudo dmesg | grep -i "taint"
```

## 4. 取证与保全要点
- 优先采集：PID 对应文件、命令行、连接、样本、时间线。
- 证据优先场景可先：
```bash
kill -SIGSTOP <pid>
kill -SIGCONT <pid>
```
- 删除前先看：
```bash
lsof <file>
ls -li <file>
cat /proc/$$/mountinfo
```
- 若文件已删除但进程还在，可尝试：
```bash
cp /proc/<pid>/exe /tmp/recovered.bin
```
- 涉及恢复文件时，不要继续往原分区写入。

## 5. 高风险误区
- 不要一上来就 `kill -9`
- 不要只杀单个 pid，忽略进程组/子进程
- 不要把 `history` 当唯一证据
- 不要认为 `ps/top` 看不到就一定不存在
- 不要先删样本再做哈希/取证
- 不要忽视隐藏文件和点目录

## 6. 善后与扩面
重点拉清单：
- 同密码服务器
- 同漏洞/同服务服务器
- 同管理员维护服务器
- 可通过 SSH key 互信直达的服务器
- 与受害主机频繁交互的服务器

最低恢复动作：
- 改密 / 清理 SSH key
- 打补丁
- 限制监听地址
- 备份重要数据
