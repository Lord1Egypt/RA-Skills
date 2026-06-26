# Linux 性能优化实战案例分析

> 本文档收录了5类典型场景的完整诊断→解决→验证流程，可作为遇到类似问题时的参考范本。

---

## 案例 1：MySQL 数据库服务器内存优化

**环境：** 16GB 内存，8核 CPU，MySQL 5.7  
**症状：** 系统响应变慢，偶尔出现连接超时，OOM killer 触发

### 诊断过程

```bash
# 检查内存使用
free -h
# available 仅 500MB（总16GB）

# 检查 OOM 日志
dmesg | grep -i oom
# 发现 MySQL 进程被杀死记录

# 检查 swappiness
sysctl vm.swappiness
# vm.swappiness = 60（默认值过高）

# 检查透明大页
cat /sys/kernel/mm/transparent_hugepage/enabled
# [always] madvise never ← 数据库场景应关闭
```

### 解决方案

```bash
# 1. 降低 swappiness（数据库推荐 1~10）
echo "vm.swappiness = 10" >> /etc/sysctl.conf
sysctl -p

# 2. 禁用透明大页
echo never > /sys/kernel/mm/transparent_hugepage/enabled
echo never > /sys/kernel/mm/transparent_hugepage/defrag
# 持久化（写入 systemd service，见 references/memory.md 第4节）

# 3. 优化 MySQL 配置（/etc/my.cnf）
# innodb_buffer_pool_size = 10G  # 物理内存的 70%
# innodb_log_file_size = 512M
# max_connections = 500

# 4. 保护 MySQL 进程不被 OOM Kill
echo -500 > /proc/$(pgrep mysqld)/oom_score_adj
```

### 验证效果

```bash
watch -n 1 'free -h'              # 内存可用量应稳定
sysctl vm.swappiness              # 确认值为 10
dmesg -w                          # 无新的 OOM 记录
cat /sys/kernel/mm/transparent_hugepage/enabled   # 应显示 never
```

### 经验总结

1. **数据库 swappiness 必须调低**（推荐 1~10）
2. **THP 会严重影响数据库性能**（MySQL/Redis/PostgreSQL 官方均建议关闭）
3. **innodb_buffer_pool_size 不超过物理内存的 70-80%**
4. **用 oom_score_adj 保护关键进程**

---

## 案例 2：Web 服务器高并发连接优化

**环境：** Nginx 反向代理，QPS 5000+  
**症状：** 高峰期报 "Cannot assign requested address"，连接错误率上升

### 诊断过程

```bash
# 检查连接状态（TIME_WAIT 爆炸）
ss -tan | awk '{print $1}' | sort | uniq -c
# TIME-WAIT: 15234（过多，端口濒临耗尽）

# 检查本地端口范围
sysctl net.ipv4.ip_local_port_range
# 32768 60999（约28000个端口，不够用）

# 检查文件描述符限制
ulimit -n
# 1024（严重过低）

# 检查队列溢出
netstat -s | grep -i listen
# "times the listen queue of a socket overflowed"（队列溢出）
```

### 解决方案

```bash
# 一键优化网络参数
cat > /etc/sysctl.d/99-highperf-web.conf << 'EOF'
net.ipv4.tcp_tw_reuse = 1
net.ipv4.tcp_fin_timeout = 30
net.ipv4.ip_local_port_range = 1024 65535
net.core.somaxconn = 65535
net.ipv4.tcp_max_syn_backlog = 8192
fs.file-max = 2097152
EOF
sysctl -p /etc/sysctl.d/99-highperf-web.conf

# 调整用户文件描述符限制
cat >> /etc/security/limits.conf << 'EOF'
nginx soft nofile 65535
nginx hard nofile 65535
EOF

# Nginx 配置同步调整
# events { worker_connections 65535; multi_accept on; use epoll; }
# http { keepalive_timeout 65; keepalive_requests 1000; }
```

### 验证效果

```bash
ss -tan | grep -c TIME-WAIT       # 从15000降至500
sysctl net.ipv4.ip_local_port_range  # 确认1024 65535
ab -n 100000 -c 1000 http://example.com/   # 错误率从5%降至0.01%
```

### 经验总结

1. **TIME_WAIT 过多=端口范围不够 + 未开启重用**
2. **默认端口范围只有28000个，高并发必须扩大**
3. **文件描述符默认1024，任何服务都需要调大**
4. **应用层 listen backlog 也要同步调大**

---

## 案例 3：日志服务器磁盘 I/O 瓶颈

**环境：** 日志聚合服务器，HDD 磁盘  
**症状：** 系统间歇性卡顿，命令响应慢，应用日志写入延迟

### 诊断过程

```bash
# 确认 iowait 高
top -bn1 | grep Cpu
# 45.2%wa（iowait 极高）

# 磁盘 I/O 统计
iostat -xz 1
# sda: %util=99.8%, await=150ms（严重拥塞）

# 找 I/O 密集进程
iotop -o
# rsyslogd 写入量最大

# 检查调度器
cat /sys/block/sda/queue/scheduler
# [mq-deadline]（HDD 应使用 bfq）

# 检查磁盘健康
smartctl -a /dev/sda | grep Reallocated
# Reallocated_Sector_Ct = 15（有坏道！）
```

### 解决方案

```bash
# 1. 切换为 bfq 调度器（HDD 公平调度）
echo bfq > /sys/block/sda/queue/scheduler

# 2. 优化脏页回写（减少写入积压）
sysctl -w vm.dirty_ratio=20
sysctl -w vm.dirty_background_ratio=5
sysctl -w vm.dirty_expire_centisecs=3000
sysctl -w vm.dirty_writeback_centisecs=500

# 3. 优化 rsyslog 异步写入（/etc/rsyslog.conf）
# $ActionQueueType LinkedList
# $ActionQueueFileName fwdRule1
# $ActionResumeRetryCount -1

# 4. 硬件层：规划 HDD 替换为 SSD 或专用日志磁盘
```

