---
slug: "google-workspace-mcp-free"
name: "google-workspace-mcp-free"
version: "1.0.0"
displayName: "Workspace 工具协议免费版"
summary: "免Google Cloud Console配置,OAuth登录即用Gmail/Calendar/Drive/Docs/Sheets的基础读取能力,覆盖邮件检索、日程查看、文件下载与文档表格,提供."
summary_zh: "免Google Cloud Console配置,OAuth登录即用Gmail/Calendar/Drive/Docs/Sheets的基础读取能力,覆盖邮件检索、日程查看、文件下载与文档表格,提供核心能力"
license: "MIT"
description: "|-. 适用于需要google workspace mcp相关能力的开发场景,包含结构化的工作流程和可复用的模板,帮助用户快速完成任务并保持代码质量.该技能适用于相关开发场景,包含结构化的工作流程和配置指引.经过深度差异化处置,针对用户反馈和使用痛点进行了改进,提升了实用性和可操作性.该技能适用于相关开发场景,包含结构化的工作流程和配置指引.经过深度差异化处置,针对用户反馈和使用痛点进行了改进,提升了实用性和可操作性."
  通过 @presto-ai/google-workspace-mcp 以纯OAuth登录方式访问Google Workspace,跳过Cloud Console建项目、启用API、下载client_secret.json等繁琐步骤。免费版提供Gmail邮件搜索与读取、Calendar日程查看、Drive文件检索与下载、Docs文档检索与文本提取、Sheets表格区域读取等基础能力,适合个人开发者体验Google Workspace自动化办公。写入、发送、会议创建、Chat与Slides等高级能力见付费版.
tags:
  - 通用办公
  - google
  - workspace
  - mcp
  - automation
  - Productivity
  - 工具
  - 效率
  - 通信
  - 邮件
tools:
  - read
  - exec
  - glob
  - grep
homepage: ""
category: "Automation"
pricing_tier: free
---
# Google Workspace 工具协议 免费版

通过 `@presto-ai/google-workspace-mcp` 以OAuth登录访问Google Workspace,无需在Google Cloud Console创建项目或下载client_secret.json。首次使用时弹出浏览器完成Google授权,凭证保存在 `./.config/google-workspace-mcp/`.
免费版聚焦基础读取场景,提供邮件检索、日程查看、文件下载与文档表格文本提取能力。所有工具通过同一OAuth凭证访问,无需为每个服务单独配置.
## 输入格式

| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| input | string | 是 | Workspace 工具协议免费版处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

## 依赖说明

### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**: Windows / macOS / Linux

### 依赖项
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-----|:-----|:-----|:-----|
| LLM API | API | 必需 | 由Agent内置LLM提供 |

### API Key 配置
需要配置对应API Key，详见上文环境配置章节

### 可用性分类
- **分类**: MD+EXEC（）

**API Key配置方式**:
```bash
export API_KEY=${API_KEY:?请设置环境变量}
```
配置后需重启会话或开启新终端生效。API Key应妥善保管,避免泄露到版本控制系统.
## 核心能力

免费版开放以下读取类工具,均通过 `mcporter call --server google-workspace --tool "<tool>"` 调用.
**Gmail 邮件(2项)**: `gmail.search` 按Gmail查询语法检索邮件列表,支持 `is:unread`、`from:`、`after:`、`label:` 等运算符; `gmail.get` 按 messageId 读取单封邮件正文与元数据.
**Calendar 日历(2项)**: `calendar.list` 列出当前账号所有日历及其ID; `calendar.listEvents` 按 timeMin/timeMax 区间拉取指定日历的事件,包含标题、时间与参会者.
**Drive 云盘(2项)**: `drive.search` 按文件名或全文内容检索,返回文件ID与基本信息; `drive.downloadFile` 按 fileId 下载到本地指定路径.
**Docs 文档(2项)**: `docs.find` 检索文档标题或内容; `docs.getText` 提取文档纯文本,便于后续摘要与检索.
**Sheets 表格(2项)**: `sheets.getText` 读取整表文本; `sheets.getRange` 按 `Sheet1!A1:D20` 形式读取指定区域数据.
**Time 时间(2项)**: `time.getCurrentDate` 获取当前日期; `time.getTimeZone` 获取时区,用于日程时间换算.
**Auth 鉴权(2项)**: `auth.clear` 清除凭证触发重新授权; `auth.refreshToken` 刷新令牌.
#
## 快速开始

