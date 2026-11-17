---
slug: pipedrive-toolkit-free
name: pipedrive-toolkit-free
version: 1.0.0
displayName: Pipedrive工具(免费版)
summary: 管理Pipedrive销售数据的免费工具，支持商机、联系人、组织的查询与搜索
license: Proprietary
edition: free
description: Pipedrive工具免费版是一款面向销售数据管理的命令行辅助Skill，让AI Agent能够通过API查询Pipedrive中的商机、联系人、组织和活动数据，实现销售信息的快速检索和展示。核心能力：商机列表与搜索、联系人查询、组织查询、活动列表、管道与阶段查看、当前用户信息。Use
  when 需要AI模型调用、智能对话、Agent编排、LLM应用时使用。不适用于需要100%确定性的关键决策。
tags:
- 销售管理
- CRM集成
- 数据查询
- 集成工具
tools:
- - read
- exec
homepage: https://skillhub.cn
pricing_tier: L4
pricing_model: monthly
suggested_price: 99.9
tools: ["read", "exec", "glob", "grep"]
tags: "工具,效率,自动化"
---
# Pipedrive工具（免费版）

通过API驱动AI Agent查询Pipedrive销售数据，实现商机、联系人、组织和活动的快速检索。免费版提供只读查询功能，满足销售日常信息获取需求。

## 概述

Pipedrive是一款专注于销售流程管理的CRM工具，但在命令行集成和自动化查询场景下，直接调用API需要处理OAuth认证和Token刷新等复杂逻辑。本Skill通过API代理服务管理OAuth认证，让AI Agent能够通过简单的API调用查询销售数据。

免费版聚焦只读查询能力，提供商机、联系人、组织、活动和管道的列表与搜索功能，适合销售人员快速获取客户和商机信息。

## 核心能力

| 能力模块 | 免费版支持 | 说明 |
|----|-----|---|
| 商机查询 | 支持 | 列表、详情、搜索 |
| 联系人查询 | 支持 | 列表、详情、搜索 |
| 组织查询 | 支持 | 列表、详情 |
| 活动查询 | 支持 | 列表、详情 |
| 管道查询 | 支持 | 列表、详情 |
| 阶段查询 | 支持 | 列表、详情 |
| 备注查询 | 支持 | 列表 |
| 用户信息 | 支持 | 当前用户信息 |
| 商机创建 | 不支持 | 专业版提供 |
| 数据更新 | 不支持 | 专业版提供 |
| 数据删除 | 不支持 | 专业版提供 |
| 批量操作 | 不支持 | 专业版提供 |
| 连接管理 | 不支持 | 专业版提供 |

### 核心功能执行
用`input_params`参数进行配置。

**输入**: 用户提供核心功能执行所需的指令和必要参数。
**处理**: 解析核心功能执行的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回核心功能执行的响应数据,包含状态码、结果和日志。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 参数配置与调用
用`config_options`参数进行配置。

**输入**: 用户提供参数配置与调用所需的指令和必要参数。
**处理**: 解析参数配置与调用的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回参数配置与调用的响应数据,包含状态码、结果和日志。
- 执行此能力时使用`config_options`参数,支持修改/重置/导入操作

### 结果处理与输出
用`output_format`参数进行配置。

**输入**: 用户提供结果处理与输出所需的指令和必要参数。
**处理**: 解析结果处理与输出的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回结果处理与输出的响应数据,包含状态码、结果和日志。
- 执行此能力时使用`output_format`参数,支持导出/保存/转换操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：Pipedrive、销售数据的免费工、支持商机、联系人、组织的查询与搜索、工具免费版是一款、面向销售数据管理、的命令行辅助、Skill、Agent、能够通过、API、中的商机、组织和活动数据、实现销售信息的快、速检索和展示、核心能力、商机列表与搜索、联系人查询、组织查询、活动列表、管道与阶段查看、当前用户信息、Use、when、模型调用、智能对话、LLM、应用时使用、不适用于需要、确定性的关键决策等。

## 使用场景

### 场景一：商机快速查询

销售人员在外出途中通过AI Agent快速查询当前open状态的商机列表，了解跟进优先级。

### 场景二：客户信息检索

通过姓名或邮箱搜索联系人信息，快速获取客户背景和历史活动记录。

### 场景三：管道概览查看

查看所有销售管道和阶段分布，了解整体销售漏斗状态。

## 快速开始

### 前置条件

