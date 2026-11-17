# 本机磁盘健康与备份韧性改造记录（2026-09-04）

## 硬件基线（实测 SMART）
- 机型 Dell Precision Tower 7810 / RHEL 8.10 / Xeon E5-2620 v3 ×2 (24线程) / 32G DDR4-1866 / RTX 3060 12G
- **sda = HGST HUS728T8TALE6L4 8T**（通电 25,473h≈2.9年、313次电源循环、温度 50°C(9~55)、重映射0/待映射0/离线0、**Command_Timeout=10,354,688**⚠️、UDMA_CRC 0、末次自检 175 天前）
- **nvme0n1 = Colorful CN600 2TB PLUS**（348h、写入1.04TB、磨损0%、Spare 100%、温度45°C、0错误）→ /mnt/nvme_fast 349G/1.9T

## 分区结构（关键判定）
- sda5 /data 2.6T xfs(219G/9%) | sda9 / 100G xfs(33G/33%) | sda10 /home 200G xfs(56G/28%) | nvme0n1p1 /mnt/nvme_fast 1.9T xfs(349G/19%)
- Windows 残留：sda3 2T ntfs + sda4 608M + sda6 3.1G（未挂载、保留不动）
- **sda11 2.4T 裸分区**：PARTLABEL="Linux /home partition" 误导（sda9/sda10 反而标 "NTFS"！）→ blkid 无 TYPE 字段 = 无文件系统 = 零数据 → 判定可安全格式化
- 结论：PARTLABEL 全盘混乱不可信（多次重装残留），唯一权威 = blkid FSTYPE/TYPE

## 结构性风险（方案依据）
1. 🔴 /、/home、/data、/data/backup 全部同盘 sda——物理损坏全没
2. 🔴 无任何异机备份（NAS 192.168.3.2 当前不可达：ping loss + 445 拒连）
3. 🟡 Command_Timeout 千万级（线缆/背板/固件信号）
4. 🟡 温度 50°C 持续偏高
5. 🟢 sda11 2.4T 空闲 → 备份扩展位

## 改造落地
- **backup_weekly.sh**：BACKUP_ROOT /data/backup → /backup（sda11）；新增第7段 NVMe 异盘核心副本 → /mnt/nvme_fast/core_backup/$DATE，KEEP=2
- **核心副本清单**（~5-8G）：hermes(排 hermes-agent/backups/state-snapshots/checkpoints/migration/sessions.bak.*/lsp/audio_cache/.cache) + openclaw + dsh + Documents + knowledge-base + guji-rag + scripts
- **disk_smart_monitor.sh**（哨兵）+ cron 4a305a4b75df 每日 09:30 no_agent；基线 ~/.hermes/scripts/disk_smart_baseline.txt
- **backup_restore_drill.sh**：路径 /data/backup→/backup；第4步哈希不一致增加版本滞后容错（源 mtime > 备份日期 → ⚠️ warning 不计 FAIL）；误报实例：8/30 备份 vs 9/2 更新 openclaw.json
- cron 62e888704a92（9/10 观察期提醒）已移除（数据 9/4 提前清理完：/data 512G→219G 释放294G + /root/.ollama 10G）

## 待用户终端执行（agent 被 mkfs hardline block）
```bash
sudo mkfs.xfs -f -L backup /dev/sda11
sudo mkdir -p /backup && sudo mount /dev/sda11 /backup
echo "UUID=$(sudo blkid -s UUID -o value /dev/sda11) /backup xfs defaults,noatime 0 2" | sudo tee -a /etc/fstab
sudo chown <user>:<user> /backup
df -hT /backup | tail -1
```
执行后：迁移 /data/backup(22G)→/backup（rsync 校验→旧目录改名 /data/backup_legacy_20260904 留存），跑 backup_weekly.sh 验证全链路。
