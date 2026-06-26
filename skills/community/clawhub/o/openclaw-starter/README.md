# OpenClaw 新手一站式引导 🚀

> 🎯 **5 分钟快速上手 OpenClaw** —— 从零开始，一站式完成环境检测、安装配置、Skills 推荐、渠道设置

[![ClawHub](https://img.shields.io/badge/ClawHub-openclaw--starter-blue)](https://clawhub.ai/testmtcode/openclaw-starter)
[![Version](https://img.shields.io/badge/version-1.0.0-green)](https://clawhub.ai/testmtcode/openclaw-quickstart)
[![License](https://img.shields.io/badge/license-MIT--0-lightgrey)](https://clawhub.ai/testmtcode/openclaw-quickstart)

---

## ✨ 核心功能

| 功能 | 描述 |
|------|------|
| 🔍 **环境检测** | 检测 Node.js、npm、系统环境 |
| 📦 **安装检查** | 检查 OpenClaw 安装状态 |
| ⚙️ **配置向导** | Gateway 配置交互式引导 |
| 🎒 **Skills 推荐** | 根据用户类型推荐必备技能 |
| 💬 **渠道配置** | Telegram/WhatsApp/Discord 设置 |
| 📖 **使用教程** | 首次使用引导和示例 |

---

## 🚀 快速开始

### 安装依赖

```bash
cd skills/openclaw-quickstart
pip3 install -r requirements.txt
```

### 使用方式

```bash
# 交互式引导（推荐）
python3 scripts/quickstart.py --interactive

# 一键完成
python3 scripts/quickstart.py --all

# 环境检测
python3 scripts/quickstart.py --check-env

# Skills 推荐
python3 scripts/quickstart.py --recommend --type beginner
```

---

## 📊 输出示例

### 环境检测

```
🔍 环境检测报告
━━━━━━━━━━━━━━━━
✅ Node.js: v22.22.1
✅ npm: 10.9.3
✅ 系统：Linux 6.17.0-19-generic
✅ Python: 3.11.0

📋 结论：环境正常，可以安装 OpenClaw
```

### Skills 推荐

```
🎒 根据你的需求推荐 Skills
━━━━━━━━━━━━━━━━
用户类型：新手套餐

1. game-deals - 限免游戏查询 ⭐⭐⭐⭐⭐
2. weather - 天气查询 ⭐⭐⭐⭐⭐
3. rss-aggregator - RSS 阅读 ⭐⭐⭐⭐
4. password-generator - 密码生成 ⭐⭐⭐⭐
5. unit-converter - 单位转换 ⭐⭐⭐⭐

一键安装：
clawhub install game-deals weather rss-aggregator
```

---

## 🎒 推荐套餐

### 新手套餐
```bash
clawhub install game-deals weather rss-aggregator password-generator unit-converter
```

### 开发者套餐
```bash
clawhub install git-essentials json-formatter ocr-local pdf-toolkit-pro
```

### 自动化套餐
```bash
clawhub install cron-manager reminder-skill webhook-handler email-sender
```

---

## 📋 完整文档

详细使用说明请查看 [SKILL.md](SKILL.md)

---

## ⚠️ 说明

- 🔒 所有检测在本地完成，不上传数据
- 📊 推荐基于 ClawHub 公开数据
- 📖 适合 OpenClaw 新手用户

---

## 📄 许可证

**MIT-0** - 自由使用、修改、分发，无需署名

---

**🎯 让 OpenClaw 入门更简单！**
