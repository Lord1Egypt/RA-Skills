# 自动回复规则参考

规则存储在 `~/.openclaw/workspace/email-assistant/auto_reply_rules.json`。

## 规则格式

```json
{
  "id": "a1b2c3d4",
  "name": "外出自动回复 - 老板",
  "enabled": true,
  "match": {
    "to_addresses": ["me@company.com"],
    "sender_domains": [],
    "keywords_subject": ["紧急", "重要"],
    "keywords_body": []
  },
  "reply": {
    "subject_prefix": "Re: ",
    "body_template": "感谢您的邮件。我已收到，稍后将尽快回复。\n\n---\n此邮件由自动回复系统发送"
  },
  "created_at": 1687350000.0
}
```

## 匹配条件 (match)

匹配逻辑：**AND 跨条件类型，OR 单条件类型内**。

- 所有 **已配置** 的匹配条件类型都需要满足（AND 逻辑）
- 在 **同一个类型** 内，匹配任意一个值即可（OR 逻辑）
- 所有条件数组均为空 → 匹配全部邮件（catch-all）

| 字段 | 类型 | 说明 |
|------|------|------|
| `to_addresses` | string[] | 匹配收件人地址（邮件被发送到这些地址时触发） |
| `sender_domains` | string[] | 匹配发件人的邮件域名（如 `@company.com`） |
| `keywords_subject` | string[] | 匹配主题中的关键词（任一匹配即可） |
| `keywords_body` | string[] | 匹配正文中的关键词（任一匹配即可） |

**示例：**
- 所有条件数组均为空 → 匹配全部邮件（catch-all）
- 只有 `sender_domains=["@boss.com"]` → 任何来自 @boss.com 的邮件都匹配
- `sender_domains` + `keywords_subject` 同时设置 → 来自指定域名 **且** 主题包含关键词的邮件匹配

### ⚠️ 安全警告

**Catch-all（全部匹配）风险：**
- 会回复每一封收到的邮件，包括垃圾邮件、钓鱼邮件、自动通知
- 可能形成邮件循环（自动回复触发对方的自动回复，无限循环）
- 请谨慎使用 catch-all，尽量使用具体匹配条件

**附件泄露风险：**
- `attachments` 字段中的文件会随自动回复一起发送给每位匹配的发件人
- 如果 catch-all 规则配置了附件，所有来信者都会收到该文件
- 务必检查附件内容是否适合对外发送

**建议：**
- 优先使用 `sender_domains` 或 `keywords_subject` 限制匹配范围
- 使用前先用 `--dry-run` 预览
- 定期检查和清理自动回复规则

## 回复配置 (reply)

| 字段 | 类型 | 说明 |
|------|------|------|
| `subject_prefix` | string | 回复主题前缀，默认 `Re: ` |
| `body_template` | string | 回复正文模板（必填） |
| `attachments` | string[] | 可选附件路径列表 |

## 使用示例

### 场景 1：对老板设置自动回复

```
规则名称: 老板自动回复
匹配:
  sender_domains: ["@boss.com"]
回复模板: "收到您的邮件，我正在处理中，稍后回复您。"
```

### 场景 2：外出时自动回复所有邮件

```
规则名称: 外出自动回复 (catch-all)
匹配: (全部为空 — catch-all)
回复模板: "您好，我正在休假中，将于6月30日返回。期间如遇紧急事项请电话联系。"
```

### 场景 3：紧急关键词自动回复

```
规则名称: 紧急邮件通知
匹配:
  keywords_subject: ["紧急", "urgent", "asap"]
回复模板: "您的邮件已标记为紧急，我已收到通知并会尽快处理。"
```

## 通过 auto_reply.py 添加规则

将规则定义保存为 JSON 文件，然后运行:

```bash
python auto_reply.py add rule_definition.json
```

## 通过 LLM 创建规则示例

用户说："设置对老板的邮件自动回复'我已收到，稍后回复你'"

LLM 应生成规则定义 JSON:

```json
{
  "name": "老板自动回复",
  "match": {
    "sender_domains": ["@boss.com"]
  },
  "reply": {
    "body_template": "我已收到您的邮件，稍后回复你。"
  }
}
```

然后调用 `auto_reply.py add <tempfile>` 来创建。
