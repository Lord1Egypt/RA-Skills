# 快手生活服务 OpenAPI 完整参考

本文档包含快手生活服务 openAPI 的所有接口详细说明。

## API 基础信息

- **基础地址**: `https://lbs-open.kuaishou.com`
- **认证方式**: 所有接口需在请求头中携带 `access-token`
- **内容类型**: `application/json`
- **文档链接**: https://docs.corp.kuaishou.com/d/home/fcABGZ7JGTqHnqn4WcaH8DkUp

## 接口列表

### 1. 查询商家某个子账号信息

查询指定子账号的详细信息。

**接口地址**: `POST /goodlife/v1/merchant/QueryStaffUserInfo`

**请求示例**:
```bash
curl --location 'https://lbs-open.kuaishou.com/goodlife/v1/merchant/QueryStaffUserInfo' \
--header 'Content-Type: application/json' \
--header 'access-token: YOUR_ACCESS_TOKEN' \
--data '{
    "id": 3559238
}'
```

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| id | integer | 是 | 子账号ID |

---

### 2. 查询商家待办事项列表

获取商家的待办事项列表。

**接口地址**: `GET /goodlife/v1/workbench/todo_list`

**请求示例**:
```bash
curl --location --request GET 'https://lbs-open.kuaishou.com/goodlife/v1/workbench/todo_list' \
--header 'Content-Type: application/json' \
--header 'access-token: YOUR_ACCESS_TOKEN' \
--data '{
    "kwaiId": "",
    "staffKsUserId": "",
    "remark": "",
    "mobile": "",
    "status": 1,
    "dataResourceId": [],
    "dataType": 0,
    "outPoiId": "",
    "currentPage": 1,
    "pageSize": 10
}'
```

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| kwaiId | string | 否 | 快手ID |
| staffKsUserId | string | 否 | 员工快手用户ID |
| remark | string | 否 | 备注 |
| mobile | string | 否 | 手机号 |
| status | integer | 否 | 状态(1:待处理) |
| dataResourceId | array | 否 | 数据资源ID列表 |
| dataType | integer | 否 | 数据类型 |
| outPoiId | string | 否 | 外部门店ID |
| currentPage | integer | 否 | 当前页码,默认1 |
| pageSize | integer | 否 | 每页条数,默认10 |

---

### 3. 查询商家子账号列表

获取商家的所有子账号列表。

**接口地址**: `POST /goodlife/v1/merchant/subAccounts`

**请求示例**:
```bash
curl --location 'https://lbs-open.kuaishou.com/goodlife/v1/merchant/subAccounts' \
--header 'Content-Type: application/json' \
--header 'access-token: YOUR_ACCESS_TOKEN' \
--data '{
    "kwai_id": "",
    "staff_ks_user_id": "1280915625",
    "remark": "",
    "role_id": "",
    "mobile": "",
    "status": "",
    "data_resource_id": [],
    "data_type": 0,
    "out_poi_id": "",
    "current_page": 1,
    "page_size": 10
}'
```

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| kwai_id | string | 否 | 快手ID |
| staff_ks_user_id | string | 否 | 员工快手用户ID |
| remark | string | 否 | 备注 |
| role_id | string | 否 | 角色ID |
| mobile | string | 否 | 手机号 |
| status | string | 否 | 状态 |
| data_resource_id | array | 否 | 数据资源ID列表 |
| data_type | integer | 否 | 数据类型 |
| out_poi_id | string | 否 | 外部门店ID |
| current_page | integer | 否 | 当前页码,默认1 |
| page_size | integer | 否 | 每页条数,默认10 |

---

### 4. 查询商家经营退款数据汇总

查询商家的退款数据汇总信息。

**接口地址**: `POST /goodlife/v1/metric/queryMetric`

