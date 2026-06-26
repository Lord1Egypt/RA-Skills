# 内核参数速查全表

> 本文档列出所有常用内核参数的默认值、建议值和适用场景，配合 `sysctl` 命令使用。
>
> 修改前必读：先用 `sysctl 参数名` 记录原始值；生产环境先临时生效再持久化。

---

## 一、内存参数

| 参数 | 默认值 | 建议值 | 场景说明 |
|------|--------|--------|---------|
| `vm.swappiness` | 60 | 10（服务器）/ 1（数据库）| 降低换页倾向 |
| `vm.min_free_kbytes` | 内存相关 | 131072~262144 | 防止 OOM 误杀，预留内核内存 |
| `vm.dirty_ratio` | 20~40 | 10（写密集）/ 60（批量写） | 脏页触发阻塞阈值 |
| `vm.dirty_background_ratio` | 10 | 5 | 后台回写触发阈值 |
| `vm.dirty_expire_centisecs` | 3000 | 1500 | 脏页强制刷盘时间(cs) |
| `vm.dirty_writeback_centisecs` | 500 | 300~500 | 后台回写线程唤醒间隔(cs) |
| `vm.dirty_bytes` | 0（未设置）| 268435456（256MB）| 绝对值控制，与ratio二选一 |
| `vm.dirty_background_bytes` | 0（未设置）| 67108864（64MB）| 绝对值控制，与background_ratio二选一 |
| `vm.overcommit_memory` | 0 | 0（默认）/ 1（允许）| 0=启发式, 1=允许, 2=严格 |
| `vm.overcommit_ratio` | 50 | 80 | overcommit_memory=2时的比例 |
| `vm.vfs_cache_pressure` | 100 | 50~200 | VFS缓存回收压力（>100更激进） |
| `vm.nr_hugepages` | 0 | 按需 | 静态HugePage数量（数据库） |
| `vm.numa_stat` | 1 | 保持默认 | NUMA统计 |

---

## 二、CPU/调度参数

| 参数 | 默认值 | 建议值 | 场景说明 |
|------|--------|--------|---------|
| `kernel.sched_min_granularity_ns` | 3000000 (3ms) | 10000000 (10ms) | 调度最小粒度，增大减少切换 |
| `kernel.sched_wakeup_granularity_ns` | 4000000 (4ms) | 15000000 (15ms) | 唤醒粒度，防止频繁抢占 |
| `kernel.sched_migration_cost_ns` | 500000 (0.5ms) | 5000000 (5ms) | 进程迁移代价，增大减少跨核 |
| `kernel.numa_balancing` | 1 | 0（延迟敏感）| NUMA自动均衡（延迟敏感关闭） |
| `kernel.sched_autogroup_enabled` | 1 | 0（服务器）| 进程组自动调度（服务器关闭） |
| `kernel.pid_max` | 32768 | 4194304 | 最大PID数（容器密集环境调大） |
| `kernel.threads-max` | 取决内存 | 保持默认 | 最大线程数 |

---

## 三、网络参数

### TCP 连接状态

| 参数 | 默认值 | 建议值 | 场景说明 |
|------|--------|--------|---------|
| `net.ipv4.tcp_tw_reuse` | 0 | 1 | 允许重用TIME_WAIT连接 |
| `net.ipv4.tcp_fin_timeout` | 60 | 30 | FIN_WAIT_2超时时间(秒) |
| `net.ipv4.tcp_max_tw_buckets` | 180000 | 262144 | TIME_WAIT桶数量上限 |
| `net.ipv4.tcp_keepalive_time` | 7200 | 600 | Keepalive探测起始时间(秒) |
| `net.ipv4.tcp_keepalive_intvl` | 75 | 30 | Keepalive探测间隔(秒) |
| `net.ipv4.tcp_keepalive_probes` | 9 | 5 | Keepalive探测次数 |
| `net.ipv4.tcp_syncookies` | 1 | 1 | SYN Cookie防护(保持开启) |

### TCP 队列与并发

| 参数 | 默认值 | 建议值 | 场景说明 |
|------|--------|--------|---------|
| `net.core.somaxconn` | 4096 | 65535 | accept队列上限 |
| `net.ipv4.tcp_max_syn_backlog` | 1024 | 65535 | SYN队列上限 |
| `net.core.netdev_max_backlog` | 1000 | 65535 | 网卡接收队列长度 |

### TCP 缓冲区

| 参数 | 默认值 | 建议值 | 场景说明 |
|------|--------|--------|---------|
| `net.core.rmem_max` | 212992 | 134217728 (128MB) | socket 接收缓冲区最大值 |
| `net.core.wmem_max` | 212992 | 134217728 (128MB) | socket 发送缓冲区最大值 |
| `net.ipv4.tcp_rmem` | 4096 87380 6291456 | 4096 131072 67108864 | TCP接收缓冲区(最小/默认/最大) |
| `net.ipv4.tcp_wmem` | 4096 16384 4194304 | 4096 131072 67108864 | TCP发送缓冲区(最小/默认/最大) |
| `net.ipv4.tcp_moderate_rcvbuf` | 1 | 1 | TCP自动调整缓冲区(保持开启) |

### 端口与文件描述符

| 参数 | 默认值 | 建议值 | 场景说明 |
|------|--------|--------|---------|
| `net.ipv4.ip_local_port_range` | 32768 60999 | 1024 65535 | 本地端口范围（连接发起方） |
| `fs.file-max` | 取决内存 | 2097152 | 系统文件描述符总限制 |

