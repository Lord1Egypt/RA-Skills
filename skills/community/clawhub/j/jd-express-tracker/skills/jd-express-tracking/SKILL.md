---
name: jd-express-tracking
description: "查询京东快递运单物流轨迹、运单详情、派送时效。调用京东物流开放接口 queryWaybillTrace / queryWaybillDetail 获取数据。"
---

# 京东快递运单查询（JD Express Tracking）

通过京东物流开放接口查询运单轨迹与详情。

## 触发条件

当 Agent 需要查询京东运单的物流轨迹或运单详情时调用本技能。

## 前置条件

- 需要有效的京东会话 token（`js-token` 鉴权头）
- 网关域名 `https://lop-proxy.jd.com` 需加入请求合法域名白名单
- 仅支持京东自营快递运单号（JD / JDV / VA 前缀，15-18 位）

## 接口

### queryWaybillTrace

通过运单号查询全程物流轨迹（按时间倒序的节点列表）。

- **接口**：`POST https://lop-proxy.jd.com/order/queryExpressTraceGroupPublic`
- **详细规范**：见 `references/api-spec.md`

### queryWaybillDetail

通过运单号查询京东快递运单基础信息（当前状态、寄件人/收件人脱敏、商品信息、下单时间）。

- **接口**：`POST https://lop-proxy.jd.com/order/queryWaybillDetailInfoUnAuthenticated`
- **详细规范**：见 `references/api-spec.md`

## 副作用

- `queryWaybillTrace` 成功后，调用方应将 `waybillCode` 写入本地 `skills_jdTracking_recent` 缓存（最多 10 条）

## 已知限制

- 仅支持京东自营快递运单号，三方运单返回空
- 后端字段名在不同环境/版本下可能不稳定，需做归一化兜底
- 物流数据存在 5-30 分钟延迟
