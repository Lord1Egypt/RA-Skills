# OpenClaw Gateway Watchdog

> 🦞 OpenClaw Gateway 24/7 稳定运行监控工具

[![GitHub Stars](https://img.shields.io/github/stars/adminlove520/gateway-watchdog)](https://github.com/adminlove520/gateway-watchdog)
[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-orange)](https://github.com/adminlove520/gateway-watchdog)

## 为什么需要

**不要用 OpenClaw 自己的 cron 监控 Gateway。** Gateway 挂了，cron job 根本收不到 wake event，形成死锁。

本工具用独立进程监控 Gateway，掉了自动重启，还能发送钉钉通知！

## 特性

- ✅ 自动检测 Gateway 状态
- ✅ 掉了自动重启
- ✅ 钉钉机器人通知
- ✅ 支持 Windows / Linux / macOS
- ✅ 每天报平安
- ✅ 开机自启

## 快速开始

### 1. 安装

```bash
# 克隆仓库
git clone https://github.com/adminlove520/gateway-watchdog.git
cd gateway-watchdog

# 配置钉钉（可选）
cp config.example.py config.py
# 编辑 config.py 填入你的钉钉 Webhook 和加签密钥
```

### 2. 配置钉钉机器人

1. 钉钉群 → 设置 → 智能群助手 → 添加机器人
2. 选择「自定义」机器人
3. 设置名字（如 Gateway Watchdog）
4. 开启「加签」安全设置
5. 复制 `Webhook 地址` 和 `加签密钥`

### 3. 运行

```bash
# 方式1: 直接运行
python gateway_monitor.py

# 方式2: 后台运行（Linux/macOS）
nohup python gateway_monitor.py &

# 方式3: 使用安装脚本（推荐）
python install.py
```

### 4. 开机自启

运行 `python install.py` 选择安装即可：

```
==================================================
OpenClaw Gateway Watchdog 安装向导
==================================================

检测到系统: Windows

1. 安装开机自启
2. 卸载开机自启
3. 直接运行（测试用）
4. 查看状态
0. 退出
```

**手动安装（Windows）**:
```powershell
schtasks /create /tn "OpenClawGatewayWatchdog" /tr "python C:\path\to\gateway_monitor.py" /sc minute /mo 1 /rl limited /f
```

## 配置说明

编辑 `config.py` 或在运行目录创建配置文件：

```python
# 钉钉配置
WEBHOOK = "https://oapi.dingtalk.com/robot/send?access_token=xxx"
SECRET = "SECxxx"

# 监控配置
CHECK_INTERVAL = 60      # 检查间隔（秒）
GATEWAY_PORT = 18789    # Gateway 端口

# 通知配置
NOTIFY_ON_STARTUP = True    # 启动时报平安
NOTIFY_ON_DOWN = True       # 掉线时通知
NOTIFY_ON_RECOVERY = True   # 恢复时通知
NOTIFY_ON_FAILED = True     # 重启失败时通知
NOTIFY_DAILY = True         # 每天报平安
```

## 通知逻辑

| 场景 | 是否通知 |
|------|----------|
| 启动时 | ✅ 报平安 |
| Gateway 掉线 | ✅ 报警 |
| 重启成功 | ✅ 报平安 |
| 重启失败 | ✅ 报警 |
| 正常运行 | ❌ 不通知 |
| 每天 8-10 点 | ✅ 报平安 |

## 重启逻辑

**掉了直接用 `--force` 强制重启**

掉线说明 Gateway 有问题，常规重启很可能起不来。所以本工具使用 `openclaw gateway --force start` 直接强制杀掉旧进程再启动。

## 开机自启

### Windows

```powershell
# 创建任务计划
schtasks /create /tn "OpenClaw Gateway Watchdog" /tr "python C:\path\to\gateway_monitor.py" /sc minute /mo 1 /rl limited /f
```

### Linux (systemd)

```ini
# /etc/systemd/system/gateway-watchdog.service
[Unit]
Description=OpenClaw Gateway Watchdog
After=network.target

[Service]
Type=simple
User=yourusername
WorkingDirectory=/path/to/gateway-watchdog
ExecStart=/usr/bin/python3 /path/to/gateway-watchdog/gateway_monitor.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable gateway-watchdog
sudo systemctl start gateway-watchdog
```

### Linux (crontab)

```bash
# 编辑 crontab
crontab -e

# 添加（每分钟检查一次）
* * * * * cd /path/to/gateway-watchdog && python gateway_monitor.py >> /tmp/gateway-watchdog.log 2>&1
```

### macOS (launchd)

```xml
<!-- ~/Library/LaunchAgents/com.openclaw.gateway-watchdog.plist -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.openclaw.gateway-watchdog</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/path/to/gateway-watchdog/gateway_monitor.py</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
```

```bash
launchctl load ~/Library/LaunchAgents/com.openclaw.gateway-watchdog.plist
```

## 项目结构

```
gateway-watchdog/
├── gateway_monitor.py    # 主程序
├── config.example.py     # 配置示例
├── README.md             # 说明文档
├── CHANGELOG.md         # 更新日志
├── ARCHITECTURE.md      # 架构图
└── install.py           # 安装脚本
```

## 监控流程图

```
┌─────────────────────────────────────────────────────────┐
│                    Watchdog 启动                          │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│              每 60 秒检查一次 Gateway                      │
└─────────────────────┬───────────────────────────────────┘
                      │
           ┌──────────┴──────────┐
           │                     │
           ▼                     ▼
    ┌─────────────┐       ┌─────────────┐
    │  Gateway    │       │  Gateway    │
    │  运行正常   │       │   掉线      │
    └──────┬──────┘       └──────┬──────┘
           │                     │
           ▼                     ▼
    ┌─────────────┐       ┌─────────────┐
    │  记录日志   │       │  钉钉通知   │
    │  (不通知)   │       │  掉线报警   │
    └─────────────┘       └──────┬──────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │  杀掉 node 进程         │
                    │  等待 2 秒              │
                    │  启动 Gateway           │
                    └──────────┬──────────────┘
                               │
                    ┌──────────┴──────────────┐
                    │                         │
                    ▼                         ▼
             ┌─────────────┐          ┌─────────────┐
             │  重启成功   │          │  重启失败   │
             └──────┬──────┘          └──────┬──────┘
                    │                         │
                    ▼                         ▼
             ┌─────────────┐          ┌─────────────┐
             │  钉钉通知   │          │  钉钉通知   │
             │  恢复成功   │          │  需要人工   │
             └─────────────┘          └─────────────┘
```

## 常见问题

### Q: 为什么不用 OpenClaw 自带的 cron？

A: Gateway 挂了之后，cron job 也收不到通知，形成死锁。独立监控更可靠。

### Q: 钉钉通知显示乱码怎么办？

A: 请使用 Python 3.7+，并确保使用 `config.py` 而非直接修改 `gateway_monitor.py`。

### Q: 如何查看日志？

A: 日志文件在 `~/.openclaw/gateway-watchdog.log`（Linux/macOS）或 `%USERPROFILE%\.openclaw\gateway-watchdog.log`（Windows）

## 更新日志

详见 [CHANGELOG.md](CHANGELOG.md)

## 贡献者

- 小溪 🦞 - 作者

## 许可证

MIT License

---

🦞 小溪的作品 - 帮哥哥守护 Gateway！
