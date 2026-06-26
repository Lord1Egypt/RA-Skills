# Outlook PyWin32 命令行工具

基于 pywin32 的 Outlook 本地自动化工具，无需 OAuth，直接操作本地 Outlook 客户端。

## 功能特性

- ✅ **邮件管理**
  - 创建新邮件并保存到草稿箱
  - 列出文件夹中的邮件
  - 读取指定邮件内容
  - 搜索邮件（支持关键词和时间范围）
  - 列出所有邮件文件夹
- ✅ **日历管理**
  - 列出即将举行的日程安排事件
  - 创建日程安排事件
  - 修改日程安排事件（仅保存，不发送通知）
  - 支持必需/可选参与人
  - 支持全天事件
  - 支持提醒设置
- ✅ **账户管理**
  - 列出所有可用的 Outlook 邮箱账户
  - 支持多账户切换
- ✅ **文件夹管理**
  - 列出所有默认文件夹

## 前提条件

无论使用哪种安装方法，都需要满足以下条件：

- Windows 系统
- 已安装 Outlook 客户端
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

## 快速开始

### 1. 查看可用方法

```bash
python scripts/outlook-pywin32.py
```

### 2. 列出邮件文件夹

```bash
python scripts/outlook-pywin32.py mail-folders
```

### 3. 创建一封新邮件

```bash
python scripts/outlook-pywin32.py mail-new --to user@example.com --subject "测试邮件" --body "这是一封测试邮件"
```

### 4. 列出日程安排

```bash
python scripts/outlook-pywin32.py calendar-list
```

### 5. 创建一个日程

```bash
python scripts/outlook-pywin32.py calendar-new --subject "团队会议" --start "2026-03-13 14:00:00" --location "会议室A"
```

## 详细文档

完整的使用文档请参见 [SKILL.md](./SKILL.md)。

## 配置

### 配置文件

在 `scripts` 目录下创建 `config.json` 文件，可配置默认邮箱账户：

```json
{
  "outlook_account": "your.email@example.com"
}
```

### 环境变量

- `OUTLOOK_ACCOUNT`: 默认邮箱账户地址（优先级高于配置文件）

## 使用示例

### 邮件相关

```bash
# 列出可用的 Outlook 账户
python scripts/outlook-pywin32.py account-list

# 列出收件箱前 10 封邮件
python scripts/outlook-pywin32.py mail-list --folder inbox --limit 10

# 读取第 1 封邮件
python scripts/outlook-pywin32.py mail-read --folder inbox --index 1

# 搜索包含"发票"关键词的邮件
python scripts/outlook-pywin32.py mail-search --query "发票"

# 搜索指定时间范围的邮件
python scripts/outlook-pywin32.py mail-search --start-time 2024-01-01 --end-time 2024-12-31
```

### 日历相关

```bash
# 列出未来 3 天的日程（不包含今天）
python scripts/outlook-pywin32.py calendar-list --days 3 --include-today false

# 创建带有参与人的日程
python scripts/outlook-pywin32.py calendar-new \
  --subject "项目评审" \
  --start "2026-03-14 10:00:00" \
  --end "2026-03-14 11:30:00" \
  --location "会议室A" \
  --required-attendees "zhangsan@example.com;lisi@example.com" \
  --optional-attendees "wangwu@example.com"

# 创建全天事件
python scripts/outlook-pywin32.py calendar-new --subject "公司年会" --start "2026-03-15" --all-day true

# 修改日程（通过主题搜索）
python scripts/outlook-pywin32.py calendar-edit --subject "团队会议" --new-subject "团队会议（已修改）" --location "新会议室"

# 修改日程（通过开始时间搜索）
python scripts/outlook-pywin32.py calendar-edit --start "2026-03-14 10:00:00" --new-start "2026-03-14 10:30:00" --new-end "2026-03-14 12:00:00"
```

## 项目结构

```
outlook-pywin32/
├── scripts/
│   ├── outlook-pywin32.py      # 主程序入口
│   ├── config.json              # 配置文件（可选）
│   └── outlook_pywin32/
│       ├── __init__.py
│       ├── utils.py             # 公共工具函数
│       ├── account.py           # 账户相关方法
│       ├── mail.py              # 邮件相关方法
│       ├── calendar.py          # 日历相关方法
│       └── folder.py            # 文件夹相关方法
├── SKILL.md                     # 详细使用文档
├── README.md                    # 本文件
└── ...
```

## 许可证

本项目仅供学习和个人使用。

## 贡献

欢迎提交 Issue 和 Pull Request！

## 注意事项

- 此工具仅在 Windows 系统上运行
- 需要本地安装 Outlook 客户端
- 首次运行时，Outlook 可能会弹出安全警告，需要允许访问
- 可能需要管理权限