**请求示例**:
```bash
curl --location 'https://lbs-open.kuaishou.com/goodlife/v1/metric/queryMetric' \
--header 'Content-Type: application/json' \
--header 'access-token: YOUR_ACCESS_TOKEN' \
--data '{
    "metric_param": {
        "metric_key": "getLocallifeMerchantRefundInfo"
    }
}'
```

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| metric_param.metric_key | string | 是 | 指标键值,固定为 `getLocallifeMerchantRefundInfo` |

---

### 5. 查询商家经营职人数据汇总

查询商家的职人经营数据汇总。

**接口地址**: `POST /goodlife/v1/metric/queryMetric`

**请求示例**:
```bash
curl --location 'https://lbs-open.kuaishou.com/goodlife/v1/metric/queryMetric' \
--header 'Content-Type: application/json' \
--header 'access-token: YOUR_ACCESS_TOKEN' \
--data '{
    "metric_param": {
        "metric_key": "merchantArtisanDataHomePageOverview",
        "param": [
            {
                "param_name": "beginDate",
                "param_value": ["20260314", "20260307"]
            },
            {
                "param_name": "endDate",
                "param_value": ["20260320", "20260313"]
            }
        ]
    }
}'
```

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| metric_param.metric_key | string | 是 | 指标键值,固定为 `merchantArtisanDataHomePageOverview` |
| metric_param.param | array | 否 | 参数列表 |
| param.param_name | string | 是 | 参数名(beginDate/endDate) |
| param.param_value | array | 是 | 参数值数组,日期格式为YYYYMMDD |

---

### 6. 查询某个职人的经营数据汇总

查询单个职人的经营数据汇总。

**接口地址**: `POST /goodlife/v1/metric/queryMetric`

**请求示例**:
```bash
curl --location 'https://lbs-open.kuaishou.com/goodlife/v1/metric/queryMetric' \
--header 'Content-Type: application/json' \
--header 'access-token: YOUR_ACCESS_TOKEN' \
--data '{
    "metric_param": {
        "metric_key": "merchantArtisanDataHomePageOverview",
        "param": [
            {
                "param_name": "beginDate",
                "param_value": ["20260314", "20260307"]
            },
            {
                "param_name": "endDate",
                "param_value": ["20260320", "20260313"]
            },
            {
                "param_name": "artisanId",
                "param_value": ["1468396855"]
            }
        ]
    }
}'
```

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| metric_param.metric_key | string | 是 | 指标键值,固定为 `merchantArtisanDataHomePageOverview` |
| metric_param.param | array | 是 | 参数列表 |
| param.param_name | string | 是 | 参数名(beginDate/endDate/artisanId) |
| param.param_value | array | 是 | 参数值数组 |

---

### 7. 查询商家职人自动激励状态信息

查询商家职人的自动激励状态。

**接口地址**: `POST /goodlife/v1/artisan/QueryAutoCommissionInfo`

**请求示例**:
```bash
curl --location 'https://lbs-open.kuaishou.com/goodlife/v1/artisan/QueryAutoCommissionInfo' \
--header 'Content-Type: application/json' \
--header 'access-token: YOUR_ACCESS_TOKEN' \
--data '{}'
```

---

### 8. 查询职人列表

查询商家的职人列表。

**接口地址**: `POST /goodlife/v1/merchant/artisan_list`

**请求示例**:
```bash
curl --location 'https://lbs-open.kuaishou.com/goodlife/v1/merchant/artisan_list' \
--header 'Content-Type: application/json' \
--header 'access-token: YOUR_ACCESS_TOKEN' \
--data '{
    "uid": [],
    "merchant_base_page_request": {
        "current_page": 1,
        "page_size": 10
    },
    "city_code": ""
}'
```

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| uid | array | 否 | 职人ID列表 |
| merchant_base_page_request.current_page | integer | 否 | 当前页码,默认1 |
| merchant_base_page_request.page_size | integer | 否 | 每页条数,默认10 |
| city_code | string | 否 | 城市代码 |

---

***职人状态码status含义映射***
1：签约成功
2：解绑中
3：已解绑
1001：待商家确认
1002：职人已撤销
1003：商家拒绝
2003：职人拒绝
2002：商家已撤销
2001：待职人确认

