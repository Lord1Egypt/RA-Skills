# MikroTik RouterOS Skill for OpenClaw

通过 API 连接和管理 MikroTik RouterOS 设备的 OpenClaw Skill。

## 功能

- ✅ 查看设备状态（系统信息、CPU、内存、存储）
- ✅ 查看防火墙规则（filter、NAT、mangle）
- ✅ 查看网络配置（接口、IP 地址、路由、DNS）
- ✅ 执行自定义 RouterOS 命令
- ✅ 支持多设备连接
- ✅ 网络扫描（类似 Winbox，无需配置）
- ✅ 交互式开局流程

## 🚀 快速开始（新用户开局）

### 方式一：交互式开局（推荐）

**1. 说出口令**：
```
mikrotik 开局
```

**2. AI 自动扫描**：
```
📡 扫描完成！发现 3 个设备:

[1] 192.168.1.10 (00:0C:42:AA:BB:CC)
[2] 192.168.1.20 (4C:5E:0C:DD:EE:FF)
[3] 192.168.1.1 (D4:CA:6D:11:22:33)
```

**3. 告诉 AI 账号密码**：
```
全部使用 admin/空密码
```

**4. AI 测试连接并保存**：
```
✅ 连接成功！配置已保存到 TOOLS.md
```

**5. 开始使用**：
```
查看 device1 状态
mikrotik office firewall
```

### 方式二：手动配置

在 `~/.openclaw/workspace/TOOLS.md` 中添加：

```markdown
### MikroTik 设备
- **office**: 192.168.1.1, admin, 空密码
- **home**: 192.168.88.1, admin, yourpassword
```

## 安装

### 方法 1: 手动安装（当前可用）

```bash
# 克隆仓库
git clone https://github.com/YOUR_USERNAME/openclaw-mikrotik-skill.git
cd openclaw-mikrotik-skill

# 复制到 OpenClaw skills 目录
cp -r mikrotik /usr/lib/node_modules/openclaw/skills/

# 重启 OpenClaw Gateway
openclaw gateway restart
```

### 方法 2: 通过 ClawHub（即将上线）

```bash
# 待发布到 ClawHub 后可用
npx clawhub install mikrotik
```



## 配置

在 `TOOLS.md` 中添加 MikroTik 设备信息：

```markdown
### MikroTik 设备

- **office**: 192.168.1.1, admin, 空密码
- **home**: 192.168.88.1, admin, yourpassword
```

## 用法

### 自然语言命令

```
查看 mikrotik 设备状态
mikrotik 防火墙配置
检查路由器运行情况
查看网络接口
查看无线客户端
mikrotik office 客户端
mikrotik ap wifi
在 mikrotik 上执行 /system/resource/print
```

### 可用命令

| 命令 | 说明 |
|------|------|
| `状态` / `status` | 查看设备状态（CPU、内存、运行时间） |
| `防火墙` / `firewall` | 查看防火墙规则（filter、NAT） |
| `接口` / `interface` | 查看网络接口列表 |
| `客户端` / `client` / `无线` / `wifi` | **查看无线客户端连接（CAPsMAN）** ⭐ |
| `路由` / `route` | 查看路由表 |
| `DHCP` | 查看 DHCP 配置和租约 |
| `ARP` | 查看 ARP 表 |
| `流量` / `traffic` | 查看接口流量统计 |
| `WireGuard` / `wg` | 查看 WireGuard 隧道状态 |
| `扫描` / `scan` | 扫描局域网设备（无需配置） |

### 命令行工具

```bash
cd mikrotik-api
python3 cli.py 192.168.1.1 status      # 查看设备状态
python3 cli.py 192.168.1.1 firewall    # 查看防火墙
python3 cli.py 192.168.1.1 interfaces  # 查看接口
python3 cli.py 192.168.1.1 routes      # 查看路由
```

### Python API

```python
from mikrotik_api import MikroTikAPI, QuickCommands

with MikroTikAPI('192.168.1.1') as api:
    api.login()
    quick = QuickCommands(api)
    quick.print_status()
```

## 示例输出

### 设备状态

```
📡 MikroTik RouterOS 设备状态
============================================================
  设备名：OFFICE
  版本：7.21.2 (stable)
  运行时间：1w2d9h9m39s
  CPU: MIPS 1004Kc V2.15 @ 880MHz
  CPU 负载：1%
  内存：61.6MB / 256.0MB
  存储：3.6MB / 16.0MB
============================================================
```

### 无线客户端（v1.8.1 新增）⭐

```
📶 无线客户端 (CAPsMAN)
============================================================

✅ 已连接 2 个无线客户端:

  【客户端 1】
    MAC: 00:11:22:33:44:55
    SSID: MyWiFi | 接口：cap2
    信号：-49 ⭐⭐⭐
    速率：TX 702Mbps-80MHz/2S | RX 585Mbps-80MHz/2S
    连接时间：1d47m
    IP 地址：192.168.1.101
       流量：TX 1.8GB / RX 1.2GB

  【客户端 2】
    MAC: AA:BB:CC:DD:EE:FF
    SSID: MyWiFi | 接口：cap2
    信号：-34 ⭐⭐⭐⭐⭐
    速率：TX 866.6Mbps-80MHz/2S/SGI | RX 702Mbps-80MHz/2S
    连接时间：20m
    IP 地址：192.168.1.102
       流量：TX 29.7MB / RX 892KB
```

## 依赖

- Python 3.6+
- OpenClaw 2026.3.2+
- MikroTik RouterOS API 已启用（默认端口 8728）

## 注意事项

1. 确保 RouterOS 的 API 服务已启用（`/ip/service/print` 查看）
2. 默认端口 8728，SSL 端口 8729
3. 空密码设备注意安全风险
4. 部分命令需要管理员权限

## 文件结构

```
mikrotik/
├── SKILL.md           # Skill 说明和配置
├── handler.py         # 命令处理器
├── README.md          # 本文件
└── mikrotik-api/      # Python API 客户端
    ├── __init__.py
    ├── client.py      # 核心 API 客户端
    ├── commands.py    # 常用命令封装
    ├── cli.py         # 命令行工具
    └── README.md      # API 文档
```

## 开发

### 测试

```bash
cd mikrotik-api
python3 cli.py 192.168.1.1 status
```

### 添加新功能

1. 在 `commands.py` 中添加新方法
2. 在 `handler.py` 中添加命令处理
3. 更新 `SKILL.md` 文档

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License

## 作者

虾哥 🤖

## 相关链接

- [OpenClaw 文档](https://docs.openclaw.ai)
- [MikroTik API 文档](https://help.mikrotik.com/docs/display/ROS/API)
- [ClawHub](https://clawhub.com)
