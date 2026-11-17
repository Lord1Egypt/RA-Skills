# 硬件要求与系统参数速查

## 硬件要求

| 项目 | 最低要求 | 推荐配置 |
|------|---------|---------|
| 内存 | 512MB | 4GB+ |
| 磁盘 | 11GB | 50GB+（SSD） |
| CPU | 1核 | 4核+ |

## 支持架构

x86_64、龙芯(LoongArch)、飞腾/鲲鹏(ARM64)、海光、兆芯等

## Linux 系统参数

### 内核参数（`/etc/sysctl.conf`）

```ini
kernel.shmmax = 68719476736
kernel.shmall = 4294967296
kernel.shmmni = 4096
kernel.sem = 250 32000 100 128
net.ipv4.ip_local_port_range = 1024 65535
net.core.rmem_default = 1048576
net.core.rmem_max = 4194304
net.core.wmem_default = 262144
net.core.wmem_max = 1048576
fs.file-max = 777216
```

应用：`sysctl -p`

### 资源限制（`/etc/security/limits.conf`）

```ini
kingbase soft nofile 102400
kingbase hard nofile 102400
kingbase soft nproc 102400
kingbase hard nproc 102400
```

### systemd 配置

确保 `/etc/systemd/logind.conf` 中设置：

```ini
RemoveIPC=no
```

### 创建专用用户

```bash
groupadd kingbase
useradd -g kingbase -m kingbase
echo "kingbase" | passwd --stdin kingbase
```

### 目录规划

```bash
# 安装目录
sudo mkdir -p /opt/Kingbase/ES
sudo chown -R kingbase:kingbase /opt/Kingbase

# 数据目录
sudo mkdir -p /data/kingbase/data
sudo chown -R kingbase:kingbase /data/kingbase
```

## Windows 系统要求

- 以管理员身份运行安装程序
- 默认安装路径：`C:\Kingbase\ES\V9`
- 推荐使用专用 Windows 用户账户运行数据库服务
