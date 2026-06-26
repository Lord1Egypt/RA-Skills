---
name: pinduoduo-cs-assistant
slug: pinduoduo-cs-assistant-v2
version: 1.1.1
description: "拼多多商家客服自动化助手 - 基于 CDP (Chrome DevTools Protocol) 连接真实浏览器、自动登录拼多多商家后台、智能消息回复、售后处理。使用用户日常 Chrome，天然携带登录态，避免平台风控"
changelog: "v1.1.0: 添加 CDP Proxy 支持、完整的 Chrome 远程调试配置说明、CDB 数据库持久化、站点经验积累功能"
metadata: {"clawdbot":{"emoji":"🛒","requires":{"bins":["node"],"npm_deps":["ws","node-fetch"]},"os":["linux","darwin","win32"]}}
---

# 拼多多商家客服自动化助手

## 🎯 核心功能

### 1. 浏览器自动化登录
- ✅ 自动打开拼多多商家后台
- ✅ 扫码登录/账号密码登录
- ✅ Session 持久化（避免重复登录）
- ✅ 多店铺账号切换

### 2. 智能消息读取
- ✅ 实时监听买家咨询消息
- ✅ 未读消息自动提醒
- ✅ 消息内容提取（文本/图片/订单信息）
- ✅ 买家历史订单查询

### 3. 智能回复生成
- ✅ 基于上下文自动生成回复
- ✅ 话术库匹配（售前/售后/物流/退换货）
- ✅ 个性化回复（带买家昵称、订单信息）
- ✅ 表情包/图片自动匹配

### 4. 快捷回复发送
- ✅ 一键发送常用话术
- ✅ 自定义话术模板
- ✅ 批量回复（促销活动时）
- ✅ 发送记录追踪

### 5. 售后订单处理
- ✅ 退款申请自动读取
- ✅ 退换货工单处理
- ✅ 物流异常预警
- ✅ 差评预警与挽回

---

## 📋 使用命令

### 启动客服助手
```bash
# 启动浏览器并登录拼多多商家后台
node src/index.ts login --shop "店铺名称"

# 保持会话（监听新消息）
node src/index.ts listen --duration 3600
```

### 消息处理
```bash
# 读取未读消息
node src/index.ts messages --unread

# 回复指定买家
node src/index.ts reply --buyer-id "买家 ID" --message "回复内容"

# 智能回复（AI 生成）
node src/index.ts smart-reply --conversation-id "会话 ID"
```

### 话术管理
```bash
# 查看话术库
node src/index.ts templates --list

# 添加新话术
node src/index.ts templates --add --category "售前" --content "话术内容"

# 批量导入话术
node src/index.ts templates --import ./cs-templates.json
```

### 售后处理
```bash
# 查看待处理售后
node src/index.ts after-sales --pending

# 处理退款申请
node src/index.ts refund --order-id "订单号" --action "approve/reject"

# 物流查询
node src/index.ts logistics --order-id "订单号"
```

---

## 🔧 技术实现

### Browser 自动化流程

```typescript
// 1. 打开拼多多商家后台
browser.open("https://mms.pinduoduo.com")

// 2. 等待登录（扫码或账号密码）
browser.snapshot() // 获取登录页面状态

// 3. 检测登录状态
const isLoggedIn = await browser.evaluate(() => {
  return !!document.querySelector('.user-avatar')
})

// 4. 进入客服工作台
browser.act({
  kind: "click",
  ref: "客服工作台" // aria-ref
})

// 5. 监听消息
setInterval(async () => {
  const unreadMessages = await fetchUnreadMessages()
  if (unreadMessages.length > 0) {
    await handleMessages(unreadMessages)
  }
}, 5000) // 每 5 秒检查一次
```

### 智能回复逻辑

```typescript
// 话术匹配引擎
function matchTemplate(message: string, context: any): string {
  // 1. 意图识别
  const intent = classifyIntent(message)
  // 售前咨询、物流查询、退换货、产品质量、发票问题...
  
  // 2. 关键词匹配
  const keywords = extractKeywords(message)
  
  // 3. 从话术库匹配最佳回复
  const template = findBestMatch(intent, keywords)
  
  // 4. 填充个性化信息
  return fillTemplate(template, {
    buyerName: context.buyerName,
    productName: context.productName,
    logisticsInfo: context.logisticsInfo
  })
}
```

