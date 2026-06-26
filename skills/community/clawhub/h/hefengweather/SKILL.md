---
name: 和风天气查询
description: 提供基于和风天气API的全面气象数据查询服务,包括实时天气、多天预报、逐小时预报、空气质量、生活指数、气象预警、天文数据、分钟级降水预报、格点天气和地理信息查询。当用户需要查询天气信息、空气质量、气象预警或天文数据时触发此技能。
author: fengyu
version: 1.0.0
category: weather
tags: [weather, forecast, air-quality, astronomy, qweather]
dependencies: |
  - Python >= 3.11
  - httpx >= 0.25.0
  - python-dotenv >= 1.0.0
  - pyjwt >= 2.8.0 (可选,JWT认证)
  - cryptography >= 41.0.0 (可选,JWT认证)
config:
  always: false
  env:
    required:
      - HEFENG_API_HOST
    optional:
      - HEFENG_API_KEY
      - HEFENG_PROJECT_ID
      - HEFENG_KEY_ID
      - HEFENG_PRIVATE_KEY_PATH
      - HEFENG_PRIVATE_KEY
---

# 和风天气查询 Skill

## 概述

基于和风天气API的气象数据查询服务,提供全面的天气相关数据查询功能,支持实时天气、天气预报、空气质量、生活指数等多种气象数据查询。

## 前置配置

### 1. 获取和风天气API

