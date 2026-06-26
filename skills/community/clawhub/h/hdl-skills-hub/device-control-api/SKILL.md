---
id: device-control-api
slug: device-control-api
name: 智能家居设备查询与控制 API
description: 供 OpenClaw 调用，用于获取用户家庭中的设备列表及其状态，并执行开关、调光、温度调节等控制操作。
version: 1.1.1
tools: [getDeviceControlData, controlDevice, getDeviceInfo]
tags: [api, device, control, smart-home, documentation]
permissions: [authenticated]
priority: 60
---

# 1. 强制认证与安全约束
- **无 Token 不调用 (STRICT)**: 严禁在没有有效 `accessToken` 的情况下调用此接口。
- **强制前置校验**: 在发起请求前，AI 必须确认 `accessToken` 存在。若不存在，必须先执行分步登录流程。
- **401 处理**: 若接口返回 401（未授权），AI 必须立即尝试 `refreshToken`，成功后静默重试此请求。
- **凭据源**: 系统变量 `${HDL_APP_KEY}`, `${HDL_APP_SECRET}` 必须从根目录下的 `.env` 文件（路径：`../.env`）读取。
- **动态 homeId**: **严禁**使用硬编码的 `homeId`。在调用任何接口前，必须先通过 **[home-management-api](../home-management-api/SKILL.md)** 获取用户选择的房屋 ID。
- **多房屋支持**: 若用户有多个房屋，AI 必须根据用户选择的房屋动态传递 `homeId` 参数。

---

# 2. 接口详细说明

## 2.1 获取设备列表 (getDeviceControlData)
- **接口地址**: `https://gateway.hdlcontrol.com/home-wisdom/app/device/list`
- **请求方式**: `POST`
- **内容类型**: `application/json;charset=UTF-8`

### 2.1.1 请求参数 (AppDeviceListDTO)
| 字段名 | 类型 | 必选 | 描述                                   | 示例 |
| :--- | :--- | :--- |:-------------------------------------| :--- |
| `homeId` | Long | **是** | 住宅房屋 ID。**必须固定使用：`${HDL_HOME_ID}`**。 | `${HDL_HOME_ID}` |
| `gatewayId` | Long | 否 | 网关 ID 查询。                            | `1483281443578613762` |
| `searchType` | String | 否 | 查询方式：`ALL`(全量, 默认), `PAGE`(分页)。      | `"ALL"` |
| `roomId` | Long | 否 | 按房间 ID 过滤。                           | `1483281443578613763` |
| `spk` | String | 否 | 按功能类型过滤（如 `light.dimming`）。          | `"light.dimming"` |
| `collect` | String | 否 | 是否只查询收藏设备：`"1"`(是), `"0"`(否)。        | `"1"` |
| `pageSize` | Long | 否 | 每页条数（`searchType=PAGE` 时生效）。         | `10` |
| `pageNo` | Long | 否 | 当前页码（`searchType=PAGE` 时生效）。         | `1` |
| `appKey` | String | **是** | (BaseDTO) 取自 `${HDL_APP_KEY}`。       | `${HDL_APP_KEY}` |
| `timestamp` | Long | **是** | (BaseDTO) 13 位毫秒级时间戳。                | `1774425423000` |
| `sign` | String | **是** | (BaseDTO) 安全签名。                      | `"abc123xyz..."` |

### 2.1.2 请求示例 (JSON)
```json
{
  "homeId": ${HDL_HOME_ID},
  "searchType": "ALL",
  "appKey": "${HDL_APP_KEY}",
  "timestamp": 1774425423000,
  "sign": "abc123xyz..."
}
```

### 2.1.3 响应结果 (Result<PageVO<DeviceVO>>)
```json
{
  "code": 0,
  "isSuccess": true,
  "data": {
    "total": 1,
    "list": [
      {
        "deviceId": 1483281466097831937,
        "name": "客厅吸顶灯",
        "spk": "light.dimming",
        "gatewayId": 1483281443578613762,
        "online": true,
        "attributes": [
          { "key": "on_off", "value": "on" },
          { "key": "brightness", "value": "80" }
        ]
      }
    ]
  }
}
```

---

## 2.2 控制设备 (controlDevice)
- **接口地址**: `https://gateway.hdlcontrol.com/home-wisdom/app/device/control`
- **请求方式**: `POST`

### 2.2.1 请求参数 (AppDeviceControlDTO)
| 字段名 | 类型 | 必选 | 描述 | 示例 |
| :--- | :--- | :--- | :--- | :--- |
| `homeId` | Long | **是** | 住宅房屋 ID。固定使用：`${HDL_HOME_ID}`。 | `${HDL_HOME_ID}` |
| `gatewayId` | Long | **是** | 设备所属的网关 ID。 | `1483281443578613762` |
| `actions` | List | **是** | 控制动作列表。 | (见下文) |
| `appKey` | String | **是** | (BaseDTO) 固定为 `${HDL_APP_KEY}`。 | `${HDL_APP_KEY}` |
| `timestamp` | Long | **是** | (BaseDTO) 13 位毫秒级时间戳。 | `1774425423000` |
| `sign` | String | **是** | (BaseDTO) 安全签名。 | `"abc123xyz..."` |

### Action 结构
- `deviceId` (Long, 必填): 目标设备 ID。
- `spk` (String, 可选): 功能类型。
- `attributes` (List<StatusBean>, 必填): 控制属性列表。
  - `key` (String): 属性键（如 `on_off`, `brightness`, `target_temperature`）。
  - `value` (String): 属性值（如 `on`, `off`, `50`, `26`）。

