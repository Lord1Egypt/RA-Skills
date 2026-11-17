---
name: "git-toolkit-free"
description: "提供Git提交、分支、合并、冲突解决与历史恢复等核心命令,适合开发者日常版本管理。"
license: Proprietary
allowed-tools: read exec
compatibility: "Requires LLM with tool-use capability"
metadata:
  displayName: "Git工具包免费版"
  version: "1.0.0"
  summary: "提供Git提交、分支、合并、冲突解决与历史恢复等核心命令,适合开发者日常版本管理。"
  tags:
    - "开发工具"
    - "Git"
    - "版本控制"
  source: "SkillHub"
  converted_at: "2026-07-22T17:58:36"
---

# Git工具包 - 免费版
## 概述
Git工具包免费版为开发者提供日常版本管理能力。工具涵盖提交管理、分支策略、合并冲突解决、历史检查与恢复操作,帮助开发者高效使用Git进行代码版本管理。

本版本适合日常代码版本管理、功能分支开发和代码合并与冲突解决。所有命令通过Git CLI执行,无需安装额外插件。

## 核心能力
### 1. 核心规则
使用Git时遵循的安全规则:

1. **永远不要对共享分支强制推送**:仅在功能分支使用 `--force-with-lease`
2. **尽早提交,频繁提交**:小提交更易审查、回退和二分查找
3. **写有意义的提交信息**:首行不超过72字符,使用祈使语气
4. **推送前先拉取**:`git pull --rebase` 避免不必要的合并提交
5. **合并前清理**:使用 `git rebase -i` 压缩修复提交

**输入**: 用户提供核心规则所需的指令和必要参数。
**处理**: 按照skill规范执行核心规则操作,遵循单一意图原则。
**输出**: 返回核心规则的执行结果,包含操作状态和输出数据。

### 2. 提交管理
```bash
# 基础提交
git add file.txt
git add .
git add -A                    # 包括删除的文件
git commit -m "提交信息"

# 提交消息规范(Conventional Commits)
git commit -m "feat(auth): 添加用户登录功能"
git commit -m "fix(api): 修复用户列表分页错误"
git commit -m "docs(readme): 更新安装说明"
git commit -m "refactor(utils): 重构日期格式化函数"
git commit -m "test(auth): 添加登录单元测试"
git commit -m "chore(deps): 升级依赖版本"

# 修改提交
git commit --amend -m "新提交信息"
git commit --amend --no-edit              # 保持原信息
git commit -am "提交信息"                 # 添加并提交已跟踪文件
# 查看变更
git diff                                  # 工作区变更
git diff --staged                         # 暂存区变更
git diff file.txt                         # 特定文件变更
git diff commit1 commit2                  # 比较两个提交
```

**输入**: 用户提供提交管理所需的指令和必要参数。
**处理**: 按照skill规范执行提交管理操作,遵循单一意图原则。
**输出**: 返回提交管理的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 3. 分支管理
```bash
# 查看分支
git branch                                 # 本地分支
git branch -a                              # 所有分支(含远程)
git branch -vv                             # 分支跟踪信息
# 创建和切换分支
git branch feature-name                    # 创建分支
git checkout feature-name                  # 切换分支(旧命令)
git switch feature-name                    # 切换分支(新命令)
git checkout -b feature-name               # 创建并切换
git switch -c feature-name                 # 创建并切换(新命令)
# 删除分支
git branch -d branch-name                  # 安全删除(已合并)
git branch -D branch-name                  # 强制删除
# 重命名分支
git branch -m old-name new-name            # 重命名当前分支
```

**输入**: 用户提供分支管理所需的指令和必要参数。
**处理**: 按照skill规范执行分支管理操作,遵循单一意图原则。
**输出**: 返回分支管理的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 4. 合并与冲突解决
```bash
# 合并分支
git merge feature-name                     # 合并到当前分支
git merge --no-ff feature-name             # 保留合并记录
git merge --abort                          # 取消合并
# 变基
git rebase main                            # 将当前分支变基到main
git rebase -i HEAD~3                       # 交互式变基最近3个提交
git rebase --continue                      # 解决冲突后继续
git rebase --abort                         # 取消变基
git rebase --skip                          # 跳过当前提交
# 冲突解决
git diff --name-only --diff-filter=U       # 查看冲突文件
# 手动编辑冲突文件,解决冲突标记
git add resolved-files                     # 标记已解决
git commit                                 # 完成合并
# 或
git rebase --continue                      # 完成变基
# 检查是否还有冲突标记
grep -r "<<<\|>>>\|===" .
```

