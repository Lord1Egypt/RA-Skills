---
name: opencli-agent
description: 当用户希望通过命令行自动化与网站或在线服务交互时，应使用本技能。它支持在 Twitter/X 上发帖、浏览 Reddit、获取 B站热门、下载小红书内容等 70+ 个平台的操作——全部通过 opencli 工具完成。触发场景包括社交媒体操作（发帖、点赞、关注、搜索）、内容获取（热门、时间线、动态流）、下载（视频、图片、文章）以及 opencli 支持的任何网络服务自动化。
---

# OpenCLI Agent

## 概述

本技能将自然语言指令转换为 `opencli` 命令，可自动与 70+ 个网站和服务（Twitter/X、Reddit、B站、小红书、YouTube 等）进行交互。OpenCLI 复用 Chrome 浏览器的登录会话，无需暴露密码或 API 密钥。

## 环境检查

在执行任何 opencli 命令之前，先运行环境检查脚本确认环境就绪：

```bash
bash {SKILL_DIR}/scripts/check_setup.sh
```

如果脚本报告问题，引导用户完成以下安装步骤：

1. **安装 Node.js** (>= 20.0.0): `brew install node` 或访问 https://nodejs.org
2. **安装 OpenCLI**: `npm install -g @jackwener/opencli`
3. **安装浏览器扩展**:
   - 从 https://github.com/jackwener/opencli/releases 下载 `opencli-extension.zip`
   - 打开 Chrome → `chrome://extensions` → 开启"开发者模式"
   - 点击"加载已解压的扩展程序" → 选择解压后的文件夹
4. **登录目标网站**：在 Chrome 中登录目标网站（例如：发推前先在 Chrome 中登录 twitter.com）
5. **验证**：运行 `opencli doctor` 确认扩展和守护进程连接正常

## 命令执行流程

收到用户指令后，按以下流程执行：

### 第一步：解析意图

从用户请求中识别三个要素：

- **平台** — 哪个服务（twitter, bilibili, reddit, xiaohongshu 等）
- **动作** — 要做什么（post, search, like, follow, download, trending 等）
- **参数** — 内容、数量限制、输出路径、格式等

### 第二步：映射为 OpenCLI 命令

使用以下格式构造命令：

```
opencli <platform> <action> [arguments] [--options]
```

参考 `{SKILL_DIR}/references/command_reference.md` 获取完整命令目录。如果不确定某个平台支持的命令，运行：

```bash
opencli <platform> --help
```

或列出所有可用命令：

```bash
opencli list
```

### 第三步：执行并反馈

通过终端执行命令，然后：

- 解析输出，以易读格式呈现结果
- 如果命令失败，检查错误信息并建议修复方法（例如"请先在 Chrome 中登录 Twitter"）
- 对于数据检索命令，需要进一步处理时使用 `-f json` 获取结构化输出

## 通用全局选项

| 选项 | 缩写 | 描述 |
|--------|-------|-------------|
| `--format <type>` | `-f` | 输出格式: `table` (默认), `json`, `yaml`, `md`, `csv` |
| `--limit <n>` | | 限制结果数量 |
| `-v` | | 详细/调试模式 |

## 平台命令速查

### 社交媒体 — 发帖与互动

**Twitter/X:**
```bash
# 发布推文
opencli twitter post "Hello World"

# 回复特定推文
opencli twitter reply <tweet_id> "reply content"

# 点赞推文
opencli twitter like <tweet_id>

# 关注用户
opencli twitter follow <username>

# 取消关注
opencli twitter unfollow <username>

# 搜索推文
opencli twitter search "keyword" --limit 10

# 获取时间线
opencli twitter timeline --limit 20

# 获取热门话题
opencli twitter trending

# 获取用户资料
opencli twitter profile <username>

# 拉黑 / 解除拉黑
opencli twitter block <username>
opencli twitter unblock <username>

# 收藏
opencli twitter bookmark <tweet_id>
opencli twitter unbookmark <tweet_id>

# 删除推文
opencli twitter delete <tweet_id>

# 下载媒体
opencli twitter download <tweet_id> --output ./twitter
```

