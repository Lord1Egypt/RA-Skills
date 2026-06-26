# 飞书配置流程

> 你是 AI Agent，此文档指导你如何引导用户在 TUI 中完成飞书 Bot 创建和绑定。

---

## 前置准备：查询团队 Agent 信息

**执行命令获取团队 Agent 信息：**
```bash
opclawtm list-agents
```

**向用户说明：**
- 记录总助理名称 → 第一个创建飞书应用
- 记录管理者名称 → 第二个创建飞书应用
- 记录审核者名称 → 第三个创建飞书应用
- 按此顺序逐个完成 Bot 创建和绑定

---

## Step 1：为总助理创建飞书 Bot

**引导用户操作：**

在 TUI 中：
1. 选择「飞书配置」→「➕ 为 Agent 添加飞书 Bot」
2. 选择总助理

### 1.1 在飞书开放平台创建应用

**引导用户操作：**
1. Ctrl+点击教程链接：https://www.feishu.cn/content/article/7602519239445974205
2. 进入飞书开放平台：https://open.feishu.cn/app
3. 点击「创建企业自建应用」
4. 应用名称填写：**总助理的名称**（如：小助手）

### 1.2 启用机器人能力

**引导用户操作：**
1. 进入「应用能力」→「机器人」
2. 开启机器人能力
3. 机器人名称填写：**总助理的名称**

### 1.3 配置应用权限

**引导用户操作：**
1. 进入「权限管理」→ 点击「批量导入」
2. 复制以下 JSON 内容：

```json
{
 "scopes": {
 "tenant": [
 "contact:contact.base:readonly",
 "docx:document:readonly",
 "im:chat:read",
 "im:chat:update",
 "im:message.group_at_msg:readonly",
 "im:message.p2p_msg:readonly",
 "im:message.pins:read",
 "im:message.pins:write_only",
 "im:message.reactions:read",
 "im:message.reactions:write_only",
 "im:message:readonly",
 "im:message:recall",
 "im:message:send_as_bot",
 "im:message:send_multi_users",
 "im:message:send_sys_msg",
 "im:message:update",
 "im:resource",
 "application:application:self_manage",
 "cardkit:card:write",
 "cardkit:card:read"
 ],
 "user": [
 "contact:user.employee_id:readonly",
 "offline_access","base:app:copy",
 "base:field:create",
 "base:field:delete",
 "base:field:read",
 "base:field:update",
 "base:record:create",
 "base:record:delete",
 "base:record:retrieve",
 "base:record:update",
 "base:table:create",
 "base:table:delete",
 "base:table:read",
 "base:table:update",
 "base:view:read",
 "base:view:write_only",
 "base:app:create",
 "base:app:update",
 "base:app:read",
 "board:whiteboard:node:create",
 "board:whiteboard:node:read",
 "calendar:calendar:read",
 "calendar:calendar.event:create",
 "calendar:calendar.event:delete",
 "calendar:calendar.event:read",
 "calendar:calendar.event:reply",
 "calendar:calendar.event:update",
 "calendar:calendar.free_busy:read",
 "contact:contact.base:readonly",
 "contact:user.base:readonly",
 "contact:user:search",
 "docs:document.comment:create",
 "docs:document.comment:read",
 "docs:document.comment:update",
 "docs:document.media:download",
 "docs:document:copy",
 "docx:document:create",
 "docx:document:readonly",
 "docx:document:write_only",
 "drive:drive.metadata:readonly",
 "drive:file:download",
 "drive:file:upload",
 "im:chat.members:read",
 "im:chat:read",
 "im:message",
 "im:message.group_msg:get_as_user",
 "im:message.p2p_msg:get_as_user",
 "im:message:readonly",
 "search:docs:read",
 "search:message",
 "space:document:delete",
 "space:document:move",
 "space:document:retrieve",
 "task:comment:read",
 "task:comment:write",
 "task:task:read",
 "task:task:write",
 "task:task:writeonly",
 "task:tasklist:read",
 "task:tasklist:write",
 "wiki:node:copy",
 "wiki:node:create",
 "wiki:node:move",
 "wiki:node:read",
 "wiki:node:retrieve",
 "wiki:space:read",
 "wiki:space:retrieve",
 "wiki:space:write_only"
 ]
 }
}
```

