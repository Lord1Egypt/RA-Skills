---
name: opencli
description: Universal CLI Hub for browser automation and website command-line access. Use when: (1) user wants to interact with websites via CLI (Bilibili, Zhihu, Twitter, Reddit, etc.); (2) need browser automation (click, type, screenshot, scrape); (3) user wants to control Chrome programmatically; (4) calling any built-in opencli commands. Triggers on requests like "帮我查一下B站热门视频", "操作一下Twitter", "抓取某网站内容", "用opencli", or any reference to opencli commands.
---

# OpenCLI — Universal CLI Hub & Browser Automation

opencli 已安装于 `/Users/c/.openclaw/opencli`，可通过 `opencli` 命令直接调用。

## 快速检查

```bash
opencli --version      # 验证安装
opencli list           # 列出所有可用命令
opencli doctor         # 检查扩展 + daemon 连接状态
```

## 核心命令分类

### 公开 API（无需登录）
| 站点 | 示例命令 |
|------|---------|
| 新闻 | `opencli bbc news`, `opencli 36kr news` |
| 搜索 | `opencli bilibili search "关键词"`, `opencli hackernews search "关键词"` |
| 榜单 | `opencli bilibili hot`, `opencli bilibili ranking` |
| 论文 | `opencli arxiv search "关键词"`, `opencli arxiv paper <id>` |
| GitHub | `opencli github trending` |

### 需要登录的命令（cookie/intercept 模式）
需要 Chrome 已登录目标网站。常用：
- `opencli bilibili favorite` — 我的收藏夹
- `opencli bilibili history` — 观看历史
- `opencli bilibili feed` — 关注动态
- `opencli twitter timeline` — Twitter 时间线
- `opencli reddit frontpage` — Reddit 首页

### 浏览器自动化（operate 命令）
```bash
opencli operate open <url>           # 打开网页
opencli operate state                # 查看页面元素（带索引）
opencli operate click <N>           # 点击元素
opencli operate type <N> "文本"      # 输入文本
opencli operate screenshot          # 截图
opencli operate get value <N>        # 获取输入框值
opencli operate scroll <N>           # 滚动
opencli operate back                 # 返回
opencli operate wait time <秒>       # 等待
```

### 外部 CLI Hub（自动安装）
```bash
opencli gh pr list --limit 5        # GitHub CLI
opencli docker ps                    # Docker
opencli obsidian search "关键词"     # Obsidian
```

## 执行规则

1. **公开命令直接执行**：`opencli <site> <command> [args]`
2. **需要登录的命令先检查**：确保 Chrome 已登录目标网站
3. **operate 命令链式调用**：用 `&&` 合并多个操作减少往返
4. **自动安装**：如果外部 CLI 不存在，opencli 会自动尝试安装

## 输出格式

opencli 输出为结构化文本，直接可读。JSON 格式可通过 `opencli ... --json` 获取（部分命令支持）。

## 常用命令参考

```bash
# B站
opencli bilibili hot --limit 5
opencli bilibili search "关键词" --limit 10
opencli bilibili user-videos <uid>

# Twitter/X
opencli twitter trending
opencli twitter search "关键词" --limit 10

# Reddit
opencli reddit hot
opencli reddit frontpage

# GitHub
opencli github trending

# 新闻
opencli bbc news
opencli 36kr news
opencli hackernews top --limit 5

# 论文
opencli arxiv search "LLM" --limit 5
```
