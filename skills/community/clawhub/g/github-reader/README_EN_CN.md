# GitHub Reader Skill v3.2

**深度解读 GitHub 项目，生成结构化分析报告**  
**Deeply analyze GitHub projects and generate structured analysis reports**  
**纯 GitHub REST API / Pure GitHub REST API**

---

## 🎯 功能特性 / Features

### 核心功能 / Core Features

- 📊 **自动分析** — 输入 GitHub URL 自动生成深度报告  
  **Auto Analysis** — Input GitHub URL to auto-generate reports

- 📖 **多维度解读** — 项目卡片、README 摘要、链接等  
  **Multi-dimensional Analysis** — Project cards, README summary, links

- ⚡ **智能缓存** — 24 小时缓存，重复查询 < 0.1 秒  
  **Smart Caching** — 24-hour cache, repeated queries < 0.1s

- 🔒 **纯 GitHub API** — 无第三方依赖  
  **Pure GitHub API** — No third-party dependencies

---

## 🚀 快速开始 / Quick Start

### 安装 / Installation

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

# 自然语言 (需含 owner/repo)
分析 HKUDS/nanobot
```

> ⚠️ 泛化语句不触发 / Generic phrases (e.g. "analyze this repo" without repo name) won't trigger

---

## 🔒 安全与隐私 / Security & Privacy

**v3.2 变更**:
- ❌ 移除 Zread、GitView — 不再向任何第三方发送数据
- ✅ 纯 GitHub REST API (`api.github.com`)
- ✅ 本地缓存，可配置可清除
- ✅ 输入验证、SSRF 防护、路径防遍历

---

## 📊 输出示例 / Output Example

```markdown
# 📦 microsoft/BitNet 深度解读报告

> 分析时间: 2026-05-24 15:30
> 数据来源: GitHub REST API（纯 API，不经第三方）

## 💡 项目简介
BitNet.cpp 是微软官方推出的 1 比特量化大语言模型推理框架...

## 📊 项目卡片
| 指标 | 值 |
|------|-----|
| ⭐ Stars | 12.5k |
| 🍴 Forks | 2.1k |
| 📝 Issues | 156 |
| 🐍 语言 | Python |
| 📄 许可证 | MIT |

## 🔗 链接
| 平台 | 链接 |
|------|------|
| GitHub | https://github.com/microsoft/BitNet |

🔒 数据流向声明：本次分析仅使用 GitHub REST API，不会将仓库信息发送给任何第三方服务。
```

---

## ⚙️ 配置 / Configuration

```bash
# 缓存配置 / Cache Configuration
export GITVIEW_CACHE_DIR="/tmp/gitview_cache"
export GITVIEW_CACHE_TTL="24"

# API 配置 / API Configuration
export GITVIEW_GITHUB_DELAY="1.0"       # API 间隔 / API delay (seconds)
export GITVIEW_GITHUB_TIMEOUT="10"      # API 超时 / API timeout (seconds)
```

---

## 📁 文件结构 / File Structure

```
github-reader/
├── github_reader_v3_secure.py    # v3.2 主代码 / v3.2 main code
├── __init__.py                   # Skill 注册 / Skill registration
├── clawhub.json                  # ClawHub 元数据 / ClawHub metadata
├── SECURITY.md                   # 安全说明 / Security guide
├── SKILL.md                      # 使用指南 / User guide
├── RELEASE_NOTES.md              # 发布说明 / Release notes
├── README.md                     # 简要说明 / Brief README
├── README_BILINGUAL.md           # 双语说明 / Bilingual README
├── PACKAGE.md                    # 打包说明 / Package guide
└── install_v3_secure.sh          # 安装脚本 / Installation script
```

---

## 🔧 技术栈 / Tech Stack

- **语言 / Language**: Python 3.9+
- **依赖 / Dependencies**: httpx（HTTP 客户端）
- **数据源 / Data source**: GitHub REST API（唯一 / only）
- **第三方服务 / Third-party**: 无 / None
- **缓存 / Cache**: 本地文件系统（JSON）/ Local filesystem (JSON)

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
