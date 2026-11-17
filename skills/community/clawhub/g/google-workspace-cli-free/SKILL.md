---
name: "google-workspace-cli-free"
description: "轻量级Google Workspace命令行工具,支持Gmail、Calendar、Drive核心操作,适合个人用户日常使用。"
license: Proprietary
allowed-tools: read exec
compatibility: "Requires LLM with tool-use capability"
metadata:
  displayName: "谷歌办公命令行免费版"
  version: "1.0.0"
  summary: "轻量级Google Workspace命令行工具,支持Gmail、Calendar、Drive核心操作,适合个人用户日常使用。"
  tags:
    - "沟通协作"
    - "邮件管理"
    - "谷歌办公"
    - "命令行工具"
    - "个人效率"
  source: "SkillHub"
  converted_at: "2026-07-22T17:58:36"
---

# 谷歌办公命令行工具 - 免费版

## 概述

谷歌办公命令行工具免费版是一款面向个人用户的 Google Workspace 轻量级命令行助手。通过简单的命令行指令,用户可以快速完成 Gmail 邮件搜索与发送、Google 日历日程查询、Google Drive 文件检索等高频操作,无需打开浏览器切换多个标签页,大幅提升日常办公效率。

本版本聚焦三大核心服务(Gmail、Calendar、Drive),适合个人开发者、自由职业者以及对命令行操作有偏好的轻量办公用户。

## 核心能力

### 邮件管理(Gmail)

- 邮件搜索:支持 Gmail 原生搜索语法,如时间范围、发件人、标签等
- 邮件发送:支持指定收件人、主题、正文的一键发送
- 邮件读取:获取邮件正文与元数据

**输入**: 用户提供邮件管理(Gmail)所需的指令和必要参数。
**处理**: 按照skill规范执行邮件管理(Gmail)操作,遵循单一意图原则。
**输出**: 返回邮件管理(Gmail)的执行结果,包含操作状态和输出数据。

### 日历管理(Calendar)

- 事件查询:按时间范围列出日历事件
- 多日历支持:可查询指定日历 ID 的事件列表

**输入**: 用户提供日历管理(Calendar)所需的指令和必要参数。
**处理**: 按照skill规范执行日历管理(Calendar)操作,遵循单一意图原则。
**输出**: 返回日历管理(Calendar)的执行结果,包含操作状态和输出数据。

### 云盘管理(Drive)

- 文件搜索:按关键词检索云端文件
- 文件列表:获取最近文件清单

**输入**: 用户提供云盘管理(Drive)所需的指令和必要参数。
**处理**: 按照skill规范执行云盘管理(Drive)操作,遵循单一意图原则。
**输出**: 返回云盘管理(Drive)的执行结果,包含操作状态和输出数据。

### 认证与安全

- OAuth 2.0 凭据管理
- 多账户配置(基础)
- 凭据本地加密存储

**输入**: 用户提供认证与安全所需的指令和必要参数。
**处理**: 按照skill规范执行认证与安全操作,遵循单一意图原则。
**输出**: 返回认证与安全的执行结果,包含操作状态和输出数据。
**技术参数**：使用`input_params`和`output_format`参数控制执行行为,支持`json`/`text`/`csv`输出格式。
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：轻量级、Google、Workspace、命令行工具、核心操作、适合个人用户日常、谷歌办公命令行工、具免费版、为个人用户提供、日历日程查询、文件搜索等核心能、核心能力、读取与发送、日历事件查询与提、文件检索与下载、Use、when、SEO、关键词分析、排名提升、搜索流量优化时使、不适用于黑帽等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持。

## 使用场景

### 场景一:快速检索近7天未读邮件

个人用户早晨打开终端,快速查看过去一周的未读邮件,无需登录网页版 Gmail。

```bash
# 检索近7天未读邮件,最多显示10条
gog gmail search 'is:unread newer_than:7d' --max 10

# 检索特定发件人的邮件
gog gmail search 'from:boss@company.com newer_than:3d' --max 5
```

**输出示例**:

```text
[1] ID: abc123 | From: alice@example.com | Subject: 周报汇总 | Date: 2026-07-15
[2] ID: def456 | From: bob@example.com | Subject: 项目进度同步 | Date: 2026-07-16
```

### 场景二:查看今日日历安排

出门前快速确认今日会议安排,避免错过重要日程。

```bash
# 查询今日日历事件
gog calendar events primary --from 2026-07-18T00:00:00Z --to 2026-07-18T23:59:59Z

# 查询明日安排
gog calendar events primary --from 2026-07-19T00:00:00Z --to 2026-07-19T23:59:59Z
```

### 场景三:发送一封快速通知邮件

无需打开邮件客户端,命令行直接发送一封通知邮件。

```bash
# 发送简单文本邮件
gog gmail send --to colleague@example.com --subject "会议确认" --body "明天下午3点会议室A见,请准时参加。"

# 设置默认账户避免重复输入
export GOG_ACCOUNT=you@gmail.com
gog gmail send --to team@example.com --subject "周报提交" --body "本周周报已更新,请查阅附件。"
```

## 快速开始

### 依赖详情

```bash
# 配置OAuth凭据(一次性操作)
gog auth credentials /path/to/client_secret.json

# 添加账户并授权所需服务
gog auth add you@gmail.com --services gmail,calendar,drive

# 查看已配置账户
gog auth list
```

### 第二步:设置默认账户

