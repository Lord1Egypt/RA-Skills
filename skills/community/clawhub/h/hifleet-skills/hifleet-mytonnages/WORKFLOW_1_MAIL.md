# Workflow 1 · 邮箱配置（与 `SKILL.md` §1 完全对应）

以下为 **1.1～1.4** 全文；**不得删减、不得改顺序**。

### 1.1 引导用户提供邮箱信息

请向用户说明（以下内容可复述）：

```text
请提供以下邮箱配置信息（这些信息将保存在本地，仅用于邮件查询）：

1. 邮箱地址（如：username@company.com）
2. IMAP服务器地址（如：imap.company.com 或 imap.163.com）
3. IMAP服务器端口（通常为993，使用SSL）
4. 邮箱第三方客户端密码（不是登录密码，需在邮箱设置中获取）
```

### 1.2 接收并验证用户输入

依次获取用户的邮箱配置信息

验证邮箱格式是否正确

尝试使用提供的信息连接邮箱服务器进行验证

如果验证失败，提示用户检查信息并重新输入

### 1.3 保存配置（禁止要求用户自己操作）

助手在用户确认信息无误后，使用当前宿主环境允许的方式写入配置（例如 Codex / OpenClaw 的内置写入工具、设置界面、或约定路径下的安全存储）。**不得**要求用户运行 `mkdir`/`echo`/`chmod` 或任何终端命令。

推荐落盘路径（若环境支持文件存储）：当前安装包内的 `hifleet-mytonnages/config.json`。例如 Codex 可位于 `$CODEX_HOME/skills/hifleet-skills/hifleet-mytonnages/config.json`，OpenClaw 可位于 `~/.openclaw/workspace/skills/hifleet-skills/hifleet-mytonnages/config.json`；若部署方另设 `HIFLEET_MYTONNAGES_DIR`，则写入该目录下的 `config.json`。敏感字段按当前宿主/插件规范保存（如单独的密钥存储），**勿在普通对话里复述用户密码**。

若当前宿主环境仅支持「对话内临时邮箱」而无持久化，则按该环境能力降级，并在说明中如实告知用户限制。

### 1.4 配置成功提示

```text
✅ 邮箱配置成功！现在可以使用以下命令查询邮件：
- “最近有什么船盘”
- “有没有去中国的货”
- “帮我查查近5天的邮件”
```
