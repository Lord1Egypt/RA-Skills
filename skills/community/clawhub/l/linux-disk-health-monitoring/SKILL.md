---
name: linux-disk-health-monitoring
description: 磁盘健康/SMART/备份韧性。Use when 查硬盘健康、SMART监控、备份同盘风险、drill排查。
version: 1.0.0
author: peterliu-512
license: MIT
metadata:
  hermes:
    tags: [devops, disk, smart, backup, resilience, sentinel]
    related_skills: [linux-disk-space-triage, system-full-backup-seal-sop, linux-fast-diREDACTED-SECRET]
---

# Linux 磁盘健康监控与备份韧性

## When to Use
- 用户问磁盘健康/寿命/SMART/硬盘风险/磁盘健康管理方案
- 需搭建磁盘监控告警（"健康静默、异常推送"哨兵模式）
- 评估备份架构可靠性（同盘备份、同盘多副本、无异地副本）
- 备份恢复演练（drill）报错/误报排查
- 新增/改造周备份脚本与恢复验证流程

## 核心结论先行原则（给高管的表达框架）
1. **备份与源同物理盘 ≠ 容灾**——盘挂全没。可靠性层次：同分区 < 同盘异分区 < 异盘(同机) < 异机。先查清这个再谈方案
2. **SMART 总评 PASSED 不等于无风险**——看具体属性与趋势：温度、Command_Timeout 环比、距上次自检时长、重映射/待映射是否 >0
3. **分区归属判定以 blkid 的 FSTYPE 为准，PARTLABEL 不可信**（本机实测：sda9/sda10 是 xfs 却标 PARTLABEL="NTFS"；sda11 标 "Linux /home partition" 却是无文件系统裸分区）——blkid 无 TYPE 字段 = 无文件系统 = 无数据，可安全格式化
4. 输出结构：健康基线表(两盘对比) + 风险矩阵(分级) + 分层方案 **P0监控/P1备份架构/P2替换预案/P3物理治理** + 数据分级合规备注(L1不可再生/L2代码/L3媒体红线只进不出)

## 实测采集命令
```bash
# HDD：关注重映射/待映射/离线/命令超时/通电时长/温度
sudo smartctl -a /dev/sda | grep -E 'SMART overall|Reallocated|Current_Pending|Offline_Uncorrect|UDMA_CRC|Power_On_Hours|Temperature_Celsius|Command_Timeout'
# 自检记录（距上次自检太久=自检荒废，如175天）
sudo smartctl -l selftest /dev/sda | tail -5
# NVMe：磨损/备用/温度/错误
sudo smartctl -a /dev/nvme0n1 | grep -E 'Percentage Used|Available Spare|Temperature:|Media and Data|Critical Warning|Power On Hours'
# 分区身份（权威判定，先于任何格式化/删除决策）
sudo blkid /dev/sda*; lsblk -o NAME,SIZE,FSTYPE,MOUNTPOINT /dev/sda
```

## 本机健康基线判读经验（HGST 8T + NVMe）
- 温度：机械盘 ≥50°C 偏高（目标 <45，每降 10°C 寿命约翻倍）；NVMe 45°C 正常
- Command_Timeout 千万级（如 10,354,688）：盘面未必坏，常见 SATA 线缆/背板/固件信号——记录基线观察趋势，物理治理需用户动手
- 通电 2.9 万小时 ≈3.3 年，企业盘 5 年寿命窗口 → 建议 12 个月内替换预案（先完成备份韧性再谈换盘=无损操作）

## NVMe awk 解析坑（实测字段位，必须 ^ 锚定）
`smartctl -A /dev/nvme0n1` 输出：`^Temperature: 45 Celsius` → `$2`；`^Percentage Used: 0%` → `$3`(去%)；`^Media and Data Integrity Errors: 0` → `$6`；`^Critical Warning: 0x00` → `$3`。不锚定行首会误匹配他行、字段号错位产出 `used=%` 垃圾值。

## 静默哨兵模式（Hermes cron no_agent，最优雅的监控形态）
- 脚本 stdout **空=健康静默**（no_agent 语义：空输出不推送）；**非空=异常推送**
- **环比检测**：只升不降属性（Command_Timeout）存基线文件，当前 > 基线才告警；首跑建基线会误报一次属预期
- **周自检闭环**：脚本内置 `date +%u`==7 且距上次自检 >144h → 触发 `smartctl -t short`（8T 约2-4分钟异步）；每次跑查 selftest 含 FAILED 即告警
- 阈值参考：HDD 温度≥55 / 重映射·待映射·离线 >0 / Command_Timeout 环比增长 / SMART 非 PASSED / NVMe 磨损≥80% / Critical Warning≠0x00 / 数据完整性错误>0

## 备份韧性改造要点（防物理盘故障）
- 核心不可再生数据清单（本机）：`.hermes`(记忆+会话+state.db+skills+cache交付物) / `.openclaw` / `.dsh` / `~/Documents`(Obsidian Vault实体) / `/data/knowledge-base` / `/data/guji-rag` / `~/scripts`
- `.hermes` 异盘副本**排除项**（可再生源码/内部备份不复制，8.3G→~2.5G）：`hermes-agent`、`hermes-agent-backup-*`、`backups`、`state-snapshots`、`checkpoints`、`migration`、`sessions.bak.*`、`lsp`、`audio_cache`、`.cache`
- 周备份 KEEP=5≈月（同盘异分区防逻辑损坏）；异盘核心副本 KEEP=2（防副本自身损坏）
- **恢复演练哈希误报**：备份版本滞后于源属正常——源文件 mtime 晚于备份日期时哈希不一致降级 ⚠️ warning 不计 FAIL；只有源不新于备份仍不一致才算真失败

## Pitfalls（踩过的坑）
1. **mkfs/格式化在 Hermes 无条件 blocklist**——agent 即使 sudo 也执行不了（BLOCKED hardline），必须把精确命令（mkfs+mount+fstab+chown 一条龙）交给用户终端执行。给命令前先自己完成 blkid 验证消除用户疑虑
2. 新挂载点（/backup）及 /data、/mnt/nvme_fast 根目录 root 755——用户可写子目录须 `sudo mkdir -p` + `sudo chown 用户`，否则 rsync 权限失败；非 sudo 全盘 rm 会因部分 root 文件删不掉且 `&&` 短路
3. 大删除（百G级）用 background=true + notify_on_complete，先 `du -sh` 预期值再动手；删除中见"权限不够"先看属主再决定 sudo
4. rsync 默认不跟符号链接（-a 含 -l 保留链接本身）——KB 软链结构照抄即可，恢复时实体路径一致则通（与周备份同构最稳）
5. Hermes cron gateway_running:false 是容器视角误报，任务是否真跑以宿主 systemctl active + output 当日 md 为准

## 支持文件
- `scripts/disk_smart_monitor.sh` — 磁盘健康哨兵成品（HDD+NVMe 全指标+基线+周自检闭环，可直接接 cron no_agent）
- `references/diREDACTED-SECRET.md` — 本机 2026-09-04 实测：SMART 基线数值、结构性风险、sda11 归属验证、备份架构改造记录
