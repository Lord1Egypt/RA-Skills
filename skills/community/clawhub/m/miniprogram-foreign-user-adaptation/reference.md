# 境外用户适配 -- 代码参考

本文档包含各适配维度的完整代码示例，供 AI 助手在给出具体修复方案时引用。

---

## 1. 账号体系代码示例

### 1.1 手机号快速验证组件（推荐方式）

```html
<!-- WXML -->
<button open-type="getPhoneNumber" bindgetphonenumber="onGetPhoneNumber">
  授权手机号
</button>
```

```javascript
// JS
Page({
  onGetPhoneNumber(e) {
    if (e.detail.errMsg === 'getPhoneNumber:ok') {
      const { code } = e.detail
      wx.request({
        url: 'https://api.yourapp.com/auth/phone',
        method: 'POST',
        data: { code },
        success(res) {
          // res.data.phoneNumber 格式："+8613800138000" 或 "+441234567890"
          console.log('手机号获取成功', res.data.phoneNumber)
        }
      })
    }
  }
})
```

### 1.2 自行搭建手机号验证码通道

```html
<!-- WXML：国际区号选择 + 手机号输入 -->
<view class="phone-input-container">
  <picker mode="selector" range="{{areaCodes}}" range-key="label" bindchange="onAreaCodeChange">
    <view class="area-code-picker">
      {{selectedAreaCode.label}}
    </view>
  </picker>
  <input
    type="text"
    placeholder="Enter phone number"
    maxlength="20"
    bindinput="onPhoneInput"
    value="{{phoneNumber}}"
  />
</view>
<button bindtap="sendVerifyCode" disabled="{{countdown > 0}}">
  {{countdown > 0 ? countdown + 's' : 'Send Code'}}
</button>
```

```javascript
Page({
  data: {
    areaCodes: [
      { code: '+86', label: '+86 China', minLen: 11, maxLen: 11 },
      { code: '+1', label: '+1 USA/Canada', minLen: 10, maxLen: 10 },
      { code: '+44', label: '+44 UK', minLen: 10, maxLen: 11 },
      { code: '+81', label: '+81 Japan', minLen: 10, maxLen: 11 },
      { code: '+82', label: '+82 South Korea', minLen: 10, maxLen: 11 },
      { code: '+66', label: '+66 Thailand', minLen: 9, maxLen: 10 },
      { code: '+65', label: '+65 Singapore', minLen: 8, maxLen: 8 },
      { code: '+60', label: '+60 Malaysia', minLen: 9, maxLen: 10 },
    ],
    selectedAreaCode: { code: '+86', label: '+86 China', minLen: 11, maxLen: 11 },
    phoneNumber: '',
    countdown: 0,
  },

  onAreaCodeChange(e) {
    const index = e.detail.value
    this.setData({ selectedAreaCode: this.data.areaCodes[index] })
  },

  onPhoneInput(e) {
    this.setData({ phoneNumber: e.detail.value })
  },

  validatePhone() {
    const { selectedAreaCode, phoneNumber } = this.data
    const digits = phoneNumber.replace(/\D/g, '')
    if (digits.length < selectedAreaCode.minLen || digits.length > selectedAreaCode.maxLen) {
      wx.showToast({
        title: `Phone number should be ${selectedAreaCode.minLen}-${selectedAreaCode.maxLen} digits`,
        icon: 'none'
      })
      return false
    }
    return true
  },

  async sendVerifyCode() {
    if (!this.validatePhone()) return
    const { selectedAreaCode, phoneNumber } = this.data
    const fullNumber = selectedAreaCode.code + phoneNumber
    wx.request({
      url: 'https://api.yourapp.com/sms/send',
      method: 'POST',
      data: { phone: fullNumber },
      success: () => {
        this.startCountdown()
        wx.showToast({ title: 'Code sent', icon: 'success' })
      },
      fail: () => {
        wx.showToast({ title: 'Failed to send, try email instead', icon: 'none' })
      }
    })
  },

  startCountdown() {
    this.setData({ countdown: 60 })
    const timer = setInterval(() => {
      if (this.data.countdown <= 1) {
        clearInterval(timer)
        this.setData({ countdown: 0 })
      } else {
        this.setData({ countdown: this.data.countdown - 1 })
      }
    }, 1000)
  }
})
```