### 验证效果

```bash
watch -n 1 'iostat -x 1 2 | grep sda'
# await 从 150ms 降至 20ms，%util 从99%降至40%
```

### 经验总结

1. **HDD 使用 bfq，SSD 使用 mq-deadline**
2. **日志服务器应使用独立磁盘，不与系统盘共用**
3. **磁盘出现坏扇区要立即规划更换，不要等彻底损坏**
4. **脏页回写参数影响 I/O 尖峰行为**

---

## 案例 4：Java 应用内存泄漏排查

**环境：** Java 8，Heap 8GB  
**症状：** 运行几天后 OOM，GC 频率越来越高，Full GC 后内存不下降

### 诊断过程

```bash
# 监控内存趋势（每5秒）
watch -n 5 'ps -p $(pgrep java) -o rss,vsz'
# RSS 持续增长，没有回落

# 查看 GC 日志（JVM 参数需包含 -Xloggc:/var/log/gc.log）
tail -f /var/log/gc.log
# Full GC 频率越来越高，Old Gen 使用量不下降

# 生成堆转储
jmap -dump:format=b,file=/tmp/heap.hprof $(pgrep java)
# 使用 Eclipse MAT 或 jhat 分析 heap.hprof
```

### 解决方案

```bash
# 1. 优化 JVM 参数
JAVA_OPTS="-Xms8g -Xmx8g
  -XX:+UseG1GC
  -XX:MaxGCPauseMillis=200
  -XX:+HeapDumpOnOutOfMemoryError
  -XX:HeapDumpPath=/var/log/java/
  -XX:+PrintGCDetails
  -Xloggc:/var/log/gc.log
  -XX:+UseStringDeduplication"

# 2. 代码层面（根据堆转储分析结果）
# - 修复内存泄漏（未关闭的连接/流）
# - ThreadLocal 使用后调用 remove()
# - 避免静态集合持续增长

# 3. 操作系统保护
echo -500 > /proc/$(pgrep java)/oom_score_adj
```

### 验证效果

```bash
grep "Full GC" /var/log/gc.log | wc -l   # Full GC 次数显著减少
watch -n 10 'ps -p $(pgrep java) -o rss' # 内存稳定，不再持续增长
```

### 经验总结

1. **JVM 必须启用 GC 日志和 OOM 自动堆转储**
2. **G1 GC 适合大 Heap（>4GB）**
3. **ThreadLocal 是最常见的内存泄漏来源之一**
4. **监控比事后排查更重要**

---

## 案例 5：容器/K8s 资源争抢导致 Pod 变慢

**环境：** Kubernetes 多租户集群  
**症状：** Pod 间歇性变慢，日志出现 CPU throttled

### 诊断过程

```bash
# 检查 Pod 资源
kubectl top pods
kubectl describe pod <pod-name> | grep -A5 "Limits\|Requests"

# 检查 CPU throttling（关键！）
kubectl exec <pod> -- cat /sys/fs/cgroup/cpu/cpu.stat
# nr_throttled 持续增长 ← 说明被 CPU limit 限制

# 检查节点资源
kubectl top nodes
kubectl describe node <node-name> | grep -A10 "Allocated resources"

# 检查 OOM 事件
kubectl get events | grep OOMKilled
```

### 解决方案

```yaml
# 1. 合理调整 requests 和 limits
resources:
  requests:
    memory: "512Mi"
    cpu: "500m"
  limits:
    memory: "1Gi"
    cpu: "2000m"   # limit 设为 requests 的 2-4 倍，允许 burst

# 2. 关键服务使用 Guaranteed QoS（requests = limits）
resources:
  requests:
    memory: "1Gi"
    cpu: "1000m"
  limits:
    memory: "1Gi"
    cpu: "1000m"
```

```bash
# 3. 容器内系统调优（需要 privileged 权限或宿主机操作）
# 调整调度参数减少上下文切换
sysctl -w kernel.sched_min_granularity_ns=10000000

# 4. 宿主机节点预留系统资源（kubelet 配置）
# --system-reserved=cpu=1,memory=2Gi
# --kube-reserved=cpu=500m,memory=1Gi
```

### 验证效果

```bash
kubectl exec <pod> -- cat /sys/fs/cgroup/cpu/cpu.stat
# nr_throttled 停止增长

kubectl top pods --containers
# CPU 使用率在 requests 和 limits 之间波动（正常）
```

### 经验总结

1. **CPU throttling 是容器变慢最常见的隐性原因**
2. **limit 不要设得太小，应留 2-4 倍 burst 空间**
3. **关键服务用 Guaranteed QoS，保证资源不被抢占**
4. **节点必须预留足够的系统资源**

---

## 通用排查七步法

```
1. 收集症状
   └─ 用户反馈什么？监控告警了什么？从什么时候开始？

2. 确定范围
   └─ 单机问题 还是 全局问题？
   └─ 持续问题 还是 间歇问题？

3. 运行快照
   └─ bash scripts/collect_snapshot.sh > /tmp/snapshot.txt

4. 定位子系统
   └─ CPU / 内存 / 磁盘 / 网络？
   └─ 应用层 / 系统层 / 硬件层？

5. 深入分析
   └─ 查阅对应 references/*.md 文档
   └─ 使用专项工具（perf/iotop/ss/...）

6. 实施优化
   └─ 临时生效 → 观察效果 → 确认后持久化
   └─ 每次只改一个变量，方便定位效果

7. 文档记录
   └─ 问题原因 + 解决方案 + 经验教训
   └─ 更新性能基线数据
```