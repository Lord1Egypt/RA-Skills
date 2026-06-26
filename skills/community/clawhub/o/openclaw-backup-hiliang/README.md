# OpenClaw Backup

> 自动备份 OpenClaw 配置，让数据永不丢失

一个 OpenClaw skill，提供交互式配置向导，自动备份你的 OpenClaw 配置。

## 安装

### Windows

```powershell
# 克隆到 OpenClaw skills 目录
cd $env:USERPROFILE\.openclaw\skills
git clone https://github.com/Hi-Jiajun/openclaw-backup.git
```

### Linux / Mac

```bash
# 克隆到 OpenClaw skills 目录
cd ~/.openclaw/skills
git clone https://github.com/Hi-Jiajun/openclaw-backup.git
```

或从 ClawHub 直接安装：https://clawhub.ai/skills/openclaw-backup-hiliang

## 特性

- 🎯 交互式配置向导，5分钟快速上手
- 🔄 自动备份，保留多个版本
- 🧹 智能清理，自动转移和删除旧备份
- 🌐 支持 Windows / Linux / Mac

## 快速开始

### Windows

```powershell
# 首次配置（交互式向导）
powershell -ExecutionPolicy Bypass -File "scripts/setup.ps1"

# 执行备份
powershell -ExecutionPolicy Bypass -File "scripts/backup.ps1"
```

### Linux

```bash
# 首次配置（交互式向导）
chmod +x scripts/setup.sh
./scripts/setup.sh

# 执行备份
chmod +x scripts/backup.sh
./scripts/backup.sh
```

### Mac

```bash
# 首次配置（交互式向导）
chmod +x scripts/setup.sh
./scripts/setup.sh

# 执行备份
chmod +x scripts/backup.sh
./scripts/backup.sh
```

详细说明请查看 [SKILL.md](SKILL.md)

## 感谢支持

如果这个项目对你有帮助，欢迎扫码捐赠支持！你的支持是我持续更新和维护的动力！ 🙏

### 支付宝

<img src="1772974731593.jpg" width="200" />

### 微信

<img src="mm_facetoface_collect_qrcode_1772974720410.png" width="200" />

---

## Star ⭐

如果对你有帮助，欢迎 Star！

https://github.com/Hi-Jiajun/openclaw-backup
