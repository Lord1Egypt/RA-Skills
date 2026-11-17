# SKILL.md - Gateway Watchdog Skill

> 一句话让 OpenClaw 安装 Gateway Watchdog

## 触发条件

- "安装 Gateway Watchdog"
- "Gateway 监控"
- "gateway watchdog"
- "守护 Gateway"

## 功能

1. **自动安装** Gateway Watchdog 监控脚本
2. **自动配置** 钉钉通知（可选）
3. **自动设置** 开机自启
4. **自动运行** 监控服务

## 安装流程

### 第一步：克隆仓库

```bash
git clone https://github.com/adminlove520/gateway-watchdog.git
cd gateway-watchdog
```

### 第二步：配置（可选）

```bash
cp config.example.py config.py
# 编辑 config.py 填入钉钉 Webhook 和加签密钥
```

### 第三步：运行安装脚本

```bash
python install.py
# 选择 "1" 安装开机自启
```

## 配置说明

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| WEBHOOK | 钉钉 Webhook URL | "" |
| SECRET | 钉钉加签密钥 | "" |
| CHECK_INTERVAL | 检查间隔（秒） | 60 |
| NOTIFY_DAILY | 每天报平安 | True |

## 通知场景

- ✅ 启动时报平安
- ✅ Gateway 掉线报警
- ✅ 重启成功报平安
- ✅ 重启失败报警
- ☀️ 每天 8-10 点报平安

## 使用命令

```bash
# 安装（已在仓库目录）
python install.py

# 查看状态
python install.py  # 选择 4

# 卸载
python install.py  # 选择 2
```

## 检查日志

```bash
# Windows
type %USERPROFILE%\.openclaw\gateway-watchdog.log

# Linux/macOS
cat ~/.openclaw/gateway-watchdog.log
```

## 作者

🦞 小溪 - 帮哥哥守护 Gateway
