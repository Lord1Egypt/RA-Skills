---
name: juyingiot
description: 北京聚英电子有限公司聚英云平台设备控制技能，支持通过 JYDAM、jydam、juyingiot、jycloud、聚英云、北京聚英电子有限公司 等关键词搜索，提供设备添加说明、API_Token 获取说明、设备列表查询、状态读取与设备控制能力。
version: 1.0.1
---

# 操作JYDAM设备

## 简体中文

### 技能说明
本技能用于连接 **北京聚英电子有限公司** 的 **聚英云平台** 设备，并执行以下操作：

- 获取当前账号下的设备列表
- 获取单个设备状态
- 刷新设备实时状态
- 打开某一路继电器
- 关闭某一路继电器
- 按设备名称定位设备后执行控制

### 搜索关键词
为了方便用户搜索和发现本技能，以下关键词均应能命中本技能：

- JYDAM
- jydam
- juyingiot
- jycloud
- 聚英云
- 聚英云平台
- 北京聚英电子有限公司

### 用户输入的外置参数
本技能需要用户提供一个外置参数：

- `API_Token`

`API_Token` 是用户在 **聚英云平台** 中获取的个人接口访问凭证。

规则：
- 不要在技能中写死 `API_Token`
- 不要伪造 `API_Token`
- 不要将一个用户的 Token 用于另一个用户
- 如果用户未提供 `API_Token`，先提示用户提供
- 所有接口请求都必须在 HTTP Header 中携带：

Authorization: <API_Token>

每个用户添加该能力时，必须填写自己独立的 `API_Token`。

### 如何在聚英云平台添加设备并获取 Token
在使用本技能前，用户需要先在 **聚英云平台** 完成设备接入，并准备接口访问凭证。

建议说明如下：

1. 用户先登录聚英云平台账号。
2. 在聚英云平台中完成设备添加、设备接入或设备绑定。
3. 确认目标设备已经出现在当前账号下。
4. 在聚英云平台获取当前用户自己的 `API_Token`。
5. 在安装本技能时，将该 `API_Token` 作为外置参数填写。
6. 后续所有设备查询与控制请求都会使用该 Token 进行鉴权。

如果用户尚未在聚英云平台添加设备，或尚未获取自己的 `API_Token`，则无法正常使用本技能。

### Base URL
https://openapi.iot02.com/api/v1

### 关键标识
- `unid`: 设备唯一 ID
- `io`: 通道号

通道编号补充说明：
- 在查询反馈中，`io` 从 `0` 开始编号，即第 1 路通道对应 `0`
- 在控制通道时，`io` 使用从 `1` 开始的编号标识，即第 1 路通道传 `1`

### 支持的操作

#### 1. 获取全部设备列表
Method:
GET

Path:
`/equip-read/all-equip-state`

Headers:
- `Authorization: <API_Token>`

#### 2. 获取单个设备状态
Method:
GET

Path:
`/equip-read/equip-state?unid={unid}`

Headers:
- `Authorization: <API_Token>`

#### 3. 刷新单个设备状态
Method:
POST

Path:
`/equip-opr/equip-read`

Headers:
- `Authorization: <API_Token>`
- `Content-Type: application/json`

JSON body:
```json
{
  "unid": "<device_unid>",
  "opr": "do",
  "regstart": 0,
  "regnum": 10
}
```

调用该接口后，等待约 1 秒，再重新读取设备状态。

#### 4. 打开单个通道
Method:
POST

Path:
`/equip-opr/equip-open`

Headers:
- `Authorization: <API_Token>`
- `Content-Type: application/json`

JSON body:
```json
{
  "unid": "<device_unid>",
  "io": 1
}
```

#### 5. 关闭单个通道
Method:
POST

Path:
`/equip-opr/equip-close`

Headers:
- `Authorization: <API_Token>`
- `Content-Type: application/json`

JSON body:
```json
{
  "unid": "<device_unid>",
  "io": 1
}
```

### 行为规则
- 当用户要求列出设备时，先调用设备列表接口。
- 当用户使用设备名称而不是 `unid` 时，先获取设备列表并匹配目标设备。
- 如果匹配到多个设备，要求用户进一步确认。
- 在发送控制命令前，确保目标设备和目标通道明确无歧义。
- 只有当用户明确要求控制设备时，才执行控制操作。
- 不要在不明确的情况下猜测目标设备。

### 错误处理
- 若接口返回鉴权相关错误，提示用户提供的 `API_Token` 可能无效、已过期或没有对应权限。
- 若设备不存在，提示无法匹配对应的 `unid` 或设备名称。
- 若控制失败，尽量直接返回接口错误信息。

