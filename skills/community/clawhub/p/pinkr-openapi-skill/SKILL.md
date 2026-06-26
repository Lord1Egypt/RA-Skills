---
name: pinkr_openapi_skill
title: 品氪 OpenApi 开放平台 Skill
description: 品氪提供的OpenApi开放平台，支持门店、导购、会员、订单、退单、库存、商品、积分、储值、卡券、销售等全链路CRM/SCRM数据同步与管理。通过安全认证的API接口实现第三方系统与品氪平台的数据互通。
required_env_vars:
  - PK_APPKEY
  - PK_API_URL
primary_credential:
  - PK_APPKEY
credentials:
  - name: PK_APPKEY
    description: 品氪开放平台分配的APPKEY，用于接口认证
    required: true
    type: secret
  - name: PK_API_URL
    description: 品氪OpenAPI的基础地址
    required: false
    type: string
    default: "http://dev.openapi.pinkr.com"
---

# pinkr_openapi 品氪 OpenApi 开放平台 Skill

本 Skill 由品氪提供 OpenApi 开放平台，支持门店管理、导购管理、会员管理、订单管理、退单管理、库存管理、商品管理、积分管理、储值管理、卡券管理、销售数据同步、营销数据分析、分销管理等全链路 CRM/SCRM 功能。通过调用品氪后端相关原生接口，实现第三方系统与品氪平台的数据互通，所有操作均通过安全认证的 API 接口完成。

```yaml
tags: ["SCRM", "CRM", "openAPI", "api", "会员管理", "订单管理", "商品管理"]
use_when:
  - 用户需要同步门店、导购基础数据到品氪平台
  - 用户需要管理会员信息（查询/新增/更新会员）
  - 用户需要同步订单、退单、发货信息
  - 用户需要管理商品、库存数据
  - 用户需要同步积分、储值、卡券数据
  - 用户需要同步销售小票数据
  - 用户需要查询营销统计数据
  - 用户需要查询分销订单数据
not_for:
  - 非授权的第三方数据访问
  - 商业数据倒卖、非法数据爬取
# 环境变量配置
parameters:
  - name: PK_APPKEY
    description: 品氪开放平台分配的APPKEY
    required: true
    type: secret
    default: process.env.PK_APPKEY
  - name: PK_API_URL
    description: 品氪API基础地址
    required: false
    type: string
    default: process.env.PK_API_URL || "http://dev.openapi.pinkr.com"
```

## 功能说明

根据**用户问句**自动识别意图并调用对应接口，支持以下功能模块：

1. **门店管理**：上传门店基础数据。
2. **导购管理**：上传导购基础数据，支持所属门店绑定。
3. **会员标签**：上传标签分类、标签、会员标签明细，获取标签资料。
4. **订单管理**：获取订单列表及商品明细，更新发货信息，接收第三方订单，更新仓库发货状态。
5. **退单管理**：获取退货退款单、退款单，更新退货退款状态和退款状态，接收第三方退货单。
6. **库存管理**：获取仓库清单和商品清单，批量更新/获取商品库存。
7. **商品管理**：上传商品尺码、颜色、SPU属性，上传商品，上传商品价格（千店千面），全量上传商品。
8. **会员管理**：获取/更新会员信息，更新会员等级，新增会员卡，获取品氪会员信息，新增会员收货地址。
9. **积分管理**：新增会员积分流水。
10. **储值管理**：新增会员储值流水，绑定储值卡，储值卡变动消息推送。
11. **卡券管理**：批量核销卡券。
12. **销售数据**：接收小票（同步第三方订单明细）。
13. **营销数据**：获取会员统计、目标管理、分组信息、标签会员等数据。
14. **分销管理**：获取付费订单列表。
15. **订阅消息服务**：接收品氪端推送的会员、积分、储值、卡券、商品、库存、订单等变更消息。

## 配置

- **PK_APPKEY**：品氪开放平台分配的 APPKEY，需保密。
- **PK_API_URL**：品氪 API 基础 URL，测试环境为 `http://dev.openapi.pinkr.com`。
- 正式环境每接口每秒并发数上限默认为 10。

在使用前，请确保已配置以下环境变量：

```javascript
// 导出APPKEY和API地址
export PK_APPKEY= ${PK_APPKEY} || process.env.PK_APPKEY
export PK_API_URL= process.env.PK_API_URL || "http://dev.openapi.pinkr.com"
```

## 使用方式

1. 在品氪开放平台申请商户号和接口接入 IP 地址。
2. 开放平台分配接入的 APPKEY。
3. 使用 POST 请求接口，所有请求均使用 `Content-Type: application/json`。

## 数据请求格式

所有接口使用统一的 POST 表单方式提交：

```json
{
  "method": "接口名称",
  "appid": "pinkr",
  "data": "请求数据实体(JSON格式字符串)",
  "v": "1"
}
```

| 参数名 | 类型 | 说明 |
| :--- | :--- | :--- |
| method | string | API 接口名称 |
| appid | string | 商户的 appid |
| data | string | 请求数据实体（JSON 格式字符串） |
| v | string | API 协议版本，默认为 1 |

## 公共响应参数

| 参数名 | 类型 | 说明 |
| :--- | :--- | :--- |
| code | string | 状态码 |
| message | string | 信息 |
| data | string | 数据 |

## 状态码

| 代码 | 说明 |
| :--- | :--- |
| 200 | 成功 |
| 400 | 失败 |
| 1001 | 参数非法 |
| 1101 | 类不存在 |
| 1102 | 方法不存在 |
| 1104 | 商户状态未开启 |
| 10001 | APPID 不存在 |
| 10002 | 当前 API 未配置 |
| 10101 | 请求接口错误 |
| 19001 | 订单已存在 |
| 19002 | 原订单不存在 |
| 19003 | 原订单商品明细不存在 |
| 19004 | 不符合拆单条件 |
| 20001 | 退单已存在 |
| 20002 | 退单不存在 |
| 20003 | 退单状态非法 |

---

## 功能概览

