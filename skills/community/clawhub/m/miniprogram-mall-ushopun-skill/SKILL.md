---
name: "miniprogram-mall-ushopun-official"
description: "基于 Ushopun（优社云AI）官方 miniProgramV2 真实项目构建的微信小程序商城前端，覆盖首页、分类、商品详情、购物车、结算、订单、个人中心等 50+ 页面与完整交易链路。内置 dev.ushopun.com OpenAPI（接口前缀 /api/v2，返回体 code/content/data，guid/token/shopId 鉴权）完整接口对接规范与每个方法的调用示例。当用户需要开发对接 Ushopun 后端（优社云）的微信小程序商城时调用此 Skill。后端接口文档参考同目录 openapi.json（#File ./openapi.json，servers 为 {tenant}.ushopun.com 泛域名模板，开发填 dev，正式替换租户子域名）。"
---

# 微信小程序商城 Ushopun（优社云 V2）开发规范

> **本 Skill 定位**：微信小程序**商城**前端开发工具，基于 Ushopun 官方 `miniProgramV2` 真实项目提炼，聚焦「首页 → 分类 → 详情 → 购物车 → 结算 → 订单 → 个人中心」完整交易闭环，并原生对接 Ushopun 后端 OpenAPI。
>
> **后端数据源**：`dev.ushopun.com`（优社云 OpenAPI，`openapi.json` 为接口权威文档）。接口前缀统一为 `/api/v2`，返回体统一为 `{ code, content, data, success }`，鉴权通过请求头 `guid`（用户 GUID）+ `authorization`（JWT Token）+ `shopId`（店铺/自提点）完成。
>
> **示例站点**：正式对接前，请先在 `https://dev.ushopun.com` 示例站点 / 后台开通对应模块并确认接口可达（域名、鉴权、模块开关）。本 Skill 不负责引导付款，付款与账号开通请直接联系优社云AI官方。
>
> **连接器 ApiToken（Agent 前置授权）**：本 Skill 被 workbuddy / trae 等 AI Agent 使用时，Agent 需先引导用户到 `ushopun.com` 登录账号 → 在后台/控制台创建连接器并复制「连接器 ApiToken」→ 提供给 Agent，用于读取接口文档、验证字段或联调。该凭证为租户级敏感凭证，禁止写死进生成的小程序源码，仅通过配置占位符/环境变量承载。

---

## 技术栈

- **框架**：原生微信小程序（不使用 Taro / uni-app）
- **API 层**：自封装请求模块（`api/api.js` + `api/conf.js`）
- **鉴权**：Header 携带 `guid`（用户标识）+ `authorization`（JWT Token）+ `shopId`（店铺/自提点）
- **样式**：WXSS，尺寸单位 `rpx`（750rpx = 屏幕宽度），图标用 iconfont
- **富文本**：wxParse 组件（商品详情 `full` 字段 HTML 渲染）
- **主题色**：`#950000`（Ushopun 品牌深红），导航栏白字标题「Ushopun商城」

## 项目目录结构（miniProgramV2）

```
miniProgramV2/
├── api/
│   ├── conf.js          # 所有 API 端点常量（统一管理，禁止硬编码 URL）
│   └── api.js           # HTTP 请求封装（自动注入 guid/token/shopId）
├── pages/               # 业务页面（每页 .js/.wxml/.wxss/.json 四件套）
│   ├── index/           # 首页（轮播、分类入口、热卖推荐、优惠券弹窗）
│   ├── category/        # 一级分类 + 二级分类
│   ├── subcategory/     # 分类商品列表（触底加载）
│   ├── detail/          # 商品详情（SKU 联动、收藏、加购、立即购买）
│   ├── search/          # 搜索
│   ├── cart/            # 购物车（全选/单选、数量加减、结算）
│   ├── checkout/        # 结算/提交订单（地址、优惠券、支付方式）
│   ├── checkoutdetail/  # 订单详情
│   ├── order/           # 订单（分状态）
│   ├── orderList/       # 订单列表（Tab 切换）
│   ├── payFinish/       # 支付成功
│   ├── my/              # 个人中心
│   ├── login/           # 账号密码登录
│   ├── souquan/         # 微信授权登录引导
│   ├── address/         # 地址管理
│   ├── address-edit/    # 地址编辑
│   ├── collect/         # 收藏夹
│   ├── comment/         # 商品评价
│   ├── commentDetail/   # 评价详情
│   ├── mycomment/       # 我的评价
│   ├── available_coupon/  # 可用优惠券
│   ├── youhuijuan/      # 优惠券中心
│   ├── usedcunpond/     # 优惠券（已使用）
│   ├── point/           # 积分
│   ├── recharge/        # 充值
│   ├── rechargeList/    # 充值记录
│   ├── cashout/         # 提现
│   ├── distribution/    # 分销中心
│   ├── dividend/        # 分红明细
│   ├── bonusDetail/     # 奖金明细
│   ├── myCustomer/      # 我的客户
│   ├── myinvitre/       # 我的邀请
│   ├── partner/         # 合伙人
│   ├── saleOrder/       # 销售订单
│   ├── salePage/        # 销售页
│   ├── returnrequests/  # 退换货申请
│   ├── returndetail/    # 退货详情
│   ├── wuliuxinxi/      # 物流信息
│   ├── platform/        # 平台页
│   ├── supplier/        # 供应商
│   ├── options/         # 分店/自提点选择
│   ├── sharepage/       # 分享推广页
│   ├── question/        # 常见问题
│   ├── questionList/    # 问题列表
│   ├── welcome/         # 欢迎页
│   ├── warrant/         # 授权/售后
│   ├── idcar/           # 身份证
│   ├── pwdset/          # 密码设置
│   └── logs/            # 日志/调试
├── templates/           # 可复用 WXML 模板（swiper/product-view/order-state/my-view 等）
├── style/               # 公共样式（color/template/iconfont/weui/empower）
├── utils/util.js        # 工具函数
├── libs/                # 第三方库（qqmap-wx-jssdk.min.js）
├── wxParse/             # 富文本解析
├── data/                # 静态数据（省市区等）
├── images/              # 图片资源
├── app.js               # 应用入口（globalData + onLaunch）
├── app.json             # 应用配置（页面路由、TabBar、窗口样式）
└── app.wxss             # 全局样式入口
```

---

## 一、API 对接规范

### 1.1 基础配置

```javascript
// app.js globalData
globalData: {
  host: 'https://dev.ushopun.com/api',   // 后端 API 基础地址（已含 /api，生产可替换租户域名）
  // 本地调试：http://localhost:5136/api
  token: '',                              // 登录后写入的 JWT Token
  guid: '',                               // 登录后写入的用户 GUID
  customer: null                          // 当前用户信息
}
```

> `conf.js` 中的端点以 `/v2/...` 开头，`api.js` 通过 `host + url` 拼接出完整地址 `https://dev.ushopun.com/api/v2/...`。

### 1.2 统一返回结构（camelCase）

```json
{ "code": 200, "content": "请求成功！", "data": { }, "success": true }
```

| code | 含义 | 前端处理 |
|------|------|----------|
| 200  | 成功，业务数据在 `data` | 取 `data` 渲染 |
| 250  | 业务警告，`content` 为提示语 | `wx.showToast({ title: content, icon: 'none' })` |
| 301  | 跳转新地址，`content` 为 URL | `wx.redirectTo` / `wx.navigateTo` |
| 400  | 错误请求 | 提示 `content` |
| 401  | 未授权/未登录 | 清 token 跳登录页 |
| 403  | 模块未开启（module not open） | 提示「功能未开启」 |
| 404  | 找不到（not found） | 提示「数据不存在」 |
| 220  | 升级/需审核（is's update） | 引导用户申请升级（如代理升级） |
| 350  | 未批准（disapproved） | 提示「审核未通过」 |

> 特殊：`/account/checkaccount` 接口 `code` 为 `1`（可用）/`0`（已存在），非标准码，需单独处理。

