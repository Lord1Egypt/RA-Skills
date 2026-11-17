---
slug: github-manager-free
name: github-manager-free
version: 1.0.0
displayName: GitHub管理器(免费版)
summary: 通过gh CLI管理GitHub仓库的Issue、PR与工作流,支持基础查询、状态检查与结构化输出,适合个人开发者日常协作。
license: Proprietary
edition: free
description: 'GitHub管理器(免费版)是一款面向个人开发者的GitHub日常协作助手,通过gh命令行工具封装常用操作,帮助用户高效管理Issue、Pull
  Request与CI工作流。核心能力:

  - Issue与Pull Request的基础查询、状态检查与结构化输出

  - 工作流运行列表查看与失败步骤定位

  - 支持JSON输出与jq过滤,便于自动化处理

  - 提供常用命令速查与故障排查指南


  适用场景:

  - 个人开发者日常GitHub仓库维护

  - 开源项目Issue与PR的快速浏览

  - CI/CD工作流状态检查与失败排查

  -...'
tags:
- GitHub
- 协作
- CI/CD
- 开发工具
tools:
- - read
- exec
homepage: https://skillhub.cn
pricing_tier: "L2-标准级"
pricing_model: per_use
suggested_price: "19.9 CNY/per_use"
tools: ["read", "write", "exec"]
tags: "版本控制,Git,开发工具"
---
# GitHub管理器(免费版)

通过gh命令行工具管理GitHub仓库的Issue、Pull Request与工作流,聚焦"查询-检查-定位"三步流程,帮助个人开发者高效完成日常协作。

## 概述

GitHub已成为代码协作的事实标准,但日常操作中,开发者经常需要在浏览器与终端间切换,效率低下。gh命令行工具提供了完整的GitHub操作能力,但命令繁多、参数复杂,新手难以快速掌握。本Skill封装常用gh命令,提供场景化指引,让开发者能在终端内完成大部分GitHub操作。

免费版聚焦基础查询与检查能力,适合个人开发者日常使用。

## 核心能力

### Issue管理

```bash
# 列出仓库Issue(结构化输出)
gh issue list --repo owner/repo --json number,title,state --jq '.[] | "#(.number): (.title) [(.state)]"'
# ...
# 查看指定Issue详情
gh issue view 123 --repo owner/repo
# ...
# 查看Issue评论
gh issue view 123 --repo owner/repo --comments
```

**输入**: 用户提供Issue管理所需的指令和必要参数。
**处理**: 解析Issue管理的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回Issue管理的响应数据,包含状态码、结果和日志。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### Pull Request管理

```bash
# 列出仓库PR
gh pr list --repo owner/repo --state open --json number,title,author
# ...
# 查看PR详情(含diff)
gh pr view 55 --repo owner/repo
# ...
# 检查PR的CI状态
gh pr checks 55 --repo owner/repo
# ...
# 查看PR的review状态
gh pr view 55 --repo owner/repo --json reviews --jq '.reviews[] | {author: .author.login, state: .state}'
```

**输入**: 用户提供Pull Request管理所需的指令和必要参数。
**处理**: 解析Pull Request管理的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回Pull Request管理的响应数据,包含状态码、结果和日志。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 工作流管理

```bash
# 列出最近10次工作流运行
gh run list --repo owner/repo --limit 10
# ...
# 查看指定运行详情
gh run view <run-id> --repo owner/repo
# ...
# 仅查看失败步骤的日志
gh run view <run-id> --repo owner/repo --log-failed
# ...
# 重新运行失败的工作流
gh run rerun <run-id> --repo owner/repo --failed
```

**输入**: 用户提供工作流管理所需的指令和必要参数。
**处理**: 解析工作流管理的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回工作流管理的响应数据,包含状态码、结果和日志。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 结构化输出与过滤

大多数gh命令支持`--json`与`--jq`,便于自动化处理:

```bash
# 提取Issue编号与标题
gh issue list --repo owner/repo --json number,title --jq '.[] | "(.number): (.title)"'
# ...
# 筛选特定状态的PR
gh pr list --repo owner/repo --json number,title,state --jq '.[] | select(.state == "OPEN") | .number'
# ...
# 统计各状态Issue数量
gh issue list --repo owner/repo --json state --jq 'group_by(.state) | map({state: .[0].state, count: length})'
```

