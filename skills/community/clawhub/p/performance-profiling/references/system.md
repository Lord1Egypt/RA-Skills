# 系统性能

## CPU

```bash
top -o %CPU
htop
mpstat 1

# CPU 信息
lscpu
cat /proc/cpuinfo
nproc

# 负载
cat /proc/loadavg
uptime
```

## 内存

```bash
free -h
vmstat 1

# 进程内存
pmap -x PID
cat /proc/PID/status | grep Vm

# 内存泄漏
valgrind --leak-check=full ./program
```

## I/O

```bash
iostat -x 1
iotop

# 进程 I/O
pidstat -d 1
cat /proc/PID/io

# 打开的文件
lsof
lsof -p PID
```

## 火焰图

```bash
# perf
perf record -g -p PID
perf report

# 生成火焰图
git clone https://github.com/brendangregg/FlameGraph
perf script | FlameGraph/stackcollapse-perf.pl | FlameGraph/flamegraph.pl > flame.svg
```

## 综合

```bash
vmstat 1                    # 内存、CPU、I/O
sar -u 1 5                  # CPU
sar -r 1 5                  # 内存
sar -d 1 5                  # 磁盘
sar -n DEV 1 5              # 网络
```
