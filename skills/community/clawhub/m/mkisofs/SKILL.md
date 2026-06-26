# Mkisofs Skill - ISO 镜像创建

## 技能描述 | Skill Description

**名称 | Name:** mkisofs  
**版本 | Version:** 1.0.0  
**作者 | Author:** OS Build Agent  
**领域 | Domain:** ISO 9660 Image Creation  

专业的 ISO 镜像创建和管理技能，支持 mkisofs/genisoimage/xorriso 等工具，用于创建可启动和不可启动的 ISO 镜像。

Professional ISO image creation and management skill supporting mkisofs/genisoimage/xorriso tools for creating bootable and non-bootable ISO images.

---

## 功能列表 | Features

### 1. ISO 创建 | ISO Creation
- 创建标准 ISO | Create standard ISO
- 创建可启动 ISO | Create bootable ISO
- 创建 UEFI 启动 ISO | Create UEFI bootable ISO
- 创建混合 ISO | Create hybrid ISO
- 多启动镜像支持 | Multi-boot image support

### 2. 文件系统 | Filesystem
- ISO 9660 支持 | ISO 9660 support
- Joliet 扩展 | Joliet extensions
- Rock Ridge 扩展 | Rock Ridge extensions
- UDF 支持 | UDF support

### 3. 启动配置 | Boot Configuration
- El Torito 启动 | El Torito boot
- ISOLINUX 配置 | ISOLINUX config
- GRUB2 集成 | GRUB2 integration
- 混合 MBR/GPT | Hybrid MBR/GPT

### 4. 镜像操作 | Image Operations
- 镜像信息查看 | View image info
- 镜像挂载 | Mount image
- 镜像提取 | Extract image
- 镜像修改 | Modify image

### 5. 验证测试 | Verification
- 启动测试 | Boot test
- 完整性校验 | Integrity check
- 兼容性测试 | Compatibility test

---

## 配置 | Configuration

### 工具安装 | Tool Installation

```bash
# RHEL/Fedora
dnf install mkisofs xorriso isolinux

# openSUSE
zypper install mkisofs xorriso isolinux

# Debian/Ubuntu
apt-get install mkisofs xorriso isolinux
```

### 常用目录结构 | Common Directory Structure

```
iso_root/
├── isolinux/
│   ├── isolinux.bin      # ISOLINUX 引导程序
│   ├── isolinux.cfg      # ISOLINUX 配置
│   └── boot.cat         # 启动目录表
├── images/
│   ├── efiboot.img      # UEFI 启动镜像
│   └── hdboot.img       # 硬盘启动镜像
├── packages/            # RPM/DEB 包
├── docs/                # 文档
└── README.txt           # 说明文件
```

---

## 使用示例 | Usage Examples

### 基本 ISO 创建 | Basic ISO Creation

```bash
# 创建标准 ISO 镜像
# Create standard ISO image
mkisofs -o output.iso /path/to/source

# 创建带卷标的 ISO
# Create ISO with volume label
mkisofs -o output.iso \
  -V "MY_VOLUME" \
  /path/to/source

# 创建带 Joliet 支持的 ISO (Windows 兼容)
# Create ISO with Joliet support (Windows compatible)
mkisofs -o output.iso \
  -J \
  -V "MY_VOLUME" \
  /path/to/source

# 创建带 Rock Ridge 支持的 ISO (Unix 兼容)
# Create ISO with Rock Ridge support (Unix compatible)
mkisofs -o output.iso \
  -R \
  -V "MY_VOLUME" \
  /path/to/source

# 创建完全兼容的 ISO (Joliet + Rock Ridge)
# Create fully compatible ISO (Joliet + Rock Ridge)
mkisofs -o output.iso \
  -J -R \
  -V "MY_VOLUME" \
  -allow-lowercase \
  /path/to/source
```

### 可启动 ISO 创建 | Bootable ISO Creation

```bash
# 创建 ISOLINUX 启动 ISO
# Create ISOLINUX bootable ISO
mkisofs -o bootable.iso \
  -J -R \
  -V "BOOT_ISO" \
  -b isolinux/isolinux.bin \
  -c isolinux/boot.cat \
  -no-emul-boot \
  -boot-load-size 4 \
  -boot-info-table \
  -isolinux-dir isolinux \
  /path/to/iso_root

# 创建 UEFI 启动 ISO
# Create UEFI bootable ISO
mkisofs -o uefi.iso \
  -J -R \
  -V "UEFI_ISO" \
  -b images/efiboot.img \
  -no-emul-boot \
  -boot-load-size 1 \
  -boot-info-table \
  /path/to/iso_root

# 创建 BIOS+UEFI 混合启动 ISO
# Create BIOS+UEFI hybrid bootable ISO
mkisofs -o hybrid.iso \
  -J -R \
  -V "HYBRID_ISO" \
  -b isolinux/isolinux.bin \
  -c isolinux/boot.cat \
  -no-emul-boot \
  -boot-load-size 4 \
  -boot-info-table \
  -eltorito-alt-boot \
  -b images/efiboot.img \
  -no-emul-boot \
  /path/to/iso_root
```

