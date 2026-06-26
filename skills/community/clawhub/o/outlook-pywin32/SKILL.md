***

name: outlook-pywin32
description: "通过pywin32本地操作Outlook的命令行工具。支持邮件管理、日历管理、账户管理和文件夹管理等功能。使用命令: outlook-pywin32.py <方法名> --参数 值"
----------------------------------------------------------------------------------------------

# Outlook PyWin32 命令行工具

## 版本更新

### v0.8

**新增功能：**

- 重构代码结构，将功能模块拆分为独立文件
- 添加 `folder-list` 方法，支持列出所有默认文件夹
- 优化代码组织，提高可维护性

### v0.7

**新增功能：**

- 添加 `calendar-edit` 方法，支持修改日程安排事件
- 支持通过主题或开始时间搜索日程
- 支持修改日程的各种属性（主题、时间、地点、参与人等）
- 修改后仅保存，不发送通知

**修复的bug：**

- 修复了 `calendar-list` 和 `calendar-edit` 方法中当指定账户不存在时的错误
- 优化了时间匹配逻辑，提高搜索可靠性

## 前提条件

基于pywin32的Outlook本地自动化工具，无需OAuth，直接操作本地Outlook。

无论使用哪种安装方法，都需要满足以下条件：

- Windows系统
- 已安装Outlook客户端
- Python 3.7+
- pywin32 库

## 安装

### 方法一：通过 ClawHub 安装（推荐）

```bash
clawhub install outlook-pywin32
```

### 方法二：手动安装

克隆或下载此项目

## 安装依赖

```bash
pip install pywin32
```

## 用法

```bash
python scripts/outlook-pywin32.py <方法名> --参数 值 --参数2 值2
```

## 可用方法

### 邮件相关

| 方法           | 说明               | 参数                                                    |
| ------------ | ---------------- | ----------------------------------------------------- |
| mail-folders | 检查并列出邮件文件夹       | --account                                             |
| mail-new     | 创建邮件并保存到草稿箱      | --to, --subject, --body, --cc, --bcc                  |
| mail-list    | 列出邮件             | --folder, --limit, --account                          |
| mail-read    | 读取邮件             | --folder, --index, --account                          |
| mail-search  | 搜索邮件             | --query, --limit, --account, --start-time, --end-time |
| account-list | 列出所有可用的Outlook账户 | 无                                                     |

### 文件夹相关

| 方法           | 说明               | 参数                                                    |
| ------------ | ---------------- | ----------------------------------------------------- |
| folder-list  | 列出所有默认文件夹       | --account                                             |

### 日历相关

| 方法            | 说明                    | 参数                                                                                                                                                          |
| ------------- | --------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| calendar-list | 列出即将举行的日程安排事件         | --limit, --days, --include-today, --account                                                                                                                 |
| calendar-new  | 创建一个日程安排事件            | --subject, --start, --end, --location, --body, --required-attendees, --optional-attendees, --all-day, --reminder, --account                                 |
| calendar-edit | 修改一个日程安排事件（仅保存，不发送通知） | --subject, --start, --new-subject, --new-start, --new-end, --location, --body, --required-attendees, --optional-attendees, --all-day, --reminder, --account |

## 参数说明

### 通用参数

- `--account`: 邮箱账户地址（可选）
  - 优先级：1. 传入参数 2. 环境变量 OUTLOOK\_ACCOUNT 3. config.json 文件

### 邮件相关参数

#### mail-search 特有参数

- `--query`: 搜索关键词（可选）
- `--start-time`: 起始时间（可选，如 2024-01-01 或 2024-01-01 09:00:00）
  - 只指定日期时，默认设置为 00:00:00
- `--end-time`: 结束时间（可选，如 2024-12-31 或 2024-12-31 18:00:00）
  - 只指定日期时，默认设置为 23:59:59

### 日历相关参数

#### calendar-list 特有参数

- `--limit`: 返回数量（默认10）
- `--days`: 查看未来几天的事件（默认7）
- `--include-today`: 是否包含今天的事件（true/false，默认true）

#### calendar-new 特有参数

- `--subject`: 日程主题（必需）
- `--start`: 开始时间（格式: YYYY-MM-DD HH:MM:SS 或 YYYY-MM-DD）
- `--end`: 结束时间（可选，默认开始时间+30分钟）
- `--location`: 地点（可选）
- `--body`: 备注（可选）
- `--required-attendees`: 必需参与人（多个用分号分隔）
- `--optional-attendees`: 可选参与人（多个用分号分隔）
- `--all-day`: 是否全天事件（true/false，默认false）
- `--reminder`: 提醒提前分钟数（默认15, 0表示不提醒）

## 配置文件

在 scripts 目录下创建 `config.json` 文件，可配置默认邮箱账户：

```json
{
  "outlook_account": "xx@cuhk.edu.cn"
}
```

## 环境变量

- `OUTLOOK_ACCOUNT`: 默认邮箱账户地址

## 示例

### 邮件相关示例

```bash
# 列出可用的Outlook账户
python scripts/outlook-pywin32.py account-list

# 检查邮件文件夹
python scripts/outlook-pywin32.py mail-folders

# 创建邮件
python scripts/outlook-pywin32.py mail-new --to user@example.com --subject "测试" --body "你好"

# 列出收件箱前10封邮件
python scripts/outlook-pywin32.py mail-list --folder inbox --limit 10

# 列出指定账户的邮件
python scripts/outlook-pywin32.py mail-list --account xx@cuhk.edu.cn

# 读取第1封邮件
python scripts/outlook-pywin32.py mail-read --folder inbox --index 1

# 只按关键词搜索邮件
python scripts/outlook-pywin32.py mail-search --query "发票"

# 只按时间范围搜索邮件
python scripts/outlook-pywin32.py mail-search --start-time 2024-01-01 --end-time 2024-12-31

# 同时使用关键词和时间范围搜索
python scripts/outlook-pywin32.py mail-search --query "会议" --start-time 2024-01-01 --end-time 2024-12-31

# 使用config.json中的账户搜索
python scripts/outlook-pywin32.py mail-search --query "会议"
```

### 日历相关示例

```bash
# 列出未来7天的日程（包含今天）
python scripts/outlook-pywin32.py calendar-list

# 列出未来3天的日程（不包含今天）
python scripts/outlook-pywin32.py calendar-list --days 3 --include-today false

# 创建一个简单的日程
python scripts/outlook-pywin32.py calendar-new --subject "团队会议" --start "2026-03-13 14:00:00"

# 创建一个带有地点和参与人的日程
python scripts/outlook-pywin32.py calendar-new \
  --subject "项目评审" \
  --start "2026-03-14 10:00:00" \
  --end "2026-03-14 11:30:00" \
  --location "会议室A" \
  --required-attendees "zhangsan@example.com;lisi@example.com" \
  --optional-attendees "wangwu@example.com" \
  --body "讨论项目进展"

# 创建一个全天事件
python scripts/outlook-pywin32.py calendar-new --subject "公司年会" --start "2026-03-15" --all-day true --reminder 0
```

### 文件夹相关示例

```bash
# 列出所有默认文件夹
python scripts/outlook-pywin32.py folder-list

# 列出指定账户的默认文件夹
python scripts/outlook-pywin32.py folder-list --account xx@cuhk.edu.cn
```

