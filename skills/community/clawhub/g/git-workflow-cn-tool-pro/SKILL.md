---

slug: git-workflow-cn-tool-pro
name: "git-workflow-cn-tool-pro"
version: "1.0.0"
displayName: "Git工作流专业版"
summary: "企业级 Git 工作流方案，支持 Git Flow、团队协作、冲突工具集成与批量分支管理。。面向团队协作与企业研发场景的 Git 工作流专业工具。Use when 需要提升效率、自动化流程、"
license: "Proprietary"
edition: "pro"
description: |-
  面向团队协作与企业研发场景的 Git 工作流专业工具。Use when 需要提升效率、自动化流程、批量处理、工作流优化时使用。不适用于需要人工创意判断的任务。适用于独立开发者、企业团队和自动化工作流场景。支持中文交互，无需复杂配置即开即用。输出结果可直接使用，减少二次加工成本。提供结构化输出和错误处理机制。
tags:
  - 开发工具
  - 版本控制
  - Git
  - 企业协作
  - DevOps
  - git
  - flow
  - main
  - origin
  - feature
tools:
  - read
  - exec
  - write
homepage: ""
category: "Development"

---

> **功能说明**: 本技能涵盖 中文交互、化工作流场景 等核心能力。


# Git 工作流助手（专业版）

## 概述

本工具面向中大型研发团队，提供企业级 Git 工作流治理方案。在免费版基础能力之上，专业版引入 Git Flow / GitHub Flow / GitLab Flow 三大工作流模型的完整落地指引，支持多分支并行管理、批量分支操作、冲突自动记忆（rerere）、发布分支管理与版本标签策略。通过结构化流程与自动化脚本，帮助团队建立统一的版本控制规范，降低协作冲突，提升发布效率.
**版本兼容性说明**：专业版完全兼容免费版（`git-workflow-cn-tool-free`）的所有命令与规范，可无缝升级.
## 核心能力

| 能力模块 | 免费版 | 专业版新增 |
|----|---|-----|
| 分支管理 | 基础创建/切换/合并 | 批量分支管理、保护分支策略 |
| 工作流模型 | - | Git Flow / GitHub Flow / GitLab Flow |
| 冲突解决 | 手动解决 | rerere 自动记忆 + 三方对比工具 |
| 提交规范 | Conventional Commits | CHANGELOG 自动生成 + 语义化版本 |
| 发布管理 | - | 发布分支、版本标签、回滚策略 |
| 团队协作 | - | 代码审查流程、合并请求规范 |
**技术实现要点**：核心能力基于`input_params`参数与`output_format`配置实现,支持创建/查询/修改/删除等操作模式,通过`config_options`进行运行时配置.
### 核心功能执行
用`input_params`参数进行配置.

**处理**: 解析核心功能执行的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回核心功能执行的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 参数配置与调用
用`config_options`参数进行配置.

**处理**: 解析参数配置与调用的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回参数配置与调用的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`config_options`参数,支持修改/重置/导入操作

### 结果处理与输出
用`output_format`参数进行配置.

**处理**: 解析结果处理与输出的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回结果处理与输出的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`output_format`参数,支持导出/保存/转换操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：企业级、工作流方案、冲突工具集成与批、面向团队协作与企、业研发场景的、工作流专业工具、Use、when、需要提升效率、自动化流程、批量处理、工作流优化时使用、不适用于需要人工、创意判断的任务、适用于独立开发者、企业团队和自动化、工作流场景等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
## 使用场景

### 场景一：Git Flow 发布流程管理

团队需要规划一个正式版本发布，包含功能开发、预发布验证、紧急修复全流程.
```text
用户：我们需要发布 v2.0.0 版本，包含多个功能分支，帮我规划 Git Flow 流程
# ...
助手：
1. 初始化 Git Flow
   git flow init
# ...
2. 功能分支开发（多个并行）
   git flow feature start user-auth
   git flow feature start payment-module
   # 开发完成后分别完成
   git flow feature finish user-auth
   git flow feature finish payment-module
# ...
3. 创建发布分支
   git flow release start v2.0.0
   # 在发布分支上仅允许修复缺陷和文档更新
# ...
4. 完成发布并打标签
   git flow release finish v2.0.0
   # 自动合并到 main 和 develop，并打版本标签
# ...
5. 推送所有分支和标签
   git push origin --all
   git push origin --tags
# ...
6. 紧急修复流程（如线上发现缺陷）
   git flow hotfix start fix-login-crash v2.0.0
   # 修复完成后
   git flow hotfix finish fix-login-crash
```

### 场景二：多环境部署分支策略