### 9. 商家交易实时汇总信息

查询商家的交易实时汇总数据。

**接口地址**: `POST /goodlife/v1/merchant/QueryMerchantRealTimeMetric`

**请求示例**:
```bash
curl --location 'https://lbs-open.kuaishou.com/goodlife/v1/merchant/QueryMerchantRealTimeMetric' \
--header 'Content-Type: application/json' \
--header 'access-token: YOUR_ACCESS_TOKEN' \
--data '{
    "distribute_type": "ALL",
    "module_key": "dataHomeTradeInfo"
}'
```

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| distribute_type | string | 是 | 分发类型(ALL:全部) |
| module_key | string | 是 | 模块键值,固定为 `dataHomeTradeInfo` |

---

### 10. 查询某个门店的用户评价评分

查询指定门店的用户评价评分信息。

**接口地址**: `GET /goodlife/rest/merchant/apicenter/pc/comment/poiRatingScore`

**请求示例**:
```bash
curl --location 'https://lbs-open.kuaishou.com/goodlife/rest/merchant/apicenter/pc/comment/poiRatingScore?out_poi_id=3002950207824404841' \
--header 'access-token: YOUR_ACCESS_TOKEN'
```

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| out_poi_id | string | 是 | 外部门店ID |

---

### 11. 扫码物料

查询扫码物料列表。

**接口地址**: `POST /goodlife/rest/merchant/apicenter/poi/qrCode/list`

**请求示例**:
```bash
curl --location 'https://lbs-open.kuaishou.com/goodlife/rest/merchant/apicenter/poi/qrCode/list' \
--header 'Content-Type: application/json' \
--header 'access-token: YOUR_ACCESS_TOKEN' \
--data '{
    "page_req": {
        "current_page": 1,
        "page_size": 10
    },
    "poi_ids": []
}'
```

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| page_req.current_page | integer | 否 | 当前页码,默认1 |
| page_req.page_size | integer | 否 | 每页条数,默认10 |
| poi_ids | array | 否 | 门店ID列表 |

---

### 12. 查询评价分析

查询评价分析数据。

**接口地址**: `POST /goodlife/rest/merchant/apicenter/metric/queryMetrics`

**请求示例**:
```bash
curl --location --request POST 'https://lbs-open.kuaishou.com/goodlife/rest/merchant/apicenter/metric/queryMetrics' \
--header 'Content-Type: application/json' \
--header 'access-token: YOUR_ACCESS_TOKEN' \
--data ''
```

---

### 13. 查询已授权 & 未授权的应用列表

查询商家的应用授权列表。

**接口地址**: `GET /goodlife/rest/merchant/apicenter/developer/auth/list`

**请求示例**:
```bash
curl --location 'https://lbs-open.kuaishou.com/goodlife/rest/merchant/apicenter/developer/auth/list' \
--header 'access-token: YOUR_ACCESS_TOKEN'
```

---

### 14. 查询商家商品基础激励的总体状态

查询商家商品基础激励的总体状态。

**接口地址**: `GET /goodlife/rest/merchant/apicenter/artisan/item/commission/page/query`

**请求示例**:
```bash
curl --location 'https://lbs-open.kuaishou.com/goodlife/rest/merchant/apicenter/artisan/item/commission/page/query?page=1&page_size=10&commission_status=10&item_id=&scene=itemBaseCommissionPage&access-token=YOUR_ACCESS_TOKEN'
```

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| page | integer | 否 | 当前页码,默认1 |
| page_size | integer | 否 | 每页条数,默认10 |
| commission_status | integer | 否 | 激励状态(10:激励中) |
| item_id | string | 否 | 商品ID |
| scene | string | 是 | 场景,固定为 `itemBaseCommissionPage` |
| access-token | string | 是 | 访问令牌 |

---

### 15. 查询某个门店下最新的某些条件的评论

查询门店的评论列表。

**接口地址**: `GET /goodlife/rest/merchant/apicenter/pc/comment/poiCommentList`

