# 📰 last30days-cn — 中国平台深度研究引擎

> 🚀 30 天的研究，30 秒的结果。8 大平台。零过时信息。

**last30days-cn** 是一个 AI Agent 技能（Skill），能够自动搜索中国互联网 8 大主流平台最近 30 天的内容，综合分析后生成有据可查的研究报告。

🔗 本项目基于 [mvanhorn/last30days-skill](https://github.com/mvanhorn/last30days-skill) 进行深度本土化改造，完全面向中国用户和中文互联网平台。

🕷️ v2.0 集成 [MediaCrawler](https://github.com/NanmiCoder/MediaCrawler) 爬虫引擎思路，大幅减少 API Key 依赖。v2.1 修复百度/小红书反爬问题，XHR 拦截替代 DOM 解析，Bing 兜底搜索，已移除无效的 ScrapeCreators 小红书集成。

👤 **作者 / Author:** Jesse ([@Jesseovo](https://github.com/Jesseovo))

---

## ⚠️ 免责声明 / Disclaimer

> **请务必仔细阅读以下内容。使用本项目即表示您同意以下所有条款。**

### 法律合规声明

1. **本项目仅供学习和研究目的**。所有爬虫功能仅用于技术学习与研究交流，**严禁用于商业用途**。
2. 使用者必须严格遵守中华人民共和国相关法律法规，包括但不限于：
   - 《中华人民共和国网络安全法》
   - 《中华人民共和国数据安全法》
   - 《中华人民共和国个人信息保护法》
   - 《中华人民共和国反不正当竞争法》
3. 使用者必须遵守各平台的**服务条款（ToS）**和 **robots.txt** 规定。
4. **禁止**将本项目用于以下行为：
   - 大规模、高频率地抓取平台数据
   - 收集、存储或传播他人个人隐私信息
   - 破坏或干扰平台正常运营
   - 任何形式的非法数据倒卖或商业牟利
   - 对外提供自动化数据采集服务
5. 本项目开发者**不承担**因使用本项目而产生的任何法律责任。用户应**自行承担**使用本项目的全部法律风险。
6. 如有侵权，请联系作者，将在第一时间处理。

### 技术免责

- 爬虫功能依赖 Playwright 浏览器自动化，模拟正常用户浏览行为，**不涉及**逆向加密算法或破解安全机制。
- 各平台接口随时可能变更，本项目不保证所有功能始终可用。
- 建议将请求频率控制在合理范围内（如每次搜索间隔 ≥ 5 秒），避免被平台封禁。

> 💡 **爬虫违法违规的案例频发，请务必合法合规使用。**
> 参考：[中国爬虫相关法律案例汇总](https://github.com/HiddenStrawberry/Crawler_Illegal_Cases_In_China)

---

## ✨ v2.0 新特性

### 🆕 v2.0 vs v1.0 对比

| 特性 | v1.0 | v2.0 |
|:---:|:---:|:---:|
| 免费可用平台数 | 4 个 | **7 个**（安装 Playwright 后） |
| 需要 API Key 的平台 | 微博、小红书、抖音、微信 | **仅微信**（其余可用爬虫替代） |
| 数据获取方式 | 仅 API + 公开接口 | API + **爬虫引擎** + 公开接口 |
| 安装难度 | 需配置多个 API Key | `pip install playwright` 即可 |
| marketplace.json | 缺少 owner 字段（Bug） | ✅ 已修复 |

### 核心升级

1. **集成 MediaCrawler 爬虫引擎** — 基于 Playwright 浏览器自动化，无需逆向加密算法，大幅降低使用门槛
2. **7/8 平台零配置可用** — 除微信外，所有平台均可无需 API Key 使用
3. **智能降级策略** — API 优先 → 爬虫模式 → 公开接口，三级自动降级
4. **修复 Issue #1** — 修复 marketplace.json 缺少 owner 字段导致 Claude Code 安装失败的 bug
5. **登录态缓存** — 爬虫模式支持 Cookie 持久化，减少重复登录

---

## 📋 平台支持

| 平台 | 模块 | 数据获取方式 | 需要配置 |
|:---:|:---:|:---:|:---:|
| 🔴 微博 | `weibo.py` | API / 🕷️爬虫 / 公开接口 | ✅ 爬虫模式无需配置 |
| 📕 小红书 | `xiaohongshu.py` | API / 🕷️爬虫 / 公开接口 | ✅ 爬虫模式无需配置 |
| 📺 B站 | `bilibili.py` | 公开 API / 🕷️爬虫备用 | ✅ 无需配置 |
| 💬 知乎 | `zhihu.py` | 公开搜索 / 🕷️爬虫备用 | ✅ 无需配置 |
| 🎵 抖音 | `douyin.py` | API / 🕷️爬虫 / 公开接口 | ✅ 爬虫模式无需配置 |
| 💚 微信 | `wechat.py` | API / 搜狗搜索 | `WECHAT_API_KEY`（可选） |
| 🔵 百度 | `baidu.py` | 公开搜索 / API | ✅ 基础搜索无需配置 |
| 📰 头条 | `toutiao.py` | 公开接口 | ✅ 无需配置 |

> 🕷️ = 需要安装 Playwright（`pip install playwright && playwright install chromium`）

---

## 🤖 Agent 平台安装

### Cursor（推荐）

将项目克隆到 Cursor 技能目录：

```bash
git clone https://github.com/Jesseovo/last30days-skill-cn.git
```

然后在 Cursor 中将 `SKILL.md` 添加为项目技能。

### Claude Code

```bash
# 方式一：通过 Marketplace 安装（推荐）
claude install Jesseovo/last30days-skill-cn

# 方式二：手动安装
git clone https://github.com/Jesseovo/last30days-skill-cn.git ~/.claude/skills/last30days-cn
```

### OpenClaw / ClawHub

```bash
git clone https://github.com/Jesseovo/last30days-skill-cn.git ~/.agents/skills/last30days-cn
```

### Gemini CLI

```bash
git clone https://github.com/Jesseovo/last30days-skill-cn.git
# 在 Gemini CLI 中作为扩展加载
```

### 通用 Agent

任何支持 **Bash / Read / Write** 工具的 AI Agent 都可以使用本技能。

---

## ⚙️ 配置指南

### 📍 第一步：安装依赖

```bash
pip install jieba
```

### 📍 第二步：安装爬虫引擎（推荐，可获取 7/8 平台数据）

```bash
pip install playwright
playwright install chromium
```

> 安装 Playwright 后，微博、小红书、抖音、B站（备用）、知乎（备用）均可无需 API Key 使用。

### 📍 第三步：创建配置文件（可选）

如果您希望使用 API 模式获取更稳定的数据，或需要使用微信公众号搜索：

```bash
mkdir -p ~/.config/last30days-cn
touch ~/.config/last30days-cn/.env
chmod 600 ~/.config/last30days-cn/.env
```

**Windows（PowerShell）等价：** 创建目录与空配置文件可用 `New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.config\last30days-cn"` 与 `New-Item -ItemType File -Path "$env:USERPROFILE\.config\last30days-cn\.env" -Force`。限制 `.env` 仅当前用户可读写可近似使用 `icacls "$env:USERPROFILE\.config\last30days-cn\.env" /inheritance:r /grant:r "$($env:USERNAME):(R,W)"`（与 Unix `chmod 600` 意图相近，权限模型不同）。

编辑 `~/.config/last30days-cn/.env`，按需填入 API Key：

```ini
# ============================================
# last30days-cn v2.0 配置文件
# ============================================
# 📌 说明：所有 API Key 均为可选
# 安装 Playwright 后，大部分平台已可通过爬虫模式使用
# API Key 提供更稳定的数据获取方式
# ============================================

# 🔴 微博开放平台（可选，已有爬虫模式替代）
# 获取方式: https://open.weibo.com → 创建应用 → 获取 Access Token
WEIBO_ACCESS_TOKEN=

# 📕 小红书（可选，已有爬虫模式替代）
# 获取方式: https://scrapecreators.com → 注册 → 获取 API Key
SCRAPECREATORS_API_KEY=

# 💬 知乎 Cookie（可选，增强搜索质量）
# 获取方式: 浏览器登录知乎 → F12 → Network → 复制 Cookie 值
ZHIHU_COOKIE=

# 🎵 抖音（可选，已有爬虫模式替代）
# 获取方式: https://tikhub.io → 注册 → 获取 API Key
TIKHUB_API_KEY=

# 💚 微信公众号搜索（目前无爬虫替代，需 API Key 才能使用）
# 获取方式: 使用第三方微信搜索 API 服务商
WECHAT_API_KEY=

# 🔵 百度搜索 API（可选，公开搜索已可用）
# 获取方式: https://cloud.baidu.com → 搜索服务 → 创建应用
BAIDU_API_KEY=
BAIDU_SECRET_KEY=
```

### 📍 第四步：验证配置

```bash
python scripts/last30days.py --diagnose
```

将输出各平台的可用状态和爬虫引擎状态：

```json
{
  "weibo": true,
  "xiaohongshu": false,
  "bilibili": true,
  "zhihu": true,
  "douyin": true,
  "wechat": false,
  "baidu_api": false,
  "toutiao": true,
  "crawler_engine": {
    "playwright_available": true,
    "cached_logins": [],
    "note": "安装 Playwright 后，微博/小红书/抖音/B站/知乎可无需 API Key 使用爬虫模式"
  }
}
```

---

## 🚀 使用方式

### 基本用法

```bash
python scripts/last30days.py "AI编程助手" --emit compact
```

### 命令行参数

| 参数 | 说明 | 示例 |
|:---:|:---:|:---:|
| `--emit` | 输出模式 | `compact` / `json` / `md` / `context` / `path` |
| `--quick` | 快速搜索 | 更少数据源，更快速度 |
| `--deep` | 深度搜索 | 更多数据源，更全面 |
| `--days N` | 回溯天数 | `--days 7`（最近一周） |
| `--search` | 指定搜索源 | `--search weibo,bilibili,zhihu` |
| `--diagnose` | 诊断配置 | 显示各平台可用状态 |
| `--timeout SECS` | 全局超时秒数 | 覆盖默认全局超时 |
| `--save-dir DIR` | 自动保存原始输出目录 | 将原始输出写入指定目录 |
| `--debug` | 调试模式 | 输出详细日志 |

### 使用示例

```bash
# 🔍 搜索 AI 相关话题
python scripts/last30days.py "最新AI工具" --emit compact

# ⚡ 快速搜索，仅 B站和知乎
python scripts/last30days.py "Python教程" --quick --search bilibili,zhihu

# 📊 深度搜索并保存结果
python scripts/last30days.py "新能源汽车" --deep --save-dir ~/Documents/research

# 📋 输出 JSON 格式（适合程序处理）
python scripts/last30days.py "ChatGPT替代品" --emit json

# 🗓️ 仅搜索最近 7 天
python scripts/last30days.py "热门话题" --days 7
```

---

## 🔧 数据获取策略（三级降级）

v2.0 采用三级自动降级策略，确保最大可用性：

```
优先级 1: API 模式（如配置了 API Key）
    ↓ 失败或未配置
优先级 2: 爬虫模式（MediaCrawler，需要 Playwright）
    ↓ 失败或未安装
优先级 3: 公开接口（HTTP 直接请求，无需任何配置）
```

### 各平台数据获取方式对比

| 平台 | API 模式 | 爬虫模式 | 公开接口 |
|:---:|:---:|:---:|:---:|
| 微博 | `WEIBO_ACCESS_TOKEN` | ✅ Playwright | ✅ m.weibo.cn |
| 小红书 | MCP HTTP API(可选) | ✅ Playwright (XHR拦截) | ⚠️ 命中率低 |
| B站 | - | ✅ Playwright(备用) | ✅ 公开 API |
| 知乎 | `ZHIHU_COOKIE`(增强) | ✅ Playwright(备用) | ✅ 公开搜索 |
| 抖音 | `TIKHUB_API_KEY` | ✅ Playwright | ✅ 备用接口 |
| 微信 | `WECHAT_API_KEY` | - | ✅ 搜狗搜索 |
| 百度 | `BAIDU_API_KEY` | - | ⚠️ 公开搜索可能被拦截，Bing 兜底 |
| 头条 | - | - | ✅ 公开接口 |

---

## 🏗️ 项目架构

```
last30days-skill-cn/
├── 📄 SKILL.md              # Agent 技能定义文件
├── 📄 README.md             # 项目说明（本文件）
├── 📄 LICENSE               # MIT 许可证
├── 📄 requirements.txt      # Python 依赖
├── 📁 scripts/
│   ├── 🐍 last30days.py     # 主入口 CLI
│   └── 📁 lib/
│       ├── crawler_bridge.py  # 🆕 MediaCrawler 爬虫桥接模块
│       ├── weibo.py          # 微博搜索模块
│       ├── xiaohongshu.py    # 小红书搜索模块
│       ├── bilibili.py       # B站搜索模块
│       ├── zhihu.py          # 知乎搜索模块
│       ├── douyin.py         # 抖音搜索模块
│       ├── wechat.py         # 微信公众号模块
│       ├── baidu.py          # 百度搜索模块
│       ├── toutiao.py        # 今日头条模块
│       ├── schema.py         # 数据结构定义
│       ├── score.py          # 评分系统
│       ├── normalize.py      # 数据标准化
│       ├── dedupe.py         # 去重
│       ├── render.py         # 输出渲染
│       ├── relevance.py      # 相关性计算
│       ├── query.py          # 查询预处理
│       ├── query_type.py     # 查询类型检测
│       ├── entity_extract.py # 实体抽取
│       ├── env.py            # 环境配置管理
│       ├── cache.py          # 缓存管理
│       ├── dates.py          # 日期工具
│       ├── http.py           # HTTP 客户端
│       ├── ui.py             # 终端 UI
│       └── setup_wizard.py   # 配置向导
├── 📁 fixtures/              # 示例数据
├── 📁 tests/                 # 测试用例
└── 📁 hooks/                 # Agent 钩子
```

---

## 📊 评分系统

每条搜索结果的综合评分（0-100）基于：

| 维度 | 权重 | 说明 |
|:---:|:---:|:---|
| 🎯 相关性 | 45% | 与查询主题的文本匹配度 |
| 🕐 时效性 | 25% | 内容发布时间的新鲜程度 |
| 🔥 互动度 | 30% | 各平台互动指标（见下表） |

### 各平台互动指标

| 平台 | 互动指标 |
|:---:|:---|
| 微博 | 转发 + 评论 + 点赞 |
| 小红书 | 点赞 + 收藏 + 评论 + 分享 |
| B站 | 播放 + 弹幕 + 评论 + 投币 + 收藏 |
| 知乎 | 赞同 + 评论 + 收藏 |
| 抖音 | 点赞 + 评论 + 分享 + 播放 |
| 头条 | 评论 + 阅读 + 点赞 |

---

## 🙏 致谢

- [mvanhorn/last30days-skill](https://github.com/mvanhorn/last30days-skill) — 原始英文版项目
- [NanmiCoder/MediaCrawler](https://github.com/NanmiCoder/MediaCrawler) — 爬虫引擎技术灵感来源

---

## 📜 许可证

本项目基于 [MIT License](LICENSE) 发布。

- 🔗 原始项目: [mvanhorn/last30days-skill](https://github.com/mvanhorn/last30days-skill) by Matt Van Horn
- 🇨🇳 中文本土化: Jesse ([@Jesseovo](https://github.com/Jesseovo))

---

---

# 📰 last30days-cn — Chinese Platform Deep Research Engine

> 🚀 30 days of research. 30 seconds of work. 8 platforms. Zero stale info.

**last30days-cn** is an AI Agent skill that automatically searches 8 major Chinese internet platforms for the last 30 days of content and generates well-cited research reports.

🔗 This project is a Chinese-localized fork of [mvanhorn/last30days-skill](https://github.com/mvanhorn/last30days-skill), fully adapted for Chinese users and platforms.

🕷️ v2.0 integrates [MediaCrawler](https://github.com/NanmiCoder/MediaCrawler) crawler engine concepts, significantly reducing API key dependencies.

👤 **Author:** Jesse ([@Jesseovo](https://github.com/Jesseovo))

---

## ⚠️ Disclaimer

> **This project is for educational and research purposes only.**

1. All crawler features are intended solely for technical learning and research. **Commercial use is strictly prohibited.**
2. Users must comply with all applicable laws and regulations, including but not limited to data protection and privacy laws.
3. Users must respect each platform's Terms of Service (ToS) and robots.txt.
4. The developer assumes **no liability** for any legal consequences arising from the use of this project.
5. **Do NOT** use this project for large-scale data scraping, personal data collection, or any illegal activities.

---

## ✨ Key Features (v2.0)

- 🔍 **8 Chinese Platforms** — Weibo, Xiaohongshu, Bilibili, Zhihu, Douyin, WeChat, Baidu, Toutiao
- 🕷️ **MediaCrawler Integration** — Playwright-based browser automation, 7/8 platforms work without API keys
- 🤖 **Multi-Agent Compatible** — Works with Cursor, Claude Code, OpenClaw, Gemini CLI, and more
- 🇨🇳 **Chinese NLP** — jieba-based word segmentation, Chinese stopwords, synonym expansion
- 📊 **Smart Scoring** — Relevance 45% + Recency 25% + Engagement 30%
- 🔄 **Three-tier Fallback** — API → Crawler → Public API, automatic degradation

---

## 🚀 Quick Start

### Installation

```bash
git clone https://github.com/Jesseovo/last30days-skill-cn.git
cd last30days-skill-cn
pip install jieba

# Optional: Install Playwright for crawler mode (enables 7/8 platforms without API keys)
pip install playwright
playwright install chromium
```

### Configuration

```bash
mkdir -p ~/.config/last30days-cn
# Edit ~/.config/last30days-cn/.env with your API keys (all optional)
```

**Windows (PowerShell):** create the config directory with `New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.config\last30days-cn"`, then create the file with `New-Item -ItemType File -Path "$env:USERPROFILE\.config\last30days-cn\.env" -Force` (or edit `%USERPROFILE%\.config\last30days-cn\.env` in your editor). To restrict `.env` to the current user (similar intent to `chmod 600`; ACL model differs), run `icacls "$env:USERPROFILE\.config\last30days-cn\.env" /inheritance:r /grant:r "$($env:USERNAME):(R,W)"`.

### Usage

```bash
python scripts/last30days.py "AI tools" --emit compact
python scripts/last30days.py --diagnose   # Check platform availability
```

### Agent Installation

| Agent Platform | Installation Path |
|:---:|:---|
| **Cursor** | Clone and add SKILL.md as project skill |
| **Claude Code** | `claude install Jesseovo/last30days-skill-cn` |
| **OpenClaw** | `~/.agents/skills/last30days-cn` |
| **Gemini CLI** | Load as Gemini extension |
| **General** | Any agent with Bash/Read/Write tools |

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).

- 🔗 Original: [mvanhorn/last30days-skill](https://github.com/mvanhorn/last30days-skill) by Matt Van Horn
- 🇨🇳 Chinese Fork: Jesse ([@Jesseovo](https://github.com/Jesseovo))
