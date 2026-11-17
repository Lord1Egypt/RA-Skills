---

name: "git-workflow-cn-tool-free"
description: "Git 分支管理、冲突解决与提交规范助手，覆盖个人开发者日常版本控制场景。Use when 需要代码生成、编程辅助、调试测试、开发部署时使用。不适用于无明确技术栈的模糊需求。适用于独立开发者、企业团队和自动化工作流场景。支持中文交互，无需复杂配置即开即用。输出结果可直接使用，减少二次加工成本。提供结构化输出和错误处理机制。"
license: Proprietary
allowed-tools: read exec
compatibility: "Requires LLM with tool-use capability"
metadata:
  displayName: "Git工作流助手免费版"
  version: "1.0.0"
  summary: "Git 分支管理、冲突解决与提交规范助手，覆盖个人开发者日常版本控制场景。"
  tags:
    - "开发工具"
    - "版本控制"
    - "Git"
    - "工作流"
  source: "SkillHub"
  converted_at: "2026-07-22T17:58:36"
tools:
  - exec
  - read
  - write

---

> **功能说明**: 本技能涵盖 中文交互、化工作流场景 等核心能力。


# Git 工作流助手（免费版）

## 概述

本工具为独立开发者提供 Git 日常操作的结构化指引，覆盖分支管理、冲突解决、提交规范三大核心场景。通过自然语言指令驱动，帮助开发者快速完成版本控制任务，降低 Git 学习成本，提升提交信息质量。免费版聚焦个人开发场景中的高频操作，提供开箱即用的命令速查与规范模板。

## 核心能力

| 能力模块 | 描述 | 典型用法 |
| --- | --- | --- |
| 分支管理 | 创建、切换、合并、删除分支 | `创建并切换到 feature/login 分支` |
| 冲突解决 | 识别冲突标记并提供解决策略 | `帮我解决 Git 合并冲突` |
| 提交规范 | 生成符合 Conventional Commits 的提交信息 | `为这些改动生成提交信息` |
| 撤销回滚 | 撤销暂存、回滚提交、恢复删除文件 | `撤销最后一次提交` |
**技术实现要点**：核心能力基于`input_params`参数与`output_format`配置实现,支持创建/查询/修改/删除等操作模式,通过`config_options`进行运行时配置。

### 核心功能执行
用`input_params`参数进行配置。

**输出**: 返回核心功能执行的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 参数配置与调用
用`config_options`参数进行配置。

**输出**: 返回参数配置与调用的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`config_options`参数,支持修改/重置/导入操作

### 结果处理与输出
用`output_format`参数进行配置。

**输出**: 返回结果处理与输出的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`output_format`参数,支持导出/保存/转换操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：冲突解决与提交规、范助手、覆盖个人开发者日、常版本控制场景、面向独立开发者的、工作流辅助工具、聚焦分支管理、范三大核心能力、分支创建、合并的标准化操作、合并冲突识别与基、础解决策略、提交规范生成、命令速查与撤销回、滚操作等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持。

## 使用场景

### 场景一：个人项目分支规划

开发者需要在个人项目中规划功能分支，保持主分支稳定。

```text
用户：我要开发登录功能，帮我规划分支策略

助手：
1. 从 main 分支创建功能分支
   git checkout -b feature/login main

2. 开发完成后提交
   git add .
   git commit -m "feat(auth): 添加登录功能"

3. 合并回主分支
   git checkout main
   git merge feature/login
   git branch -d feature/login
```

### 场景二：规范化提交信息生成

开发者完成代码改动后，需要生成符合规范的提交信息。

```text
用户：为以下改动生成提交信息
- 修改了支付模块的金额计算逻辑
- 修复了小数精度丢失问题

助手：
git commit -m "fix(payment): 修复支付金额计算精度丢失问题

- 使用整数分单位替代浮点元单位
- 统一金额计算入口方法
- 补充边界测试用例"
```

### 场景三：合并冲突处理

功能分支合并时出现冲突，需要快速定位并解决。

```text
用户：合并 feature/login 时出现冲突，怎么处理

助手：
1. 查看冲突文件
   git status

2. 冲突标记格式
   <<<<<<< HEAD
   当前分支内容
   =======
   合并分支内容
   >>>>>>> feature/login

3. 手动编辑后标记解决
   git add .
   git commit

4. 如需放弃合并
   git merge --abort
```

## 不适用场景

以下场景Git工作流助手免费版不适合处理：

- 实际人员绩效评估
- 财务预算审批
- 合同法务审核

## 触发条件

需要项目管理、任务规划、进度跟踪、团队协作时使用。不适用于非本工具能力范围的需求。

## 快速开始

1. 阅读## 核心能力章节了解skill功能
2. 按## 依赖说明配置环境
3. 执行所需能力对应的命令
4. 参考## 错误处理章节处理异常
5. 查看## FAQ解答常见疑问

### 基础配置

```bash
# 初始化身份信息
git config --global user.name "Your Name"
email "email@example.com"

# 设置默认分支名
git config --global init.defaultBranch main

# 配置常用别名
git config --global alias.co checkout
lg "log --graph --oneline --all"
```

### 常用命令速查

