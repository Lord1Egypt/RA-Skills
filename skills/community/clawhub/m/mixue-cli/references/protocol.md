# 协议细节（逆向）

BASE = `https://mxsa.mxbc.net`，APPID = `d82be6bbc1da11eb9dd000163e122ecb`。
小程序 appid `wx7696c66d2245d107`。

> **版本**：本文 2026-10-28 依据一次真实小程序抓包（Reqable，172 条请求，小程序 v2.8.64）校对。
> 标注 🆕 的是本次新增确认的端点。CLI 的实现**没有改动**（现有签名与端点实测仍可用）。

## 鉴权

请求头带三样：

```
Access-Token: <JWT，195 字符>          # 登录态，~/mixue/tools/token.txt
x-ssos-cid:  <customerId>              # 如 <你的customerId>，可选但建议带
version:     2.8.64                    # 小程序版本号
```

`Access-Token` 失效返回 `{"code":401,"msg":"Access-Token失效，请重新登录"}`。
获取途径（按省事程度）：
1. 用户在小程序里操作 → 抓包 HAR → 取任一请求的 `Access-Token` 头（去重后通常只有一个）
2. `login --phone <手机> --code <验证码>`（需短信，验证码不进聊天）

## 签名算法（CLI 现行，仍有效）

```
sign = base64url_nopad( RSA_PKCS1_v1_5_SHA256( canonical ) )
canonical = 把「query 业务参数 + JSON body 全部字段 + appId + t」按 key 排序拼 k=v&...
            嵌套对象/数组按其紧凑 JSON 字符串参与排序
appId = d82be6bbc1da11eb9dd000163e122ecb ,  t = 13 位毫秒时间戳
```

即：body 字段也参与签名（漏了 body 字段会报 4003 invalid sign）。

### ⚠️ 新版本签名可能已换算法（只记录，别跟风改）

抓包里小程序发的 body 字段是 `业务字段 + appId + t + s + sign`：

```
t      = 1793189127104      # 13 位毫秒
s      = 3                  # 疑似签名版本/类型
sign   = 69 字符，形如 9b1c3e32…（hex 风格）
```

69 字符**不是** CLI 那套 RSA base64url（2048 位 RSA 应为 ~342 字符），说明小程序新版可能改成了短摘要签名。
但 CLI 用 RSA 方式实测 `menu` / `order` 全部返回 200，**所以不要因为抓包长这样就改实现**。
真遇到 4003 大面积失败时，再回头对比 `s` 与 `sign` 的生成方式。

## 端点（POST 为主，body 都参与签名）

### 门店 / 菜单
- 查店（CLI 用）：`/api/v2/shopinfo/findNear` {latitude, longitude}
- 🆕 推荐店：`/api/v3/shopinfo/findRecommend`、`/api/v4/shopinfo/findRecommend` {longitude, latitude}
- 门店详情：🆕 `/api/v2/shopinfo/get/{shopId}`
- 菜单：`/api/v3/shop/menu/info` {shopId, orderType}
- 🆕 菜单扩展：`/api/v2/shop/v2/menu/extInfo` {shopId, orderType}
- 🆕 营销菜单：`/api/v1/marketingMenu/query` {shopId, orderType}
- 🆕 热销：`/api/v1/hotProduct/list` {channelType, shopId}
- 🆕 搜索词：`/api/v1/searchWord/list` {channelType, shopId}
- 🆕 门店营销位：`/api/v2/shop/listMarketing` {shopId, orderType}
- 🆕 赠品角标：`/api/v2/shop/giftProduct/corner?shopId=&orderType=`（GET）

### 购物车 / 算价
- 加购：`/api/v3/shoppingCart/addProduct` {shopId, productId, productAmount, modifiedTime}（modifiedTime 取自菜单商品）
- 算价：`/api/v3/shoppingCart/calcprice` {shopId, orderType, takeType, orderChannel}
- 清空：`/api/v3/shoppingCart/clearCart`
- 🆕 购物车列表：`/api/v3/shoppingCart/listCartProducts` {shopId, orderType, useProductVoucherMode, useCouponMode, plusDiscount…}
- 🆕 结算更新：`/api/v3/shoppingCart/settlement/update` {shopId, orderType, takeType, plusDiscountProductList, useWalletPay…}
- 🆕 结算营销：`/api/v3/shoppingCart/settlement/marketing/list` {shopId, orderType, marketingTypes}
- 🆕 拼单购物车：`/api/v1/groupcart/info`（GET）

