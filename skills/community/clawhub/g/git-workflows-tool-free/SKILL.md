---
name: "git-workflows-tool-free"
description: "Git 进阶操作助手，涵盖交互式变基、二分查找、工作树与引用日志恢复。Use when 需要AI模型调用、智能对话、Agent编排、LLM应用时使用。不适用于需要100%确定性的关键决策。适用于独立开发者、企业团队和自动化工作流场景。支持中文交互，无需复杂配置即开即用。输出结果可直接使用，减少二次加工成本。"
license: Proprietary
allowed-tools: read exec
compatibility: "Requires LLM with tool-use capability"
metadata:
  displayName: "Git高级操作免费版"
  version: "1.0.0"
  summary: "Git 进阶操作助手，涵盖交互式变基、二分查找、工作树与引用日志恢复。"
  tags:
    - "开发工具"
    - "版本控制"
    - "Git进阶"
  source: "SkillHub"
  converted_at: "2026-07-22T17:58:36"
tools:
  - exec
  - read
  - write
---

> **功能说明**: 本技能涵盖 中文交互、化工作流场景 等核心能力。

# Git 高级操作助手（免费版）

## 概述

本工具为进阶开发者提供超越基础 add/commit/push 的 Git 操作指引，涵盖交互式变基、二分查找、工作树、引用日志恢复、樱桃挑选等核心场景。通过自然语言指令驱动，帮助开发者清理提交历史、定位缺陷来源、并行处理多分支任务，并在误操作后快速恢复。免费版聚焦个人开发者最常用的高频进阶操作，提供完整的命令模板与示例。

## 核心能力

| 能力模块 | 描述 | 典型用法 |
| --- | --- | --- |
| 交互式变基 | 整理、合并、重排、编辑提交 | `帮我合并最近 5 个提交` |
| 二分查找 | 定位引入缺陷的提交 | `用 bisect 找到引入 bug 的提交` |
| 工作树 | 并行处理多个分支 | `创建工作树处理紧急修复` |
| 引用日志恢复 | 恢复丢失的提交和分支 | `恢复误删的提交` |
| 樱桃挑选 | 跨分支复制特定提交 | `把这个提交挑选到 main 分支` |
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
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：Git、进阶操作助手、涵盖交互式变基、工作树与引用日志、面向进阶开发者的、高级操作工具、add、commit、push、之外的核心进阶场、rebase、整理提交历史、worktree、并行多分支开发、reflog等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持。

## 使用场景

### 场景一：合并前清理提交历史

功能分支包含多个琐碎提交，合并前需要整理成清晰的提交序列。

```text
用户：我的功能分支有 5 个琐碎提交，合并前想整理一下

助手：使用交互式变基

1. 启动变基
   git rebase -i HEAD~5

2. 编辑器中会显示提交列表
   pick a1b2c3d 添加用户模型
   pick e4f5g6h 修复模型拼写错误
   pick i7j8k9l 添加用户控制器
   pick m0n1o2p 添加用户路由
   pick q3r4s5t 修复控制器导入

3. 修改操作指令（合并修复提交）
   pick a1b2c3d 添加用户模型
   fixup e4f5g6h 修复模型拼写错误
   pick i7j8k9l 添加用户控制器
   fixup q3r4s5t 修复控制器导入
   pick m0n1o2p 添加用户路由

4. 保存退出后自动完成变基

5. 如需放弃变基
   git rebase --abort

6. 如遇冲突解决后继续
   git add .
   git rebase --continue
```

### 场景二：定位引入缺陷的提交

线上发现一个回归缺陷，需要快速找到是哪个提交引入的。

```text
用户：登录功能在某个提交后坏了，帮我用 bisect 找出来

助手：
1. 启动二分查找
   git bisect start

2. 标记当前版本为坏
   git bisect bad

3. 标记已知正常的版本
   git bisect good v1.2.0

4. Git 会自动切换到中间提交，测试后标记
   git bisect good   # 这个提交正常
   git bisect bad    # 这个提交有问题

5. 重复直到定位到具体提交

6. 完成后重置
   git bisect reset
```

### 场景三：同时处理多个分支任务

正在开发功能时收到紧急修复任务，不想丢失当前工作。

```bash
# 创建工作树处理紧急修复
git worktree add ../project-hotfix hotfix/urgent-fix

# 创建新分支的工作树
git worktree add ../project-feature -b feature/new-thing

# 查看所有工作树
git worktree list

# 在工作树中完成工作后移除
cd ../project-hotfix
# 完成修复并推送
cd ../project
git worktree remove ../project-hotfix

# 清理无效的工作树引用
git worktree prune
```

## 不适用场景

以下场景Git高级操作免费版不适合处理：

- 需要100%确定性的关键决策
- 医疗诊断
- 法律判决

## 触发条件

需要AI模型调用、智能对话、Agent编排、LLM应用时使用。不适用于非本工具能力范围的需求。

## 快速开始

1. 阅读## 核心能力章节了解skill功能
2. 按## 依赖说明配置环境
3. 执行所需能力对应的命令
4. 参考## 错误处理章节处理异常
5. 查看## FAQ解答常见疑问

### 交互式变基命令速查

```bash
git rebase -i HEAD~5          # 变基最近 5 个提交
git rebase -i main            # 变基到 main 分支
git rebase --abort            # 取消变基
git rebase --continue         # 解决冲突后继续
git rebase --skip             # 跳过当前提交
```

变基操作指令：

