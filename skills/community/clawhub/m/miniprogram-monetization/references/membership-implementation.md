# 会员系统实现方案

## 一、会员模式设计

### 1.1 订阅类型

| 类型 | 时长 | 定价建议 | 续费率预期 |
|------|------|----------|-----------|
| 周卡 | 7天 | ¥5-9 | 20-30% |
| 月卡 | 30天 | ¥19-39 | 40-50% |
| 季卡 | 90天 | ¥49-99 | 50-60% |
| 年卡 | 365天 | ¥99-299 | 60-80% |

### 1.2 权益分层

**金字塔模型：**

```
        ┌─────────┐
        │ 年度会员 │  最高权益
        ├─────────┤
        │ 季度会员 │  中等权益
        ├─────────┤
        │ 月度会员 │  基础权益
        ├─────────┤
        │ 免费用户 │  试用权益
        └─────────┘
```

---

## 二、数据库设计

### 2.1 表结构

```sql
-- 用户表
CREATE TABLE users (
  id INT PRIMARY KEY AUTO_INCREMENT,
  openid VARCHAR(64) UNIQUE NOT NULL,
  nickname VARCHAR(100),
  avatar_url VARCHAR(500),
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_openid (openid)
);

-- 会员套餐表
CREATE TABLE membership_plans (
  id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(50) NOT NULL,          -- '月卡', '季卡', '年卡'
  duration_days INT NOT NULL,         -- 30, 90, 365
  price DECIMAL(10,2) NOT NULL,       -- 价格
  original_price DECIMAL(10,2),       -- 原价
  description TEXT,                   -- 套餐描述
  features JSON,                      -- 权益列表
  is_active BOOLEAN DEFAULT true,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 会员订阅表
CREATE TABLE memberships (
  id INT PRIMARY KEY AUTO_INCREMENT,
  user_id INT NOT NULL,
  plan_id INT NOT NULL,
  order_id VARCHAR(64),               -- 关联订单
  status ENUM('active', 'expired', 'cancelled') DEFAULT 'active',
  start_time DATETIME NOT NULL,
  end_time DATETIME NOT NULL,
  auto_renew BOOLEAN DEFAULT false,   -- 是否自动续费
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id),
  FOREIGN KEY (plan_id) REFERENCES membership_plans(id),
  INDEX idx_user_status (user_id, status),
  INDEX idx_end_time (end_time)
);

-- 订阅记录表
CREATE TABLE subscription_logs (
  id INT PRIMARY KEY AUTO_INCREMENT,
  user_id INT NOT NULL,
  action ENUM('subscribe', 'renew', 'cancel', 'expire', 'upgrade', 'downgrade') NOT NULL,
  plan_id INT,
  old_plan_id INT,
  amount DECIMAL(10,2),
  remark TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_user_id (user_id),
  INDEX idx_created_at (created_at)
);
```

### 2.2 初始化套餐数据

```sql
INSERT INTO membership_plans (name, duration_days, price, original_price, features) VALUES
('月卡', 30, 29.00, 39.00, '["高级功能", "去广告", "专属客服"]'),
('季卡', 90, 69.00, 117.00, '["高级功能", "去广告", "专属客服", "数据导出"]'),
('年卡', 365, 199.00, 468.00, '["高级功能", "去广告", "专属客服", "数据导出", "优先更新", "一对一咨询"]');
```

---

## 三、核心功能实现

### 3.1 订阅会员

