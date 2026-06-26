# 基准测试工具集


## 目录

- [fio — 磁盘 I/O 基准](#fio-磁盘-io-基准)
- [sysbench — CPU / 内存基准](#sysbench-cpu-内存基准)
- [iperf3 — 网络基准](#iperf3-网络基准)
- [wrk / wrk2 — HTTP 基准](#wrk-wrk2-http-基准)
- [性能参考基准值](#性能参考基准值)
- [基准测试最佳实践](#基准测试最佳实践)
## fio — 磁盘 I/O 基准

```bash
# 安装
sudo apt install -y fio    # Debian/Ubuntu
sudo dnf install -y fio    # RHEL/CentOS

# 顺序读（模拟备份读取）
fio --name=seq-read --ioengine=libaio --direct=1 --rw=read \
  --bs=1M --numjobs=4 --size=1G --runtime=60 --time_based --group_reporting

# 顺序写
fio --name=seq-write --ioengine=libaio --direct=1 --rw=write \
  --bs=1M --numjobs=4 --size=1G --runtime=60 --time_based --group_reporting

# 随机读 4K（模拟数据库 IOPS）
fio --name=rand-read --ioengine=libaio --direct=1 --rw=randread \
  --bs=4k --numjobs=16 --iodepth=64 --size=1G --runtime=60 --time_based --group_reporting

# 随机写 4K
fio --name=rand-write --ioengine=libaio --direct=1 --rw=randwrite \
  --bs=4k --numjobs=16 --iodepth=64 --size=1G --runtime=60 --time_based --group_reporting

# 混合读写 70/30（典型数据库负载）
fio --name=mixed --ioengine=libaio --direct=1 --rw=randrw --rwmixread=70 \
  --bs=4k --numjobs=8 --iodepth=32 --size=1G --runtime=60 --time_based --group_reporting
```

### fio 结果解读

| 指标 | 说明 |
|------|------|
| **IOPS** | 每秒 I/O 操作数（随机读写关注） |
| **BW (bandwidth)** | 带宽/吞吐量（顺序读写关注） |
| **lat (latency)** | 延迟（avg/p99 都要看） |
| **clat** | 完成延迟 |
| **slat** | 提交延迟 |

---

## sysbench — CPU / 内存基准

```bash
# 安装
sudo apt install -y sysbench

# CPU 基准（多线程）
sysbench cpu --threads=4 --time=30 run

# 内存基准
sysbench memory --threads=4 --time=30 \
  --memory-block-size=1K --memory-total-size=100G run

# MySQL 基准
sysbench oltp_read_write --db-driver=mysql --mysql-host=localhost \
  --mysql-user=root --mysql-db=sbtest --tables=10 --table-size=100000 \
  --threads=16 --time=60 prepare
sysbench oltp_read_write --db-driver=mysql --mysql-host=localhost \
  --mysql-user=root --mysql-db=sbtest --tables=10 --table-size=100000 \
  --threads=16 --time=60 run
```

---

## iperf3 — 网络基准

```bash
# 安装
sudo apt install -y iperf3

# 服务端
iperf3 -s

# TCP 吞吐测试
iperf3 -c <server-ip> -t 30 -P 4    # 30 秒，4 并行流

# UDP 丢包测试
iperf3 -c <server-ip> -u -b 1G -t 30

# 反向测试（服务端发送）
iperf3 -c <server-ip> -R -t 30

# 双向同时测试
iperf3 -c <server-ip> --bidir -t 30
```

---

## wrk / wrk2 — HTTP 基准

```bash
# 安装
sudo apt install -y wrk

# 基本测试（10 线程，400 连接，30 秒）
wrk -t 10 -c 400 -d 30s http://localhost:8080/api

# 带脚本（POST 请求等）
wrk -t 4 -c 100 -d 30s -s post.lua http://localhost:8080/api

# wrk2（恒定请求速率，更精确的延迟分布）
wrk2 -t 4 -c 100 -d 30s -R 10000 http://localhost:8080/api
```

---

## 性能参考基准值

> 以下数值为典型硬件上的参考范围，实际结果因硬件、内核版本、文件系统等差异较大。仅用于快速判断"结果是否合理"。

### fio 磁盘 I/O 参考

| 测试场景 | HDD (7200rpm) | SATA SSD | NVMe SSD | 云盘(SSD) |
|----------|:----------:|:--------:|:--------:|:---------:|
| 顺序读 (1M) | 100-200 MB/s | 400-550 MB/s | 2-7 GB/s | 100-500 MB/s |
| 顺序写 (1M) | 80-150 MB/s | 300-500 MB/s | 1-5 GB/s | 100-300 MB/s |
| 随机读 4K IOPS | 100-200 | 30K-90K | 200K-1M+ | 10K-100K |
| 随机写 4K IOPS | 100-200 | 20K-70K | 100K-500K | 10K-50K |
| 随机读 4K 延迟 | 5-15ms | 0.05-0.2ms | 0.01-0.1ms | 0.2-2ms |

### sysbench CPU 参考

| CPU 型号 | 单线程 events/s | 多线程 (4核) |
|----------|:-----------:|:----------:|
| Intel i5-12400 | ~3,500 | ~13,000 |
| Intel Xeon 8375C | ~2,500 | ~10,000 |
| AMD EPYC 9654 | ~3,000 | ~12,000 |
| Apple M2 | ~4,000 | ~15,000 |
| 云服务器 (通用型) | ~1,500-3,000 | ~6,000-12,000 |

### iperf3 网络参考

| 网络类型 | 典型吞吐 | 典型延迟 |
|----------|:--------:|:--------:|
| 千兆以太网 | 940 Mbps | < 1ms |
| 万兆以太网 | 9.4 Gbps | < 0.5ms |
| 25G 以太网 | 23+ Gbps | < 0.3ms |
| 同机房 (云) | 1-10 Gbps | 0.1-0.5ms |
| 跨可用区 (云) | 1-5 Gbps | 0.5-2ms |
| 跨地域 (云) | 100-500 Mbps | 10-100ms |

### wrk HTTP 参考

| 场景 | 框架 | 典型 QPS | 典型 p99 延迟 |
|------|------|:--------:|:----------:|
| Hello World | Nginx 静态 | 100K-500K | < 1ms |
| Hello World | Go net/http | 50K-200K | < 2ms |
| Hello World | Node.js Fastify | 30K-50K | < 5ms |
| JSON API | Go Gin | 30K-100K | 1-5ms |
| JSON API | Spring Boot | 10K-30K | 2-10ms |
| DB 查询 (简单) | 通用 | 5K-20K | 5-50ms |

> 💡 **如何判断结果好坏**：
> - 结果在参考范围内 → ✅ 正常
> - 低于参考范围 50% 以上 → ⚠️ 可能有瓶颈，需要排查
> - 低于参考范围 80% 以上 → 🔴 严重性能问题

---

## 基准测试最佳实践

1. **预热** — 跑几分钟预热后再采集数据
2. **多次运行** — 至少跑 3-5 次取中位数
3. **隔离变量** — 一次只改一个参数
4. **记录环境** — 记录硬件、内核版本、配置
5. **关注 p99** — 平均值会掩盖尾部延迟
6. **避免干扰** — 测试时关闭不相关服务
