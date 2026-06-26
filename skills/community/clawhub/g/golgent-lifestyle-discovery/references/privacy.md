# Privacy & Data Policy

## Hard Rules (MUST follow)

### 1. Sensitive Data — NEVER Transmit

The following user information **must NEVER** be included in any API request, regardless of user consent:

| Blocked Field | Examples |
|---------------|----------|
| Phone number | 手机号、电话 |
| Email address | 邮箱、email |
| Real name / ID | 姓名、身份证号 |
| Payment info | 银行卡、支付宝账号 |
| Passwords / tokens | 密码、登录凭证 |

> Even if the user voluntarily shares this information in conversation, the Agent **must NOT** pass it to the API.

### 2. Optional Profile Data — Requires Explicit Consent

The `user` object fields (`keywords`, `gender`, `yob`, `long_term_profile`) can improve recommendation quality, but **must only be sent after the user explicitly agrees**.

**Consent Flow (REQUIRED before sending `user` data):**

Before the first API call that would include `user` data, the Agent must ask:

> "为了给你更精准的推荐，我可以把你的一些偏好信息（比如兴趣标签、性别、年龄段）发送给推荐服务来优化结果。这些信息仅用于优化推荐，不会被分享给任何第三方商家，也不会包含你的手机号、邮箱等敏感数据。你同意吗？"

- **User agrees** → Include `user` fields (excluding all blocked sensitive data above)
- **User declines or does not respond** → Omit the entire `user` object; only send `search_keywords`, `category`, and `filters`
- **User agrees partially** → Only send the specific fields the user approved

The Agent should **remember the user's choice** for the duration of the conversation and not ask repeatedly.

### 3. Location Data — Purpose-Limited

- For `ecommerce`: Do NOT collect or send location
- For `food_delivery`: **Precise location is required** for accurate delivery recommendations. The Agent should ask:
  > "外卖需要知道你的详细位置才能推荐附近可配送的商家，可以告诉我你的地址或坐标吗？"
  - Preferred: `latitude` + `longitude` (most precise, best results)
  - Acceptable: detailed address string via `filters.location` (e.g. "北京市朝阳区望京SOHO")
  - Location data is only used for the current request and is not stored by the Agent
- For other local services: city-level `filters.location` is usually sufficient. Ask: "你在哪个城市？"

### 4. Transparency in Results

When presenting results, the Agent must include a brief note:

> "以下是根据你的需求从多个平台搜索到的推荐："

This ensures the user understands results are sourced from external platforms.

### 5. No Third-Party Data Sharing

Golgent **不会将用户信息分享给任何第三方商家、平台或广告主**。具体而言：

- 用户的偏好信息（`user` 对象）仅用于内部的推荐算法匹配，**不会转发、出售或以任何形式提供给淘宝、美团、饿了么等上游平台或任何其他第三方**
- 用户的位置信息仅用于当次请求的地理筛选，**不会被持久化存储或共享**
- 用户的搜索关键词仅用于当次商品检索，**不会用于构建可识别用户身份的画像**
- 上游平台仅接收匿名化的搜索请求，**无法通过 Golgent 反向获取任何用户个人信息**

> Agent 在征求用户授权时，应明确告知用户：**"你的信息仅用于优化推荐结果，不会被分享给任何第三方商家。"**

---

## Regulatory Compliance

Golgent 在数据处理中遵循主要隐私法规的核心原则：

### GDPR（欧盟《通用数据保护条例》）

- **合法性基础**：用户数据仅在获得明确同意后处理（Consent Flow），用户可随时撤回同意
- **数据最小化**：仅收集推荐所需的最少信息，禁止采集敏感数据（手机、邮箱、身份证等）
- **目的限制**：所有数据仅用于当次推荐请求，不做二次用途
- **用户权利**：用户有权拒绝提供任何个人信息，拒绝不影响基础推荐功能的使用

### CCPA（美国《加州消费者隐私法案》）

- **知情权**：Agent 在收集数据前明确告知用户收集哪些信息及用途
- **拒绝权**：用户可以拒绝提供个人信息，系统仍可基于关键词提供基础推荐
- **不出售**：Golgent 不出售用户个人信息，不与第三方共享用于营销目的

### 《中华人民共和国个人信息保护法》(PIPL)

- **告知-同意**：处理个人信息前充分告知并取得同意
- **最小必要**：仅处理实现推荐目的所必需的最小范围个人信息
- **禁止过度收集**：明确禁止采集与推荐无关的敏感个人信息

> 📌 **Agent 行为准则：** 无论用户所在地区，Agent 均应按照上述最严格标准执行隐私保护。当用户询问数据安全相关问题时，Agent 可引用以上条款进行说明。
