---
name: kuaidaili
description: 快代理(Kuaidaili)代理IP服务集成。Use when you need to (1) fetch proxy IPs from Kuaidaili API, (2) check account balance, (3) manage proxy orders, (4) test proxy connectivity. Triggers on phrases like "快代理", "kuaidaili", "获取代理IP", "proxy pool", "代理池".
---

# 快代理 (Kuaidaili) Skill

集成快代理API，提供代理IP获取、账户管理等功能。

## 配置

在使用前，需要设置环境变量或在脚本中配置：

```bash
# 环境变量方式（推荐）
export KUAIDAILI_SECRET_ID="your_secret_id"
export KUAIDAILI_SIGNATURE="your_signature"

# 或在调用脚本时传入参数
python scripts/get_proxies.py --secret-id YOUR_ID --signature YOUR_SIG
```

获取密钥：
1. 登录快代理用户中心
2. 进入"订单管理" → "API接口"
3. 生成API链接，提取 `secret_id` 和 `signature`

## 主要功能

### 1. 获取代理IP

```bash
# 获取10个私密代理IP（JSON格式）
python scripts/get_proxies.py --num 10 --format json

# 获取5个独享代理IP（文本格式）
python scripts/get_proxies.py --type dedicated --num 5 --format text

# 指定地区
python scripts/scripts/get_proxies.py --area 北京 --num 10
```

### 2. 查询账户余额

```bash
python scripts/check_balance.py
```

### 3. 测试代理连接

```bash
python scripts/test_proxy.py --proxy "http://user:pass@ip:port"
```

## 代理类型

- **私密代理** (`private`): 高匿名、高可用
- **独享代理** (`dedicated`): 专属IP、稳定性高
- **隧道代理** (`tunnel`): 按流量计费、自动切换

## 常用参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--num` | 获取IP数量 | 10 |
| `--format` | 返回格式 (json/text) | json |
| `--area` | 指定地区 | 不限 |
| `--protocol` | 协议类型 (http/https/socks5) | http |
| `--sep` | 分隔符 (1=\n, 2=\r, 3=空格) | 1 |

## API参考

详细API文档见 [references/api_reference.md](references/api_reference.md)

## 错误处理

常见错误码：
- `1001`: 参数错误
- `1002`: 认证失败
- `1003`: 余额不足
- `1004`: 订单不存在

## 示例：爬虫集成

```python
import requests
import json

# 获取代理
resp = requests.get("https://dev.kdlapi.com/api/getproxy", params={
    "secret_id": "your_id",
    "signature": "your_sig",
    "num": 10,
    "format": "json"
})
proxies_data = resp.json()

# 使用代理
for proxy in proxies_data["data"]["proxy_list"]:
    proxies = {"http": proxy, "https": proxy}
    requests.get("https://httpbin.org/ip", proxies=proxies)
```
