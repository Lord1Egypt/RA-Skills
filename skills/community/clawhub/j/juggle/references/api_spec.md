# Juggle API 规范

## 目录
- [概览](#概览)
- [流程触发接口](#流程触发接口)
- [异步流程结果查询接口](#异步流程结果查询接口)
- [常见错误码](#常见错误码)
- [使用示例](#使用示例)

## 概览
通过 Juggle OpenAPI 触发流程执行，支持同步和异步两种流程类型，异步流程可通过轮询接口获取执行结果。

## 流程触发接口

### 基本信息
- **Path**: `/open/v1/flow/trigger/{flowVersion}/{flowKey}`
- **Method**: POST
- **Content-Type**: application/json

### 请求头

| 名称 | 类型 | 是否必填 | 描述 |
|------|------|----------|------|
| Juggle-Token | String | 非必填 | OpenApi 的令牌值，通过请求头传递 |
| Content-Type | String | 必填 | 固定值：application/json |

### 路径参数

| 名称 | 类型 | 是否必填 | 描述 |
|------|------|----------|------|
| flowVersion | String | 必填 | 流程版本 |
| flowKey | String | 必填 | 流程 Key |

### 请求体

| 名称 | 类型 | 是否必填 | 描述 |
|------|------|----------|------|
| flowData | Object | 非必填 | 流程定义的入参 Key 与 value 的键值对，如果流程没有入参，可以不填 |

**请求体示例**：
```json
{
  "flowData": {
    "orderId": "12345",
    "userId": "user001",
    "amount": 100.50
  }
}
```

### 响应格式

| 名称 | 类型 | 描述 |
|------|------|------|
| success | Boolean | 是否成功 |
| errorCode | Long | 错误码 |
| errorMsg | String | 错误信息 |
| result | Object | 流程定义中设置的出参结果 |
| - flowInstanceId | String | 流程触发后的实例 ID |
| - flowType | String | 流程类型（sync：同步，async：异步） |
| - status | String | 流程的执行状态 |
| - data | Map | 流程返回的实际数据，即流程定义中定义的出参 |

**同步流程成功响应示例**：
```json
{
  "success": true,
  "errorCode": null,
  "errorMsg": null,
  "result": {
    "flowInstanceId": "flow-instance-12345",
    "flowType": "sync",
    "status": "FINISH",
    "data": {
      "processResult": "completed",
      "outputValue": "result-data"
    }
  }
}
```

**异步流程成功响应示例**：
```json
{
  "success": true,
  "errorCode": null,
  "errorMsg": null,
  "result": {
    "flowInstanceId": "flow-instance-67890",
    "flowType": "async",
    "status": "RUNNING",
    "data": null
  }
}
```

**失败响应示例**：
```json
{
  "success": false,
  "errorCode": 40001,
  "errorMsg": "流程不存在",
  "result": null
}
```

## 异步流程结果查询接口

### 基本信息
- **Path**: `/v1/open/flow/getAsyncFlowResult/`
- **Method**: GET
- **Content-Type**: application/json

### 请求头

| 名称 | 类型 | 是否必填 | 描述 |
|------|------|----------|------|
| Juggle-Token | String | 非必填 | OpenApi 的令牌值，通过请求头传递 |
| Content-Type | String | 必填 | 固定值：application/json |

### 查询参数

| 名称 | 类型 | 是否必填 | 描述 |
|------|------|----------|------|
| flowInstanceId | String | 必填 | 异步流程实例 ID |

### 响应格式

| 名称 | 类型 | 描述 |
|------|------|------|
| success | Boolean | 是否成功 |
| errorCode | Long | 错误码 |
| errorMsg | String | 错误信息 |
| result | Object | 流程定义中设置的出参结果 |

**执行中响应示例**：
```json
{
  "success": true,
  "errorCode": null,
  "errorMsg": null,
  "result": null
}
```

**执行完成响应示例**：
```json
{
  "success": true,
  "errorCode": null,
  "errorMsg": null,
  "result": {
    "processResult": "completed",
    "outputValue": "final-result"
  }
}
```

**执行失败响应示例**：
```json
{
  "success": false,
  "errorCode": null,
  "errorMsg": null,
  "result": {}
}
```

## 常见错误码

| 错误码 | 描述 | 解决方案 |
|--------|------|----------|
| 40001 | 流程不存在 | 检查 flowVersion 和 flowKey 是否正确 |
| 40002 | 认证失败 | 检查 Juggle-Token 是否有效 |
| 40003 | 参数错误 | 检查 flowData 格式是否符合流程定义 |
| 40004 | 流程实例不存在 | 检查 flowInstanceId 是否正确 |
| 50001 | 服务器内部错误 | 联系管理员或稍后重试 |

## 使用示例

### 流程触发示例

#### cURL 示例
```bash
curl -X POST "https://api.juggle.plus/open/v1/flow/trigger/v1/order-process" \
  -H "Content-Type: application/json" \
  -H "Juggle-Token: your-token-here" \
  -d '{
    "flowData": {
      "orderId": "12345",
      "userId": "user001"
    }
  }'
```

#### Python 示例
```python
import requests

url = "https://api.juggle.plus/open/v1/flow/trigger/v1/order-process"
headers = {
    "Content-Type": "application/json",
    "Juggle-Token": "your-token-here"
}
data = {
    "flowData": {
        "orderId": "12345",
        "userId": "user001"
    }
}

response = requests.post(url, headers=headers, json=data)
result = response.json()
print(result)
```

### 异步流程结果查询示例

#### cURL 示例
```bash
curl -X GET "https://api.juggle.plus/v1/open/flow/getAsyncFlowResult/?flowInstanceId=flow-instance-12345" \
  -H "Content-Type: application/json" \
  -H "Juggle-Token: your-token-here"
```

#### Python 示例
```python
import requests
import time

base_url = "https://api.juggle.plus"
flow_instance_id = "flow-instance-12345"
headers = {
    "Content-Type": "application/json",
    "Juggle-Token": "your-token-here"
}

# 轮询查询结果
while True:
    url = f"{base_url}/v1/open/flow/getAsyncFlowResult/"
    response = requests.get(url, headers=headers, params={"flowInstanceId": flow_instance_id})
    result = response.json()
    
    if result["success"]:
        status = result["result"]["status"]
        if status == "SUCCESS":
            print("流程执行成功:", result["result"]["data"])
            break
        elif status == "FAILED":
            print("流程执行失败:", result["result"]["data"])
            break
        else:
            print(f"流程执行中，状态: {status}")
            time.sleep(2)  # 等待 2 秒后再次查询
    else:
        print("查询失败:", result["errorMsg"])
        break
```

## 注意事项
1. `Juggle-Token` 的必要性取决于具体流程配置，某些流程可能允许匿名访问
2. `flowData` 的字段名和类型必须与流程定义的入参一致
3. 响应中的 `flowInstanceId` 可用于后续查询流程执行状态
4. 异步流程需要通过轮询接口获取最终结果，建议设置合理的轮询间隔（如 2-5 秒）
5. 根据返回的 `flowType` 字段判断流程类型，采取不同的处理策略
