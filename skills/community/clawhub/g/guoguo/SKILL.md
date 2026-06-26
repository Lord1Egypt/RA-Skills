---
name: create-send-order
description: 裹裹寄件下单，通过MCP连接裹裹寄件服务创建寄件订单。当用户需要寄件、下单、创建寄件订单、寄快递时使用此skill。触发词：寄件、下单、寄快递、寄件下单、创建订单、裹裹下单。
---

# 裹裹寄件下单

通过 MCP 连接裹裹寄件服务（GUOGUO_SEND_SERVICE），为用户创建寄件订单。

## 前置检查：自动配置 MCP

**每次触发此 skill 时，必须先执行此步骤。**

检查当前可用的 MCP tool 列表中是否存在 `guoguo_send_server` 相关的 tool（如 `mcp_guoguo_send_server_GUOGUO_SEND_ORDER_CREATE`）。

- **如果已存在** → 跳过，直接进入下单流程
- **如果不存在** → 执行自动配置脚本（使用 skill 加载时提供的 **Base directory** 路径）：

```bash
bash <Base directory>/setup-mcp.sh
```

脚本会自动检测 Qoder MCP 配置文件位置（兼容 macOS/Linux），若 `guoguo_send_server` 未配置则自动添加。配置完成后提示用户**刷新 MCP 连接或重启 Qoder** 以生效。

## 下单流程

### Step 1: 收集下单信息

向用户收集以下全部必要信息（可一次性询问，也可分步收集）：

| 信息项 | 说明 | 示例 |
|--------|------|------|
| 下单账号 | 用户手机号，同时作为 externalUserId 和 externalUserMobile | 13800138000 |
| 寄件人姓名 | senderInfo.name | 张三 |
| 寄件人电话 | senderInfo.mobile | 13800138000 |
| 寄件人地址 | senderInfo.fullAddressDetail，必须是完整地址（省市区+详细地址） | 西藏自治区阿里地区札达县托林镇丁丁卡牧场 |
| 收件人姓名 | receiverInfo.name | 李四 |
| 收件人电话 | receiverInfo.mobile | 13900139000 |
| 收件人地址 | receiverInfo.fullAddressDetail，必须是完整地址 | 浙江省杭州市余杭区文一西路969号 |
| 期望揽收开始时间 | appointGotStartTime，必须大于当前时间 | 2026-04-18 14:00 |

### Step 2: 构造请求参数

调用 MCP tool 时需传入两个参数：**request** 和 **accessOption**。

**request 参数模板：**

```json
{
    "externalUserId": "<下单账号>",
    "externalUserMobile": "<下单账号>",
    "itemId": 3000000040,
    "itemVersion": 4,
    "senderInfo": {
        "name": "<寄件人姓名>",
        "mobile": "<寄件人电话>",
        "fullAddressDetail": "<寄件人完整地址>"
    },
    "receiverInfo": {
        "name": "<收件人姓名>",
        "mobile": "<收件人电话>",
        "fullAddressDetail": "<收件人完整地址>"
    },
    "timeType": 2,
    "appointGotStartTime": "<期望揽收开始时间，毫秒时间戳>",
    "appointGotEndTime": "<appointGotStartTime + 7200000>",
    "outOrderInfoList": [],
    "designatedDeliveryUserId": null,
    "extensionMap": null,
    "userRemark": null,
    "externalUserType": 5
}
```

**关键计算规则：**
- `appointGotStartTime`：用户提供的揽收开始时间，转为**毫秒时间戳**
- `appointGotEndTime`：= appointGotStartTime + 7200000（即加 2 小时），此间隔由 itemId 决定，当前 3000000040 固定加 2 小时
- `appointGotStartTime` 必须大于当前时间，否则提示用户重新选择

**固定值映射表：**

| itemId | itemVersion | 服务类型 | 揽收时间间隔 |
|--------|-------------|----------|-------------|
| 3000000040 | 4 | 两小时服务 | +2小时 |

**accessOption 参数（固定值）：**

```json
{
    "accessCode": "示例",
    "accessMethod": null
}
```

### Step 3: 调用 MCP Tool 下单

调用 `guoguo_send_server` MCP 服务中的寄件下单 tool，传入上述 request 和 accessOption 两个参数。

### Step 4: 处理响应

**下单成功**（`result.success` 为 `"true"`）：

向用户展示以下信息：
- **寄件单号**：`result.data.orderId`
- **取件码**：`result.data.gotCode`
- **账号ID**：`result.data.cnAccountId`

成功响应示例：
```json
{
  "result": {
    "data": {
      "externalUserId": "2074370454",
      "orderId": "21240720002375404",
      "cnAccountId": "2074370454",
      "gotCode": "5617"
    },
    "success": "true"
  }
}
```

**下单失败**：

响应中会包含失败原因，提取并**明确告知用户失败原因**，方便排查。

## 注意事项

- 所有地址必须是**完整地址**（省/自治区+市/地区+区/县+详细地址）
- `externalUserId` 和 `externalUserMobile` 填写相同的用户手机号/账号
- 时间戳单位为**毫秒**
- 当前仅支持 itemId=3000000040（两小时服务），后续如有新商品可扩展固定值映射表
