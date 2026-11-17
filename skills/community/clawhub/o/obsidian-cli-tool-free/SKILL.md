---
slug: obsidian-cli-tool-free
name: obsidian-cli-tool-free
version: 1.0.0
displayName: Obsidian CLI(免费版)
summary: "通过命令行管理Obsidian笔记库的免费工具，支持文件操作、搜索、标签与日常笔记。Obsidian CLI工具免费版是一款面向个人知识管理场景的命令行辅助Skill，让AI Agent能够"
license: Proprietary
edition: free
description: Obsidian CLI工具免费版是一款面向个人知识管理场景的命令行辅助Skill，让AI Agent能够直接通过命令行操作Obsidian笔记库，实现笔记的创建、读取、搜索和基础管理。核心能力：文件读写与列表、全文搜索与标签查询、Daily
  Notes日常笔记、基础任务管理、属性读写。Use when 需要项目管理、任务规划、进度跟踪、团队协作时使用。不适用于实际人员绩效评估.
tags:
  - 笔记管理
  - 命令行工具
  - 知识库
  - 集成工具
  - 工具
  - 效率
  - 自动化
  - 知识
  - 文档
  - 写作
  - 电商
  - 研究
  - obsidian
  - file
  - daily
  - bash
  - agent
tools:
  - read
  - exec
  - glob
  - grep
homepage: ""
category: "Automation"
---
# Obsidian CLI工具（免费版）

通过命令行驱动AI Agent操作Obsidian笔记库，实现笔记的自动化创建、检索与整理。免费版提供核心文件操作、搜索和日常笔记功能，满足个人知识管理的基础需求.
## 概述

Obsidian是一款流行的本地优先知识管理工具，但其图形界面操作在面对批量笔记处理、自动化整理和跨工具集成时效率较低。本Skill封装了Obsidian命令行接口，让AI Agent能够通过自然语言指令直接操作笔记库，将重复性的知识整理工作自动化.
免费版覆盖以下核心场景：笔记的创建与编辑、全文检索、标签与属性管理、Daily Notes日常笔记、基础任务跟踪.
## 核心能力

| 能力模块 | 免费版支持 | 说明 |
|----|-----|---|
| 文件读写 | 支持 | 创建、读取、追加、列表文件 |
| 全文搜索 | 支持 | 关键词搜索、路径过滤、结果格式化 |
| 标签管理 | 支持 | 查看标签、按频率排序 |
| 属性读写 | 支持 | 读取和设置Frontmatter属性 |
| Daily Notes | 支持 | 打开、读取、追加日常笔记 |
| 任务管理 | 基础 | 列出和切换任务状态 |
| 模板管理 | 不支持 | 专业版提供 |
| 插件管理 | 不支持 | 专业版提供 |
| 文件历史 | 不支持 | 专业版提供 |
| 开发者工具 | 不支持 | 专业版提供 |

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
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：通过命令行管理、Obsidian、笔记库的免费工具、支持文件操作、标签与日常笔记、CLI、工具免费版是一款、面向个人知识管理、场景的命令行辅助、Skill、Agent、能够直接通过命令、行操作、笔记库、实现笔记的创建、搜索和基础管理、核心能力、文件读写与列表、全文搜索与标签查、Daily、Notes、日常笔记、基础任务管理、属性读写、Use、when、需要项目管理、任务规划、进度跟踪、团队协作时使用、不适用于实际人员、绩效评估等.
## 使用场景

### 场景一：快速检索笔记

在拥有数百篇笔记的库中，通过命令行快速定位包含特定关键词的笔记，无需手动翻阅.
### 场景二：自动化日常笔记

每天自动创建Daily Note并追加待办事项，建立稳定的日志习惯.
### 场景三：知识库结构巡检

定期检查孤立笔记（无反向链接）、断链（未解析的链接），保持知识库健康度.
## 快速开始

### 前置条件

1. Obsidian 1.12及以上版本，需Catalyst许可证
2. 在Obsidian中开启：设置 → 通用 → 命令行接口 → 启用
3. 按提示注册`obsidian`命令后重启终端
4. Obsidian应用必须处于运行状态

### 依赖详情

```bash
obsidian version
```

### 60秒上手

```bash
# 1. 查看当前活动文件信息
obsidian file
# ...
# 2. 列出所有文件
obsidian files
# ...
# 3. 创建一篇新笔记
obsidian create name="我的第一篇笔记" content="# 标题 正文内容"
# ...
# 4. 搜索包含关键词的笔记
obsidian search query="会议记录"
# ...
# 5. 读取指定笔记内容
obsidian read file="我的第一篇笔记"
```

**响应解析**: 完成完成后,查看输出响应确认任务状态。成功时输出包含解析摘要和响应数据;失败时根据错误信息排查问题,查阅错误解析章节获取恢复步骤.
## 示例

### 命令结构

```bash
obsidian <命令> [参数名=参数值] [标志]
```

- 参数格式：`name=value`（含空格的值需用引号包裹）
- 标志：布尔开关，添加即启用
- 多行内容：使用`\n`表示换行
- 复制输出：添加`--copy`将结果复制到剪贴板

### 文件定位方式

| 方式 | 格式 | 说明 |
|:-----|:-----|:-----|
| 按名称 | `file=笔记名` | 通过Wikilink解析，按名称匹配 |
| 按路径 | `path="文件夹/笔记.md"` | 从库根目录开始的精确路径 |

### 常用文件操作

