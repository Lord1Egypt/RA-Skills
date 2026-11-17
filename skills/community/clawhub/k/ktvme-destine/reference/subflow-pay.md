# 支付子流程（subflow-pay）

> 📖 **API 详细定义**：详见 [api-order.md](./api-order.md) 的 `roomHourCreateOrder` 返回字段
>
> 📖 **通用约束**：详见 [api-overview.md](./api-overview.md)

---

## 调用时机

在以下场景中，主技能应调用本子流程：

- **订单创建成功后**：`roomHourCreateOrder` 成功返回 `payment_link` / `qr_code` / `expire_time`
- **用户未在有效期内完成支付，要求重新支付时**：需重新查询时段并下单（详见下方「超时重新支付」）


---

## 完整流程

```
┌─ 支付流程 ──────────────────────────────────────┐
│                                                   │
│  Step 1: 接收 roomHourCreateOrder 返回的支付信息  │
│          （operate_id / payment_link / qr_code /  │
│           expire_time）                           │
│     ↓                                             │
│  Step 2: 向用户展示支付二维码（≤ 200×200）+        │
│          支付链接 + 订单号 + 有效期                │
│     ↓                                             │
│  Step 3: 启动后台轮询（自动）                     │
│          python scripts/poll_order_status.py <id>  │
│          每 5 秒查询，最长 6 分钟                  │
│     ↓                                             │
│  Step 4: 读取轮询结果                             │
│          ✅ poll_status=paid → 展示预约成功页     │
│          ⏰ poll_status=timeout → 提示超时重下单   │
│                                                   │
└───────────────────────────────────────────────────┘
```

---

## 详细步骤说明

### Step 1: 接收支付信息

`roomHourCreateOrder` 成功后**直接返回**以下字段，无需再调用任何支付接口：

| 字段              | 类型   | 说明                                                       |
| ----------------- | ------ | ---------------------------------------------------------- |
| `operate_id`      | String | 订单号                                                     |
| `payment_link`    | String | 支付url，直接展示成超链接，点击去支付，必须展示             |
| `qr_code`         | String | 支付二维码图片 URL，直接用预览面板在线展示，不要下载，用 `present_files` 展示即可扫码    |
| `expire_time`     | String | 有效期（yyyy-MM-dd HH:mm:ss），锁定包厢时间 + 支付时间     |

> ⚠️ `expire_time` 既是锁定包厢的时间，也是支付时间，**超出则无法下单**。

### Step 2: 向用户展示支付二维码并引导操作

**展示规范**：

1. **支付二维码图片 URL，直接用预览面板在线展示，不要下载，用 `present_files` 展示即可扫码
2. **二维码尺寸最多 200×200**，避免过大影响阅读
3. 同时展示支付链接（必须展示）、订单号、有效期
4. 二维码不可用时，引导用户点击 `payment_link`扫码支付

**推荐输出话术**：

```
✅ 下单成功！请扫码完成支付

![支付二维码](data.qr_code)   <!-- 尺寸控制在 200×200 以内 -->

🔗 支付链接（必须展示）：
   {data.payment_link}

📋 订单号：{data.operate_id}
⏰ 支付有效期：{data.expire_time}

正在为您监控支付状态，请在有效期内完成支付...
```

### Step 3: 启动后台轮询

二维码展示后，**立即启动后台轮询脚本**：

```bash
# 必须传 run_in_background=true，记下返回的 task_id
python3 scripts/poll_order_status.py <operate_id>
```

**轮询配置**：
- 轮询间隔：**5 秒**
- 最长时长：**6 分钟**（72 次）
- 成功判定：订单 `status` ∈ `{1, 2, 3, 4}`

**轮询结果输出**：脚本执行完毕后，将结果写入 `/tmp/poll_result_{order_id}.json`

```json
// 成功支付
{
  "poll_status": "paid",
  "order_id": "7608052439251950",
  "message": "订单已支付，预约成功",
  "elapsed_seconds": 12
}

// 超时未支付
{
  "poll_status": "timeout",
  "order_id": "7608052439251950",
  "message": "订单已超时未支付，请重新下单",
  "elapsed_seconds": 360
}
```

### Step 4: 阻塞等待轮询结果并处理

> ⚠️ **【强制】Agent 必须用 `TaskOutput(block=true)` 阻塞等待后台轮询任务完成，收到系统通知后再继续处理。在收到结果前，会话不得结束！**

**操作流程**：