### 1.3 服务端国际短信发送（Node.js + Twilio）

```javascript
const twilio = require('twilio')
const client = twilio(process.env.TWILIO_ACCOUNT_SID, process.env.TWILIO_AUTH_TOKEN)

async function sendInternationalSMS(phoneNumber, code) {
  try {
    const message = await client.messages.create({
      body: `Your verification code is: ${code}. Valid for 5 minutes.`,
      from: process.env.TWILIO_PHONE_NUMBER,
      to: phoneNumber  // 格式："+441234567890"
    })
    return { success: true, sid: message.sid }
  } catch (error) {
    console.error('SMS send failed:', error.message)
    return { success: false, error: error.message }
  }
}
```

### 1.4 邮箱验证入口

```html
<!-- WXML：邮箱验证入口 -->
<view class="auth-options">
  <button bindtap="switchToPhone" class="{{authMode === 'phone' ? 'active' : ''}}">
    Phone
  </button>
  <button bindtap="switchToEmail" class="{{authMode === 'email' ? 'active' : ''}}">
    Email
  </button>
</view>

<view wx:if="{{authMode === 'email'}}">
  <input
    type="text"
    placeholder="Enter your email"
    bindinput="onEmailInput"
    value="{{email}}"
  />
  <view class="code-row">
    <input
      type="number"
      placeholder="Verification code"
      maxlength="6"
      bindinput="onCodeInput"
      value="{{verifyCode}}"
    />
    <button bindtap="sendEmailCode" disabled="{{emailCountdown > 0}}">
      {{emailCountdown > 0 ? emailCountdown + 's' : 'Send Code'}}
    </button>
  </view>
  <button bindtap="verifyEmail" type="primary">Verify</button>
</view>
```

```javascript
Page({
  data: {
    authMode: 'phone',
    email: '',
    verifyCode: '',
    emailCountdown: 0,
  },

  switchToPhone() { this.setData({ authMode: 'phone' }) },
  switchToEmail() { this.setData({ authMode: 'email' }) },
  onEmailInput(e) { this.setData({ email: e.detail.value }) },
  onCodeInput(e) { this.setData({ verifyCode: e.detail.value }) },

  validateEmail() {
    const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/
    if (!emailRegex.test(this.data.email)) {
      wx.showToast({ title: 'Invalid email format', icon: 'none' })
      return false
    }
    return true
  },

  async sendEmailCode() {
    if (!this.validateEmail()) return
    wx.request({
      url: 'https://api.yourapp.com/email/send-code',
      method: 'POST',
      data: { email: this.data.email },
      success: () => {
        wx.showToast({ title: 'Code sent to your email', icon: 'success' })
        this.setData({ emailCountdown: 60 })
        const timer = setInterval(() => {
          if (this.data.emailCountdown <= 1) {
            clearInterval(timer)
            this.setData({ emailCountdown: 0 })
          } else {
            this.setData({ emailCountdown: this.data.emailCountdown - 1 })
          }
        }, 1000)
      }
    })
  },

  async verifyEmail() {
    wx.request({
      url: 'https://api.yourapp.com/email/verify',
      method: 'POST',
      data: { email: this.data.email, code: this.data.verifyCode },
      success(res) {
        if (res.data.success) {
          wx.showToast({ title: 'Verified', icon: 'success' })
        } else {
          wx.showToast({ title: 'Invalid code', icon: 'none' })
        }
      }
    })
  }
})
```

