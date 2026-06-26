---
name: opencli-content-hunter
description: 基于 opencli 的多平台内容捕手技能。抓取全球热门内容、趋势热点、搜索关键词相关内容。**每当用户提到抓多平台、搜全网、全网热点、多平台抓取时必须触发此技能。** 支持65+平台。每次执行时主动让用户确认平台范围和登录意愿，之后用户可随时说"调整平台"重新选择。触发词：多平台抓取、全网热点、搜全网、opencli抓取、全平台热门。
---

# opencli 内容捕手技能

## 概述

基于 `@jackwener/opencli` 的多平台内容抓取技能，复用 Chrome 登录态，零风控、秒级响应，支持 **65+ 平台**。

---

## 支持平台全列表

### 🇨🇳 国内平台

| 平台 | 热门命令 | 搜索命令 | 深度抓取 |
|------|---------|---------|---------|
| 小红书 | `feed` | `search "关键词"` | `creator-notes` `user` |
| B站 | `hot` `ranking` | `search "关键词"` | `comments` `subtitle` |
| 知乎 | `hot` | `search "关键词"` | `question` `download` |
| 微博 | `hot` | `search "关键词"` | `user` `comments` |
| 雪球 | `hot-stock` `hot` | `search "关键词"` | `stock` `comments` |
| 即刻 | `feed` | `search "关键词"` | - |
| 36氪 | `hot` `news` | `search "关键词"` | `article` |
| 豆瓣 | `movie-hot` `book-hot` | `search "关键词"` | `top250` `reviews` |
| 什么值得买 | - | `search "关键词"` | - |
| 新浪财经 | - | `search "关键词"` | `stock` `rolling-news` |
| 携程 | - | `search "关键词"` | - |
| Boss直聘 | - | `search "关键词"` | `detail` `chatlist` |
| 学习通 | - | - | `assignments` `exams` |
| 微信公众号 | - | - | `download` |
| 微信读书 | `ranking` | `search "关键词"` | `shelf` `highlights` |
| V2EX | `hot` `latest` | - | `topic` `replies` |
| 新浪博客 | `hot` | `search "关键词"` | `article` `user` |

### 🌍 国外平台

| 平台 | 热门命令 | 搜索命令 | 深度抓取 |
|------|---------|---------|---------|
| Twitter/X | `trending` `timeline` | `search "关键词"` | `profile` `thread` |
| Reddit | `hot` `frontpage` `popular` | `search "关键词"` | `subreddit` `read` |
| YouTube | - | `search "关键词"` | `video` `channel` `transcript` |
| Instagram | `explore` | `search "关键词"` | `profile` |
| TikTok | `explore` | `search "关键词"` | `profile` |
| LinkedIn | - | `search "关键词"` | `timeline` |
| Hacker News | `top` `new` `best` | `search "关键词"` | `user` |
| Product Hunt | `hot` `today` | - | `browse` |
| Bluesky | `trending` | `search "关键词"` | `profile` `thread` |
| DEV.to | `top` | - | `tag` `user` |
| Stack Overflow | `hot` `bounties` | `search "关键词"` | - |
| Steam | - | - | `top-sellers` |
| Substack | `feed` | `search "关键词"` | `publication` |
| arxiv | - | `search "关键词"` | `paper` |
| Hugging Face | `top` | - | - |
| BBC | `news` | - | - |
| Bloomberg | `main` `markets` `tech` | - | `news` |
| Google News | `news` | `search "关键词"` | - |
| Google Trends | `trends` | - | - |
| Wikipedia | - | `search "关键词"` | `summary` `trending` |

### 💰 金融/投资平台

| 平台 | 热门命令 | 搜索命令 | 深度抓取 |
|------|---------|---------|---------|
| 雪球 | `hot-stock` `hot` | `search "股票"` | `stock` `fund` |
| 新浪财经 | - | `search "股票"` | `stock` `news` |
| Yahoo Finance | - | `search "股票"` | `quote` |
| Barchart | - | - | `quote` `options` `greeks` |

### 🎨 图片/设计平台

| 平台 | 热门命令 | 搜索命令 | 深度抓取 |
|------|---------|---------|---------|
| Pixiv | `ranking` | `search "关键词"` | `detail` `illusts` |
| Yollomi | - | - | `generate` `video` `edit` |

### 🎙️ 播客/音频平台

