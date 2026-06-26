---
name: m5-email-reader
description: 只读邮件助手，通过 POP3 协议读取163、QQ、Gmail、Outlook等任意邮箱的邮件。支持：查询邮件总数、获取最近若干封邮件的标题列表、读取邮件完整内容（正文+附件信息）、按序号读取指定邮件、按关键词搜索邮件主题。当用户询问"帮我看看邮件"、"读一下邮箱"、"邮件里有没有XX"、"最近有什么邮件"、"查一下邮箱里的验证码"等邮件读取相关需求时使用。
---

# Email Reader

通过 POP3 SSL 协议只读邮箱，支持任意标准 POP3 邮箱。所有操作**只读**，不会删除或修改邮件。

## 核心脚本

`scripts/email_reader.py` — 所有功能入口，JSON 输出。

```bash
# 查总数
python3 scripts/email_reader.py count

# 最近 10 封标题（仅头部，速度快）
python3 scripts/email_reader.py subjects --n 10

# 最近 5 封完整内容（含正文）
python3 scripts/email_reader.py list --n 5

# 按序号读指定邮件
python3 scripts/email_reader.py read --index 42

# 在最近 100 封中搜索主题含关键词的邮件
python3 scripts/email_reader.py search --keyword 验证码 --range 100
```

## 配置方式（三层优先级，高优先级覆盖低优先级）

### 方式 1：命令行参数（最高优先级，适合临时测试）

```bash
python3 scripts/email_reader.py \
  --user your@163.com \
  --pass_ YOUR_AUTH_CODE \
  --server pop.163.com \
  --port 995 \
  subjects --n 5
```

### 方式 2：环境变量（推荐，安全可靠）

```bash
export EMAIL_USER="your@163.com"
export EMAIL_PASS="YOUR_AUTH_CODE"
export POP3_SERVER="pop.163.com"
export POP3_PORT="995"
python3 scripts/email_reader.py subjects --n 5
```

在 OpenClaw 中，可通过 `gateway config.patch` 将环境变量写入全局配置：

```json
{
  "env": {
    "EMAIL_USER": "your@163.com",
    "EMAIL_PASS": "YOUR_AUTH_CODE",
    "POP3_SERVER": "pop.163.com",
    "POP3_PORT": "995"
  }
}
```

### 方式 3：.email_config 文件（适合本地使用，不推荐提交到版本库）

在 `scripts/` 目录下创建 `.email_config`：

```ini
[email]
user   = your@163.com
pass_  = YOUR_AUTH_CODE
server = pop.163.com
port   = 995
```

> ⚠️ **安全提醒**：`.email_config` 含明文密码，请确保文件权限为 `600`，并加入 `.gitignore`。

## 邮箱服务器配置

各邮箱 POP3 服务器地址和授权码获取方式，参见 `references/providers.md`。

**163邮箱快捷配置**：
- Server: `pop.163.com`，Port: `995`
- 需使用**授权码**而非登录密码（邮箱设置 → POP3/SMTP → 开启 → 获取授权码）

## 工作流程

1. 先询问用户的邮箱账号、授权码（密码）、邮箱类型
2. 根据邮箱类型查 `references/providers.md` 确认服务器地址
3. 决定配置方式（推荐环境变量），完成配置
4. 运行脚本，解析 JSON 输出后以自然语言回复用户

## 输出格式

脚本统一输出 JSON，agent 解析后转为自然语言回复用户。示例：

```json
{
  "total": 523,
  "emails": [
    {
      "index": 523,
      "subject": "【网易】您的账户安全提醒",
      "from": "noreply@163.com",
      "date": "2026-03-25 10:30:00"
    }
  ]
}
```

## 注意事项

- 首次连接慢属正常（POP3 需要完整下载邮件）
- `subjects` 子命令只拉取头部，比 `list` 快得多，适合先浏览再精读
- 邮件 `index` 从 1 开始，数字越大越新
- 正文超长时建议截取前 2000 字符展示
