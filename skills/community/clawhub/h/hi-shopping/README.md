# SEAP Shopping Skill

这是一个用于 OpenClaw 的购物 skill，支持用户在场购买和不在场预约购买两种场景。

## 功能特性

- 🛒 **在场购买**：用户直接选择商品并立即购买
- ⏰ **预约购买**：用户设置定时任务，在指定时间自动购买
- 📋 **商品搜索**：基于用户意图搜索相关商品
- 🔢 **序号选择**：通过序号快速选择商品
- 💾 **状态管理**：自动维护购物会话状态

## 安装步骤
1. 确保 skill 文件已放置在正确位置：
   ```
   ~/.openclaw/skills/seap-shopping/
   ├── SKILL.md
   ├── seap.config.json
   ├── index.ts
   ├── README.md
   └── scripts/
       ├── seap-cli.ts     # TypeScript CLI 源码
       └── seap-cli.js     # 编译后的JavaScript
   ```

2. 配置 `seap.config.json`：
   ```json
   {
     "authCode": "your_auth_code_here",
     "secretToken": "your_secret_token_here",
     "address": "your_delivery_address_here"
   }
   ```

## 使用方法

### 触发条件

当用户消息中包含"买"字时，此 skill 会自动触发。

### 在场购买流程

1. **用户输入**：
   ```
   我想买一瓶红酒
   ```

2. **系统响应**：
   ```
   # 商品搜索结果

   1. **拉菲红酒2015**
      - SKU: SKU001
      - 价格: ¥899
      - 描述: 法国波尔多产区红酒
      - 评分: 4.8/5.0
      - 店铺: 红酒专营店

   2. **奔富红酒**
      - SKU: SKU002
      - 价格: ¥599
      - 描述: 澳大利亚进口红酒
      - 评分: 4.6/5.0
      - 店铺: 进口食品店
   ...
   n. **XXX**
      - SKU: XXX
      - 价格: XXX
      - 描述: XXXX
      - 评分: 4.6/5.0
      - 店铺: XXXX
   请选择你想要购买的商品序号（1-n）：
   ```

3. **用户确认**：
   ```
   1
   ```

4. **购买结果**：
   ```
   ✅ 购买成功！

   订单号：ORDER123456

   商品将发送至：北京市朝阳区xxx
   ```

### 预约购买流程

1. **用户输入**：
   ```
   三十分钟后帮我买一瓶红酒
   ```

2. **系统响应**（同在场购买的商品选择）

3. **用户确认**：
   ```
   1
   ```

4. **任务创建确认**：
   ```
   ✅ 已创建预约购买任务！

   任务 ID：cron_job_123
   执行时间：30分钟后

   到时会自动为你购买 "拉菲红酒2015"，并将发送至：北京市朝阳区xxx
   ```

5. **任务完成通知**：
   ```
   预约购买任务已完成！

   ✅ 购买成功！
   订单号：ORDER123456
   商品将发送至：北京市朝阳区xxx
   ```

## 文件结构

```
seap-shopping/
├── SKILL.md              # Skill 说明文档
├── seap.config.json      # 配置文件
├── hubAgentApi.md        # API 接口定义
├── index.ts              # 主逻辑实现
├── README.md             # 使用说明
└── ${sessionId}_state.json  # 临时状态文件（运行时生成）
└── ${sessionId}.json     # 搜索结果缓存（运行时生成）
└── scripts/
    ├── seap-cli.ts     # TypeScript CLI 源码
    └── seap-cli.js     # 编译后的JavaScript
```

## API 依赖

此 skill 依赖以下命令行工具：

- **search 命令**：商品搜索
  ```bash
  node scripts/seap-cli.js search --sessionId=${sessionId} --intent=${intent} --format md
  ```

- **aipay 命令**：购买执行
  ```bash
  node scripts/seap-cli.js aipay --sessionId=${sessionId} --skuId=${skuId}
  ```

## 配置说明

### seap.config.json

```json
{
  "authCode": "your_auth_code_here",      // 云侧接口认证凭证
  "secretToken": "your_secret_token_here", // 支付令牌（用于预约购买）
  "address": "your_delivery_address_here"  // 收货地址
}
```

## 状态管理

Skill 使用 JSON 文件维护会话状态：

- **文件位置**：`${skill_path}/${sessionId}_state.json`
- **状态结构**：
  ```json
  {
    "sessionId": "string",
    "mode": "present|absent",
    "intent": "string",
    "cron": "string (optional)",
    "selectedSkuId": "string (optional)",
    "currentStep": "idle|searching|selecting|buying|completed",
    "searchResults": []
  }
  ```

## 错误处理

Skill 会在以下情况下返回错误信息：

1. 商品搜索失败
2. 用户输入无效的序号
3. 购买接口调用失败
4. 定时任务创建失败

## 注意事项

1. 确保 `seap-cli.js` 文件存在且可执行
2. 配置文件必须填写正确的认证信息
3. 预约购买功能需要 OpenClaw 的 cron 工具支持
4. 状态文件会自动清理，但也可以手动删除以重置会话

## 扩展功能

### 时间表达式解析

当前的时间解析较为简化，可以扩展支持更复杂的时间表达式：

- "明天上午10点"
- "下周三晚上"
- "2024年4月1日"

### 支付方式扩展

可以扩展支持多种支付方式，配置结构可以改为：

```json
{
  "paymentMethods": [
    {
      "type": "alipay",
      "token": "alipay_token"
    },
    {
      "type": "wechat",
      "token": "wechat_token"
    }
  ]
}
```

## 测试

可以手动测试 skill 功能：

```bash
# 测试搜索命令
node scripts/seap-cli.js search --sessionId=test_session --intent="红酒" --format md

# 测试购买命令
node scripts/seap-cli.js aipay --sessionId=test_session --skuId=SKU001
```

## 常见问题

**Q: 购买失败怎么办？**
A: 检查网络连接、配置文件中的认证信息，以及商品 skuId 是否正确。

**Q: 预约购买任务没有执行？**
A: 确保 OpenClaw 的 cron 服务正常运行，并且 cron 表达式格式正确。

**Q: 如何取消预约购买？**
A: 当前版本暂不支持取消功能，可以通过删除定时任务手动取消。