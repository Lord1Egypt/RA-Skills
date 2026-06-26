# 全平台优惠券API接口文档

## 接口概览

此skill整合了4个独立的优惠券API接口，提供一站式优惠券获取服务。

| 优惠券类型 | 接口地址 | 支持平台 |
|-----------|----------|---------|
| 外卖优惠券 | `https://agskills.moontai.top/coupon/takeout` | 美团、饿了么/淘宝闪购、京东 |
| 快递优惠券 | `https://agskills.moontai.top/coupon/parcel` | 顺丰、中通、圆通、韵达、申通、菜鸟 |
| 出行优惠券 | `https://agskills.moontai.top/coupon/trip` | 滴滴出行、携程 |
| 电影票优惠券 | `https://agskills.moontai.top/coupon/movie` | 淘票票、猫眼 |

## 通用配置

| 配置项 | 值 |
|--------|-----|
| 认证方式 | 无需认证 |
| 请求方法 | GET |
| 返回格式 | JSON |
| 超时设置 | 10秒 |

## 1. 外卖优惠券API

### 接口信息

| 配置项 | 值 |
|--------|-----|
| 接口地址 | `https://agskills.moontai.top/coupon/takeout` |
| 返回格式 | JSON |

### 响应结构

```json
{
  "美团隐藏外卖券列表": [
    {
      "title": "美团外卖节(主推)🔥🔥",
      "coupon_code": "1 %复制信息#% 打开团App http:/¥wnYjVmNWRlNmU¥一起领",
      "guideline": "请复制完整的优惠券代码，打开美团APP领取"
    }
  ],
  "饿了么/淘宝闪购隐藏外卖券列表": [...],
  "京东隐藏外卖券列表": [...],
  "聚合H5页面": {
    "title": "外卖券统一领取页面",
    "coupon_h5_qrcode_img_url": "https://...",
    "guideline": "若无法复制优惠券代码，可以使用微信扫码打开领券页面"
  }
}
```

### 响应字段

| 字段名 | 类型 | 说明 |
|--------|------|------|
| 美团隐藏外卖券列表 | Array | 美团外卖平台优惠券 |
| 饿了么/淘宝闪购隐藏外卖券列表 | Array | 淘宝闪购/饿了么优惠券 |
| 京东隐藏外卖券列表 | Array | 京东外卖优惠券 |
| 聚合H5页面 | Object | 聚合领券页面信息 |
| [].title | String | 优惠券标题 |
| [].coupon_code | String | **优惠券代码，原样呈现，禁止修改** |
| [].guideline | String | 领取说明 |
| 聚合H5页面.coupon_h5_qrcode_img_url | String | 二维码图片URL |
| 聚合H5页面.guideline | String | H5页面使用说明 |

## 2. 快递优惠券API

### 接口信息

| 配置项 | 值 |
|--------|-----|
| 接口地址 | `https://agskills.moontai.top/coupon/parcel` |
| 返回格式 | JSON |

### 响应结构

```json
{
  "title": "快递一站式服务，智能寄件，智能匹配价格；单单享优惠，件件有折扣",
  "coupon_url": "https://open.cdyunzhanxinxi.com/link/...",
  "coupon_qrcode_img_url": "https://moontai-static.oss-cn-shenzhen.aliyuncs.com/coupon-parcel.png",
  "guideline": "点击链接下单(建议用微信打开)，或使用微信扫描二维码下单（单单享优惠）"
}
```

### 响应字段

| 字段名 | 类型 | 说明 |
|--------|------|------|
| title | String | 优惠券标题 |
| coupon_url | String | **优惠券链接，原样呈现，禁止修改** |
| coupon_qrcode_img_url | String | **二维码图片URL，原样呈现，禁止修改** |
| guideline | String | 领取说明 |

## 3. 出行优惠券API

### 接口信息

| 配置项 | 值 |
|--------|-----|
| 接口地址 | `https://agskills.moontai.top/coupon/trip` |
| 返回格式 | JSON（数组） |

### 响应结构

