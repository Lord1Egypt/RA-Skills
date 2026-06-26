# Last Words - 最后留言

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

一个 OpenClaw skill，用于在长时间无活动后自动向亲人发送最后留言。

## ✨ 功能特点

- 📝 **文字留言** - 记录想对亲人说的话
- 🎙️ **语音留言** - 支持录制或上传语音附件
- 📧 **邮件发送** - 自动发送邮件（包含语音附件）
- ⏰ **自动检测** - 10天/20天警告，30天自动发送
- 🐛 **调试模式** - 立即测试，无需等待30天
- 💬 **交互配置** - 通过聊天即可完成所有配置

## 📦 安装

### 方式一：通过 OpenClaw 安装（推荐）

```bash
openclaw skill install last-words
```

### 方式二：手动安装

```bash
cd ~/.openclaw/skills
git clone https://github.com/yourusername/last-words.git
```

## 🔧 配置

### 方式一：聊天交互配置（最简单）

直接在 OpenClaw 聊天中输入：

```
配置最后留言邮箱
```

然后按提示一步步输入：
1. 你的发件邮箱（QQ邮箱）
2. 邮箱授权码（**不是登录密码**，获取方式见下方）
3. 收件人邮箱（父母/亲人的邮箱）

配置完成后会自动测试发送。

### 方式二：使用 .env 文件

```bash
cd last-words
cp .env.example .env
# 编辑 .env 文件填入配置
nano .env
```

`.env` 文件示例：
```env
# 发件邮箱（QQ邮箱）
SMTP_USER=your-qq@qq.com

# 邮箱授权码（16位，不是登录密码）
SMTP_PASS=xxxxxxxxxxxxxxxx

# 收件人邮箱
CONTACT_EMAIL=parent@example.com
```

然后执行：
```bash
python3 scripts/configure_delivery.py --from-env
```

### 方式三：命令行配置

```bash
python3 scripts/configure_delivery.py \
  --method email \
  --contact "parent@example.com" \
  --smtp-host smtp.qq.com \
  --smtp-port 465 \
  --smtp-user "your-qq@qq.com" \
  --smtp-pass "your-auth-code"
```

## 📝 设置留言

### 通过聊天（推荐）

```
我想给我爸妈留下最后一句话
```

然后直接输入你想说的话，支持文字或语音。

### 通过命令行

```bash
# 保存文字留言
python3 scripts/save_message.py --message "爸爸妈妈我爱你们"

# 添加语音附件
python3 scripts/audio_manager.py save /path/to/voice.wav
```

## 🔑 获取 QQ 邮箱授权码

**注意：不是邮箱登录密码！**

