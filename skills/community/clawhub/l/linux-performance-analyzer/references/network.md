# 网络调优参考手册

## 目录
1. [快速诊断](#1-快速诊断)
2. [TCP 连接状态优化](#2-tcp-连接状态优化)
3. [TCP 缓冲区调优](#3-tcp-缓冲区调优)
4. [连接队列优化](#4-连接队列优化)
5. [端口与文件描述符](#5-端口与文件描述符)
6. [BBR 拥塞控制](#6-bbr-拥塞控制)
7. [conntrack 连接跟踪](#7-conntrack-连接跟踪)
8. [网卡多队列与 RPS/RFS](#8-网卡多队列与-rpsrfs)
9. [网络延迟排查](#9-网络延迟排查)
10. [高并发服务完整配置示例](#10-高并发服务完整配置示例)

---

## 1. 快速诊断

```bash
# 连接状态统计
ss -s

# TCP 连接状态分布
ss -ant | awk '{print $1}' | sort | uniq -c | sort -rn

# 网络错误统计（关注非0项）
netstat -s 2>/dev/null | grep -E "fail|error|drop|overflow|reject|retransmit" | grep -v "^    0"

# 网络接口统计（RX/TX 错误）
ip -s link | grep -A5 "eth0\|ens\|bond"
netstat -i

# 网络连接数量
ss -ant | wc -l

# 实时网络流量
sar -n DEV 1 5 2>/dev/null || ip -s link

# conntrack 状态
cat /proc/sys/net/netfilter/nf_conntrack_count 2>/dev/null
cat /proc/sys/net/netfilter/nf_conntrack_max 2>/dev/null
```

**关键指标解读：**
| 指标 | 正常 | 告警 |
|------|------|------|
| TIME_WAIT 数量 | < 5000 | > 10000（端口耗尽风险） |
| CLOSE_WAIT 数量 | < 100 | > 1000（代码未关闭连接） |
| 重传率 | < 0.1% | > 1% |
| conntrack 使用率 | < 60% | > 80% |

---

## 2. TCP 连接状态优化

```bash
# 查看当前参数
sysctl net.ipv4.tcp_tw_reuse
sysctl net.ipv4.tcp_fin_timeout
sysctl net.ipv4.tcp_keepalive_time

# TIME_WAIT 优化（高并发短连接场景）
# 启用 TIME_WAIT 连接重用
sysctl -w net.ipv4.tcp_tw_reuse=1       # 允许重用 TIME_WAIT socket（连接发起方）
# ⚠️ tcp_tw_recycle 在内核 4.12+ 已移除，勿使用

# 缩短 FIN_TIMEOUT（加速 TIME_WAIT 回收）
sysctl -w net.ipv4.tcp_fin_timeout=30   # 默认60s，缩短到30s

# TIME_WAIT bucket 数量（防止 TIME_WAIT 桶溢出）
sysctl -w net.ipv4.tcp_max_tw_buckets=262144   # 默认180000

# Keepalive 优化（长连接场景）
sysctl -w net.ipv4.tcp_keepalive_time=600      # 600s 无数据后发探测（默认7200s）
sysctl -w net.ipv4.tcp_keepalive_intvl=30      # 探测间隔30s
sysctl -w net.ipv4.tcp_keepalive_probes=5      # 发5次探测后断开

# CLOSE_WAIT 过多（通常是代码问题，应用层未调用 close()）
# 快速定位：查看哪个进程持有大量 CLOSE_WAIT
ss -antp state close-wait | awk '{print $NF}' | sort | uniq -c | sort -rn | head -10

# 持久化
cat >> /etc/sysctl.d/99-perf-master.conf << 'EOF'
net.ipv4.tcp_tw_reuse = 1
net.ipv4.tcp_fin_timeout = 30
net.ipv4.tcp_max_tw_buckets = 262144
net.ipv4.tcp_keepalive_time = 600
net.ipv4.tcp_keepalive_intvl = 30
net.ipv4.tcp_keepalive_probes = 5
EOF
```

---

## 3. TCP 缓冲区调优

```bash
# 查看当前缓冲区设置
sysctl net.core.rmem_max net.core.wmem_max
sysctl net.ipv4.tcp_rmem net.ipv4.tcp_wmem

# 高带宽场景优化（万兆网络 / 高延迟 WAN）
# BDP (带宽延迟积) = 带宽 × RTT
# 例：10Gbps × 50ms RTT → BDP = 62.5MB

# 增大 Socket 缓冲区
sysctl -w net.core.rmem_max=134217728     # 128MB
sysctl -w net.core.wmem_max=134217728     # 128MB
sysctl -w net.core.rmem_default=262144    # 256KB
sysctl -w net.core.wmem_default=262144    # 256KB

# TCP 自动调整缓冲区（最小/默认/最大）
sysctl -w net.ipv4.tcp_rmem="4096 131072 67108864"   # 4KB/128KB/64MB
sysctl -w net.ipv4.tcp_wmem="4096 131072 67108864"

# 启用 TCP 缓冲区自动调整
sysctl -w net.ipv4.tcp_moderate_rcvbuf=1

# 内存缓冲区总量（TCP 使用的总内存：最小/压力/最大，单位页）
sysctl -w net.ipv4.tcp_mem="262144 524288 1048576"

# 高并发低延迟场景（减小缓冲区，降低延迟）
sysctl -w net.ipv4.tcp_rmem="4096 32768 1048576"
sysctl -w net.ipv4.tcp_wmem="4096 32768 1048576"

# 持久化
cat >> /etc/sysctl.d/99-perf-master.conf << 'EOF'
net.core.rmem_max = 134217728
net.core.wmem_max = 134217728
net.ipv4.tcp_rmem = 4096 131072 67108864
net.ipv4.tcp_wmem = 4096 131072 67108864
net.ipv4.tcp_moderate_rcvbuf = 1
EOF
```

---

## 4. 连接队列优化

```bash
# 查看当前队列设置
sysctl net.core.somaxconn
sysctl net.ipv4.tcp_max_syn_backlog
sysctl net.core.netdev_max_backlog

# 检查队列溢出（关注 "times the listen queue" 行）
netstat -s | grep -i listen
ss -lnt   # 查看各 LISTEN 端口的 Recv-Q（应接近0）

# 高并发服务优化
sysctl -w net.core.somaxconn=65535            # accept 队列大小（默认4096）
sysctl -w net.ipv4.tcp_max_syn_backlog=65535  # SYN 队列大小（默认1024）
sysctl -w net.core.netdev_max_backlog=65535   # 网卡接收队列（默认1000）

# 开启 SYN Cookie（防 SYN Flood 同时保证 SYN 队列不溢出）
sysctl -w net.ipv4.tcp_syncookies=1

# ⚠️ somaxconn 设置后，应用层 listen(fd, backlog) 的 backlog 也要同步调大
# Nginx: listen 80 backlog=65535;
# Java: new ServerSocket(port, 65535);

# 持久化
cat >> /etc/sysctl.d/99-perf-master.conf << 'EOF'
net.core.somaxconn = 65535
net.ipv4.tcp_max_syn_backlog = 65535
net.core.netdev_max_backlog = 65535
net.ipv4.tcp_syncookies = 1
EOF
```

---

## 5. 端口与文件描述符

```bash
# 查看本地端口范围
sysctl net.ipv4.ip_local_port_range   # 默认：32768 60999（约28000个）

# 扩大端口范围（主动发起大量连接的服务）
sysctl -w net.ipv4.ip_local_port_range="1024 65535"   # 约64000个

# 查看文件描述符限制
ulimit -n          # 当前进程限制
cat /proc/sys/fs/file-max   # 系统全局限制
cat /proc/sys/fs/file-nr    # 已分配/空闲/最大

# 增大文件描述符（系统级）
sysctl -w fs.file-max=2097152

# 增大文件描述符（用户级，/etc/security/limits.conf）
cat >> /etc/security/limits.conf << 'EOF'
* soft nofile 65535
* hard nofile 65535
root soft nofile 65535
root hard nofile 65535
EOF

# 当前 session 临时生效
ulimit -n 65535

# 针对特定服务（systemd unit）
# [Service]
# LimitNOFILE=65535

# 验证服务的文件描述符限制
cat /proc/<PID>/limits | grep "open files"

# 持久化
cat >> /etc/sysctl.d/99-perf-master.conf << 'EOF'
fs.file-max = 2097152
net.ipv4.ip_local_port_range = 1024 65535
EOF
```

---

## 6. BBR 拥塞控制

```bash
# 查看当前拥塞控制算法
sysctl net.ipv4.tcp_congestion_control
cat /proc/sys/net/ipv4/tcp_available_congestion_control

# 开启 BBR（内核 4.9+，显著提升高延迟/丢包网络性能）
modprobe tcp_bbr 2>/dev/null
echo tcp_bbr >> /etc/modules-load.d/modules.conf

sysctl -w net.ipv4.tcp_congestion_control=bbr
sysctl -w net.core.default_qdisc=fq   # BBR 推荐搭配 fq 队列

# 验证
sysctl net.ipv4.tcp_congestion_control   # 应显示 bbr
lsmod | grep bbr

# 持久化
cat >> /etc/sysctl.d/99-perf-master.conf << 'EOF'
net.ipv4.tcp_congestion_control = bbr
net.core.default_qdisc = fq
EOF

# BBR 效果最显著的场景：
# - 广域网高延迟（跨地域）
# - 有一定丢包率（1-5%）的网络
# - 大文件传输

# 回滚
sysctl -w net.ipv4.tcp_congestion_control=cubic
```

---

## 7. conntrack 连接跟踪

```bash
# 查看 conntrack 使用情况
cat /proc/sys/net/netfilter/nf_conntrack_count   # 当前连接数
cat /proc/sys/net/netfilter/nf_conntrack_max     # 最大连接数

# 使用率计算
count=$(cat /proc/sys/net/netfilter/nf_conntrack_count 2>/dev/null)
max=$(cat /proc/sys/net/netfilter/nf_conntrack_max 2>/dev/null)
echo "conntrack 使用率: $((count * 100 / max))% ($count/$max)"

# 扩大 conntrack 表
sysctl -w net.netfilter.nf_conntrack_max=1048576

# 缩短 conntrack 超时（减少表项占用）
sysctl -w net.netfilter.nf_conntrack_tcp_timeout_established=600   # 默认432000s(5天)→600s
sysctl -w net.netfilter.nf_conntrack_tcp_timeout_time_wait=60      # 默认120s→60s
sysctl -w net.netfilter.nf_conntrack_tcp_timeout_close_wait=60
sysctl -w net.netfilter.nf_conntrack_tcp_timeout_fin_wait=60

# 查看 conntrack 表内容
conntrack -L 2>/dev/null | head -20
conntrack -L 2>/dev/null | wc -l   # 统计条数

# ⚠️ conntrack 耗尽会导致新连接被拒绝，症状：
# kernel: nf_conntrack: table full, dropping packet.
# 监控：
dmesg | grep "nf_conntrack: table full" | tail -5

# 持久化
cat >> /etc/sysctl.d/99-perf-master.conf << 'EOF'
net.netfilter.nf_conntrack_max = 1048576
net.netfilter.nf_conntrack_tcp_timeout_established = 600
EOF
```

---

## 8. 网卡多队列与 RPS/RFS

```bash
# 查看网卡队列数
ls /sys/class/net/eth0/queues/
ethtool -l eth0 2>/dev/null | head -10

# 设置网卡多队列（需网卡支持）
ethtool -L eth0 combined 8   # 8个收发合并队列

# RPS（接收端包处理分发，软件模拟多队列）
# 将接收到的包分发到所有 CPU 处理
for rxq in /sys/class/net/eth0/queues/rx-*/rps_cpus; do
    echo ff > $rxq   # 所有CPU参与（ff=8核，ffff=16核）
done

# RFS（接收端流向目标，让数据包在发起进程的 CPU 上处理）
sysctl -w net.core.rps_sock_flow_entries=32768
for rxq in /sys/class/net/eth0/queues/rx-*/rps_flow_cnt; do
    echo 4096 > $rxq
done

# XPS（发送端分发，将不同流的包分配到不同 CPU）
for txq in /sys/class/net/eth0/queues/tx-*/xps_cpus; do
    echo ff > $txq
done

# 检查网卡中断绑核状态
cat /proc/interrupts | grep eth0

# 网卡 Ring Buffer 大小（减少丢包）
ethtool -g eth0 2>/dev/null     # 查看
ethtool -G eth0 rx 4096 tx 4096  # 设置4096
```

---

## 9. 网络延迟排查

```bash
# 基础延迟测量
ping -c 100 <target_ip> | tail -3   # 查看 avg/mdev

# 路由追踪（发现中间节点瓶颈）
traceroute -n <target_ip>
mtr --report --report-cycles 100 <target_ip>   # 更详细

# TCP 连接延迟（包含 DNS + TCP 握手 + TLS）
curl -o /dev/null -s -w "\n\
DNS:       %{time_namelookup}s\n\
Connect:   %{time_connect}s\n\
TLS:       %{time_appconnect}s\n\
TTFB:      %{time_starttransfer}s\n\
Total:     %{time_total}s\n" https://example.com

# 丢包测量
ping -c 1000 -i 0.01 <target_ip> | tail -3   # 快速ping 1000次

# 查看 TCP 重传详情
ss -ti dst <target_ip>   # 查看特定连接的重传统计

# 网络延迟抖动（jitter）
ping -c 100 <target_ip> | awk -F/ '/avg/ {print "jitter(mdev):", $5 "ms"}'

# 检查本地网络队列延迟
tc qdisc show dev eth0   # 查看队列规则
```

---

## 10. 高并发服务完整配置示例

> 适用：Nginx/Go/Node.js HTTP 服务，QPS 5000+，短连接为主

```bash
cat > /etc/sysctl.d/99-highperf-network.conf << 'EOF'
# === 连接队列 ===
net.core.somaxconn = 65535
net.ipv4.tcp_max_syn_backlog = 65535
net.core.netdev_max_backlog = 65535
net.ipv4.tcp_syncookies = 1

# === TIME_WAIT 优化 ===
net.ipv4.tcp_tw_reuse = 1
net.ipv4.tcp_fin_timeout = 30
net.ipv4.tcp_max_tw_buckets = 262144

# === 端口范围 ===
net.ipv4.ip_local_port_range = 1024 65535

# === 文件描述符 ===
fs.file-max = 2097152

# === TCP 缓冲区 ===
net.core.rmem_max = 134217728
net.core.wmem_max = 134217728
net.ipv4.tcp_rmem = 4096 131072 67108864
net.ipv4.tcp_wmem = 4096 131072 67108864
net.ipv4.tcp_moderate_rcvbuf = 1

# === Keepalive ===
net.ipv4.tcp_keepalive_time = 600
net.ipv4.tcp_keepalive_intvl = 30
net.ipv4.tcp_keepalive_probes = 5

# === BBR 拥塞控制 ===
net.ipv4.tcp_congestion_control = bbr
net.core.default_qdisc = fq

# === conntrack ===
net.netfilter.nf_conntrack_max = 1048576
net.netfilter.nf_conntrack_tcp_timeout_established = 600
EOF

sysctl -p /etc/sysctl.d/99-highperf-network.conf

# 验证生效
sysctl net.core.somaxconn
sysctl net.ipv4.tcp_congestion_control
ss -s
```