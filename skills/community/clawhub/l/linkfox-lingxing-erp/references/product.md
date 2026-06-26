# 领星产品接口参考

所有接口均为 POST 请求（除标注 GET 外），域名：`https://openapi.lingxing.com`

---

## ProductLists - 查询本地产品列表

**路径**: `/erp/sc/routing/data/local_inventory/productList`
**方法**: POST

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 分页长度，默认/上限1000 |
| update_time_start | 否 | int | 更新时间开始（时间戳秒，左闭右开） |
| update_time_end | 否 | int | 更新时间结束（时间戳秒） |
| create_time_start | 否 | int | 创建时间开始（时间戳秒） |
| create_time_end | 否 | int | 创建时间结束（时间戳秒） |
| sku_list | 否 | array | 本地产品SKU列表 |
| sku_identifier_list | 否 | array | SKU识别码列表 |

**关键返回字段**: id, sku, sku_identifier, product_name, pic_url, ps_id, spu, bid, cid, brand_name, category_name, status（0停售/1在售/2开发中/3清仓）, is_combo, cg_price, open_status, global_tags, create_time, update_time

---

## ProductDetails - 查询本地产品详情

**路径**: `/erp/sc/routing/data/local_inventory/productInfo`
**方法**: POST

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| id | 否 | int | 产品id（三选一必填） |
| sku | 否 | string | 产品SKU（三选一必填） |
| sku_identifier | 否 | string | SKU识别码（三选一必填） |

**关键返回字段**: id, sku, product_name, pic_url, status, cid, bid, brand_name, category_name, cg_price, cg_delivery, special_attr, attachment_id, supplier_quote, combo_product_list, product_logistics_relation, declaration, clearance, aux_relation_list

---

## Brand - 查询产品品牌列表

**路径**: `/erp/sc/data/local_inventory/brand`
**方法**: POST

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 分页长度，默认/上限1000 |

**关键返回字段**: bid, title（品牌名称）, brand_code

---

## Category - 查询产品分类列表

**路径**: `/erp/sc/routing/data/local_inventory/category`
**方法**: POST

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 分页长度，默认/上限1000 |
| ids | 否 | array | 分类ID列表 |

**关键返回字段**: cid, title（分类名称）, parent_cid, category_code

---

## UpcList - 获取UPC编码列表

**路径**: `/listing/publish/api/upc/upcList`
**方法**: POST

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 分页长度，默认20 |

**关键返回字段**: data>>total, data>>list>>id, data>>list>>commodity_code, data>>list>>code_type, data>>list>>is_used（0未使用/1已使用）, data>>list>>use_time, data>>list>>gmt_create

---

## GetProductTag - 查询产品标签

**路径**: `/label/operation/v1/label/product/list`
**方法**: GET（无请求参数）

**关键返回字段**: data>>list>>label_id, data>>list>>label_name, data>>list>>gmt_created, data>>total

---

## GetPagingLogLists - 查询产品操作日志

**路径**: `/basicOpen/product/getPagingLogLists`
**方法**: POST

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| businessId | 是 | long | 产品id（对应ProductLists的data>>id） |
| startTime | 是 | string | 开始时间 |
| endTime | 是 | string | 结束时间 |
| page | 否 | int | 页码，默认1 |
| size | 否 | int | 每页大小，默认20 |

**关键返回字段**: data>>action, data>>datetime, data>>detail, data>>userId, data>>userName

---

## attributeList - 查询产品属性列表

**路径**: `/erp/sc/routing/storage/attribute/attributeList`
**方法**: POST

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| offset | 是 | int | 分页偏移量 |
| length | 是 | int | 分页长度，上限200 |

**关键返回字段**: data>>total, data>>list>>pa_id, data>>list>>attr_name, data>>list>>create_time, data>>list>>item_list>>pai_id, data>>list>>item_list>>attr_value

---

## batchGetProductInfo - 批量查询本地产品详情

**路径**: `/erp/sc/routing/data/local_inventory/batchGetProductInfo`
**方法**: POST

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| productIds | 否 | array | 产品id列表，上限100（三选一必填） |
| skus | 否 | array | 产品SKU列表，上限100（三选一必填） |
| sku_identifiers | 否 | array | SKU识别码列表，上限100（三选一必填） |

**关键返回字段**: 与 ProductDetails 相同，返回数组

---

## bundledProductList - 查询捆绑产品关系列表

**路径**: `/erp/sc/routing/data/local_inventory/bundledProductList`
**方法**: POST

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 分页长度，默认/上限1000 |

**关键返回字段**: id, sku, product_name, cg_price, status_text, bundled_products>>productId, bundled_products>>sku, bundled_products>>bundledQty, bundled_products>>cost_ratio

---

## getTransparencyProductList - 查询透明计划商品列表

**路径**: `/basicOpen/product/getTransparencyProductList`
**方法**: POST

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 分页长度，默认20，最大200 |
| isRelateMsku | 否 | int | 是否关联MSKU：1是/2否 |
| productStatus | 否 | string | 产品状态：all/Enrolled/In OPR/Protected/NoStatus |
| searchField | 否 | string | 搜索字段名（如asin） |
| searchValue | 否 | string | 搜索值 |

**关键返回字段**: data>>pageList>>id, asin, sellerSku, brandName, productStatus, gtin, labelType, tcodeTotal, tcodeNotUsedTotal, accountName, picUrl, data>>total

---

## productAuxList - 查询产品辅料列表

**路径**: `/erp/sc/routing/data/local_inventory/productAuxList`
**方法**: POST

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 分页长度，默认/上限1000 |

**关键返回字段**: id, sku, product_name, cg_price, cg_product_length/width/height/net_weight, purchase_supplier_quote, aux_relation_product>>pid/sku/quantity

---

## spuInfo - 查询多属性产品详情

**路径**: `/erp/sc/routing/storage/spu/info`
**方法**: POST

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| ps_id | 否 | int | SPU唯一id（与spu二选一必填） |
| spu | 否 | string | SPU编码（与ps_id二选一必填） |

**关键返回字段**: ps_id, spu, spu_name, status, cid, bid, brand_name, category_name, purchase_info, sku_list>>sku/product_name/attribute, aux_relation_list, logistics, attribute_skc_list

---

## spuList - 查询多属性产品列表

**路径**: `/erp/sc/routing/storage/spu/spuList`
**方法**: POST

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| offset | 否 | int | 分页偏移量，默认0 |
| length | 否 | int | 分页长度，默认1000，上限1000 |
| update_time_start | 否 | int | 更新时间开始（时间戳秒） |
| update_time_end | 否 | int | 更新时间结束（时间戳秒） |
| spu_list | 否 | array | SPU列表 |

**关键返回字段**: ps_id, spu, spu_name, status, cid, bid, brand_name, category_name, sku_count, create_time, update_time

---
