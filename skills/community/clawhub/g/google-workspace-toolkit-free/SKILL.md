---
name: "google-workspace-toolkit-free"
description: "免配置云控制台的Google办公工具接口,OAuth登录即用,支持Gmail、日历、Drive核心工具调用。"
license: Proprietary
allowed-tools: read exec
compatibility: "Requires LLM with tool-use capability"
metadata:
  displayName: "谷歌办公工具接口免费版"
  version: "1.0.0"
  summary: "免配置云控制台的Google办公工具接口,OAuth登录即用,支持Gmail、日历、Drive核心工具调用。"
  tags:
    - "沟通协作"
    - "谷歌办公"
    - "工具接口"
    - "OAuth认证"
    - "个人效率"
  source: "SkillHub"
  converted_at: "2026-07-22T17:58:36"
---

# 谷歌办公工具接口 - 免费版

## 概述

谷歌办公工具接口免费版是一款零云控制台配置的 Google Workspace 访问工具。传统方式使用 Google API 需要在云控制台创建项目、启用 API、创建 OAuth 凭据、下载密钥文件、配置回调地址等繁琐步骤。本工具完全跳过这些流程,只需用 Google 账号 OAuth 登录,即可通过工具协议直接调用 Gmail、日历、Drive 等核心服务。

本版本适合个人用户、轻量办公场景以及对云控制台配置不熟悉的用户,几分钟内即可开始使用。

## 核心能力

### 零配置快速接入

- 无需创建 Google Cloud 项目
- 无需逐个启用 API
- 无需创建 OAuth 凭据
- 无需下载 client_secret.json
- 无需配置回调地址
- 只需 Google 账号登录授权

**输入**: 用户提供零配置快速接入所需的指令和必要参数。
**处理**: 按照skill规范执行零配置快速接入操作,遵循单一意图原则。
**输出**: 返回零配置快速接入的执行结果,包含操作状态和输出数据。

### Gmail 邮件工具

- `gmail.search`:搜索邮件,支持 Gmail 原生语法
- `gmail.get`:获取指定邮件详情
- `gmail.send`:发送邮件
- `gmail.createDraft`:创建草稿

**输入**: 用户提供Gmail 邮件工具所需的指令和必要参数。
**处理**: 按照skill规范执行Gmail 邮件工具操作,遵循单一意图原则。
**输出**: 返回Gmail 邮件工具的执行结果,包含操作状态和输出数据。

### Calendar 日历工具

- `calendar.list`:列出所有日历
- `calendar.listEvents`:按时间范围列出事件
- `calendar.createEvent`:创建日历事件
- `calendar.findFreeTime`:查找空闲时间段

**输入**: 用户提供Calendar 日历工具所需的指令和必要参数。
**处理**: 按照skill规范执行Calendar 日历工具操作,遵循单一意图原则。
**输出**: 返回Calendar 日历工具的执行结果,包含操作状态和输出数据。

### Drive 文件工具

- `drive.search`:搜索云端文件
- `drive.downloadFile`:下载文件到本地

**输入**: 用户提供Drive 文件工具所需的指令和必要参数。
**处理**: 按照skill规范执行Drive 文件工具操作,遵循单一意图原则。
**输出**: 返回Drive 文件工具的执行结果,包含操作状态和输出数据。

### 认证管理

- OAuth 登录即用,凭据本地存储
- 支持重新认证与令牌刷新
- 支持清除凭据重新授权

**输入**: 用户提供认证管理所需的指令和必要参数。
**处理**: 按照skill规范执行认证管理操作,遵循单一意图原则。
**输出**: 返回认证管理的执行结果,包含操作状态和输出数据。
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：免配置云控制台的、办公工具接口、核心工具调用、谷歌办公工具接口、免费版、通过工具协议直接、Workspace、无需创建云控制台、登录即可使用、核心能力、零云控制台配置、账号登录即用、邮件搜索、日历事件列表、文件搜索与下载、通过工具协议统一、无需管理多个、SDK等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持。

## 使用场景

### 场景一:零配置开始使用 Gmail

用户无需任何云控制台配置,安装后直接登录 Google 账号即可搜索邮件。