| 平台 | 热门命令 | 搜索命令 | 深度抓取 |
|------|---------|---------|---------|
| Apple Podcasts | `top` | `search "关键词"` | `episodes` |
| 小宇宙 | `podcast` | - | `episode` |
| Spotify | - | `search "关键词"` | `play` `queue` |

---

## 触发方式

### 触发词 → 对应操作

| 触发词示例 | 执行命令 |
|-----------|---------|
| "抓热门" / "全平台热门" | 所有平台热门抓取 |
| "小红书热门" / "B站热门" | 单平台热门 |
| "搜AI" / "抓XXX相关内容" | 关键词搜索（所有平台） |
| "Twitter趋势" / "Reddit热门" | 国外平台热门 |
| "抓推特" / "抓Reddit" | 指定国外平台 |
| "知乎热榜" / "微博热搜" | 指定国内平台 |
| "Hacker News热门" / "Product Hunt" | 指定科技平台 |
| "股票XXX" / "基金热门" | 金融平台 |
| "生成汇报" | 汇总已有数据 |

### 默认全平台热门抓取

```bash
# 国内
opencli bilibili hot --limit 10 -f json
opencli xiaohongshu feed --limit 10 -f json
opencli zhihu hot --limit 10 -f json
opencli weibo hot --limit 10 -f json
opencli xueqiu hot-stock --limit 10 -f json
opencli 36kr hot --limit 10 -f json
opencli douban movie-hot --limit 10 -f json

# 国外
opencli twitter trending -f json
opencli reddit hot --limit 10 -f json
opencli hackernews top --limit 10 -f json
opencli youtube search " trending" --limit 10 -f json
opencli producthunt hot --limit 10 -f json
opencli bluesky trending --limit 10 -f json
```

---

## 前置要求

### 1. 安装 opencli
```bash
npm install -g @jackwener/opencli
```

### 2. 安装 Chrome 扩展（必须！）

**步骤：**
1. 下载：`https://github.com/jackwener/opencli/releases` → 下载 `opencli-extension.zip`
2. 解压到任意位置（如 `~/Downloads/opencli-extension/`）
3. 打开 Chrome → `chrome://extensions/`
4. 开启右上角「开发者模式」
5. 点击「加载已解压的扩展程序」
6. 选择解压后的 `extension` 文件夹

### 3. 在 Chrome 中登录目标平台

在 Chrome 浏览器中打开并登录：
- **国内**：bilibili.com、xiaohongshu.com、zhihu.com、weibo.com 等
- **国外**：twitter.com、reddit.com、youtube.com 等

### 4. 验证安装
```bash
opencli doctor
```

---

## 技能执行流程

### 第一步：技能初始化

**输出给用户（发送消息到群）：**
```
🐸 opencli-content-hunter 技能初始化

请按顺序完成以下两个步骤：

Step 1/2：安装 opencli
npm install -g @jackwener/opencli

Step 2/2：安装 Chrome 扩展
1. 下载：https://github.com/jackwener/opencli/releases → opencli-extension.zip
2. 解压后 Chrome → chrome://extensions/ → 开启开发者模式 → 加载已解压的扩展程序

两个步骤都完成后，回复"已完成"，我将验证并继续抓取。 🐸
```

### 第二步：验证安装
```bash
opencli doctor
# 验证 opencli 和 Chrome 扩展状态
```

**如果 Chrome 扩展未连接（Extension: not connected）：**

→ 执行登录引导流程：
```
⚠️ 检测到 Chrome 扩展未连接

请按以下步骤操作：

Step 1：安装 opencli（如果未安装）
npm install -g @jackwener/opencli

Step 2：安装 Chrome 扩展
1. 下载：https://github.com/jackwener/opencli/releases → opencli-extension.zip
2. 解压后 Chrome → chrome://extensions/ → 开启开发者模式 → 加载已解压的扩展程序

两个步骤都完成后，回复"已完成"，我将验证并继续。 🐸
```

**如果扩展已连接：**
→ 直接进入第三步（平台选择）

### 第三步：平台选择

**⚠️ 每次首次执行都会让用户确认平台选择和登录意愿。**

**发送平台列表给用户确认：**

