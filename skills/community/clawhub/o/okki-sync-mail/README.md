# 📧 OKKI Sync Mail

**版本：** 2.0.0  
**更新日期：** 2026-03-28  
**作者：** Farreach Electronic Sales Team

---

## 🎯 功能简介

**OKKI Sync Mail** 是一个完整的邮件自动化解决方案，专为外贸业务设计。集成了 OKKI CRM，实现邮件自动捕获、智能分类、自动同步跟进记录等功能。

### 核心功能

1. **📥 邮件自动捕获**
   - IMAP 自动监听新邮件
   - 自动归档到本地（Obsidian 兼容）
   - 自动匹配 OKKI 客户（域名 + 向量搜索）

2. **📤 邮件发送**
   - SMTP 发送邮件
   - dry-run 模式（预览不发）
   - 发送日志记录
   - 速率限制（50 封/小时）
   - 定时发送

3. **🔗 OKKI 自动同步**
   - inbound 邮件自动创建跟进记录（remark_type=102）
   - outbound 邮件自动创建跟进记录
   - 客户匹配（域名精确匹配 + 向量搜索回退）
   - 去重机制

4. **📋 邮件管理**
   - 创建/移动/删除邮件文件夹
   - 标记星标
   - 邮件规则/过滤器（自动分类）
   - 签名模板管理

5. **⚡ 性能优化**
   - IMAP/SMTP 连接池
   - 批量操作支持
   - 交互式模式

---

## 🚀 快速开始

### 1. 安装

```bash
# 从 clawhub 安装
clawhub install okki-sync-mail

# 或手动克隆
cd /Users/wilson/.openclaw/workspace/skills
git clone <repo> okki-sync-mail
cd okki-sync-mail
npm install
```

### 2. 配置

创建 `.env` 文件：

```bash
# IMAP 配置（接收邮件）
IMAP_HOST=imaphz.qiye.163.com
IMAP_PORT=993
IMAP_USER=your-email@example.com
IMAP_PASS=<授权码>
IMAP_TLS=true

# SMTP 配置（发送邮件）
SMTP_HOST=smtphz.qiye.163.com
SMTP_PORT=465
SMTP_SECURE=true
SMTP_USER=your-email@example.com
SMTP_PASS=<授权码>

# OKKI 配置
OKKI_CLI_PATH=/Users/wilson/.openclaw/workspace/xiaoman-okki/api/okki_cli.py
VECTOR_SEARCH_PATH=/Users/wilson/.openclaw/workspace/vector_store/okki_vector_search_v3.py

# 安全配置
SMTP_RATE_LIMIT=50  # 每小时最多发送 50 封
ALLOWED_READ_DIRS=/Users/wilson/.openclaw/workspace
```

### 3. 基本使用

#### 检查新邮件

```bash
cd /Users/wilson/.openclaw/workspace/skills/okki-sync-mail

# 检查最新 10 封邮件（自动同步 OKKI）
node auto-capture.js check 10

# 只检查未读邮件
node auto-capture.js check --unseen
```

#### 发送邮件

```bash
# 简单邮件
node scripts/smtp.js send \
  --to "customer@example.com" \
  --subject "Product Inquiry" \
  --body "Hi, thanks for your inquiry..."

# 带附件
node scripts/smtp.js send \
  --to "customer@example.com" \
  --subject "Quotation" \
  --body "Please find attached quotation." \
  --attach "/path/to/quotation.pdf"

# dry-run 模式（预览不发）
node scripts/smtp.js send \
  --to "customer@example.com" \
  --subject "Test" \
  --body "Test email" \
  --dry-run

# 定时发送
node scripts/smtp.js send \
  --to "customer@example.com" \
  --subject "Scheduled Email" \
  --body "This will be sent later." \
  --send-at "2026-03-29 09:00"
```

#### 邮件管理

```bash
# 创建文件夹
node scripts/imap.js create-mailbox "Customers/USA"

# 移动邮件
node scripts/imap.js move-mail 12345 "Customers/USA"

# 标记星标
node scripts/imap.js flag-mail 12345 --starred

# 删除邮件
node scripts/imap.js delete-mail 12345
```

