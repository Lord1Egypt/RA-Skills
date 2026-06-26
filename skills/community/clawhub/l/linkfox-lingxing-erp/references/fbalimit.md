# 领星FBA库容限制接口参考

所有接口均为 POST 请求，域名：`https://openapi.lingxing.com`

---

## GetIpiInfo - 查询IPI绩效指标信息

**路径**: `/erp/sc/routing/fbaLimit/restock/getIpiInfo`

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| offset | 否 | int | 分页偏移量 |
| length | 否 | int | 分页长度 |
| sids | 否 | string | 店铺id，多个以英文逗号分隔 |
| seller_ids | 否 | string | 亚马逊卖家id，多个以英文逗号分隔 |
| mids | 否 | string | 站点id，多个以英文逗号分隔 |

**关键返回字段**: data>>seller_id, data>>seller_account_name, data>>seller_name, data>>marketplace, data>>update_date, data>>vol_unit_text, data>>ipi, data>>excess_inventory_rate

---

## replenishmentRestrictionList - 查询补货限制列表

**路径**: `/basicOpen/openapi/replenishmentRestriction/page/list`

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| storage_type | 是 | string | 仓储类型 |
| offset | 否 | int | 分页偏移量 |
| length | 否 | int | 分页长度 |
| sids | 否 | string | 店铺id，多个以英文逗号分隔 |

**关键返回字段**: data>>data>>month, data>>list>>sid, data>>list>>vol_unit_type, data>>list>>ipi, data>>list>>update_type, data>>list>>excess_inventory_rate, data>>list>>excess_inventory_color, data>>list>>sell_through_rate

---
