---
name: github-stars-tracker
version: 1.0.0
description: GitHub 仓库 Stars 变化监控与通知。追踪指定仓库的 star 增长、fork 变化，发现新趋势。适合开发者关注项目动态。
author: 你的名字
triggers:
  - "GitHub stars"
  - "追踪仓库"
  - "项目动态"
  - "star 变化"
---

# GitHub Stars Tracker 🌟

监控 GitHub 仓库的 stars、forks、watchers 变化，追踪你关心的项目动态。

## 功能

- 📊 追踪指定仓库的 star 数量变化
- 📈 记录历史数据，生成变化趋势
- 🔔 当 star 快速增长时通知
- 📝 支持多仓库同时监控

## 使用方法

### 添加要追踪的仓库

```bash
# 使用 owner/repo 格式
python3 scripts/tracker.py add owner/repo
```

### 查看仓库状态

```bash
python3 scripts/tracker.py status owner/repo
```

### 列出所有追踪的仓库

```bash
python3 scripts/tracker.py list
```

### 检查变化

```bash
python3 scripts/tracker.py check
```

## 配置

首次使用需要设置 GitHub Token（避免 API 限流）：

```bash
export GITHUB_TOKEN=your_token_here
```

获取 Token：https://github.com/settings/tokens

## 示例

```bash
# 追踪一些热门 AI 项目
python3 scripts/tracker.py add openai/openai-python
python3 scripts/tracker.py add anthropics/claude-code
python3 scripts/tracker.py add

# 查看状态
python3 scripts/tracker.py status openai/openai-python
```
