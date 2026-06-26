# 领星订单 / Listing / 运营操作接口参考

所有接口均为 POST 请求，域名：`https://openapi.lingxing.com`

---

## mwsOrders - 查询亚马逊订单列表

**路径**: `/erp/sc/data/mws/orders`
**令牌桶容量**: 1（串行调用）

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sid | 否 | int | 店铺ID（与 sid_list 任选其一） |
| sid_list | 否 | array | 店铺ID列表，最大长度20 |
| start_date | 是 | string | 开始时间，格式 Y-m-d 或 Y-m-d H:i:s |
| end_date | 是 | string | 结束时间，左闭右开 |
| date_type | 否 | int | 1=订购时间（默认），2=订单修改时间，3=平台更新时间，10=发货时间 |
| order_status | 否 | array | ["Pending","Unshipped","PartiallyShipped","Shipped","Canceled"] |
| sort_desc_by_date_type | 否 | int | 0=不排序（默认），1=降序，2=升序 |
| fulfillment_channel | 否 | int | 1=AFN，2=MFN |
| offset | 否 | int | 分页偏移，默认0 |
| length | 否 | int | 每页条数，默认1000，上限5000 |

**关键返回字段**: sid, seller_name, amazon_order_id, order_status, order_total_amount, fulfillment_channel, is_return, is_return_order, is_replaced_order, item_list[asin/seller_sku/quantity_ordered], purchase_date_local, shipment_date_local, refund_amount

**调用示例**:
```bash
python3 lingxing.py --api mwsOrders \
  --params '{"start_date": "2024-01-01", "end_date": "2024-01-31"}' --all
```

---

## mwsListing - 查询亚马逊 Listing

**路径**: `/erp/sc/data/mws/listing`
**令牌桶容量**: 1（账号级别共享，串行调用）

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sid | 是 | string | 店铺ID，多个用英文逗号分隔，如 "813,814" |
| is_pair | 否 | int | 1=已配对，2=未配对 |
| is_delete | 否 | int | 0=未删除，1=已删除 |
| pair_update_start_time | 否 | string | 配对更新开始时间（北京时间，Y-m-d H:i:s），需 is_pair=1 |
| pair_update_end_time | 否 | string | 配对更新结束时间 |
| listing_update_start_time | 否 | string | All Listing报表更新开始时间（零时区） |
| listing_update_end_time | 否 | string | All Listing报表更新结束时间 |
| search_field | 否 | string | seller_sku / asin / sku |
| search_value | 否 | array | 搜索值列表，上限10个 |
| exact_search | 否 | int | 0=模糊，1=精确（默认） |
| store_type | 否 | int | 1=非低价商店，2=低价商店 |
| offset | 否 | int | 分页偏移，默认0 |
| length | 否 | int | 每页条数，默认1000，上限1000 |

**关键返回字段**: sid, seller_sku, asin, parent_asin, item_name, local_sku, local_name, status, price, landed_price, afn_fulfillable_quantity, afn_unsellable_quantity, fulfillment_channel_type, seller_rank, seller_category_new, review_num, last_star, total_volume, yesterday_volume, fourteen_volume, thirty_volume, seven_amount, thirty_amount

**调用示例**:
```bash
# 查询单个店铺所有 Listing
python3 lingxing.py --api mwsListing \
  --params '{"sid": "813", "is_pair": 1, "is_delete": 0}' --all

# 按 ASIN 精确查询
python3 lingxing.py --api mwsListing \
  --params '{"sid": "813", "search_field": "asin", "search_value": ["B0XXXXXX"]}'
```

---

## orderReturnInformation - 查询多渠道订单退货换货信息

**路径**: `/order/amzod/api/orderDetails/returnInformation`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| order_info | 是 | array | 订单信息列表，上限200条 |
| order_info>>sid | 是 | int | 店铺ID |
| order_info>>seller_fulfillment_order_id | 是 | string | 卖家订单号 |

**关键返回字段**: amazon_order_id, seller_fulfillment_order_id, order_status, purchase_date_local, order_return_replace_tab>>return_tab[return_date/msku/asin/return_quantity/return_reason/return_status/customer_comments], order_return_replace_tab>>replace_tab[replacement_reason/msku/shipment_date]

**调用示例**:
```bash
python3 lingxing.py --api orderReturnInformation \
  --params '{"order_info": [{"sid": 813, "seller_fulfillment_order_id": "xxx-R"}]}'
```

---

## scOrderSetRemark - SC订单设置备注

**路径**: `/basicOpen/platformOrder/scOrder/setRemark`
**令牌桶容量**: 1

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sid | 是 | int | 店铺ID |
| amazonOrderId | 是 | string | 亚马逊订单号 |
| remark | 是 | string | 备注内容（传空字符串可清除备注） |

**返回**: code=0 表示成功，data=null

**调用示例**:
```bash
python3 lingxing.py --api scOrderSetRemark \
  --params '{"sid": 813, "amazonOrderId": "111-1234567-8901234", "remark": "已跟进"}'
```

> **注意**: `scOrderSetRemark` 是写操作，会修改领星系统内订单备注，请谨慎调用。