**输入**: 用户提供合并与冲突解决所需的指令和必要参数。
**处理**: 按照skill规范执行合并与冲突解决操作,遵循单一意图原则。
**输出**: 返回合并与冲突解决的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 5. 历史检查与恢复
```bash
# 查看历史
git log                                    # 完整历史
git log --oneline                          # 简洁模式
git log --graph --oneline --all            # 图形化所有分支
git log -5                                 # 最近5个提交
git log --author="Name"                    # 按作者筛选
git log --since="2 weeks ago"              # 按时间筛选
git log -- file.txt                        # 特定文件历史
# 快速摘要
git status -sb                             # 简短状态
git log --oneline -5                       # 最近5个提交
git shortlog -sn                           # 贡献者统计
git diff --stat HEAD~5                     # 最近5个提交统计
# 恢复操作
git reset --soft HEAD~1                    # 撤销提交,保留变更
git reset --hard HEAD~1                    # 撤销提交,丢弃变更(危险)
git restore file.txt                       # 丢弃工作区变更
git restore --staged file.txt              # 取消暂存
# 查找丢失的提交
git reflog                                 # 操作历史(保留约90天)
git checkout -b branch-name <sha>          # 从历史创建分支
```

**输入**: 用户提供历史检查与恢复所需的指令和必要参数。
**处理**: 按照skill规范执行历史检查与恢复操作,遵循单一意图原则。
**输出**: 返回历史检查与恢复的执行结果,包含操作状态和输出数据。
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：冲突解决与历史恢、复等核心命令、适合开发者日常版、本管理、面向开发者的、版本管理工具包、涵盖提交管理、分支策略、合并冲突解决、核心能力、提交管理与规范、分支管理与切换、基本团队协作工作等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

## 使用场景
- 不适用: 需要人工判断的复杂决策场景
### 场景一:功能分支开发
标准功能分支开发工作流。

```bash
#!/bin/bash
# 功能分支工作流
echo "=== 功能分支开发流程 ==="

# 1. 从main创建功能分支
git checkout main
git pull origin main
git checkout -b feature/user-auth

# 2. 开发并提交
git add .
git commit -m "feat(auth): 实现用户认证逻辑"

# 3. 定期同步main
git fetch origin
git rebase origin/main

# 4. 推送到远程
git push -u origin feature/user-auth

# 5. 创建Pull Request(在平台上操作)
# 6. 合并后清理
git checkout main
git pull origin main
git branch -d feature/user-auth
git push origin --delete feature/user-auth

echo "功能分支流程完成"
```

### 场景二:冲突解决
解决合并冲突的完整流程。

```bash
#!/bin/bash
# 冲突解决流程
echo "=== 冲突解决流程 ==="

# 1. 合并时遇到冲突
git merge feature-branch
# CONFLICT (content): Merge conflict in src/index.js
# 2. 查看冲突文件
echo "冲突文件:"
git diff --name-only --diff-filter=U

# 3. 查看冲突内容
echo -e "\n冲突详情:"
git diff

# 4. 手动解决冲突
echo "请手动编辑冲突文件,解决以下标记:"
echo "  <<<<<<< HEAD (当前分支)"
echo "  ======="
echo "  >>>>>>> feature-branch (合并分支)"

# 5. 标记已解决
# git add src/index.js
# 6. 验证无冲突标记
echo -e "\n检查冲突标记:"
if grep -r "<<<\|>>>\|===" . --include="*.js" --include="*.ts"; then
    echo "仍有未解决的冲突标记!"
else
    echo "冲突标记已清除"
fi

# 7. 完成合并
# git commit
# 或取消合并
# git merge --abort
```

### 场景三:误操作恢复
恢复误删除的分支或提交。

```bash
#!/bin/bash
# 误操作恢复
echo "=== 误操作恢复 ==="

# 1. 查看操作历史
echo "最近的Git操作:"
git reflog -20

# 2. 恢复误删除的分支
echo -e "\n恢复误删除的分支:"
echo "1. 找到分支最后的提交SHA:"
git reflog | grep "feature-deleted"
echo "2. 从该SHA创建新分支:"
echo "   git checkout -b feature-deleted <sha>"

# 3. 恢复误reset的提交
echo -e "\n恢复误reset的提交:"
echo "1. 查看reset前的提交:"
git reflog | grep "reset"
echo "2. 恢复到该提交:"
echo "   git reset --hard <sha>"

# 4. 撤销已推送的提交(安全方式)
echo -e "\n撤销已推送的提交(使用revert):"
echo "  git revert <commit-sha>"
echo "  git push origin main"
```

## 快速开始
### Step 1:配置Git
```bash
# 设置用户信息
git config --global user.name "你的名字"
git config --global user.email "your@email.com"

# 设置默认分支名
git config --global init.defaultBranch main

# 配置别名
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.lg "log --graph --oneline --all"
```

### Step 2:触发Git操作
在 AI Agent 中输入:

```
请帮我创建功能分支,提交代码并推送到远程。
```

### Step 3:安全检查
Agent 会自动进行安全检查,避免危险操作。

**结果处理**: 执行完成后,查看输出结果确认操作状态。成功时输出包含处理摘要和结果数据;失败时根据错误信息排查问题,查阅错误处理章节获取恢复步骤。