| 功能模块 | 接口名称 | 说明 | 状态 |
| --- | --- | --- | --- |
| 获取快递列表 | `common.express.get` | 获取支持的快递公司列表 | 已完成 |
| 上传门店 | `store.upload` | 上传门店基础数据，重复上传覆盖 | 已完成 |
| 上传导购 | `guide.upload` | 上传导购基础数据，支持所属门店绑定 | 已完成 |
| 上传标签分类 | `tag.category.upload` | 上传标签分类主数据 | 已完成 |
| 上传标签 | `tag.tag.upload` | 上传标签主数据 | 已完成 |
| 上传会员标签明细 | `tag.memberTag.upload` | 更新品氪端会员的标签明细 | 已完成 |
| 获取标签资料 | `tag.tag.get` | 获取商户定义的标签基础资料 | 已完成 |
| 获取订单列表 | `order.order.get` | 获取线上订单列表（分页） | 已完成 |
| 获取订单商品明细 | `order.orderGoods.get` | 获取订单商品明细 | 已完成 |
| 更新订单发货信息 | `order.delivery.update` | 更改线上订单发货状态 | 已完成 |
| 接收第三方订单 | `order.order.add` | 接收第三方商城订单到品氪端 | 已完成 |
| 更新订单仓库状态 | `order.storage.updateStatus` | 更改订单仓库提交状态 | 已完成 |
| 获取退货退款单 | `refund.returnRefund.get` | 获取退货退款单列表（分页） | 已完成 |
| 更新退货退款状态 | `refund.returnRefund.status.update` | 商家同意退货/已收货等 | 已完成 |
| 获取退款单 | `refund.refund.get` | 获取申请退款/退款完成列表（分页） | 已完成 |
| 更新退款状态 | `refund.status.update` | 商家同意退款 | 已完成 |
| 接收第三方退货单 | `refund.returnRefund.add` | 接收第三方退货单到品氪端 | 已完成 |
| 获取换货单(弃用) | `exchange.get` | 获取换货单列表（分页） | 已弃用 |
| 更新换货单状态(弃用) | `exchange.status.update` | 更新换货单状态 | 已弃用 |
| 获取仓库清单 | `stock.storageList.get` | 获取需要同步库存的仓库清单 | 已完成 |
| 获取商品清单 | `stock.goodsList.get` | 获取需要同步库存的商品清单 | 已完成 |
| 批量更新商品库存 | `stock.goodsStock.batchUpdate` | 批量同步商品库存到品氪端 | 已完成 |
| 批量获取商品库存 | `warehouse.goodsStock.get` | 批量获取商品库存（分页） | 已完成 |
| 上传商品尺码 | `goods.size.upload` | 上传商品 SKU 绑定的尺码 | 已完成 |
| 上传商品颜色 | `goods.color.upload` | 上传商品 SKU 绑定的颜色 | 已完成 |
| 上传商品SPU父级属性 | `goods.attributeName.upload` | 上传商品 SPU 父级属性 | 已完成 |
| 上传商品SPU子属性 | `goods.attributeValue.upload` | 上传商品 SPU 子属性 | 已完成 |
| 上传商品 | `goods.goods.upload` | 上传商品 | 已完成 |
| 上传商品价格 | `goods.price.upload` | 上传商品价格（千店千面） | 已完成 |
| 全量上传商品 | `goods.goods.fullUpload` | 全量上传商品（含颜色/尺码/属性自动创建） | 已完成 |
| 获取会员信息 | `member.info.get` | 获取品氪端会员信息 | 已完成 |
| 更新会员等级 | `member.level.update` | 更新品氪端会员等级 | 已完成 |
| 更新会员信息 | `member.info.update` | 更新品氪端会员信息 | 已完成 |
| 新增会员卡 | `member.add` | 第三方会员开卡后同步至品氪 | 已完成 |
| 获取品氪会员信息 | `pinkrMember.info.get` | 获取品氪端会员信息（缓存60秒） | 已完成 |
| 新增会员收货地址 | `member.address.add` | 新增会员收货地址 | 已完成 |
| 新增会员积分流水 | `integral.add` | 新增会员积分流水 | 已完成 |
| 新增会员储值流水 | `deposit.add` | 新增会员储值流水 | 已完成 |
| 新增储值卡绑定 | `deposit.card.bind` | 新增会员与储值卡绑定信息 | 已完成 |
| 储值卡消息推送 | `deposit.card.sendTemplateMessage` | 储值卡流水变动发送消息 | 开发中 |
| 批量核销卡券 | `coupon.status.batchUse` | 批量核销品氪端会员卡券 | 已完成 |
| 接收小票 | `sale.order.add` | 同步第三方订单明细到品氪端 | 已完成 |
| 获取会员统计 | `data.member.count` | 获取会员相关统计数据 | 已完成 |
| 获取目标管理 | `data.target.get` | 获取商户目标管理（销售/开卡目标） | 已完成 |
| 获取会员分组资料 | `data.member.group.groupInfo.get` | 获取会员分组基础资料 | 已完成 |
| 获取预设分组类型 | `data.member.group.config.get` | 获取预设会员分组类型 | 已完成 |
| 获取分组下会员 | `data.member.group.get` | 获取对应会员分组下的会员 | 已完成 |
| 获取标签基础资料 | `data.Tag.get` | 获取商户标签基础资料 | 已完成 |
| 获取标签下会员 | `data.Tag.Member.get` | 获取商户标签下的会员 | 已完成 |
| 获取付费订单 | `distribution.paidOrder.get` | 获取分销付费订单列表（分页） | 已完成 |

---

## 前置要求

- 用户需在品氪开放平台申请商户号并获取 `PK_APPKEY`。
- 接入前需在品氪开放平台配置接口接入 IP 地址。
- 正式环境每接口每秒并发数上限默认为 10。
- 请求使用 POST 表单方式提交，`appid` 字段传 `pinkr`。

---

## 接口说明

### 1. 获取支持的快递列表

- **功能**：获取支持的快递列表
- **接口名称**：`common.express.get`
- **请求参数**：无
- **返回数据**：

| 参数名称 | 参数类型 | 参数说明 |
| :--- | :--- | :--- |
| express_name | string | 快递公司名称 |
| express_code | string | 快递公司代码 |

---

### 2. 上传门店

- **功能**：上传门店基础数据，重复上传会覆盖上一次数据
- **接口名称**：`store.upload`
- **请求参数**：

| 参数名称 | 参数类型 | 必须 | 参数说明 | 示例值 |
| :--- | :--- | :--- | :--- | :--- |
| store_no | string | 是 | 门店代码 | |
| store_name | string | 是 | 门店名称 | |
| address | string | 否 | 详细地址 | |
| telephone | string | 是 | 电话号码 | |
| business_model | int | 否 | 经营模式：0 直营店 / 1 联营店 / 2 加盟店 | |

---

### 3. 上传导购

- **功能**：上传导购基础数据，重复上传会覆盖上一次数据
- **接口名称**：`guide.upload`
- **请求参数**：

| 参数名称 | 参数类型 | 必须 | 参数说明 |
| :--- | :--- | :--- | :--- |
| guide_no | string | 是 | 导购编号 |
| guide_name | string | 是 | 导购名称 |
| store_no | string | 是 | 门店代码 |
| position | int | 是 | 职位：0 店长 / 1 导购 |
| sex | int | 是 | 性别：1 男 / 2 女 |
| guide_status | int | 是 | 状态：0 在职 / 2 离职 |
| phone | string | 否 | 手机号码 |
| entry_date | date | 否 | 入职日期（格式：2019-03-21） |
| birthday | date | 否 | 生日（格式：2019-03-21） |
| belonging_store | object[] | 否 | 所属的门店 |
| >> store_no | string | 是 | 门店代码 |

