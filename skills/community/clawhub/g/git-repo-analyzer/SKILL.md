---
name: git-repo-analyzer
description: |
  智能分析 Git 仓库或普通链接，自动识别内容类型并执行相应处理流程。
  支持四种类型：1) OpenClaw Skills 项目（风险检测与收藏）2) 论文/文档项目（加入 dashifu——wiki 待处理队列）3) 功能项目（评估 OpenClaw 学习可行性）4) 普通网页/文章（加入 dashifu——wiki 待处理队列）。
  当用户提供任何 URL（Git 地址或普通链接）、要求分析链接、处理项目、收录文章、保存网页时触发此 skill。
---

# Git Repo Analyzer

## Overview

本 skill 用于自动识别用户提供的 URL 类型，并根据内容分类执行后处理：

- **Git 仓库** → 检测子类型（Skill / 论文 / 功能项目）→ 执行安装/队列/评估
- **论文/文档项目（Git 仓库）** → 不实时处理，将链接记录到 `~/.openclaw/workspace/memory/kb-queue.json` 异步队列
- **功能项目** → 代码结构分析与 OpenClaw 封装可行性评估
- **直链文件** → 不下载，将链接记录到 `~/.openclaw/workspace/memory/kb-queue.json` 异步队列
- **普通网页** → 不提取，将链接记录到 `~/.openclaw/workspace/memory/kb-queue.json` 异步队列

不适合的场景：需要登录的私有页面、纯本地文件路径。

## Workflow Decision Tree

```
用户输入 URL
    │
    ▼
detect_url_type.py
    │
    ├─ git-repo ──► analyze_git_repo.py
    │                     │
    │           skill ──► analyze_skill_security.py
    │                     │    │ pass/warn ──► install_skill.py
    │                     │    │ fail ──► 阻止安装并清理
    │                     │
    │           paper ──► process_paper_repo.py (queue)
    │                     │    └──► append to ~/.openclaw/workspace/memory/kb-queue.json
    │                     │
    │        function ──► evaluate_function.py
    │
    ├─ direct-file ──► process_direct_file.py (queue)
    │                     └──► append to ~/.openclaw/workspace/memory/kb-queue.json
    │
    └─ webpage ──► process_webpage.py (queue)
                         └──► append to ~/.openclaw/workspace/memory/kb-queue.json
```

## Scripts

### detect_url_type.py

输入 URL，输出 JSON 类型分析结果。

```bash
python3 scripts/detect_url_type.py "https://github.com/user/repo"
# {"url": "...", "type": "git-repo", "domain": "github.com"}
```

### analyze_git_repo.py

输入 Git URL，通过 API 或文件列表判断子类型（skill / paper / function / unknown）。

```bash
python3 scripts/analyze_git_repo.py "https://github.com/user/repo"
```

依赖环境变量：`GITHUB_TOKEN`、`GITLAB_TOKEN`（可选，用于提升 API 限额）。

### analyze_skill_security.py

浅克隆仓库到 staging，读取 `SKILL.md` 并扫描危险指令，返回安全评级（safe / caution / dangerous）。

```bash
python3 scripts/analyze_skill_security.py "https://github.com/user/repo" "repo_name"
```

若评级为 `dangerous`，脚本会自动清理 staging 目录。

### install_skill.py

将 staging 中的 Skill 安装到 `~/.openclaw/skills/installed/`。

```bash
python3 scripts/install_skill.py /path/to/staging "repo_name" "https://github.com/user/repo"
```

### process_paper_repo.py

识别为论文/文档仓库后，**不克隆、不分析内容**，仅将链接以结构化 JSON 记录到 `~/.openclaw/workspace/memory/kb-queue.json`，交给 `kb-archive-process` 每日自动处理。

```bash
python3 scripts/process_paper_repo.py "https://github.com/user/papers" "papers"
```

### evaluate_function.py

克隆功能项目仓库，统计语言分布、代码行数、是否具备 CLI/测试，评估封装为 OpenClaw Skill 的可行性评分与建议。

```bash
python3 scripts/evaluate_function.py "https://github.com/user/tool" "tool"
```

### process_direct_file.py

识别为直链文件后，**不下载**，仅将链接以结构化 JSON 记录到 `~/.openclaw/workspace/memory/kb-queue.json`，交给 `kb-archive-process` 每日自动处理。

```bash
python3 scripts/process_direct_file.py "https://example.com/paper.pdf" "pdf"
```

### process_webpage.py

识别为普通网页后，默认**不提取内容**，仅将链接以结构化 JSON 记录到 `~/.openclaw/workspace/memory/kb-queue.json`，交给 `kb-archive-process` 每日自动处理。

**特殊平台**：若 URL 为 `zhuanlan.zhihu.com` 专栏文章，会优先调用 `zhihu-article-fetcher` skill（Playwright 浏览器自动化）尝试抓取正文；成功后直接保存为 `.md` 到 `memory/` 目录。抓取失败则 fallback 回队列模式。

```bash
python3 scripts/process_webpage.py "https://example.com/blog" "example.com"
```

## Directory Conventions

Skill 中间目录：

```
~/.openclaw/skills/
├── staging/           # 临时克隆目录
└── installed/         # 已安装 Skills
```

异步队列文件：

```
~/.openclaw/workspace/memory/kb-queue.json   # 论文/文档/网页/文件链接的统一待处理队列（JSON 格式）
```

## Handling Unknown Git Repo Subtypes

当 `analyze_git_repo.py` 返回 `subtype: unknown` 时：

1. 告知用户检测到的前 10 个文件列表
2. 让用户选择：`skill` / `paper` / `function`
3. 根据选择执行对应脚本（paper 默认走 queue）