### 2.2.2 控制请求示例 (JSON)
```json
{
  "homeId": ${HDL_HOME_ID},
  "gatewayId": 1483281443578613762,
  "actions": [
    {
      "deviceId": 1483281466097831937,
      "spk": "light.dimming",
      "attributes": [
        { "key": "on_off", "value": "on" },
        { "key": "brightness", "value": "100" }
      ]
    }
  ],
  "appKey": "${HDL_APP_KEY}",
  "timestamp": 1774425423000,
  "sign": "abc123xyz..."
}
```

---

## 2.3 获取设备详情 (getDeviceInfo)
- **接口地址**: `https://gateway.hdlcontrol.com/home-wisdom/app/device/info`
- **请求方式**: `POST`

### 2.3.1 请求参数 (AppDeviceGetDTO)
| 字段名 | 类型 | 必选 | 描述 | 示例 |
| :--- | :--- | :--- | :--- | :--- |
| `homeId` | Long | **是** | 住宅房屋 ID。固定使用：`${HDL_HOME_ID}`。 | `${HDL_HOME_ID}` |
| `deviceIds` | List<Long> | **是** | 需要查询详情的设备 ID 列表。 | `[1483281466097831937]` |
| `appKey` | String | **是** | (BaseDTO) 固定为 `${HDL_APP_KEY}`。 | `${HDL_APP_KEY}` |
| `timestamp` | Long | **是** | (BaseDTO) 13 位毫秒级时间戳。 | `1774425423000` |
| `sign` | String | **是** | (BaseDTO) 安全签名。 | `"abc123xyz..."` |

### 2.3.2 请求示例 (JSON)
```json
{
  "homeId": ${HDL_HOME_ID},
  "deviceIds": [1483281466097831937],
  "appKey": "${HDL_APP_KEY}",
  "timestamp": 1774425423000,
  "sign": "abc123xyz..."
}
```

## 5.3 响应结果 (Result<List<DeviceVO>>)
返回 `DeviceVO` 列表。每个对象包含：
- `deviceId`: 设备 ID。
- `name`: 设备名称。
- `spk`: 功能类型。
- `icon`: **设备图标 URL (用于 UI 展示)**。
- `imageUrl`: **设备实时状态图片 URL (若存在则建议展示)**。
- `attributes`: 当前属性列表（key/value）。
- `productProtocol`: 完整的物模型定义（包含该设备支持的所有控制指令及其取值范围）。
- `online`: 在线状态。

---

# 4. 设备功能类型 (SPK) 与本地视觉反馈映射
AI 在控制设备成功后，**必须**展示对应的状态图片。优先展示接口返回的 `imageUrl` 或 `icon`；若接口无返回，则根据 `spk` 和设备状态使用以下 **本地资源 (Local Assets)** 进行展示。

### 4.1 本地图片命名规则 (MANDATORY)
AI 必须根据设备的 `spk` 字段和当前控制/查询到的状态，**将其翻译为开发者规定的“固定状态词 (Fixed Status Words)”**，然后动态拼接文件名。

**命名规则**: `spk` + `_` + `固定状态词` + `.png`
存放路径: https://hdl-hz-dev.oss-cn-hangzhou.aliyuncs.com/test/device/image/

#### 开发者规定的固定状态词映射表:
| 用户意图/设备状态描述 | AI 翻译后的固定状态词 | 示例 (以 spk=light.rgb 为例) |
| :--- | :--- | :--- |
| 暖色、暖光、温馨模式 | `warm` | `light.rgb_warm.png` |
| 冷色、冷光、办公模式 | `cold` | `light.rgb_cold.png` |
| 中性光、自然光 | `medium` | `light.rgb_medium.png` |
| 关闭、熄灭、停止运行 | `close` | `light.rgb_close.png` |
| 开启、打开、启动 (通用) | `on` | `light.switch_on.png` |
| 关闭、断开 (通用) | `off` | `light.switch_off.png` |
| 打开、展开 (如窗帘) | `open` | `curtain_open.png` |
| 停止、保持 (如窗帘) | `stop` | `curtain_stop.png` |
| 触发、报警、检测到 (传感器) | `active` | `sensor_active.png` |

---

# 5. 交互示例 (意图转换与本地图片反馈)

### 场景 A：色温灯调节
1. **用户**：“把书房灯调成温馨的暖色。”
2. **AI**：(调用 `controlDevice`) -> (识别 spk 为 `light.rgb`) -> (将“温馨的暖色”映射为固定词 `warm`)
3. **AI**：“好的，书房灯已为您调节为暖色。✅  
   ![书房暖色灯](../assets/images/light.rgb_warm.png)”

### 场景 B：窗帘控制
1. **用户**：“把窗帘拉开一半吧。”
2. **AI**：(调用 `controlDevice`) -> (识别 spk 为 `curtain`) -> (将“拉开”映射为固定词 `open`)
3. **AI**：“好的，正在为您拉开窗帘。✅  
   ![窗帘打开](../assets/images/curtain_open.png)”

---

# 6. 调用策略与最佳实践
1. **先查后控**: AI 应当先通过 `getDeviceControlData` 获取设备列表，识别出 `deviceId`、`gatewayId` 和支持的 `spk`。
2. **状态反馈**: 控制成功后，AI 应当根据接口返回的 `isSuccess` 状态，结合控制时的属性值（如 `on_off: on`）告知用户操作结果。
3. **精准匹配**: 构造控制指令时，必须确保 `key` 和 `value` 与设备协议 (`productProtocol`) 中的定义完全一致。
4. **异常处理**: 若接口返回 `code != 0` 或 `isSuccess == false`，应清晰告知用户失败原因（如“网关离线”或“设备响应超时”）。
