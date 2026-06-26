# ip-api.com API 字段参考

## 基础信息

| 字段 | 说明 | 示例 |
|------|------|------|
| `status` | 查询状态 | success / fail |
| `query` | 查询的 IP | 8.8.8.8 |
| `message` | 错误信息（仅失败时） | "reserved range" |

## 地理位置

| 字段 | 说明 | 示例 |
|------|------|------|
| `country` | 国家名称 | 美国 |
| `countryCode` | 国家代码 | US |
| `region` | 省/州代码 | CA |
| `regionName` | 省/州全名 | California |
| `city` | 城市 | Mountain View |
| `zip` | 邮编 | 94035 |
| `lat` | 纬度 | 37.386 |
| `lon` | 经度 | -122.0838 |

## 网络信息

| 字段 | 说明 | 示例 |
|------|------|------|
| `timezone` | 时区 | America/Los_Angeles |
| `isp` | 网络服务提供商 | Google LLC |
| `org` | 组织名称 | Public DNS |
| `as` | AS 号 | AS15169 Google LLC |
| `asname` | AS 名称 | GOOGLE |
| `mobile` | 是否移动网络 | true / false |
| `proxy` | 是否代理 | true / false |
| `hosting` | 是否托管服务 | true / false |

## fields 参数值

使用 `fields` 参数可以指定返回的字段，常用值：

| 值 | 说明 |
|----|------|
| `61439` | 所有字段（推荐） |
| `country,city` | 仅国家和城市 |
| `country,city,isp` | 国家、城市、ISP |
| `query,country,city,lat,lon` | 自定义字段组合 |

## 请求示例

```bash
# 所有字段
curl "ip-api.com/json/8.8.8.8?fields=61439"

# 仅国家和城市
curl "ip-api.com/json/8.8.8.8?fields=country,city"

# 自定义字段
curl "ip-api.com/json/8.8.8.8?fields=query,country,city,isp"

# JSON 格式（默认）
curl "ip-api.com/json/8.8.8.8"

# XML 格式
curl "ip-api.com/xml/8.8.8.8"

# 纯文本
curl "ip-api.com/txt/8.8.8.8"
```

## 速率限制

| 类型 | 限制 |
|------|------|
| 每分钟 | 60 次请求 |
| 每天 | 4500 次请求 |

**注意：** 超出限制会返回 429 错误

## 保留 IP 范围

以下 IP 无法查询（会返回错误）：

- `127.0.0.0/8` — 本地回环
- `10.0.0.0/8` — 私有网络 A 类
- `172.16.0.0/12` — 私有网络 B 类
- `192.168.0.0/16` — 私有网络 C 类
- `169.254.0.0/16` — 链路本地

## 付费版功能

免费版限制较多，商业用途建议购买付费版：

- 更高的速率限制
- HTTPS 支持
- 更精确的位置
- 商业用途许可

官网：https://ip-api.com/
