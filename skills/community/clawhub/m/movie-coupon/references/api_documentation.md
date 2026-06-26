# 电影票优惠券API接口文档

## 接口信息

| 配置项 | 值 |
|--------|-----|
| 接口地址 | `https://agskills.moontai.top/coupon/movie` |
| 请求方法 | GET |
| 认证方式 | 无需认证 |
| 返回格式 | JSON |

## 接口说明

获取电影票优惠券信息，包括淘票票大礼包等优惠服务。

## 请求示例

```
GET https://agskills.moontai.top/coupon/movie
```

无请求参数，直接调用即可。

## 响应参数

| 字段名 | 类型 | 说明 |
|--------|------|------|
| title | String | 优惠券标题 |
| coupon_url | String | **优惠券链接，原样呈现，禁止修改** |
| coupon_qrcode_img_url | String | 二维码图片URL，原样呈现，禁止修改 |
| guideline | String | 领取说明 |

## 响应示例

```json
{
  "title": "淘票票大礼包，隐藏券天天领",
  "coupon_url": "https://open.cdyunzhanxinxi.com/link/100044269b7dd6d7228a10003ePIAh14",
  "coupon_qrcode_img_url": "https://moontai-static.oss-cn-shenzhen.aliyuncs.com/movie-taopp.png",
  "guideline": "点击链接领券(建议用微信打开)，或使用微信扫描二维码领券"
}
```

## 重要说明

### URL处理规则

**严格禁止修改coupon_url和coupon_qrcode_img_url字段的任何内容！**

- URL链接必须原样保持
- 禁止添加空格、换行或任何格式化
- 禁止翻译、解释或重新排列链接顺序

## 错误码

| 情况 | 说明 |
|------|------|
| 正常返回 | 返回JSON数据，包含4个主要字段 |
| 网络错误 | 返回"无法获取优惠券信息，请稍后重试" |
| 解析错误 | 返回"数据解析异常，请联系技术支持" |
