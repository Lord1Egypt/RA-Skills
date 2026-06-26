# Open Health Link（当前接入：breo Scalp5）API 接口参考

本文档定义 Open Health Link 当前接入的 breo Scalp5 后端 RESTful API，供 skill 脚本调用。

**基础路径**: `/ai-oc-proxy`

**环境**:

| 环境 | 地址 |
|------|------|
| 生产环境 | `https://op.breo.cn/ai-oc-proxy` |

当前 skill 固定使用生产环境地址，不支持切换开发/测试环境。

---

## 一、授权相关接口

### 1. 获取授权码

获取授权码和 HMAC-SHA256 签名秘钥，用于启动授权流程。

- **接口路径**: `/api/auth/code/ge`
- **请求方法**: `GET`
- **请求参数**: 无

**响应参数**:

| 参数名 | 类型 | 说明 |
|--------|------|------|
| code | String | 授权码 |
| secret | String | 授权密钥（用于二维码内容生成） |

**响应示例**:

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "code": "AUTH_CODE_123456",
    "secret": "hmac_secret_key_example"
  }
}
```

**业务说明**:

- 返回的 `code` 用于后续查询授权状态
- 返回的 `secret` 用于生成二维码内容并完成 App 扫码授权

**本地使用方式**:

1. 将接口返回的 `code` 与 `secret` 组合生成二维码内容
2. 由 skill 生成二维码 PNG 图片并发送给用户扫码
3. 授权方式仅支持二维码图片扫码，不提供链接跳转授权兜底

---

### 2. 查询授权结果

根据授权码查询用户的授权状态和结果。

- **接口路径**: `/api/auth/result/{code}`
- **请求方法**: `GET`
- **路径参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| code | String | 是 | 授权码 |

**响应参数**:

| 参数名 | 类型 | 说明 |
|--------|------|------|
| authorized | Boolean | 是否已授权 |
| uid | String | 授权用户 ID（未授权时为 null） |
| authType | Integer | 授权业务类型（未授权时为 null） |
| authToken | String | 用户授权唯一标识（授权成功时返回） |

**响应示例 — 未授权**:

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "authorized": false,
    "uid": null,
    "authType": null,
    "authToken": null
  }
}
```

**响应示例 — 已授权**:

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "authorized": true,
    "uid": "USER_123456",
    "authType": 1,
    "authToken": "AUTH_TOKEN_789012"
  }
}
```

**业务说明**:

- 建议轮询间隔 3 秒
- 授权码 10 分钟内有效，超时后需重新获取
- 授权码不存在时返回 HTTP 404

---

## 二、数据相关接口

> 注意：数据接口的网关地址与授权接口不同。

### 1. 获取头皮检测报告列表

- **生产环境**: `https://op.breo.cn/op/cla`
- **接口路径**: `/auth/dt/{authToken}/list`
- **请求方法**: `GET`

**路径参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| authToken | String | 是 | 用户授权令牌 |

**Query 参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| day | Integer | 否 | 查询天数，范围 1-90 |

**业务说明**:

- `day` 不传时由后端使用默认查询范围。
- 当返回鉴权错误（401/403）时，应视为 token 失效并引导重新授权。
- 护理方案名由该接口一并返回（字段：`schemeName`），无独立护理方案接口。

**脚本调用示例**:

```bash
node scripts/fetch-report-list.js --day 30
```

**护理方案知识库联动**:

- 若需讲解方案详情，可将返回的 `schemeName` 传给方案知识库脚本（默认从远程 CSV 拉取）：

```bash
node scripts/plan-catalog.js "<schemeName>" --view summary
```

- 默认数据源：`https://breo-obs.obs.cn-south-1.myhuaweicloud.com/agents/plan-catalog.csv`

数据结构定义见 `data-schema.md`。

---

## 错误码说明

| 错误码 | 说明 |
|--------|------|
| 200 | 成功 |
| 400 | 请求参数错误 |
| 404 | 授权记录不存在 |
| 500 | 服务器内部错误 |

**错误响应示例**:

```json
{
  "code": 404,
  "message": "授权记录不存在",
  "data": null
}
```