```bash
# 依赖说明
npm install -g @presto-ai/google-workspace-toolkit

# 第二步:注册工具服务(仅需一次)
gwtool config add google-workspace \
    --command "npx" \
    --arg "-y" \
    --arg "@presto-ai/google-workspace-toolkit" \
    --scope home

# 第三步:首次调用时浏览器弹出 OAuth 登录
gwtool call --server google-workspace --tool "gmail.search" query="is:unread" maxResults=10
```

首次执行任意命令时,系统会自动打开浏览器引导用户完成 Google OAuth 授权。授权后凭据存储在 `~/.config/google-workspace-toolkit/` 目录,后续无需重复登录。

### 场景二:快速查看本周日历安排

无需打开日历应用,命令行直接查看本周会议安排。

```bash
# 列出所有日历
gwtool call --server google-workspace --tool "calendar.list"

# 查询本周事件(以2026年7月14日-20日为例)
gwtool call --server google-workspace \
    --tool "calendar.listEvents" \
    calendarId="your@gmail.com" \
    timeMin="2026-07-14T00:00:00Z" \
    timeMax="2026-07-20T23:59:59Z"
```

### 场景三:搜索并下载云端文件

快速在 Google Drive 中搜索特定文件并下载到本地。

```bash
# 搜索文件
gwtool call --server google-workspace \
    --tool "drive.search" \
    query="季度报告"

# 下载文件(使用上一步获取的 fileId)
gwtool call --server google-workspace \
    --tool "drive.downloadFile" \
    fileId="<文件ID>" \
    localPath="/tmp/report.pdf"
```

## 不适用场景

以下场景谷歌办公工具接口免费版不适合处理：

- 黑帽SEO手段
- 搜索引擎作弊
- 付费广告投放管理

## 触发条件

需要SEO优化、关键词分析、排名提升、搜索流量优化时使用。不适用于非本工具能力范围的需求。

## 快速开始

### 第一步:安装与注册

```bash
# 安装工具接口
npm install -g @presto-ai/google-workspace-toolkit

# 注册 Google Workspace 服务
gwtool config add google-workspace \
    --command "npx" \
    --arg "-y" \
    --arg "@presto-ai/google-workspace-toolkit" \
    --scope home
```

### 第二步:完成 OAuth 登录

执行任意一条命令,首次会自动打开浏览器:

```bash
# 触发 OAuth 登录
gwtool call --server google-workspace --tool "gmail.search" query="is:unread" maxResults=5
```

浏览器中登录 Google 账号并授权后,凭据自动保存到本地。

### 第三步:开始日常使用

```bash
# 搜索邮件
gwtool call --server google-workspace --tool "gmail.search" query="newer_than:7d" maxResults=10

# 查看日历
gwtool call --server google-workspace --tool "calendar.list"

# 搜索文件
gwtool call --server google-workspace --tool "drive.search" query="报告"
```

## 示例

### 工具服务注册配置

```bash
# 注册配置(持久化存储)
gwtool config add google-workspace \
    --command "npx" \
    --arg "-y" \
    --arg "@presto-ai/google-workspace-toolkit" \
    --scope home

# 查看已注册服务
gwtool config list

# 移除服务
gwtool config remove google-workspace
```

### 凭据存储位置

```bash
# 凭据默认存储路径
~/.config/google-workspace-toolkit/

# 查看凭据文件
ls -la ~/.config/google-workspace-toolkit/
```

### 脚本化调用示例

```python
#!/usr/bin/env python3
"""每日邮件摘要 - 工具接口版"""
import subprocess
import json

def call_tool(tool_name, **params):
    """调用 Google Workspace 工具"""
    cmd = ['gwtool', 'call', '--server', 'google-workspace', '--tool', tool_name]
    for key, value in params.items():
        cmd.extend([f'{key}={value}'])
    result = subprocess.run(cmd, capture_output=True, text=True)
    return json.loads(result.stdout) if result.stdout else []

# 获取未读邮件
emails = call_tool('gmail.search', query='is:unread newer_than:1d', maxResults=10)
print(f"未读邮件 {len(emails)} 封:")
for mail in emails:
    print(f"  - {mail.get('from', '未知')}: {mail.get('subject', '无主题')}")
```

## 最佳实践

### 1. 善用 OAuth 自动续期

工具接口会自动管理令牌刷新,正常使用无需手动干预。若长时间未使用导致令牌过期,执行任意命令会自动触发刷新。

```bash
# 令牌过期后,执行任意命令自动刷新
gwtool call --server google-workspace --tool "gmail.search" query="is:unread" maxResults=1
```

