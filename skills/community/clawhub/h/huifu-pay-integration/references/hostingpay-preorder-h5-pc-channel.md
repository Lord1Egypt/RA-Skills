# H5、PC 预下单渠道扩展请求参数

> 本文件覆盖 H5/PC 预下单的渠道侧扩展对象：`wx_data`、`alipay_data`、`dy_data`、`unionpay_data`、`terminal_device_data`、`largeamt_data`。


## 目录

- 使用说明
- `wx_data`
- `alipay_data`
- `dy_data`
- `unionpay_data`
- `terminal_device_data`
- `largeamt_data`
- 实现备注

## 使用说明

- 这些字段都挂在请求 `data` 节点下。
- 官方文档把它们定义成 `String(JSON Object)`，也就是外层仍是字符串，内部再放 JSON 对象。
- 只在对应渠道或交易类型下传递，不要把所有渠道对象一次性都塞进去。

## `wx_data`

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| `attach` | 附加数据 | String | 127 | N | 查询接口和支付通知中原样返回 |
| `detail` | 商品详情 | Object | 6000 | N | 单品优惠功能字段 |
| `goods_tag` | 订单优惠标记 | String | 32 | N | 代金券或立减优惠参数 |
| `receipt` | 开发票入口开放标识 | String | 8 | N | 发票入口标识 |
| `scene_info` | 场景信息 | Object | 2048 | N | 当前支持上报门店信息 |
| `promotion_flag` | 单品优惠标识 | String | 1 | N | `Y`=使用单品优惠；若为 `Y`，则 `detail` 必填 |
| `product_id` | 新增商品 ID | String | 32 | N | 直连模式且 `trade_type=T_NATIVE` 时必填 |

### `wx_data.detail`

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| `cost_price` | 订单原价 | String | 12 | N | 用于防止一张小票分多次支付重复享受优惠 |
| `receipt_id` | 商品小票 ID | String | 32 | N | 商家小票 ID |
| `goods_detail` | 单品列表 | Array | 2048 | Y | JSON 数组 |

### `wx_data.detail.goods_detail[]`

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| `goods_id` | 商品编码 | String | 32 | N | 由字母、数字、中划线、下划线组成 |
| `goods_name` | 商品名称 | String | 256 | N | 商品实际名称 |
| `price` | 商品单价 | String | 12 | N | 单位元；如商户有优惠，应传优惠后的单价 |
| `quantity` | 商品数量 | Int | 11 | N | 用户购买数量 |
| `wxpay_goods_id` | 微信侧商品编码 | String | 32 | N | 微信侧商品编码 |

### `wx_data.scene_info`

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| `store_info` | 门店信息 | Object | 2048 | N | 门店信息 |

### `wx_data.scene_info.store_info`

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| `id` | 门店 ID | String | 32 | N | 商户自定义门店编号 |
| `name` | 门店名称 | String | 64 | N | 商户自定义门店名称 |
| `area_code` | 门店行政区划码 | String | 6 | N | 行政区划码 |
| `address` | 门店详细地址 | String | 128 | N | 商户自定义地址 |

## `alipay_data`

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| `alipay_store_id` | 支付宝店铺编号 | String | 32 | N | 支付宝侧店铺编号 |
| `extend_params` | 业务扩展参数 | Object | 2048 | N | 业务扩展参数 |
| `goods_detail` | 商品列表信息 | Array | 2048 | N | 订单包含的商品列表 |
| `merchant_order_no` | 商户原始订单号 | String | 32 | N | 商户原始订单号 |
| `operator_id` | 商户操作员编号 | String | 28 | N | 操作员编号 |
| `product_code` | 销售产品码 | String | 32 | N | 销售产品码 |
| `seller_id` | 卖家支付宝用户号 | String | 28 | N | 卖家支付宝用户号 |
| `store_id` | 商户门店编号 | String | 32 | N | 商户门店编号 |
| `subject` | 订单标题 | String | 256 | N | 直连模式必填 |
| `store_name` | 商家门店名称 | String | 512 | N | 直连模式字段 |
| `ali_business_params` | 商户业务信息 | String | 512 | N | JSON 字符串 |

### `alipay_data.extend_params`

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| `card_type` | 卡类型 | String | 32 | N | 卡类型 |
| `food_order_type` | 点餐场景类型 | String | 20 | N | `QR_ORDER`、`PRE_ORDER`、`HOME_DELIVERY`、`DIRECT_PAYMENT`、`QR_FOOD_ORDER`、`P_QR_FOOD_ORDER`、`SELF_PICK`、`TAKE_OUT`、`OTHER` |
| `hb_fq_num` | 花呗分期数 | String | 5 | N | 花呗分期数 |
| `hb_fq_seller_percent` | 花呗卖家手续费百分比 | String | 3 | N | 花呗商贴支付默认传 `0` |
| `industry_reflux_info` | 行业数据回流信息 | String | 64 | N | 行业数据回流信息 |
| `fq_channels` | 信用卡分期资产方式 | String | 20 | N | `alipayfq_cc` 表示信用卡分期；为空默认花呗 |
| `parking_id` | 停车场 ID | String | 28 | N | 向支付宝停车平台申请的停车场标识 |
| `sys_service_provider_id` | 系统商编号 | String | 64 | N | 系统商签约协议 PID |

