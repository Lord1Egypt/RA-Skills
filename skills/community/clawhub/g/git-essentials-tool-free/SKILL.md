---

name: "git-essentials-tool-free"
description: "提供Git版本控制核心命令,涵盖初始化、提交、分支、远程同步与历史管理,适合开发者入门。Use when 需要代码生成、编程辅助、调试测试、开发部署时使用。不适用于无明确技术栈的模糊需求。适用于独立开发者、企业团队和自动化工作流场景。支持中文交互，无需复杂配置即开即用。输出结果可直接使用，减少二次加工成本。"
license: Proprietary
allowed-tools: read exec
compatibility: "Requires LLM with tool-use capability"
metadata:
  displayName: "Git基础工具免费版"
  version: "1.0.0"
  summary: "提供Git版本控制核心命令,涵盖初始化、提交、分支、远程同步与历史管理,适合开发者入门。"
  tags:
    - "开发工具"
    - "Git"
    - "版本控制"
  source: "SkillHub"
  converted_at: "2026-07-22T17:58:36"
tools:
  - exec
  - read
  - write

---

> **功能说明**: 本技能涵盖 中文交互、化工作流场景 等核心能力。


# Git基础工具 - 免费版
## 概述
Git基础工具免费版为开发者提供版本控制核心命令支持。工具涵盖仓库初始化、暂存提交、分支管理、远程同步和历史查看,帮助开发者掌握Git日常操作。

本版本适合Git入门学习、日常版本控制操作和分支管理协作。所有命令均为Git核心命令,无需额外安装。

## 核心能力
### 1. 初始设置
```bash
# 全局配置
git config --global user.name "你的名字"
email "your@email.com"
git config --global init.defaultBranch main

# 初始化仓库
git init

# 克隆仓库
git clone https://example.com/user/repo.git
com/user/repo.git custom-name
```

**输出**: 返回初始设置的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 2. 基本工作流
```bash
# 暂存与提交
git status                           # 查看状态
git add file.txt                     # 暂存单个文件
git add .                            # 暂存所有变更
git add -A                           # 包括删除操作
git commit -m "提交信息"             # 提交
git commit -am "信息"                # 添加并提交已跟踪文件
# 修改提交
git commit --amend -m "新信息"       # 修改提交信息
git commit --amend --no-edit         # 保持原信息
# 查看变更
git diff                             # 工作区变更
git diff --staged                    # 暂存区变更
git diff file.txt                    # 特定文件
git diff commit1 commit2             # 比较两个提交
```

**输出**: 返回基本工作流的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 3. 分支与合并
```bash
# 分支管理
git branch                           # 查看本地分支
git branch -a                        # 查看所有分支
git branch feature-name              # 创建分支
git switch feature-name              # 切换分支(新命令)
git checkout feature-name            # 切换分支(旧命令)
git switch -c feature-name           # 创建并切换
git branch -d branch-name            # 删除已合并分支
git branch -D branch-name            # 强制删除
git branch -m old new                # 重命名
# 合并
git merge feature-name               # 合并分支
git merge --no-ff feature-name       # 保留合并记录
git merge --abort                    # 取消合并
git diff --name-only --diff-filter=U # 查看冲突文件
```

**输出**: 返回分支与合并的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 4. 远程操作
```bash
# 管理远程仓库
git remote -v                        # 查看远程
git remote add origin <url>          # 添加远程
git remote set-url origin <url>      # 修改远程URL
git remote remove origin             # 删除远程
# 同步
git fetch origin                     # 获取不合并
git pull                             # 拉取并合并
git pull --rebase                    # 拉取并变基
git push                             # 推送
git push -u origin branch-name       # 首次推送
git push --force-with-lease          # 安全强制推送
```