---

### 4. 上传标签分类

- **功能**：上传标签分类主数据
- **接口名称**：`tag.category.upload`
- **请求参数**：

| 参数名称 | 参数类型 | 必须 | 参数说明 |
| :--- | :--- | :--- | :--- |
| category_code | string | 是 | 标签分类代码 |
| category_name | string | 是 | 标签分类名 |

---

### 5. 上传标签

- **功能**：上传标签主数据
- **接口名称**：`tag.tag.upload`
- **请求参数**：

| 参数名称 | 参数类型 | 必须 | 参数说明 |
| :--- | :--- | :--- | :--- |
| category_code | string | 是 | 标签分类代码 |
| tag_code | string | 是 | 标签代码 |
| tag_name | string | 是 | 标签名 |

---

### 6. 上传会员标签明细

- **功能**：更新品氪端会员的标签明细
- **接口名称**：`tag.memberTag.upload`
- **请求参数**：

| 参数名称 | 参数类型 | 必须 | 参数说明 |
| :--- | :--- | :--- | :--- |
| card_no | string | 是 | 品氪端会员唯一识别卡号ID |
| tags | object[] | 是 | 标签数组 |
| tags.*.category_code | string | 是 | 标签分类代码 |
| tags.*.tag_code | string | 是 | 标签代码 |

---

### 7. 获取标签资料

- **功能**：获取商户定义的标签基础资料
- **接口名称**：`tag.tag.get`
- **请求参数**：无
- **返回数据**：

| 参数名称 | 参数类型 | 参数说明 |
| :--- | :--- | :--- |
| category_name | string | 标签分类名（如果为空，则是一级标签分类） |
| tag_name | string | 二级标签名 |

---

### 8. 获取订单列表（分页）

- **功能**：获取线上订单列表，被拆单生成的新子订单不会显示
- **接口名称**：`order.order.get`
- **请求参数**：

| 参数名称 | 参数类型 | 必须 | 参数说明 |
| :--- | :--- | :--- | :--- |
| order_time_start | datetime | 否 | 下单开始时间 |
| order_time_end | datetime | 否 | 下单结束时间 |
| update_time_start | datetime | 否 | 更新开始时间 |
| update_time_end | datetime | 否 | 更新结束时间 |
| order_status | string | 是 | 订单状态：-2 已拆单 / 1 待发货 / 4 已发货 |
| express_type | int | 否 | 物流类型：0 自提 |
| order_nos | string | 否 | 订单号，多个用逗号分隔 |

**返回数据主要字段**：

| 参数名称 | 参数类型 | 参数说明 |
| :--- | :--- | :--- |
| order_no | string | 订单号 |
| crm_card_no | string | CRM卡号 |
| erp_card_no | string | ERP卡号 |
| bind_guide_no | string | 绑定导购编号 |
| bind_store_no | string | 绑定门店编号 |
| order_money | decimal | 订单金额 |
| order_fact_money | decimal | 实付金额 |
| customer_price | string | 会员折扣优惠金额 |
| coupon_price | decimal | 卡券优惠金额 |
| promotion_price | decimal | 促销活动优惠金额 |
| bonus_price | decimal | 积分抵现优惠金额 |
| postage_price | decimal | 运费金额 |
| consume_number | int | 订单商品数量 |
| order_status | string | 订单状态 |
| express_type | int | 物流类型 |
| express_name | string | 快递公司名称 |
| express_no | string | 快递单号 |
| username | string | 收货人 |
| mobile | string | 收货人手机 |
| order_time | datetime | 下单时间 |
| pay_time | datetime | 付款时间 |
| delivery_time | datetime | 发货时间 |
| payments | array[object] | 支付方式列表 |

> 订单金额计算逻辑：`order_fact_money = order_money - customer_price - promotion_price - coupon_price - bonus_price + postage_price + wipe_off_price + change_price`

---

### 9. 获取订单商品明细

- **功能**：获取订单商品明细
- **接口名称**：`order.orderGoods.get`
- **请求参数**：

| 参数名称 | 参数类型 | 必须 | 参数说明 |
| :--- | :--- | :--- | :--- |
| order_no | string | 是 | 订单号 |

**返回数据主要字段**：

| 参数名称 | 参数类型 | 参数说明 |
| :--- | :--- | :--- |
| order_no | string | 订单号 |
| order_goods | array[object] | 订单商品明细 |
| order_goods.*.goods_sn | string | 商品编号 |
| order_goods.*.goods_name | string | 商品名称 |
| order_goods.*.sku_code | string | SKU代码 |
| order_goods.*.color_code | string | 颜色代码 |
| order_goods.*.size_code | string | 尺码代码 |
| order_goods.*.number | int | 数量 |
| order_goods.*.goods_tag_price | decimal | 吊牌单价 |
| order_goods.*.goods_real_price | decimal | 现售单价 |
| order_goods.*.goods_fact_money | decimal | 商品实付总金额 |

> 商品实付单价 = goods_fact_money / number

---

### 10. 更新订单发货信息

- **功能**：更改线上订单发货状态
- **接口名称**：`order.delivery.update`
- **请求参数**：

| 参数名称 | 参数类型 | 必须 | 参数说明 |
| :--- | :--- | :--- | :--- |
| order_no | string | 是 | 原订单号 |
| channel_order_no | string | 是 | 渠道订单号 |
| express_name | string | 是 | 快递公司名称 |
| express_code | string | 是 | 快递公司编号 |
| express_no | string | 是 | 物流单号 |
| is_split | int | 是 | 是否拆单：0 否 |
| delivery_goods | array[object] | 是 | 商品明细 |

**delivery_goods 商品明细**：

> 必须传商品『款 goods_sn、外部编码 sku_code』或『款 goods_sn、色 color_code、码 size_code』参数，两种方式二选一。

| 参数名称 | 参数类型 | 必须 | 参数说明 |
| :--- | :--- | :--- | :--- |
| goods_sn | string | 是 | 商品编号 |
| color_code | string | 否 | 颜色代码，与外部编码方式二选一 |
| size_code | string | 否 | 尺码代码，与外部编码方式二选一 |
| sku_code | string | 否 | SKU外部编码，与款色码方式二选一 |
| deliver_storage_code | string | 是 | 发货仓库编号 |

---

### 11. 接收第三方订单