3. 直接导入替换
4. 保存权限配置

### 1.4 配置事件订阅

**引导用户操作：**
1. 在飞书开放平台进入「事件订阅」页面
2. 开启「使用长连接接收事件」开关
3. 添加事件：`im.message.receive_v1`
4. 保存配置

### 1.5 配置消息卡片回调

**引导用户操作：**
1. 进入「消息卡片」→「回调配置」页面
2. 开启「使用长连接接收事件」开关
3. 保存配置

### 1.6 创建版本并发布

**引导用户操作：**
1. 进入「版本管理与发布」页面
2. 点击「创建版本」
3. 填写版本号和更新说明
4. 保存版本
5. 点击「申请上线」
6. 等待审核通过

### 1.7 获取凭证并填写

**引导用户操作：**
1. 进入「凭证与基础信息」页面
2. 复制 App ID（cli_xxx 格式）
3. 复制 App Secret
4. 在 TUI 输入框填写 App ID
5. 在 TUI 输入框填写 App Secret
6. 选择私聊策略：pairing（推荐）
7. 确认保存

---

## Step 2：启动 Gateway 并配对授权

### 2.1 启动 Gateway

**告知用户：**
- 必须先启动 Gateway，否则长连接配置会失败
- 在命令行执行：`openclaw gateway`

### 2.2 配对授权

**引导用户操作：**
1. 在飞书搜索并添加刚创建的机器人
2. 发送私聊消息
3. 机器人会返回配对码

**如果没有返回配对码，向用户确认：**
- 是否完成了版本保存？
- 飞书应用是否已上线？
- Gateway 是否已启动？

### 2.3 在 TUI 中完成配对

**引导用户操作：**
1. 选择「飞书配置」→「配对管理」
2. 输入配对码
3. 完成配对授权

---

## Step 3：为其他团队成员创建飞书 Bot

**向用户说明：**

按照相同流程，为管理者和审核者创建飞书 Bot：

### 3.1 为管理者创建

**引导用户操作：**
1. 在飞书开放平台创建新应用
2. 应用名称填写：**管理者的名称**
3. 重复 Step 1 的流程（1.1 - 1.7）

### 3.2 为审核者创建

**引导用户操作：**
1. 在飞书开放平台创建新应用
2. 应用名称填写：**审核者的名称**
3. 重复 Step 1 的流程（1.1 - 1.7）

---

## Step 4：飞书群绑定

**引导用户操作：**

### 4.1 将 Bot 拉入飞书群

**向用户说明：**
1. 在飞书中创建一个群或使用现有群
2. 将总助理 Bot 添加到群中

### 4.2 获取群 ID

**引导用户操作：**
1. 进入群设置
2. 点击「群信息」
3. 找到群 ID（oc_xxx 格式）

### 4.3 在 TUI 中绑定群

**引导用户操作：**
1. 选择「飞书配置」→「🔗 绑定飞书群到事业部」
2. 选择部门
3. 输入群 ID（oc_xxx 格式）
4. 确认绑定

---

## Step 5：用户 ID 绑定

### 5.1 你查找用户 ID

**执行命令查找日志：**
```bash
cat ~/.openclaw/logs/gateway.log | grep "ou_"
```

**向用户反馈：**
- 找到 `ou_` 开头的 ID
- 直接显示给用户

### 5.2 在 TUI 中绑定用户 ID

**引导用户操作：**
1. 选择「飞书配置」→「🔗 设置飞书 Open ID」
2. 输入 Open ID（ou_xxx 格式）
3. 确认绑定

---

## 配置验证

**引导用户操作：**
1. 在 TUI 选择「飞书配置」→「📋 查看飞书 Bot 配置的 Agent 列表」
2. 确认所有团队成员都已绑定 Bot
3. 在 TUI 选择「团队查看」确认群绑定状态