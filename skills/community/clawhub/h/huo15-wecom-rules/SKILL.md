# huo15-wecom-rules / 火一五企微

**【版权：青岛火一五信息科技有限公司 账号：huo15】**

企业微信全局规则技能 - 整合所有企微相关操作规范

## 技能说明

本技能提供企业微信 API 操作的标准化规则，确保所有消息和文件发送行为一致。

---

## 一、文件发送规则

### 核心原则

发送任何文件给用户时，默认使用企业微信 API 发送。

### 执行流程（强制）

1. **第一步**：优先尝试使用企业微信 API 发送（`message` 工具 + `media` 参数）
2. **第二步**：如果企微 API 发送失败（错误码、IP 白名单限制等），再使用其他方式发送（如临时链接）
3. **不要跳过企微 API**：每次发送文件都必须先尝试企微 API

### 执行方式

- 使用 `message` 工具，`action=send`
- 必须带 `media` 参数（文件路径）
- 必须带 `target` 参数（用户 ID，格式：`user:<userid>`）
- 可选带 `message` 参数（附加说明文字）

### 适用范围

- 所有用户（赵博、赵小博及其他所有微信/企微用户）
- 所有文件发送场景（Word、Excel、PDF、图片等）

### 示例

```
message(action=send, target="user:ZhaoBo", media="/path/to/file.docx", message="文件说明")
```

---

## 二、主动发送消息规则

### 触发条件

当用户说"发送给xxx"或"发个消息给xxx"时，默认使用企业微信 API 主动发送消息。

### 执行方式

- 使用 `message` 工具，`action=send`
- 必须带 `target` 参数（用户 ID，格式：`user:<userid>`）
- 必须带 `message` 参数（消息内容）

### 适用范围

- 所有用户（赵博、赵小博及其他所有企微用户）
- 所有主动发送消息场景（提醒、通知等）

### 示例

```
message(action=send, target="user:ZhaoBo", message="提醒内容")
```

---

## 三、消息格式规则

### 群聊格式

- Markdown 支持有限，避免使用 `# ** * ~~` 等符号
- 使用纯文本 + emoji
- 列表用数字编号 `1. 2. 3.`
- 链接直接显示 URL

### 适用场景

企业微信群聊消息

---

## 四、企微 API 失败处理

### 错误码处理

- 错误码 60020（IP 白名单限制）→ 自动切换到临时链接模式
- 其他错误 → 记录日志并通知用户

### 重试机制

- 首次发送失败后，自动重试 1 次
- 重试仍失败则切换备用方案

---

## 五、企微用户信息获取

### 获取时机

每次新会话启动时

### 获取内容

- 用户姓名（用于称呼）
- userid（用于发送消息）
- 性别（用于称呼：sir/女士）

### 存储位置

存入 `memory/shared/MEMORY.md`，标注来源用户

---

## 六、用户称呼规则

### 男性用户

- 姓氏 + sir
- 例如：张sir、黄sir

### 女性用户

- 姓氏 + 女士/Ma'am
- 例如：王女士、李Ma'am

### 不确定时

- 不确定性别时默认使用 Ma'am
- 如果获取不到姓名，主动询问"请问您叫什么名字？"

---

## 七、消息类型规则

### 1. TEXT（文本消息）- 默认类型

适用于普通通知、提醒。

```bash
# 发送文本消息
message(action=send, target="user:用户ID", message="消息内容")
```

### 2. TEXT_CARD（卡片消息）- 重要通知

适用于重要通知、带按钮链接的消息。

**特点**：
- 标题 + 描述 + 按钮链接
- 适合：任务提醒、审批通知、报告查看

**企微API发送**：
```bash
# 使用企微API发送卡片消息
CORP_ID="wwd00a4d7e69fffdf1"
SECRET="Jg7-sBKn1rhynH_NUgAf-C6dxmNrpUIxLz8qfQ109OQ"
AGENT_ID=1000009

TOKEN=$(curl -s "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=$CORP_ID&corpsecret=$SECRET" | jq -r '.access_token')

curl -s -X POST "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=$TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "touser": "用户ID",
    "agentid": 1000009,
    "msgtype": "textcard",
    "textcard": {
      "title": "标题",
      "description": "描述内容",
      "url": "https://example.com/link",
      "btntxt": "查看详情"
    }
  }'
```

### 3. NEWS（图文消息）- 报告/新闻

