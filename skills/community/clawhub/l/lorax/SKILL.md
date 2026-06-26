# Lorax Skill - 系统镜像构建

## 技能描述 | Skill Description

**名称 | Name:** lorax  
**版本 | Version:** 1.0.0  
**作者 | Author:** OS Build Agent  
**领域 | Domain:** System Image Creation (Fedora/RHEL)  

专业的系统镜像构建技能，使用 Lorax 工具创建可启动的 ISO、 disk 镜像、云镜像等，支持 Anaconda 安装镜像和 Live 镜像。

Professional system image creation skill using Lorax tool to create bootable ISOs, disk images, cloud images, supporting Anaconda installer and Live images.

---

## 功能列表 | Features

### 1. ISO 镜像创建 | ISO Image Creation
- Anaconda 安装镜像 | Anaconda installer
- Live ISO 镜像 | Live ISO images
- 网络启动镜像 | Network boot images
- 自定义启动镜像 | Custom boot images

### 2. 磁盘镜像 | Disk Images
- QCOW2 镜像 | QCOW2 images
- VMDK 镜像 | VMDK images
- VDI 镜像 | VDI images
- 原始磁盘镜像 | Raw disk images
- 分区配置 | Partition configuration

### 3. 云镜像 | Cloud Images
- AWS AMI | AWS AMI
- Azure VHD | Azure VHD
- GCE tar.gz | GCE tar.gz
- OpenStack qcow2 | OpenStack qcow2

### 4. 模板系统 | Template System
- Lorax 模板 | Lorax templates
- 自定义模板 | Custom templates
- 模板变量 | Template variables
- 条件构建 | Conditional builds

### 5. 包管理 | Package Management
- 包选择 | Package selection
- 包组 | Package groups
- 自定义仓库 | Custom repositories
- 包排除 | Package exclusion

### 6. 启动配置 | Boot Configuration
- GRUB2 配置 | GRUB2 configuration
- ISOLINUX 配置 | ISOLINUX configuration
- 内核参数 | Kernel parameters
- 启动菜单 | Boot menu

---

## 配置 | Configuration

### 工具安装 | Tool Installation

```bash
# RHEL/Fedora
dnf install lorax lorax-templates-generic

# 可选工具 | Optional tools
dnf install virt-install virt-builder guestfs-tools
```

### 目录结构 | Directory Structure

```
/usr/share/lorax/
├── templates/           # 模板文件
│   ├── Fedora/         # Fedora 模板
│   └── RHEL/           # RHEL 模板
├── conf/               # 配置文件
└── logs/               # 日志文件

/var/tmp/lorax/         # 构建临时目录
```

---

## 使用示例 | Usage Examples

### 创建安装 ISO | Create Installer ISO

```bash
# 基本安装 ISO 创建
# Basic installer ISO creation
lorax \
  -p "Fedora" \
  -v "39" \
  -r "39" \
  -o "/var/tmp/lorax" \
  /path/to/repo

# 完整参数示例
# Full parameter example
lorax \
  -p "Fedora" \
  -v "39" \
  -r "39" \
  -o "/var/tmp/lorax" \
  --project "Fedora Project" \
  --release "Fedora 39" \
  --variant "Server" \
  --bugurl "https://bugzilla.redhat.com" \
  --isfinal \
  --installpkgs "fedora-release,systemd" \
  --excludepkgs "firewalld" \
  --macboot \
  /path/to/repo
```

### 创建 Live ISO | Create Live ISO

```bash
# 创建 Live ISO
# Create Live ISO
livemedia-creator \
  --make-iso \
  --iso-only \
  --iso-name "Fedora-Live-Workstation-x86_64-39.iso" \
  --project "Fedora" \
  --releasever "39" \
  --title "Fedora Live Workstation" \
  --extra-kernel-args "rhgb quiet" \
  --unionfs-config "NONE" \
  /path/to/ks/file

# 使用自动安装文件
# Using kickstart file
livemedia-creator \
  --make-iso \
  --iso-only \
  --ks "fedora-live.ks" \
  --project "Fedora" \
  --releasever "39" \
  --title "Fedora Live" \
  /path/to/repo
```

### 创建磁盘镜像 | Create Disk Images

```bash
# 创建 QCOW2 镜像
# Create QCOW2 image
virt-builder \
  --fedora-39 \
  --size 20G \
  --format qcow2 \
  --output "fedora-39.qcow2" \
  --install "fedora-release,systemd"

# 创建 VMDK 镜像
# Create VMDK image
virt-builder \
  --fedora-39 \
  --size 20G \
  --format vmdk \
  --output "fedora-39.vmdk"

# 创建多格式镜像
# Create multi-format image
virt-builder \
  --fedora-39 \
  --size 20G \
  --output "fedora-39" \
  --formats "qcow2,vmdk,vdi"
```