### 安全说明
- 本技能可能会控制真实硬件设备。
- 仅在用户明确授权和明确指令下执行控制。
- 当请求存在歧义时，不要猜测要控制的设备。
- 在目标不明确时，优先执行只读操作。

---

## 繁體中文

### 技能說明
本技能用於連接 **北京聚英電子有限公司** 的 **聚英雲平台** 設備，並執行以下操作：

- 取得目前帳號下的設備列表
- 取得單一設備狀態
- 刷新設備即時狀態
- 開啟某一路繼電器
- 關閉某一路繼電器
- 依設備名稱定位設備後執行控制

### 搜尋關鍵詞
為了方便使用者搜尋和發現本技能，以下關鍵詞均應能命中本技能：

- JYDAM
- jydam
- juyingiot
- jycloud
- 聚英雲
- 聚英雲平台
- 北京聚英電子有限公司

### 使用者輸入的外部參數
本技能需要使用者提供一個外部參數：

- `API_Token`

`API_Token` 是使用者在 **聚英雲平台** 中取得的個人介面存取憑證。

規則：
- 不要在技能中硬編碼 `API_Token`
- 不要偽造 `API_Token`
- 不要將某位使用者的 Token 用於另一位使用者
- 如果使用者尚未提供 `API_Token`，先提示使用者提供
- 所有介面請求都必須在 HTTP Header 中攜帶：

Authorization: <API_Token>

每位使用者新增此能力時，必須填寫自己獨立的 `API_Token`。

### 如何在聚英雲平台新增設備並取得 Token
在使用本技能前，使用者需要先在 **聚英雲平台** 完成設備接入，並準備介面存取憑證。

建議說明如下：

1. 使用者先登入聚英雲平台帳號。
2. 在聚英雲平台中完成設備新增、設備接入或設備綁定。
3. 確認目標設備已經出現在目前帳號下。
4. 在聚英雲平台取得目前使用者自己的 `API_Token`。
5. 安裝本技能時，將該 `API_Token` 作為外部參數填寫。
6. 後續所有設備查詢與控制請求都會使用該 Token 進行鑑權。

如果使用者尚未在聚英雲平台新增設備，或尚未取得自己的 `API_Token`，則無法正常使用本技能。

### Base URL
https://openapi.iot02.com/api/v1

### 關鍵識別
- `unid`: 設備唯一 ID
- `io`: 通道號

通道編號補充說明：
- 在查詢回饋中，`io` 從 `0` 開始編號，即第 1 路通道對應 `0`
- 在控制通道時，`io` 使用從 `1` 開始的編號標識，即第 1 路通道傳 `1`

### 支援的操作

#### 1. 取得全部設備列表
Method:
GET

Path:
`/equip-read/all-equip-state`

Headers:
- `Authorization: <API_Token>`

#### 2. 取得單一設備狀態
Method:
GET

Path:
`/equip-read/equip-state?unid={unid}`

Headers:
- `Authorization: <API_Token>`

#### 3. 刷新單一設備狀態
Method:
POST

Path:
`/equip-opr/equip-read`

Headers:
- `Authorization: <API_Token>`
- `Content-Type: application/json`

JSON body:
```json
{
  "unid": "<device_unid>",
  "opr": "do",
  "regstart": 0,
  "regnum": 10
}
```

呼叫此介面後，等待約 1 秒，再重新讀取設備狀態。

#### 4. 開啟單一路通道
Method:
POST

Path:
`/equip-opr/equip-open`

Headers:
- `Authorization: <API_Token>`
- `Content-Type: application/json`

JSON body:
```json
{
  "unid": "<device_unid>",
  "io": 1
}
```

#### 5. 關閉單一路通道
Method:
POST

Path:
`/equip-opr/equip-close`

Headers:
- `Authorization: <API_Token>`
- `Content-Type: application/json`

JSON body:
```json
{
  "unid": "<device_unid>",
  "io": 1
}
```

### 行為規則
- 當使用者要求列出設備時，先呼叫設備列表介面。
- 當使用者使用設備名稱而不是 `unid` 時，先取得設備列表並比對目標設備。
- 如果比對到多個設備，要求使用者進一步確認。
- 在送出控制命令前，確保目標設備和目標通道明確無歧義。
- 只有在使用者明確要求控制設備時，才執行控制操作。
- 不要在不明確的情況下猜測目標設備。

