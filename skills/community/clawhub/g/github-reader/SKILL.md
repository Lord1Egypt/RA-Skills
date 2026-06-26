# GitHub Reader Skill v3.2

**深度解读 GitHub 项目 / Deeply Analyze GitHub Projects**

📖 输入 GitHub 仓库链接，自动生成结构化分析报告 — 纯 GitHub REST API，不经过任何第三方服务。

---

## 🚀 安装 / Installation

```bash
cd github-reader/
./install_v3_secure.sh
```

重启 Agent gateway：
```bash
openclaw gateway restart
```

---

## 💡 用法 / Usage

### 命令方式（推荐，精准触发）
```
/github-read microsoft/BitNet
```

### GitHub URL
```
https://github.com/HKUDS/nanobot
```

### 自然语言（需包含 owner/repo）
```
分析 HKUDS/nanobot
解读仓库：microsoft/BitNet
```

> ⚠️ **注意**：不带仓库名的泛化语句（如 "帮我分析这个仓库"）不会触发，避免误触发。

---

## 📊 输出示例 / Output Example

```markdown
# 📦 microsoft/BitNet 深度解读报告

> 分析时间: 2026-05-24 15:30
> 数据来源: GitHub REST API（纯 API，不经第三方）

---

## 💡 项目简介
BitNet.cpp 是微软官方推出的 1 比特量化大语言模型推理框架...

## 📊 项目卡片

| 指标 | 值 |
|------|-----|
| ⭐ Stars | 12.5k |
| 🍴 Forks | 2.1k |
| 📝 Issues | 156 |
| 🐍 语言 | Python |
| 📄 许可证 | MIT License |
| 🕐 最后更新 | 3天前 |

## 🔗 链接
| 平台 | 链接 |
|------|------|
| GitHub | https://github.com/microsoft/BitNet |

## 📖 README 摘要
> BitNet.cpp is the official inference framework for 1-bit LLMs...

## 🔗 快速开始
```bash
git clone https://github.com/microsoft/BitNet.git
cd BitNet
```

🔒 数据流向声明：本次分析仅使用 GitHub REST API，不会将仓库信息发送给任何第三方服务。分析结果本地缓存 24 小时，缓存目录：/tmp/gitview_cache。

---
*v3.2 — 纯 GitHub API，无第三方数据外传*
```

---

## 🔒 隐私与安全 / Privacy & Security

### 数据流向
- ✅ **仅使用 GitHub 官方 REST API**（`api.github.com`）
- ✅ **不经过任何第三方服务**（Zread、GitView 等已移除）
- ✅ **分析结果本地缓存**，缓存位置和时长可配置
- ✅ **不访问用户的私有仓库列表或 Token**

### 缓存管理
缓存目录：`/tmp/gitview_cache`（默认），可通过环境变量修改：
```bash
export GITVIEW_CACHE_DIR="/path/to/cache"  # 缓存目录
export GITVIEW_CACHE_TTL="24"              # 缓存时间（小时）
```

清除缓存：`rm -rf /tmp/gitview_cache`

---

## ⚙️ 配置 / Configuration

```bash
# 缓存配置
export GITVIEW_CACHE_DIR="/tmp/gitview_cache"
export GITVIEW_CACHE_TTL="24"
export GITVIEW_CACHE_MAX_SIZE="1"    # MB

# 性能配置
export GITVIEW_GITHUB_DELAY="1.0"    # API 调用间隔（秒）

# 超时配置
export GITVIEW_GITHUB_TIMEOUT="10"   # API 超时（秒）
```

---

## 📈 性能指标 / Performance

| 场景 | 耗时 | 备注 |
|------|------|------|
| 首次分析 | 3-5 秒 | API 调用 + 本地生成 |
| 缓存命中 | < 0.1 秒 | 直接返回 |
| 缓存有效期 | 24 小时 | 可配置 |

---

## 📁 文件结构 / File Structure

```
github-reader/
├── github_reader_v3_secure.py    # v3.2 主代码（纯 API）
├── __init__.py                   # Skill 注册
├── clawhub.json                  # ClawHub 元数据
├── SECURITY.md                   # 安全说明（代码对应）
├── SKILL.md                      # 本文件
├── RELEASE_NOTES.md              # 发布说明
├── README.md                     # 简要说明
├── README_BILINGUAL.md           # 双语说明
├── README_EN_CN.md               # 详细中英对照
├── PACKAGE.md                    # 打包说明
└── install_v3_secure.sh          # 安装脚本
```

---

## 🔄 版本变更（v3.1 → v3.2）

| 变更 | 说明 |
|------|------|
| ❌ 移除 Zread | 不再调用 zread.ai，不再生成 Zread 链接 |
| ❌ 移除 GitView | 不再引用本地 GitView 服务 |
| ✅ 纯 API | 完全基于 GitHub REST API |
| ✅ 收紧触发 | 只接受显式 owner/repo 格式 |
| ✅ 隐私声明 | 输出中包含数据流向说明 |
| ✅ SECURITY.md | 移除未验证的自检清单 |

---

## 📄 许可证 / License

MIT License

## 👨‍💻 作者 / Author

**Kris Lu**

---

*版本: v3.2（纯 API 安全版）*  
*最后更新: 2026-05-24*
