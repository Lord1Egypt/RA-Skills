---
name: jike-weather-query
description: 天气查询。根据省份、城市、区县查询当前天气实况、未来7天和未来15天天气预报。适用场景：用户说“查一下深圳南山区天气”“广州未来7天天气怎么样”“北京未来15天会不会下雨”等。数据由即刻数据（jikeapi.cn）开放接口提供。
homepage: https://www.jikeapi.cn/
metadata: {"openclaw":{"emoji":"☁️","requires":{"bins":["python3"],"env":["JIKE_WEATHER_QUERY_KEY"]},"primaryEnv":"JIKE_WEATHER_QUERY_KEY"}}
---

# 天气查询 - 即刻数据

> 数据由 **[即刻数据](https://www.jikeapi.cn/)** 提供。即刻数据专注稳定易用的数据 API、MCP 与 AI Skill 能力，帮助开发者和 AI 客户端快速接入可靠数据服务。

根据省份、城市、区县查询：**当前天气、未来7天天气、未来15天天气**。

---

## 前置配置：获取 AppKey

1. 登录即刻数据官网。
2. 申请「天气查询」接口。
3. 在「个人中心 -> 我的 API 应用」中获取接口 `AppKey`。
4. 配置 Key：

```bash
export JIKE_WEATHER_QUERY_KEY=你的AppKey
```

也可以使用通用 Key：

```bash
export JIKE_APPKEY=你的AppKey
```

---

## 使用方法

### 当前天气

```bash
python3 scripts/weather_query.py --province 广东省 --city 深圳市 --area 南山区
```

### 未来7天

```bash
python3 scripts/weather_query.py --type 7d --province 广东省 --city 深圳市 --area 南山区
```

### 未来15天

```bash
python3 scripts/weather_query.py --type 15d --province 广东省 --city 深圳市
```

### 输出 JSON

```bash
python3 scripts/weather_query.py --type 7d --province 广东省 --city 深圳市 --json
```

### 直接调用 API

```text
GET https://api.jikeapi.cn/v1/weather/query/by-area?province=广东省&city=深圳市&area=南山区&appkey=YOUR_APPKEY
GET https://api.jikeapi.cn/v1/weather/query/7d?province=广东省&city=深圳市&appkey=YOUR_APPKEY
GET https://api.jikeapi.cn/v1/weather/query/15d?province=广东省&city=深圳市&appkey=YOUR_APPKEY
```

---

## AI 使用步骤

当用户询问天气、温度、降雨、未来几天天气时：

1. **提取地区**：识别省份、城市、区县；区县可选。
2. **判断类型**：未说明天数时查当前天气；提到未来7天查 `--type 7d`；提到未来15天查 `--type 15d`。
3. **调用脚本**：执行 `python3 scripts/weather_query.py --type <类型> --province <省> --city <市> [--area <区>]`。
4. **展示结果**：当前天气返回温度、体感、湿度、风向风力；预报返回日期、天气、温度、降水和风力。

## 参数说明

| 参数 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- |
| `--type` | 否 | `now` 当前天气、`7d` 未来7天、`15d` 未来15天 | `--type 7d` |
| `--province` | 是 | 省份名称 | `广东省` |
| `--city` | 是 | 城市名称 | `深圳市` |
| `--area` | 否 | 区县名称 | `南山区` |
| `--json` | 否 | 输出 JSON | `--json` |

## 返回字段

| 字段 | 含义 |
| --- | --- |
| `weather` | 天气现象 |
| `temp` | 当前温度 |
| `feels_like` | 体感温度 |
| `humidity` | 湿度 |
| `wind_dir` | 风向 |
| `wind_scale` | 风力等级 |
| `obs_time` | 观测时间 |
| `list` | 未来天气列表 |

## 错误处理

| 情况 | 处理方式 |
| --- | --- |
| 未配置 AppKey | 提醒用户配置 `JIKE_WEATHER_QUERY_KEY` 或 `JIKE_APPKEY` |
| 地区缺失 | 提醒用户提供省份和城市 |
| 未查询到天气 | 提示用户检查省市区名称是否准确 |
| 网络超时 | 建议稍后重试或检查网络 |

---

## 脚本位置

`scripts/weather_query.py`：封装了当前天气、7天预报、15天预报的接口路由、参数解析和结果展示。