### 1.3 鉴权机制

| Header | 说明 | 来源 |
|--------|------|------|
| `guid` | 用户 GUID | 登录后由 JWT 解析，或注册/登录接口返回 |
| `authorization` | JWT Token | `/account/login` 或 `/weixinopen/login` 返回的 `token` |
| `shopId` | 店铺/自提点 ID | 用户选择门店后本地缓存（`adress.id`） |

**鉴权标记**（对应后端控制器标注）：

| 标记 | 含义 |
|------|------|
| `[ApiAuthorize]` | 必须登录（header `authorization` 为有效 JWT），失败返回 `{ code: 401 }` |
| `[ApiAuthorize(false)]` | 匿名可访问，但会尝试解析 JWT 注入 guid |
| 无标记 | 公开接口，无需登录 |

### 1.4 api.js — 请求封装（核心）

```javascript
// api/api.js
const app = getApp()

const request = (url, options) => {
  return new Promise((resolve, reject) => {
    const fullUrl = `${app.globalData.host}${url}`  // host 已含 /api，url 以 /v2 开头

    let shopId = 0
    if (wx.getStorageSync('adress')) {
      shopId = wx.getStorageSync('adress').id
    }

    wx.request({
      url: fullUrl,
      method: options.method,
      data: options.method === 'GET' ? options.data : JSON.stringify(options.data),
      header: {
        'Content-Type': 'application/json; charset=UTF-8',
        guid: wx.getStorageSync('guid') || '',
        authorization: wx.getStorageSync('token') || '',
        shopId
      },
      success(request) {
        const res = request.data || {}
        if (res.code === 200) {
          resolve(res)          // 成功，调用方取 res.data
        } else if (res.code === 401) {
          wx.removeStorageSync('token')
          wx.removeStorageSync('guid')
          wx.navigateTo({ url: '/pages/login/login' })
          reject(res)
        } else {
          reject(res)           // 250 业务警告 / 404 等，调用方用 content 提示
        }
      },
      fail(error) {
        wx.showToast({ title: '网络异常，请稍后重试', icon: 'none' })
        reject(error)
      }
    })
  })
}

const get    = (url, options = {}) => request(url, { method: 'GET',    data: options })
const post   = (url, options)      => request(url, { method: 'POST',   data: options })
const put    = (url, options)      => request(url, { method: 'PUT',    data: options })
const remove = (url, options)      => request(url, { method: 'DELETE', data: options })

module.exports = { get, post, put, remove }
```

### 1.5 页面调用模式

```javascript
import api from '../../api/api'
import { productId, orderList } from '../../api/conf'

Page({
  data: { model: {}, list: [] },
  onLoad(options) {
    // GET 调用
    api.get(productId, { id: options.id })
      .then(res => this.setData({ model: res.data }))
      .catch(err => wx.showToast({ title: err.content || '加载失败', icon: 'none' }))

    // POST 调用
    api.post(orderList, { orderstatus: 0, page: 1 })
      .then(res => this.setData({ list: res.data.items }))
      .catch(err => wx.showToast({ title: err.content || '加载失败', icon: 'none' }))
  }
})
```

---

## 二、完整接口清单（按业务模块，含每个方法的调用方式）

> 下表均来自 `openapi.json`（`dev.ushopun.com` 真实后端 V2），路径前缀统一 `/api/v2`。「鉴权」列：`✔` = 必须登录（`[ApiAuthorize]`），`○` = 匿名可访问（`[ApiAuthorize(false)]`），`-` = 公开。所有接口统一用 `api.get(conf.xxx, params)` / `api.post(conf.xxx, data)` 调用。

### 2.1 账号 Account（前缀 /api/v2/account）

| 端点常量 | HTTP | 子路由 | 参数 | 返回 | 鉴权 |
|----------|------|--------|------|------|------|
| `login` | POST | /login | model: MoLogin（name, password） | { guid, token, nickname } | - |
| `online` | GET | /online | guid | 1 已注册 / 0 未注册 | ○ |
| `logout` | GET | /logout | - | - | - |
| `register` | POST | /register | model: MoRegister（phone, password, token, inviteCode） | - | - |
| `sendsmsforregister` | POST | /sendsmsforregister | phone | - | - |
| `chanagepwd` | POST | /chanagepwd | model: MoChangePassword | - | ○ |
| `sendsmsforfindpwd` | POST | /sendsmsforfindpwd | phone | - | - |
| `pwdset` | POST | /pwdset | model: MoPasswordRecovery | - | - |
| `checkaccount` | GET | /checkaccount | account | code=1 可用 / 0 不可用 | - |

**调用示例**：

```javascript
// 账号密码登录
api.post(login, { name: '13800138000', password: '123456' })
  .then(res => {
    // res.data = { guid, token, nickname }
    wx.setStorageSync('guid', res.data.guid)
    wx.setStorageSync('token', res.data.token)
  })

// 注册（先发验证码）
api.post(sendsmsforregister, { phone: '13800138000' })
api.post(register, { phone: '13800138000', password: '123456', token: '短信码', inviteCode: '邀请码' })
```

### 2.2 微信授权登录 / 注册（前缀 /api/v2/weixinopen）

| 端点常量 | HTTP | 子路由 | 参数 | 返回 | 鉴权 |
|----------|------|--------|------|------|------|
| `weixinminilogin` | GET | /login | code, state, encryptedData="", iv="" | TokenEntity { guid, token, openId } | - |
| `weixinminiphone` | GET | /phonenumber | code, encryptedData, iv | { phone } | - |
| `weixininfosubmit` | POST | /customer_nextstep | model: MoNextStep | TokenEntity | - |

**微信登录流程**：

```javascript
// 1. wx.login 获取 code → 微信授权登录
api.get(weixinminilogin, { code, state, encryptedData, iv })
  .then(res => {
    wx.setStorageSync('guid', res.data.guid)
    wx.setStorageSync('token', res.data.token)
    wx.setStorageSync('openId', res.data.openId)
  })

// 2. 绑定手机号（open-type="getPhoneNumber"）
api.get(weixinminiphone, { code, encryptedData, iv })
  .then(res => wx.setStorageSync('phone', res.data.phone))
```

### 2.3 用户 Customer（前缀 /api/v2/customer，类级 ✔）

| 端点常量 | HTTP | 子路由 | 参数 | 返回 |
|----------|------|--------|------|------|
| `getcustomer` | GET | /get | - | MoInfo |
| `customerinfo` | GET | /info | - | MoCustomerInfo |
| `customersubmit` | POST | /submit | model: MoCustomerRequest | - |
| `customerpoints` | GET | /points | page=1, size=12 | MoPoints |
| `uploadavatar` | POST | /uploadavatar | uploadAvatar | MoAvatar |
| `checkshop` | POST | /checkshop | Id | - |
| `myinvitecode` | GET | /myinvitecode | - | MoInviteCode |
| `myinvitees` | GET | /myinvitees | page=1, size=12 | MoInvitees |

### 2.4 地址 Address（前缀 /api/v2/address，类级 ✔）

| 端点常量 | HTTP | 子路由 | 参数 | 返回 |
|----------|------|--------|------|------|
| `addressList` | GET | /list | - | List\<MoAddress\> |
| `addressdelete` | POST | /delete | addressId | - |
| `addressadd` | POST | /add | model: MoAddressEdit | - |
| `addressdefault` | POST | /default | addressId | - |
| `addressedit` | POST | /edit | addressId, model: MoAddressEdit | - |

### 2.5 商品 Product（前缀 /api/v2/product）

