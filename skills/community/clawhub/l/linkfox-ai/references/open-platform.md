# LinkFox AI 开放平台 - 接入与错误码

## 接入流程

1. 注册紫鸟开放平台：https://open.ziniao.com  
2. 认证开发者，创建 LinkFox 卖家应用：https://open.ziniao.com/docSupport?docId=116  
3. 将应用绑定到团队：https://www.linkfox.com/team/api-guide  
4. 鉴权方式以官方文档为准：[API 调用指南 - 简单通用模式（推荐）](https://open.ziniao.com/docSupport?docId=233)

## API 基础地址

- 默认：`https://sbappstoreapi.ziniao.com/openapi-router`  
- 路径前缀：`/linkfox-ai`  
- 无固定 IP 时可使用代理：`https://sbappstoreapi-proxy.linkfox.com`（需配置白名单 IP：120.79.189.15）

## 响应外层结构

所有接口的响应均由开放平台包装了一层外层结构，实际业务数据在 `data` 字段中。

```json
{
  "request_id": "abc123",
  "code": 0,
  "msg": "success",
  "data": {
    // 此处为业务接口的实际响应体
    "traceId": "...",
    "code": "200",
    "msg": "成功",
    "data": { /* 业务数据 */ }
  }
}
```

| 字段 | 说明 |
|------|------|
| request_id | 开放平台请求 ID |
| code | 开放平台状态码，0 为成功 |
| msg | 开放平台消息 |
| data | 业务接口实际响应（内部有自己的 traceId/code/msg/data） |

即实际数据嵌套路径为：`响应.data.data`（外层 data 是开放平台包装，内层 data 是业务数据）。

## QPS / 限流说明

- **base64 上传接口** (`/linkfox-ai/image/v2/uploadByBase64`)：全局限流 100 QPS。
- **其他接口**：默认无严格 QPS 限制，但建议单应用并发不超过 50 QPS。
- 触发限流时返回 HTTP 429 或开放平台错误码。
- 作图任务提交后需轮询 `make-info` 获取结果，建议轮询间隔 ≥ 3 秒。

## 错误码

| 错误码 | 描述 |
| --- | --- |
| ERR_FILED_VALIDATE | 参数校验异常 |
| ERR_VALIDATE_FAIL | 参数校验异常 |
| ERR_IMAGE_MAKE_AUDIT | 图片审核不通过 |
| ERR_IMAGE_MAKE_WILL_OUT | 作图点数不足 |
| ERR_FORBIDDEN | 没有ID权限，ID取错也有可能 |
| ERR_NOT_HAVE_TEAM_PRIVILEGE | 未绑定团队 |
| TEAM_PERMISSION_DISABLE_USER | 被禁用 |
| ERR_IMAGE_MAKE_COUNT_MAX | 生成中创建上限 |
| TEAM_PERMISSION_EXPIRE | 套餐已过期或者未购买套餐 |

更多说明见开放平台 https://open.ziniao.com 或本 skill 内 `references/image-make.md`。
