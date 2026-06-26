---
id: home-management-api
slug: home-management-api
name: 房屋管理 API
description: 供 OpenClaw 调用，用于获取用户的房屋列表信息。支持按房屋类型查询，并提供详细的房屋配置（如名称、类型、控制地址等）。
version: 1.0.0
tools: [queryHomeList]
tags: [api, home, management, documentation]
permissions: [authenticated]
priority: 70
---

# 1. 强制认证与安全约束
- **无 Token 不调用 (STRICT)**: 严禁在没有有效 `accessToken` 的情况下调用此接口。
- **强制前置校验**: 在发起请求前，AI 必须确认 `accessToken` 存在。若不存在，必须先执行分步登录流程。
- **401 处理**: 若接口返回 401（未授权），AI 必须立即尝试 `refreshToken`，成功后静默重试此请求。
- **凭据源**: `${HDL_APP_KEY}`, `${HDL_APP_SECRET}` 必须从根目录下的 `.env` 文件（路径：`../.env`）读取。
- **homeId 动态管理**: 本接口是所有设备控制操作的前置条件。AI 必须从本接口返回的 `data[].homeId` 中获取当前激活的房屋 ID。
- **多房屋支持**: 若返回多个房屋，AI 必须询问用户：“请问您要操作哪个房屋的设备？[房屋1], [房屋2]...”，并根据用户选择动态传递 `homeId` 给后续接口。
- **数据脱敏 (CRITICAL)**: **严禁**在答复中展示 `id`, `homeId`, `userId`, `secretKey`, `localSecret` 等任何数字 ID 或密钥。
- **展示策略**: 仅展示房屋名称 (`homeName`) 和类型 (`homeType`)。

# 2. 接口详细说明

## 2.1 获取房屋列表 (queryHomeList)
- **接口地址**: `https://gateway.hdlcontrol.com/home-wisdom/app/home/list`
- **请求方式**: `POST`
- **内容类型**: `application/json;charset=UTF-8`
- **认证方式**: `Bearer Token` (Header: `Authorization`)

### 2.1.1 请求参数 (JSON Body)
| 字段名 | 类型 | 必选 | 描述 | 示例 |
| :--- | :--- | :--- | :--- | :--- |
| `homeType` | String | 否 | 房屋类型，默认为 `"ALL"`。可选：`"BUSPRO"`, `"KNX"`, `"ZIGBEE"` 等。 | `"ALL"` |
| `autoGenerate` | Boolean | 否 | 是否自动生成，默认为 `false`。 | `false` |
| `appKey` | String | **是** | (BaseDTO) 取自 `${HDL_APP_KEY}`。 | `${HDL_APP_KEY}` |
| `timestamp` | Long | **是** | (BaseDTO) 13 位毫秒级时间戳。 | `1774832589000` |
| `sign` | String | **是** | (BaseDTO) 安全签名。 | `"f9231f092dd3146edb6b63459bff4b3e"` |

### 2.1.2 请求示例 (JSON)
```json
{
  "homeType": "ALL",
  "autoGenerate": false,
  "appKey": "${HDL_APP_KEY}",
  "timestamp": 1774832589000,
  "sign": "f9231f092dd3146edb6b63459bff4b3e"
}
```

### 2.1.3 响应结果 (Result<List<HomeVO>>)
```json
{
  "code": 0,
  "isSuccess": true,
  "data": [
    {
      "id": "1680887876682665985",
      "homeId": "1680887876682665985",
      "homeName": "MyHome",
      "homeType": "BUSPRO",
      "regionUrl": "https://china-gateway.hdlcontrol.com",
      "isBindGateway": false,
      "isRemoteControl": true,
      "deviceCount": 0,
      "secretKey": "******",
      "localSecret": "******"
    }
  ],
  "requestId": "f767c17f48f31d9b37290a3ea0b426cc",
  "timestamp": "1774832589298"
}
```

# 3. 调用策略与提示
1. **房屋切换**: 若用户有多个房屋，AI 应列出所有房屋名称 (`homeName`) 供用户选择。
2. **静默获取 HomeId**: 拿到房屋列表后，AI 内部记录选定房屋的 `homeId`，用于后续设备控制。**严禁向用户提及该 ID**。
3. **区域 URL 动态适配**: 注意响应中的 `regionUrl`，某些特定房屋的 API 可能需要切换到该 URL 下的网关。