访问 [和风天气开发者平台](https://dev.qweather.com/) 注册账号并获取API密钥。

### 2. 配置认证信息

**安全警告**：此 skill 需要 API 凭证才能工作。你可以选择以下两种方式配置：

#### 方式一：使用环境变量（推荐，更安全）

```bash
export HEFENG_API_HOST="your-domain.qweatherapi.com"
export HEFENG_API_KEY="your_api_key_here"
```

#### 方式二：使用配置脚本（会保存到文件）

```bash
python scripts/configure.py --api-host "your-domain.qweatherapi.com" --api-key "your_api_key"
```

**注意**：默认情况下，配置脚本会将凭证保存到 `~/.config/qweather/.env`。如果你不希望凭证持久化到磁盘，请使用 `--no-save` 选项：

```bash
python scripts/configure.py --api-host "your-domain.qweatherapi.com" --api-key "your_api_key" --no-save
```

如果你选择保存到文件，建议设置文件权限为 600：

```bash
chmod 600 ~/.config/qweather/.env
```

## 核心功能

### 1. 基础天气查询

#### 实时天气
查询指定城市的当前天气状况。

**触发场景**: 用户询问"今天天气怎么样"、"北京现在天气"、"当前气温"等

**执行脚本**:
```bash
python scripts/weather_now.py --city "北京"
```

**参数**:
- `--city`: 城市名称(如"北京"、"上海")
- `--location`: LocationID或经纬度(可选,与city二选一)
- `--lang`: 语言(默认"zh")
- `--unit`: 单位"m"公制或"i"英制(默认"m")

**返回示例**:
```json
{
  "now": {
    "temp": "18",
    "text": "晴",
    "windDir": "东北风",
    "windScale": "3",
    "humidity": "45"
  }
}
```

#### 天气预报
查询未来3-30天的天气预报。

**触发场景**: 用户询问"明天天气"、"未来一周天气"、"北京7天预报"等

**执行脚本**:
```bash
python scripts/weather.py --city "上海" --days "3d"
```

**参数**:
- `--city`: 城市名称(必需)
- `--days`: 预报天数,支持"3d"(默认)、"7d"、"10d"、"15d"、"30d"

#### 逐小时预报
查询未来24/72/168小时的逐小时天气预报。

**触发场景**: 用户询问"今天下午天气"、"未来24小时天气"、"每小时预报"等

**执行脚本**:
```bash
python scripts/weather_hourly.py --city "北京" --hours "24h"
```

**参数**:
- `--city`: 城市名称
- `--location`: 经纬度坐标(与city二选一)
- `--hours`: 预报小时数,"24h"(默认)、"72h"、"168h"

#### 历史天气
查询最近10天的历史天气数据。

**执行脚本**:
```bash
python scripts/weather_history.py --city "北京" --days 7
```

### 2. 空气质量查询

#### 实时空气质量
查询指定城市的实时空气质量指数(AQI)。

**触发场景**: 用户询问"空气质量怎么样"、"AQI多少"、"PM2.5"等

**执行脚本**:
```bash
python scripts/air_quality.py --city "北京"
```

**参数**:
- `--city`: 城市名称(必需)

#### 空气质量预报
查询逐小时或逐日的空气质量预报。

**执行脚本**:
```bash
# 逐小时预报
python scripts/air_quality_hourly.py --location "39.90,116.40" --hours "24h"

# 逐日预报
python scripts/air_quality_daily.py --location "39.90,116.40" --days "3d"
```

#### 历史空气质量
查询最近10天的历史空气质量数据。

**执行脚本**:
```bash
python scripts/air_quality_history.py --city "北京" --days 7
```

### 3. 生活指数查询

查询天气生活指数,包括运动、洗车、穿衣、感冒、紫外线等16种指数。

**触发场景**: 用户询问"适合运动吗"、"要不要洗车"、"穿什么衣服"等

**执行脚本**:
```bash
python scripts/indices.py --city "上海" --days "1d"
```

**参数**:
- `--city`: 城市名称(必需)
- `--days`: 预报天数,"1d"(默认)或"3d"
- `--types`: 指数类型ID(可选,默认全部16种)

**指数类型**:
- 1:运动指数, 2:洗车指数, 3:穿衣指数, 4:感冒指数, 5:紫外线指数
- 6:旅游指数, 7:花粉过敏指数, 8:舒适度指数, 9:交通指数, 10:防晒指数
- 11:化妆指数, 12:空调开启指数, 13:晾晒指数, 14:钓鱼指数, 15:太阳镜指数
- 16:空气污染扩散条件指数

### 4. 气象预警查询

查询气象灾害预警信息,包括台风、暴雨、高温等预警。

**触发场景**: 用户询问"有预警吗"、"天气预警"、"暴雨预警"等

**执行脚本**:
```bash
python scripts/warning.py --city "杭州"
```

### 5. 天文数据查询

#### 日出日落时间
查询指定地点和日期的日出日落时间。

**触发场景**: 用户询问"几点日出"、"日落时间"、"今天太阳几点下山"等

**执行脚本**:
```bash
python scripts/astronomy_sun.py --location "北京" --date "20251029"
```

**参数**:
- `--location`: 城市名、LocationID或经纬度(必需)
- `--date`: 日期,格式yyyyMMdd(今天到未来60天)

#### 月相数据
查询月升月落时间和24小时月相数据。

**执行脚本**:
```bash
python scripts/astronomy_moon.py --location "上海" --date "20251101"
```

### 6. 分钟级降水预报

查询未来2小时5分钟级的降水预报。

**触发场景**: 用户询问"会下雨吗"、"什么时候下雨"、"接下来两小时天气"等

**执行脚本**:
```bash
python scripts/minutely_5m.py --location "116.38,39.91"
```

### 7. 格点天气查询

提供高分辨率数值模式的格点天气数据(3-5公里分辨率)。

#### 格点实时天气
```bash
python scripts/grid_weather_now.py --location "116.41,39.92"
```

#### 格点每日预报
```bash
python scripts/grid_weather_daily.py --location "116.41,39.92" --days "3d"
```

#### 格点逐小时预报
```bash
python scripts/grid_weather_hourly.py --location "116.41,39.92" --hours "24h"
```

### 8. 地理信息查询

#### 热门城市列表
查询热门城市列表。

**执行脚本**:
```bash
python scripts/top_cities.py --number 10 --city-type "cn"
```

**参数**:
- `--number`: 返回数量,1-100(默认10)
- `--city-type`: 城市类型,"cn"(默认)、"world"、"overseas"

#### POI搜索
搜索兴趣点(景点、潮汐站点等)。

**执行脚本**:
```bash
# 关键词搜索
python scripts/search_poi.py --location "北京" --keyword "故宫" --poi-type "scenic"

# 范围搜索
python scripts/search_poi_range.py --location "116.38,39.91" --poi-type "scenic" --radius 5
```

**POI类型**:
- "scenic": 景点
- "TSTA": 潮汐站点

## 使用流程

1. **识别用户需求**: 根据用户问题判断需要查询的天气信息类型
2. **选择对应脚本**: 根据需求选择相应的Python脚本
3. **构造参数**: 从用户输入提取城市名称、日期等参数
4. **执行脚本**: 运行对应的Python脚本获取数据
5. **格式化输出**: 将返回的JSON数据转换为自然语言回复

## 示例对话

**用户**: 北京今天天气怎么样?

**执行流程**:
1. 识别需求:查询实时天气
2. 执行脚本:`python scripts/weather_now.py --city "北京"`
3. 解析返回数据
4. 生成回复:"北京当前天气晴,温度18°C,东北风3级,湿度45%"

**用户**: 明天上海会下雨吗?

**执行流程**:
1. 识别需求:查询明日天气预报
2. 执行脚本:`python scripts/weather.py --city "上海" --days "3d"`
3. 提取明天的天气数据
4. 生成回复:"根据天气预报,上海明天多云转阴,有阵雨,温度15-22°C"

**用户**: 现在的空气质量怎么样?

**执行流程**:
1. 识别需求:查询空气质量(需先确定城市)
2. 询问用户城市,或使用默认城市
3. 执行脚本:`python scripts/air_quality.py --city "北京"`
4. 生成回复:"当前AQI为65,空气质量良好,PM2.5浓度为45μg/m³"

## 安全注意事项

1. **API 凭证保护**：
   - 不要将 API Key 或私钥提交到版本控制
   - 使用 `--no-save` 选项避免凭证持久化到磁盘
   - 定期轮换 API Key

2. **API 主机验证**：
   - 确保 `HEFENG_API_HOST` 指向官方域名（如 `dev.qweather.com`）
   - 不要将请求发送到不受信任的服务器

3. **文件权限**：
   - 配置文件默认设置权限为 600（仅所有者可读写）
   - 配置文件目录默认设置权限为 700

## 错误处理

- 如果城市名称无效,返回"未找到该城市,请检查城市名称"
- 如果API配置错误,返回"API配置错误,请检查API密钥"
- 如果网络请求失败,返回"网络请求失败,请稍后重试"
- 如果参数错误,返回"参数错误,请检查输入"

## 参考资料

- [和风天气官方文档](https://dev.qweather.com/docs/)
- [和风天气API参考](https://dev.qweather.com/docs/api/)
- 项目仓库: [hefeng-weather-skill](https://github.com/fengyu/hefeng-weather-skill)
