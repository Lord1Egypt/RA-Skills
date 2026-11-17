# uProc node

## 何时读取

当用户要在 n8n 中使用、配置、排查或替代 `uProc node` 时读取。该卡片由官方节点文档编译，完整细节以 source 为准。

## 节点标识

- n8n node id: `n8n-nodes-base.uproc`
- node group: `app-nodes`

## 核心要点

- Learn how to use the uProc node in n8n. Follow technical documentation to integrate uProc node into your workflows.

## 关键操作 / 参数线索

- Get advanced human audio file by provided text and language
- Get an audio file by provided text and language
- Discover if a domain has a social network presence
- Discover if an email is valid, hard bounce, soft bounce, spam-trap, free, temporary, and recipient exists
- Discover if the email recipient exists, returning email status
- Check if an email domain has an SMTP server to receive emails
- Discover if the email has a social network presence
- Check if an email has a valid format
- Check if an email domain belongs to a disposable email service
- Check if email belongs to free service provider like Gmail
- Check if email is catchall
- Discover if an email exists in the Robinson list (only Spain)
- Check if email belongs to a system or role-based account
- Check if an email is a spam trap
- Discover if an IMEI number has a valid format
- Check if a LinkedIn profile is a first-degree contact
- Discover if mobile phone number exists in network operator, with worldwide coverage
- Discover if a mobile phone number has a valid format with worldwide coverage

## n8n 使用建议

- 该节点涉及 credentials 或鉴权配置；生成工作流时使用占位 credential name，不写入真实密钥。
- 需要精确字段、选项枚举、认证方式或错误解释时，回读 source 文件，不凭记忆补全。