---

## 📁 话术库结构

### 售前咨询
```json
{
  "category": "售前",
  "templates": [
    {
      "keywords": ["有货吗", "还有货", "库存"],
      "response": "亲，这款商品目前有现货的哦，您可以直接下单~"
    },
    {
      "keywords": ["什么时候发货", "几天发"],
      "response": "亲，我们一般在下单后 24-48 小时内发货，节假日顺延~"
    },
    {
      "keywords": ["能便宜吗", "优惠", "打折"],
      "response": "亲，现在店铺有满减活动，满 XX 减 XX，很划算的哦~"
    }
  ]
}
```

### 物流查询
```json
{
  "category": "物流",
  "templates": [
    {
      "keywords": ["到哪了", "物流信息", "快递"],
      "response": "亲，帮您查了一下，您的包裹目前到达【{location}】，预计{days}天内送达~"
    },
    {
      "keywords": ["怎么还没到", "太慢了"],
      "response": "亲，非常理解您的心情，我帮您催一下快递公司，有进展马上通知您~"
    }
  ]
}
```

### 售后处理
```json
{
  "category": "售后",
  "templates": [
    {
      "keywords": ["退货", "退款", "不要了"],
      "response": "亲，支持 7 天无理由退换货的，您申请一下，我们马上处理~"
    },
    {
      "keywords": ["质量问题", "坏了", "破损"],
      "response": "亲，非常抱歉给您带来不好的体验，您拍个照片，我们给您补发/退款~"
    },
    {
      "keywords": ["差评", "投诉"],
      "response": "亲，真的非常抱歉，您有什么问题随时联系我们，一定给您满意解决方案~"
    }
  ]
}
```

---

## 🛡️ 安全与合规

**本系统严格遵守：**
1. **仅人工触发** - 所有操作需人工确认
2. **官方渠道** - 仅通过拼多多官方商家后台
3. **用户隐私** - 不存储买家敏感信息
4. **频率限制** - 避免频繁请求触发风控

**本系统不会：**
- ❌ 自动发送骚扰消息
- ❌ 批量刷单/刷好评
- ❌ 抓取非公开数据
- ❌ 绕过平台风控

---

## 🚀 快速开始

### 步骤 1：配置拼多多商家账号
```bash
# 编辑配置文件
vim scripts/config.json
```

```json
{
  "shops": [
    {
      "name": "店铺 A",
      "username": "商家账号",
      "password": "加密密码",
      "autoLogin": true
    }
  ]
}
```

### 步骤 2：启动客服助手
```bash
# 登录
node src/index.ts login --shop "店铺 A"

# 开始监听消息（后台运行）
nohup node src/index.ts listen --duration 86400 &
```

### 步骤 3：查看运行状态
```bash
# 查看今日接待数据
node src/index.ts stats --today

# 查看未读消息
node src/index.ts messages --unread
```

---

## 📊 数据看板

### 实时统计
- 今日接待买家数
- 平均响应时间
- 消息回复率
- 转化率（咨询→下单）

### 周/月报
- 客服工作量统计
- 常见问题 TOP10
- 售后率分析
- 买家满意度

---

## 🔌 扩展功能

### 1. 飞书集成
- 买家咨询消息推送到飞书群
- 售后工单自动创建飞书任务
- 数据报表自动同步飞书多维表格

### 2. 微信通知
- 重要买家消息微信提醒
- 售后预警微信推送

### 3. AI 智能回复
- 接入大模型生成个性化回复
- 自动学习历史优质回复话术
- 情感分析（识别买家情绪）

---

## 🐛 常见问题

### Q1: 登录失败怎么办？
**A:** 检查网络连接，尝试手动扫码登录。Session 过期需重新登录。

### Q2: 消息监听不工作？
**A:** 检查浏览器是否保持打开状态，确认客服工作台页面处于激活状态。

### Q3: 话术匹配不准确？
**A:** 优化话术库关键词，添加更多同义词和变体。

### Q4: 被平台风控限制？
**A:** 降低请求频率，避免短时间内大量操作，人工介入处理。

---

*🛒 拼多多客服自动化助手 — 7x24 小时智能值守，提升客服效率*