1. 用 `TaskOutput(block=true, task_id=<Step 3 返回的 task_id>)` 等待脚本完成
2. 系统会在轮询脚本退出（paid 或 timeout）时自动通知 Agent
3. Agent 收到通知后，Read `/tmp/poll_result_{order_id}.json`
4. 根据 `poll_status` 处理：

#### ✅ `poll_status = paid` → 展示预约成功页

```
✅ 支付成功！预约已确认

📋 订单号：{operate_id}
👤 预订人：{guest_name}
🎁 套餐：{buy_break_name}
⏰ 时段：{used_date} {used_begin_time} - {used_end_time}
💰 金额：¥{charge}

请按时到店，期待您的光临！
```

> 💡 **字段说明**：展示字段来自 `getOrderDetail` 接口返回，详见 [api-order.md](./api-order.md#getorderdetail---查询订单详情)

#### ⏰ `poll_status = timeout` → 展示超时提示

```
⏰ 订单已超时未支付

很遗憾，您的订单已超过支付时限，包厢已自动释放。
请重新选择时段下单，感谢您的理解。

[返回 Step 4: queryRoomAvailability]
```

---

## 超时重新支付（强制约束）

> ⚠️ **【重要】支付超时由 Step 4 的 Agent 阻塞等待 + 结果读取自动处理**。

**超时自动触发**：

```
poll_order_status.py 运行 6 分钟后仍未检测到支付
    ↓
写入 /tmp/poll_result_{order_id}.json（poll_status=timeout）
    ↓
Agent 读取结果，展示超时提示
    ↓
自动返回 Step 4: queryRoomAvailability 重新查时段
```

**手动超时处理**（用户主动反馈"重新支付"）：

如果轮询脚本未运行或异常，用户反馈"支付过期了"/"重新支付"时：

1. 重新调用 `queryRoomAvailability` 查询当前可选时段（原时段可能已被他人预订或释放）
2. 按「可预订时段展示规范」重新展示可预订时段供用户选择
3. 用户选定后调用 `roomHourCreateOrder` 创建新订单
4. 展示新的支付二维码并启动新的轮询

> ❌ **禁止直接重新下单**：超时后必须先 `queryRoomAvailability` 重新查询时段，禁止直接用原订单信息调用 `roomHourCreateOrder`。

---

## 异常处理

| 场景                       | 处理策略                                                                |
| -------------------------- | ----------------------------------------------------------------------- |
| `roomHourCreateOrder` 失败 | 根据错误信息判断原因（如时段已被预订），向用户说明并引导更换时段/包厢   |
| 二维码无法展示             | 引导用户点击 `payment_link`扫码支付                     |
| 用户反馈链接打不开         | 让用户确认是否点击链接；若链接过期则按「超时重新支付」处理   |
| 支付超时（超过 expire_time）| 按「超时重新支付」流程：重新查询时段 → 用户重选 → 创建新订单            |
| 用户要求取消订单/退款       | 先确认取消意图 → 调用 `cancelBookOrder(opid)` → 告知取消成功与退款到账时间 |
| 订单时间冲突/需更换门店    | 调用 `cancelBookOrder(opid)` 取消原订单 → 重新查询时段 → 创建新订单     |
| 用户询问支付状态           | 引导用户以支付页面/收银台提示为准，或联系门店确认                       |

---

## 注意事项

1. **下单即得支付信息**：`roomHourCreateOrder` 成功后直接返回 `payment_link` / `qr_code` / `expire_time`
2. **二维码尺寸限制**：展示给用户的二维码**最多 200×200**
3. **有效期即锁房时间**：`expire_time` 同时是锁定包厢时间和支付时间，超出无法下单
4. **轮询必须阻塞等待**：展示二维码后用 `Bash(run_in_background=true)` 启动 `poll_order_status.py`，**必须**立即用 `TaskOutput(block=true)` 阻塞等待脚本完成，**在收到支付结果前会话不得结束**
5. **轮询结果读取**：收到 TaskOutput 通知后，Read `/tmp/poll_result_{order_id}.json`，`poll_status=paid` 展示成功页，`poll_status=timeout` 提示超时
6. **取消订单走 cancelBookOrder**：用户要求取消/退款或更换门店/时间时，**先调用 `cancelBookOrder`**，再按新条件查询时段下单
7. **取消需前置确认**：已支付订单取消需先向用户确认意图，避免误操作
8. **支付方式**：引导用户**扫码**或**点击 `payment_link`** 扫码支付
9. **支付前最终确认**：展示二维码前可复述订单关键信息（金额、时段、包厢）供用户确认