1. 登录 [QQ邮箱网页版](https://mail.qq.com)
2. 点击顶部「设置」→「账户」
3. 找到「POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV服务」
4. 开启「POP3/SMTP服务」
5. 按提示获取 **16位授权码**

<details>
<summary>📷 图文教程（点击展开）</summary>

![设置入口](docs/images/qq-mail-settings.png)
![开启服务](docs/images/qq-mail-smtp.png)
![获取授权码](docs/images/qq-mail-auth.png)

</details>

## 🐛 调试模式

测试邮件发送，无需等待30天：

### 通过聊天

```
最后留言 开启调试模式
最后留言 立即发送测试
最后留言 关闭调试模式
```

### 通过命令行

```bash
# 开启调试模式
python3 scripts/debug_mode.py on

# 立即发送测试
python3 scripts/debug_mode.py send

# 关闭调试模式
python3 scripts/debug_mode.py off

# 查看状态
python3 scripts/debug_mode.py status
```

## ⏰ 设置定时检查

```bash
# 每天上午9点检查
openclaw cron add \
  --name "last-words-check" \
  --schedule "0 9 * * *" \
  --command "python3 ~/.openclaw/skills/last-words/scripts/check_activity.py"
```

或使用系统 cron：
```bash
crontab -e
# 添加：0 9 * * * python3 ~/.openclaw/skills/last-words/scripts/check_activity.py
```

## 📖 完整使用流程

```
1. 安装 skill
   → openclaw skill install last-words

2. 配置邮箱
   → 说"配置最后留言邮箱"并按提示输入

3. 设置留言
   → 说"我想给我爸妈留下最后一句话"
   → 输入文字或上传语音

4. 测试发送
   → 说"最后留言 开启调试模式"
   → 说"最后留言 立即发送测试"

5. 关闭调试
   → 说"最后留言 关闭调试模式"

6. 等待生效
   → 系统会自动检测，30天无活动后发送
```

## 📋 支持的邮箱

| 邮箱 | SMTP服务器 | 端口 | 说明 |
|------|-----------|------|------|
| QQ邮箱 | smtp.qq.com | 465 | 需要授权码 |
| 163邮箱 | smtp.163.com | 465 | 需要授权码 |
| Gmail | smtp.gmail.com | 587 | 需要应用专用密码 |
| Outlook | smtp.office365.com | 587 | 需要应用密码 |

## 🛠️ 命令参考

| 命令 | 说明 |
|------|------|
| `save_message.py --message "内容"` | 保存文字留言 |
| `audio_manager.py save <文件>` | 上传语音文件 |
| `audio_manager.py record` | 录制语音 |
| `audio_manager.py play` | 播放已保存语音 |
| `configure_delivery.py` | 配置邮件发送 |
| `check_activity.py` | 手动检查活动状态 |
| `debug_mode.py on/off/status/send` | 调试模式管理 |
| `get_status.py` | 查看当前配置状态 |
| `reset.py` | 重置所有数据 |

## 🏗️ 项目结构

```
last-words/
├── SKILL.md              # OpenClaw skill 定义
├── README.md             # 本文档
├── .env.example          # 环境变量示例
├── .gitignore            # Git 忽略文件
├── scripts/
│   ├── database.py       # 数据库管理
│   ├── save_message.py   # 保存留言
│   ├── audio_manager.py  # 语音管理
│   ├── configure_delivery.py  # 配置邮件
│   ├── check_activity.py # 活动检查
│   ├── debug_mode.py     # 调试模式
│   ├── get_status.py     # 查看状态
│   └── reset.py          # 重置数据
└── docs/                 # 文档和图片
```

## 🔒 隐私与安全

- ✅ 所有数据存储在本地 SQLite 数据库
- ✅ 密码存储在本地，不上传任何服务器
- ✅ `.env` 文件已加入 `.gitignore`，不会被提交
- ✅ 支持通过聊天交互配置，避免密码泄露在命令历史中

## 🐛 常见问题

<details>
<summary><b>Q: 授权码是什么？和邮箱密码有什么区别？</b></summary>

A: 授权码是邮箱提供的第三方应用专用密码，不是登录密码。以 QQ 邮箱为例：
- 登录密码：你平时登录邮箱的密码
- 授权码：16位随机字符，专门用于 SMTP 发送邮件

获取方式：QQ邮箱 → 设置 → 账户 → 开启SMTP服务 → 获取授权码

</details>

<details>
<summary><b>Q: 支持哪些邮箱？</b></summary>

A: 目前测试支持：QQ邮箱、163邮箱、Gmail、Outlook。理论上支持所有提供 SMTP 服务的邮箱。

QQ邮箱和163邮箱使用 SSL（465端口），Gmail和Outlook使用 STARTTLS（587端口）。

</details>

<details>
<summary><b>Q: 如何确认留言已设置成功？</b></summary>

A: 三种方式：
1. 说"最后留言 调试状态"查看配置
2. 运行 `python3 scripts/get_status.py`
3. 开启调试模式后立即发送测试

</details>

<details>
<summary><b>Q: 30天是怎么计算的？</b></summary>

A: 从你最后一次与 OpenClaw 对话开始计算。每天定时检查：
- 10天无活动：发送第一次警告（给你）
- 20天无活动：发送第二次警告（给你）
- 30天无活动：自动发送最后留言（给父母）

只要你在30天内与 OpenClaw 说过话，计时就会重置。

</details>

<details>
<summary><b>Q: 可以修改留言吗？</b></summary>

A: 可以，随时可以：
- 说"我想给我爸妈留下最后一句话"重新设置
- 或直接运行 `python3 scripts/save_message.py --message "新内容"`

新留言会覆盖旧留言。

</details>

## 🤝 贡献

欢迎提交 Issue 和 PR！

1. Fork 本项目
2. 创建你的 Feature Branch (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到 Branch (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证

[MIT](LICENSE) © 2024 OpenClaw Community

---

**⚠️ 重要提醒**

本项目涉及敏感的个人告别信息，请：
- 确保亲人知道这个功能的存在
- 定期测试确保邮件能正常发送
- 保持邮箱授权码有效（过期需重新获取）
- 妥善保管你的 OpenClaw 访问权限

愿这份技术能传递爱与牵挂，但更希望它永远不被触发。