### 使用 xorriso 创建 ISO | Create ISO with xorriso

```bash
# 基本创建
# Basic creation
xorriso -as mkisofs \
  -o output.iso \
  -V "MY_VOLUME" \
  /path/to/source

# 创建可启动 ISO
# Create bootable ISO
xorriso -as mkisofs \
  -o bootable.iso \
  -b isolinux/isolinux.bin \
  -c isolinux/boot.cat \
  -no-emul-boot \
  -boot-load-size 4 \
  -boot-info-table \
  /path/to/iso_root

# 创建混合 ISO (支持 USB 启动)
# Create hybrid ISO (USB bootable)
xorriso -as mkisofs \
  -o hybrid.iso \
  -isohybrid-mbr /usr/share/syslinux/isohdpfx.bin \
  -b isolinux/isolinux.bin \
  -c isolinux/boot.cat \
  -no-emul-boot \
  -boot-load-size 4 \
  -boot-info-table \
  -eltorito-alt-boot \
  -b images/efiboot.img \
  -no-emul-boot \
  -isohybrid-gpt-basdat \
  /path/to/iso_root
```

### ISOLINUX 配置 | ISOLINUX Configuration

```bash
# isolinux.cfg 示例
# isolinux.cfg example
cat > isolinux/isolinux.cfg << 'EOF'
DEFAULT linux
LABEL linux
  MENU LABEL Boot System
  KERNEL vmlinuz
  APPEND initrd=initrd.img root=live:CDLABEL=MY_VOLUME
  LABEL rescue
  MENU LABEL Rescue Mode
  KERNEL vmlinuz
  APPEND initrd=initrd.img rescue
TIMEOUT 600
PROMPT 1
EOF
```

### GRUB2 启动配置 | GRUB2 Boot Configuration

```bash
# 创建 GRUB2 启动 ISO
# Create GRUB2 bootable ISO
mkisofs -o grub2.iso \
  -J -R \
  -V "GRUB2_ISO" \
  -b boot/grub/i386-pc/eltorito.img \
  -no-emul-boot \
  -boot-load-size 4 \
  -boot-info-table \
  -eltorito-alt-boot \
  -b boot/grub/efi.img \
  -no-emul-boot \
  /path/to/iso_root

# grub.cfg 示例
# grub.cfg example
cat > boot/grub/grub.cfg << 'EOF'
set timeout=5
menuentry "Boot System" {
  linux /vmlinuz root=live:CDLABEL=MY_VOLUME
  initrd /initrd.img
}
menuentry "Rescue Mode" {
  linux /vmlinuz rescue
  initrd /initrd.img
}
EOF
```

### 镜像操作 | Image Operations

```bash
# 查看 ISO 信息
# View ISO info
isoinfo -d -i output.iso

# 列出 ISO 内容
# List ISO contents
isoinfo -l -i output.iso

# 挂载 ISO
# Mount ISO
mount -o loop output.iso /mnt/iso

# 提取 ISO 内容
# Extract ISO contents
xorriso -osirrox on -indev output.iso -extract / /path/to/extract

# 添加到现有 ISO
# Add to existing ISO
xorriso -indev input.iso -outdev output.iso \
  -add /path/to/new/file /new/file

# 从 ISO 删除文件
# Delete file from ISO
xorriso -indev input.iso -outdev output.iso \
  -rm /path/to/file

# 转换 ISO 格式
# Convert ISO format
xorriso -indev input.iso -outdev output.udf \
  -as udfformat
```

### 验证和测试 | Verification and Testing

```bash
# 检查 ISO 完整性
# Check ISO integrity
isoinfo -d -i output.iso

# 验证启动信息
# Verify boot info
isoinfo -l -i bootable.iso | grep -E "isolinux|boot"

# 检查文件大小
# Check file size
ls -lh output.iso

# 计算校验和
# Calculate checksum
sha256sum output.iso

# 测试挂载
# Test mount
mount -o loop,ro output.iso /mnt/test
ls /mnt/test
umount /mnt/test
```

---

## 高级用法 | Advanced Usage

### 多启动 ISO | Multi-boot ISO

```bash
# 创建多启动 ISO (多个启动镜像)
# Create multi-boot ISO (multiple boot images)
mkisofs -o multiboot.iso \
  -J -R \
  -V "MULTIBOOT" \
  -b isolinux/isolinux.bin \
  -c isolinux/boot.cat \
  -no-emul-boot \
  -boot-load-size 4 \
  -boot-info-table \
  -eltorito-alt-boot \
  -b images/efiboot.img \
  -no-emul-boot \
  -eltorito-alt-boot \
  -b images/hdboot.img \
  -no-emul-boot \
  /path/to/iso_root
```