### 使用 Lorax 模板 | Use Lorax Templates

```bash
# 使用自定义模板
# Use custom template
lorax \
  -p "CustomOS" \
  -v "1.0" \
  -r "1.0" \
  -o "/var/tmp/lorax" \
  --templatedir "/path/to/templates" \
  --template "custom.tmpl" \
  /path/to/repo

# 模板变量
# Template variables
lorax \
  -p "CustomOS" \
  -v "1.0" \
  -r "1.0" \
  -o "/var/tmp/lorax" \
  --add-template-var "custom_var=value" \
  --add-template-var "another_var=value2" \
  /path/to/repo
```

### 自定义包选择 | Custom Package Selection

```bash
# 安装特定包
# Install specific packages
lorax \
  -p "Fedora" \
  -v "39" \
  -r "39" \
  -o "/var/tmp/lorax" \
  --installpkgs "fedora-release,systemd,grub2,kernel" \
  --installpkgs "gnome-desktop,firefox" \
  --excludepkgs "firewalld,postfix" \
  /path/to/repo

# 使用包组
# Use package groups
lorax \
  -p "Fedora" \
  -v "39" \
  -r "39" \
  -o "/var/tmp/lorax" \
  --installpkgs "@core,@standard" \
  --excludepkgs "@debugging" \
  /path/to/repo
```

### 云镜像创建 | Cloud Image Creation

```bash
# 创建 AWS AMI
# Create AWS AMI
virt-builder \
  --fedora-39 \
  --size 20G \
  --format qcow2 \
  --output "fedora-39-aws.qcow2" \
  --install "fedora-release,cloud-init,aws-cli" \
  --firstboot "/path/to/aws-config.sh"

# 创建 Azure VHD
# Create Azure VHD
virt-builder \
  --fedora-39 \
  --size 20G \
  --format vpc \
  --output "fedora-39-azure.vhd" \
  --install "fedora-release,cloud-init,WALinuxAgent"

# 创建 GCE 镜像
# Create GCE image
virt-builder \
  --fedora-39 \
  --size 20G \
  --format qcow2 \
  --output "fedora-39-gce.qcow2" \
  --install "fedora-release,cloud-init,google-compute-engine"

# 创建 OpenStack 镜像
# Create OpenStack image
virt-builder \
  --fedora-39 \
  --size 20G \
  --format qcow2 \
  --output "fedora-39-openstack.qcow2" \
  --install "fedora-release,cloud-init"
```

### Kickstart 文件示例 | Kickstart File Example

```bash
# fedora-live.ks 示例
# fedora-live.ks example
cat > fedora-live.ks << 'EOF'
# Platform
x86_64

# Language
lang en_US.UTF-8

# Keyboard
keyboard us

# Timezone
timezone UTC

# Root password
rootpw --plaintext password

# Bootloader
bootloader --location=mbr

# Partitioning
clearpart --all --initlabel
part / --fstype="ext4" --size=10000
part swap --size=2000

# Packages
%packages
@core
fedora-release
systemd
kernel
grub2
firefox
gnome-desktop
%end

# Post installation
%post
dnf update -y
%end
EOF
```

---

## 高级用法 | Advanced Usage

### 自定义 Lorax 模板 | Custom Lorax Template

```bash
# 创建自定义模板
# Create custom template
cat > /path/to/templates/custom.tmpl << 'EOF'
# 安装基本包
# Install base packages
installpkg fedora-release
installpkg systemd
installpkg kernel
installpkg grub2

# 安装桌面环境
# Install desktop environment
installpkg @gnome-desktop

# 创建目录
# Create directories
mkdir /etc/custom
mkdir /var/custom

# 复制文件
# Copy files
copy /path/to/config /etc/custom/config

# 运行命令
# Run commands
run ln -s /etc/custom/config /etc/config-link

# 设置启动项
# Setup boot
bootloader --append="rhgb quiet"
EOF

# 使用模板
# Use template
lorax \
  -p "CustomOS" \
  -v "1.0" \
  -r "1.0" \
  -o "/var/tmp/lorax" \
  --templatedir "/path/to/templates" \
  --template "custom.tmpl" \
  /path/to/repo
```

### 多架构构建 | Multi-architecture Build

