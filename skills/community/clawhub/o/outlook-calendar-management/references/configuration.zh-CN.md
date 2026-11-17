# 第一次连接日历

本工具通过 Microsoft Graph API（微软官方接口）操作日历，首次使用前需完成登录授权（一次性操作，之后自动续期）。
前置条件：Python 3.10+；依赖 requests/msal/tzdata 在首次运行时自动安装。

## 连接步骤（约 2 分钟）

从项目根目录运行；缺失依赖会自动安装。

```bash
python scripts/outlook_setup.py   # 无参数时使用内置默认应用
```

1. 脚本打印一个**验证码**
2. 浏览器打开 `https://www.microsoft.com/link`，输入验证码
3. 使用 Outlook 账户（微软账户）登录并授权。授权范围共 3 个权限，各自用途如下：

| 权限 | 官方描述 | 在本工具中的用途 |
|------|---------|-----------------|
| `Calendars.ReadWrite` | Have full access to user calendars（日历完全访问） | 全部日程操作：查看、添加、修改、移动、删除（走 `/me/events`、`/me/calendar*` 接口） |
| `MailboxSettings.Read` | Read user mailbox settings（读取邮箱设置） | 读取邮箱首选时区（`/me/mailboxSettings`），全天日程按它写入——机器时区与邮箱时区不同也不会跨天 |
| `User.Read` | Sign in and read user profile（登录并读取用户资料） | 设备码登录的基础权限：返回登录用户身份（姓名、邮箱）；`status` 显示当前账户 |

> 三者互不替代：`User.Read` 读"用户是谁"（身份资料，登录必需）；`MailboxSettings.Read` 读"邮箱设置了什么"（时区、语言等偏好，本工具取时区靠它）；`Calendars.ReadWrite` 读写"日程内容"。
4. 授权仍有效时自动续期；过期或被撤销后需要重新连接

> 从旧版本升级时请重跑一次 `python scripts/outlook_setup.py` 补上 `MailboxSettings.Read` 权限（本次授权会出现新的权限确认项）。

**确认成功**：`python scripts/outlook_cal.py status` 显示"✅ 已连接到 Outlook 日历"。

> 手机、电脑、网页上看到的是同一个日历——连接后所有操作实时同步。

## 换账户 / 重新连接

重新运行 `python scripts/outlook_setup.py` 即可用另一个账户授权（会覆盖当前连接）。
登录失效时（提示 invalid_grant / 401）同样如此。

## 想用自己的 Azure 应用？

默认开箱即用，通常无需操作。如需注册自己的应用（如出于安全隔离目的），见 `azure-app-setup.zh-CN.md`。
注册后仅需复制 **Client ID** 一个参数：`python scripts/outlook_setup.py <你的Client ID>`。

## 单独保存测试登录

在运行登录、日历命令之前，将 `OCAL_TOKEN_PATH` 设为单独的凭据文件，父目录需已存在。运行集成脚本时也保留此设置，其子进程会继承。未设置时仍使用 `~/.outlook_cal_token.json`。

从项目根目录运行的 PowerShell 示例：

```powershell
New-Item -ItemType Directory -Force .local-calendar-test | Out-Null
$env:OCAL_TOKEN_PATH = Join-Path (Get-Location) '.local-calendar-test/outlook-token.json'
python scripts/outlook_setup.py
python scripts/outlook_cal.py status --json
```

该目录已被 Git 忽略。单独的凭据文件保留原有登录，但不会创建独立日历：请登录准备使用的测试账户，写入前核对邮箱。