```bash
# 列出文件并按文件夹过滤
obsidian files folder="项目/"
# ...
# 列出所有文件夹
obsidian folders
# ...
# 打开指定文件
obsidian open file="会议纪要"
# ...
# 追加内容到已有笔记
obsidian append file="日志" content="\n- 新追加的条目"
# ...
# 在Frontmatter后插入内容
obsidian prepend file="日志" content="## 上午事项"
```

### 搜索与标签

```bash
# 全文搜索并显示上下文
obsidian search query="项目架构" matches
# ...
# 按路径范围搜索
obsidian search query="项目" path="项目/"
# ...
# 限定返回数量并区分大小写
obsidian search query="API" limit=10 case
# ...
# 以JSON格式输出搜索结果
obsidian search query="报告" format=json
# ...
# 查看当前文件标签
obsidian tags
# ...
# 查看全库所有标签并按频率排序
obsidian tags all counts sort=count
```

### 属性管理

```bash
# 读取笔记属性
obsidian properties file="项目计划"
# ...
# 读取单个属性
obsidian property:read name=status file="项目计划"
# ...
# 设置属性值
obsidian property:set name=status value=进行中 file="项目计划"
# ...
# 设置列表类型属性
obsidian property:set name=tags value="a,b,c" type=list file="项目计划"
# ...
# 移除属性
obsidian property:remove name=draft file="项目计划"
```

### Daily Notes

```bash
# 打开今日笔记
obsidian daily
# ...
# 读取今日笔记内容
obsidian daily:read
# ...
# 追加待办事项到今日笔记
obsidian daily:append content="- [ ] 完成周报"
```

### 基础任务管理

```bash
# 列出当前文件的待办事项
obsidian tasks
# ...
# 列出全库所有待办事项
obsidian tasks all
# ...
# 仅显示未完成的任务
obsidian tasks all todo
# ...
# 切换任务完成状态
obsidian task ref="日志.md:8" toggle
# ...
# 标记任务为已完成
obsidian task file="日志" line=8 done
```

## 最佳实践

1. **批量创建笔记时使用模板参数**：通过`content`参数预设内容结构，保持笔记格式一致性.
2. **搜索时善用路径过滤**：大型库中先用`folder`缩小范围，再执行关键词搜索，显著提升检索速度.
3. **Daily Note自动化**：将`obsidian daily:append`命令集成到每日启动脚本，自动追加固定待办模板.
4. **属性批量管理**：通过命令行循环执行`property:set`，批量更新多篇笔记的属性，避免逐篇手动编辑.
5. **JSON格式输出用于集成**：搜索时使用`format=json`输出结构化数据，便于与其他工具或脚本对接.
## 已知限制

- 本skill的能力范围受限于核心能力章节中定义的功能,不支持超出范围的操作
- 复杂业务场景建议结合人工经验判断
- 执行效率受模型能力与网络环境影响
- 当前为免费版本,如需完整功能请升级到付费版获取全部能力
## 常见问题

### Q1: 执行命令报"command not found"怎么办？

确保已按前置条件在Obsidian设置中启用命令行接口，并重启终端使PATH生效。macOS用户检查`~/.zprofile`是否包含Obsidian路径.
### Q2: 命令执行后没有反应？

Obsidian应用必须处于运行状态，CLI通过内部API与应用通信。请先启动Obsidian再执行命令.
### Q3: 搜索结果太多如何筛选？

使用`limit`参数限制返回数量，配合`path`参数按文件夹过滤，或使用`case`标志区分大小写以精确匹配.
### Q4: 如何在多Vault环境下指定操作的库？

通过`vault`参数指定：`obsidian vault="我的笔记库" <命令>`，含空格的名称需用引号包裹.
### Q5: 追加内容时换行不生效？

在命令行中使用`\n`表示换行，确保引号正确包裹整个内容字符串。例如：`content="第一行\n第二行"`.
## 依赖说明

### 运行环境

- **Agent平台**：支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**：Windows / macOS / Linux
- **Obsidian版本**：1.12及以上，需Catalyst许可证

### 第三方依赖

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|---:|---:|---:|---:|
| Obsidian应用 | 桌面应用 | 必需 | 从Obsidian官网下载安装 |
| obsidian CLI | 命令行工具 | 必需 | 在Obsidian设置中启用命令行接口 |
| LLM API | API | 必需 | 由Agent平台内置LLM提供 |

### API Key 配置

- 本Skill基于Obsidian本地命令行接口，无需额外API Key
- Obsidian Sync功能（专业版）需要Obsidian Sync订阅

### 可用性分类

- **分类**：MD+EXEC（纯Markdown指令，需要exec命令行执行能力）
- **说明**：基于Markdown的AI Skill，通过自然语言指令驱动Agent执行Obsidian命令行操作

## 免费版限制

本免费体验版限制以下高级功能：
- 模板管理与批量插入（专业版支持模板列表、读取和插入）
- 插件与主题管理（专业版支持安装、启用、禁用、卸载插件）
- 文件历史与版本对比（专业版支持版本回溯和diff比较）
- Obsidian Sync操作（专业版支持同步状态、历史恢复）
- 开发者工具（专业版支持控制台、错误查看、DOM检查、截图）
- 工作区管理（专业版支持保存和加载工作区布局）
- TUI交互模式（专业版支持带自动补全的终端交互界面）

解锁全部功能请使用专业版：obsidian-cli-tool-pro

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|:---:|:---:|:---:|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "Obsidian CLI(免费版)处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "obsidian cli"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```