- **功能**：接收第三方商城订单到品氪端
- **接口名称**：`order.order.add`
- **注意事项**：
  - 拆单后只传子单，但订单金额、优惠等都需要相应拆分
  - 所属门店代码为第三方商城在品氪的虚拟门店代码
  - 明细的合计金额必须等于主数据的金额，明细的合计数量必须等于主数据的数量
  - 订单金额计算逻辑：`order_fact_money = order_money - customer_price - promotion_price - coupon_price - bonus_price + postage_price`

**请求参数**：

| 参数名称 | 参数类型 | 必须 | 参数说明 |
| :--- | :--- | :--- | :--- |
| channel_order_no | string | 是 | 第三方单号 |
| channel_delivery_no | string | 是 | 第三方发货单号（子单号） |
| source | string | 是 | 来源：douyin 抖音 |
| order_status | string | 是 | 订单状态：2 已发货 |
| store_no | string | 是 | 所属门店代码 |
| guide_no | string | 否 | 所属导购代码 |
| delivery_store_no | string | 是 | 发货门店代码 |
| card_no | string | 否 | 品氪端会员唯一识别卡号 |
| order_mobile | string | 否 | 下单手机号 |
| channel_card_no | string | 否 | 渠道卡号 |
| coupon_codes | string[] | 否 | 优惠券 |
| order_time | datetime | 否 | 下单时间（Y-m-d H:i:s） |
| pay_time | datetime | 否 | 付款时间 |
| delivery_time | datetime | 否 | 发货时间 |
| finish_time | datetime | 否 | 完成时间 |
| express_name | string | 否 | 快递公司名称 |
| express_code | string | 否 | 快递公司代码 |
| express_no | string | 否 | 快递单号 |
| username | string | 否 | 收货人 |
| mobile | string | 否 | 收货人手机 |
| province | string | 否 | 省份名称 |
| city | string | 否 | 城市名称 |
| district | string | 否 | 地区名称 |
| address | string | 否 | 详细地址 |
| consume_number | int | 是 | 订单商品数量 |
| order_money | decimal | 是 | 订单吊牌总金额 |
| order_fact_money | decimal | 是 | 实付金额 |
| customer_price | decimal | 否 | 会员折扣优惠金额 |
| coupon_price | decimal | 否 | 卡券优惠金额 |
| promotion_price | decimal | 否 | 促销活动优惠金额 |
| bonus_price | decimal | 否 | 积分抵现优惠金额 |
| postage_price | decimal | 否 | 运费金额 |
| remark | string | 否 | 备注 |
| goods | object[] | 是 | 订单商品明细 |
| >> goods_sn | string | 是 | 商品款号 |
| >> goods_name | string | 否 | 商品名称 |
| >> sku_code | string | 否 | 外部SKU代码 |
| >> color_code | string | 是 | 颜色代码 |
| >> size_code | string | 是 | 尺码代码 |
| >> number | int | 是 | 商品数量（退单为负） |
| >> goods_tag_price | float | 是 | 单个商品吊牌价 |
| >> goods_real_price | float | 是 | 单个商品现售价 |
| >> goods_discount | int | 是 | 商品折扣（0.9代表9折） |
| >> goods_fact_money | float | 是 | 总商品实际价 |
| payments | object[] | 是 | 结算方式 |
| >> payment_code | string | 是 | 支付代码：wechat / alipay / coupon / deposit / integral / cash / union_pay / other |
| >> amount | decimal | 是 | 金额 |

---

### 12. 更新订单仓库发货状态

- **功能**：更改订单仓库提交状态
- **接口名称**：`order.storage.updateStatus`
- **请求参数**：

| 参数名称 | 参数类型 | 必须 | 参数说明 |
| :--- | :--- | :--- | :--- |
| order_no | string | 是 | 原订单号 |
| status | string | 是 | 状态：0 未转单 |

---

### 13. 获取退货退款单（分页）

- **功能**：获取退货退款单列表
- **接口名称**：`refund.returnRefund.get`
- **请求参数**：

| 参数名称 | 参数类型 | 必须 | 参数说明 |
| :--- | :--- | :--- | :--- |
| refund_time_start | datetime | 否 | 退货单开始时间 |
| refund_time_end | datetime | 否 | 退货单结束时间 |
| update_time_start | datetime | 否 | 更新开始时间 |
| update_time_end | datetime | 否 | 更新结束时间 |
| refund_status | int | 否 | 退货单状态：0 申请退货 / 1 同意退货 |
| express_type | int | 否 | 物流类型：0 自提 / 1 快递 |
| refund_no | string | 否 | 退货单号 |
| order_nos | string | 否 | 订单号，多个用逗号分隔 |
| refund_type | int | 否 | 退货类型：1 退货单 / 2 换货单 |

---

### 14. 更新退货退款单状态

- **功能**：商家同意退货、商家已收货
- **接口名称**：`refund.returnRefund.status.update`
- **请求参数**：

| 参数名称 | 参数类型 | 必须 | 参数说明 |
| :--- | :--- | :--- | :--- |
| refund_no | string | 是 | 退款单号 |
| refund_status | int | 是 | 退款状态：1 同意退货 / 2 关闭退货 / 5 确认收货 / 6 确认退款 |
| return_wechat_money | decimal | 否 | 微信支付返还 |
| return_deposit_money | decimal | 否 | 储值金额返还 |
| return_deposit_gift_money | decimal | 否 | 储值金额赠送返还 |
| username | string | 否 | 收货人（同意退货必填） |
| mobile | string | 否 | 手机号（同意退货必填） |
| address | string | 否 | 商家收货地址（同意退货必填） |

---

### 15. 获取退款单（分页）

- **功能**：获取申请退款（仅退款）、退款完成退款单列表
- **接口名称**：`refund.refund.get`
- **请求参数**：

| 参数名称 | 参数类型 | 必须 | 参数说明 |
| :--- | :--- | :--- | :--- |
| refund_time_start | datetime | 否 | 退单开始时间 |
| refund_time_end | datetime | 否 | 退单结束时间 |
| update_time_start | datetime | 否 | 更新开始时间 |
| update_time_end | datetime | 否 | 更新结束时间 |
| refund_status | int | 否 | 退款状态：0 申请退款 / 1 同意退款 / 3 退款完成 / 4 退款关闭 |
| refund_no | string | 否 | 退单号 |
| order_nos | string | 否 | 订单号，多个用逗号分隔 |

---

### 16. 更新退款状态

- **功能**：商家同意退款
- **接口名称**：`refund.status.update`
- **请求参数**：

| 参数名称 | 参数类型 | 必须 | 参数说明 |
| :--- | :--- | :--- | :--- |
| refund_no | string | 是 | 退款单号 |
| refund_status | int | 是 | 退款状态：1 同意退款 / 6 确认退款 |
| return_wechat_money | decimal | 否 | 微信支付返还 |
| return_deposit_money | decimal | 否 | 储值金额返还 |
| return_deposit_gift_money | decimal | 否 | 储值金额赠送返还 |

