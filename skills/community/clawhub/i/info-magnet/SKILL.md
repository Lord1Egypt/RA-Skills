---
name: info-magnet
description: Info Magnet — set up topics you care about and let information come to you. Supports web search, RSS feeds, and URL monitoring. Periodic scans push relevant findings.
tags:
  - information
  - monitoring
  - rss
  - productivity
  - agent
requires:
  bins:
    - python
  env: []
---

# 信息磁铁 / Info Magnet

不是你去找信息，是**信息来找你**。

Don't search for information. Set up magnets that attract it.

## 核心理念

```
传统方式：每天手动搜一遍 → 重复搜同样的东西 → 漏了重要更新
磁铁方式：设好关注点 → 自动定期扫描 → 有新的才推送 → 没有就安静
```

## 命令参考

MAGNET = python <skill_dir>/scripts/infomagnet.py

### 创建磁铁

```bash
# Web 搜索型：定期搜索关键词
$MAGNET add --name "AI 动态" --topics "大模型,AI agent,GPT-5" --sources web --schedule daily

# RSS 订阅型：监控 RSS 源
$MAGNET add --name "Hacker News 热帖" \
  --topics "tech" \
  --sources rss \
  --rss "https://hnrss.org/frontpage" \
  --schedule hourly

# URL 监控型：检测网页更新
$MAGNET add --name "OpenClaw 更新" \
  --topics "openclaw" \
  --sources url \
  --urls "https://github.com/openclaw/openclaw/releases" \
  --schedule daily
```

**参数说明：**
- `--name`：磁铁名称
- `--topics`：关注的关键词（逗号分隔）
- `--sources`：信源类型（web/rss/url，逗号分隔）
- `--schedule`：检查频率（hourly/daily/weekly）
- `--rss`：RSS feed URL
- `--urls`：要监控的网页 URL
- `--notes`：备注

### 查看所有磁铁

```bash
$MAGNET list
```

### 扫描新内容

```bash
# 扫描所有活跃磁铁
$MAGNET scan --all

# 只扫描指定磁铁
$MAGNET scan --id mag_xxx
```

扫描结果会自动保存为摘要文件，已看过的 URL 不会重复出现。

### 查看摘要

```bash
# 查看最近 24 小时的内容
$MAGNET digest

# 查看最近 7 天
$MAGNET digest --since 7d

# 只看某个磁铁
$MAGNET digest --id mag_xxx --since 48h
```

### 管理磁铁

```bash
# 暂停
$MAGNET pause --id mag_xxx

# 恢复
$MAGNET resume --id mag_xxx

# 删除
$MAGNET remove --id mag_xxx

# 标记已读（手动标记某个 URL）
$MAGNET mark-read --url "https://..."
```

### 导入 RSS

```bash
$MAGNET import-rss --url "https://rss.example.com/feed.xml" --name "我的订阅"
```

## Agent 集成工作流

### 定期扫描（Heartbeat 集成）

在 HEARTBEAT.md 中添加：

```markdown
## 信息磁铁扫描
- 运行 `python ~/.openclaw/skills/info-magnet/scripts/infomagnet.py scan --all`
- 如果有新发现，发送摘要给用户
- 如果没有，跳过
```

### 扫描 + 搜索的完整流程

```
1. $MAGNET scan --all
   → 生成待搜索的 topic 列表（web-pending 条目）

2. Agent 对每个 web-pending 执行 web_search
   → 过滤掉已见过的 URL
   → 有新的就记录

3. $MAGNET digest --since 24h
   → 汇总所有新发现

4. 推送给用户：
   "📬 今日信息摘要：发现 3 条你可能感兴趣的内容..."
```

### 智能过滤

Agent 在执行搜索后，不是把所有结果都推给用户，而是：

1. **去重**：跳过已见过的 URL
2. **相关性判断**：根据用户的关注点筛选
3. **摘要**：每条内容用 1-2 句话概括
4. **分类**：按磁铁分组展示

## 示例配置

```bash
# 技术资讯
$MAGNET add --name "技术前沿" \
  --topics "rust,webassembly,ai agent,llm" \
  --sources web,rss \
  --rss "https://hnrss.org/best,https://lobste.rs/rss" \
  --schedule daily

# 项目监控
$MAGNET add --name "我的依赖库更新" \
  --topics "playwright update,flask release" \
  --sources web \
  --schedule weekly

# 行业动态
$MAGNET add --name "AI 产品动态" \
  --topics "new ai product,chatgpt plugin,claude api" \
  --sources web \
  --schedule daily

# 中文社区
$MAGNET add --name "掘金热帖" \
  --topics "前端" \
  --sources rss \
  --rss "https://rsshub.app/juejin/category/frontend" \
  --schedule daily
```

## 数据存储

```
~/.openclaw/memory/
├── magnets.json           # 磁铁配置
├── magnet-seen.jsonl      # 已见过的 URL（去重用）
└── magnet-digests/        # 历史摘要
    ├── mag_xxx_1775095389.json
    └── ...
```

## 设计哲学

- **推 > 拉**：信息主动推送，而不是你去找
- **安静**：没有新内容就不打扰
- **去重**：同一内容只出现一次
- **可组合**：支持 web 搜索 + RSS + URL 监控混搭
- **零依赖**：纯 Python 标准库

## 局限性

- Web 搜索依赖 Agent 的 web_search 工具（需要在 Agent 环境中执行）
- RSS 解析不支持所有 feed 格式（兼容 RSS 2.0 和 Atom）
- URL 监控是简单 hash 比较，不支持动态页面
- 没有内置推送渠道，需要 Agent 通过消息通道转发
