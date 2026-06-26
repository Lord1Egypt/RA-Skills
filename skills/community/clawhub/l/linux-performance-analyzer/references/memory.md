# 内存调优参考手册

## 目录
1. [快速诊断](#1-快速诊断)
2. [Swap 与 swappiness 调优](#2-swap-与-swappiness-调优)
3. [OOM Kill 处理与预防](#3-oom-kill-处理与预防)
4. [透明大页 THP](#4-透明大页-thp)
5. [HugePage 配置](#5-hugepage-配置)
6. [脏页回写调优](#6-脏页回写调优)
7. [内存回收与 min_free_kbytes](#7-内存回收与-min_free_kbytes)
8. [Slab 缓存优化](#8-slab-缓存优化)
9. [NUMA 内存优化](#9-numa-内存优化)
10. [内存泄漏排查](#10-内存泄漏排查)
11. [容器内存限制排查](#11-容器内存限制排查)

---

## 1. 快速诊断

```bash
# 内存概览
free -h

# 详细内存信息
cat /proc/meminfo | grep -E "MemTotal|MemFree|MemAvailable|Buffers|Cached|SwapTotal|SwapFree|Dirty|Writeback|AnonPages|Slab|KernelStack|PageTables|HugePages"

# OOM 历史
dmesg | grep -iE "oom|killed process" | tail -20

# 内存占用 TOP 进程
ps aux --sort=-%mem | head -15

# Slab 缓存
slabtop -o | head -20

# Swap 使用情况
swapon --show
vmstat 1 3 | grep -E "si|so"   # si=swap in, so=swap out
```

**关键指标解读：**
| 指标 | 正常 | 警告 | 严重 |
|------|------|------|------|
| MemAvailable / MemTotal | > 30% | < 20% | < 10% |
| Swap 使用率 | 0% | > 10% | > 30% |
| Dirty / MemTotal | < 2% | > 5% | > 10% |
| vmstat si/so | = 0 | > 0 | 持续 > 100MB/s |

---

## 2. Swap 与 swappiness 调优

```bash
# 查看当前 swappiness
sysctl vm.swappiness

# 调整建议：
# 桌面系统：60（默认）
# 服务器：10（减少换页，优先使用内存）
# 数据库（MySQL/Redis）：1（几乎不换页）
sysctl -w vm.swappiness=10

# 持久化
echo "vm.swappiness=10" >> /etc/sysctl.d/99-perf-master.conf

# 创建 Swap 文件（系统无 Swap 时）
fallocate -l 4G /swapfile
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
echo '/swapfile none swap sw 0 0' >> /etc/fstab

# 验证
free -h   # Swap 行应有数值
swapon --show

# 删除 Swap
swapoff /swapfile
rm /swapfile
sed -i '/swapfile/d' /etc/fstab
```

---

## 3. OOM Kill 处理与预防

```bash
# 查看 OOM 历史
dmesg | grep -iE "oom|killed process|out of memory" | tail -30

# 查看进程的 OOM 分数（越高越容易被杀）
cat /proc/<PID>/oom_score
cat /proc/<PID>/oom_score_adj   # -1000 永不被杀，+1000 最先被杀

# 保护关键进程（永不被 OOM Kill）
echo -1000 > /proc/<PID>/oom_score_adj    # 最高保护
echo -500  > /proc/<PID>/oom_score_adj    # 强保护

# 降低 OOM 保护（非关键进程）
echo 500 > /proc/<PID>/oom_score_adj

# 脚本：保护多个关键进程
protect_procs=("mysqld" "redis-server" "nginx" "knot-cli")
for proc in "${protect_procs[@]}"; do
    PID=$(pgrep -x "$proc" | head -1)
    if [[ -n "$PID" ]]; then
        echo -500 > /proc/$PID/oom_score_adj
        echo "Protected: $proc (PID=$PID)"
    fi
done

# 全局 overcommit 策略
sysctl vm.overcommit_memory   # 0=启发式(默认), 1=总是允许, 2=严格
# 建议保持默认 0，或改为 1（允许 overcommit，适合大多数应用）
# ⚠️ overcommit_memory=2 会导致很多应用启动失败，慎用

# 内存限制（用 systemd-run 包裹）
systemd-run --scope -p MemoryMax=2G ./high_mem_app

# 验证 OOM 频率是否下降
watch -n 2 'dmesg | grep -c "Out of memory"'
```

---

## 4. 透明大页 THP

```bash
# 查看当前状态
cat /sys/kernel/mm/transparent_hugepage/enabled
# [always] madvise never

# 何时关闭 THP：
# - MySQL / PostgreSQL / Oracle（官方建议关闭）
# - Redis（官方建议关闭）
# - 延迟敏感的实时应用
# - 出现内存碎片或 khugepaged CPU 占用高时

# 临时关闭
echo never > /sys/kernel/mm/transparent_hugepage/enabled
echo never > /sys/kernel/mm/transparent_hugepage/defrag

# 持久化（写入启动脚本）
cat > /etc/systemd/system/disable-thp.service << 'EOF'
[Unit]
Description=Disable Transparent Huge Pages
After=network.target

[Service]
Type=oneshot
ExecStart=/bin/sh -c "echo never > /sys/kernel/mm/transparent_hugepage/enabled"
ExecStart=/bin/sh -c "echo never > /sys/kernel/mm/transparent_hugepage/defrag"
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
EOF
systemctl enable --now disable-thp.service

# 验证
cat /sys/kernel/mm/transparent_hugepage/enabled   # 应显示 never

# 仅对特定进程启用 THP（madvise 模式）
echo madvise > /sys/kernel/mm/transparent_hugepage/enabled
# 在代码中使用 madvise(addr, len, MADV_HUGEPAGE)
```

---

## 5. HugePage 配置

```bash
# 查看 HugePage 状态
grep -i huge /proc/meminfo

# 适用场景：数据库 SGA（Oracle/DB2）、Java 大堆、内存密集型计算

# 配置 HugePage 数量（2MB per page）
# 计算：如需 10GB HugePage → 10*1024/2 = 5120 pages
sysctl -w vm.nr_hugepages=5120

# 持久化
echo "vm.nr_hugepages=5120" >> /etc/sysctl.d/99-perf-master.conf

# 查看 HugePage 使用情况
cat /proc/meminfo | grep -i huge
# HugePages_Total: 5120
# HugePages_Free:  4096   ← 未使用的页数

# 透明大页 vs 静态 HugePage：
# - 静态 HugePage：需预分配，性能更稳定，适合数据库
# - THP：动态分配，更灵活，但可能导致延迟毛刺

# Java 使用 HugePage
java -XX:+UseLargePages -XX:LargePageSizeInBytes=2m -jar app.jar
```

---

## 6. 脏页回写调优

```bash
# 查看当前脏页状态
grep -E "Dirty|Writeback" /proc/meminfo

# 查看参数
sysctl vm.dirty_ratio vm.dirty_background_ratio vm.dirty_expire_centisecs vm.dirty_writeback_centisecs

# 参数说明：
# dirty_background_ratio：脏页超过此比例时后台回写开始（默认10%）
# dirty_ratio：脏页超过此比例时写操作被阻塞（默认20-40%）
# dirty_expire_centisecs：脏页超过此时间(cs)强制回写（默认3000 = 30s）
# dirty_writeback_centisecs：后台回写线程唤醒间隔（默认500 = 5s）

# 写密集场景（减少写回积压）
sysctl -w vm.dirty_ratio=10
sysctl -w vm.dirty_background_ratio=5
sysctl -w vm.dirty_expire_centisecs=1500
sysctl -w vm.dirty_writeback_centisecs=500

# 高吞吐写场景（允许更多脏页积累）
sysctl -w vm.dirty_ratio=60
sysctl -w vm.dirty_background_ratio=40

# 绝对值控制（推荐用字节代替百分比，内存大时更精确）
sysctl -w vm.dirty_bytes=268435456        # 256MB 触发阻塞
sysctl -w vm.dirty_background_bytes=67108864  # 64MB 触发后台回写
# ⚠️ dirty_bytes 和 dirty_ratio 二选一，设置bytes时ratio失效

# 手动触发脏页回写（谨慎，会造成 I/O 尖峰）
sync; echo 1 > /proc/sys/vm/drop_caches   # 仅清页缓存
sync; echo 3 > /proc/sys/vm/drop_caches   # 清页缓存+dentries+inodes
```

---

## 7. 内存回收与 min_free_kbytes

```bash
# 查看内存水位
sysctl vm.min_free_kbytes

# 增大内核保留内存（防止因为瞬间分配导致 OOM）
# 建议：总内存 0.1%~1%，最少 64MB，最大 256MB
sysctl -w vm.min_free_kbytes=131072   # 128MB

# 内存紧张时策略
sysctl vm.vfs_cache_pressure   # 默认100，增大=更激进回收缓存，减小=保留更多缓存

# 主动触发内存回收（不影响应用，谨慎使用）
echo 1 > /proc/sys/vm/drop_caches   # page cache
echo 2 > /proc/sys/vm/drop_caches   # dentries & inodes
echo 3 > /proc/sys/vm/drop_caches   # all

# 查看各区域内存水位
cat /proc/zoneinfo | grep -A5 "Node 0, zone"
```

---

## 8. Slab 缓存优化

```bash
# 查看 Slab 使用
slabtop -o | head -20
cat /proc/slabinfo | sort -k3 -rn | head -20

# 查看 Slab 占用总量
grep Slab /proc/meminfo

# 如果 Slab 异常大（> 物理内存 20%），排查原因
# 常见原因：
# 1. dentries/inodes 过多（大量小文件）
# 2. TCP socket 泄漏
# 3. nf_conntrack 表满

# 清理 Slab 缓存
echo 2 > /proc/sys/vm/drop_caches   # 清 dentries/inodes slab
echo 3 > /proc/sys/vm/drop_caches   # 清所有可回收 slab

# 调整 slab 缩减策略
sysctl -w vm.vfs_cache_pressure=200   # 更积极地回收 VFS 缓存（默认100）
```

---

## 9. NUMA 内存优化

```bash
# 查看 NUMA 内存分布
numastat -m 2>/dev/null
numastat -p <PID> 2>/dev/null

# 检查 NUMA 命中率（numa_miss 高说明跨节点访存频繁）
numastat | grep -E "numa_hit|numa_miss|local_node|other_node"

# 开启 NUMA 自动均衡（多 NUMA 节点服务器默认开启）
sysctl -w kernel.numa_balancing=1

# 关闭 NUMA 均衡（延迟敏感场景，减少进程迁移）
sysctl -w kernel.numa_balancing=0

# 内存交错分配（适合均匀访问大内存的场景）
numactl --interleave=all ./app

# 绑定进程到指定 NUMA 节点
numactl --cpunodebind=0 --membind=0 ./app   # 绑定到 node0
```

---

## 10. 内存泄漏排查

```bash
# 监控进程内存趋势（每5秒）
watch -n 5 'ps -p <PID> -o pid,rss,vsz,comm'

# 详细内存映射
cat /proc/<PID>/smaps | awk '/Rss/{rss+=$2} END{print "RSS:", rss"KB"}'
cat /proc/<PID>/status | grep -E "VmRSS|VmSwap|VmPeak"

# Valgrind 内存泄漏检测（C/C++）
valgrind --leak-check=full --show-leak-kinds=all ./app

# AddressSanitizer（编译时开启，性能损耗约2x）
gcc -fsanitize=address -g ./app.c -o app_asan
./app_asan   # 泄漏时会输出详细报告

# Java 堆分析
jmap -dump:format=b,file=heap.hprof <PID>
jhat heap.hprof   # 内置分析器
# 或使用 Eclipse MAT 分析 heap.hprof

# Python 内存分析
python3 -c "
import tracemalloc
tracemalloc.start()
# ... 运行代码 ...
snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')
for stat in top_stats[:10]:
    print(stat)
"
```

---

## 11. 容器内存限制排查

```bash
# 查看容器内存限制
cat /sys/fs/cgroup/memory/memory.limit_in_bytes
cat /sys/fs/cgroup/memory/memory.usage_in_bytes
cat /sys/fs/cgroup/memory/memory.failcnt          # 分配失败次数（高值说明频繁触碰上限）

# OOM Kill 记录
cat /sys/fs/cgroup/memory/memory.oom_control

# 计算实际可用内存
echo "限制: $(( $(cat /sys/fs/cgroup/memory/memory.limit_in_bytes) / 1024 / 1024 )) MB"
echo "使用: $(( $(cat /sys/fs/cgroup/memory/memory.usage_in_bytes) / 1024 / 1024 )) MB"

# Kubernetes Pod 内存
kubectl top pod <pod>
kubectl describe pod <pod> | grep -A5 "Limits\|Requests"
kubectl get events | grep OOMKilled

# 保护容器内关键进程
echo -500 > /proc/<PID>/oom_score_adj

# 运行高内存任务时限制（避免影响其他进程）
systemd-run --scope -p MemoryMax=512M python3 heavy_script.py
```