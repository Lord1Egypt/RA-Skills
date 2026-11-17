# 京东快递运单查询接口规范

本文档描述调用京东物流开放接口查询运单轨迹时所需的请求头、参数与鉴权要求。Agent MD 中只引用结论，详细字段见本文。

## 1. queryWaybillTrace

通过运单号查询全程物流轨迹（按时间倒序的节点列表）。后端可能返回分组结构（按状态分组），接口内部已做拍平归一化。

### 接口地址

`POST https://lop-proxy.jd.com/order/queryExpressTraceGroupPublic`

### 关键请求头

| Header | 说明 |
|---|---|
| `lop-dn` | `logistics-mrd.jd.com` |
| `appparams` | `{"appid":158,"ticket_type":"m","biz":"express"}` |
| `client` | `JD-H5` |
| `clientinfo` | `{"appName":"c2c","client":"m"}` |
| `clientsource` | `JD-H5` |
| `origin` | `https://logistics-mrd.jd.com` |
| `referer` | `https://logistics-mrd.jd.com/` |
| `host` | `lop-proxy.jd.com` |
| `js-token` | **京东会话 token（关键鉴权头）** |
| `bff-client` | `H5` |
| `jfe-cgi-flow` | `EXP_H5_273ce00` |
| `commit` | `273ce00` |
| `x-requested-with` | `XMLHttpRequest` |
| `server_protocol` | `HTTP/2.0` |
| `x-lop-http-version` | `HTTP/1.1` |
| `version` / `build` / `clientversion` | `1782981212000`（H5 构建号） |
| `x-jdlb-client-port` | 客户端端口号 |
| `x-original-to` | 透传目标 IP |
| `x-ssl-cipher` | `TLS_AES_256_GCM_SHA384` |
| `x-proto` | `SSL` |
| `accept` | `application/json, text/plain, */*` |
| `accept-language` | `zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7` |
| `accept-encoding` | `gzip, deflate, br, zstd` |
| `sec-fetch-mode` / `sec-fetch-dest` / `sec-fetch-site` | CORS 字段 |
| `sec-ch-ua` / `sec-ch-ua-platform` / `sec-ch-ua-mobile` | 客户端指纹 |
| `x-forwarded-for` / `j-forwarded-for` / `a-forwarded-for` | IP 链路字段 |

### 请求体（数组）

```json
[{
  "entrance": "JDAPP",
  "client": "2",                  // 2=H5, 1=小程序
  "apiVersion": "1.0.0",
  "source": 4,                    // 1=C2C, 2=BW, 3=B2C, 4=全部
  "productType": 10,              // 10=查件(包含寄件列表详情，收件列表和详情)
  "waybillCode": "JDxxxxxxxxxxxxx",
  "pin": ""
}]
```

### 副作用

成功后由调用方将 `waybillCode` 写入本地 `skills_jdTracking_recent`（最多 10 条，结构 `[{waybillCode, queriedAt}]`）。

## 2. queryWaybillDetail

通过运单号查询京东快递运单的基础信息：包括当前状态、寄件人/收件人（脱敏）、商品信息、下单时间等。

- 接口：`POST /order/queryWaybillDetailInfoUnAuthenticated`
- 来源：`src/packageSub/packageOrder/api/orderApi.ts` 的 `queryWaybillDetailInfoUnAuthenticatedAPI`
- 请求头与 `queryWaybillTrace` 保持一致
- 请求体结构相同，`waybillCode` 为必填

## 3. 前置条件

- 关键鉴权头：`js-token`（京东会话 token）
- 网关域名 `https://lop-proxy.jd.com` 已加入小程序 request 合法域名白名单
- 调用京东接口需要保证后端服务可用
- 本 skill 不依赖登录态；如需查询登录用户的私有订单，需另做带鉴权的 skill

## 4. 已知限制

- 仅支持京东自营快递运单号，三方运单（顺丰/中通等）后端会返回空
- 后端字段名不稳定时（不同环境/版本），归一化兜底逻辑会尽量提取关键字段，必要时可在真机校验后追加映射
