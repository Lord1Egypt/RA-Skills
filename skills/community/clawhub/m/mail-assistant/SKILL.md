---
name: email-assistant
description: Unified email management assistant supporting Outlook/M365 (OAuth2 via Microsoft Graph), 163, and QQ mailboxes. Use when the user wants to: (1) check/read/send emails across multiple accounts, (2) set up auto-reply rules, (3) summarize or draft emails with AI, (4) sync mailboxes on schedule, (5) manage attachments, CC/BCC, read/unread status, or filter/search emails by sender/keyword/date.
metadata:
  openclaw:
    requires:
      bins: [python3]
    install:
      - id: setup
        kind: shell
        label: "运行安装向导"
        command: "python3 skills/mail-assistant/scripts/setup_wizard.py"
        description: "交互式配置向导，添加邮箱账户并完成 OAuth 授权"
    settings:
      - key: accounts
        label: "已配置的邮箱账户"
        type: text
        readonly: true
        description: "查看当前已配置的邮箱账户。新增/删除邮箱由 Agent 自动处理，直接说出来即可"
      - key: sync
        label: "定时同步状态"
        type: text
        readonly: true
        description: "每小时自动同步，由 Agent 管理 cron 任务"
---

# Email Assistant

统一的邮箱管理助手，支持 **Outlook/Microsoft 365**（OAuth2）、**163 邮箱**、**QQ 邮箱**。

核心能力：收发邮件、AI 辅助撰写、自动回复规则、每小时定时同步。

---

### ⚠️ Agent 行为声明：用户同意要求

**Agent 在操作邮箱时必须遵守以下规则：**

| 操作类型 | 是否需要用户同意 | 说明 |
|----------|-----------------|------|
| 📬 查看邮件 | ❌ 不需要 | 只读操作，自动执行 |
| ✉️ 发送邮件 | ✅ **必须** | 发送前向用户展示摘要并确认。Agent 调用时附加 `--yes` 参数表示用户已同意 |
| 📑 标记已读/未读 | ✅ **必须** | 修改邮件状态前请求用户确认。Agent 使用 `--yes` 参数 |
| 🤖 添加/删除/切换自动回复规则 | ✅ **必须** | 修改规则前请求用户确认 |
| 📎 自动回复发送 | ✅ **必须** | 同步时不会自动发送回复，需用户手动确认或用 `--yes` 预先授权 |
| ⏰ 定时同步 | ✅ **首次需同意** | 首次设置时告知用户并确认 |

**实现机制：**
- Agent 需先向用户描述操作内容并取得同意
- 确认后 Agent 在 CLI 调用中附加 `--yes` 参数跳过交互提示
- 非交互终端（如 cron）默认拒绝所有需要确认的操作
- 系统密钥链（keyring）可用于加密存储凭证

---

---

## 📦 安装与配置（Agent 引导模式）

### 前置条件

- **Python 3.8+**（本 Skill 已安装 Python 脚本）
- **跨平台支持**：Windows / macOS / Linux 均可使用
- 无需手动运行脚本！Agent 会引导你完成设置

### 📋 配置流程（由 Agent 自动执行）

当用户说 "帮我配置邮箱" 时，Agent 按以下流程操作：

**1. 检查 accounts 目录**
```python
import os, json
from data_dir import ACCOUNTS_DIR
if not os.path.exists(ACCOUNTS_DIR):
    os.makedirs(ACCOUNTS_DIR)
# 列出已有配置
configs = [f for f in os.listdir(ACCOUNTS_DIR) if f.endswith(".json") and not f.endswith(".token.json")]
```

**2. Outlook — 创建账户配置**
```python
import json
from data_dir import ACCOUNTS_DIR
# 内置 Azure client_id（无需用户配置）
BUILTIN_CLIENT_ID = "c31fd78c-6385-4fd2-9033-d0bd72b5ceb4"

account = {
    "id": "my-outlook",
    "type": "outlook",
    "user": "",  # 空，登录后自动获取
    "oauth": {
        "client_id": BUILTIN_CLIENT_ID,
        "tenant_id": "consumers",
        "scopes": ["User.Read", "Mail.ReadWrite", "Mail.Send", "MailboxSettings.Read"],
    },
}
with open(os.path.join(ACCOUNTS_DIR, "my-outlook.json"), "w") as f:
    json.dump(account, f, indent=2)
```

**3. Outlook — 启动浏览器授权（直接 import）**
```python
import sys, os
sys.path.insert(0, "skills/mail-assistant/scripts")
import oauth_web
oauth_web.run_oauth_flow("my-outlook")
# 脚本会自动打开浏览器，用户登录后自动接收回调
```

