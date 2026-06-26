# 快代理 API 参考文档

## 概述

快代理提供RESTful API，支持获取代理IP、查询余额、管理订单等功能。

## 认证

所有API请求需要携带认证参数：

| 参数 | 说明 | 获取方式 |
|------|------|----------|
| `secret_id` | 密钥ID | 用户中心 → API接口 |
| `signature` | 签名 | 用户中心 → API接口 |

## API端点

### 1. 获取私密代理IP

```
GET https://dps.kdlapi.com/api/getdps/
```

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| secret_id | string | 是 | 密钥ID |
| signature | string | 是 | 签名 |
| num | int | 是 | 获取数量 (1-100) |
| format | string | 否 | 返回格式 (json/text) |
| area | string | 否 | 地区筛选 |
| protocol | string | 否 | 协议类型 (http/https/socks5) |
| sep | int | 否 | 分隔符 (1=\n, 2=\r, 3=空格) |
| dedup | int | 否 | 去重 (1=当天去重) |
| orderby | string | 否 | 排序方式 |

**响应示例 (JSON)：**

```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "proxy_list": [
      "http://58.218.92.60:13929",
      "http://58.218.92.60:13930"
    ],
    "order_count": 100
  }
}
```

### 2. 获取隧道代理IP

```
GET https://tps.kdlapi.com/api/gettps/
```

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| secret_id | string | 是 | 密钥ID |
| signature | string | 是 | 签名 |
| num | int | 是 | 获取数量 |
| format | string | 否 | 返回格式 |

### 3. 查询账户余额

```
GET https://dev.kdlapi.com/api/getaccountbalance
```

**响应示例：**

```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "balance": 100.50,
    "available_balance": 80.00
  }
}
```

### 4. 查询订单信息

```
GET https://dev.kdlapi.com/api/getorderinfo
```

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| secret_id | string | 是 | 密钥ID |
| signature | string | 是 | 签名 |
| order_id | string | 否 | 订单号 (不传则查询所有) |

### 5. 设置IP白名单

```
POST https://dev.kdlapi.com/api/setipwhitelist
```

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| secret_id | string | 是 | 密钥ID |
| signature | string | 是 | 签名 |
| ip_list | string | 是 | IP列表 (逗号分隔) |

## 错误码

| 错误码 | 说明 |
|--------|------|
| 0 | 成功 |
| 1001 | 参数错误 |
| 1002 | 认证失败 |
| 1003 | 余额不足 |
| 1004 | 订单不存在 |
| 1005 | IP不在白名单 |
| 1006 | 请求频率超限 |
| 1007 | 账户异常 |

## 速率限制

- 获取IP: 1次/秒
- 查询余额: 10次/分钟
- 其他接口: 5次/秒

## SDK下载

官方提供多语言SDK：
- Python: `pip install kuaidaili`
- Node.js: `npm install kuaidaili`
- Java/Golang/PHP/C#: 见官方文档

## 更多资源

- 官方文档: https://www.kuaidaili.com/doc/
- GitHub SDK: https://github.com/kuaidaili