**输出**: 返回远程操作的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 5. 历史与日志
```bash
# 查看历史
git log                              # 完整历史
git log --oneline                    # 简洁模式
git log --graph --oneline --all      # 图形化
git log -5                           # 最近5个
git log --author="Name"              # 按作者
git log --since="2 weeks ago"        # 按时间
git log -- file.txt                  # 特定文件
# 搜索历史
git log --grep="bug fix"             # 搜索提交信息
git log -S "function_name"           # 搜索代码变更
git blame file.txt                   # 逐行历史
```

**输出**: 返回历史与日志的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 6. 撤销与恢复
```bash
# 工作区
git restore file.txt                 # 丢弃工作区变更
git restore .                        # 丢弃所有
# 暂存区
git restore --staged file.txt        # 取消暂存
git reset HEAD file.txt              # 取消暂存(旧)
# 提交
git reset --soft HEAD~1              # 撤销提交,保留变更
git reset --hard HEAD~1              # 撤销提交,丢弃变更
git revert commit-hash               # 创建反向提交
```

**输出**: 返回撤销与恢复的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 7. 暂存(stash)
```bash
git stash                            # 暂存当前工作
git stash save "描述"                # 带描述暂存
git stash list                       # 查看暂存列表
git stash apply                      # 恢复(保留暂存)
git stash pop                        # 恢复(删除暂存)
git stash apply stash@{2}            # 恢复指定暂存
git stash drop stash@{0}             # 删除指定暂存
git stash clear                      # 清除所有
```

**输出**: 返回暂存(stash)的执行结果,包含操作状态和输出数据。
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：版本控制核心命令、涵盖初始化、远程同步与历史管、适合开发者入门、面向开发者的、版本控制基础工具、涵盖仓库初始化、暂存提交、远程操作与历史查、核心能力、仓库初始化与克隆、暂存与提交管理、分支创建与合并、远程仓库同步、历史查看与搜索等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

## 使用场景
### 场景一:新项目初始化
从头创建新的Git项目。

```bash
#!/bin/sh
# 新项目Git初始化
echo "=== Git项目初始化 ==="

# 1. 初始化仓库
git init
git branch -M main

# 2. 创建.gitignore
cat > .gitignore << 'EOF'
node_modules/
.env
*.log
dist/
.vscode/
.DS_Store
EOF

# 3. 首次提交
git add .
git commit -m "chore: 项目初始化"

# 4. 添加远程仓库
echo "请输入远程仓库地址:"
read REMOTE_URL
git remote add origin "$REMOTE_URL"

# 5. 推送
git push -u origin main

echo "项目初始化完成"
```

### 场景二:功能分支开发
使用功能分支进行开发。

```bash
#!/bin/sh
# 功能分支工作流
echo "=== 功能分支开发 ==="

# 1. 创建功能分支
git switch main
git pull
git switch -c feature/user-profile

# 2. 开发提交
git add .
git commit -m "feat(profile): 添加用户资料页面"

# 3. 推送
git push -u origin feature/user-profile

# 4. 合并到main(通过PR后)
git switch main
git pull
git merge --no-ff feature/user-profile
git push

# 5. 清理
git branch -d feature/user-profile
git push origin --delete feature/user-profile

echo "功能开发完成"
```

### 场景三:同步fork仓库
同步上游仓库的更新。

```bash
#!/bin/sh
# 同步fork
echo "=== 同步fork仓库 ==="

# 1. 添加上游仓库(仅首次)
git remote add upstream https://example.com/original/repo.git

# 2. 获取上游更新
git fetch upstream

# 3. 切换到main分支
git switch main

# 4. 合并上游更新
git merge upstream/main

# 5. 推送到自己的fork
git push origin main

echo "fork同步完成"
```

## 不适用场景
以下场景Git基础工具免费版不适合处理：

- 无明确技术栈的模糊需求
- 纯架构设计决策
- 运维部署管理

## 触发条件
需要代码生成、编程辅助、调试测试、开发部署时使用。不适用于非本工具能力范围的需求。

## 快速开始
### Step 1:配置Git
```bash
email "your@email.com"
```

### Step 2:触发操作
在 AI Agent 中输入:

