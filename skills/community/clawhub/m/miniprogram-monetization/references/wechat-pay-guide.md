# 微信支付接入详细教程

## 一、准备工作

### 1.1 必备条件

| 条件 | 说明 | 获取方式 |
|------|------|----------|
| 企业资质 | 营业执照/个体户执照 | 工商注册 |
| 已认证小程序 | 企业/个体户认证 | 微信公众平台 ¥300/年 |
| 商户号 | 微信支付商户号 | pay.weixin.qq.com 申请 |
| 服务器 | 公网可访问的服务器 | 云服务器 |

### 1.2 申请流程

```
第一步：申请商户号
├── 登录 pay.weixin.qq.com
├── 注册微信支付商户号
├── 提交企业资质审核（1-3天）
└── 绑定对公银行账户

第二步：开通JSAPI支付
├── 商户平台 → 产品中心
├── 我的产品 → 申请"JSAPI支付"
├── 填写应用场景
└── 等待审核（1-2天）

第三步：配置参数
├── 获取商户号(mch_id)
├── 设置API密钥（32位）
├── 下载支付证书
└── 配置支付回调域名
```

---

## 二、后端实现

### 2.1 环境配置

**依赖安装：**

```bash
npm install wechatpay-node-v3 axios
```

**配置文件：**

```javascript
// config/wechat-pay.js
module.exports = {
  appid: process.env.WX_APPID,           // 小程序AppID
  mchid: process.env.WX_MCHID,           // 商户号
  serial_no: process.env.WX_SERIAL_NO,   // 证书序列号
  privateKey: fs.readFileSync('./certs/apiclient_key.pem'), // 私钥
  apiv3_private_key: process.env.WX_APIV3_KEY, // APIv3密钥
  notify_url: 'https://yourdomain.com/api/pay/notify' // 回调地址
}
```

### 2.2 统一下单

```javascript
const { Wechatpay } = require('wechatpay-node-v3')
const pay = new Wechatpay(config)

// 创建订单
async function createOrder(orderId, amount, openid) {
  const result = await pay.transactions_jsapi({
    description: '商品描述',
    out_trade_no: orderId,
    amount: {
      total: amount, // 单位：分
      currency: 'CNY'
    },
    payer: {
      openid: openid
    },
    notify_url: config.notify_url
  })
  
  return result
}

// 获取支付参数（给前端用）
async function getPayParams(orderId, amount, openid) {
  const result = await createOrder(orderId, amount, openid)
  
  // 生成前端需要的参数
  const params = pay.getPayParamsByPrepayId(result.prepay_id)
  
  return {
    timeStamp: params.timeStamp,
    nonceStr: params.nonceStr,
    package: params.package,
    signType: params.signType,
    paySign: params.paySign
  }
}
```

### 2.3 支付回调

```javascript
// 支付结果通知
router.post('/api/pay/notify', async (req, res) => {
  try {
    // 1. 验签
    const signature = req.headers['wechatpay-signature']
    const timestamp = req.headers['wechatpay-timestamp']
    const nonce = req.headers['wechatpay-nonce']
    
    const verified = pay.verifySign({
      body: req.body,
      signature,
      timestamp,
      nonce
    })
    
    if (!verified) {
      return res.status(401).send('签名验证失败')
    }
    
    // 2. 解密数据
    const data = pay.decipher(req.body.resource)
    
    // 3. 更新订单状态
    const { out_trade_no, transaction_id } = data
    
    await db.query(`
      UPDATE orders 
      SET status = 'paid', 
          transaction_id = ?,
          paid_at = NOW()
      WHERE order_id = ?
    `, [transaction_id, out_trade_no])
    
    // 4. 返回成功
    res.json({ code: 'SUCCESS', message: '成功' })
    
  } catch (error) {
    console.error('支付回调错误:', error)
    res.status(500).send('失败')
  }
})
```

### 2.4 退款

```javascript
async function refund(orderId, refundAmount, reason) {
  const result = await pay.refunds({
    out_trade_no: orderId,
    out_refund_no: 'REFUND_' + Date.now(),
    amount: {
      refund: refundAmount,
      total: await getOrderTotal(orderId),
      currency: 'CNY'
    },
    reason: reason
  })
  
  return result
}
```

---

## 三、前端实现

### 3.1 发起支付

