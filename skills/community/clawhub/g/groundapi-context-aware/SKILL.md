---
name: groundapi-context-aware
description: Context-aware daily assistant — weather, packages, IP, tax calculator, calendar, fuel prices, traffic restrictions, and daily briefing. Powered by GroundAPI MCP tools (7 life + 2 info tools).
metadata:
  openclaw:
    requires:
      env: ["GROUNDAPI_KEY"]
    emoji: "🌤️"
    homepage: "https://groundapi.net"
    primaryEnv: "GROUNDAPI_KEY"
---

# 情境感知生活助手

当用户进行日常问候、询问天气、查快递、查 IP、算个税、查日历、查油价、查限行，或类似以下表达时自动触发：
- "今天天气怎么样"、"需要带伞吗"、"这周天气如何"
- "我的快递到哪了"、"帮我查一下运单号 XXX"
- "我现在在哪"、"帮我查一下这个 IP"
- "月薪两万到手多少"、"帮我算一下个税"
- "今天农历多少"、"五一放几天"、"今天股市开吗"
- "现在油价多少"、"92号汽油多少钱"
- "今天限号吗"、"北京限行尾号"
- "早上好"、"今天穿什么合适"
- "今天有什么新闻"、"现在什么最火"

## 前置条件

本 Skill 依赖 GroundAPI MCP Server 提供的工具。确保已配置 GroundAPI MCP 连接：

```json
{
  "mcpServers": {
    "groundapi": {
      "url": "https://mcp.groundapi.net/mcp",
      "headers": {
        "X-API-Key": "sk_gapi_xxxxx"
      }
    }
  }
}
```

## 场景一：天气查询

### 用户指定了城市

直接调用 `life_weather(city="北京", forecast=true)` 获取实时天气 + 7 天预报。

### 用户没指定城市

1. 调用 `life_ip()` 获取用户大致位置（城市）
2. 用返回的城市调用 `life_weather(city="...", forecast=true)`

### 输出格式

```
## 🌤️ {城市} 天气

### 当前
- 天气：{天气状况}
- 温度：{当前温度}°C（体感 {体感温度}°C）
- 湿度：{湿度}% | 风：{风向} {风力}
- 能见度：{能见度}

### 未来 7 天
| 日期 | 天气 | 最高 | 最低 | 建议 |
|------|------|------|------|------|
| 周一 | ☀️ 晴 | 28°C | 15°C | 适合户外 |
| ... |

### 生活建议
- 穿衣：{根据温度和天气给出建议}
- 出行：{是否需要带伞/防晒等}
```

## 场景二：快递追踪

当用户提供运单号时：

1. 调用 `life_logistics(number="SF1234567890")` 追踪物流
2. 如果是顺丰快递且需要验证，提示用户提供收件人手机后四位

### 输出格式

```
## 📦 快递追踪

- 运单号：{number}
- 快递公司：{company}
- 当前状态：{status}

### 物流轨迹
| 时间 | 状态 |
|------|------|
| 04-03 14:30 | 已签收 |
| 04-03 08:15 | 派送中 |
| 04-02 22:00 | 到达 XX 营业部 |
| ... |

预计 {到达时间判断，如果已签收则不显示}
```

## 场景三：IP 地理定位

当用户提到查 IP 或给出一个 IP 地址时：

调用 `life_ip(address="8.8.8.8")` 或 `life_ip()`（查自己）。

### 输出格式

```
## 📍 IP 定位：{IP 地址}

| 信息 | 值 |
|------|-----|
| 国家/地区 | {country} |
| 城市 | {city} |
| 经纬度 | {lat}, {lon} |
| 时区 | {timezone} |
| ISP | {isp} |
```

## 场景四：个税计算

当用户询问到手工资、个税时：

调用 `life_tax(monthly_salary=20000, insurance=2000, special_deduction=1500)`

参数说明：
- `monthly_salary`：税前月薪
- `insurance`：五险一金（用户没说就用常见比例估算）
- `special_deduction`：专项附加扣除（子女教育/房贷/租房/赡养老人等，用户没说就设为 0）

### 输出格式

```
## 💰 个税计算

| 项目 | 金额 |
|------|------|
| 税前月薪 | ¥XX,XXX |
| 五险一金 | -¥X,XXX |
| 专项附加扣除 | -¥X,XXX |
| 起征点 | -¥5,000 |
| 应纳税所得额 | ¥XX,XXX |
| 个税 | ¥X,XXX |
| **到手** | **¥XX,XXX** |
```

## 场景五：万年历 / 交易日查询

当用户询问农历、节气、节假日、是否交易日时：

调用 `life_calendar()` 或 `life_calendar(date="2026-05-01")`

### 输出格式

```
## 📅 {日期}

| 项目 | 信息 |
|------|------|
| 公历 | YYYY年MM月DD日 星期X |
| 农历 | X月X日 |
| 节气 | {如有} |
| 节假日 | {如有} |
| 是否交易日 | 是/否 |
```

## 场景六：油价查询

当用户询问油价时：

调用 `life_oil_price()` 或 `life_oil_price(province="北京")`

### 输出格式

```
## ⛽ {地区}油价

| 油品 | 价格（元/升） |
|------|-------------|
| 92号汽油 | ¥X.XX |
| 95号汽油 | ¥X.XX |
| 98号汽油 | ¥X.XX |
| 0号柴油 | ¥X.XX |
```

## 场景七：限行查询

当用户询问限号、限行时：

调用 `life_traffic(city="北京")`

如果用户没指定城市，先用 `life_ip()` 定位再查。

### 输出格式

```
## 🚗 {城市}今日限行

- 日期：{YYYY-MM-DD 星期X}
- 限行尾号：{X 和 X}
- 限行时间：{如 7:00-20:00}
- 限行区域：{如 五环以内}
```

## 场景八：日常问候（组合技）

当用户说"早上好"、"今天怎么样"等日常问候时，自动组合多个工具：

1. `life_ip()` → 定位城市
2. `life_weather(city="...", forecast=false)` → 当前天气
3. `life_calendar()` → 今天日期/农历/是否交易日
4. `life_traffic(city="...")` → 限行信息（仅限行城市）
5. `info_trending()` → 当前热搜 Top 5
6. `info_bulletin()` → 每日新闻简报

输出一段自然的问候回复，包含天气、日历、限行提醒、热点新闻摘要，语气轻松友好。

## 注意事项

- IP 定位精度有限（通常到城市级别），不要声称是精确位置
- 天气数据来自和风天气，支持中英文城市名
- 快递公司通常可自动识别，无需用户指定
- 顺丰快递比较特殊，需要收件人手机后四位验证
- 个税计算基于中国大陆最新税率表
- 限行政策因城市而异，部分城市无限行
- 输出语言跟随用户
