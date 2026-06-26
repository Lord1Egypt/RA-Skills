# 京东国际物流轨迹追踪技能

根据用户输入的批量物流单号，调用京东国际物流开放接口，批量查询物流轨迹信息。支持灵活注入 referenceNumber 物流单号参数，可根据用户查询意图自动匹配并填充对应参数。

## 触发场景

当用户需要查询物流轨迹、订单状态、包裹运输进度、运单跟踪时使用此技能，例如：
- "查一下 JDW100xxxxxx6372 的物流轨迹"
- "查询订单号 FS2026xxxxxx0098405P 的信息"
- "查询客户运单号 1435xxxxxx460 的物流"
- "查询承运商运单号 505xxxxxx44680 的轨迹"
- "帮我查一下 JDW1xxxxxx6372 的物流"
- "查一下这个单号的物流信息 JDW1xxxxxx6372"

## 操作步骤

### 1. 调用命令行获取物流轨迹查询结果
#### 核心执行规则（必须严格遵守）
1. **禁止在命令中出现任何 -- 开头的参数**（一律不允许出现）
2. 只传入**1个参数的纯值**，支持单个单号、多个单号
3. 多个单号使用英文逗号 , 直接分隔，不使用任何引号，不使用空格
4. **单号（referenceNumber）为必填参数**，不可为空

#### {baseDir}表示当前 SKILL.md 文件所在的全路径

#### 固定执行命令模板（直接替换值）
```bash
node {baseDir}/scripts/get_tracking_data.js 单号1,单号2,单号3
```

#### 真实运行示例
```bash
node {baseDir}/scripts/get_tracking_data.js "JDWxxxxxx6372"
```

## 使用示例

### 示例 1：查询单个物流单号 JDW1*****6372

```bash
node {baseDir}/scripts/get_tracking_data.js JDWxxxxxx96372
```

### 示例 2：查询多个物流单号 JDW1xxxxxx6372 和 JDW100xxxxxx696373

```bash
node {baseDir}/scripts/get_tracking_data.js JDWxxxxxx96372,JDW100xxxxxx696373
```


## 响应格式说明

### 响应状态码

| 状态码 | 说明 |
|-------|------|
| 1000 | 请求成功 |
| 其他 | 请求失败，请查看 msg 字段获取详细信息 |

### trackingNodes 数组元素说明

| 字段名 | 类型 | 说明 |
|-------|------|------|
| orderNo | string | 订单号 |
| referenceNumber | string | 物流单号 |
| referenceType | number | 单号类型（固定为 0） |
| trackings | array | 轨迹详情数组 |
| waybillNo | string | 运单号 |

### trackings 数组元素说明

| 字段名 | 类型 | 说明 |
|-------|------|------|
| extend | object | 扩展信息 |
| field | string | 字段类型 |
| operateLocation | object | 操作位置 |
| operateSiteId | string | 操作站点ID |
| operationCode | string | 操作代码 |
| operationTime | string | 时间 |
| operationType | string | 操作类型 |
| operatorName | string | 操作人 |
| remark | string | 轨迹信息 |
| waybillNo | string | 运单号 |

### operateLocation 字段说明

| 字段名 | 类型 | 说明 |
|-------|------|------|
| routeCityName | string | 城市名称 |
| routeCountry | string | 国家名称 |
| routeProvinceName | string | 州(省)名称 |

### extend 字段说明

| 字段名 | 类型 | 说明 |
|-------|------|------|
| operationTimestamp | string | 时间戳 |
| timeZone | string | 操作时区 |
| remark | string | 备注 |
| locale | string | 语言 |

### 成功响应示例 - 没有轨迹信息

```json
{
  "code": 1000,
  "msg": "请求成功",
  "data": [
    {
      "referenceNumber": "JDW10xxxxxxx96372",
      "referenceType": 0,
      "trackingNodes": []
    }
  ]
}
```

### 成功响应示例 - 有轨迹数据

