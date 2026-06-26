# 领星客服接口参考

所有接口均为 POST 请求（除标注外），域名：`https://openapi.lingxing.com`

---

## FeedbackList - 查询 4-5 星 Feedback 列表

**路径**: `/erp/sc/cs/feedback/list`
**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sid | 是 | int | 店铺ID |
| start_date | 是 | string | 开始日期，格式：Y-m-d |
| end_date | 是 | string | 结束日期，格式：Y-m-d |
| offset | 是 | int | 分页偏移量，默认0 |
| length | 是 | int | 分页长度，默认20 |

**关键返回字段**: sid, seller_name, country, star, amazon_order_id, feedback_date, feedback_content, status(0待处理/1处理中/2已完成), productList[asin/seller_sku/title], total

---

## FeedbackListMws - 查询 1-3 星 Feedback 列表

**路径**: `/erp/sc/cs/feedback/listMws`
**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sid | 是 | int | 店铺ID |
| start_date | 是 | string | 开始日期，格式：Y-m-d |
| end_date | 是 | string | 结束日期，格式：Y-m-d |
| offset | 是 | int | 分页偏移量，默认0 |
| length | 是 | int | 分页长度，默认20 |

**关键返回字段**: 同 FeedbackList（低星评价）

---

## CustomerList - 查询客户列表（旧）

**路径**: `/bd/crm/open/api/customer/list`
**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| time_search_type | 是 | int | 1=首次购买时间，2=最近购买时间 |
| start_date | 是 | string | 开始时间 |
| end_date | 是 | string | 结束时间 |
| sids | 否 | string | 店铺ID，逗号分隔 |
| offset | 否 | int | 页码，默认1 |
| length | 否 | int | 每页条数，默认100 |

**关键返回字段**: buyer_email, buyer_name, sid, country, order_items, volume, amount, refund_rate, return_rate, first_purchase_date, last_purchase_date, group

---

## AfterSalesWorkOrderList - 查询售后工单列表

**路径**: `/pb/mp/returns/workOrder/list`
**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| date_type | 是 | string | create_time=创建时间，complete_time=完成时间 |
| start_time | 是 | string | 开始时间，格式：Y-m-d H:i:s |
| end_time | 是 | string | 结束时间，格式：Y-m-d H:i:s |
| offset | 是 | int | 分页偏移量 |
| length | 是 | int | 分页长度，上限500 |

**关键返回字段**: 工单列表（售后工单详情）

---

## PerformanceNoticeList - 查询业绩通知列表

**路径**: `/basicOpen/customerService/performanceNotice/list`
**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sid | 是 | int | 店铺ID |
| status | 否 | int | 0无/1待处理/2已处理/3无需处理 |
| startDate | 否 | string | 开始时间，YYYY-MM-DD |
| endDate | 否 | string | 结束时间，YYYY-MM-DD |
| searchField | 否 | string | subject=邮件主题，content=邮件内容 |
| searchValue | 否 | string | 搜索值 |
| isRead | 否 | int | -1=全部，0=未读，1=已读 |
| offset | 否 | int | 偏移量 |
| length | 否 | int | 分页长度 |

**关键返回字段**: 业绩通知邮件列表

---

## PerformanceNoticeDetail - 查询店铺绩效详情

**路径**: `/basicOpen/customerService/storeTarget/detail`
**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| pullDate | 是 | string | 报表更新日期，yyyy-MM-dd |
| sid | 是 | int | 店铺ID |

**关键返回字段**: 店铺当日绩效指标详情

---

## mailDetail - 查询邮件详情

**路径**: `/erp/sc/data/mail/detail`
**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| webmail_uuid | 是 | string | 邮件唯一标识 |

**关键返回字段**: webmail_uuid, subject, from_name, from_address, to_address_all, date, cc, bcc, text_html, text_plain, attachments[name/size], type(0=QA/1=买家邮件/2=亚马逊邮件/3=站外邮件)

---

## mailLists - 查询邮件列表

**路径**: `/erp/sc/data/mail/lists`
**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| flag | 是 | string | sent=发件，receive=收件 |
| email | 是 | string | 店铺绑定邮箱 |
| start_date | 是 | string | 开始日期，yyyy-mm-dd |
| end_date | 是 | string | 结束日期，yyyy-mm-dd |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 分页长度，默认20 |

**关键返回字段**: webmail_uuid, subject, from_name, from_address, date, type, total

---

## review - 查询评价管理 Review

**路径**: `/erp/sc/v2/data/mws/reviews`
**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sid | 是 | int | 店铺ID |
| start_date | 是 | string | 开始时间，Y-m-d |
| end_date | 是 | string | 结束时间，Y-m-d |
| offset | 是 | int | 分页偏移量，默认0 |
| length | 是 | int | 分页长度 |
| date_field | 否 | string | review_date=评价时间（默认），create_time=创建时间 |

**关键返回字段**: asin, seller_sku, star, title, review_content, review_date, reviewer_name, status, remark, total

---

## reviewDetail - 查询评价统计 Review 每日新增数

**路径**: `/erp/sc/cs/reviewReport/detail`
**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| mid | 是 | int | 国家ID |
| asin | 是 | string | ASIN |
| start_date | 是 | string | 开始时间（间隔不超过1年） |
| end_date | 是 | string | 结束时间 |

**关键返回字段**: 每日 Review 新增数统计

---

## reviewLists - 查询评价统计 Review 列表（GET）

