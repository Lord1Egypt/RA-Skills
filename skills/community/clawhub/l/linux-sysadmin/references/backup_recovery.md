# 备份与灾难恢复

## 目录

- [1. 备份策略规划](#1-备份策略规划)
- [2. rsync 同步备份](#2-rsync-同步备份)
- [3. borgbackup 去重备份](#3-borgbackup-去重备份)
- [4. restic 云端备份](#4-restic-云端备份)
- [5. 数据库备份](#5-数据库备份)
- [6. 系统镜像与快照](#6-系统镜像与快照)
- [7. 灾难恢复](#7-灾难恢复)
- [8. 备份验证与监控](#8-备份验证与监控)
- [9. 常见故障排查](#9-常见故障排查)

---

## 1. 备份策略规划

### 1.1 3-2-1 原则

```text
3 — 至少保留 3 份数据副本
2 — 存储在 2 种不同的介质上（本地磁盘 + 远程存储）
1 — 至少 1 份异地备份（不同机房/云区域）
```

### 1.2 备份类型

```text
全量备份（Full）     — 完整备份所有数据，恢复最快，但耗时耗空间
增量备份（Incremental）— 只备份上次备份后变化的数据，最省空间
差异备份（Differential）— 只备份上次全量备份后变化的数据，折中方案
```

### 1.3 RPO/RTO 规划

```text
RPO（Recovery Point Objective）— 可接受的最大数据丢失量
  - RPO = 0：实时同步（数据库主从复制、DRBD）
  - RPO = 1h：每小时增量备份
  - RPO = 24h：每天全量备份

RTO（Recovery Time Objective）— 可接受的最大恢复时间
  - RTO < 5min：热备切换（keepalived/HAProxy）
  - RTO < 1h：快照恢复/LVM 快照
  - RTO < 4h：备份文件恢复
```

### 1.4 推荐备份方案

```text
场景              推荐工具              策略
──────────────────────────────────────────────────
文件/目录备份      rsync + cron          每日增量同步
服务器完整备份     borgbackup            每日增量 + 去重 + 加密
云端/异地备份      restic + S3           每日增量 + 加密 + 多后端
MySQL 数据库      mysqldump/xtrabackup   每日全量 + binlog 增量
PostgreSQL        pg_dump/pg_basebackup  每日全量 + WAL 归档
系统级备份        LVM 快照 + dd          全盘镜像
配置文件备份      etckeeper/git          每次变更自动提交
```

---

## 2. rsync 同步备份

### 2.1 基本用法

```bash
# 本地同步
rsync -avz /data/ /backup/data/

# 远程同步（SSH）
rsync -avz -e ssh /data/ user@backup-server:/backup/data/

# 常用选项
# -a  归档模式（保留权限、时间戳、符号链接等）
# -v  详细输出
# -z  传输时压缩
# -P  显示进度 + 支持断点续传
# --delete  删除目标端多余的文件（镜像同步）
# --exclude  排除文件/目录
# --bwlimit  限制带宽（KB/s）

# 镜像同步（保持完全一致）
rsync -avz --delete /data/ user@backup:/backup/data/

# 排除特定文件
rsync -avz --exclude='*.log' --exclude='.cache' /data/ /backup/data/

# 限速（避免影响业务）
rsync -avz --bwlimit=10240 /data/ user@backup:/backup/data/  # 10MB/s

# 只同步特定文件类型
rsync -avz --include='*.conf' --include='*/' --exclude='*' /etc/ /backup/etc/
```

### 2.2 增量备份脚本

```bash
#!/usr/bin/env bash
# rsync 增量备份脚本（硬链接方式节省空间）

BACKUP_SRC="/data"
BACKUP_DST="/backup"
DATE=$(date +%Y%m%d_%H%M%S)
LATEST_LINK="${BACKUP_DST}/latest"

# 使用 --link-dest 实现增量备份（未变化的文件使用硬链接）
rsync -avz --delete \
  --link-dest="${LATEST_LINK}" \
  "${BACKUP_SRC}/" \
  "${BACKUP_DST}/${DATE}/"

# 更新 latest 链接
rm -f "${LATEST_LINK}"
ln -s "${BACKUP_DST}/${DATE}" "${LATEST_LINK}"

# 清理 30 天前的备份
find "${BACKUP_DST}" -maxdepth 1 -type d -mtime +30 -exec rm -rf {} +

echo "备份完成: ${BACKUP_DST}/${DATE}"
```

### 2.3 rsync daemon 模式

```bash
# 服务端配置 /etc/rsyncd.conf
cat > /etc/rsyncd.conf << 'EOF'
uid = nobody
gid = nogroup
use chroot = yes
max connections = 10
log file = /var/log/rsyncd.log

[backup]
path = /backup
comment = Backup Storage
read only = no
auth users = backupuser
secrets file = /etc/rsyncd.secrets
hosts allow = 10.0.0.0/24
EOF

# 密码文件
echo "backupuser:strongpassword" > /etc/rsyncd.secrets
chmod 600 /etc/rsyncd.secrets

# 启动
systemctl enable --now rsync

# 客户端使用
export RSYNC_PASSWORD="strongpassword"
rsync -avz /data/ backupuser@backup-server::backup/data/
```

---

## 3. borgbackup 去重备份

### 3.1 安装与初始化

```bash
# 安装
apt install borgbackup   # Ubuntu/Debian
yum install borgbackup   # RHEL（EPEL）
pip3 install borgbackup  # pip 安装

# 初始化仓库（本地）
borg init --encryption=repokey /backup/borg-repo

# 初始化仓库（远程 SSH）
borg init --encryption=repokey user@backup-server:/backup/borg-repo

# 加密模式说明：
# none       — 不加密
# repokey    — 密钥存在仓库中（推荐，需记住密码）
# keyfile    — 密钥存在本地文件中（更安全，需备份密钥文件）

# 导出密钥（重要！丢失密钥无法恢复数据）
borg key export /backup/borg-repo /root/borg-key-backup.txt
```

### 3.2 创建备份

```bash
# 创建备份
borg create --stats --progress \
  /backup/borg-repo::server1-{now:%Y%m%d-%H%M%S} \
  /etc /home /var/log /opt/myapp \
  --exclude '*.log.gz' \
  --exclude '/home/*/.cache'

# 查看备份列表
borg list /backup/borg-repo

# 查看备份详情
borg info /backup/borg-repo::server1-20260401-020000

# 查看备份中的文件
borg list /backup/borg-repo::server1-20260401-020000

# 查看备份中特定路径
borg list /backup/borg-repo::server1-20260401-020000 etc/nginx/
```

### 3.3 恢复数据

```bash
# 恢复到指定目录
cd /tmp/restore
borg extract /backup/borg-repo::server1-20260401-020000

# 恢复特定文件/目录
borg extract /backup/borg-repo::server1-20260401-020000 etc/nginx/nginx.conf

# 挂载备份（只读浏览）
mkdir /mnt/borg
borg mount /backup/borg-repo::server1-20260401-020000 /mnt/borg
# 浏览文件...
borg umount /mnt/borg
```

### 3.4 清理策略

```bash
# 按策略清理旧备份
borg prune --stats \
  --keep-daily=7 \      # 保留 7 天每日备份
  --keep-weekly=4 \     # 保留 4 周每周备份
  --keep-monthly=6 \    # 保留 6 个月每月备份
  --keep-yearly=2 \     # 保留 2 年每年备份
  /backup/borg-repo

# 释放磁盘空间（prune 后执行）
borg compact /backup/borg-repo

# 检查仓库完整性
borg check /backup/borg-repo
```

### 3.5 自动化备份脚本

```bash
#!/usr/bin/env bash
# borg 自动备份脚本

export BORG_REPO="user@backup-server:/backup/borg-repo"
export BORG_PASSPHRASE="your-strong-passphrase"

BACKUP_NAME="$(hostname)-$(date +%Y%m%d-%H%M%S)"
LOG_FILE="/var/log/borg-backup.log"

echo "=== 开始备份: $(date) ===" >> "$LOG_FILE"

# 创建备份
borg create --stats --compression lz4 \
  "${BORG_REPO}::${BACKUP_NAME}" \
  /etc /home /var/lib /opt \
  --exclude '/home/*/.cache' \
  --exclude '*.tmp' \
  --exclude '*.log.gz' \
  2>&1 >> "$LOG_FILE"

backup_exit=$?

# 清理旧备份
borg prune --stats \
  --keep-daily=7 \
  --keep-weekly=4 \
  --keep-monthly=6 \
  "${BORG_REPO}" \
  2>&1 >> "$LOG_FILE"

prune_exit=$?

# 压缩仓库
borg compact "${BORG_REPO}" 2>&1 >> "$LOG_FILE"

# 记录结果
if [ $backup_exit -eq 0 ] && [ $prune_exit -eq 0 ]; then
    echo "=== 备份成功: $(date) ===" >> "$LOG_FILE"
else
    echo "=== 备份异常（backup=$backup_exit, prune=$prune_exit）: $(date) ===" >> "$LOG_FILE"
    # 发送告警...
fi

unset BORG_PASSPHRASE
```

---

## 4. restic 云端备份

### 4.1 安装与初始化

```bash
# 安装
apt install restic   # Ubuntu/Debian
yum install restic   # RHEL（EPEL）

# 初始化仓库
# 本地
restic init --repo /backup/restic-repo

# S3（AWS/MinIO）
export AWS_ACCESS_KEY_ID="your-key"
export AWS_SECRET_ACCESS_KEY="your-secret"
restic init --repo s3:s3.amazonaws.com/my-backup-bucket

# SFTP
restic init --repo sftp:user@backup-server:/backup/restic-repo

# REST Server
restic init --repo rest:http://backup-server:8000/
```

### 4.2 创建与恢复备份

```bash
# 设置密码
export RESTIC_PASSWORD="your-strong-password"
export RESTIC_REPOSITORY="/backup/restic-repo"

# 创建备份
restic backup /etc /home /opt/myapp \
  --exclude='*.log.gz' \
  --exclude='.cache' \
  --tag server1 \
  --verbose

# 查看快照列表
restic snapshots
restic snapshots --tag server1

# 恢复
restic restore latest --target /tmp/restore
restic restore latest --target /tmp/restore --include /etc/nginx/

# 挂载浏览
mkdir /mnt/restic
restic mount /mnt/restic
# 在 /mnt/restic/snapshots/ 下浏览
fusermount -u /mnt/restic

# 比较两个快照
restic diff snapshot1 snapshot2
```

### 4.3 清理策略

```bash
# 按策略保留
restic forget \
  --keep-daily 7 \
  --keep-weekly 4 \
  --keep-monthly 12 \
  --keep-yearly 2 \
  --prune

# 检查仓库完整性
restic check
restic check --read-data   # 完整验证（耗时）
```

---

## 5. 数据库备份

### 5.1 MySQL/MariaDB

```bash
# === mysqldump（逻辑备份）===
# 全库备份
mysqldump -u root -p --all-databases --single-transaction \
  --routines --triggers --events \
  | gzip > /backup/mysql/full-$(date +%Y%m%d).sql.gz

# 指定数据库备份
mysqldump -u root -p --single-transaction mydb > /backup/mysql/mydb.sql

# 恢复
mysql -u root -p < /backup/mysql/full-20260401.sql
# 或
gunzip < /backup/mysql/full-20260401.sql.gz | mysql -u root -p

# === xtrabackup（物理备份，热备，推荐生产环境）===
# 安装
apt install percona-xtrabackup-80   # MySQL 8.0

# 全量备份
xtrabackup --backup --target-dir=/backup/mysql/full \
  --user=root --password=xxx

# 增量备份
xtrabackup --backup --target-dir=/backup/mysql/incr1 \
  --incremental-basedir=/backup/mysql/full \
  --user=root --password=xxx

# 恢复
xtrabackup --prepare --target-dir=/backup/mysql/full
xtrabackup --prepare --target-dir=/backup/mysql/full \
  --incremental-dir=/backup/mysql/incr1
systemctl stop mysql
xtrabackup --copy-back --target-dir=/backup/mysql/full
chown -R mysql:mysql /var/lib/mysql
systemctl start mysql

# === binlog 时间点恢复 ===
# 查看 binlog 列表
mysqlbinlog --list-logs
SHOW BINARY LOGS;

# 恢复到指定时间点
mysqlbinlog --stop-datetime="2026-04-01 12:00:00" \
  /var/lib/mysql/binlog.000001 | mysql -u root -p
```

### 5.2 PostgreSQL

```bash
# === pg_dump（逻辑备份）===
# 单库备份
pg_dump -U postgres mydb | gzip > /backup/pg/mydb-$(date +%Y%m%d).sql.gz

# 全库备份
pg_dumpall -U postgres | gzip > /backup/pg/all-$(date +%Y%m%d).sql.gz

# 自定义格式（支持并行恢复）
pg_dump -U postgres -Fc mydb > /backup/pg/mydb.dump

# 恢复
psql -U postgres mydb < /backup/pg/mydb.sql
pg_restore -U postgres -d mydb -j 4 /backup/pg/mydb.dump  # 4 并行

# === pg_basebackup（物理备份）===
pg_basebackup -U postgres -D /backup/pg/base \
  -Ft -z -P --wal-method=stream

# === WAL 归档（持续备份）===
# postgresql.conf
# archive_mode = on
# archive_command = 'cp %p /backup/pg/wal/%f'
# wal_level = replica

# 时间点恢复（PITR）
# 1. 恢复基础备份
# 2. 配置 recovery.conf / postgresql.conf
# recovery_target_time = '2026-04-01 12:00:00'
# restore_command = 'cp /backup/pg/wal/%f %p'
```

### 5.3 Redis

```bash
# RDB 快照备份
redis-cli BGSAVE
cp /var/lib/redis/dump.rdb /backup/redis/dump-$(date +%Y%m%d).rdb

# AOF 备份
redis-cli BGREWRITEAOF
cp /var/lib/redis/appendonly.aof /backup/redis/

# 恢复
systemctl stop redis
cp /backup/redis/dump-20260401.rdb /var/lib/redis/dump.rdb
chown redis:redis /var/lib/redis/dump.rdb
systemctl start redis
```

---

## 6. 系统镜像与快照

### 6.1 LVM 快照备份

```bash
# 创建快照（需要 VG 有剩余空间）
lvcreate -L 5G -s -n root_snap /dev/vg_system/lv_root

# 挂载快照并备份
mkdir /mnt/snapshot
mount -o ro /dev/vg_system/root_snap /mnt/snapshot
tar czf /backup/system-$(date +%Y%m%d).tar.gz -C /mnt/snapshot .
umount /mnt/snapshot

# 删除快照
lvremove /dev/vg_system/root_snap
```

### 6.2 dd 全盘镜像

```bash
# 全盘镜像（需要目标磁盘 >= 源磁盘）
# 请将 DISK 替换为实际磁盘设备（通过 lsblk 确认）
DISK="/dev/sdX"
dd if="$DISK" of=/backup/disk.img bs=4M status=progress

# 压缩镜像
dd if="$DISK" bs=4M status=progress | gzip > /backup/disk.img.gz

# 恢复
dd if=/backup/disk.img of="$DISK" bs=4M status=progress
# 或
gunzip -c /backup/disk.img.gz | dd of="$DISK" bs=4M status=progress

# 注意：dd 是块级复制，源和目标必须卸载或使用只读模式
```

### 6.3 配置文件版本管理（etckeeper）

```bash
# 安装
apt install etckeeper

# 初始化（自动用 git 跟踪 /etc）
etckeeper init
etckeeper commit "Initial commit"

# 查看变更历史
cd /etc && git log --oneline -20

# 查看某个文件的变更
cd /etc && git log -p nginx/nginx.conf

# 回滚到之前的版本
cd /etc && git diff HEAD~1 nginx/nginx.conf
cd /etc && git checkout HEAD~1 -- nginx/nginx.conf

# 自动提交：etckeeper 会在 apt/yum 操作前后自动提交
```

---

## 7. 灾难恢复

### 7.1 GRUB 引导修复

```bash
# 从 Live CD/USB 启动
# 请将 /dev/sdX 替换为实际磁盘设备（通过 lsblk 确认）

# 挂载根分区
mount /dev/sdX2 /mnt
mount /dev/sdX1 /mnt/boot/efi   # UEFI 系统
mount --bind /dev /mnt/dev
mount --bind /proc /mnt/proc
mount --bind /sys /mnt/sys

# chroot 进入系统
chroot /mnt

# 重新安装 GRUB
# BIOS/MBR
grub-install /dev/sdX
update-grub

# UEFI
grub-install --target=x86_64-efi --efi-directory=/boot/efi
update-grub

# 退出 chroot
exit
umount -R /mnt
reboot
```

### 7.2 文件系统修复

```bash
# ext4 修复（请将 /dev/sdXN 替换为实际分区设备）
# 必须先卸载文件系统
umount /dev/sdXN
e2fsck -f -y /dev/sdXN

# xfs 修复
umount /dev/sdXN
xfs_repair /dev/sdXN
# 如果失败，尝试：
xfs_repair -L /dev/sdXN   # 清零日志（可能丢失数据）

# 无法卸载根分区时
# 1. 从 Live CD 启动
# 2. 或设置为只读后修复
mount -o remount,ro /
fsck -y /dev/sdXN
```

### 7.3 数据恢复

```bash
# testdisk — 分区表恢复、文件恢复（请将 /dev/sdX 替换为实际设备）
apt install testdisk
testdisk /dev/sdX

# photorec — 文件恢复（按文件类型）
photorec /dev/sdX

# extundelete — ext4 文件恢复
apt install extundelete
umount /dev/sdXN
extundelete /dev/sdXN --restore-all
# 恢复的文件在 RECOVERED_FILES/ 目录

# 注意：发现数据丢失后，立即停止写入！
# 越早恢复，成功率越高
```

### 7.4 rescue 模式

```bash
# 进入 rescue 模式
systemctl rescue
# 或在 GRUB 菜单编辑内核参数，添加 single 或 rescue

# 常见 rescue 操作
# 1. 重置 root 密码
passwd root

# 2. 修复 fstab
vi /etc/fstab

# 3. 修复网络
ip addr add 10.0.0.100/24 dev eth0
ip link set eth0 up

# 4. 重新生成 initramfs
update-initramfs -u   # Ubuntu
dracut -f             # RHEL
```

---

## 8. 备份验证与监控

### 8.1 定期验证

```bash
# borg 验证
borg check /backup/borg-repo
borg list /backup/borg-repo | tail -1   # 最新备份时间

# restic 验证
restic check
restic snapshots --latest 1   # 最新快照

# 恢复测试（每月至少一次）
mkdir /tmp/restore-test
borg extract /backup/borg-repo::latest /tmp/restore-test
# 验证关键文件是否完整
diff /etc/nginx/nginx.conf /tmp/restore-test/etc/nginx/nginx.conf
rm -rf /tmp/restore-test
```

### 8.2 备份监控脚本

```bash
#!/usr/bin/env bash
# 检查备份是否正常执行

BACKUP_DIR="/backup/borg-repo"
MAX_AGE_HOURS=26   # 最大允许间隔（小时）

# 检查最新备份时间
latest=$(borg list --last 1 --format '{time}' "$BACKUP_DIR" 2>/dev/null)
if [ -z "$latest" ]; then
    echo "❌ 无法获取备份信息"
    exit 1
fi

latest_ts=$(date -d "$latest" +%s 2>/dev/null)
now_ts=$(date +%s)
age_hours=$(( (now_ts - latest_ts) / 3600 ))

if [ "$age_hours" -gt "$MAX_AGE_HOURS" ]; then
    echo "❌ 备份过期！最新备份: $latest（$age_hours 小时前）"
    exit 1
else
    echo "✅ 备份正常。最新备份: $latest（$age_hours 小时前）"
fi

# 检查仓库完整性
borg check "$BACKUP_DIR" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️ 仓库完整性检查失败"
    exit 1
fi
```

---

## 9. 常见故障排查

### 备份空间不足

```bash
# 1. 检查备份大小
du -sh /backup/*

# 2. 清理旧备份
borg prune --keep-daily=3 --keep-weekly=2 /backup/borg-repo
borg compact /backup/borg-repo

# 3. 检查去重效率
borg info /backup/borg-repo   # 查看去重率

# 4. 排除大文件
find /data -size +100M -type f   # 找出大文件
# 在备份命令中添加 --exclude
```

### 恢复失败

```bash
# 1. 检查备份完整性
borg check /backup/borg-repo
restic check --read-data

# 2. 检查权限
ls -la /backup/borg-repo

# 3. 检查密钥/密码
borg list /backup/borg-repo   # 如果提示密码错误

# 4. 尝试从其他备份恢复
borg list /backup/borg-repo   # 列出所有备份
borg extract /backup/borg-repo::second-latest
```

### 数据库恢复后不一致

```bash
# MySQL
# 1. 检查 binlog 位置
mysqlbinlog /var/lib/mysql/binlog.000001 | tail -20

# 2. 使用 --source-data 参数备份（记录 binlog 位置）
mysqldump --source-data=2 --single-transaction mydb > backup.sql

# PostgreSQL
# 1. 检查 WAL 归档
ls -la /backup/pg/wal/

# 2. 使用 PITR 恢复到精确时间点
# recovery_target_time = '2026-04-01 11:59:59'
```
