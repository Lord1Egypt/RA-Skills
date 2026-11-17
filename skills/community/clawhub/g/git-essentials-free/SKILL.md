---
slug: "git-essentials-free"
name: "git-essentials-free"
version: 1.0.1
displayName: "Git基础版"
summary: "Git 版本控制基础能,提供核心能力"
summary_zh: "Git 版本控制基础能,提供核心能力"
license: "MIT"
description: "|- Git 版本控制基础能力，覆盖常用命令、分支管控与团队协作工作流. 核心能力:.该技能适用于相关开发场景,包含结构化的工作流程和配置指引.经过深度差异化处置,针对用户反馈和使用痛点进行了改进,提升了实用性和可操作性.该技能适用于相关开发场景,包含结构化的工作流程和配置指引.经过深度差异化处置,针对用户反馈和使用痛点进行了改进,提升了实用性和可操作性."

  - 常用 Git 命令的规范使用与问题排查

  - 基础分支管理（创建、切换、合并、删除）

  - 提交规范与冲突基础处理

  适用场景:

  - 日常代码提交、分支切换、历史查询

  - 独立开发者与小型团队的版本管理

  - 自动化工作流中的 Git 操作

  差异化:基础版聚焦 Git 核心命令与协作流程，去除了高级版的复杂合并策略、Rebase 交互式重写与二分查找等进阶能力.
tags:
  - Development
  - 版本控制
  - Git
  - 开发工具
  - commit
  - login
  - agent
tools:
  - read
  - write
  - exec
homepage: ""
category: "Development"
pricing_tier: free
---
# Git 基础版

## 核心能力

- 常用 Git 命令规范：add、commit、status、log、diff、show 等基础命令的标准用法与常见参数
- 基础分支管理：branch、checkout、switch、merge 的规范使用，支持创建、切换、合并、删除分支
- 提交规范指导：依据 Conventional Commits 规范生成提交信息，支持 feat、fix、docs、refactor、test、chore 等类型
- 冲突基础处理：识别合并冲突文件，提供基础解决思路与标记位置说明
- 远程仓库基础操作：clone、fetch、pull、push 的基础用法与常见错误识别
#
## 快速开始

1. 确认运行环境满足依赖说明中的要求
2. 在AI Agent对话中调用本技能,提供必要的输入参数
3. 检查输出结果,根据需要进行后续处理

> 详细的输入输出格式请参考下方章节说明。

## 适用场景

| 场景 | 输入 | 输出 |
|---|---|---|
| 提交代码 | 暂存区与变更说明 | 规范化的 commit 命令与提交信息 |
| 分支管理 | 分支名与目标操作 | 对应的 branch/checkout/merge 命令序列 |
| 历史查询 | 查询条件 | git log 或 git show 命令与输出解读 |
| 冲突解决 | 冲突文件路径 | 冲突标记说明与基础解决建议 |
| 远程同步 | 远程仓库名与操作 | fetch/pull/push 命令与结果说明 |

**不适用于**：复杂多分支策略（如 Git Flow 全流程）、交互式 Rebase 历史重写、二分查找定位缺陷、大规模仓库重构等场景（请使用高级版）

## 使用流程

1. 确认当前工作目录处于 Git 仓库中，且 Git 已正确安装
2. 识别用户意图，选择对应的命令类别（提交、分支、历史、冲突、远程）
3. 根据输入参数生成规范命令，必要时附带参数说明
4. 执行命令并捕获输出，对常见错误进行识别与提示
5. 若发生冲突或错误，按异常处理章节的指引操作

## 输入格式

| 参数名 | 类型 | 必填 | 说明 |
|:-----|:-----|:-----|:-----|
| action | string | 是 | 操作类型，可选: commit/branch/log/merge/conflict/remote |
| files | array | 否 | 涉及的文件列表，默认: 全部已暂存文件 |
| message | string | 否 | 提交信息或分支名，commit 操作时建议提供 |
| scope | string | 否 | 审查范围，可选: staged/unstaged/all，默认: staged |

## 输出格式

