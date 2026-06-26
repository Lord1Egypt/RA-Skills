# 飞书私聊采集完整流程

## 前置条件

用户需要提供以下信息：
- 飞书应用凭证：app_id 和 app_secret（在飞书开放平台创建自建应用获取）
- 用户权限：应用需开通以下用户权限（scope）：
  - `im:message` — 以用户身份读取/发送消息
  - `im:chat` — 以用户身份读取会话列表
- OAuth 授权码（code）：用户在浏览器中完成 OAuth 授权后，从回调 URL 中获取

---

## 获取 user_access_token 的完整流程

### Step 1：确认用户配置

当用户提供了 app_id、app_secret，并确认已开通用户权限后：

帮用户生成 OAuth 授权链接：
```
https://open.feishu.cn/open-apis/authen/v1/authorize?app_id={APP_ID}&redirect_uri=http://www.example.com&scope=im:message%20im:chat
```

⚠️ 注意：redirect_uri 需要在飞书应用的「安全设置 → 重定向 URL」中添加 `http://www.example.com`

### Step 2：用户授权流程

1. 用户在浏览器打开链接，登录并授权
2. 页面会跳转到 `http://www.example.com?code=xxx`
3. 用户复制 code 给你

### Step 3：用 code 换取 token

执行：
```bash
python3 ${SKILL_DIR}/tools/feishu_auto_collector.py --exchange-code {CODE}
```

或者直接写 Python 脚本调飞书 API 换取：

```python
# 1. 获取 app_access_token
POST https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal
Body: {"app_id": "xxx", "app_secret": "xxx"}

# 2. 用 code 换 user_access_token
POST https://open.feishu.cn/open-apis/authen/v1/oidc/access_token
Header: Authorization: Bearer {app_access_token}
Body: {"grant_type": "authorization_code", "code": "xxx"}
```

---

## 获取私聊 chat_id

用户通常不知道 chat_id。当用户有了 user_access_token 但没有 chat_id 时：

### 方法：发消息获取 chat_id

用 user_access_token 向对方的 open_id 发一条消息，返回值中会包含 chat_id：

```python
POST https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id
Header: Authorization: Bearer {user_access_token}
Body: {
  "receive_id": "{对方open_id}",
  "msg_type": "text",
  "content": "{\"text\":\"你好\"}"
}
# 返回值中的 chat_id 就是私聊会话 ID
```

⚠️ 注意：GET /im/v1/chats 不会返回私聊会话，这是飞书 API 的限制，不是权限问题，不要尝试用这个接口找私聊。

---

## 如果用户不知道对方的 open_id

用 tenant_access_token 调通讯录 API 搜索：

```python
GET https://open.feishu.cn/open-apis/contact/v3/scopes
# 返回应用可见范围内所有用户的 open_id
```

---

## 执行采集

拿到 user_access_token 和 chat_id 后：

```bash
python3 ${SKILL_DIR}/tools/feishu_auto_collector.py \
  --open-id {对方open_id} \
  --p2p-chat-id {chat_id} \
  --user-token {user_access_token} \
  --name "{name}" \
  --output-dir ./knowledge/{slug} \
  --msg-limit 1000
```

---

## 灵活性原则

以上 API 调用不一定要用 collector 脚本，如果脚本跑不通或者场景不匹配，你可以直接写 Python 脚本调飞书 API 完成任务。

### 核心 API 参考

- 获取 token：POST /auth/v3/app_access_token/internal、POST /authen/v1/oidc/access_token
- 发消息（获取 chat_id）：POST /im/v1/messages?receive_id_type=open_id
- 拉消息：GET /im/v1/messages?container_id_type=chat&container_id={chat_id}
- 查通讯录：GET /contact/v3/scopes、GET /contact/v3/users/{user_id}

---

## 自动采集内容

- 群聊：所有与他共同群聊中他发出的消息（过滤系统消息、表情包）
- 私聊：与他的私聊完整对话（含双方消息，用于理解对话语境）
- 他创建/编辑的飞书文档和 Wiki
- 相关多维表格（如有权限）

---

## 采集完成后

用 Read 读取输出目录下的文件：
- `knowledge/{slug}/messages.txt` → 消息记录（群聊 + 私聊）
- `knowledge/{slug}/docs.txt` → 文档内容
- `knowledge/{slug}/collection_summary.json` → 采集摘要

---

## 常见问题处理

如果采集失败，根据报错自行判断原因并尝试修复：

- **群聊采集失败**：bot 未添加到群聊
- **私聊采集失败**：user_access_token 过期（有效期 2 小时，可用 refresh_token 刷新）
- **权限不足**：引导用户在飞书开放平台开通对应权限并重新授权
- **其他问题**：改用其他采集方式（上传文件、粘贴内容等）
