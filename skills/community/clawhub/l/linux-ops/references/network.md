# 网络诊断

## 网络信息

```bash
ip addr                     # 网络接口
ip link                     # 接口状态
ip route                    # 路由表
hostname -I                 # IP 地址
cat /etc/resolv.conf        # DNS 配置
```

## 连接检查

```bash
ping -c 5 host              # 测试连通
telnet host 80              # 端口检查
nc -zv host 80              # 端口检查
traceroute host             # 路由追踪
mtr host                    # 更好的路由追踪
```

## 连接状态

```bash
netstat -tuln               # 监听端口
netstat -tun                # 已建立连接
ss -tuln                    # 监听端口
ss -tun                     # 已建立连接
lsof -i :80                 # 端口占用
```

## 抓包

```bash
tcpdump -i eth0             # 抓包
tcpdump -i eth0 port 80     # 指定端口
tcpdump -i eth0 host 192.168.1.100  # 指定主机
tcpdump -i eth0 -w capture.pcap     # 保存文件
```

## 防火墙

```bash
ufw status                  # 状态
ufw allow 80/tcp            # 允许端口
ufw deny 23                 # 拒绝端口
ufw enable                  # 启用
```

## DNS

```bash
nslookup example.com
dig example.com
dig @8.8.8.8 example.com
```