---

### 17. 接收第三方退货单

- **功能**：接收第三方退货单到品氪端
- **接口名称**：`refund.returnRefund.add`
- **注意事项**：明细的合计金额必须等于主数据的金额，明细的合计数量必须等于主数据的数量
- **请求参数**：

| 参数名称 | 参数类型 | 必须 | 参数说明 |
| :--- | :--- | :--- | :--- |
| channel_refund_no | string | 是 | 第三方退货单号 |
| channel_delivery_no | string | 否 | 第三方发货单号（子单号） |
| channel_origin_order_no | string | 否 | 关联第三方订单号 |
| source | string | 是 | 来源：douyin 抖音 |
| refund_status | string | 是 | 退单状态：2 顾客退货给商家 |
| card_no | string | 否 | 品氪端会员唯一识别卡号 |
| channel_card_no | string | 否 | 渠道卡号 |
| application_time | datetime | 是 | 申请退货时间 |
| agreement_time | datetime | 否 | 同意退货时间 |
| delivery_time | datetime | 是 | 买家退货时间 |
| confirm_time | datetime | 否 | 确认收货时间 |
| express_name | string | 是 | 快递公司名称 |
| express_code | string | 是 | 快递公司代码 |
| express_no | string | 是 | 快递单号 |
| username | string | 是 | 收货人 |
| mobile | string | 是 | 收货人手机 |
| province | string | 是 | 省份代码（商家收货地址） |
| city | string | 是 | 城市代码（商家收货地址） |
| district | string | 是 | 地区代码（商家收货地址） |
| address | string | 是 | 详细地址（商家收货地址） |
| consume_number | int | 是 | 订单商品数量 |
| order_money | decimal | 是 | 订单吊牌总金额 |
| refund_money | decimal | 否 | 退款金额（负数） |
| refund_bonus | int | 否 | 退款积分 |
| refund_reason | string | 否 | 退款原因 |
| goods | object[] | 是 | 订单商品明细 |
| >> goods_sn | string | 是 | 商品款号 |
| >> goods_name | string | 是 | 商品名称 |
| >> sku_code | string | 是 | 外部SKU代码 |
| >> color_code | string | 是 | 颜色代码 |
| >> size_code | string | 是 | 尺码代码 |
| >> number | int | 是 | 商品数量（负数） |
| >> goods_refund_money | float | 是 | 退款金额（负数） |

---

### 18. 获取仓库清单

- **功能**：获取需要同步商品库存的仓库清单
- **接口名称**：`stock.storageList.get`
- **请求参数**：无
- **返回数据**：

| 参数名称 | 参数类型 | 参数说明 |
| :--- | :--- | :--- |
| storage_code | string | 仓库代码 |
| storage_name | string | 仓库名称 |

---

### 19. 获取商品清单

- **功能**：获取需要同步商品库存的商品清单
- **接口名称**：`stock.goodsList.get`
- **请求参数**：无
- **返回数据**：

| 参数名称 | 参数类型 | 参数说明 |
| :--- | :--- | :--- |
| goods_sn | string | 商品代码 |
| goods_name | string | 商品名称 |
| skus | object[] | SKU列表 |
| >> color_code | string | 颜色代码 |
| >> size_code | string | 尺码代码 |
| >> sku_code | string | SKU代码 |

---

### 20. 批量更新商品库存

- **功能**：批量同步商品库存到品氪端
- **接口名称**：`stock.goodsStock.batchUpdate`
- **注意事项**：goods_stocks 数组限制数量为 300
- **请求参数**：

| 参数名称 | 参数类型 | 必须 | 参数说明 |
| :--- | :--- | :--- | :--- |
| is_summary | int | 否 | 是否汇总仓方式：0 否 / 1 是 |
| goods_stocks | object[] | 是 | 商品库存数组 |
| >> storage_code | string | 是 | 仓库代码 |
| >> goods_sn | string | 否 | 商品款号 |
| >> color_code | string | 否 | 颜色代码 |
| >> size_code | string | 否 | 尺码代码 |
| >> sku_code | string | 否 | 外部SKU代码，存在时不取款色码字段 |
| >> stock_number | int | 是 | 库存数量 |

---

### 21. 批量获取商品库存（分页）

- **功能**：获取品氪端商品库存
- **接口名称**：`warehouse.goodsStock.get`
- **请求参数**：参数都不传时不做筛选，全部返回

| 参数名称 | 参数类型 | 必须 | 参数说明 |
| :--- | :--- | :--- | :--- |
| goods_sn | string | 否 | 商品款号代码，多款用逗号分隔 |
| storage_code | string | 否 | 仓库代码，多个用逗号分隔 |
| change_begin_time | datetime | 否 | 商品库存变更开始时间 |
| change_end_time | datetime | 否 | 商品库存变更结束时间 |

**返回数据**：

| 参数名称 | 参数类型 | 参数说明 |
| :--- | :--- | :--- |
| goods_sn | string | 商品款号 |
| color_code | string | 颜色代码 |
| size_code | string | 尺码代码 |
| sku_code | string | 外部SKU代码 |
| warehouse_code | string | 仓库代码 |
| stock_number | int | 库存数量 |

---

### 22. 上传商品尺码

- **功能**：上传商品 SKU 绑定的尺码
- **接口名称**：`goods.size.upload`
- **请求参数**：

| 参数名称 | 参数类型 | 必须 | 参数说明 |
| :--- | :--- | :--- | :--- |
| size_code | string | 是 | 尺码代码 |
| size_name | string | 是 | 尺码名称 |
| sort | int | 否 | 商城排序，数字越大排序越前 |

---

### 23. 上传商品颜色

- **功能**：上传商品 SKU 绑定的颜色
- **接口名称**：`goods.color.upload`
- **请求参数**：

| 参数名称 | 参数类型 | 必须 | 参数说明 |
| :--- | :--- | :--- | :--- |
| color_code | string | 是 | 颜色代码 |
| color_name | string | 是 | 颜色名称 |

---

### 24. 上传商品 SPU 父级属性

- **功能**：上传商品 SPU 父级属性
- **接口名称**：`goods.attributeName.upload`
- **请求参数**：

| 参数名称 | 参数类型 | 必须 | 参数说明 |
| :--- | :--- | :--- | :--- |
| attribute_name | string | 是 | 父级属性名称 |
| attribute_name_code | string | 是 | 父级属性代码 |

---

### 25. 上传商品 SPU 子属性

- **功能**：上传商品 SPU 子属性
- **接口名称**：`goods.attributeValue.upload`
- **请求参数**：

| 参数名称 | 参数类型 | 必须 | 参数说明 |
| :--- | :--- | :--- | :--- |
| attribute_name_code | string | 是 | 父级属性代码 |
| attribute_value | string | 是 | 子属性名称 |
| attribute_value_code | string | 是 | 子属性代码 |