---

## 📋 完整命令参考

### IMAP 命令

| 命令 | 说明 | 示例 |
|------|------|------|
| `check` | 检查新邮件 | `node scripts/imap.js check --limit 10` |
| `fetch` | 获取完整邮件 | `node scripts/imap.js fetch <UID>` |
| `search` | 搜索邮件 | `node scripts/imap.js search --from "customer@" --limit 5` |
| `download` | 下载附件 | `node scripts/imap.js download <UID> --dir ./attachments` |
| `mark-read` | 标记已读 | `node scripts/imap.js mark-read <UID1> <UID2>` |
| `mark-unread` | 标记未读 | `node scripts/imap.js mark-unread <UID>` |
| `create-mailbox` | 创建文件夹 | `node scripts/imap.js create-mailbox "Customers"` |
| `move-mail` | 移动邮件 | `node scripts/imap.js move-mail <UID> <mailbox>` |
| `delete-mail` | 删除邮件 | `node scripts/imap.js delete-mail <UID>` |
| `flag-mail` | 标记星标 | `node scripts/imap.js flag-mail <UID> --starred` |
| `list-mailboxes` | 列出文件夹 | `node scripts/imap.js list-mailboxes` |

### SMTP 命令

| 命令 | 说明 | 示例 |
|------|------|------|
| `send` | 发送邮件 | `node scripts/smtp.js send --to "..." --subject "..." --body "..."` |
| `send --dry-run` | 预览不发 | `node scripts/smtp.js send --dry-run ...` |
| `send --send-at` | 定时发送 | `node scripts/smtp.js send --send-at "2026-03-29 09:00" ...` |
| `send --signature` | 使用签名模板 | `node scripts/smtp.js send --signature "en-sales" ...` |
| `test` | 测试连接 | `node scripts/smtp.js test` |

### 自动捕获命令

| 命令 | 说明 | 示例 |
|------|------|------|
| `check` | 检查并处理邮件 | `node auto-capture.js check 10` |
| `check --unseen` | 只检查未读 | `node auto-capture.js check --unseen` |
| `test` | 测试连接 | `node auto-capture.js test` |

### 发送日志命令

| 命令 | 说明 | 示例 |
|------|------|------|
| `recent` | 查看最近发送 | `node scripts/send-log.js recent 10` |
| `search` | 搜索发送记录 | `node scripts/send-log.js search subject "Quotation"` |
| `stats` | 查看统计 | `node scripts/send-log.js stats` |

---

## 🔗 OKKI 集成

### 跟进记录类型（remark_type）

| remark_type | 说明 | 使用场景 |
|-------------|------|----------|
| 101 | 快速记录 | 一般跟进 |
| **102** | **关联邮件备注** | 发送开发信/报价单后 |
| 110 | 邮件 | 邮件往来记录 |
| 103 | 电话 | 电话沟通 |
| 104 | 会面 | 客户拜访/来访 |
| 105 | 社交平台 | LinkedIn/微信等 |

### 自动同步流程

```
收到邮件 → 解析发件人 → 匹配 OKKI 客户 → 创建跟进记录 → 本地归档
                                                                  ↓
                                                           Obsidian 同步
```

### 客户匹配规则

1. **域名精确匹配** - 从邮箱域名匹配 OKKI 客户
2. **公共域名过滤** - 过滤 gmail.com, hotmail.com 等公共域名
3. **向量搜索回退** - 域名不匹配时使用向量搜索
4. **去重机制** - 相同 UID 不重复创建跟进记录

---

## 📁 目录结构

```
okki-sync-mail/
├── scripts/
│   ├── imap.js              # IMAP CLI 工具
│   ├── smtp.js              # SMTP CLI 工具
│   └── send-log.js          # 发送日志工具
├── signatures/              # 签名模板
│   ├── signature-en-sales.json
│   ├── signature-cn-sales.json
│   └── ...
├── scheduled/               # 定时发送队列
├── rules.json               # 邮件规则配置
├── auto-capture.js          # 自动捕获脚本
├── okki-sync.js             # OKKI 同步模块
├── rule-engine.js           # 规则引擎
├── .env                     # 配置文件（敏感）
├── SKILL.md                 # 技能文档
├── INTEGRATION.md           # 集成说明
└── README.md                # 本文档
```

