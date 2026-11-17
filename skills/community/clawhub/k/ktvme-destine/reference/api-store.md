# 门店 API

> ⚠️ **前置依赖**：本接口文档依赖 `km-bot` 工具。详见 [cli-install.md](./cli-install.md)
>
> 📖 **通用约束**：字段映射规则和禁止事项详见 [api-overview.md](./api-overview.md)

---

## searchCompany - 查询门店列表

**用途**：查询可预订的KTV门店列表

**调用方式**：

```bash
km-bot call saasktv searchCompany "{\"keyword\":\"NEO KTV\"}"
```

**请求参数**：

| 字段      | 类型   | 必填 | 说明                                           |
| --------- | ------ | ---- | ---------------------------------------------- |
| keyword   | String | 是   | 查询门店关键词，支持门店名称、城市、门店地址等 |
| latitude  | Number | 否   | 纬度，用于计算距离和排序                       |
| longitude | Number | 否   | 经度，用于计算距离和排序                       |

**成功返回示例**：

```json
{
  "jsonrpc": "2.0",
  "id": "km_rpc_xxx",
  "result": [
    {
      "companyid": 1265,
      "companyname": ["NEO · AI自助KTV"],
      "companycode": ["01171"],
      "logourl": [
        "https://filedownload-dev.ktvme.com/FileService/downloadstorefile.do?fileid=3291111"
      ],
      "companyaddress": ["长沙市天心区五一广场123号"],
      "phone": ["18000000001"],
      "distance": ["500m"],
      "business_status": 0,
      "deslowprice": 88,
      "openhour": "12:00",
      "closehour": "06:00",
      "envpicurl": ["https://env-photo1.com", "https://env-photo2.com"],
      "destine_begin_time": ["12:00"],
      "destine_end_time": ["02:00"]
    }
  ]
}
```

**返回字段说明**：

| 字段                        | 类型   | 说明                                       |
| --------------------------- | ------ | ------------------------------------------ |
| result[].companyid          | Number | 商家 ID（**用于后续查询接口参数**）        |
| result[].companycode        | Array  | 商家编码（**用于 switchCompany**）         |
| result[].companyname        | Array  | 商家名称（展示给用户）                     |
| result[].companyaddress     | Array  | 商家地址（展示给用户）                     |
| result[].phone              | Array  | 预定电话                                   |
| result[].distance           | Array  | 距离（含单位 m/km 等），需传入经纬度才返回 |
| result[].business_status    | Number | 门店状态：0:营业中 1:筹备中 2:暂停营业     |
| result[].deslowprice        | Number | 抵消价格                                   |
| result[].openhour           | String | 开门时间                                   |
| result[].closehour          | String | 关门时间                                   |
| result[].envpicurl          | Array  | 门店环境照片列表                           |
| result[].destine_begin_time | Array  | 预定开始时间                               |
| result[].destine_end_time   | Array  | 预定结束时间                               |

**需保存的关键字段**：

| 字段          | 类型   | 说明                                                           |
| ------------- | ------ | -------------------------------------------------------------- |
| `companycode` | Array  | 商家编码（字符串数组），**用于 switchCompany**                 |
| `companyid`   | Number | 商家 ID（数字），**用于后续查询接口（queryRoomAvailability 等）** |

**异常返回示例**：

```json
{
  "jsonrpc": "2.0",
  "id": "km_rpc_xxx",
  "error": {
    "code": -1,
    "message": "查询失败"
  }
}
```

---

## switchCompany - 切换当前门店

> ⚠️ **【强制要求】每次用户选择门店后必须调用此接口**
>
> **未调用此接口导致的后果**：后端会话上下文不会切换到新门店，后续所有接口调用将在错误的门店上下文中执行，导致：
>
> - 查询到的包厢/价格等信息属于旧门店
> - 创建的订单属于旧门店
> - 用户预订失败或预订到错误的门店

**用途**：切换当前操作的门店上下文

**前置条件**：必须先调用 searchCompany 获取 `companycode`

> **💡 特殊情况说明**：
>
> 如果用户直接指定门店名称（如"预订NEO KTV"），模型应：
>
> 1. 先用该门店名作为 `keyword` 调用 `searchCompany` 进行确认
> 2. 从返回结果中获取对应的 `companycode`
> 3. 再调用 `switchCompany(company_code)` 切换上下文
>
> **原因**：`companycode` 是内部编码（如 "01171"），用户不会直接提供，必须通过 `searchCompany` 确认和获取。

**调用方式**：

```bash
km-bot call saasktv switchCompany "{\"company_code\":\"01171\"}"
```

**请求参数**：

| 字段         | 类型   | 必填 | 说明     |
| ------------ | ------ | ---- | -------- |
| company_code | String | 是   | 商家编码 |

> **💡 来源说明**：
>
> - `company_code` 来自 `searchCompany` 接口返回结果中的 `companycode` 字段
> - `searchCompany` 返回的 `companycode` 是一个数组，如 `["01171"]`
> - 调用 `switchCompany` 时，需取出数组中的编码字符串（如 `"01171"`）作为参数值

**⚠️ 重要区分**：

> - `switchCompany` 使用 **`company_code`**（字符串类型）
> - 查询接口（queryRoomAvailability 等）使用 **`company_id`**（数字类型，来自 `companyid`）
> - **不要混淆这两个字段**

**成功返回示例**：

```json
{
  "jsonrpc": "2.0",
  "id": "km_rpc_xxx",
  "result": {
    "ret": 0,
    "msg": "切换成功"
  }
}
```

**异常返回示例**：

```json
{
  "jsonrpc": "2.0",
  "id": "km_rpc_xxx",
  "error": {
    "code": -1,
    "message": "门店不存在"
  }
}
```

---

## 切换门店的重置规则

**⚠️ 中途换店必须重置所有上下文**：

如果用户在已选择包厢/选择时段/甚至已进入支付环节后要求换店：

1. 调用 `searchCompany` 查询新门店（如需）
2. 调用 `switchCompany(company_code="xxx")` 切换上下文
3. **清空所有之前收集的预订信息**（包厢类型、日期、时间段、活动ID、价格等）
4. 向用户明确告知切换情况
5. 从查询包厢列表重新开始预订流程
