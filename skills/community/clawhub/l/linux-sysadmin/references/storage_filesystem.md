# 存储与文件系统管理

## 目录

- [1. 磁盘分区](#1-磁盘分区)
- [2. LVM 逻辑卷](#2-lvm-逻辑卷)
- [3. 文件系统](#3-文件系统)
- [4. RAID 管理](#4-raid-管理)
- [5. 网络存储](#5-网络存储)
- [6. Swap 与配额](#6-swap-与配额)
- [7. 常见故障排查](#7-常见故障排查)

---

## 1. 磁盘分区

### 1.1 查看磁盘信息

```bash
# 查看所有块设备
lsblk -f                # 含文件系统类型和挂载点
lsblk -o NAME,SIZE,TYPE,FSTYPE,MOUNTPOINT,UUID

# 查看分区表
fdisk -l                # 所有磁盘
fdisk -l /dev/sda       # 指定磁盘

# 查看磁盘使用情况
df -hT                  # 含文件系统类型
du -sh /var/log/*       # 目录大小
```

### 1.2 MBR 分区（fdisk，磁盘 < 2TB）

```bash
# 交互式分区
fdisk /dev/sdb
# n → 新建分区
# p → 主分区（最多 4 个）/ e → 扩展分区
# 输入分区号、起始扇区、大小（如 +10G）
# w → 写入并退出

# 非交互式创建分区（脚本化）
echo -e "n\np\n1\n\n+10G\nw" | fdisk /dev/sdb

# 通知内核重新读取分区表
partprobe /dev/sdb
```

### 1.3 GPT 分区（gdisk/parted，磁盘 >= 2TB）

```bash
# gdisk（交互式）
gdisk /dev/sdb
# n → 新建分区
# 输入分区号、起始扇区、结束扇区（如 +10G）
# 选择分区类型（8300=Linux filesystem，8e00=Linux LVM）
# w → 写入

# parted（支持脚本化，推荐）
parted /dev/sdb mklabel gpt
parted /dev/sdb mkpart primary ext4 0% 50%
parted /dev/sdb mkpart primary xfs 50% 100%
parted /dev/sdb print
```

---

## 2. LVM 逻辑卷

### 2.1 基本概念

```text
物理卷 (PV) → 卷组 (VG) → 逻辑卷 (LV) → 文件系统
/dev/sdb    → vg_data   → lv_data     → ext4/xfs
/dev/sdc    ↗            → lv_logs     → xfs
```

### 2.2 创建 LVM

```bash
# 1. 创建物理卷
pvcreate /dev/sdb /dev/sdc

# 2. 创建卷组
vgcreate vg_data /dev/sdb /dev/sdc

# 3. 创建逻辑卷
lvcreate -L 50G -n lv_data vg_data       # 指定大小
lvcreate -l 100%FREE -n lv_logs vg_data  # 使用剩余全部空间

# 4. 创建文件系统
mkfs.ext4 /dev/vg_data/lv_data
mkfs.xfs /dev/vg_data/lv_logs

# 5. 挂载
mkdir -p /data /logs
mount /dev/vg_data/lv_data /data
mount /dev/vg_data/lv_logs /logs
```

### 2.3 扩展 LVM（在线扩容）

```bash
# 场景：/data 空间不足，添加新磁盘扩容

# 1. 创建新 PV
pvcreate /dev/sdd

# 2. 扩展 VG
vgextend vg_data /dev/sdd

# 3. 扩展 LV
lvextend -L +50G /dev/vg_data/lv_data       # 增加 50G
# 或
lvextend -l +100%FREE /dev/vg_data/lv_data   # 使用全部剩余空间

# 4. 扩展文件系统（在线，无需卸载）
resize2fs /dev/vg_data/lv_data   # ext4
xfs_growfs /data                  # xfs（使用挂载点）

# 5. 验证
df -h /data
```

### 2.4 缩小 LVM（⚠️ 有风险，需备份）

```bash
# 注意：xfs 不支持缩小！只有 ext4 支持

# 1. 备份数据
tar czf /tmp/data_backup.tar.gz /data/

# 2. 卸载文件系统
umount /data

# 3. 检查文件系统
e2fsck -f /dev/vg_data/lv_data

# 4. 缩小文件系统（先缩文件系统）
resize2fs /dev/vg_data/lv_data 30G

# 5. 缩小 LV（再缩逻辑卷，大小 >= 文件系统）
lvreduce -L 30G /dev/vg_data/lv_data

# 6. 重新挂载
mount /dev/vg_data/lv_data /data
```

### 2.5 LVM 快照

```bash
# 创建快照（需要 VG 有剩余空间）
lvcreate -L 5G -s -n lv_data_snap /dev/vg_data/lv_data

# 挂载快照（只读）
mkdir /mnt/snapshot
mount -o ro /dev/vg_data/lv_data_snap /mnt/snapshot

# 从快照恢复
umount /data
lvconvert --merge /dev/vg_data/lv_data_snap
mount /dev/vg_data/lv_data /data

# 删除快照
lvremove /dev/vg_data/lv_data_snap
```

### 2.6 LVM 常用查看命令

```bash
pvs          # 物理卷摘要
pvdisplay    # 物理卷详情
vgs          # 卷组摘要
vgdisplay    # 卷组详情
lvs          # 逻辑卷摘要
lvdisplay    # 逻辑卷详情
```

---

## 3. 文件系统

### 3.1 创建文件系统

```bash
# ext4（通用，支持缩小）
mkfs.ext4 /dev/sdb1
mkfs.ext4 -L "data" /dev/sdb1   # 带标签

# xfs（高性能，大文件，不支持缩小）
mkfs.xfs /dev/sdb1
mkfs.xfs -L "data" /dev/sdb1

# btrfs（快照、压缩、子卷）
mkfs.btrfs /dev/sdb1
mkfs.btrfs -L "data" /dev/sdb1
```

### 3.2 挂载与 fstab

```bash
# 临时挂载
mount /dev/sdb1 /mnt/data
mount -o noatime,discard /dev/sdb1 /mnt/data   # SSD 优化选项

# 查看 UUID（推荐用 UUID 而非设备名）
blkid /dev/sdb1

# /etc/fstab 配置（持久化挂载）
# <设备>                                  <挂载点>  <类型>  <选项>              <dump> <pass>
UUID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx /data     ext4    defaults,noatime    0      2
UUID=yyyyyyyy-yyyy-yyyy-yyyy-yyyyyyyyyyyy /logs     xfs     defaults,noatime    0      2

# 测试 fstab（不重启）
mount -a
# 如果报错，立即修复！否则重启后可能无法启动

# 常用挂载选项
# defaults     = rw,suid,dev,exec,auto,nouser,async
# noatime      = 不更新访问时间（提升性能）
# discard      = SSD TRIM 支持
# noexec       = 禁止执行（安全，适用于 /tmp）
# nosuid       = 忽略 SUID 位（安全）
# ro           = 只读
```

### 3.3 文件系统检查与修复

```bash
# ext4 检查（需先卸载）
umount /dev/sdb1
e2fsck -f /dev/sdb1
fsck -y /dev/sdb1      # 自动修复

# xfs 检查
umount /dev/sdb1
xfs_repair /dev/sdb1

# 查看文件系统信息
tune2fs -l /dev/sdb1   # ext4
xfs_info /dev/sdb1     # xfs

# 调整 ext4 预留空间（默认 5%，大磁盘可降低）
tune2fs -m 1 /dev/sdb1   # 预留 1%
```

---

## 4. RAID 管理

### 4.1 创建 RAID

```bash
# RAID 0（条带，性能优先，无冗余）
mdadm --create /dev/md0 --level=0 --raid-devices=2 /dev/sdb /dev/sdc

# RAID 1（镜像，数据安全，50% 容量）
mdadm --create /dev/md0 --level=1 --raid-devices=2 /dev/sdb /dev/sdc

# RAID 5（条带+奇偶校验，至少 3 盘，可坏 1 盘）
mdadm --create /dev/md0 --level=5 --raid-devices=3 /dev/sdb /dev/sdc /dev/sdd

# RAID 10（镜像+条带，至少 4 盘，兼顾性能和安全）
mdadm --create /dev/md0 --level=10 --raid-devices=4 /dev/sdb /dev/sdc /dev/sdd /dev/sde

# 保存配置
mdadm --detail --scan >> /etc/mdadm/mdadm.conf
update-initramfs -u   # Ubuntu
```

### 4.2 RAID 管理

```bash
# 查看 RAID 状态
cat /proc/mdstat
mdadm --detail /dev/md0

# 标记故障盘
mdadm /dev/md0 --fail /dev/sdc

# 移除故障盘
mdadm /dev/md0 --remove /dev/sdc

# 添加新盘（自动重建）
mdadm /dev/md0 --add /dev/sdf

# 监控 RAID
mdadm --monitor --mail=admin@example.com --delay=300 /dev/md0 &
```

---

## 5. 网络存储

### 5.1 NFS

```bash
# === 服务端 ===
apt install nfs-kernel-server   # Ubuntu
yum install nfs-utils           # RHEL

# 配置共享（/etc/exports）
/data/shared  252.227.81.0/24(rw,sync,no_subtree_check,no_root_squash)
/data/public  *(ro,sync,no_subtree_check)

# 生效
exportfs -ra
systemctl restart nfs-server

# === 客户端 ===
apt install nfs-common          # Ubuntu
yum install nfs-utils           # RHEL

# 临时挂载
mount -t nfs server:/data/shared /mnt/shared

# 持久化（/etc/fstab）
server:/data/shared  /mnt/shared  nfs  defaults,_netdev  0  0

# autofs 自动挂载（按需挂载，空闲自动卸载）
apt install autofs
# /etc/auto.master
/mnt  /etc/auto.nfs  --timeout=300
# /etc/auto.nfs
shared  -rw,soft  server:/data/shared
systemctl restart autofs
```

### 5.2 SMB/CIFS（Samba）

```bash
# === 服务端 ===
apt install samba

# 配置（/etc/samba/smb.conf）
# [shared]
#    path = /data/shared
#    browseable = yes
#    read only = no
#    valid users = @smbgroup

# 创建 Samba 用户
smbpasswd -a username

# 重启
systemctl restart smbd

# === 客户端 ===
apt install cifs-utils

# 临时挂载
mount -t cifs //server/shared /mnt/shared -o username=user,password=pass

# 持久化（使用凭据文件）
# /root/.smbcredentials
# username=user
# password=pass
# domain=WORKGROUP
chmod 600 /root/.smbcredentials

# /etc/fstab
//server/shared  /mnt/shared  cifs  credentials=/root/.smbcredentials,_netdev  0  0
```

---

## 6. Swap 与配额

### 6.1 Swap 管理

```bash
# 查看 Swap 状态
swapon --show
free -h

# 创建 Swap 文件
fallocate -l 4G /swapfile        # 或 dd if=/dev/zero of=/swapfile bs=1M count=4096
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile

# 持久化（/etc/fstab）
/swapfile  none  swap  sw  0  0

# 调整 swappiness
sysctl -w vm.swappiness=10       # 临时
echo "vm.swappiness=10" >> /etc/sysctl.d/99-swap.conf   # 持久化

# zram 压缩内存（替代传统 Swap）
modprobe zram
echo lz4 > /sys/block/zram0/comp_algorithm
echo 2G > /sys/block/zram0/disksize
mkswap /dev/zram0
swapon -p 100 /dev/zram0   # 优先级高于磁盘 Swap
```

### 6.2 磁盘配额

```bash
# 启用配额（ext4）
# /etc/fstab 挂载选项添加 usrquota,grpquota
UUID=xxx  /data  ext4  defaults,usrquota,grpquota  0  2
mount -o remount /data
quotacheck -cugm /data
quotaon /data

# 设置用户配额
edquota -u username
# 或命令行方式（软限制 5G，硬限制 6G）
setquota -u username 5242880 6291456 0 0 /data

# xfs 配额
# /etc/fstab 挂载选项添加 uquota,gquota
xfs_quota -x -c "limit bsoft=5g bhard=6g username" /data

# 查看配额使用情况
repquota -a          # 所有分区
quota -u username    # 指定用户
```

---

## 7. 常见故障排查

### 磁盘空间不足

```bash
# 1. 找出大目录
du -sh /* 2>/dev/null | sort -rh | head -10
du -sh /var/log/* | sort -rh | head -10

# 2. 查找大文件
find / -type f -size +100M 2>/dev/null | head -20

# 3. 查找已删除但未释放的文件
lsof | grep deleted | sort -k7 -rn | head -10
# 重启对应进程可释放空间

# 4. 清理日志
journalctl --vacuum-size=500M
find /var/log -name "*.gz" -mtime +30 -delete

# 5. 清理包缓存
apt clean          # Ubuntu
yum clean all      # RHEL
```

### LVM 扩容后文件系统未扩展

```bash
# 检查 LV 和文件系统大小
lvs
df -h

# ext4 在线扩展
resize2fs /dev/vg_data/lv_data

# xfs 在线扩展
xfs_growfs /mountpoint
```

### 无法挂载文件系统

```bash
# 1. 检查文件系统类型
blkid /dev/sdb1

# 2. 检查文件系统完整性
fsck -n /dev/sdb1   # 只检查不修复

# 3. 检查 fstab 语法
mount -a 2>&1

# 4. 检查设备是否存在
ls -la /dev/sdb1
lsblk
```
