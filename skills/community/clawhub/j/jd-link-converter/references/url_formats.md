# 京东链接格式参考

## URL 格式对照

| 类型 | URL 格式 | 示例 |
|------|----------|------|
| 短链接 (3.cn) | `https://3.cn/{shortCode}` | `https://3.cn/2RKwn3-g` |
| 短链接 (u.jd.com) | `https://u.jd.com/{shortCode}` | `https://u.jd.com/abc123` |
| 移动端商品页 | `https://item.m.jd.com/product/{id}.html?{params}` | `https://item.m.jd.com/product/100198170140.html?utm_source=...` |
| 移动端商品页(变体) | `https://item.m.jd.com/{id}.html?{params}` | (较少见) |
| PC端商品页 | `https://item.jd.com/{id}.html` | `https://item.jd.com/100198170140.html` |
| PC端商品页(含参数) | `https://item.jd.com/{id}.html?{params}` | `https://item.jd.com/100198170140.html?cu=true` |

## 短链接解析流程

```
用户分享短链接 (3.cn / u.jd.com)
    |
    v
HTTP GET 请求，模拟京东App UA，跟踪 302 重定向
    |
    v
得到移动端长链接 (item.m.jd.com/product/{id}.html?utm_*=...)
    |
    v
正则提取商品ID: /(\d{6,12})\.html/
    |
    v
拼接PC端链接: https://item.jd.com/{id}.html
```

## 短链接跳转携带的参数

移动端长链接通常携带大量UTM追踪参数：

| 参数 | 含义 |
|------|------|
| `utm_source` | 分享来源 (androidapp / iosapp / wechatapp 等) |
| `utm_medium` | 分享媒介 (appshare / CopyURL 等) |
| `utm_campaign` | 活动标识 (如 t_335139774) |
| `utm_term` | 分享追踪ID |
| `utm_user` | 用户标识 (如 plusmember) |
| `ad_od` | 广告类型 (如 share) |
| `gx` / `gxd` | 追踪校验参数 |
| `ShareTm` | 分享时间戳加密串 |
| `dl_abtest` | AB测试标识 |

这些参数在PC端链接中全部不需要，转换时丢弃即可。

## 常见短链接域名

| 域名 | 说明 |
|------|------|
| `3.cn` | 京东主短链接域名，最常见 |
| `u.jd.com` | 京东备用短链接域名 |
| `re.jd.com` | 京东推广短链接（较少见） |

## 商品ID规律

- 商品ID为纯数字，通常6-12位
- 新品ID较长（如 100198170140），老品ID较短（如 1000400）
- PC端URL路径格式: `/{id}.html`（无 `/product/` 前缀）
- 移动端URL路径格式: `/product/{id}.html`（有 `/product/` 前缀）
