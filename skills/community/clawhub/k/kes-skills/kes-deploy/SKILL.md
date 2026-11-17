---
name: kes-deploy
name_for_command: kes-deploy
description: KingbaseES ISO 安装部署指南。当用户提到 ISO 安装、静默安装、图形化安装、开发工具、ksql、KStudio、kconsole、kingbase.conf 配置、sys_hba.conf、Windows 安装、Linux 安装时，必须使用此技能。
---

# KingbaseES 安装部署指南

本技能指导用户完成 KingbaseES 的 ISO 安装部署和开发工具配置，涵盖 Linux/Windows 安装、静默安装、开发工具和基础配置。

> **Docker 部署** → 见 `kes-docker` 技能

## 环境准备

### 硬件要求

| 项目 | 最低要求 | 推荐配置 |
|------|---------|---------|
| 内存 | 512MB | 4GB+ |
| 磁盘 | 11GB | 50GB+（SSD） |
| CPU | 1核 | 4核+ |

### 支持架构

x86_64、龙芯(LoongArch)、飞腾/鲲鹏(ARM64)、海光、兆芯等

### 支持操作系统

- CentOS 7/8
- 银河麒麟 V10
- 统信UOS
- openEuler
- 凝思安全操作系统
- 麒麟信安
- Windows 7/10/11/Server 2008+

### Linux 系统参数调整

**内核参数**（`/etc/sysctl.conf`）：
```bash
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

**资源限制**（`/etc/security/limits.conf`）：
```bash
kingbase soft nofile 102400
kingbase hard nofile 102400
kingbase soft nproc 102400
kingbase hard nproc 102400
```

**RemoveIPC**：确保`/etc/systemd/logind.conf`中设置`RemoveIPC=no`

### 创建专用用户（Linux）

```bash
groupadd kingbase
useradd -g kingbase -m kingbase
echo "kingbase" | passwd --stdin kingbase
```

### 目录规划

```bash
sudo mkdir -p /opt/Kingbase/ES
sudo chown -R kingbase:kingbase /opt/Kingbase

sudo mkdir -p /data/kingbase/data
sudo chown -R kingbase:kingbase /data/kingbase
```

## ISO 安装 — Linux

### 安装前准备

```bash
mount -o loop KingbaseES_V9_xxx.iso /mnt
su - kingbase
cd /mnt
```

### 方式一：图形化安装

```bash
sh setup.sh -i swing
```

安装向导步骤：语言 → 许可协议 → 组件选择 → 安装路径 → 实例配置 → 确认安装

### 方式二：命令行交互安装

```bash
sh setup.sh -i console
```

### 方式三：静默安装（推荐用于自动化）

```bash
./setup.sh -i silent -f silent.cfg
```

**silent.cfg 配置示例**：
```ini
INSTALL_PATH=/opt/Kingbase/ES/V9
LICENSE_PATH=/path/to/license.dat
COMPONENTS=Server,Interface,KStudio,KDTS,DeployTool,KingbaseHA
CREATE_SHORTCUT=false
DB_USER=SYSTEM
DB_PASS=123456
DB_PASS2=123456
ENCODING_PARAM=UTF8
CASE_SENSITIVE_PARAM=0
BLOCK_SIZE_PARAM=8192
AUTHENTICATION_METHOD_PARAM=scram-sha-256
```

**组件说明**：
- `Server`：数据库服务器核心
- `Interface`：开发接口（JDBC/ODBC/Python等）
- `KStudio`：可视化开发工具
- `KDTS`：数据同步工具
- `DeployTool`：部署管理工具
- `KingbaseHA`：高可用组件

### 安装后检查

```bash
su - kingbase
export KINGBASE_HOME=/opt/Kingbase/ES/V9
export PATH=$KINGBASE_HOME/Server/bin:$PATH

kingbase -V
ksql -U SYSTEM -d test  # 执行: select version();
```

## ISO 安装 — Windows

### 安装要求

- 以**管理员身份**运行安装程序
- 默认安装路径：`C:\Kingbase\ES\V9`

### 安装方式

```cmd
# 图形化安装
setup.exe

# 命令行交互安装
setup.bat -i console

# 静默安装
setup.bat -i silent -f silent.cfg
```

**认证方法选项**：`scram-sha-256`、`scram-sm3`、`sm4`、`sm3`（后三者为国密算法）

### 安装后检查

```cmd
kingbase.exe -V
ksql -U SYSTEM -d test  -- 执行: select version();
```

## 开发工具

### ksql（命令行客户端）

KingbaseES 默认的命令行交互工具。

```bash
ksql -U USERNAME -d DATABASE -h HOST -p PORT

