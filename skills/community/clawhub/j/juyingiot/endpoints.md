# Endpoints

## 简体中文

### Base URL
https://openapi.iot02.com/api/v1

### 认证方式
所有请求都需要：

Authorization: <API_Token>

`API_Token` 是用户提供的外置参数。

### 1. 获取全部设备
Method:
GET

Path:
`/equip-read/all-equip-state`

说明：
返回当前账号下可见的全部设备及其状态信息。

### 2. 获取单个设备状态
Method:
GET

Path:
`/equip-read/equip-state?unid={unid}`

说明：
返回单个设备当前状态。
其中查询反馈中的 `io` 通道编号从 `0` 开始，即第 1 路通道对应 `0`。

### 3. 刷新单个设备状态
Method:
POST

Path:
`/equip-opr/equip-read`

说明：
触发服务器读取设备最新实时状态。调用后等待约 1 秒，再重新查询设备状态。

Example body:
```json
{
  "unid": "JY9220351854ALLR",
  "opr": "do",
  "regstart": 0,
  "regnum": 10
}
```

### 4. 打开单个通道
Method:
POST

Path:
`/equip-opr/equip-open`

说明：
控制通道时，`io` 使用从 `1` 开始的编号标识，即第 1 路通道传 `1`。

Example body:
```json
{
  "unid": "JY9220351854ALLR",
  "io": 1
}
```

### 5. 关闭单个通道
Method:
POST

Path:
`/equip-opr/equip-close`

说明：
控制通道时，`io` 使用从 `1` 开始的编号标识，即第 1 路通道传 `1`。

Example body:
```json
{
  "unid": "JY9220351854ALLR",
  "io": 1
}
```

---

## 繁體中文

### Base URL
https://openapi.iot02.com/api/v1

### 驗證方式
所有請求都需要：

Authorization: <API_Token>

`API_Token` 是使用者提供的外部參數。

### 1. 取得全部設備
Method:
GET

Path:
`/equip-read/all-equip-state`

說明：
回傳目前帳號下可見的全部設備及其狀態資訊。

### 2. 取得單一設備狀態
Method:
GET

Path:
`/equip-read/equip-state?unid={unid}`

說明：
回傳單一設備目前狀態。
其中查詢回饋中的 `io` 通道編號從 `0` 開始，即第 1 路通道對應 `0`。

### 3. 刷新單一設備狀態
Method:
POST

Path:
`/equip-opr/equip-read`

說明：
觸發伺服器讀取設備最新即時狀態。呼叫後等待約 1 秒，再重新查詢設備狀態。

Example body:
```json
{
  "unid": "JY9220351854ALLR",
  "opr": "do",
  "regstart": 0,
  "regnum": 10
}
```

### 4. 開啟單一通道
Method:
POST

Path:
`/equip-opr/equip-open`

說明：
控制通道時，`io` 使用從 `1` 開始的編號標識，即第 1 路通道傳 `1`。

Example body:
```json
{
  "unid": "JY9220351854ALLR",
  "io": 1
}
```

### 5. 關閉單一通道
Method:
POST

Path:
`/equip-opr/equip-close`

說明：
控制通道時，`io` 使用從 `1` 開始的編號標識，即第 1 路通道傳 `1`。

Example body:
```json
{
  "unid": "JY9220351854ALLR",
  "io": 1
}
```

---

## English

### Base URL
https://openapi.iot02.com/api/v1

### Authentication
All requests require:

Authorization: <API_Token>

`API_Token` is a user-provided external parameter.

### 1. List all devices
Method:
GET

Path:
`/equip-read/all-equip-state`

Description:
Returns all devices visible to the current user account.

### 2. Get one device state
Method:
GET

Path:
`/equip-read/equip-state?unid={unid}`

Description:
Returns the current state of one device.
In query feedback, the `io` channel index is `0`-based, so channel 1 corresponds to `0`.

### 3. Refresh one device state
Method:
POST

Path:
`/equip-opr/equip-read`

Description:
Triggers the server to fetch the latest real-time device state. Wait about 1 second, then read the state again.

Example body:
```json
{
  "unid": "JY9220351854ALLR",
  "opr": "do",
  "regstart": 0,
  "regnum": 10
}
```

### 4. Open one channel
Method:
POST

Path:
`/equip-opr/equip-open`

Description:
For control commands, `io` uses `1`-based numbering, so channel 1 should be sent as `1`.

Example body:
```json
{
  "unid": "JY9220351854ALLR",
  "io": 1
}
```

### 5. Close one channel
Method:
POST

Path:
`/equip-opr/equip-close`

Description:
For control commands, `io` uses `1`-based numbering, so channel 1 should be sent as `1`.

Example body:
```json
{
  "unid": "JY9220351854ALLR",
  "io": 1
}
```