### 拥塞控制

| 参数 | 默认值 | 建议值 | 场景说明 |
|------|--------|--------|---------|
| `net.ipv4.tcp_congestion_control` | cubic | bbr | BBR适合高延迟/丢包网络 |
| `net.core.default_qdisc` | pfifo_fast | fq | BBR推荐搭配fq队列 |

### conntrack

| 参数 | 默认值 | 建议值 | 场景说明 |
|------|--------|--------|---------|
| `net.netfilter.nf_conntrack_max` | 65536 | 1048576 | conntrack表大小（需iptables） |
| `net.netfilter.nf_conntrack_tcp_timeout_established` | 432000 (5天) | 600 | 已建立连接超时(秒) |
| `net.netfilter.nf_conntrack_tcp_timeout_time_wait` | 120 | 60 | TIME_WAIT超时(秒) |

---

## 四、I/O 参数

| 参数 | 默认值 | 建议值 | 场景说明 |
|------|--------|--------|---------|
| `/sys/block/sdX/queue/scheduler` | mq-deadline/none | 见磁盘调优文档 | I/O调度器 |
| `/sys/block/sdX/queue/nr_requests` | 64/128 | 256（SSD）| 磁盘请求队列深度 |
| `/sys/block/sdX/queue/read_ahead_kb` | 128 | 2048（顺序读）| 预读缓冲大小(KB) |

---

## 五、文件系统参数

| 参数 | 默认值 | 建议值 | 场景说明 |
|------|--------|--------|---------|
| `fs.inotify.max_user_watches` | 8192 | 524288 | inotify 监控文件数（IDE/容器场景） |
| `fs.inotify.max_user_instances` | 128 | 512 | inotify 实例数 |
| `fs.aio-max-nr` | 65536 | 1048576 | 异步 I/O 请求数上限 |
| `fs.nr_open` | 1048576 | 2097152 | 单进程最大打开文件数 |

---

## 六、一键查看所有关键参数现状

```bash
echo "=== 内存参数 ===" && \
sysctl vm.swappiness vm.dirty_ratio vm.dirty_background_ratio vm.min_free_kbytes vm.overcommit_memory 2>/dev/null

echo "=== CPU/调度参数 ===" && \
sysctl kernel.sched_min_granularity_ns kernel.sched_migration_cost_ns kernel.numa_balancing 2>/dev/null

echo "=== 网络参数 ===" && \
sysctl net.core.somaxconn net.ipv4.tcp_tw_reuse net.ipv4.tcp_fin_timeout \
  net.ipv4.ip_local_port_range net.ipv4.tcp_congestion_control \
  net.core.rmem_max net.core.wmem_max 2>/dev/null

echo "=== 文件描述符 ===" && \
sysctl fs.file-max fs.file-nr fs.inotify.max_user_watches 2>/dev/null
```

---

## 七、完整持久化配置文件模板

```bash
cat > /etc/sysctl.d/99-perf-master.conf << 'EOF'
# linux-perf-master 调优配置
# 生成时间：$(date)
# 原始值备份：sysctl -a > /tmp/sysctl_backup_$(date +%Y%m%d).txt

# ── 内存 ──────────────────────────────────
vm.swappiness = 10
vm.min_free_kbytes = 131072
vm.dirty_ratio = 10
vm.dirty_background_ratio = 5
vm.dirty_expire_centisecs = 1500
vm.dirty_writeback_centisecs = 500

# ── CPU 调度 ──────────────────────────────
kernel.sched_min_granularity_ns = 10000000
kernel.sched_wakeup_granularity_ns = 15000000
kernel.sched_migration_cost_ns = 5000000

# ── 网络 TCP ─────────────────────────────
net.ipv4.tcp_tw_reuse = 1
net.ipv4.tcp_fin_timeout = 30
net.ipv4.tcp_max_tw_buckets = 262144
net.ipv4.tcp_keepalive_time = 600
net.ipv4.tcp_keepalive_intvl = 30
net.ipv4.tcp_keepalive_probes = 5
net.ipv4.tcp_syncookies = 1

# ── 网络队列 ─────────────────────────────
net.core.somaxconn = 65535
net.ipv4.tcp_max_syn_backlog = 65535
net.core.netdev_max_backlog = 65535

# ── 网络缓冲区 ───────────────────────────
net.core.rmem_max = 134217728
net.core.wmem_max = 134217728
net.ipv4.tcp_rmem = 4096 131072 67108864
net.ipv4.tcp_wmem = 4096 131072 67108864
net.ipv4.tcp_moderate_rcvbuf = 1

# ── 端口与文件描述符 ─────────────────────
net.ipv4.ip_local_port_range = 1024 65535
fs.file-max = 2097152
fs.inotify.max_user_watches = 524288

# ── 拥塞控制（需内核4.9+） ───────────────
net.ipv4.tcp_congestion_control = bbr
net.core.default_qdisc = fq
EOF

# 使配置生效
sysctl --system

# 验证
sysctl -p /etc/sysctl.d/99-perf-master.conf
```

---

## 八、回滚所有更改

```bash
# 方案1：临时回滚（重启失效，但立即生效）
sysctl -w vm.swappiness=60
sysctl -w vm.dirty_ratio=20
# ... 逐一回滚

# 方案2：删除配置文件并重新加载
rm /etc/sysctl.d/99-perf-master.conf
sysctl --system
# 注意：已通过 sysctl -w 临时设置的值不会自动还原，需手动回滚
```