| 端点常量 | HTTP | 子路由 | 参数 | 返回 | 鉴权 |
|----------|------|--------|------|------|------|
| `featuredbycid` | GET | /featuredbycid | cid, count, picsize?, specshow/tagshow/fullshow | List\<MoProductOverview\> | - |
| `homePro` | GET | /homeproducts | picsize?, specshow/tagshow/fullshow | List\<MoProductOverview\> | - |
| `specialproducts` | GET | /specialproducts | count, picsize?, ... | List\<MoProductOverview\> | - |
| `alsopurchased` | GET | /alsopurchased | pId, count, picsize?, ... | List\<MoProductOverview\> | - |
| `taglist` | GET | /taglist | count | List\<MoProductTag\> | - |
| `productbytag` | GET | /getbytag | tagName, count, picsize?, ... | List\<MoProductOverview\> | - |
| `getproductattr` | GET | /getproductattr | pId | MoProductAttrList（SKU 联动） | - |
| `getproductspec` | GET | /getproductspec | pId | List\<MoProductSpec\> | - |
| `productId` | GET | /getbyid | id | MoProduct | - |
| `productbysku` | GET | /getbysku | sku | MoProduct | - |
| `productpost` | POST | /post | mo: MoProductRequest | long | ✔ |

**调用示例**：

```javascript
api.get(productId, { id: 123 }).then(res => this.setData({ product: res.data }))
api.get(homePro, { picsize: 200 }).then(res => this.setData({ products: res.data }))
api.get(getproductattr, { pId: 123 }).then(res => this.setData({ attrs: res.data.attrs, tables: res.data.tables }))
```

### 2.6 分类 / 品牌 / 搜索

**Category（/api/v2/category）**

| 端点常量 | HTTP | 子路由 | 参数 | 返回 |
|----------|------|--------|------|------|
| `homecategories` | GET | /homecategories | - | List\<MoCategory\> |
| `categoryget` | GET | /get | id | MoCategory |
| `category` | GET | /sublist | loadsub=false, catId=0 | List\<MoCategoryList\> |

**Brand（/api/v2/brand）**

| 端点常量 | HTTP | 子路由 | 参数 | 返回 |
|----------|------|--------|------|------|
| `brandlist` | GET | /list | name="", picsize?, page=1, size=12 | MoBrandList |
| `brandfeaturelist` | GET | /featurelist | picsize? | List\<MoSimpleBrand\> |
| `brandget` | GET | /get | mid, picsize? | MoSimpleBrand |
| `brandfeaturedproducts` | GET | /featuredproducts | mid, count, ... | List\<MoProductOverview\> |

**Search（/api/v2/search）**

| 端点常量 | HTTP | 子路由 | 参数 | 返回 |
|----------|------|--------|------|------|
| `search` | GET | /find | q, sid, mid, cid, minPrice, maxPrice, page, size, orderBy | MoSearch |
| `searCate` | GET | /findbycid | cid, mid, tagName, minPrice/maxPrice, page, size, orderBy | MoCategory |
| `findbymid` | GET | /findbymid | mid, cid, tagName, minPrice/maxPrice, page, size, orderBy | MoBrand |
| `findbyoid` | GET | /findbyoid | oid, mid, cid, tagName, minPrice/maxPrice, page, size, orderBy | MoCustomerSearch |
| `hotcategory` | GET | /hotcategory | - | List\<KeyValueModel\> |
| `hotsearch` | GET | /hot | - | List\<string\> |
| `searchhistory` | GET | /history | - | List\<string\> |

### 2.7 购物车 ShoppingCart（前缀 /api/v2/shoppingcart，类级 ✔）

| 端点常量 | HTTP | 子路由 | 参数 | 返回 |
|----------|------|--------|------|------|
| `getShoppingcart` | GET | /get | - | MoCart |
| `cartCount` | GET | /count | - | int |
| `producttocart` | POST | /producttocart | model: MoAddCart（pId, qty, attrValue） | long |
| `productstocart` | POST | /productstocart | model: List\<MoAddCart\> | - |
| `producttocheckout` | POST | /producttocheckout | model: MoAddCart | long |
| `cartallselected` | POST | /cartallselected | selected | - |
| `updatecartitem` | POST | /updatecartitem | item: MoUpdateCart | MoUpdateCart |
| `removecartitem` | POST | /removecartitem | id | - |
| `removecart` | POST | /removecart | - | - |
| `wishlist` | GET | /wishlist | page=1, size=12 | MoCart |
| `removewishlistitem` | POST | /removewishlistitem | id | - |
| `iscollect` | POST | /iscollect | pid | int（1 已收藏 / 0 未收藏） |
| `towishlist` | POST | /towishlist | model: MoAddCart | long |
| `tocheckout` | POST | /tocheckout | - | - |

**调用示例**：

```javascript
api.get(getShoppingcart).then(res => this.setData({ cart: res.data }))
api.post(producttocart, { pId: 123, qty: 1, attrValue: 'combination_1_2' })
api.post(updatecartitem, { id: 1, quantity: 2, selected: true })
api.get(cartCount).then(res => this.setData({ count: res.data }))
```

### 2.8 结算 Checkout（前缀 /api/v2/checkout，类级 ✔）

| 端点常量 | HTTP | 子路由 | 参数 | 返回 |
|----------|------|--------|------|------|
| `checkminsubtotal` | GET | /checkminsubtotal | - | - |
| `getcheckout` | GET | /get | - | MoCheckout |
| `getpaymentmethod` | GET | /getpaymentmethod | - | List\<MoPaymentMethod\> |
| `getshippingmethod` | GET | /getshippingmethod | - | List\<MoShippingMethod\> |
| `submitcheckout` | POST | /submit | request: MoCheckoutRequest | MoCheckoutResponse |
| `quicksubmit` | POST | /quicksubmit | request: MoQuickOrderRequest | MoQuickOrderResponse |

### 2.9 订单 Order（前缀 /api/v2/order，类级 ✔）

| 端点常量 | HTTP | 子路由 | 参数 | 返回 |
|----------|------|--------|------|------|
| `returnrequests` | GET | /returnrequests | typeId=0, page=1, size=12 | MoReturnList |
| `returnpost` | POST | /returnpost | moReturn: MoReturn | - |
| `orderList` | GET | /list | startTime, endTime, orderstatus=0, page=1, size=12 | MoOrderList |
| `orderDetail` | GET | /detail | oid | MoOrderDetail |
| `orderconfirm` | POST | /complete | mo: MoOrderCancel | - |
| `orderdeliver` | POST | /deliver | mo: MoOrderDeliver | - |
| `ordercancel` | POST | /cancel | mo: MoOrderCancel | - |

### 2.10 支付（Plugin / WeixinOpenPayment）

**Plugin（/api/v2/plugin）**

| 端点常量 | HTTP | 子路由 | 参数 | 返回 | 鉴权 |
|----------|------|--------|------|------|------|
| `weixinwaploginenabled` | GET | /weixinwaploginenabled | - | - | - |
| `weixinwaploginurl` | GET | /weixinwaploginurl | callback | object | ✔ |
| `weixinopenloginenabled` | GET | /weixinopenloginenabled | - | - | - |
| `weixinopenlogin` | GET | /weixinopenlogin | code, state, encryptedData, iv | TokenEntity | - |
| `weixinopenphonenumber` | GET | /weixinopenphonenumber | code, encryptedData, iv | PhoneEntity | - |
| `weixinwappaymentenabled` | GET | /weixinwappaymentenabled | - | - | - |
| `weixinwapaymenturl` | GET | /weixinwapaymenturl | orderId, paytype | MoPayment | ✔ |
| `weixinopenpaymentenabled` | GET | /weixinopenpaymentenabled | - | - | - |
| `weixinopenpaymenturl` | GET | /weixinopenpaymenturl | orderId, paytype | MoPayment | ✔ |
| `alipaywappaymentenabled` | GET | /alipaywappaymentenabled | - | - | - |
| `alipaywappaymenturl` | GET | /alipaywappaymenturl | orderId, paytype | MoPayment | ✔ |

**WeixinOpenPayment（/api/v2/weixinopenpayment）**

| 端点常量 | HTTP | 子路由 | 参数 | 返回 |
|----------|------|--------|------|------|
| `weixinminipay` | GET | /paying | orderId, paytype, openId="" | MoWeixinOpenPayment |

