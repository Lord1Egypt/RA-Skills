# Mp2rss Skill

[![License: MIT-0](https://img.shields.io/badge/License-MIT--0-blue.svg)](https://opensource.org/licenses/MIT-0)

让 AI Agent 帮你管理 **微信公众号** 与 **X（Twitter）账号** 的 RSS 订阅 —— 一句话订阅、自然语言查找、按需读历史文章 / 推文 / 长文。

本仓库是 [Mp2rss](https://mp2rss.bugcode.dev) 服务的 OpenClaw Agent Skill 包，基于 [`mp2rss` CLI](https://github.com/areyoubugcoder/mp2rss-cli) 实现。

---

## ✨ 核心能力

### 微信公众号（MP）

| 能力 | 说明 |
|------|------|
| 📡 **一键订阅** | 发一个公众号文章链接（`mp.weixin.qq.com/s/...`），Agent 自动把整个公众号订阅到你的 Feed |
| 📋 **列表与搜索** | 「我订阅了哪些公众号」「搜一下我订阅的财经类公众号」 |
| 🗑️ **取消订阅** | 「把 某号 从订阅里删了」，Agent 先核对 mpId 再删 |
| 📰 **历史文章** | 「某号 最近发了什么」/「拉一下 某号 的文章」 |

### X（Twitter）账号

| 能力 | 说明 |
|------|------|
| 🐦 **列出 X 订阅** | 「我订阅了哪些 X 账号」 |
| 📨 **推文流** | 「@elonmusk 最近发了啥」（Agent 先 `x list` 找到 `xUserId` 再拉推文） |
| 📝 **长文流** | 「拉一下 某 X 账号的 Articles」 |
| ⚠️ **订阅 / 取消订阅 X 账号** | **仅在 Web 控制台**（<https://mp2rss.bugcode.dev/>）—— CLI 与 API 都不暴露 X 写类端点，Agent 会引导你去控制台 |

### 通用

| 能力 | 说明 |
|------|------|
| 🔐 **登录态管理** | 「我的 Feed Key 是什么」「登录 mp2rss」 |
| 📤 **结构化输出** | 所有命令支持 `-o json`，Agent 可直接解析做后续处理 |

---

## 💡 使用场景

### 通勤路上看到好公众号

> 👤 订阅这个公众号 https://mp.weixin.qq.com/s/abc123xyz
>
> 🤖 已订阅「某公众号」到你的 Feed。

### 不记得订过哪些号

> 👤 我订阅了哪些公众号？
>
> 🤖 当前共 42 个订阅。前 20 个：某公众号（最近发文 2 小时前）、另一个号（昨天）……

### 找特定主题

> 👤 我订阅的财经类公众号有哪些
>
> 🤖 找到 5 个匹配：财经早知道、第一财经……

### 翻看历史

> 👤 财经早知道 最近发了什么
>
> 🤖 最近 10 篇文章：1. xxx 标题（昨天）2. xxx 标题（前天）……

### 不想看了

> 👤 把 财经早知道 从订阅里删了
>
> 🤖 确认删除「财经早知道」（mpId 123456）？已删除 ✓

### 看大 V 推文

> 👤 @elonmusk 最近发了啥？
>
> 🤖 （先 `x list` 拿到 xUserId 44196397）最近 5 条推文：1. ……

### 想订阅一个 X 账号

> 👤 帮我订阅 @paulg 这个号
>
> 🤖 X 账号的订阅 / 取消订阅只能在 Web 控制台操作。打开 https://mp2rss.bugcode.dev/「订阅管理 → X」搜索 paulg 完成订阅；订阅好我就能用 `mp2rss x posts/articles` 帮你拉内容。

---

## 📦 安装

### 前置：装 Mp2rss CLI 二进制

skill 本身只描述如何调用 CLI，所以必须先装 `mp2rss` 二进制（任选其一）：

```bash
# 方式 A：npm（推荐，跨平台一致）
pnpm add -g @mp2rss/cli

# 方式 B：macOS / Linux 一键脚本
curl -fsSL https://raw.githubusercontent.com/areyoubugcoder/mp2rss-cli/main/scripts/install.sh | sh
```

也可在 [Releases](https://github.com/areyoubugcoder/mp2rss-cli/releases/latest) 下载对应平台二进制。

### 装 Skill

```bash
# 方式 A：通过 ClawHub（推荐）
openclaw skills install mp2rss

# 方式 B：手动
mkdir -p ~/.openclaw/workspace/skills/mp2rss
cd ~/.openclaw/workspace/skills/mp2rss
curl -sL https://raw.githubusercontent.com/areyoubugcoder/mp2rss-openclaw/main/SKILL.md -o SKILL.md
curl -sL https://raw.githubusercontent.com/areyoubugcoder/mp2rss-openclaw/main/package.json -o package.json
# 视需要再拉 references/ 子文档
```

---

## 🔑 授权登录

安装完成后说「登录 mp2rss」，Agent 自动跑 `mp2rss auth login` 走浏览器 loopback 授权。CI / 无头环境用：

```bash
mp2rss auth login -k <feed-key>            # 直传
mp2rss auth login --no-browser             # 远程模式，仅打印授权 URL
```

Feed Key 可在 <https://mp2rss.bugcode.dev/> 登录后查看或重置。配置文件位置 `~/.mp2rss/config.json`。

### 用环境变量配置（可选）

```bash
export MP2RSS_FEED_KEY=gk_live_xxxxxxxx
export MP2RSS_API_URL=https://mp2rss.bugcode.dev    # 自托管时需要
```

优先级（高 → 低）：CLI flag `--api-key` > `MP2RSS_FEED_KEY` env > `~/.mp2rss/config.json`。

---

## 🛠 子命令速查

### 通用

| 命令 | 说明 |
|------|------|
| `mp2rss auth login [-k <key>] [--no-browser]` | 登录（三种模式：浏览器 / Feed Key 直传 / 远程） |
| `mp2rss auth status [-o json]` | 查登录态、Feed Key 来源、最近登录时间 |
| `mp2rss auth logout` | 清空 Feed Key |

### 微信公众号

| 命令 | 说明 |
|------|------|
| `mp2rss mp subscribe <article-url> [-o json]` | 订阅；参数必须是 `mp.weixin.qq.com/s/...` 文章 URL |
| `mp2rss mp list [-q <kw>] [-p <page>] [--page-size <n>]` | 列出公众号订阅 |
| `mp2rss mp search <keyword>` | `mp list -q` 语法糖 |
| `mp2rss mp remove <mpId> [-y]` | 取消订阅公众号 |
| `mp2rss mp articles <mpId> [-p <page>] [--page-size <n>]` | 查公众号历史文章 |

### X（Twitter）

| 命令 | 说明 |
|------|------|
| `mp2rss x list [-q <kw>] [-p <page>] [--page-size <n>]` | 列出已订阅的 X 账号 |
| `mp2rss x posts <xUserId> [-p <page>] [--page-size <n>]` | 拉 X 账号推文流 |
| `mp2rss x articles <xUserId> [-p <page>] [--page-size <n>]` | 拉 X 账号长文流 |

> X 账号**搜索 / 订阅 / 取消订阅**仅 Web 控制台支持，CLI 与 Open API 都不暴露这些写类端点。

完整字段、JSON shape 与 Agent 行为规范见 [SKILL.md](SKILL.md) 和 [references/](references/) 子文档。

---

## ⚠️ 重要约束

- **订阅公众号传的是文章 URL** —— 不是公众号名、不是二维码、不是公众号主页。识别不到合法文章 URL 时 Agent 应反问用户索要任意一篇文章链接
- **`mpId` 是 int64** —— JS 环境解析 JSON 时需先把 `mpId` 替换为字符串再 `JSON.parse`，否则精度丢失
- **`xUserId` 是字符串** —— 虽然内容是数字串，API 契约即字符串形态，无需转换；注意不要传 `@handle`
- **取消订阅公众号前先核对 mpId** —— 用 `mp list -q` / `mp search` 拿到准确 mpId 再删，避免误删
- **X 写类操作不可达** —— 用户要订阅 / 取消订阅 X 账号时，Agent 必须引导到 Web 控制台「订阅管理 → X」，不要尝试构造 CLI 命令
- **`auth login` 不支持 `-o json`** —— 仅输出文本反馈，其它子命令均支持

---

## 🔗 相关

- [Mp2rss 服务](https://mp2rss.bugcode.dev) —— 微信公众号 / X 账号 RSS 订阅服务
- [`mp2rss` CLI](https://github.com/areyoubugcoder/mp2rss-cli) —— Go 命令行客户端（Skill 调用的底层）
- [Mp2rss 文档站](https://areyoubugcoder.github.io/Mp2RSS/) —— 服务介绍、Open API 与 CLI 完整文档

---

## License

[MIT-0](LICENSE)
