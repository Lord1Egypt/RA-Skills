# 领星多平台 V2 接口参考

所有接口均为 POST 请求，域名：`https://openapi.lingxing.com`

---

## MultiPlatOrderV2 - 查询订单管理订单列表

**路径**: `/pb/mp/order/v2/list`
**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| offset | 是 | int | 分页偏移量 |
| length | 是 | int | 分页长度，上限500 |
| date_type | 否* | string | update_time/global_purchase_time/global_delivery_time/global_payment_time/delivery_time（仅按平台单号查时可不传） |
| start_time | 否* | int | 开始时间戳（秒），查询跨度不超过31天 |
| end_time | 否* | int | 结束时间戳（秒） |
| store_id | 否 | array | 多平台店铺ID |
| platform_code | 否 | array | 平台code（10001=Amazon，10002=Shopify，10003=eBay，10008=Walmart，10011=TikTok，10021=SHEIN，10022=Temu全托管，10024=Temu半托管 等） |
| platform_order_nos | 否 | array | 平台单号列表，上限200（eBay/Newegg/Coupang/Shopify/Mercado/Shopline 除外） |
| platform_order_names | 否 | array | 特定平台单号（eBay/Newegg/Coupang/Shopify/Mercado/Shopline 用此字段） |
| order_status | 否 | int | 1=同步中，2=已同步，3=待付款，4=待审核，5=待发货，6=已发货，7=已取消，8=不显示，9=平台发货 |
| include_delete | 否 | boolean | 是否包含已删除订单 |

**关键返回字段**: platform_code, store_id, platform_order_no, order_status, purchase_time, payment_time, delivery_time, buyer_name, shipping_address, items[msku/sku/quantity/price], freight_amount

---

## StoreInfoV2 - 查询多平台店铺信息

**路径**: `/pb/mp/shop/v2/getSellerList`
**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| platform_code | 否 | array | 平台code列表 |
| is_sync | 否 | int | 1=启用，0=停用 |
| status | 否 | int | 1=正常授权，0=授权失败 |
| offset | 否 | int | 分页偏移量 |
| length | 否 | int | 分页长度，上限200 |

**关键返回字段**: store_id, sid, store_name, platform_code, platform_name, currency, is_sync

---

## PairListV2 - 查询多平台配对列表

**路径**: `/pb/mp/listing/v2/getPairList`
**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| msku | 否 | array | MSKU列表 |
| sku | 否 | array | 本地SKU列表 |
| store_ids | 否 | array | 店铺ID列表 |
| platform_codes | 否 | array | 平台code列表 |
| start_time | 否 | string | 操作开始时间 |
| end_time | 否 | string | 操作结束时间 |
| use_cursor | 否 | boolean | 使用分页游标（数据多时推荐） |
| cursor_id | 否 | boolean | 游标ID（use_cursor=true时必填） |
| offset | 否 | int | 分页偏移量 |
| length | 否 | int | 分页条数 |

**关键返回字段**: msku, sku, store_id, platform_code, pair_time

---

## QueryShippingListV2 - 查询平台仓发货单列表 v2

**路径**: `/basicOpen/multiplatform/query/shippingList`
**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| platformCodes | 是 | array | 10008=Walmart，10011=TikTok，10022=Temu，10027=Shein |
| timeField | 否 | int | 1=创建时间，2=发货时间，3=开船时间，4=预计到港，5=实际妥投，6=实际发货 |
| startTime | 否 | string | 开始时间，Y-m-d |
| endTime | 否 | string | 结束时间，Y-m-d |
| shippingListStatus | 否 | int | 0=待配货，1=待发货，2=已发货，3=已作废 |
| pickingStatus | 否 | string | 1=已拣货，0=待拣货 |
| searchField | 否 | int | 1=MSKU，2=发货单号，7=货件单号，8=商品条码 |
| searchSingleValue | 否 | string | 模糊搜索值 |
| storeIds | 否 | array | 店铺ID列表 |
| offset | 否 | int | 分页偏移量 |
| length | 否 | int | 分页长度 |