```json
{
  "code": 1000,
  "data": [
    {
      "referenceNumber": "JDW10xxxxxxx96372",
      "referenceType": 0,
      "trackingNodes": [
        {
          "orderNo": "FS2026xxxxxx98405P",
          "referenceNumber": "JDW10xxxxxx96372",
          "referenceType": 0,
          "trackings": [
            {
              "extend": {
                "operationTimestamp": "1774431780000",
                "timeZone": "UTC+08:00",
                "remark": "已分配车辆和司机/ Vehicle and driver assigned",
                "locale": "zh-CN"
              },
              "field": "waybill",
              "operateLocation": {},
              "operateSiteId": "",
              "operationCode": "A02",
              "operationTime": "2026-03-25 17:43:00",
              "operationType": "8000",
              "operatorName": "liukunmiao",
              "remark": "已提货/Cargo already picked up",
              "waybillNo": "JDW10xxxxxx96372"
            },
            {
              "extend": {
                "operationTimestamp": "1774490659000",
                "timeZone": "UTC+08:00",
                "remark": "承运商已上门提货",
                "locale": "zh-CN"
              },
              "field": "waybill",
              "operateLocation": {},
              "operateSiteId": "",
              "operationCode": "DMPU",
              "operationTime": "2026-03-26 10:04:19",
              "operationType": "8000",
              "operatorName": "bjtfei",
              "remark": "承运商已上门提货",
              "waybillNo": "JDW10xxxxxx96372"
            },
            {
              "extend": {
                "operationTimestamp": "1774490967000",
                "timeZone": "UTC+08:00",
                "remark": "已妥投/Cargo delivered",
                "locale": "zh-CN"
              },
              "field": "waybill",
              "operateLocation": {},
              "operateSiteId": "",
              "operationCode": "DLV",
              "operationTime": "2026-03-26 10:09:27",
              "operationType": "8000",
              "operatorName": "bjtfei",
              "remark": "已妥投/Cargo delivered",
              "waybillNo": "JDW10xxxxxx96372"
            }
          ],
          "waybillNo": "JDW10xxxxxx96372"
        }
      ]
    }
  ],
  "msg": "请求成功"
}
```

### 成功响应示例 - 批量查询（两个单号）

```json
{
  "code": 1000,
  "data": [
    {
      "referenceNumber": "JDW100xxxxxx643",
      "referenceType": 0,
      "trackingNodes": [
        {
          "carrierWaybillNo": "JDW100xxxxxx643",
          "orderNo": "FS2025xxxxxx076950",
          "referenceNumber": "JDW1xxxxxx23643",
          "referenceType": 0,
          "trackings": [
            {
              "extend": {
                "locale": "zh-CN",
                "SPP": "WAYBILL",
                "state": "COSH",
                "operationTimestamp": "1762617596000",
                "packageId": "JDW100xxxxxx643-1-1-",
                "timeZone": "UTC+08:00"
              },
              "field": "waybill",
              "operateLocation": {},
              "operationCode": "COSH",
              "operationTime": "2025-11-08 23:59:56",
              "operationType": "8000",
              "operatorName": "COSH",
              "remark": "Client Order Shipped"
            },
            {
              "extend": {
                "locale": "zh-CN",
                "SPP": "SPP99009b",
                "cityName": "HGK",
                "state": "CXLHDP",
                "operationTimestamp": "1762713000000",
                "packageId": "JDW100xxxxxx643-1-1-",
                "timeZone": "UTC+08:00"
              },
              "field": "waybill",
              "operateLocation": {
                "routeCityName": "HGK"
              },
              "operationCode": "CXLHDP",
              "operationTime": "2025-11-10 02:30:00",
              "operationType": "8000",
              "operatorName": "CXLHDP",
              "remark": "Departure from origin port",
              "waybillNo": "505755044680"
            },
            {
              "extend": {
                "locale": "zh-CN",
                "SPP": "SPP99009b",
                "cityName": "ICN",
                "state": "CXLHAP",
                "operationTimestamp": "1762725840000",
                "packageId": "JDW100xxxxxx643-1-1-",
                "timeZone": "UTC+08:00"
              },
              "field": "waybill",
              "operateLocation": {
                "routeCityName": "ICN"
              },
              "operationCode": "CXLHAP",
              "operationTime": "2025-11-10 06:04:00",
              "operationType": "8000",
              "operatorName": "CXLHAP",
              "remark": "Arrive at destination port",
              "waybillNo": "505755044680"
            }
          ],
          "waybillNo": "JDW100xxxx23643"
        }
      ]
    },
    {
      "referenceNumber": "JDW100xxxx23643",
      "referenceType": 0,
      "trackingNodes": [
        {
          "referenceNumber": "JDW100xxxxxx643",
          "referenceType": 0,
          "trackings": [],
          "waybillNo": "JDW100xxxxxx643"
        }
      ]
    }
  ],
  "msg": "请求成功"
}
```

