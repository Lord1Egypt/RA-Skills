# 领星物流接口参考

所有接口均为 POST 请求，域名：`https://openapi.lingxing.com`

---

## ChannelList - 查询物流渠道列表

**路径**: `/erp/sc/data/local_inventory/channelList`

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| offset | 是 | int | 分页偏移量 |
| length | 是 | int | 分页长度 |

**关键返回字段**: id, channel_name, method_id, method_name, billing_type, volume_calc_param, zip_code, valid_period

---

## QueryHeadLogisticsProvider - 查询头程物流商列表

**路径**: `/basicOpen/logistics/headLogisticsProvider/query/list`

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| search | 是 | object | 搜索条件对象 |
| search>>page | 是 | int | 页码 |
| search>>length | 是 | int | 每页大小 |
| search>>enabled | 否 | int | 是否启用 |
| search>>isAuth | 否 | int | 是否已授权 |
| search>>payMethod | 否 | int | 付款方式 |
| search>>searchField | 否 | string | 搜索字段名 |
| search>>searchValue | 否 | string | 搜索值 |

**关键返回字段**: data>>total, data>>providers>>providerId, data>>providers>>name, data>>providers>>code, data>>providers>>enabled, data>>providers>>logisticsType, data>>providers>>isAuth, data>>providers>>supplierCode, data>>providers>>supplierName

---

## transportMethodList - 查询运输方式列表

**路径**: `/basicOpen/businessConfig/transportMethod/list`
**参数**: 无（直接调用即可）

**关键返回字段**: data>>method_id, data>>code, data>>name, data>>is_system, data>>enabled, data>>remark, data>>creator_id, data>>creator_name

---
