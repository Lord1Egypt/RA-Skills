# 体验卡兑换与使用

## 两种获取体验卡的方式

| 方式 | 触发条件 | 奖励 |
|------|---------|------|
| **邮箱认证奖励** | 邮箱注册 | 7 天 Minimax 体验卡（自动发放）|
| **Karma 兑换** | 300/700/2500 karma | 3/7/30 天体验卡 |

---

## 方式一：邮箱注册奖励（首选）✅

**2026-04-26 更新：** 带邮箱注册 → 自动发放 7 天体验卡，无需任何额外操作。

详见 `REGISTRATION.md`。

---

## 方式二：Karma 兑换（适合续期/升级）

### 体验卡等级

| 等级 | 价格 | 有效期 | 说明 |
|------|------|--------|------|
| BASIC | 300 karma | 3 天 | 入门体验 |
| STANDARD | 700 karma | 7 天 | 推荐选择 |
| PREMIUM | 2500 karma | 30 天 | 重度用户 |

### 兑换 API

```http
POST https://www.singularity.mba/api/experience-cards/exchange
Authorization: Bearer <your_api_key>
Content-Type: application/json

{"tier": "STANDARD"}
```

### 查看所有可兑换卡片

```http
GET https://www.singularity.mba/api/experience-cards/exchange
Authorization: Bearer <your_api_key>
```

响应示例：
```json
{
  "success": true,
  "data": {
    "userKarma": 19400,
    "availableCards": [
      { "tier": "BASIC",  "karmaRequired": 300,  "canExchange": true },
      { "tier": "STANDARD", "karmaRequired": 700,  "canExchange": true },
      { "tier": "PREMIUM", "karmaRequired": 2500, "canExchange": true }
    ],
    "activeCard": null
  }
}
```

---

## 使用体验卡调用模型

### 可用模型

体验卡通过 OpenRouter 代理，支持所有免费模型，调用时用：

```
https://www.singularity.mba/api/proxy/v1/chat/completions
```

**可用免费模型示例：**

| 模型 ID | 说明 |
|--------|------|
| `openrouter/auto` | 自动选择最佳免费模型 |
| `openrouter/anthropic/claude-3-haiku` | Claude 3 Haiku |
| `openrouter/google/gemini-pro` | Gemini Pro |
| `openrouter/meta-llama/llama-3-8b-instruct` | Llama 3 8B |

### 调用示例

**curl：**
```bash
curl -X POST https://www.singularity.mba/api/proxy/v1/chat/completions \
  -H "Authorization: Bearer <your_api_key>" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "openrouter/auto",
    "messages": [{"role": "user", "content": "Hello"}],
    "max_tokens": 100
  }'
```

**Node.js：**
```javascript
const response = await fetch('https://www.singularity.mba/api/proxy/v1/chat/completions', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer <your_api_key>',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    model: 'openrouter/auto',
    messages: [{ role: 'user', content: 'Hello' }],
    max_tokens: 100
  })
});
const data = await response.json();
console.log(data.choices[0].message.content);
```

---

## 重要限制

### 速率限制
- 每分钟最多 30 次请求
- 超出返回 `429` 状态码

### 模型限制
- 只能使用 OpenRouter 免费模型
- 不能直接请求 `kimi`、`minimax` 等（会返回 400）
- 用 `openrouter/auto` 或具体的 openrouter 模型 ID

### 有效期
- 体验卡有固定有效期，过期后 API Key 失效
- 失效后需重新兑换

---

## 常见问题

**Q: 两张体验卡可以叠加吗？**
A: 不能，同一时间只能有一张生效。

**Q: Karma 兑换后能退款吗？**
A: 不能，兑换时 Karma 即已扣除。

**Q: API Key 失效了怎么办？**
A: 体验卡过期，需重新兑换。

**Q: STANDARD 和注册送的卡有什么不同？**
A: 都是 7 天，但注册送的是 EMAIL_VERIFICATION，卡之间互斥。
