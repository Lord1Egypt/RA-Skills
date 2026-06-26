# 🦞 OpenClaw Migrate v3 - Release Notes

**Version**: 3.0.0  
**Date**: 2026-03-26  
**Slug**: openclaw-migrate-v3

---

## 🎯 What's New / 新功能

### Core Philosophy / 核心理念

> **"Like moving your home" - 像搬家一样**
> 
> Pack everything that's **yours**, reinstall **consumables** at the new place.
> 
> 打包所有**你的东西**，在新家重新安装**消耗品**。

---

### Key Changes / 核心变更

#### ✅ Now Packs / 现在打包

| Item | Why / 原因 |
|------|-----------|
| **credentials/** | Your API keys, your identity / 你的 API Keys，你的身份 |
| **openclaw.json** | Your configuration / 你的配置 |
| **SOUL.md, USER.md** | Your persona / 你的身份 |
| **memory/** | Your data / 你的数据 |
| **skills/** | Your tools / 你的工具 |
| **cron/** | Your tasks / 你的任务 |

#### ❌ Now Excludes / 现在排除

| Item | Why / 原因 |
|------|-----------|
| **node_modules/** | Reinstall at new place / 到新家重新安装 |
| **.git/** | Not needed / 不需要 |
| **completions/** | Auto-regenerated / 自动重新生成 |
| ***.log** | Not needed / 不需要 |

---

## 🚀 Usage / 使用

### Quick Start / 快速开始

```bash
# 1. Pack / 打包
openclaw-migrate pack --output ~/my-openclaw/

# 2. Transfer / 传输
rsync -av ~/my-openclaw/ user@new-pc:~/

# 3. Unpack / 归位
openclaw-migrate unpack --input ~/my-openclaw/
```

### Advanced / 高级用法

```bash
# Versioned pack / 版本化打包
openclaw-migrate pack --versioned --output ~/packs/

# Incremental backup / 增量备份
openclaw-migrate pack --incremental ~/packs/base/ --output ~/packs/delta/

# Auto transfer / 自动传输
openclaw-migrate transfer --input ~/packs/ --target user@new-pc:~/
```

---

## 📊 Comparison / 对比

### v2 vs v3

| Feature / 功能 | v2 | v3 |
|---------------|----|----|
| **credentials/** | ❌ Excluded | ✅ **Packed** |
| **node_modules/** | ❌ Excluded | ❌ Excluded (reinstall) |
| **Auto install** | ❌ No | ✅ **Yes** |
| **Philosophy** | Backup | **Moving home** |

---

## 💡 Why This Matters / 为什么重要

### Before (v2) / 之前

```bash
# Pack / 打包
❌ Excluded credentials/  # Lost API keys!

# Unpack / 归位
❌ Had to manually configure everything  # Painful!
```

### After (v3) / 之后

```bash
# Pack / 打包
✅ Included credentials/  # All your configs!

# Unpack / 归位
✅ Auto reinstall dependencies  # Easy!
✅ Your configs restored  # Perfect!
```

---

## 🎯 Use Cases / 使用场景

### Scenario 1: Moving to New Computer

```bash
# Old computer / 旧电脑
openclaw-migrate pack --output ~/my-openclaw/

# Transfer / 传输
rsync -av ~/my-openclaw/ user@new-pc:~/

# New computer / 新电脑
openclaw-migrate unpack --input ~/my-openclaw/
# ✅ Auto installs dependencies
# ✅ Restores all your configs
```

### Scenario 2: Daily Backup

```bash
# Every night / 每晚
openclaw-migrate pack --incremental ~/packs/base/ --output ~/packs/daily/
# ✅ Only changed files
# ✅ Fast and efficient
```

---

## 📦 What Gets Packed / 打包内容

### Your Assets / 你的资产

```
my-openclaw/
├── credentials/        ✅ Your API keys
├── config/
│   ├── openclaw.json  ✅ Your config
│   ├── SOUL.md        ✅ Your persona
│   ├── USER.md        ✅ Your profile
│   └── ...
├── skills/            ✅ Your tools
├── memory/            ✅ Your data
└── cron/              ✅ Your tasks
```

### Not Packed / 不打包

```
❌ node_modules/       # Reinstall with npm install
❌ .git/               # Not needed
❌ completions/        # Auto-generated
❌ *.log               # Not needed
```

---

## 🔧 Installation / 安装

```bash
# Install from ClawHub
npx clawhub install openclaw-migrate-v3

# Or clone from GitHub
git clone https://github.com/your-org/openclaw-migrate-v3
```

---

## 📝 Documentation / 文档

| Document | Language |
|----------|----------|
| [README.md](README.md) | 🇨🇳 Chinese |
| [README.en.md](README.en.md) | 🇺🇸 English |
| [EXCLUDE-STRATEGY.md](EXCLUDE-STRATEGY.md) | 🇨🇳 Chinese |
| [MIGRATION-GUIDE.md](MIGRATION-GUIDE.md) | 🇨🇳 Chinese |

---

## 🎉 Success Stories / 成功案例

### User Testimonial / 用户评价

> "Finally! A migration tool that packs **my stuff**, not just files.
> Moved to a new computer in 5 minutes, all my configs intact!"
> 
> "终于！一个打包**我的东西**的迁移工具。
> 5 分钟搬到新电脑，所有配置完好无损！"

---

## 🚧 Known Issues / 已知问题

| Issue / 问题 | Status / 状态 |
|-------------|--------------|
| Incremental backup size calculation | ⚠️ Working on it |
| Transfer progress bar | ⚠️ Planned |

---

## 📞 Support / 支持

- **GitHub Issues**: https://github.com/your-org/openclaw-migrate-v3/issues
- **Discord**: https://discord.gg/clawd
- **ClawHub**: https://clawhub.ai/skills/openclaw-migrate-v3

---

## 🎯 Roadmap / 路线图

### v3.1 (Next Week)
- [ ] Better progress bar / 更好的进度条
- [ ] Cloud transfer (Dropbox/Google Drive) / 云传输

### v3.2 (Next Month)
- [ ] Web UI / Web 界面
- [ ] Scheduled backups / 定时备份

---

**License**: MIT-0  
**Author**: Your Name  
**Contributors**: OpenClaw Community

---

**Ready to move your OpenClaw home? 🏠**

**准备好搬家你的 OpenClaw 了吗？🏠**

```bash
npx clawhub install openclaw-migrate-v3
```
