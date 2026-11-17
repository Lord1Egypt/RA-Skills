---
name: linux-disk-space-triage
description: Linux磁盘告警清理与根分区扩容分析。Use when 磁盘告警、需腾空间、问如何扩大根分区。
version: 1.0.0
author: peterliu-512
license: MIT
metadata:
  hermes:
    tags: [devops, disk, storage, xfs, docker, capacity-planning]
    related_skills: [local-service-usage-audit, system-full-backup-seal-sop]
---

# Linux 磁盘告警治理与扩容分析

## When to Use
- `df` 显示某分区使用率告警（通常 >80%），需要腾空间
- 用户问"如何扩大根目录 / 的容量"（扩容分析）
- 磁盘清理需要区分"可安全删"与"项目刚需"并给出依据

## 第一步：分区结构诊断（先看布局再动手）
```bash
df -h / /data /home                 # 哪些分区告警、哪些充裕
lsblk -o NAME,SIZE,TYPE,FSTYPE,MOUNTPOINT   # 分区布局 + 文件系统类型
df -T /                              # 确认 / 是 xfs 还是 ext4
pvs; vgs; lvs                        # 是否 LVM（LVM 可 lvextend 在线扩）
sudo fdisk -l /dev/sda               # 物理盘布局、分区顺序、空闲扇区
sudo du -xsh /var /usr /opt /tmp /root 2>/dev/null | sort -rh   # / 分区大头
sudo du -sh /var/lib/docker          # docker 常是 / 分区隐形大头
docker system df                     # 镜像/容器/卷/构建缓存占用与可回收量
```

## 关键规则（决定方案）
- **xfs 只能扩容不能缩容**——任何"缩一个 xfs 分区给邻居腾空间"的方案都不可行，只能整体迁移
- **ext4 可缩可扩**（resize2fs），但根分区仍需离线操作
- **GPT 分区只能向后扩**：目标分区后面必须有可用空间（相邻分区已删除/未分配）
- **/ 是 xfs 时**：`growpart` 扩分区表 + `xfs_growfs /` 可在线扩文件系统（前提是分区表腾出了空间）
- 物理盘混合 Windows/Linux 分区时（如 sda3 ntfs + sda9/sda10 linux），动分区表前必须先备份

## 可清理项清单（按风险从低到高）
```bash
# 1. Docker（最安全，通常最大）
docker builder prune -f              # 构建缓存（可 100% 回收，常 3G+）
docker image prune -f                # 悬空镜像（仅删 dangling，不动在用）
docker volume prune -f               # 悬空卷

# 2. 系统日志
sudo rm -f /var/log/messages-*       # 旧轮转文件（保留当前 messages，单份可 400-600M）
sudo journalctl --vacuum-size=300M   # 归档 journal（一次性）
# 持久化限制：
sudo mkdir -p /etc/systemd/journald.conf.d
echo -e "[Journal]\nSystemMaxUse=300M" | sudo tee /etc/systemd/journald.conf.d/size.conf

# 3. /tmp 残留（确认无依赖再删；如安装包已装好则安装包可删）
sudo du -sh /tmp/* | sort -rh

# 4. 无用镜像（必须先确认无容器引用！）
docker ps -a --format "{{.Image}}" | sort -u   # 看哪些镜像在用
docker rmi <image>                    # 有容器引用会报 conflict: container ... is using

# 5. 容器日志隐形杀手（json 文件无限增长，默认不轮转）
sudo du -sh /var/lib/docker/containers
# 治理：/etc/docker/daemon.json 加 log-opts 后重启 docker（会中断所有容器，选低峰）
# {"log-driver":"json-file","log-opts":{"max-size":"50m","max-file":"3"}}
```

## 扩容分析框架（用户问"扩到 250G"这类时）
1. 诊断分区顺序与空闲空间：`fdisk -l` 看目标分区相邻位置；`lsblk -f` 看是否有未格式化空闲分区（partlabel 可提示原用途）
2. 判定路径：
   - **方案 A（推荐先行，零风险）**：把 / 分区上的大目录（典型是 /var/lib/docker 55G）迁到空闲大分区（如 /data 2.6T）：`rsync` → 停 docker → 改 daemon.json `data-root` → 重启。等效"扩容"且不动分区表、可回滚
   - **方案 B（真扩容，中高风险，需备份+停机窗口）**：把相邻分区（如 /home）整体迁移到空闲分区 → 删除原分区 → `growpart /dev/sda <n>` 扩展目标分区到邻接起点 → `xfs_growfs /` 在线扩文件系统
   - 扩容上限 = 目标分区起点到下一分区起点的全部空间；精确控制容量用 `parted resizepart`
3. 任何分区表操作前：备份分区表（`sgdisk --backup`）+ 关键数据 rsync；fstab 改动后必须先重启验证

## /home 腾空间标准流程（清理 → 迁移 → 缓存重定向 三步闭环）
清理只是第一步，根治靠迁移 + 缓存重定向，否则缓存几个月又涨回去：
1. **清理**：按「可清理项清单」逐项回收（缓存/安装包残留/冗余模型/旧备份）
2. **大目录迁移**：~/models、项目目录等用 `rsync + 软链接` 迁到 /data（详见 `references/data-dir-migration-softlink-pattern.md`，含 venv/git 验证、权限坑、完整性校验）
3. **缓存重定向**：pip.conf / .npmrc / UV_CACHE_DIR 指向 /data/cache，防新增长；旧缓存手动删除回收
本机 2026-08-29 实测：/home 96% → 27%（清理回收 72G + models 65G + 项目 3.5G），方案可复制。

## Pitfalls
- **pkill -f 自杀陷阱（实测 exit -15）**：`pkill -f '@scope/pkg'` 会匹配到执行命令的 bash 自身（命令串里含该字符串），把自己 SIGTERM 杀掉。修复：方括号技巧 `pkill -f '[x]xx'`（正则不匹配自身），或先 `ps aux` 查 PID 再精确 kill。pgrep -f 同理会误报自身
- 大目录 du/grep 超时（/data 2.7T、/home 200G）：用 `du -xsh` 限定挂载点、`sudo du -sh` 逐目录，别全盘
- docker 镜像层共享：`docker images` 显示的多 tag 可能同一 ID（实际一份存储）；悬空镜像 prune 后 reclaimed 可能为 0B（层被引用）
- 删 /var/log/messages-* 前确认 logrotate 配置正常，否则当前日志会无限增长
- 磁盘清理后应复检 `df -h` 报告前后对比；清理对象按"有依据不动"原则说明（在用容器镜像、CUDA、系统依赖）

## 验证
- 清理后：`df -h` 对比使用率与可用空间（实测 89%→79%，回收 10G）
- 扩容后：`df -hT /` 确认新容量 + `xfs_info /` 确认文件系统已扩展

## 支持文件
- `references/diREDACTED-SECRET.md` — 2026-08 实测案例：清理明细、分区布局、250G 扩容方案三选