```
🌐 请选择你要抓取的平台：

A. 全部平台（含需要登录的）
   🇨🇳 国内：B站、小红书、知乎、微博、雪球、豆瓣、即刻、36氪、微信公众号、微信读书
   🌏 国外：Twitter、Reddit、YouTube、Instagram、TikTok、LinkedIn
   📰 媒体：BBC、Bloomberg、Google News
   💻 科技：Hacker News、DEV.do、Stack Overflow、Product Hunt、Bluesky
   📚 学术：arxiv、Hugging Face、Wikipedia
   🎮 游戏：Steam
   ⚠️ 以上大部分需要 Chrome 登录

B. 只要不需要登录的（全部可抓平台，共19个）
   📰 新闻媒体：BBC、Bloomberg、Google News、Wikipedia
   💻 科技/开发者：Hacker News、DEV.do、Stack Overflow、arXiv、Hugging Face、Bluesky、V2EX、Lobsters
   🎙️ 播客：Apple Podcasts
   🎮 游戏：Steam
   🛒 电商：豆瓣（图书/电影）、微信读书、什么值得买
   💬 工具：Dictionary
   🌐 其他：新浪财经

C. 自选（告诉我你要哪些，比如"Hacker News + B站 + Twitter"）

📌 之后可以说"调整平台"重新选择
```

### 第四步：登录引导（仅当用户选择了需要登录的平台时）

根据用户选择，检测是否包含需登录平台：
```bash
opencli bilibili hot --limit 1
opencli xiaohongshu feed --limit 1
# ... 测试用户选择的平台
```

**如果用户选择了需要登录的平台，发送引导：**
```
🔐 以下平台需要 Chrome 登录：
- 小红书：https://www.xiaohongshu.com
- B站：https://www.bilibili.com
...（只列用户选择的需要登录的平台）

请在 Chrome 中打开各网址并完成登录。
（登录一次后永久有效）

完成后回复"已登录"，我将验证并继续。
```

**如果用户只选择了公开平台：**
→ 跳过登录引导，直接执行抓取

### 第五步：执行抓取

**⚠️ 重要：如果用户选择B（所有不需要登录的平台），必须抓取全部19个平台，不能只抓部分！**

按用户选择的平台执行抓取：
```bash
# 选项B：抓取全部19个公开平台，每平台 TOP 10
# 新闻媒体
opencli bbc news --limit 10
opencli bloomberg main --limit 10
opencli google news --limit 10
opencli wikipedia trending --limit 10

# 科技/开发者
opencli hackernews top --limit 10
opencli devto top --limit 10
opencli stackoverflow hot --limit 10
opencli arxiv search "AI" --limit 10
opencli hf top --limit 10
opencli bluesky trending --limit 10
opencli v2ex hot --limit 10
opencli lobsters newest --limit 10

# 播客
opencli apple-podcasts top --limit 10

# 游戏
opencli steam top-sellers --limit 10

# 电商/图书
opencli douban movie-hot --limit 10
opencli weread ranking --limit 10
opencli smzdm search "热门" --limit 10

# 工具
opencli dictionary search "AI" --limit 10

# 其他
opencli sinafinance news --limit 10

# 选项C：只抓用户指定的平台
opencli <平台1> <命令> --limit 10
opencli <平台2> <命令> --limit 10
```

### 第六步：生成汇报

汇总所有平台数据，按以下格式输出：
- 用户选择的平台热门 TOP50
- 跨平台热点话题
- 趋势分析
- 推荐深度阅读
- 点评

### 平台调整（后续修改）

**如果用户之后说"调整平台"、"换平台"、"我要加/减XXX"：**
→ 回到第三步，重新让用户确认选择和登录意愿

---

## 平台登录要求速查表

**✅ 实测成功（不需要登录，19个）：**

| 平台 | 热门命令 | 状态 |
|------|---------|------|
| Hacker News | `hackernews top` | ✅ |
| DEV.do | `devto top` | ✅ |
| BBC | `bbc news` | ✅ |
| Google News | `google news` | ✅ |
| arXiv | `arxiv search "关键词"` | ✅ |
| Hugging Face | `hf top` | ✅ |
| Bluesky | `bluesky trending` | ✅ |
| Stack Overflow | `stackoverflow hot` | ✅ |
| Lobsters | `lobsters newest` | ✅ |
| Wikipedia | `wikipedia trending` | ✅ |
| Bloomberg | `bloomberg main` | ✅ |
| Steam | `steam top-sellers` | ✅ |
| V2EX | `v2ex hot` | ✅ |
| Apple Podcasts | `apple-podcasts top` | ✅ |
| 豆瓣电影 | `douban movie-hot` | ✅ |
| 微信读书 | `weread ranking` | ✅ |
| Dictionary | `dictionary search` | ✅ |
| 新浪财经 | `sinafinance news` | ✅ |
| 什么值得买 | `smzdm search` | ✅ |