**4. 163 / QQ 邮箱 — 创建配置**
```python
import json
from data_dir import ACCOUNTS_DIR
account = {
    "id": "my-163",  # 或 my-qq
    "type": "163",  # 或 qq
    "user": "user@163.com",
    "smtp": {"host": "smtp.163.com", "port": 465, "auth": "授权码"},
    "imap": {"host": "imap.163.com", "port": 993, "auth": "授权码"},
}
with open(os.path.join(ACCOUNTS_DIR, "my-163.json"), "w") as f:
    json.dump(account, f, indent=2)
```

**5. 测试连接（直接 import）**
```python
import sys, os
sys.path.insert(0, "skills/mail-assistant/scripts")
from outlook_api import list_inbox
list_inbox("my-outlook", limit=1)
```

**6. 设置定时同步（直接 import）**
```python
import sys
sys.path.insert(0, "skills/mail-assistant/scripts")
import sync_all
sync_all.cmd_sync()
```

也可以使用 setup_wizard.py 交互式配置：
```bash
python3 skills/mail-assistant/scripts/setup_wizard.py
```

---

## 🔑 添加邮箱账户（Agent 引导模式）

以下配置流程由 Agent 自动执行。参看上方「配置流程」节中的 Python 代码段。

### Outlook / Microsoft 365

用户只需说 "添加 Outlook 邮箱"，Agent 即可自动：
1. 创建 `accounts/my-outlook.json` 配置文件（内置 Azure 应用注册）
2. 通过 `import oauth_web` 直接调用启动浏览器授权
3. 用户登录 Microsoft 账户并授权
4. 完成配置

### 163 邮箱

用户提供邮箱地址和授权码，Agent 自动：
1. 创建 `accounts/my-163.json` 配置文件
2. 通过 `import email_client` 直接调用验证连接
3. 确认配置成功

### QQ 邮箱

用户提供邮箱地址和授权码，Agent 自动：
1. 创建 `accounts/my-qq.json` 配置文件
2. 通过 `import email_client` 直接调用验证连接
3. 确认配置成功

---

## 🚀 核心功能

| 功能 | 说明 |
|------|------|
| 📬 收件箱查看 | 列出邮件、预览详情、查看附件 |
| ✉️ 发送邮件 | 支持附件、CC、BCC，AI 辅助撰写 |
| 🔍 搜索筛选 | 按发件人/关键词/时间搜索 |
| 📑 标记已读/未读 | 管理邮件状态（操作会打印日志） |
| 🤖 自动回复 | 按域名/关键词设置自动回复规则（⚠️ 使用 --dry-run 预览） |
| ⏰ 定时同步 | 每小时自动同步（OpenClaw cron） |
| 🔄 手动同步 | `python3 scripts/sync_all.py`（支持 --dry-run） |

### 自然语言交互示例

| 你说 | 我做什么 |
|------|---------|
| "帮我查一下今天 Outlook 的邮件" | 读取 Outlook 收件箱，筛选今天的邮件 |
| "给 xx@qq.com 发一封请假邮件" | 撰写邮件 → 你确认 → 发送 |
| "总结最近 3 封重要邮件" | 提取最近邮件，用 LLM 总结 |
| "设置对老板的邮件自动回复" | 创建自动回复规则（先预览再启用） |
| "帮我把这封邮件标记为已读" | 调用 API 标记已读（打印操作日志） |

---

## 💻 编程式调用指南（供 Agent / 开发者使用）

本 Skill 的 Python 脚本既可作为 CLI 运行，也可作为 Python 模块导入。

**建议使用 import 方式调用**，令牌过期会自动刷新。

### Outlook / M365

```python
import sys
sys.path.insert(0, "skills/mail-assistant/scripts")

from outlook_api import list_inbox, read_mail, mark_read, mark_unread, search

# 列出最近 5 封未读邮件
list_inbox("my-outlook", limit=5, unread_only=True)

# 搜索邮件
search("my-outlook", "发票", limit=10)

# 读取单封邮件
read_mail("my-outlook", "<message-id>")

# 标记已读/未读
mark_read("my-outlook", "<message-id>")
mark_unread("my-outlook", "<message-id>")
```

所有函数打印 JSON 到 stdout。如需在 Python 中捕获返回值，使用 import 方式：