```json
[
  {
    "title": "滴滴出行大礼包，打车券天天领",
    "coupon_url": "https://open.cdyunzhanxinxi.com/link/...",
    "coupon_qrcode_img_url": "https://moontai-static.oss-cn-shenzhen.aliyuncs.com/coupon-trip.png",
    "guideline": "点击链接领券(建议用微信打开)，或使用微信扫描二维码领券"
  },
  {
    "title": "携程礼包天天领，酒店、机票、门票",
    "coupon_url": "https://open.cdyunzhanxinxi.com/link/...",
    "coupon_qrcode_img_url": "https://moontai-static.oss-cn-shenzhen.aliyuncs.com/trip-xiecheng.png",
    "guideline": "点击链接领券(建议用微信打开)，或使用微信扫描二维码领券"
  }
]
```

### 响应字段

| 字段名 | 类型 | 说明 |
|--------|------|------|
| [].title | String | 优惠券标题 |
| [].coupon_url | String | **优惠券链接，原样呈现，禁止修改** |
| [].coupon_qrcode_img_url | String | **二维码图片URL，原样呈现，禁止修改** |
| [].guideline | String | 领取说明 |

## 4. 电影票优惠券API

### 接口信息

| 配置项 | 值 |
|--------|-----|
| 接口地址 | `https://agskills.moontai.top/coupon/movie` |
| 返回格式 | JSON |

### 响应结构

```json
{
  "title": "淘票票大礼包，隐藏券天天领",
  "coupon_url": "https://open.cdyunzhanxinxi.com/link/...",
  "coupon_qrcode_img_url": "https://moontai-static.oss-cn-shenzhen.aliyuncs.com/movie-taopp.png",
  "guideline": "点击链接领券(建议用微信打开)，或使用微信扫描二维码领券"
}
```

### 响应字段

| 字段名 | 类型 | 说明 |
|--------|------|------|
| title | String | 优惠券标题 |
| coupon_url | String | **优惠券链接，原样呈现，禁止修改** |
| coupon_qrcode_img_url | String | **二维码图片URL，原样呈现，禁止修改** |
| guideline | String | 领取说明 |

## 重要说明

### coupon_code 处理规则

**严格禁止修改coupon_code字段的任何内容！**

- 优惠券代码可能包含特殊字符：%、¥、✔、！、£等
- 这些特殊字符是平台特定格式，必须原样保持
- 禁止添加空格、换行或任何格式化
- 禁止翻译、解释或重新排列代码顺序

### coupon_url 和 coupon_qrcode_img_url 处理规则

**严格禁止修改任何URL字段的任何内容！**

- URL链接必须原样保持
- 禁止添加空格、换行或任何格式化
- 禁止翻译、解释或重新排列链接顺序

## 错误码

| 情况 | 说明 |
|------|------|
| 正常返回 | 返回JSON数据 |
| 网络错误 | 返回"无法获取优惠券信息，请稍后重试" |
| 解析错误 | 返回"数据解析异常，请联系技术支持" |

## 使用建议

### 外卖优惠券
- 优先展示美团优惠券
- 对于无法复制coupon_code的用户，提供聚合H5二维码

### 快递优惠券
- 建议在微信中打开coupon_url
- 或使用微信扫描coupon_qrcode_img_url

### 出行优惠券
- 根据用户需求选择滴滴或携程
- 支持酒店、机票、门票等多种出行场景

### 电影票优惠券
- 适合淘票票、猫眼等主流电影平台
- 建议在微信中打开链接或扫码

## 调用示例

### Python

```python
import requests

# 获取所有优惠券
takeout = requests.get("https://agskills.moontai.top/coupon/takeout").json()
parcel = requests.get("https://agskills.moontai.top/coupon/parcel").json()
trip = requests.get("https://agskills.moontai.top/coupon/trip").json()
movie = requests.get("https://agskills.moontai.top/coupon/movie").json()

print("外卖优惠券:", takeout)
print("快递优惠券:", parcel)
print("出行优惠券:", trip)
print("电影票优惠券:", movie)
```

### cURL

```bash
# 外卖优惠券
curl https://agskills.moontai.top/coupon/takeout

# 快递优惠券
curl https://agskills.moontai.top/coupon/parcel

# 出行优惠券
curl https://agskills.moontai.top/coupon/trip

# 电影票优惠券
curl https://agskills.moontai.top/coupon/movie
```