---

### 26. 上传商品

- **功能**：上传商品
- **接口名称**：`goods.goods.upload`
- **请求参数**：

| 参数名称 | 参数类型 | 必须 | 参数说明 |
| :--- | :--- | :--- | :--- |
| goods_sn | string | 是 | 商品款号 |
| goods_name | string | 是 | 商品名称 |
| skus | array | 是 | 商品SKU对象数组 |
| >> color_code | string | 是 | 颜色代码 |
| >> size_code | string | 是 | 尺码代码 |
| >> sku_code | string | 否 | SKU代码 |
| >> goods_real_price | string | 是 | 商品现售价 |
| >> goods_tag_price | string | 是 | 商品吊牌价 |
| >> goods_discount | string | 是 | 商品折扣 |
| attributes | array | 否 | 商品属性对象数组 |
| >> attribute_name_code | string | 是 | 商品父级属性代码 |
| >> attribute_value_code | string | 是 | 商品子属性代码 |

---

### 27. 上传商品价格（千店千面）

- **功能**：上传商品价格作为千店千面商品价格调价单
- **接口名称**：`goods.price.upload`
- **请求参数**：

| 参数名称 | 参数类型 | 必须 | 参数说明 |
| :--- | :--- | :--- | :--- |
| goods_sn | string | 是 | 商品编号 |
| color_code | string | 否 | 颜色代码，与外部编码方式二选一 |
| size_code | string | 否 | 尺码代码，与外部编码方式二选一 |
| sku_code | string | 否 | SKU外部编码，与款色码方式二选一 |
| store_no | string | 是 | 门店编号 |
| goods_tag_price | decimal | 是 | 商城商品吊牌价 |
| mall_goods_real_price | decimal | 是 | 商城商品现售价 |
| goods_discount | int | 是 | 商品折扣，例：9折传90 |

---

### 28. 全量上传商品

- **功能**：全量上传商品，含颜色、尺码、属性基础资料自动创建
- **接口名称**：`goods.goods.fullUpload`
- **请求参数**：

| 参数名称 | 参数类型 | 必须 | 参数说明 |
| :--- | :--- | :--- | :--- |
| goods_sn | string | 是 | 商品款号 |
| goods_name | string | 是 | 商品名称 |
| skus | array | 是 | 商品SKU对象数组 |
| >> color_code | string | 是 | 颜色代码 |
| >> color_name | string | 是 | 颜色名称 |
| >> size_code | string | 是 | 尺码代码 |
| >> size_name | string | 是 | 尺码名称 |
| >> sku_code | string | 否 | SKU代码 |
| >> goods_real_price | string | 是 | 商品现售价 |
| >> goods_tag_price | string | 是 | 商品吊牌价 |
| >> goods_discount | string | 是 | 商品折扣 |
| attributes | array | 否 | 商品属性对象数组 |
| >> attribute_name | string | 是 | 商品父级属性名称 |
| >> attribute_name_code | string | 是 | 商品父级属性代码 |
| >> attribute_value | string | 是 | 商品子属性名称 |
| >> attribute_value_code | string | 是 | 商品子属性代码 |

---

### 29. 获取会员信息

- **功能**：获取品氪端的会员信息
- **接口名称**：`member.info.get`
- **请求参数**：

| 参数名称 | 参数类型 | 必须 | 参数说明 |
| :--- | :--- | :--- | :--- |
| card_no | string | 否，二选一 | 品氪端会员唯一识别卡号ID |
| mobile | string | 否，二选一 | 会员手机号 |

**返回数据**：

| 参数名称 | 参数类型 | 参数说明 |
| :--- | :--- | :--- |
| card_no | string | 品氪端会员唯一识别卡号ID |
| customer_name | string | 会员姓名 |
| ID_card | string | 身份证（只对银联商户） |
| phone | string | 手机号 |
| remaining_amount | float | 用户余额 |
| remaining_bonus | float | 用户积分 |
| open_card_store_no | string | 开卡门店 |
| open_card_time | string | 开卡时间 |
| bind_guide_no | string | 绑定导购 |
| is_followed | int | 公众号关注状态：-1 取关 |

---

### 30. 更新会员等级

- **功能**：更新品氪端会员等级
- **接口名称**：`member.level.update`
- **请求参数**：

| 参数名称 | 参数类型 | 必须 | 参数说明 |
| :--- | :--- | :--- | :--- |
| card_no | string | 是 | 品氪端会员唯一识别卡号ID |
| level_code | string | 是 | 等级代码 |

---

### 31. 更新会员信息

- **功能**：更新品氪端会员信息
- **接口名称**：`member.info.update`
- **请求参数**：

| 参数名称 | 参数类型 | 必填 | 参数说明 |
| :--- | :--- | :--- | :--- |
| card_no | string | 是 | 品氪端会员唯一识别卡号ID |
| customer_name | string | 否 | 会员姓名 |
| sex | int | 否 | 性别：1 男 / 2 女 |
| mobile | array | 否 | 手机号码 |
| birthday | string | 否 | 出生日期（格式：2019-03-06） |
| channel_card_no | string | 否 | 第三方会员卡号，品氪端为空时补全 |
| bind_guide_no | string | 否 | 绑定导购代码 |

---

### 32. 新增会员卡

- **功能**：第三方会员开卡后同步至品氪
- **接口名称**：`member.add`
- **注意事项**：该会员卡对应积分、储值、小票需通过对应接口上传到品氪
- **请求参数**：

| 参数名称 | 参数类型 | 必填 | 参数说明 |
| :--- | :--- | :--- | :--- |
| channel_card_no | string | 是 | 第三方会员唯一识别卡号ID |
| phone | string | 是 | 手机号 |
| name | int | 是 | 会员名称 |
| sex | array | 是 | 性别：1 男 / 2 女 |
| birthday | string | 是 | 生日（格式：2019-03-06） |
| series_code | string | 否 | 系列代码 |
| level_code | string | 是 | 等级代码 |
| bind_store_no | string | 否 | 绑定门店代码 |
| bind_guide_no | string | 否 | 绑定导购代码 |
| open_card_store_no | string | 否 | 开卡门店代码 |
| open_card_guide_no | string | 否 | 开卡导购代码 |

**返回数据**：

| 参数名称 | 参数类型 | 参数说明 |
| :--- | :--- | :--- |
| data.card_no | string | 品氪端会员唯一识别卡号ID |

---

### 33. 获取品氪会员信息

- **功能**：获取品氪端的会员信息，缓存 60 秒更新一次
- **接口名称**：`pinkrMember.info.get`
- **请求参数**：