### 成功响应示例 - 未查询到单据的物流轨迹（单个查询）

```json
{
  "code": 1000,
  "msg": "请求成功",
  "data": []
}
```

### 格式化输出示例

#### 输出开头要求
**物流轨迹详情：**

京东运单号:JDWxxxxxx890
京东订单号:FS1xxxxxx900

| 序号 | 时间 | 地点 | 轨迹 |
|-----|---------|-------|------|
| 1 | UTC+8 2026-03-25 17:43:00 | MISSOURI CITY，US，TX | 已提货/Cargo already picked up |
| 2 | UTC+8 2026-03-26 10:04:19 | CHAMPAIGN，US，IL | 承运商已上门提货 |
| 3 | UTC+8 2026-03-26 10:09:27 | Lake Zurich，US，IL | ✅Delivered |

#### 示例 2：批量查询结果
**单号 JDW000xxxxxx6629 轨迹详情：**

| 序号 | 时间 | 地点 | 轨迹 |
|-----|---------|-------|------|
| 1 | UTC+8 2026-03-25 18:43:00 | MISSOURI CITY，US，TX | 已提货/Cargo already picked up |
| 2 | UTC+8 2026-03-26 12:04:19 | CHAMPAIGN，US，IL | 承运商已上门提货 |
| 3 | UTC+8 2026-03-26 14:09:27 | Lake Zurich，US，IL | ✅Delivered |

**单号 JDW00xxxxxx6630 轨迹详情：**
- 物流单号 JDW00xxxxxx6630 未查询到物流轨迹

**单号 JDW00xxxxx6631 错误信息：**
- [错误信息描述]

#### 示例 3：批量查询结果（两个单号，一时区示例）
【客户信息】
客户编码：KH00000000001

**单号 JDW10xxxxxx3643 轨迹详情：**

| 序号 | 时间 | 地点 | 轨迹 |
|-----|------|-------|------|
| 1 | UTC+8 2025-11-08 23:59:56 |  | Parcel Data Received |
| 2 | UTC+8 2025-11-10 02:30:00 | US | Shipment information sent to FedEx |
| 3 | UTC+8 2025-11-10 06:04:00 | MISSOURI CITY，TX，US | Picked up |

**单号 JDW200xxxxxx098 轨迹详情：**
- 物流单号 JDW200xxxxxx098 未查询到物流轨迹

#### 示例 4：未查询到单据的物流轨迹（单个查询）

查询结果：物流单号 JDW200xxxxxx098 未查询到物流轨迹

## 输出结果处理

- 输出结果字段包含序号、时间、地点和轨迹
- 如果`轨迹信息`字段返回内容与`Delivered`或`delivered`完全匹配，在`轨迹`中必须在其左侧加上`✅`，例如：`✅Delivered`
- `地点`严格按照[城市名称，州(省)名称,国家名称]进行拼接展示，如果字段为空，则不展示
- 如果 trackingNodes 为空数组，表示该单号暂无轨迹信息
- `时间`严格按照[操作时区 时间]进行拼接展示，并且不要换行展示
- 展示时间时，使用 `trackings[].operationTime` 字段（已格式化为 "YYYY-MM-DD HH:mm:ss"），而不是 `extend.operationTimestamp` 时间戳
- 展示时区时，优先使用 `trackings[].extend.timeZone`

## 注意事项

- `JDW`开头的单号表示京东运单号
- `FS`开头的单号表示京东订单号
- 每个物流单号需要在 referenceList 数组中单独创建一个对象
- referenceType 固定为 0，无需修改
- customerCode 保持为空字符串
- 支持批量查询，在 referenceList 数组中追加多个单号对象即可
- 固定参数（appKey、includeFields、locale、scope、timeZone）保持不变
- **重要：当响应的 data 数组为空时，表示未查询到单号的物流轨迹，此时直接返回简单提示信息："查询结果：物流单号 {单号} 未查询到物流轨迹"。不要输出任何其他信息。**

## 可选：数据分析（按需提供）

在展示完基础数据后，如果数据有分析价值，可以追加以下分析（任选，根据数据情况）：

**物流轨迹可分析：**
- 平均配送时长
- 各环节耗时分布
- 异常节点识别

**注意：** 数据分析是可选的，仅在数据量≥3条时提供，必须基于真实数据，不得编造。