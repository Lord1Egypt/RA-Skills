# MikroTik RouterOS API 工具

MikroTik RouterOS API Python 客户端和命令行工具。

## 安装

无需安装，直接使用即可。依赖：Python 3.6+

## 用法

### 命令行工具

```bash
cd /root/.openclaw/workspace/tools/mikrotik-api

# 查看设备状态
python3 cli.py 192.168.1.1 status

# 查看防火墙规则
python3 cli.py 192.168.1.1 firewall

# 查看网络接口
python3 cli.py 192.168.1.1 interfaces

# 查看路由表
python3 cli.py 192.168.1.1 routes

# 执行自定义命令
python3 cli.py 192.168.1.1 cmd /system/resource/print

# 指定用户名密码
python3 cli.py 192.168.1.1 status -u admin -p yourpassword
```

### Python 库

```python
from mikrotik_api import MikroTikAPI, QuickCommands

# 连接设备
api = MikroTikAPI('192.168.1.1', username='admin', password='')
api.connect()
api.login()

# 方法 1: 使用快捷命令
quick = QuickCommands(api)
quick.print_status()  # 打印完整状态

# 获取系统资源
resource = quick.system.get_resource()
print(f"CPU 负载：{resource['cpu-load']}%")

# 获取防火墙规则
rules = quick.firewall.get_filter_rules()

# 获取网络接口
interfaces = quick.network.get_interfaces()

# 方法 2: 执行自定义命令
results = api.run_command('/system/resource/print')
for item in results:
    print(item)

# 断开连接
api.disconnect()
```

### 上下文管理器

```python
from mikrotik_api import MikroTikAPI, QuickCommands

with MikroTikAPI('192.168.1.1') as api:
    api.login()
    quick = QuickCommands(api)
    quick.print_status()
# 自动断开连接
```

## API 参考

### MikroTikAPI

| 方法 | 说明 |
|------|------|
| `connect()` | 建立连接 |
| `disconnect()` | 断开连接 |
| `login()` | 登录 |
| `run_command(cmd, args)` | 执行 API 命令 |

### SystemCommands

| 方法 | 说明 |
|------|------|
| `get_resource()` | 系统资源（CPU、内存等） |
| `get_identity()` | 设备标识 |
| `get_version()` | 系统版本 |
| `get_health()` | 健康状态（温度、电压） |
| `reboot()` | 重启设备 |
| `shutdown()` | 关闭设备 |

### FirewallCommands

| 方法 | 说明 |
|------|------|
| `get_filter_rules()` | 过滤规则 |
| `get_nat_rules()` | NAT 规则 |
| `get_mangle_rules()` | Mangle 规则 |
| `get_active_connections()` | 活动连接 |
| `get_connection_stats()` | 连接统计 |

### NetworkCommands

| 方法 | 说明 |
|------|------|
| `get_interfaces()` | 网络接口 |
| `get_ip_addresses()` | IP 地址配置 |
| `get_routes()` | 路由表 |
| `get_dns()` | DNS 配置 |
| `get_dhcp_leases()` | DHCP 租约 |
| `get_arp()` | ARP 表 |
| `get_neighbors()` | 邻居发现 |

## 常用命令路径

```
# 系统
/system/resource/print
/system/identity/print
/system/routerboard/print
/system/health/print

# 接口
/interface/print
/interface/ethernet/print

# IP
/ip/address/print
/ip/route/print
/ip/dns/print
/ip/dhcp-server/lease/print
/ip/arp/print
/ip/firewall/connection/print

# 防火墙
/ip/firewall/filter/print
/ip/firewall/nat/print
/ip/firewall/mangle/print

# 其他
/ip/neighbor/print
/system/logging/print
```

## 注意事项

1. **API 端口**: 默认 8728 (SSL 用 8729)
2. **认证**: 支持空密码和 MD5 challenge-response
3. **协议**: 二进制 length-prefixed 格式
4. **超时**: 默认 5 秒，可根据网络情况调整

## 示例输出

```
============================================================
📡 MikroTik RouterOS 设备状态
============================================================
  设备名：MikroTik
  版本：7.21.2 (stable)
  运行时间：1w2d8h45m38s
  CPU: MIPS 1004Kc V2.15 @ 880MHz
  CPU 负载：2%
  内存：64.7MB / 268MB
  存储：3.8MB / 16MB
============================================================
```

## 作者

虾哥 🤖

## 许可证

MIT