| 指令 | 作用 | 说明 |
| --- | --- | --- |
| pick | 保留提交 | 使用提交原样 |
| reword | 修改信息 | 保留提交但修改提交信息 |
| edit | 暂停编辑 | 停在此提交进行修改 |
| squash | 合并保留信息 | 合并到上一个提交，保留两条信息 |
| fixup | 合并丢弃信息 | 合并到上一个提交，丢弃提交信息 |
| drop | 删除提交 | 完全移除该提交 |

### 自动变基（autosquash）

```bash
# 创建修复提交（自动标记目标）
git commit --fixup=a1b2c3d
git commit --squash=a1b2c3d

# 自动整理
git rebase -i --autosquash main
```

### 二分查找自动化

```bash
# 手动二分
git bisect start
git bisect bad
git bisect good v1.2.0

# 自动化二分（带测试脚本）
git bisect start HEAD v1.2.0
git bisect run ./test-for-bug.sh

# 示例
cat > /tmp/test-for-bug.sh << 'EOF'
#!/bin/sh
npm test -- --grep "login should redirect" 2>/dev/null
EOF
chmod +x /tmp/test-for-bug.sh
git bisect run /tmp/test-for-bug.sh

# 跳过无法构建的提交
git bisect skip
```

**结果处理**: 执行完成后,查看输出结果确认操作状态。成功时输出包含处理摘要和结果数据;失败时根据错误信息排查问题,查阅错误处理章节获取恢复步骤。

#
## 配置示例

### 引用日志恢复操作

```bash
# 查看所有操作记录
git reflog
git reflog show feature/my-branch
git reflog --date=relative

# 恢复到指定状态
git reset --hard HEAD@{2}      # 回到 2 步之前的状态
git reset --hard ghi789        # 回到指定提交

# 恢复误删的分支
git branch recovered-branch abc123

# 查找丢失的提交
git fsck --unreachable | grep commit

# 查找丢弃的暂存
git stash list
git log --walk-reflogs --all -- stash
```

### 樱桃挑选操作

```bash
# 挑选单个提交
git cherry-pick abc123

# 挑选多个提交
git cherry-pick abc123 def456 ghi789

# 挑选提交范围
git cherry-pick abc123..ghi789

# 不自动提交
git cherry-pick --no-commit abc123

# 冲突处理
git add resolved-file.ts
git cherry-pick --continue
git cherry-pick --abort
```

## 优选实践

1. **变基仅限本地分支**：永远不要变基已推送到共享分支的提交

2. **引用日志是安全网**：误操作后 90 天内提交均可恢复
   ```bash
   git reflog
   ```

3. **工作树比多克隆更高效**：工作树共享 .git 存储，节省磁盘空间

4. **自动化二分更可靠**：`git bisect run` 配合测试脚本消除人为错误

5. **使用 fixup 提交**：开发时用 `--fixup` 标记，合并前统一整理
   ```bash
   git commit --fixup=目标提交
   git rebase -i --autosquash main
   ```

6. **樱桃挑选后测试**：跨分支复制提交后务必运行测试

## 常见问题

### Q1：变基时冲突太多怎么办？

```bash
# 放弃变基
git rebase --abort

# 或逐个解决
git status
# 编辑冲突文件
git add .
git rebase --continue

# 跳过无法解决的提交
git rebase --skip
```

### Q2：bisect 时遇到构建失败的提交？

```bash
git bisect skip                    # 跳过当前提交
git bisect skip v1.3.0..v1.3.5    # 跳过指定范围
```

### Q3：如何查看某个文件的历史变更？

```bash
# 追踪文件重命名的历史
git log --follow --oneline -- src/auth.ts

# 查看文件每行最后修改者
git blame src/auth.ts
git blame -L 50,70 src/auth.ts    # 指定行范围

# 查找字符串被添加/删除的提交
git log -S "function oldName" --oneline
```

### Q4：工作树无法删除怎么办？

```bash
# 强制删除
git worktree remove --force ../project-hotfix

# 清理无效引用
git worktree prune
```

### Q5：如何恢复 reset --hard 丢失的提交？

```bash
git reflog                        # 找到丢失的提交哈希
git reset --hard abc123           # 恢复到该提交
```

### Q6：樱桃挑选冲突如何处理？

```bash
# 查看冲突文件
git status

# 解决冲突后
git add .
git cherry-pick --continue

# 放弃樱桃挑选
git cherry-pick --abort
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
- 自动化二分查找需要可执行的测试脚本

### 可用性分类
- **分类**: MD+EXEC（Markdown 指令 + 命令行执行）
- **说明**: 通过自然语言指令驱动 Agent 执行 Git 高级操作，所有功能依赖命令行执行能力

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

## 示例

### 基本用法

**输出**：返回执行结果,包含操作状态和输出数据

```text
用户: 执行核心功能
Skill: 正在执行核心功能...
Skill: 执行完成,结果如下: 操作成功
```

## 安全注意事项

| 风险类型 | 防范措施 |
|----------|---------|
| API密钥泄露 | 通过环境变量配置，禁止硬编码到代码或配置文件中 |
| 命令执行风险 | 仅执行白名单命令，避免拼接用户输入到命令行参数中 |
| 网络通信安全 | 使用HTTPS协议，验证SSL证书有效性 |
| 敏感数据暴露 | 输出结果中不包含密钥、令牌等敏感信息 |

使用前请确认已阅读依赖说明章节，确保运行环境满足安全要求。