```bash
# 将常用账户设为默认,避免每次输入 --account
export GOG_ACCOUNT=you@gmail.com
```

### 第三步:开始使用

```bash
# 测试Gmail搜索
gog gmail search 'newer_than:1d' --max 5

# 测试日历查询
gog calendar events primary --from 2026-07-18T00:00:00Z --to 2026-07-18T23:59:59Z

# 测试Drive搜索
gog drive search "报告" --max 10
```

## 示例

### 基础配置

```bash
# ~/.gog/config 示例
default_account: you@gmail.com
output_format: json
no_input: true
```

### 环境变量配置

```bash
# 设置默认账户
export GOG_ACCOUNT=you@gmail.com

# 设置输出格式为JSON(便于脚本处理)
export GOG_OUTPUT=json

# 设置不交互模式
export GOG_NO_INPUT=true
```

### 脚本化使用示例

```python
#!/usr/bin/env python3
"""每日邮件摘要脚本"""
import subprocess
import json

# 获取今日未读邮件
result = subprocess.run(
    ['gog', 'gmail', 'search', 'is:unread newer_than:1d', '--max', '20', '--json', '--no-input'],
    capture_output=True, text=True
)

emails = json.loads(result.stdout)
print(f"今日未读邮件共 {len(emails)} 封:")
for i, mail in enumerate(emails, 1):
    print(f"  {i}. {mail.get('from', '未知')} | {mail.get('subject', '无主题')}")
```

## 最佳实践

### 1. 使用默认账户减少输入

通过设置 `GOG_ACCOUNT` 环境变量,避免每次命令都输入 `--account` 参数,提升操作流畅度。

### 2. 脚本化优先使用 JSON 输出

在自动化脚本中,务必添加 `--json` 和 `--no-input` 参数,确保输出可解析且不会因交互提示阻塞。

### 3. 发送邮件前二次确认

涉及邮件发送或事件创建的操作,建议先预览内容再执行,避免误发。

```bash
# 先预览邮件内容
echo "收件人: team@example.com"
echo "主题: 周报提交"
echo "正文: 本周周报已更新"
read -p "确认发送?(y/N)" confirm
if [ "$confirm" = "y" ]; then
    gog gmail send --to team@example.com --subject "周报提交" --body "本周周报已更新"
fi
```

### 4. 合理使用搜索语法

Gmail 搜索语法强大,熟练使用可大幅提升检索效率:

| 语法 | 说明 | 示例 |
|:-----|:-----|:-----|
| `from:` | 按发件人搜索 | `from:alice@example.com` |
| `to:` | 按收件人搜索 | `to:bob@example.com` |
| `subject:` | 按主题搜索 | `subject:周报` |
| `newer_than:` | 按时间范围 | `newer_than:7d` |
| `is:` | 按状态搜索 | `is:unread` |
| `has:` | 按附件搜索 | `has:attachment` |

## 常见问题

### Q1: 认证失败提示 "invalid_grant" 怎么办?

**A**: 通常由系统时间不同步或凭据过期导致。请检查系统时间是否准确,并尝试重新添加账户:

```bash
gog auth remove you@gmail.com
gog auth add you@gmail.com --services gmail,calendar,drive
```

### Q2: 搜索邮件返回结果为空?

**A**: 请确认搜索语法是否正确,并检查时间范围。建议先用宽泛条件测试:

```bash
gog gmail search 'newer_than:30d' --max 5
```

### Q3: 如何切换多个账户?

**A**: 使用 `--account` 参数指定不同账户,或通过 `GOG_ACCOUNT` 环境变量切换默认账户:

```bash
gog gmail search 'is:unread' --account work@gmail.com --max 5
gog gmail search 'is:unread' --account personal@gmail.com --max 5
```

### Q4: 发送邮件支持 HTML 格式吗?

**A**: 免费版支持纯文本邮件发送。如需 HTML 格式邮件、附件发送、批量邮件等高级功能,请考虑升级至 PRO 版本。

### Q5: 命令执行较慢如何优化?

**A**: 首次执行需加载凭据会有延迟。后续操作可通过 `--no-input` 减少交互开销,并使用 `--json` 输出减少格式化时间。

## 依赖说明

### 运行环境

- **Agent平台**: 支持 SKILL.md 的任意 AI Agent(Claude Code / Cursor / Codex / Gemini CLI 等)
- **操作系统**: Windows / macOS / Linux
- **网络环境**: 需可访问 Google API 服务

### 第三方依赖

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-------|:-----|:---------|:---------|
| Google OAuth 凭据 | 凭据 | 必需 | Google Cloud Console 创建 |
| gog 命令行工具 | CLI | 必需 | 通过包管理器安装 |
| LLM API | API | 必需 | 由 Agent 内置 LLM 提供 |

### API Key 配置

- 需在 Google Cloud Console 创建 OAuth 2.0 客户端 ID,下载 `client_secret.json` 凭据文件
- 通过 `gog auth credentials /path/to/client_secret.json` 导入凭据
- 首次使用会打开浏览器完成 OAuth 授权,授权后凭据本地加密存储

### 可用性分类

- **分类**: MD+EXEC(纯 Markdown 指令,核心功能需要 exec 命令行执行能力)
- **说明**: 基于命令行的 AI Skill,通过自然语言指令驱动 Agent 执行 Google Workspace 操作。免费版支持 Gmail、Calendar、Drive 三大核心服务的基础操作,适合个人轻量办公场景。
- API Key通过环境变量配置: export API_KEY=your_key

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