```python
import sys, json, io
sys.path.insert(0, "skills/mail-assistant/scripts")
from outlook_api import cmd_list_inbox, _get_token

token = _get_token("my-outlook")
old_stdout = sys.stdout
sys.stdout = io.StringIO()
try:
    cmd_list_inbox(token, ["", "", "--limit", "5"])
    output = sys.stdout.getvalue()
finally:
    sys.stdout = old_stdout
emails = json.loads(output)
```

### 163 / QQ 邮箱

```python
from email_client import list_inbox, read_mail, mark_read

list_inbox("my-qq", limit=5, unread_only=True)
read_mail("my-163", "<uid>")
```

### 自动回复规则

```python
import sys, json, io
sys.path.insert(0, "skills/mail-assistant/scripts")
import auto_reply

# 直接调用
old_stdout = sys.stdout
sys.stdout = io.StringIO()
try:
    auto_reply.cmd_list()
    rules_json = sys.stdout.getvalue()
finally:
    sys.stdout = old_stdout
rules = json.loads(rules_json)
```

### 手动同步

```python
import sys
sys.path.insert(0, "skills/mail-assistant/scripts")
import sync_all
sync_all.cmd_sync()
  # 或 sync_all.cmd_sync(dry_run=True) 预览
  # 或 sync_all.cmd_sync(account_filter="my-outlook") 同步单个账户
```

## 🔧 脚本参考

| 脚本 | 用途 |
|------|------|
| `scripts/setup_wizard.py` | 交互式配置向导（推荐） |
| `scripts/oauth_web.py` | Outlook 浏览器授权（PKCE + 本地服务器） |
| `scripts/oauth_manager.py` | OAuth2 令牌管理（auth/refresh/revoke） |
| `scripts/outlook_api.py` | Microsoft Graph API 调用 |
| `scripts/email_client.py` | SMTP/IMAP 发送（163/QQ） |
| `scripts/auto_reply.py` | 自动回复规则管理 |
| `scripts/sync_all.py` | 同步所有邮箱 + 触发自动回复 |
| `scripts/email_utils.py` | 工具函数（格式化、状态管理） |

### 数据持久化 & 脚本路径

邮箱账户配置、OAuth 令牌、同步状态和自动回复规则**存储在 skill 目录之外**，
位于 `~/.openclaw/workspace/.email-assistant/`，因此更新 skill 时不会丢失配置。

```
~/.openclaw/workspace/
├── .email-assistant/          ← 持久化数据（更新 skill 不受影响）
│   ├── accounts/              账户配置 + OAuth 令牌
│   ├── auto_reply_rules.json  自动回复规则
│   └── sync_state.json        同步状态
├── skills/mail-assistant/     ← skill 代码（可被 clawhub update 替换）
│   └── scripts/               Python 脚本
```

可通过环境变量 `EMAIL_ASSISTANT_DATA_DIR` 自定义数据目录路径。

脚本路径（供 Agent 调用）：
```python
import os
SCRIPTS_DIR = os.path.join("skills", "mail-assistant", "scripts")
```

如果 sandbox 环境不允许相对路径，可使用 `subprocess.run` 时设置 `cwd` 参数。

### 常见错误排查

| 报错 | 原因 | 解决方法 |
|------|------|----------|
| `Unsafe Login` 或 select INBOX 失败 | 163/QQ 邮箱安全检测 | 检查 IMAP 服务是否开启，授权码是否过期，重新生成授权码 |
| `IMAP login` 失败 | 授权码错误 | 在网页邮箱中重新生成授权码 |
| `SMTP Authentication` 失败 | SMTP 授权码错误 | 确认 SMTP 服务已开启，授权码正确 |
| `invalid_client` / `redirect_uri` 错误 | Azure 配置问题 | 确认 Azure 应用已添加移动平台重定向 URI: `http://localhost:1456` |
| `authorization_pending` | 用户未在浏览器完成授权 | 等待用户完成登录，或检查代码是否过期 |

---

## ⬆️ 升级指南（v1.5.x → v1.7.0）

### 数据持久化说明（v1.5.4+）

从 v1.5.4 开始，账户配置、OAuth 令牌、自动回复规则和同步状态**已迁移到 skill 目录之外**：

| 数据类型 | 旧位置（v1.5.3 及更早） | 新位置（v1.5.4+） |
|----------|------------------------|-------------------|
| 账户配置 | `skills/mail-assistant/accounts/` | `~/.openclaw/workspace/.email-assistant/accounts/` |
| OAuth 令牌 | `skills/mail-assistant/accounts/*.token.json` | 同上 |
| 自动回复规则 | `skills/mail-assistant/auto_reply_rules.json` | `~/.openclaw/workspace/.email-assistant/auto_reply_rules.json` |
| 同步状态 | `skills/mail-assistant/sync_state.json` | `~/.openclaw/workspace/.email-assistant/sync_state.json` |