| 参数名称 | 参数类型 | 必须 | 参数说明 |
| :--- | :--- | :--- | :--- |
| update_time_start | datetime | 否 | 更新开始时间 |
| update_time_end | datetime | 否 | 更新结束时间 |
| page_size | int | 否 | 每页记录数 |

**返回数据**：

| 参数名称 | 参数类型 | 参数说明 |
| :--- | :--- | :--- |
| pinkr_card_no | string | 品氪端会员唯一识别卡号ID |
| erp_card_no | string | ERP卡号 |
| customer_name | string | 会员姓名 |
| open_card_store_no | string | 开卡门店 |
| open_card_time | string | 开卡时间 |
| bind_guide_no | string | 绑定导购 |
| is_followed | int | 公众号关注状态：-1 取关 |
| is_import_active | int | 是否导入激活：0 否 / 1 是 |
| active_time | datetime | 激活时间 |
| active_store_no | string | 激活门店代码 |
| active_guide_no | string | 激活导购代码 |

---

### 34. 新增会员收货地址

- **功能**：新增会员收货地址
- **接口名称**：`member.address.add`
- **请求参数**：

| 参数名称 | 参数类型 | 必填 | 参数说明 |
| :--- | :--- | :--- | :--- |
| card_no | string | 是 | 品氪端会员唯一识别卡号ID |
| customer_name | string | 是 | 收货人姓名 |
| mobile | string | 是 | 收货人手机号码 |
| province_name | string | 是 | 收货省份名称 |
| city_name | string | 是 | 收货市级名称 |
| area_name | string | 是 | 收货区级名称 |
| address | string | 是 | 详细地址 |

---

### 35. 新增会员积分流水

- **功能**：新增会员积分流水
- **接口名称**：`integral.add`
- **请求参数**：

| 参数名称 | 参数类型 | 必须 | 参数说明 |
| :--- | :--- | :--- | :--- |
| card_no | string | 否 | 品氪端会员唯一识别卡号ID |
| channel_card_no | string | 否 | 第三方会员卡号 |
| channel_integral_no | string | 是 | 第三方积分流水唯一标记 |
| integral_code | string | 是 | 积分来源代码（见下方说明） |
| integral | int | 是 | 变动积分，新增为正，减少为负 |
| consume_no | string | 否 | 关联订单号 |
| change_time | datetime | 是 | 业务发生时间 |

**积分来源代码**：

| 代码 | 说明 |
| :--- | :--- |
| order_offline | 消费新增 |
| order_back | 退货 |
| order_cancel | 订单作废 |
| erp_generate | ERP生成 |
| erp_expire | ERP积分到期 |
| erp_adjust | ERP调整 |
| failure_time_out | 积分过期 |
| consumption_send_bonus | 单笔消费送积分 |
| stored_amount | 充值活动 |
| register | 注册送积分 |
| order_bonus_online | 订单积分商品 |
| from_openapi | 来自openapi |

---

### 36. 新增会员储值流水

- **功能**：新增会员储值流水
- **接口名称**：`deposit.add`
- **请求参数**：

| 参数名称 | 参数类型 | 必须 | 参数说明 |
| :--- | :--- | :--- | :--- |
| card_no | string | 是 | 品氪端会员唯一识别卡号ID |
| channel_card_no | string | 否 | 第三方会员卡号 |
| channel_deposit_no | string | 是 | 第三方储值流水唯一标记 |
| amount_type | string | 是 | 储值类型：0 充值 / 1 消费 |
| store_no | string | 否 | 门店代码 |
| guide_no | string | 否 | 导购代码 |
| amount | decimal | 是 | 储值金额（正负数，见说明） |
| gift_amount | decimal | 是 | 赠送金额 |
| change_time | datetime | 是 | 业务发生时间 |

> 储值金额说明：类型为 0、2、3、5 时为正数，类型为 1、4 时为负数。

---

### 37. 新增储值卡绑定

- **功能**：线下售卡绑定，传递储值卡与会员的绑定信息到品氪
- **接口名称**：`deposit.card.bind`
- **请求参数**：

| 参数名称 | 参数类型 | 必须 | 参数说明 |
| :--- | :--- | :--- | :--- |
| card_no | string | 是 | 品氪端会员唯一识别卡号ID |
| deposited_card_no | string | 是 | 储值卡号 |
| store_no | string | 否 | 销售绑定门店代码 |

---

### 38. 批量核销卡券

- **功能**：批量更改品氪端会员卡券状态
- **接口名称**：`coupon.status.batchUse`
- **请求参数**：

| 参数名称 | 参数类型 | 必须 | 参数说明 |
| :--- | :--- | :--- | :--- |
| coupon_codes | string[] | 是 | 券号数组 |

---

### 39. 接收小票

- **功能**：同步第三方订单明细到品氪端
- **接口名称**：`sale.order.add`
- **请求参数**：

| 参数名称 | 参数类型 | 必须 | 参数说明 |
| :--- | :--- | :--- | :--- |
| order_no | string | 是 | 第三方单号 |
| order_type | int | 是 | 订单类型：0 订单 / 1 退单 |
| origin_order_no | string | 否 | 原订单号，退单时存在 |
| store_no | string | 是 | 门店代码 |
| delivery_store_no | string | 否 | 发货门店 |
| guide_no | string | 是 | 导购代码 |
| guide_performances | object[] | 是 | 导购业绩数组（退单为负） |
| >> guide_no | string | 是 | 导购代码 |
| >> performance_money | decimal | 是 | 导购业绩 |
| >> number | int | 是 | 销售件数 |
| card_no | string | 否 | 品氪端会员唯一识别卡号ID |
| channel_card_no | string | 否 | 第三方会员卡号 |
| coupon_codes | string[] | 否 | 优惠券 |
| order_time | datetime | 是 | 订单时间 |
| consume_number | int | 是 | 订单商品数量（退单为负） |
| order_money | decimal | 是 | 订单吊牌总金额（退单为负） |
| goods | object[] | 是 | 订单商品明细 |
| >> goods_sn | string | 是 | 商品款号 |
| >> goods_name | string | 是 | 商品名称 |
| >> sku_code | string | 否 | 外部SKU代码 |
| >> color_code | string | 是 | 颜色代码 |
| >> size_code | string | 是 | 尺码代码 |
| >> number | int | 是 | 商品数量（退单为负） |
| >> goods_tag_price | float | 是 | 单个商品吊牌价 |
| >> goods_real_price | float | 是 | 单个商品现售价 |
| >> goods_discount | int | 是 | 商品折扣（90代表9折） |
| >> goods_fact_money | float | 是 | 总商品实际价 |
| payments | object[] | 是 | 结算方式 |
| >> payment_code | string | 是 | 支付代码：wechat / alipay / coupon / deposit / integral / cash / other |
| >> code | string | 否 | 关联代码（如卡券号） |
| >> amount | decimal | 是 | 金额 |

