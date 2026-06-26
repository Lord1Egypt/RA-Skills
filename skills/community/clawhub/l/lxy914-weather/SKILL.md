---
name: qweather
description: 和风天气 API 查询服务，支持实时天气、天气预报和小时预报。使用城市名称进行查询。
---

# 和风天气 (QWeather)

和风天气提供详细的天气数据查询服务。

## 前置条件

需要和风天气 API Key：
1. 注册账号：https://dev.qweather.com/
2. 创建应用获取 API Key和API HOST

## 配置信息

设置环境变量：
- `QWEATHER_API_KEY`: 和风天气 API Key
- `QWEATHER_BASE_URL`: API Host（如 `https://xxxxxxxx.re.qweatherapi.com`）

## 使用方法

### 使用 Python 脚本查询

```bash
# 查询实时天气
python scripts/qweather_cli.py now 北京

# 查询天气预报（默认 7 天，支持 3/7/10/15/30 天）
python scripts/qweather_cli.py daily 上海
python scripts/qweather_cli.py daily 太原 3

# 查询小时预报（默认 24 小时）
python scripts/qweather_cli.py hourly 广州
python scripts/qweather_cli.py hourly 深圳 12
```

### 选项

- `--json`: 输出 JSON 格式
- `--plain`: 纯文本模式（不使用 emoji）

## 使用示例

### 查询当前天气
```
"今天天气怎么样？"
"查询上海的实时天气"
"北京现在多少度？"
```

### 查询天气预报
```
"未来 3 天天气如何？"
"太原明天下雨吗？"
"下周天气预报"
```

### 查询小时预报
```
"今天下午天气怎么样？"
"明天每小时天气"
```

## 注意事项

1. 实况数据有 5-20 分钟延迟
2. 免费额度：2000 次/天