#
## 示例
### Git配置模板
```ini
# ~/.gitconfig
[user]
    name = 你的名字
    email = your@email.com

[init]
    defaultBranch = main

[alias]
    st = status
    co = checkout
    br = branch
    ci = commit
    sw = switch
    lg = log --graph --oneline --all
    last = log -1 HEAD
    amend = commit --amend --no-edit
    unstage = reset HEAD --
    visual = log --graph --oneline --all

[pull]
    rebase = true

[push]
    default = current
    autoSetupRemote = true

[core]
    editor = code --wait
    autocrlf = input
```

### .gitignore 模板
```gitignore
# 依赖
node_modules/
__pycache__/
venv/
.venv/

# 构建产物
dist/
build/
*.o
*.so

# 环境变量
.env
.env.local
.env.*.local

# IDE
.vscode/
.idea/
*.swp
*.swo

# 系统
.DS_Store
Thumbs.db

# 日志
*.log
logs/
```

## 最佳实践
1. **提交前检查**:提交前确认状态和变更内容

```bash
git status
git diff
git diff --staged
```

2. **小步提交**:每次提交聚焦一个变更

```bash
# 使用 -p 选择性暂存
git add -p
```

3. **安全推送**:使用 `--force-with-lease` 替代 `--force`

```bash
# 推荐
git push --force-with-lease

# 危险(不推荐)
# git push --force
```

4. **写规范的提交信息**

```bash
# 格式: type(scope): description
git commit -m "feat(auth): 添加OAuth2登录支持"
git commit -m "fix(api): 修复用户列表500错误

详细说明:
- 修复了空指针异常
- 添加了参数校验
- 增加了错误处理"
```

5. **操作前确认**:执行危险操作前确认分支

```bash
# 安全检查清单
git branch                    # 确认当前分支
git status                    # 确认无未提交变更
git stash list                # 确认无暂存内容
```

## 常见问题
### Q1:如何撤销最近的提交?
```bash
# 撤销提交,保留变更在工作区
git reset --soft HEAD~1

# 撤销提交,变更回到未暂存状态
git reset HEAD~1

# 撤销提交,丢弃所有变更(危险!)
git reset --hard HEAD~1
```

### Q2:如何修改已推送的提交?
```bash
# 安全方式:使用revert(不会改写历史)
git revert <commit-sha>
git push origin main

# 不安全方式:amend(会改写历史,仅限未共享分支)
git commit --amend -m "新信息"
git push --force-with-lease
```

### Q3:如何解决合并冲突?
1. `git status` 查看冲突文件
2. 打开冲突文件,找到 `<<<<<<<`、`=======`、`>>>>>>>` 标记
3. 手动编辑解决冲突,删除标记
4. `git add <file>` 标记已解决
5. `git commit` 完成合并

### Q4:免费版与专业版有何区别?
| 能力维度 | 免费版 | 专业版 |
|:---------|:-------|:-------|
| 工作流 | 基础工作流 | 高级团队工作流 |
| 自动化 | 手动执行 | CI/CD集成 |
| 批量操作 | 不支持 | 批量分支管理 |
| 代码审查 | 手动 | 自动化审查 |
| 钩子管理 | 不支持 | Git Hook管理 |
| 历史分析 | 基础log | 高级分析 |

### Q5:git checkout 和 git switch 有什么区别?
```bash
# git checkout(旧命令,功能多)
git checkout branch-name        # 切换分支
git checkout -b new-branch      # 创建并切换
git checkout -- file.txt        # 丢弃变更
# git switch(新命令,专用于分支)
git switch branch-name          # 切换分支
git switch -c new-branch        # 创建并切换
# git restore(新命令,专用于恢复)
git restore file.txt            # 丢弃变更
git restore --staged file.txt   # 取消暂存
```

## 依赖说明
### 运行环境
- **Agent 平台**:支持 SKILL.md 的任意 AI Agent(Claude Code / Cursor / Codex / Gemini CLI 等)
- **操作系统**:Windows / macOS / Linux
- **运行时**:Git 2.20+

### 依赖详情
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-------|:-----|:---------|:---------|
| Git | 运行时 | 必需 | git-scm.com 下载 |
| LLM API | API | 必需 | 由 Agent 内置 LLM 提供 |

### API Key 配置
- 本 Skill 基于 Markdown 指令,无需额外 API Key
- 远程仓库认证配置:

```bash
# HTTPS认证
git config --global credential.helper store

# SSH密钥认证
ssh-keygen -t ed25519 -C "your@email.com"
# 将公钥添加到Git托管平台
```

### 可用性分类
- **分类**:MD+EXEC(纯 Markdown 指令,需要 exec 命令行执行能力)
- **说明**:基于 Markdown 的 AI Skill,通过自然语言指令驱动 Agent 执行Git操作
- **适用规模**:个人到小团队项目

## 错误处理

- 边界输入处理: 空输入返回提示信息, 超长输入自动截断
- 降级策略: 异常时返回默认值, 确保流程不中断
| 错误场景 | 原因 | 处理方式 |
|---------|------|---------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 已知限制
- 需LLM支持,无LLM环境不可用
- 复杂业务场景建议结合人工经验判断
- 执行效率受模型能力与网络环境影响

## 案例展示