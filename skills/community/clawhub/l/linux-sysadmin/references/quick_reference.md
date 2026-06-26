# Linux Sysadmin 速查表与常见场景快速处理

> 本文档包含十二大模块的常用命令速查表和常见场景的快速处理模板。

## 目录

- [速查表](#速查表)
  - [用户与权限](#用户与权限)
  - [存储与文件系统](#存储与文件系统)
  - [网络配置](#网络配置)
  - [服务管理](#服务管理)
  - [防火墙与安全](#防火墙与安全)
  - [监控与日志](#监控与日志)
  - [备份与恢复](#备份与恢复)
  - [证书与 TLS](#证书与-tls)
  - [自动化编排（Ansible）](#自动化编排ansible)
  - [容器管理](#容器管理)
  - [IaC 基础设施即代码](#iac-基础设施即代码)
- [常见场景快速处理](#常见场景快速处理)

---

## 速查表

### 用户与权限

| 任务 | 命令 | 参考文档 |
|------|------|---------|
| 添加用户 | `useradd -m -s /bin/bash -G sudo username` | references/user_permission.md |
| 修改密码 | `passwd username` | references/user_permission.md |
| 锁定账户 | `usermod -L username` | references/user_permission.md |
| 配置 sudo | `visudo` 或编辑 `/etc/sudoers.d/` | references/user_permission.md |
| SSH 密钥部署 | `ssh-copy-id user@host` | references/ssh_management.md |
| 文件权限设置 | `chmod 750 dir && chown user:group dir` | references/user_permission.md |
| 设置 ACL | `setfacl -m u:user:rwx /path` | references/user_permission.md |

### 存储与文件系统

| 任务 | 命令 | 参考文档 |
|------|------|---------|
| 查看磁盘布局 | `lsblk -f && fdisk -l` | references/storage_filesystem.md |
| 创建分区 | `fdisk /dev/sdX` 或 `gdisk /dev/sdX` | references/storage_filesystem.md |
| 创建 LVM | `pvcreate → vgcreate → lvcreate` | references/storage_filesystem.md |
| 扩展 LV | `lvextend -L +10G /dev/vg/lv && resize2fs` | references/storage_filesystem.md |
| 挂载文件系统 | `mount /dev/sdX1 /mnt && 编辑 /etc/fstab` | references/storage_filesystem.md |
| 文件系统修复 | `fsck -y /dev/sdX1`（需卸载） | references/storage_filesystem.md |
| 创建 Swap | `mkswap /swapfile && swapon /swapfile` | references/storage_filesystem.md |

### 网络配置

| 任务 | 命令 | 参考文档 |
|------|------|---------|
| 配置 IP | `nmcli con mod eth0 ipv4.addresses 192.0.2.10/24` | references/network_config.md |
| 添加路由 | `ip route add 198.51.100.0/24 via 192.0.2.1` | references/network_config.md |
| 配置 DNS | 编辑 `/etc/resolv.conf` 或 `systemd-resolved` | references/network_config.md |
| Bond 聚合 | `nmcli con add type bond ...` | references/network_config.md |
| 网络诊断 | `ping/traceroute/mtr/dig/ss/tcpdump` | references/network_config.md |

### 服务管理

| 任务 | 命令 | 参考文档 |
|------|------|---------|
| 启动/停止服务 | `systemctl start/stop/restart svc` | references/systemd_services.md |
| 开机自启 | `systemctl enable svc` | references/systemd_services.md |
| 查看日志 | `journalctl -u svc -f --since "1h ago"` | references/systemd_services.md |
| 编写 unit 文件 | `/etc/systemd/system/myapp.service` | references/systemd_services.md |
| 定时任务 | `systemctl enable --now myapp.timer` | references/systemd_services.md |
| 安装软件包 | `apt install / yum install / dnf install` | references/systemd_services.md |

### 防火墙与安全

| 任务 | 命令 | 参考文档 |
|------|------|---------|
| 开放端口 | `firewall-cmd --add-port=8080/tcp --permanent` | references/firewall_security.md |
| 封禁 IP | `firewall-cmd --add-rich-rule='rule family=ipv4 source address=x.x.x.x reject'` | references/firewall_security.md |
| NAT 转发 | `iptables -t nat -A PREROUTING ...` | references/firewall_security.md |
| 查看规则 | `iptables -L -n -v --line-numbers` | references/firewall_security.md |
| 安全基线检查 | `bash scripts/security_audit.sh` | references/firewall_security.md |

### 监控与日志

| 任务 | 命令 | 参考文档 |
|------|------|---------|
| 实时系统监控 | `htop` / `glances` / `dstat -cdnm 5` | references/monitoring_logging.md |
| 查看历史性能 | `sar -u` / `sar -r` / `sar -d` | references/monitoring_logging.md |
| 查看服务日志 | `journalctl -u svc -f --since "1h ago"` | references/monitoring_logging.md |
| 按级别过滤日志 | `journalctl -p err` | references/monitoring_logging.md |
| 配置日志轮转 | 编辑 `/etc/logrotate.d/myapp` | references/monitoring_logging.md |
| 清理日志空间 | `journalctl --vacuum-size=500M` | references/monitoring_logging.md |
| 部署 Prometheus | 安装 node_exporter + prometheus | references/monitoring_logging.md |

### 备份与恢复

| 任务 | 命令 | 参考文档 |
|------|------|---------|
| 检查备份状态 | `bash scripts/backup_manager.sh status` | references/backup_recovery.md |
| rsync 增量备份 | `rsync -avz --link-dest=... src/ dst/` | references/backup_recovery.md |
| borg 创建备份 | `borg create repo::name /dirs` | references/backup_recovery.md |
| borg 恢复备份 | `borg extract repo::name` | references/backup_recovery.md |
| MySQL 全量备份 | `mysqldump --single-transaction` | references/backup_recovery.md |
| GRUB 引导修复 | chroot + `grub-install` + `update-grub` | references/backup_recovery.md |
| 文件系统修复 | `fsck -y /dev/sdX`（需卸载） | references/backup_recovery.md |

### 证书与 TLS

| 任务 | 命令 | 参考文档 |
|------|------|---------|
| 检查证书过期 | `bash scripts/cert_check.sh domain.com` | references/certificate_tls.md |
| 生成自签名证书 | `openssl req -x509 -newkey rsa:2048 ...` | references/certificate_tls.md |
| 申请 Let's Encrypt | `certbot --nginx -d domain.com` | references/certificate_tls.md |
| 证书自动续期 | `certbot renew --dry-run` | references/certificate_tls.md |
| 查看证书详情 | `openssl x509 -in cert.crt -text -noout` | references/certificate_tls.md |
| 验证证书链 | `openssl verify -CAfile ca.crt cert.crt` | references/certificate_tls.md |
| 远程检查证书 | `openssl s_client -connect host:443` | references/certificate_tls.md |

### 自动化编排（Ansible）

| 任务 | 命令 | 参考文档 |
|------|------|---------|
| 检查 Ansible 环境 | `bash scripts/ansible_check.sh env` | references/ansible_automation.md |
| 测试主机连通性 | `ansible all -m ping` | references/ansible_automation.md |
| 执行 Playbook | `ansible-playbook playbooks/site.yaml` | references/ansible_automation.md |
| Dry-run 预览 | `ansible-playbook site.yaml --check --diff` | references/ansible_automation.md |
| Vault 加密 | `ansible-vault encrypt secrets.yaml` | references/ansible_automation.md |
| 安装 Collection | `ansible-galaxy collection install community.general` | references/ansible_automation.md |
| Playbook 语法检查 | `ansible-playbook site.yaml --syntax-check` | references/ansible_automation.md |

### 容器管理

| 任务 | 命令 | 参考文档 |
|------|------|---------|
| 容器安全审计 | `bash scripts/container_audit.sh` | references/container_management.md |
| 运行容器 | `docker run -d --name app -p 8080:80 image` | references/container_management.md |
| 查看容器日志 | `docker logs -f --tail 100 app` | references/container_management.md |
| 进入容器 | `docker exec -it app /bin/sh` | references/container_management.md |
| Compose 部署 | `docker compose up -d` | references/container_management.md |
| 镜像构建 | `docker build -t app:v1 .` | references/container_management.md |
| 系统清理 | `docker system prune -a --volumes` | references/container_management.md |

### IaC 基础设施即代码

| 任务 | 命令 | 参考文档 |
|------|------|---------|
| Terraform 初始化 | `terraform init` | references/infrastructure_as_code.md |
| 预览变更 | `terraform plan -out=tfplan` | references/infrastructure_as_code.md |
| 应用变更 | `terraform apply tfplan` | references/infrastructure_as_code.md |
| 导入已有资源 | `terraform import resource.name id` | references/infrastructure_as_code.md |
| Packer 构建镜像 | `packer build .` | references/infrastructure_as_code.md |
| Vagrant 启动 | `vagrant up` | references/infrastructure_as_code.md |
| IaC 安全扫描 | `tfsec . && checkov -d .` | references/infrastructure_as_code.md |

---

## 常见场景快速处理

### 🔴 用户管理

```bash
# 创建用户（含 home 目录、默认 shell、附加组）
useradd -m -s /bin/bash -G sudo,docker username
passwd username

# 配置 SSH 密钥登录（详见 references/ssh_management.md）
su - username
mkdir -p ~/.ssh && chmod 700 ~/.ssh
# 将公钥写入 authorized_keys
echo "ssh-ed25519 AAAA..." >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys

# 配置 sudo 免密（详见 references/user_permission.md）
echo "username ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/username
chmod 440 /etc/sudoers.d/username
visudo -c  # 语法检查
```

### 🔴 磁盘扩容（LVM）

```bash
# 诊断
lsblk -f && df -hT && pvs && vgs && lvs

# LVM 在线扩容（详见 references/storage_filesystem.md）
# 1. 创建 PV
pvcreate /dev/sdb
# 2. 扩展 VG
vgextend vg_data /dev/sdb
# 3. 扩展 LV（+100% 剩余空间）
lvextend -l +100%FREE /dev/vg_data/lv_data
# 4. 扩展文件系统
resize2fs /dev/vg_data/lv_data   # ext4
# xfs_growfs /mountpoint          # xfs
```

### 🔴 网络配置

```bash
# 诊断
ip -br addr && ip route && cat /etc/resolv.conf

# 配置静态 IP（详见 references/network_config.md）
# nmcli 方式（推荐）
nmcli con mod "eth0" ipv4.method manual \
  ipv4.addresses "192.0.2.10/24" \
  ipv4.gateway "192.0.2.1" \
  ipv4.dns "203.0.113.1,203.0.113.2"
nmcli con up "eth0"

# 验证
ip addr show eth0 && ip route && ping -c 3 203.0.113.1
```

### 🔴 服务管理

```bash
# 诊断
systemctl status myapp
journalctl -u myapp --no-pager -n 50

# 创建 systemd 服务（详见 references/systemd_services.md）
cat > /etc/systemd/system/myapp.service << 'EOF'
[Unit]
Description=My Application
After=network.target

[Service]
Type=simple
User=myapp
WorkingDirectory=/opt/myapp
ExecStart=/opt/myapp/bin/server
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable --now myapp
systemctl status myapp
```

### 🔴 防火墙配置

```bash
# 诊断
firewall-cmd --state && firewall-cmd --list-all

# 开放端口（详见 references/firewall_security.md）
firewall-cmd --add-port=80/tcp --permanent
firewall-cmd --add-port=443/tcp --permanent
firewall-cmd --reload
firewall-cmd --list-ports

# 或 iptables 方式
iptables -A INPUT -p tcp --dport 80 -j ACCEPT
iptables -A INPUT -p tcp --dport 443 -j ACCEPT
iptables-save > /etc/iptables/rules.v4
```

### 🟡 SSH 加固

```bash
# 加固 sshd 配置（详见 references/ssh_management.md）
cp /etc/ssh/sshd_config /etc/ssh/sshd_config.bak.$(date +%Y%m%d)
cat > /etc/ssh/sshd_config.d/hardening.conf << 'EOF'
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
MaxAuthTries 3
ClientAliveInterval 300
ClientAliveCountMax 2
X11Forwarding no
AllowTcpForwarding no
EOF

sshd -t && systemctl reload sshd
```

### 🟡 监控部署

```bash
# 部署 Node Exporter（详见 references/monitoring_logging.md）
wget https://github.com/prometheus/node_exporter/releases/download/v1.8.2/node_exporter-1.8.2.linux-amd64.tar.gz
tar xzf node_exporter-1.8.2.linux-amd64.tar.gz
cp node_exporter-1.8.2.linux-amd64/node_exporter /usr/local/bin/

# 创建 systemd 服务并启动
cat > /etc/systemd/system/node_exporter.service << 'EOF'
[Unit]
Description=Prometheus Node Exporter
After=network.target
[Service]
Type=simple
User=nobody
ExecStart=/usr/local/bin/node_exporter --collector.systemd --collector.processes
Restart=on-failure
[Install]
WantedBy=multi-user.target
EOF
systemctl daemon-reload && systemctl enable --now node_exporter
curl -s http://localhost:9100/metrics | head -5
```

### 🟡 备份配置

```bash
# 使用备份管理脚本（详见 references/backup_recovery.md）
# 检查备份状态
bash scripts/backup_manager.sh status

# 执行备份
BACKUP_SRC="/etc /home /opt" BACKUP_DST="/backup" bash scripts/backup_manager.sh run

# 或使用 borgbackup 手动备份
borg init --encryption=repokey /backup/borg-repo
borg create --stats --compression lz4 \
  /backup/borg-repo::$(hostname)-$(date +%Y%m%d) \
  /etc /home /opt
borg prune --keep-daily=7 --keep-weekly=4 /backup/borg-repo
```

### 🟡 证书管理

```bash
# 检查证书过期时间（详见 references/certificate_tls.md）
bash scripts/cert_check.sh www.example.com api.example.com

# 申请 Let's Encrypt 证书
certbot --nginx -d www.example.com -d example.com

# 测试自动续期
certbot renew --dry-run

# 生成自签名证书（开发环境）
openssl req -x509 -newkey rsa:2048 -keyout server.key -out server.crt \
  -days 365 -nodes -subj "/CN=localhost"
```

### 🟡 Ansible 自动化

```bash
# 检查 Ansible 环境（详见 references/ansible_automation.md）
bash scripts/ansible_check.sh env

# 编写并执行 Playbook
cat > deploy.yaml << 'EOF'
---
- name: 部署 Web 服务器
  hosts: webservers
  become: yes
  tasks:
    - name: 安装 Nginx
      apt:
        name: nginx
        state: present
        update_cache: yes
    - name: 启动 Nginx
      service:
        name: nginx
        state: started
        enabled: yes
EOF
ansible-playbook -i inventory deploy.yaml --check --diff
ansible-playbook -i inventory deploy.yaml
```

### 🟡 容器管理

```bash
# 容器安全审计（详见 references/container_management.md）
bash scripts/container_audit.sh

# Docker Compose 部署
docker compose up -d
docker compose ps
docker compose logs -f

# 容器安全运行
docker run -d --name app \
  --user 1000:1000 \
  --read-only --tmpfs /tmp \
  --cap-drop=ALL \
  --security-opt=no-new-privileges \
  --memory=512m --cpus=1.0 \
  --restart=unless-stopped \
  myapp:v2.1.0
```

### 🟡 Terraform IaC

```bash
# Terraform 工作流（详见 references/infrastructure_as_code.md）
terraform init
terraform fmt -recursive
terraform validate
terraform plan -out=tfplan
terraform apply tfplan

# 导入已有资源
terraform import tencentcloud_instance.web ins-xxxxxxxx
```
