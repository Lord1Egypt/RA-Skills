# 📅 iCloud Calendar Skill — 安装与配置指南

完整从 0 到 1 的配置流程。大约需要 5 分钟。

---

## 📋 你需要准备什么

| 项目 | 说明 | 状态 |
|------|------|:----:|
| **iCloud 账号** | Apple ID 邮箱 (your@icloud.com) | ✅ 必须有 |
| **App-Specific Password** | Apple 生成的专用应用密码 (非登录密码!) | ⬜ 需要生成 |
| **Python 3.8+** | 运行脚本的解释器 | ⬜ 需要安装 |
| **OpenClaw** | 宿主框架 | ✅ 已安装 |

---

## 🔑 第一步：生成 iCloud 专用密码（App-Specific Password）

> ⚠️ 这不是你的 Apple ID 登录密码！Apple 要求第三方应用使用"专用密码"。

1. 打开浏览器访问 [appleid.apple.com](https://appleid.apple.com)
2. 登录你的 Apple ID
3. 进入 **Sign-In and Security**（登录与安全）→ **App-Specific Passwords**（专用密码）
4. 点击 **Generate an app-specific password**（生成专用密码）或 `+` 按钮
5. 输入密码标签（如 "OpenClaw Calendar"），点击 **Create**（创建）
6. 系统显示一个 **`xxxx-xxxx-xxxx-xxxx`** 格式的密码 → **立即复制保存**，关闭页面后就看不到了

### ❓ 常见问题

**Q：找不到 App-Specific Passwords 选项？**  
A：确认你已开启双重认证（Sign-In and Security → Two-Factor Authentication）。

**Q：密码格式是什么？**  
A：`xxxx-xxxx-xxxx-xxxx`，16 位，4 组用 `--` 连接。

**Q：可以重复使用已生成的密码吗？**  
A：可以。但如果忘记密码，只能重新生成一个新的，旧密码无法查看。

---

## 🐍 第二步：安装 Python 依赖

打开终端运行：

```bash
# 检查 Python 版本（需要 3.8+）
python --version

# 安装 caldav 库（版本锁定 >=1.3.0,<2.0）
pip install "caldav>=1.3.0,<2.0"
```

### ❓ 常见问题

**Q：`pip` 不是内部命令？**  
A：尝试 `python -m pip install "caldav>=1.3.0,<2.0"`

**Q：Windows PowerShell 执行策略报错？**  
A：以管理员身份运行：`Set-ExecutionPolicy RemoteSigned -Scope CurrentUser`

---

## ⚙️ 第三步：配置 OpenClaw 环境变量

编辑 OpenClaw 配置文件 `~/.openclaw/openclaw.json`（或你的配置路径），在 `skills.entries` 中添加 `calendar-add` 条目：

```json
{
  "skills": {
    "entries": {
      "calendar-add": {
        "env": {
          "ICLOUD_EMAIL": "your-email@icloud.com",
          "ICLOUD_APP_PASSWORD": "xxxx-xxxx-xxxx-xxxx"
        }
      }
    }
  }
}
```

替换：
- `"your-email@icloud.com"` → 你的 iCloud 账号邮箱
- `"xxxx-xxxx-xxxx-xxxx"` → 第一步生成的专用密码

> ⚠️ **安全提醒：**
> - 凭据**只能**通过环境变量传递，脚本不接受 `--email` 或 `--password` 命令行参数
> - 确保 `openclaw.json` 文件权限为 `600`（仅你的用户可读）
> - 如果配置文件被其他人读取，你的 iCloud 日历就会被访问

---

## 🔄 第四步：重启 OpenClaw 使配置生效

```bash
openclaw gateway restart
```

重启后环境变量 `ICLOUD_EMAIL` 和 `ICLOUD_APP_PASSWORD` 会被注入到脚本的运行环境中。

---

## ✅ 第五步：验证安装

### 测试 1：列出你的日历

```bash
python skills/calendar-add/scripts/add-event.py --list-calendars
```

预期输出（JSON 数组，包含你 iCloud 中的所有日历）：
```json
[{"index": 0, "name": "个人"}, {"index": 1, "name": "工作"}]
```

如果看到错误：
- `"Authentication failed"` → 检查邮箱和密码是否正确
- `"Connection failed"` → 检查网络连接，确认 iCloud 可以访问

### 测试 2：查询今天的日程

```bash
python skills/calendar-add/scripts/add-event.py --query today
```

预期：返回今天的日程列表（如果没有则返回空数组）。

### 测试 3：创建一个测试事件

```bash
python skills/calendar-add/scripts/add-event.py \
    --summary "测试日程" \
    --start "2026-12-25T10:00:00" \
    --end "2026-12-25T11:00:00" \
    --calendar "个人"
```

预期：返回成功 JSON，然后在 iPhone 日历 App 中可以看到该事件。

---

## 🔒 安全机制说明

| 机制 | 说明 |
|------|------|
| **凭据零泄露** | 所有认证信息仅通过环境变量传递，进程列表看不到 |
| **异常脱敏** | 错误消息不包含 token/headers/bearer 等敏感信息 |
| **删除防护** | `--delete` 需要 `CONFIRM_DELETE=1` 才能执行 |
| **更新防护** | `--update-find` 需要 `CONFIRM_UPDATE=1` 才能执行 |
| **Dry Run** | 删除前可设 `DELETE_DRY_RUN=1` 预览不执行 |
| **日志轮转** | 日志最多 512KB × 5 备份 = 2.5MB，自动清理旧日志 |
| **内容截断** | 日志中事件标题/摘要截断至 30 字符 |

---

## 📂 文件结构

```
skills/calendar-add/
├── SKILL.md          # 技能说明（Agent 如何调用）
├── CONFIG.md         # 本文档（安装配置指南）
├── CHANGELOG.md      # v1.4.0 → v2.0.0 全量变更日志
├── scripts/
│   └── add-event.py  # 主脚本（v2.0.0）
├── logs/
│   └── calendar.log  # 操作日志（自动轮转）
└── test_add_event.py # 测试套件（95 个 case）
```

---

## ❓ 常见故障排查

| 错误 | 原因 | 解决方法 |
|------|------|----------|
| `Missing ICLOUD_EMAIL or ICLOUD_APP_PASSWORD` | 环境变量未设置 | 检查 openclaw.json 是否配置并重启 |
| `Authentication failed` | App Password 错误或账号不对 | 重新生成 App-Specific Password |
| `Connection failed` | iCloud CalDAV 不可达 | 检查网络/防火墙，确认 `caldav.icloud.com` 可达 |
| `No calendars found` | 日历服务未启用 | 登录 iCloud 网页版 → 日历 → 确认有日历 |
| `Unknown timezone` | 时区名拼写错误 | 使用标准 IANA 时区名，如 `Asia/Shanghai` |
| `Delete requires CONFIRM_DELETE` | 未设确认标志 | 运行前设 `CONFIRM_DELETE=1` 环境变量 |

---

## 📞 需要帮助？

- 技术文档：<https://docs.openclaw.ai>
- 社区讨论：<https://discord.com/invite/clawd>
