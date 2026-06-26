---
name: seap-shopping
version: 1.0.0
trigger: "用户触发购买、帮我买、预约购买等厂家"
description: 用户在场/不在场购买skill
---

# SEAP Shopping Skill

这是一个用于处理购物需求的 skill，支持用户在场购买和不在场预约购买两种场景。

## 触发条件

当用户对话中包含"买"字时，自动触发此 skill。

## 配置文件

配置文件位于 `seap.config.json`，包含以下配置项：

```json
{
  "authCode": "your_auth_code_here",
  "addresses": [
    {
      "name": "收货人姓名",
      "phone": "135xxxxxxxx",
      "country": "CN",
      "province": "广东省",
      "city": "深圳市",
      "district": "龙岗区",
      "detail": "详细地址"
    }
  ],
  "autoPush": {
    "enabled": true,
    "channel": "webchat"
  }
}
```

- **authCode**: 用于调用云侧接口传输的凭证
- **addresses**: 收货地址列表，支持多个地址，每个地址包含姓名、电话、省市区及详细地址
- **autoPush**: 自动推送配置，启用购买结果自动通知

## 依赖工具

依赖 `scripts/seap-cli.js` 执行相关命令。技能可在普通环境中运行，无需acpx运行时。

## 命令行工具

### seap-cli.js 主要命令

- `search` - 搜索商品
- `aipay` - 执行购买（基于确认信息）

## 工作流程

执行命令进入skill目录
```bash
cd ~/.openclaw/workspace/skills/seap-shopping
```

### 场景一：用户在场购买

1. 用户发送对话，例如"我想买一瓶红酒"
2. 提取用户意图关键词原文为"queryGoodsIntention"，当前商品数量为"quantity"
3. 执行命令：
   ```bash
   node scripts/seap-cli search --sessionId=${openclaw当前sessionId} --intent=${queryGoodsIntention} --format md
   ```
4. **⚠️ 重要**：将查询后的 markdown 通过对话信息返回**所有**商品数据并按顺序标号，供用户进行选择
   - 必须显示搜索返回的全部商品，不得限制数量或只显示部分
   - 确保用户能看到所有可选商品
5. 用户对话确认指定序号商品后，读取 `${openclaw当前sessionId}.json` 文件对应序号的商品，获取商品 "skuId"，从mercInfo的id字段中获取"mercInfoId"
6. **地址确认对话**：
   - 系统自动从 `seap.config.json` 读取当前收货地址数据结构
   - 通过 OpenClaw 消息功能向用户显示当前地址："当前收货地址：[地址]，是否确认？(回复确认/修改：新地址)"
   - 用户确认地址或提供新地址
   - 如果用户修改地址，解析对应地址格式：'收货人姓名 收货人电话 国家 省份 市 区 详细地址'，解析后按对应数据结构更新 `seap.config.json` 文件
7. **购买确认**：
   - 生成确认文件 `${sessionId}_confirmed.json`，包含商品和确认后的地址信息
8. 执行购买命令：
   ```bash
   node scripts/seap-cli aipay --sessionId=${openclaw当前sessionId} --skuId=${skuId} --quantity=${quantity} --mercInfoId=${mercInfoId}
   ```
9. **文件清理**：
   - 购买成功后：自动清理 `${sessionId}_confirmed.json` 确认文件
   - 保留 `${sessionId}.json` 作为最终购买结果
10. 将购买后的结果信息返回给用户进行提示，根据 success 区分"购买成功"或"购买失败"

### 场景二：用户不在场购买

1. 用户发起预约购买:"三十分钟后帮我买一瓶红酒" 或 "1分钟后帮我买一瓶红酒"
  提取用户意图关键词原文为"queryGoodsIntention"，当前商品数量为"quantity"

2. 搜索商品:
   执行命令
   ```bash
   node scripts/seap-cli search --sessionId=${sessionId} --intent=${queryGoodsIntention} --format md
   ```

3. **⚠️ 重要用户选择商品**：将查询后的 markdown 通过对话信息返回**所有**商品数据并按顺序标号，供用户进行选择
   - 必须显示搜索返回的全部商品，不得限制数量或只显示部分
   - 确保用户能看到所有可选商品
   - 系统显示带序号的商品列表

4. 用户回复序号（如"1"）选择商品，系统读取 `${sessionId}.json` 文件获取对应商品信息，获取商品 "skuId"，从mercInfo的id字段中获取"mercInfoId"

5. **地址确认对话**：
   - 系统自动从 `seap.config.json` 读取当前收货地址数据结构
   - 通过 OpenClaw 消息功能向用户显示当前地址："当前收货地址：[地址]，是否确认？(回复确认/修改：新地址)"
   - 用户确认地址或提供新地址
   - 如果用户修改地址，解析对应地址格式：'收货人姓名 收货人电话 国家 省份 市 区 详细地址'，解析后按对应数据结构更新 `seap.config.json` 文件

6. **购买确认**：
   - 生成确认文件 `${sessionId}_confirmed.json`，包含商品和确认后的地址信息