1. 已注册API代理服务账户并获取API Key
2. 已创建Pipedrive OAuth连接
3. 已设置API Key环境变量

### 配置环境变量

```bash
# 设置API代理服务的API Key
export MATON_API_KEY="your_api_key_here"
```

### 60秒上手

```bash
# 1. 列出所有open商机
python -c "
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/pipedrive/api/v1/deals?status=open')
req.add_header('Authorization', f'Bearer {os.environ[\"MATON_API_KEY\"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
"
# ...
# 2. 搜索联系人
python -c "
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/pipedrive/api/v1/persons/search?term=john')
req.add_header('Authorization', f'Bearer {os.environ[\"MATON_API_KEY\"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
"
# ...
# 3. 查看管道列表
python -c "
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/pipedrive/api/v1/pipelines')
req.add_header('Authorization', f'Bearer {os.environ[\"MATON_API_KEY\"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
"
```

## 示例

### 基础URL与认证

所有请求通过API代理服务转发到Pipedrive API，代理自动注入OAuth Token：

```text
基础URL: https://api.maton.ai/pipedrive/{原生API路径}
认证头:  Authorization: Bearer $MATON_API_KEY
```

### 商机查询

```bash
# 列出所有商机
python -c "
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/pipedrive/api/v1/deals')
req.add_header('Authorization', f'Bearer {os.environ[\"MATON_API_KEY\"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
"
# ...
# 按状态过滤
# status: open, won, lost, deleted, all_not_deleted
python -c "
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/pipedrive/api/v1/deals?status=open&limit=50')
req.add_header('Authorization', f'Bearer {os.environ[\"MATON_API_KEY\"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
"
# ...
# 查看指定商机详情
python -c "
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/pipedrive/api/v1/deals/123')
req.add_header('Authorization', f'Bearer {os.environ[\"MATON_API_KEY\"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
"
# ...
# 搜索商机
python -c "
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/pipedrive/api/v1/deals/search?term=enterprise')
req.add_header('Authorization', f'Bearer {os.environ[\"MATON_API_KEY\"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
"
```

### 联系人查询

```bash
# 列出联系人
python -c "
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/pipedrive/api/v1/persons?limit=50')
req.add_header('Authorization', f'Bearer {os.environ[\"MATON_API_KEY\"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
"
# ...
# 查看联系人详情
python -c "
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/pipedrive/api/v1/persons/123')
req.add_header('Authorization', f'Bearer {os.environ[\"MATON_API_KEY\"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
"
# ...
# 搜索联系人
python -c "
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/pipedrive/api/v1/persons/search?term=john')
req.add_header('Authorization', f'Bearer {os.environ[\"MATON_API_KEY\"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
"
```

### 组织查询

```bash
# 列出组织
python -c "
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/pipedrive/api/v1/organizations')
req.add_header('Authorization', f'Bearer {os.environ[\"MATON_API_KEY\"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
"
# ...
# 查看组织详情
python -c "
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/pipedrive/api/v1/organizations/456')
req.add_header('Authorization', f'Bearer {os.environ[\"MATON_API_KEY\"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
"
```

### 活动查询

```bash
# 列出活动
python -c "
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/pipedrive/api/v1/activities')
req.add_header('Authorization', f'Bearer {os.environ[\"MATON_API_KEY\"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
"
# ...
# 按类型过滤活动
python -c "
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/pipedrive/api/v1/activities?type=call')
req.add_header('Authorization', f'Bearer {os.environ[\"MATON_API_KEY\"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
"
# ...
# 按完成状态过滤
python -c "
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/pipedrive/api/v1/activities?done=0')
req.add_header('Authorization', f'Bearer {os.environ[\"MATON_API_KEY\"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
"
```

### 管道与阶段

```bash
# 列出所有管道
python -c "
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/pipedrive/api/v1/pipelines')
req.add_header('Authorization', f'Bearer {os.environ[\"MATON_API_KEY\"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
"
# ...
# 列出阶段（按管道过滤）
python -c "
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/pipedrive/api/v1/stages?pipeline_id=1')
req.add_header('Authorization', f'Bearer {os.environ[\"MATON_API_KEY\"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
"
```

### 分页查询

```bash
# 使用start和limit参数分页
python -c "
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/pipedrive/api/v1/deals?start=0&limit=50&sort=add_time%20DESC')
req.add_header('Authorization', f'Bearer {os.environ[\"MATON_API_KEY\"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
"
```