1. 确认运行环境满足依赖说明中的要求
2. 在AI Agent对话中调用本技能,提供必要的输入参数
3. 检查输出结果,根据需要进行后续处理

> 详细的输入输出格式请参考下方章节说明。

## 使用流程

1. **环境确认**: 确认Agent平台已加载本skill，检查依赖说明中的环境要求
2. **指令输入**: 向Agent描述需要执行的任务，引用`google-workspace-mcp-free`的相关能力
3. **执行处理**: Agent按照核心能力章节的指令执行任务
4. **结果验证**: 检查输出结果是否符合预期，参考错误处理章节处理异常

#
## 安装与授权

```bash
npm install -g @presto-ai/google-workspace-mcp
mcporter config add google-workspace --command "npx" --arg "-y" --arg "@presto-ai/google-workspace-mcp" --scope home
```

首次调用任意工具会打开浏览器请求Google授权,完成后凭证写入 `./.
## 常用命令

```bash
mcporter call --server google-workspace --tool "gmail.search" query="is:unread" maxResults=10
get" messageId="18c1f3a2b5d4e6f7"
mcporter call --server google-workspace --tool "calendar.list"
listEvents" calendarId="primary" timeMin="2026-07-20T00:00:00Z" timeMax="2026-07-20T23:59:59Z"
mcporter call --server google-workspace --tool "drive.search" query="季度财报"
downloadFile" fileId="1A2B3C4D5E6F" localPath="/tmp/report.pdf"
mcporter call --server google-workspace --tool "docs.find" query="会议纪要"
getText" documentId="1A2B3C4D5E6F"
mcporter call --server google-workspace --tool "sheets.getRange" spreadsheetId="1A2B3C4D5E6F" range="Sheet1!A1:D20"
mcporter call --server google-workspace --tool "time.getCurrentDate"
```

### Gmail 查询语法提示

`gmail.search` 的 query 参数沿用Gmail原生搜索运算符,常用组合:

- `is:unread` 未读邮件
- `from:client@corp.com` 指定发件人
- `subject:周报` 按主题匹配
- `after:2026/07/01` 指定日期之后
- `label:important` 按标签过滤
- `has:attachment` 仅含附件

多个条件用空格连接表示与关系,如 `from:manager@corp.com is:unread after:2026/07/01`.
### 文件与文档ID获取

`drive.search` 与 `docs.find` 返回结果中包含 fileId/documentId,后续 `drive.downloadFile`、`docs.getText`、`sheets.getRange` 需传入该ID。若已知文档URL,可记录其中 `/d/<ID>/` 片段作为ID使用.
## 适用场景

- **邮件快速检索**: 按发件人、主题或未读状态搜索邮件并读取正文,适合收件箱巡查与信息定位。例如查询某客户近一周往来邮件并提取关键诉求.
- **日程查看**: 拉取当日或本周日历事件,适合会前确认安排与时间冲突排查。配合 `time.getTimeZone` 可避免跨时区日程错位.
- **文档资料读取**: 跨Drive与Docs检索并提取文本,适合资料查阅与要点摘录。读取Sheets区域数据可用于本地报表或分析.
- **文件下载归档**: 将云盘中的PDF或附件下载到本地,便于离线查阅与备份.
## 使用案例

### 案例一: 晨会前快速准备

晨会前查看当日日程与未读重要邮件,确认时间安排与待办.
操作:
- `time.getTimeZone` 确认当前时区,避免日程时间错位
- `calendar.listEvents` 拉取 `calendarId="primary"` 当日 09:00-18:00 事件
- `gmail.search` 查询 `is:unread maxResults=10` 获取未读邮件列表
- 对关键邮件调用 `gmail.get` 读取正文,摘录需汇报的要点
- 将日程与邮件要点整理为晨会口头汇报提纲

### 案例二: 查阅共享文档与表格

定位团队共享的方案文档与数据表,提取文本用于本地分析.
操作:
- `drive.search` 检索 `query="需求方案"` 找到目标文件
- `docs.find` 搜索 `query="评审纪要"` 后 `docs.getText` 提取正文
- `sheets.getRange` 读取配套数据表 `Sheet1!A1:D20` 区域
- 将文档要点与表格数据合并到本地分析流程

## 免费版与付费版差异

免费版仅开放读取类工具,适合个人查阅与信息定位。付费版在此基础上提供邮件发送与草稿管理、日程创建与空闲时段查找、文档增改、Chat空间消息、People联系人资料、Slides读取等共49个工具,并配套更完整的异常处理与跨服务编排案例,适合日常办公自动化.
## 异常处理

- **OAuth令牌过期**: 工具返回401或未授权时,调用 `auth.refreshToken` 刷新; 仍失败则 `auth.clear` 后重新触发浏览器授权.
- **首次授权浏览器未弹出**: 确认系统默认浏览器已设置且非headless环境; 远程SSH场景需本地授权后复制 `./.config/google-workspace-mcp/` 目录.
- **gmail.search 返回空**: 校验查询语法(如 `is:unread`、`from:`、`after:`),放宽时间或标签条件; Gmail查询不支持正则,仅支持其原生搜索运算符.
- **drive.downloadFile 写入失败**: `localPath` 所在目录无写权限时更换到 `/tmp` 或用户目录; 文件过大受Google导出配额限制.
- **sheets.getRange 范围超界**: 工作表名需与实际一致(默认 `Sheet1`),区域引用如 `Sheet1!A1:B10`; 超出已用区域返回空值而非报错.
| 错误场景 | 原因 | 处理方式 |
|---:|---:|---:|
| LLM响应超时或无响应 | 网络延迟或模型负载过高 | 检查网络连接和配置后重试;确认Agent平台LLM服务正常 |
| 输入内容格式不正确 | 用户输入不符合skill预期格式 | 对照使用流程章节检查输入格式;参考示例章节修正输入 |
| 执行结果与预期不符 | 指令描述不够明确或上下文不足 | 提供更详细的指令描述,补充必要的上下文信息 |
| 命令执行失败 | 运行环境不满足要求或权限不足 | 对照依赖说明章节确认环境配置;检查命令权限设置 |

## 常见问题

**是否必须创建Google Cloud项目?**
不需要。本技能通过托管OAuth绕过Cloud Console建项目、启用API等步骤,只需浏览器登录Google账号即可.
**凭证存储在哪里? 如何切换账号?**
凭证保存在 `./.config/google-workspace-mcp/`。切换账号时执行 `auth.clear` 清除当前凭证,再次调用工具会触发新账号的浏览器授权.
**免费版能发送邮件或创建会议吗?**
不能。免费版仅提供读取类工具,发送邮件、创建/修改日程、文档写入等能力需升级到付费版.
**支持Google Workspace企业账号吗?**
支持,前提是企业管理员未在第三方应用访问策略中禁用相应API scope.
## 错误处理

| 错误场景(续)| 原因 | 处理方式 |
|:------:|:------:|:------:|
| LLM响应超时或无响应 | 网络延迟或模型负载过高 | 检查网络连接和配置后重试；确认Agent平台LLM服务正常 |
| 输入内容格式不正确 | 用户输入不符合skill预期格式 | 检查输入是否符合skill使用说明中的格式要求，参考示例章节 |
| 执行结果与预期不符 | 指令描述不够明确或上下文不足 | 提供更详细的指令描述，补充必要的上下文信息 |
| 命令执行失败 | 运行环境不满足要求或权限不足 | 确认运行环境符合依赖说明中的要求；检查命令权限设置 |

## 已知限制

- 依赖网络与Google服务可用性,离线不可用.
- OAuth令牌有有效期,长时间未使用可能需重新授权.
- 免费版仅支持读取,无法发送邮件、创建日程或编辑文档.
- 不包含Chat、Slides、People等高级工具.
- Gmail单次搜索maxResults受API上限约束,大批量拉取需分页.
## 升级提示

当前为免费版,仅开放基础读取能力。升级到付费版 `google-workspace-mcp` 可解锁全部49个工具,包括Gmail发送与草稿、Calendar会议创建与空闲时段查找、Docs文档增改、Chat空间消息、People联系人资料等,并获取更完整的异常处理与使用案例,适合日常办公自动化与跨服务工作流编排.
## 输出格式

```json
{
  "success": true,
  "data": {
    "result": "Workspace MCP免费版处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "google-workspace-mcp"
    }
  },
  "execution_log": [
    "解析输入参数",
    "执行核心处理",
    "格式化输出结果"
  ],
  "error": null
}
```
