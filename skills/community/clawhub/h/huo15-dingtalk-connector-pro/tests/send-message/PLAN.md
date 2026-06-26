# send-message 模块测试方案

## 1. 模块划分与职责

本套件覆盖“群机器人 webhook”发送相关的辅助函数：

- **sendMarkdownMessage(config, sessionWebhook, title, markdown, options?)**：发送 markdown 消息；可选 `options.atUserId`。
- **sendTextMessage(config, sessionWebhook, text, options?)**：发送纯文本消息；可选 `options.atUserId`。
- **sendMessage(config, sessionWebhook, text, options?)**：根据内容自动判断 text/markdown（或通过 `options.useMarkdown` 强制/禁用），并可通过 `options.title` 指定 markdown 标题。

## 2. 用例表（覆盖现有测试）

### 2.1 sendMarkdownMessage

| 序号 | 场景 | 输入 | 期望 | 说明 |
|------|------|------|------|------|
| 1 | 发送成功 | title+markdown | 返回非空结果 | 主路径 |
| 2 | atUserId | options.atUserId='user123' | 请求 body 包含 `at` 字段 | @ 某人 |
| 3 | 默认标题 | title='' | 不抛错 | 标题回退（由实现决定） |

### 2.2 sendTextMessage

| 序号 | 场景 | 输入 | 期望 |
|------|------|------|------|
| 4 | 发送成功 | 'Hello world' | 返回非空结果 |
| 5 | atUserId | options.atUserId='user123' | 请求 body 包含 `at` 字段 |

### 2.3 sendMessage（自动判断/强制）

| 序号 | 场景 | content | options.useMarkdown | 期望 | 说明 |
|------|------|---------|-------------|------|------|
| 6 | 自动 markdown：标题语法 | `# Title\n**Bold**` | - | 按 markdown 发送 | 识别 `#`、`**` |
| 7 | 自动 markdown：多行 | `Line1\nLine2` | - | 按 markdown 发送 | 多行判定 |
| 8 | 自动 text：单行纯文本 | `Plain text` | - | 按 text 发送 |  |
| 9 | 强制 text | `# Title` | false | 按 text 发送 | 覆盖自动识别 |
| 10 | 强制 markdown | `Plain text` | true | 按 markdown 发送 |  |
| 11 | 自定义标题 | 任意 | true（并设置 options.title） | 使用自定义 title | markdown 标题 |
| 12 | 自动 markdown：列表/代码/粗斜体/链接 | `- a\n- b` / `` `code` `` / `**b**` / `[link](...)` | - | 按 markdown 发送 | 语法探测 |

## 3. 预期正确输出与潜在错误

- **正确**：自动判定规则稳定且可被 `useMarkdown` 覆盖；携带 atUserId 时请求体包含 `at`；标题为空时有合理回退；网络异常由上层捕获（测试中以“不抛错/返回值存在”为主）。
- **潜在错误原因**：markdown 判定过于激进导致纯文本被当 markdown；`useMarkdown` 逻辑反转；`at` 字段结构不符合钉钉 webhook 规范；title 为空触发服务端校验失败。

