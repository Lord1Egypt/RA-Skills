---
name: juhe-weather
description: 天气预报查询。查询指定城市的天气情况（温度、湿度、AQI、天气、风向等）及生活指数（穿衣、运动、洗车等）。使用场景：用户说"北京天气怎么样"、"查一下上海天气"、"苏州今天多少度"、"天气预报"、"生活指数"等。通过聚合数据（juhe.cn）API 实时查询，支持城市名称或城市 ID，免费注册即可使用。
homepage: https://www.juhe.cn/docs/api/id/73
metadata: {"openclaw":{"emoji":"🌤️","requires":{"bins":["python3"],"env":["JUHE_WEATHER_KEY"]},"primaryEnv":"JUHE_WEATHER_KEY"}}
---

# 天气预报查询

> 数据由 **[聚合数据](https://www.juhe.cn)** 提供 — 查询温度、湿度、AQI、天气状况、风向等，支持城市名称或城市 ID。

支持三种查询：**天气实况与预报**、**生活指数**、**天气种类列表**。

---

## 前置配置：获取 API Key

1. 前往 [聚合数据官网](https://www.juhe.cn) 免费注册账号
2. 进入 [天气预报 API](https://www.juhe.cn/docs/api/id/73) 页面，点击「申请使用」
3. 审核通过后在「我的API」中获取 AppKey
4. 配置 Key（**三选一**）：

```bash
# 方式一：环境变量（推荐）
export JUHE_WEATHER_KEY=你的AppKey

# 方式二：.env 文件
echo "JUHE_WEATHER_KEY=你的AppKey" > scripts/.env

# 方式三：命令行传入
python scripts/weather.py --key 你的AppKey 北京
```

---

## 使用方法

### 查询城市天气（实况 + 近 5 天预报）

```bash
python scripts/weather.py 北京
python scripts/weather.py 上海
python scripts/weather.py 苏州
```

输出示例（苏州）：

```
🌤️ 苏州 天气

【实况】
  天气: 雾  温度: 12℃  湿度: 83%
  风向: 东北风  5-6级
  AQI: 54

【近5天预报】
  2026-03-24  9/14℃  阴转多云  东北风转北风
  2026-03-25  10/20℃  多云转阴  北风转东南风
  2026-03-26  12/21℃  阴转小雨  东南风转东北风
  2026-03-27  9/15℃  多云转晴  东北风转南风
  2026-03-28  12/21℃  多云  东南风

{
  "success": true,
  "data": {
    "city": "苏州",
    "realtime": {"temperature": "12", "humidity": "83", "info": "雾", "direct": "东北风", "power": "5-6级", "aqi": "54"},
    "future": [
      {"date": "2026-03-24", "temperature": "9/14℃", "weather": "阴转多云", "direct": "东北风转北风"},
      {"date": "2026-03-25", "temperature": "10/20℃", "weather": "多云转阴", "direct": "北风转东南风"},
      {"date": "2026-03-26", "temperature": "12/21℃", "weather": "阴转小雨", "direct": "东南风转东北风"},
      ...
    ]
  }
}
```

### 查询生活指数（穿衣、运动、洗车等）

```bash
python scripts/weather.py 北京 --life
```

### 直接调用 API（无需脚本）

```
# 天气查询
GET http://apis.juhe.cn/simpleWeather/query?key=YOUR_KEY&city=北京

# 生活指数
GET http://apis.juhe.cn/simpleWeather/life?key=YOUR_KEY&city=北京

# 天气种类列表
GET http://apis.juhe.cn/simpleWeather/wids?key=YOUR_KEY
```

---

## 返回字段说明

### 天气实况 (realtime)

| 字段 | 含义 | 示例 |
|------|------|------|
| info | 天气情况 | 晴、多云、阴 |
| temperature | 温度(℃) | 4 |
| humidity | 湿度(%) | 82 |
| direct | 风向 | 西北风 |
| power | 风力 | 3级 |
| aqi | 空气质量指数 | 80 |

### 生活指数 (life)

| 字段 | 含义 |
|------|------|
| chuanyi | 穿衣指数 |
| yundong | 运动指数 |
| ganmao | 感冒指数 |
| xiche | 洗车指数 |
| ziwaixian | 紫外线指数 |
| daisan | 带伞建议 |
| kongtiao | 空调建议 |
| shushidu | 舒适度 |
| diaoyu | 钓鱼指数 |
| guomin | 过敏指数 |

---

## AI 使用指南

当用户询问天气相关信息时，按以下步骤操作：

1. **识别意图** — 查天气实况、未来几天预报、或生活指数
2. **提取城市** — 从用户消息提取城市名称（如「北京」「上海」）
3. **调用脚本或 API** — city 参数需 UTF-8 URL 编码
4. **展示结果** — 突出温度、天气、AQI；生活指数用表格或列表

### 错误处理

| 情况 | 处理方式 |
|------|----------|
| 207301 | 错误的查询城市名，检查城市名称是否正确 |
| 207302 | 查询不到该城市相关信息，尝试换城市名或城市 ID |
| 207303 | 网络错误，建议重试 |
| 10001/10002 | API Key 无效，引导用户至 [聚合数据](https://www.juhe.cn/docs/api/id/73) 重新申请 |
| 10012 | 请求超过次数限制，建议升级套餐 |

---

## 脚本位置

`scripts/weather.py` — 封装天气查询、生活指数、输出格式化和错误处理。

---

## 关于聚合数据

[聚合数据（juhe.cn）](https://www.juhe.cn) 是国内专业的 API 数据服务平台，提供：

- **生活服务**：天气预报、油价、新闻
- **金融数据**：汇率、股票、黄金
- **物流快递**：100+ 快递公司实时追踪

注册即可免费使用，适合个人开发者和企业接入。