### 下单 / 支付 / 取餐
- 建单：`/api/v2/order/save`（见 SKILL 的 8003 坑：channel=2+miniProgType=1+券字段）
- 取消：`/api/v2/order/cancel` {orderCode}
- 订单列表：`/api/v2/order/cust/list` {type, pageNum, pageSize}
- 聚合支付：`/api/v2/order/prepay` {orderCode, payType, openId}（真正扣款；CLI 只生成参数不直接付）
- 取餐号：`/api/v2/order/getTakeNo` {orderCode}（🆕 抓包里是 **GET** + query）

### 券 / 营销 / 会员
- 🆕 可用券：`/api/v1/customercoupons/availableCouponsNew` {shopId, orderType, discountAmount, goodsList, pageNumber, pageSize}
- 🆕 券总数：`/api/v1/customercoupons/total`、`/api/v1/customercoupons/shopTotal` {shopId, menuScenario}
- 🆕 抽奖包：`/ordact/api/v1/luck-pack/info` {shopId, orderType}
- 🆕 积分任务：`/ordact/api/v1/accumulatePoint/taskArea/info`、`/ordact/api/v1/accumulatePoint/querySchedule` {shopIds, orderType}
- 🆕 下单得积分预览：`/api/v1/customer/v2/getOrderPointAndGrowth` {pageType, actualPayAmount}
- 🆕 会员信息：`/api/v1/customer/info`（GET）
- 🆕 钱包余额：`/api/v1/wallet/balance`（GET）
- 🆕 礼品卡：`/api/v1/giftcard/summary`（GET）
- 🆕 首页活动区 / 广告位 / 推荐买：`/api/v1/homeActivityArea/query`、`/api/v1/adinfo/adplace/queryNew`、`/api/v1/adinfo/recommendBuy/query`
- 🆕 订阅消息：`/submsg/webapp/v1/subscribe/listTemplate`、`/submsg/webapp/v1/subscribe/wechat/report`
- 🆕 导航/版本/配置：`/api/v1/app/nav`、`/api/v1/app/version`、`/api/v1/app/config`

枚举（实测有效）：orderType=1 自取、takeType=1、orderChannel=2 小程序(+miniProgType=1)。

## 错误码

| code | 含义 | 处理 |
|---|---|---|
| 0 | 成功 | — |
| 4002 | sign expired | 重发（CLI 自动带新 t） |
| 4003 | invalid sign | 签名参数没带全，body 字段也要参与签名 |
| 4000 | 参数校验失败 | 看 msg，字段/枚举不对（如漏 miniProgType） |
| 401 | Access-Token 不能为空/失效 | 设 token |
| 7041 | 人机验证不通过 | 短信接口要验证码 token，脚本发不了 |
| 8002 | 商品信息变更 | 加购带 modifiedTime |
| 8003 | 优惠价格变更 | 见 SKILL：channel 或券字段问题 |
| 8004 | 购物车信息不存在 | 先 addProduct 再下单 |
| 7009 | 重复取消 | 订单已取消过 |

## 支付跳转

小程序 appid `wx7696c66d2245d107`，收银台页 `pages/order_detail/pay/index`。
`paylink` 生成 weixin:// scheme + H5 redirect + 二维码；用户微信扫一扫在收银台确认才真正扣款。

## 从 HAR 取 token（实测流程）

用户发来 HAR 后：

```python
# 1. 找任意带 Access-Token 的请求，去重（通常只有一个）
# 2. 写入 token.txt（0600）
# 3. 验证：mixue_cli.py whoami → 应显示真实手机号
```

HAR 里含完整凭据，**等于账号钥匙**：处理完提醒用户删掉，不要转发。
