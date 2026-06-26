# 聚合下单渠道分册：银联


## 目录

- 适用交易类型
- `method_expand` 对象边界
- 官方接入前准备
- `U_JSAPI` / `U_NATIVE` 请求字段
- `U_MICROPAY` 请求字段
- 同步返回银联扩展
- 异步 `unionpay_response`
- 银联实现备注

## 适用交易类型

| `trade_type` | 场景 |
|--------------|------|
| `U_JSAPI` | 银联 JS 支付 |
| `U_NATIVE` | 银联正扫 |
| `U_MICROPAY` | 银联付款码反扫 |

## `method_expand` 对象边界

- `trade_type` 负责选择银联场景。
- `method_expand` 的 JSON 内容直接就是银联对象本身。
- 不要再写成带 `U_JSAPI`、`U_MICROPAY` 等场景 key 的包装结构。

## 官方接入前准备

- 官方开发指引要求先完成商户进件并开通银联业务。
- `U_JSAPI` 场景下，需先走银联网页授权获取 `auth_code`，再调用获取银联用户标识接口换取 `user_id`。
- 用户前端页面收到支付完成回调后，后端仍需调用查询订单 API 确认最终状态。

## `U_JSAPI` / `U_NATIVE` 请求字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `qr_code` | String | N | 台牌码 URL；官方说明 `U_JSAPI` 必填 |
| `addn_data` | String | N | 收款方附加数据 |
| `customer_ip` | String | N | 持卡人 IP；JS 支付必填 |
| `front_url` | String | N | 前台通知地址 |
| `order_desc` | String | N | 订单描述 |
| `payee_comments` | String | N | 收款方附言 |
| `payee_info` | Object | N | 收款方信息 |
| `req_reserved` | String | N | 请求方自定义域 |
| `user_id` | String | N | 银联用户标识 |

### `payee_info`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `mer_cat_code` | String | N | 商户类别码 |
| `sub_id` | String | N | 子商户编号 |
| `sub_name` | String | N | 子商户名称 |
| `term_id` | String | N | 终端号 |

## `U_MICROPAY` 请求字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `auth_code` | String | N | 用户付款码 |
| `currency_code` | String | N | 币种 |
| `invoice_st` | String | N | 是否支持发票 |
| `mer_cat_code` | String | N | 商户类别 |
| `pnr_ins_id_cd` | String | N | 服务商机构标识码 |
| `specfeeinfo` | String | N | 特殊计费信息 |
| `term_id` | String | N | 终端号 |
| `addn_data` | String | N | 收款方附加数据 |
| `pid_info` | Object | N | 服务商信息 |

### `pid_info`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `pnr_order_id` | String | N | 服务商订单号 |
| `pid_sct` | String | N | 服务商场景类型 |
| `trade_scene` | String | N | 交易场景 |

## 同步返回银联扩展

同步返回的 `method_expand` 中，银联侧常见字段如下：

| 字段 | 说明 |
|------|------|
| `qr_valid_time` | 正扫 / JS 场景二维码有效期 |
| `coupon_info[]` | 银联优惠信息 |
| `acc_no` | 付款账号 |

## 异步 `unionpay_response`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `coupon_info` | Array | N | 银联优惠信息 |
| `acc_no` | String | N | 付款账号 |

### `coupon_info[]`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `addnInfo` | String | N | 附加信息 |
| `spnsrId` | String | Y | 出资方 |
| `type` | String | Y | 项目类型 |
| `offstAmt` | String | Y | 抵消交易金额 |
| `id` | String | N | 项目编号 |
| `desc` | String | N | 项目简称 |

## 银联实现备注

- `U_JSAPI` 场景下，`user_id` 与 `customer_ip` 都是官方强调的关键字段。
- `U_NATIVE` 与 `U_JSAPI` 使用同一批扩展结构，但并不是每次都要求把所有字段传满。
- `U_MICROPAY` 的 `pid_info` 属于银联反扫独有扩展，不要混到 JS / 正扫请求里。
- `U_MICROPAY.auth_code` 必须来自扫码设备实时采集。
