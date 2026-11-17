# 🌊 kurobbs-wiki — 库街区鸣潮 WIKI 查询 + 配队助手

> 🌍 **Read this in** · [English](README.en.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [中文](README.md)

一个遵循 **Agent Skill 开放标准**（SKILL.md）的通用技能，直接通过库街区（kurobbs）公开 API 查询鸣潮（Wuthering Waves）的图鉴、攻略与角色资料，并内置**机制画像 + 配队引擎**，还能登录你自己的库街区账号、用真实角色池组队。支持任意能加载 Agent Skill 的 AI（Claude、Cursor、Copilot、Gemini、OpenClaw 等）。

> 本项目灵感来自日常打鸣潮时"查角色攻略、配队要靠一个个翻网页"的痛点，做成一个 skill 就能在对话里直接问。

---

## ✨ 功能一览

| 模块 | 命令 | 说明 |
|------|------|------|
| 🔍 目录/列表 | `tree` / `list` | 分类目录树（170+ 节点）+ 分类下条目 |
| 📖 词条详情 | `detail` | 角色/武器/道具/攻略详情，支持 `--render` Markdown 排版、`--section` 精确取段 |
| 🔎 名称搜索 | `search` | 跨分类搜索，自动遍历三级子分类 |
| 🖼️ 社区帖媒体 | `post` | 绕过 WAF 抓一图流/视频帖的图片、封面、m3u8 视频 |
| 🧠 机制画像 | `probe` | 6 维度机制档案（效应/增益/流派/技能/声骸/武器） |
| 🤝 配对引擎 | `pair` / `team` | 双角色 5 维兼容评分、池选队、全量 60 人枚举、攻略交叉验证补池 |
| 🎯 LLM 精排 | `candidates` + `--profile` | 规则粗筛候选 + LLM 逐队精排（配队最准） |
| 👤 我的账号 | `my` | 登录库街区、查真实角色、用自己角色配队、token 续期 |

---

## 📦 安装

### 方式一：从本地目录安装（最简）

把本仓库 `kurobbs-wiki/` 目录放入你的 AI 的 skills 目录（Claude Code、Cursor、Copilot 等均支持），或在支持该目录的 agent 中：

```bash
# 将 SKILL_DIR 指向本仓库根目录的绝对路径
# Windows 示例
set SKILL_DIR=D:\tools\kurobbs-wiki

# macOS / Linux 示例
export SKILL_DIR=~/tools/kurobbs-wiki
```

### 方式二：通过 npx skills（若已收录到市场后）

```bash
npx skills add Alphamancer/kurobbs-wiki
```

> 发布后即可通过市场一键安装，详见下方「发布与收录」。

### 依赖

- **Python 3.8+**（纯标准库，`wikiquery.py` 无第三方依赖）
- **Playwright**（仅 `post` 抓取社区帖媒体时需要）
  ```bash
  pip install playwright && playwright install chromium
  ```
- **ffmpeg**（可选，`--download-video` 下载 m3u8 视频为 mp4 时用）

---

## 🚀 快速上手

```bash
cd $SKILL_DIR

# 1. 初始化目录树（缓存到 ~/.kurobbs-wiki-cache/）
python -X utf8 -u scripts/wikiquery.py tree

# 2. 搜索角色
python -X utf8 -u scripts/wikiquery.py search 穗穗 --preview --limit 3

# 3. 取攻略正文某小节
python -X utf8 -u scripts/wikiquery.py detail <previewEntryId> --section "编队&队伍轴推荐"

# 4. 机制画像 + 配队
python -X utf8 -u scripts/wikiquery.py probe 穗穗
python -X utf8 -u scripts/wikiquery.py team 穗穗 --pool 洛瑟菈,今汐,秧秧 --top 3

# 5. 登录你的账号，用真实角色配队
python -X utf8 -u scripts/wikiquery.py my login    # 浏览器里填手机号→拖滑块→填验证码
python -X utf8 -u scripts/wikiquery.py my roles
python -X utf8 -u scripts/wikiquery.py my team 穗穗 --guide-pool --top 5
```

> 💡 **提示**：所有命令都应在 skill 目录下执行，且带上 `-X utf8 -u`（Windows 下中文/emoji 输出需要）。

---

## 🧠 配队引擎怎么用

### 双角色评分

```bash
python -X utf8 -u scripts/wikiquery.py pair 穗穗 洛瑟菈
```

5 维度各 20 分：效应协同 / 延奏匹配 / 定位互补 / 声骸联动 / 触发闭环。≥80 高度契合。

### 从角色池组队

```bash
python -X utf8 -u scripts/wikiquery.py team 穗穗 --pool 洛瑟菈,今汐,秧秧 --top 3   # 指定池子
python -X utf8 -u scripts/wikiquery.py team 穗穗 --all --top 5                    # 全量枚举 60 人
python -X utf8 -u scripts/wikiquery.py team 穗穗 --guide-pool --top 5             # 攻略交叉验证自动补池
```

每个队伍会标注来源：🟢 攻略实锤 / 🟡 混合 / 🔵 引擎推断，并附 📚 攻略 URL 供你点击验证。

### LLM 精排（配队最准）

```bash
# 步骤 1：规则粗筛候选池（秒级）
python -X utf8 -u scripts/wikiquery.py candidates 绯雪 --guide-pool

# 步骤 2：拿候选队伍 + 三角色六维度完整画像（输出很大，重定向到文件）
python -X utf8 -u scripts/wikiquery.py team 绯雪 --pool 千咲,维里奈,穗穗 --profile --top 10 > %TEMP%\team_profile.txt
```

由 Claude 基于真实画像数据逐队 6 维度精排，识别"机制拐"、"协奏副C"等规则难判断的定位。

---

## 🔐 隐私与数据说明

> ⚠️ **请务必阅读**——本 skill 包含读取你账号数据的登录功能。

- **WIKI 查询（`tree`/`list`/`detail`/`search`/`probe`/`pair`/`team`）**：全部走**公开、无鉴权**的 API，**不需要登录**，不涉及任何个人数据。
- **「我的账号」功能（`my login`/`my roles`/`my team`/`my sync`）**：需要你主动在浏览器里登录库街区。登录后，以下数据会**保存在你本地** `~/.kurobbs-wiki-cache/`：
  - `account.json` — 登录 token + 你的角色列表
  - `role_details/` — 每个角色的共鸣链解锁、实际武器/声骸、技能等级、面板
- **这些数据只存本机，不会上传到任何服务器**。token 约 45 分钟过期，`my renew` 可续期。
- 本 skill **不会**在未登录时猜测或伪造你的账号角色，也不会向第三方发送你的账号数据。

**如果你想完全离线/不登录**：只用 `tree`/`search`/`detail`/`probe`/`pair`/`team` 即可，完全不需要 `my` 系列命令。

---

## 📚 目录结构

```
kurobbs-wiki/
├── SKILL.md               # Skill 指令（触发条件、命令速查、工作流、关键坑）
├── README.md              # 本文件（中文，面向使用者）
├── README.en.md           # English 版本
├── README.ja.md           # 日本語 版本
├── README.ko.md           # 한국어 版本
├── PUBLISHING.md          # 发布操作清单（作者专用，面向使用者无需看）
├── _meta.json             # skill 元数据
├── references/
│   └── catalogue-map.md   # 分类 ID 映射速查表（170+ 节点）
└── scripts/
    ├── wikiquery.py       # 主 CLI（tree/list/detail/search/probe/pair/team/candidates/my）纯标准库
    ├── post_fetch.py      # 社区帖媒体抓取（Playwright 绕过 WAF）
    └── kuro_login.py      # 登录库街区（浏览器交互）
```

---

## ⚠️ 已知限制

- **私有 API，无官方文档**：字段结构可能随库街区改版变化；报错时先 `tree --refresh` 重拉目录树。
- **低频使用**：公开无鉴权接口，频繁请求可能触发风控，脚本内置 0.05s 限速。
- **分类动态变化**：游戏更新会新增版本活动分类，搜不到新内容时 `list <分类> --refresh` 或 `tree --refresh`。
- **攻略词条是"占位卡片"**：`detail <5位id>` 可能返回 2031，需用 `search --preview` 拿内嵌真实 entryId（这是结构，不是 bug）。
- **Windows 必须带 `-X utf8 -u`**：否则中文/emoji 输出会在 GBK 编码下崩溃。

---

## 🧾 许可证

[MIT](LICENSE)

---

## 🙏 喜欢的话，帮它被更多人看到

如果你觉得这个 skill 有用，欢迎把它分享给玩鸣潮的朋友，或收录到你的 skill 市场。

安装命令：

```bash
npx skills add Alphamancer/kurobbs-wiki
```

---

## 🤝 贡献

欢迎提 issue 和 PR。开发时注意：

- 修改后跑 `python -X utf8 -c "import py_compile; py_compile.compile('scripts/wikiquery.py', doraise=True)"` 验证语法
- 保持 `wikiquery.py` 纯标准库（`post` 子命令除外），避免给查询主流程加第三方依赖
- 遵守 SKILL.md 中的「关键坑」与「已知卡点速查」约定
