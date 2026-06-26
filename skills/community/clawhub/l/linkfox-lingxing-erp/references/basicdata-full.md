# 领星基础数据接口参考

所有接口均为 POST 请求（除标注 GET 外），域名：`https://openapi.lingxing.com`

---

## AccoutLists - 查询ERP账户列表

**路径**: `/erp/sc/data/account/lists`
**方法**: GET（无请求参数）

**关键返回字段**: uid, username, realname, mobile, email, status（0禁用/1正常）, role, seller（店铺权限）, is_master

---

## AllMarketplace - 查询亚马逊市场列表

**路径**: `/erp/sc/data/seller/allMarketplace`
**方法**: GET（无请求参数）

**关键返回字段**: mid（领星站点ID）, region, country, code（国家代码如US/UK）, marketplace_id（亚马逊市场ID）

---

## AttachmentDownload - 附件下载

**路径**: `/erp/sc/routing/common/file/download`
**方法**: POST

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| file_id | 是 | int | 附件id（来自对应功能接口返回的附件id） |

**关键返回字段**: file_name, mime_type, content（base64编码的文件内容）

---

## ConceptSellerLists - 查询概念店铺列表

**路径**: `/erp/sc/data/seller/conceptLists`
**方法**: GET（无请求参数）

**关键返回字段**: id（概念店铺ID）, mid（概念市场ID）, name, seller_id, seller_account_name, seller_account_id, region, country, status（1启用/2禁用）

---

## Currency - 查询货币月汇率

**路径**: `/erp/sc/routing/finance/currency/currencyMonth`
**方法**: POST

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| date | 是 | string | 汇率月份，格式 YYYY-MM |

**关键返回字段**: date, code（币种代码如CNY/USD）, icon, name, rate_org（官方汇率）, my_rate（自定义汇率）

---

## CustomAttachmentDownload - 自定义附件下载

**路径**: `/erp/sc/routing/customized/file/download`
**方法**: POST

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| file_id | 是 | string | 附件文件id（来自订单详情接口） |

**关键返回字段**: file_name, mime_type, content（base64编码文件内容）

---

## StateList - 查询省份列表

**路径**: `/basicOpen/multiplatform/profit/report/stateList`
**方法**: POST

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| countryCode | 是 | string | 国家编码二字码，如 US/AF/DE |

**关键返回字段**: data>>states>>countryCode, data>>states>>stateOrProvinceName, data>>states>>code（州/省编码）

---

## WorldStateLists - 查询亚马逊国家地区列表

**路径**: `/erp/sc/data/worldState/lists`
**方法**: POST

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| country_code | 是 | string | 国家code，来自 AllMarketplace 接口的 code 字段 |

**关键返回字段**: country_code, state_or_province_name, code（地区code）

---