**关键返回字段**: 发货单列表（发货单号、状态、货件、商品明细）

---

## QueryShippingListPage - 查询平台仓发货单列表（Walmart 旧版）

**路径**: `/cepf/warehouse/api/openApi/queryShippingListPage`
**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| store_id | 否 | array | 店铺ID |
| shipping_list_codes | 否 | array | 发货单编号，上限100 |
| cargo_code | 否 | string | 货件单号 |
| shipping_list_status | 否 | int | 0=待配货，1=待发货，2=已发货，3=已作废 |
| start_time | 否 | string | 创建开始时间，Y-m-d |
| end_time | 否 | string | 创建结束时间，Y-m-d |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 分页长度，默认15，上限200 |

**关键返回字段**: 发货单列表（仅支持Walmart，建议改用 QueryShippingListV2）

---

## QueryWFSCargoPage - 查询 WFS 货件列表

**路径**: `/cepf/warehouse/api/openApi/queryWFSCargoPage`
**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| store_id | 否 | array | 店铺ID |
| cargo_status_list | 否 | array | 0=PENDING_SHIPMENT_DETAILS，1=AWAITING_DELIVERY，2=RECEIVING_IN_PROGRESS，3=CLOSED，4=CANCELLED |
| inbound_order_id | 否 | string | 入库订单编号 |
| start_time | 否 | string | 创建开始时间，Y-m-d |
| end_time | 否 | string | 创建结束时间，Y-m-d |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 分页长度，默认15，上限200 |

**关键返回字段**: 货件列表（货件号、状态、入库数量、商品明细）

---

## QueryWFSInventionPage - 查询 WFS 库存列表

**路径**: `/cepf/warehouse/api/openApi/queryWFSInventionPage`
**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| store_id | 是 | array | 店铺ID |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 分页长度，默认15，上限200 |

**关键返回字段**: records[item_id, gtin, available_quantity, inbound_quantity, platform_product_status, ats03_months, ats36_months, ats69_months, ats912_months, ats1_years, last30_days_po_units]

---

## AliexpressListV2 - 查询 AliExpress 在线商品（托管模式）

**路径**: `/basicOpen/multiplatform/aliexpress/list/v2`
**参数**: offset, length（分页）；store_id（店铺筛选）等

**关键返回字段**: 商品列表（product_id, msku, title, price, status, inventory）

---

## aliexpressList - 查询 AliExpress 在线商品（自运营）

**路径**: `/basicOpen/multiplatform/aliExpress/list`
**参数**: offset, length（分页）；store_id, msku 等

**关键返回字段**: item_id, msku, status, price, title

---

## eBayList - 查询 eBay 在线商品列表

**路径**: `/basicOpen/multiplatform/ebay/list`
**参数**: offset, length（分页）；store_id 等

**关键返回字段**: msku, listing_status, site_name, accept_price, product_auto_restock_response

---

## walmartList - 查询 Walmart 在线商品

**路径**: `/basicOpen/multiplatform/walmart/list`
**参数**: offset, length（分页）；store_id 等

**关键返回字段**: title, store_name, fulfillment_type_name, buy_box_shipping_price, quantityAdjustBefore, offer_end_date

---

## TemuList - 查询 Temu 在线商品

**路径**: `/basicOpen/multiplatform/temu/list`
**参数**: offset, length（分页）；store_id 等

**关键返回字段**: mskuId, title, principalName, usableInventory, attribute, wareHouseDataList

---

## TemuCargo - 查询 Temu 货件

**路径**: `/basicOpen/multiplatform/temu/cargo`
**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| startTime | 是 | string | 开始时间 |
| offset/length | 否 | int | 分页 |

**关键返回字段**: cargoGoodListResponses[mskuCargo/purchaseOrderSn/sku], deliverPackageNum, deliveryAddress

---

## TikTokList - 查询 TikTok 在线商品

**路径**: `/basicOpen/multiplatform/tiktok/list`
**参数**: offset, length（分页）；store_id 等

**关键返回字段**: id, storeId, pname, usableInventory, currency

---

## SheinList - 查询 Shein 在线商品