**❌ 实测失败（不建议使用，6个）：**

| 平台 | 问题 | 原因 |
|------|------|------|
| Product Hunt | 网络错误 | 浏览器连接超时 |
| 新浪博客 | 页面结构变化 | selector h1找不到 |
| Paper Review | 命令不存在 | 只有`review`和`feedback`命令 |
| 小宇宙 | 参数缺失 | 需要提供播客ID |
| Yollomi | 参数缺失 | 需要提供prompt参数 |
| Reuters | 超时 | 每次都超时 |

**⚠️ 需要登录或不稳定：**

| 平台 | 状态 |
|------|------|
| 小红书 | 需要登录，数据少 |
| 知乎 | 需要登录，返回空 |
| Twitter | 需要登录 |
| Reddit | 需要登录，超时 |
| IMDB | 不稳定，有时失败 |

**说明：**
- ✅ 不需要 = 公开可用，直接抓取
- ⚠️ 需要 = 需要在 Chrome 中登录该网站


## 汇报格式

```
📊 内容捕手汇报 - YYYY-MM-DD HH:mm

🔥 全平台热门 TOP50

【小红书】
1. 标题 | 点赞:X 收藏:X
   → 一句话说明内容是什么
2. 标题 | 点赞:X 收藏:X
   → 一句话说明内容是什么
...

【B站】
1. 标题 | 播放:X 弹幕:X
   → 一句话说明内容是什么
2. 标题 | 播放:X 弹幕:X
   → 一句话说明内容是什么
...

【知乎】
1. 标题 | 热度:X
   → 一句话说明内容是什么
...

【微博】
1. 标题 | 转发:X 评论:X
   → 一句话说明内容是什么
...

【Twitter】
1. 标题 | 转发:X 点赞:X
   → 一句话说明内容是什么
...

【Reddit】
1. 标题 | 票数:X 评论:X
   → 一句话说明内容是什么
...

【Hacker News】
1. 标题 | 分数:X 评论:X
   → 一句话说明内容是什么
...

### 默认全平台热门抓取

```bash
# 国内（每个平台取 TOP 50）
opencli bilibili hot --limit 50 -f json
opencli xiaohongshu feed --limit 50 -f json
opencli zhihu hot --limit 50 -f json
opencli weibo hot --limit 50 -f json
opencli xueqiu hot-stock --limit 50 -f json
opencli 36kr hot --limit 50 -f json
opencli douban movie-hot --limit 50 -f json

# 国外（每个平台取 TOP 50）
opencli twitter trending --limit 50 -f json
opencli reddit hot --limit 50 -f json
opencli hackernews top --limit 50 -f json
opencli youtube search " trending" --limit 50 -f json
opencli producthunt hot --limit 50 -f json
opencli bluesky trending --limit 50 -f json
```
- 话题A：在微博/B站/知乎 同，时热门
- 话题B：在 Twitter/Reddit 讨论热度较高

🎯 趋势分析
1. XX话题在多个平台上升
2. XX内容形式表现突出

📖 推荐深度阅读
- 小红书：标题 | URL
- YouTube：标题 | URL
- 知乎：标题 | URL

🐸 点评
基于今日全平台热门内容，整体趋势是...
```

---

## 命令速查

```bash
# 查看所有可用命令
opencli list

# 查看特定平台命令
opencli list bilibili
opencli list xiaohongshu
opencli list twitter

# 测试连接状态
opencli doctor

# 测试单平台
opencli bilibili hot --limit 3 -f table
opencli hackernews top --limit 3 -f table

# 查看命令帮助
opencli <平台> <命令> --help
```

---

## 输出格式

所有命令支持 `-f` 参数：
```bash
-f table   # 表格（默认）
-f json    # JSON（推荐用于程序处理）
-f yaml    # YAML
-f md      # Markdown
-f csv     # CSV
```

---

## 依赖工具

| 工具 | 用途 |
|------|------|
| `opencli` | 主抓取工具 |
| `browser` | 截图、登录引导（如需要） |
| `message` | 汇报发送到群 |

---

## 注意事项

1. **Chrome 扩展必须保持连接** - 每次使用前建议 `opencli doctor` 检查
2. **目标平台需在 Chrome 中登录** - 登录一次后永久有效
3. **公开 API 平台不需要登录** - Hacker News、DEV.to、Wikipedia 等
4. **不确定时用 `opencli <平台> --help`** - 查看完整命令列表
5. **更新 opencli** - `npm install -g @jackwener/opencli@latest`