**请求示例**:
```bash
curl --location 'https://lbs-open.kuaishou.com/goodlife/rest/merchant/apicenter/pc/comment/poiCommentList?access-token=YOUR_ACCESS_TOKEN'
```

---

### 16. 查询职人的定向激励数据

查询职人的定向激励数据。

**接口地址**: `POST /goodlife/rest/merchant/apicenter/artisan/direct/commission/page/query`

**请求示例**:
```bash
curl --location 'https://lbs-open.kuaishou.com/goodlife/rest/merchant/apicenter/artisan/direct/commission/page/query' \
--header 'Content-Type: application/json' \
--header 'access-token: YOUR_ACCESS_TOKEN' \
--data '{
    "page": 1,
    "page_size": 10,
    "keyword": ""
}'
```

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| page | integer | 否 | 当前页码,默认1 |
| page_size | integer | 否 | 每页条数,默认10 |
| keyword | string | 否 | 关键词搜索 |

---

### 17. 查询官号

查询官号信息。

**接口地址**: `POST /goodlife/rest/merchant/apicenter/officialAccount/queryOfficialAccountCardInfo`

**请求示例**:
```bash
curl --location 'https://lbs-open.kuaishou.com/goodlife/rest/merchant/apicenter/officialAccount/queryOfficialAccountCardInfo' \
--header 'Content-Type: application/json' \
--header 'access-token: YOUR_ACCESS_TOKEN' \
--data '{}'
```

---

### 18. 查询门店认领的审核信息

查询门店认领的审核信息。

**接口地址**: `POST /goodlife/shopManage/poiMangeList`

**请求示例**:
```bash
curl --location 'https://lbs-open.kuaishou.com/goodlife/shopManage/poiMangeList' \
--header 'Content-Type: application/json' \
--header 'access-token: YOUR_ACCESS_TOKEN' \
--data '{
    "poiId": 3002401525209437461,
    "page": 1,
    "pageSize": 10
}'
```

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| poiId | integer | 是 | 门店ID |
| page | integer | 否 | 当前页码,默认1 |
| pageSize | integer | 否 | 每页条数,默认10 |

---

### 19. 查询商家所有的合同信息

查询商家的所有合同信息。

**接口地址**: `GET /goodlife/queryMerchantAllContract`

**请求示例**:
```bash
curl --location --request GET 'https://lbs-open.kuaishou.com/goodlife/queryMerchantAllContract' \
--header 'Content-Type: application/json' \
--header 'access-token: YOUR_ACCESS_TOKEN'
```

---

### 20. 查询商家的品牌资质列表

查询商家的品牌资质列表。

**接口地址**: `GET /goodlife/invest/queryBrandInfoList`

**请求示例**:
```bash
curl --location --request GET 'https://lbs-open.kuaishou.com/goodlife/invest/queryBrandInfoList' \
--header 'Content-Type: application/json' \
--header 'access-token: YOUR_ACCESS_TOKEN'
```

**响应参数参数**:
- validStatus: 0:生效中 1:未生效
- applyStatus: 1:审核中 2:审核成功 3:审核失败

---

### 21. 查询商家的区域列表

查询商家的区域列表。

**接口地址**: `POST /goodlife/merchantArea/queryList`

**请求示例**:
```bash
curl --location 'https://lbs-open.kuaishou.com/goodlife/merchantArea/queryList' \
--header 'Content-Type: application/json' \
--header 'access-token: YOUR_ACCESS_TOKEN'
```

---

### 22. 批量查询商品列表

批量查询商品列表信息。

**接口地址**: `POST /goodlife/v1/item/itemlist/batch/query`

