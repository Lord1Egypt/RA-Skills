# Examples

## 简体中文

### 示例 1：列出设备
用户：
列出我的 JYDAM 设备

预期行为：
- 检查 `API_Token` 是否已提供
- 调用：
  GET /equip-read/all-equip-state
- 使用请求头：
  Authorization: <API_Token>

### 示例 2：查询单个设备状态
用户：
查询 juyingiot 设备 JY912028250F7FUQ-96 的状态

预期行为：
- 调用：
  GET /equip-read/equip-state?unid=JY912028250F7FUQ-96
- 理解返回结果时注意：查询反馈中的 `io` 从 `0` 开始编号，第 1 路通道对应 `0`

### 示例 3：打开单个通道
用户：
打开 jycloud 设备 JY9220351854ALLR 的第 1 路

预期行为：
- 调用：
  POST /equip-opr/equip-open
- JSON body:
```json
{
  "unid": "JY9220351854ALLR",
  "io": 1
}
```
- 控制通道时注意：发送控制命令时，第 1 路通道传 `1`

### 示例 4：关闭单个通道
用户：
关闭聚英云设备 JY9220351854ALLR 的第 1 路

预期行为：
- 调用：
  POST /equip-opr/equip-close
- JSON body:
```json
{
  "unid": "JY9220351854ALLR",
  "io": 1
}
```
- 控制通道时注意：发送控制命令时，第 1 路通道传 `1`

### 示例 5：先按名称匹配设备
用户：
关闭温室1的 2 号通道

预期行为：
- 先调用：
  GET /equip-read/all-equip-state
- 根据设备名称匹配 “温室1”
- 匹配成功后再执行关闭操作
- 若控制第 2 路通道，则控制命令中的 `io` 应传 `2`

### 示例 6：平台准备说明
用户：
我还没用过这个能力，应该怎么开始？

建议回复：
- 请先在聚英云平台添加你的设备
- 确认设备已经绑定到当前账号下
- 获取你自己的 `API_Token`
- 安装或使用技能时填写该 `API_Token`
- 然后再执行设备查询和控制

---

## 繁體中文

### 範例 1：列出設備
使用者：
列出我的 JYDAM 設備

預期行為：
- 檢查 `API_Token` 是否已提供
- 呼叫：
  GET /equip-read/all-equip-state
- 使用請求頭：
  Authorization: <API_Token>

### 範例 2：查詢單一設備狀態
使用者：
查詢 juyingiot 設備 JY912028250F7FUQ-96 的狀態

預期行為：
- 呼叫：
  GET /equip-read/equip-state?unid=JY912028250F7FUQ-96
- 理解回傳結果時注意：查詢回饋中的 `io` 從 `0` 開始編號，第 1 路通道對應 `0`

### 範例 3：開啟單一通道
使用者：
開啟 jycloud 設備 JY9220351854ALLR 的第 1 路

預期行為：
- 呼叫：
  POST /equip-opr/equip-open
- JSON body:
```json
{
  "unid": "JY9220351854ALLR",
  "io": 1
}
```
- 控制通道時注意：發送控制命令時，第 1 路通道傳 `1`

### 範例 4：關閉單一通道
使用者：
關閉聚英雲設備 JY9220351854ALLR 的第 1 路

預期行為：
- 呼叫：
  POST /equip-opr/equip-close
- JSON body:
```json
{
  "unid": "JY9220351854ALLR",
  "io": 1
}
```
- 控制通道時注意：發送控制命令時，第 1 路通道傳 `1`

### 範例 5：先依名稱比對設備
使用者：
關閉溫室1的 2 號通道

預期行為：
- 先呼叫：
  GET /equip-read/all-equip-state
- 根據設備名稱比對「溫室1」
- 比對成功後再執行關閉操作
- 若控制第 2 路通道，則控制命令中的 `io` 應傳 `2`

### 範例 6：平台準備說明
使用者：
我還沒用過這個能力，應該怎麼開始？

建議回覆：
- 請先在聚英雲平台新增你的設備
- 確認設備已經綁定到目前帳號下
- 取得你自己的 `API_Token`
- 安裝或使用技能時填寫該 `API_Token`
- 然後再執行設備查詢和控制

---

## English

### Example 1: list devices
User:
List my JYDAM devices

Expected behavior:
- Check whether `API_Token` is available
- Call:
  GET /equip-read/all-equip-state
- Use header:
  Authorization: <API_Token>

### Example 2: get one device state
User:
Check the state of juyingiot device JY912028250F7FUQ-96

Expected behavior:
- Call:
  GET /equip-read/equip-state?unid=JY912028250F7FUQ-96
- When reading the response, note that `io` in query feedback is `0`-based, so channel 1 corresponds to `0`

### Example 3: open one channel
User:
Open channel 1 on jycloud device JY9220351854ALLR

Expected behavior:
- Call:
  POST /equip-opr/equip-open
- JSON body:
```json
{
  "unid": "JY9220351854ALLR",
  "io": 1
}
```
- For control commands, send `1` for channel 1

### Example 4: close one channel
User:
Close channel 1 on Juying Cloud device JY9220351854ALLR

Expected behavior:
- Call:
  POST /equip-opr/equip-close
- JSON body:
```json
{
  "unid": "JY9220351854ALLR",
  "io": 1
}
```
- For control commands, send `1` for channel 1

### Example 5: match by device name first
User:
Close channel 2 on Greenhouse 1

Expected behavior:
- First call:
  GET /equip-read/all-equip-state
- Match the device name "Greenhouse 1"
- Then send the close command
- If controlling channel 2, `io` in the control command should be `2`

### Example 6: onboarding guidance
User:
I have never used this skill before. How do I start?

Suggested response:
- First add your devices on the Juying Cloud Platform
- Confirm the devices are visible under your current account
- Obtain your own `API_Token`
- Enter that `API_Token` when installing or using the skill
- Then proceed with device queries and control

---