\q          # 退出
\l          # 列出数据库
\d          # 列出表
\d TABLE    # 查看表结构
\du         # 列出用户
\timing     # 开关计时
\copy       # 数据导入导出
```

### ksqlcmd

增强版命令行工具，支持更多格式化选项和脚本执行。

```bash
ksqlcmd -U USERNAME -d DATABASE -H HOST -P PORT -f script.sql
```

### KStudio（可视化开发工具）

KingbaseES 的集成开发环境：
- 数据库连接管理
- SQL编辑器（语法高亮、自动补全）
- 表设计器
- 数据导入导出
- 存储过程调试
- 性能分析

启动方式：
```bash
# Linux
$KINGBASE_HOME/KStudio/KStudio

# Windows
开始菜单 → Kingbase → KStudio
```

### kconsole（数据库管控工具）

用于数据库实例的全生命周期管理：
- 创建/删除数据库实例
- 启动/停止/重启数据库
- 监控数据库状态
- 配置参数调整

```bash
kconsole
```

## 配置文件

### kingbase.conf

主配置文件，位于数据目录。关键参数：

```ini
listen_addresses = '*'
port = 54321
max_connections = 100

shared_buffers = 4GB              # 建议物理内存的1/3
work_mem = 64MB
maintenance_work_mem = 1GB

wal_level = replica
max_wal_senders = 3
archive_mode = on
archive_command = 'cp %p /archive/%f'

logging_collector = on
log_directory = 'log'
log_filename = 'kingbase-%Y-%m-%d_%H%M%S.log'
log_statement = 'ddl'
log_min_duration_statement = 1000

effective_cache_size = 12GB       # 建议物理内存的3/4
random_page_cost = 1.1            # SSD设置为1.1
```

### sys_hba.conf

客户端认证配置，位于数据目录。

```ini
# TYPE  DATABASE  USER    ADDRESS       METHOD
local   all       all                   scram-sha-256
host    all       all     127.0.0.1/32  scram-sha-256
host    all       all     0.0.0.0/0     scram-sha-256
```

**认证方法**：
- `trust`：无条件信任（仅测试环境）
- `scram-sha-256`：默认密码认证
- `scram-sm3`：国密SM3密码认证
- `sm4`：国密SM4加密认证
- `sm3`：国密SM3认证
- `md5`：MD5密码认证
- `cert`：客户端证书认证
- `ident`：操作系统用户映射

修改后需重新加载：`SELECT sys_reload_conf();`

## 目录结构

```
/opt/Kingbase/ES/V9/
├── Server/
│   ├── bin/          # 可执行文件（kingbase, ksql等）
│   ├── lib/          # 库文件（libkci.so等）
│   └── include/      # 头文件
├── ClientTools/      # 客户端工具
├── Interface/        # 开发接口（JDBC/ODBC/Python/Go/Node.js）
├── KStudio/          # 可视化开发工具
├── SupTools/         # 辅助工具（KDTS/KDNavigator等）
├── install/          # 安装实例目录
├── doc/              # 文档
├── Uninstaller/      # 卸载程序
├── license.dat       # 授权文件
└── KESRealPro/       # 实时防护
```

## 卸载

### Linux

```bash
systemctl stop kingbase
$KINGBASE_HOME/Uninstaller/uninstall.sh
sudo rm -rf /opt/Kingbase/ES/V9
sudo userdel -r kingbase
```

### Windows

```cmd
C:\Kingbase\ES\V9\Uninstaller\uninstall.bat
```

## 常见问题

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| 安装时磁盘空间不足 | 空间不够 | 安装目录≥5GB，数据目录≥6GB |
| 图形化安装无法启动 | 未安装X11或DISPLAY未设置 | 使用 `setup.sh -i console` |
| 静默安装失败 | silent.cfg参数错误 | 检查参数名拼写和取值范围 |
| ksql连接被拒绝 | 端口未监听或sys_hba.conf限制 | 检查 `listen_addresses` |
| 国密认证无法连接 | 客户端/服务端认证方法不匹配 | 确保 METHOD 与客户端一致 |
| 安装后服务未启动 | 未勾选自动启动 | `systemctl start kingbase` |
| Windows安装权限不足 | 未以管理员身份运行 | 右键→"以管理员身份运行" |

## 相关技能

- **kes-docker** — Docker 容器化部署

## 参考文档

```
kes-deploy/
├── SKILL.md            # 本文件
├── ref/
│   └── hardware-requirements.md   # 硬件要求与系统参数速查
└── test-cases.md
```