```bash
# x86_64 架构
# x86_64 architecture
lorax \
  -p "Fedora" \
  -v "39" \
  -r "39" \
  -o "/var/tmp/lorax-x86_64" \
  --arch "x86_64" \
  /path/to/repo

# aarch64 架构
# aarch64 architecture
lorax \
  -p "Fedora" \
  -v "39" \
  -r "39" \
  -o "/var/tmp/lorax-aarch64" \
  --arch "aarch64" \
  /path/to/repo

# ppc64le 架构
# ppc64le architecture
lorax \
  -p "Fedora" \
  -v "39" \
  -r "39" \
  -o "/var/tmp/lorax-ppc64le" \
  --arch "ppc64le" \
  /path/to/repo
```

### 网络安装镜像 | Network Install Image

```bash
# 创建精简网络安装 ISO
# Create minimal network install ISO
lorax \
  -p "Fedora" \
  -v "39" \
  -r "39" \
  -o "/var/tmp/lorax-net" \
  --netboot-only \
  --installpkgs "anaconda,grub2,syslinux" \
  /path/to/repo
```

---

## 命令参考 | Command Reference

### Lorax 选项 | Lorax Options

| 选项 | Option | 描述 | Description |
|------|--------|------|-------------|
| `-p` | product | 产品名称 | Product name |
| `-v` | version | 版本号 | Version |
| `-r` | release | 发布号 | Release |
| `-o` | output | 输出目录 | Output directory |
| `--arch` | architecture | 目标架构 | Target architecture |
| `--installpkgs` | install packages | 安装包列表 | Packages to install |
| `--excludepkgs` | exclude packages | 排除包列表 | Packages to exclude |
| `--templatedir` | template dir | 模板目录 | Template directory |
| `--template` | template | 模板文件 | Template file |
| `--macboot` | mac boot | Mac 启动支持 | Mac boot support |

### livemedia-creator 选项 | Options

| 选项 | Option | 描述 | Description |
|------|--------|------|-------------|
| `--make-iso` | make ISO | 创建 ISO | Create ISO |
| `--make-disk` | make disk | 创建磁盘镜像 | Create disk image |
| `--iso-only` | ISO only | 仅 ISO | ISO only |
| `--ks` | kickstart | Kickstart 文件 | Kickstart file |
| `--title` | title | 镜像标题 | Image title |

### virt-builder 选项 | Options

| 选项 | Option | 描述 | Description |
|------|--------|------|-------------|
| `--format` | format | 镜像格式 | Image format |
| `--size` | size | 镜像大小 | Image size |
| `--output` | output | 输出文件 | Output file |
| `--install` | install | 安装包 | Install packages |
| `--firstboot` | firstboot | 首次启动脚本 | Firstboot script |

---

## 最佳实践 | Best Practices

### 1. 镜像优化 | Image Optimization
- 清理不必要的文件 | Clean unnecessary files
- 压缩镜像减小体积 | Compress images to reduce size
- 移除调试信息 | Remove debug info

### 2. 安全性 | Security
- 使用最新安全更新 | Use latest security updates
- 配置防火墙 | Configure firewall
- 设置强密码策略 | Set strong password policy

### 3. 测试验证 | Testing
- 在虚拟机中测试启动 | Test boot in VM
- 验证所有功能 | Verify all functions
- 检查日志文件 | Check log files

---

## 故障排除 | Troubleshooting

### 构建失败 | Build Failed
```bash
# 查看详细日志
# View detailed logs
cat /var/tmp/lorax/lorax.log

# 检查依赖
# Check dependencies
dnf deplist lorax

# 清理临时文件
# Clean temp files
rm -rf /var/tmp/lorax/*
```

### 启动失败 | Boot Failed
```bash
# 检查 GRUB 配置
# Check GRUB configuration
grep -r "menuentry" /boot/grub2/

# 验证内核
# Verify kernel
rpm -qa kernel

# 检查启动日志
# Check boot logs
journalctl -xb
```

---

## 参考资料 | References

- [Lorax 官方文档 | Lorax Official Docs](https://github.com/weldr/lorax)
- [Fedora 镜像指南 | Fedora Image Guide](https://fedoraproject.org/wiki/Fedora_Media_Server)
- [virt-builder 文档 | virt-builder Docs](https://libguestfs.org/virt-builder.1.html)
- [Kickstart 文档 | Kickstart Docs](https://docs.fedoraproject.org/en-US/fedora/f39/install-guide/install/Kickstart_Syntax_Reference/)

---

## 许可证 | License

MIT License

---

## 更新日志 | Changelog

### v1.0.0 (2026-03-23)
- 初始版本，完整的 Lorax 支持
- Initial release with full Lorax support
- 中英文双语文档
- Bilingual documentation (Chinese/English)
