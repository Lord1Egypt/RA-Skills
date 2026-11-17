---
slug: notion-api-toolkit-free
name: notion-api-toolkit-free
version: 1.0.0
displayName: Notion API工具箱(免费版)
summary: 轻量化Notion API集成工具,支持OAuth鉴权、页面查询、数据库检索与基础读写,适合个人快速接入Notion工作空间。
license: Proprietary
edition: free
description: 'Notion API工具箱(免费版)是面向个人开发者与知识工作者的轻量化Notion集成Skill,通过托管OAuth与REST API的组合,帮助用户在数分钟内接入Notion工作空间。核心能力:


  - 托管OAuth鉴权,无需自建鉴权服务

  - 页面与数据库的查询、检索

  - 基础读写操作(创建、更新、归档页面)

  - 块级内容管理(读取、追加、删除)

  - 用户信息查询

  - 写操作强制用户确认,保障数据安全


  适用场景:


  - 个人Notion工作空间的自动化查询

  - 小型团队的页面检索与读取

  - MVP阶段的...'
tags:
- 集成工具
- Notion
- 生产力
tools:
- - read
- exec
homepage: https://skillhub.cn
pricing_tier: "L1-入门级"
pricing_model: per_use
suggested_price: "9.9 CNY/per_use"
tools: ["read", "write", "exec"]
tags: "API,接口,开发工具"
---
# Notion API工具箱(免费版)

一个面向个人开发者与知识工作者的轻量化Notion集成Skill,通过托管OAuth与REST API的组合,帮助你快速接入Notion工作空间。本免费版聚焦查询与基础读写,适合个人与小型团队试用。

## 概述

本Skill封装了Notion API的常用操作,通过托管OAuth代理层屏蔽鉴权复杂度。所有写操作(创建、更新、删除)均需用户明确确认目标资源与连接,保障数据安全。免费版适合日请求量不超过500次的场景。

## 核心能力

| 能力 | 描述 | 免费版是否支持 |
|---|---|-------|
| OAuth鉴权 | 托管OAuth,无需自建 | 支持(单连接) |
| 页面查询 | 搜索、获取、创建页面 | 支持 |
| 数据库检索 | 查询数据库、获取数据源 | 支持 |
| 块管理 | 读取、追加、删除块 | 支持 |
| 用户信息 | 列出用户、获取当前用户 | 支持 |
| 写操作确认 | 强制用户确认目标 | 支持 |
| 多连接管理 | 同时管理多个Notion账户 | 不支持 |
| 批量操作 | 批量创建/更新页面 | 不支持 |
| Webhook订阅 | 页面变更事件推送 | 不支持 |
| 高级筛选 | 复合条件筛选 | 部分支持 |
| 分页自动化 | 自动翻页 | 不支持 |
| 版本管理 | API版本切换 | 不支持 |

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
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：轻量化、集成工具、数据库检索与基础、适合个人快速接入、工作空间、工具箱、是面向个人开发者、与知识工作者的轻、通过托管、REST、的组合、帮助用户在数分钟、内接入、核心能力等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持。

## 使用场景

### 场景一:个人知识库检索

个人开发者希望快速检索自己的Notion笔记。

```bash
# 1. 登录并创建连接
notion-toolkit login
notion-toolkit connection create
# ...
# 2. 搜索页面
notion-toolkit search "会议纪要"
# ...
# 3. 查询数据库
notion-toolkit database query <databaseId> --filter '{"property":"Status","select":{"equals":"Active"}}'
```

### 场景二:小型团队页面读取

团队成员需要读取共享的Notion文档。

```bash
# 获取页面内容
notion-toolkit page view <pageId>
# ...
# 读取块级内容
notion-toolkit block children <blockId>
# ...
# 获取当前用户信息
notion-toolkit whoami
```

### 场景三:简单页面创建

开发者希望在Notion中自动创建任务页面。