**支付对接流程**：

```javascript
api.get(weixinopenpaymenturl, { orderId: 123, paytype: 'Order' }).then(res => {
  const p = res.data  // MoPayment 含支付参数
  wx.requestPayment({
    timeStamp: p.timeStamp, nonceStr: p.nonceStr,
    package: p.package, signType: p.signType, paySign: p.paySign,
    success() { /* 支付成功 */ },
    fail() { /* 支付失败 */ }
  })
})
```

### 2.11 优惠券 / 积分 / 钱包 / 充值卡

**Coupon（/api/v2/coupon）**

| 端点常量 | HTTP | 子路由 | 参数 | 返回 | 鉴权 |
|----------|------|--------|------|------|------|
| `couponshow` | POST | /show | account | List\<MoCoupon\> | - |
| `couponlist` | GET | /couponlist | type, page=1, size=12 | MoCouponList | ✔ |
| `coupon_center` | GET | /center | page=1, size=12 | MoCouponList | ✔ |
| `getcoupon` | POST | /getcoupon | code | - | ✔ |
| `usablecoupon` | GET | /usablecoupon | orderTotal | List\<MoCoupon\> | ✔ |

**PointsExchange（/api/v2/pointsexchange，类级 ✔）**

| 端点常量 | HTTP | 子路由 | 参数 | 返回 |
|----------|------|--------|------|------|
| `pointsexchangelist` | GET | /list | - | object |
| `pointsexchange` | POST | /exchange | ruleId | object |

**Wallet（/api/v2/wallet，类级 ✔）**

| 端点常量 | HTTP | 子路由 | 参数 | 返回 |
|----------|------|--------|------|------|
| `wallet` | GET | /get | - | MoWallet |
| `walletrecharge` | POST | /recharge | model: MoRechargePost | MoRecharge |
| `walletrechargelist` | POST | /rechargelist | ps=0, page=1, size=10 | MoRechargeList |
| `walletexchange` | POST | /exchange | model: MoExchange | MoExchange |
| `walletexchangelist` | POST | /exchangelist | page, size | MoExchangeList |
| `walletcardexchange` | POST | /cardexchange | moCard: MoCardExchange | - |
| `walletrecordlist` | GET | /recordlist | page, size | MoWalletRecordList |

**RechargeCard（/api/v2/rechargecard）**

| 端点常量 | HTTP | 子路由 | 参数 | 返回 |
|----------|------|--------|------|------|
| `rechargecardlist` | GET | /list | page=1, size=12 | MoRechargeCardList |
| `rechargecarditem` | GET | /item | id | MoRechargeCard |

**RechargeCardItem（/api/v2/rechargecarditem）**

| 端点常量 | HTTP | 子路由 | 参数 | 返回 |
|----------|------|--------|------|------|
| `rechargecarditemlist` | GET | /list | cardId, page=1, size=12 | MoRechargeCardItemList |
| `rechargecarditemget` | GET | /item | id | MoRechargeCardItem |

### 2.12 分销代理 Agents（前缀 /api/v2/agents，类级 ✔）

| 端点常量 | HTTP | 子路由 | 参数 | 返回 |
|----------|------|--------|------|------|
| `agentupgrade` | GET | /upgrade | - | code=220 需审核 |
| `agentmyinfo` | GET | /myinfo | - | MyAgentInfo |
| `agentspostinfo` | POST | /postinfo | moPostInfo: MoPostInfo | - |
| `agentmysummary` | GET | /mysummary | - | MoBonusSummary |
| `agentmyusers` | GET | /myusers | page=1, size=12 | MoInvitees |
| `agentmyorders` | GET | /myorders | page=1, size=12 | MoAgentOrder |
| `agentmybonus` | GET | /mybonus | page=1, size=12 | MoAgentBonus |

### 2.13 评价 Review（前缀 /api/v2/productreview）

| 端点常量 | HTTP | 子路由 | 参数 | 返回 | 鉴权 |
|----------|------|--------|------|------|------|
| `commentlist` | GET | /list | pId, page=1, size=12 | MoProductReviewList | - |
| `myreviews` | GET | /myreviews | page=1, size=12 | MoMyReviewList | ✔ |
| `productreviewing` | GET | /productreviewing | page=1, size=12 | MoOrderNoReviewList | ✔ |
| `commentsubmit` | POST | /submit | model: MoReviewRequest | - | ✔ |

### 2.14 收藏 Favorites（前缀 /api/v2/favorites，类级 ✔）

| 端点常量 | HTTP | 子路由 | 参数 | 返回 |
|----------|------|--------|------|------|
| `favoriteslist` | GET | /list | picsize?, specshow/tagshow/fullshow, page=1, size=12 | MoFavoritesList |
| `favoritessubmit` | POST | /submit | model: MoFavoritesRequest（productId） | - |
| `favoritesremove` | POST | /remove | id | - |
| `recentproductlist` | GET | /list-recentproduct | 同上 | MoFavoritesList |
| `recentproductsubmit` | POST | /submit-recentproduct | model | - |
| `recentproductremove` | POST | /remove-recentproduct | id | - |

### 2.15 通用 Common（前缀 /api/v2/common）

| 端点常量 | HTTP | 子路由 | 参数 | 返回 | 鉴权 |
|----------|------|--------|------|------|------|
| `referrerinfo` | GET | /referrerinfo | code | MoReferrerInfo | - |
| `referrerauto` | GET | /referrerauto | - | MoReferrerInfo | ✔ |
| `banner` | GET | /banner | name, picsize=50 | MoBannerZone | - |
| `forminfo` | GET | /forminfo | name | MoFormInfo | - |
| `formsubmit` | POST | /formsubmit | name, model: MoFormSubmit | int | - |
| `getform` | POST | /getform | id | MoFormData | - |
| `levels` | GET | /levels | - | List\<MoAllLevel\> | - |
| `allprovinces` | POST | /allprovinces | - | List\<MoProvinces\> | - |
| `uploadpicture` | POST | /uploadpicture | upload: MoBase64 | MoPictureResponse | ✔ |
| `picturepost` | POST | /picturepost | form | MoPictureResponse | ✔ |
| `producttype` | GET | /producttype | - | List\<KeyValueStrModel\> | - |
| `orderstatus` | GET | /orderstatus | - | List\<KeyValueStrModel\> | - |
| `ordertype` | GET | /ordertype | - | List\<KeyValueStrModel\> | - |
| `returnreasons` | GET | /returnreasons | - | List\<string\> | - |
| `returnactions` | GET | /returnactions | - | List\<string\> | - |
| `requesttypes` | GET | /requesttypes | - | List\<KeyValueStrModel\> | - |
| `paymentstatus` | GET | /paymentstatus | - | List\<KeyValueStrModel\> | - |
| `shippingstatus` | GET | /shippingstatus | - | List\<KeyValueStrModel\> | - |
| `pluginscenes` | GET | /pluginscenes | - | List\<KeyValueStrModel\> | - |
| `customattrtype` | GET | /customattrtype | - | List\<KeyValueStrModel\> | - |
| `messagetype` | GET | /messagetype | - | List\<KeyValueStrModel\> | - |

### 2.16 内容资讯（Topic / News / Blog）

**Topic（/api/v2/topic）**

| 端点常量 | HTTP | 子路由 | 参数 | 返回 |
|----------|------|--------|------|------|
| `topiclist` | GET | /list | page=1, size=12 | MoTopicList |
| `topicdetail` | GET | /detail | systemName | MoTopic（含富文本 body） |

**News（/api/v2/news）**

| 端点常量 | HTTP | 子路由 | 参数 | 返回 |
|----------|------|--------|------|------|
| `newslist` | GET | /list | page=1, size=12 | MoNewsList |
| `newsitem` | GET | /item | id | MoNews |

**Blog（/api/v2/blog）**