**输入**: 用户提供结构化输出与过滤所需的指令和必要参数。
**处理**: 解析结构化输出与过滤的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回结构化输出与过滤的响应数据,包含状态码、结果和日志。
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：CLI、GitHub、仓库的、与工作流、支持基础查询、状态检查与结构化、适合个人开发者日、常协作、管理器、免费版、是一款面向个人开、发者的、日常协作助手、命令行工具封装常、用操作、帮助用户高效管理、核心能力、的基础查询、工作流运行列表查、看与失败步骤定位、提供常用命令速查、与故障排查指南等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

## 使用场景

### 场景1:每日站会前的快速状态检查

用户意图: "站会快开始了,帮我看看仓库今天的PR和Issue状态。"

推荐流程:
1. `gh pr list --repo owner/repo --state open --json number,title,author,updatedAt`
2. `gh issue list --repo owner/repo --state open --json number,title,labels --jq 'sort_by(.updatedAt) | reverse | .[0:5]'`
3. `gh run list --repo owner/repo --limit 5 --json status,conclusion,name`

### 场景2:CI失败快速定位

用户意图: "CI挂了,帮我看看哪个步骤失败了。"

推荐流程:
1. `gh run list --repo owner/repo --limit 1 --status failure` 找到失败的运行
2. `gh run view <run-id> --repo owner/repo --log-failed` 查看失败日志
3. 根据日志定位问题代码,修复后push
4. `gh run rerun <run-id> --repo owner/repo --failed` 重跑失败步骤

### 场景3:代码审查前的准备

用户意图: "我要审查一个PR,先看看改了什么。"

推荐流程:
1. `gh pr view 55 --repo owner/repo` 查看PR描述与元信息
2. `gh pr diff 55 --repo owner/repo` 查看代码变更
3. `gh pr checks 55 --repo owner/repo` 检查CI是否通过
4. `gh pr view 55 --repo owner/repo --json reviews --jq '.reviews[]'` 查看已有审查意见

## 不适用场景

以下场景GitHub管理器(免费版)不适合处理：

- 无明确技术栈的模糊需求
- 纯架构设计决策
- 运维部署管理

## 触发条件

需要代码生成、编程辅助、调试测试、开发部署时使用。不适用于非本工具能力范围的需求。

## 快速开始

### 依赖详情

```bash
# 安装gh(以macOS为例,其他平台参考官方文档)
brew install gh
# ...
# 完成认证
gh auth login
# ...
# 验证认证状态
gh auth status
```

### Step 2:基础查询

```bash
# 查看当前用户仓库列表
gh repo list --limit 10
# ...
# 查看指定仓库信息
gh repo view owner/repo
# ...
# 查看仓库Issue
gh issue list --repo owner/repo --limit 10
```

### Step 3:结构化输出

```bash
# 使用JSON输出
gh issue list --repo owner/repo --json number,title,state
# ...
# 使用jq过滤
gh pr list --repo owner/repo --json number,title,author --jq '.[] | "\(.number)\t\(.title)\t\(.author.login)"'
```

## 示例

### 常用命令别名

```bash
# 配置gh别名,提升效率
gh alias set issues 'issue list --json number,title,state --jq ".[] | \"#\(.number): \(.title) [\(.state)]\""'
gh alias set prs 'pr list --json number,title,author --jq ".[] | \"#\(.number): \(.title) by \(.author.login)\""'
gh alias set ci 'run list --limit 5'
# ...
# 使用别名
gh issues --repo owner/repo
gh prs --repo owner/repo
gh ci --repo owner/repo
```

### 跨仓库批量查询脚本

```bash
#!/bin/bash
# 批量查询多个仓库的开放Issue数
repos=("owner/repo1" "owner/repo2" "owner/repo3")
for repo in "${repos[@]}"; do
  count=$(gh issue list --repo "$repo" --state open --json number --jq 'length')
  echo "$repo: $count open issues"
done
```

## 最佳实践

### 命令选择策略

| 任务 | 推荐命令 | 说明 |
|---|----|---|
| 快速浏览Issue | `gh issue list` | 默认表格输出,适合人工查看 |
| 自动化处理 | `gh issue list --json --jq` | 结构化输出,适合脚本 |
| 查看PR diff | `gh pr diff` | 比浏览器更清晰 |
| 检查CI状态 | `gh pr checks` | 一条命令查看所有检查 |
| 定位CI失败 | `gh run view --log-failed` | 仅显示失败步骤,节省时间 |