---

### 40. 获取会员统计数据

- **功能**：获取会员相关统计数据，默认缓存两个小时
- **接口名称**：`data.member.count`
- **请求参数**：无
- **返回数据**：

| 参数名称 | 参数类型 | 参数说明 |
| :--- | :--- | :--- |
| customer_count | int | 总会员数 |
| followed_customer_count | int | 关注会员数 |
| opened_card_customer_count | int | 开卡会员数 |
| bind_customer_count | int | 绑定会员数 |
| consumed_customer_count | int | 消费会员数 |
| from_erp_customer_count | int | ERP激活会员数 |

---

### 41. 获取商户目标管理

- **功能**：获取商户目标管理，包括销售目标和开卡目标，默认缓存两个小时
- **接口名称**：`data.target.get`
- **请求参数**：

| 参数名称 | 参数类型 | 必须 | 参数说明 |
| :--- | :--- | :--- | :--- |
| target_type | int | 是 | 目标类型：1 销售目标 |
| page | int | 是 | 分页页数 |

---

### 42. 获取会员分组基础资料

- **功能**：获取会员分组基础资料，缓存时间 1 小时
- **接口名称**：`data.member.group.groupInfo.get`
- **请求参数**：

| 参数名称 | 参数类型 | 必须 | 参数说明 |
| :--- | :--- | :--- | :--- |
| type | int | 是 | 分组类型：0 预设分组 |

---

### 43. 获取预设会员分组类型

- **功能**：获取预设会员分组类型
- **接口名称**：`data.member.group.config.get`
- **请求参数**：无

---

### 44. 获取对应会员分组下的会员

- **功能**：获取对应会员分组下的会员
- **接口名称**：`data.member.group.get`
- **请求参数**：

| 参数名称 | 参数类型 | 必须 | 参数说明 |
| :--- | :--- | :--- | :--- |
| group_id | int | 是 | 会员分组 id |
| config_id | int | 否 | 会员分组类型 id |
| page | int | 是 | 分页页数 |

---

### 45. 获取标签基础资料

- **功能**：获取商户标签基础资料，缓存时间 1 小时
- **接口名称**：`data.Tag.get`
- **请求参数**：

| 参数名称 | 参数类型 | 必须 | 参数说明 |
| :--- | :--- | :--- | :--- |
| tag_type | string | 是 | 标签类型：guide_tag 导购打标 |

---

### 46. 获取标签下的会员

- **功能**：获取商户标签下的会员
- **接口名称**：`data.Tag.Member.get`
- **请求参数**：

| 参数名称 | 参数类型 | 必须 | 参数说明 |
| :--- | :--- | :--- | :--- |
| tag_id | int | 是 | 标签 id |

**返回数据**：

| 参数名称 | 参数类型 | 参数说明 |
| :--- | :--- | :--- |
| card_nos | array | 会员品氪卡号数组 |

---

### 47. 获取付费订单（分页）

- **功能**：获取分销付费订单列表
- **接口名称**：`distribution.paidOrder.get`
- **请求参数**：

| 参数名称 | 参数类型 | 必须 | 参数说明 |
| :--- | :--- | :--- | :--- |
| update_time_start | datetime | 否 | 更新开始时间 |
| update_time_end | datetime | 否 | 更新结束时间 |
| distribute_status | int | 否 | 分销状态：0 冻结期 / -1 不结算全额退款 / -2 不结算仅退款 / 1 待结算 / 2 已结算 / 3 不分佣 |

---

## 订阅消息服务

品氪开放平台提供主动推送服务，包括会员信息、积分、储值、卡券等消息订阅类型。第三方订阅后无需手动轮询调用。

### 验签算法

1. 将 appid、appkey、data、method、nonce、timestamp 根据参数名称 ASCII 码表顺序排序，拼接成 query string
2. 以 MD5(32) 算法计算签名字符串
3. 对签名字符串所有字符大写化
4. 将 sign 字段与其他参数一同放在请求中

### 重推机制

品氪开放平台对推送消息提供每 10 秒 1 次，共三次的重推机制。

### 订阅消息接口列表

| 类型 | 接口名称 | 说明 |
| :--- | :--- | :--- |
| 会员-开卡 | `subscribe.member.info.add` | 推送会员信息 |
| 会员-变更 | `subscribe.member.info.update` | 推送会员信息变更 |
| 会员-标签 | `subscribe.member.tag.change` | 推送会员标签变更 |
| 积分 | `subscribe.integral.add` | 推送会员积分流水 |
| 储值-流水 | `subscribe.deposit.add` | 推送会员储值流水 |
| 储值-卡片 | `subscribe.deposit.card.add` | 推送储值卡 |
| 储值-余额变动 | `subscribe.deposit.card.change` | 推送储值卡余额变动 |
| 卡券-信息 | `subscribe.coupon.info.add` | 推送卡券信息 |
| 卡券-明细 | `subscribe.coupon.detail.add` | 推送卡券明细 |
| 卡券-状态变更 | `subscribe.coupon.detail.status.update` | 推送卡券状态变更 |
| 商品-尺码 | `subscribe.goods.size.upload` | 推送商品尺码 |
| 商品-颜色 | `subscribe.goods.color.upload` | 推送商品颜色 |
| 商品-父属性 | `subscribe.goods.attributeName.upload` | 推送商品SPU父级属性 |
| 商品-子属性 | `subscribe.goods.attributeValue.upload` | 推送商品SPU子属性 |
| 商品-信息 | `subscribe.goods.goods.upload` | 推送商品信息 |
| 库存-变动 | `subscribe.stock.goodsStock.change` | 推送商品库存变动 |
| 订单-地址变更 | `subscribe.order.address.update` | 推送订单修改收货地址 |
| 退单-申请退款 | `subscribe.refund.refund.apply` | 推送申请仅退款 |

---

## 错误处理

| 错误码 | 说明 | 处理方式 |
| :--- | :--- | :--- |
| 10001 | APPID 不存在 | 检查 PK_APPKEY 是否正确 |
| 10002 | 当前 API 未配置 | 联系品氪开放平台确认接口权限 |
| 1001 | 参数非法 | 检查请求参数格式和必填项 |
| 1104 | 商户状态未开启 | 联系品氪开放平台确认商户状态 |
| 10101 | 请求接口错误 | 检查 method 参数是否正确 |
| 网络错误 | 连接超时等 | 重试最多 3 次，仍失败则提示"网络异常，请稍后重试" |

## 配置要求

- **PK_APPKEY**：品氪开放平台分配的 APPKEY，需保密。
- **PK_API_URL**：品氪 API 基础 URL。
- **依赖工具**：`curl`（用于发起请求）、`jq`（用于解析 JSON 响应）。
