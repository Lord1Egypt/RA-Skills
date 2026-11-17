<p align="center">
  <img alt="mu-skill-hunter" src="assets/default-banner.png" width="100%">
</p>

# 🔍 mu-skill-hunter · Skill严选猎手

> 四源发现、安全审查、趋势追踪——GitHub / ClawHub / SkillHub / Skills.sh 一站式 Skill 搜索工具，支持关键词搜索、12 条安全规则审查、定时趋势报告。

[English](README.md) | **中文** | [🌐 在线主页](https://muippt.github.io/mu-skill-hunter/)

[![微信公众号](https://img.shields.io/badge/muippt-07C160?logo=wechat&logoColor=white)](https://mp.weixin.qq.com/s/YLtXENt_7WzO2DgJCFUtPA)
[![小红书](https://img.shields.io/badge/muippt-FF2442?logo=xiaohongshu&logoColor=white)](https://xhslink.com/m/ESxtgUNMdl)
[![书籍](https://img.shields.io/badge/书籍-图解团队管理-BBDDE5?logo=bookstack&logoColor=white)](https://item.m.jd.com/product/14547345.html)
[![mu-skill集合](https://img.shields.io/badge/mu--skill集合-9E95B7?logo=refinedgithub&logoColor=white)](https://muippt.github.io/mu-skill-hub/)
[![License](https://img.shields.io/github/license/muippt/mu-skill-hunter)](LICENSE)
[![Version](https://img.shields.io/github/v/release/muippt/mu-skill-hunter)](https://github.com/muippt/mu-skill-hunter/releases)
[![Stars](https://img.shields.io/github/stars/muippt/mu-skill-hunter)](https://github.com/muippt/mu-skill-hunter/stargazers)

---

### 💡 使用场景示例

- 🔍 **"找一个能填写PDF表单的Skill"** — 同时搜索四个源，返回带描述、链接、热度指标的排序结果
- 🛡️ **"安装前帮我审查这个Skill"** — 下载到沙箱暂存区，运行 12 条规则静态安全扫描，报告风险等级（LOW/MEDIUM/HIGH/EXTREME）
- 📊 **"这周有什么新Skill？"** — 生成本周热门 Top 8 周报，三维严选（热度50% + 相关性30% + 新鲜度20%）
- 📦 **"在ClawHub上搜MCP工具"** — 指定单源搜索，并行调用 `clawhub inspect` 获取下载量和摘要
- 🐉 **"在SkillHub上找Skill（国内）"** — 查询腾讯SkillHub公开API，国内加速、合规的技能搜索
- ⏰ **"建立每周自动周报"** — 定时自动巡检，按你设定的频率推送精选推荐到消息平台
- 🧹 **"找本周GitHub上新建的Agent Skill"** — 追踪本周新建仓库，在走红前发现新项目
- ✅ **"安全安装这个Skill"** — 暂存区隔离 + scanner.py审计 + 风险分级安装命令输出

---

### ✨ 核心亮点

#### 🌐 四源采集

| 数据源 | API类型 | 是否需要鉴权 | 优势 |
|--------|---------|-------------|------|
| GitHub | HTTP API | GITHUB_TOKEN（可选，60→5000次/h） | 最大的仓库池，stars/语言/更新元数据 |
| ClawHub | CLI (npx) | 无需 | 精选Skill注册表，inspect获取下载量/摘要 |
| SkillHub | HTTP API + CLI | 无需（公开） | 国内加速，腾讯出品，CN友好 |
| Skills.sh | CLI (npx) | 无需 | 安装量可见，新兴生态 |

根据你输入的关键词，搜索引擎并行查询全部4个源，去重后以统一排序展示，来源标签区分（🐙GitHub / 🦀ClawHub / 🐉SkillHub / 🛠️Skills.sh）。

#### 🛡️ 12条安全审查规则

每个外部Skill在安装前都通过 `scanner.py` 扫描：

- **10条硬拒绝规则**（R1-R10）：外部URL请求、base64解码执行、eval/exec动态执行、凭证路径访问、Agent文件访问、代码混淆、裸IP请求、提权操作、凭证外发、未声明包安装
- **2条AI特有规则**（AI1-AI2）：Prompt Injection检测、挖矿特征检测
- **4条黄旗规则**（Y1-Y4）：Agent目录写入、网络请求、环境变量修改、后台进程

扫描器只输出**摘要信息**（rule_id、文件名、行号），不输出原始代码——防止扫描内容中的 Prompt Injection。

#### 📊 三维严选机制

```
严选依据 = 热度 (50%) + 相关性 (30%) + 新鲜度 (20%)
```

- **热度**：stars/下载量的对数归一化
- **相关性**：关键词命中密度（agent-skill、mcp、automation等）
- **新鲜度**：本周新建=20，本月=10，更早=2

周报强制混排：≥4 GitHub + ≥2 ClawHub + ≥1 SkillHub + ≥1 Skills.sh（有数据时）。

#### 📨 定时趋势报告

- 精选推荐 + 备选区，按三维严选排序
- 来源强制多样性，防止单一来源霸榜
- 去重：ClawHub按slug，GitHub同作者≤2
- 定时自动推送到你常用的消息平台
- 推送频率完全可自定义——每周、每两周，按你的节奏来

---

### 📌 与同类工具对比

| 功能 | mu-skill-hunter | 手动GitHub搜索 | 仅ClawHub CLI | 仅Skills.sh |
|------|----------------|---------------|---------------|-------------|
| 数据源 | 4个（GitHub + ClawHub + SkillHub + Skills.sh） | 1个（GitHub） | 1个（ClawHub） | 1个（Skills.sh） |
| 安全扫描 | 12条规则静态分析 | 无 | 无 | 无 |
| 三维严选 | 热度 + 相关性 + 新鲜度 | 无 | 无 | 无 |
| 周报 | 定时自动 + 精选推荐 | 手动 | 无 | 无 |
| 并行搜索 | 四源同时 | 串行 | 单源 | 单源 |
| 下载量 | ClawHub inspect + SkillHub API | 无 | 有 | 有 |
| 国内加速 | SkillHub（腾讯） | 无 | 无 | 无 |
| 风险分级安装 | 四级（LOW/MED/HIGH/EXTREME） | 用户自行判断 | 无 | 无 |
| Prompt Injection防护 | AI1规则 + 沙箱隔离 | 无 | 无 | 无 |

---

### 🚀 三大工作流

| 工作流 | 场景 | 触发方式 |
|--------|------|---------|
| 🔍 搜索发现 | "找一个能做X的Skill" | 用户描述需求或说"找Skill" |
| 🛡️ 安全审查 | "帮我审查/安装这个Skill" | 用户准备安装某个外部Skill |
| 📊 周报推送 | 每周热门Skill摘要 | 定时（频率可自定义）或手动 `trending.py --period weekly` |

---

### ⚙️ 技术规格

| 项目 | 说明 |
|------|------|
| 语言 | Python 3.8+ |
| 依赖 | 无（仅标准库：urllib, subprocess, json, re, argparse） |
| 外部CLI（可选） | `clawhub`（npm）、`skillhub`（curl安装）、`skills`（npm） |
| GitHub API | REST v3，GITHUB_TOKEN可选（60→5000次/h） |
| SkillHub API | 公开HTTP，无需鉴权 |
| 输出格式 | 人类可读表格（默认）或 JSON（`--json` 参数） |
| 安全扫描器 | 12条规则（10条硬拒绝 + 2条AI特有）+ 4条黄旗 |
| 严选机制 | 热度50% + 相关性30% + 新鲜度20%，三维综合排序 |
| 平台 | macOS / Linux / Windows（Python 3.8+） |
| 包体积 | ~50KB（3个Python脚本 + 3个参考文档） |

---

### 🛠️ 快速开始

**1. 克隆并配置**

```bash
git clone https://github.com/muippt/mu-skill-hunter.git
cd mu-skill-hunter
# 可选：配置 GitHub Token 提升搜索速率
export GITHUB_TOKEN="your_github_token"
```

**2. 四源搜索**

```bash
python3 scripts/search.py "agent skill mcp" --limit 8
```

**3. 安装前安全审查**

```bash
python3 scripts/scanner.py /path/to/external-skill --json
```

---

### 🔒 安全与隐私

- **纯本地运行** — 所有脚本在本机执行，不向任何服务器发送数据
- **无遥测** — 零追踪、零分析、零回传
- **沙箱暂存** — 外部Skill下载到 `/tmp/skill-hunter-staging/`，绝不直接安装到正式目录
- **扫描器隔离** — `scanner.py` 只输出摘要，不输出原始代码，防止扫描内容中的 Prompt Injection
- **风险分级安装** — 四级风险评估（🟢 LOW / 🟡 MEDIUM / 🔴 HIGH / ⛔ EXTREME），HIGH/EXTREME 必须人工确认
- **Token安全** — GITHUB_TOKEN 仅从环境变量读取，绝不写入任何文件

---

### ⭐ Star 趋势

如果 mu-skill-hunter 帮你发现了好用的 Skill，欢迎给个 Star！⭐

[![Star History Chart](assets/star-history.png)](https://www.star-history.com/?repos=muippt%2Fmu-skill-hunter&type=date)

> 四源发现、12条安全规则、1套三维严选——放心搜索、审查、安装 AI Agent Skill。

---

### 👤 作者简介

🎓 清华大学出版社签约作家 / 2026当当影响力作家 / 某互联网大厂 AI 大模型业务 HR 砖家 / 一级人力资源管理师 / 二级心理咨询师 / 野生设计师

📚 著有[《图解团队管理》](https://item.m.jd.com/product/14547345.html)，服务客户有字节跳动、腾讯、百度、中国移动、SMG、BOE…

💡 [微信公众号](https://mp.weixin.qq.com/s/YLtXENt_7WzO2DgJCFUtPA) / [小红书](https://xhslink.com/m/ESxtgUNMdl)：muippt

### 📄 许可证与致谢

[MIT](LICENSE) © 2026 木先生iPPT

本项目基于以下优秀平台和工具构建：
- [GitHub API](https://docs.github.com/en/rest) — 仓库搜索与元数据
- [ClawHub](https://clawhub.ai) — 精选 AI Agent Skill 注册表
- [SkillHub](https://skillhub.cn) — 腾讯出品的国内加速 Skill 商店
- [Skills.sh](https://skills.sh) — 新兴 Skill 发现平台

> 声明：本项目大部分内容由 AI 辅助完成。如您认为您的作品被使用但未获得适当署名，请提交 issue。
