# 用户与权限管理

## 目录

- [1. 用户管理](#1-用户管理)
- [2. 组管理](#2-组管理)
- [3. 密码策略](#3-密码策略)
- [4. 文件权限](#4-文件权限)
- [5. ACL 细粒度控制](#5-acl-细粒度控制)
- [6. sudo 配置](#6-sudo-配置)
- [7. 强制访问控制](#7-强制访问控制)
- [8. 常见故障排查](#8-常见故障排查)

---

## 1. 用户管理

### 1.1 创建用户

```bash
# 基本创建（含 home 目录和默认 shell）
useradd -m -s /bin/bash username

# 指定 UID、附加组、注释
useradd -m -s /bin/bash -u 1500 -G sudo,docker -c "John Doe" johndoe

# 创建系统用户（无 home 目录、无登录 shell，用于服务账户）
useradd -r -s /usr/sbin/nologin -d /nonexistent myservice
```

### 1.2 修改用户

```bash
# 修改用户名
usermod -l newname oldname

# 修改 home 目录（同时移动内容）
usermod -d /home/newhome -m username

# 添加到附加组（不影响现有组）
usermod -aG docker,sudo username

# 修改默认 shell
usermod -s /bin/zsh username

# 锁定/解锁账户
usermod -L username   # 锁定（密码前加 !）
usermod -U username   # 解锁

# 设置账户过期日期
usermod -e 2026-12-31 username
```

### 1.3 删除用户

```bash
# 删除用户（保留 home 目录）
userdel username

# 删除用户及 home 目录
userdel -r username

# 删除前检查用户进程
ps -u username
# 如有进程需先终止
pkill -u username
```

### 1.4 查询用户信息

```bash
# 查看用户详情
id username
finger username 2>/dev/null || getent passwd username

# 查看用户所属组
groups username

# 查看所有可登录用户
grep -v -E "nologin|/bin/false" /etc/passwd

# 查看当前登录用户
who -a
w

# 查看登录历史
last -20
lastlog
```

---

## 2. 组管理

```bash
# 创建组
groupadd developers
groupadd -g 2000 devops   # 指定 GID

# 删除组
groupdel developers

# 添加用户到组
gpasswd -a username developers

# 从组中移除用户
gpasswd -d username developers

# 查看组成员
getent group developers
# 或
grep "^developers:" /etc/group

# 修改文件的所属组
chgrp developers /opt/project
```

---

## 3. 密码策略

### 3.1 密码管理

```bash
# 设置/修改密码
passwd username

# 强制用户下次登录修改密码
passwd -e username
# 或
chage -d 0 username

# 查看密码过期信息
chage -l username

# 设置密码策略（最长90天、最短7天、提前14天警告）
chage -M 90 -m 7 -W 14 username
```

### 3.2 PAM 密码复杂度

```bash
# /etc/security/pwquality.conf（RHEL/CentOS）
minlen = 12          # 最小长度
dcredit = -1         # 至少 1 个数字
ucredit = -1         # 至少 1 个大写字母
lcredit = -1         # 至少 1 个小写字母
ocredit = -1         # 至少 1 个特殊字符
maxrepeat = 3        # 最多连续重复 3 个字符
reject_username      # 不能包含用户名
enforce_for_root     # 对 root 也生效
```

### 3.3 登录失败锁定

```bash
# /etc/pam.d/common-auth（Ubuntu）或 /etc/pam.d/system-auth（RHEL）
# 在 pam_unix.so 之前添加：
auth required pam_faillock.so preauth silent audit deny=5 unlock_time=900
auth [default=die] pam_faillock.so authfail audit deny=5 unlock_time=900

# 查看锁定状态
faillock --user username

# 手动解锁
faillock --user username --reset
```

---

## 4. 文件权限

### 4.1 基本权限（rwx）

```bash
# 权限表示
# r=4  w=2  x=1
# rwxr-xr-x = 755
# rw-r--r-- = 644

# 修改权限
chmod 755 /opt/app/bin/server       # 数字模式
chmod u+x script.sh                 # 符号模式：所有者加执行权限
chmod g+w,o-r file.txt              # 组加写权限，其他人去读权限
chmod -R 750 /opt/app               # 递归修改

# 修改所有者
chown user:group file.txt
chown -R user:group /opt/app        # 递归修改
```

### 4.2 特殊权限（SUID/SGID/Sticky Bit）

```bash
# SUID（4）— 以文件所有者身份执行
chmod u+s /usr/bin/myapp     # 或 chmod 4755
# 典型例子：/usr/bin/passwd 需要 SUID 才能修改 /etc/shadow

# SGID（2）— 以文件所属组身份执行 / 目录下新文件继承组
chmod g+s /opt/shared        # 或 chmod 2775
# 目录设置 SGID 后，新创建的文件自动继承目录的组

# Sticky Bit（1）— 只有所有者能删除自己的文件
chmod +t /tmp                # 或 chmod 1777
# 典型例子：/tmp 目录设置 Sticky Bit 防止用户互删文件

# 查找 SUID/SGID 文件（安全审计）
find / -perm /4000 -type f 2>/dev/null   # SUID 文件
find / -perm /2000 -type f 2>/dev/null   # SGID 文件
```

### 4.3 umask

```bash
# 查看当前 umask
umask          # 如 0022
umask -S       # 如 u=rwx,g=rx,o=rx

# 设置 umask
umask 027      # 新文件 640，新目录 750

# 持久化（写入 profile）
echo "umask 027" >> /etc/profile.d/umask.sh
```

### 4.4 文件属性（chattr）

```bash
# 设置不可修改（即使 root 也不能修改/删除）
chattr +i /etc/resolv.conf

# 设置仅追加（日志文件常用）
chattr +a /var/log/audit.log

# 查看文件属性
lsattr /etc/resolv.conf

# 移除属性
chattr -i /etc/resolv.conf
```

---

## 5. ACL 细粒度控制

```bash
# 查看 ACL
getfacl /opt/project

# 设置用户 ACL
setfacl -m u:johndoe:rwx /opt/project

# 设置组 ACL
setfacl -m g:developers:rx /opt/project

# 设置默认 ACL（新文件自动继承）
setfacl -d -m u:johndoe:rwx /opt/project
setfacl -d -m g:developers:rx /opt/project

# 递归设置 ACL
setfacl -R -m u:johndoe:rwx /opt/project

# 移除特定 ACL
setfacl -x u:johndoe /opt/project

# 移除所有 ACL
setfacl -b /opt/project

# 备份和恢复 ACL
getfacl -R /opt/project > acl_backup.txt
setfacl --restore=acl_backup.txt
```

---

## 6. sudo 配置

### 6.1 基本配置

```bash
# 始终使用 visudo 编辑（会做语法检查）
visudo

# 或编辑独立文件（推荐，便于管理）
visudo -f /etc/sudoers.d/developers
```

### 6.2 常用配置示例

```bash
# /etc/sudoers.d/developers

# 用户 johndoe 可以执行所有命令
johndoe ALL=(ALL) ALL

# 用户 johndoe 免密执行所有命令
johndoe ALL=(ALL) NOPASSWD: ALL

# 组 developers 可以重启 nginx 和查看日志
%developers ALL=(ALL) NOPASSWD: /usr/bin/systemctl restart nginx, \
                                /usr/bin/journalctl -u nginx*

# 用户 deployer 只能以 www-data 身份执行部署脚本
deployer ALL=(www-data) NOPASSWD: /opt/deploy/deploy.sh

# 命令别名（批量授权）
Cmnd_Alias NETWORK_CMDS = /usr/sbin/iptables, /usr/sbin/ip, /usr/bin/ss
%netadmins ALL=(ALL) NOPASSWD: NETWORK_CMDS

# 禁止某些危险命令
johndoe ALL=(ALL) ALL, !/usr/bin/su, !/usr/bin/bash, !/usr/bin/sh
```

### 6.3 sudo 审计

```bash
# 查看 sudo 日志
grep sudo /var/log/auth.log     # Ubuntu/Debian
grep sudo /var/log/secure       # RHEL/CentOS

# 启用详细审计（/etc/sudoers）
Defaults logfile="/var/log/sudo.log"
Defaults log_input, log_output
Defaults iolog_dir="/var/log/sudo-io/%{user}"
```

---

## 7. 强制访问控制

### 7.1 SELinux（RHEL/CentOS）

```bash
# 查看状态
getenforce               # Enforcing / Permissive / Disabled
sestatus                  # 详细状态

# 临时切换模式
setenforce 0              # 切换到 Permissive（不重启）
setenforce 1              # 切换到 Enforcing

# 持久化修改（需重启）
# 编辑 /etc/selinux/config
# SELINUX=enforcing|permissive|disabled

# 查看文件上下文
ls -Z /var/www/html/
# -rw-r--r--. root root system_u:object_r:httpd_sys_content_t:s0 index.html

# 修改文件上下文
semanage fcontext -a -t httpd_sys_content_t "/opt/myapp(/.*)?"
restorecon -Rv /opt/myapp

# 查看/修改布尔值
getsebool -a | grep httpd
setsebool -P httpd_can_network_connect on   # -P 持久化

# 查看 SELinux 拒绝日志
ausearch -m AVC -ts recent
# 或
sealert -a /var/log/audit/audit.log

# 生成自定义策略
audit2allow -a -M mypolicy
semodule -i mypolicy.pp
```

### 7.2 AppArmor（Ubuntu/Debian）

```bash
# 查看状态
aa-status

# 将配置文件切换到 complain 模式（只记录不阻止）
aa-complain /etc/apparmor.d/usr.sbin.nginx

# 切换到 enforce 模式
aa-enforce /etc/apparmor.d/usr.sbin.nginx

# 禁用某个配置文件
ln -s /etc/apparmor.d/usr.sbin.nginx /etc/apparmor.d/disable/
apparmor_parser -R /etc/apparmor.d/usr.sbin.nginx

# 查看日志
dmesg | grep apparmor
journalctl -k | grep apparmor
```

---

## 8. 常见故障排查

### 用户无法登录

```bash
# 1. 检查账户是否锁定
passwd -S username   # 第二字段 L=锁定 P=有密码 NP=无密码

# 2. 检查账户是否过期
chage -l username

# 3. 检查 shell 是否有效
getent passwd username | cut -d: -f7

# 4. 检查 PAM 配置
pam_tally2 --user=username 2>/dev/null || faillock --user username

# 5. 检查 SSH 配置（如果是远程登录）
grep -E "AllowUsers|DenyUsers|AllowGroups|DenyGroups" /etc/ssh/sshd_config
```

### 权限被拒绝

```bash
# 1. 检查基本权限
ls -la /path/to/file
namei -l /path/to/file   # 检查路径上每一级的权限

# 2. 检查 ACL
getfacl /path/to/file

# 3. 检查 SELinux
ls -Z /path/to/file
ausearch -m AVC -ts recent | grep /path/to/file

# 4. 检查 AppArmor
aa-status
dmesg | grep DENIED

# 5. 检查文件属性
lsattr /path/to/file
```

### sudo 不工作

```bash
# 1. 语法检查
visudo -c

# 2. 检查用户组
id username | grep sudo

# 3. 检查 sudoers.d 目录
ls -la /etc/sudoers.d/

# 4. 检查日志
tail -20 /var/log/auth.log   # Ubuntu
tail -20 /var/log/secure     # RHEL
```
