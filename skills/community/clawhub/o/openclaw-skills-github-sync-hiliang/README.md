# OpenClaw Skills GitHub Sync

> 将你的 OpenClaw skills 同步到 GitHub

一个 OpenClaw skill，提供交互式配置向导，将你的 skills 同步到 GitHub 仓库。

## 安装

### Windows

```powershell
# 克隆到 OpenClaw skills 目录
cd $env:USERPROFILE\.openclaw\skills
git clone https://github.com/Hi-Jiajun/openclaw-skills-github-sync.git
```

### Linux / Mac

```bash
# 克隆到 OpenClaw skills 目录
cd ~/.openclaw/skills
git clone https://github.com/Hi-Jiajun/openclaw-skills-github-sync.git
```

或从 ClawHub 直接安装：https://clawhub.ai/skills/openclaw-skills-github-sync-hiliang

## 特性

- 🎯 交互式配置向导
- 🔒 手动确认同步
- 🌐 私有/公开双仓库支持
- 🌍 支持 Windows / Linux / Mac

## 快速开始

### Windows

```powershell
# 首次配置（交互式向导）
powershell -ExecutionPolicy Bypass -File "scripts/setup.ps1"

# 执行同步
powershell -ExecutionPolicy Bypass -File "scripts/sync.ps1"
```

### Linux / Mac

```bash
# 首次配置（交互式向导）
chmod +x scripts/setup.sh
./scripts/setup.sh

# 执行同步
chmod +x scripts/sync.sh
./scripts/sync.sh
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

https://github.com/Hi-Jiajun/openclaw-skills-github-sync