```javascript
// pages/pay/pay.js
Page({
  data: {
    order: null
  },
  
  // 创建订单并发起支付
  async handlePay() {
    wx.showLoading({ title: '支付中...' })
    
    try {
      // 1. 创建订单
      const order = await this.createOrder()
      
      // 2. 获取支付参数
      const payParams = await this.getPayParams(order.id)
      
      // 3. 调起微信支付
      await wx.requestPayment({
        timeStamp: payParams.timeStamp,
        nonceStr: payParams.nonceStr,
        package: payParams.package,
        signType: payParams.signType,
        paySign: payParams.paySign
      })
      
      // 4. 支付成功
      wx.hideLoading()
      wx.showToast({ title: '支付成功', icon: 'success' })
      
      // 5. 跳转到结果页
      wx.redirectTo({
        url: `/pages/pay-result/pay-result?orderId=${order.id}`
      })
      
    } catch (error) {
      wx.hideLoading()
      
      if (error.errMsg.includes('cancel')) {
        wx.showToast({ title: '已取消支付', icon: 'none' })
      } else {
        wx.showToast({ title: '支付失败', icon: 'error' })
      }
    }
  },
  
  // 创建订单
  async createOrder() {
    const res = await wx.request({
      url: 'https://yourdomain.com/api/orders',
      method: 'POST',
      data: {
        productId: this.data.productId,
        amount: this.data.amount
      }
    })
    return res.data
  },
  
  // 获取支付参数
  async getPayParams(orderId) {
    const res = await wx.request({
      url: 'https://yourdomain.com/api/pay/params',
      method: 'POST',
      data: { orderId }
    })
    return res.data
  }
})
```

### 3.2 支付结果页

```javascript
// pages/pay-result/pay-result.js
Page({
  onLoad(options) {
    const { orderId } = options
    this.checkPayStatus(orderId)
  },
  
  async checkPayStatus(orderId) {
    const res = await wx.request({
      url: `https://yourdomain.com/api/orders/${orderId}`
    })
    
    if (res.data.status === 'paid') {
      this.setData({ 
        status: 'success',
        order: res.data 
      })
    } else {
      // 支付处理中，轮询查询
      setTimeout(() => {
        this.checkPayStatus(orderId)
      }, 2000)
    }
  }
})
```

---

## 四、常见问题

### Q1：签名错误

**原因：**
- 参数顺序错误
- 编码问题（中文未转义）
- 密钥不正确

**解决：**
```javascript
// 使用官方SDK自动处理签名
const pay = new Wechatpay(config)
// 不要自己手动拼接签名字符串
```

### Q2：回调通知收不到

**检查清单：**
- [ ] 服务器公网可访问
- [ ] 回调URL是HTTPS
- [ ] 防火墙未拦截微信服务器IP
- [ ] 证书配置正确

### Q3：支付后订单状态未更新

**原因：**
- 回调未成功处理
- 数据库更新失败

**解决：**
```javascript
// 1. 主动查询订单状态
async function queryOrder(orderId) {
  const result = await pay.query({ out_trade_no: orderId })
  if (result.trade_state === 'SUCCESS') {
    // 更新订单
  }
}

// 2. 定时任务补偿
setInterval(async () => {
  const unpaidOrders = await db.query(`
    SELECT * FROM orders 
    WHERE status = 'pending' 
    AND created_at < DATE_SUB(NOW(), INTERVAL 5 MINUTE)
  `)
  
  for (const order of unpaidOrders) {
    await queryOrder(order.id)
  }
}, 60000) // 每分钟检查一次
```

---

## 五、安全建议

1. **敏感信息不要硬编码** — 使用环境变量
2. **证书文件安全存储** — 不提交到Git
3. **验证回调签名** — 防止伪造请求
4. **金额单位用分** — 避免浮点精度问题
5. **幂等处理** — 同一订单号多次回调只处理一次

---

## 六、测试

### 6.1 沙箱测试

```javascript
// 使用微信支付沙箱环境
const sandboxPay = new Wechatpay({
  ...config,
  base_url: 'https://api.mch.weixin.qq.com/sandboxnew'
})
```

### 6.2 测试账号

- 微信支付提供沙箱测试账号
- 可模拟支付成功/失败场景
- 测试通过后再切换正式环境

---

*文档版本：v1.0*
*更新时间：2026-05-14*
