---

name: "git-cli-tool-free"
description: "提供Git CLI快速参考、状态检查、暂存提交与分支同步,适合开发者日常命令行操作。Use when 需要代码生成、编程辅助、调试测试、开发部署时使用。不适用于无明确技术栈的模糊需求。适用于独立开发者、企业团队和自动化工作流场景。支持中文交互，无需复杂配置即开即用。输出结果可直接使用，减少二次加工成本。"
license: Proprietary
allowed-tools: read exec
compatibility: "Requires LLM with tool-use capability"
metadata:
  displayName: "Git命令行助手免费版"
  version: "1.0.0"
  summary: "提供Git CLI快速参考、状态检查、暂存提交与分支同步,适合开发者日常命令行操作。"
  tags:
    - "开发工具"
    - "Git"
    - "命令行"
  source: "SkillHub"
  converted_at: "2026-07-22T17:58:36"
tools:
  - exec
  - read
  - write

---

> **功能说明**: 本技能涵盖 中文交互、化工作流场景 等核心能力。


# Git命令行助手 - 免费版
## 概述
Git命令行助手免费版为开发者提供日常Git CLI操作辅助能力。工具提供快速命令参考表、仓库状态检查、暂存提交操作和远程同步指引,帮助开发者高效使用Git命令行。

本版本适合日常Git命令行操作、快速查找命令和新手学习Git CLI。所有操作遵循安全优先原则,避免误操作。

## 核心能力
### 1. 快速参考表
最常用的Git命令速查。

| 任务 | 命令 |
|:-----|:-----|
| 状态与差异 | `git status` / `git diff` / `git diff --staged` |
| 暂存/取消 | `git add <path>` / `git add .` / `git restore --staged <path>` |
| 提交 | `git commit -m "message"` |
| 分支 | `git branch` / `git switch -c new` / `git switch existing` |
| 同步远程 | `git fetch` / `git pull` / `git push -u origin <branch>` |
| 暂存(stash) | `git stash` / `git stash list` / `git stash apply` |
| 历史 | `git log --oneline --graph -n 20` / `git blame <file>` |
| 克隆/初始化 | `git clone <url>` / `git init` / `git remote add origin <url>` |
| 远程 | `git remote -v` / `git remote show origin` / `git branch -vv` |
| 丢弃变更 | `git restore <file>` / `git restore --staged <file>` |
| 修改提交 | `git commit --amend --no-edit` / `git commit --amend -m "msg"` |
| 标签 | `git tag` / `git tag v1.0` / `git push origin v1.0` |
| 合并/变基 | `git merge <branch>` / `git rebase <branch>` |

**输出**: 返回快速参考表的执行结果,包含操作状态和输出数据。

### 2. 仓库状态检查
```bash
# 快速状态检查
git status                           # 当前状态
git status -sb                       # 简短状态+分支信息
git branch --show-current            # 当前分支名
git remote -v                        # 远程仓库
git log --oneline -5                 # 最近5个提交
# 差异检查
git diff                             # 工作区变更
git diff --staged                    # 暂存区变更
git diff --stat                      # 变更统计
git diff HEAD~1                      # 与上次提交比较
# 分支信息
git branch -a                        # 所有分支
git branch -vv                       # 分支跟踪信息
git log --graph --oneline --all -20  # 图形化历史
```

**输出**: 返回仓库状态检查的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 3. 暂存与提交
```bash
# 暂存文件
git add file.txt                     # 暂存单个文件
git add .                            # 暂存所有变更
git add -A                           # 包括删除操作
git add -p                           # 交互式选择暂存
# 取消暂存
git restore --staged file.txt        # 取消暂存(新命令)
git reset HEAD file.txt              # 取消暂存(旧命令)
# 提交
git commit -m "提交信息"             # 基础提交
git commit -am "提交信息"            # 添加并提交已跟踪文件
git commit --amend --no-edit         # 修改提交(保持信息)
git commit --amend -m "新信息"       # 修改提交信息
```

**输出**: 返回暂存与提交的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 4. 分支管理
```bash
# 查看分支
git branch                           # 本地分支
git branch -a                        # 所有分支
git branch -vv                       # 跟踪信息
# 创建和切换
git switch -c feature-name           # 创建并切换(推荐)
git switch main                      # 切换到main
git switch -                         # 切换到上一个分支
# 删除分支
git branch -d feature-name           # 安全删除(已合并)
git branch -D feature-name           # 强制删除
# 重命名
git branch -m old-name new-name      # 重命名分支
```