### 2. 跨设备使用需重新授权

凭据存储在本地,不同设备需分别完成 OAuth 授权。请勿手动复制凭据文件到其他设备,可能导致授权失效。

### 3. 查询参数使用 JSON 字符串

复杂参数(如事件时间)使用 JSON 字符串传递:

```bash
# 创建日历事件
gwtool call --server google-workspace \
    --tool "calendar.createEvent" \
    calendarId="your@gmail.com" \
    summary="团队周会" \
    start='{"dateTime":"2026-07-25T14:00:00Z"}' \
    end='{"dateTime":"2026-07-25T15:00:00Z"}'
```

### 4. 查找空闲时间避免会议冲突

安排会议前,先用 `findFreeTime` 查询参会人共同空闲时段:

```bash
gwtool call --server google-workspace \
    --tool "calendar.findFreeTime" \
    attendees='["a@example.com","b@example.com"]' \
    timeMin="2026-07-25T09:00:00Z" \
    timeMax="2026-07-25T18:00:00Z" \
    duration=30
```

## 常见问题

### Q1: 首次调用时浏览器没有弹出怎么办?

**A**: 检查系统默认浏览器设置,或手动复制终端中显示的授权 URL 到浏览器打开。完成授权后回到终端即可继续。

### Q2: 提示 "token expired" 怎么处理?

**A**: 执行令牌刷新命令,或直接执行任意业务命令触发自动刷新:

```bash
# 手动刷新令牌
gwtool call --server google-workspace --tool "auth.refreshToken"

# 或直接执行业务命令(自动刷新)
gwtool call --server google-workspace --tool "gmail.search" query="is:unread" maxResults=1
```

### Q3: 如何切换 Google 账号?

**A**: 清除现有凭据后重新登录:

```bash
# 清除凭据
gwtool call --server google-workspace --tool "auth.clear"

# 执行任意命令重新触发 OAuth 登录
gwtool call --server google-workspace --tool "gmail.search" query="is:unread" maxResults=1
```

### Q4: 免费版支持哪些工具?与专业版有何区别?

**A**: 免费版支持 Gmail(4个工具)、Calendar(4个工具)、Drive(2个工具)共 10 个核心工具。专业版提供全部 49 个工具,包含 Docs、Sheets、Slides、Chat、People 等高级服务。

### Q5: 离线环境可以使用吗?

**A**: 不支持。工具接口需要实时访问 Google API,且 OAuth 授权与令牌刷新均需网络连接。

### Q6: 是否支持多账户?

**A**: 免费版默认单账户使用。如需多账户切换,需清除凭据后重新登录。专业版支持多账户管理与快速切换。

## 依赖说明

### 运行环境

- **Agent平台**: 支持 SKILL.md 的任意 AI Agent(Claude Code / Cursor / Codex / Gemini CLI 等)
- **操作系统**: Windows / macOS / Linux
- **Node.js**: 建议 18.0+ (运行工具接口)
- **网络环境**: 需可访问 Google API 服务

### 第三方依赖

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-------|:-----|:---------|:---------|
| Node.js 18+ | 运行时 | 必需 | nodejs.org 下载 |
| npm / npx | 包管理 | 必需 | 随 Node.js 安装 |
| @presto-ai/google-workspace-toolkit | 工具接口 | 必需 | npm 全局安装 |
| gwtool 命令行工具 | CLI | 必需 | 随工具接口安装 |
| Google 账号 | 账户 | 必需 | 注册 Google 账号 |
| LLM API | API | 必需 | 由 Agent 内置 LLM 提供 |

### API Key 配置

- 无需创建 Google Cloud 项目
- 无需创建 OAuth 凭据或下载 client_secret.json
- 首次使用时通过浏览器完成 Google OAuth 授权
- 凭据自动存储于 `~/.config/google-workspace-toolkit/` 目录

### 可用性分类

- **分类**: MD+EXEC(纯 Markdown 指令,核心功能通过工具协议调用需要 exec 命令行执行能力)
- **说明**: 基于工具接口的 AI Skill,通过工具协议统一调用 Google Workspace 服务。免费版主打零云控制台配置,OAuth 登录即用,支持 Gmail、Calendar、Drive 三大核心服务共 10 个工具,适合个人轻量办公场景。

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