# 📦 GitHub Reader Skill v3.2

**深度解读 GitHub 项目 — 纯 GitHub REST API，无第三方依赖**

---

## 🎯 简介

只需输入 GitHub 仓库链接，自动生成分析报告（项目卡片、README 摘要、快速开始等）。所有数据来自 GitHub 官方 REST API，不经过任何第三方服务。

---

## ⚡ 快速开始

### 安装

```bash
clawhub install github-reader

# 或手动安装
cd github-reader/
./install_v3_secure.sh
```

### 使用

```bash
# 命令模式（推荐）
/github-read microsoft/BitNet

# GitHub URL
https://github.com/HKUDS/nanobot

# 自然语言（需包含 owner/repo）
分析 HKUDS/nanobot
```

> ⚠️ 泛化语句（如 "帮我分析这个仓库"）不会触发，避免误触发。

---

## 🔒 隐私与安全

- ✅ **纯 GitHub REST API** — 只与 `api.github.com` 通信
- ✅ **无第三方依赖** — Zread、GitView 等已移除
- ✅ **本地缓存** — 数据不离开设备（缓存到 `/tmp/gitview_cache`）
- ✅ **输入验证** — 防 URL 注入、SSRF、路径遍历、缓存投毒

---

## 📊 输出内容

分析报告包含：
1. 💡 项目简介
2. 📊 项目卡片（Stars、Forks、Issues、语言、许可证等）
3. 📖 README 摘要
4. 🔗 GitHub 链接
5. 🚀 快速开始（clone + cd）
6. 🔒 数据流向声明

---

## ⚙️ 配置

```bash
# 缓存配置
export GITVIEW_CACHE_TTL="24"           # 缓存时间（小时）
export GITVIEW_GITHUB_DELAY="1.0"       # API 间隔（秒）
export GITVIEW_GITHUB_TIMEOUT="10"      # API 超时（秒）
```

---

## 📈 性能

| 场景 | 耗时 |
|------|------|
| 首次分析 | 3-5 秒 |
| 缓存命中 | < 0.1 秒 |

---

## 📄 许可证

MIT License

## 👨‍💻 作者

**Kris Lu**

---

*版本: v3.2（纯 API 安全版）*  
*更新: 2026-05-24*