| 端点常量 | HTTP | 子路由 | 参数 | 返回 | 鉴权 |
|----------|------|--------|------|------|------|
| `bloglist` | GET | /list | customerId, page=1, size=12 | MoBlogList | - |
| `blogitem` | GET | /item | id | MoBlog | - |
| `blogpost` | POST | /post | model: MoBlogPost | MoBlog | ✔ |
| `blogcategories` | GET | /categories | - | List\<MoPaperCategory\> | - |
| `blogpapers` | GET | /papers | categoryId | List\<MoPaper\> | - |

### 2.17 消息 / 物流 / 其他营销

**PM（/api/v2/pm，类级 ✔）**

| 端点常量 | HTTP | 子路由 | 参数 | 返回 |
|----------|------|--------|------|------|
| `pmmarkRead` | POST | /markRead | msgIds | - |
| `pmsend` | POST | /send | model: MoSendMessage | - |
| `pmlist` | GET | /list | type=0, page=1, size=12 | MoMessageList |
| `pmdelpm` | GET | /delpm | msgId | - |

**Shipping（/api/v2/shipping）**

| 端点常量 | HTTP | 子路由 | 参数 | 返回 | 鉴权 |
|----------|------|--------|------|------|------|
| `pickuplist` | GET | /pickuplist | - | List\<MoPickupPoint\> | - |
| `shopsearch` | GET | /shopsearch | keyword, lat, lng, page=1, size=20 | object | - |
| `shipments` | GET | /shipments | oid | MoShipmentBrief | ✔ |

**Kdniao（/api/v2/kdniao）**

| 端点常量 | HTTP | 子路由 | 参数 | 返回 | 鉴权 |
|----------|------|--------|------|------|------|
| `expresskdniaoapiurl` | GET | /expresskdniaoapiurl | company, number | MoExpressInfo | ✔ |

**Seckill（/api/v2/seckill）**

| 端点常量 | HTTP | 子路由 | 参数 | 返回 |
|----------|------|--------|------|------|
| `seckillstatus` | GET | /status | - | MoSeckillStatus |
| `seckilllist` | GET | /list | page=1, size=10 | List\<MoSeckillProduct\> |
| `seckilldetail` | GET | /{id} | id | MoSeckillDetail |

**PinTuan（/api/v2/pintuan）**

| 端点常量 | HTTP | 子路由 | 参数 | 返回 | 鉴权 |
|----------|------|--------|------|------|------|
| `pintuanproduct` | GET | /product | pId, ptcId=0 | MoPinTuanProduct | ✔ |
| `pintuangroup` | GET | /group | - | MoPinTuan | - |
| `pintuankaituan` | POST | /kaituan | kaituan: MoKaiTuan | object | ✔ |

**SignIn（/api/v2/signin，类级 ✔）**

| 端点常量 | HTTP | 子路由 | 参数 | 返回 |
|----------|------|--------|------|------|
| `signinstatus` | GET | /status | - | SignInStatusResponse |
| `signin` | POST | /signin | - | SignInResultResponse |
| `signinrecords` | GET | /records | page=1, size=10 | MoSignInRecords |
| `signincalendar` | GET | /calendar | year, month | MoSignInCalendar |

**Task（/api/v2/task，类级 ✔）**

| 端点常量 | HTTP | 子路由 | 参数 | 返回 |
|----------|------|--------|------|------|
| `tasklist` | GET | /list | - | object |
| `taskclaim` | POST | /claim | taskRecordId | object |
| `taskunclaimed` | GET | /unclaimed | - | object |

**Share（/api/v2/share，类级 ✔）**

| 端点常量 | HTTP | 子路由 | 参数 | 返回 |
|----------|------|--------|------|------|
| `sharereward` | POST | /reward | - | MoShareReward |

**PreOrder（/api/v2/preorder，类级 ✔）**

| 端点常量 | HTTP | 子路由 | 参数 | 返回 |
|----------|------|--------|------|------|
| `preorderpayrest` | POST | /pay-rest | orderId, paymentMethod | MoPayRestResult |
| `preorderrestinfo` | GET | /rest-info | orderId | MoPreOrderRest |

**TierPrice（/api/v2/tierprice，类级 ✔）**

| 端点常量 | HTTP | 子路由 | 参数 | 返回 |
|----------|------|--------|------|------|
| `tierprices` | GET | /tierprices | productId | List\<MoTierPrice\> |

**Bundle（/api/v2/bundle）**

| 端点常量 | HTTP | 子路由 | 参数 | 返回 |
|----------|------|--------|------|------|
| `bundlelist` | GET | /list | - | object |
| `bundledetail` | GET | /{id} | id | object |

**Page（/api/v2/page）**

| 端点常量 | HTTP | 子路由 | 参数 | 返回 |
|----------|------|--------|------|------|
| `pageindex` | GET | /index | - | MoBrandList |
| `pagefeaturelist` | GET | /featurelist | picsize? | List\<MoSimpleBrand\> |
| `pageget` | GET | /get | mid, picsize? | MoSimpleBrand |
| `pagefeaturedproducts` | GET | /featuredproducts | mid, count, ... | List\<MoProductOverview\> |

**AuthWeixinMini（/api/v2/authweixinmini）**

| 端点常量 | HTTP | 子路由 | 参数 | 返回 | 鉴权 |
|----------|------|--------|------|------|------|
| `nicknameupdate` | POST | /update | model: MoUpdate | ApiResponse | ✔ |

---

## 三、完整 conf.js 端点常量清单

> 所有端点均不含 `/api` 前缀（由 `api.js` 拼接，`host` 已含 `/api`），端点以 `/v2/...` 开头，直接复制即可对接全部后端接口。