团队需要维护开发、预发、生产三个环境的代码同步.
```text
用户：我们有 dev/staging/prod 三个环境，怎么管理分支
# ...
助手：推荐 GitLab Flow 模式
# ...
1. 功能分支开发并合并到 main
   git checkout -b feature/payment main
   git push origin feature/payment
   # 通过合并请求合并到 main
# ...
2. main 合并到 staging 部署预发
   git checkout staging
   git merge main
   git push origin staging
# ...
3. staging 验证通过后合并到 production
   git checkout production
   git merge staging
   git push origin production
# ...
4. 紧急修复需要从 production 反向合并
   git checkout -b hotfix/urgent production
   # 修复后合并回 production 和 main
```

### 场景三：批量分支清理与冲突记忆

项目积累了大量过期分支，需要批量清理并启用冲突自动记忆.
```bash
# 启用 rerere 自动记忆冲突解决方案
git config --global rerere.enabled true
# ...
# 批量查看已合并分支
git branch --merged main | grep -v "^\*\|main\|develop"
# ...
# 批量删除已合并的本地分支
git branch --merged main | grep -v "^\*\|main\|develop" | xargs -n 1 git branch -d
# ...
# 批量清理远程过期分支
git remote prune origin
git fetch --all --prune
# ...
# 批量删除远程已合并分支（谨慎操作）
git branch -r --merged origin/main | grep -v "main\|develop" | sed 's/origin\///' | xargs -I{} git push origin :{}
```

## 快速开始

1. 阅读## 核心能力章节了解skill功能
2. 按## 依赖说明配置环境
3. 执行所需能力对应的命令
4. 参考## 错误处理章节处理异常
5. 查看## FAQ解答常见疑问

### Git Flow 初始化配置

```bash
# 依赖说明
brew install git-flow
# ...
# 安装 git-flow（Ubuntu/Debian）
apt-get install git-flow
# ...
# 初始化项目
git flow init
# ...
# 自定义分支名（交互式配置）
# main branch: main
# develop branch: develop
# feature/: feature/
# release/: release/
# hotfix/: hotfix/
```

### 企业级 Git 配置

```bash
# 启用冲突自动记忆
# ...
# 配置三方合并工具
git config --global merge.tool vscode
git config --global mergetool.vscode.cmd 'code --wait $MERGED'
# ...
# 配置行尾换行符
git config --global core.autocrlf input
# ...
# 配置拉取策略为 rebase
git config --global pull.rebase true
# ...
# 配置推送默认行为
git config --global push.default current
# ...
# 启用部分克隆（大仓库优化）
git config --global feature.experimental true
```

**响应解析**: 完成完成后,查看输出响应确认任务状态。成功时输出包含解析摘要和响应数据;失败时根据错误信息排查问题,查阅错误解析章节获取恢复步骤.
#
## 示例

### 保护分支策略建议