**路径**: `/erp/sc/v2/cs/reviewReport/lists`
**方法**: GET
**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| start_date | 是 | string | 开始时间，Y-m-d（间隔不超过1年） |
| end_date | 是 | string | 结束时间，Y-m-d |
| sid | 否 | int | 店铺ID |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 分页长度，默认20 |

**关键返回字段**: asin, sid, total_reviews, five_star, four_star, three_star, two_star, one_star, total

---

## reviewV2 - 查询评论管理 Review（新）

**路径**: `/basicOpen/openapi/service/v3/data/mws/reviews`
**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| date_field | 是 | string | review_time/create_time/last_update_time |
| start_date | 是 | string | 开始时间，Y-m-d |
| end_date | 是 | string | 结束时间，Y-m-d |
| sids | 否 | string | 店铺ID，逗号分隔 |
| mids | 否 | string | 站点ID，逗号分隔 |
| search_field | 否 | string | asin/parent_asin/remark/amazon_order_id |
| search_value | 否 | string | 搜索值 |
| offset | 否 | int | 分页偏移量 |
| length | 否 | int | 分页长度 |

**关键返回字段**: asin, parent_asin, star, title, review_content, review_time, reviewer_name, seller_sku, status, remark

---

## feedbackDetail - 查询评价统计 Feedback 每日新增数

**路径**: `/erp/sc/cs/feedbackReport/detail`
**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sid | 是 | int | 店铺ID |
| start_date | 是 | string | 开始时间（间隔不超过1年） |
| end_date | 是 | string | 结束时间 |

**关键返回字段**: 每日 Feedback 新增数统计

---

## feedbackLists - 查询评价统计 Feedback 列表

**路径**: `/erp/sc/cs/feedbackReport/lists`
**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| start_date | 是 | string | 开始时间，Y-m-d（间隔不超过1年） |
| end_date | 是 | string | 结束时间，Y-m-d |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 分页长度，默认20 |

**关键返回字段**: sid, seller_name, total_feedback, five_star, four_star, three_star, two_star, one_star

---

## customerServiceCrmcustomerIndex - 查询客户列表（新）

**路径**: `/basicOpen/customerService/crm/customer/index`
**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| date_field | 否 | string | 1=首次购买时间，2=最近购买时间 |
| start_date | 否 | string | 开始时间，Y-m-d |
| end_date | 否 | string | 结束时间，Y-m-d |
| sids | 否 | string | 店铺ID |
| search_field | 否 | string | buyer_email/buyer_name |
| search_value | 否 | string | 搜索值 |
| currency_type | 否 | int | 0=原币种，1=CNY，2=USD |
| offset | 否 | int | 偏移量，默认0 |
| length | 否 | int | 分页长度，默认20，上限200 |

**关键返回字段**: buyer_email, buyer_name, sid, country, order_items, volume, amount, per_customer_transaction, refund_rate, return_rate, feedback_number, first_purchase_date, last_purchase_date, group

---

## customerServiceRmaManageList - 查询 RMA 管理

**路径**: `/basicOpen/customerService/rmaManage/list`
**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sid | 是 | array | 店铺ID数组 |
| searchTimeFiled | 是 | string | createTime=创建时间，operationTime=操作时间 |
| startTime | 是 | string | 开始日期，Y-m-d |
| endTime | 是 | string | 结束日期，Y-m-d |
| searchValue | 是 | array | 搜索值（msku/asin支持多个） |
| searchField | 是 | string | msku/asin/sku |
| pageNum | 是 | int | 页码 |
| pageSize | 是 | int | 每页数量 |

**关键返回字段**: records[rmaNo, amazonOrderId, asin, sellerSku, itemName, sellerName, country, afterSaleTypeName, processWayName, channelSourceName, createTime, operationTime], total, pageCount

---

## storePerformanceList - 查询店铺绩效列表

**路径**: `/basicOpen/customerService/storeTarget/list`
**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| search_field_time | 否 | string | pull_date=报表获取时间，update_date=更新时间 |
| search_time | 否 | string | 搜索时间，Y-m-d |
| sids | 否 | string | 店铺ID，逗号分隔 |
| anomaly_indicator | 否 | array | 异常指标筛选（commodity_policy_compliance/on_time_delivery/valid_tracking/pre_fulfillment_cancellation/late_shipment/invoice_defect/fba_order_with_defect/order_with_defect） |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 分页长度，默认20，上限200 |

**关键返回字段**: sid, pull_date, order_with_defect, late_shipment, pre_fulfillment_cancellation, valid_tracking, on_time_delivery, fba_order_with_defect, invoice_defect, ahr_score, ahr_status

---

## voiceOfBuyerList - 查询买家之声列表

**路径**: `/basicOpen/customerService/voiceOfBuyer/list`
**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sids | 否 | array | 店铺ID |
| fulfillment_channel | 否 | string | FBA/MFN |
| pxc_health | 否 | array | -1=反馈不足，0=极差，1=不合格，2=一般，3=良好，4=极好 |
| search_field | 否 | string | asin/msku/sku |
| search_value | 否 | array | 搜索值 |
| return_badge | 否 | array | Yes/No/At_Risk |
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 分页长度，默认20，上限200 |

**关键返回字段**: asin, msku, fnsku, title, fulfillment_channel, ncx_rate, ncx_count, order_count, most_common_return_reason_bucket, pcx_health_text, returnBadge, returnRate, event_date

---