**路径**: `/basicOpen/multiplatform/shein/list`
**参数**: offset, length（分页）；store_id 等

**关键返回字段**: mskuId, title, principalName, status, wareHouseDataList, attribute

---

## ShopifyVariantList - 查询 Shopify 在线商品

**路径**: `/basicOpen/multiplatform/shopify/variantList`
**参数**: offset, length（分页）；store_id 等

**关键返回字段**: title, store_name, weight, listing_start_time, location_infos

---

## CoupangStockList - 查询 Coupang 库存

**路径**: `/basicOpen/multiplatform/coupang/stockSearch`
**参数**: offset, length（分页）；store_id 等

**关键返回字段**: stockPage[records[storeName, ...]]

---

## FbsStockList - 查询 FBS 库存

**路径**: `/basicOpen/multiplatform/fbs/stockSearch`
**参数**: offset, length（分页）；store_id 等

**关键返回字段**: records[shopSkuId, whsId, irApprovalQty, last60Sold, notMovingTag, gmtCreate]

---

## FbtStockList - 查询 FBT 库存

**路径**: `/basicOpen/multiplatform/fbt/stockSearch/v2`
**参数**: offset, length（分页）；store_id 等

**关键返回字段**: page[records[goodReferenceCode, totalInventoryQuantity, ...]]

---

## FbtStockSearch - 查询 Temu 库存

**路径**: `/basicOpen/multiplatform/fbt/stockSearch`
**参数**: offset, length（分页）；store_id 等

**关键返回字段**: list[mskuList[msku], quantity, adviceQuantity, inventorySaleDays, warehouseInventoryNum, todaySaleVolume]

---

## FullList - 查询 FULL 库存

**路径**: `/basicOpen/multiplatform/full/stockSearch`
**参数**: offset, length（分页）；store_id 等

**关键返回字段**: 库存记录列表

---

## WayfairStockList - 查询 Wayfair 库存

**路径**: `/basicOpen/multiplatform/wayfair/stockSearch`
**参数**: offset, length（分页）；store_id 等

**关键返回字段**: page[records[supplierPartNumber, heldQty, options, ...], total]

---

## LineList - 查询 Line 在线商品

**路径**: `/basicOpen/multiplatform/line/list`
**参数**: offset, length（分页）；store_id 等

**关键返回字段**: list[bid, imgUrl, children[id/pid/productUniqueId/storeName/availableNumber]]

---

## addCargoGoodsList - 查询 WFS 货件可添加商品列表

**路径**: `/basicOpen/multiplatform/cargo/addCargoGoods/list`
**参数**: store_id 等

**关键返回字段**: item_id 等商品信息

---

## WalmartPaymentQueryPage - 查询报告详情（Walmart Payment）

**路径**: `/cepf/fms/openapi/walmartPayment/queryPage`
**参数**: store_id, report_date, offset, length 等

**关键返回字段**: records[transaction_key, partner_gtin, product_type, commission_rule, ship_to_zipcode, ...]

---

## WalmartPaymentQueryReport - 查询可用报告列表（Walmart Payment）

**路径**: `/cepf/fms/openapi/walmartPayment/queryReport`
**参数**: store_id 等

**关键返回字段**: list[report_date, ...]

---

## WalmartCommentList - 查询 Walmart Review 列表

**路径**: `/basicOpen/multiplatform/walmart/queryCommentList`
**参数**: store_id, start_date, end_date, offset, length 等

**关键返回字段**: records[commentTitle, productMsku, storeName, title, ...], current, total

---

## profitReportMsku - 查询结算利润报表（MSKU 维度）

**路径**: `/basicOpen/multiplatform/profit/report/msku`
**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| startDate | 是 | string | 开始结算日期，Y-m-d |
| endDate | 是 | string | 结束结算日期，Y-m-d |
| offset | 是 | int | 分页偏移量，默认0 |
| length | 是 | int | 分页长度，默认1000 |
| platformCodeS | 否 | array | 平台code列表 |
| sids | 否 | string | 店铺ID，逗号分隔 |
| mids | 否 | string | 国家ID，逗号分隔 |
| currencyCode | 否 | string | 原币种/USD/EUR/GBP/CNY |
| searchField | 否 | string | msku/local_sku/platform_order_no |
| searchValue | 否 | string | 搜索值 |