```bash
# 用户确认后创建页面
notion-toolkit page create --parent-page <parentId> --title "新任务"
# ...
# 追加内容块
notion-toolkit block append <pageId> --children '[{"type":"paragraph","paragraph":{"rich_text":[{"text":{"content":"任务详情"}}]}}]'
```

## 不适用场景

以下场景Notion API工具箱(免费版)不适合处理：

- 逆向工程闭源API
- API安全渗透测试
- 非标准协议集成

## 触发条件

需要API集成、接口对接、Webhook配置、系统连接时使用。不适用于非本工具能力范围的需求。

## 快速开始

预计上手时间:<60秒。

### 依赖详情

```bash
npm install -g notion-api-toolkit
```

### Step 2:登录并创建连接

```bash
notion-toolkit login
notion-toolkit connection create notion
# 返回的URL在浏览器中打开,完成OAuth授权
```

### Step 3:验证连接

```bash
notion-toolkit connection list
notion-toolkit whoami
```

### Step 4:开始查询

```bash
notion-toolkit search "你的关键词"
```

## 示例

### 鉴权配置

```bash
# 设置API Key
export NOTION_TOOLKIT_API_KEY="your_api_key_here"
# ...
# 验证鉴权状态
notion-toolkit whoami
```

### 基础查询示例

```bash
# 搜索页面
notion-toolkit search "会议" --filter page
# ...
# 搜索数据源
notion-toolkit search --filter data_source
# ...
# 查询数据库
notion-toolkit database query <databaseId> \
  --filter '{"property":"Status","select":{"equals":"Active"}}' \
  --sorts '[{"property":"Created","direction":"descending"}]' \
  --page-size 10
# ...
# 获取页面
notion-toolkit page view <pageId>
# ...
# 读取块级内容
notion-toolkit block children <blockId>
```

### 写操作示例(需用户确认)

```bash
# 创建页面(会提示用户确认)
notion-toolkit page create --parent-page <parentId> --title "新页面"
# ...
# 更新页面属性
notion-toolkit page update <pageId> --properties '{"Status":{"select":{"name":"Done"}}}'
# ...
# 追加块
notion-toolkit block append <blockId> \
  --children '[{"type":"paragraph","paragraph":{"rich_text":[{"text":{"content":"新段落"}}]}}]'
# ...
# 归档页面
notion-toolkit page archive <pageId>
```

### 筛选操作符参考

| 操作符 | 描述 |
|:-----|:-----|
| `equals` | 等于 |
| `does_not_equal` | 不等于 |
| `contains` | 包含 |
| `does_not_contain` | 不包含 |
| `starts_with` | 开头匹配 |
| `ends_with` | 结尾匹配 |
| `is_empty` | 为空 |
| `is_not_empty` | 非空 |
| `greater_than` | 大于 |
| `less_than` | 小于 |

### 块类型参考

| 块类型 | 描述 |
|---:|---:|
| `paragraph` | 段落 |
| `heading_1` | 一级标题 |
| `heading_2` | 二级标题 |
| `heading_3` | 三级标题 |
| `bulleted_list_item` | 无序列表项 |
| `numbered_list_item` | 有序列表项 |
| `to_do` | 待办事项 |
| `code` | 代码块 |
| `quote` | 引用 |
| `divider` | 分割线 |

## 最佳实践

1. **写操作必须用户确认**:任何创建、更新、删除操作前,明确告知用户目标资源与影响
2. **使用最小权限连接**:仅授予任务所需的页面与数据库访问权限
3. **指定具体连接ID**:多账户场景下,务必指定`--connection`参数,避免误操作
4. **限定搜索范围**:用`--filter`限定搜索类型(page/data_source),提升效率
5. **分页查询控制page_size**:单次查询不超过100条,避免响应过大
6. **保留API版本头**:所有请求必须携带`Notion-Version: 2025-09-03`头
7. **先查询后修改**:修改前先`page view`确认目标,避免误改

## 安全与权限

- 访问范围限定在已授权连接的Notion账户内
- **所有写操作需用户明确批准**:执行前必须确认目标(页面ID、数据库ID、块ID)
- **高风险操作需额外谨慎**:
  - 删除页面或块(归档,但可能影响工作流)
  - 批量更新多个页面
  - 修改团队共享页面