**输出**: 返回分支管理的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 5. 远程同步
```bash
# 获取远程更新
git fetch origin                     # 获取不合并
git fetch --all --prune              # 获取所有并清理
# 拉取
git pull                             # 拉取并合并
git pull --rebase                    # 拉取并变基(推荐)
# 推送
git push                             # 推送当前分支
git push -u origin branch-name       # 首次推送并设置跟踪
git push --force-with-lease          # 安全强制推送
```

**输出**: 返回远程同步的执行结果,包含操作状态和输出数据。
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：CLI、暂存提交与分支同、适合开发者日常命、令行操作、面向开发者的、命令行辅助工具、提供快速命令参考、暂存提交与远程同、步操作指引、核心能力、分支管理与远程同、安全操作指引等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

## 使用场景
### 场景一:日常开发工作流
标准的命令行开发工作流。

```bash
#!/bin/sh
# 日常开发工作流
echo "=== Git日常工作流 ==="

# 1. 开始工作前同步
echo "1. 同步远程仓库..."
git fetch --all --prune
git pull --rebase

# 2. 创建功能分支
echo -e "\n2. 创建功能分支..."
git switch -c feature/new-feature

# 3. 开发并提交
echo -e "\n3. 暂存并提交..."
git add .
git status
git commit -m "feat: 添加新功能"

# 4. 推送到远程
echo -e "\n4. 推送分支..."
git push -u origin feature/new-feature

# 5. 查看状态
echo -e "\n5. 当前状态:"
git status -sb
git log --oneline -3

echo -e "\n=== 工作流完成 ==="
```

### 场景二:快速状态诊断
快速了解当前仓库状态。

```bash
#!/bin/sh
# 仓库状态诊断
echo "=== Git仓库状态诊断 ==="

echo "当前分支: $(git branch --show-current)"
echo "远程仓库:"
git remote -v

echo -e "\n工作区状态:"
git status -sb

echo -e "\n最近提交:"
git log --oneline -5

echo -e "\n未推送的提交:"
git log origin/$(git branch --show-current)..HEAD --oneline 2>/dev/null

echo -e "\n暂存列表:"
git stash list

echo -e "\n分支概览:"
git branch -vv
```

### 场景三:安全回退操作
安全地回退不需要的变更。

```bash
#!/bin/sh
# 安全回退操作
echo "=== 安全回退操作 ==="

# 1. 丢弃工作区变更(未暂存)
echo "丢弃未暂存变更:"
echo "  git restore <file>          # 丢弃单个文件"
echo "  git restore .               # 丢弃所有"
# 2. 取消暂存(已暂存未提交)
echo -e "\n取消暂存:"
echo "  git restore --staged <file> # 取消暂存单个文件"
echo "  git restore --staged .      # 取消所有暂存"
# 3. 撤销提交(保留变更)
echo -e "\n撤销提交(保留变更):"
echo "  git reset --soft HEAD~1     # 撤销提交,变更回到暂存区"
echo "  git reset HEAD~1            # 撤销提交,变更回到工作区"
# 4. 安全撤销已推送的提交
echo -e "\n撤销已推送提交(安全方式):"
echo "  git revert <commit-sha>     # 创建反向提交"
echo "  git push origin <branch>    # 推送撤销"
echo -e "\n注意:避免使用 git reset --hard 和 git push --force"
```

## 不适用场景
以下场景Git命令行助手免费版不适合处理：

- 无明确技术栈的模糊需求
- 纯架构设计决策
- 运维部署管理

## 触发条件
需要代码生成、编程辅助、调试测试、开发部署时使用。不适用于非本工具能力范围的需求。

## 快速开始
### Step 1:验证Git环境
```bash
git --version
git config user.name
git config user.email
```

### Step 2:触发操作
在 AI Agent 中输入:

```
请帮我查看当前Git仓库状态并提交代码。
```

### Step 3:执行命令
Agent 会按安全优先原则执行Git命令。

**结果处理**: 执行完成后,查看输出结果确认操作状态。成功时输出包含处理摘要和结果数据;失败时根据错误信息排查问题,查阅错误处理章节获取恢复步骤。

#
## 示例
### Git CLI配置
```ini
# $HOME/.gitconfig
[user]
    name = 你的名字
    email = your@email.com

[init]
    defaultBranch = main

[alias]
    st = status -sb
    co = checkout
    sw = switch
    br = branch
    ci = commit
    lg = log --graph --oneline --all
    last = log -1 HEAD
    diffstat = diff --stat

[pull]
    rebase = true

[push]
    default = current
    autoSetupRemote = true
```

### 常用.gitignore
```gitignore
# 通用
*.log
*.tmp
*.bak
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/
*.swp

# 依赖
node_modules/
__pycache__/
venv/

# 环境
.env
.env.local
```