**请求示例**:
```bash
curl --location 'https://lbs-open.kwailocallife.com/goodlife/v1/item/itemlist/batch/query' \
--header 'Content-Type: application/json;charset=UTF-8' \
--header 'access-token: YOUR_ACCESS_TOKEN' \
--data '{
    "cursor": 0,
    "size": 20,
    "product_id": [123456, 789012],
    "start_time": 1710000000,
    "end_time": 1710086400,
    "out_id": ["ext_id_001", "ext_id_002"]
}'
```

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| cursor | integer | 是 | 查询游标,默认0 |
| size | integer | 是 | 每页条数,默认20 |
| product_id | array | 否 | 商品ID列表 |
| start_time | integer | 否 | 开始时间戳 |
| end_time | integer | 否 | 结束时间戳 |
| out_id | array | 否 | 外部商品ID列表 |


---

### 23. 查询商品关联的门店信息

查询商品关联的门店信息。

**接口地址**: `GET /goodlife/v1/item/poi/query`

**请求示例**:
```bash
curl --location 'https://lbs-open.kwailocallife.com/goodlife/v1/item/poi/query?item_id=123456&page_num=1&page_size=10' \
--header 'Content-Type: application/json;charset=UTF-8' \
--header 'access-token: YOUR_ACCESS_TOKEN'
```

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| item_id | integer | 否 | 商品ID |
| page_num | integer | 否 | 页码,默认1 |
| page_size | integer | 否 | 每页条数,默认10 |

**参考文档**: https://open.kwailocallife.com/docs/api?apiName=goodlife.v1.item.poi.query&version=1&cid=%E5%95%86%E5%93%81API_1767&cnName=%E6%9F%A5%E8%AF%A2%E5%95%86%E5%93%81%E5%85%B3%E8%81%94%E7%9A%84%E9%97%A8%E5%BA%97%E4%BF%A1%E6%81%AF

---

### 24. 批量查询门店维度商品信息

批量查询门店维度的商品SKU信息。

**接口地址**: `POST /goodlife/v1/item/itemskulist/batch/query`

**请求示例**:
```bash
curl --location 'https://lbs-open.kwailocallife.com/goodlife/v1/item/itemskulist/batch/query' \
--header 'Content-Type: application/json;charset=UTF-8' \
--header 'access-token: YOUR_ACCESS_TOKEN' \
--data '{
    "poi_id": 3002401525209437461,
    "cursor": 0,
    "size": 20
}'
```

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| poi_id | integer | 否 | 门店ID |
| cursor | integer | 否 | 查询游标 |
| size | integer | 否 | 每页条数 |

**参考文档**: https://open.kwailocallife.com/docs/api?apiName=goodlife.v1.item.itemskulist.batch.query&version=1&cid=%E5%95%86%E5%93%81API_19433&cnName=%E6%89%B9%E9%87%8F%E6%9F%A5%E8%AF%A2%E9%97%A8%E5%BA%97%E7%BB%B4%E5%BA%A6%E5%95%86%E5%93%81%E4%BF%A1%E6%81%AF

---

## 通用说明

### 认证方式

所有接口都需要在请求头中携带 `access-token`:

```
--header 'access-token: YOUR_ACCESS_TOKEN'
```

### 日期格式

日期参数统一使用 `YYYYMMDD` 格式,例如: `20260320` 表示 2026年3月20日。

### 分页参数

大部分列表接口支持分页,参数命名可能不同:

- `current_page` / `currentPage` / `page`: 当前页码,从1开始
- `page_size` / `pageSize`: 每页条数,通常为10

### 响应格式

所有接口返回 JSON 格式数据,通常包含以下字段:

```json
{
    "result": 1,
    "error_msg": "success",
    "data": {
        // 具体数据
    }
}
```

### 错误处理

常见错误码:

- `result: 1` - 成功
- `result: 非1` - 失败,查看 `error_msg` 了解具体原因

## 注意事项

1. **认证要求**: 必须提供有效的 `access-token`,否则返回认证失败
2. **请求频率**: 建议控制请求频率,避免频繁调用导致限流
3. **数据权限**: 不同账号的数据权限不同,可能影响返回的数据范围
4. **参数验证**: 调用前验证必填参数是否完整
5. **网络环境**: 确保能访问 `https://lbs-open.kuaishou.com`