**关键返回字段**: totalSum[salesNum, refundNum, buyerFreightAmount, platformLogisticsAmount, platformFineAmount, currencyIcon]，列表明细

---

## profitReportOrder - 查询结算利润报表（订单维度）

**路径**: `/basicOpen/multiplatform/profit/report/order`
**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| startDate | 是 | string | 开始结算日期，Y-m-d |
| endDate | 是 | string | 结束结算日期，Y-m-d |
| offset | 是 | int | 分页偏移量，默认0 |
| length | 是 | int | 分页长度，默认200 |
| searchDateType | 否 | int | 1=下单时间，2=结算日期（默认），3=发货日期 |
| transactionTypeS | 否 | array | 0=销售，2=退货，4=退款，5=补发，6=调整，7=其他 |
| platformCodeS | 否 | array | 平台code列表 |
| currencyCode | 否 | string | 汇率币种 |

**关键返回字段**: totalSum[salesNum, refundRate, platformOtherIncomeAmount, promotionExtendAmount]，订单明细列表

---

## profitReportSeller - 查询结算利润报表（店铺维度）

**路径**: `/basicOpen/multiplatform/profit/report/seller`
**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| startDate | 是 | string | 开始结算日期，Y-m-d |
| endDate | 是 | string | 结束结算日期，Y-m-d |
| offset | 是 | int | 分页偏移量，默认0 |
| length | 是 | int | 分页长度，默认1000 |
| platformCodeS | 否 | array | 平台code列表 |
| sids | 否 | string | 店铺ID，逗号分隔 |
| currencyCode | 否 | string | 汇率币种 |

**关键返回字段**: totalSum[buyerFreightAmount, refundNum, platformLogisticsAmount, platformFineAmount, currencyIcon]，店铺维度明细

---

## profitReportSku - 查询结算利润报表（SKU 维度）

**路径**: `/basicOpen/multiplatform/profit/report/sku`
**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| startDate | 是 | string | 开始结算日期，Y-m-d |
| endDate | 是 | string | 结束结算日期，Y-m-d |
| mids | 是 | string | 国家ID，逗号分隔 |
| offset | 是 | int | 分页偏移量，默认0 |
| length | 是 | int | 分页长度，默认1000 |
| platformCodeS | 否 | array | 平台code列表 |
| currencyCode | 否 | string | 汇率币种 |

**关键返回字段**: totalSum[buyerFreightAmount, refundNum, platformLogisticsAmount, currencyIcon]，SKU 维度明细

---

## newPlatformOrderList - 查询平台订单列表（新）

**路径**: `/cepfPlatformOrder/open-api/newPlatformOrder/list`
**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| dateType | 是 | int | 0=平台数据变动时间，1=订购时间，2=订购时间(北京)，3=支付时间，4=支付时间(北京)，5=发货时间 |
| platformCodeList | 否 | array | 平台code（支持TikTok/Temu半托管/Line/Lazada/Shopee/Shopify等） |
| deliveryTypeList | 否 | array | 0=自发货，1=平台发货，2=部分自发货 |
| searchType | 否 | int | 1=sku，2=品名，3=msku，4=商品id，5=平台单号，6=参考号，7=商品标题 |
| searchSingleValue | 否 | string | 模糊搜索值 |
| searchMultiValue | 否 | array | 精确搜索值列表 |
| siteCodeList | 否 | array | 站点列表 |
| pageNum | 否 | int | 页码 |
| pageSize | 否 | int | 每页大小 |

**关键返回字段**: 订单列表（平台单号、状态、购买时间、配送信息、商品明细）

---

## addressReturnAddressList - 查询退件地址列表

**路径**: `/basicOpen/multiplatform/address/returnAddressList`
**参数**: 无必填（可按 store_id 等筛选）

**关键返回字段**: mobile, street_detail 等退件地址信息

---
