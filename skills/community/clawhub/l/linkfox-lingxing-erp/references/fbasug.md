# 领星FBA补货建议接口参考

所有接口均为 POST 请求，域名：`https://openapi.lingxing.com`

---

## GetSummaryList - 查询补货建议汇总列表

**路径**: `/erp/sc/routing/restocking/analysis/getSummaryList`

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| data_type | 是 | int | 数据维度类型 |
| sid_list | 否 | array | 店铺id列表 |
| asin_list | 否 | array | ASIN列表 |
| msku_list | 否 | array | MSKU列表 |
| mode | 否 | int | 模式 |
| listing_date_range | 否 | array | 上架日期范围 |
| offset | 否 | int | 分页偏移量 |
| length | 否 | int | 分页长度 |

**关键返回字段**: data>>basic_info>>data_type, data>>basic_info>>node_type, data>>basic_info>>sid, data>>basic_info>>asin, data>>basic_info>>msku_fnsku_list

---

## ConfigASIN - 查询ASIN补货配置

**路径**: `/erp/sc/routing/fbaSug/asin/getConfig`

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sid | 是 | int | 店铺id |
| asin | 是 | string | ASIN |

**关键返回字段**: data>>info>>days_total, data>>info>>days_total2, data>>info>>days_plan, data>>info>>days_purchase, data>>info>>days_qc

---

## ConfigMSKU - 查询MSKU补货配置

**路径**: `/erp/sc/routing/fbaSug/msku/getConfig`

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sid | 是 | string | 店铺id |
| msku | 是 | string | MSKU |

**关键返回字段**: data>>info>>days_total, data>>info>>days_total2, data>>info>>days_plan, data>>info>>days_purchase, data>>info>>days_qc

---

## DailySalesInfoFeatureASIN - 查询ASIN日销售特征数据

**路径**: `/erp/sc/routing/fbaSug/asin/getDailySalesInfoFeature`

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sid | 是 | int | 店铺id |
| asin | 是 | string | ASIN |
| sug_type | 是 | int | 建议类型 |
| mode | 否 | int | 模式 |

**关键返回字段**: data>>list（日期销量列表）, data>>sug_date_line>>date, data>>sug_date_line>>desc, data>>sug_date_line>>title

---

## DailySalesInfoFeatureMSKU - 查询MSKU日销售特征数据

**路径**: `/erp/sc/routing/fbaSug/msku/getDailySalesInfoFeature`

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sid | 是 | int | 店铺id |
| msku | 是 | string | MSKU |
| sug_type | 是 | int | 建议类型 |
| mode | 否 | int | 模式 |

**关键返回字段**: data>>list（日期销量列表）, data>>sug_date_line>>date, data>>sug_date_line>>desc, data>>sug_date_line>>title

---

## InfoASIN - 查询ASIN补货建议信息

**路径**: `/erp/sc/routing/fbaSug/asin/getInfo`

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sid | 是 | int | 店铺id |
| asin | 是 | string | ASIN |
| mode | 否 | int | 模式 |

**关键返回字段**: data>>sid, data>>asin, data>>mode, data>>quantity_fba_valid, data>>msku_list>>msku

---

## InfoMSKU - 查询MSKU补货建议信息

**路径**: `/erp/sc/routing/fbaSug/msku/getInfo`

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sid | 是 | int | 店铺id |
| msku | 是 | string | MSKU |
| mode | 否 | int | 模式 |

**关键返回字段**: data>>sid, data>>msku, data>>mode, data>>quantity_sug_replenishment, data>>quantity_sug_send, data>>quantity_fba_valid

---

## SourceListASIN - 查询ASIN补货来源列表

**路径**: `/erp/sc/routing/fbaSug/asin/getSourceList`

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sid | 是 | int | 店铺id |
| asin | 是 | string | ASIN |
| type | 否 | string | 补货来源类型 |
| mode | 否 | string | 模式 |

**关键返回字段**: data>>mode, data>>source_list>>quantity, data>>source_list>>type, data>>source_list>>amazon_sale_date, data>>source_list>>remark

---

## SourceListMSKU - 查询MSKU补货来源列表

**路径**: `/erp/sc/routing/fbaSug/msku/getSourceList`

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| sid | 是 | int | 店铺id |
| msku | 是 | string | MSKU |
| type | 否 | string | 补货来源类型 |
| mode | 否 | string | 模式 |

**关键返回字段**: data>>mode, data>>source_list>>quantity, data>>source_list>>type, data>>source_list>>amazon_sale_date, data>>source_list>>remark

---
