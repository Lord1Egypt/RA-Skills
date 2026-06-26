# 用户权限

## 用户管理

```bash
whoami                      # 当前用户
id                          # 用户信息
id username                 # 指定用户信息
cat /etc/passwd             # 所有用户

# 创建用户
useradd username
useradd -m -s /bin/bash username   # 创建 home，指定 shell
adduser username            # 交互式创建

# 删除用户
userdel username
userdel -r username         # 同时删除 home

# 修改密码
passwd
passwd username
```

## 组管理

```bash
groups                      # 当前用户组
groups username             # 指定用户组
cat /etc/group              # 所有组

groupadd groupname
groupdel groupname
gpasswd -a user group       # 添加用户到组
gpasswd -d user group       # 从组删除用户
```

## 权限管理

```bash
ls -la                      # 查看权限

# 修改权限
chmod 755 file
chmod +x file
chmod -R 755 directory/

# 修改所有者
chown user file
chown user:group file
chown -R user:group directory/

# ACL
getfacl file
setfacl -m u:user:rwx file
setfacl -x u:user file
```

## sudo

```bash
# 添加到 sudo 组
usermod -aG sudo username   # Debian/Ubuntu
usermod -aG wheel username  # CentOS/RHEL

# /etc/sudoers
username ALL=(ALL) NOPASSWD: ALL
```
