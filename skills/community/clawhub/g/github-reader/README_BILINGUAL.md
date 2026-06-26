# 📦 GitHub Reader Skill v3.2

**深度解读 GitHub 项目 / Deeply Analyze GitHub Projects**  
**纯 GitHub API，无第三方依赖 / Pure GitHub API, no third-party services**

---

## 🎯 简介 / Introduction

**中文**: 输入 GitHub 仓库链接，自动生成分析报告（项目卡片、README 摘要等）。所有数据来自 GitHub 官方 REST API。

**English**: Input a GitHub repo link to auto-generate analysis reports (project cards, README summary, etc.). All data comes from GitHub's official REST API.

---

## ⚡ 快速开始 / Quick Start

### 安装 / Install

```bash
# ClawHub
clawhub install github-reader

# 手动 / Manual
cd github-reader/
./install_v3_secure.sh
```

### 使用 / Usage

```bash
# 命令 / Command (推荐)
/github-read microsoft/BitNet

# URL
https://github.com/HKUDS/nanobot

# 自然语言 / Natural language (需含 owner/repo)
分析 HKUDS/nanobot
解读仓库：microsoft/BitNet
```

> ⚠️ 泛化语句不触发 / Generic phrases won't trigger (e.g. "analyze this repo" without a repo name)

---

## 🔒 安全与隐私 / Security & Privacy

- ✅ **纯 GitHub API** / **Pure GitHub API** — 只与 `api.github.com` 通信
- ✅ **无第三方** / **No third-party** — Zread、GitView 等已移除
- ✅ **本地缓存** / **Local cache** — 数据不离开设备
- ✅ **输入验证** / **Input validation** — 防注入、SSRF、遍历、投毒

---

## 📊 输出 / Output

1. 💡 项目简介 / Project intro
2. 📊 项目卡片 / Project cards (Stars, Forks, Issues, Language, License)
3. 📖 README 摘要 / README summary
4. 🔗 GitHub 链接 / GitHub links
5. 🚀 快速开始 / Quick start
6. 🔒 数据流向声明 / Data flow notice

---

## ⚙️ 配置 / Configuration

```bash
export GITVIEW_CACHE_TTL="24"           # 缓存时间 / Cache TTL (hours)
export GITVIEW_GITHUB_DELAY="1.0"       # API 间隔 / API delay (seconds)
export GITVIEW_GITHUB_TIMEOUT="10"      # API 超时 / API timeout (seconds)
```

---

## 📈 性能 / Performance

| 场景 / Scenario | 耗时 / Time |
|----------------|-------------|
| 首次分析 / First analysis | 3-5 秒 |
| 缓存命中 / Cache hit | < 0.1 秒 |

---

## 📄 许可证 / License

MIT License

## 👨‍💻 作者 / Author

**Kris Lu**

---

*版本: v3.2（纯 API 安全版）*  
*更新: 2026-05-24*