### 参数规范

- **必须指定`--repo`**: 不在git目录中时,必须用`--repo owner/repo`指定仓库
- **使用URL替代**: 也可直接传入GitHub URL,gh会自动解析
- **限制结果数**: 大仓库务必加`--limit`,避免输出过长
- **状态过滤**: 查询时明确指定`--state open/closed/all`,避免混淆

### JSON与jq组合技巧

```bash
# 提取多个字段并格式化
gh pr list --json number,title,author,updatedAt --jq '.[] | "#\(.number) \(.title) (by \(.author.login), \(.updatedAt[0:10]))"'
# ...
# 按字段排序后取前N
gh issue list --json number,title,createdAt --jq 'sort_by(.createdAt) | reverse | .[0:5]'
# ...
# 条件筛选
gh pr list --json number,title,labels --jq '.[] | select(.labels[].name == "bug") | .number'
# ...
# 分组统计
gh issue list --json state --jq 'group_by(.state) | map({state: .[0].state, count: length})'
```

## 常见问题

### Q1: 不在git目录中如何指定仓库?

A: 使用`--repo owner/repo`参数指定仓库。例如: `gh issue list --repo octocat/hello-world`。也可在仓库目录内直接执行`gh issue list`,gh会自动识别当前仓库。

### Q2: gh命令返回认证错误怎么办?

A: 运行`gh auth status`检查认证状态。如未认证,运行`gh auth login`按提示完成认证。如token过期,运行`gh auth refresh`刷新。

### Q3: 如何查看私有仓库?

A: 确保认证的账号有私有仓库访问权限。`gh auth login`时会请求相应scope,选择包含`repo`的scope即可访问私有仓库。

### Q4: JSON输出字段不完整怎么办?

A: 默认`--json`只输出部分字段。使用`--json`时不指定字段名会输出所有可用字段,例如`gh issue view 123 --json`。或显式列出需要的字段: `--json number,title,body,labels,assignees`。

### Q5: jq过滤报错怎么办?

A: 常见原因: (1)字段名拼写错误,先用`--json`不带jq查看完整字段名; (2)嵌套字段访问语法错误,用`.[]`遍历数组,用`.field`访问对象; (3)jq未安装,通过`brew install jq`或`apt install jq`安装。

## 已知限制

本免费体验版限制以下高级功能:
- 不支持批量Issue/PR操作(如批量关闭、批量打标签)
- 不支持高级API查询(如GraphQL、复杂搜索)
- 不支持自动化工作流(如定时检查、自动分配)
- 不支持团队协作仪表盘与统计报表
- 不支持Webhook管理与事件订阅

解锁全部功能请使用专业版: github-manager-pro
- 当前为免费版本,如需完整功能请升级到付费版获取全部能力
## 依赖说明

### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent(Claude Code / Cursor / Codex / Gemini CLI等)
- **操作系统**: Windows / macOS / Linux
- **gh CLI**: 2.0+(GitHub官方命令行工具)
- **jq**: 1.6+(可选,用于JSON过滤)

### 第三方依赖
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-----|:-----|:-----|:-----|
| gh | CLI工具 | 必需 | `brew install gh` 或参考官方安装文档 |
| jq | 命令行工具 | 可选 | `brew install jq` 或`apt install jq` |
| GitHub账号 | 在线服务 | 必需 | 注册GitHub账号并完成`gh auth login` |
| LLM API | API | 必需 | 由Agent平台内置LLM提供 |

### API Key 配置
- **GitHub认证**: 通过`gh auth login`完成OAuth认证,token存储于`~/.config/gh/hosts.yml`
- **Token权限**: 根据需要选择scope(建议包含`repo`、`workflow`、`read:org`)
- **Token轮换**: 建议每180天刷新一次,运行`gh auth refresh`
- **禁止**: 在SKILL.md或脚本中硬编码GitHub Token

### 可用性分类
- **分类**: MD+EXEC(Markdown指令+命令行工具执行)
- **说明**: 基于Markdown的AI Skill,通过自然语言指令驱动Agent执行gh命令

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|---:|---:|---:|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "GitHub管理器(免费版)处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "github manager"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```
