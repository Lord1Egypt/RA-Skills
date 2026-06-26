---
name: ip-locator
description: 自动获取 IP 地址的归属地信息。支持查询任意 IP 或当前公网 IP。使用 ip-api.com 免费服务，无需 API 密钥。当用户需要查询 IP 位置、网络信息、归属地时触发此技能。
---

# IP 归属地查询技能

## 何时使用

✅ **使用场景：**
- "查询这个 IP 的归属地"
- "我的公网 IP 是多少？在哪里？"
- "192.168.1.1 是哪个国家的？"
- "帮我看看这个 IP 的详细信息"
- 网络安全分析、日志排查

❌ **不使用场景：**
- 内网 IP 定位（内网 IP 无地理位置）
- 需要精确到街道级别的位置
- 商业用途（免费版有速率限制）
- 批量查询大量 IP（需购买付费 API）

## 快速命令

### 查询当前公网 IP
```bash
curl -s "ip-api.com/json/?fields=61439"
```

### 查询指定 IP
```bash
curl -s "ip-api.com/json/8.8.8.8?fields=61439"
```

### 简洁输出（仅国家 + 城市）
```bash
curl -s "ip-api.com/json/8.8.8.8?fields=country,city"
```

## 脚本使用

```bash
# 查询指定 IP
./scripts/ip-lookup.sh 8.8.8.8

# 查询当前公网 IP
./scripts/ip-lookup.sh

# 批量查询
./scripts/ip-lookup.sh 8.8.8.8 1.1.1.1 208.67.222.222
```

## API 字段说明

`fields=61439` 包含以下信息：
- `status` — 查询状态
- `country` — 国家
- `countryCode` — 国家代码
- `region` — 省/州
- `regionName` — 省/州全名
- `city` — 城市
- `zip` — 邮编
- `lat` — 纬度
- `lon` — 经度
- `timezone` — 时区
- `isp` — 网络服务提供商
- `org` — 组织
- `as` — AS 号
- `query` — 查询的 IP

## 输出示例

```json
{
  "status": "success",
  "country": "美国",
  "countryCode": "US",
  "region": "CA",
  "regionName": "California",
  "city": "Mountain View",
  "zip": "94035",
  "lat": 37.386,
  "lon": -122.0838,
  "timezone": "America/Los_Angeles",
  "isp": "Google LLC",
  "org": "Public DNS",
  "as": "AS15169 Google LLC",
  "query": "8.8.8.8"
}
```

## 注意事项

- ⚠️ 免费版限制：每分钟 60 次查询，每天 4500 次
- ⚠️ 内网 IP（如 192.168.x.x）无法定位
- ⚠️ 位置信息是估算值，非精确位置
- ✅ 无需 API 密钥
- ✅ 支持 IPv4 和 IPv6
- ✅ 商业使用需购买付费版

## 相关资源

- 详细字段说明：见 `references/fields.md`
- API 文档：https://ip-api.com/docs/