```javascript
// ============ 账号 Account ============
const login               = '/v2/account/login'
const online              = '/v2/account/online'
const logout              = '/v2/account/logout'
const register            = '/v2/account/register'
const sendsmsforregister  = '/v2/account/sendsmsforregister'
const chanagepwd          = '/v2/account/chanagepwd'
const sendsmsforfindpwd   = '/v2/account/sendsmsforfindpwd'
const pwdset              = '/v2/account/pwdset'
const checkaccount        = '/v2/account/checkaccount'

// ============ 微信授权 WeixinOpen ============
const weixinminilogin     = '/v2/weixinopen/login'
const weixinminiphone     = '/v2/weixinopen/phonenumber'
const weixininfosubmit    = '/v2/weixinopen/customer_nextstep'

// ============ 用户 Customer ============
const getcustomer         = '/v2/customer/get'
const customerinfo        = '/v2/customer/info'
const customersubmit      = '/v2/customer/submit'
const customerpoints      = '/v2/customer/points'
const uploadavatar        = '/v2/customer/uploadavatar'
const checkshop           = '/v2/customer/checkshop'
const myinvitecode        = '/v2/customer/myinvitecode'
const myinvitees          = '/v2/customer/myinvitees'

// ============ 地址 Address ============
const addressList         = '/v2/address/list'
const addressdelete       = '/v2/address/delete'
const addressadd          = '/v2/address/add'
const addressdefault      = '/v2/address/default'
const addressedit         = '/v2/address/edit'

// ============ 商品 Product ============
const featuredbycid       = '/v2/product/featuredbycid'
const homePro             = '/v2/product/homeproducts'
const specialproducts     = '/v2/product/specialproducts'
const alsopurchased       = '/v2/product/alsopurchased'
const taglist             = '/v2/product/taglist'
const productbytag        = '/v2/product/getbytag'
const getproductattr      = '/v2/product/getproductattr'
const getproductspec      = '/v2/product/getproductspec'
const productId           = '/v2/product/getbyid'
const productbysku        = '/v2/product/getbysku'
const productpost         = '/v2/product/post'

// ============ 分类 / 品牌 / 搜索 ============
const homecategories      = '/v2/category/homecategories'
const categoryget         = '/v2/category/get'
const category            = '/v2/category/sublist'
const brandlist           = '/v2/brand/list'
const brandfeaturelist    = '/v2/brand/featurelist'
const brandget            = '/v2/brand/get'
const brandfeaturedproducts = '/v2/brand/featuredproducts'
const search              = '/v2/search/find'
const searCate            = '/v2/search/findbycid'
const findbymid           = '/v2/search/findbymid'
const findbyoid           = '/v2/search/findbyoid'
const hotcategory         = '/v2/search/hotcategory'
const hotsearch           = '/v2/search/hot'
const searchhistory       = '/v2/search/history'

// ============ 购物车 ShoppingCart ============
const getShoppingcart     = '/v2/shoppingcart/get'
const cartCount           = '/v2/shoppingcart/count'
const producttocart       = '/v2/shoppingcart/producttocart'
const productstocart      = '/v2/shoppingcart/productstocart'
const producttocheckout   = '/v2/shoppingcart/producttocheckout'
const cartallselected     = '/v2/shoppingcart/cartallselected'
const updatecartitem      = '/v2/shoppingcart/updatecartitem'
const removecartitem      = '/v2/shoppingcart/removecartitem'
const removecart          = '/v2/shoppingcart/removecart'
const wishlist            = '/v2/shoppingcart/wishlist'
const removewishlistitem  = '/v2/shoppingcart/removewishlistitem'
const iscollect           = '/v2/shoppingcart/iscollect'
const towishlist          = '/v2/shoppingcart/towishlist'
const tocheckout          = '/v2/shoppingcart/tocheckout'

// ============ 结算 Checkout ============
const checkminsubtotal    = '/v2/checkout/checkminsubtotal'
const getcheckout         = '/v2/checkout/get'
const getpaymentmethod    = '/v2/checkout/getpaymentmethod'
const getshippingmethod   = '/v2/checkout/getshippingmethod'
const submitcheckout      = '/v2/checkout/submit'
const quicksubmit         = '/v2/checkout/quicksubmit'

// ============ 订单 Order ============
const returnrequests      = '/v2/order/returnrequests'
const returnpost          = '/v2/order/returnpost'
const orderList           = '/v2/order/list'
const orderDetail         = '/v2/order/detail'
const orderconfirm        = '/v2/order/complete'
const orderdeliver        = '/v2/order/deliver'
const ordercancel         = '/v2/order/cancel'

// ============ 支付 Plugin / WeixinOpenPayment ============
const weixinwaploginenabled    = '/v2/plugin/weixinwaploginenabled'
const weixinwaploginurl        = '/v2/plugin/weixinwaploginurl'
const weixinopenloginenabled   = '/v2/plugin/weixinopenloginenabled'
const weixinopenlogin          = '/v2/plugin/weixinopenlogin'
const weixinopenphonenumber    = '/v2/plugin/weixinopenphonenumber'
const weixinwappaymentenabled  = '/v2/plugin/weixinwappaymentenabled'
const weixinwapaymenturl       = '/v2/plugin/weixinwapaymenturl'
const weixinopenpaymentenabled = '/v2/plugin/weixinopenpaymentenabled'
const weixinopenpaymenturl     = '/v2/plugin/weixinopenpaymenturl'
const alipaywappaymentenabled  = '/v2/plugin/alipaywappaymentenabled'
const alipaywappaymenturl      = '/v2/plugin/alipaywappaymenturl'
const weixinminipay            = '/v2/weixinopenpayment/paying'

// ============ 优惠券 Coupon ============
const couponshow          = '/v2/coupon/show'
const couponlist          = '/v2/coupon/couponlist'
const coupon_center       = '/v2/coupon/center'
const getcoupon           = '/v2/coupon/getcoupon'
const usablecoupon        = '/v2/coupon/usablecoupon'

// ============ 积分 / 钱包 / 充值卡 ============
const pointsexchangelist  = '/v2/pointsexchange/list'
const pointsexchange      = '/v2/pointsexchange/exchange'
const wallet              = '/v2/wallet/get'
const walletrecharge      = '/v2/wallet/recharge'
const walletrechargelist  = '/v2/wallet/rechargelist'
const walletexchange      = '/v2/wallet/exchange'
const walletexchangelist  = '/v2/wallet/exchangelist'
const walletcardexchange  = '/v2/wallet/cardexchange'
const walletrecordlist    = '/v2/wallet/recordlist'
const rechargecardlist    = '/v2/rechargecard/list'
const rechargecarditem    = '/v2/rechargecard/item'
const rechargecarditemlist = '/v2/rechargecarditem/list'
const rechargecarditemget = '/v2/rechargecarditem/item'

// ============ 分销代理 Agents ============
const agentupgrade        = '/v2/agents/upgrade'
const agentmyinfo         = '/v2/agents/myinfo'
const agentspostinfo      = '/v2/agents/postinfo'
const agentmysummary      = '/v2/agents/mysummary'
const agentmyusers        = '/v2/agents/myusers'
const agentmyorders       = '/v2/agents/myorders'
const agentmybonus        = '/v2/agents/mybonus'

// ============ 评价 Review ============
const commentlist         = '/v2/productreview/list'
const myreviews           = '/v2/productreview/myreviews'
const productreviewing    = '/v2/productreview/productreviewing'
const commentsubmit       = '/v2/productreview/submit'

// ============ 收藏 Favorites ============
const favoriteslist       = '/v2/favorites/list'
const favoritessubmit     = '/v2/favorites/submit'
const favoritesremove     = '/v2/favorites/remove'
const recentproductlist   = '/v2/favorites/list-recentproduct'
const recentproductsubmit = '/v2/favorites/submit-recentproduct'
const recentproductremove = '/v2/favorites/remove-recentproduct'

// ============ 通用 Common ============
const referrerinfo        = '/v2/common/referrerinfo'
const referrerauto        = '/v2/common/referrerauto'
const banner              = '/v2/common/banner'
const forminfo            = '/v2/common/forminfo'
const formsubmit          = '/v2/common/formsubmit'
const getform             = '/v2/common/getform'
const levels              = '/v2/common/levels'
const allprovinces        = '/v2/common/allprovinces'
const uploadpicture       = '/v2/common/uploadpicture'
const picturepost         = '/v2/common/picturepost'
const producttype         = '/v2/common/producttype'
const orderstatus         = '/v2/common/orderstatus'
const ordertype           = '/v2/common/ordertype'
const returnreasons       = '/v2/common/returnreasons'
const returnactions       = '/v2/common/returnactions'
const requesttypes        = '/v2/common/requesttypes'
const paymentstatus       = '/v2/common/paymentstatus'
const shippingstatus      = '/v2/common/shippingstatus'
const pluginscenes        = '/v2/common/pluginscenes'
const customattrtype      = '/v2/common/customattrtype'
const messagetype         = '/v2/common/messagetype'

// ============ 内容资讯 Topic / News / Blog ============
const topiclist           = '/v2/topic/list'
const topicdetail         = '/v2/topic/detail'
const newslist            = '/v2/news/list'
const newsitem            = '/v2/news/item'
const bloglist            = '/v2/blog/list'
const blogitem            = '/v2/blog/item'
const blogpost            = '/v2/blog/post'
const blogcategories      = '/v2/blog/categories'
const blogpapers          = '/v2/blog/papers'

// ============ 消息 PM ============
const pmmarkRead          = '/v2/pm/markRead'
const pmsend              = '/v2/pm/send'
const pmlist              = '/v2/pm/list'
const pmdelpm             = '/v2/pm/delpm'

// ============ 物流 Shipping / Kdniao ============
const pickuplist          = '/v2/shipping/pickuplist'
const shopsearch          = '/v2/shipping/shopsearch'
const shipments           = '/v2/shipping/shipments'
const expresskdniaoapiurl = '/v2/kdniao/expresskdniaoapiurl'

// ============ 营销 Seckill / PinTuan / SignIn / Task / Share / PreOrder / TierPrice / Bundle / Page ============
const seckillstatus       = '/v2/seckill/status'
const seckilllist         = '/v2/seckill/list'
const pintuanproduct      = '/v2/pintuan/product'
const pintuangroup        = '/v2/pintuan/group'
const pintuankaituan      = '/v2/pintuan/kaituan'
const signinstatus        = '/v2/signin/status'
const signin              = '/v2/signin/signin'
const signinrecords       = '/v2/signin/records'
const signincalendar      = '/v2/signin/calendar'
const tasklist            = '/v2/task/list'
const taskclaim           = '/v2/task/claim'
const taskunclaimed       = '/v2/task/unclaimed'
const sharereward         = '/v2/share/reward'
const preorderpayrest     = '/v2/preorder/pay-rest'
const preorderrestinfo    = '/v2/preorder/rest-info'
const tierprices          = '/v2/tierprice/tierprices'
const bundlelist          = '/v2/bundle/list'
const pageindex           = '/v2/page/index'
const pagefeaturelist     = '/v2/page/featurelist'
const pageget             = '/v2/page/get'
const pagefeaturedproducts = '/v2/page/featuredproducts'
const nicknameupdate      = '/v2/authweixinmini/update'

module.exports = {
  // Account
  login, online, logout, register, sendsmsforregister, chanagepwd,
  sendsmsforfindpwd, pwdset, checkaccount,
  // WeixinOpen
  weixinminilogin, weixinminiphone, weixininfosubmit,
  // Customer
  getcustomer, customerinfo, customersubmit, customerpoints, uploadavatar,
  checkshop, myinvitecode, myinvitees,
  // Address
  addressList, addressdelete, addressadd, addressdefault, addressedit,
  // Product
  featuredbycid, homePro, specialproducts, alsopurchased, taglist, productbytag,
  getproductattr, getproductspec, productId, productbysku, productpost,
  // Category/Brand/Search
  homecategories, categoryget, category, brandlist, brandfeaturelist, brandget,
  brandfeaturedproducts, search, searCate, findbymid, findbyoid, hotcategory,
  hotsearch, searchhistory,
  // ShoppingCart
  getShoppingcart, cartCount, producttocart, productstocart, producttocheckout,
  cartallselected, updatecartitem, removecartitem, removecart, wishlist,
  removewishlistitem, iscollect, towishlist, tocheckout,
  // Checkout
  checkminsubtotal, getcheckout, getpaymentmethod, getshippingmethod,
  submitcheckout, quicksubmit,
  // Order
  returnrequests, returnpost, orderList, orderDetail, orderconfirm, orderdeliver,
  ordercancel,
  // Plugin/Payment
  weixinwaploginenabled, weixinwaploginurl, weixinopenloginenabled,
  weixinopenlogin, weixinopenphonenumber, weixinwappaymentenabled,
  weixinwapaymenturl, weixinopenpaymentenabled, weixinopenpaymenturl,
  alipaywappaymentenabled, alipaywappaymenturl, weixinminipay,
  // Coupon
  couponshow, couponlist, coupon_center, getcoupon, usablecoupon,
  // Points/Wallet/RechargeCard
  pointsexchangelist, pointsexchange, wallet, walletrecharge, walletrechargelist,
  walletexchange, walletexchangelist, walletcardexchange, walletrecordlist,
  rechargecardlist, rechargecarditem, rechargecarditemlist, rechargecarditemget,
  // Agents
  agentupgrade, agentmyinfo, agentspostinfo, agentmysummary, agentmyusers,
  agentmyorders, agentmybonus,
  // Review
  commentlist, myreviews, productreviewing, commentsubmit,
  // Favorites
  favoriteslist, favoritessubmit, favoritesremove, recentproductlist,
  recentproductsubmit, recentproductremove,
  // Common
  referrerinfo, referrerauto, banner, forminfo, formsubmit, getform, levels,
  allprovinces, uploadpicture, picturepost, producttype, orderstatus, ordertype,
  returnreasons, returnactions, requesttypes, paymentstatus, shippingstatus,
  pluginscenes, customattrtype, messagetype,
  // Topic/News/Blog
  topiclist, topicdetail, newslist, newsitem, bloglist, blogitem, blogpost,
  blogcategories, blogpapers,
  // PM
  pmmarkRead, pmsend, pmlist, pmdelpm,
  // Shipping/Kdniao
  pickuplist, shopsearch, shipments, expresskdniaoapiurl,
  // Marketing
  seckillstatus, seckilllist, pintuanproduct, pintuangroup, pintuankaituan,
  signinstatus, signin, signinrecords, signincalendar, tasklist, taskclaim,
  taskunclaimed, sharereward, preorderpayrest, preorderrestinfo, tierprices,
  bundlelist, pageindex, pagefeaturelist, pageget, pagefeaturedproducts,
  nicknameupdate
}
```