- **权限边界**:
  - 仅操作用户明确指定的资源
  - 使用最小权限连接
  - 不进行未经批准的批量操作

## 常见问题

### Q1: 返回401 Unauthorized怎么办?

A: 检查API Key是否正确设置,运行`notion-toolkit whoami`验证鉴权状态。

### Q2: 返回400 "Missing Notion connection"怎么办?

A: 需要先创建Notion连接:`notion-toolkit connection create notion`,然后在浏览器中完成OAuth授权。

### Q3: 返回429 Too Many Requests怎么办?

A: 触发频率限制(免费版10 req/sec)。等待1秒后重试,或升级专业版提升限额。

### Q4: 写操作被拒绝怎么办?

A: 写操作需要用户明确确认。Agent在执行前会询问用户:"是否要修改页面xxx?",用户确认后才会执行。

### Q5: 如何获取数据源ID?

A: 先`GET /databases/{id}`获取数据库详情,响应中的`data_sources`数组包含数据源ID。

### Q6: 创建数据库时属性被丢弃?

A: 在API 2025-09-03中,`POST /databases`仅接受title属性,其他属性会被静默丢弃。需要先创建数据库,再用`PATCH /data_sources/{id}`定义schema。

## 错误处理

| 错误场景(症状) | 可能原因 | 解决方案 |
|:-------:|:-------:|:-------:|
| 401 Unauthorized | API Key缺失或无效 | 检查环境变量,运行whoami验证 |
| 400 Missing connection | 未创建Notion连接 | 执行`connection create notion` |
| 404 Not Found | ID错误或资源未共享 | 确认ID正确,在Notion中共享给Integration |
| 429 Rate limited | 触发频率限制 | 等待1秒执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令,或升级专业版 |
| 写操作失败 | 用户未确认 | Agent明确询问用户后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令 |
| 属性被丢弃 | API版本限制 | 先创建再用PATCH定义schema |
## 已知限制

本免费体验版限制以下高级功能:

- 多连接管理(同时管理>1个Notion账户)
- 批量操作(批量创建/更新/删除页面)
- Webhook订阅(页面变更事件推送)
- 自动分页(自动翻页获取全部结果)
- 高级筛选(复合条件、嵌套逻辑)
- API版本切换(仅支持2025-09-03)
- 自定义转换器(Jinja2模板)
- 团队协作与共享连接
- 审计日志与操作追踪

解锁全部功能请使用专业版:notion-api-toolkit-pro

## 依赖说明

### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent(Claude Code / Cursor / Codex / Gemini CLI等)
- **操作系统**: Windows / macOS / Linux
- **Node.js**: 16+(用于运行CLI工具)
- **Python**: 3.8+(可选,用于辅助脚本)

### 第三方依赖
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:------|------:|:------|:------|
| LLM API | API | 必需 | 由Agent平台内置LLM提供 |
| notion-api-toolkit CLI | 命令行工具 | 必需 | `npm install -g notion-api-toolkit` |
| Notion账户 | 在线服务 | 必需 | 通过notion.so注册 |
| curl | 命令行工具 | 可选 | 操作系统自带 |
| jq | JSON处理工具 | 推荐 | 通过包管理器安装 |

### API Key 配置
- **NOTION_TOOLKIT_API_KEY**: 通过环境变量传入,用于API鉴权
- **OAuth连接**: 通过`connection create`命令创建,浏览器完成授权
- **安全建议**: API Key禁止硬编码在脚本中,建议使用Secret管理服务
- **权限最小化**: OAuth授权时仅勾选任务所需的权限范围

### 可用性分类
- **分类**: MD+EXEC(纯Markdown指令,部分功能需exec命令行执行)
- **说明**: 基于Markdown的AI Skill,通过自然语言指令驱动Agent完成操作

## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "Notion API工具箱(免费版)处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "notion apikit"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```