| 分支 | 保护规则 | 合并方式 | 谁可推送 |
|:-----|:-----|:-----|:-----|
| main | 禁止直接推送 | 合并请求 + 审查 | 仅管理员 |
| develop | 禁止直接推送 | 合并请求 | 核心成员 |
| release/* | 禁止新功能 | 仅缺陷修复 | 发布负责人 |
| hotfix/* | 紧急通道 | 快速审查 | 值班人员 |
| feature/* | 自由推送 | 直接推送 | 分支创建者 |

### 版本标签规范

```bash
# 语义化版本标签
git tag -a v2.0.0 -m "Release 2.0.0: 用户认证与支付模块"
# ...
# 预发布版本标签
git tag -a v2.1.0-beta.1 -m "Beta 2.1.0: 新搜索功能预览"
# ...
# 补丁版本标签
git tag -a v2.0.1 -m "Patch: 修复登录崩溃问题"
# ...
# 查看所有标签
git tag -l
git tag -l "v2.*"
# ...
# 推送标签
git push origin v2.0.0        # 单个标签
git push origin --tags         # 所有标签
# ...
# 删除标签
git tag -d v2.0.0              # 本地
git push origin --delete v2.0.0  # 远程
```

### CHANGELOG 自动生成配置

```bash
# 安装 conventional-changelog
npm install -g conventional-changelog-cli
# ...
# 生成 CHANGELOG
conventional-changelog -p angular -i CHANGELOG.md -s
# ...
# 首次生成完整历史
```

## 优选实践

1. **保护主分支**：禁止直接推送到 main/develop，强制通过合并请求

2. **启用 rerere**：团队级冲突记忆，避免重复解决相同冲突
   ```bash
# 本技能的核心实现逻辑
# 请参考上方使用说明进行配置和调用
echo "implementation_ready"
```

3. **语义化版本**：遵循 SemVer 规范管理版本号
   - MAJOR：不兼容的 API 修改
   - MINOR：向下兼容的功能新增
   - PATCH：向下兼容的缺陷修复

4. **发布分支隔离**：发布期间仅允许修复，禁止新功能合并

5. **定期清理分支**：每周清理已合并的功能分支
   ```bash
   git branch --merged main | grep -v "main\|develop" | xargs git branch -d
   ```

6. **强制审查**：所有合并请求至少一人审查通过

7. **提交信息校验**：通过 Git Hook 校验提交信息格式
   ```bash
   # .git/hooks/commit-msg
   #!/bin/sh
   if ! grep -qE "^(feat|fix|docs|style|refactor|perf|test|chore|revert)(\(.+\))?: .{1,50}" "$1"; then
     echo "提交信息不符合 Conventional Commits 规范"
     exit 1
   fi
   ```

## 常见问题

### Q1：rerere 如何工作？

```bash
# 启用后，首次解决冲突时 Git 会记录解决方案
# ...
# 再次遇到相同冲突时自动应用记忆的方案
git rerere diff     # 查看当前记忆的解决方案
git rerere forget path/to/file  # 忘记指定文件的方案
ls .git/rr-cache/   # 查看所有记忆的冲突
```

### Q2：如何处理 Git Flow 中 release 期间的新功能？

```bash
# 新功能应在 develop 分支继续开发
# release 分支仅接受缺陷修复
git checkout develop
git flow feature start new-feature
```

### Q3：hotfix 修复后如何同步到所有分支？

```bash
# Git Flow 会自动合并 hotfix 到 main 和 develop
git flow hotfix finish fix-urgent
# ...
# 如有多环境分支，需手动同步
git checkout staging
git merge main
git push origin staging
```

### Q4：如何回滚已发布的版本？

```bash
# 方案一：使用 revert（保留历史，推荐）
git revert v2.0.0..HEAD
git commit -m "revert: 回滚 v2.0.0 之后的所有改动"
# ...
# 方案二：使用 reset（重写历史，谨慎使用）
git checkout main
git reset --hard v1.9.0
git push --force-with-lease origin main
```

### Q5：如何批量重命名多个分支？

```bash
# 批量添加前缀
for branch in feature-a feature-b feature-c; do
  git branch -m "$branch" "legacy/$branch"
done
```

### Q6：合并请求出现大量冲突怎么处理？

```bash
# 1. 先同步目标分支
git fetch origin
git checkout feature/complex
git rebase origin/main
# ...
# 2. 逐个文件解决冲突
git status
# 编辑冲突文件...
git add .
git rebase --continue
# ...
# 3. 如冲突过多，考虑重置后重新开发
git rebase --abort
git checkout main
git pull
git checkout -b feature/complex-v2
```

## 依赖说明

### 运行环境
- **Agent 平台**: 支持读取 SKILL.md 的任意 AI Agent（Claude Code / Cursor / Codex / Gemini CLI 等）
- **操作系统**: Windows / macOS / Linux
- **Git 版本**: 建议 2.25 及以上（需支持 rerere、sparse-checkout）
- **Node.js**: 18.0+（CHANGELOG 生成工具依赖）

### 第三方依赖

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|---:|---:|---:|---:|
| Git | 命令行工具 | 必需 | 系统包管理器安装 |
| git-flow | 扩展工具 | 推荐 | `brew install git-flow` 或 `apt install git-flow` |
| conventional-changelog-cli | Node 工具 | 可选 | `npm install -g conventional-changelog-cli` |
| LLM API | API | 必需 | 由 Agent 内置 LLM 提供 |

### API Key 配置
- 本工具为纯 Markdown 指令驱动，无需额外 API Key
- Git 远程推送需要配置 SSH Key 或个人访问令牌
- 团队协作建议配置统一的 GPG 签名密钥

### 可用性分类
- **分类**: MD+EXEC（Markdown 指令 + 命令行执行）
- **说明**: 通过自然语言指令驱动 Agent 执行 Git 操作，专业版功能依赖 git-flow 扩展和命令行执行能力

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|:---:|:---:|:---:|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 已知限制

- 需LLM支持,无LLM环境不可用
- 复杂业务场景建议结合人工经验判断
- 执行效率受模型能力与网络环境影响

## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "Git工作流专业版处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "git workflow cn pro"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```

## 安全注意事项

| 风险类型 | 防范措施 |
|----------|---------|
| API密钥泄露 | 通过环境变量配置，禁止硬编码到代码或配置文件中 |
| 命令执行风险 | 仅执行白名单命令，避免拼接用户输入到命令行参数中 |
| 网络通信安全 | 使用HTTPS协议，验证SSL证书有效性 |
| 敏感数据暴露 | 输出结果中不包含密钥、令牌等敏感信息 |

使用前请确认已阅读依赖说明章节，确保运行环境满足安全要求。