---

## 四、核心业务流程

### 4.1 登录授权流

```
① 账号密码登录：
   api.post(login, { name, password })
   → res.data = { guid, token, nickname }
   → wx.setStorageSync('guid', guid); wx.setStorageSync('token', token)

② 微信授权登录：
   wx.login() → code
   → api.get(weixinminilogin, { code, state, encryptedData, iv })
   → res.data = { guid, token, openId }（TokenEntity）
   → 存储 guid + token

③ 绑定手机号：
   <button open-type="getPhoneNumber">
   → api.get(weixinminiphone, { code, encryptedData, iv })
   → res.data = { phone }
```

### 4.2 购买流

```
详情选 SKU → 加入购物车(producttocart) / 立即购买(producttocheckout)
  → 购物车列表勾选(getShoppingcart + cartallselected)
  → 结算页(getcheckout)选地址/优惠券/支付方式
  → api.post(submitcheckout, { request: {...} }) → 创建订单
  → api.get(weixinopenpaymenturl, { orderId, paytype }) → 支付参数
  → wx.requestPayment → 支付成功 → 跳转支付成功页
```

### 4.3 分销流

```
用户分享（path 携带 code）→ 新用户进入存储 code
  → api.get(referrerauto) → 自动绑定推荐关系
  → 新用户下单 → 推荐人获佣金/分红
  → 代理中心(agentmyinfo/mysummary/mybonus)查看收益
```

---

## 五、场景化界面规划（按业务场景）

> 同一套 `miniProgramV2` 页面 + `openapi.json` 接口，可按业务场景裁剪组合。生成前先确认目标场景，再决定启用哪些页面与接口模块；未指定时默认生成「标准 B2C 商城」核心链路。场景可叠加（如「分销 + 社区团购」）。

### 5.1 标准 B2C 商城（核心交易闭环）

- **定位**：通用商品交易，最快上线
- **页面**：index / category / subcategory / detail / search / cart / checkout / checkoutdetail / order / orderList / payFinish / my / login / address / address-edit / collect / comment
- **接口模块**：account、product、category、brand、search、shoppingcart、checkout、order、payment、address、favorites、review、common(banner)
- **TabBar**：首页 / 分类 / 购物车 / 我的
- **首页结构**：轮播 `banner` + 公告 `topic` + 金刚区分类入口 `homecategories` + 热卖/新品商品卡 `homePro/productbytag` + 优惠券弹窗 `couponshow`

### 5.2 社区团购 / O2O 门店自提

- **定位**：社区团长、就近自提、门店/提货点
- **页面**：index（顶部自提点入口）+ options（自提点/分店选择）+ category + detail + cart + checkout + order + wuliuxinxi + shopsearch 相关
- **接口模块**：shipping（pickuplist/shopsearch）+ customer（checkshop）+ 标准交易模块
- **TabBar**：首页 / 分类 / 购物车 / 我的
- **关键差异**：下单前先选 `shopId`（自提点，`adress.id` 注入 header）；checkout 展示自提点而非收货地址；配送方式走 `getshippingmethod`

### 5.3 分销裂变商城