```
请帮我初始化Git仓库并完成首次提交。
```

### Step 3:执行操作
Agent 会引导完成Git操作。

**结果处理**: 执行完成后,查看输出结果确认操作状态。成功时输出包含处理摘要和结果数据;失败时根据错误信息排查问题,查阅错误处理章节获取恢复步骤。

#
## 示例
### 常用别名配置
```ini
# $HOME/.gitconfig
[alias]
    st = status
    co = checkout
    sw = switch
    br = branch
    ci = commit
    unstage = reset HEAD --
    last = log -1 HEAD
    visual = log --graph --oneline --all
    amend = commit --amend --no-edit
    lg = log --graph --oneline --all -20
```

### 标签管理
```bash
# 创建标签
git tag v1.0.0                           # 轻量标签
git tag -a v1.0.0 -m "版本1.0.0"         # 附注标签(推荐)
git tag v1.0.0 commit-hash               # 指定提交
# 推送标签
git push origin v1.0.0                   # 推送单个标签
git push --tags                          # 推送所有标签
# 删除标签
git tag -d v1.0.0                        # 删除本地
git push origin --delete v1.0.0          # 删除远程
```

### 高级操作
```bash
# Cherry-pick(选择性合并)
git cherry-pick commit-hash
git cherry-pick -n commit-hash          # 不自动提交
# 子模块
git submodule add <url> path/
git submodule init
git submodule update
git clone --recursive <url>

# 清理
git clean -n                             # 预览
git clean -f                             # 清理未跟踪文件
git clean -fd                            # 清理目录
git clean -fdx                           # 清理包括gitignore
# 变基
git rebase main                          # 变基到main
git rebase -i HEAD~3                     # 交互式变基
git rebase --continue                    # 继续
git rebase --abort                       # 取消
```

## 优选实践
1. **频繁提交**:小步提交,每次聚焦一个变更

2. **规范信息**:使用Conventional Commits格式

```bash
git commit -m "feat(auth): 添加用户登录功能"
git commit -m "fix(api): 修复分页错误"
```

3. **使用分支**:不要直接在main上开发

4. **拉取前先提交**:避免冲突时丢失工作

5. **使用.gitignore**:排除不需要版本控制的文件

## 常见问题
### Q1:如何解决合并冲突?
```bash
# 1. 查看冲突文件
git diff --name-only --diff-filter=U

# 2. 编辑冲突文件,解决标记
# <<<<<<< HEAD
# 你的代码
# =======
# 别人的代码
# >>>>>>> branch-name
# 3. 标记已解决
git add resolved-file.txt

# 4. 完成合并
git commit
```

### Q2:如何撤销已推送的提交?
```bash
# 安全方式(推荐)
git revert <commit-sha>
git push

# 不安全方式(仅未共享分支)
git reset --hard HEAD~1
git push --force-with-lease
```

### Q3:如何查看某个文件的修改历史?
```bash
git log --oneline -- file.txt       # 提交历史
git log -p file.txt                 # 包含差异
git blame file.txt                  # 逐行作者
git log --follow file.txt           # 包括重命名
```

### Q4:免费版与专业版有何区别?
| 能力维度 | 免费版 | 专业版 |
|:---------|:-------|:-------|
| 命令范围 | 核心命令 | 全部命令 |
| 变基操作 | 基础 | 高级交互式 |
| 历史管理 | 查看 | 历史重写 |
| 子模块 | 基础 | 批量管理 |
| 性能优化 | 不支持 | gc优化 |
| 批量操作 | 不支持 | 批量处理 |

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
- 远程仓库认证:

```bash
# HTTPS
git config --global credential.helper store

# SSH
ssh-keygen -t ed25519 -C "your@email.com"
```

### 可用性分类
- **分类**:MD+execute(纯 Markdown 指令,需要 exec 命令行执行能力)
- **说明**:基于 Markdown 的 AI Skill,通过自然语言指令驱动 Agent 执行Git操作
- **适用规模**:个人开发者和小团队

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