```javascript
// services/membership.js

class MembershipService {
  /**
   * 订阅会员
   */
  async subscribe(userId, planId, orderId) {
    const connection = await db.getConnection()
    
    try {
      await connection.beginTransaction()
      
      // 1. 获取套餐信息
      const [plan] = await connection.query(
        'SELECT * FROM membership_plans WHERE id = ? AND is_active = true',
        [planId]
      )
      
      if (!plan) {
        throw new Error('套餐不存在或已下架')
      }
      
      // 2. 检查是否有现有会员
      const [existing] = await connection.query(`
        SELECT * FROM memberships 
        WHERE user_id = ? AND status = 'active'
        FOR UPDATE
      `, [userId])
      
      // 3. 计算会员时间
      let startTime = new Date()
      let endTime = new Date()
      
      if (existing) {
        // 有现有会员，从现有结束时间开始续期
        startTime = new Date(existing.end_time)
        endTime = new Date(startTime)
        endTime.setDate(endTime.getDate() + plan.duration_days)
        
        // 升级套餐
        if (plan.duration_days > existing.plan_duration) {
          await connection.query(`
            UPDATE memberships SET status = 'cancelled' WHERE id = ?
          `, [existing.id])
        }
      } else {
        endTime.setDate(endTime.getDate() + plan.duration_days)
      }
      
      // 4. 创建会员记录
      const [result] = await connection.query(`
        INSERT INTO memberships 
        (user_id, plan_id, order_id, start_time, end_time)
        VALUES (?, ?, ?, ?, ?)
      `, [userId, planId, orderId, startTime, endTime])
      
      // 5. 记录日志
      await connection.query(`
        INSERT INTO subscription_logs 
        (user_id, action, plan_id, amount)
        VALUES (?, 'subscribe', ?, ?)
      `, [userId, planId, plan.price])
      
      await connection.commit()
      
      return {
        membershipId: result.insertId,
        startTime,
        endTime,
        plan: plan.name
      }
      
    } catch (error) {
      await connection.rollback()
      throw error
    } finally {
      connection.release()
    }
  }
  
  /**
   * 检查会员状态
   */
  async checkMembership(userId) {
    const [membership] = await db.query(`
      SELECT m.*, p.name as plan_name, p.features
      FROM memberships m
      JOIN membership_plans p ON m.plan_id = p.id
      WHERE m.user_id = ? AND m.status = 'active' AND m.end_time > NOW()
      ORDER BY m.end_time DESC
      LIMIT 1
    `, [userId])
    
    if (!membership) {
      return {
        isMember: false,
        plan: null,
        features: []
      }
    }
    
    return {
      isMember: true,
      plan: membership.plan_name,
      features: JSON.parse(membership.features),
      endTime: membership.end_time,
      daysRemaining: Math.ceil((new Date(membership.end_time) - new Date()) / (1000 * 60 * 60 * 24))
    }
  }
  
  /**
   * 取消自动续费
   */
  async cancelAutoRenew(userId) {
    await db.query(`
      UPDATE memberships 
      SET auto_renew = false 
      WHERE user_id = ? AND status = 'active'
    `, [userId])
  }
  
  /**
   * 处理过期会员
   */
  async processExpiredMemberships() {
    const expired = await db.query(`
      SELECT * FROM memberships 
      WHERE status = 'active' AND end_time <= NOW()
    `)
    
    for (const membership of expired) {
      await db.query(`
        UPDATE memberships SET status = 'expired' WHERE id = ?
      `, [membership.id])
      
      await db.query(`
        INSERT INTO subscription_logs 
        (user_id, action, plan_id)
        VALUES (?, 'expire', ?)
      `, [membership.user_id, membership.plan_id])
    }
    
    return expired.length
  }
}

module.exports = new MembershipService()
```

---

## 四、定时任务

### 4.1 检查过期会员

```javascript
// cron/membership-cron.js

const cron = require('node-cron')
const membershipService = require('../services/membership')

// 每天凌晨执行
cron.schedule('0 0 * * *', async () => {
  console.log('开始检查过期会员...')
  
  const count = await membershipService.processExpiredMemberships()
  
  console.log(`处理了 ${count} 个过期会员`)
})
```

### 4.2 会员到期提醒

```javascript
// 提前3天提醒
cron.schedule('0 9 * * *', async () => {
  const expiringSoon = await db.query(`
    SELECT m.*, u.openid 
    FROM memberships m
    JOIN users u ON m.user_id = u.id
    WHERE m.status = 'active' 
    AND m.end_time BETWEEN NOW() AND DATE_ADD(NOW(), INTERVAL 3 DAY)
    AND m.auto_renew = false
  `)
  
  for (const membership of expiringSoon) {
    // 发送订阅消息提醒
    await sendSubscribeMessage(membership.openid, {
      thing1: '会员即将到期',
      time2: membership.end_time.toLocaleDateString(),
      thing3: '点击续费享优惠'
    })
  }
})
```

---

## 五、前端实现

### 5.1 会员中心页面

```xml
<!-- pages/membership/index.wxml -->
<view class="membership-page">
  <!-- 会员状态 -->
  <view class="status-card">
    <view wx:if="{{isMember}}" class="member-info">
      <image src="/images/vip-badge.png" class="badge" />
      <text class="plan-name">{{membership.plan}}</text>
      <text class="expire">有效期至 {{membership.endTime}}</text>
      <text class="days">剩余 {{membership.daysRemaining}} 天</text>
    </view>
    <view wx:else class="non-member">
      <text class="title">开通会员</text>
      <text class="subtitle">解锁全部高级功能</text>
    </view>
  </view>
  
  <!-- 套餐选择 -->
  <view class="plans">
    <view 
      wx:for="{{plans}}" 
      wx:key="id"
      class="plan-item {{selectedPlanId === item.id ? 'active' : ''}}"
      bindtap="selectPlan"
      data-id="{{item.id}}"
    >
      <text class="name">{{item.name}}</text>
      <text class="price">¥{{item.price}}</text>
      <text class="original">原价 ¥{{item.original_price}}</text>
      <view class="features">
        <text wx:for="{{item.features}}" wx:key="*this">{{item}}</text>
      </view>
    </view>
  </view>
  
  <!-- 购买按钮 -->
  <button class="buy-btn" bindtap="handleBuy">
    立即开通 ¥{{selectedPlan.price}}
  </button>
  
  <!-- 权益说明 -->
  <view class="benefits">
    <text class="title">会员权益</text>
    <view class="benefit-item" wx:for="{{allBenefits}}" wx:key="*this">
      <icon type="success" />
      <text>{{item}}</text>
    </view>
  </view>
</view>
```

