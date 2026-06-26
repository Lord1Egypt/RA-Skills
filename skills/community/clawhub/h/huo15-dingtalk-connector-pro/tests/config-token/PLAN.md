# 配置与 Token 模块测试方案

## 1. 模块划分与职责

- **getConfig(cfg: ClawdbotConfig)**  
  返回 `cfg?.channels?.['dingtalk-connector'] ?? {}`。
- **isConfigured(cfg)**  
  返回 `Boolean(config.clientId && config.clientSecret)`，config 来自 getConfig。
- **getAccessToken(config)**  
  请求钉钉 OAuth 接口，缓存 token，过期前 60 秒内复用。
- **getOapiAccessToken(config)**  
  请求旧版 gettoken，errcode===0 时返回 access_token，否则或异常返回 null。
- **getUnionId(staffId, config, log)**  
  先查缓存；无缓存则 getOapiAccessToken + user/get，拿到 unionid 后缓存并返回；异常或无 unionid 返回 null。

## 2. 已覆盖用例（与 `config-token.test.ts` 对齐）

> 说明：本章节仅列出**已在测试中覆盖**的用例，确保文档与现状 100% 一致。

### 2.1 getConfig

| 序号 | 输入 cfg | 期望 | 说明 |
|------|----------|------|------|
| 1 | `{ channels: { 'dingtalk-connector': { clientId: 'a', clientSecret: 'b' } } }` | 该对象 | 正常 |
| 2 | `{ channels: {} }` | `{}` | 无 dingtalk 键 |
| 3 | `{}` | `{}` | 无 channels |
| 4 | `undefined` | `{}` | cfg 缺失 |

### 2.2 isConfigured

| 序号 | 输入 cfg | 期望 | 说明 |
|------|----------|------|------|
| 7 | 含 clientId+clientSecret | true | 正常 |
| 8 | `{ channels: {} }` | false | 无配置 |
| 9 | `{ channels: { 'dingtalk-connector': { clientId: 'a' } } }` | false | 缺 clientSecret |
| 10 | `{ channels: { 'dingtalk-connector': { clientSecret: 'b' } } }` | false | 缺 clientId |

### 2.3 getAccessToken

| 序号 | axios.post 返回 | 期望 | 说明 |
|------|-----------------|------|------|
| 12 | `{ data: { accessToken: 't', expireIn: 3600 } }` | 't' | 首次获取 |
| 13 | 同上，连续调用两次 | 第二次不请求，仍返回 't' | 缓存命中 |

### 2.4 getOapiAccessToken

| 序号 | axios.get 返回/行为 | 期望 | 说明 |
|------|---------------------|------|------|
| 15 | `{ data: { errcode: 0, access_token: 'tok' } }` | 'tok' | 成功 |
| 16 | `{ data: { errcode: 1 } }` | null | 失败 |
| 17 | throw Error | null | 异常被吞，返回 null |

### 2.5 getUnionId

| 序号 | gettoken 行为 | user/get 返回 | 期望 | 说明 |
|------|----------------|---------------|------|------|
| 18 | 返回 token | `{ data: { unionid: 'u1' } }` | 'u1' | 成功 |
| 19 | 同上，同一 staffId 再调 | - | 'u1'，不再请求 | 缓存 |

## 3. 待补充用例（文档列出但当前未覆盖）

> 说明：以下用例用于后续补齐覆盖，**不代表当前已测**。

### 3.1 getConfig

| 序号 | 输入 cfg | 期望 | 说明 |
|------|----------|------|------|
| P1 | `null` | `{}` | cfg 为 null |
| P2 | `{ channels: { 'dingtalk-connector': null } }` | 视实现：`null` 或 `{}` | 键存在但值为 null |

### 3.2 isConfigured

| 序号 | 输入 cfg | 期望 | 说明 |
|------|----------|------|------|
| P3 | clientId/clientSecret 为空字符串 | false | 弱假值 |

### 3.3 getAccessToken

| 序号 | axios.post 返回 | 期望 | 说明 |
|------|-----------------|------|------|
| P4 | 缺少 accessToken/expireIn | 抛错或返回异常结构 | 以实现契约为准 |

### 3.4 getUnionId

| 序号 | gettoken 行为 | user/get 返回 | 期望 | 说明 |
|------|----------------|---------------|------|------|
| P5 | 返回 null | - | null | 无 token 不调 user/get |
| P6 | 返回 token | `{ data: {} }` 无 unionid | null | 应记录日志并返回 null |
| P7 | 返回 token | throw | null | 异常被吞并返回 null |

## 7. 预期正确输出与潜在错误

- **正确**：getConfig 缺键或 cfg 空得 {}；isConfigured 仅 clientId 与 clientSecret 均真才 true；getOapiAccessToken 异常返回 null；getUnionId 缓存与异常路径返回 null。
- **错误原因**：errcode 判断写成 !==0 反了；未 try-catch 导致抛错；缓存 key 混用；时间单位用秒未乘 1000。
