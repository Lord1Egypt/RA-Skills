# 容器与 K8s 性能调优

> 覆盖 Docker/containerd 容器运行时和 Kubernetes 环境下的性能诊断、资源配置、CPU throttling、内存管理、网络优化等核心场景。

## 目录

- [容器性能诊断快速入门](#容器性能诊断快速入门)
- [cgroup v1 vs v2](#cgroup-v1-vs-v2)
- [CPU Throttling 排查与优化](#cpu-throttling-排查与优化)
- [容器内存管理](#容器内存管理)
- [K8s 资源配置最佳实践](#k8s-资源配置最佳实践)
- [容器内核参数限制](#容器内核参数限制)
- [语言运行时容器感知](#语言运行时容器感知)
- [Service Mesh 性能影响与优化](#service-mesh-性能影响与优化)
- [容器网络性能](#容器网络性能)
- [容器 I/O 性能](#容器-io-性能)
- [K8s 性能监控](#k8s-性能监控)
- [常见问题排查](#常见问题排查)

---

## 容器性能诊断快速入门

### 容器内快速检查

```bash
# ① 查看 cgroup 版本
stat -fc %T /sys/fs/cgroup/ 2>/dev/null
# cgroup2fs → v2, tmpfs → v1

# ② CPU 限制
# cgroup v1
cat /sys/fs/cgroup/cpu/cpu.cfs_quota_us 2>/dev/null
cat /sys/fs/cgroup/cpu/cpu.cfs_period_us 2>/dev/null
# cgroup v2
cat /sys/fs/cgroup/cpu.max 2>/dev/null

# ③ 内存限制
# cgroup v1
cat /sys/fs/cgroup/memory/memory.limit_in_bytes 2>/dev/null
cat /sys/fs/cgroup/memory/memory.usage_in_bytes 2>/dev/null
# cgroup v2
cat /sys/fs/cgroup/memory.max 2>/dev/null
cat /sys/fs/cgroup/memory.current 2>/dev/null

# ④ CPU throttling 统计
# cgroup v1
cat /sys/fs/cgroup/cpu/cpu.stat 2>/dev/null
# cgroup v2
cat /sys/fs/cgroup/cpu.stat 2>/dev/null

# ⑤ 内存 OOM 事件
# cgroup v1
cat /sys/fs/cgroup/memory/memory.oom_control 2>/dev/null
# cgroup v2
cat /sys/fs/cgroup/memory.events 2>/dev/null

# ⑥ 实际可用 CPU 核数计算
QUOTA=$(cat /sys/fs/cgroup/cpu/cpu.cfs_quota_us 2>/dev/null || echo "-1")
PERIOD=$(cat /sys/fs/cgroup/cpu/cpu.cfs_period_us 2>/dev/null || echo "100000")
if [ "$QUOTA" != "-1" ]; then
    echo "CPU 限制: $(echo "scale=2; $QUOTA / $PERIOD" | bc) 核"
else
    echo "CPU 无限制"
fi
```

### 宿主机侧检查

```bash
# 查看容器资源使用
docker stats --no-stream

# K8s Pod 资源使用
kubectl top pods -n <namespace>
kubectl top nodes

# 查看 Pod 的 cgroup 路径
POD_ID=$(crictl pods --name <pod-name> -q)
crictl inspectp $POD_ID | grep cgroupsPath
```

---

## cgroup v1 vs v2

### 路径差异

| 资源 | cgroup v1 路径 | cgroup v2 路径 |
|------|---------------|---------------|
| CPU 配额 | `/sys/fs/cgroup/cpu/cpu.cfs_quota_us` | `/sys/fs/cgroup/cpu.max` |
| CPU 周期 | `/sys/fs/cgroup/cpu/cpu.cfs_period_us` | （合并到 cpu.max） |
| CPU 统计 | `/sys/fs/cgroup/cpu/cpu.stat` | `/sys/fs/cgroup/cpu.stat` |
| CPU 权重 | `/sys/fs/cgroup/cpu/cpu.shares` | `/sys/fs/cgroup/cpu.weight` |
| 内存限制 | `/sys/fs/cgroup/memory/memory.limit_in_bytes` | `/sys/fs/cgroup/memory.max` |
| 内存使用 | `/sys/fs/cgroup/memory/memory.usage_in_bytes` | `/sys/fs/cgroup/memory.current` |
| 内存事件 | `/sys/fs/cgroup/memory/memory.oom_control` | `/sys/fs/cgroup/memory.events` |
| I/O 限制 | `/sys/fs/cgroup/blkio/` | `/sys/fs/cgroup/io.max` |

### cgroup v2 cpu.max 格式

```bash
# 格式: $QUOTA $PERIOD
# 例如: 200000 100000 → 2 个 CPU 核
cat /sys/fs/cgroup/cpu.max
200000 100000
```

### cgroup v2 cpu.stat 字段

```text
usage_usec 12345678        # 总 CPU 使用时间（微秒）
user_usec 10000000         # 用户态 CPU 时间
system_usec 2345678        # 内核态 CPU 时间
nr_periods 56789           # 调度周期总数
nr_throttled 1234          # 被限流的周期数
throttled_usec 5678901     # 被限流的总时间（微秒）
```

---

## CPU Throttling 排查与优化

### 什么是 CPU Throttling

当容器在一个 CFS 调度周期（默认 100ms）内用完了 CPU 配额，内核会暂停该容器的所有线程，直到下一个周期开始。这就是 **CPU throttling**。

### 诊断 Throttling

```bash
# 方法一：直接读取 cgroup
# cgroup v1
cat /sys/fs/cgroup/cpu/cpu.stat
# nr_periods 56789       ← 总调度周期数
# nr_throttled 1234      ← 被限流的周期数
# throttled_time 5678901 ← 被限流的总纳秒数

# 计算限流比例
awk '/nr_periods/{p=$2} /nr_throttled/{t=$2} END{printf "限流比例: %.2f%%\n", t/p*100}' /sys/fs/cgroup/cpu/cpu.stat

# 方法二：K8s 中通过 Prometheus
# container_cpu_cfs_throttled_periods_total / container_cpu_cfs_periods_total

# 方法三：持续监控限流
watch -n 1 'cat /sys/fs/cgroup/cpu/cpu.stat'
```

### Throttling 判断标准

| 限流比例 | 严重程度 | 建议 |
|:--------:|:--------:|------|
| < 5% | ✅ 正常 | 偶尔突发，可接受 |
| 5% - 25% | ⚠️ 警告 | 影响延迟，应增加 CPU limit |
| > 25% | 🔴 严重 | 严重影响性能，必须调整 |

### 优化方案

#### 方案一：增加 CPU limit

```yaml
# K8s Pod spec
resources:
  requests:
    cpu: "1000m"      # 1 核
  limits:
    cpu: "2000m"      # 2 核（增加 headroom）
```

#### 方案二：去掉 CPU limit（推荐 Google/Zalando 实践）

```yaml
# 只设 request，不设 limit → 允许 burst
resources:
  requests:
    cpu: "1000m"
  # 不设 limits.cpu
```

> ⚠️ **注意**：去掉 CPU limit 会导致 Pod 变为 Burstable QoS，在节点资源紧张时可能被优先驱逐。

#### 方案三：调整 CFS 周期（需宿主机权限）

```bash
# 将 CFS 周期从 100ms 调整为 5ms（减少单次限流的延迟影响）
# 适用于延迟敏感型服务
echo 5000 > /sys/fs/cgroup/cpu/cpu.cfs_period_us
# 同步调整 quota 保持总 CPU 不变
# 例如原来 quota=200000/period=100000（2核）
# 改为 quota=10000/period=5000（仍然是 2 核）
echo 10000 > /sys/fs/cgroup/cpu/cpu.cfs_quota_us
```

---

## 容器内存管理

### OOM Kill 排查

```bash
# 容器内检查
dmesg | grep -i "oom\|killed process" | tail -20

# cgroup v1 OOM 事件
cat /sys/fs/cgroup/memory/memory.oom_control
# oom_kill_disable 0
# under_oom 0
# oom_kill 3    ← 已发生 3 次 OOM Kill

# cgroup v2 内存事件
cat /sys/fs/cgroup/memory.events
# low 0
# high 0
# max 5         ← 达到内存上限 5 次
# oom 3         ← OOM Kill 3 次
# oom_kill 3

# K8s 中查看 OOM 历史
kubectl describe pod <pod-name> | grep -A5 "Last State"
kubectl get events --field-selector reason=OOMKilling -n <namespace>
```

### 内存使用详情

```bash
# cgroup v1
cat /sys/fs/cgroup/memory/memory.stat
# cache 1234567890      ← 页缓存
# rss 987654321         ← 实际使用的物理内存
# mapped_file 123456789 ← 内存映射文件
# swap 0                ← Swap 使用量

# cgroup v2
cat /sys/fs/cgroup/memory.stat
# anon 987654321        ← 匿名页（堆/栈）
# file 1234567890       ← 文件页（缓存）
# shmem 12345678        ← 共享内存

# 内存使用率计算
USAGE=$(cat /sys/fs/cgroup/memory/memory.usage_in_bytes 2>/dev/null || cat /sys/fs/cgroup/memory.current 2>/dev/null)
LIMIT=$(cat /sys/fs/cgroup/memory/memory.limit_in_bytes 2>/dev/null || cat /sys/fs/cgroup/memory.max 2>/dev/null)
echo "内存使用: $(echo "scale=2; $USAGE / 1048576" | bc) MB / $(echo "scale=2; $LIMIT / 1048576" | bc) MB ($(echo "scale=1; $USAGE * 100 / $LIMIT" | bc)%)"
```

### 内存优化建议

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| 频繁 OOM Kill | limit 设置过低 | 增加 memory limit，分析内存使用模式 |
| 内存持续增长 | 内存泄漏 | 使用语言对应的内存分析工具 |
| cache 占用高 | 文件 I/O 频繁 | 正常行为，cache 可被回收 |
| RSS 突然飙高 | 大对象分配 | 检查应用日志、使用 pprof/MAT 分析 |

---

## K8s 资源配置最佳实践

### requests vs limits

| 参数 | 作用 | 设置建议 |
|------|------|---------|
| `requests.cpu` | 调度保证（节点必须有这么多空闲 CPU） | 设为应用稳态 CPU 使用量 |
| `limits.cpu` | CPU 硬上限（超过会 throttle） | 设为 requests 的 1.5-3 倍，或不设 |
| `requests.memory` | 调度保证 + OOM 评分依据 | 设为应用稳态内存使用量 |
| `limits.memory` | 内存硬上限（超过会 OOM Kill） | **必须设置**，设为 requests 的 1.2-1.5 倍 |

### QoS 类别

| QoS | 条件 | 驱逐优先级 | 适用场景 |
|-----|------|:----------:|---------|
| **Guaranteed** | 所有容器 requests = limits | 最后被驱逐 | 核心服务 |
| **Burstable** | 至少一个容器 requests ≠ limits | 中等 | 大部分服务 |
| **BestEffort** | 没有设置任何 requests/limits | 最先被驱逐 | 批处理任务 |

### 推荐配置模板

```yaml
# 延迟敏感型服务（API 网关、Web 服务）
resources:
  requests:
    cpu: "500m"
    memory: "512Mi"
  limits:
    # cpu: 不设置，允许 burst
    memory: "768Mi"

---
# CPU 密集型服务（计算、编码）
resources:
  requests:
    cpu: "2000m"
    memory: "1Gi"
  limits:
    cpu: "4000m"     # 允许 burst 到 4 核
    memory: "1.5Gi"

---
# 内存密集型服务（缓存、数据库）
resources:
  requests:
    cpu: "500m"
    memory: "4Gi"
  limits:
    cpu: "1000m"
    memory: "4Gi"    # Guaranteed QoS，防止 OOM 影响数据

---
# 批处理任务
resources:
  requests:
    cpu: "100m"
    memory: "256Mi"
  limits:
    cpu: "4000m"
    memory: "2Gi"
```

### VPA / HPA 配置

```yaml
# HPA - 水平自动扩缩
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: my-app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-app
  minReplicas: 2
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70    # CPU 使用率 > 70% 扩容
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 60    # 扩容冷却期
    scaleDown:
      stabilizationWindowSeconds: 300   # 缩容冷却期（防抖动）
```

---

## 容器内核参数限制

### 容器内可修改的 sysctl 参数

K8s 将 sysctl 分为 **safe** 和 **unsafe** 两类：

#### Safe sysctl（默认允许）

```yaml
# Pod spec 中直接设置
spec:
  securityContext:
    sysctls:
    - name: net.ipv4.ip_local_port_range
      value: "1024 65535"
    - name: net.ipv4.tcp_syncookies
      value: "1"
    - name: kernel.shm_rmid_forced
      value: "1"
```

#### Unsafe sysctl（需要集群管理员启用）

```yaml
# 需要在 kubelet 配置中启用
# --allowed-unsafe-sysctls='net.core.somaxconn,net.ipv4.tcp_tw_reuse'

spec:
  securityContext:
    sysctls:
    - name: net.core.somaxconn
      value: "65535"
    - name: net.ipv4.tcp_tw_reuse
      value: "1"
```

#### 必须在宿主机修改的参数

| 参数 | 原因 | 说明 |
|------|------|------|
| `vm.swappiness` | 全局内存策略 | 影响所有容器 |
| `vm.dirty_ratio` | 全局脏页策略 | 影响所有容器 |
| `vm.min_free_kbytes` | 全局内存保留 | 影响所有容器 |
| `kernel.sched_*` | CPU 调度器参数 | 影响所有容器 |
| `net.core.rmem_max` | 全局 socket 缓冲区 | 需宿主机设置 |
| `net.core.wmem_max` | 全局 socket 缓冲区 | 需宿主机设置 |
| `net.ipv4.tcp_rmem` | TCP 读缓冲区 | 需宿主机设置 |
| `net.ipv4.tcp_wmem` | TCP 写缓冲区 | 需宿主机设置 |

---

## 语言运行时容器感知

### Java

```bash
# Java 8u191+ / Java 11+ 默认启用容器感知
java -XX:+PrintFlagsFinal -version 2>&1 | grep UseContainerSupport
# bool UseContainerSupport = true

# 关键 JVM 参数
# -XX:+UseContainerSupport    启用容器感知（默认开启）
# -XX:MaxRAMPercentage=75.0   堆内存占容器 limit 的 75%
# -XX:InitialRAMPercentage=50.0  初始堆占 50%
# -XX:+UseG1GC               G1 GC（通用推荐）
java \
  -XX:+UseContainerSupport \
  -XX:MaxRAMPercentage=75.0 \
  -XX:InitialRAMPercentage=50.0 \
  -XX:+UseG1GC \
  -XX:MaxGCPauseMillis=200 \
  -jar app.jar

# ⚠️ 常见坑：
# 1. Java 8u131-8u190 需要手动启用: -XX:+UnlockExperimentalVMOptions -XX:+UseCGroupMemoryLimitForHeap
# 2. 不要同时设置 -Xmx 和 MaxRAMPercentage，-Xmx 优先级更高
# 3. 堆外内存（Metaspace/DirectByteBuffer/线程栈）不受 MaxRAMPercentage 控制
#    建议 memory limit = 堆内存 × 1.5（留 50% 给堆外）
```

### Go

```bash
# Go 1.19+ 支持 GOMEMLIMIT
# 自动感知 cgroup CPU 限制需要第三方库

# 方法一：设置 GOMEMLIMIT（推荐）
GOMEMLIMIT=3200MiB ./app    # 容器 limit 4Gi，设为 80%

# 方法二：使用 automaxprocs 自动适配 CPU
# import _ "go.uber.org/automaxprocs"
# 自动将 GOMAXPROCS 设为 cgroup CPU 配额

# ⚠️ 常见坑：
# 1. 默认 GOMAXPROCS = 宿主机 CPU 核数，不是容器配额
#    在 48 核宿主机上 limit 2 核，GOMAXPROCS=48 → 大量上下文切换
# 2. GOMEMLIMIT 应设为 memory limit 的 80-90%（留 buffer 给非堆内存）
# 3. Go 1.19 之前只有 GOGC，无法设硬上限
```

### Python

```python
# Python 没有内置容器感知
# 需要手动读取 cgroup 限制

import os
import multiprocessing

def get_cpu_limit():
    """获取容器 CPU 限制"""
    try:
        # cgroup v2
        with open('/sys/fs/cgroup/cpu.max') as f:
            quota, period = f.read().strip().split()
            if quota == 'max':
                return os.cpu_count()
            return int(quota) // int(period)
    except FileNotFoundError:
        pass
    try:
        # cgroup v1
        with open('/sys/fs/cgroup/cpu/cpu.cfs_quota_us') as f:
            quota = int(f.read().strip())
        with open('/sys/fs/cgroup/cpu/cpu.cfs_period_us') as f:
            period = int(f.read().strip())
        if quota == -1:
            return os.cpu_count()
        return max(1, quota // period)
    except FileNotFoundError:
        return os.cpu_count()

def get_memory_limit():
    """获取容器内存限制"""
    try:
        # cgroup v2
        with open('/sys/fs/cgroup/memory.max') as f:
            val = f.read().strip()
            return int(val) if val != 'max' else None
    except FileNotFoundError:
        pass
    try:
        # cgroup v1
        with open('/sys/fs/cgroup/memory/memory.limit_in_bytes') as f:
            val = int(f.read().strip())
            # 超大值表示无限制
            return val if val < 2**62 else None
    except FileNotFoundError:
        return None

# 使用示例
cpu_limit = get_cpu_limit()
print(f"CPU 限制: {cpu_limit} 核")
# 设置进程池/线程池大小
# pool = multiprocessing.Pool(cpu_limit)
```

### Node.js

```bash
# Node.js 12+ 自动感知容器内存限制
# 但默认 --max-old-space-size 可能不够

# 推荐设置
# --max-old-space-size=3072   容器 limit 4Gi，堆设为 75%
# --max-semi-space-size=64    新生代大小（高吞吐可增大）
node \
  --max-old-space-size=3072 \
  --max-semi-space-size=64 \
  app.js

# 或使用环境变量
NODE_OPTIONS="--max-old-space-size=3072" node app.js

# ⚠️ 常见坑：
# 1. Node.js 默认堆上限约 1.5GB（64位系统），容器 limit 更大时需手动设置
# 2. Worker Threads 每个 worker 有独立的 V8 堆，总内存 = 主线程 + N × worker 堆
# 3. 原生插件（C++ addon）的内存不受 V8 堆限制控制
```

### Rust

```bash
# Rust 没有 GC，内存管理由编译器保证，通常无需容器感知配置
# 但以下场景需要注意：

# 1. 线程数量：默认使用 num_cpus crate 获取 CPU 核数 → 可能获取到宿主机核数
#    解决方案：使用 num_cpus 0.14+（已支持 cgroup 感知）
#    或手动读取 cgroup CPU 配额
TOKIO_WORKER_THREADS=4 ./app    # 手动限制 tokio 工作线程数

# 2. Rayon 并行度：默认使用所有 CPU 核
RAYON_NUM_THREADS=4 ./app       # 限制 rayon 线程池大小

# 3. 内存分配器：jemalloc/mimalloc 在容器中表现更好
# Cargo.toml:
# [dependencies]
# tikv-jemallocator = "0.5"

# ⚠️ 常见坑：
# 1. num_cpus < 0.14 会读取宿主机 CPU 数（不感知 cgroup）
# 2. tokio 默认 worker 线程 = CPU 核数，在 48 核宿主机 limit 2 核时会创建 48 个线程
# 3. mmap 分配的内存不受 Rust 所有权管理，需注意容器内存限制
```

### C/C++

```bash
# C/C++ 程序通常直接使用系统调用，没有运行时容器感知
# 需要手动处理以下问题：

# 1. 获取容器 CPU 限制（而非宿主机 CPU 数）
# 不要使用 sysconf(_SC_NPROCESSORS_ONLN)，它返回宿主机 CPU 数
# 正确做法：读取 cgroup 文件
cat /sys/fs/cgroup/cpu.max 2>/dev/null || \
  echo "$(cat /sys/fs/cgroup/cpu/cpu.cfs_quota_us) $(cat /sys/fs/cgroup/cpu/cpu.cfs_period_us)"

# 2. 线程池大小应基于容器 CPU 配额，而非 std::thread::hardware_concurrency()
# C++ 示例：
# int get_container_cpus() {
#     // 优先读取 cgroup v2
#     std::ifstream f("/sys/fs/cgroup/cpu.max");
#     if (f.is_open()) {
#         std::string quota_s, period_s;
#         f >> quota_s >> period_s;
#         if (quota_s != "max") return std::max(1, std::stoi(quota_s) / std::stoi(period_s));
#     }
#     return std::thread::hardware_concurrency();
# }

# 3. 内存分配器选择
# glibc malloc 在容器中可能导致内存碎片
# 推荐：jemalloc 或 tcmalloc
LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libjemalloc.so ./app

# ⚠️ 常见坑：
# 1. std::thread::hardware_concurrency() 返回宿主机核数
# 2. /proc/cpuinfo 显示宿主机所有 CPU
# 3. glibc malloc 的 ARENA 数量默认 = 8 × CPU核数，在容器中会过多
#    设置 MALLOC_ARENA_MAX=4 限制 arena 数量
MALLOC_ARENA_MAX=4 ./app
```

---

## Service Mesh 性能影响与优化

### Sidecar 代理的性能开销

Service Mesh（如 Istio/Linkerd）通过 sidecar 代理拦截所有网络流量，会引入额外延迟和资源消耗：

| 指标 | 无 Service Mesh | Istio (Envoy) | Linkerd | 说明 |
|------|:--------------:|:--------------:|:-------:|------|
| 延迟增加 | 基线 | +2-10ms (p50) | +1-3ms (p50) | 取决于 mTLS 和策略复杂度 |
| CPU 开销 | 0 | 100-500m / pod | 50-200m / pod | sidecar 本身消耗 |
| 内存开销 | 0 | 50-150Mi / pod | 20-50Mi / pod | Envoy 占用较大 |
| 吞吐影响 | 基线 | -5~15% | -2~8% | 高并发场景更明显 |

### 诊断 Service Mesh 性能问题

```bash
# 1. 确认延迟是否来自 sidecar
# 对比 Pod 内直连 vs 经过 sidecar 的延迟
# Pod 内直接访问（绕过 sidecar）
kubectl exec -it <pod> -c app -- curl -w "%{time_total}\n" -o /dev/null -s http://localhost:8080/health
# 经过 sidecar 访问
kubectl exec -it <pod> -c app -- curl -w "%{time_total}\n" -o /dev/null -s http://<service-name>/health

# 2. 检查 Envoy sidecar 资源使用
kubectl top pod <pod-name> --containers
# 关注 istio-proxy 容器的 CPU 和内存

# 3. Envoy 统计信息
kubectl exec -it <pod> -c istio-proxy -- curl localhost:15000/stats | grep -E "upstream_rq|downstream_rq|cx_active"

# 4. 检查 mTLS 握手开销
kubectl exec -it <pod> -c istio-proxy -- curl localhost:15000/stats | grep ssl
```

### 优化方案

```yaml
# 1. 为 sidecar 分配足够资源（避免 CPU throttling）
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
spec:
  meshConfig:
    defaultConfig:
      concurrency: 2          # Envoy worker 线程数（匹配 CPU limit）
  values:
    global:
      proxy:
        resources:
          requests:
            cpu: "100m"
            memory: "128Mi"
          limits:
            cpu: "500m"       # 高流量服务需增大
            memory: "256Mi"
```

```yaml
# 2. 对延迟不敏感的内部服务禁用 mTLS
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: disable-mtls-internal
spec:
  selector:
    matchLabels:
      app: internal-batch-job
  mtls:
    mode: DISABLE
```

```yaml
# 3. 对不需要 mesh 功能的 Pod 跳过 sidecar 注入
metadata:
  annotations:
    sidecar.istio.io/inject: "false"    # 跳过 sidecar
```

```bash
# 4. Envoy 并发优化
# 默认 concurrency=2，高流量服务可增大
# 在 Pod annotation 中设置：
# sidecar.istio.io/proxyCPU: "500m"
# sidecar.istio.io/proxyMemory: "256Mi"
```

### 性能优化清单

| 优化项 | 预期效果 | 适用场景 |
|--------|---------|---------|
| 增大 sidecar CPU limit | 减少 throttling 延迟 | sidecar CPU 使用率 > 80% |
| 设置合理的 concurrency | 匹配 CPU 配额 | 高并发服务 |
| 禁用不需要的 mTLS | 减少 1-3ms 延迟 | 内部批处理服务 |
| 跳过 sidecar 注入 | 消除所有 mesh 开销 | 不需要 mesh 功能的服务 |
| 使用 Linkerd 替代 Istio | 更低的资源开销 | 只需要 mTLS + 可观测性 |
| 启用 HTTP/2 多路复用 | 减少连接建立开销 | gRPC / 高并发 HTTP |
| 使用 Istio ambient mesh | 无 sidecar 架构 | Istio 1.18+，减少资源开销 |

---

## 容器网络性能

### 常见网络模式性能对比

| 网络模式 | 延迟开销 | 吞吐影响 | 适用场景 |
|----------|:--------:|:--------:|---------|
| Host 网络 | 无 | 无 | 高性能网络服务 |
| Bridge (veth) | +10-30μs | -5~15% | 默认模式 |
| Overlay (VXLAN) | +50-100μs | -10~20% | 跨节点通信 |
| Calico (BGP) | +5-15μs | -2~5% | K8s 推荐 |
| Cilium (eBPF) | +2-10μs | -1~3% | 高性能 K8s |

### 容器内网络诊断

```bash
# 检查 DNS 解析延迟（K8s 常见瓶颈）
time nslookup kubernetes.default.svc.cluster.local

# 如果 DNS 慢（> 100ms），检查 CoreDNS
kubectl logs -n kube-system -l k8s-app=kube-dns --tail=50

# 检查 conntrack 表
cat /proc/sys/net/netfilter/nf_conntrack_count
cat /proc/sys/net/netfilter/nf_conntrack_max
# count 接近 max → conntrack 表满，会丢包

# 容器间网络延迟测试
# Pod A:
iperf3 -s
# Pod B:
iperf3 -c <pod-a-ip> -t 10
```

### K8s DNS 优化

```yaml
# Pod spec 中配置 DNS 策略
spec:
  dnsPolicy: ClusterFirst
  dnsConfig:
    options:
    - name: ndots
      value: "2"           # 默认 5，减少不必要的 DNS 查询
    - name: single-request-reopen
      value: ""            # 避免 DNS 查询丢包
    - name: timeout
      value: "2"
    - name: attempts
      value: "3"
```

> **ndots 优化说明**：K8s 默认 `ndots=5`，查询 `api.example.com` 时会先尝试 `api.example.com.default.svc.cluster.local` 等 5 次，最后才查外部 DNS。设为 2 可大幅减少无效 DNS 查询。

---

## 容器 I/O 性能

### I/O 限制配置

```yaml
# K8s 不直接支持 I/O 限制，需要通过 cgroup 或存储类配置

# Docker 运行时设置
docker run --device-read-bps /dev/sda:100mb --device-write-bps /dev/sda:50mb myapp

# cgroup v2 I/O 限制
echo "8:0 rbps=104857600 wbps=52428800" > /sys/fs/cgroup/io.max
```

### 容器存储性能建议

| 存储类型 | 性能 | 适用场景 |
|----------|------|---------|
| emptyDir (tmpfs) | 最快（内存速度） | 临时缓存、中间文件 |
| emptyDir (disk) | 快（本地磁盘） | 临时数据 |
| hostPath | 快（本地磁盘） | 需要持久化的本地数据 |
| PVC (local-storage) | 快 | 数据库、有状态服务 |
| PVC (网络存储) | 慢（取决于网络） | 共享存储 |
| PVC (云盘 SSD) | 中等 | 云环境通用 |

---

## K8s 性能监控

### Prometheus 关键指标

```promql
# CPU throttling 比例
sum(rate(container_cpu_cfs_throttled_periods_total{pod="my-pod"}[5m]))
/
sum(rate(container_cpu_cfs_periods_total{pod="my-pod"}[5m]))

# 内存使用率
container_memory_working_set_bytes{pod="my-pod"}
/
container_spec_memory_limit_bytes{pod="my-pod"}

# OOM Kill 次数
kube_pod_container_status_restarts_total{pod="my-pod"}

# 网络流量
sum(rate(container_network_receive_bytes_total{pod="my-pod"}[5m]))
sum(rate(container_network_transmit_bytes_total{pod="my-pod"}[5m]))

# 磁盘 I/O
sum(rate(container_fs_reads_bytes_total{pod="my-pod"}[5m]))
sum(rate(container_fs_writes_bytes_total{pod="my-pod"}[5m]))
```

### kubectl 快速诊断命令

```bash
# Pod 资源使用概览
kubectl top pods -n <namespace> --sort-by=cpu
kubectl top pods -n <namespace> --sort-by=memory

# 节点资源压力
kubectl describe node <node-name> | grep -A5 "Conditions"
# MemoryPressure, DiskPressure, PIDPressure

# Pod 事件（OOM、Eviction、FailedScheduling）
kubectl get events -n <namespace> --sort-by='.lastTimestamp' | tail -20

# Pod 详细状态
kubectl describe pod <pod-name> -n <namespace>

# 查看资源配额使用
kubectl describe resourcequota -n <namespace>
```

---

## 常见问题排查

### 问题 1：Pod 频繁 OOM Kill

```bash
# 排查步骤
# 1. 确认内存限制
kubectl describe pod <pod-name> | grep -A2 "Limits"

# 2. 查看内存使用趋势
kubectl top pod <pod-name> --containers

# 3. 进入容器查看详细内存
kubectl exec -it <pod-name> -- cat /sys/fs/cgroup/memory.stat

# 4. 检查是否内存泄漏
# Java: jmap -heap <PID>
# Go: curl localhost:6060/debug/pprof/heap > heap.out
# Python: tracemalloc
# Node.js: --inspect + Chrome DevTools
```

**解决方案优先级**：
1. 确认是否内存泄漏（修复代码）
2. 增加 memory limit
3. 优化应用内存使用（缓存策略、连接池大小）

### 问题 2：服务延迟抖动

```bash
# 排查步骤
# 1. 检查 CPU throttling
cat /sys/fs/cgroup/cpu/cpu.stat | grep throttled

# 2. 检查 GC 暂停（Java/Go）
# Java: -XX:+PrintGCDetails -Xloggc:/tmp/gc.log
# Go: GODEBUG=gctrace=1

# 3. 检查同节点是否有 noisy neighbor
kubectl top pods -n <namespace> --sort-by=cpu

# 4. 检查网络延迟
ping <service-ip>
```

**解决方案**：
1. 增加 CPU limit 或去掉 CPU limit
2. 调整 GC 参数
3. 使用 Pod Anti-Affinity 分散部署
4. 使用 PriorityClass 确保关键服务优先级

### 问题 3：Pod 调度失败 (Insufficient cpu/memory)

```bash
# 排查步骤
# 1. 查看节点资源分配情况
kubectl describe nodes | grep -A5 "Allocated resources"

# 2. 检查是否 requests 设置过高
kubectl get pods -n <namespace> -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.spec.containers[*].resources.requests}{"\n"}{end}'

# 3. 查看是否有资源碎片
kubectl describe nodes | grep -E "Capacity|Allocatable|Allocated"
```

**解决方案**：
1. 降低 requests（但不低于实际使用量）
2. 使用 VPA 自动调整 requests
3. 扩容集群节点
4. 使用 Pod Disruption Budget 平衡可用性

### 问题 4：容器启动慢

```bash
# 排查步骤
# 1. 镜像拉取时间
kubectl describe pod <pod-name> | grep -A2 "Events"
# 看 Pulling / Pulled 事件的时间差

# 2. 应用启动时间
kubectl logs <pod-name> --timestamps | head -20

# 3. 健康检查配置
kubectl describe pod <pod-name> | grep -A5 "Liveness\|Readiness\|Startup"
```

**优化方案**：
1. 使用小基础镜像（alpine / distroless）
2. 多阶段构建减小镜像体积
3. 配置 imagePullPolicy: IfNotPresent
4. 设置合理的 startupProbe（给应用足够启动时间）
5. 预热镜像（DaemonSet 预拉取）