**Reddit:**
```bash
opencli reddit hot --limit 10                          # 获取热门帖子
opencli reddit search "keyword" --limit 10             # 搜索帖子
opencli reddit post <subreddit> "title" "body"         # 发帖
opencli reddit comment <post_id> "comment content"     # 评论
```

**Facebook:**
```bash
opencli facebook feed --limit 10     # 获取动态流
opencli facebook post "content"      # 发布动态
```

**Instagram:**
```bash
opencli instagram feed --limit 10        # 获取动态
opencli instagram profile <username>     # 查看用户资料
```

**LinkedIn:**
```bash
opencli linkedin feed --limit 10        # 获取动态
opencli linkedin profile <username>     # 查看用户资料
```

**Bluesky:**
```bash
opencli bluesky feed --limit 10     # 获取动态
opencli bluesky post "content"      # 发布帖子
```

### 内容平台 — 中文

**Bilibili (B站):**
```bash
opencli bilibili hot --limit 10                            # 获取热门视频
opencli bilibili search "keyword" --limit 10               # 搜索视频
opencli bilibili download <BV_ID> --output ./bilibili      # 下载视频（需 yt-dlp）
```

**Xiaohongshu (小红书):**
```bash
opencli xiaohongshu hot --limit 10                             # 获取热门笔记
opencli xiaohongshu search "keyword" --limit 10                # 搜索笔记
opencli xiaohongshu download <note_id> --output ./xhs          # 下载笔记（图片/视频）
```

**Zhihu (知乎):**
```bash
opencli zhihu hot --limit 10                   # 获取热门问题
opencli zhihu search "keyword" --limit 10      # 搜索问答
```

**Weibo (微博):**
```bash
opencli weibo hot --limit 10                   # 获取热搜
opencli weibo search "keyword" --limit 10      # 搜索微博
```

**Douyin (抖音):**
```bash
opencli douyin hot --limit 10                  # 获取热门视频
opencli douyin search "keyword" --limit 10     # 搜索视频
```

### 新闻与科技

**HackerNews:**
```bash
opencli hackernews top --limit 10      # 获取热门文章
opencli hackernews new --limit 10      # 获取最新文章
```

**Product Hunt:**
```bash
opencli producthunt top --limit 10     # 获取热门产品
```

### 桌面应用控制

```bash
opencli cursor chat "message"          # 在 Cursor IDE 中发送消息
opencli chatgpt send "message"         # 向 ChatGPT 桌面版发送消息
opencli notion search "keyword"        # 在 Notion 中搜索
```

### 外部 CLI 集线器

OpenCLI 可以代理并自动安装外部 CLI 工具：

```bash
# 如果 gh 未安装，会自动安装后再执行命令
opencli gh pr list --limit 5
opencli docker ps
```

## 错误处理

| 错误 | 原因 | 解决方案 |
|-------|-------|----------|
| `Extension not connected` | Chrome 扩展未加载或 Chrome 未运行 | 确保 Chrome 已打开且扩展已启用 |
| `Unauthorized` / 空数据 | 未登录目标网站 | 在 Chrome 中登录该网站 |
| `Command not found` | opencli 未安装或不在 PATH 中 | 运行 `npm install -g @jackwener/opencli` |
| `Node version error` | Node.js 版本过低 (< 20.0.0) | 升级 Node.js 到 20.0.0 以上 |
| `Timeout` | 页面加载过慢或站点被屏蔽 | 检查网络连接；使用 `-v` 查看调试信息 |

## 重要说明

- 执行写操作（发帖、点赞、关注等）前，始终确保用户已在 Chrome 中登录目标网站
- 对于公开数据的只读操作（如 `hackernews top`），无需登录
- 视频下载可能需要安装 yt-dlp：`brew install yt-dlp`
- 需要程序化处理输出时使用 `-f json`
- 当用户请求中平台不明确时，请求用户澄清
- 发现新命令或未文档化命令，运行 `opencli list` 或 `opencli <platform> --help`
