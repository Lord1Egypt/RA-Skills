# 🦞 OpenWRT Router Skill

> 一个 OpenClaw / Hermes 等 AI 智能体的技能包，通过 LuCI RPC API 远程管理 OpenWRT 路由器，**无需 SSH**，只需提供账号密码即可。

## ✨ 功能

- 📋 **查看 DHCP 租约** - 谁连了网一目了然
- 📶 **WiFi 连接设备** - 查看无线客户端信号强度
- 🌐 **ARP 活跃设备** - 有线 + 本地网络设备扫描
- 📱 **综合设备查询** - 整合DHCP、ARP、WiFi，显示所有联网设备
- ⏱ **系统状态** - CPU 负载、内存、磁盘、运行时间
- 📦 **软件管理** - 列出已安装软件包、安装新软件
- 🌡 **CPU 温度** - 查看路由器温度
- 🔗 **连接数统计** - 查看当前活跃连接数
- 🏠 **多路由器管理** - 支持管理多台 OpenWRT 路由器

## 🔧 原理

利用 OpenWRT 的 LuCI Web 接口（`cgi-bin/luci/rpc/sys`）执行远程 shell 命令，返回 JSON 格式结果。

```
POST http://<router_ip>/cgi-bin/luci/rpc/sys?auth=<token>
→ {"method":"exec","params":["<shell_command>"]}
← {"id":null,"result":"<stdout>","error":null}
```

**认证方式**：HTTP POST 登录 → 获取 `sysauth` Cookie → 携带 Cookie 调用 RPC API

## 📦 安装

### 方式一：手动安装

```bash
# 克隆仓库
git clone https://github.com/nary24/openwrt-router-skill.git

# 复制到 OpenClaw skills 目录
cp -r openwrt-router-skill ~/.openclaw/workspace/skills/openwrt-router/
```

### 方式二：使用 .skill 包

```bash
# 解压到 skills 目录即可
unzip openwrt-router.skill -d ~/.openclaw/workspace/skills/
```

## ⚙️ 配置

在 `TOOLS.md` 或智能体的配置文件中记录路由器信息：

```markdown
### OpenWRT 路由器

- **家**  (别名: 我家)
  - IP: 192.168.123.1
  - 用户: root
  - 密码: your_password
  - 型号: RAX3000M

- **租房** (别名: 租房小区)
  - IP: 192.168.125.1
  - 用户: root
  - 密码: your_password
```

## 🚀 使用示例

### 与智能体对话

> **你：** 看看家里路由器有多少人在用网
> **智能体：** 正在查询 192.168.123.1 的 DHCP 租约...
> 📋 当前有 4 台设备在线：
> - 192.168.123.245 Redmi-K50
> - 192.168.123.244 STK-AL00
> - 192.168.123.104 POT-AL00a
> - 192.168.123.106 iQOO-Neo6-SE

> **你：** 租房那边装了什么软件
> **智能体：** 🔄 切换至 192.168.125.1（租房小区）
> 已安装 123 个软件包，主要软件：docker, lucky, passwall2, openclash...

> **你：** 帮我在家里装个 tree 命令
> **智能体：** ✅ `tree` 安装成功！tree v2.1.1

### 命令行脚本

```bash
# 查看所有信息
./scripts/openwrt_manager.sh 192.168.123.1 your_pass all

# 查看所有联网设备（综合查询）
./scripts/openwrt_manager.sh 192.168.123.1 your_pass devices

# 只看 DHCP 租约
./scripts/openwrt_manager.sh 192.168.123.1 your_pass leases

# 看 WiFi 设备
./scripts/openwrt_manager.sh 192.168.123.1 your_pass wifi
```

## 🏗 项目结构

```
openwrt-router/
├── SKILL.md                    # 技能描述（智能体加载入口）
├── README.md                   # 本文件
├── scripts/
│   └── openwrt_manager.sh      # 路由器管理 Shell 脚本
└── references/
    └── (参考文档占位)
```

## 🔌 兼容性

- ✅ **OpenClaw** - 直接放入 `skills/` 目录即可
- ✅ **Hermes** - 兼容标准 AgentSkill 格式
- ✅ **任何 AI 智能体** - SKILL.md 提供了完整的 API 调用说明
- ✅ **OpenWRT / ImmortalWrt / LEDE** - 只要支持 LuCI 即可
- ❌ 需要 `curl` 命令（OpenClaw 运行环境中要有）

## 📊 支持的 OpenWRT 命令

| 功能 | 命令 |
|------|------|
| 综合设备查询 | DHCP + ARP + WiFi 组合查询 |
| DHCP 租约 | `cat /tmp/dhcp.leases` |
| ARP 表 | `cat /proc/net/arp` |
| WiFi 设备 | `iwinfo <iface> assoclist` |
| 内存 | `free -m` |
| CPU 信息 | `cat /proc/cpuinfo` |
| CPU 温度 | `cat /sys/class/thermal/thermal_zone0/temp` |
| 磁盘 | `df -h` |
| 负载 | `cat /proc/loadavg` |
| 连接数 | `cat /proc/net/nf_conntrack \| wc -l` |
| 安装软件 | `opkg update && opkg install <pkg>` |
| 已安装列表 | `opkg list-installed` |

## 🤝 贡献

欢迎 Issue 和 PR！如果有好的想法，也可以 Fork 后分享到 ClawdHub。

## 📄 License

MIT