```bash
# 状态查看
git status                         # 查看工作区状态
git log --oneline                  # 简洁日志
git log --graph --oneline --all    # 图形化日志
git diff                           # 查看未暂存改动
git diff --staged                  # 查看已暂存改动
git show COMMIT_ID                 # 查看提交详情

# 分支操作
git branch                         # 本地分支列表
git branch -a                      # 所有分支（含远程）
git branch feature/login           # 创建分支
git checkout -b feature/login      # 创建并切换
git switch -c feature/login        # 新语法创建并切换
git checkout feature/login         # 切换分支
git switch feature/login           # 新语法切换
git branch -d feature/login        # 安全删除（已合并）
git branch -D feature/login        # 强制删除

# 合并操作
git merge feature/login            # 合并分支
git merge --no-ff feature/login    # 禁用快进合并（保留记录）

# 远程操作
git remote -v                      # 查看远程仓库
git fetch origin                   # 获取远程更新
git pull origin main               # 拉取并合并
git push origin main               # 推送到远程
git push -u origin feature/login   # 推送并设置上游
```

**结果处理**: 执行完成后,查看输出结果确认操作状态。成功时输出包含处理摘要和结果数据;失败时根据错误信息排查问题,查阅错误处理章节获取恢复步骤。

#
## 示例

### 提交规范模板

Conventional Commits 格式：

```text
<type>(<scope>): <subject>

<body>

<footer>
```

| Type | 描述 | 示例 |
| --- | --- | --- |
| feat | 新功能 | `feat(auth): 添加登录功能` |
| fix | 修复缺陷 | `fix(api): 修复接口超时` |
| docs | 文档更新 | `docs(readme): 更新安装说明` |
| style | 代码格式 | `style: 格式化代码` |
| refactor | 重构 | `refactor(utils): 优化工具函数` |
| perf | 性能优化 | `perf(list): 优化列表渲染` |
| test | 测试 | `test(auth): 添加登录测试` |
| chore | 构建/工具 | `chore: 更新依赖` |
| revert | 回滚 | `revert: 回滚登录功能` |

### 暂存操作配置

```bash
git stash                          # 暂存当前修改
git stash save "WIP: 登录功能"     # 带消息暂存
git stash list                     # 查看暂存列表
git stash pop                      # 恢复并删除暂存
git stash apply                    # 恢复但保留暂存
git stash drop stash@{0}           # 删除指定暂存
git stash clear                    # 清空所有暂存
```

## 优选实践

1. **提交前先拉取**：避免不必要的冲突
   ```bash
   git pull --rebase origin main
   ```

2. **功能分支及时合并**：避免长期分叉导致冲突累积

3. **避免直接提交到 main**：通过功能分支合并

4. **重要操作先备份**：危险操作前创建备份分支
   ```bash
   git branch backup-before-reset
   ```

5. **提交粒度适中**：一个提交解决一个问题

6. **使用 .gitignore**：忽略不需要追踪的文件

## 常见问题

### Q1：如何撤销最后一次提交但保留改动？

```bash
git reset --soft HEAD~1
```

### Q2：如何修改最后一次提交的信息？

```bash
git commit --amend -m "新的提交信息"
```

### Q3：如何恢复误删的分支？

```bash
git reflog                        # 查找分支最后的提交
git checkout -b recovered-branch COMMIT_ID
```

### Q4：如何回滚某个提交？

```bash
git revert COMMIT_ID              # 生成一个反向提交
git revert --no-commit COMMIT_ID  # 不自动提交
```

### Q5：合并冲突太多想放弃怎么办？

```bash
git merge --abort                 # 取消合并，恢复合并前状态
```

### Q6：如何清理未追踪的文件？

```bash
git clean -n                      # 预览将要删除的文件
git clean -f                      # 删除未追踪文件
git clean -fd                     # 删除未追踪文件和目录
```

## 依赖说明

### 运行环境
- **Agent 平台**: 支持读取 SKILL.md 的任意 AI Agent（Claude Code / Cursor / Codex / Gemini CLI 等）
- **操作系统**: Windows / macOS / Linux
- **Git 版本**: 建议 2.20 及以上

### 依赖详情

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-------|:-----|:---------|:---------|
| Git | 命令行工具 | 必需 | 系统包管理器安装 |
| LLM API | API | 必需 | 由 Agent 内置 LLM 提供 |

### API Key 配置
- 本工具为纯 Markdown 指令驱动，无需额外 API Key
- Git 远程推送需要配置 SSH Key 或个人访问令牌

### 可用性分类
- **分类**: MD+EXEC（Markdown 指令 + 命令行执行）
- **说明**: 通过自然语言指令驱动 Agent 执行 Git 操作，部分功能需要 exec 命令行执行能力

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
- 当前为免费版本,如需完整功能请升级到付费版获取全部能力

## 安全注意事项

| 风险类型 | 防范措施 |
|----------|---------|
| API密钥泄露 | 通过环境变量配置，禁止硬编码到代码或配置文件中 |
| 命令执行风险 | 仅执行白名单命令，避免拼接用户输入到命令行参数中 |
| 网络通信安全 | 使用HTTPS协议，验证SSL证书有效性 |
| 敏感数据暴露 | 输出结果中不包含密钥、令牌等敏感信息 |

使用前请确认已阅读依赖说明章节，确保运行环境满足安全要求。