适用于报告、新闻、活动推送，可带封面图片。

**特点**：
- 标题 + 描述 + 封面图片 + 链接
- 适合：周报、月报、活动通知、新闻推送

**企微API发送**：
```bash
curl -s -X POST "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=$TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "touser": "用户ID",
    "agentid": 1000009,
    "msgtype": "news",
    "news": {
      "articles": [
        {
          "title": "文章标题",
          "description": "文章描述",
          "url": "https://example.com/article",
          "picurl": "https://example.com/cover.jpg"
        }
      ]
    }
  }'
```

### 4. 批量@多人（群聊）

适用于群聊中@多个人的场景。

**企微API发送**：
```bash
curl -s -X POST "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=机器人Key" \
  -H "Content-Type: application/json" \
  -d '{
    "msgtype": "text",
    "text": {
      "content": "提醒内容",
      "mentioned_list": ["userid1", "userid2", "userid3"]
    }
  }'
```

---

## 八、常用企微API汇总

### 配置信息（已配置）

| 配置项 | 值 |
|--------|-----|
| 企业ID | wwd00a4d7e69fffdf1 |
| AgentId | 1000009 |
| Secret | Jg7-sBKn1rhynH_NUgAf-C6dxmNrpUIxLz8qfQ109OQ |
| 机器人Webhook | 30e68984-0562-4d13-b3cc-16d0df7a382a |

### 常用API

```bash
# 获取Access Token
curl -s "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=$CORP_ID&corpsecret=$SECRET"

# 发送应用消息（私聊）
curl -s -X POST "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=$TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"touser": "用户ID", "agentid": 1000009, "msgtype": "text", "text": {"content": "消息内容"}}'

# 发送群机器人消息
curl -s -X POST "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=机器人Key" \
  -H "Content-Type: application/json" \
  -d '{"msgtype": "text", "text": {"content": "消息内容"}}'
```

---

## 九、用户信息自动获取规则

### 触发时机

1. **新会话启动** - 用户输入 `/new` 或开启新会话时
2. **定时刷新** - 每隔 1 天自动获取一次
3. **任何用户对话时** - 首次对话时获取

### 获取内容

- 用户姓名（name）
- userid
- 性别（用于称呼）

### 执行方式

```bash
# 获取 Access Token
CORP_ID="wwd00a4d7e69fffdf1"
SECRET="Jg7-sBKn1rhynH_NUgAf-C6dxmNrpUIxLz8qfQ109OQ"
TOKEN=$(curl -s "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=$CORP_ID&corpsecret=$SECRET" | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)

# 获取用户信息
curl -s "https://qyapi.weixin.qq.com/cgi-bin/user/get?access_token=$TOKEN&userid=用户ID"
```

### 存储位置

获取后存入 `memory/shared/MEMORY.md`，标注来源用户：
```markdown
## {用户姓名}存入
- userid: xxx
- 姓名: xxx
- 性别: xxx
```

### 称呼更新

根据获取到的性别动态更新称呼：
- 男性：姓氏 + sir
- 女性：姓氏 + 女士/Ma'am
- 不确定：默认 Ma'am

---

## 十、会话启动用户信息获取

### 触发时机

每次新会话启动时（输入 `/new` 或开启新会话）

### 执行流程

1. 从消息元数据获取 `chat_id`（即 userid）
2. 调用企微 API 获取用户详细信息
3. 存储到 `memory/shared/MEMORY.md`，标注来源

### 存储格式

```markdown
## {用户姓名}存入
- userid: xxx
- 姓名: xxx
- 性别: xxx
```

### 重要

- 根据 `chat_id` 确定用户身份
- 公有记忆所有用户共享
- 存入公有记忆时必须标注来源用户

---

## 十一、文件发送规则（合并自 AGENTS.md）

### 默认规则

发送文件时 → 使用企微 API 上传并发送**文件本身**，不要发临时下载链接或路径

### 执行流程

1. **第一步**：使用企微 API 发送文件本身
2. **第二步**：转发消息时 → 使用企微 API 转发
3. **第三步**：提醒功能 → 使用企微 API 发送提醒
4. **如果企微 API 发送失败，再尝试其他方式**

---

## 注意事项

1. 本技能规则优先于其他分散的企微操作规范
2. 所有企微相关操作必须遵循本技能
3. 如有新规则更新，统一在本技能中追加
