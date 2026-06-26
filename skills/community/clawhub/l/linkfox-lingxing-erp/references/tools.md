# 领星工具接口参考

所有接口均为 POST 请求，域名：`https://openapi.lingxing.com`

---

## CompetitiveMonitorList - 查询竞品监控列表

**路径**: `/basicOpen/tool/competitiveMonitor/list`
**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| levels | 否 | array | 竞品等级：1=A，2=B，3=C，4=D |
| update_time_start | 否 | string | 更新开始时间，Y-m-d |
| update_time_end | 否 | string | 更新结束时间，Y-m-d |
| search_field | 否 | string | asin |
| search_value | 否 | string | 搜索值，多个用逗号分隔，上限200 |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 分页长度，默认20，上限200 |

**关键返回字段**: asin, asin_url, title, price, currency, level_name, rating, star, review_num, big_category_rank, big_category, small_ranks[small_rank/small_category_text], monitor_status, buybox_price, fbm_seller_num, fba_seller_num, main_image, featurebullets, item_weight, product_dimensions

---

## GetKeywordList - 查询关键词排名列表

**路径**: `/erp/sc/routing/tool/toolKeywordRank/getKeywordList`
**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| offset | 是 | int | 分页偏移量，默认0 |
| length | 是 | int | 分页长度，默认20，上限2000 |
| mid | 否 | int | 国家ID |
| start_date | 否 | string | 开始日期，Y-m-d |
| end_date | 否 | string | 结束日期，Y-m-d |

**关键返回字段**: id, key_word, rank, page, asin, parent_asin, title, country, current_page_rank, sbv_page, rank_text, sbv_text, is_sponsored(1=广告/0=自然), type(1=PC/2=移动端), monitor_time, create_time, keyword_num, monitors

---

## warningMessageGoodsList - 查询预警消息列表（商品）

**路径**: `/basicOpen/settings/warningMessage/goodsList`
**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| start_date | 是 | string | 开始日期【提醒时间】，间隔不超过90天，Y-m-d |
| end_date | 是 | string | 结束日期，Y-m-d |
| show_status | 是 | int | 0=待处理，1=全部 |
| model_id_list | 否 | array | 预警模型：1=Listing调价，2=FBA费变更，3=Listing下架，6=FBA费异常，7=折扣异常，18=业务指标，20=折扣叠加，21=buybox丢失，26=父ASIN变更 |
| sids | 否 | array | 店铺ID |
| search_field | 否 | string | rule_name/asin/msku |
| search_value | 否 | string | 搜索值 |
| offset | 否 | int | 分页偏移量 |
| length | 否 | int | 分页长度，默认50，上限200 |

**关键返回字段**: message_id, asin, title, msku_list, model_name, rule_name, metric, notify_time, receiver, handle_status, read_status, monitor_time

---

## warningMessageInventoryList - 查询预警消息列表（库存）

**路径**: `/basicOpen/settings/warningMessage/inventoryList`
**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| start_date | 是 | string | 开始日期【提醒时间】，间隔不超过90天，Y-m-d |
| end_date | 是 | string | 结束日期，Y-m-d |
| show_status | 是 | int | 0=待处理，1=全部 |
| model_id_list | 否 | array | 预警模型：4=本地库存，5=亚马逊库存，22=本地库龄，23=亚马逊库龄 |
| product_type_list | 否 | array | 2=MSKU，3=SKU+仓库+店铺+FNSKU |
| offset | 否 | int | 分页偏移量 |
| length | 否 | int | 分页长度，默认50，上限200 |

**关键返回字段**: message_id, model_id, model_name, product_type_str, monitor_type_str, notify_time, receiver, handle_status, read_status, monitor_time

---