**升级时配置不会丢失**，所有现有配置会自动迁移。具体流程：

1. **自动迁移**（推荐）：升级后首次运行任一脚本时，由 `data_dir.py` 自动处理
2. **手动迁移**：也可运行迁移脚本主动迁移：
   ```bash
   python3 scripts/migrate_data.py
   ```
3. **旧版兼容性**：如果旧配置仍在 skill 目录内，`data_dir.py` 会优先级检测并迁移
4. **自定义路径**：设置环境变量 `EMAIL_ASSISTANT_DATA_DIR` 可自定义数据目录

> **如果升级后找不到账户**：运行 `python3 scripts/migrate_data.py` 手动迁移旧数据。
> 该脚本会自动从 `skills/mail-assistant/accounts/` 复制到新位置，不会覆盖已有文件。

### v1.7.0 安全升级注意事项

本版本进行了大量安全加固。升级后：
- 无需重新配置已有账户
- 但建议运行一次全量同步验证功能正常：`python3 scripts/sync_all.py`
- OAuth 令牌会自动刷新，无需重新授权
- 163/QQ 授权码如有更新会提示重新输入

---

## 🔐 安全与隐私

### ⚠️ 安全审计声明

此 Skill 于 2026-06 经过 NVIDIA SkillSpector 安全审计。以下为已修复或需注意的安全事项。

### ✅ v1.7.0 已修复的安全问题

| 编号 | 问题 | 严重度 | 修复方式 |
|------|------|--------|----------|
| 1 | subprocess 命令执行 | 中 | 全部改为 Python 直接 import 调用 |
| 2 | OAuth state 未验证（CSRF） | 中 | callback 中校验 state 参数 |
| 3 | cmd_revoke 仅删除本地令牌 | 中 | 增加向 Microsoft 的 HTTP 撤销请求 |
| 4 | 自动回复匹配逻辑文档矛盾 | 中 | 文档修正为 AND 跨类型 / OR 类型内 |
| 5 | 缺少用户警告 | 可见下方 | 全面补充安全提示 |

### 已知安全注意事项（请用户知悉）

1. **共享 Azure 应用** — 本 Skill 内置的 Azure 应用注册由 Skill 开发者提供，所有用户共享。授权后将获得 Mail.ReadWrite + Mail.Send 等权限。如需更高安全性，可在 Azure 门户创建自己的应用注册。

2. **163/QQ 授权码明文存储** — 授权码以 JSON 明文存储在 `~/.openclaw/workspace/.email-assistant/accounts/` 目录中。请确保：
   - 该目录不被纳入版本控制（Git）
   - 定期在网页邮箱中重新生成授权码
   - 不再使用时及时在网页邮箱中撤销

3. **自动回复风险** — 自动回复功能可能形成邮件循环、放大垃圾邮件、或向不可信发件人泄露附件。建议：
   - 使用 `--dry-run` 预览后再启用
   - 配置 `sender_domains` 等具体匹配条件，避免 catch-all
   - 定期检查和清理自动回复规则

4. **邮件状态修改** — mark-read/mark-unread 操作直接修改邮箱状态，操作日志已记录。

### 安全最佳实践

- ✅ **系统密钥链加密存储**（v1.8.0+）：凭证优先存入操作系统密钥链（Windows Credential Manager / macOS Keychain / Linux Secret Service），而非仅明文 JSON。使用时临时解密，不影响速度。需安装 `pip install keyring`
- ✅ OAuth2 令牌本地存储，不离开本机
- ✅ 邮件正文不写入长期存储（MEMORY.md）
- ✅ 随时可通过以下命令完全撤销授权：
  ```
  python3 scripts/oauth_manager.py revoke <account-id>
  ```
  （此操作会向 Microsoft 发送令牌撤销请求并删除本地令牌文件）
- ✅ QQ/163 使用授权码而非密码
- ✅ 所有脚本调用改为直接 import，消除 subprocess 攻击面
- ✅ OAuth 流程增加 state 验证，防止 CSRF 攻击
- ✅ 自动回复增加安全警告和 dry-run 支持
- ✅ **所有写操作需用户确认**：发送邮件、标记已读/未读、修改自动回复规则均需用户同意后才能执行

---

## 📚 参考文档

- `references/microsoft_graph.md` — Microsoft Graph API 详细文档
- `references/email_protocols.md` — SMTP/IMAP 配置参考
- `references/auto_reply_rules.md` — 自动回复规则格式