### UDF 格式 ISO | UDF Format ISO

```bash
# 创建 UDF 格式 ISO (支持大文件)
# Create UDF format ISO (supports large files)
xorriso -as mkisofs \
  -o output.udf \
  -V "UDF_VOLUME" \
  -udf \
  /path/to/source

# 创建 ISO+UDF 混合格式
# Create ISO+UDF hybrid format
xorriso -as mkisofs \
  -o hybrid.iso \
  -V "HYBRID" \
  -iso-level 3 \
  -udf \
  /path/to/source
```

### 压缩 ISO | Compressed ISO

```bash
# 创建压缩 ISO (xz)
# Create compressed ISO (xz)
mkisofs -o - /path/to/source | xz > output.iso.xz

# 解压并挂载
# Decompress and mount
xzcat output.iso.xz | mount -o loop -t iso9660 /dev/stdin /mnt/iso
```

---

## 命令参考 | Command Reference

### mkisofs/genisoimage 选项 | Options

| 选项 | Option | 描述 | Description |
|------|--------|------|-------------|
| `-o` | output | 输出文件 | Output file |
| `-V` | volume-id | 卷标 | Volume label |
| `-J` | joliet | Joliet 扩展 | Joliet extensions |
| `-R` | rock-ridge | Rock Ridge 扩展 | Rock Ridge extensions |
| `-b` | boot-image | 启动镜像 | Boot image |
| `-c` | boot-catalog | 启动目录表 | Boot catalog |
| `-no-emul-boot` | no emulation | 无模拟启动 | No emulation boot |
| `-boot-load-size` | load size | 加载扇区数 | Load sectors |
| `-boot-info-table` | info table | 启动信息表 | Boot info table |
| `-eltorito-alt-boot` | alt boot | 备用启动 | Alternative boot |
| `-allow-lowercase` | lowercase | 允许小写 | Allow lowercase |

### xorriso 命令 | Commands

| 命令 | Command | 描述 | Description |
|------|---------|------|-------------|
| `-as mkisofs` | mkisofs mode | mkisofs 兼容模式 | mkisofs compatible |
| `-indev` | input device | 输入镜像 | Input image |
| `-outdev` | output device | 输出镜像 | Output image |
| `-add` | add | 添加文件 | Add files |
| `-rm` | remove | 删除文件 | Remove files |
| `-extract` | extract | 提取文件 | Extract files |
| `-osirrox on` | osirrox | 启用提取 | Enable extraction |

---

## 最佳实践 | Best Practices

### 1. 兼容性 | Compatibility
- 使用 Joliet+Rock Ridge 确保跨平台兼容
- Use Joliet+Rock Ridge for cross-platform compatibility
- 测试在不同系统上的挂载
- Test mounting on different systems

### 2. 启动测试 | Boot Testing
- 在虚拟机中测试启动
- Test boot in VM
- 验证 BIOS 和 UEFI 启动
- Verify both BIOS and UEFI boot

### 3. 文件大小 | File Size
- 对于>4GB 文件使用 UDF 格式
- Use UDF for files >4GB
- 考虑压缩大镜像
- Consider compressing large images

---

## 故障排除 | Troubleshooting

### 启动失败 | Boot Failed
```bash
# 检查启动文件是否存在
# Check if boot files exist
isoinfo -l -i bootable.iso | grep -E "isolinux|boot"

# 验证启动配置
# Verify boot configuration
cat isolinux/isolinux.cfg
```

### 挂载失败 | Mount Failed
```bash
# 检查文件系统类型
# Check filesystem type
file output.iso

# 尝试不同文件系统
# Try different filesystem
mount -t iso9660 -o loop output.iso /mnt
mount -t udf -o loop output.iso /mnt
```

---

## 参考资料 | References

- [mkisofs 手册 | mkisofs Manual](https://linux.die.net/man/8/mkisofs)
- [xorriso 文档 | xorriso Docs](https://www.gnu.org/software/xorriso/)
- [ISOLINUX 文档 | ISOLINUX Docs](https://wiki.syslinux.org/wiki/index.php/ISOLINUX)
- [El Torito 规范 | El Torito Spec](https://en.wikipedia.org/wiki/El_Torito_(CD-ROM_standard))

---

## 许可证 | License

MIT License

---

## 更新日志 | Changelog

### v1.0.0 (2026-03-23)
- 初始版本，完整的 ISO 创建支持
- Initial release with full ISO creation support
- 中英文双语文档
- Bilingual documentation (Chinese/English)