```json
{
  "success": true,
  "data": {
    "overall_status": "ok",
    "branch": "feature/login",
    "commands": [
      {
        "cmd": "git add src/login.js",
        "exit_code": 0,
        "output": ""
      },
      {
        "cmd": "git commit -m \"feat(login): 修复登录重定向问题\"",
        "exit_code": 0,
        "output": "[feature/login 8a3f2c1] feat(login): 修复登录重定向问题"
      }
    ],
    "summary": "已提交 1 个变更到 feature/login 分支",
    "warnings": []
  },
  "error": null
}
```

## 异常处理

| 错误场景 | 原因 | 处理方式 |
|---:|---:|---:|
| 不是 Git 仓库 | 当前目录未初始化 | 提示执行 git init 或切换到仓库根目录 |
| 提交信息缺失 | 未提供 message 参数 | 建议按 Conventional Commits 规范补充提交信息 |
| 合并冲突 | 分支合并时存在同一文件的不同修改 | 列出冲突文件，标注 <<<<<<< 与 ======= 位置，建议手动解决后 git add |
| 远程拒绝推送 | 远程分支已有新提交 | 建议先执行 git pull --rebase 再推送 |
| 凭证错误 | 未配置 SSH Key 或 Token | 提示检查远程仓库凭证配置 |

## 依赖说明

### 运行环境
- **Agent平台**: 支持SKILL.md规范的任意AI Agent
- **操作系统**: Windows / macOS / Linux
- **Git 版本**: 建议 2.20 及以上

### 依赖项
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:---:|:---:|:---:|:---:|
| Git CLI | 命令行工具 | 必需 | 系统包管理器安装 |
| LLM API | API | 必需 | 由Agent内置LLM提供 |

### API Key 配置
- 本Skill基于指令驱动，无需额外API Key

### 可用性分类
- **分类**: MD+EXEC（）
- **说明**: 基于Markdown的AI Skill，通过自然语言指令驱动Agent执行Git命令

## 案例展示

### 示例1：规范化提交变更

```
输入: action=commit, files=["src/api.js"], message="修复接口超时问题"
处理: git add src/api.js -> 生成 Conventional Commits 信息 -> git commit
输出: 提交成功，分支为 feature/api，commit hash 为 8a3f2c1
```

### 示例2：切换并合并分支

```
输入: action=branch, 目标=合并 feature/login 到 main
处理: git checkout main -> git pull -> git merge feature/login
输出: 合并成功，无冲突；若存在冲突则列出冲突文件
```

## 常见问题

### Q1: 如何开始使用 Git 基础版？
A: 请先确认 Git 已安装并在 PATH 中可用，然后按"输入格式"提供 action 与相关参数即可.
### Q2: 遇到合并冲突怎么办？
A: 基础版会列出冲突文件并标注冲突位置，需要手动解决后执行 git add 与 git commit。如需自动化的冲突解决建议，可升级至高级版.
### Q3: Git 基础版支持 Rebase 吗？
A: 基础版仅支持基础的 merge 操作，不包含交互式 Rebase、历史重写、cherry-pick 等进阶能力.
### Q4: 如何获取交互式 Rebase、二分查找、复杂合并策略等高级能力？
A: 这些属于高级版能力。基础版聚焦日常提交与协作，如需进阶的分支策略与历史管理能力，请升级至高级版.
## 错误处理

| 错误场景(续)| 原因 | 处理方式 |
|:---------|---------:|:---------|
| LLM响应超时或无响应 | 网络延迟或模型负载过高 | 检查网络连接和配置后重试；确认Agent平台LLM服务正常 |
| 输入内容格式不正确 | 用户输入不符合skill预期格式 | 检查输入是否符合skill使用说明中的格式要求，参考示例章节 |
| 执行结果与预期不符 | 指令描述不够明确或上下文不足 | 提供更详细的指令描述，补充必要的上下文信息 |
| 命令执行失败 | 运行环境不满足要求或权限不足 | 确认运行环境符合依赖说明中的要求；检查命令权限设置 |

## 已知限制

- 不支持交互式 Rebase 与历史重写（如修改历史提交信息、压缩提交）
- 不支持二分查找（git bisect）定位缺陷引入点
- 不支持复杂合并策略（如 octopus、ours、theirs 等策略选项）
- 不支持 Git LFS、子模块的深度管理
- 不支持 Git Hook 的自动生成与调试
- 冲突解决仅提供位置标注，不提供自动合并建议