- **定位**：代理/合伙人、佣金分红、邀请拉新
- **页面**：index + distribution + dividend + bonusDetail + myCustomer + myinvitre + partner + saleOrder + salePage + sharepage + warrant + idcar + 核心交易页
- **接口模块**：agents + customer（myinvitecode/myinvitees）+ common（referrerinfo/referrerauto）+ 交易模块
- **TabBar**：首页 / 分类 / 购物车 / 我的（我的页顶部强化「分销中心」入口）
- **关键差异**：登录后引导绑定推荐关系 `referrerauto`；分享 path 携带 code；我的页突出「收益/我的客户/邀请」

### 5.4 会员积分 / 钱包商城

- **定位**：会员资产、积分兑换、充值、签到留存
- **页面**：point + recharge + rechargeList + cashout + youhuijuan + available_coupon + usedcunpond + 核心交易页
- **接口模块**：wallet + pointsexchange + rechargecard + coupon + signin + task
- **TabBar**：首页 / 分类 / 购物车 / 我的（我的页顶部资产卡片）
- **关键差异**：我的页顶部资产卡片（余额/积分/优惠券）；签到 `signin` / 任务 `task` 引导每日活跃；积分商城 `pointsexchange` 兑换商品

### 5.5 秒杀 / 拼团 / 预售营销商城

- **定位**：限时秒杀、拼团、预售、阶梯价等营销玩法
- **页面**：index（活动楼层）+ seckill / pintuan / preorder 相关活动页 + 核心交易页
- **接口模块**：seckill + pintuan + preorder + tierprice + bundle + 交易模块
- **TabBar**：首页 / 分类 / 购物车 / 我的
- **关键差异**：首页增加活动楼层入口；活动商品卡带倒计时 `seckill` / 进度条 `pintuan`；拼团需「开团/参团」交互

### 5.6 内容电商 / 品牌资讯

- **定位**：资讯种草 + 商品转化
- **页面**：blog（列表/详情）+ news + topic + detail（商品）+ search + 核心交易页
- **接口模块**：blog + news + topic + product + search
- **TabBar**：首页 / 分类 / 购物车 / 我的（首页信息流）
- **关键差异**：首页以内容信息流为主，文章内嵌商品卡片跳转商品详情

### 5.7 场景选择与生成规则

1. 生成前先询问/确认目标场景，按上表确定启用页面与接口模块
2. 未指定时默认生成「标准 B2C 商城」核心链路：account / index / category / detail / cart / checkout / order / my / address
3. TabBar 保持 2~5 个，超出部分下沉到「我的」页入口或首页金刚区

---

## 六、页面展示规范

### 6.1 页面四件套

| 文件 | 作用 |
|------|------|
| `页面名.js` | 页面逻辑（数据、生命周期、事件、导航） |
| `页面名.wxml` | 页面结构（WXML 模板语法、组件引用） |
| `页面名.wxss` | 页面样式 |
| `页面名.json` | 页面配置（导航栏标题、组件注册） |

### 6.2 JS 页面结构模板

```javascript
import api from '../../api/api'
import { /* 需要的端点 */ } from '../../api/conf'

Page({
  data: { /* 响应式变量 */ },
  onLoad(options) { /* 页面加载，处理路由参数 */ },
  onShow() { /* 页面显示/切回前台 */ },
  onReady() { /* 初次渲染完成 */ },
  getData() { /* 业务方法，驼峰命名，动词开头 */ },
  onPullDownRefresh() { this.onShow(); wx.stopPullDownRefresh() },
  onReachBottom() { /* 触底分页 page++ */ },
  onShareAppMessage() { return { title: '分享标题', path: '/pages/xxx/xxx?id=' + this.data.id } }
})
```

### 6.3 核心页面结构

| 页面 | 结构说明 |
|------|----------|
| **index 首页** | 轮播(banner) + 公告(topic) + 分类入口(homecategories) + 热卖商品(productbytag) + 优惠券弹窗(couponshow/getcoupon) |
| **category 分类** | 左侧一级分类，右侧二级分类+商品 |
| **subcategory 二级分类** | 商品列表，触底加载 |
| **detail 商品详情** | 商品图轮播 + 价格 + SKU 面板(getproductattr/getproductspec) + 富文本详情(wxParse) + 底部操作栏 |
| **cart 购物车** | 商品列表 + 全选/单选 + 数量加减(updatecartitem) + 删除(removecartitem) + 结算 |
| **checkout 结算** | 地址 + 商品清单 + 优惠券 + 支付方式 + 提交订单(submitcheckout) |
| **order/orderList 订单** | Tab 切换(待付款/待发货/待收货/已完成) + 订单卡片 + 操作按钮 |
| **checkoutdetail 订单详情** | 状态 + 地址 + 商品 + 订单信息 + 操作按钮 |
| **my 个人中心** | 用户信息卡片 + 功能入口网格 + 分销/订单/收藏/地址/优惠券入口 |
| **search 搜索** | 搜索框 + 热门搜索(hotsearch) + 搜索结果(search) |

### 6.4 状态覆盖

所有列表/详情页必须覆盖四种状态：**加载中 / 空数据 / 错误 / 正常**；按钮需覆盖业务状态（如商品：正常、售罄、下架、即将开卖）。

---

## 七、交互与反馈规范

| 场景 | 实现 |
|------|------|
| 加载中 | `wx.showLoading({ title: '加载中', mask: true })` / `wx.hideLoading()` |
| 成功 | `wx.showToast({ title: '成功' })` |
| 失败 | `wx.showToast({ title: err.content || '失败', icon: 'none' })` |
| 确认 | `wx.showModal({ title, content, success })` |
| 下拉刷新 | `onPullDownRefresh` + `wx.stopPullDownRefresh()` |
| 触底加载 | `onReachBottom` + `page++` |
| 分享 | `onShareAppMessage` 返回 `{ title, path }` |

---

## 八、部署上线

1. 修改 `app.js` 中 `globalData.host` 为后端 API 地址（开发用 `https://dev.ushopun.com/api`，正式替换为租户域名 `https://{tenant}.ushopun.com/api`）
2. 在 `project.config.json` 填写小程序 AppID
3. 后端管理后台配置微信支付商户信息
4. 替换腾讯地图 SDK key（如使用定位）
5. 配置合法域名（request/uploadFile 域名，含 `dev.ushopun.com` 与正式租户域名）
6. 微信开发者工具上传代码、提交审核

> **对接前必读**：先在 `https://dev.ushopun.com` 示例站点确认目标模块已开通、接口可达（域名白名单、鉴权、模块开关）。若模块返回 `code: 403`（module not open）或 `code: 220`（需升级），说明需在后台开通对应功能，具体开通与付费请直接联系优社云AI官方。

---

## 九、开发硬性要求

1. API 端点必须在 `conf.js` 定义常量，禁止在页面中硬编码 URL
2. 所有请求通过 `api.js` 封装方法调用，禁止直接 `wx.request`
3. 请求头自动携带 `guid`（用户标识）、`authorization`（JWT Token）、`shopId`（店铺/自提点）
4. 使用 `this.setData()` 更新数据，数组项更新用字符串 key：`['arr[' + i + '].field']`
5. 图片必须设置 `mode` 属性（推荐 `widthFix`）
6. 列表渲染必须指定 `wx:key`
7. 覆盖所有状态：加载中 / 空数据 / 错误 / 正常
8. 响应码：`code === 200` 成功（取 `data`），`code === 250` 业务警告（提示 `content`），`code === 401` 未授权（跳登录），`code === 220` 需审核，`code === 404` 找不到
9. 错误提示优先取 `err.content`，成功数据统一从 `res.data` 读取；`checkaccount` 接口特殊：`code === 1` 可用、`code === 0` 已存在
10. 金额字段统一 `Number(x).toFixed(2)` 保留两位小数；分页默认每页 12 条（个别接口按后端默认值），触底加载 `page++`
11. 尺寸单位统一使用 `rpx`（750rpx = 屏幕宽度）；图片必须设置 `mode`
12. 代码遵循微信小程序最新基础库规范，纯原生 wx，无第三方框架依赖，可直接导入微信开发者工具运行