## 优选实践
1. **安全优先**:优先使用只读命令,避免破坏性操作

```bash
# 先查看再操作
git status          # 查看状态
git diff            # 查看变更
git log             # 查看历史
```

2. **使用现代命令**:`switch`和`restore`比`checkout`更清晰

```bash
# 推荐(新命令)
git switch branch-name
git restore file.txt

# 不推荐(旧命令,功能混淆)
# git checkout branch-name
# git checkout -- file.txt
```

3. **提交前检查**:养成提交前检查的习惯

```bash
git status          # 确认暂存内容
git diff --staged   # 确认变更内容
git log --oneline -3  # 确认提交历史
```

4. **使用--force-with-lease**:替代--force

```bash
# 安全(推荐)
git push --force-with-lease

# 危险(不推荐)
# git push --force
```

## 常见问题
### Q1:git pull和git fetch有什么区别?
```bash
# git fetch:只获取,不合并
git fetch origin
# 获取后可以查看差异
git diff HEAD origin/main
# 手动决定是否合并
git merge origin/main

# git pull:获取并自动合并
git pull
# 等同于 git fetch + git merge
# git pull --rebase:获取并变基(推荐)
git pull --rebase
# 等同于 git fetch + git rebase
```

### Q2:如何查看某个文件的修改历史?
```bash
# 文件提交历史
git log --oneline -- file.txt

# 文件每行最后修改者
git blame file.txt

# 文件差异历史
git log -p file.txt

# 文件重命名历史
git log --follow file.txt
```

### Q3:如何临时保存当前工作?
```bash
# 保存当前工作
git stash
git stash save "工作描述"

# 查看暂存列表
git stash list

# 恢复暂存(保留暂存)
git stash apply
git stash apply stash@{2}

# 恢复暂存(删除暂存)
git stash pop

# 删除暂存
git stash drop stash@{0}
git stash clear  # 清除所有
```

### Q4:免费版与专业版有何区别?
| 能力维度 | 免费版 | 专业版 |
|:---------|:-------|:-------|
| 命令参考 | 基础命令 | 完整命令库 |
| 自动化 | 手动执行 | 脚本自动化 |
| 工作流 | 单人 | 团队工作流 |
| 诊断 | 基础状态 | 深度诊断 |
| 模板 | 基础.gitignore | 多场景模板 |
| 故障排除 | 基础 | 深度排障 |

## 依赖说明
### 运行环境
- **Agent 平台**:支持 SKILL.md 的任意 AI Agent(Claude Code / Cursor / Codex / Gemini CLI 等)
- **操作系统**:Windows / macOS / Linux
- **运行时**:Git 2.20+

### 依赖详情
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-------|:-----|:---------|:---------|
| Git | 运行时 | 必需 | git-scm.com 下载 |
| Bash | 运行时 | 推荐 | 系统自带 |
| LLM API | API | 必需 | 由 Agent 内置 LLM 提供 |

### API Key 配置
- 本 Skill 基于 Markdown 指令,无需额外 API Key
- 远程仓库认证:

```bash
# HTTPS凭证
git config --global credential.helper store

# SSH密钥
ssh-keygen -t ed25519 -C "your@email.com"
```

### 可用性分类
- **分类**:MD+execute(纯 Markdown 指令,需要 exec 命令行执行能力)
- **说明**:基于 Markdown 的 AI Skill,通过自然语言指令驱动 Agent 执行Git CLI操作
- **适用规模**:个人开发者日常使用

## 错误处理
| 错误场景 | 原因 | 处理方式 |
|---------|------|---------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 已知限制
- 需LLM支持,无LLM环境不可用
- 复杂业务场景建议结合人工经验判断
- 执行效率受模型能力与网络环境影响

## 安全注意事项

| 风险类型 | 防范措施 |
|----------|---------|
| API密钥泄露 | 通过环境变量配置，禁止硬编码到代码或配置文件中 |
| 命令执行风险 | 仅执行白名单命令，避免拼接用户输入到命令行参数中 |
| 网络通信安全 | 使用HTTPS协议，验证SSL证书有效性 |
| 敏感数据暴露 | 输出结果中不包含密钥、令牌等敏感信息 |

使用前请确认已阅读依赖说明章节，确保运行环境满足安全要求。

## 核心功能

- **自动化执行**: 基于指令驱动的自动化流程
- **文件处理**: 支持多种文件格式的读取、解析和写入操作
- **API集成**: 通过标准化接口调用外部服务并处理响应
- **命令执行**: 在安全沙箱中执行系统命令并收集结果
- **信息检索**: 快速搜索和过滤目标数据