**参考官方文档**
- [手机号快速验证组件](https://developers.weixin.qq.com/miniprogram/dev/framework/open-ability/getPhoneNumber.html)

---

## 2. 信息录入代码示例

### 2.1 证件类型扩展

```html
<picker mode="selector" range="{{idTypes}}" range-key="label" bindchange="onIdTypeChange">
  <view class="picker-display">
    {{selectedIdType.label}}
  </view>
</picker>
<input
  type="text"
  placeholder="{{selectedIdType.placeholder}}"
  maxlength="{{selectedIdType.maxLen}}"
  bindinput="onIdNumberInput"
/>
```

```javascript
Page({
  data: {
    idTypes: [
      {
        value: 'id_card',
        label: 'Resident ID Card / 居民身份证',
        placeholder: 'Enter 18-digit ID number',
        maxLen: 18,
        regex: /^\d{17}[\dXx]$/
      },
      {
        value: 'passport',
        label: 'Passport / 护照',
        placeholder: 'Enter passport number',
        maxLen: 20,
        regex: /^[A-Za-z0-9]{5,20}$/
      },
      {
        value: 'foreigner_permanent',
        label: 'Foreigner Permanent Resident ID / 外国人永久居留身份证',
        placeholder: 'Enter permanent resident ID number',
        maxLen: 15,
        regex: /^[A-Za-z0-9]{15}$/
      },
      {
        value: 'hk_mo_tw',
        label: 'HK/Macau/Taiwan Travel Permit / 港澳台通行证',
        placeholder: 'Enter travel permit number',
        maxLen: 18,
        regex: /^[A-Za-z0-9]{6,18}$/
      }
    ],
    selectedIdType: null,
    idNumber: '',
  },

  onLoad() {
    this.setData({ selectedIdType: this.data.idTypes[0] })
  },

  onIdTypeChange(e) {
    const index = e.detail.value
    this.setData({
      selectedIdType: this.data.idTypes[index],
      idNumber: ''
    })
  },

  onIdNumberInput(e) {
    this.setData({ idNumber: e.detail.value })
  },

  validateIdNumber() {
    const { selectedIdType, idNumber } = this.data
    if (!selectedIdType.regex.test(idNumber)) {
      wx.showToast({
        title: `Invalid ${selectedIdType.label} number format`,
        icon: 'none'
      })
      return false
    }
    return true
  }
})
```

### 2.2 姓名输入规则放宽

```html
<view class="name-input-group">
  <view class="form-item">
    <text class="label">First Name</text>
    <input
      type="text"
      placeholder="e.g. John"
      maxlength="50"
      bindinput="onFirstNameInput"
    />
  </view>
  <view class="form-item">
    <text class="label">Last Name</text>
    <input
      type="text"
      placeholder="e.g. Smith"
      maxlength="50"
      bindinput="onLastNameInput"
    />
  </view>
</view>
```

```javascript
Page({
  validateName(name) {
    if (!name || name.trim().length === 0) {
      return { valid: false, msg: 'Name is required' }
    }
    if (name.length > 50) {
      return { valid: false, msg: 'Name is too long (max 50 characters)' }
    }
    const nameRegex = /^[\u4e00-\u9fa5A-Za-z\s\-'\.]+$/
    if (!nameRegex.test(name)) {
      return { valid: false, msg: 'Name contains invalid characters' }
    }
    return { valid: true }
  }
})
```

### 2.3 地址输入国际化

```html
<view class="address-section">
  <view wx:if="{{!isOverseas}}">
    <picker mode="region" bindchange="onRegionChange">
      <view>{{regionText || 'Select region'}}</view>
    </picker>
  </view>
  <view wx:else>
    <input
      type="text"
      placeholder="Address Line 1"
      maxlength="100"
      bindinput="onAddressLine1Input"
      value="{{addressLine1}}"
    />
    <input
      type="text"
      placeholder="Address Line 2 (optional)"
      maxlength="100"
      bindinput="onAddressLine2Input"
      value="{{addressLine2}}"
    />
    <view class="address-row">
      <input type="text" placeholder="City" bindinput="onCityInput" value="{{city}}" />
      <input type="text" placeholder="State / Province" bindinput="onStateInput" value="{{state}}" />
    </view>
    <view class="address-row">
      <input type="text" placeholder="Postal Code" bindinput="onPostalInput" value="{{postalCode}}" />
      <input type="text" placeholder="Country" bindinput="onCountryInput" value="{{country}}" />
    </view>
  </view>
</view>
```

**参考官方文档**
- [wx.getAppBaseInfo](https://developers.weixin.qq.com/miniprogram/dev/api/base/system/wx.getAppBaseInfo.html)

---

## 3. 多语言服务代码示例 (可选增强方案)

> 平台翻译已可用（零成本），以下自建 i18n 方案适合需要精确控制翻译质量的场景。

### 3.1 i18n 工具模块

```javascript
// utils/i18n.js
const languages = {
  'zh_CN': require('../locales/zh_CN.js'),
  'en': require('../locales/en.js'),
  'ja': require('../locales/ja.js'),
  'ko': require('../locales/ko.js'),
  'th': require('../locales/th.js'),
}

let currentLang = 'zh_CN'

function initLanguage() {
  const appBaseInfo = wx.getAppBaseInfo()
  const sysLang = appBaseInfo.language || 'zh_CN'
  const langMap = {
    'zh_CN': 'zh_CN',
    'zh_TW': 'zh_CN',
    'en': 'en',
    'ja': 'ja',
    'ko': 'ko',
    'th': 'th',
  }
  currentLang = langMap[sysLang] || 'en'
  return currentLang
}

function t(key, params = {}) {
  const keys = key.split('.')
  let result = languages[currentLang]
  for (const k of keys) {
    if (result && typeof result === 'object') {
      result = result[k]
    } else {
      result = undefined
      break
    }
  }
  if (result === undefined) {
    result = languages['en']
    for (const k of keys) {
      if (result && typeof result === 'object') {
        result = result[k]
      } else {
        result = key
        break
      }
    }
  }
  if (typeof result === 'string' && params) {
    Object.keys(params).forEach(param => {
      result = result.replace(new RegExp(`\\{${param}\\}`, 'g'), params[param])
    })
  }
  return result || key
}

function setLanguage(lang) {
  if (languages[lang]) {
    currentLang = lang
    return true
  }
  return false
}

function isChinese() {
  return currentLang === 'zh_CN'
}

module.exports = { initLanguage, t, setLanguage, isChinese, currentLang }
```

### 3.2 语言包示例

```javascript
// locales/zh_CN.js
module.exports = {
  common: { confirm: '确认', cancel: '取消', loading: '加载中...', retry: '重试' },
  auth: { phoneLogin: '手机号登录', emailLogin: '邮箱登录', sendCode: '发送验证码', enterPhone: '请输入手机号', enterEmail: '请输入邮箱' },
  home: { title: '首页', orderTicket: '购票', myOrders: '我的订单' }
}

// locales/en.js
module.exports = {
  common: { confirm: 'Confirm', cancel: 'Cancel', loading: 'Loading...', retry: 'Retry' },
  auth: { phoneLogin: 'Phone Login', emailLogin: 'Email Login', sendCode: 'Send Code', enterPhone: 'Enter phone number', enterEmail: 'Enter email' },
  home: { title: 'Home', orderTicket: 'Book Tickets', myOrders: 'My Orders' }
}
```

### 3.3 在 App 和页面中使用

```javascript
// app.js
const { initLanguage } = require('./utils/i18n')
App({
  onLaunch() {
    const lang = initLanguage()
    this.globalData.language = lang
  },
  globalData: { language: 'zh_CN' }
})

// pages/home/home.js
const { t, isChinese } = require('../../utils/i18n')
Page({
  data: { pageTitle: '', showMarketingBanner: true },
  onLoad() {
    this.setData({
      pageTitle: t('home.title'),
      showMarketingBanner: isChinese(),
    })
  }
})
```

### 3.4 custom-tab-bar 多语言

```javascript
// custom-tab-bar/index.js
const { t } = require('../utils/i18n')
Component({
  lifetimes: {
    ready() {
      this.setData({
        list: [
          { icon: 'home', value: 'home', label: t('tab.home') },
          { icon: 'chat', value: 'message', label: t('tab.message') },
          { icon: 'user', value: 'my', label: t('tab.my') },
        ]
      })
    }
  }
})
```

**参考官方文档**
- [小程序翻译能力](https://developers.weixin.qq.com/community/minihome/article/doc/000222bddd4e70130844a1db66b413)

---

## 4. 差异化 UI 代码示例

### 4.1 语言路由分流

```javascript
// utils/router.js
function isOverseasUser() {
  const appBaseInfo = wx.getAppBaseInfo()
  const language = appBaseInfo.language || 'zh_CN'
  const chineseLanguages = ['zh_CN', 'zh_TW', 'zh_HK']
  return !chineseLanguages.includes(language)
}

function navigateByLanguage(domesticPage, internationalPage) {
  const targetPage = isOverseasUser() ? internationalPage : domesticPage
  wx.navigateTo({ url: targetPage })
}

module.exports = { isOverseasUser, navigateByLanguage }
```

### 4.2 条件渲染

```html
<!-- 营销弹窗 - 仅国内用户展示 -->
<view class="marketing-popup" wx:if="{{!isOverseas && showPopup}}">
  <!-- 国内营销内容 -->
</view>

<!-- 核心服务入口 - 所有用户展示 -->
<view class="core-services">
  <view class="service-item" bindtap="goToTickets">
    <image src="/images/icon-ticket.png" />
    <text>{{t_orderTicket}}</text>
  </view>
  <view class="service-item" bindtap="goToMap">
    <image src="/images/icon-map.png" />
    <text>{{t_map}}</text>
  </view>
  <view class="service-item" bindtap="goToHelp">
    <image src="/images/icon-help.png" />
    <text>{{t_help}}</text>
  </view>
</view>

<!-- 积分任务 - 仅国内用户展示 -->
<view class="task-center" wx:if="{{!isOverseas}}">
  <!-- 积分任务内容 -->
</view>
```

```javascript
const { isOverseasUser } = require('../../utils/router')
const { t } = require('../../utils/i18n')

Page({
  data: {
    isOverseas: false,
    showPopup: true,
    t_orderTicket: '',
    t_map: '',
    t_help: '',
  },

  onLoad() {
    const overseas = isOverseasUser()
    this.setData({
      isOverseas: overseas,
      showPopup: !overseas,
      t_orderTicket: t('home.orderTicket'),
      t_map: t('home.map'),
      t_help: t('home.help'),
    })
  }
})
```

### 4.3 WXSS 排版适配

```css
/* 文本容器：弹性布局避免溢出 */
.text-container {
  display: flex;
  flex-wrap: wrap;
  word-break: break-word;
  overflow-wrap: break-word;
}

/* 按钮文本：预留宽度 */
.btn-text {
  min-width: 160rpx;
  padding: 0 24rpx;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* 标签类文本：自适应宽度 */
.tag {
  display: inline-block;
  padding: 8rpx 20rpx;
  max-width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* 列表项：文本区域弹性伸缩 */
.list-item {
  display: flex;
  align-items: center;
}
.list-item .label {
  flex-shrink: 0;
  width: 200rpx;
}
.list-item .value {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
}
```

**参考官方文档**
- [wx.getAppBaseInfo](https://developers.weixin.qq.com/miniprogram/dev/api/base/system/wx.getAppBaseInfo.html)

---

## 官方文档来源

- 手机号快速验证组件: https://developers.weixin.qq.com/miniprogram/dev/framework/open-ability/getPhoneNumber.html
- 小程序翻译能力: https://developers.weixin.qq.com/community/minihome/article/doc/000222bddd4e70130844a1db66b413
- wx.getAppBaseInfo: https://developers.weixin.qq.com/miniprogram/dev/api/base/system/wx.getAppBaseInfo.html
- 境外交流专区: https://developers.weixin.qq.com/community/minihome/mixflow/3721056300659130376
