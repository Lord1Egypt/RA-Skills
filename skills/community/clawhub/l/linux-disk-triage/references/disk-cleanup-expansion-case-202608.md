# 磁盘清理与扩容实测案例（2026-08-16，本机）

## 场景
`/` 分区 89% 告警（100G 中已用 89G，仅 12G 可用）。目标是恢复可用空间，随后用户问"如何扩到 250G"。

## 清理结果（89% → 79%，回收 ~10G）
| 清理项 | 释放 | 命令 |
|---|---|---|
| Docker 构建缓存 | 3.2G | `docker builder prune -f` |
| 系统日志旧轮转 | 2.0G | `sudo rm -f /var/log/messages-*`（4 份 465-575M） |
| journald 归档 | 1.2G | `sudo journalctl --vacuum-size=300M` |
| /tmp 残留 | 1.8G | ollama 安装包 1.4G + 临时提取目录/hm_test* |
| 无用镜像 | 0.1G | `docker rmi ai-device-manager:*`（先 `docker ps -a` 确认无容器引用） |
| Docker 悬空镜像 prune | 0B 磁盘 | 层被在用镜像共享（`Total reclaimed space: 0B`）——预期现象 |

**未动**：在用容器镜像（量化研究 6G、open-webui 4.7G、ollama 6G、自研媒资 4.7G）、基础镜像（仍有容器引用，rmi 报 conflict 属预期，先确认再处置）、CUDA/opt/nvidia（系统依赖）。

## 分区布局（单块 7.3T GPT 盘 sda，混合 Windows+Linux）
```
sda3  2T   ntfs  (Windows)
sda5  2.6T xfs   /data   ← 仅用 69G，空余 2.6T
sda7  1G   ext4  /boot
sda8  16G  swap
sda9  100G xfs   /       ← 目标扩容（docker 55G 在 /var/lib/docker，是大头）
sda10 200G xfs   /home   ← 已用 72G；xfs 不能缩容
sda11 2.4T 未格式化       ← 完全空闲，PARTLABEL="Linux /home partition"（历史遗留）
```

## 扩容到 250G 的方案（给用户的对比）
- **方案 A（推荐先行）**：docker 数据目录迁 /data/docker → `/` 从 79% 降到 ~25%（等效扩容 55G），零风险可回滚，docker 重启约 2 分钟
- **方案 B（真扩容）**：/home 迁移到 sda11（格式化 + rsync + fstab）→ 删 sda10 → `growpart /dev/sda 9` → `xfs_growfs /`。上限 300G（sda9 起点 9955766272 到 sda11 起点 10584915968）。需备份 + 停机窗口 30-60 分钟
- **方案 C**：先 A 后 B（推荐组合，A 降低 B 的紧迫性与风险）

## 关键判断依据
- 不是 LVM（lsblk 无 lv/vg 层级）→ 不能 lvextend，只能分区级操作
- xfs 只能扩不能缩 → /home 不能原地缩小，必须整体迁移
- 扩容方向只能向后（GPT 分区表约束），sda9 后面是 sda10，所以先移 /home

## 后续治理建议（未执行）
1. docker 容器日志无上限（17 容器 json 日志）：daemon.json `log-opts: max-size=50m, max-file=3`（需重启 docker，选低峰）
2. journald `SystemMaxUse=300M` 持久化（本次 vacuum 是一次性的）
3. 每月例行清理 cron（builder prune + journal vacuum + /tmp）
