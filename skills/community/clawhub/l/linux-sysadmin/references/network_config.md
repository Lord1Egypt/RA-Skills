# 网络配置

## 目录

- [1. 网络接口管理](#1-网络接口管理)
- [2. IP 地址配置](#2-ip-地址配置)
- [3. 路由管理](#3-路由管理)
- [4. DNS 配置](#4-dns-配置)
- [5. 高级网络配置](#5-高级网络配置)
- [6. 网络诊断工具](#6-网络诊断工具)
- [7. 常见故障排查](#7-常见故障排查)

---

## 1. 网络接口管理

### 1.1 查看接口信息

```bash
# 查看所有接口（简洁）
ip -br addr
ip -br link

# 查看详细信息
ip addr show
ip addr show eth0

# 查看接口统计
ip -s link show eth0

# 传统命令（部分系统需安装 net-tools）
ifconfig -a
```

### 1.2 接口启停

```bash
# 启用/禁用接口
ip link set eth0 up
ip link set eth0 down

# 修改 MTU
ip link set eth0 mtu 9000   # 巨帧

# 修改 MAC 地址
ip link set eth0 down
ip link set eth0 address 00:11:22:33:44:55
ip link set eth0 up
```

---

## 2. IP 地址配置

### 2.1 临时配置（重启失效）

```bash
# 添加 IP 地址
ip addr add 10.0.0.100/24 dev eth0

# 删除 IP 地址
ip addr del 10.0.0.100/24 dev eth0

# 添加多个 IP（虚拟 IP）
ip addr add 10.0.0.101/24 dev eth0 label eth0:1
```

### 2.2 持久化配置 — NetworkManager（nmcli）

```bash
# 查看连接
nmcli con show
nmcli con show "eth0"

# 配置静态 IP
nmcli con mod "eth0" ipv4.method manual
nmcli con mod "eth0" ipv4.addresses "10.0.0.100/24"
nmcli con mod "eth0" ipv4.gateway "10.0.0.1"
nmcli con mod "eth0" ipv4.dns "8.8.8.8,8.8.4.4"
nmcli con up "eth0"

# 配置 DHCP
nmcli con mod "eth0" ipv4.method auto
nmcli con up "eth0"

# 创建新连接
nmcli con add type ethernet con-name "static-eth0" ifname eth0 \
  ipv4.method manual ipv4.addresses "10.0.0.100/24" \
  ipv4.gateway "10.0.0.1" ipv4.dns "8.8.8.8"

# 查看设备状态
nmcli dev status
```

### 2.3 持久化配置 — Netplan（Ubuntu 18.04+）

```yaml
# /etc/netplan/01-netcfg.yaml
network:
  version: 2
  renderer: networkd   # 或 NetworkManager
  ethernets:
    eth0:
      dhcp4: false
      addresses:
        - 10.0.0.100/24
      routes:
        - to: default
          via: 10.0.0.1
      nameservers:
        addresses:
          - 8.8.8.8
          - 8.8.4.4
```

```bash
# 应用配置
netplan apply

# 调试（不实际应用）
netplan try   # 120 秒后自动回滚
```

### 2.4 持久化配置 — 传统配置文件

```bash
# RHEL/CentOS（/etc/sysconfig/network-scripts/ifcfg-eth0）
TYPE=Ethernet
BOOTPROTO=static
NAME=eth0
DEVICE=eth0
ONBOOT=yes
IPADDR=10.0.0.100
NETMASK=255.255.255.0
GATEWAY=10.0.0.1
DNS1=8.8.8.8
DNS2=8.8.4.4

# Ubuntu 传统方式（/etc/network/interfaces）
auto eth0
iface eth0 inet static
    address 10.0.0.100
    netmask 255.255.255.0
    gateway 10.0.0.1
    dns-nameservers 8.8.8.8 8.8.4.4
```

---

## 3. 路由管理

### 3.1 查看路由表

```bash
# 查看路由表
ip route show
ip route show table all

# 查看特定目的地的路由
ip route get 8.8.8.8
```

### 3.2 静态路由

```bash
# 添加路由（临时）
ip route add 10.0.0.0/8 via 10.0.0.1
ip route add 172.16.0.0/12 via 10.0.0.1 dev eth0

# 添加默认路由
ip route add default via 10.0.0.1

# 删除路由
ip route del 10.0.0.0/8

# 持久化 — nmcli
nmcli con mod "eth0" +ipv4.routes "10.0.0.0/8 10.0.0.1"
nmcli con up "eth0"

# 持久化 — Netplan
# 在 ethernets.eth0.routes 中添加
# - to: 10.0.0.0/8
#   via: 10.0.0.1
```

### 3.3 策略路由

```bash
# 场景：双网卡，不同流量走不同出口

# 创建路由表
echo "100 isp1" >> /etc/iproute2/rt_tables
echo "200 isp2" >> /etc/iproute2/rt_tables

# 为不同源 IP 指定路由表
ip rule add from 10.0.0.100 table isp1
ip rule add from 10.0.0.101 table isp2

# 在各路由表中添加默认路由
ip route add default via 10.0.0.1 table isp1
ip route add default via 252.227.81.8 table isp2

# 查看策略规则
ip rule show
```

---

## 4. DNS 配置

### 4.1 基本配置

```bash
# 直接编辑（可能被 NetworkManager 覆盖）
cat > /etc/resolv.conf << 'EOF'
nameserver 8.8.8.8
nameserver 8.8.4.4
search example.com
options timeout:2 attempts:3
EOF

# 防止被覆盖
chattr +i /etc/resolv.conf
# 取消保护
chattr -i /etc/resolv.conf
```

### 4.2 systemd-resolved

```bash
# 查看 DNS 状态
resolvectl status
# 或
systemd-resolve --status

# 配置（/etc/systemd/resolved.conf）
[Resolve]
DNS=8.8.8.8 8.8.4.4
FallbackDNS=8.8.8.8
Domains=example.com
DNSSEC=no
DNSOverTLS=no
Cache=yes

# 重启
systemctl restart systemd-resolved

# 测试解析
resolvectl query www.example.com
```

### 4.3 hosts 文件

```bash
# /etc/hosts（优先于 DNS 查询）
127.0.0.1   localhost
10.0.0.100  myserver.example.com myserver

# 查看解析顺序
cat /etc/nsswitch.conf | grep hosts
# hosts: files dns  → 先查 /etc/hosts，再查 DNS
```

---

## 5. 高级网络配置

### 5.1 VLAN

```bash
# 加载 8021q 模块
modprobe 8021q

# 创建 VLAN 接口（临时）
ip link add link eth0 name eth0.100 type vlan id 100
ip addr add 10.0.0.100/24 dev eth0.100
ip link set eth0.100 up

# nmcli 方式（持久化）
nmcli con add type vlan con-name vlan100 dev eth0 id 100 \
  ipv4.method manual ipv4.addresses "10.0.0.100/24"
```

### 5.2 Bond（链路聚合）

```bash
# nmcli 创建 Bond
# 创建 bond 主接口
nmcli con add type bond con-name bond0 ifname bond0 \
  bond.options "mode=802.3ad,miimon=100,lacp_rate=fast"

# 添加从接口
nmcli con add type ethernet con-name bond0-slave1 ifname eth0 master bond0
nmcli con add type ethernet con-name bond0-slave2 ifname eth1 master bond0

# 配置 IP
nmcli con mod bond0 ipv4.method manual ipv4.addresses "10.0.0.100/24" \
  ipv4.gateway "10.0.0.1"

# 启用
nmcli con up bond0

# 查看 Bond 状态
cat /proc/net/bonding/bond0

# Bond 模式说明：
# mode=0 (balance-rr)   — 轮询，负载均衡
# mode=1 (active-backup) — 主备，高可用（最常用）
# mode=2 (balance-xor)  — 基于 MAC 哈希
# mode=4 (802.3ad)      — LACP，需交换机支持（性能最好）
# mode=6 (balance-alb)  — 自适应负载均衡
```

### 5.3 Bridge（网桥）

```bash
# nmcli 创建网桥
nmcli con add type bridge con-name br0 ifname br0 \
  ipv4.method manual ipv4.addresses "10.0.0.100/24" \
  ipv4.gateway "10.0.0.1"

# 将物理接口加入网桥
nmcli con add type ethernet con-name br0-port1 ifname eth0 master br0

# 启用
nmcli con up br0

# 查看网桥
bridge link show
```

---

## 6. 网络诊断工具

### 6.1 连通性测试

```bash
# ping（ICMP）
ping -c 5 8.8.8.8
ping -c 5 -s 1472 -M do 8.8.8.8   # 测试 MTU（1472+28=1500）

# traceroute（路径追踪）
traceroute 8.8.8.8
traceroute -T -p 80 8.8.8.8   # TCP 模式

# mtr（持续追踪，综合 ping + traceroute）
mtr -r -c 100 8.8.8.8
```

### 6.2 DNS 诊断

```bash
# dig（推荐）
dig www.example.com
dig @8.8.8.8 www.example.com    # 指定 DNS 服务器
dig +trace www.example.com       # 完整解析链路
dig -x 10.0.0.100                # 反向解析

# nslookup
nslookup www.example.com
nslookup www.example.com 8.8.8.8

# host
host www.example.com
```

### 6.3 端口与连接

```bash
# ss（推荐，替代 netstat）
ss -tlnp          # TCP 监听端口
ss -ulnp          # UDP 监听端口
ss -ant            # 所有 TCP 连接
ss -s              # 连接统计

# nc（端口测试）
nc -zv host 80           # TCP 端口测试
nc -zvu host 53          # UDP 端口测试
nc -l 8080               # 监听端口（简单服务器）

# 端口扫描
nmap -sT -p 1-1024 host   # TCP 扫描
```

### 6.4 抓包

```bash
# tcpdump
tcpdump -i eth0 -nn port 80               # 指定端口
tcpdump -i eth0 -nn host 10.0.0.100         # 指定主机
tcpdump -i eth0 -nn -w capture.pcap        # 保存到文件
tcpdump -i eth0 -nn -c 100 'tcp[tcpflags] & (tcp-syn) != 0'  # SYN 包

# 读取抓包文件
tcpdump -r capture.pcap -nn
```

---

## 7. 常见故障排查

### 网络不通

```bash
# 1. 检查接口状态
ip link show eth0   # 是否 UP？

# 2. 检查 IP 配置
ip addr show eth0   # IP 是否正确？

# 3. 检查网关
ip route show       # 默认路由是否存在？
ping -c 3 gateway   # 网关是否可达？

# 4. 检查 DNS
cat /etc/resolv.conf
dig www.example.com  # DNS 是否正常？

# 5. 检查防火墙
iptables -L -n      # 是否有 DROP 规则？

# 6. 检查 ARP
ip neigh show       # ARP 表是否正常？
arping -I eth0 gateway  # ARP 是否可达？
```

### DNS 解析失败

```bash
# 1. 检查 resolv.conf
cat /etc/resolv.conf

# 2. 直接测试 DNS 服务器
dig @8.8.8.8 www.example.com

# 3. 检查 systemd-resolved
resolvectl status

# 4. 检查 nsswitch.conf
grep hosts /etc/nsswitch.conf

# 5. 清除 DNS 缓存
resolvectl flush-caches
# 或
systemd-resolve --flush-caches
```

### 网络性能差

```bash
# 1. 带宽测试
iperf3 -c server-ip -t 30

# 2. 延迟测试
mtr -r -c 100 target-ip

# 3. 检查网卡错误
ip -s link show eth0
ethtool -S eth0 | grep -i error

# 4. 检查网卡速率
ethtool eth0 | grep Speed

# 5. 检查 TCP 重传
ss -ti | grep retrans
```
