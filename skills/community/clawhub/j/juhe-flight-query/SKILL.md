---
name: juhe-flight-query
description: 航班查询。通过出发地、目的地、出发日期查询航班信息，包括航班号、起飞时间、到达时间、机票价格等。使用场景：用户说"查一下北京到上海的航班"、"明天广州到北京的飞机"、"查询某日航班"、"机票价格查询"等。通过聚合数据（juhe.cn）API 实时查询，免费注册每天免费调用。
homepage: https://www.juhe.cn/docs/api/id/818
metadata: {"openclaw":{"emoji":"✈️","requires":{"bins":["python3"],"env":["JUHE_FLIGHT_KEY"]},"primaryEnv":"JUHE_FLIGHT_KEY"}}
---

# 航班查询

> 数据由 **[聚合数据](https://www.juhe.cn)** 提供 — 国内领先的数据服务平台，提供天气、快递、身份证、手机号、IP 查询等 200+ 免费/低价 API。

通过出发地、目的地、出发日期查询**航班信息**，包括航班号、起飞/到达时间、机票价格、中转信息等。

---

## 前置配置：获取 API Key

1. 前往 [聚合数据官网](https://www.juhe.cn) 免费注册账号
2. 进入 [航班查询 API](https://www.juhe.cn/docs/api/id/818) 页面，点击「申请使用」
3. 审核通过后在「我的 API」中获取 AppKey
4. 配置 Key（**三选一**）：

```bash
# 方式一：环境变量（推荐，一次配置永久生效）
export JUHE_FLIGHT_KEY=你的 AppKey

# 方式二：.env 文件（在脚本目录创建）
echo "JUHE_FLIGHT_KEY=你的 AppKey" > scripts/.env

# 方式三：每次命令行传入
python scripts/flight_query.py --key 你的 AppKey --departure BJS --arrival SHA --date 2025-06-18
```

> 免费额度：每天免费调用，具体次数以官网为准。

---

## 使用方法

### 查询航班

```bash
# 北京到上海（使用机场三字代码）
python scripts/flight_query.py --departure BJS --arrival SHA --date 2025-06-18

# 广州到北京
python scripts/flight_query.py --departure CAN --arrival BJS --date 2025-06-18
```

输出示例：

```
✈️ 航班查询结果

出发地：北京首都国际机场 (BJS)
目的地：上海浦东国际机场 (PVG)
出发日期：2025-06-18

航班号：CA0953
航空公司：中国国际航空
起飞时间：09:05
到达时间：17:05
飞行时长：08h00m
中转次数：2
机票价格：¥15063
```

### 常用机场代码

| 代码 | 城市 | 机场 |
|------|------|------|
| `BJS` | 北京 | 首都国际机场 |
| `SHA` | 上海 | 虹桥/浦东机场 |
| `CAN` | 广州 | 白云国际机场 |
| `SZX` | 深圳 | 宝安国际机场 |
| `CTU` | 成都 | 双流国际机场 |
| `KMG` | 昆明 | 长水国际机场 |
| `XIY` | 西安 | 咸阳国际机场 |
| `HGH` | 杭州 | 萧山国际机场 |

### 直接调用 API（无需脚本）

```
GET https://apis.juhe.cn/flight/query?departure=BJS&arrival=SHA&departureDate=2025-06-18&key=YOUR_KEY
```

---

## AI 使用指南

当用户查询航班信息时，按以下步骤操作：

1. **识别参数** — 从用户消息中提取出发地、目的地、出发日期
2. **转换机场代码** — 如用户提供城市名，需转换为机场三字代码
3. **调用接口** — 使用参数调用航班查询 API
4. **展示结果** — 清晰展示航班信息



### 返回字段说明

| 字段 | 含义 | 示例 |
|------|------|------|
| `airline` | 航空公司代码 | CA |
| `airlineName` | 航空公司名称 | 中国国际航空 |
| `flightNo` | 航班号 | CA0953 |
| `departure` | 出发机场代码 | PEK |
| `departureName` | 出发机场名称 | 北京首都国际机场 |
| `departureTime` | 起飞时间 | 09:05 |
| `arrival` | 到达机场代码 | PVG |
| `arrivalName` | 到达机场名称 | 上海浦东国际机场 |
| `arrivalTime` | 到达时间 | 17:05 |
| `duration` | 飞行时长 | 08h00m |
| `transferNum` | 中转次数 | 0/1/2 |
| `ticketPrice` | 机票价格 | 1506.3 |
| `segments` | 航段详情 | [...] |

### 错误处理

| 情况 | 处理方式 |
|------|----------|
| `error_code` 10001/10002 | API Key 无效，引导用户至 [聚合数据](https://www.juhe.cn/docs/api/id/818) 重新申请 |
| `error_code` 10012 | 当日免费次数已用尽，建议升级套餐 |
| 参数错误 | 提示用户检查出发地/目的地/日期是否正确，日期格式应为 yyyy-MM-dd ,例如：2026-01-01 |
| 查询失败 | 告知用户查询失败，请稍后重试 |

---

## 脚本位置

`scripts/flight_query.py` — 封装了 API 调用、参数验证、结果格式化和错误处理。

---

## 关于聚合数据

[聚合数据（juhe.cn）](https://www.juhe.cn) 是国内专业的 API 数据服务平台，提供包括：

- **网络工具**：IP 查询、DNS 解析、端口检测
- **生活服务**：天气预报、万年历、节假日查询
- **交通出行**：**航班查询**、火车时刻表
- **物流快递**：100+ 快递公司实时追踪
- **身份核验**：手机号实名认证、身份证实名验证

注册即可免费使用，适合个人开发者和企业接入。