### 錯誤處理
- 若介面回傳鑑權相關錯誤，提示使用者提供的 `API_Token` 可能無效、已過期或沒有對應權限。
- 若設備不存在，提示無法比對對應的 `unid` 或設備名稱。
- 若控制失敗，盡量直接回傳介面錯誤資訊。

### 安全說明
- 本技能可能會控制真實硬體設備。
- 僅在使用者明確授權和明確指令下執行控制。
- 當請求存在歧義時，不要猜測要控制的設備。
- 在目標不明確時，優先執行唯讀操作。

---

## English

### Skill overview
This skill is used to connect devices on the **Juying Cloud Platform** operated by **Beijing Juying Electronics Co., Ltd.**, and perform the following actions:

- list all devices under the current account
- get the state of one device
- refresh real-time device state
- open one relay/output channel
- close one relay/output channel
- resolve a device by name before sending control commands

### Search keywords
To improve discoverability, the following search terms should all match this skill:

- JYDAM
- jydam
- juyingiot
- jycloud
- 聚英云
- 聚英云平台
- 北京聚英电子有限公司

### User-provided external parameter
This skill requires one user-provided external parameter:

- `API_Token`

`API_Token` is the user's own API credential obtained from the **Juying Cloud Platform**.

Rules:
- Never hardcode `API_Token`
- Never invent `API_Token`
- Never reuse one user's token for another user
- If `API_Token` is missing, ask the user to provide it first
- Every request must send this HTTP header:

Authorization: <API_Token>

Each user must provide their own `API_Token` when adding this skill.

### How to add devices and get a token on the Juying Cloud Platform
Before using this skill, the user should first complete device onboarding on the **Juying Cloud Platform** and prepare an API credential.

Suggested guidance:

1. The user logs in to their Juying Cloud Platform account.
2. The user adds, binds, or onboards devices on the platform.
3. The user confirms that the target device appears under the current account.
4. The user obtains their own `API_Token` from the Juying Cloud Platform.
5. During skill installation, the user enters that `API_Token` as an external parameter.
6. All subsequent read and control requests use that token for authorization.

If the user has not added devices on the platform, or has not obtained their own `API_Token`, the skill cannot be used properly.

### Base URL
https://openapi.iot02.com/api/v1

### Important identifiers
- `unid`: unique device ID
- `io`: channel number

Additional channel numbering note:
- In query feedback, `io` is `0`-based, so channel 1 corresponds to `0`
- In control commands, `io` is `1`-based, so channel 1 should be sent as `1`

### Supported actions

#### 1. List all devices
Method:
GET

Path:
`/equip-read/all-equip-state`

Headers:
- `Authorization: <API_Token>`

#### 2. Get one device state
Method:
GET

Path:
`/equip-read/equip-state?unid={unid}`

Headers:
- `Authorization: <API_Token>`

#### 3. Refresh one device state
Method:
POST

Path:
`/equip-opr/equip-read`

Headers:
- `Authorization: <API_Token>`
- `Content-Type: application/json`

JSON body:
```json
{
  "unid": "<device_unid>",
  "opr": "do",
  "regstart": 0,
  "regnum": 10
}
```

After calling this endpoint, wait about 1 second, then read the device state again.

#### 4. Open one channel
Method:
POST

Path:
`/equip-opr/equip-open`

Headers:
- `Authorization: <API_Token>`
- `Content-Type: application/json`

JSON body:
```json
{
  "unid": "<device_unid>",
  "io": 1
}
```

#### 5. Close one channel
Method:
POST

Path:
`/equip-opr/equip-close`

Headers:
- `Authorization: <API_Token>`
- `Content-Type: application/json`

JSON body:
```json
{
  "unid": "<device_unid>",
  "io": 1
}
```

### Behavior guidelines
- If the user asks to list devices, call the device list endpoint first.
- If the user refers to a device by name instead of `unid`, first list devices and match the correct target.
- If multiple devices match, ask the user to clarify.
- Before sending a control command, make sure the target device and channel are unambiguous.
- Only control devices when the user explicitly asks to do so.
- Never guess the target device when the request is ambiguous.

### Error handling
- If the API returns an authorization-related error, explain that the provided `API_Token` may be invalid, expired, or missing permission.
- If the device cannot be found, explain that the `unid` or device name could not be matched.
- If a control request fails, report the API error message when available.

### Safety notes
- This skill may control real hardware devices.
- Only perform control operations after clear user authorization and clear instructions.
- Do not guess device targets when the request is ambiguous.
- Prefer read-only actions first when the user's goal is unclear.
