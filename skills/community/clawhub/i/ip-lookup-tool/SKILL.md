---
name: ip-lookup-tool
description: 查询当前公网 IP、城市位置（含中文名）和运营商。当用户问“我的 IP 是多少”“我现在的 IP 地址”“我在哪个城市上网”这类问题时使用。优先返回公网出口 IP，而不是局域网 IP。
---

# IP Lookup Tool

当用户问这些问题时，触发本 skill：

- 我的 IP 是多少
- 我现在的 IP 地址
- 看看我现在在哪个城市上网
- 查一下当前公网 IP 和位置

## 行为原则

- 返回 **公网出口 IP**（如 `23.x.x.x`），不要返回 192.168/10.x 这类内网地址
- 使用轻量免鉴权接口，例如 `https://ipinfo.io/json` 等
- 只做一次 HTTP 请求，优先顺序：
  1. `https://ipinfo.io/json`
  2. `https://ifconfig.co/json`
  3. `https://api.ip.sb/geoip`
- 若主源失败，自动降级到下一源
- 不要对精确位置做过度解读，只提供大致城市/国家信息
- 明确说明“这是公网出口 IP，不一定等于本机局域网 IP”

## 脚本说明

脚本路径：`skills/ip-lookup/scripts/ip_lookup.js`

用途：查询当前会话出口的公网 IP 和大致位置。

调用示例：

```bash
node skills/ip-lookup/scripts/ip_lookup.js
```

输出（人类可读）：

```text
公网 IP：23.249.16.36
城市：新宿区（Tokyo, JP）
运营商：AS400618 Prime Security Corp.
```

如需要 JSON（例如后续程序处理），可使用：

```bash
node skills/ip-lookup/scripts/ip_lookup.js --json
```

返回字段：

- `ip`：公网 IP 地址
- `city`：英文城市（若有）
- `cityZh`：中文城市/区县（best-effort，若有）
- `region`：地区/省份（若有）
- `country`：国家代码
- `org`：运营商/自治系统信息（若有）
- `loc`：经纬度字符串（若有）
- `source`：实际使用的接口来源
- `fetchedAt`：ISO 格式查询时间

## 错误处理

- 接口访问失败时，明确说明“暂时无法获取公网 IP”，不要编造 IP 或位置
- 若部分字段缺失（如没有城市），只返回能确定的信息
- 若多次接口都失败，建议用户稍后重试或检查网络