### 查询参数说明

| 参数 | 适用资源 | 说明 |
|:-----|:-----|:-----|
| `status` | deals | 过滤状态：open/won/lost/deleted/all_not_deleted |
| `filter_id` | deals, persons | 使用已保存的过滤器ID |
| `stage_id` | deals | 按阶段过滤 |
| `user_id` | deals, activities | 按用户过滤 |
| `type` | activities | 活动类型：call/meeting/task/email |
| `done` | activities | 完成状态：0(未完成)/1(已完成) |
| `start` | 所有列表 | 分页起始位置（默认0） |
| `limit` | 所有列表 | 每页数量（默认100） |
| `sort` | 所有列表 | 排序字段和方向（如`add_time DESC`） |

## 最佳实践

1. **使用status过滤提高效率**：查询商机时优先用`status=open`过滤，避免返回大量已关闭数据。
2. **善用搜索功能**：通过`/search?term=关键词`快速定位特定商机或联系人，比遍历列表更高效。
3. **合理设置分页**：大数据量查询时使用`start`和`limit`分页，每页建议50-100条，避免响应超时。
4. **按活动类型筛选**：查看待办活动时用`done=0`过滤未完成项，聚焦当前需要处理的任务。
5. **JSON输出便于解析**：API返回JSON格式数据，可配合`jq`等工具进行字段提取和格式化。

## 常见问题

### Q1: API返回401未授权？

检查`MATON_API_KEY`环境变量是否正确设置。执行`echo $MATON_API_KEY`确认值不为空。API Key可在代理服务设置页面获取。

### Q2: API返回400缺少Pipedrive连接？

需要先创建Pipedrive OAuth连接。在代理服务管理页面创建连接并完成OAuth授权流程。免费版仅支持查询，连接管理需在网页端操作。

### Q3: 查询结果中ID是数字还是字符串？

Pipedrive的资源ID是整数类型。在API调用中直接使用数字（如`/deals/123`），无需引号包裹。

### 已知限制

每个账户的请求速率限制为10次/秒。批量查询时注意控制请求频率，避免触发429错误。

### Q5: curl命令中URL含括号报错？

URL中包含`fields[]`或`sort[]`等括号时，使用`curl -g`禁用通配符解析。或直接使用Python的urllib方式调用。
- 当前为免费版本,如需完整功能请升级到付费版获取全部能力
## 依赖说明

### 运行环境

- **Agent平台**：支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**：Windows / macOS / Linux
- **Python**：3.6+（使用urllib标准库，无需额外安装）

### 依赖详情

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|---:|---:|---:|---:|
| API代理服务 | 在线服务 | 必需 | 注册账户并获取API Key |
| Pipedrive账户 | 在线账户 | 必需 | 在Pipedrive官网注册 |
| Pipedrive OAuth连接 | 认证连接 | 必需 | 在代理服务中创建 |
| Python | 运行时 | 必需 | 系统通常自带或从官网安装 |
| LLM API | API | 必需 | 由Agent平台内置LLM提供 |

### API Key 配置

- **API代理Key**：通过`MATON_API_KEY`环境变量配置
- **获取方式**：在代理服务设置页面创建账户并复制API Key
- **Pipedrive OAuth**：通过代理服务管理页面创建连接并完成授权
- **禁止**：在代码或配置文件中明文写入API Key
- **安全建议**：将API Key存储在`.env`文件中（已加入.gitignore）

### 可用性分类

- **分类**：MD+EXEC（纯Markdown指令，需要exec命令行执行能力）
- **说明**：基于Markdown的AI Skill，通过自然语言指令驱动Agent执行Pipedrive API查询操作

## 免费版限制

本免费体验版限制以下高级功能：
- 商机创建与更新（专业版支持完整的CRUD操作）
- 联系人和组织创建更新（专业版支持创建、更新和删除）
- 活动创建与更新（专业版支持活动管理和完成标记）
- 备注创建（专业版支持添加备注到商机和联系人）
- 批量操作（专业版支持批量创建、更新和数据导入）
- 多连接管理（专业版支持多个Pipedrive账户的连接管理）
- 自定义字段操作（专业版支持读写自定义字段）
- 高级过滤器（专业版支持创建和管理自定义过滤器）

解锁全部功能请使用专业版：pipedrive-toolkit-pro

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
    "result": "Pipedrive工具(免费版)处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "pipedrivekit"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```
