---
name: no-empty-message
enabled: true
event: PreMessage
matcher: "^\\s*$"
action: block
priority: 100
---

禁止发送空消息或纯空白消息。

---
name: no-plaintext-secrets
enabled: true
event: PreMessage
matcher: "(password|secret|token|api_key)\\s*[:=]\\s*\\S+"
action: warn
priority: 90
---

消息中可能包含明文密钥或密码。

建议使用环境变量或密钥管理工具，不要在消息中直接传递敏感信息。

---
name: warn-long-message
enabled: true
event: PreMessage
matcher: ".{4001,}"
action: warn
priority: 30
---

消息超过 4000 字符，建议分段发送以提高可读性。

---
name: no-markdown-tables-in-chat
enabled: true
event: PreMessage
matcher: "\\|.*\\|.*\\|"
action: warn
priority: 20
---

消息包含 Markdown 表格。

Discord/WhatsApp 不支持表格渲染，建议改用列表格式。

---
name: warn-all-caps
enabled: true
event: PreMessage
matcher: "^[A-Z\\s\\d\\W]{20,}$"
action: warn
priority: 10
---

消息全部为大写字母，看起来像在喊叫。确认是否有意为之。