---

## ⚙️ 高级配置

### 邮件规则配置

编辑 `rules.json`：

```json
{
  "rules": [
    {
      "name": "询价高优先级",
      "conditions": {
        "subject_contains": ["询价", "quotation", "RFQ"]
      },
      "action": {
        "priority": "high",
        "category": "inquiry"
      }
    },
    {
      "name": "广告低优先级",
      "conditions": {
        "subject_contains": ["推广", "promotion", "unsubscribe"]
      },
      "action": {
        "priority": "low",
        "category": "spam"
      }
    }
  ]
}
```

### 签名模板配置

在 `signatures/` 目录创建模板：

```json
{
  "name": "Sales Team - English",
  "signature": {
    "name": "[Your Name]",
    "title": "Sales Manager",
    "company": "Farreach Electronic Co., Limited",
    "address": [
      "Add: No. 56, Xingwang Road, Pingshan Town, Jinwan District, Zhuhai, Guangdong, China",
      "Add: Van Lam Industrial Park, Yen My District, Hung Yen Province, Vietnam"
    ],
    "email": "your-email@example.com",
    "tel": "+86 (756) 8699660",
    "website": "www.farreach-cable.com",
    "tagline": "18 Years | HDMI Certified | ISO9001 | China + Vietnam Dual Base"
  }
}
```

### 定时任务（Cron）

```bash
# 每 30 分钟检查新邮件
*/30 * * * * cd /Users/wilson/.openclaw/workspace/skills/okki-sync-mail && node auto-capture.js check --unseen >> /tmp/mail-capture.log 2>&1
```

---

## 🧪 测试

```bash
# 测试 IMAP 连接
node auto-capture.js test

# 测试 SMTP 连接
node scripts/smtp.js test

# 测试 OKKI 同步
node okki-sync.js test

# 测试规则引擎
node rule-engine.js test
```

---

## 🐛 故障排除

### IMAP 连接失败

```bash
# 检查网络
ping imaphz.qiye.163.com

# 检查端口
telnet imaphz.qiye.163.com 993

# 查看错误日志
node auto-capture.js check 2>&1 | tee /tmp/mail-error.log
```

### 登录失败

- 确认授权码是否正确
- 确认邮箱已开启 IMAP/SMTP 服务
- 联系邮箱管理员检查账户状态

### OKKI 同步失败

```bash
# 测试 OKKI CLI
python3 /Users/wilson/.openclaw/workspace/xiaoman-okki/api/okki_cli.py list_users

# 测试向量搜索
python3 /Users/wilson/.openclaw/workspace/vector_store/okki_vector_search_v3.py search "测试"
```

---

## 📝 更新日志

### v2.0.0 (2026-03-28)

**新增功能：**
- ✅ dry-run 模式（预览不发）
- ✅ 发送日志记录
- ✅ 速率限制（50 封/小时）
- ✅ inbound 邮件 OKKI 同步
- ✅ 签名模板管理
- ✅ 邮件规则/过滤器
- ✅ 移动邮件到文件夹
- ✅ 连接池优化
- ✅ 定时发送
- ✅ 交互式模式
- ✅ 邮件预览功能

**修复：**
- ✅ 修复 OKKI API 参数错误（trail_type → remark_type）
- ✅ 修复 dry-run 参数解析问题

### v1.0.0 (2026-03-09)

- 初始版本
- IMAP/SMTP 基本功能
- OKKI 基础集成

---

## 📄 许可证

MIT License

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📞 支持

- **文档：** `/Users/wilson/.openclaw/workspace/skills/okki-sync-mail/SKILL.md`
- **问题报告：** 创建 Issue
- **Farreach 知识库：** `/Users/wilson/obsidian-vault/Farreach 知识库/`