### `alipay_data.goods_detail[]`

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| `goods_id` | 商品编号 | String | 32 | Y | 商品编号 |
| `goods_name` | 商品名称 | String | 256 | Y | 商品名称 |
| `price` | 商品单价 | String | 16 | Y | 单位元 |
| `quantity` | 商品数量 | String | 10 | Y | 商品数量 |
| `body` | 商品描述 | String | 1000 | N | 商品描述 |
| `categories_tree` | 商品类目树 | String | 128 | N | 从根类目到叶子类目 ID 组成 |
| `goods_category` | 商品类目 | String | 24 | N | 商品类目 |
| `show_url` | 商品展示地址 | String | 400 | N | 商品展示 URL |

## `dy_data`

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| `sub_appid` | 子商户应用 ID | String | 32 | Y | 抖音开放平台申请的应用 ID，且需与 `sub_mchid` 绑定 |
| `coupon_info` | 优惠标记 | String | - | N | JSON 字符串；可传业务场景、个性化策略或指定优惠信息 |
| `h5_info` | H5 场景信息 | Object | 2048 | Y | H5 场景信息 |
| `scene_info` | 场景信息 | Object | 2048 | Y | 支付场景描述 |

### `dy_data.h5_info`

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| `type` | 场景类型 | String | 32 | Y | `Ios`、`Android`、`Wap` |
| `app_name` | 应用名称 | String | 64 | N | 应用名称 |
| `app_url` | 网站 URL | String | 128 | N | 网站 URL |
| `bundle_id` | iOS Bundle ID | String | 128 | N | iOS 平台 Bundle ID |
| `package_name` | Android PackageName | String | 128 | N | Android 平台包名 |

### `dy_data.scene_info`

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| `payer_client_ip` | 用户终端 IP | String | 45 | Y | 支持 IPv4 和 IPv6 |

## `unionpay_data`

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| `addn_data` | 收款方附加数据 | String | 3000 | N | 参考银联收款方附加数据说明 |
| `area_info` | 地区信息 | String | 32 | N | 地区编码 |
| `front_url` | 前台通知地址 | String | 200 | N | 用户支付完成点击“返回”后，银联浏览器 `POST` 到该地址 |
| `payee_comments` | 收款方附言 | String | 100 | N | 收款方附言 |
| `payee_info` | 收款方信息 | Object | 2048 | N | 收款方信息 |
| `pnr_ins_id_cd` | 服务商机构标识码 | String | 11 | N | 银联分配的服务商机构标识码 |
| `req_reserved` | 请求方自定义域 | String | 500 | N | 请求方自定义域 |
| `term_info` | 终端信息 | String | 32 | N | 终端信息 |
| `pid_info` | 服务商信息 | String | - | N | 官方表里写成字符串，实际承载 JSON 对象 |

### `unionpay_data.payee_info`

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| `mer_cat_code` | 商户类别 | String | 4 | N | 银联商户类别码 |
| `sub_id` | 二级商户代码 | String | 20 | N | 二级商户代码 |
| `sub_name` | 二级商户名称 | String | 100 | N | 二级商户名称 |
| `term_id` | 终端号 | String | 8 | N | 终端号 |

### `unionpay_data.pid_info`

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| `pnr_order_id` | 服务商订单编号 | String | 40 | N | 同一交易日期内不可重复，且不能包含 `-` 或 `_` |
| `pid_sct` | 服务商密文 | String | 8 | N | 按服务商代码标识加密算法生成 |
| `trade_scene` | 场景标识 | String | 8 | N | `1` 表示扫码点餐 |

## `terminal_device_data`

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| `devs_id` | 汇付机具号 | String | 32 | Y | 通过汇付报备的机具必传 |

## `largeamt_data`

| 参数 | 中文名 | 类型 | 长度 | 必填 | 说明 |
|------|--------|------|------|------|------|
| `certificate_name` | 付款方名称 | String | 64 | N | 大额支付三要素校验时必填 |
| `bank_card_no` | 付款方银行卡号 | String | 2048 | N | 大额支付四要素校验时必填；需用汇付公钥 RSA 加密 |

## 实现备注

- `terminal_device_data.devs_id` 在“通过汇付报备机具”场景属于硬要求，缺失时汇付侧可能直接拒单。
- `unionpay_data.front_url` 必须是外网可访问地址，且是用户点击“返回”后由浏览器发起的同步跳转，不是后台异步通知。
- `dy_data.sub_appid` 官方说明要求填写移动应用类型 AppID，同时要确保与 `sub_mchid` 已绑定。