7. **🔧 购买时间确认**
   # 步骤1：确认购买时间
   系统解析用户原始时间表达式（如"1分钟后"）
   计算确切的执行时间戳

   # 步骤2：发送确认消息
   "⏰ **购买时间确认**

   您选择的商品：[商品名称]
   预计购买时间：[时间表达式] (约[具体时间])

   请确认是否继续预约购买：
   - 确认预约购买
   - 或者修改购买时间
   - 或者取消购买"

   # 步骤3：等待用户确认
   用户回复确认、修改时间或取消

   # 步骤4：处理用户选择
   - 确认：创建定时任务，系统将在指定时间自动购买
   - 修改：重新开始预约流程
   - 取消：清理临时文件，结束流程

8. **🔧 创建定时购买任务**
   系统解析用户原始时间表达式（如"1分钟后"）计算确切的执行时间戳，自动创建 OpenClaw cron 任务
   任务配置：
   {
     "name": "预约购买 - [商品名称]",
     "schedule": {
       "kind": "at",
       "at": "[ISO格式的执行时间]"
     },
     "payload": {
       "kind": "agentTurn",
       "message": "你正在执行一个定时购买任务。

   任务信息：
   - 商品SKU: ${skuId}
   - 原始会话: ${原sessionKey}

   请按以下步骤完成购买并推送结果：

   1. 执行购买命令：
      node scripts/seap-cli aipay --sessionId=${原sessionKey} --skuId=${skuId} --quantity=${quantity} --mercInfoId=${mercInfoId}
   2. 读取购买结果：
      从 ${原sessionKey}.json 文件读取购买结果

   3. 推送结果到原会话：
      使用 sessions_send 将购买结果发送到原始会话

   4. 清理临时文件（如果有）",
       "timeoutSeconds": 120
     },
     "sessionTarget": "current",
     "deleteAfterRun": true,
     "delivery": {
       "mode": "announce"
     }
   }

   # ⚠️ 重要说明：
   # 1. delivery.mode 必须设置为 "announce" 或 "webhook" 以便推送结果
   # 2. payload 中的 message 必须包含完整的结果推送逻辑
   # 3. 必须使用 sessions_send 工具将结果推送到原会话

9.提示用户任务已创建
   "✅ 预约购买任务已创建！

   📦 **商品信息**
   - 名称：[商品名称]
   - 价格：¥[价格]
   - SKU：[SKU]

   📍 **收货地址**
   [收货地址]

   ⏰ **执行时间**
   [时间表达式] (约[具体时间])

   系统将在指定时间自动执行购买，并将结果通知您。"
   ```

10. **定时任务自动执行**
   - 到达指定时间后，OpenClaw自动在当前会话中执行任务
   - Agent在当前会话中执行购买命令（使用 aipay）
   - Agent读取购买结果（从 ${sessionKey}.json）

11. **🔧 购买结果自动推送（Agent在当前会话中执行）**
   由于使用 sessionTarget="current"，购买结果会自动显示在当前会话
   无需手动使用 sessions_send 推送结果
   Agent只需执行购买命令，结果会自动呈现给用户

   # 步骤1：定时任务触发购买
   系统自动执行执行命令
   ```bash
   node scripts/seap-cli aipay --sessionId=${原sessionKey} --skuId=${skuId} --quantity=${quantity} --mercInfoId=${mercInfoId}
   ```

   # 步骤2：生成完整购买结果
   {
    "sessionId": "${sessionId}",
    "skuId": "[商品SKU]",
    "productName": "[商品名称]",
    "productPrice": [价格],
    "orderId": "[生成的订单号]",
    "success": [布尔值],
    "address": "[收货地址]",
    "executedAt": "[执行时间]",
    "executionType": "scheduled"
   }

   # 步骤3：保存购买结果
   更新 ${sessionId}.json 文件，包含完整的购买信息

   # 步骤4：自动生成结果消息
   生成用户友好的通知消息：
   "✅ 预约购买任务已完成！

   📦 **商品信息**
   - 名称：[商品名称]
   - 价格：¥[价格]
   - SKU：[SKU]

   📋 **订单信息**
   - 订单号：[订单号]
   - 状态：[成功/失败]

   📍 **收货地址**
   [收货地址]

   ⏰ **完成时间**
   [完成时间]

   💡 这是您的预约购买结果。"

   # 步骤5：推送结果至原会话
   使用 sessions_send 将结果发送到用户的原始会话
   确保用户能够立即收到购买完成通知

   # 步骤7：清理临时文件
   购买完成后清理临时文件：
   - 删除 ${sessionId}_task.json
   - 删除 ${sessionId}_confirmed.json
   - 保留 ${sessionId}.json 作为购买记录


#### 📊 **状态管理**

- **${sessionId}.json** - 保存搜索结果和最终购买结果
- **${sessionId}_confirmed.json** - 临时保存购买确认信息（执行后清理）
- **${sessionId}_cron.json** - 保存定时任务配置（执行后清理）
- **${sessionId}_task.json** - 保存预约购买任务配置（执行后清理）

#### ✅ **预期效果**

1. **无缝体验**：用户确认购买后，系统自动处理后续所有流程
2. **准时执行**：定时任务确保在指定时间自动执行购买
3. **实时通知**：购买完成后立即推送详细结果
4. **可靠管理**：完整的任务生命周期和错误处理机制  