### 5.2 页面逻辑

```javascript
// pages/membership/index.js
Page({
  data: {
    isMember: false,
    membership: null,
    plans: [],
    selectedPlanId: null,
    selectedPlan: null
  },
  
  async onLoad() {
    await this.loadMembership()
    await this.loadPlans()
  },
  
  async loadMembership() {
    const res = await wx.request({
      url: 'https://yourdomain.com/api/membership/status'
    })
    
    this.setData({
      isMember: res.data.isMember,
      membership: res.data
    })
  },
  
  async loadPlans() {
    const res = await wx.request({
      url: 'https://yourdomain.com/api/membership/plans'
    })
    
    const plans = res.data.map(p => ({
      ...p,
      features: JSON.parse(p.features)
    }))
    
    this.setData({ 
      plans,
      selectedPlanId: plans[0].id,
      selectedPlan: plans[0]
    })
  },
  
  selectPlan(e) {
    const id = e.currentTarget.dataset.id
    const plan = this.data.plans.find(p => p.id === id)
    
    this.setData({
      selectedPlanId: id,
      selectedPlan: plan
    })
  },
  
  async handleBuy() {
    // 1. 创建订单
    const order = await wx.request({
      url: 'https://yourdomain.com/api/orders',
      method: 'POST',
      data: {
        type: 'membership',
        planId: this.data.selectedPlanId
      }
    })
    
    // 2. 发起支付
    const payParams = await wx.request({
      url: 'https://yourdomain.com/api/pay/params',
      method: 'POST',
      data: { orderId: order.data.id }
    })
    
    await wx.requestPayment(payParams.data)
    
    // 3. 支付成功
    wx.showToast({ title: '开通成功', icon: 'success' })
    
    setTimeout(() => {
      wx.redirectTo({ url: '/pages/membership/index' })
    }, 1500)
  }
})
```

---

## 六、续费与升级

### 6.1 续费逻辑

```javascript
async function renewMembership(userId, planId) {
  // 续费本质上是新订阅，时间从当前会员结束时间开始
  return await membershipService.subscribe(userId, planId, generateOrderId())
}
```

### 6.2 升级套餐

```javascript
async function upgradePlan(userId, newPlanId) {
  // 1. 计算当前会员剩余价值
  const current = await getCurrentMembership(userId)
  const remainingDays = Math.ceil((new Date(current.end_time) - new Date()) / (1000 * 60 * 60 * 24))
  const remainingValue = (current.price / current.duration_days) * remainingDays
  
  // 2. 计算升级差价
  const newPlan = await getPlan(newPlanId)
  const upgradePrice = newPlan.price - remainingValue
  
  // 3. 创建升级订单
  if (upgradePrice > 0) {
    return await createUpgradeOrder(userId, newPlanId, upgradePrice)
  } else {
    // 直接升级
    return await directUpgrade(userId, newPlanId)
  }
}
```

---

## 七、数据统计

### 7.1 关键指标

```sql
-- 会员总数
SELECT COUNT(*) FROM memberships WHERE status = 'active';

-- 本月新增会员
SELECT COUNT(*) FROM memberships 
WHERE status = 'active' AND created_at >= DATE_FORMAT(NOW(), '%Y-%m-01');

-- 会员收入
SELECT 
  DATE(created_at) as date,
  COUNT(*) as new_members,
  SUM(amount) as revenue
FROM subscription_logs
WHERE action IN ('subscribe', 'renew')
AND created_at >= DATE_SUB(NOW(), INTERVAL 30 DAY)
GROUP BY DATE(created_at);

-- 会员留存率（续费率）
SELECT 
  COUNT(CASE WHEN action = 'renew' THEN 1 END) / COUNT(*) as renewal_rate
FROM subscription_logs
WHERE action IN ('subscribe', 'renew');
```

---

*文档版本：v1.0*
*更新时间：2026-05-14*
